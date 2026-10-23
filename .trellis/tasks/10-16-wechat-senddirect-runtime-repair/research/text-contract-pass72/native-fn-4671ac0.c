// Ghidra inferred pseudocode; requested=0x4671ac0
// entry=04671ac0 end=04671c33

undefined8 FUN_04671ac0(undefined8 param_1,undefined8 param_2)

{
  long *plVar1;
  long lVar2;
  long lVar3;
  undefined8 uVar4;
  long local_40;
  long *local_38;
  
  (**(code **)(*DAT_0a45df38 + 0x68))(&local_40);
  plVar1 = local_38;
  lVar3 = local_40;
  if ((local_38 != (long *)0x0) && (local_38[1] = local_38[1] + 1, local_38 != (long *)0x0)) {
    LOAcquire();
    lVar2 = local_38[1];
    local_38[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_38 + 0x10))(local_38);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  if (lVar3 == 0) {
    uVar4 = 0;
  }
  else {
    (**(code **)(*DAT_0a45df38 + 0x68))(&local_40);
    if ((local_38 != (long *)0x0) && (local_38[1] = local_38[1] + 1, local_38 != (long *)0x0)) {
      LOAcquire();
      lVar3 = local_38[1];
      local_38[1] = lVar3 + -1;
      LORelease();
      if (lVar3 == 0) {
        (**(code **)(*local_38 + 0x10))(local_38);
        __ZNSt3__119__shared_weak_count14__release_weakEv(local_38);
      }
    }
    uVar4 = FUN_04555cac(local_40,param_2);
    if (local_38 != (long *)0x0) {
      LOAcquire();
      lVar3 = local_38[1];
      local_38[1] = lVar3 + -1;
      LORelease();
      if (lVar3 == 0) {
        (**(code **)(*local_38 + 0x10))(local_38);
        __ZNSt3__119__shared_weak_count14__release_weakEv(local_38);
      }
    }
  }
  if (plVar1 != (long *)0x0) {
    LOAcquire();
    lVar3 = plVar1[1];
    plVar1[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*plVar1 + 0x10))(plVar1);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  return uVar4;
}


