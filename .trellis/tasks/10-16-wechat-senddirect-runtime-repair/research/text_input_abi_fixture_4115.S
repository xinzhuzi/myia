// Owned fixture only: record hidden result storage and return an empty pair.
.text
.p2align 2
.globl _probe_text_input_create
_probe_text_input_create:
  adrp x9, _text_input_abi_result@PAGE
  add x9, x9, _text_input_abi_result@PAGEOFF
  str x8, [x9]
  stp xzr, xzr, [x8]
  ret
