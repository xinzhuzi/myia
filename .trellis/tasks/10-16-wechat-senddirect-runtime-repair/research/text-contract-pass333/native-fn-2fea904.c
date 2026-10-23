// Ghidra inferred pseudocode; requested=0x2fea904
// entry=02fea904 end=02fea967

void FUN_02fea904(long param_1)

{
  long lVar1;
  long *plVar2;
  
  plVar2 = *(long **)(param_1 + 0xc0);
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
  FUN_02fc5bc4(param_1 + 8);
  __ZdlPvm(param_1,200);
  return;
}


