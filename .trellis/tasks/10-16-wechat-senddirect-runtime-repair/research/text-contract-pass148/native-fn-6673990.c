// Ghidra inferred pseudocode; requested=0x6673990
// entry=06673990 end=06673f83

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_06673990(long *param_1,long param_2,long *param_3)

{
  long lVar1;
  long lVar2;
  ulong uVar3;
  long *plVar4;
  long *plVar5;
  code *pcVar6;
  long **pplVar7;
  long *plVar8;
  long local_1b0;
  long *local_1a8;
  undefined1 auStack_178 [48];
  undefined8 ***local_148 [2];
  char local_131;
  long alStack_e0 [3];
  long *local_c8;
  long local_c0;
  long *plStack_b8;
  long local_b0;
  long alStack_a8 [3];
  long *local_90;
  long local_88;
  undefined1 *local_80;
  long *plStack_78;
  undefined8 local_70;
  long lStack_68;
  undefined8 local_60;
  undefined1 *puStack_58;
  undefined8 local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  if (param_1[0x4d] == 0) {
    lVar2 = FUN_0668d9e8(5);
    if (lVar2 == 0) {
      FUN_0668e658();
    }
    else {
      if ((DAT_0a517add & 1) == 0) {
        DAT_0a517ad8 = (undefined4)ram0x08782918;
        DAT_0a517adc = 0;
        DAT_0a517add = 1;
      }
      if ((DAT_0a517cb2 & 1) == 0) {
        DAT_0a517ca8._0_1_ = s_co_core_resume_ie__i_09684bb0[8];
        DAT_0a517ca8._1_1_ = s_co_core_resume_ie__i_09684bb0[9];
        DAT_0a517ca8._2_1_ = s_co_core_resume_ie__i_09684bb0[10];
        DAT_0a517ca8._3_1_ = s_co_core_resume_ie__i_09684bb0[0xb];
        DAT_0a517ca8._4_1_ = s_co_core_resume_ie__i_09684bb0[0xc];
        DAT_0a517ca8._5_1_ = s_co_core_resume_ie__i_09684bb0[0xd];
        DAT_0a517ca8._6_1_ = s_co_core_resume_ie__i_09684bb0[0xe];
        DAT_0a517ca8._7_1_ = s_co_core_resume_ie__i_09684bb0[0xf];
        DAT_0a517cb0 = 0x66;
        DAT_0a517cb2 = 1;
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
      FUN_0668db5c(&local_1b0,&DAT_0a517ad8,&DAT_0a517ca8,&DAT_0a517ae0,0x14b0000a800);
      if ((DAT_0a517c03 & 1) == 0) {
        _DAT_0a517bec = CONCAT44((int)DAT_096830c8,(int)DAT_08b2fcb0);
        uRam000000000a517bf4 = CONCAT44((int)ram0x08480938,(int)DAT_08771500);
        DAT_0a517bfc = (undefined4)DAT_08b72b50;
        DAT_0a517c00 = 0x295f;
        DAT_0a517c02 = 0;
        DAT_0a517c03 = 1;
      }
      if ((DAT_0a517cba & 1) == 0) {
        DAT_0a517cb4 = (undefined4)DAT_08692140;
        DAT_0a517cb8 = 0x5f;
        DAT_0a517cba = 1;
      }
      if (-1 < local_131) {
        local_148[0] = local_148;
      }
      FUN_06670568(auStack_178,&DAT_0a517bec,local_148[0],&DAT_0a517cb4);
      thunk_FUN_0668e878(&local_1b0);
    }
  }
  else {
    FUN_0668e56c();
  }
  uVar3 = FUN_0668dad0(0);
  if ((uVar3 & 1) != 0) {
    if ((DAT_0a517add & 1) == 0) {
      DAT_0a517ad8 = (undefined4)ram0x08782918;
      DAT_0a517adc = 0;
      DAT_0a517add = 1;
    }
    if ((DAT_0a517cb2 & 1) == 0) {
      DAT_0a517ca8._0_1_ = s_co_core_resume_ie__i_09684bb0[8];
      DAT_0a517ca8._1_1_ = s_co_core_resume_ie__i_09684bb0[9];
      DAT_0a517ca8._2_1_ = s_co_core_resume_ie__i_09684bb0[10];
      DAT_0a517ca8._3_1_ = s_co_core_resume_ie__i_09684bb0[0xb];
      DAT_0a517ca8._4_1_ = s_co_core_resume_ie__i_09684bb0[0xc];
      DAT_0a517ca8._5_1_ = s_co_core_resume_ie__i_09684bb0[0xd];
      DAT_0a517ca8._6_1_ = s_co_core_resume_ie__i_09684bb0[0xe];
      DAT_0a517ca8._7_1_ = s_co_core_resume_ie__i_09684bb0[0xf];
      DAT_0a517cb0 = 0x66;
      DAT_0a517cb2 = 1;
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
    FUN_0668db5c(&local_1b0,&DAT_0a517ad8,&DAT_0a517ca8,&DAT_0a517ae0,0x14c00000800);
    if ((DAT_0a517cf0 & 1) == 0) {
      _DAT_0a517cbc = CONCAT44((int)DAT_088a71c8,(int)DAT_08487d28);
      uRam000000000a517cc4 = CONCAT44((int)DAT_086eef70,(int)DAT_084d1018);
      _DAT_0a517ccc = CONCAT44((int)DAT_087ec760,(int)DAT_089069d8);
      uRam000000000a517cd4 = CONCAT44((int)DAT_084de688,(int)ram0x09684bc0);
      _DAT_0a517cdc = CONCAT44((int)DAT_08b69bc8,(int)DAT_0877c0b0);
      uRam000000000a517ce4 = CONCAT44((int)DAT_08487480,(int)DAT_09684bc8);
      DAT_0a517cec = (undefined4)ram0x084c9468;
      DAT_0a517cf0 = 1;
    }
    plVar4 = (long *)(local_1b0 + 0x68);
    if (*(char *)(local_1b0 + 0x7f) < '\0') {
      plVar4 = (long *)*plVar4;
    }
    local_88 = param_1[0x74];
    local_80 = &DAT_aaaaaaaa0000000b;
    local_70 = 0xaaaaaaaa00000010;
    plStack_78 = (long *)param_1[0x75];
    if (-1 < *(char *)((long)param_1 + 0x3bf)) {
      plStack_78 = param_1 + 0x75;
    }
    local_50 = 0xaaaaaaaa00000006;
    local_60 = 0xaaaaaaaa0000000a;
    puStack_58 = &DAT_aaaaaaaa00000000;
    lStack_68 = param_2;
    FUN_0668e1e4(local_1b0 + 0x38,&DAT_0a517cbc,plVar4,&local_88,3);
    FUN_0668dbac();
    thunk_FUN_0668e878(&local_1b0);
  }
  lVar2 = *param_1;
  local_1b0 = lVar2;
  if ((param_1[1] == 0) ||
     (plVar4 = (long *)__ZNSt3__119__shared_weak_count4lockEv(), local_1a8 = plVar4,
     plVar4 == (long *)0x0)) {
                    /* WARNING: Subroutine does not return */
    FUN_00283500();
  }
  plVar8 = (long *)param_1[0x4d];
  pplVar7 = (long **)(param_3 + 3);
  plVar5 = *pplVar7;
  if (plVar5 == (long *)0x0) {
    pplVar7 = &local_c8;
LAB_06673dc0:
    *pplVar7 = (long *)0x0;
  }
  else {
    local_c8 = plVar5;
    if (plVar5 != param_3) goto LAB_06673dc0;
    local_c8 = alStack_e0;
    (**(code **)(*plVar5 + 0x18))(plVar5,alStack_e0);
  }
  lVar1 = plVar4[1];
  plVar4[1] = lVar1 + 1;
  local_90 = (long *)0x0;
  local_c0 = lVar2;
  plStack_b8 = plVar4;
  local_b0 = param_2;
  plVar4 = (long *)__Znwm(lVar1,0x40);
  *plVar4 = (long)&PTR_FUN_09fb2590;
  if (local_c8 == (long *)0x0) {
    pplVar7 = (long **)(plVar4 + 4);
LAB_06673e44:
    *pplVar7 = (long *)0x0;
  }
  else {
    if (local_c8 != alStack_e0) {
      pplVar7 = &local_c8;
      plVar4[4] = (long)local_c8;
      goto LAB_06673e44;
    }
    plVar4[4] = (long)(plVar4 + 1);
    (**(code **)(*local_c8 + 0x18))(local_c8);
    param_2 = local_b0;
  }
  plVar4[6] = (long)plStack_b8;
  plVar4[5] = local_c0;
  local_c0 = 0;
  plStack_b8 = (long *)0x0;
  plVar4[7] = param_2;
  local_90 = plVar4;
  (**(code **)(*plVar8 + 0x10))(plVar8,alStack_a8);
  if (local_90 == alStack_a8) {
    pcVar6 = *(code **)(*local_90 + 0x20);
LAB_06673ebc:
    (*pcVar6)();
  }
  else if (local_90 != (long *)0x0) {
    pcVar6 = *(code **)(*local_90 + 0x28);
    goto LAB_06673ebc;
  }
  plVar4 = plStack_b8;
  if (plStack_b8 != (long *)0x0) {
    LOAcquire();
    lVar2 = plStack_b8[1];
    plStack_b8[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*plStack_b8 + 0x10))(plStack_b8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if (local_c8 == alStack_e0) {
    pcVar6 = *(code **)(*local_c8 + 0x20);
  }
  else {
    if (local_c8 == (long *)0x0) goto LAB_06673f1c;
    pcVar6 = *(code **)(*local_c8 + 0x28);
  }
  (*pcVar6)();
LAB_06673f1c:
  plVar4 = local_1a8;
  if (local_1a8 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_1a8[1];
    local_1a8[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_1a8 + 0x10))(local_1a8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


