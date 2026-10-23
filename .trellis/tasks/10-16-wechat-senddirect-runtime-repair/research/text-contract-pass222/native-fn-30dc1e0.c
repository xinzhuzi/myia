// Ghidra inferred pseudocode; requested=0x30dc1e0
// entry=030dc1e0 end=030dc26b

void FUN_030dc1e0(undefined8 param_1,undefined8 param_2,undefined8 *param_3)

{
  long *plVar1;
  long lVar2;
  undefined8 uVar3;
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
  uVar3 = FUN_030dc6fc(&local_38);
  FUN_00f57630(param_1,uVar3);
  plVar1 = local_30;
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


