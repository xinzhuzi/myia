// Ghidra inferred pseudocode; requested=0x303fdf0
// entry=0303fdf0 end=0303fe67

void FUN_0303fdf0(long *param_1,undefined8 *param_2)

{
  long *plVar1;
  long lVar2;
  undefined8 local_30;
  long *local_28;
  
  local_30 = *param_2;
  local_28 = (long *)param_2[1];
  if (local_28 != (long *)0x0) {
    local_28[1] = local_28[1] + 1;
  }
  (**(code **)(*param_1 + 0x80))(param_1,&local_30);
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
  return;
}


