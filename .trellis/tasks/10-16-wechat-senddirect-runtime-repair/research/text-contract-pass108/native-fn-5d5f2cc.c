// Ghidra inferred pseudocode; requested=0x5d5f2cc
// entry=05d5f2cc end=05d5f5bb

void FUN_05d5f2cc(long param_1,uint param_2)

{
  undefined8 uVar1;
  ulong uVar2;
  byte bVar3;
  long lVar4;
  undefined8 uVar5;
  undefined8 *puVar6;
  long *plVar7;
  long *plVar8;
  undefined8 local_118 [2];
  char local_101;
  undefined8 local_100;
  undefined8 uStack_f8;
  long local_f0;
  undefined4 local_e8;
  undefined3 uStack_e4;
  undefined8 local_e0;
  long *local_d8;
  long *local_d0;
  undefined8 uStack_c8;
  undefined8 local_c0;
  ulong local_b8;
  undefined4 local_b0;
  undefined3 uStack_ac;
  byte local_a9;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  long *local_90;
  undefined **local_88;
  long lStack_80;
  ulong local_78;
  undefined ***local_70;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  uVar5 = FUN_0008a8b8(param_1 + 0x130);
  FUN_05e18374(local_118,"net_core.cc");
  puVar6 = (undefined8 *)
           __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKc
                     (local_118,&DAT_09855ac0);
  local_f0 = puVar6[2];
  uStack_f8 = puVar6[1];
  local_100 = *puVar6;
  puVar6[1] = 0;
  puVar6[2] = 0;
  *puVar6 = 0;
  puVar6 = (undefined8 *)
           __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKc
                     (&local_100,"StopTask");
  uVar1 = *puVar6;
  uVar2 = puVar6[1];
  local_e8._0_3_ = (undefined3)*(undefined4 *)(puVar6 + 2);
  local_e8._3_1_ = (undefined1)*(undefined4 *)((long)puVar6 + 0x13);
  uStack_e4 = (undefined3)((uint)*(undefined4 *)((long)puVar6 + 0x13) >> 8);
  bVar3 = *(byte *)((long)puVar6 + 0x17);
  *puVar6 = 0;
  puVar6[1] = 0;
  puVar6[2] = 0;
  local_e0 = 0;
  plVar7 = (long *)__Znwm(0x38);
  plVar7[2] = 0;
  plVar8 = plVar7 + 1;
  *plVar8 = 0;
  plVar7[3] = 0;
  *plVar7 = (long)&PTR_FUN_09f2cfd0;
  local_d8 = (long *)__Znwm(0x18);
  *local_d8 = (long)&PTR_FUN_09f2d020;
  local_d8[1] = (long)(plVar7 + 3);
  local_d8[2] = (long)plVar7;
  *plVar8 = *plVar8 + 1;
  LOAcquire();
  lVar4 = *plVar8;
  *plVar8 = lVar4 + -1;
  LORelease();
  if (lVar4 == 0) {
    (**(code **)(*plVar7 + 0x10))(plVar7);
    __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
  }
  local_d0 = (long *)0x0;
  uStack_c8 = 600000;
  if ((char)bVar3 < '\0') {
    FUN_00018d20(&local_c0,uVar1,uVar2);
  }
  else {
    local_b0 = local_e8;
    uStack_ac = uStack_e4;
    local_c0 = uVar1;
    local_b8 = uVar2;
    local_a9 = bVar3;
  }
  local_a8 = FUN_05e1b2ac();
  uStack_a0 = 0;
  uVar2 = local_b8;
  if (-1 < (char)local_a9) {
    uVar2 = (ulong)local_a9;
  }
  if (uVar2 == 0) {
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
              (&local_c0,"N10mars_boost8functionIFvvEEE");
  }
  local_88 = &PTR_FUN_09f4c1d8;
  local_78 = (ulong)param_2;
  lStack_80 = param_1;
  local_70 = &local_88;
  FUN_0596d190(&local_98,&local_d8);
  FUN_0596d1f8(local_98,&local_88);
  if (local_90 != (long *)0x0) {
    LOAcquire();
    lVar4 = local_90[1];
    local_90[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*local_90 + 0x10))(local_90);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_90);
    }
  }
  if (local_70 == &local_88) {
    lVar4 = 0x20;
  }
  else {
    if (local_70 == (undefined ***)0x0) goto LAB_05d5f504;
    lVar4 = 0x28;
  }
  (**(code **)((long)*local_70 + lVar4))();
LAB_05d5f504:
  FUN_05dfb04c(&local_88,uVar5,&local_e0,&DAT_0a5015f8);
  if ((char)local_a9 < '\0') {
    __ZdlPv(local_c0);
  }
  if (local_d0 != (long *)0x0) {
    (**(code **)(*local_d0 + 8))();
  }
  if (local_d8 != (long *)0x0) {
    (**(code **)(*local_d8 + 8))();
  }
  if ((char)bVar3 < '\0') {
    __ZdlPv(uVar1);
  }
  if (local_f0 < 0) {
    __ZdlPv(local_100);
  }
  if (local_101 < '\0') {
    __ZdlPv(local_118[0]);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_68) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


