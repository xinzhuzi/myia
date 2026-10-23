// Ghidra inferred pseudocode; requested=0x6683134
// entry=06683134 end=066833e7

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_06683134(long param_1,long param_2)

{
  ulong uVar1;
  long *plVar2;
  long *plVar3;
  long lVar4;
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
  __ZNSt3__15mutex4lockEv(param_1 + 0x78);
  plVar2 = (long *)(param_1 + 0xb8);
  plVar3 = *(long **)(param_1 + 0xc0);
  if (plVar3 == plVar2) {
LAB_06683194:
    if (plVar3 != plVar2) {
      uVar1 = FUN_0668dad0(0);
      if ((uVar1 & 1) != 0) {
        if ((DAT_0a518455 & 1) == 0) {
          DAT_0a518450 = (undefined4)ram0x08782918;
          DAT_0a518454 = 0;
          DAT_0a518455 = 1;
        }
        if ((DAT_0a518596 & 1) == 0) {
          DAT_0a518588._0_1_ = s_on_complerase_jo_09686178[0];
          DAT_0a518588._1_1_ = s_on_complerase_jo_09686178[1];
          DAT_0a518588._2_1_ = s_on_complerase_jo_09686178[2];
          DAT_0a518588._3_1_ = s_on_complerase_jo_09686178[3];
          DAT_0a518588._4_1_ = s_on_complerase_jo_09686178[4];
          DAT_0a518588._5_1_ = s_on_complerase_jo_09686178[5];
          DAT_0a518588._6_1_ = s_on_complerase_jo_09686178[6];
          DAT_0a518588._7_1_ = s_on_complerase_jo_09686178[7];
          DAT_0a518590 = (undefined4)DAT_084ac0b8;
          DAT_0a518594 = 0x5f;
          DAT_0a518596 = 1;
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
        FUN_0668db5c(local_128,&DAT_0a518450,&DAT_0a518588,&DAT_0a518470,0x7300000800);
        lVar4 = plVar3[2];
        if (*(char *)(lVar4 + 0x97) < '\0') {
          FUN_00018d20(&local_140,*(undefined8 *)(lVar4 + 0x80),*(undefined8 *)(lVar4 + 0x88));
        }
        else {
          uStack_138 = *(undefined8 *)(lVar4 + 0x88);
          local_140 = *(undefined1 **)(lVar4 + 0x80);
          local_130 = *(ulong *)(lVar4 + 0x90);
        }
        if ((DAT_0a5185a5 & 1) == 0) {
          DAT_0a518598._0_1_ = s_on_complerase_jo_09686178[8];
          DAT_0a518598._1_1_ = s_on_complerase_jo_09686178[9];
          DAT_0a518598._2_1_ = s_on_complerase_jo_09686178[10];
          DAT_0a518598._3_1_ = s_on_complerase_jo_09686178[0xb];
          DAT_0a518598._4_1_ = s_on_complerase_jo_09686178[0xc];
          DAT_0a518598._5_1_ = s_on_complerase_jo_09686178[0xd];
          DAT_0a518598._6_1_ = s_on_complerase_jo_09686178[0xe];
          DAT_0a518598._7_1_ = s_on_complerase_jo_09686178[0xf];
          DAT_0a5185a0 = (undefined4)DAT_08781110;
          DAT_0a5185a4 = 0;
          DAT_0a5185a5 = 1;
        }
        plVar2 = (long *)(local_128[0] + 0x68);
        if (*(char *)(local_128[0] + 0x7f) < '\0') {
          plVar2 = (long *)*plVar2;
        }
        local_58 = local_140;
        if (-1 < (long)local_130) {
          local_58 = (undefined1 *)&local_140;
        }
        local_50 = 0xaaaaaaaa00000010;
        local_40 = 0xaaaaaaaa00000006;
        local_48 = &DAT_aaaaaaaa00000000;
        FUN_0668e1e4(local_128[0] + 0x38,&DAT_0a518598,plVar2,&local_58,1);
        FUN_0668dbac();
        if ((long)local_130 < 0) {
          __ZdlPvm(local_140,local_130 & 0x7fffffffffffffff);
        }
        thunk_FUN_0668e878(local_128);
      }
      lVar4 = *plVar3;
      plVar2 = (long *)plVar3[1];
      *(long **)(lVar4 + 8) = plVar2;
      *plVar2 = lVar4;
      *(long *)(param_1 + 200) = *(long *)(param_1 + 200) + -1;
      plVar2 = (long *)plVar3[3];
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
      __ZdlPvm(plVar3,0x20);
    }
  }
  else {
    do {
      if (plVar3[2] == param_2) goto LAB_06683194;
      plVar3 = (long *)plVar3[1];
    } while (plVar3 != plVar2);
  }
  lVar4 = *(long *)(param_1 + 200);
  __ZNSt3__15mutex6unlockEv(param_1 + 0x78);
  if (lVar4 == 0) {
    FUN_0297faec(param_1);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_38) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


