// Isolated integration fixture. Job/Group/Config below are OUR implementations,
// not recovered native layouts or a verified native scheduler. No target loader.
#define main existing_operation_fixture_main
#include "test_newsendmsg_operation_4115.cpp"
#undef main
#include "newsendmsg_job_abi_4115.hpp"
#include <fstream>
#include <iterator>

namespace newsendmsg4115 {
struct Job {
  JobBody body;
  JobFinished finished;
  bool cancelled = false;
  bool done = false;
};
struct JobGroup { std::vector<std::weak_ptr<Job>> jobs; };
struct JobConfig { unsigned fixture_tag = 4115; };
}
namespace {
unsigned job_stops = 0, launches = 0;
JobHandle fixture_launch(JobGroup* group, const JobConfig* config,
                         JobBody* body, JobFinished* finished) {
  assert(group && config && config->fixture_tag == 4115 && body && finished);
  ++launches;
  auto job = std::make_shared<Job>();
  job->body = std::move(*body);
  job->finished = std::move(*finished);
  group->jobs.push_back(job);
  return job;
}
void stop_fixture_job(const JobHandle& job) {
  if (!job->cancelled) { job->cancelled = true; ++job_stops; }
}
void run_fixture_job(const JobHandle& job) {
  assert(!job->done);
  auto body = std::move(job->body);
  if (!job->cancelled && body) body();
  body = {}; // Match the observed body disposal before the finished callback.
  auto finished = std::move(job->finished);
  if (finished) finished(job->cancelled);
  finished = {};
  job->done = true;
}
struct FlowState {
  std::unique_ptr<ResearchOperation> operation;
  std::exception_ptr failure;
  bool job_finished = false;
  bool job_cancelled = false;
};
// Fixture adapter: wires the EXISTING operation into the verified LaunchJob
// type. Control calls are restricted to this fixture's owner thread. This is
// not a contract for calling the real WeChat group or cancellation services.
struct FixtureFlow {
  std::shared_ptr<FlowState> state = std::make_shared<FlowState>();
  JobHandle job;
  Clock::time_point end;
  const std::thread::id owner = std::this_thread::get_id();
  FixtureFlow(JobGroup& group, const JobConfig& config, Service& service,
              std::string wire, Clock::time_point deadline_value)
      : end(deadline_value) {
    JobBody body = [held = state, &service, wire = std::move(wire), deadline_value] {
      try {
        held->operation = std::make_unique<ResearchOperation>(
            functions, &service, &options, "fixture-route", wire.data(), wire.size(),
            deadline_value);
      } catch (...) { held->failure = std::current_exception(); }
    };
    JobFinished finished = [held = state](bool cancelled) {
      held->job_finished = true;
      held->job_cancelled = cancelled;
    };
    LaunchJob submit = fixture_launch;
    job = submit(&group, &config, &body, &finished);
    assert(job && !body && !finished);
  }
  void stop(bool timeout = false) {
    assert(owner == std::this_thread::get_id());
    stop_fixture_job(job); // This does not delete a queued network request.
    if (state->operation) {
      if (timeout) state->operation->expire(end);
      else state->operation->cancel();
    }
  }
};
void balanced() { assert(bodies == 0 && responses == 0 && requests == 0); }
}
int main(int argc, char** argv) {
  if (argc != 2) return 2;
  std::ifstream input(argv[1], std::ios::binary);
  assert(input);
  const std::string wire{std::istreambuf_iterator<char>(input), {}};
  assert(!wire.empty());
  unsigned cases = 0;
  const JobConfig config{};
  {
    JobGroup group; Service service;
    FixtureFlow flow(group, config, service, wire, deadline());
    assert(factories == 0 && requests == 0);
    run_fixture_job(flow.job);
    assert(flow.state->job_finished && !flow.state->job_cancelled);
    assert(requests == 1 && flow.state->operation);
    assert(flow.state->operation->snapshot().phase == OperationPhase::pending);
    // Job completion precedes request completion; it is not drain or delivery.
    auto request = service.take(flow.state->operation->task_id());
    assert(request->body == wire && request->routing == "fixture-route");
    std::thread callback([owned = std::move(request)]() mutable { finish(std::move(owned)); });
    callback.join();
    auto result = flow.state->operation->snapshot();
    assert(result.callback_observed && result.response_copied && !result.sent);
    balanced(); ++cases;
  }
  {
    JobGroup group; Service service;
    const auto before = factories.load();
    FixtureFlow flow(group, config, service, wire, deadline());
    flow.stop(); flow.stop();
    run_fixture_job(flow.job);
    assert(flow.state->job_finished && flow.state->job_cancelled);
    assert(!flow.state->operation && factories == before);
    balanced(); ++cases;
  }
  {
    JobGroup group; Service service;
    FixtureFlow flow(group, config, service, wire, deadline());
    run_fixture_job(flow.job);
    const auto before = cancels.load();
    flow.stop(); flow.stop();
    assert(cancels == before + 1 && requests == 0);
    assert(flow.state->operation->snapshot().phase == OperationPhase::cancelled);
    balanced(); ++cases;
  }
  for (bool timeout : {false, true}) {
    JobGroup group; Service service;
    FixtureFlow flow(group, config, service, wire, deadline());
    run_fixture_job(flow.job);
    auto detached = service.take(flow.state->operation->task_id());
    flow.stop(timeout);
    assert(requests == 1); // Request already belongs to the callback side.
    std::thread callback([owned = std::move(detached)]() mutable { finish(std::move(owned)); });
    callback.join();
    auto result = flow.state->operation->snapshot();
    assert(result.phase == (timeout ? OperationPhase::timed_out : OperationPhase::cancelled));
    assert(result.callback_observed && result.response_copied && !result.sent);
    balanced(); ++cases;
  }
  {
    JobGroup group; Service service;
    const auto before = factories.load();
    FixtureFlow flow(group, config, service, wire, Clock::now());
    run_fixture_job(flow.job);
    assert(flow.state->job_finished && flow.state->failure);
    assert(!flow.state->operation && factories == before);
    balanced(); ++cases;
  }
  {
    JobGroup group; Service service;
    const auto before = factories.load();
    reject_body = true;
    FixtureFlow flow(group, config, service, wire, deadline());
    run_fixture_job(flow.job);
    reject_body = false;
    assert(flow.state->job_finished && flow.state->failure);
    assert(!flow.state->operation && factories == before);
    balanced(); ++cases;
  }
  {
    JobGroup group; Service service;
    const auto before = factories.load();
    throw_factory = true;
    FixtureFlow flow(group, config, service, wire, deadline());
    run_fixture_job(flow.job);
    throw_factory = false;
    assert(flow.state->failure && factories == before + 1);
    assert(!flow.state->operation); // No retry on an unknown factory outcome.
    balanced(); ++cases;
  }
  {
    JobGroup group; Service service;
    std::weak_ptr<FlowState> flow_state;
    std::uint32_t id = 0;
    {
      FixtureFlow flow(group, config, service, wire, deadline());
      flow_state = flow.state;
      run_fixture_job(flow.job);
      id = flow.state->operation->task_id();
    }
    assert(flow_state.expired() && !service.last_state.expired() && requests == 1);
    // The request's copied completion owns OperationState after both handles die.
    finish(service.take(id));
    assert(service.last_state.expired());
    balanced(); ++cases;
  }
  // Explicitly demonstrate why cancelling just the job is insufficient.
  {
    JobGroup group; Service service;
    FixtureFlow flow(group, config, service, wire, deadline());
    run_fixture_job(flow.job);
    const auto before = cancels.load();
    stop_fixture_job(flow.job);
    assert(cancels == before && requests == 1);
    assert(flow.state->operation->snapshot().phase == OperationPhase::pending);
    flow.stop();
    assert(cancels == before + 1);
    balanced(); ++cases;
  }
  balanced();
  assert(cases == 10 && launches == 10 && job_stops == 5);
  std::cout << "{\"cases\":10,\"job_completion_is_not_request_drain\":true,"
               "\"job_cancel_is_not_request_cancel\":true,"
               "\"late_callback_preserves_terminal_state\":true,"
               "\"owned_wire_matches_factory_copy\":true,"
               "\"balanced_lifetime\":true,\"wechat_loaded\":false,\"sent\":false}\n";
}
