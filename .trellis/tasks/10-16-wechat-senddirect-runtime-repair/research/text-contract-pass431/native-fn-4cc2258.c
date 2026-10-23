// Ghidra inferred pseudocode; requested=0x4cc2258
// entry=04cc2258 end=04cc22b3

long FUN_04cc2258(long param_1)

{
  long *plVar1;
  long lVar2;
  long *plVar3;
  long lVar4;
  
  lVar4 = *(long *)(param_1 + 0x220);
  if ((lVar4 != 0) && (plVar3 = *(long **)(param_1 + 0x228), plVar3 != (long *)0x0)) {
    plVar1 = plVar3 + 1;
    *plVar1 = *plVar1 + 1;
    LOAcquire();
    lVar2 = *plVar1;
    *plVar1 = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*plVar3 + 0x10))(plVar3);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  return lVar4 + 0xf0;
}


