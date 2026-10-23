// Reuse the isolated fixture, adding an adversarial pre-return completion.
#define main operation_fixture_main
#include "test_newsendmsg_operation_4115.cpp"
#undef main

namespace {
std::thread early_worker;
std::atomic<bool> entered{false}, completed{false};
std::uint32_t early_factory(void* service, const void* body, const std::string* routing,
                            const void* options_ptr, Completion* completion) {
  auto publication = completion->target<CallbackCapture>()->publication;
  const auto id = factory(service, body, routing, options_ptr, completion);
  auto request = static_cast<Service*>(service)->take(id);
  early_worker = std::thread([publication, owned = std::move(request)]() mutable {
    assert(!publication->try_lock()); // Another thread still owns factory gate.
    entered.store(true, std::memory_order_release);
    finish(std::move(owned));
    completed.store(true, std::memory_order_release);
  });
  while (!entered.load(std::memory_order_acquire)) std::this_thread::yield();
  // Equivalent to the native factory's final request+8 read after enqueue:
  // the request must still exist even though completion is already in flight.
  assert(requests == 1 && !completed.load(std::memory_order_acquire));
  return id;
}
}
int main() {
  Service service;
  auto early_functions = functions;
  early_functions.factory = early_factory;
  ResearchOperation operation(early_functions, &service, &options, "", "x", 1, deadline());
  early_worker.join();
  assert(completed.load(std::memory_order_acquire));
  assert(operation.snapshot().callback_observed && !operation.snapshot().sent);
  assert(requests == 0 && responses == 0 && bodies == 0);
  std::cout << "{\"cases\":1,\"callback_before_factory_return\":true,"
               "\"request_preserved_until_factory_return\":true,\"wechat_loaded\":false,\"sent\":false}\n";
}
