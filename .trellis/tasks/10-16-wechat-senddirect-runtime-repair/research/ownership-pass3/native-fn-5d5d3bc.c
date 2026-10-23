// Ghidra inferred pseudocode; requested=0x5d5d3bc
// entry=05d5d3bc end=05d5d6ff

void FUN_05d5d3bc(long param_1)

{
  undefined8 uVar1;
  ulong uVar2;
  byte bVar3;
  long lVar4;
  undefined8 uVar5;
  undefined8 *puVar6;
  long *plVar7;
  long *plVar8;
  undefined8 local_558 [2];
  char local_541;
  undefined8 local_540;
  undefined8 uStack_538;
  long local_530;
  undefined4 local_528;
  undefined3 uStack_524;
  long local_520;
  undefined1 auStack_518 [536];
  undefined8 local_300;
  long *local_2f8;
  long *local_2f0;
  undefined8 local_2e8;
  undefined8 local_2e0;
  ulong local_2d8;
  undefined4 local_2d0;
  undefined3 uStack_2cc;
  byte local_2c9;
  undefined8 local_2c8;
  undefined8 local_2c0;
  undefined8 local_2b8;
  long *local_2b0;
  long local_2a8;
  undefined1 auStack_2a0 [536];
  long alStack_88 [3];
  long *local_70;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_520 = param_1;
  thunk_FUN_05daa3c8(auStack_518);
  uVar5 = FUN_0008a8b8(param_1 + 0x130);
  FUN_05e18374(local_558,"net_core.cc");
  puVar6 = (undefined8 *)
           __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKc
                     (local_558,&DAT_09855ac0);
  local_530 = puVar6[2];
  uStack_538 = puVar6[1];
  local_540 = *puVar6;
  puVar6[1] = 0;
  puVar6[2] = 0;
  *puVar6 = 0;
  puVar6 = (undefined8 *)
           __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKc
                     (&local_540,"StartTask");
  uVar1 = *puVar6;
  uVar2 = puVar6[1];
  local_528._0_3_ = (undefined3)*(undefined4 *)(puVar6 + 2);
  local_528._3_1_ = (undefined1)*(undefined4 *)((long)puVar6 + 0x13);
  uStack_524 = (undefined3)((uint)*(undefined4 *)((long)puVar6 + 0x13) >> 8);
  bVar3 = *(byte *)((long)puVar6 + 0x17);
  *puVar6 = 0;
  puVar6[1] = 0;
  puVar6[2] = 0;
  local_300 = 0;
  plVar7 = (long *)__Znwm(0x38);
  plVar7[2] = 0;
  plVar8 = plVar7 + 1;
  *plVar8 = 0;
  plVar7[3] = 0;
  *plVar7 = (long)&PTR_FUN_09f2cfd0;
  local_2f8 = (long *)__Znwm(0x18);
  *local_2f8 = (long)&PTR_FUN_09f2d020;
  local_2f8[1] = (long)(plVar7 + 3);
  local_2f8[2] = (long)plVar7;
  *plVar8 = *plVar8 + 1;
  LOAcquire();
  lVar4 = *plVar8;
  *plVar8 = lVar4 + -1;
  LORelease();
  if (lVar4 == 0) {
    (**(code **)(*plVar7 + 0x10))(plVar7);
    __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
  }
  local_2f0 = (long *)0x0;
  local_2e8 = 600000;
  if ((char)bVar3 < '\0') {
    FUN_00018d20(&local_2e0,uVar1,uVar2);
  }
  else {
    local_2d0 = local_528;
    uStack_2cc = uStack_524;
    local_2e0 = uVar1;
    local_2d8 = uVar2;
    local_2c9 = bVar3;
  }
  local_2c8 = FUN_05e1b2ac();
  local_2c0 = 0;
  uVar2 = local_2d8;
  if (-1 < (char)local_2c9) {
    uVar2 = (ulong)local_2c9;
  }
  if (uVar2 == 0) {
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
              (&local_2e0,"N10mars_boost8functionIFvvEEE");
  }
  local_2a8 = local_520;
  thunk_FUN_05daa3c8(auStack_2a0,auStack_518);
  plVar7 = (long *)__Znwm(0x228);
  *plVar7 = (long)&PTR_FUN_09f4c158;
  plVar7[1] = local_2a8;
  thunk_FUN_05daa3c8(plVar7 + 2,auStack_2a0);
  local_70 = plVar7;
  FUN_0596d190(&local_2b8,&local_2f8);
  FUN_0596d1f8(local_2b8,alStack_88);
  if (local_2b0 != (long *)0x0) {
    LOAcquire();
    lVar4 = local_2b0[1];
    local_2b0[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*local_2b0 + 0x10))(local_2b0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_2b0);
    }
  }
  if (local_70 == alStack_88) {
    lVar4 = 0x20;
  }
  else {
    if (local_70 == (long *)0x0) goto LAB_05d5d638;
    lVar4 = 0x28;
  }
  (**(code **)(*local_70 + lVar4))();
LAB_05d5d638:
  FUN_046364ec(auStack_2a0);
  FUN_05dfb04c(&local_2a8,uVar5,&local_300,&DAT_0a5015f8);
  if ((char)local_2c9 < '\0') {
    __ZdlPv(local_2e0);
  }
  if (local_2f0 != (long *)0x0) {
    (**(code **)(*local_2f0 + 8))();
  }
  if (local_2f8 != (long *)0x0) {
    (**(code **)(*local_2f8 + 8))();
  }
  if ((char)bVar3 < '\0') {
    __ZdlPv(uVar1);
  }
  if (local_530 < 0) {
    __ZdlPv(local_540);
  }
  if (local_541 < '\0') {
    __ZdlPv(local_558[0]);
  }
  FUN_046364ec(auStack_518);
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_68) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


