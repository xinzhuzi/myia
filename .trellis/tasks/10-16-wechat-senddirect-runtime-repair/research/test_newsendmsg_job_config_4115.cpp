// Self-owned ABI/configuration integration; no target process or library.
#define main existing_operation_fixture_main
#include "test_newsendmsg_operation_4115.cpp"
#undef main
#include "newsendmsg_body_start_gate_4115.hpp"
#include "newsendmsg_job_config_4115.hpp"
#include <array>

extern "C" {
std::uint64_t job_abi_registers[5] = {};
void probe_job_config_words(const JobConfig*, std::uint64_t*);
}
JobHandle probe_job_full(JobGroup*, const JobConfig*, JobBody*, JobFinished*)
    __asm("_probe_job_full");
void invoke_config_body(JobBody*) __asm("_probe_job_body_erasure");

int main() {
  unsigned scenarios = 0;
  JobGroupConfigSnapshot group;
  group.defaults.name = "group name must not replace the request name";
  group.defaults.word18 = 0x1122334455667788ull;
  group.defaults.word20 = 0x8877665544332211ull;
  group.defaults.word28 = 0xfedcba9876543210ull;
  group.defaults.word30 = 37;
  group.defaults.flags = 0;
  {
    JobConfig requested;
    requested.name = "owned request name";
    const auto plan = resolve_job_launch(requested, group);
    assert(plan.config.name == requested.name);
    assert(plan.config.word18 == group.defaults.word18);
    assert(plan.config.word20 == group.defaults.word20);
    assert(plan.config.word28 == group.defaults.word28);
    assert(plan.config.word30 == 37 && plan.config.flags == 0);
    assert(plan.register_in_group && plan.action == JobInitialAction::start);
    ++scenarios;
  }
  {
    JobConfig requested;
    requested.word18 = 0x0123456789abcdefull;
    requested.word28 = 0x8000000100000001ull;
    requested.word30 = -2; // Only -1 inherits, not every negative value.
    requested.flags = 0x80000001u; // Only the exact sentinel inherits.
    const auto plan = resolve_job_launch(requested, group);
    assert(plan.config.word18 == requested.word18);
    assert(plan.config.word20 == group.defaults.word20);
    assert(plan.config.word28 == requested.word28);
    assert(plan.config.word30 == -2 && plan.config.flags == 0x80000001u);
    assert(plan.register_in_group && plan.action == JobInitialAction::deferred);
    ++scenarios;
  }
  {
    JobGroupConfigSnapshot empty;
    const auto plan = resolve_job_launch(JobConfig{}, empty);
    // Layout resolution never invents object identities or marks readiness.
    assert(!plan.config.word18 && !plan.config.word20 && !plan.config.word28);
    assert(plan.config.word30 == -1 && plan.config.flags == 0x80000000u);
    ++scenarios;
  }
  {
    // Independently enumerate the four low-bit choices and both group flags.
    const std::array<JobInitialAction, 4> actions = {
        JobInitialAction::start, JobInitialAction::deferred,
        JobInitialAction::start, JobInitialAction::deferred};
    const std::array<bool, 4> registered = {true, true, false, false};
    unsigned cases = 0;
    for (bool group_cancelled : {false, true}) {
      for (bool group_suppressed : {false, true}) {
        auto sample = group;
        sample.cancelled = group_cancelled;
        sample.word140 = group_suppressed ? 2u : 0u;
        for (std::uint32_t flags = 0; flags != 4; ++flags) {
          JobConfig requested;
          requested.flags = flags;
          const auto plan = resolve_job_launch(requested, sample);
          assert(plan.register_in_group == (!group_suppressed && registered[flags]));
          assert(plan.action == (group_cancelled ? JobInitialAction::cancel : actions[flags]));
          ++cases;
        }
      }
    }
    assert(cases == 16);
    ++scenarios;
  }
  {
    JobConfig requested;
    requested.name = std::string(256, 'x') + "\xe9\x85\x8d\xe7\xbd\xae";
    auto plan = resolve_job_launch(requested, group);
    assert(plan.config.name == requested.name);
    assert(plan.config.name.data() != requested.name.data());
    const auto copy = plan.config;
    plan.config.name.assign("changed");
    assert(copy.name == requested.name);
    ++scenarios;
  }
  {
    JobConfig requested;
    requested.word18 = group.defaults.word18;
    requested.word20 = group.defaults.word20;
    requested.word28 = group.defaults.word28;
    requested.word30 = -2;
    requested.flags = 0x80000003u;
    std::array<std::uint64_t, 5> words{};
    probe_job_config_words(&requested, words.data());
    assert(words[0] == requested.word18 && words[1] == requested.word20);
    assert(words[2] == requested.word28 && words[3] == 0xfffffffeull);
    assert(words[4] == 0x80000003ull);
    JobBody body = [] {};
    JobFinished finished = [](bool) {};
    unsigned marker = 0;
    auto* owned_group_marker = reinterpret_cast<JobGroup*>(&marker);
    LaunchJob launcher = &probe_job_full;
    const auto handle = launcher(owned_group_marker, &requested, &body, &finished);
    assert(!handle);
    assert(job_abi_registers[0] == reinterpret_cast<std::uintptr_t>(owned_group_marker));
    assert(job_abi_registers[1] == reinterpret_cast<std::uintptr_t>(&requested));
    assert(job_abi_registers[2] == reinterpret_cast<std::uintptr_t>(&body));
    assert(job_abi_registers[3] == reinterpret_cast<std::uintptr_t>(&finished));
    assert(job_abi_registers[4] != 0); // Nontrivial handle returns through x8.
    ++scenarios;
  }
  {
    Service service;
    JobConfig requested;
    requested.flags = 3;
    const auto plan = resolve_job_launch(requested, group);
    assert(!plan.register_in_group && plan.action == JobInitialAction::deferred);
    auto gate = std::make_shared<BodyStartGate>();
    std::unique_ptr<ResearchOperation> operation;
    unsigned native_job_cancel = 0;
    const auto before = factories.load();
    auto body = make_start_gated_body(gate, [&] {
      operation = std::make_unique<ResearchOperation>(
          functions, &service, &options, "route", "text", 4, deadline());
    });
    assert(gate->cancel_on_executor([&] { ++native_job_cancel; }) ==
           JobCancelAction::deferred_before_body);
    invoke_config_body(&body);
    assert(!operation && factories == before && native_job_cancel == 0);
    assert(gate->snapshot().left && !gate->snapshot().sent);
    ++scenarios;
  }
  {
    Service service;
    auto gate = std::make_shared<BodyStartGate>();
    std::unique_ptr<ResearchOperation> operation;
    auto body = make_start_gated_body(gate, [&] {
      operation = std::make_unique<ResearchOperation>(
          functions, &service, &options, "route", "text", 4, deadline());
    });
    invoke_config_body(&body);
    body = {};
    unsigned native_job_cancel = 0;
    assert(gate->cancel_on_executor([&] { ++native_job_cancel; }) ==
           JobCancelAction::after_body);
    assert(operation->cancel() && native_job_cancel == 0);
    assert(operation->snapshot().phase == OperationPhase::cancelled);
    assert(!operation->snapshot().sent);
    operation.reset();
    assert(service.last_state.expired());
    ++scenarios;
  }
  assert(bodies == 0 && requests == 0 && responses == 0);
  std::cout << "{\"scenarios\":" << scenarios << ",\"branch_cases\":16,"
               "\"config_bytes\":56,\"host_abi\":true,"
               "\"real_operation_component\":true,\"balanced_lifetime\":true,"
               "\"target_executed\":false,\"sent\":false}\n";
}
