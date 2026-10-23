// Owned fixture with real host erased invocation; no WeChat code is executed.
#include "newsendmsg_body_start_gate_4115.hpp"
#include <cassert>
#include <deque>
#include <future>
#include <iostream>
#include <string>
#include <thread>
#include <vector>

using namespace newsendmsg4115;
void invoke_body(JobBody*) __asm("_probe_job_body_erasure");
struct TypedBodyError { int value; };

int main(int argc, char** argv) {
  const bool keep_owner_alive = argc == 2;
  assert(argc == 1 || (argc == 2 && std::string(argv[1]) == "--owner-alive"));
  bool thread_id_reused = false;
  // 1. Ordinary body reaches the host vslot+0x30 exactly once.
  {
    auto gate = std::make_shared<BodyStartGate>();
    int body_calls = 0;
    auto body = make_start_gated_body(gate, [&] { ++body_calls; });
    invoke_body(&body);
    const auto state = gate->snapshot();
    assert(body_calls == 1 && state.entered && state.left && !state.sent);
    assert(!state.native_cancel_claimed);
  }
  // 2. Pre-entry cancellation must not reach native cancellation/factory.
  // Captured storage remains owned until the queued function is destroyed.
  {
    auto gate = std::make_shared<BodyStartGate>();
    auto marker = std::make_shared<int>(4115);
    std::weak_ptr<int> weak = marker;
    int body_calls = 0, native_calls = 0;
    auto body = make_start_gated_body(gate, [&, marker] {
      assert(*marker == 4115);
      ++body_calls;
    });
    marker.reset();
    assert(gate->cancel_on_executor([&] { ++native_calls; }) ==
           JobCancelAction::deferred_before_body);
    invoke_body(&body);
    assert(body_calls == 0 && native_calls == 0 && !weak.expired());
    const auto state = gate->snapshot();
    assert(state.invoked && !state.entered && state.left && !state.sent);
    body = {};
    assert(weak.expired());
  }
  // 3. Cancellation queued DURING launch can precede the queued first resume.
  // A serial executor alone does not exclude this order. The core/cleanup here
  // is our model; this does not run a native scheduler or prove its full drain.
  {
    auto gate = std::make_shared<BodyStartGate>();
    std::deque<JobBody> queue;
    int body_calls = 0, native_calls = 0, parameter_cleanups = 0;
    auto body = make_start_gated_body(gate, [&] { ++body_calls; });
    queue.push_back([&] {
      assert(gate->cancel_on_executor([&] { ++native_calls; }) ==
             JobCancelAction::deferred_before_body);
    });
    queue.push_back([&] {
      invoke_body(&body);
      ++parameter_cleanups;
    });
    while (!queue.empty()) {
      auto callback = std::move(queue.front());
      queue.pop_front();
      callback();
    }
    assert(body_calls == 0 && native_calls == 0 && parameter_cleanups == 1);
  }
  // 4. Once body entry is observed, reentrant cancellation forwards only once.
  // The separate request cancellation is not performed by the start gate.
  {
    auto gate = std::make_shared<BodyStartGate>();
    int native_calls = 0, request_calls = 0;
    auto body = make_start_gated_body(gate, [&] {
      ++request_calls; // Explicit coordinator-owned request cancellation model.
      assert(gate->cancel_on_executor([&] { ++native_calls; }) ==
             JobCancelAction::forwarded);
      assert(gate->cancel_on_executor([&] { ++native_calls; }) ==
             JobCancelAction::duplicate);
    });
    invoke_body(&body);
    assert(native_calls == 1 && request_calls == 1);
    assert(gate->snapshot().native_cancel_claimed && gate->snapshot().left);
  }
  // 5. Body return does not need another native job cancellation.
  {
    auto gate = std::make_shared<BodyStartGate>();
    int native_calls = 0;
    auto body = make_start_gated_body(gate, [] {});
    invoke_body(&body);
    assert(gate->cancel_on_executor([&] { ++native_calls; }) ==
           JobCancelAction::after_body);
    assert(native_calls == 0 && !gate->snapshot().sent);
  }
  // 6. Foreign-thread body/cancel attempts are rejected before injected code.
  {
    auto gate = std::make_shared<BodyStartGate>();
    int native_calls = 0, body_calls = 0;
    auto body = make_start_gated_body(gate, [&] { ++body_calls; });
    std::vector<std::thread> threads;
    for (int i = 0; i < 32; ++i) threads.emplace_back([&] {
      assert(gate->cancel_on_executor([&] { ++native_calls; }) ==
             JobCancelAction::wrong_executor);
      invoke_body(&body);
    });
    for (auto& thread : threads) thread.join();
    const auto state = gate->snapshot();
    assert(state.wrong_executor && !state.cancel_requested && !state.entered);
    assert(body_calls == 0 && native_calls == 0);
    invoke_body(&body);
    assert(body_calls == 1);
  }
  // 7. The original typed exception crosses the wrapper unchanged.
  {
    auto gate = std::make_shared<BodyStartGate>();
    auto body = make_start_gated_body(gate, [] { throw TypedBodyError{4115}; });
    try { invoke_body(&body); assert(false); }
    catch (const TypedBodyError& error) { assert(error.value == 4115); }
    assert(gate->snapshot().entered && gate->snapshot().left);
  }
  // 8. Throwing cancel control is consumed, never implicitly retried.
  {
    auto gate = std::make_shared<BodyStartGate>();
    int native_calls = 0;
    auto body = make_start_gated_body(gate, [&] {
      gate->cancel_on_executor([&] { ++native_calls; throw 27; });
    });
    try { invoke_body(&body); assert(false); }
    catch (int error) { assert(error == 27); }
    assert(gate->cancel_on_executor([&] { ++native_calls; }) ==
           JobCancelAction::duplicate);
    assert(native_calls == 1 && gate->snapshot().left);
  }
  // 9. A duplicate erased call cannot run the body twice.
  {
    auto gate = std::make_shared<BodyStartGate>();
    int body_calls = 0;
    auto body = make_start_gated_body(gate, [&] { ++body_calls; });
    auto clone = body;
    invoke_body(&body);
    invoke_body(&clone);
    assert(body_calls == 1 && gate->snapshot().duplicate_body);
  }
  // 10. Missing input/control fails without calling anything native.
  {
    auto gate = std::make_shared<BodyStartGate>();
    try { make_start_gated_body({}, [] {}); assert(false); }
    catch (const std::invalid_argument&) {}
    try { make_start_gated_body(gate, {}); assert(false); }
    catch (const std::invalid_argument&) {}
    auto body = make_start_gated_body(gate, [&] {
      assert(gate->cancel_on_executor({}) == JobCancelAction::missing_control);
    });
    invoke_body(&body);
    assert(gate->snapshot().missing_control && !gate->snapshot().native_cancel_claimed);
  }
  // 11. Another thread must not acquire the original admission token. Default
  // mode observes possible ID reuse after exit; --owner-alive guarantees that
  // the original ID is still occupied, covering rejection without ID reuse.
  {
    std::shared_ptr<BodyStartGate> gate;
    std::thread::id retired;
    std::promise<void> ready, release;
    auto released = release.get_future();
    std::thread creator([&] {
      gate = std::make_shared<BodyStartGate>();
      retired = std::this_thread::get_id();
      ready.set_value();
      if (keep_owner_alive) released.wait();
    });
    ready.get_future().wait();
    if (!keep_owner_alive) creator.join();
    int body_calls = 0;
    auto body = make_start_gated_body(gate, [&] { ++body_calls; });
    std::thread replacement([&] {
      thread_id_reused = std::this_thread::get_id() == retired;
      invoke_body(&body);
      assert(gate->cancel_on_executor({}) == JobCancelAction::wrong_executor);
    });
    replacement.join();
    if (keep_owner_alive) {
      release.set_value();
      creator.join();
      assert(!thread_id_reused);
    }
    assert(body_calls == 0 && gate->snapshot().wrong_executor);
  }
  std::cout << "{\"scenarios\":11,\"foreign_threads\":32,\"thread_id_reused\":"
            << (thread_id_reused ? "true" : "false") << ","
               "\"host_erased_abi\":true,"
               "\"target_executed\":false,\"native_send_called\":false,\"sent\":false}\n";
}
