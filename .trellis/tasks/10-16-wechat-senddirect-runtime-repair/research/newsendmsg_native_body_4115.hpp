// Research only; callers inject functions. No loader or WeChat process access.
#pragma once
#include <array>
#include <cstddef>
#include <cstdint>
#include <stdexcept>

namespace newsendmsg4115 {
struct BodyFunctions {
  // Frozen native entries: ctor 0x465bdac, ParseFromArray 0x5ab3ab8,
  // non-deleting destructor 0x465d634. Addresses are evidence, never resolved here.
  void (*construct)(void*);
  bool (*parse)(void*, const void*, std::int32_t);
  void (*destroy)(void*);
};

class NativeBody {
 public:
  NativeBody(BodyFunctions functions, const void* bytes, std::size_t size)
      : functions_(functions) {
    if (!functions.construct || !functions.parse || !functions.destroy)
      throw std::invalid_argument("complete native body functions are required");
    if (!bytes || size == 0 || size > 16U * 1024U * 1024U)
      throw std::invalid_argument("body violates local input bound");
    functions_.construct(storage_.data());
    try {
      if (!functions_.parse(storage_.data(), bytes, static_cast<std::int32_t>(size)))
        throw std::runtime_error("native protobuf parse/initialization failed");
    } catch (...) {
      functions_.destroy(storage_.data());
      throw;
    }
  }
  ~NativeBody() noexcept { functions_.destroy(storage_.data()); }
  NativeBody(const NativeBody&) = delete;
  NativeBody& operator=(const NativeBody&) = delete;
  NativeBody(NativeBody&&) = delete;
  NativeBody& operator=(NativeBody&&) = delete;
  const void* get() const noexcept { return storage_.data(); }
 private:
  BodyFunctions functions_;
  alignas(8) std::array<std::byte, 48> storage_{};
};
} // namespace newsendmsg4115
