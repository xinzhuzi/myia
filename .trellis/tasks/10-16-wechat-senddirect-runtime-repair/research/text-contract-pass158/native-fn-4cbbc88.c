// Ghidra inferred pseudocode; requested=0x4cbbc88
// entry=04cbbc88 end=04cbbd1f

void FUN_04cbbc88(undefined8 *param_1,long param_2)

{
  int iVar1;
  ulong uVar2;
  undefined8 uVar3;
  
  iVar1 = FUN_04cbd748();
  if ((iVar1 == 0) &&
     ((((uVar2 = FUN_04bb3974(param_2 + 0x18), (uVar2 & 1) != 0 ||
        (uVar2 = FUN_04bb3974(param_2 + 0x30), (uVar2 & 1) != 0)) ||
       (uVar2 = FUN_04bb3a88(param_2 + 0x18), (uVar2 & 1) != 0)) ||
      (iVar1 = FUN_04bb3a88(param_2 + 0x30), iVar1 != 0)))) {
    FUN_04cbd8fc(param_1,param_2);
    return;
  }
  if (-1 < *(char *)(param_2 + 0x2f)) {
    uVar3 = *(undefined8 *)(param_2 + 0x18);
    param_1[1] = *(undefined8 *)(param_2 + 0x20);
    *param_1 = uVar3;
    param_1[2] = *(undefined8 *)(param_2 + 0x28);
    return;
  }
  FUN_00018d20(param_1,*(undefined8 *)(param_2 + 0x18),*(undefined8 *)(param_2 + 0x20));
  return;
}


