// Local fixture only: capture registers and return an empty shared_ptr via x8.
.text
.p2align 2
.globl _probe_job_full
_probe_job_full:
  adrp x9, _job_abi_registers@PAGE
  add x9, x9, _job_abi_registers@PAGEOFF
  stp x0, x1, [x9]
  stp x2, x3, [x9, #16]
  str x8, [x9, #32]
  stp xzr, xzr, [x8]
  ret

.p2align 2
.globl _probe_job_simple
_probe_job_simple:
  adrp x9, _job_abi_registers@PAGE
  add x9, x9, _job_abi_registers@PAGEOFF
  stp x0, x1, [x9]
  stp x2, xzr, [x9, #16]
  str x8, [x9, #32]
  stp xzr, xzr, [x8]
  ret
