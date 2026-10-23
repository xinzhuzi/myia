// Ghidra inferred pseudocode; requested=0x66823c4
// entry=066823c4 end=066826db

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_066823c4(long param_1)

{
  int iVar1;
  long *plVar2;
  long *plVar3;
  long lVar4;
  undefined1 *local_150;
  undefined8 uStack_148;
  ulong local_140;
  long *local_138;
  long *local_130;
  undefined1 *local_68;
  undefined8 local_60;
  undefined1 *local_58;
  undefined8 local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  iVar1 = FUN_0668dad0(0);
  if (iVar1 != 0) {
    if ((DAT_0a518455 & 1) == 0) {
      DAT_0a518450 = (undefined4)ram0x08782918;
      DAT_0a518454 = 0;
      DAT_0a518455 = 1;
    }
    if ((DAT_0a518531 & 1) == 0) {
      DAT_0a51852c = (undefined4)DAT_08728498;
      DAT_0a518530 = 0;
      DAT_0a518531 = 1;
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
    FUN_0668db5c(&local_138,&DAT_0a518450,&DAT_0a51852c,&DAT_0a518470,0x4300000800);
    plVar3 = local_138;
    if (*(char *)(param_1 + 0xef) < '\0') {
      FUN_00018d20(&local_150,*(undefined8 *)(param_1 + 0xd8),*(undefined8 *)(param_1 + 0xe0));
    }
    else {
      uStack_148 = *(undefined8 *)(param_1 + 0xe0);
      local_150 = *(undefined1 **)(param_1 + 0xd8);
      local_140 = *(ulong *)(param_1 + 0xe8);
    }
    if ((DAT_0a51850c & 1) == 0) {
      DAT_0a518500 = DAT_09686150;
      DAT_0a518508 = (undefined4)DAT_09686158;
      DAT_0a51850c = 1;
    }
    plVar2 = plVar3 + 0xd;
    if (*(char *)((long)plVar3 + 0x7f) < '\0') {
      plVar2 = (long *)*plVar2;
    }
    local_68 = local_150;
    if (-1 < (long)local_140) {
      local_68 = (undefined1 *)&local_150;
    }
    local_60 = 0xaaaaaaaa00000010;
    local_50 = 0xaaaaaaaa00000006;
    local_58 = &DAT_aaaaaaaa00000000;
    FUN_0668e1e4(plVar3 + 7,&DAT_0a518500,plVar2,&local_68,1);
    lVar4 = *plVar3;
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
    local_68 = *(undefined1 **)(param_1 + 200);
    plVar3 = (long *)(lVar4 + 0x68);
    if (*(char *)(lVar4 + 0x7f) < '\0') {
      plVar3 = (long *)*plVar3;
    }
    local_60 = 0xaaaaaaaa00000009;
    local_50 = 0xaaaaaaaa00000006;
    local_58 = &DAT_aaaaaaaa00000000;
    FUN_0668e1e4(lVar4 + 0x38,&DAT_0a518510,plVar3,&local_68,1);
    FUN_0668dbac();
    if ((long)local_140 < 0) {
      __ZdlPvm(local_150,local_140 & 0x7fffffffffffffff);
    }
    thunk_FUN_0668e878(&local_138);
  }
  __ZNSt3__15mutex4lockEv(param_1 + 0x78);
  lVar4 = *(long *)(param_1 + 200);
  while (lVar4 != 0) {
    lVar4 = *(long *)(param_1 + 0xc0);
    plVar3 = *(long **)(lVar4 + 0x10);
    plVar2 = *(long **)(lVar4 + 0x18);
    if (plVar2 != (long *)0x0) {
      lVar4 = plVar2[1];
      plVar2[1] = lVar4 + 1;
    }
    local_138 = plVar3;
    local_130 = plVar2;
    __ZNSt3__15mutex6unlockEv(lVar4,param_1 + 0x78);
    if (plVar3 != (long *)0x0) {
      (**(code **)(*plVar3 + 0x20))(plVar3);
      FUN_06682a40(param_1,&local_138);
      plVar2 = local_130;
    }
    if (plVar2 != (long *)0x0) {
      LOAcquire();
      lVar4 = plVar2[1];
      plVar2[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*plVar2 + 0x10))(plVar2);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
      }
    }
    if (plVar3 == (long *)0x0) goto LAB_066826a8;
    __ZNSt3__15mutex4lockEv(param_1 + 0x78);
    lVar4 = *(long *)(param_1 + 200);
  }
  __ZNSt3__15mutex6unlockEv(param_1 + 0x78);
LAB_066826a8:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


