// Ghidra inferred pseudocode; requested=0x4670680
// entry=04670680 end=04670773

void FUN_04670680(void)

{
  long lVar1;
  undefined8 uVar2;
  long *local_40;
  long *local_38;
  
  uVar2 = (**(code **)(*DAT_0a45df38 + 0x68))(&local_40);
  if ((local_38 != (long *)0x0) && (local_38[1] = local_38[1] + 1, local_38 != (long *)0x0)) {
    LOAcquire();
    lVar1 = local_38[1];
    local_38[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_38 + 0x10))(local_38);
      uVar2 = __ZNSt3__119__shared_weak_count14__release_weakEv(local_38);
    }
  }
  if (local_40 != (long *)0x0) {
    uVar2 = (**(code **)(*local_40 + 0x18))(local_40);
  }
  if (local_38 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_38[1];
    local_38[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_38 + 0x10))(local_38);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_38);
    }
  }
  if (local_40 == (long *)0x0) {
    FUN_04b530ec(uVar2);
  }
  return;
}


