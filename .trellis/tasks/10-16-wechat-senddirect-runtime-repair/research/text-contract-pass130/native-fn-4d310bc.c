// Ghidra inferred pseudocode; requested=0x4d310bc
// entry=04d310bc end=04d31153

undefined8 * FUN_04d310bc(undefined8 *param_1,long param_2)

{
  undefined4 uVar1;
  undefined8 *puVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  
  puVar2 = (undefined8 *)FUN_04cbd624(param_2);
  if (*(char *)((long)puVar2 + 0x17) < '\0') {
    FUN_00018d20(param_1,*puVar2,puVar2[1]);
  }
  else {
    uVar4 = puVar2[1];
    uVar3 = *puVar2;
    param_1[2] = puVar2[2];
    param_1[1] = uVar4;
    *param_1 = uVar3;
  }
  uVar1 = *(undefined4 *)(param_2 + 0xf4);
  *(undefined4 *)(param_1 + 3) = *(undefined4 *)(param_2 + 0x114);
  *(undefined4 *)((long)param_1 + 0x1c) = uVar1;
  param_1[4] = *(undefined8 *)(param_2 + 0x100);
  if (*(char *)(param_2 + 0x277) < '\0') {
    FUN_00018d20(param_1 + 5,*(undefined8 *)(param_2 + 0x260),*(undefined8 *)(param_2 + 0x268));
  }
  else {
    uVar4 = *(undefined8 *)(param_2 + 0x268);
    uVar3 = *(undefined8 *)(param_2 + 0x260);
    param_1[7] = *(undefined8 *)(param_2 + 0x270);
    param_1[6] = uVar4;
    param_1[5] = uVar3;
  }
  return param_1;
}


