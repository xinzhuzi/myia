// Ghidra inferred pseudocode; requested=0x30c2de4
// entry=030c2de4 end=030c2e87

undefined8 * FUN_030c2de4(undefined8 *param_1,long param_2)

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
  *param_1 = &PTR_thunk_FUN_030c2fe4_09de8268;
  param_1[1] = 0;
  FUN_0465bdac(param_1 + 0xf);
  FUN_0465bdcc(param_1 + 0x15);
  *(undefined4 *)((long)param_1 + 0xc) = *(undefined4 *)(param_2 + 0x10);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 3,param_2 + 0x18);
  *(bool *)((long)param_1 + 0x31) = *(int *)(param_2 + 0xc) != 0;
  *(undefined1 *)((long)param_1 + 0x33) = *(undefined1 *)(param_2 + 0x30);
  *(undefined4 *)(param_1 + 2) = 1;
  return param_1;
}


