// Research declarations only: no addresses, loading, object lookup or send entry.
#pragma once
#include "newsendmsg_job_abi_4115.hpp"
#include <cstdint>

namespace newsendmsg4115 {
struct Executor;
using ExecutorTicket = std::uint64_t;
// Executor vslot+0x10: x0=this, x1=nontrivial function storage, x0 return=ticket.
// The executor can move/clone the function. Submission is not body completion.
using SubmitExecutorTask = ExecutorTicket (*)(Executor*, JobBody*);
// Executor vslot+0x20 forwards to looper vslot+0x38; x1 is the FULL ticket.
// Native removal supplies no success/drain return value and is not an affinity test.
using RemoveExecutorTask = void (*)(Executor*, ExecutorTicket);
static_assert(sizeof(ExecutorTicket) == 8);
// Removing a queued ordinary task can destroy captures under the looper mutex.
// Capture destructors must not throw, reenter the executor, or invoke native control.
// In-flight execution, scheduling records and network requests remain separate.
} // namespace newsendmsg4115
