// Ghidra inferred pseudocode; requested=0x77bdd0
// entry=0077bdd0 end=0077be73

void FUN_0077bdd0(long *param_1)

{
  long *plVar1;
  long *plVar2;
  long lVar3;
  
  plVar2 = (long *)__Znwm(0x610);
  FUN_0077be90();
  plVar1 = plVar2 + 3;
  *param_1 = (long)plVar1;
  param_1[1] = (long)plVar2;
  if ((plVar1 != (long *)0x0) && ((lVar3 = plVar2[5], lVar3 == 0 || (*(long *)(lVar3 + 8) == -1))))
  {
    if (plVar2 != (long *)0x0) {
      plVar2[1] = plVar2[1] + 1;
      plVar2[2] = plVar2[2] + 1;
    }
    plVar2[4] = (long)plVar1;
    plVar2[5] = (long)plVar2;
    if (lVar3 != 0) {
      __ZNSt3__119__shared_weak_count14__release_weakEv();
    }
    if (plVar2 != (long *)0x0) {
      LOAcquire();
      lVar3 = plVar2[1];
      plVar2[1] = lVar3 + -1;
      LORelease();
      if (lVar3 == 0) {
        (**(code **)(*plVar2 + 0x10))(plVar2);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
        return;
      }
    }
  }
  return;
}


