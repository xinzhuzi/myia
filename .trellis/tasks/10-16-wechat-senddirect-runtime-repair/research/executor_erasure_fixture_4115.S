// Host ABI probes only; passed objects/functions always belong to this fixture.
.text
.p2align 2
.globl _probe_executor_submit
_probe_executor_submit:
  ldr x9, [x0]
  ldr x9, [x9, #16]
  // Preserve x0=this and x1=owned nontrivial function storage; x0 returns ticket.
  br x9

.p2align 2
.globl _probe_executor_remove
_probe_executor_remove:
  ldr x9, [x0]
  ldr x9, [x9, #32]
  // Preserve every bit of the 64-bit ticket in x1. No boolean result is used.
  br x9
