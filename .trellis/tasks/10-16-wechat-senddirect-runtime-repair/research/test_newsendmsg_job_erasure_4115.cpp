// Standalone callback ABI fixture; no WeChat loading or native addresses.
#include "newsendmsg_job_abi_4115.hpp"
#include <array>
#include <cassert>
#include <cstdint>
#include <cstring>
#include <iostream>

using namespace newsendmsg4115;
void probe_body(JobBody*) __asm("_probe_job_body_erasure");
void probe_finished(JobFinished*, const bool*) __asm("_probe_job_finished_erasure");

template <class Function>
std::uintptr_t erased_address(const Function& value) {
  std::uintptr_t address = 0;
  // Exact layout under test: native reads the erased pointer at +0x18.
  std::memcpy(&address, reinterpret_cast<const char*>(&value) + 24, sizeof(address));
  return address;
}

int main() {
  static_assert(sizeof(bool) == 1);
  const std::array<std::uintptr_t, 4> padding{1, 2, 3, 4};
  int body_calls = 0;
  auto small_body = [&body_calls] { ++body_calls; };
  auto large_body = [padding, &body_calls] { body_calls += padding[3]; };
  static_assert(sizeof(small_body) <= 24 && sizeof(large_body) > 24);
  JobBody inline_body = small_body;
  JobBody heap_body = large_body;
  assert(erased_address(inline_body) == reinterpret_cast<std::uintptr_t>(&inline_body));
  assert(erased_address(heap_body) != 0);
  assert(erased_address(heap_body) != reinterpret_cast<std::uintptr_t>(&heap_body));
  probe_body(&inline_body);
  assert(body_calls == 1);
  probe_body(&heap_body);
  assert(body_calls == 5);

  int inline_calls = 0;
  int true_values = 0;
  auto small_finished = [&inline_calls, &true_values](bool value) {
    ++inline_calls;
    true_values += value;
  };
  int heap_calls = 0;
  int weighted_values = 0;
  auto large_finished = [padding, &heap_calls, &weighted_values](bool value) {
    ++heap_calls;
    weighted_values += padding[0] + value;
  };
  static_assert(sizeof(small_finished) <= 24 && sizeof(large_finished) > 24);
  JobFinished inline_finished = small_finished;
  JobFinished heap_finished = large_finished;
  assert(erased_address(inline_finished) ==
         reinterpret_cast<std::uintptr_t>(&inline_finished));
  assert(erased_address(heap_finished) != 0);
  assert(erased_address(heap_finished) != reinterpret_cast<std::uintptr_t>(&heap_finished));
  bool value = true;
  probe_finished(&inline_finished, &value);
  value = false;
  probe_finished(&inline_finished, &value);
  assert(inline_calls == 2 && true_values == 1);
  value = true;
  probe_finished(&heap_finished, &value);
  value = false;
  probe_finished(&heap_finished, &value);
  assert(heap_calls == 2 && weighted_values == 3);
  std::cout << "{\"cases\":4,\"inline_and_heap\":true,"
               "\"raw_virtual_invoke\":true,\"bool_reference_checked\":true}\n";
}
