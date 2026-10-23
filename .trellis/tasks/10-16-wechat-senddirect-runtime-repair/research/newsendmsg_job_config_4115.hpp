// Frozen 4.1.15 research ABI. No addresses, object lookup or native execution.
#pragma once
#include "newsendmsg_job_abi_4115.hpp"
#include <cstddef>
#include <cstdint>
#include <string>
#include <type_traits>
#include <utility>

namespace newsendmsg4115 {
// The three machine words remain borrowed values. Their layout does not prove
// the identity, lifetime or thread safety of the native objects they designate.
struct JobConfig {
  std::string name;
  std::uintptr_t word18 = 0;
  std::uintptr_t word20 = 0;
  std::uintptr_t word28 = 0;
  std::int32_t word30 = -1;
  std::uint32_t flags = 0x80000000u;
};
static_assert(std::is_standard_layout<JobConfig>::value);
static_assert(sizeof(std::string) == 24 && alignof(std::string) == 8);
static_assert(sizeof(JobConfig) == 0x38 && alignof(JobConfig) == 8);
static_assert(offsetof(JobConfig, name) == 0);
static_assert(offsetof(JobConfig, word18) == 0x18);
static_assert(offsetof(JobConfig, word20) == 0x20);
static_assert(offsetof(JobConfig, word28) == 0x28);
static_assert(offsetof(JobConfig, word30) == 0x30);
static_assert(offsetof(JobConfig, flags) == 0x34);

// Owned representation, NOT a native group layout. A live group could change
// between configuration resolution, registration and the cancellation query.
struct JobGroupConfigSnapshot {
  JobConfig defaults;
  std::uint32_t word140 = 0;
  bool cancelled = false;
};
enum class JobInitialAction { start, deferred, cancel };
struct ResolvedJobLaunch {
  JobConfig config;
  bool register_in_group;
  JobInitialAction action;
};

// Implements only the field/branch contract of 0x66846b8. This function does
// not inspect a real group, register a Job, start one or perform cancellation.
inline ResolvedJobLaunch resolve_job_launch(
    const JobConfig& requested, const JobGroupConfigSnapshot& group) {
  JobConfig config = requested;
  if (!config.word18) config.word18 = group.defaults.word18;
  if (!config.word20) config.word20 = group.defaults.word20;
  if (!config.word28) config.word28 = group.defaults.word28;
  if (config.word30 == -1) config.word30 = group.defaults.word30;
  // Equality, not a sign-bit mask: explicit flags with bit 31 are preserved.
  if (config.flags == 0x80000000u) config.flags = group.defaults.flags;
  const bool register_in_group = ((group.word140 | config.flags) & 2u) == 0;
  const JobInitialAction action = group.cancelled ? JobInitialAction::cancel :
      ((config.flags & 1u) ? JobInitialAction::deferred : JobInitialAction::start);
  return {std::move(config), register_in_group, action};
}
} // namespace newsendmsg4115
