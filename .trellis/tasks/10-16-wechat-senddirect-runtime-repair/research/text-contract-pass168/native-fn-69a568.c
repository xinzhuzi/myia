// Ghidra inferred pseudocode; requested=0x69a568
// entry=0069a568 end=0069a613

undefined8 * FUN_0069a568(undefined8 *param_1)

{
  undefined8 local_38 [2];
  undefined7 local_28;
  char cStack_21;
  
  FUN_00033e1c(local_38);
  FUN_0069a714(param_1,local_38);
  if (cStack_21 < '\0') {
    __ZdlPvm(local_38[0],CONCAT17(cStack_21,local_28) & 0x7fffffffffffffff);
  }
  *(undefined4 *)(param_1 + 0xc5) = 0;
  param_1[0xc2] = 0;
  param_1[0xc1] = 0;
  param_1[0xc4] = 0;
  param_1[0xc3] = 0;
  param_1[0xbe] = 0;
  param_1[0xbd] = 0;
  param_1[0xc0] = 0;
  param_1[0xbf] = 0;
  param_1[0xba] = 0;
  param_1[0xb9] = 0;
  param_1[0xbc] = 0;
  param_1[0xbb] = 0;
  *param_1 = &PTR_thunk_FUN_01be95a8_09eb28a8;
  *(undefined4 *)((long)param_1 + 0x68c) = 0;
  *(undefined8 *)((long)param_1 + 0x634) = 0;
  *(undefined8 *)((long)param_1 + 0x62c) = 0;
  *(undefined8 *)((long)param_1 + 0x644) = 0;
  *(undefined8 *)((long)param_1 + 0x63c) = 0;
  *(undefined8 *)((long)param_1 + 0x654) = 0;
  *(undefined8 *)((long)param_1 + 0x64c) = 0;
  *(undefined8 *)((long)param_1 + 0x664) = 0;
  *(undefined8 *)((long)param_1 + 0x65c) = 0;
  *(undefined8 *)((long)param_1 + 0x674) = 0;
  *(undefined8 *)((long)param_1 + 0x66c) = 0;
  *(undefined8 *)((long)param_1 + 0x684) = 0;
  *(undefined8 *)((long)param_1 + 0x67c) = 0;
  FUN_0002b2c0(param_1 + 0xd2);
  param_1[0xde] = 0;
  param_1[0xdd] = 0;
  param_1[0xe0] = 0;
  param_1[0xdf] = 0;
  param_1[0xda] = 0;
  param_1[0xd9] = 0;
  param_1[0xdc] = 0;
  param_1[0xdb] = 0;
  param_1[0xd6] = 0;
  param_1[0xd5] = 0;
  param_1[0xd8] = 0;
  param_1[0xd7] = 0;
  return param_1;
}


