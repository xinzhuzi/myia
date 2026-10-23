// Isolated fixture: mirror only native erased-function invocation instructions.
.text
.p2align 2
.globl _probe_job_body_erasure
_probe_job_body_erasure:
  ldr x0, [x0, #24]
  ldr x9, [x0]
  ldr x9, [x9, #48]
  br x9

.p2align 2
.globl _probe_job_finished_erasure
_probe_job_finished_erasure:
  ldr x0, [x0, #24]
  ldr x9, [x0]
  ldr x9, [x9, #48]
  // x1 preserves the address of the one-byte bool supplied by the caller.
  br x9
