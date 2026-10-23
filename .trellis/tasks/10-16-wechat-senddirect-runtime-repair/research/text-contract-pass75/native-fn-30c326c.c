// Ghidra inferred pseudocode; requested=0x30c326c
// entry=030c326c end=030c32ff

void FUN_030c326c(long param_1)

{
  long lVar1;
  long *plVar2;
  
  plVar2 = *(long **)(param_1 + 0x28);
  if (plVar2 != (long *)0x0) {
    LOAcquire();
    lVar1 = plVar2[1];
    plVar2[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*plVar2 + 0x10))(plVar2);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
      plVar2 = *(long **)(param_1 + 0x10);
      goto joined_r0x030c3294;
    }
  }
  plVar2 = *(long **)(param_1 + 0x10);
joined_r0x030c3294:
  if (plVar2 != (long *)0x0) {
    LOAcquire();
    lVar1 = plVar2[1];
    plVar2[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*plVar2 + 0x10))(plVar2);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
      return;
    }
  }
  return;
}


