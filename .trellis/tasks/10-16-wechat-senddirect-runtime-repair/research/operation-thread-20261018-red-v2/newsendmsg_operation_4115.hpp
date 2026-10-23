// Research only: dependency-injected operation, with no WeChat loader/addresses.
// The caller must supply a proven native execution context. This file does not
// establish thread affinity, authorize native execution, or permit module unload.
#pragma once
#include "newsendmsg_completion_4115.hpp"
#include "newsendmsg_native_body_4115.hpp"
#include "newsendmsg_native_response_4115.hpp"
#include <chrono>
#include <mutex>
#include <string>
#include <utility>

namespace newsendmsg4115 {
enum class OperationPhase { pending, callback, cancelled, timed_out };
struct OperationSnapshot {
  OperationPhase phase;
  bool callback_observed;
  std::int32_t error_type;
  std::int32_t error_code;
  bool response_copied;
  bool response_copy_failed;
  std::vector<std::byte> response_wire;
  bool sent = false; // Independent delivery evidence remains mandatory.
};
struct OperationState {
  std::mutex mutex;
  OperationSnapshot result{OperationPhase::pending, false, 0, 0, false, false, {}};
};
struct CallbackCapture {
  std::shared_ptr<OperationState> state;
  std::shared_ptr<std::mutex> publication;
  ResponseFunctions response;
  const void* (*response_from_request)(void*);
  // Shared ownership keeps storage alive after the initiating scope returns.
  bool operator()(void* request, std::int32_t type, std::int32_t code) const noexcept {
    // Native 0x30c295c holds this gate across factory and cancellation setup;
    // 0x30c3420 waits before copying response. Prevent early request deletion
    // while factory 0x30c2c1c still reads request+8 after enqueue.
    std::lock_guard<std::mutex> published(*publication);
    std::vector<std::byte> wire;
    bool copied = false, failed = false;
    if (type == 0 && code == 0) {
      try {
        NativeResponse owned(response, response_from_request(request));
        wire = owned.wire(); // Deep copy before OnTaskEnd deletes the request.
        copied = true;
      } catch (...) {
        failed = true; // Never propagate an exception through native dispatch.
      }
    }
    std::lock_guard<std::mutex> lock(state->mutex);
    if (!state->result.callback_observed) {
      auto& result = state->result;
      result.callback_observed = true;
      result.error_type = type;
      result.error_code = code;
      result.response_copied = copied;
      result.response_copy_failed = failed;
      result.response_wire = std::move(wire);
      if (result.phase == OperationPhase::pending)
        result.phase = OperationPhase::callback;
    }
    return true; // Request lifetime belongs to native OnTaskEnd, including errors.
  }
};
static_assert(sizeof(CallbackCapture) > 24); // Native factory uses the heap arm.

struct OperationFunctions {
  BodyFunctions body;
  ResponseFunctions response;
  // Request factory 0x30c2c1c: no hidden result, returns uint32 task id.
  std::uint32_t (*factory)(void*, const void*, const std::string*, const void*, Completion*);
  // Service vslot+0x30: adjusts this to owner, stops and deletes a queued request.
  void (*cancel)(void*, std::uint32_t);
  const void* (*response_from_request)(void*);
};

class ResearchOperation {
 public:
  using Clock = std::chrono::steady_clock;
  ResearchOperation(OperationFunctions functions, void* service, const void* options,
                    const std::string& routing, const void* body, std::size_t size,
                    Clock::time_point deadline)
      : functions_(functions), service_(service), deadline_(deadline),
        state_(std::make_shared<OperationState>()) {
    if (!service || !options || !functions.factory || !functions.cancel ||
        !functions.response_from_request || !functions.response.construct ||
        !functions.response.copy || !functions.response.destroy ||
        !functions.response.initialized || !functions.response.byte_size ||
        !functions.response.serialize_cached || deadline <= Clock::now())
      throw std::invalid_argument("complete operation contract and future deadline required");
    NativeBody owned(functions.body, body, size);
    auto publication = std::make_shared<std::mutex>();
    std::lock_guard<std::mutex> publish_after_factory(*publication);
    Completion completion = CallbackCapture{
        state_, publication, functions.response, functions.response_from_request};
    task_id_ = functions.factory(service, owned.get(), &routing, options, &completion);
    // NativeBody is deep-copied by the factory. Native owns its callback copy.
    // A throwing factory leaves outcome unknown; there is deliberately no retry.
  }
  ResearchOperation(const ResearchOperation&) = delete;
  ResearchOperation& operator=(const ResearchOperation&) = delete;
  ResearchOperation(ResearchOperation&&) = delete;
  ResearchOperation& operator=(ResearchOperation&&) = delete;
  // No implicit native call in the destructor; the external bounded supervisor
  // must drive cancellation in the verified execution context before teardown.
  ~ResearchOperation() = default;

  bool cancel() { return stop(OperationPhase::cancelled); }
  bool expire(Clock::time_point now) {
    return now >= deadline_ ? stop(OperationPhase::timed_out) : false;
  }
  OperationSnapshot snapshot() const {
    std::lock_guard<std::mutex> lock(state_->mutex);
    return state_->result;
  }
  std::uint32_t task_id() const noexcept { return task_id_; }
 private:
  bool stop(OperationPhase phase) {
    // Serialize all cancel invocations; callback uses a separate mutex.
    std::lock_guard<std::mutex> control(control_);
    {
      std::lock_guard<std::mutex> lock(state_->mutex);
      if (state_->result.phase != OperationPhase::pending) return false;
      state_->result.phase = phase;
    }
    // A callback already removed from the native map may arrive after this.
    // It records evidence without replacing this terminal local outcome.
    functions_.cancel(service_, task_id_);
    return true;
  }
  OperationFunctions functions_;
  void* service_;
  Clock::time_point deadline_;
  std::shared_ptr<OperationState> state_;
  std::uint32_t task_id_ = 0;
  std::mutex control_;
};
} // namespace newsendmsg4115
