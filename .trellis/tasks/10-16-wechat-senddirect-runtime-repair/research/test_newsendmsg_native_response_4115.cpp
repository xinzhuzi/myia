// Standalone native-response ownership fixture; never loads WeChat.
#include "newsendmsg_native_response_4115.hpp"
#include <cassert>
#include <cstring>
#include <iostream>
#include <string>

using namespace newsendmsg4115;
namespace {
struct FixtureResponse { std::string bytes; int cached = -1; bool valid = true; };
static_assert(sizeof(FixtureResponse) <= 56 && alignof(FixtureResponse) <= 8);
unsigned constructed = 0, destroyed = 0;
bool fail_copy = false, wrong_end = false;
void construct(void* target) { new (target) FixtureResponse; ++constructed; }
void copy(void* target, const void* source) {
  if (fail_copy) throw std::runtime_error("fixture copy failure");
  *static_cast<FixtureResponse*>(target) = *static_cast<const FixtureResponse*>(source);
}
void destroy(void* target) { static_cast<FixtureResponse*>(target)->~FixtureResponse(); ++destroyed; }
bool initialized(const void* target) { return static_cast<const FixtureResponse*>(target)->valid; }
std::int32_t size(void* target) {
  auto& response = *static_cast<FixtureResponse*>(target);
  response.cached = static_cast<int>(response.bytes.size());
  return response.cached;
}
std::byte* write(const void* target, std::byte* buffer) {
  const auto& response = *static_cast<const FixtureResponse*>(target);
  assert(response.cached == static_cast<int>(response.bytes.size()));
  std::memcpy(buffer, response.bytes.data(), response.bytes.size());
  return buffer + response.bytes.size() - (wrong_end ? 1 : 0);
}
const ResponseFunctions functions{construct, copy, destroy, initialized, size, write};
template <typename F> void fails(F action) {
  bool rejected = false;
  try { action(); } catch (const std::exception&) { rejected = true; }
  assert(rejected);
}
}
int main() {
  unsigned cases = 0;
  {
    FixtureResponse source{"\x08\x01", -1, true};
    NativeResponse owned(functions, &source);
    source.bytes.assign(300, 'z'); // Request storage can change after copy.
    const auto wire = owned.wire();
    assert(wire.size() == 2 && wire[0] == std::byte{8} && wire[1] == std::byte{1});
    ++cases;
  }
  for (unsigned mode = 0; mode < 4; ++mode) {
    FixtureResponse source{"abc", -1, mode != 0};
    if (mode == 1) source.bytes.clear();
    if (mode == 2) source.bytes.assign(16 * 1024 * 1024 + 1, 'x');
    wrong_end = mode == 3;
    fails([&] { NativeResponse owned(functions, &source); owned.wire(); });
    wrong_end = false;
    ++cases;
  }
  {
    FixtureResponse source{"abc", -1, true};
    fail_copy = true;
    fails([&] { NativeResponse owned(functions, &source); });
    fail_copy = false;
    ++cases;
  }
  fails([&] { NativeResponse owned(functions, nullptr); }); ++cases;
  auto incomplete = functions;
  incomplete.byte_size = nullptr;
  FixtureResponse source;
  fails([&] { NativeResponse owned(incomplete, &source); }); ++cases;
  assert(constructed == destroyed);
  std::cout << "{\"cases\":" << cases << ",\"balanced_lifetime\":true,"
               "\"cached_size_order\":true,\"wechat_loaded\":false,\"sent\":false}\n";
}
