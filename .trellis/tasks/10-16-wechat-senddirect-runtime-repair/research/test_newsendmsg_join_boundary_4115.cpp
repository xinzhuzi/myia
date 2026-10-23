// Owned counterexample for the frozen completion ordering, not a native job.
// No WeChat loader, addresses, attachment, network, or product integration.
#include <atomic>
#include <cassert>
#include <chrono>
#include <condition_variable>
#include <functional>
#include <future>
#include <iostream>
#include <memory>
#include <mutex>
#include <thread>
#include <vector>

namespace {
class Gate {
  std::mutex mutex_;
  std::condition_variable changed_;
  bool open_ = false;
public:
  void open() {
    std::lock_guard<std::mutex> lock(mutex_);
    open_ = true;
    changed_.notify_all();
  }
  void wait() {
    std::unique_lock<std::mutex> lock(mutex_);
    if (!changed_.wait_for(lock, std::chrono::seconds(2), [this] { return open_; }))
      std::terminate();
  }
};
struct Payload {
  std::atomic<unsigned>& destroyed;
  explicit Payload(std::atomic<unsigned>& count) : destroyed(count) {}
  ~Payload() { ++destroyed; }
};
struct OwnedJob {
  std::promise<int> published;
  std::function<void(bool)> finished;
};
void exercise(bool cancelled) {
  std::atomic<unsigned> destroyed{0};
  std::atomic<bool> entered{false}, returned{false}, queued_called{false};
  Gate before_callback, callback_entered, allow_callback_return;
  auto payload = std::make_shared<Payload>(destroyed);
  std::weak_ptr<Payload> retained = payload;
  auto job = std::make_shared<OwnedJob>();
  job->finished = [held = payload, &entered, &returned,
                   &callback_entered, &allow_callback_return, cancelled](bool value) {
    assert(held && value == cancelled);
    entered = true;
    callback_entered.open();
    allow_callback_return.wait();
    returned = true;
  };
  // The native signals dispatcher may enqueue a separately owned receiver.
  // This owned receiver intentionally keeps the payload beyond callback return.
  std::vector<std::function<void()>> executor;
  executor.emplace_back([held = payload, &queued_called] {
    assert(held);
    queued_called = true;
  });
  payload.reset();
  auto result = job->published.get_future();
  std::thread worker([held = job, &before_callback, cancelled] {
    // Frozen 0x667fc38 publishes an integer zero before its final callback.
    // The gate makes the otherwise timing-dependent gap deterministic.
    held->published.set_value(0);
    before_callback.wait();
    held->finished(cancelled);
  });
  assert(result.wait_for(std::chrono::seconds(2)) == std::future_status::ready);
  assert(result.get() == 0);
  assert(!entered && !returned && !retained.expired() && destroyed == 0);
  before_callback.open();
  callback_entered.wait();
  assert(entered && !returned && !retained.expired() && destroyed == 0);
  allow_callback_return.open();
  worker.join();
  assert(returned && !queued_called && !retained.expired() && destroyed == 0);
  job.reset();
  assert(!retained.expired() && destroyed == 0); // Queued receiver still owns it.
  executor.front()();
  executor.clear();
  assert(queued_called && retained.expired() && destroyed == 1);
}
}
int main() {
  exercise(false);
  exercise(true);
  std::cout << "{\"scenarios\":2,\"result_before_callback\":true,"
               "\"entered_is_not_returned\":true,\"callback_return_is_not_capture_release\":true,"
               "\"queued_receiver_outlives_job\":true,\"balanced_owned_lifetime\":true,"
               "\"native_scheduler_executed\":false,\"sent\":false}\n";
}
