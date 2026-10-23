// Ghidra inferred pseudocode; requested=0x6681744
// entry=06681744 end=0668183b

void FUN_06681744(long *param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
                 undefined8 param_5)

{
  long *plVar1;
  long *plVar2;
  long lVar3;
  long *plVar4;
  undefined1 local_51;
  
  plVar2 = (long *)__Znwm(0x170);
  plVar4 = plVar2 + 1;
  *plVar4 = 0;
  plVar2[2] = 0;
  *plVar2 = (long)&PTR_FUN_09fb2bd0;
  local_51 = 0xaa;
  plVar1 = plVar2 + 3;
  FUN_06681860(&local_51,plVar1,param_3,param_4,param_5);
  *param_1 = (long)plVar1;
  param_1[1] = (long)plVar2;
  if ((plVar1 != (long *)0x0) &&
     ((lVar3 = plVar2[0x17], lVar3 == 0 || (*(long *)(lVar3 + 8) == -1)))) {
    if (plVar2 != (long *)0x0) {
      plVar2[1] = plVar2[1] + 1;
      plVar2[2] = plVar2[2] + 1;
    }
    plVar2[0x16] = (long)plVar1;
    plVar2[0x17] = (long)plVar2;
    if (lVar3 != 0) {
      __ZNSt3__119__shared_weak_count14__release_weakEv();
    }
    if (plVar2 != (long *)0x0) {
      LOAcquire();
      lVar3 = *plVar4;
      *plVar4 = lVar3 + -1;
      LORelease();
      if (lVar3 == 0) {
        (**(code **)(*plVar2 + 0x10))(plVar2);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
      }
    }
  }
  return;
}


