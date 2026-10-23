// Ghidra inferred pseudocode; requested=0x30c1cec
// entry=030c1cec end=030c1d9f

undefined8 * FUN_030c1cec(undefined8 *param_1,undefined8 *param_2)

{
  undefined8 uVar1;
  undefined8 uVar2;
  
  uVar1 = *param_2;
  param_1[1] = param_2[1];
  *param_1 = uVar1;
  *param_2 = 0;
  param_2[1] = 0;
  uVar1 = param_2[2];
  param_1[3] = param_2[3];
  param_1[2] = uVar1;
  param_2[2] = 0;
  param_2[3] = 0;
  FUN_0465d5c8(param_1 + 4,param_2 + 4);
  if (*(char *)((long)param_2 + 0x67) < '\0') {
    FUN_00018d20(param_1 + 10,param_2[10],param_2[0xb]);
  }
  else {
    uVar2 = param_2[0xb];
    uVar1 = param_2[10];
    param_1[0xc] = param_2[0xc];
    param_1[0xb] = uVar2;
    param_1[10] = uVar1;
  }
  param_1[0xd] = param_2[0xd];
  if (*(char *)((long)param_2 + 0x87) < '\0') {
    FUN_00018d20(param_1 + 0xe,param_2[0xe],param_2[0xf]);
  }
  else {
    uVar2 = param_2[0xf];
    uVar1 = param_2[0xe];
    param_1[0x10] = param_2[0x10];
    param_1[0xf] = uVar2;
    param_1[0xe] = uVar1;
  }
  param_1[0x11] = param_2[0x11];
  return param_1;
}


