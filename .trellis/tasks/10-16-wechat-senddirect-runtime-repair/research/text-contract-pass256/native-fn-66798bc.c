// Ghidra inferred pseudocode; requested=0x66798bc
// entry=066798bc end=06679be7

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_066798bc(long param_1)

{
  int iVar1;
  long *plVar2;
  byte *pbVar3;
  undefined8 uVar4;
  undefined8 *puVar5;
  long lVar6;
  code *pcVar7;
  long local_158;
  long *local_150;
  undefined8 local_88;
  undefined1 *local_80;
  long lStack_78;
  undefined8 local_70;
  undefined1 *puStack_68;
  undefined8 local_60;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  puVar5 = &DAT_0a12cff8;
  lVar6 = 0x52;
  do {
    __ZNSt3__15mutex4lockEv(&DAT_0a12cfb0);
    pcVar7 = (code *)*puVar5;
    __ZNSt3__15mutex6unlockEv(&DAT_0a12cfb0);
    if ((pcVar7 != (code *)0x0) && (*(long *)(param_1 + lVar6 * 8) != 0)) {
      (*pcVar7)();
      *(undefined8 *)(param_1 + lVar6 * 8) = 0;
    }
    lVar6 = lVar6 + 1;
    puVar5 = puVar5 + 1;
  } while (lVar6 != 0x72);
  if (*(code **)(param_1 + 600) != (code *)0x0) {
    (**(code **)(param_1 + 600))(*(undefined8 *)(param_1 + 0x260));
    *(undefined8 *)(param_1 + 600) = 0;
  }
  plVar2 = *(long **)(param_1 + 0x270);
  if (plVar2 != (long *)0x0) {
    (**(code **)(*plVar2 + 0x18))
              (plVar2,*(undefined8 *)(param_1 + 0x278),*(undefined8 *)(param_1 + 0x280));
  }
  pbVar3 = (byte *)(*(code *)PTR___tlv_bootstrap_0a24dec8)();
  if ((*pbVar3 & 1) == 0) {
    FUN_07134000();
  }
  uVar4 = (*(code *)PTR___tlv_bootstrap_0a24deb0)();
  FUN_066767e8(&local_158,uVar4,*(undefined8 *)(param_1 + 0x270));
  FUN_06676714(local_158,param_1);
  if (local_150 != (long *)0x0) {
    LOAcquire();
    lVar6 = local_150[1];
    local_150[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*local_150 + 0x10))(local_150);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_150);
    }
  }
  iVar1 = FUN_0668dad0(1);
  if (iVar1 != 0) {
    if ((DAT_0a517add & 1) == 0) {
      DAT_0a517ad8 = (undefined4)ram0x08782918;
      DAT_0a517adc = 0;
      DAT_0a517add = 1;
    }
    if ((DAT_0a517f98 & 1) == 0) {
      DAT_0a517f90._0_1_ = s_sp_<_topcleanup_09684c90[8];
      DAT_0a517f90._1_1_ = s_sp_<_topcleanup_09684c90[9];
      DAT_0a517f90._2_1_ = s_sp_<_topcleanup_09684c90[10];
      DAT_0a517f90._3_1_ = s_sp_<_topcleanup_09684c90[0xb];
      DAT_0a517f90._4_1_ = s_sp_<_topcleanup_09684c90[0xc];
      DAT_0a517f90._5_1_ = s_sp_<_topcleanup_09684c90[0xd];
      DAT_0a517f90._6_1_ = s_sp_<_topcleanup_09684c90[0xe];
      DAT_0a517f90._7_1_ = s_sp_<_topcleanup_09684c90[0xf];
      DAT_0a517f98 = 1;
    }
    if ((DAT_0a517aec & 1) == 0) {
      DAT_0a517ae0._0_1_ = s_co_core_resume_ie__i_09684bb0[0];
      DAT_0a517ae0._1_1_ = s_co_core_resume_ie__i_09684bb0[1];
      DAT_0a517ae0._2_1_ = s_co_core_resume_ie__i_09684bb0[2];
      DAT_0a517ae0._3_1_ = s_co_core_resume_ie__i_09684bb0[3];
      DAT_0a517ae0._4_1_ = s_co_core_resume_ie__i_09684bb0[4];
      DAT_0a517ae0._5_1_ = s_co_core_resume_ie__i_09684bb0[5];
      DAT_0a517ae0._6_1_ = s_co_core_resume_ie__i_09684bb0[6];
      DAT_0a517ae0._7_1_ = s_co_core_resume_ie__i_09684bb0[7];
      DAT_0a517ae8 = (undefined4)DAT_085722b0;
      DAT_0a517aec = 1;
    }
    FUN_0668db5c(&local_158,&DAT_0a517ad8,&DAT_0a517f90,&DAT_0a517ae0,0x13900002800);
    if ((DAT_0a517fc0 & 1) == 0) {
      _DAT_0a517f9c = CONCAT44((int)DAT_087ec760,(int)DAT_089069d8);
      uRam000000000a517fa4 = CONCAT44((int)DAT_08563410,(int)DAT_08593ec8);
      _DAT_0a517fac = CONCAT44((int)DAT_084de688,(int)DAT_09684ca0);
      uRam000000000a517fb4 = CONCAT44((int)DAT_08b69bc8,(int)DAT_0877c0b0);
      DAT_0a517fbc = (undefined4)DAT_09684c88;
      DAT_0a517fc0 = 1;
    }
    plVar2 = (long *)(local_158 + 0x68);
    if (*(char *)(local_158 + 0x7f) < '\0') {
      plVar2 = (long *)*plVar2;
    }
    local_88 = *(undefined8 *)(param_1 + 0x3a0);
    local_80 = &DAT_aaaaaaaa0000000b;
    lStack_78 = *(long *)(param_1 + 0x3a8);
    if (-1 < *(char *)(param_1 + 0x3bf)) {
      lStack_78 = param_1 + 0x3a8;
    }
    local_60 = 0xaaaaaaaa00000006;
    local_70 = 0xaaaaaaaa00000010;
    puStack_68 = &DAT_aaaaaaaa00000000;
    FUN_0668e1e4(local_158 + 0x38,&DAT_0a517f9c,plVar2,&local_88,2);
    FUN_0668dbac();
    thunk_FUN_0668e878(&local_158);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


