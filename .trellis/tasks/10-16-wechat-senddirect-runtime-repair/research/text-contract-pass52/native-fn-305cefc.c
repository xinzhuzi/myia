// Ghidra inferred pseudocode; requested=0x305cefc
// entry=0305cefc end=0305cfdb

void FUN_0305cefc(undefined8 *param_1,long param_2)

{
  long lVar1;
  long *plVar2;
  undefined8 uVar3;
  undefined8 *puVar4;
  undefined8 uVar5;
  undefined1 auStack_38 [8];
  long *local_30;
  
  plVar2 = (long *)FUN_04669774();
  uVar3 = (**(code **)(*plVar2 + 0x18))();
  FUN_0305cff0(auStack_38,uVar3,param_2,param_2 + 0x60,param_2 + 0x78);
  FUN_066856fc(auStack_38);
  puVar4 = (undefined8 *)FUN_0305d198(auStack_38);
  *param_1 = *puVar4;
  if (*(char *)((long)puVar4 + 0x1f) < '\0') {
    FUN_00018d20(param_1 + 1,puVar4[1],puVar4[2]);
  }
  else {
    uVar5 = puVar4[2];
    uVar3 = puVar4[1];
    param_1[3] = puVar4[3];
    param_1[2] = uVar5;
    param_1[1] = uVar3;
  }
  lVar1 = puVar4[5];
  param_1[4] = puVar4[4];
  param_1[5] = lVar1;
  if (lVar1 != 0) {
    *(long *)(lVar1 + 8) = *(long *)(lVar1 + 8) + 1;
  }
  if (local_30 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_30[1];
    local_30[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_30 + 0x10))(local_30);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_30);
    }
  }
  return;
}


