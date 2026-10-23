// Standalone service fixture matching verified map-removal/callback ordering.
// No WeChat library is loaded; all native functions below are local fixtures.
#include "newsendmsg_operation_4115.hpp"
#include <cassert>
#include <cstring>
#include <iostream>
#include <map>
#include <thread>

using namespace newsendmsg4115;
namespace {
struct Body { std::string bytes; };
struct Response { std::string bytes; int cached = -1; bool valid = true; };
static_assert(sizeof(Body) <= 48 && sizeof(Response) <= 56);
std::atomic<unsigned> bodies{0}, responses{0}, requests{0}, cancels{0}, factories{0};
bool reject_body = false, throw_factory = false;
void body_new(void* target) { new (target) Body; ++bodies; }
bool body_parse(void* target, const void* bytes, std::int32_t size) {
  static_cast<Body*>(target)->bytes.assign(static_cast<const char*>(bytes), size);
  return !reject_body;
}
void body_delete(void* target) { static_cast<Body*>(target)->~Body(); --bodies; }
void response_new(void* target) { new (target) Response; ++responses; }
void response_copy(void* target, const void* source) {
  *static_cast<Response*>(target) = *static_cast<const Response*>(source);
}
void response_delete(void* target) { static_cast<Response*>(target)->~Response(); --responses; }
bool response_valid(const void* target) { return static_cast<const Response*>(target)->valid; }
std::int32_t response_size(void* target) {
  auto& response = *static_cast<Response*>(target);
  response.cached = static_cast<int>(response.bytes.size());
  return response.cached;
}
std::byte* response_write(const void* target, std::byte* output) {
  const auto& response = *static_cast<const Response*>(target);
  assert(response.cached == static_cast<int>(response.bytes.size()));
  std::memcpy(output, response.bytes.data(), response.bytes.size());
  return output + response.bytes.size();
}
struct Request {
  std::string body, routing;
  Response response{"\x08\x01", -1, true};
  Completion completion;
  Request() { ++requests; }
  ~Request() { --requests; }
};
struct Service {
  std::mutex mutex;
  std::map<std::uint32_t, std::unique_ptr<Request>> pending;
  std::uint32_t next = 41;
  std::weak_ptr<OperationState> last_state;
  std::unique_ptr<Request> take(std::uint32_t id) {
    std::lock_guard<std::mutex> lock(mutex);
    auto entry = pending.find(id);
    if (entry == pending.end()) return {};
    auto request = std::move(entry->second);
    pending.erase(entry);
    return request; // Callback runs outside the map mutex, as native does.
  }
};
std::uint32_t factory(void* target, const void* body, const std::string* routing,
                      const void* options, Completion* completion) {
  ++factories;
  assert(options && completion && *completion);
  if (throw_factory) throw std::runtime_error("fixture factory rejected before transfer");
  auto& service = *static_cast<Service*>(target);
  auto request = std::make_unique<Request>();
  request->body = static_cast<const Body*>(body)->bytes;
  request->routing = *routing;
  service.last_state = completion->target<CallbackCapture>()->state;
  request->completion = std::move(*completion);
  std::lock_guard<std::mutex> lock(service.mutex);
  const auto id = service.next++;
  service.pending.emplace(id, std::move(request));
  return id;
}
void cancel(void* target, std::uint32_t id) {
  ++cancels;
  auto request = static_cast<Service*>(target)->take(id);
  // Native cancel deletes a queued request WITHOUT invoking completion.
}
const void* response_from_request(void* request) {
  return &static_cast<Request*>(request)->response;
}
void finish(std::unique_ptr<Request> request, int type = 0, int code = 0) {
  assert(request);
  // Exercise native erased libc++ invoke slot with reference arguments.
  void* object = nullptr;
  std::memcpy(&object, reinterpret_cast<const char*>(&request->completion) + 0x18, 8);
  assert(object && object != &request->completion);
  void** table = nullptr;
  std::memcpy(&table, object, 8);
  using Invoke = bool (*)(void*, void**, int*, int*);
  Invoke invoke = nullptr;
  std::memcpy(&invoke, reinterpret_cast<const char*>(table) + 0x30, 8);
  void* raw = request.get();
  assert(invoke(object, &raw, &type, &code));
  // Request, response, and completion are destroyed AFTER callback returns.
}
const OperationFunctions functions{
  {body_new, body_parse, body_delete},
  {response_new, response_copy, response_delete, response_valid, response_size, response_write},
  factory, cancel, response_from_request};
const int options = 0;
using Clock = ResearchOperation::Clock;
auto deadline() { return Clock::now() + std::chrono::seconds(10); }
template <typename F> void fails(F action) {
  bool rejected = false;
  try { action(); } catch (const std::exception&) { rejected = true; }
  assert(rejected);
}
}
int main() {
  unsigned cases = 0;
  {
    Service service;
    ResearchOperation operation(functions, &service, &options, "route", "body", 4, deadline());
    assert(bodies == 0 && requests == 1); // Factory copied the body.
    auto request = service.take(operation.task_id());
    assert(request->body == "body" && request->routing == "route");
    std::thread worker([&] { finish(std::move(request)); }); worker.join();
    const auto result = operation.snapshot();
    assert(result.phase == OperationPhase::callback && result.callback_observed);
    assert(result.response_copied && !result.response_copy_failed && !result.sent);
    assert(result.response_wire.size() == 2 && requests == 0 && responses == 0);
    assert(!operation.cancel());
    ++cases;
  }
  for (int kind = 0; kind < 3; ++kind) {
    Service service;
    ResearchOperation operation(functions, &service, &options, "", "x", 1, deadline());
    auto request = service.take(operation.task_id());
    if (kind == 2) request->response.valid = false;
    finish(std::move(request), kind == 0 ? -1 : 0, kind == 1 ? -13 : 0);
    const auto result = operation.snapshot();
    assert(result.callback_observed && !result.response_copied && !result.sent);
    assert(result.response_copy_failed == (kind == 2));
    ++cases;
  }
  {
    Service service;
    ResearchOperation operation(functions, &service, &options, "", "x", 1, deadline());
    const auto before = cancels.load();
    std::vector<std::thread> workers;
    for (int i = 0; i < 32; ++i) workers.emplace_back([&] { operation.cancel(); });
    for (auto& worker : workers) worker.join();
    assert(cancels == before + 1 && requests == 0);
    assert(operation.snapshot().phase == OperationPhase::cancelled);
    assert(!operation.snapshot().callback_observed && !operation.snapshot().sent);
    ++cases;
  }
  {
    Service service;
    const auto end = deadline();
    ResearchOperation operation(functions, &service, &options, "", "x", 1, end);
    assert(!operation.expire(end - std::chrono::nanoseconds(1)));
    assert(operation.expire(end) && !operation.expire(end));
    assert(requests == 0 && operation.snapshot().phase == OperationPhase::timed_out);
    ++cases;
  }
  for (bool timeout : {false, true}) {
    Service service;
    const auto end = deadline();
    ResearchOperation operation(functions, &service, &options, "", "x", 1, end);
    auto detached = service.take(operation.task_id());
    assert(timeout ? operation.expire(end) : operation.cancel());
    assert(requests == 1); // Cancel cannot delete a request removed by OnTaskEnd.
    finish(std::move(detached));
    const auto result = operation.snapshot();
    assert(result.phase == (timeout ? OperationPhase::timed_out : OperationPhase::cancelled));
    assert(result.callback_observed && result.response_copied && !result.sent);
    ++cases;
  }
  {
    Service service;
    std::uint32_t id;
    {
      ResearchOperation operation(functions, &service, &options, "", "x", 1, deadline());
      id = operation.task_id();
    }
    assert(!service.last_state.expired()); // Capture owns state after handle dies.
    finish(service.take(id));
    assert(service.last_state.expired());
    ++cases;
  }
  {
    Service service;
    const auto before = factories.load();
    fails([&] { ResearchOperation op(functions, &service, &options, "", "x", 1, Clock::now()); });
    assert(factories == before);
    reject_body = true;
    fails([&] { ResearchOperation op(functions, &service, &options, "", "x", 1, deadline()); });
    reject_body = false;
    assert(factories == before && bodies == 0);
    throw_factory = true;
    fails([&] { ResearchOperation op(functions, &service, &options, "", "x", 1, deadline()); });
    throw_factory = false;
    assert(factories == before + 1 && bodies == 0 && requests == 0);
    ++cases;
  }
  // Repeated cross-thread completion/cancel races cover both native map owners.
  for (int run = 0; run < 100; ++run) {
    Service service;
    ResearchOperation operation(functions, &service, &options, "", "x", 1, deadline());
    std::thread complete([&] {
      auto request = service.take(operation.task_id());
      if (request) finish(std::move(request));
    });
    std::thread stop([&] { operation.cancel(); });
    complete.join(); stop.join();
    const auto result = operation.snapshot();
    assert(result.phase != OperationPhase::pending && !result.sent);
    assert(requests == 0 && bodies == 0 && responses == 0);
  }
  ++cases;
  assert(requests == 0 && bodies == 0 && responses == 0);
  std::cout << "{\"cases\":" << cases << ",\"cancel_races\":100,"
               "\"late_callback_preserves_terminal_state\":true,"
               "\"balanced_lifetime\":true,\"wechat_loaded\":false,\"sent\":false}\n";
  return 0;
}
