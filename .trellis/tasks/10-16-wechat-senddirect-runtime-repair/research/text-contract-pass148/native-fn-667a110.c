// Ghidra inferred pseudocode; requested=0x667a110
// entry=0667a110 end=0667a20b

void FUN_0667a110(long *param_1,undefined8 param_2,undefined8 *param_3,undefined8 *param_4,
                 undefined8 *param_5,undefined8 param_6)

{
  long *plVar1;
  long lVar2;
  long *plVar3;
  
  plVar1 = (long *)__Znwm(0x410);
  plVar3 = plVar1 + 1;
  *plVar3 = 0;
  plVar1[2] = 0;
  *plVar1 = (long)&PTR_FUN_09fb2720;
  lVar2 = FUN_0667a274(plVar1 + 3,*param_3,*param_4,*param_5,param_6);
  *param_1 = lVar2;
  param_1[1] = (long)plVar1;
  if ((lVar2 != 0) && ((lVar2 = plVar1[4], lVar2 == 0 || (*(long *)(lVar2 + 8) == -1)))) {
    if (plVar1 != (long *)0x0) {
      plVar1[1] = plVar1[1] + 1;
      plVar1[2] = plVar1[2] + 1;
    }
    plVar1[3] = (long)(plVar1 + 3);
    plVar1[4] = (long)plVar1;
    if (lVar2 != 0) {
      __ZNSt3__119__shared_weak_count14__release_weakEv();
    }
    if (plVar1 != (long *)0x0) {
      LOAcquire();
      lVar2 = *plVar3;
      *plVar3 = lVar2 + -1;
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


