// Ghidra inferred pseudocode; requested=0x667378c
// entry=0667378c end=0667381b

void FUN_0667378c(undefined8 *param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
                 undefined8 param_5)

{
  long lVar1;
  undefined8 local_50;
  long *local_48;
  undefined8 local_40;
  undefined8 local_38;
  undefined8 uStack_30;
  undefined1 uStack_21;
  
  local_40 = param_4;
  local_38 = param_3;
  uStack_30 = param_2;
  FUN_0667a110(&local_50,&uStack_21,&uStack_30,&local_38,&local_40,param_5);
  *param_1 = local_50;
  param_1[1] = local_48;
  if (local_48 != (long *)0x0) {
    local_48[1] = local_48[1] + 1;
    if (local_48 != (long *)0x0) {
      LOAcquire();
      lVar1 = local_48[1];
      local_48[1] = lVar1 + -1;
      LORelease();
      if (lVar1 == 0) {
        (**(code **)(*local_48 + 0x10))(local_48);
        __ZNSt3__119__shared_weak_count14__release_weakEv(local_48);
      }
    }
  }
  return;
}


