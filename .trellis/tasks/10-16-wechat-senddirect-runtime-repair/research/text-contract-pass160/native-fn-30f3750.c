// Ghidra inferred pseudocode; requested=0x30f3750
// entry=030f3750 end=030f37d7

undefined8 * FUN_030f3750(undefined8 *param_1,long *param_2)

{
  long *plVar1;
  long lVar2;
  long local_30;
  long *plStack_28;
  
  local_30 = *param_2;
  plVar1 = (long *)param_2[1];
  lVar2 = local_30;
  if (plVar1 != (long *)0x0) {
    lVar2 = plVar1[1];
    plVar1[1] = lVar2 + 1;
  }
  plStack_28 = plVar1;
  FUN_030ef9e0(lVar2,param_1,&local_30,0);
  if (plVar1 != (long *)0x0) {
    LOAcquire();
    lVar2 = plVar1[1];
    plVar1[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*plVar1 + 0x10))(plVar1);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  *param_1 = &PTR_thunk_FUN_030f34f8_09de9568;
  return param_1;
}


