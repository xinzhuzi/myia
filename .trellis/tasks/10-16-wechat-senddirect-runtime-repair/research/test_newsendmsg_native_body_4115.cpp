#include "newsendmsg_native_body_4115.hpp"
#include <cassert>
#include <cstring>
#include <iostream>
#include <type_traits>
using namespace newsendmsg4115;

static unsigned constructed = 0, parsed = 0, destroyed = 0;
static unsigned char* last_body = nullptr;
static unsigned mode = 0;
static const unsigned char wire[] = {0x08,0x01,0x12,0x0a,0x0a,0x02,0x0a,0,0x18,0,0x20,0,0x28,0};
static void construct(void* body) {
  assert(reinterpret_cast<std::uintptr_t>(body) % 8 == 0);
  std::memset(body, 0x45, 48);
  last_body = static_cast<unsigned char*>(body);
  ++constructed;
}
static bool parse(void* body, const void* bytes, std::int32_t size) {
  assert(body == last_body && last_body[47] == 0x45);
  assert(size == sizeof(wire) && std::memcmp(bytes, wire, sizeof(wire)) == 0);
  ++parsed;
  if (mode == 2) throw std::runtime_error("fixture parser error");
  last_body[47] = 0x46; // Model partially allocated state even on failure.
  return mode == 0;
}
static void destroy(void* body) {
  assert(body == last_body);
  assert(last_body[47] == 0x45 || last_body[47] == 0x46);
  std::memset(body, 0, 48);
  ++destroyed;
}
int main() {
  static_assert(!std::is_copy_constructible_v<NativeBody>);
  static_assert(!std::is_move_constructible_v<NativeBody>);
  const BodyFunctions functions{construct, parse, destroy};
  {
    NativeBody body(functions, wire, sizeof(wire));
    assert(body.get() == last_body && destroyed == 0);
  }
  assert(constructed == 1 && parsed == 1 && destroyed == 1);
  for (mode = 1; mode <= 2; ++mode) {
    bool rejected = false;
    try { NativeBody body(functions, wire, sizeof(wire)); }
    catch (const std::runtime_error&) { rejected = true; }
    assert(rejected && constructed == destroyed);
  }
  for (std::size_t size : {std::size_t{0}, std::size_t{16U*1024U*1024U+1U}}) {
    bool rejected = false;
    try { NativeBody body(functions, wire, size); }
    catch (const std::invalid_argument&) { rejected = true; }
    assert(rejected && constructed == 3 && destroyed == 3);
  }
  for (unsigned index = 0; index < 3; ++index) {
    BodyFunctions incomplete = functions;
    if (index == 0) incomplete.construct = nullptr;
    if (index == 1) incomplete.parse = nullptr;
    if (index == 2) incomplete.destroy = nullptr;
    bool rejected = false;
    try { NativeBody body(incomplete, wire, sizeof(wire)); }
    catch (const std::invalid_argument&) { rejected = true; }
    assert(rejected && constructed == 3);
  }
  bool rejected = false;
  try { NativeBody body(functions, nullptr, sizeof(wire)); }
  catch (const std::invalid_argument&) { rejected = true; }
  assert(rejected && constructed == 3);
  std::cout << "{\"cases\":9,\"constructed\":" << constructed
            << ",\"destroyed\":" << destroyed
            << ",\"parse_failures_cleaned\":true,\"wechat_loaded\":false,\"sent\":false}\n";
}
