// Ghidra inferred pseudocode; requested=0x21b3484
// entry=021b3484 end=021b34df

long FUN_021b3484(long param_1)

{
  long lVar1;
  long *plVar2;
  
  if ((*(char *)(param_1 + 0x18) == '\x01') &&
     (plVar2 = *(long **)(param_1 + 8), plVar2 != (long *)0x0)) {
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


