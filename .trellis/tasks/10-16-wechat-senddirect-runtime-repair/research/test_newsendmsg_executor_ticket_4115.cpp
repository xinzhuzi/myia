// All objects, service calls and queue operations in this file are owned fixtures.
#define main existing_operation_fixture_main
#include "test_newsendmsg_operation_4115.cpp"
#undef main
#include "newsendmsg_executor_abi_4115.hpp"
#include <cstddef>

ExecutorTicket submit_through_slot(Executor*, JobBody*) __asm("_probe_executor_submit");
void remove_through_slot(Executor*, ExecutorTicket) __asm("_probe_executor_remove");
void invoke_ticket_body(JobBody*) __asm("_probe_job_body_erasure");

namespace {
struct FixtureVTable {
  void (*unused0)();
  void (*unused1)();
  SubmitExecutorTask submit;
  void (*unused3)();
  RemoveExecutorTask remove;
};
static_assert(offsetof(FixtureVTable, submit) == 0x10);
static_assert(offsetof(FixtureVTable, remove) == 0x20);
struct QueuedRecord { JobBody body; };
struct FixtureExecutor {
  const FixtureVTable* table;
  std::map<ExecutorTicket, std::unique_ptr<QueuedRecord>> records;
  std::mutex mutex{};
  ExecutorTicket next = 0x0000000300000029ULL;
  ExecutorTicket last_removed = 0;
  bool removal_lock_held = false;
  Executor* observed_this = nullptr;
  JobBody* observed_function = nullptr;
  Executor* opaque() { return reinterpret_cast<Executor*>(this); }
};
ExecutorTicket submit_fixture(Executor* object, JobBody* body) {
  auto& executor = *reinterpret_cast<FixtureExecutor*>(object);
  executor.observed_this = object;
  executor.observed_function = body;
  const auto ticket = executor.next++;
  auto record = std::make_unique<QueuedRecord>();
  record->body = std::move(*body);
  executor.records.emplace(ticket, std::move(record));
  return ticket;
}
void remove_fixture(Executor* object, ExecutorTicket ticket) {
  auto& executor = *reinterpret_cast<FixtureExecutor*>(object);
  std::lock_guard<std::mutex> lock(executor.mutex);
  executor.last_removed = ticket;
  const auto found = executor.records.find(ticket);
  if (found != executor.records.end()) {
    executor.removal_lock_held = true;
    found->second->body = {}; // Ordinary queued payload dies while lock is held.
    executor.removal_lock_held = false;
    // The scheduling record remains until the modeled worker reclaims it.
  }
}
const FixtureVTable table{nullptr, nullptr, submit_fixture, nullptr, remove_fixture};
struct DisposalProbe {
  FixtureExecutor* executor;
  bool* disposed;
  ~DisposalProbe() noexcept {
    assert(executor->removal_lock_held);
    *disposed = true;
  }
};
}

int main() {
  unsigned scenarios = 0;
  {
    FixtureExecutor executor{&table, {}};
    unsigned calls = 0;
    JobBody body = [&] { ++calls; };
    const auto ticket = submit_through_slot(executor.opaque(), &body);
    assert(ticket == 0x0000000300000029ULL && calls == 0);
    assert(executor.observed_this == executor.opaque());
    assert(executor.observed_function == &body);
    // No assertion that the moved-from source must be empty.
    body = {};
    invoke_ticket_body(&executor.records.at(ticket)->body);
    assert(calls == 1 && executor.records.size() == 1);
    ++scenarios;
  }
  {
    FixtureExecutor executor{&table, {}};
    bool disposed = false;
    auto probe = std::shared_ptr<DisposalProbe>(new DisposalProbe{&executor, &disposed});
    JobBody body = [probe] { assert(false); };
    const auto ticket = submit_through_slot(executor.opaque(), &body);
    body = {};
    probe.reset();
    assert(!disposed);
    remove_through_slot(executor.opaque(), ticket);
    assert(disposed && executor.last_removed == ticket);
    assert(executor.records.size() == 1 && !executor.records.at(ticket)->body);
    // Payload release does not mean the record/heap/whole executor is drained.
    executor.records.erase(ticket);
    ++scenarios;
  }
  {
    FixtureExecutor executor{&table, {}};
    JobBody body = [] {};
    const auto ticket = submit_through_slot(executor.opaque(), &body);
    remove_through_slot(executor.opaque(), static_cast<std::uint32_t>(ticket));
    assert(executor.records.at(ticket)->body); // High index bits are required.
    remove_through_slot(executor.opaque(), ticket + 1);
    assert(executor.records.at(ticket)->body); // Low generation bits must match.
    remove_through_slot(executor.opaque(), ticket);
    assert(!executor.records.at(ticket)->body);
    ++scenarios;
  }
  {
    FixtureExecutor executor{&table, {}};
    auto marker = std::make_shared<int>(4115);
    std::weak_ptr<int> weak = marker;
    JobBody body = [marker] { assert(*marker == 4115); };
    auto external_copy = body;
    marker.reset();
    const auto ticket = submit_through_slot(executor.opaque(), &body);
    body = {};
    remove_through_slot(executor.opaque(), ticket);
    assert(!weak.expired());
    external_copy = {};
    assert(weak.expired());
    ++scenarios;
  }
  {
    Service service;
    FixtureExecutor executor{&table, {}};
    std::unique_ptr<ResearchOperation> operation;
    JobBody body = [&] {
      operation = std::make_unique<ResearchOperation>(
          functions, &service, &options, "route", "text", 4, deadline());
    };
    const auto ticket = submit_through_slot(executor.opaque(), &body);
    body = {};
    // An ordinary dispatch unlinks the index before executing outside its lock.
    auto active = std::move(executor.records.at(ticket));
    executor.records.erase(ticket);
    invoke_ticket_body(&active->body);
    assert(operation && requests == 1);
    auto detached = service.take(operation->task_id());
    remove_through_slot(executor.opaque(), ticket); // Already dispatched; no status result.
    active.reset();
    assert(requests == 1 && !service.last_state.expired());
    assert(operation->cancel()); // Independent request cancellation remains necessary.
    finish(std::move(detached));
    const auto state = operation->snapshot();
    assert(state.phase == OperationPhase::cancelled && state.callback_observed);
    assert(state.response_copied && !state.sent);
    operation.reset();
    assert(service.last_state.expired() && requests == 0);
    ++scenarios;
  }
  assert(bodies == 0 && responses == 0 && requests == 0);
  std::cout << "{\"scenarios\":" << scenarios << ",\"host_virtual_slots\":true,"
               "\"ticket_bits\":64,\"real_operation_component\":true,"
               "\"balanced_lifetime\":true,\"target_executed\":false,\"sent\":false}\n";
}
