// Ghidra inferred pseudocode; requested=0x66845d0
// entry=066845d0 end=0668462b

undefined8 * FUN_066845d0(undefined8 *param_1)

{
  FUN_066819f4(param_1 + 1);
  *param_1 = &PTR_FUN_09fb2f78;
  param_1[0x21] = 0;
  param_1[0x20] = 0;
  param_1[0x23] = 0;
  param_1[0x22] = 0;
  param_1[0x25] = 0;
  param_1[0x24] = 0;
  param_1[0x26] = 0;
  param_1[0x27] = 0x80000000ffffffff;
  *(undefined4 *)(param_1 + 0x28) = 0;
  *(undefined1 *)(param_1 + 0x1f) = 1;
  return param_1;
}


