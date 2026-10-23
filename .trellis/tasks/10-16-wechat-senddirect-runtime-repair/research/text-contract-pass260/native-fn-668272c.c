// Ghidra inferred pseudocode; requested=0x668272c
// entry=0668272c end=066829f3

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0668272c(long param_1)

{
  byte bVar1;
  int iVar2;
  long *plVar3;
  long lVar4;
  undefined1 *local_140;
  undefined8 uStack_138;
  ulong local_130;
  long *local_128 [26];
  undefined1 *local_58;
  undefined8 local_50;
  undefined1 *local_48;
  undefined8 local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  iVar2 = FUN_0668dad0(0);
  if (iVar2 != 0) {
    if ((DAT_0a518455 & 1) == 0) {
      DAT_0a518450 = (undefined4)ram0x08782918;
      DAT_0a518454 = 0;
      DAT_0a518455 = 1;
    }
    if ((DAT_0a51852b & 1) == 0) {
      DAT_0a518524 = (undefined4)DAT_0849e748;
      DAT_0a518528 = 0x6c65;
      DAT_0a51852a = 0;
      DAT_0a51852b = 1;
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
    FUN_0668db5c(local_128,&DAT_0a518450,&DAT_0a518524,&DAT_0a518470,0x3700000800);
    if (*(char *)(param_1 + 0xef) < '\0') {
      FUN_00018d20(&local_140,*(undefined8 *)(param_1 + 0xd8),*(undefined8 *)(param_1 + 0xe0));
    }
    else {
      uStack_138 = *(undefined8 *)(param_1 + 0xe0);
      local_140 = *(undefined1 **)(param_1 + 0xd8);
      local_130 = *(ulong *)(param_1 + 0xe8);
    }
    if ((DAT_0a51850c & 1) == 0) {
      DAT_0a518500 = DAT_09686150;
      DAT_0a518508 = (undefined4)DAT_09686158;
      DAT_0a51850c = 1;
    }
    plVar3 = local_128[0] + 0xd;
    if (*(char *)((long)local_128[0] + 0x7f) < '\0') {
      plVar3 = (long *)*plVar3;
    }
    local_58 = local_140;
    if (-1 < (long)local_130) {
      local_58 = (undefined1 *)&local_140;
    }
    local_50 = 0xaaaaaaaa00000010;
    local_40 = 0xaaaaaaaa00000006;
    local_48 = &DAT_aaaaaaaa00000000;
    FUN_0668e1e4(local_128[0] + 7,&DAT_0a518500,plVar3,&local_58,1);
    lVar4 = *local_128[0];
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
    local_58 = *(undefined1 **)(param_1 + 200);
    plVar3 = (long *)(lVar4 + 0x68);
    if (*(char *)(lVar4 + 0x7f) < '\0') {
      plVar3 = (long *)*plVar3;
    }
    local_50 = 0xaaaaaaaa00000009;
    local_40 = 0xaaaaaaaa00000006;
    local_48 = &DAT_aaaaaaaa00000000;
    FUN_0668e1e4(lVar4 + 0x38,&DAT_0a518510,plVar3,&local_58,1);
    FUN_0668dbac();
    if ((long)local_130 < 0) {
      __ZdlPvm(local_140,local_130 & 0x7fffffffffffffff);
    }
    thunk_FUN_0668e878(local_128);
  }
  __ZNSt3__15mutex4lockEv(param_1 + 0x78);
  LOAcquire();
  bVar1 = *(byte *)(param_1 + 0xd1);
  *(byte *)(param_1 + 0xd1) = 1;
  LORelease();
  if ((bVar1 & 1) == 0) {
    for (lVar4 = *(long *)(param_1 + 0xc0); lVar4 != param_1 + 0xb8; lVar4 = *(long *)(lVar4 + 8)) {
      if (*(long **)(lVar4 + 0x10) != (long *)0x0) {
        (**(code **)(**(long **)(lVar4 + 0x10) + 0x18))();
      }
    }
  }
  __ZNSt3__15mutex6unlockEv(param_1 + 0x78);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


