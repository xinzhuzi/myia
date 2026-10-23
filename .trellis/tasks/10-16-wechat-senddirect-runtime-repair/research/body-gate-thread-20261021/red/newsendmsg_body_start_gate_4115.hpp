// Research component only: no native addresses, loader, executor or send calls.
#pragma once
#include "newsendmsg_job_abi_4115.hpp"
#include <memory>
#include <mutex>
#include <stdexcept>
#include <thread>
#include <utility>

namespace newsendmsg4115 {
enum class BodyAdmission { run, skip_cancelled, reject };
enum class JobCancelAction {
  deferred_before_body, forwarded, after_body, duplicate, wrong_executor,
  missing_control
};
struct BodyStartSnapshot {
  bool invoked = false;
  bool entered = false;
  bool left = false;
  bool cancel_requested = false;
  bool native_cancel_claimed = false;
  bool wrong_executor = false;
  bool duplicate_body = false;
  bool missing_control = false;
  bool sent = false;
};

// Construct on the selected executor. Every body/cancel entry must use that
// same thread; this guard does not itself schedule anything or own the Job.
class BodyStartGate {
 public:
  BodyStartGate() : owner_(current_executor_thread()) {}
  BodyAdmission admit() {
    std::lock_guard<std::mutex> lock(mutex_);
    if (!on_owner()) return BodyAdmission::reject;
    if (state_.invoked) {
      state_.duplicate_body = true;
      return BodyAdmission::reject;
    }
    state_.invoked = true;
    if (state_.cancel_requested) {
      state_.left = true;
      return BodyAdmission::skip_cancelled;
    }
    state_.entered = true;
    return BodyAdmission::run;
  }
  void leave() noexcept {
    std::lock_guard<std::mutex> lock(mutex_);
    state_.left = true;
  }
  JobCancelAction cancel_on_executor(const std::function<void()>& cancel_job) {
    {
      std::lock_guard<std::mutex> lock(mutex_);
      if (!on_owner()) return JobCancelAction::wrong_executor;
      if (state_.cancel_requested) return JobCancelAction::duplicate;
      state_.cancel_requested = true;
      // Never invoke native core cancellation while its initial state can be 0.
      // Returning normally from a skipped body preserves native parameter cleanup.
      if (!state_.entered) return JobCancelAction::deferred_before_body;
      if (state_.left) return JobCancelAction::after_body;
      if (!cancel_job) {
        state_.missing_control = true;
        return JobCancelAction::missing_control;
      }
      state_.native_cancel_claimed = true;
    }
    // Do not hold our mutex across native/reentrant code. An exception is not
    // swallowed and the first claim remains consumed; no automatic retry.
    cancel_job();
    return JobCancelAction::forwarded;
  }
  BodyStartSnapshot snapshot() const {
    std::lock_guard<std::mutex> lock(mutex_);
    return state_;
  }
 private:
  static std::shared_ptr<const std::thread::id> current_executor_thread() {
    // Keep the original thread's identity object alive after it exits. The
    // implementation may recycle std::thread::id values for a later thread;
    // it cannot recycle this still-owned token.
    thread_local const auto identity =
        std::make_shared<const std::thread::id>(std::this_thread::get_id());
    return identity;
  }
  bool on_owner() {
    if (owner_ == current_executor_thread()) return true;
    state_.wrong_executor = true;
    return false;
  }
  const std::shared_ptr<const std::thread::id> owner_;
  mutable std::mutex mutex_;
  BodyStartSnapshot state_;
};
struct StartedBodyScope {
  std::shared_ptr<BodyStartGate> gate;
  ~StartedBodyScope() { gate->leave(); }
};
inline JobBody make_start_gated_body(std::shared_ptr<BodyStartGate> gate, JobBody body) {
  if (!gate || !body)
    throw std::invalid_argument("owned start gate and nonempty body required");
  return [gate = std::move(gate), body = std::move(body)] {
    if (gate->admit() != BodyAdmission::run) return;
    StartedBodyScope scope{gate};
    // Preserve the original exception type for the native JobBody handlers.
    body();
  };
}
// The coordinator must separately cancel the network request (service/task_id).
// Neither this snapshot nor a body return proves queue/request/callback drain.
// Gate/body captures must not strongly retain their own native Job.
} // namespace newsendmsg4115
