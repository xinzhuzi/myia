// Ghidra inferred pseudocode; requested=0x4668950
// entry=04668950 end=04668aab

void FUN_04668950(long param_1)

{
  long *plVar1;
  long lVar2;
  int iVar3;
  undefined1 *local_70;
  long *plStack_68;
  undefined8 local_60;
  undefined8 local_58;
  long *local_50;
  undefined1 *local_48;
  long *local_40;
  undefined **local_38;
  
  (**(code **)(*DAT_0a45df38 + 0x88))(&local_58);
  local_38 = &PTR_FUN_09bf4208;
  local_70 = &SUB_aaaaaaaaaaaaaaaa;
  plStack_68 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0456f244(&local_70,local_58,&local_38);
  plVar1 = plStack_68;
  local_48 = local_70;
  local_40 = plStack_68;
  if (plStack_68 != (long *)0x0) {
    plStack_68[1] = plStack_68[1] + 1;
    if (plStack_68 != (long *)0x0) {
      LOAcquire();
      lVar2 = plStack_68[1];
      plStack_68[1] = lVar2 + -1;
      LORelease();
      if (lVar2 == 0) {
        (**(code **)(*plStack_68 + 0x10))(plStack_68);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
      }
    }
  }
  iVar3 = FUN_04273328(local_48);
  plVar1 = local_40;
  if (local_40 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_40[1];
    local_40[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_40 + 0x10))(local_40);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  if (local_50 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_50[1];
    local_50[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_50 + 0x10))(local_50);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_50);
    }
  }
  if (-1 < iVar3) {
    FUN_0487d1fc(&local_70);
    if (*(char *)(param_1 + 0x147) < '\0') {
      __ZdlPvm(*(undefined8 *)(param_1 + 0x130),*(ulong *)(param_1 + 0x140) & 0x7fffffffffffffff);
    }
    *(long **)(param_1 + 0x138) = plStack_68;
    *(undefined1 **)(param_1 + 0x130) = local_70;
    *(undefined8 *)(param_1 + 0x140) = local_60;
  }
  return;
}


