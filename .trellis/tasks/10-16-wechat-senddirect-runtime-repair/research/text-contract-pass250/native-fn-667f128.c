// Ghidra inferred pseudocode; requested=0x667f128
// entry=0667f128 end=0667f4c3

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 * FUN_0667f128(undefined8 *param_1)

{
  long lVar1;
  int iVar2;
  long *plVar3;
  long *plVar4;
  code *pcVar5;
  undefined1 *local_150;
  undefined8 uStack_148;
  ulong local_140;
  long local_138 [26];
  undefined8 *local_68;
  undefined1 *local_60;
  undefined1 *puStack_58;
  undefined8 local_50;
  undefined1 *puStack_48;
  undefined8 local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  *param_1 = &PTR_thunk_FUN_0667f128_09fb2c20;
  iVar2 = FUN_0668dad0(0);
  if (iVar2 != 0) {
    if ((DAT_0a5181e5 & 1) == 0) {
      DAT_0a5181e0 = (undefined4)ram0x08782918;
      DAT_0a5181e4 = 0;
      DAT_0a5181e5 = 1;
    }
    if ((DAT_0a518225 & 1) == 0) {
      DAT_0a518218._0_1_ = s_co_job_ico_job_c________join_____09685c10[0x20];
      DAT_0a518218._1_1_ = s_co_job_ico_job_c________join_____09685c10[0x21];
      DAT_0a518218._2_1_ = s_co_job_ico_job_c________join_____09685c10[0x22];
      DAT_0a518218._3_1_ = s_co_job_ico_job_c________join_____09685c10[0x23];
      DAT_0a518218._4_1_ = s_co_job_ico_job_c________join_____09685c10[0x24];
      DAT_0a518218._5_1_ = s_co_job_ico_job_c________join_____09685c10[0x25];
      DAT_0a518218._6_1_ = s_co_job_ico_job_c________join_____09685c10[0x26];
      DAT_0a518218._7_1_ = s_co_job_ico_job_c________join_____09685c10[0x27];
      DAT_0a518220 = (undefined4)DAT_08480948;
      DAT_0a518224 = 0;
      DAT_0a518225 = 1;
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
    FUN_0668db5c(local_138,&DAT_0a5181e0,&DAT_0a518218,&DAT_0a5181f8,0x3400000800);
    if (*(char *)((long)param_1 + 0x97) < '\0') {
      FUN_00018d20(&local_150,param_1[0x10],param_1[0x11]);
    }
    else {
      uStack_148 = param_1[0x11];
      local_150 = (undefined1 *)param_1[0x10];
      local_140 = param_1[0x12];
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
    plVar4 = (long *)(local_138[0] + 0x68);
    if (*(char *)(local_138[0] + 0x7f) < '\0') {
      plVar4 = (long *)*plVar4;
    }
    local_60 = &DAT_aaaaaaaa0000000f;
    puStack_58 = local_150;
    if (-1 < (long)local_140) {
      puStack_58 = (undefined1 *)&local_150;
    }
    local_40 = 0xaaaaaaaa00000006;
    local_50 = 0xaaaaaaaa00000010;
    puStack_48 = &DAT_aaaaaaaa00000000;
    local_68 = param_1;
    FUN_0668e1e4(local_138[0] + 0x38,&DAT_0a518208,plVar4,&local_68,2);
    FUN_0668dbac();
    if ((long)local_140 < 0) {
      __ZdlPvm(local_150,local_140 & 0x7fffffffffffffff);
    }
    thunk_FUN_0668e878(local_138);
  }
  if ((long *)param_1[0x29] != (long *)0x0) {
    (**(code **)(*(long *)param_1[0x29] + 8))();
    param_1[0x29] = 0;
  }
  plVar4 = (long *)param_1[0x23];
  if (plVar4 != (long *)0x0) {
    plVar3 = (long *)plVar4[3];
    if (plVar3 == plVar4) {
      pcVar5 = *(code **)(*plVar3 + 0x20);
LAB_0667f368:
      (*pcVar5)();
    }
    else if (plVar3 != (long *)0x0) {
      pcVar5 = *(code **)(*plVar3 + 0x28);
      goto LAB_0667f368;
    }
    __ZdlPvm(plVar4,0x20);
    param_1[0x23] = 0;
  }
  plVar4 = (long *)param_1[0x27];
  if (plVar4 == param_1 + 0x24) {
    pcVar5 = *(code **)(*plVar4 + 0x20);
  }
  else {
    if (plVar4 == (long *)0x0) goto LAB_0667f3a8;
    pcVar5 = *(code **)(*plVar4 + 0x28);
  }
  (*pcVar5)();
LAB_0667f3a8:
  if (*(char *)((long)param_1 + 0xf7) < '\0') {
    __ZdlPvm(param_1[0x1c],param_1[0x1e] & 0x7fffffffffffffff);
  }
  plVar4 = (long *)param_1[0x1a];
  if (plVar4 != (long *)0x0) {
    LOAcquire();
    lVar1 = plVar4[1];
    plVar4[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*plVar4 + 0x10))(plVar4);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  plVar4 = (long *)param_1[0x18];
  if (plVar4 != (long *)0x0) {
    LOAcquire();
    lVar1 = plVar4[1];
    plVar4[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*plVar4 + 0x10))(plVar4);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  plVar4 = (long *)param_1[0x16];
  if (plVar4 != (long *)0x0) {
    LOAcquire();
    lVar1 = plVar4[1];
    plVar4[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*plVar4 + 0x10))(plVar4);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if (param_1[0x14] != 0) {
    __ZNSt3__119__shared_weak_count14__release_weakEv();
  }
  *param_1 = &PTR_FUN_09fb2cc8;
  if (*(char *)((long)param_1 + 0x97) < '\0') {
    __ZdlPvm(param_1[0x10],param_1[0x12] & 0x7fffffffffffffff);
  }
  FUN_06685cbc(param_1 + 3);
  FUN_0668614c(param_1 + 1);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return param_1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


