// Ghidra inferred pseudocode; requested=0x410d33c
// entry=0410d33c end=0410d71f

void FUN_0410d33c(long param_1)

{
  long *plVar1;
  long **pplVar2;
  code *pcVar3;
  ulong uVar4;
  long lVar5;
  undefined1 auStack_230 [32];
  undefined8 local_210;
  long *local_208;
  undefined1 *local_200;
  long *local_1f8;
  undefined1 auStack_1f0 [8];
  long *local_1e8;
  long alStack_1e0 [3];
  long *local_1c8;
  long alStack_1c0 [3];
  long *local_1a8;
  long alStack_1a0 [3];
  long *local_188;
  long local_170;
  undefined1 auStack_168 [112];
  long local_f8;
  long lStack_f0;
  long alStack_e8 [3];
  long *local_d0;
  long alStack_c8 [3];
  long *local_b0;
  long alStack_a8 [3];
  long *local_90;
  long local_88;
  long local_80;
  long lStack_78;
  long local_70;
  long alStack_68 [3];
  long *local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  FUN_04112ab8(auStack_1f0);
  lVar5 = *(long *)(param_1 + 0x78);
  local_200 = &SUB_aaaaaaaaaaaaaaaa;
  local_1f8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_04669774();
  FUN_0466ad74(&local_210);
  if ((DAT_0a43e903 & 1) == 0) {
    DAT_0a43e8f8._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
    DAT_0a43e8f8._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
    DAT_0a43e8f8._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
    DAT_0a43e8f8._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
    DAT_0a43e8f8._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
    DAT_0a43e8f8._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
    DAT_0a43e8f8._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
    DAT_0a43e8f8._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
    DAT_0a43e900 = 0x2928;
    DAT_0a43e902 = 0;
    DAT_0a43e903 = 1;
  }
  if ((DAT_0a43e6d6 & 1) == 0) {
    uVar4 = 0;
    do {
      (&DAT_0a43e67b)[uVar4] = (&DAT_089bee1d)[uVar4] + 0x8a ^ (&DAT_089bee0d)[uVar4 & 0xf];
      uVar4 = uVar4 + 1;
    } while (uVar4 != 0x5b);
    DAT_0a43e6d6 = 1;
  }
  FUN_0003bb6c(auStack_230,&DAT_0a43e8f8,&DAT_0a43e67b,0x183);
  FUN_02fec014(auStack_168,param_1 + 8);
  FUN_04112ab8(&local_f8,auStack_1f0);
  local_50 = (long *)0x0;
  local_70 = lVar5;
  plVar1 = (long *)__Znwm(0x108);
  *plVar1 = (long)&PTR_FUN_09e5b298;
  FUN_02fec014(plVar1 + 1,auStack_168);
  plVar1[0x10] = lStack_f0;
  plVar1[0xf] = local_f8;
  local_f8 = 0;
  lStack_f0 = 0;
  if (local_d0 == (long *)0x0) {
    pplVar2 = (long **)(plVar1 + 0x14);
LAB_0410d4b0:
    *pplVar2 = (long *)0x0;
  }
  else {
    if (local_d0 != alStack_e8) {
      pplVar2 = &local_d0;
      plVar1[0x14] = (long)local_d0;
      goto LAB_0410d4b0;
    }
    plVar1[0x14] = (long)(plVar1 + 0x11);
    (**(code **)(*local_d0 + 0x18))();
  }
  if (local_b0 == (long *)0x0) {
    pplVar2 = (long **)(plVar1 + 0x18);
LAB_0410d4f4:
    *pplVar2 = (long *)0x0;
  }
  else {
    if (local_b0 != alStack_c8) {
      pplVar2 = &local_b0;
      plVar1[0x18] = (long)local_b0;
      goto LAB_0410d4f4;
    }
    plVar1[0x18] = (long)(plVar1 + 0x15);
    (**(code **)(*local_b0 + 0x18))();
  }
  if (local_90 == (long *)0x0) {
    pplVar2 = (long **)(plVar1 + 0x1c);
LAB_0410d538:
    *pplVar2 = (long *)0x0;
  }
  else {
    if (local_90 != alStack_a8) {
      pplVar2 = &local_90;
      plVar1[0x1c] = (long)local_90;
      goto LAB_0410d538;
    }
    plVar1[0x1c] = (long)(plVar1 + 0x19);
    (**(code **)(*local_90 + 0x18))();
  }
  plVar1[0x1d] = local_88;
  plVar1[0x1f] = lStack_78;
  plVar1[0x1e] = local_80;
  local_80 = 0;
  lStack_78 = 0;
  plVar1[0x20] = local_70;
  local_50 = plVar1;
  FUN_0453bbe0(&local_200,local_210,auStack_230,alStack_68,1);
  if (local_50 == alStack_68) {
    pcVar3 = *(code **)(*local_50 + 0x20);
LAB_0410d5b4:
    (*pcVar3)();
  }
  else if (local_50 != (long *)0x0) {
    pcVar3 = *(code **)(*local_50 + 0x28);
    goto LAB_0410d5b4;
  }
  FUN_0410d8d4(auStack_168);
  if (local_208 != (long *)0x0) {
    LOAcquire();
    lVar5 = local_208[1];
    local_208[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*local_208 + 0x10))(local_208);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_208);
    }
  }
  plVar1 = local_1f8;
  if (local_1f8 != (long *)0x0) {
    LOAcquire();
    lVar5 = local_1f8[1];
    local_1f8[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*local_1f8 + 0x10))(local_1f8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  if (local_170 != 0) {
    __ZNSt3__119__shared_weak_count14__release_weakEv();
  }
  if (local_188 == alStack_1a0) {
    pcVar3 = *(code **)(*local_188 + 0x20);
LAB_0410d658:
    (*pcVar3)();
  }
  else if (local_188 != (long *)0x0) {
    pcVar3 = *(code **)(*local_188 + 0x28);
    goto LAB_0410d658;
  }
  if (local_1a8 == alStack_1c0) {
    pcVar3 = *(code **)(*local_1a8 + 0x20);
LAB_0410d688:
    (*pcVar3)();
  }
  else if (local_1a8 != (long *)0x0) {
    pcVar3 = *(code **)(*local_1a8 + 0x28);
    goto LAB_0410d688;
  }
  if (local_1c8 == alStack_1e0) {
    pcVar3 = *(code **)(*local_1c8 + 0x20);
  }
  else {
    if (local_1c8 == (long *)0x0) goto LAB_0410d6bc;
    pcVar3 = *(code **)(*local_1c8 + 0x28);
  }
  (*pcVar3)();
LAB_0410d6bc:
  if (local_1e8 != (long *)0x0) {
    LOAcquire();
    lVar5 = local_1e8[1];
    local_1e8[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*local_1e8 + 0x10))(local_1e8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_1e8);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


