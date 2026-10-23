// Ghidra inferred pseudocode; requested=0x2ebf1d8
// entry=02ebf1d8 end=02ebf267

undefined8 * FUN_02ebf1d8(undefined8 *param_1,undefined8 *param_2)

{
  long *plVar1;
  long lVar2;
  undefined8 local_30;
  long *local_28;
  
  param_1[1] = 0;
  param_1[2] = 0;
  *param_1 = &PTR_FUN_09ddab98;
  local_30 = *param_2;
  local_28 = (long *)param_2[1];
  lVar2 = 0;
  if (local_28 != (long *)0x0) {
    lVar2 = local_28[1];
    local_28[1] = lVar2 + 1;
  }
  thunk_FUN_030ef9e0(lVar2,param_1 + 3,&local_30,1);
  plVar1 = local_28;
  if (local_28 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_28[1];
    local_28[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_28 + 0x10))(local_28);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  return param_1;
}


