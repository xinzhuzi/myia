// Ghidra inferred pseudocode; requested=0x5cc1c54
// entry=05cc1c54 end=05cc1cdb

void FUN_05cc1c54(long param_1,long param_2)

{
  long *plVar1;
  long lVar2;
  long local_30;
  long *local_28;
  
  local_30 = param_2;
  local_28 = (long *)__Znwm(0x20);
  *local_28 = (long)&PTR___ZNSt3__119__shared_weak_countD2Ev_09f46118;
  local_28[1] = 0;
  local_28[2] = 0;
  local_28[3] = param_2;
  FUN_0596281c(param_1 + 0x10,&local_30);
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


