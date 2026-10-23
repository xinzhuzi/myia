// Ghidra inferred pseudocode; requested=0x6677980
// entry=06677980 end=06677a0f

void FUN_06677980(long param_1)

{
  long lVar1;
  code *UNRECOVERED_JUMPTABLE;
  long *plVar2;
  
  plVar2 = *(long **)(param_1 + 0x30);
  if (plVar2 != (long *)0x0) {
    LOAcquire();
    lVar1 = plVar2[1];
    plVar2[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*plVar2 + 0x10))(plVar2);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  plVar2 = *(long **)(param_1 + 0x20);
  if (plVar2 == (long *)(param_1 + 8)) {
    UNRECOVERED_JUMPTABLE = *(code **)(*plVar2 + 0x20);
  }
  else {
    if (plVar2 == (long *)0x0) {
      return;
    }
    UNRECOVERED_JUMPTABLE = *(code **)(*plVar2 + 0x28);
  }
                    /* WARNING: Could not recover jumptable at 0x066779fc. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*UNRECOVERED_JUMPTABLE)();
  return;
}


