// Owned fault-injection fixture; actual Apple ARM64 erased invocation, no WeChat.
#include "newsendmsg_job_finished_4115.hpp"
#include <cassert>
#include <iostream>
#include <string>
#include <thread>
#include <vector>

using namespace newsendmsg4115;
void probe_finished(JobFinished*, const bool*) __asm("_probe_job_finished_erasure");

struct Marker {
  int* alive;
  explicit Marker(int& count) : alive(&count) { ++*alive; }
  ~Marker() { --*alive; }
};

int main() {
  // Actual host erased vslot+0x30 receives the address of the native bool.
  {
    auto state = std::make_shared<FinishedFailureState>();
    int calls = 0, trues = 0;
    auto finished = make_guarded_job_finished(state, [&](bool flag) {
      ++calls;
      trues += flag;
    });
    bool flag = true;
    probe_finished(&finished, &flag);
    flag = false;
    probe_finished(&finished, &flag);
    assert(calls == 2 && trues == 1);
    assert(!state->snapshot().failure_observed && !state->snapshot().sent);
  }
  {
    auto state = std::make_shared<FinishedFailureState>();
    auto finished = make_guarded_job_finished(state, [](bool) {
      throw std::runtime_error("owned final notification failed");
    });
    bool flag = false;
    probe_finished(&finished, &flag);
    const auto failure = state->snapshot();
    assert(failure.failure_observed && failure.exception_available && !failure.sent);
    try {
      std::rethrow_exception(failure.exception);
      assert(false);
    } catch (const std::runtime_error& error) {
      assert(std::string(error.what()) == "owned final notification failed");
    }
  }
  {
    auto state = std::make_shared<FinishedFailureState>();
    auto finished = make_guarded_job_finished(state, [](bool) { throw 4115; });
    bool flag = true;
    probe_finished(&finished, &flag);
    try {
      std::rethrow_exception(state->snapshot().exception);
      assert(false);
    } catch (int error) {
      assert(error == 4115);
    }
  }
  {
    auto state = std::make_shared<FinishedFailureState>();
    auto finished = make_guarded_job_finished(state, [](bool flag) { throw flag ? 1 : 2; });
    bool flag = true;
    probe_finished(&finished, &flag);
    const auto first = state->snapshot().exception;
    flag = false;
    probe_finished(&finished, &flag);
    assert(state->snapshot().exception == first);
    try { std::rethrow_exception(first); } catch (int error) { assert(error == 1); }
  }
  {
    std::weak_ptr<FinishedFailureState> weak;
    JobFinished copy;
    int alive = 0;
    {
      auto state = std::make_shared<FinishedFailureState>();
      weak = state;
      auto marker = std::make_shared<Marker>(alive);
      auto finished = make_guarded_job_finished(state, [marker](bool) { throw 3; });
      copy = finished;
    }
    assert(!weak.expired() && alive == 1);
    bool flag = false;
    probe_finished(&copy, &flag);
    assert(weak.lock()->snapshot().failure_observed);
    copy = nullptr;
    assert(weak.expired() && alive == 0);
  }
  {
    auto state = std::make_shared<FinishedFailureState>();
    auto finished = make_guarded_job_finished(state, [](bool) { throw 17; });
    std::vector<std::thread> threads;
    std::atomic<bool> go{false};
    std::atomic<unsigned> completed{0};
    for (unsigned i = 0; i < 32; ++i) {
      threads.emplace_back([finished, &go, &completed]() mutable {
        while (!go.load(std::memory_order_acquire)) std::this_thread::yield();
        bool flag = false;
        probe_finished(&finished, &flag);
        completed.fetch_add(1, std::memory_order_release);
      });
    }
    go.store(true, std::memory_order_release);
    while (completed.load(std::memory_order_acquire) != 32) {
      const auto snapshot = state->snapshot();
      if (snapshot.exception_available) assert(snapshot.failure_observed && snapshot.exception);
    }
    for (auto& thread : threads) thread.join();
    try { std::rethrow_exception(state->snapshot().exception); }
    catch (int error) { assert(error == 17); }
    assert(!state->snapshot().sent);
  }
  {
    auto state = std::make_shared<FinishedFailureState>();
    bool rejected_empty = false, rejected_state = false;
    try { make_guarded_job_finished(state, {}); }
    catch (const std::invalid_argument&) { rejected_empty = true; }
    try { make_guarded_job_finished({}, [](bool) {}); }
    catch (const std::invalid_argument&) { rejected_state = true; }
    assert(rejected_empty && rejected_state);
  }
  {
    // A final notification fault must return to the enclosing owned cleanup.
    auto state = std::make_shared<FinishedFailureState>();
    auto finished = make_guarded_job_finished(state, [](bool) { throw 19; });
    int argument_alive = 0;
    std::weak_ptr<Marker> weak;
    {
      auto argument = std::make_shared<Marker>(argument_alive);
      weak = argument;
      bool flag = false;
      probe_finished(&finished, &flag);
      assert(argument_alive == 1 && state->snapshot().failure_observed);
      argument.reset();
    }
    assert(weak.expired() && argument_alive == 0);
  }
  std::cout << "{\"cases\":8,\"erased_bool_invoke\":true,\"std_and_nonstd_caught\":true,"
               "\"first_failure_preserved\":true,\"clone_lifetime_balanced\":true,"
               "\"concurrent_faults\":32,\"cleanup_after_final_fault\":true,"
               "\"native_scheduler_executed\":false,\"sent\":false}\n";
}
