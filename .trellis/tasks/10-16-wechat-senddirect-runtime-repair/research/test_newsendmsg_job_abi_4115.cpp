// Standalone host ABI fixture. Never links, loads or invokes WeChat.
#include "newsendmsg_job_abi_4115.hpp"
#include <cassert>
#include <cstdint>
#include <iostream>

namespace newsendmsg4115 {
struct Job {
  explicit Job(int* value) : destroyed(value) {}
  ~Job() { ++*destroyed; }
  int* destroyed;
};
struct JobGroup {};
struct JobConfig {};
} // namespace newsendmsg4115

using namespace newsendmsg4115;
extern "C" {
std::uintptr_t job_abi_registers[5]{};
}

// Assembly-backed declarations retain C++ return semantics and fixed symbols.
JobHandle probe_full(JobGroup*, const JobConfig*, JobBody*, JobFinished*)
    __asm("_probe_job_full");
JobHandle probe_simple(JobGroup*, const JobConfig*, JobBody*)
    __asm("_probe_job_simple");

static JobGroup* expected_group;
static const JobConfig* expected_config;
static JobBody* expected_body;
static JobFinished* expected_finished;
static int destroyed = 0;

JobHandle owned_fixture(JobGroup* group, const JobConfig* config,
                        JobBody* body, JobFinished* finished) {
  assert(group == expected_group && config == expected_config);
  assert(body == expected_body && finished == expected_finished);
  JobBody retained_body = *body;
  JobFinished retained_finished = *finished;
  retained_body();
  retained_finished(true);
  return std::make_shared<Job>(&destroyed);
}

int main() {
  JobGroup group;
  JobConfig config;
  int body_calls = 0;
  int finish_calls = 0;
  bool finish_value = false;
  JobBody body = [&] { ++body_calls; };
  JobFinished finished = [&](bool value) {
    ++finish_calls;
    finish_value = value;
  };

  LaunchJob full = probe_full;
  JobHandle empty = full(&group, &config, &body, &finished);
  assert(!empty);
  assert(job_abi_registers[0] == reinterpret_cast<std::uintptr_t>(&group));
  assert(job_abi_registers[1] == reinterpret_cast<std::uintptr_t>(&config));
  assert(job_abi_registers[2] == reinterpret_cast<std::uintptr_t>(&body));
  assert(job_abi_registers[3] == reinterpret_cast<std::uintptr_t>(&finished));
  assert(job_abi_registers[4] == reinterpret_cast<std::uintptr_t>(&empty));

  LaunchJobWithoutFinished simple = probe_simple;
  JobHandle second_empty = simple(&group, &config, &body);
  assert(!second_empty);
  assert(job_abi_registers[0] == reinterpret_cast<std::uintptr_t>(&group));
  assert(job_abi_registers[1] == reinterpret_cast<std::uintptr_t>(&config));
  assert(job_abi_registers[2] == reinterpret_cast<std::uintptr_t>(&body));
  assert(job_abi_registers[4] == reinterpret_cast<std::uintptr_t>(&second_empty));
  assert(body_calls == 0 && finish_calls == 0);

  expected_group = &group;
  expected_config = &config;
  expected_body = &body;
  expected_finished = &finished;
  LaunchJob owned = owned_fixture;
  JobHandle handle = owned(&group, &config, &body, &finished);
  assert(handle && body_calls == 1);
  assert(finish_calls == 1 && finish_value);
  assert(destroyed == 0);
  std::weak_ptr<Job> weak = handle;
  JobHandle copy = handle;
  handle.reset();
  assert(!weak.expired() && destroyed == 0);
  copy.reset();
  assert(weak.expired() && destroyed == 1);
  weak.reset();
  std::cout << "{\"cases\":5,\"hidden_x8\":true,"
               "\"arguments_match\":true,\"ownership_checked\":true}\n";
}
