// Ghidra inferred pseudocode; requested=0x6677b20
// entry=06677b20 end=06677dcb

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_06677b20(long param_1)

{
  undefined4 uVar1;
  int iVar2;
  byte *pbVar3;
  undefined8 uVar4;
  long *plVar5;
  long lVar6;
  undefined8 uVar7;
  long local_118;
  long *local_110;
  undefined1 *local_48;
  undefined8 local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  if ((*(long **)(param_1 + 0x18) == (long *)0x0) ||
     (iVar2 = (**(code **)(**(long **)(param_1 + 0x18) + 0x30))(), iVar2 != 0)) {
    pbVar3 = (byte *)(*(code *)PTR___tlv_bootstrap_0a24dec8)();
    if ((*pbVar3 & 1) == 0) {
      FUN_07134000();
    }
    uVar4 = (*(code *)PTR___tlv_bootstrap_0a24deb0)();
    lVar6 = *(long *)(param_1 + 0x20);
    uVar1 = *(undefined4 *)(lVar6 + 0x3cc);
    uVar7 = *(undefined8 *)(param_1 + 0x30);
    FUN_066767e8(&local_118,uVar4,*(undefined8 *)(lVar6 + 0x270));
    FUN_066761cc(local_118,(long *)(param_1 + 0x20),uVar1,uVar7);
    if (local_110 != (long *)0x0) {
      LOAcquire();
      lVar6 = local_110[1];
      local_110[1] = lVar6 + -1;
      LORelease();
      if (lVar6 == 0) {
        (**(code **)(*local_110 + 0x10))(local_110);
        __ZNSt3__119__shared_weak_count14__release_weakEv(local_110);
      }
    }
  }
  else {
    iVar2 = FUN_0668dad0();
    if (iVar2 != 0) {
      if ((DAT_0a517add & 1) == 0) {
        DAT_0a517ad8 = (undefined4)ram0x08782918;
        DAT_0a517adc = 0;
        DAT_0a517add = 1;
      }
      if ((DAT_0a517c53 & 1) == 0) {
        DAT_0a517c48._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
        DAT_0a517c48._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
        DAT_0a517c48._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
        DAT_0a517c48._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
        DAT_0a517c48._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
        DAT_0a517c48._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
        DAT_0a517c48._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
        DAT_0a517c48._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
        DAT_0a517c50 = 0x2928;
        DAT_0a517c52 = 0;
        DAT_0a517c53 = 1;
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
      FUN_0668db5c(&local_118,&DAT_0a517ad8,&DAT_0a517c48,&DAT_0a517ae0,0x15300000800);
      if ((DAT_0a517d20 & 1) == 0) {
        _DAT_0a517cf4 = CONCAT44((int)DAT_084d1018,(int)DAT_084ca3e0);
        uRam000000000a517cfc = CONCAT44((int)DAT_089069d8,(int)DAT_086eef70);
        _DAT_0a517d04 = CONCAT44((int)DAT_09684c50,(int)DAT_087ec760);
        uRam000000000a517d0c = CONCAT44((int)DAT_08502a60,(int)DAT_086a84c8);
        DAT_0a517d14 = CONCAT44((int)DAT_0854de08,(int)DAT_085411d0);
        DAT_0a517d1c = (undefined4)DAT_0854de10;
        DAT_0a517d20 = 1;
      }
      plVar5 = (long *)(local_118 + 0x68);
      if (*(char *)(local_118 + 0x7f) < '\0') {
        plVar5 = (long *)*plVar5;
      }
      local_40 = 0xaaaaaaaa00000006;
      local_48 = &DAT_aaaaaaaa00000000;
      FUN_0668e1e4(local_118 + 0x38,&DAT_0a517cf4,plVar5,&local_48,0);
      FUN_0668dbac();
      thunk_FUN_0668e878(&local_118);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


