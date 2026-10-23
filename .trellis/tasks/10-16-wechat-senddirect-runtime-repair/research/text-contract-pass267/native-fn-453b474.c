// Ghidra inferred pseudocode; requested=0x453b474
// entry=0453b474 end=0453b60f

void FUN_0453b474(void)

{
  long *plVar1;
  long lVar2;
  undefined8 *puVar3;
  undefined8 uVar4;
  undefined8 *local_58;
  long *local_50;
  undefined8 *puStack_48;
  code *local_40;
  code *pcStack_38;
  undefined8 local_30;
  code *pcStack_28;
  
  lVar2 = FUN_066769d8();
  puVar3 = (undefined8 *)__Znwm(0x20);
  *puVar3 = &PTR_FUN_09e86b38;
  puVar3[3] = puVar3;
  local_58 = puVar3;
  local_50 = (long *)__Znwm(0x28);
  *local_50 = (long)&PTR___ZNSt3__119__shared_weak_countD2Ev_09e86bc8;
  local_50[1] = 0;
  local_50[2] = 0;
  local_50[3] = (long)puVar3;
  local_50[4] = (long)FUN_0453ec9c;
  local_40 = (code *)&DAT_0453ee3c;
  pcStack_38 = FUN_0453ec5c;
  local_30 = 0;
  pcStack_28 = FUN_0453ee64;
  puStack_48 = puVar3;
  FUN_06686420(lVar2 + 0x78,&puStack_48,0,0,0,&local_58);
  plVar1 = local_50;
  if (local_50 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_50[1];
    local_50[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_50 + 0x10))(local_50);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  uVar4 = FUN_066769d8();
  puVar3 = (undefined8 *)__Znwm(0x20);
  *puVar3 = &PTR_FUN_09e86c18;
  puVar3[3] = puVar3;
  local_58 = puVar3;
  local_50 = (long *)__Znwm(0x28);
  *local_50 = (long)&PTR___ZNSt3__119__shared_weak_countD2Ev_09e86ca8;
  local_50[1] = 0;
  local_50[2] = 0;
  local_50[3] = (long)puVar3;
  local_50[4] = (long)FUN_0453ef84;
  local_40 = FUN_0453f0e4;
  pcStack_38 = FUN_0453ef40;
  local_30 = 0;
  pcStack_28 = FUN_0453f110;
  puStack_48 = puVar3;
  FUN_06686420(uVar4,&puStack_48,0,0,0,&local_58);
  plVar1 = local_50;
  if (local_50 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_50[1];
    local_50[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_50 + 0x10))(local_50);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  return;
}


