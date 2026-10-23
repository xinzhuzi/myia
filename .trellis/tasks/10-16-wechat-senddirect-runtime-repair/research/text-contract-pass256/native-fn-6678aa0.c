// Ghidra inferred pseudocode; requested=0x6678aa0
// entry=06678aa0 end=0667903f

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_06678aa0(long param_1)

{
  long lVar1;
  long *plVar2;
  long lVar3;
  int iVar4;
  ulong uVar5;
  long *plVar6;
  long lVar7;
  long local_148;
  long *local_140;
  undefined8 local_78;
  undefined1 *local_70;
  long lStack_68;
  undefined8 local_60;
  undefined1 *puStack_58;
  undefined8 local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  FUN_0001accc(0);
  iVar4 = FUN_0668dad0(1);
  if (iVar4 != 0) {
    if ((DAT_0a517add & 1) == 0) {
      DAT_0a517ad8 = (undefined4)ram0x08782918;
      DAT_0a517adc = 0;
      DAT_0a517add = 1;
    }
    if ((DAT_0a517e68 & 1) == 0) {
      DAT_0a517e60[0] = s_co_main_09684c78[0];
      DAT_0a517e60[1] = s_co_main_09684c78[1];
      DAT_0a517e60[2] = s_co_main_09684c78[2];
      DAT_0a517e60[3] = s_co_main_09684c78[3];
      DAT_0a517e60[4] = s_co_main_09684c78[4];
      DAT_0a517e60[5] = s_co_main_09684c78[5];
      DAT_0a517e60[6] = s_co_main_09684c78[6];
      DAT_0a517e60[7] = s_co_main_09684c78[7];
      DAT_0a517e68 = 1;
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
    FUN_0668db5c(&local_148,&DAT_0a517ad8,DAT_0a517e60,&DAT_0a517ae0,0x22400002800);
    if ((DAT_0a517e90 & 1) == 0) {
      _DAT_0a517e6c = CONCAT44((int)DAT_087ec760,(int)DAT_089069d8);
      uRam000000000a517e74 = CONCAT44((int)DAT_084d8320,(int)DAT_084f7f28);
      _DAT_0a517e7c = CONCAT44((int)DAT_084de688,(int)DAT_09684c80);
      uRam000000000a517e84 = CONCAT44((int)DAT_08b69bc8,(int)DAT_0877c0b0);
      DAT_0a517e8c = (undefined4)DAT_09684c88;
      DAT_0a517e90 = 1;
    }
    plVar6 = (long *)(local_148 + 0x68);
    if (*(char *)(local_148 + 0x7f) < '\0') {
      plVar6 = (long *)*plVar6;
    }
    local_78 = *(undefined8 *)(param_1 + 0x3a0);
    local_70 = &DAT_aaaaaaaa0000000b;
    lStack_68 = *(long *)(param_1 + 0x3a8);
    if (-1 < *(char *)(param_1 + 0x3bf)) {
      lStack_68 = param_1 + 0x3a8;
    }
    local_50 = 0xaaaaaaaa00000006;
    local_60 = 0xaaaaaaaa00000010;
    puStack_58 = &DAT_aaaaaaaa00000000;
    FUN_0668e1e4(local_148 + 0x38,&DAT_0a517e6c,plVar6,&local_78,2);
    FUN_0668dbac();
    thunk_FUN_0668e878(&local_148);
  }
  if (((DAT_0a517ac0 & 1) == 0) && (iVar4 = ___cxa_guard_acquire(&DAT_0a517ac0), iVar4 != 0)) {
    FUN_06676a4c(&DAT_0a5179d0);
    ___cxa_guard_release(&DAT_0a517ac0);
  }
  lVar1 = param_1 + 0x3a8;
  FUN_06676d7c(&DAT_0a5179d0,*(undefined8 *)(param_1 + 0x3a0),lVar1,0,1);
  (**(code **)(param_1 + 0x250))(*(undefined8 *)(param_1 + 0x260));
  plVar6 = (long *)(*(code *)PTR___tlv_bootstrap_0a24de80)();
  plVar6 = (long *)*plVar6;
  if (plVar6 != (long *)0x0) {
    if (plVar6[1] != 0) {
      lVar7 = *plVar6;
      plVar6 = (long *)__ZNSt3__119__shared_weak_count4lockEv();
      if (plVar6 != (long *)0x0) {
        plVar2 = plVar6 + 1;
        *plVar2 = *plVar2 + 1;
        LOAcquire();
        lVar3 = *plVar2;
        *plVar2 = lVar3 + -1;
        LORelease();
        local_148 = lVar7;
        local_140 = plVar6;
        if (lVar3 == 0) {
          (**(code **)(*plVar6 + 0x10))();
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
        }
        goto LAB_06678d40;
      }
    }
                    /* WARNING: Subroutine does not return */
    FUN_00283500();
  }
  local_148 = 0;
  local_140 = (long *)0x0;
LAB_06678d40:
  lVar7 = local_148;
  iVar4 = *(int *)(local_148 + 0x288);
  if (iVar4 != 3) {
    *(int *)(local_148 + 0x3c8) = *(int *)(local_148 + 0x3c8) + 1;
  }
  if (*(code **)(param_1 + 600) != (code *)0x0) {
    (**(code **)(param_1 + 600))(*(undefined8 *)(param_1 + 0x260));
    *(undefined8 *)(param_1 + 600) = 0;
    iVar4 = *(int *)(lVar7 + 0x288);
  }
  plVar6 = local_140;
  if (iVar4 != 3) {
    *(int *)(lVar7 + 0x3c8) = *(int *)(lVar7 + 0x3c8) + -1;
  }
  if (local_140 != (long *)0x0) {
    LOAcquire();
    lVar7 = local_140[1];
    local_140[1] = lVar7 + -1;
    LORelease();
    if (lVar7 == 0) {
      (**(code **)(*local_140 + 0x10))(local_140);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  *(undefined4 *)(param_1 + 0x288) = 3;
  uVar5 = FUN_0668dad0(1);
  if ((uVar5 & 1) != 0) {
    if ((DAT_0a517add & 1) == 0) {
      DAT_0a517ad8 = (undefined4)ram0x08782918;
      DAT_0a517adc = 0;
      DAT_0a517add = 1;
    }
    if ((DAT_0a517e68 & 1) == 0) {
      DAT_0a517e60[0] = s_co_main_09684c78[0];
      DAT_0a517e60[1] = s_co_main_09684c78[1];
      DAT_0a517e60[2] = s_co_main_09684c78[2];
      DAT_0a517e60[3] = s_co_main_09684c78[3];
      DAT_0a517e60[4] = s_co_main_09684c78[4];
      DAT_0a517e60[5] = s_co_main_09684c78[5];
      DAT_0a517e60[6] = s_co_main_09684c78[6];
      DAT_0a517e60[7] = s_co_main_09684c78[7];
      DAT_0a517e68 = 1;
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
    FUN_0668db5c(&local_148,&DAT_0a517ad8,DAT_0a517e60,&DAT_0a517ae0,0x23700002800);
    if ((DAT_0a517eb8 & 1) == 0) {
      _DAT_0a517e94 = CONCAT44((int)DAT_087ec760,(int)DAT_089069d8);
      uRam000000000a517e9c = CONCAT44((int)DAT_0852aa18,(int)DAT_084f5b10);
      _DAT_0a517ea4 = CONCAT44((int)DAT_084de688,(int)DAT_09684c80);
      uRam000000000a517eac = CONCAT44((int)DAT_08b69bc8,(int)DAT_0877c0b0);
      DAT_0a517eb4 = (undefined4)DAT_09684c88;
      DAT_0a517eb8 = 1;
    }
    plVar6 = (long *)(local_148 + 0x68);
    if (*(char *)(local_148 + 0x7f) < '\0') {
      plVar6 = (long *)*plVar6;
    }
    local_78 = *(undefined8 *)(param_1 + 0x3a0);
    local_70 = &DAT_aaaaaaaa0000000b;
    lStack_68 = *(long *)(param_1 + 0x3a8);
    if (-1 < *(char *)(param_1 + 0x3bf)) {
      lStack_68 = lVar1;
    }
    local_50 = 0xaaaaaaaa00000006;
    local_60 = 0xaaaaaaaa00000010;
    puStack_58 = &DAT_aaaaaaaa00000000;
    FUN_0668e1e4(local_148 + 0x38,&DAT_0a517e94,plVar6,&local_78,2);
    FUN_0668dbac();
    thunk_FUN_0668e878(&local_148);
  }
  if (((DAT_0a517ac0 & 1) == 0) && (iVar4 = ___cxa_guard_acquire(&DAT_0a517ac0), iVar4 != 0)) {
    FUN_06676a4c(&DAT_0a5179d0);
    ___cxa_guard_release(&DAT_0a517ac0);
  }
  FUN_06676d7c(&DAT_0a5179d0,*(undefined8 *)(param_1 + 0x3a0),lVar1,1,3);
  FUN_0001accc(0,*(undefined8 *)(param_1 + 0x110),*(undefined8 *)(param_1 + 0x118));
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


