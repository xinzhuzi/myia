// Ghidra inferred pseudocode; requested=0x6676b84
// entry=06676b84 end=06676bef

long * FUN_06676b84(long *param_1)

{
  long lVar1;
  long *plVar2;
  
  lVar1 = *param_1;
  if (*(int *)(lVar1 + 0x288) != 3) {
    *(int *)(lVar1 + 0x3c8) = *(int *)(lVar1 + 0x3c8) + -1;
  }
  plVar2 = (long *)param_1[1];
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
  return param_1;
}


