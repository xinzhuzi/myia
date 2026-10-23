// Standalone libc++ ABI/lifetime fixture. Never loads or attaches to WeChat.
#include "newsendmsg_completion_4115.hpp"
#include <cassert>
#include <cstring>
#include <iostream>
#include <string>
#include <thread>
#include <vector>

using namespace newsendmsg4115;

static void* erased_pointer(const Completion& function) {
  void* result = nullptr;
  std::memcpy(&result, reinterpret_cast<const char*>(&function) + 0x18, 8);
  return result;
}

// Match the verified heap-transfer arm of factory 0x30c2c1c exactly.
// Both objects remain valid libc++ functions; the source is left empty.
static void transfer_heap(Completion& target, Completion& source) {
  assert(!target);
  void* pointer = erased_pointer(source);
  assert(pointer && pointer != &source);
  std::memcpy(reinterpret_cast<char*>(&target) + 0x18, &pointer, 8);
  pointer = nullptr;
  std::memcpy(reinterpret_cast<char*>(&source) + 0x18, &pointer, 8);
}

static bool invoke_like_native(Completion& completion, void* request, int type, int code) {
  void* object = erased_pointer(completion);
  assert(object);
  void** vtable = nullptr;
  std::memcpy(&vtable, object, 8);
  using Invoke = bool (*)(void*, void**, int*, int*);
  Invoke invoke = nullptr;
  std::memcpy(&invoke, reinterpret_cast<const char*>(vtable) + 0x30, 8);
  return invoke(object, &request, &type, &code);
}

int main() {
  static_assert(sizeof(std::string) == 24);
  static_assert(sizeof(int) == 4 && sizeof(void*) == 8);
  unsigned checks = 0;
  for (std::size_t size : {0U, 1U, 22U, 23U, 24U, 1000U}) {
    const std::string text(size, 'x');
    unsigned char raw[24];
    std::memcpy(raw, &text, sizeof(raw));
    std::size_t length = raw[23];
    const char* data = reinterpret_cast<const char*>(&text);
    if ((raw[23] & 0x80) != 0) {
      std::memcpy(&length, raw + 8, 8);
      std::memcpy(&data, raw, 8);
    }
    assert(length == text.size());
    assert(std::string(data, length) == text);
    ++checks;
  }
  {
    auto state = std::make_shared<CompletionState>();
    std::weak_ptr<CompletionState> weak = state;
    Completion source = make_completion(state), owned;
    transfer_heap(owned, source);
    assert(!source && owned && state.use_count() == 2);
    source = nullptr;
    state.reset();
    assert(!weak.expired());
    std::thread worker([&] {
      assert(invoke_like_native(owned, reinterpret_cast<void*>(0x1234), -9, -13));
    });
    worker.join();
    const auto result = weak.lock()->snapshot();
    assert(result.received && result.error_type == -9 && result.error_code == -13);
    assert(!result.sent);
    assert(invoke_like_native(owned, nullptr, 0, 0));
    assert(weak.lock()->snapshot().error_code == -13); // First result is immutable.
    owned = nullptr;
    assert(weak.expired());
    checks += 6;
  }
  {
    auto state = std::make_shared<CompletionState>();
    Completion original = make_completion(state);
    Completion copy = original; // Exercise libc++ heap clone and independent destruction.
    original = nullptr;
    assert(invoke_like_native(copy, nullptr, 0, 0));
    assert(state->snapshot().received && !state->snapshot().sent);
    checks += 2;
  }
  {
    auto state = std::make_shared<CompletionState>();
    std::vector<std::thread> workers;
    for (int i = 1; i <= 32; ++i)
      workers.emplace_back([state, i] { state->record(i, -i); });
    for (auto& worker : workers) worker.join();
    const auto result = state->snapshot();
    assert(result.received && result.error_type >= 1 && result.error_type <= 32);
    assert(result.error_code == -result.error_type && !result.sent);
    ++checks;
  }
  {
    bool rejected = false;
    try { auto invalid = make_completion(nullptr); }
    catch (const std::invalid_argument&) { rejected = true; }
    assert(rejected);
    ++checks;
  }
  std::cout << "{\"checks\":" << checks
            << ",\"heap_transfer\":true,\"invoke_vslot_0x30\":true,"
            << "\"first_result_preserved\":true,\"capture_released\":true,"
            << "\"wechat_loaded\":false,\"target_attached\":false,\"sent\":false}\n";
}
