// Research only. Injected functions; no loader, debugger or process access.
#pragma once
#include <array>
#include <cstddef>
#include <cstdint>
#include <stdexcept>
#include <vector>

namespace newsendmsg4115 {
struct ResponseFunctions {
  // Frozen entries: ctor 0x465bdcc, copy 0x465f460, dtor 0x465ed38,
  // initialized 0x465f4a0, ByteSize 0x465f354, cached array writer 0x5ab3bc0.
  // The array writer consumes cached sizes; ByteSize MUST run first.
  void (*construct)(void*);
  void (*copy)(void*, const void*);
  void (*destroy)(void*);
  bool (*initialized)(const void*);
  std::int32_t (*byte_size)(void*);
  std::byte* (*serialize_cached)(const void*, std::byte*);
};

class NativeResponse {
 public:
  NativeResponse(ResponseFunctions functions, const void* source)
      : functions_(functions) {
    if (!source || !functions.construct || !functions.copy || !functions.destroy ||
        !functions.initialized || !functions.byte_size || !functions.serialize_cached)
      throw std::invalid_argument("complete response functions and source required");
    functions_.construct(storage_.data());
    try {
      functions_.copy(storage_.data(), source);
    } catch (...) {
      functions_.destroy(storage_.data());
      throw;
    }
  }
  ~NativeResponse() noexcept { functions_.destroy(storage_.data()); }
  NativeResponse(const NativeResponse&) = delete;
  NativeResponse& operator=(const NativeResponse&) = delete;
  NativeResponse(NativeResponse&&) = delete;
  NativeResponse& operator=(NativeResponse&&) = delete;

  std::vector<std::byte> wire() {
    if (!functions_.initialized(storage_.data()))
      throw std::runtime_error("native response is missing required fields");
    const std::int32_t size = functions_.byte_size(storage_.data());
    if (size <= 0 || size > 16 * 1024 * 1024)
      throw std::runtime_error("native response violates local size bound");
    std::vector<std::byte> result(static_cast<std::size_t>(size));
    if (functions_.serialize_cached(storage_.data(), result.data()) != result.data() + size)
      throw std::runtime_error("native response serialized length mismatch");
    return result;
  }
 private:
  ResponseFunctions functions_;
  alignas(8) std::array<std::byte, 56> storage_{};
};
} // namespace newsendmsg4115
