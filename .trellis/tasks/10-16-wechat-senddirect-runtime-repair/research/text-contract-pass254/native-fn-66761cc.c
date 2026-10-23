// Ghidra inferred pseudocode; requested=0x66761cc
// entry=066761cc end=06676347

void FUN_066761cc(long param_1,long *param_2,undefined4 param_3,long param_4)

{
  long *plVar1;
  long *plVar2;
  long *plVar3;
  long lVar4;
  long local_58;
  long *local_50;
  undefined4 local_48;
  undefined4 uStack_44;
  long lStack_40;
  undefined1 uStack_31;
  
  lVar4 = *param_2;
  if (*(int *)(lVar4 + 0x288) == 0) {
    local_50 = (long *)param_2[1];
    if (local_50 != (long *)0x0) {
      local_50[1] = local_50[1] + 1;
    }
    plVar1 = *(long **)(param_1 + 0x28);
    local_48 = param_3;
    lStack_40 = param_4;
    if (plVar1 < *(long **)(param_1 + 0x30)) {
      *plVar1 = lVar4;
      plVar1[1] = (long)local_50;
      local_58 = 0;
      local_50 = (long *)0x0;
      plVar1[3] = param_4;
      plVar1[2] = CONCAT44(uStack_44,param_3);
      plVar1 = plVar1 + 4;
    }
    else {
      local_58 = lVar4;
      plVar1 = (long *)FUN_0667d374(param_1 + 0x20,&local_58);
    }
    *(long **)(param_1 + 0x28) = plVar1;
    FUN_0667d508(*(long *)(param_1 + 0x20),plVar1,&uStack_31,
                 (long)plVar1 - *(long *)(param_1 + 0x20) >> 5);
    plVar1 = local_50;
    if (local_50 != (long *)0x0) {
      LOAcquire();
      lVar4 = local_50[1];
      local_50[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*local_50 + 0x10))(local_50);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
      }
    }
    FUN_0667637c(param_1,0);
  }
  else if (*(int *)(lVar4 + 0x288) != 3) {
    plVar1 = (long *)__Znwm(0x20);
    plVar1[1] = param_4;
    *plVar1 = (long)&PTR_FUN_09df9538;
    plVar1[2] = (long)PTR___ZTIx_09b36ac8;
    plVar1[3] = (long)(plVar1 + 1);
    plVar3 = *(long **)(lVar4 + 0x398);
    if (plVar3 != (long *)0x0) {
      plVar2 = (long *)*plVar3;
      *plVar3 = (long)plVar1;
      if (plVar2 != (long *)0x0) {
        (**(code **)(*plVar2 + 8))();
      }
      plVar1 = (long *)0x0;
      *(undefined8 *)(lVar4 + 0x398) = 0;
    }
    *(undefined8 *)(lVar4 + 0x390) = 0;
    FUN_06677e1c(lVar4);
    if (plVar1 != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x06676278. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(*plVar1 + 8))(plVar1);
      return;
    }
  }
  return;
}


