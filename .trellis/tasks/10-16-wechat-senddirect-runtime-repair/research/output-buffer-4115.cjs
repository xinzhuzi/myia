'use strict';

// Offline prototype only: no hooks, attachment, task creation or module discovery.
// Caller must supply the actual x4 output from dispatcher 0x5971c24 and prove
// task/callback ownership. A plausible memory layout is NOT a type proof.
const CONTRACT = Object.freeze({
  arm64Sha256: '6a5bd0cbb39ad3092c15e9debda2db4969eedf1b58caad244d88033a996833a7',
  dispatcher: 0x5971c24,
  outputArgument: 4,
  reserve: 0x5ded3c4, // void (AutoBuffer*, size_t), native __FitSize
  pointerAtOffset: 0x56300b4, // void* (AutoBuffer*, size_t)
  position: 0x08,
  length: 0x10,
  capacity: 0x18,
  mallocUnit: 0x20,
  maxLength: 0x3200000, // native __FitSize assertion: <= 50 MiB
});

function sizeField(buffer, offset) {
  const value = buffer.add(offset).readU64().toNumber();
  if (!Number.isSafeInteger(value) || value < 0) {
    throw new Error('invalid AutoBuffer integer');
  }
  return value;
}

function bufferState(buffer) {
  if (buffer.isNull()) throw new Error('null output buffer');
  const position = sizeField(buffer, CONTRACT.position);
  const length = sizeField(buffer, CONTRACT.length);
  const capacity = sizeField(buffer, CONTRACT.capacity);
  const unit = sizeField(buffer, CONTRACT.mallocUnit);
  if (position > length || length > capacity || capacity > CONTRACT.maxLength ||
      unit === 0 || unit > CONTRACT.maxLength) {
    throw new Error('invalid AutoBuffer state');
  }
  return { position, length, capacity };
}

function createBufferWriter({ reserve, pointerAtOffset }) {
  if (typeof reserve !== 'function' || typeof pointerAtOffset !== 'function') {
    throw new TypeError('verified native buffer helpers required');
  }
  return function writeSerialized(output, payload) {
    if (!(payload instanceof Uint8Array) || payload.byteLength === 0 ||
        payload.byteLength > CONTRACT.maxLength) {
      throw new TypeError('nonempty serialized protobuf bytes required');
    }
    // Validate before touching native memory. Never overwrite a protobuf object
    // as a buffer and never call an action-code accessor as a serializer.
    bufferState(output);
    try {
      // AllocWrite adds position and only grows length; __FitSize reserves
      // capacity without those side effects, allowing exact replacement.
      reserve(output, payload.byteLength);
      const capacity = sizeField(output, CONTRACT.capacity);
      const destination = pointerAtOffset(output, 0);
      if (capacity < payload.byteLength || destination.isNull()) {
        throw new Error('native buffer allocation failed');
      }
      destination.writeByteArray(payload.buffer.slice(
        payload.byteOffset, payload.byteOffset + payload.byteLength,
      ));
      output.add(CONTRACT.position).writeU64(0);
      output.add(CONTRACT.length).writeU64(payload.byteLength);
      bufferState(output);
      // This is serialization evidence, never a send acknowledgement.
      return { serialized: true, bytesWritten: payload.byteLength, sent: false };
    } catch (error) {
      // A failed/partial copy must not expose old or partial bytes as a request.
      // Ownership stays with the native AutoBuffer; never free its pointer.
      output.add(CONTRACT.position).writeU64(0);
      output.add(CONTRACT.length).writeU64(0);
      throw error;
    }
  };
}

module.exports = Object.freeze({ CONTRACT, createBufferWriter });
