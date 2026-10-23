// Ghidra inferred pseudocode; requested=0x3189980
// entry=03189980 end=03189a53

void FUN_03189980(undefined8 *param_1,undefined8 param_2,undefined8 *param_3)

{
  long *plVar1;
  long lVar2;
  undefined8 *puVar3;
  undefined8 uVar4;
  undefined8 uVar5;
  undefined8 local_38;
  long *local_30;
  undefined8 local_28;
  
  local_38 = *param_3;
  local_30 = (long *)param_3[1];
  lVar2 = 0;
  if (local_30 != (long *)0x0) {
    lVar2 = local_30[1];
    local_30[1] = lVar2 + 1;
  }
  local_28 = 0;
  FUN_066856fc(lVar2,&local_38);
  puVar3 = (undefined8 *)FUN_0312bae8(&local_38);
  *param_1 = *puVar3;
  if (*(char *)((long)puVar3 + 0x1f) < '\0') {
    FUN_00018d20(param_1 + 1,puVar3[1],puVar3[2]);
  }
  else {
    uVar5 = puVar3[2];
    uVar4 = puVar3[1];
    param_1[3] = puVar3[3];
    param_1[2] = uVar5;
    param_1[1] = uVar4;
  }
  plVar1 = local_30;
  lVar2 = puVar3[5];
  param_1[4] = puVar3[4];
  param_1[5] = lVar2;
  if (lVar2 != 0) {
    *(long *)(lVar2 + 8) = *(long *)(lVar2 + 8) + 1;
  }
  if (local_30 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_30[1];
    local_30[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_30 + 0x10))(local_30);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  return;
}


