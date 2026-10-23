// Ghidra inferred pseudocode; requested=0x667f4d8
// entry=0667f4d8 end=0667f533

void FUN_0667f4d8(long param_1)

{
  long lVar1;
  long *plVar2;
  
  if (param_1 != 0) {
    plVar2 = *(long **)(param_1 + 8);
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
    __ZdlPvm(param_1,0x10);
    return;
  }
  return;
}


