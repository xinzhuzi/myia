// Reads owned C++ objects only, using the frozen native configuration offsets.
.text
.p2align 2
.globl _probe_job_config_words
_probe_job_config_words:
  ldp x8, x9, [x0, #0x18]
  stp x8, x9, [x1]
  ldr x8, [x0, #0x28]
  str x8, [x1, #0x10]
  ldr w8, [x0, #0x30]
  ldr w9, [x0, #0x34]
  stp x8, x9, [x1, #0x18]
  ret
