// Standalone host ABI and ownership fixture. No WeChat libraries or addresses.
#include "newsendmsg_text_service_abi_4115.hpp"
#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <new>
#include <utility>

using namespace newsendmsg4115;
using namespace std::string_literals;
extern "C" { std::uintptr_t text_service_abi_arguments[3]{}; }
TextServiceResult probe_submit(void*, const TextInputHandle*)
    __asm("_probe_text_service_submit");

namespace {
int identity;
int cases = 0;
int values_created = 0;
int values_destroyed = 0;
int calls = 0;
std::weak_ptr<std::string> input_lifetime;
enum class Mode { normal, error, empty, throws };
Mode mode = Mode::normal;
struct FixtureValue {
  TextInputHandle input;
  explicit FixtureValue(TextInputHandle source) : input(std::move(source)) { ++values_created; }
  ~FixtureValue() { ++values_destroyed; }
};
TextInputHandle owned_input() {
  assert(input_lifetime.expired() && values_created == values_destroyed);
  auto owner = std::make_shared<std::string>("owned fixture input");
  input_lifetime = owner;
  return TextInputHandle(owner, reinterpret_cast<TextInputOpaque*>(owner.get()));
}
TextServiceResult fixture_submit(void* service, const TextInputHandle* input) {
  ++calls;
  assert(service == &identity && input && *input);
  TextServiceResult result;
  if (mode == Mode::empty) return result;
  result.status_text = std::string(100000, 'x') + "中文\0尾部"s;
  auto owner = std::make_shared<FixtureValue>(*input);
  result.value = std::shared_ptr<TextServiceValueOpaque>(
      owner, reinterpret_cast<TextServiceValueOpaque*>(owner.get()));
  if (mode == Mode::error) {
    result.status_first = 7;
    result.status_second = 9;
  }
  if (mode == Mode::throws) throw std::runtime_error("own fixture failure after allocation");
  return result;
}
} // namespace

int main() {
  {
    // Construction from a returned prvalue must use this exact hidden x8 slot.
    alignas(TextServiceResult) std::array<std::byte, 0x50> storage;
    storage.fill(std::byte{0xa5});
    TextInputHandle input;
    SubmitTextInput function = probe_submit;
    auto* result = new (storage.data() + 0x10) TextServiceResult(function(&identity, &input));
    assert(text_service_abi_arguments[0] == reinterpret_cast<std::uintptr_t>(&identity));
    assert(text_service_abi_arguments[1] == reinterpret_cast<std::uintptr_t>(&input));
    assert(text_service_abi_arguments[2] == reinterpret_cast<std::uintptr_t>(result));
    assert(result->status_first == 0x11223344 && result->status_second == 0x55667788);
    assert(result->status_text.empty() && !result->value);
    result->~TextServiceResult();
    assert(std::all_of(storage.begin(), storage.begin() + 0x10,
                       [](auto byte) { return byte == std::byte{0xa5}; }));
    assert(std::all_of(storage.begin() + 0x40, storage.end(),
                       [](auto byte) { return byte == std::byte{0xa5}; }));
    ++cases;
  }
  SubmitTextInput submit = fixture_submit;
  {
    auto input = owned_input();
    {
      const auto result = submit(&identity, &input);
      assert(result.status_first == 0 && result.status_second == 0 && result.value);
      assert(result.status_text.size() == 100000 + std::string("中文\0尾部", 13).size());
      input.reset();
      assert(!input_lifetime.expired() && values_created == values_destroyed + 1);
    }
    assert(input_lifetime.expired() && values_created == values_destroyed);
    ++cases;
  }
  {
    mode = Mode::error;
    auto input = owned_input();
    {
      const auto result = submit(&identity, &input);
      assert(result.status_first == 7 && result.status_second == 9);
      assert(result.value && !result.status_text.empty());
    }
    input.reset();
    assert(input_lifetime.expired() && values_created == values_destroyed);
    ++cases;
  }
  {
    mode = Mode::normal;
    auto input = owned_input();
    {
      auto original = submit(&identity, &input);
      auto copy = original;
      assert(copy.value.use_count() == 2 && copy.status_text == original.status_text);
      copy.status_text = "independent copy";
      assert(original.status_text.size() > 100000);
      auto moved = std::move(copy);
      assert(!copy.value && moved.value == original.value);
      original.value.reset(); input.reset();
      assert(!input_lifetime.expired() && moved.value.use_count() == 1);
    }
    assert(input_lifetime.expired() && values_created == values_destroyed);
    ++cases;
  }
  {
    mode = Mode::throws;
    auto input = owned_input();
    bool threw = false;
    try { const auto result = submit(&identity, &input); }
    catch (const std::runtime_error&) { threw = true; }
    assert(threw && values_created == values_destroyed && !input_lifetime.expired());
    input.reset();
    assert(input_lifetime.expired());
    ++cases;
  }
  {
    mode = Mode::empty;
    auto input = owned_input();
    const auto result = submit(&identity, &input);
    assert(result.status_first == 0 && result.status_second == 0 && !result.value);
    input.reset();
    assert(input_lifetime.expired() && values_created == values_destroyed);
    ++cases;
  }
  {
    TextServiceResult empty;
    assert(empty.status_first == 0 && empty.status_second == 0);
    assert(empty.status_text.empty() && !empty.value);
    ++cases;
  }
  assert(cases == 7 && calls == 5 && values_created == values_destroyed);
  std::cout << "{\"cases\":7,\"hidden_x8\":true,\"arguments_match\":true,"
               "\"result_size\":48,\"guard_regions_intact\":true,"
               "\"ownership_checked\":true,\"exception_cleanup\":true,"
               "\"wechat_loaded\":false,\"sent\":false}\n";
}
