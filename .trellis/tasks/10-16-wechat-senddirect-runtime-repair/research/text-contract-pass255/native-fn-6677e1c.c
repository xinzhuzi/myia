// Ghidra inferred pseudocode; requested=0x6677e1c
// entry=06677e1c end=06678a6f

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_06677e1c(long param_1)

{
  uint3 uVar1;
  undefined1 uVar2;
  int iVar3;
  undefined8 uVar4;
  long lVar5;
  pthread_t p_Var6;
  undefined8 *puVar7;
  long *plVar8;
  ulong uVar9;
  pthread_t p_Var10;
  undefined4 uVar11;
  undefined4 uVar12;
  long *local_178 [7];
  undefined1 auStack_140 [48];
  undefined8 ***local_110 [2];
  char local_f9;
  undefined1 *local_a8;
  undefined1 *local_a0;
  long lStack_98;
  undefined8 local_90;
  undefined1 *puStack_88;
  undefined1 *local_80;
  undefined8 uStack_78;
  undefined8 local_70;
  undefined1 *puStack_68;
  undefined8 local_60;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  iVar3 = FUN_0668dad0(0);
  if (iVar3 != 0) {
    if ((DAT_0a517add & 1) == 0) {
      DAT_0a517ad8 = (undefined4)ram0x08782918;
      DAT_0a517adc = 0;
      DAT_0a517add = 1;
    }
    if ((DAT_0a517d36 & 1) == 0) {
      DAT_0a517d28._0_1_ = s_do_resumoc_c_09684c58[0];
      DAT_0a517d28._1_1_ = s_do_resumoc_c_09684c58[1];
      DAT_0a517d28._2_1_ = s_do_resumoc_c_09684c58[2];
      DAT_0a517d28._3_1_ = s_do_resumoc_c_09684c58[3];
      DAT_0a517d28._4_1_ = s_do_resumoc_c_09684c58[4];
      DAT_0a517d28._5_1_ = s_do_resumoc_c_09684c58[5];
      DAT_0a517d28._6_1_ = s_do_resumoc_c_09684c58[6];
      DAT_0a517d28._7_1_ = s_do_resumoc_c_09684c58[7];
      DAT_0a517d30 = (undefined4)DAT_08805050;
      DAT_0a517d34 = 0x77;
      DAT_0a517d36 = 1;
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
    FUN_0668db5c(local_178,&DAT_0a517ad8,&DAT_0a517d28,&DAT_0a517ae0,0x18f00000800);
    local_a8 = (undefined1 *)CONCAT44(local_a8._4_4_,*(undefined4 *)(param_1 + 0x288));
    if ((DAT_0a517d74 & 1) == 0) {
      uVar9 = 0;
      do {
        uVar11 = *(undefined4 *)((long)&DAT_096853f9 + uVar9);
        uVar1 = CONCAT12((char)((uint)uVar11 >> 8),(short)uVar11) & 0xff00ff;
        uVar12 = *(undefined4 *)((long)&DAT_096853e5 + uVar9 % 0x14);
        *(uint *)((long)&DAT_0a517d37 + uVar9) =
             CONCAT13((char)((uint)uVar11 >> 0x18) + 0x8aU ^ (byte)((uint)uVar12 >> 0x18),
                      CONCAT12((char)((uint)uVar11 >> 0x10) + 0x8aU ^ (byte)((uint)uVar12 >> 0x10),
                               CONCAT11((char)(uVar1 >> 0x10) + 0x8aU ^ (byte)((uint)uVar12 >> 8),
                                        (char)uVar1 + 0x8aU ^ (byte)uVar12)));
        uVar9 = uVar9 + 4;
      } while (uVar9 != 0x3c);
      DAT_0a517d73 = 0;
      DAT_0a517d74 = 1;
    }
    plVar8 = local_178[0] + 0xd;
    if (*(char *)((long)local_178[0] + 0x7f) < '\0') {
      plVar8 = (long *)*plVar8;
    }
    FUN_06679c10(local_178[0] + 7,&DAT_0a517d37,plVar8,param_1 + 0x3a0,param_1 + 0x3a8,&local_a8,
                 param_1 + 0x3f0);
    FUN_0668dbac();
    thunk_FUN_0668e878(local_178);
  }
  if (*(int *)(param_1 + 0x288) == 2) {
    p_Var10 = *(pthread_t *)(param_1 + 0x3c0);
    p_Var6 = _pthread_self();
    if (p_Var6 != p_Var10) {
      if ((DAT_0a517add & 1) == 0) {
        DAT_0a517ad8 = (undefined4)ram0x08782918;
        DAT_0a517adc = 0;
        DAT_0a517add = 1;
      }
      if ((DAT_0a517d36 & 1) == 0) {
        DAT_0a517d28._0_1_ = s_do_resumoc_c_09684c58[0];
        DAT_0a517d28._1_1_ = s_do_resumoc_c_09684c58[1];
        DAT_0a517d28._2_1_ = s_do_resumoc_c_09684c58[2];
        DAT_0a517d28._3_1_ = s_do_resumoc_c_09684c58[3];
        DAT_0a517d28._4_1_ = s_do_resumoc_c_09684c58[4];
        DAT_0a517d28._5_1_ = s_do_resumoc_c_09684c58[5];
        DAT_0a517d28._6_1_ = s_do_resumoc_c_09684c58[6];
        DAT_0a517d28._7_1_ = s_do_resumoc_c_09684c58[7];
        DAT_0a517d30 = (undefined4)DAT_08805050;
        DAT_0a517d34 = 0x77;
        DAT_0a517d36 = 1;
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
      FUN_0668db5c(local_178,&DAT_0a517ad8,&DAT_0a517d28,&DAT_0a517ae0,0x1c20000b000);
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
      if (-1 < local_f9) {
        local_110[0] = local_110;
      }
      local_a0 = (undefined1 *)0xaaaaaaaa00000006;
      local_a8 = &DAT_aaaaaaaa00000000;
      FUN_0668e1e4(auStack_140,&DAT_0a517b00,local_110[0],&local_a8,0);
      if ((DAT_0a517e2e & 1) == 0) {
        _DAT_0a517df8 = CONCAT44((int)DAT_088cf4f8,(int)DAT_08502a60);
        uRam000000000a517e00 = CONCAT44((int)DAT_084874c0,(int)DAT_088fbaf0);
        _DAT_0a517e08 = CONCAT44((int)ram0x08937b60,(int)DAT_085b06f8);
        uRam000000000a517e10 = CONCAT44((int)DAT_084875b0,(int)DAT_084cf928);
        _DAT_0a517e18 = CONCAT44((int)DAT_085c24f8,(int)DAT_08482368);
        uRam000000000a517e20 = CONCAT44((int)DAT_088898b8,(int)DAT_084d7878);
        DAT_0a517e28 = (undefined4)DAT_08482348;
        DAT_0a517e2c = 100;
        DAT_0a517e2e = 1;
      }
      plVar8 = local_178[0] + 0xd;
      if (*(char *)((long)local_178[0] + 0x7f) < '\0') {
        plVar8 = (long *)*plVar8;
      }
      local_a0 = (undefined1 *)0xaaaaaaaa00000006;
      local_a8 = &DAT_aaaaaaaa00000000;
      FUN_0668e1e4(local_178[0] + 7,&DAT_0a517df8,plVar8,&local_a8,0);
      FUN_0668dbac();
      thunk_FUN_0668e878(local_178);
      goto LAB_06678a38;
    }
    iVar3 = (**(code **)(**(long **)(param_1 + 0x270) + 0x20))();
    if (iVar3 != 0) {
      FUN_066795fc(param_1);
    }
    *(undefined4 *)(param_1 + 0x288) = 1;
    local_178[0] = (long *)0x0;
    plVar8 = (long *)(*(code *)PTR___tlv_bootstrap_0a24de80)();
    lVar5 = *plVar8;
    puVar7 = (undefined8 *)(*(code *)PTR___tlv_bootstrap_0a24de98)();
    uVar4 = *puVar7;
    *plVar8 = param_1;
    *puVar7 = *(undefined8 *)(param_1 + 0x3a0);
    FUN_0001accc(local_178,*(undefined8 *)(param_1 + 0x230),*(undefined8 *)(param_1 + 0x238));
    _co_swapcontext(param_1 + 0x10,param_1 + 0x130);
    FUN_0001accc(local_178[0]);
    *plVar8 = lVar5;
    *puVar7 = uVar4;
LAB_066789dc:
    iVar3 = (**(code **)(**(long **)(param_1 + 0x270) + 0x20))();
    if ((iVar3 != 0) && (*(int *)(param_1 + 0x288) != 3)) {
      FUN_06679088(param_1);
    }
  }
  else {
    if (*(int *)(param_1 + 0x288) == 0) {
      plVar8 = *(long **)(param_1 + 0x270);
      if (plVar8 == (long *)0x0) {
        plVar8 = (long *)FUN_066734b4();
        *(long **)(param_1 + 0x270) = plVar8;
        if (*(long *)(param_1 + 0x280) != 0) goto LAB_066784f4;
LAB_06678508:
        uVar4 = (**(code **)(*plVar8 + 0x28))();
        *(undefined8 *)(param_1 + 0x280) = uVar4;
      }
      else {
        if (*(long *)(param_1 + 0x280) == 0) goto LAB_06678508;
LAB_066784f4:
        uVar9 = (**(code **)(*plVar8 + 0x20))();
        if ((uVar9 & 1) != 0) {
          plVar8 = *(long **)(param_1 + 0x270);
          goto LAB_06678508;
        }
        uVar4 = *(undefined8 *)(param_1 + 0x280);
      }
      lVar5 = (**(code **)(**(long **)(param_1 + 0x270) + 0x10))(*(long **)(param_1 + 0x270),uVar4);
      *(long *)(param_1 + 0x278) = lVar5;
      if (lVar5 + 1U < 2) {
        if ((DAT_0a517add & 1) == 0) {
          DAT_0a517ad8 = (undefined4)ram0x08782918;
          DAT_0a517adc = 0;
          DAT_0a517add = 1;
        }
        if ((DAT_0a517d36 & 1) == 0) {
          DAT_0a517d28._0_1_ = s_do_resumoc_c_09684c58[0];
          DAT_0a517d28._1_1_ = s_do_resumoc_c_09684c58[1];
          DAT_0a517d28._2_1_ = s_do_resumoc_c_09684c58[2];
          DAT_0a517d28._3_1_ = s_do_resumoc_c_09684c58[3];
          DAT_0a517d28._4_1_ = s_do_resumoc_c_09684c58[4];
          DAT_0a517d28._5_1_ = s_do_resumoc_c_09684c58[5];
          DAT_0a517d28._6_1_ = s_do_resumoc_c_09684c58[6];
          DAT_0a517d28._7_1_ = s_do_resumoc_c_09684c58[7];
          DAT_0a517d30 = (undefined4)DAT_08805050;
          DAT_0a517d34 = 0x77;
          DAT_0a517d36 = 1;
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
        FUN_0668db5c(local_178,&DAT_0a517ad8,&DAT_0a517d28,&DAT_0a517ae0,0x19c0000b000);
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
        if (-1 < local_f9) {
          local_110[0] = local_110;
        }
        local_a0 = (undefined1 *)0xaaaaaaaa00000006;
        local_a8 = &DAT_aaaaaaaa00000000;
        FUN_0668e1e4(auStack_140,&DAT_0a517b00,local_110[0],&local_a8,0);
        if ((DAT_0a517d9c & 1) == 0) {
          _DAT_0a517d78 = CONCAT44((int)DAT_0853f0a0,(int)DAT_087faf40);
          uRam000000000a517d80 = CONCAT44((int)DAT_088fbaf0,(int)ram0x09684c60);
          _DAT_0a517d88 = CONCAT44((int)DAT_0852e830,(int)DAT_084874c0);
          uRam000000000a517d90 = CONCAT44((int)DAT_084caf50,(int)DAT_08771650);
          DAT_0a517d98 = (undefined4)DAT_09684c68;
          DAT_0a517d9c = 1;
        }
        plVar8 = local_178[0] + 0xd;
        if (*(char *)((long)local_178[0] + 0x7f) < '\0') {
          plVar8 = (long *)*plVar8;
        }
        local_a0 = (undefined1 *)0xaaaaaaaa00000006;
        local_a8 = &DAT_aaaaaaaa00000000;
        FUN_0668e1e4(local_178[0] + 7,&DAT_0a517d78,plVar8,&local_a8,0);
        lVar5 = *local_178[0];
        uVar2 = (**(code **)(**(long **)(param_1 + 0x270) + 0x20))();
        uStack_78 = (**(code **)(**(long **)(param_1 + 0x270) + 0x28))();
        if ((DAT_0a517df5 & 1) == 0) {
          uVar9 = 0;
          do {
            uVar11 = *(undefined4 *)((long)&DAT_09685482 + uVar9);
            uVar1 = CONCAT12((char)((uint)uVar11 >> 8),(short)uVar11) & 0xff00ff;
            uVar12 = *(undefined4 *)((long)&DAT_0968546e + uVar9 % 0x14);
            *(uint *)((long)&DAT_0a517d9d + uVar9) =
                 CONCAT13((char)((uint)uVar11 >> 0x18) + 0x8aU ^ (byte)((uint)uVar12 >> 0x18),
                          CONCAT12((char)((uint)uVar11 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar12 >> 0x10),
                                   CONCAT11((char)(uVar1 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar12 >> 8),
                                            (char)uVar1 + 0x8aU ^ (byte)uVar12)));
            uVar9 = uVar9 + 4;
          } while (uVar9 != 0x58);
          DAT_0a517df5 = 1;
        }
        plVar8 = (long *)(lVar5 + 0x68);
        if (*(char *)(lVar5 + 0x7f) < '\0') {
          plVar8 = (long *)*plVar8;
        }
        local_a8 = *(undefined1 **)(param_1 + 0x278);
        local_a0 = &DAT_aaaaaaaa0000000f;
        lStack_98 = *(long *)(param_1 + 0x280);
        local_90 = 0xaaaaaaaa00000009;
        local_80 = &DAT_aaaaaaaa00000000;
        puStack_88 = (undefined1 *)CONCAT71(0xaaaaaaaaaaaaaa,uVar2);
        local_60 = 0xaaaaaaaa00000006;
        local_70 = 0xaaaaaaaa00000009;
        puStack_68 = &DAT_aaaaaaaa00000000;
        FUN_0668e1e4(lVar5 + 0x38,&DAT_0a517d9d,plVar8,&local_a8,4);
        FUN_0668dbac();
        thunk_FUN_0668e878(local_178);
      }
      uVar9 = (**(code **)(**(long **)(param_1 + 0x270) + 0x20))();
      if ((uVar9 & 1) == 0) {
        FUN_066874ec(*(undefined8 *)(param_1 + 0x278),*(undefined8 *)(param_1 + 0x280));
      }
      _co_getcontext(param_1 + 0x130);
      *(undefined8 *)(param_1 + 0x230) = *(undefined8 *)(param_1 + 0x278);
      *(undefined8 *)(param_1 + 0x238) = *(undefined8 *)(param_1 + 0x280);
      *(long *)(param_1 + 0x240) = param_1 + 0x10;
      p_Var6 = _pthread_self();
      *(pthread_t *)(param_1 + 0x3c0) = p_Var6;
      *(undefined4 *)(param_1 + 0x288) = 1;
      local_178[0] = (long *)0x0;
      plVar8 = (long *)(*(code *)PTR___tlv_bootstrap_0a24de80)();
      lVar5 = *plVar8;
      puVar7 = (undefined8 *)(*(code *)PTR___tlv_bootstrap_0a24de98)();
      uVar4 = *puVar7;
      *plVar8 = param_1;
      *puVar7 = *(undefined8 *)(param_1 + 0x3a0);
      _co_makecontext(param_1 + 0x130,FUN_06678aa0,param_1);
      FUN_0001accc(local_178,*(undefined8 *)(param_1 + 0x230),*(undefined8 *)(param_1 + 0x238));
      _co_swapcontext(param_1 + 0x10,param_1 + 0x130);
      FUN_0001accc(local_178[0]);
      *plVar8 = lVar5;
      *puVar7 = uVar4;
      goto LAB_066789dc;
    }
    if ((DAT_0a517add & 1) == 0) {
      DAT_0a517ad8 = (undefined4)ram0x08782918;
      DAT_0a517adc = 0;
      DAT_0a517add = 1;
    }
    if ((DAT_0a517d36 & 1) == 0) {
      DAT_0a517d28._0_1_ = s_do_resumoc_c_09684c58[0];
      DAT_0a517d28._1_1_ = s_do_resumoc_c_09684c58[1];
      DAT_0a517d28._2_1_ = s_do_resumoc_c_09684c58[2];
      DAT_0a517d28._3_1_ = s_do_resumoc_c_09684c58[3];
      DAT_0a517d28._4_1_ = s_do_resumoc_c_09684c58[4];
      DAT_0a517d28._5_1_ = s_do_resumoc_c_09684c58[5];
      DAT_0a517d28._6_1_ = s_do_resumoc_c_09684c58[6];
      DAT_0a517d28._7_1_ = s_do_resumoc_c_09684c58[7];
      DAT_0a517d30 = (undefined4)DAT_08805050;
      DAT_0a517d34 = 0x77;
      DAT_0a517d36 = 1;
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
    FUN_0668db5c(local_178,&DAT_0a517ad8,&DAT_0a517d28,&DAT_0a517ae0,0x1db0000b000);
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
    if (-1 < local_f9) {
      local_110[0] = local_110;
    }
    local_a0 = (undefined1 *)0xaaaaaaaa00000006;
    local_a8 = &DAT_aaaaaaaa00000000;
    FUN_0668e1e4(auStack_140,&DAT_0a517b00,local_110[0],&local_a8,0);
    if ((DAT_0a517e5f & 1) == 0) {
      _DAT_0a517e30 = CONCAT44((int)DAT_087ec760,(int)DAT_089069d8);
      uRam000000000a517e38 = CONCAT44((int)DAT_08543ae8,(int)DAT_084d1058);
      _DAT_0a517e40 = CONCAT44((int)DAT_08738c08,(int)DAT_08543af0);
      uRam000000000a517e48 = CONCAT44((int)DAT_09684c70,(int)DAT_08738c10);
      DAT_0a517e50 = CONCAT44((int)DAT_084c85d0,(int)DAT_084cf930);
      DAT_0a517e58 = (undefined4)DAT_08b6ec38;
      DAT_0a517e5c = 0x225f;
      DAT_0a517e5e = 0;
      DAT_0a517e5f = 1;
    }
    plVar8 = local_178[0] + 0xd;
    if (*(char *)((long)local_178[0] + 0x7f) < '\0') {
      plVar8 = (long *)*plVar8;
    }
    local_a8 = *(undefined1 **)(param_1 + 0x3a0);
    local_a0 = &DAT_aaaaaaaa0000000b;
    lStack_98 = *(long *)(param_1 + 0x3a8);
    if (-1 < *(char *)(param_1 + 0x3bf)) {
      lStack_98 = param_1 + 0x3a8;
    }
    local_80 = (undefined1 *)0xaaaaaaaa00000006;
    local_90 = 0xaaaaaaaa00000010;
    puStack_88 = &DAT_aaaaaaaa00000000;
    FUN_0668e1e4(local_178[0] + 7,&DAT_0a517e30,plVar8,&local_a8,2);
    FUN_0668dbac();
    thunk_FUN_0668e878(local_178);
  }
  if (*(int *)(param_1 + 0x288) == 3) {
    uVar9 = (**(code **)(**(long **)(param_1 + 0x270) + 0x20))();
    if ((uVar9 & 1) == 0) {
      FUN_06687bb8(*(undefined8 *)(param_1 + 0x278),*(undefined8 *)(param_1 + 0x280));
    }
    FUN_066798bc(param_1);
  }
LAB_06678a38:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_58) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


