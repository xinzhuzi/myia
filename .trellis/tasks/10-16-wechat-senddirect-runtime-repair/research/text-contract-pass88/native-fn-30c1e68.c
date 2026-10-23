// Ghidra inferred pseudocode; requested=0x30c1e68
// entry=030c1dec end=030c1eb7

undefined8 * FUN_030c1dec(undefined8 *param_1,undefined8 *param_2)

{
  long lVar1;
  long lVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  
  lVar1 = param_2[1];
  *param_1 = *param_2;
  param_1[1] = lVar1;
  if (lVar1 != 0) {
    *(long *)(lVar1 + 8) = *(long *)(lVar1 + 8) + 1;
  }
  lVar1 = param_2[3];
  param_1[2] = param_2[2];
  param_1[3] = lVar1;
  lVar2 = 0;
  if (lVar1 != 0) {
    lVar2 = *(long *)(lVar1 + 8);
    *(long *)(lVar1 + 8) = lVar2 + 1;
  }
  FUN_0465d5c8(lVar2,param_1 + 4,param_2 + 4);
  if (*(char *)((long)param_2 + 0x67) < '\0') {
    FUN_00018d20(param_1 + 10,param_2[10],param_2[0xb]);
  }
  else {
    uVar4 = param_2[0xb];
    uVar3 = param_2[10];
    param_1[0xc] = param_2[0xc];
    param_1[0xb] = uVar4;
    param_1[10] = uVar3;
  }
  param_1[0xd] = param_2[0xd];
  if (*(char *)((long)param_2 + 0x87) < '\0') {
    FUN_00018d20(param_1 + 0xe,param_2[0xe],param_2[0xf]);
  }
  else {
    uVar4 = param_2[0xf];
    uVar3 = param_2[0xe];
    param_1[0x10] = param_2[0x10];
    param_1[0xf] = uVar4;
    param_1[0xe] = uVar3;
  }
  param_1[0x11] = param_2[0x11];
  return param_1;
}


