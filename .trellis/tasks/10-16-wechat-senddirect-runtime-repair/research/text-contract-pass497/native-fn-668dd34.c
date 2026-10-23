// Ghidra inferred pseudocode; requested=0x668dd34
// entry=0668dd34 end=0668ddc7

void FUN_0668dd34(long param_1)

{
  long lVar1;
  long lVar2;
  long *plVar3;
  long lVar4;
  
  __ZNSt3__115recursive_mutex4lockEv(param_1 + 0xa0);
  FUN_0668d5c8(param_1 + 0x18);
  lVar1 = *(long *)(param_1 + 0x70);
  for (lVar4 = *(long *)(param_1 + 0x78); lVar4 != lVar1; lVar4 = lVar4 + -0x10) {
    plVar3 = *(long **)(lVar4 + -8);
    if (plVar3 != (long *)0x0) {
      LOAcquire();
      lVar2 = plVar3[1];
      plVar3[1] = lVar2 + -1;
      LORelease();
      if (lVar2 == 0) {
        (**(code **)(*plVar3 + 0x10))(plVar3);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
      }
    }
  }
  *(long *)(param_1 + 0x78) = lVar1;
  __ZNSt3__115recursive_mutex6unlockEv(param_1 + 0xa0);
  return;
}


