// Owned component integration only; no target library or native scheduler.
#define main existing_operation_fixture_main
#include "test_newsendmsg_operation_4115.cpp"
#undef main
#include "newsendmsg_body_start_gate_4115.hpp"

void invoke_start_gated_body(JobBody*) __asm("_probe_job_body_erasure");

int main() {
  unsigned scenarios = 0;
  // Before entry, no factory/request exists; normal wrapper disposal owns release.
  {
    Service service;
    auto gate = std::make_shared<BodyStartGate>();
    std::unique_ptr<ResearchOperation> operation;
    unsigned job_cancel_calls = 0;
    const auto before = factories.load();
    auto body = make_start_gated_body(gate, [&] {
      operation = std::make_unique<ResearchOperation>(
          functions, &service, &options, "route", "text", 4, deadline());
    });
    assert(gate->cancel_on_executor([&] { ++job_cancel_calls; }) ==
           JobCancelAction::deferred_before_body);
    invoke_start_gated_body(&body);
    assert(!operation && factories == before && job_cancel_calls == 0);
    assert(requests == 0 && !gate->snapshot().sent);
    ++scenarios;
  }
  // Entered body: job cancel and request cancel are separately driven controls.
  // Native map-removal ordering is modeled by the existing owned Service.
  for (bool completion_already_removed : {false, true}) {
    Service service;
    auto gate = std::make_shared<BodyStartGate>();
    std::unique_ptr<ResearchOperation> operation;
    std::unique_ptr<Request> detached;
    unsigned job_cancel_calls = 0;
    const auto before = cancels.load();
    auto body = make_start_gated_body(gate, [&] {
      operation = std::make_unique<ResearchOperation>(
          functions, &service, &options, "route", "text", 4, deadline());
      if (completion_already_removed) detached = service.take(operation->task_id());
      assert(operation->cancel());
      assert(gate->cancel_on_executor([&] { ++job_cancel_calls; }) ==
             JobCancelAction::forwarded);
    });
    invoke_start_gated_body(&body);
    assert(job_cancel_calls == 1 && cancels == before + 1);
    assert(operation->snapshot().phase == OperationPhase::cancelled);
    assert(requests == (completion_already_removed ? 1u : 0u));
    if (detached) finish(std::move(detached));
    const auto state = operation->snapshot();
    assert(state.callback_observed == completion_already_removed);
    assert(state.response_copied == completion_already_removed);
    assert(state.phase == OperationPhase::cancelled && !state.sent);
    assert(!operation->cancel());
    assert(gate->cancel_on_executor([&] { ++job_cancel_calls; }) ==
           JobCancelAction::duplicate);
    body = {};
    operation.reset();
    assert(service.last_state.expired() && requests == 0);
    ++scenarios;
  }
  // After the body is gone, independent request timeout still reaches its control.
  {
    Service service;
    auto gate = std::make_shared<BodyStartGate>();
    std::unique_ptr<ResearchOperation> operation;
    const auto end = deadline();
    auto body = make_start_gated_body(gate, [&] {
      operation = std::make_unique<ResearchOperation>(
          functions, &service, &options, "route", "text", 4, end);
    });
    invoke_start_gated_body(&body);
    body = {};
    auto detached = service.take(operation->task_id());
    unsigned job_cancel_calls = 0;
    assert(gate->cancel_on_executor([&] { ++job_cancel_calls; }) ==
           JobCancelAction::after_body);
    assert(operation->expire(end) && job_cancel_calls == 0);
    finish(std::move(detached));
    const auto state = operation->snapshot();
    assert(state.phase == OperationPhase::timed_out && state.callback_observed);
    assert(state.response_copied && !state.sent);
    operation.reset();
    assert(service.last_state.expired());
    ++scenarios;
  }
  assert(bodies == 0 && requests == 0 && responses == 0);
  std::cout << "{\"scenarios\":" << scenarios << ",\"real_operation_component\":true,"
               "\"host_erased_abi\":true,\"balanced_lifetime\":true,"
               "\"native_scheduler_executed\":false,\"target_executed\":false,\"sent\":false}\n";
}
