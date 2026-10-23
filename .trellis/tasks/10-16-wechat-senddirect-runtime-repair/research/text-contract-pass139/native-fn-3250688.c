// Ghidra inferred pseudocode; requested=0x3250688
// entry=03250688 end=03250763

void FUN_03250688(long *param_1,undefined8 param_2,undefined8 param_3)

{
  long *plVar1;
  long lVar2;
  long lVar3;
  long *plVar4;
  
  plVar1 = (long *)__Znwm(0x398);
  plVar4 = plVar1 + 1;
  *plVar4 = 0;
  plVar1[2] = 0;
  *plVar1 = (long)&PTR_FUN_09de9488;
  lVar2 = FUN_03065454(plVar1 + 3,param_3);
  plVar1[3] = (long)&PTR_thunk_FUN_0303ff18_09de7f68;
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


