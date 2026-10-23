// Ghidra inferred pseudocode; requested=0x305d668
// entry=0305d668 end=0305d6db

void FUN_0305d668(long param_1,undefined8 *param_2)

{
  long *plVar1;
  long lVar2;
  undefined8 local_30;
  long *local_28;
  
  local_30 = *param_2;
  local_28 = (long *)param_2[1];
  lVar2 = 0;
  if (local_28 != (long *)0x0) {
    lVar2 = local_28[1];
    local_28[1] = lVar2 + 1;
  }
  FUN_0305d770(lVar2,param_1 + 8,&local_30);
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


