// Ghidra inferred pseudocode; requested=0x4c7d950
// entry=04c7d950 end=04c7db47

void FUN_04c7d950(undefined8 *param_1,undefined8 param_2,long *param_3)

{
  ulong uVar1;
  long lVar2;
  undefined4 uVar3;
  undefined8 uVar4;
  long *plVar5;
  long *plVar6;
  undefined1 *local_80;
  long *local_78;
  long local_70;
  long *local_68;
  undefined8 local_60;
  long *local_58;
  undefined1 *local_50;
  long *plStack_48;
  
  local_50 = &SUB_aaaaaaaaaaaaaaaa;
  plStack_48 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_00d6bd24(&local_50,&local_60);
  lVar2 = *param_3;
  uVar4 = *(undefined8 *)(lVar2 + 0x510);
  plVar6 = *(long **)(lVar2 + 0x518);
  if (plVar6 != (long *)0x0) {
    lVar2 = plVar6[1];
    plVar6[1] = lVar2 + 1;
  }
  local_60 = uVar4;
  local_58 = plVar6;
  lVar2 = FUN_012ee8e4(lVar2,uVar4);
  uVar1 = *(ulong *)(lVar2 + 8);
  if (-1 < (char)*(byte *)(lVar2 + 0x17)) {
    uVar1 = (ulong)*(byte *)(lVar2 + 0x17);
  }
  uVar3 = 0x2a;
  if (uVar1 != 0) {
    uVar3 = 0x42;
  }
  *(undefined4 *)(local_50 + 0xe4) = uVar3;
  if (plVar6 != (long *)0x0) {
    plVar6[1] = plVar6[1] + 1;
  }
  *(undefined8 *)(local_50 + 0x5c8) = uVar4;
  plVar5 = *(long **)(local_50 + 0x5d0);
  *(long **)(local_50 + 0x5d0) = plVar6;
  if (plVar5 != (long *)0x0) {
    LOAcquire();
    lVar2 = plVar5[1];
    plVar5[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*plVar5 + 0x10))(plVar5);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
    }
  }
  local_70 = *param_3;
  local_68 = (long *)param_3[1];
  if (local_68 != (long *)0x0) {
    local_68[1] = local_68[1] + 1;
  }
  local_80 = local_50;
  local_78 = plStack_48;
  lVar2 = 0;
  if (plStack_48 != (long *)0x0) {
    lVar2 = plStack_48[1];
    plStack_48[1] = lVar2 + 1;
  }
  FUN_04c6c5d0(lVar2,param_2,&local_70,&local_80);
  plVar6 = local_78;
  if (local_78 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_78[1];
    local_78[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_78 + 0x10))(local_78);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  plVar6 = local_68;
  if (local_68 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_68[1];
    local_68[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_68 + 0x10))(local_68);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  plVar6 = local_58;
  param_1[1] = plStack_48;
  *param_1 = local_50;
  local_50 = (undefined1 *)0x0;
  plStack_48 = (long *)0x0;
  if (local_58 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_58[1];
    local_58[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_58 + 0x10))(local_58);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  plVar6 = plStack_48;
  if (plStack_48 != (long *)0x0) {
    LOAcquire();
    lVar2 = plStack_48[1];
    plStack_48[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*plStack_48 + 0x10))(plStack_48);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  return;
}


