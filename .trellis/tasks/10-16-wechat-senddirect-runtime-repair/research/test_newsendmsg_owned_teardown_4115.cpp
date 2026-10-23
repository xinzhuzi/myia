// Owned operation integration for the recovered normal job/core ownership path.
// These are fixture layouts, never native offsets, loaders, or executors.
#define main existing_operation_fixture_main
#include "test_newsendmsg_operation_4115.cpp"
#undef main
#include <algorithm>
#include <functional>
#include <vector>

namespace {
struct TeardownCounts {
  unsigned jobs = 0, cores = 0, contexts = 0;
  bool final_returned = false, group_removed = false, core_done = false;
  std::uint32_t task_id = 0;
  std::vector<std::string> events;
};
struct OwnedCore;
struct OwnedGroup;
struct OwnedContext {
  TeardownCounts& counts;
  std::unique_ptr<ResearchOperation> operation;
  explicit OwnedContext(TeardownCounts& c) : counts(c) {}
  ~OwnedContext() { ++counts.contexts; counts.events.push_back("context_destroyed"); }
};
struct OwnedJob {
  TeardownCounts& counts;
  OwnedGroup& group;
  std::shared_ptr<OwnedCore> core;
  std::function<void()> body;
  std::function<void(bool)> finished;
  OwnedJob(TeardownCounts& c, OwnedGroup& g) : counts(c), group(g) {}
  ~OwnedJob() {
    assert(counts.final_returned && counts.group_removed);
    ++counts.jobs;
    counts.events.push_back("job_destroyed");
  }
  void run();
};
struct OwnedGroup {
  std::vector<std::shared_ptr<OwnedJob>> held;
  void completed(OwnedJob* job) {
    held.erase(std::remove_if(held.begin(), held.end(),
                             [job](const auto& entry) { return entry.get() == job; }), held.end());
    job->counts.group_removed = true;
    job->counts.events.push_back("group_removed");
  }
};
struct OwnedCore {
  TeardownCounts& counts;
  std::shared_ptr<OwnedJob> argument;
  explicit OwnedCore(TeardownCounts& c) : counts(c) {}
  ~OwnedCore() { assert(!argument && counts.core_done); ++counts.cores; }
  void run() {
    assert(argument);
    argument->run();
    assert(counts.final_returned);
    // Core keeps itself alive through the executor closure while this breaks
    // the job->core->argument->job cycle. No local shared Job copy is retained.
    argument.reset();
    counts.events.push_back("argument_released");
    counts.core_done = true;
  }
};
void OwnedJob::run() {
  auto task = std::move(body);
  body = {};
  assert(task);
  task();
  task = {};
  counts.events.push_back("result_published");
  group.completed(this); // The observed group registration has no executor.
  assert(counts.group_removed);
  finished(false);
  assert(counts.final_returned);
  // Final function remains stored here until Job destruction.
}
void exercise(bool keep_external_job) {
  TeardownCounts counts;
  OwnedGroup group;
  Service service;
  auto context = std::make_shared<OwnedContext>(counts);
  std::weak_ptr<OwnedContext> weak_context = context;
  auto job = std::make_shared<OwnedJob>(counts, group);
  std::weak_ptr<OwnedJob> weak_job = job;
  job->core = std::make_shared<OwnedCore>(counts);
  std::weak_ptr<OwnedCore> weak_core = job->core;
  job->core->argument = job;
  job->body = [held = context, &service, &counts] {
    constexpr char bytes[] = "owned teardown";
    held->operation = std::make_unique<ResearchOperation>(
        functions, &service, &options, "fixture-route", bytes, sizeof(bytes)-1, deadline());
    counts.task_id = held->operation->task_id();
  };
  job->finished = [held = context, &counts](bool cancelled) {
    assert(!cancelled && held->operation && counts.group_removed);
    assert(held->operation->snapshot().phase == OperationPhase::pending);
    counts.final_returned = true;
    counts.events.push_back("final_returned");
  };
  context.reset();
  group.held.push_back(job);
  std::vector<std::function<void()>> executor;
  executor.emplace_back([core = job->core] { core->run(); });
  if (!keep_external_job) job.reset();
  assert(!weak_job.expired() && !weak_context.expired() && !weak_core.expired());
  std::thread worker([&] { executor.front()(); });
  worker.join();
  assert(group.held.empty() && counts.core_done && counts.final_returned);
  assert(requests == 1 && bodies == 0 && responses == 0);
  assert(!service.last_state.expired()); // Independent native-response capture.
  assert(!weak_core.expired()); // Executor still owns its submitted closure.
  if (keep_external_job) {
    assert(!weak_job.expired() && !weak_context.expired());
    assert(counts.jobs == 0 && counts.contexts == 0);
    job.reset();
  }
  assert(weak_job.expired() && weak_context.expired());
  assert(counts.jobs == 1 && counts.contexts == 1 && counts.cores == 0);
  assert(counts.events[0] == "result_published");
  assert(counts.events[1] == "group_removed");
  assert(counts.events[2] == "final_returned");
  const auto released = std::find(counts.events.begin(), counts.events.end(), "argument_released");
  const auto destroyed = std::find(counts.events.begin(), counts.events.end(), "job_destroyed");
  assert(released != counts.events.end() && destroyed != counts.events.end());
  assert(keep_external_job ? released < destroyed : destroyed < released);
  executor.clear();
  assert(weak_core.expired() && counts.cores == 1);
  auto response_state = service.last_state.lock();
  assert(response_state);
  auto request = service.take(counts.task_id);
  assert(request && request->body == "owned teardown");
  finish(std::move(request)); // Late response AFTER all job/core/context release.
  OperationSnapshot result;
  {
    std::lock_guard<std::mutex> lock(response_state->mutex);
    result = response_state->result;
  }
  assert(result.callback_observed && result.response_copied && !result.sent);
  response_state.reset();
  assert(service.last_state.expired());
  assert(bodies == 0 && responses == 0 && requests == 0);
}
}
int main() {
  exercise(false);
  exercise(true);
  std::cout << "{\"cases\":2,\"group_removed_before_final\":true,"
               "\"argument_released_after_final\":true,\"external_owner_delays_job_destruction\":true,"
               "\"executor_capture_retains_core\":true,\"late_request_survives_job_teardown\":true,"
               "\"balanced_lifetime\":true,\"native_scheduler_executed\":false,\"sent\":false}\n";
}
