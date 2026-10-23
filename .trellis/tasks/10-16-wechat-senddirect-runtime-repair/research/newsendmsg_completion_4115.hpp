// Research only: no loader, debugger, WeChat addresses or native invocations.
#pragma once
#include <array>
#include <atomic>
#include <cstdint>
#include <functional>
#include <memory>
#include <stdexcept>

namespace newsendmsg4115 {
struct CompletionResult {
  bool received;
  std::int32_t error_type;
  std::int32_t error_code;
  bool sent; // A callback alone cannot establish delivery.
};

class CompletionState {
 public:
  bool record(std::int32_t type, std::int32_t code) noexcept {
    unsigned expected = 0;
    if (!phase_.compare_exchange_strong(expected, 1, std::memory_order_relaxed))
      return false;
    error_type_ = type;
    error_code_ = code;
    phase_.store(2, std::memory_order_release);
    return true;
  }
  CompletionResult snapshot() const noexcept {
    if (phase_.load(std::memory_order_acquire) != 2)
      return {false, 0, 0, false};
    return {true, error_type_, error_code_, false};
  }
 private:
  std::atomic<unsigned> phase_{0};
  std::int32_t error_type_ = 0;
  std::int32_t error_code_ = 0;
};

// OnTaskEnd supplies addresses of its request pointer and two int32 locals.
// libc++ forwards by reference inside its erased virtual operator().
using Completion = std::function<bool(void*, std::int32_t, std::int32_t)>;
static_assert(sizeof(Completion) == 32 && alignof(Completion) == 8);

struct OwnedCompletion {
  std::shared_ptr<CompletionState> state;
  // Force heap storage: erased functor exceeds the native 24-byte inline area.
  std::array<std::uintptr_t, 2> storage_padding{};
  bool operator()(void*, std::int32_t type, std::int32_t code) const noexcept {
    state->record(type, code);
    // Native OnTaskEnd owns and destroys the request after this returns true.
    // Do not retain/dereference its request pointer or destroy it here.
    return true;
  }
};
static_assert(sizeof(OwnedCompletion) > 24);
inline Completion make_completion(const std::shared_ptr<CompletionState>& state) {
  if (!state) throw std::invalid_argument("completion state is required");
  return OwnedCompletion{state, {}};
}
} // namespace newsendmsg4115
