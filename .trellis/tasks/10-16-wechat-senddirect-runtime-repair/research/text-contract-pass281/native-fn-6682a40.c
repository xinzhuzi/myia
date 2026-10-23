// Ghidra inferred pseudocode; requested=0x6682a40
// entry=06682a40 end=06682ccb

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_06682a40(long param_1,long *param_2)

{
  long lVar1;
  ulong uVar2;
  long *plVar3;
  long lVar4;
  long *plVar5;
  undefined1 *local_140;
  undefined8 uStack_138;
  ulong local_130;
  long local_128 [26];
  undefined1 *local_58;
  undefined8 local_50;
  undefined1 *local_48;
  undefined8 local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  FUN_06686370(*param_2 + 8,param_1);
  __ZNSt3__15mutex4lockEv(param_1 + 0x78);
  if ((*(long *)(param_1 + 200) != 0) && (*param_2 == *(long *)(*(long *)(param_1 + 0xc0) + 0x10)))
  {
    uVar2 = FUN_0668dad0(0);
    if ((uVar2 & 1) != 0) {
      if ((DAT_0a518455 & 1) == 0) {
        DAT_0a518450 = (undefined4)ram0x08782918;
        DAT_0a518454 = 0;
        DAT_0a518455 = 1;
      }
      if ((DAT_0a518571 & 1) == 0) {
        DAT_0a518568._0_1_ = s_pop_job_pop_job_add_job_09686160[0];
        DAT_0a518568._1_1_ = s_pop_job_pop_job_add_job_09686160[1];
        DAT_0a518568._2_1_ = s_pop_job_pop_job_add_job_09686160[2];
        DAT_0a518568._3_1_ = s_pop_job_pop_job_add_job_09686160[3];
        DAT_0a518568._4_1_ = s_pop_job_pop_job_add_job_09686160[4];
        DAT_0a518568._5_1_ = s_pop_job_pop_job_add_job_09686160[5];
        DAT_0a518568._6_1_ = s_pop_job_pop_job_add_job_09686160[6];
        DAT_0a518568._7_1_ = s_pop_job_pop_job_add_job_09686160[7];
        DAT_0a518570 = 0;
        DAT_0a518571 = 1;
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
      FUN_0668db5c(local_128,&DAT_0a518450,&DAT_0a518568,&DAT_0a518470,0x6800000800);
      lVar4 = *param_2;
      if (*(char *)(lVar4 + 0x97) < '\0') {
        FUN_00018d20(&local_140,*(undefined8 *)(lVar4 + 0x80),*(undefined8 *)(lVar4 + 0x88));
      }
      else {
        uStack_138 = *(undefined8 *)(lVar4 + 0x88);
        local_140 = *(undefined1 **)(lVar4 + 0x80);
        local_130 = *(ulong *)(lVar4 + 0x90);
      }
      if ((DAT_0a518583 & 1) == 0) {
        DAT_0a518578._0_1_ = s_pop_job_pop_job_add_job_09686160[8];
        DAT_0a518578._1_1_ = s_pop_job_pop_job_add_job_09686160[9];
        DAT_0a518578._2_1_ = s_pop_job_pop_job_add_job_09686160[10];
        DAT_0a518578._3_1_ = s_pop_job_pop_job_add_job_09686160[0xb];
        DAT_0a518578._4_1_ = s_pop_job_pop_job_add_job_09686160[0xc];
        DAT_0a518578._5_1_ = s_pop_job_pop_job_add_job_09686160[0xd];
        DAT_0a518578._6_1_ = s_pop_job_pop_job_add_job_09686160[0xe];
        DAT_0a518578._7_1_ = s_pop_job_pop_job_add_job_09686160[0xf];
        DAT_0a518580 = 0x5f25;
        DAT_0a518582 = 0;
        DAT_0a518583 = 1;
      }
      plVar3 = (long *)(local_128[0] + 0x68);
      if (*(char *)(local_128[0] + 0x7f) < '\0') {
        plVar3 = (long *)*plVar3;
      }
      local_58 = local_140;
      if (-1 < (long)local_130) {
        local_58 = (undefined1 *)&local_140;
      }
      local_50 = 0xaaaaaaaa00000010;
      local_40 = 0xaaaaaaaa00000006;
      local_48 = &DAT_aaaaaaaa00000000;
      FUN_0668e1e4(local_128[0] + 0x38,&DAT_0a518578,plVar3,&local_58,1);
      FUN_0668dbac();
      if ((long)local_130 < 0) {
        __ZdlPvm(local_140,local_130 & 0x7fffffffffffffff);
      }
      thunk_FUN_0668e878(local_128);
    }
    plVar3 = *(long **)(param_1 + 0xc0);
    lVar1 = *(long *)(param_1 + 200);
    lVar4 = *plVar3;
    plVar5 = (long *)plVar3[1];
    *(long **)(lVar4 + 8) = plVar5;
    *plVar5 = lVar4;
    *(long *)(param_1 + 200) = lVar1 + -1;
    plVar5 = (long *)plVar3[3];
    if (plVar5 != (long *)0x0) {
      LOAcquire();
      lVar4 = plVar5[1];
      plVar5[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*plVar5 + 0x10))(plVar5);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
      }
    }
    __ZdlPvm(plVar3,0x20);
  }
  __ZNSt3__15mutex6unlockEv(param_1 + 0x78);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


