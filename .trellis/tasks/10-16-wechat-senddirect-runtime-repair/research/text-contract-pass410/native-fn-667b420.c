// Ghidra inferred pseudocode; requested=0x667b420
// entry=0667b420 end=0667b8ab

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0667b420(long param_1,undefined8 *param_2)

{
  long *plVar1;
  undefined8 uVar2;
  long *plVar3;
  undefined4 uVar4;
  long lVar5;
  long *plVar6;
  undefined8 uVar7;
  undefined **ppuVar8;
  code *pcVar9;
  long lVar10;
  long *plVar11;
  undefined **local_140;
  long *plStack_138;
  undefined8 local_130;
  undefined ***local_128;
  undefined1 auStack_108 [48];
  undefined8 *******local_d8 [2];
  char local_c1;
  undefined8 local_70;
  undefined8 uStack_68;
  long *local_60;
  long *local_58;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  uVar2 = *param_2;
  plVar3 = (long *)param_2[1];
  if (plVar3 != (long *)0x0) {
    plVar3[1] = plVar3[1] + 1;
  }
  plVar6 = (long *)(*(code *)PTR___tlv_bootstrap_0a24de80)();
  plVar6 = (long *)*plVar6;
  plVar11 = (long *)section_00000248.addr;
  if (plVar6 != (long *)0x0) {
    if (plVar6[1] == 0) {
LAB_0667b8a0:
                    /* WARNING: Subroutine does not return */
      FUN_00283500();
    }
    lVar10 = *plVar6;
    plVar6 = (long *)__ZNSt3__119__shared_weak_count4lockEv();
    if (plVar6 == (long *)0x0) goto LAB_0667b8a0;
    plVar1 = plVar6 + 1;
    *plVar1 = *plVar1 + 1;
    LOAcquire();
    lVar5 = *plVar1;
    *plVar1 = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*plVar6 + 0x10))(plVar6);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
    plVar11 = *(long **)(lVar10 + 0x268);
    LOAcquire();
    lVar10 = *plVar1;
    *plVar1 = lVar10 + -1;
    LORelease();
    if (lVar10 == 0) {
      (**(code **)(*plVar6 + 0x10))(plVar6);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  if (plVar11 == (long *)0x0) {
    if ((DAT_0a517add & 1) == 0) {
      DAT_0a517ad8 = (undefined4)unique0x10000531;
      DAT_0a517adc = 0;
      DAT_0a517add = 1;
    }
    if ((DAT_0a517c53 & 1) == 0) {
      DAT_0a517c50 = 0x2928;
      DAT_0a517c52 = 0;
      DAT_0a517c53 = 1;
      DAT_0a517c48 = s_StartScaoperatorh_op_084cadf8._8_8_;
    }
    if ((DAT_0a517aec & 1) == 0) {
      DAT_0a517ae8 = (undefined4)DAT_085722b0;
      DAT_0a517aec = 1;
      DAT_0a517ae0 = s_co_core_resume_ie__i_09684bb0._0_8_;
    }
    FUN_0668db5c(&local_140,&DAT_0a517ad8,&DAT_0a517c48,&DAT_0a517ae0,0x2fe0000b000);
    if ((DAT_0a517b0e & 1) == 0) {
      DAT_0a517b00._0_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[0];
      DAT_0a517b00._1_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[1];
      DAT_0a517b00._2_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[2];
      DAT_0a517b00._3_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[3];
      DAT_0a517b00._4_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[4];
      DAT_0a517b00._5_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[5];
      DAT_0a517b00._6_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[6];
      DAT_0a517b00._7_1_ = s_Fatal_ersend_noereceive_noexcept_087d8ab0[7];
      DAT_0a517b08 = (undefined4)DAT_084d8788;
      DAT_0a517b0c = 0x20;
      DAT_0a517b0e = 1;
    }
    if (-1 < local_c1) {
      local_d8[0] = local_d8;
    }
    uStack_68 = 0xaaaaaaaa00000006;
    local_70 = (undefined **)&DAT_aaaaaaaa00000000;
    FUN_0668e1e4(auStack_108,&DAT_0a517b00,local_d8[0],&local_70,0);
    if ((DAT_0a518187 & 1) == 0) {
      _DAT_0a51815c = CONCAT44((int)ram0x08620fa0,(int)DAT_09684bf0);
      uRam000000000a518164 = CONCAT44((int)DAT_08a3e740,(int)DAT_09684cb8);
      _DAT_0a51816c = CONCAT44((int)DAT_09684cc8,(int)DAT_09684cc0);
      uRam000000000a518174 = CONCAT44((int)DAT_09684c10,(int)DAT_08771a60);
      DAT_0a51817c = CONCAT44((int)DAT_0854c0c0,(int)DAT_085f45d0);
      DAT_0a518184 = 0x7274;
      DAT_0a518186 = 0;
      DAT_0a518187 = 1;
    }
    ppuVar8 = local_140 + 0xd;
    if (*(char *)((long)local_140 + 0x7f) < '\0') {
      ppuVar8 = (undefined **)*ppuVar8;
    }
    uStack_68 = 0xaaaaaaaa00000007;
    local_70 = (undefined **)CONCAT44(0xaaaaaaaa,*(undefined4 *)(param_1 + 8));
    local_58 = (long *)0xaaaaaaaa00000006;
    local_60 = (long *)&DAT_aaaaaaaa00000000;
    FUN_0668e1e4(local_140 + 7,&DAT_0a51815c,ppuVar8,&local_70,1);
    FUN_0668dbac();
    thunk_FUN_0668e878(&local_140);
    goto joined_r0x0667b75c;
  }
  uVar4 = *(undefined4 *)(param_1 + 8);
  if (plVar3 == (long *)0x0) {
    local_60 = (long *)0x0;
  }
  else {
    plVar6 = plVar3 + 1;
    *plVar6 = *plVar6 + 1;
    *plVar6 = *plVar6 + 1;
    local_60 = plVar3;
  }
  local_70 = &PTR_FUN_09fb2860;
  uStack_68 = uVar2;
  local_58 = &local_70;
  uVar7 = (**(code **)(*plVar11 + 0x18))(plVar11,uVar4,&local_70);
  if (local_58 == &local_70) {
    pcVar9 = *(code **)(*local_58 + 0x20);
LAB_0667b7bc:
    (*pcVar9)();
  }
  else if (local_58 != (long *)0x0) {
    pcVar9 = *(code **)(*local_58 + 0x28);
    goto LAB_0667b7bc;
  }
  if (plVar3 != (long *)0x0) {
    LOAcquire();
    lVar10 = plVar3[1];
    plVar3[1] = lVar10 + -1;
    LORelease();
    if (lVar10 == 0) {
      (**(code **)(*plVar3 + 0x10))(plVar3);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  local_140 = &PTR_FUN_09fb28e0;
  plStack_138 = plVar11;
  local_130 = uVar7;
  local_128 = &local_140;
  FUN_06668c44(uVar2,&local_140);
  if (local_128 == &local_140) {
    (*(code *)(*local_128)[4])();
  }
  else if (local_128 != (undefined ***)0x0) {
    (*(code *)(*local_128)[5])();
  }
joined_r0x0667b75c:
  if (plVar3 != (long *)0x0) {
    LOAcquire();
    lVar10 = plVar3[1];
    plVar3[1] = lVar10 + -1;
    LORelease();
    if (lVar10 == 0) {
      (**(code **)(*plVar3 + 0x10))(plVar3);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


