'use strict';
const assert = require('node:assert/strict');
const { test } = require('node:test');
const { CONTRACT, createBufferWriter } = require('./output-buffer-4115.cjs');

function fixture({ capacity = 8, length = 3, position = 2 } = {}) {
  const header = Buffer.alloc(56, 0xa5);
  const writes = [];
  const calls = [];
  let data = Buffer.alloc(capacity + 16, 0xa5);
  const field = (offset, value) => header.writeBigUInt64LE(BigInt(value), 8 + offset);
  field(0, capacity ? 0x1000 : 0);
  field(8, position); field(16, length); field(24, capacity); field(32, 8);
  class Pointer {
    constructor(offset = 0) { this.offset = offset; }
    isNull() { return false; }
    add(offset) { return new Pointer(this.offset + offset); }
    readU64() {
      const n = header.readBigUInt64LE(8 + this.offset);
      return { toNumber: () => Number(n) };
    }
    writeU64(n) { writes.push(this.offset); field(this.offset, n); }
  }
  const output = new Pointer();
  const helpers = {
    reserve(pointer, size) {
      assert.equal(pointer, output);
      calls.push('reserve');
      const before = Number(header.readBigUInt64LE(32));
      if (size > before) {
        const next = Math.ceil(size / 8) * 8;
        const resized = Buffer.alloc(next + 16, 0xa5);
        data.copy(resized, 8, 8, 8 + before);
        data = resized;
        field(0, 0x2000); field(24, next);
      }
    },
    pointerAtOffset(pointer, offset) {
      assert.equal(pointer, output); assert.equal(offset, 0);
      calls.push('pointerAtOffset');
      return { isNull: () => false, writeByteArray: bytes => {
        const source = Buffer.from(bytes);
        source.copy(data, 8);
      } };
    },
  };
  return { header, output, helpers, writes, calls, field, data: () => data,
    length: () => Number(header.readBigUInt64LE(24)),
    guards: () => {
      assert.deepEqual(header.subarray(0, 8), Buffer.alloc(8, 0xa5));
      assert.deepEqual(header.subarray(48), Buffer.alloc(8, 0xa5));
      assert.deepEqual(data.subarray(0, 8), Buffer.alloc(8, 0xa5));
      assert.deepEqual(data.subarray(-8), Buffer.alloc(8, 0xa5));
    },
  };
}

for (const text of ['你好，微信', 'long body '.repeat(100), 'a', 'with\u0000binary']) {
  test('exact bytes and length: ' + text.length, () => {
    const f = fixture();
    const payload = new TextEncoder().encode(text);
    const result = createBufferWriter(f.helpers)(f.output, payload);
    assert.deepEqual(result, { serialized: true, bytesWritten: payload.length, sent: false });
    assert.deepEqual(f.data().subarray(8, 8 + payload.length), Buffer.from(payload));
    assert.equal(f.length(), payload.length);
    assert.deepEqual(f.writes, [8, 16]);
    assert.deepEqual(f.calls, ['reserve', 'pointerAtOffset']);
    f.guards();
  });
}

test('multiple overwrites shrink length and keep native ownership', () => {
  const f = fixture({ capacity: 0, length: 0, position: 0 });
  const write = createBufferWriter(f.helpers);
  for (const text of ['a'.repeat(256), '短', 'b'.repeat(513), 'z']) {
    const bytes = new TextEncoder().encode(text);
    write(f.output, bytes);
    assert.equal(f.length(), bytes.length);
    assert.deepEqual(f.data().subarray(8, 8 + bytes.length), Buffer.from(bytes));
    f.guards();
  }
});

test('Uint8Array view does not leak bytes outside its slice', () => {
  const f = fixture();
  createBufferWriter(f.helpers)(f.output, new Uint8Array([1, 2, 3, 4]).subarray(1, 3));
  assert.deepEqual(f.data().subarray(8, 10), Buffer.from([2, 3]));
  assert.equal(f.length(), 2);
});

test('partial copy failure clears request length and propagates error', () => {
  const f = fixture();
  f.helpers.pointerAtOffset = () => ({ isNull: () => false, writeByteArray: () => {
    f.data()[8] = 0xff; throw new Error('partial write');
  } });
  assert.throws(() => createBufferWriter(f.helpers)(f.output, new Uint8Array([1, 2])), /partial write/);
  assert.equal(f.length(), 0);
  assert.equal(f.header.readBigUInt64LE(16), 0n);
  f.guards();
});

test('native allocation failure cannot report serialization success', () => {
  const f = fixture();
  f.helpers.reserve = () => { f.field(0, 0); f.field(24, 0); };
  f.helpers.pointerAtOffset = () => ({ isNull: () => true });
  assert.throws(() => createBufferWriter(f.helpers)(f.output, new Uint8Array([1, 2])), /allocation failed/);
  assert.equal(f.length(), 0);
  f.guards();
});

for (const [offset, value] of [[8, 9], [16, 9], [32, 0], [24, 2n ** 63n]]) {
  test('invalid object rejected before native call: field ' + offset, () => {
    const f = fixture(); f.field(offset, value);
    const before = Buffer.from(f.header);
    assert.throws(() => createBufferWriter(f.helpers)(f.output, new Uint8Array([1])));
    assert.deepEqual(f.header, before);
    assert.deepEqual(f.calls, []);
    assert.deepEqual(f.writes, []);
  });
}

test('invalid payload has zero memory effects', () => {
  const f = fixture();
  const write = createBufferWriter(f.helpers);
  for (const value of [null, 'text', [1, 2], new Uint8Array()]) {
    assert.throws(() => write(f.output, value), /serialized protobuf bytes/);
  }
  assert.deepEqual(f.writes, []); assert.deepEqual(f.calls, []);
});

test('contract keeps output argument and full five-field native layout', () => {
  assert.equal(CONTRACT.outputArgument, 4);
  assert.equal(CONTRACT.mallocUnit, 0x20);
  assert.equal(CONTRACT.reserve, 0x5ded3c4);
});
