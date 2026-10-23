// Ghidra inferred pseudocode; requested=0x30d66c0
// entry=030d66c0 end=030d68e7

void FUN_030d66c0(int *param_1,long *param_2,long *param_3)

{
  long *plVar1;
  long lVar2;
  long local_80;
  long *plStack_78;
  long local_70;
  long *local_68;
  undefined1 *local_60;
  long *local_58;
  undefined8 local_50;
  long *local_48;
  long local_40;
  long *local_38;
  
  lVar2 = *param_3;
  local_40 = *(long *)(lVar2 + 0x18);
  local_38 = *(long **)(lVar2 + 0x20);
  if (local_38 != (long *)0x0) {
    local_38[1] = local_38[1] + 1;
    lVar2 = *param_3;
  }
  local_50 = *(undefined8 *)(lVar2 + 0x28);
  local_48 = *(long **)(lVar2 + 0x30);
  if (local_48 != (long *)0x0) {
    local_48[1] = local_48[1] + 1;
    lVar2 = *param_3;
  }
  local_60 = &SUB_aaaaaaaaaaaaaaaa;
  local_58 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  if ((*(long *)(lVar2 + 8) == 0) ||
     (local_60 = (undefined1 *)
                 ___dynamic_cast(*(long *)(lVar2 + 8),&PTR_DAT_09c37aa0,&PTR_DAT_09eb2580,0),
     local_60 == (undefined1 *)0x0)) {
    local_60 = (undefined1 *)0x0;
    local_58 = (long *)0x0;
  }
  else {
    local_58 = *(long **)(lVar2 + 0x10);
    if (local_58 != (long *)0x0) {
      local_58[1] = local_58[1] + 1;
      lVar2 = *param_3;
    }
  }
  *(undefined1 **)(param_1 + 6) = &SUB_aaaaaaaaaaaaaaaa;
  *(undefined1 **)(param_1 + 4) = &SUB_aaaaaaaaaaaaaaaa;
  *(undefined1 **)(param_1 + 10) = &SUB_aaaaaaaaaaaaaaaa;
  *(undefined1 **)(param_1 + 8) = &SUB_aaaaaaaaaaaaaaaa;
  *(undefined1 **)(param_1 + 2) = &SUB_aaaaaaaaaaaaaaaa;
  *(undefined1 **)param_1 = &SUB_aaaaaaaaaaaaaaaa;
  local_68 = (long *)param_3[1];
  if (local_68 != (long *)0x0) {
    local_68[1] = local_68[1] + 1;
  }
  local_70 = lVar2;
  (**(code **)(*param_2 + 0xd0))(param_1,param_2,&local_70);
  plVar1 = local_68;
  if (local_68 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_68[1];
    local_68[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_68 + 0x10))(local_68);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = local_38;
  if ((*param_1 != 0 || param_1[1] != 0) && (*(int *)(local_40 + 0x118) == 1)) {
    local_80 = local_40;
    plStack_78 = local_38;
    lVar2 = local_40;
    if (local_38 != (long *)0x0) {
      lVar2 = local_38[1];
      local_38[1] = lVar2 + 1;
    }
    FUN_030d5738(lVar2,param_2,&local_80);
    if (plVar1 != (long *)0x0) {
      LOAcquire();
      lVar2 = plVar1[1];
      plVar1[1] = lVar2 + -1;
      LORelease();
      if (lVar2 == 0) {
        (**(code **)(*plVar1 + 0x10))(plVar1);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
      }
    }
  }
  plVar1 = local_58;
  if (local_58 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_58[1];
    local_58[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_58 + 0x10))(local_58);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
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
  return;
}


