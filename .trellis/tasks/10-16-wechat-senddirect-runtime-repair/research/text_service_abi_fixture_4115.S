// Own fixture only: record x0/x1/x8, return a 48-byte nontrivial value.
.text
.p2align 2
.globl _probe_text_service_submit
_probe_text_service_submit:
  adrp x9, _text_service_abi_arguments@PAGE
  add x9, x9, _text_service_abi_arguments@PAGEOFF
  stp x0, x1, [x9]
  str x8, [x9, #16]
  mov w10, #0x3344
  movk w10, #0x1122, lsl #16
  mov w11, #0x7788
  movk w11, #0x5566, lsl #16
  stp w10, w11, [x8]
  stp xzr, xzr, [x8, #8]
  stp xzr, xzr, [x8, #24]
  str xzr, [x8, #40]
  ret
