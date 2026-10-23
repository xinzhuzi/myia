// Ghidra inferred pseudocode; requested=0x466aca8
// entry=0466aca8 end=0466ad2b

void FUN_0466aca8(undefined8 *param_1)

{
  long lVar1;
  undefined8 local_30;
  long *local_28;
  
  (**(code **)(*DAT_0a45df38 + 0x68))(&local_30);
  *param_1 = local_30;
  param_1[1] = local_28;
  if (local_28 != (long *)0x0) {
    local_28[1] = local_28[1] + 1;
    if (local_28 != (long *)0x0) {
      LOAcquire();
      lVar1 = local_28[1];
      local_28[1] = lVar1 + -1;
      LORelease();
      if (lVar1 == 0) {
        (**(code **)(*local_28 + 0x10))(local_28);
        __ZNSt3__119__shared_weak_count14__release_weakEv(local_28);
      }
    }
  }
  return;
}


