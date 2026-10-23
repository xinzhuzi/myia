// Ghidra inferred pseudocode; requested=0x69a714
// entry=0069a714 end=0069a807

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 * FUN_0069a714(undefined8 *param_1,undefined8 *param_2)

{
  undefined8 uVar1;
  undefined8 uVar2;
  
  param_1[2] = 0;
  param_1[1] = 0;
  param_1[4] = 0;
  param_1[3] = 0;
  param_1[6] = 0;
  param_1[5] = 0;
  param_1[8] = 0;
  param_1[7] = 0;
  param_1[10] = 0;
  param_1[9] = 0;
  param_1[0xc] = 0;
  param_1[0xb] = 0;
  param_1[0xe] = 0;
  param_1[0xd] = 0;
  *(undefined4 *)(param_1 + 0xf) = 0;
  uVar1 = _DAT_085276e0;
  *(undefined8 *)((long)param_1 + 0x84) = _UNK_085276e8;
  *(undefined8 *)((long)param_1 + 0x7c) = uVar1;
  *(undefined1 *)(param_1 + 0x1b) = 0;
  param_1[0x13] = 0;
  param_1[0x12] = 0;
  param_1[0x15] = 0;
  param_1[0x14] = 0;
  *(undefined1 *)(param_1 + 0x16) = 0;
  *param_1 = &PTR_thunk_FUN_0069b42c_09eb2650;
  param_1[0x1c] = 0;
  *(undefined4 *)(param_1 + 0x1d) = 0;
  FUN_0002b2c0(param_1 + 0x1e);
  *(undefined1 *)(param_1 + 0x21) = 0;
  param_1[0x23] = 0;
  param_1[0x24] = 0;
  param_1[0x22] = 0;
  FUN_0002b2c0(param_1 + 0x25);
  _bzero(param_1 + 0x28,0x440);
  FUN_04ce790c(param_1 + 0xa6);
  if (*(char *)((long)param_2 + 0x17) < '\0') {
    FUN_00018d20(param_1 + 0xb0,*param_2,param_2[1]);
  }
  else {
    uVar2 = param_2[1];
    uVar1 = *param_2;
    param_1[0xb2] = param_2[2];
    param_1[0xb1] = uVar2;
    param_1[0xb0] = uVar1;
  }
  *(undefined1 *)((long)param_1 + 0x5c7) = 0;
  param_1[0xb3] = 0;
  param_1[0xb5] = 0;
  param_1[0xb4] = 0;
  *(undefined1 *)(param_1 + 0xb6) = 0;
  *(undefined4 *)((long)param_1 + 0x7c) = 1;
  return param_1;
}


