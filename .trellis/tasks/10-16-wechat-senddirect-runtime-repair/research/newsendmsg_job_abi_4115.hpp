// Research ABI only. No addresses, loader, debugger, scheduler or send entry.
// Actual group/config identity, thread affinity and full drain remain unproved.
#pragma once
#include <functional>
#include <memory>

namespace newsendmsg4115 {
struct Job;
struct JobGroup;
struct JobConfig;
using JobHandle = std::shared_ptr<Job>;
using JobBody = std::function<void()>;
using JobFinished = std::function<void(bool)>;

// The nontrivial return uses hidden x8 on this host's Apple ARM64 ABI.
// x0=group, x1=config, x2=body, x3=finished; x8=16-byte result storage.
// Body/finished may be moved or cloned; they are not integer/pointer values.
using LaunchJob = JobHandle (*)(JobGroup*, const JobConfig*, JobBody*, JobFinished*);
// Native forwarding wrapper has only x0/group, x1/config, x2/body, plus x8.
using LaunchJobWithoutFinished = JobHandle (*)(JobGroup*, const JobConfig*, JobBody*);

static_assert(sizeof(JobHandle) == 16 && alignof(JobHandle) == 8);
static_assert(sizeof(JobBody) == 32 && alignof(JobBody) == 8);
static_assert(sizeof(JobFinished) == 32 && alignof(JobFinished) == 8);
} // namespace newsendmsg4115
