// Ghidra inferred pseudocode; requested=0x467c394
// entry=0467c394 end=0467c45f

void FUN_0467c394(long *param_1,undefined8 param_2,undefined8 param_3)

{
  long *plVar1;
  long lVar2;
  long lVar3;
  long *plVar4;
  
  plVar1 = (long *)__Znwm(0x4b0);
  plVar4 = plVar1 + 1;
  *plVar4 = 0;
  plVar1[2] = 0;
  *plVar1 = (long)&PTR_FUN_09e93260;
  lVar2 = thunk_FUN_0454cb70(plVar1 + 3,param_3);
  *param_1 = lVar2;
  param_1[1] = (long)plVar1;
  if ((lVar2 != 0) && ((lVar3 = plVar1[5], lVar3 == 0 || (*(long *)(lVar3 + 8) == -1)))) {
    if (plVar1 != (long *)0x0) {
      plVar1[1] = plVar1[1] + 1;
      plVar1[2] = plVar1[2] + 1;
    }
    plVar1[4] = lVar2;
    plVar1[5] = (long)plVar1;
    if (lVar3 != 0) {
      __ZNSt3__119__shared_weak_count14__release_weakEv(lVar3);
    }
    if (plVar1 != (long *)0x0) {
      LOAcquire();
      lVar2 = *plVar4;
      *plVar4 = lVar2 + -1;
      LORelease();
      if (lVar2 == 0) {
        (**(code **)(*plVar1 + 0x10))(plVar1);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
        return;
      }
    }
  }
  return;
}


