// Standalone host fixture; never links, loads or invokes WeChat.
#include "newsendmsg_text_input_4115.hpp"
#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <vector>

using namespace newsendmsg4115;
extern "C" { std::uintptr_t text_input_abi_result{}; }
TextInputHandle probe_create() __asm("_probe_text_input_create");

namespace {
int identity;
int other_identity;
int created = 0;
int destroyed = 0;
int create_calls = 0;
int assign_calls = 0;
int fail_assign_call = 0;
int cases = 0;
constexpr std::byte guard{0xa5};

enum class Mode { fresh, empty, wrong_vtable, low, high, routing, body, throws };
Mode mode = Mode::fresh;

struct FixturePayload {
  const void* vtable = &identity;
  std::array<std::byte, 0x88> prefix;
  std::string routing;
  std::array<std::byte, 0x3c> middle;
  std::uint32_t low = 0;
  std::uint32_t high = 0;
  std::array<std::byte, 0x4dc> suffix;
  std::string body;
  std::array<std::byte, 0x18> tail;
  FixturePayload() {
    ++created;
    prefix.fill(guard); middle.fill(guard); suffix.fill(guard); tail.fill(guard);
  }
  ~FixturePayload() {
    const auto intact = [](const auto& bytes) {
      return std::all_of(bytes.begin(), bytes.end(), [](auto byte) { return byte == guard; });
    };
    assert(intact(prefix) && intact(middle) && intact(suffix) && intact(tail));
    ++destroyed;
  }
};
static_assert(offsetof(FixturePayload, routing) == 0x90);
static_assert(offsetof(FixturePayload, low) == 0xe4);
static_assert(offsetof(FixturePayload, high) == 0xe8);
static_assert(offsetof(FixturePayload, body) == 0x5c8);
static_assert(sizeof(FixturePayload) == 0x5f8);
std::weak_ptr<FixturePayload> last;
FixturePayload* active = nullptr;

TextInputHandle create_owned() {
  ++create_calls;
  if (mode == Mode::throws) throw std::runtime_error("fixture factory failure");
  if (mode == Mode::empty) return {};
  auto owner = std::make_shared<FixturePayload>();
  active = owner.get();
  last = owner;
  switch (mode) {
    case Mode::wrong_vtable: owner->vtable = &other_identity; break;
    case Mode::low: owner->low = 49; break;
    case Mode::high: owner->high = 1; break;
    case Mode::routing: owner->routing = "stale"; break;
    case Mode::body: owner->body = "stale"; break;
    default: break;
  }
  return TextInputHandle(owner, reinterpret_cast<TextInputOpaque*>(owner.get()));
}

std::string& assign_owned(std::string& destination, const std::string& source) {
  ++assign_calls;
  assert(active && active->low == 0 && active->high == 0);
  assert(&destination == &active->routing || &destination == &active->body);
  // Fail after mutation as well: destruction must own partially assigned strings.
  destination.assign(source);
  if (assign_calls == fail_assign_call)
    throw std::runtime_error("fixture string assignment failure");
  return destination;
}

TextInputFunctions functions() { return {create_owned, assign_owned, &identity}; }
void reset(Mode next = Mode::fresh) {
  assert(last.expired() && created == destroyed);
  last.reset(); active = nullptr;
  mode = next; create_calls = 0; assign_calls = 0; fail_assign_call = 0;
}
template<class Exception, class Action> void rejects(Action action) {
  bool rejected = false;
  try { action(); } catch (const Exception&) { rejected = true; }
  assert(rejected && last.expired() && created == destroyed);
  ++cases;
}
} // namespace

int main() {
  CreateTextInput abi = probe_create;
  TextInputHandle empty = abi();
  assert(!empty && text_input_abi_result == reinterpret_cast<std::uintptr_t>(&empty));
  ++cases;

  std::vector<std::string> bodies = {
      "今天真是个好日子🙂\n第二行",
      std::string(200000, 'x') + "中文尾部",
      "<category>brand_account</category>保留正文",
      "<![CDATA[<category>emoticon</category>]]>\r\n<&>\"",
      std::string("abc\0def", 7),
  };
  for (const auto& body : bodies) {
    reset();
    {
      NativeTextInput input(functions(), "filehelper", body);
      assert(input.handle() && active->routing == "filehelper" && active->body == body);
      assert(active->low == 1 && active->high == 0);
      assert(create_calls == 1 && assign_calls == 2 && !last.expired());
    }
    assert(last.expired() && created == destroyed);
    ++cases;
  }
  for (int missing = 0; missing < 3; ++missing) {
    reset();
    auto f = functions();
    if (missing == 0) f.create = nullptr;
    if (missing == 1) f.assign = nullptr;
    if (missing == 2) f.expected_vtable = nullptr;
    rejects<std::invalid_argument>([&] { NativeTextInput input(f, "filehelper", "x"); });
    assert(create_calls == 0 && assign_calls == 0);
  }
  reset();
  rejects<std::invalid_argument>([] { NativeTextInput input(functions(), "", "x"); });
  assert(create_calls == 0);
  reset();
  rejects<std::invalid_argument>([] { NativeTextInput input(functions(), "filehelper", ""); });
  assert(create_calls == 0);

  for (auto rejected_mode : {Mode::empty, Mode::wrong_vtable, Mode::low, Mode::high,
                             Mode::routing, Mode::body, Mode::throws}) {
    reset(rejected_mode);
    rejects<std::runtime_error>([] { NativeTextInput input(functions(), "filehelper", "x"); });
    assert(create_calls == 1 && assign_calls == 0);
  }
  for (int failure : {1, 2}) {
    reset(); fail_assign_call = failure;
    rejects<std::runtime_error>([] { NativeTextInput input(functions(), "filehelper", "partial正文"); });
    assert(create_calls == 1 && assign_calls == failure);
  }
  reset();
  {
    TextInputHandle retained;
    {
      std::string route = "filehelper", body = "copied正文";
      NativeTextInput input(functions(), route, body);
      route = "changed"; body.clear();
      assert(active->routing == "filehelper" && active->body == "copied正文");
      retained = input.handle();
    }
    assert(!last.expired() && created == destroyed + 1);
    assert(active->routing == "filehelper" && active->body == "copied正文");
    retained.reset();
    assert(last.expired() && created == destroyed);
  }
  ++cases;
  assert(cases == 21);
  std::cout << "{\"cases\":" << cases << ",\"hidden_x8\":true,"
               "\"byte_preservation\":true,\"ownership_checked\":true,"
               "\"exception_cleanup\":true,\"guard_regions_intact\":true}\n";
}
