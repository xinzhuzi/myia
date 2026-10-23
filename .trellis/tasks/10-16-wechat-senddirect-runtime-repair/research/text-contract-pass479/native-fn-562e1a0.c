// Ghidra inferred pseudocode; requested=0x562e1a0
// entry=0562e1a0 end=0562e24b

void FUN_0562e1a0(long *param_1,long param_2)

{
  long lVar1;
  int iVar2;
  long lVar3;
  int *piVar4;
  long *plVar5;
  
  piVar4 = *(int **)(param_2 + 8);
  if (piVar4 != (int *)0x0) {
    LOAcquire();
    *piVar4 = *piVar4 + 1;
    LORelease();
  }
  piVar4 = (int *)param_1[1];
  if (piVar4 != (int *)0x0) {
    LOAcquire();
    iVar2 = *piVar4;
    *piVar4 = iVar2 + -1;
    LORelease();
    if (iVar2 == 1) {
      (**(code **)(*param_1 + 0x10))();
    }
  }
  lVar3 = *(long *)(param_2 + 8);
  lVar1 = *(long *)(param_2 + 0x10);
  if (lVar1 != 0) {
    *(long *)(lVar1 + 8) = *(long *)(lVar1 + 8) + 1;
  }
  plVar5 = (long *)param_1[2];
  param_1[1] = lVar3;
  param_1[2] = lVar1;
  if (plVar5 != (long *)0x0) {
    LOAcquire();
    lVar3 = plVar5[1];
    plVar5[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*plVar5 + 0x10))(plVar5);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
      return;
    }
  }
  return;
}


