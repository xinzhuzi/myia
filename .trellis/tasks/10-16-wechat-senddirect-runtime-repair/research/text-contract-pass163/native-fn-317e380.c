// Ghidra inferred pseudocode; requested=0x317e380
// entry=0317e380 end=0317e3fb

void FUN_0317e380(undefined8 param_1,undefined8 *param_2)

{
  long *plVar1;
  long lVar2;
  undefined8 local_30;
  long *plStack_28;
  
  local_30 = *param_2;
  plVar1 = (long *)param_2[1];
  if (plVar1 != (long *)0x0) {
    plVar1[1] = plVar1[1] + 1;
  }
  plStack_28 = plVar1;
  FUN_0317df64(param_1,&local_30,0);
  if (plVar1 != (long *)0x0) {
    LOAcquire();
    lVar2 = plVar1[1];
    plVar1[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*plVar1 + 0x10))(plVar1);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
      return;
    }
  }
  return;
}


