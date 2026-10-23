// Ghidra inferred pseudocode; requested=0x56435bc
// entry=056435bc end=05643637

void FUN_056435bc(undefined8 param_1,undefined8 *param_2)

{
  long lVar1;
  long *plVar2;
  
  if (param_2 != (undefined8 *)0x0) {
    FUN_056435bc(param_1,*param_2);
    FUN_056435bc(param_1,param_2[1]);
    plVar2 = (long *)param_2[8];
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
    FUN_0562fd84(param_2 + 4);
    __ZdlPvm(param_2,0x48);
    return;
  }
  return;
}


