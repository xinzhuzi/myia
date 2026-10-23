// Ghidra inferred pseudocode; requested=0x667e0e4
// entry=0667e0e4 end=0667e5d3

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 * FUN_0667e0e4(undefined8 *param_1,long param_2,long *param_3,long param_4)

{
  long *plVar1;
  undefined **ppuVar2;
  long lVar3;
  ulong uVar4;
  undefined **ppuVar5;
  code *pcVar6;
  long *plVar7;
  long *plVar8;
  long *plVar9;
  long *plVar10;
  undefined8 uVar11;
  undefined8 uVar12;
  undefined8 uVar13;
  undefined8 ***local_190;
  undefined8 uStack_188;
  ulong local_180;
  undefined **local_178 [3];
  undefined ***local_160;
  undefined8 *local_a8;
  undefined1 *local_a0;
  undefined8 ***pppuStack_98;
  undefined8 local_90;
  undefined1 *puStack_88;
  undefined8 local_80;
  long local_78;
  
  local_78 = *(long *)PTR____stack_chk_guard_09b36c98;
  *param_1 = &PTR_FUN_09fb2cc8;
  FUN_066860b0(param_1 + 1);
  FUN_06685c88(param_1 + 3);
  plVar8 = param_1 + 0x10;
  param_1[0x11] = 0;
  *plVar8 = 0;
  param_1[0x13] = 0;
  param_1[0x12] = 0;
  param_1[0x14] = 0;
  *param_1 = &PTR_thunk_FUN_0667f128_09fb2c20;
  param_1[1] = &PTR_FUN_09fb2d18;
  param_1[0x15] = 0;
  param_1[0x16] = 0;
  FUN_021efaf0(param_1 + 0x17,local_178);
  param_1[0x1a] = 0;
  param_1[0x19] = 0;
  param_1[0x21] = 0;
  param_1[0x1e] = 0;
  param_1[0x1d] = 0;
  param_1[0x20] = 0;
  param_1[0x1f] = 0;
  param_1[0x1c] = 0;
  param_1[0x1b] = 0;
  param_1[0x22] = 0x80000000ffffffff;
  plVar1 = param_1 + 0x24;
  plVar7 = param_1 + 0x27;
  *plVar7 = 0;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(plVar8,param_2);
  plVar9 = (long *)param_1[0x16];
  param_1[0x15] = 0;
  param_1[0x16] = 0;
  if (plVar9 != (long *)0x0) {
    LOAcquire();
    lVar3 = plVar9[1];
    plVar9[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*plVar9 + 0x10))(plVar9);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar9);
    }
  }
  uVar11 = param_1[0x17];
  plVar9 = (long *)param_1[0x18];
  if (plVar9 != (long *)0x0) {
    plVar10 = plVar9 + 1;
    *plVar10 = *plVar10 + 1;
    *plVar10 = *plVar10 + 1;
  }
  plVar10 = (long *)param_1[0x1a];
  param_1[0x19] = uVar11;
  param_1[0x1a] = plVar9;
  if (plVar10 != (long *)0x0) {
    LOAcquire();
    lVar3 = plVar10[1];
    plVar10[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*plVar10 + 0x10))(plVar10);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
    }
  }
  param_1[0x1b] = 0;
  if (plVar9 != (long *)0x0) {
    LOAcquire();
    lVar3 = plVar9[1];
    plVar9[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*plVar9 + 0x10))(plVar9);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar9);
    }
  }
  local_178[0] = &PTR_FUN_09fb2d78;
  local_160 = local_178;
  FUN_06668e84(param_1[0x17],local_178);
  if (local_160 == local_178) {
    (*(code *)(*local_160)[4])();
  }
  else if (local_160 != (undefined ***)0x0) {
    (*(code *)(*local_160)[5])();
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_1 + 0x1c,param_2);
  uVar12 = *(undefined8 *)(param_2 + 0x20);
  uVar11 = *(undefined8 *)(param_2 + 0x18);
  uVar13 = *(undefined8 *)(param_2 + 0x28);
  param_1[0x22] = *(undefined8 *)(param_2 + 0x30);
  param_1[0x21] = uVar13;
  param_1[0x20] = uVar12;
  param_1[0x1f] = uVar11;
  lVar3 = __Znwm(0x20);
  plVar9 = param_3 + 3;
  plVar10 = (long *)*plVar9;
  if (plVar10 == (long *)0x0) {
    plVar9 = (long *)(lVar3 + 0x18);
LAB_0667e310:
    *plVar9 = 0;
  }
  else {
    if (plVar10 != param_3) {
      *(long **)(lVar3 + 0x18) = plVar10;
      goto LAB_0667e310;
    }
    *(long *)(lVar3 + 0x18) = lVar3;
    (**(code **)(*plVar10 + 0x18))(plVar10,lVar3);
  }
  param_1[0x23] = lVar3;
  plVar9 = (long *)param_1[0x27];
  param_1[0x27] = 0;
  if (plVar9 == plVar1) {
    pcVar6 = *(code **)(*plVar9 + 0x20);
LAB_0667e364:
    (*pcVar6)();
  }
  else if (plVar9 != (long *)0x0) {
    pcVar6 = *(code **)(*plVar9 + 0x28);
    goto LAB_0667e364;
  }
  plVar9 = (long *)(param_4 + 0x18);
  lVar3 = *plVar9;
  if (lVar3 != 0) {
    if (lVar3 == param_4) {
      *plVar7 = (long)plVar1;
      (**(code **)(*(long *)*plVar9 + 0x18))((long *)*plVar9,plVar1);
      goto LAB_0667e3a8;
    }
    *plVar7 = lVar3;
    plVar7 = plVar9;
  }
  *plVar7 = 0;
