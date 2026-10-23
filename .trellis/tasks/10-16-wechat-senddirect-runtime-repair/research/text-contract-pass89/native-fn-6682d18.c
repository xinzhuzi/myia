// Ghidra inferred pseudocode; requested=0x6682d18
// entry=06682d18 end=066830b7

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_06682d18(long *param_1,long *param_2)

{
  long lVar1;
  long *plVar2;
  ulong uVar3;
  long *plVar4;
  undefined1 *local_170;
  undefined8 uStack_168;
  ulong local_160;
  undefined8 ***local_150;
  long lStack_148;
  ulong local_140;
  long *local_138;
  code *pcStack_130;
  code *local_128;
  undefined8 uStack_120;
  code *local_118;
  undefined8 ***local_68;
  long *local_60;
  undefined1 *puStack_58;
  undefined8 local_50;
  undefined1 *puStack_48;
  undefined8 local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  pcStack_130 = FUN_06683424;
  local_128 = FUN_06683134;
  uStack_120 = 0;
  local_118 = FUN_06683440;
  local_68 = (undefined8 ***)0x0;
  local_60 = (long *)0x0;
  local_138 = param_1;
  FUN_06686420(*param_2 + 8,&local_138,0,1,0,&local_68);
  plVar2 = local_60;
  if (local_60 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_60[1];
    local_60[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_60 + 0x10))(local_60);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  __ZNSt3__15mutex4lockEv(param_1 + 0xf);
  plVar2 = (long *)__Znwm(0x20);
  lVar1 = param_2[1];
  plVar2[2] = *param_2;
  plVar2[3] = lVar1;
  if (lVar1 != 0) {
    *(long *)(lVar1 + 8) = *(long *)(lVar1 + 8) + 1;
  }
  lVar1 = param_1[0x17];
  *plVar2 = lVar1;
  plVar2[1] = (long)(param_1 + 0x17);
  *(long **)(lVar1 + 8) = plVar2;
  param_1[0x17] = (long)plVar2;
  param_1[0x19] = param_1[0x19] + 1;
  uVar3 = FUN_0668dad0(0);
  if ((uVar3 & 1) != 0) {
    if ((DAT_0a518455 & 1) == 0) {
      DAT_0a518450 = (undefined4)ram0x08782918;
      DAT_0a518454 = 0;
      DAT_0a518455 = 1;
    }
    if ((DAT_0a518540 & 1) == 0) {
      DAT_0a518538._0_1_ = s_pop_job_pop_job_add_job_09686160[0x10];
      DAT_0a518538._1_1_ = s_pop_job_pop_job_add_job_09686160[0x11];
      DAT_0a518538._2_1_ = s_pop_job_pop_job_add_job_09686160[0x12];
      DAT_0a518538._3_1_ = s_pop_job_pop_job_add_job_09686160[0x13];
      DAT_0a518538._4_1_ = s_pop_job_pop_job_add_job_09686160[0x14];
      DAT_0a518538._5_1_ = s_pop_job_pop_job_add_job_09686160[0x15];
      DAT_0a518538._6_1_ = s_pop_job_pop_job_add_job_09686160[0x16];
      DAT_0a518538._7_1_ = s_pop_job_pop_job_add_job_09686160[0x17];
      DAT_0a518540 = 1;
    }
    if ((DAT_0a518481 & 1) == 0) {
      uRam000000000a518478._0_1_ = s_co_job_group_cppjobs__size_______09686190[8];
      uRam000000000a518478._1_1_ = s_co_job_group_cppjobs__size_______09686190[9];
      uRam000000000a518478._2_1_ = s_co_job_group_cppjobs__size_______09686190[10];
      uRam000000000a518478._3_1_ = s_co_job_group_cppjobs__size_______09686190[0xb];
      uRam000000000a518478._4_1_ = s_co_job_group_cppjobs__size_______09686190[0xc];
      uRam000000000a518478._5_1_ = s_co_job_group_cppjobs__size_______09686190[0xd];
      uRam000000000a518478._6_1_ = s_co_job_group_cppjobs__size_______09686190[0xe];
      uRam000000000a518478._7_1_ = s_co_job_group_cppjobs__size_______09686190[0xf];
      DAT_0a518470 = s_co_job_group_cppjobs__size_______09686190[0];
      DAT_0a518470_1._0_1_ = s_co_job_group_cppjobs__size_______09686190[1];
      DAT_0a518470_1._1_1_ = s_co_job_group_cppjobs__size_______09686190[2];
      DAT_0a518470_1._2_1_ = s_co_job_group_cppjobs__size_______09686190[3];
      DAT_0a518470_1._3_1_ = s_co_job_group_cppjobs__size_______09686190[4];
      DAT_0a518470_1._4_1_ = s_co_job_group_cppjobs__size_______09686190[5];
      DAT_0a518470_1._5_1_ = s_co_job_group_cppjobs__size_______09686190[6];
      DAT_0a518470_1._6_1_ = s_co_job_group_cppjobs__size_______09686190[7];
      DAT_0a518480 = 0;
      DAT_0a518481 = 1;
    }
    FUN_0668db5c(&local_138,&DAT_0a518450,&DAT_0a518538,&DAT_0a518470,0x5300000800);
    plVar2 = local_138;
    if (*(char *)((long)param_1 + 0xef) < '\0') {
      FUN_00018d20(&local_150,param_1[0x1b],param_1[0x1c]);
    }
    else {
      lStack_148 = param_1[0x1c];
      local_150 = (undefined8 ***)param_1[0x1b];
      local_140 = param_1[0x1d];
    }
    lVar1 = *param_2;
    if (*(char *)(lVar1 + 0x97) < '\0') {
      FUN_00018d20(&local_170,*(undefined8 *)(lVar1 + 0x80),*(undefined8 *)(lVar1 + 0x88));
    }
    else {
      uStack_168 = *(undefined8 *)(lVar1 + 0x88);
      local_170 = *(undefined1 **)(lVar1 + 0x80);
      local_160 = *(ulong *)(lVar1 + 0x90);
    }
    if ((DAT_0a518560 & 1) == 0) {
      uRam000000000a518558._0_1_ = s_co_job_group_cppjobs__size_______09686190[0x28];
      uRam000000000a518558._1_1_ = s_co_job_group_cppjobs__size_______09686190[0x29];
      uRam000000000a518558._2_1_ = s_co_job_group_cppjobs__size_______09686190[0x2a];
      uRam000000000a518558._3_1_ = s_co_job_group_cppjobs__size_______09686190[0x2b];
      uRam000000000a518558._4_1_ = s_co_job_group_cppjobs__size_______09686190[0x2c];
      uRam000000000a518558._5_1_ = s_co_job_group_cppjobs__size_______09686190[0x2d];
      uRam000000000a518558._6_1_ = s_co_job_group_cppjobs__size_______09686190[0x2e];
      uRam000000000a518558._7_1_ = s_co_job_group_cppjobs__size_______09686190[0x2f];
      DAT_0a518550 = s_co_job_group_cppjobs__size_______09686190[0x20];
      DAT_0a518550_1._0_1_ = s_co_job_group_cppjobs__size_______09686190[0x21];
      DAT_0a518550_1._1_1_ = s_co_job_group_cppjobs__size_______09686190[0x22];
      DAT_0a518550_1._2_1_ = s_co_job_group_cppjobs__size_______09686190[0x23];
      DAT_0a518550_1._3_1_ = s_co_job_group_cppjobs__size_______09686190[0x24];
      DAT_0a518550_1._4_1_ = s_co_job_group_cppjobs__size_______09686190[0x25];
      DAT_0a518550_1._5_1_ = s_co_job_group_cppjobs__size_______09686190[0x26];
      DAT_0a518550_1._6_1_ = s_co_job_group_cppjobs__size_______09686190[0x27];
      DAT_0a518560 = 1;
    }
    plVar4 = plVar2 + 0xd;
    if (*(char *)((long)plVar2 + 0x7f) < '\0') {
      plVar4 = (long *)*plVar4;
    }
    local_60 = (long *)0xaaaaaaaa00000010;
    local_68 = local_150;
    if (-1 < (long)local_140) {
      local_68 = &local_150;
    }
    puStack_58 = local_170;
    if (-1 < (long)local_160) {
      puStack_58 = (undefined1 *)&local_170;
    }
    local_40 = 0xaaaaaaaa00000006;
    local_50 = 0xaaaaaaaa00000010;
    puStack_48 = &DAT_aaaaaaaa00000000;
    FUN_0668e1e4(plVar2 + 7,&DAT_0a518550,plVar4,&local_68,2);
    lVar1 = *plVar2;
    if ((DAT_0a518522 & 1) == 0) {
      uRam000000000a518518._0_1_ = s_co_job_group_cppjobs__size_______09686190[0x18];
      uRam000000000a518518._1_1_ = s_co_job_group_cppjobs__size_______09686190[0x19];
      uRam000000000a518518._2_1_ = s_co_job_group_cppjobs__size_______09686190[0x1a];
      uRam000000000a518518._3_1_ = s_co_job_group_cppjobs__size_______09686190[0x1b];
      uRam000000000a518518._4_1_ = s_co_job_group_cppjobs__size_______09686190[0x1c];
      uRam000000000a518518._5_1_ = s_co_job_group_cppjobs__size_______09686190[0x1d];
      uRam000000000a518518._6_1_ = s_co_job_group_cppjobs__size_______09686190[0x1e];
      uRam000000000a518518._7_1_ = s_co_job_group_cppjobs__size_______09686190[0x1f];
      DAT_0a518510 = s_co_job_group_cppjobs__size_______09686190[0x10];
      DAT_0a518510_1._0_1_ = s_co_job_group_cppjobs__size_______09686190[0x11];
      DAT_0a518510_1._1_1_ = s_co_job_group_cppjobs__size_______09686190[0x12];
      DAT_0a518510_1._2_1_ = s_co_job_group_cppjobs__size_______09686190[0x13];
      DAT_0a518510_1._3_1_ = s_co_job_group_cppjobs__size_______09686190[0x14];
      DAT_0a518510_1._4_1_ = s_co_job_group_cppjobs__size_______09686190[0x15];
      DAT_0a518510_1._5_1_ = s_co_job_group_cppjobs__size_______09686190[0x16];
      DAT_0a518510_1._6_1_ = s_co_job_group_cppjobs__size_______09686190[0x17];
      DAT_0a518520 = 0x5f;
      DAT_0a518522 = 1;
    }
    local_68 = (undefined8 ***)param_1[0x19];
    plVar2 = (long *)(lVar1 + 0x68);
    if (*(char *)(lVar1 + 0x7f) < '\0') {
      plVar2 = (long *)*plVar2;
    }
    local_60 = (long *)0xaaaaaaaa00000009;
    local_50 = 0xaaaaaaaa00000006;
    puStack_58 = &DAT_aaaaaaaa00000000;
    FUN_0668e1e4(lVar1 + 0x38,&DAT_0a518510,plVar2,&local_68,1);
    FUN_0668dbac();
    if ((long)local_160 < 0) {
      __ZdlPvm(local_170,local_160 & 0x7fffffffffffffff);
    }
    if ((long)local_140 < 0) {
      __ZdlPvm(local_150,local_140 & 0x7fffffffffffffff);
    }
    thunk_FUN_0668e878(&local_138);
  }
  __ZNSt3__15mutex6unlockEv(param_1 + 0xf);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


