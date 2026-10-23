// Ghidra inferred pseudocode; requested=0x6674d5c
// entry=06674d5c end=066756bb

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_06674d5c(long *param_1)

{
  long *plVar1;
  uint3 uVar2;
  long lVar3;
  long *plVar4;
  long *plVar5;
  int iVar6;
  long *plVar7;
  long *plVar8;
  undefined8 *puVar9;
  long *plVar10;
  long *plVar11;
  ulong uVar12;
  long lVar13;
  undefined4 uVar14;
  undefined4 uVar15;
  long *local_170;
  long *plStack_168;
  long local_160;
  long *local_158;
  long *local_150;
  undefined1 auStack_138 [48];
  undefined8 ***local_108 [2];
  char local_f1;
  long local_a0;
  long *local_98;
  long local_90;
  long *plStack_88;
  long *local_80;
  long *plStack_78;
  long *local_70;
  long *local_68;
  undefined1 *puStack_60;
  undefined8 local_58;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  plVar7 = (long *)(*(code *)PTR___tlv_bootstrap_0a24de80)();
  plVar7 = (long *)*plVar7;
  if (plVar7 == (long *)0x0) {
    local_a0 = 0;
    local_98 = (long *)0x0;
    goto LAB_06674de0;
  }
  if (plVar7[1] == 0) {
LAB_066756b4:
                    /* WARNING: Subroutine does not return */
    FUN_00283500();
  }
  lVar13 = *plVar7;
  plVar7 = (long *)__ZNSt3__119__shared_weak_count4lockEv();
  if (plVar7 == (long *)0x0) goto LAB_066756b4;
  plVar1 = plVar7 + 1;
  *plVar1 = *plVar1 + 1;
  LOAcquire();
  lVar3 = *plVar1;
  *plVar1 = lVar3 + -1;
  LORelease();
  local_a0 = lVar13;
  local_98 = plVar7;
  if (lVar3 == 0) {
    (**(code **)(*plVar7 + 0x10))();
    __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
    if (local_a0 == 0) goto LAB_06674de0;
LAB_06675034:
    if (((*(byte *)(local_a0 + 0x3f0) & 1) == 0) && (*(int *)(local_a0 + 0x3c8) < 1)) {
      plVar7 = (long *)0xffffffffffffffff;
      goto LAB_06675060;
    }
    iVar6 = FUN_06668c3c(*param_1);
    if (iVar6 == 0) {
      LOAcquire();
      plVar4 = *(long **)(local_a0 + 1000);
      *(undefined1 **)(local_a0 + 1000) = (undefined1 *)((long)plVar4 + 1);
      LORelease();
      plVar8 = (long *)__Znwm(0x20);
      plVar7 = plVar8 + 1;
      *plVar7 = 0;
      plVar8[2] = 0;
      *plVar8 = (long)&PTR_FUN_09c20b80;
      plVar11 = plVar8 + 3;
      *(undefined4 *)plVar11 = 0;
      lVar13 = *param_1;
      plVar1 = (long *)param_1[1];
      if (plVar1 != (long *)0x0) {
        plVar5 = plVar1 + 1;
        *plVar5 = *plVar5 + 1;
        *plVar5 = *plVar5 + 1;
      }
      if (plVar8 != (long *)0x0) {
        *plVar7 = *plVar7 + 1;
      }
      local_160 = local_a0;
      local_158 = local_98;
      if (local_98 != (long *)0x0) {
        local_98[1] = local_98[1] + 1;
      }
      plVar5 = plVar7;
      if (plVar8 != (long *)0x0) {
        plVar5 = (long *)*plVar7;
        *plVar7 = (long)plVar5 + 1;
      }
      local_70 = (long *)local_a0;
      local_68 = local_98;
      if (local_98 != (long *)0x0) {
        plVar5 = (long *)local_98[1];
        local_98[1] = (long)plVar5 + 1;
      }
      local_170 = plVar11;
      plStack_168 = plVar8;
      local_150 = plVar4;
      local_80 = plVar11;
      plStack_78 = plVar8;
      __ZNSt3__115recursive_mutex4lockEv(plVar5,lVar13 + 0x10);
      plVar5 = (long *)__Znwm(0x30);
      thunk_FUN_066684f8(plVar5,0);
      local_90 = *plVar5;
      plVar7 = (long *)plVar5[1];
      lVar3 = local_90;
      if (plVar7 != (long *)0x0) {
        lVar3 = plVar7[1];
        plVar7[1] = lVar3 + 1;
      }
      *(undefined1 *)(plVar5 + 3) = 0;
      plStack_88 = plVar7;
      puVar9 = (undefined8 *)__Znwm(lVar3,0x30);
      puVar9[2] = plStack_168;
      puVar9[1] = local_170;
      *puVar9 = &PTR_FUN_09fb2970;
      local_170 = (long *)0x0;
      plStack_168 = (long *)0x0;
      puVar9[4] = local_158;
      puVar9[3] = local_160;
      local_160 = 0;
      local_158 = (long *)0x0;
      puVar9[5] = local_150;
      plVar5[4] = (long)puVar9;
      *(undefined1 *)((long)plVar5 + 0x19) = 0;
      puVar9 = (undefined8 *)__Znwm(0x28);
      *puVar9 = &PTR_FUN_09fb2a38;
      puVar9[2] = plStack_78;
      puVar9[1] = local_80;
      local_80 = (long *)0x0;
      plStack_78 = (long *)0x0;
      puVar9[4] = local_68;
      puVar9[3] = local_70;
      local_70 = (long *)0x0;
      local_68 = (long *)0x0;
      plVar5[5] = (long)puVar9;
      plVar10 = (long *)__Znwm(0x18);
      plVar10[2] = (long)plVar5;
      plVar5 = (long *)(lVar13 + 200);
      lVar3 = *plVar5;
      *plVar10 = lVar3;
      plVar10[1] = (long)plVar5;
      *(long **)(lVar3 + 8) = plVar10;
      *plVar5 = (long)plVar10;
      *(long *)(lVar13 + 0xd8) = *(long *)(lVar13 + 0xd8) + 1;
      FUN_0666991c(lVar13);
      __ZNSt3__115recursive_mutex6unlockEv(lVar13 + 0x10);
      if (plVar7 != (long *)0x0) {
        plVar5 = plVar7 + 1;
        *plVar5 = *plVar5 + 1;
        LOAcquire();
        lVar3 = *plVar5;
        *plVar5 = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*plVar7 + 0x10))(plVar7);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
        }
        LOAcquire();
        lVar3 = *plVar5;
        *plVar5 = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*plVar7 + 0x10))(plVar7);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
        }
      }
      plVar7 = local_68;
      if (local_68 != (long *)0x0) {
        LOAcquire();
        lVar3 = local_68[1];
        local_68[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*local_68 + 0x10))(local_68);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
        }
      }
      plVar7 = plStack_78;
      if (plStack_78 != (long *)0x0) {
        LOAcquire();
        lVar3 = plStack_78[1];
        plStack_78[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*plStack_78 + 0x10))(plStack_78);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
        }
      }
      plVar7 = local_158;
      if (local_158 != (long *)0x0) {
        LOAcquire();
        lVar3 = local_158[1];
        local_158[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*local_158 + 0x10))(local_158);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
        }
      }
      plVar7 = plStack_168;
      if (plStack_168 != (long *)0x0) {
        LOAcquire();
        lVar3 = plStack_168[1];
        plStack_168[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*plStack_168 + 0x10))(plStack_168);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
        }
      }
      if (plVar1 != (long *)0x0) {
        LOAcquire();
        lVar3 = plVar1[1];
        plVar1[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*plVar1 + 0x10))(plVar1);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
        }
      }
      plVar7 = (long *)FUN_06672da4();
      if (((long)plVar7 < 0) || (plVar7 == plVar4)) {
        if ((long)plVar7 < 0) {
          *(undefined4 *)plVar11 = 1;
          FUN_06668f30(lVar13);
        }
      }
      else {
        if ((DAT_0a517add & 1) == 0) {
          DAT_0a517ad8 = (undefined4)ram0x08782918;
          DAT_0a517adc = 0;
          DAT_0a517add = 1;
        }
        if ((DAT_0a517aff & 1) == 0) {
          DAT_0a517af0._0_1_ = s_await_nocls_allocls__09684bf8[0];
          DAT_0a517af0._1_1_ = s_await_nocls_allocls__09684bf8[1];
          DAT_0a517af0._2_1_ = s_await_nocls_allocls__09684bf8[2];
          DAT_0a517af0._3_1_ = s_await_nocls_allocls__09684bf8[3];
          DAT_0a517af0._4_1_ = s_await_nocls_allocls__09684bf8[4];
          DAT_0a517af0._5_1_ = s_await_nocls_allocls__09684bf8[5];
          DAT_0a517af0._6_1_ = s_await_nocls_allocls__09684bf8[6];
          DAT_0a517af0._7_1_ = s_await_nocls_allocls__09684bf8[7];
          DAT_0a517af8 = (undefined4)DAT_085322c0;
          DAT_0a517afc = 0x7470;
          DAT_0a517afe = 0;
          DAT_0a517aff = 1;
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
        FUN_0668db5c(&local_170,&DAT_0a517ad8,&DAT_0a517af0,&DAT_0a517ae0,0x32c0000b000);
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
        if (-1 < local_f1) {
          local_108[0] = local_108;
        }
        plStack_78 = (long *)0xaaaaaaaa00000006;
        local_80 = (long *)&DAT_aaaaaaaa00000000;
        FUN_0668e1e4(auStack_138,&DAT_0a517b00,local_108[0],&local_80,0);
        if ((DAT_0a517b7e & 1) == 0) {
          uVar12 = 0;
          do {
            uVar14 = *(undefined4 *)((long)&DAT_096850c4 + uVar12);
            uVar2 = CONCAT12((char)((uint)uVar14 >> 8),(short)uVar14) & 0xff00ff;
            uVar15 = *(undefined4 *)((long)&DAT_096850b0 + uVar12 % 0x14);
            *(uint *)((long)&DAT_0a517b3c + uVar12) =
                 CONCAT13((char)((uint)uVar14 >> 0x18) + 0x8aU ^ (byte)((uint)uVar15 >> 0x18),
                          CONCAT12((char)((uint)uVar14 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar15 >> 0x10),
                                   CONCAT11((char)(uVar2 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar15 >> 8),
                                            (char)uVar2 + 0x8aU ^ (byte)uVar15)));
            uVar12 = uVar12 + 4;
          } while (uVar12 != 0x40);
          DAT_0a517b7c = 0x29;
          DAT_0a517b7e = 1;
        }
        plVar11 = local_170 + 0xd;
        if (*(char *)((long)local_170 + 0x7f) < '\0') {
          plVar11 = (long *)*plVar11;
        }
        plStack_78 = (long *)0xaaaaaaaa0000000a;
        local_58 = 0xaaaaaaaa00000006;
        local_68 = (long *)0xaaaaaaaa0000000a;
        puStack_60 = &DAT_aaaaaaaa00000000;
        local_80 = plVar4;
        local_70 = plVar7;
        FUN_0668e1e4(local_170 + 7,&DAT_0a517b3c,plVar11,&local_80,2);
        FUN_0668dbac();
        thunk_FUN_0668e878(&local_170);
        plVar7 = (long *)0x0;
      }
      if (plVar1 != (long *)0x0) {
        LOAcquire();
        lVar13 = plVar1[1];
        plVar1[1] = lVar13 + -1;
        LORelease();
        if (lVar13 == 0) {
          (**(code **)(*plVar1 + 0x10))(plVar1);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
        }
      }
      if (plVar8 != (long *)0x0) {
        LOAcquire();
        lVar13 = plVar8[1];
        plVar8[1] = lVar13 + -1;
        LORelease();
        if (lVar13 == 0) {
          (**(code **)(*plVar8 + 0x10))(plVar8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
        }
      }
      goto LAB_06675060;
    }
  }
  else {
    if (lVar13 != 0) goto LAB_06675034;
LAB_06674de0:
    if ((DAT_0a517add & 1) == 0) {
      DAT_0a517ad8 = (undefined4)ram0x08782918;
      DAT_0a517adc = 0;
      DAT_0a517add = 1;
    }
    if ((DAT_0a517aff & 1) == 0) {
      DAT_0a517af0._0_1_ = s_await_nocls_allocls__09684bf8[0];
      DAT_0a517af0._1_1_ = s_await_nocls_allocls__09684bf8[1];
      DAT_0a517af0._2_1_ = s_await_nocls_allocls__09684bf8[2];
      DAT_0a517af0._3_1_ = s_await_nocls_allocls__09684bf8[3];
      DAT_0a517af0._4_1_ = s_await_nocls_allocls__09684bf8[4];
      DAT_0a517af0._5_1_ = s_await_nocls_allocls__09684bf8[5];
      DAT_0a517af0._6_1_ = s_await_nocls_allocls__09684bf8[6];
      DAT_0a517af0._7_1_ = s_await_nocls_allocls__09684bf8[7];
      DAT_0a517af8 = (undefined4)DAT_085322c0;
      DAT_0a517afc = 0x7470;
      DAT_0a517afe = 0;
      DAT_0a517aff = 1;
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
    FUN_0668db5c(&local_170,&DAT_0a517ad8,&DAT_0a517af0,&DAT_0a517ae0,0x3150000b000);
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
    if (-1 < local_f1) {
      local_108[0] = local_108;
    }
    plStack_78 = (long *)0xaaaaaaaa00000006;
    local_80 = (long *)&DAT_aaaaaaaa00000000;
    FUN_0668e1e4(auStack_138,&DAT_0a517b00,local_108[0],&local_80,0);
    if ((DAT_0a517b3b & 1) == 0) {
      _DAT_0a517b10 = CONCAT44((int)DAT_08532068,(int)DAT_087faf40);
      uRam000000000a517b18 = CONCAT44((int)ram0x084cd9a0,(int)DAT_08532070);
      _DAT_0a517b20 = CONCAT44((int)DAT_084d7818,(int)DAT_08486af0);
      uRam000000000a517b28 = CONCAT44((int)DAT_087954f8,(int)DAT_087faf48);
      DAT_0a517b30 = CONCAT44((int)DAT_084a2f50,(int)DAT_087faf50);
      DAT_0a517b38 = 0x7478;
      DAT_0a517b3a = 0;
      DAT_0a517b3b = 1;
    }
    plVar7 = local_170 + 0xd;
    if (*(char *)((long)local_170 + 0x7f) < '\0') {
      plVar7 = (long *)*plVar7;
    }
    plStack_78 = (long *)0xaaaaaaaa00000006;
    local_80 = (long *)&DAT_aaaaaaaa00000000;
    FUN_0668e1e4(local_170 + 7,&DAT_0a517b10,plVar7,&local_80,0);
    FUN_0668dbac();
    thunk_FUN_0668e878(&local_170);
  }
  plVar7 = (long *)0x0;
LAB_06675060:
  plVar1 = local_98;
  if (local_98 != (long *)0x0) {
    LOAcquire();
    lVar13 = local_98[1];
    local_98[1] = lVar13 + -1;
    LORelease();
    if (lVar13 == 0) {
      (**(code **)(*local_98 + 0x10))(local_98);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail(plVar7);
  }
  return;
}


