// Ghidra inferred pseudocode; requested=0x667fc38
// entry=0667fc38 end=0667fce3

void FUN_0667fc38(long param_1,undefined1 param_2)

{
  byte bVar1;
  long *plVar2;
  long *local_30;
  undefined1 local_21;
  
  LOAcquire();
  bVar1 = *(byte *)(param_1 + 0x142);
  *(byte *)(param_1 + 0x142) = 1;
  LORelease();
  if ((bVar1 & 1) == 0) {
    local_30 = (long *)__Znwm(0x20);
    *local_30 = (long)&PTR_FUN_09dd53d8;
    *(undefined4 *)(local_30 + 1) = 0;
    local_30[2] = (long)PTR___ZTIi_09b36ab0;
    local_30[3] = (long)(local_30 + 1);
    FUN_066696dc(*(undefined8 *)(param_1 + 0xb8),&local_30);
    if (local_30 != (long *)0x0) {
      (**(code **)(*local_30 + 8))();
    }
    FUN_0667fd04(param_1 + 8,param_1);
    plVar2 = *(long **)(param_1 + 0x138);
    if (plVar2 != (long *)0x0) {
      local_21 = param_2;
      (**(code **)(*plVar2 + 0x30))(plVar2,&local_21);
    }
  }
  return;
}


