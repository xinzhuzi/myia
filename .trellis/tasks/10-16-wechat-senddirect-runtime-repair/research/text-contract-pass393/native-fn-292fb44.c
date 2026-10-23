// Ghidra inferred pseudocode; requested=0x292fb44
// entry=0292fb44 end=0292fc13

undefined8 * FUN_0292fb44(undefined8 *param_1,undefined8 *param_2)

{
  long lVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  
  lVar1 = param_2[1];
  *param_1 = *param_2;
  param_1[1] = lVar1;
  if (lVar1 != 0) {
    *(long *)(lVar1 + 8) = *(long *)(lVar1 + 8) + 1;
  }
  if (*(char *)((long)param_2 + 0x27) < '\0') {
    FUN_00018d20(param_1 + 2,param_2[2],param_2[3]);
  }
  else {
    uVar3 = param_2[3];
    uVar2 = param_2[2];
    param_1[4] = param_2[4];
    param_1[3] = uVar3;
    param_1[2] = uVar2;
  }
  lVar1 = param_2[6];
  param_1[5] = param_2[5];
  param_1[6] = lVar1;
  if (lVar1 != 0) {
    *(long *)(lVar1 + 8) = *(long *)(lVar1 + 8) + 1;
  }
  if (*(char *)((long)param_2 + 0x4f) < '\0') {
    FUN_00018d20(param_1 + 7,param_2[7],param_2[8]);
  }
  else {
    uVar3 = param_2[8];
    uVar2 = param_2[7];
    param_1[9] = param_2[9];
    param_1[8] = uVar3;
    param_1[7] = uVar2;
  }
  *(undefined4 *)(param_1 + 10) = *(undefined4 *)(param_2 + 10);
  lVar1 = param_2[0xc];
  param_1[0xb] = param_2[0xb];
  param_1[0xc] = lVar1;
  if (lVar1 != 0) {
    *(long *)(lVar1 + 8) = *(long *)(lVar1 + 8) + 1;
  }
  return param_1;
}


