// Ghidra inferred pseudocode; requested=0x30d69a0
// entry=030d692c end=030d6a4b

void FUN_030d692c(undefined8 *param_1,long *param_2,long *param_3)

{
  long *plVar1;
  long lVar2;
  long local_50;
  long *local_48;
  undefined8 local_40;
  long *local_38;
  undefined8 local_30;
  long *local_28;
  
  local_50 = *param_3;
  local_30 = *(undefined8 *)(local_50 + 0x18);
  local_28 = *(long **)(local_50 + 0x20);
  if (local_28 != (long *)0x0) {
    local_28[1] = local_28[1] + 1;
    local_50 = *param_3;
  }
  local_40 = *(undefined8 *)(local_50 + 0x28);
  local_38 = *(long **)(local_50 + 0x30);
  if (local_38 != (long *)0x0) {
    local_38[1] = local_38[1] + 1;
    local_50 = *param_3;
  }
  param_1[3] = &SUB_aaaaaaaaaaaaaaaa;
  param_1[2] = &SUB_aaaaaaaaaaaaaaaa;
  param_1[5] = &SUB_aaaaaaaaaaaaaaaa;
  param_1[4] = &SUB_aaaaaaaaaaaaaaaa;
  param_1[1] = &SUB_aaaaaaaaaaaaaaaa;
  *param_1 = &SUB_aaaaaaaaaaaaaaaa;
  local_48 = (long *)param_3[1];
  if (local_48 != (long *)0x0) {
    local_48[1] = local_48[1] + 1;
  }
  (**(code **)(*param_2 + 0xd8))(param_2,&local_50);
  plVar1 = local_48;
  if (local_48 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_48[1];
    local_48[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_48 + 0x10))(local_48);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = local_38;
  if (local_38 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_38[1];
    local_38[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_38 + 0x10))(local_38);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = local_28;
  if (local_28 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_28[1];
    local_28[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_28 + 0x10))(local_28);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  return;
}