LAB_0667e3a8:
  *(undefined1 *)(param_1 + 0x28) = 0;
  *(undefined1 *)((long)param_1 + 0x141) = 0;
  *(undefined1 *)((long)param_1 + 0x142) = 0;
  *(undefined1 *)((long)param_1 + 0x143) = 0;
  *(undefined1 *)(param_1 + 0x2a) = 0;
  param_1[0x29] = 0;
  uVar4 = FUN_0668dad0(0);
  if ((uVar4 & 1) != 0) {
    if ((DAT_0a5181e5 & 1) == 0) {
      DAT_0a5181e0 = (undefined4)ram0x08782918;
      DAT_0a5181e4 = 0;
      DAT_0a5181e5 = 1;
    }
    if ((DAT_0a5181f4 & 1) == 0) {
      DAT_0a5181e8._0_1_ = s_co_job_ico_job_c________join_____09685c10[0];
      DAT_0a5181e8._1_1_ = s_co_job_ico_job_c________join_____09685c10[1];
      DAT_0a5181e8._2_1_ = s_co_job_ico_job_c________join_____09685c10[2];
      DAT_0a5181e8._3_1_ = s_co_job_ico_job_c________join_____09685c10[3];
      DAT_0a5181e8._4_1_ = s_co_job_ico_job_c________join_____09685c10[4];
      DAT_0a5181e8._5_1_ = s_co_job_ico_job_c________join_____09685c10[5];
      DAT_0a5181e8._6_1_ = s_co_job_ico_job_c________join_____09685c10[6];
      DAT_0a5181e8._7_1_ = s_co_job_ico_job_c________join_____09685c10[7];
      DAT_0a5181f0 = (undefined4)DAT_084852a8;
      DAT_0a5181f4 = 1;
    }
    if ((DAT_0a518203 & 1) == 0) {
      DAT_0a5181f8._0_1_ = s_co_job_ico_job_c________join_____09685c10[8];
      DAT_0a5181f8._1_1_ = s_co_job_ico_job_c________join_____09685c10[9];
      DAT_0a5181f8._2_1_ = s_co_job_ico_job_c________join_____09685c10[10];
      DAT_0a5181f8._3_1_ = s_co_job_ico_job_c________join_____09685c10[0xb];
      DAT_0a5181f8._4_1_ = s_co_job_ico_job_c________join_____09685c10[0xc];
      DAT_0a5181f8._5_1_ = s_co_job_ico_job_c________join_____09685c10[0xd];
      DAT_0a5181f8._6_1_ = s_co_job_ico_job_c________join_____09685c10[0xe];
      DAT_0a5181f8._7_1_ = s_co_job_ico_job_c________join_____09685c10[0xf];
      DAT_0a518200 = 0x7070;
      DAT_0a518202 = 0;
      DAT_0a518203 = 1;
    }
    FUN_0668db5c(local_178,&DAT_0a5181e0,&DAT_0a5181e8,&DAT_0a5181f8,0x3000000800);
    ppuVar2 = local_178[0];
    if (*(char *)((long)param_1 + 0x97) < '\0') {
      FUN_00018d20(&local_190,param_1[0x10],param_1[0x11]);
    }
    else {
      uStack_188 = param_1[0x11];
      local_190 = (undefined8 ***)*plVar8;
      local_180 = param_1[0x12];
    }
    if ((DAT_0a518214 & 1) == 0) {
      DAT_0a518208._0_1_ = s_co_job_ico_job_c________join_____09685c10[0x10];
      DAT_0a518208._1_1_ = s_co_job_ico_job_c________join_____09685c10[0x11];
      DAT_0a518208._2_1_ = s_co_job_ico_job_c________join_____09685c10[0x12];
      DAT_0a518208._3_1_ = s_co_job_ico_job_c________join_____09685c10[0x13];
      DAT_0a518208._4_1_ = s_co_job_ico_job_c________join_____09685c10[0x14];
      DAT_0a518208._5_1_ = s_co_job_ico_job_c________join_____09685c10[0x15];
      DAT_0a518208._6_1_ = s_co_job_ico_job_c________join_____09685c10[0x16];
      DAT_0a518208._7_1_ = s_co_job_ico_job_c________join_____09685c10[0x17];
      DAT_0a518210 = (undefined4)DAT_09684c88;
      DAT_0a518214 = 1;
    }
    ppuVar5 = ppuVar2 + 0xd;
    if (*(char *)((long)ppuVar2 + 0x7f) < '\0') {
      ppuVar5 = (undefined **)*ppuVar5;
    }
    local_a0 = &DAT_aaaaaaaa0000000f;
    pppuStack_98 = local_190;
    if (-1 < (long)local_180) {
      pppuStack_98 = &local_190;
    }
    local_80 = 0xaaaaaaaa00000006;
    local_90 = 0xaaaaaaaa00000010;
    puStack_88 = &DAT_aaaaaaaa00000000;
    local_a8 = param_1;
    FUN_0668e1e4(ppuVar2 + 7,&DAT_0a518208,ppuVar5,&local_a8,2);
    FUN_0668dbac();
    if ((long)local_180 < 0) {
      __ZdlPvm(local_190,local_180 & 0x7fffffffffffffff);
    }
    thunk_FUN_0668e878(local_178);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_78) {
    return param_1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


