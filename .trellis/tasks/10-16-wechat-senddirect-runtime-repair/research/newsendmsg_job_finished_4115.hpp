// Research only: protect AI-owned final notifications from escaping native dispatch.
// No loader, addresses, native calls, scheduler, implicit cancellation or send gate.
#pragma once
#include "newsendmsg_job_abi_4115.hpp"
#include <atomic>
#include <exception>
#include <stdexcept>
#include <utility>

namespace newsendmsg4115 {
struct FinishedFailureSnapshot {
  bool failure_observed;
  bool exception_available;
  std::exception_ptr exception;
  bool sent = false;
};

class FinishedFailureState {
 public:
  void record(std::exception_ptr error) noexcept {
    unsigned expected = 0;
    if (!phase_.compare_exchange_strong(expected, 1, std::memory_order_acq_rel))
      return;
    exception_ = std::move(error);
    phase_.store(2, std::memory_order_release);
  }
  FinishedFailureSnapshot snapshot() const noexcept {
    const unsigned phase = phase_.load(std::memory_order_acquire);
    if (phase != 2) return {phase != 0, false, {}};
    return {true, true, exception_};
  }
 private:
  std::atomic<unsigned> phase_{0};
  std::exception_ptr exception_;
};

struct GuardedJobFinished {
  std::shared_ptr<FinishedFailureState> state;
  JobFinished notification;
  void operator()(bool native_cancelled) const noexcept {
    try {
      notification(native_cancelled);
    } catch (...) {
      state->record(std::current_exception());
    }
  }
};

inline JobFinished make_guarded_job_finished(
    std::shared_ptr<FinishedFailureState> state, JobFinished notification) {
  if (!state || !notification)
    throw std::invalid_argument("owned state and nonempty final notification required");
  return GuardedJobFinished{std::move(state), std::move(notification)};
}
// This wrapper is only for an owned final notification that makes no native calls.
// Do not use catch-all around JobBody: preserve its two native typed handlers.
// Captured objects must have nonthrowing destructors and must not
// strongly retain their own native Job. Snapshot/return never proves full drain.
} // namespace newsendmsg4115
