// Ghidra inferred pseudocode; requested=0x6677a10
// entry=06677a10 end=06677a97

void FUN_06677a10(long param_1)

{
  long lVar1;
  code *pcVar2;
  long *plVar3;
  
  plVar3 = *(long **)(param_1 + 0x30);
  if (plVar3 != (long *)0x0) {
    LOAcquire();
    lVar1 = plVar3[1];
    plVar3[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*plVar3 + 0x10))(plVar3);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  plVar3 = *(long **)(param_1 + 0x20);
  if (plVar3 == (long *)(param_1 + 8)) {
    pcVar2 = *(code **)(*plVar3 + 0x20);
  }
  else {
    if (plVar3 == (long *)0x0) goto LAB_06677a80;
    pcVar2 = *(code **)(*plVar3 + 0x28);
  }
  (*pcVar2)();
LAB_06677a80:
  __ZdlPvm(param_1,0x40);
  return;
}


