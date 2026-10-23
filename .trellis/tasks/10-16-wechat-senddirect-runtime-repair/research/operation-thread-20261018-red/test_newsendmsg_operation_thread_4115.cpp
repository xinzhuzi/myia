// Self-owned thread-affinity regression. No target library, loader or process.
#define main existing_operation_fixture_main
#include "test_newsendmsg_operation_4115.cpp"
#undef main
#include <condition_variable>

int main() {
  unsigned cases = 0;
  std::atomic<unsigned> rejected{0};
  auto reject_control = [&](auto action) {
    try { action(); }
    catch (const std::logic_error&) { ++rejected; }
  };
  bool passed = true;
  {
    Service service;
    const auto end = deadline();
    ResearchOperation operation(functions, &service, &options, "", "x", 1, end);
    const auto before = cancels.load();
    std::vector<std::thread> workers;
    for (unsigned i = 0; i < 32; ++i) workers.emplace_back([&] {
      reject_control([&] { operation.cancel(); });
      reject_control([&] { operation.expire(end); });
      // Evidence reads remain allowed on response/observer threads.
      if (operation.snapshot().sent) std::terminate();
    });
    for (auto& worker : workers) worker.join();
    passed = passed && rejected == 64 && cancels == before && requests == 1;
    passed = passed && operation.snapshot().phase == OperationPhase::pending;
    passed = passed && !operation.expire(end - std::chrono::nanoseconds(1));
    if (operation.snapshot().phase == OperationPhase::pending) {
      passed = passed && operation.cancel() && !operation.cancel();
    }
    passed = passed && cancels == before + 1 && requests == 0;
    ++cases;
  }
  {
    Service service;
    const auto end = deadline();
    ResearchOperation operation(functions, &service, &options, "", "x", 1, end);
    auto detached = service.take(operation.task_id());
    passed = passed && operation.expire(end);
    const auto before = cancels.load();
    std::thread callback([&] {
      reject_control([&] { operation.cancel(); });
      // A not-yet-due expiry is still a control command, even after completion.
      reject_control([&] { operation.expire(end - std::chrono::nanoseconds(1)); });
      finish(std::move(detached));
      const auto result = operation.snapshot();
      if (result.phase != OperationPhase::timed_out || !result.callback_observed ||
          !result.response_copied || result.sent) std::terminate();
    });
    callback.join();
    passed = passed && rejected == 66 && cancels == before && requests == 0;
    ++cases;
  }
  {
    Service service;
    std::mutex handoff_mutex;
    std::condition_variable handoff;
    std::unique_ptr<ResearchOperation> operation;
    bool ready = false, checked = false;
    std::thread executor([&] {
      auto owned = std::make_unique<ResearchOperation>(
          functions, &service, &options, "", "x", 1, deadline());
      {
        std::unique_lock<std::mutex> lock(handoff_mutex);
        operation = std::move(owned);
        ready = true;
        handoff.notify_one();
        handoff.wait(lock, [&] { return checked; });
      }
      operation->cancel();
      operation.reset();
    });
    {
      std::unique_lock<std::mutex> lock(handoff_mutex);
      handoff.wait(lock, [&] { return ready; });
      const auto before = cancels.load();
      reject_control([&] { operation->cancel(); });
      passed = passed && rejected == 67 && cancels == before;
      checked = true;
      handoff.notify_one();
    }
    executor.join();
    passed = passed && service.last_state.expired() && requests == 0;
    ++cases;
  }
  passed = passed && bodies == 0 && responses == 0 && requests == 0;
  std::cout << "{\"cases\":" << cases << ",\"wrong_thread_rejections\":" << rejected
            << ",\"passed\":" << (passed ? "true" : "false")
            << ",\"wechat_loaded\":false,\"sent\":false}\n";
  return passed ? 0 : 1;
}
