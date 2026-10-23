// All function pointers below refer to owned fixtures, never to WeChat.
#define main existing_operation_fixture_main
#include "test_newsendmsg_operation_4115.cpp"
#undef main
#include "newsendmsg_executor_operation_4115.hpp"
#include <type_traits>

namespace {
thread_local void* fixture_executor = nullptr;
std::atomic<unsigned> getter_calls{0}, body_calls{0};
void* get_fixture_executor() { ++getter_calls; return fixture_executor; }
void counted_body_new(void* target) { ++body_calls; body_new(target); }
template <typename Error, typename Action>
void rejects(Action action) {
  bool rejected = false;
  try { action(); } catch (const Error&) { rejected = true; }
  assert(rejected);
}
}

int main() {
  static_assert(!std::is_copy_constructible_v<ExecutorResearchOperation>);
  static_assert(!std::is_move_constructible_v<ExecutorResearchOperation>);
  unsigned cases = 0;
  int expected = 0, other = 0;
  const ExecutorContext context{get_fixture_executor, &expected};
  auto checked = functions;
  checked.body.construct = counted_body_new;
  // Missing contracts must not call even the injected getter. Wrong TLS must
  // reject before any body constructor, parser, factory, request or callback.
  for (unsigned kind = 0; kind < 4; ++kind) {
    Service service;
    auto invalid = context;
    fixture_executor = &expected;
    if (kind == 0) invalid.current_executor = nullptr;
    if (kind == 1) invalid.expected_executor = nullptr;
    if (kind == 2) fixture_executor = nullptr;
    if (kind == 3) fixture_executor = &other;
    const auto before_get = getter_calls.load(), before_body = body_calls.load();
    const auto before_factory = factories.load(), before_cancel = cancels.load();
    auto construct = [&] {
      ExecutorResearchOperation operation(invalid, checked, &service, &options,
                                           "route", "body", 4, deadline());
    };
    if (kind < 2) rejects<std::invalid_argument>(construct);
    else rejects<std::logic_error>(construct);
    assert(getter_calls == before_get + (kind < 2 ? 0 : 1));
    assert(body_calls == before_body && factories == before_factory);
    assert(cancels == before_cancel && requests == 0 && service.last_state.expired());
    ++cases;
  }
  fixture_executor = &expected;
  {
    Service service;
    const auto end = deadline();
    ExecutorResearchOperation operation(context, checked, &service, &options,
                                         "route", "body", 4, end);
    const auto before = cancels.load();
    for (void* wrong : {static_cast<void*>(nullptr), static_cast<void*>(&other)}) {
      fixture_executor = wrong;
      rejects<std::logic_error>([&] { operation.cancel(); });
      rejects<std::logic_error>([&] { operation.expire(end - std::chrono::nanoseconds(1)); });
      assert(cancels == before && requests == 1);
      assert(operation.snapshot().phase == OperationPhase::pending);
    }
    fixture_executor = &expected;
    assert(!operation.expire(end - std::chrono::nanoseconds(1)));
    assert(operation.cancel() && !operation.cancel());
    assert(requests == 0 && cancels == before + 1);
    // Completed controls still enforce context; no fast-path bypass.
    fixture_executor = nullptr;
    rejects<std::logic_error>([&] { operation.cancel(); });
    rejects<std::logic_error>([&] { operation.expire(end); });
    assert(operation.snapshot().phase == OperationPhase::cancelled);
    ++cases;
  }
  fixture_executor = &expected;
  std::atomic<unsigned> wrong_thread_rejections{0};
  {
    Service service;
    const auto end = deadline();
    ExecutorResearchOperation operation(context, checked, &service, &options, "", "x", 1, end);
    const auto before = cancels.load();
    std::vector<std::thread> workers;
    for (unsigned i = 0; i < 32; ++i) workers.emplace_back([&] {
      // Artificially equal fixture pointers must not bypass the owner token.
      fixture_executor = &expected;
      try { operation.cancel(); } catch (const std::logic_error&) { ++wrong_thread_rejections; }
      try { operation.expire(end); } catch (const std::logic_error&) { ++wrong_thread_rejections; }
      const auto before_get = getter_calls.fetch_add(0);
      assert(operation.task_id() != 0 && !operation.snapshot().sent);
      // Snapshot does not call the getter; global equality cannot be asserted
      // here while other workers query it concurrently.
      (void)before_get;
    });
    for (auto& worker : workers) worker.join();
    assert(wrong_thread_rejections == 64 && cancels == before && requests == 1);
    assert(operation.snapshot().phase == OperationPhase::pending);
    assert(operation.cancel() && requests == 0);
    ++cases;
  }
  {
    Service service;
    const auto end = deadline();
    ExecutorResearchOperation operation(context, checked, &service, &options, "", "x", 1, end);
    auto detached = service.take(operation.task_id());
    assert(operation.expire(end));
    const auto before_get = getter_calls.load(), before_cancel = cancels.load();
    std::thread callback([&] {
      assert(fixture_executor == nullptr);
      finish(std::move(detached));
      const auto result = operation.snapshot();
      assert(result.phase == OperationPhase::timed_out && result.callback_observed);
      assert(result.response_copied && !result.response_copy_failed && !result.sent);
      assert(result.response_wire == (std::vector<std::byte>{std::byte{8}, std::byte{1}}));
    });
    callback.join();
    assert(getter_calls == before_get && cancels == before_cancel && requests == 0);
    ++cases;
  }
  {
    Service service;
    auto operation = std::make_unique<ExecutorResearchOperation>(
        context, checked, &service, &options, "", "x", 1, deadline());
    const auto id = operation->task_id();
    const auto before_get = getter_calls.load(), before_cancel = cancels.load();
    std::thread teardown([&] {
      assert(fixture_executor == nullptr);
      assert(!operation->snapshot().sent);
      operation.reset(); // No implicit getter/cancel, even outside the executor.
    });
    teardown.join();
    assert(getter_calls == before_get && cancels == before_cancel && requests == 1);
    assert(!service.last_state.expired());
    finish(service.take(id));
    assert(service.last_state.expired() && requests == 0);
    ++cases;
  }
  {
    Service service;
    const auto before = factories.load();
    reject_body = true;
    rejects<std::runtime_error>([&] {
      ExecutorResearchOperation operation(context, checked, &service, &options, "", "x", 1, deadline());
    });
    reject_body = false;
    assert(factories == before && bodies == 0 && requests == 0);
    throw_factory = true;
    rejects<std::runtime_error>([&] {
      ExecutorResearchOperation operation(context, checked, &service, &options, "", "x", 1, deadline());
    });
    throw_factory = false;
    assert(factories == before + 1 && bodies == 0 && requests == 0);
    ++cases;
  }
  assert(bodies == 0 && responses == 0 && requests == 0);
  std::cout << "{\"cases\":" << cases << ",\"wrong_thread_rejections\":"
            << wrong_thread_rejections << ",\"passed\":true,\"balanced_lifetime\":true,"
               "\"wechat_loaded\":false,\"sent\":false}\n";
}
