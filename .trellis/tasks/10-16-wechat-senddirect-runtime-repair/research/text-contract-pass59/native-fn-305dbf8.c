// Ghidra inferred pseudocode; requested=0x305dbf8
// entry=0305dbf8 end=0305dc9b

undefined8 * FUN_0305dbf8(undefined8 *param_1,long param_2)

{
  *(undefined4 *)(param_1 + 2) = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  param_1[5] = 0;
  *(undefined4 *)(param_1 + 6) = 0x1010000;
  param_1[8] = 0;
  param_1[9] = 0;
  param_1[7] = 0;
  param_1[0xd] = 0;
  *(undefined1 *)(param_1 + 0xe) = 0;
  *(undefined4 *)((long)param_1 + 0x74) = 0;
  *param_1 = &PTR_thunk_FUN_0305de10_09de5860;
  param_1[1] = 0;
  FUN_050ef4f4(param_1 + 0xf);
  FUN_050ef52c(param_1 + 0x1b);
  *(undefined4 *)((long)param_1 + 0xc) = *(undefined4 *)(param_2 + 0x10);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 3,param_2 + 0x18);
  *(bool *)((long)param_1 + 0x31) = *(int *)(param_2 + 0xc) != 0;
  *(undefined1 *)((long)param_1 + 0x33) = *(undefined1 *)(param_2 + 0x30);
  *(undefined4 *)(param_1 + 2) = 1;
  return param_1;
}


