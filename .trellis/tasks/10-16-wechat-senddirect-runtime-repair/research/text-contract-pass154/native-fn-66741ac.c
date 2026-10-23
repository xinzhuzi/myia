// Ghidra inferred pseudocode; requested=0x66741ac
// entry=066741ac end=06674c3f

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_066741ac(long param_1)

{
  uint3 uVar1;
  int iVar2;
  long *plVar3;
  undefined1 *puVar4;
  long *plVar5;
  long lVar6;
  long *plVar7;
  ulong uVar8;
  undefined4 uVar9;
  undefined4 uVar10;
  undefined1 auVar11 [16];
  long *local_130 [7];
  undefined1 auStack_f8 [48];
  undefined8 **local_c8 [2];
  char local_b1;
  undefined8 local_60;
  undefined8 uStack_58;
  undefined1 *local_50;
  undefined8 local_48;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  auVar11 = (*(code *)PTR___tlv_bootstrap_0a24de80)();
  puVar4 = auVar11._8_8_;
  uVar9 = (undefined4)ram0x08782918;
  uVar10 = (undefined4)DAT_085722b0;
  if (*auVar11._0_8_ == param_1) {
    if ((DAT_0a517add & 1) == 0) {
      DAT_0a517adc = 0;
      DAT_0a517add = 1;
      DAT_0a517ad8 = uVar9;
    }
    if ((DAT_0a517fd3 & 1) == 0) {
      DAT_0a517fc8._0_1_ = s_cancel_nnon__09684bd0[0];
      DAT_0a517fc8._1_1_ = s_cancel_nnon__09684bd0[1];
      DAT_0a517fc8._2_1_ = s_cancel_nnon__09684bd0[2];
      DAT_0a517fc8._3_1_ = s_cancel_nnon__09684bd0[3];
      DAT_0a517fc8._4_1_ = s_cancel_nnon__09684bd0[4];
      DAT_0a517fc8._5_1_ = s_cancel_nnon__09684bd0[5];
      DAT_0a517fc8._6_1_ = s_cancel_nnon__09684bd0[6];
      DAT_0a517fc8._7_1_ = s_cancel_nnon__09684bd0[7];
      DAT_0a517fd0 = 0x776f;
      DAT_0a517fd2 = 0;
      DAT_0a517fd3 = 1;
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
      DAT_0a517aec = 1;
      DAT_0a517ae8 = uVar10;
    }
    FUN_0668db5c(local_130,&DAT_0a517ad8,&DAT_0a517fc8,&DAT_0a517ae0,0x1650000b000);
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
    if (-1 < local_b1) {
      local_c8[0] = local_c8;
    }
    uStack_58 = 0xaaaaaaaa00000006;
    local_60 = &DAT_aaaaaaaa00000000;
    FUN_0668e1e4(auStack_f8,&DAT_0a517b00,local_c8[0],&local_60,0);
    if ((DAT_0a518019 & 1) == 0) {
      uVar8 = 0;
      do {
        uVar10 = *(undefined4 *)((long)&DAT_096857a0 + uVar8);
        uVar1 = CONCAT12((char)((uint)uVar10 >> 8),(short)uVar10) & 0xff00ff;
        uVar9 = *(undefined4 *)((long)&DAT_0968578c + uVar8 % 0x14);
        *(uint *)((long)&DAT_0a517fd4 + uVar8) =
             CONCAT13((char)((uint)uVar10 >> 0x18) + 0x8aU ^ (byte)((uint)uVar9 >> 0x18),
                      CONCAT12((char)((uint)uVar10 >> 0x10) + 0x8aU ^ (byte)((uint)uVar9 >> 0x10),
                               CONCAT11((char)(uVar1 >> 0x10) + 0x8aU ^ (byte)((uint)uVar9 >> 8),
                                        (char)uVar1 + 0x8aU ^ (byte)uVar9)));
        uVar8 = uVar8 + 4;
      } while (uVar8 != 0x44);
      DAT_0a518018 = 0;
      DAT_0a518019 = 1;
    }
    plVar5 = local_130[0] + 0xd;
    if (*(char *)((long)local_130[0] + 0x7f) < '\0') {
      plVar5 = (long *)*plVar5;
    }
    uStack_58 = 0xaaaaaaaa00000006;
    local_60 = &DAT_aaaaaaaa00000000;
    FUN_0668e1e4(local_130[0] + 7,&DAT_0a517fd4,plVar5,&local_60,0);
    goto LAB_06674680;
  }
  if (*(int *)(param_1 + 0x288) != 3) {
    if (*(int *)(param_1 + 0x288) == 0) {
      *(undefined4 *)(param_1 + 0x288) = 3;
    }
    else {
      if ((long)puVar4 < 0) {
        if (-1 < *(int *)(param_1 + 0x3c8)) {
          *(undefined1 *)(param_1 + 0x3f0) = 0;
          if (*(int *)(param_1 + 0x3c8) == 0) {
            plVar5 = (long *)__Znwm(0x20);
            plVar5[1] = (long)puVar4;
            *plVar5 = (long)&PTR_FUN_09df9538;
            plVar5[2] = (long)PTR___ZTIx_09b36ac8;
            plVar5[3] = (long)(plVar5 + 1);
            plVar7 = *(long **)(param_1 + 0x398);
            if (plVar7 != (long *)0x0) {
              plVar3 = (long *)*plVar7;
              *plVar7 = (long)plVar5;
              if (plVar3 != (long *)0x0) {
                (**(code **)(*plVar3 + 8))();
              }
              plVar5 = (long *)0x0;
              *(undefined8 *)(param_1 + 0x398) = 0;
            }
            *(undefined8 *)(param_1 + 0x390) = 0;
            FUN_06677e1c(param_1);
            if (plVar5 != (long *)0x0) {
              if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
                    /* WARNING: Could not recover jumptable at 0x06674c38. Too many branches */
                    /* WARNING: Treating indirect jump as call */
                (**(code **)(*plVar5 + 8))(plVar5);
                return;
              }
              goto LAB_06674c3c;
            }
          }
          else {
            iVar2 = FUN_0668dad0(1);
            if (iVar2 != 0) {
              if ((DAT_0a517add & 1) == 0) {
                DAT_0a517ad8 = (undefined4)ram0x08782918;
                DAT_0a517adc = 0;
                DAT_0a517add = 1;
              }
              if ((DAT_0a517fd3 & 1) == 0) {
                DAT_0a517fc8._0_1_ = s_cancel_nnon__09684bd0[0];
                DAT_0a517fc8._1_1_ = s_cancel_nnon__09684bd0[1];
                DAT_0a517fc8._2_1_ = s_cancel_nnon__09684bd0[2];
                DAT_0a517fc8._3_1_ = s_cancel_nnon__09684bd0[3];
                DAT_0a517fc8._4_1_ = s_cancel_nnon__09684bd0[4];
                DAT_0a517fc8._5_1_ = s_cancel_nnon__09684bd0[5];
                DAT_0a517fc8._6_1_ = s_cancel_nnon__09684bd0[6];
                DAT_0a517fc8._7_1_ = s_cancel_nnon__09684bd0[7];
                DAT_0a517fd0 = 0x776f;
                DAT_0a517fd2 = 0;
                DAT_0a517fd3 = 1;
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
              FUN_0668db5c(local_130,&DAT_0a517ad8,&DAT_0a517fc8,&DAT_0a517ae0,0x17900002800);
              if ((DAT_0a5180a1 & 1) == 0) {
                _DAT_0a51808c = CONCAT44((int)DAT_084de6a0,(int)DAT_087faf40);
                uRam000000000a518094 = CONCAT44((int)DAT_0849e748,(int)DAT_084de6a8);
                DAT_0a51809c = (undefined4)DAT_08593f18;
                DAT_0a5180a0 = 0;
                DAT_0a5180a1 = 1;
              }
              plVar5 = local_130[0] + 0xd;
              if (*(char *)((long)local_130[0] + 0x7f) < '\0') {
                plVar5 = (long *)*plVar5;
              }
              uStack_58 = 0xaaaaaaaa00000006;
              local_60 = &DAT_aaaaaaaa00000000;
              FUN_0668e1e4(local_130[0] + 7,&DAT_0a51808c,plVar5,&local_60,0);
              lVar6 = *local_130[0];
              if ((DAT_0a518088 & 1) == 0) {
                _DAT_0a51806c = CONCAT44((int)DAT_0849e748,(int)ram0x09684bd8);
                uRam000000000a518074 = CONCAT44((int)DAT_084a4f10,(int)DAT_09684be0);
                DAT_0a51807c = CONCAT44((int)DAT_09684be8,(int)DAT_08492268);
                DAT_0a518084 = (undefined4)ram0x084c9468;
                DAT_0a518088 = 1;
              }
              plVar5 = (long *)(lVar6 + 0x68);
              if (*(char *)(lVar6 + 0x7f) < '\0') {
                plVar5 = (long *)*plVar5;
              }
              uStack_58 = 0xaaaaaaaa00000006;
              local_60 = (undefined1 *)CONCAT44(0xaaaaaaaa,*(undefined4 *)(param_1 + 0x3c8));
              local_48 = 0xaaaaaaaa00000006;
              local_50 = &DAT_aaaaaaaa00000000;
              FUN_0668e1e4(lVar6 + 0x38,&DAT_0a51806c,plVar5,&local_60,1);
              goto LAB_06674680;
            }
          }
          goto LAB_0667468c;
        }
        if ((DAT_0a517add & 1) == 0) {
          DAT_0a517adc = 0;
          DAT_0a517add = 1;
          DAT_0a517ad8 = uVar9;
        }
        if ((DAT_0a517fd3 & 1) == 0) {
          DAT_0a517fc8._0_1_ = s_cancel_nnon__09684bd0[0];
          DAT_0a517fc8._1_1_ = s_cancel_nnon__09684bd0[1];
          DAT_0a517fc8._2_1_ = s_cancel_nnon__09684bd0[2];
          DAT_0a517fc8._3_1_ = s_cancel_nnon__09684bd0[3];
          DAT_0a517fc8._4_1_ = s_cancel_nnon__09684bd0[4];
          DAT_0a517fc8._5_1_ = s_cancel_nnon__09684bd0[5];
          DAT_0a517fc8._6_1_ = s_cancel_nnon__09684bd0[6];
          DAT_0a517fc8._7_1_ = s_cancel_nnon__09684bd0[7];
          DAT_0a517fd0 = 0x776f;
          DAT_0a517fd2 = 0;
          DAT_0a517fd3 = 1;
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
          DAT_0a517aec = 1;
          DAT_0a517ae8 = uVar10;
        }
        FUN_0668db5c(local_130,&DAT_0a517ad8,&DAT_0a517fc8,&DAT_0a517ae0,0x1730000b000);
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
        if (-1 < local_b1) {
          local_c8[0] = local_c8;
        }
        uStack_58 = 0xaaaaaaaa00000006;
        local_60 = &DAT_aaaaaaaa00000000;
        FUN_0668e1e4(auStack_f8,&DAT_0a517b00,local_c8[0],&local_60,0);
        if ((DAT_0a51806b & 1) == 0) {
          _DAT_0a518050 = CONCAT44((int)DAT_084d77a0,(int)DAT_087faf40);
          uRam000000000a518058 = CONCAT44((int)DAT_084cade0,(int)DAT_084d77a8);
          DAT_0a518060 = CONCAT44((int)ram0x084897a0,(int)DAT_084cae70);
          DAT_0a518068 = 0x2065;
          DAT_0a51806a = 0;
          DAT_0a51806b = 1;
        }
        plVar5 = local_130[0] + 0xd;
        if (*(char *)((long)local_130[0] + 0x7f) < '\0') {
          plVar5 = (long *)*plVar5;
        }
        uStack_58 = 0xaaaaaaaa00000006;
        local_60 = &DAT_aaaaaaaa00000000;
        FUN_0668e1e4(local_130[0] + 7,&DAT_0a518050,plVar5,&local_60,0);
        lVar6 = *local_130[0];
        if ((DAT_0a518088 & 1) == 0) {
          _DAT_0a51806c = CONCAT44((int)DAT_0849e748,(int)ram0x09684bd8);
          uRam000000000a518074 = CONCAT44((int)DAT_084a4f10,(int)DAT_09684be0);
          DAT_0a51807c = CONCAT44((int)DAT_09684be8,(int)DAT_08492268);
          DAT_0a518084 = (undefined4)ram0x084c9468;
          DAT_0a518088 = 1;
        }
        plVar5 = (long *)(lVar6 + 0x68);
        if (*(char *)(lVar6 + 0x7f) < '\0') {
          plVar5 = (long *)*plVar5;
        }
        uStack_58 = 0xaaaaaaaa00000006;
        local_60 = (undefined1 *)CONCAT44(0xaaaaaaaa,*(undefined4 *)(param_1 + 0x3c8));
        local_48 = 0xaaaaaaaa00000006;
        local_50 = &DAT_aaaaaaaa00000000;
        FUN_0668e1e4(lVar6 + 0x38,&DAT_0a51806c,plVar5,&local_60,1);
      }
      else {
        if ((DAT_0a517add & 1) == 0) {
          DAT_0a517adc = 0;
          DAT_0a517add = 1;
          DAT_0a517ad8 = uVar9;
        }
        if ((DAT_0a517fd3 & 1) == 0) {
          DAT_0a517fc8._0_1_ = s_cancel_nnon__09684bd0[0];
          DAT_0a517fc8._1_1_ = s_cancel_nnon__09684bd0[1];
          DAT_0a517fc8._2_1_ = s_cancel_nnon__09684bd0[2];
          DAT_0a517fc8._3_1_ = s_cancel_nnon__09684bd0[3];
          DAT_0a517fc8._4_1_ = s_cancel_nnon__09684bd0[4];
          DAT_0a517fc8._5_1_ = s_cancel_nnon__09684bd0[5];
          DAT_0a517fc8._6_1_ = s_cancel_nnon__09684bd0[6];
          DAT_0a517fc8._7_1_ = s_cancel_nnon__09684bd0[7];
          DAT_0a517fd0 = 0x776f;
          DAT_0a517fd2 = 0;
          DAT_0a517fd3 = 1;
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
          DAT_0a517aec = 1;
          DAT_0a517ae8 = uVar10;
        }
        FUN_0668db5c(local_130,&DAT_0a517ad8,&DAT_0a517fc8,&DAT_0a517ae0,0x16f0000b000);
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
        if (-1 < local_b1) {
          local_c8[0] = local_c8;
        }
        uStack_58 = 0xaaaaaaaa00000006;
        local_60 = &DAT_aaaaaaaa00000000;
        FUN_0668e1e4(auStack_f8,&DAT_0a517b00,local_c8[0],&local_60,0);
        if ((DAT_0a51803a & 1) == 0) {
          _DAT_0a51801c = CONCAT44((int)DAT_084d77a0,(int)DAT_087faf40);
          uRam000000000a518024 = CONCAT44((int)DAT_084cade0,(int)DAT_084d77a8);
          DAT_0a51802c = CONCAT44((int)DAT_084df3f0,(int)DAT_084cae70);
          DAT_0a518034 = (undefined4)DAT_08483220;
          DAT_0a518038 = 0x20;
          DAT_0a51803a = 1;
        }
        plVar5 = local_130[0] + 0xd;
        if (*(char *)((long)local_130[0] + 0x7f) < '\0') {
          plVar5 = (long *)*plVar5;
        }
        uStack_58 = 0xaaaaaaaa00000006;
        local_60 = &DAT_aaaaaaaa00000000;
        FUN_0668e1e4(local_130[0] + 7,&DAT_0a51801c,plVar5,&local_60,0);
        lVar6 = *local_130[0];
        if ((DAT_0a51804c & 1) == 0) {
          DAT_0a518040._0_1_ = s_reason__name____owl_asynlooper_c_09683008[0];
          DAT_0a518040._1_1_ = s_reason__name____owl_asynlooper_c_09683008[1];
          DAT_0a518040._2_1_ = s_reason__name____owl_asynlooper_c_09683008[2];
          DAT_0a518040._3_1_ = s_reason__name____owl_asynlooper_c_09683008[3];
          DAT_0a518040._4_1_ = s_reason__name____owl_asynlooper_c_09683008[4];
          DAT_0a518040._5_1_ = s_reason__name____owl_asynlooper_c_09683008[5];
          DAT_0a518040._6_1_ = s_reason__name____owl_asynlooper_c_09683008[6];
          DAT_0a518040._7_1_ = s_reason__name____owl_asynlooper_c_09683008[7];
          DAT_0a518048 = (undefined4)ram0x084c9468;
          DAT_0a51804c = 1;
        }
        plVar5 = (long *)(lVar6 + 0x68);
        if (*(char *)(lVar6 + 0x7f) < '\0') {
          plVar5 = (long *)*plVar5;
        }
        uStack_58 = 0xaaaaaaaa0000000a;
        local_48 = 0xaaaaaaaa00000006;
        local_50 = &DAT_aaaaaaaa00000000;
        local_60 = puVar4;
        FUN_0668e1e4(lVar6 + 0x38,&DAT_0a518040,plVar5,&local_60,1);
      }
LAB_06674680:
      FUN_0668dbac();
      thunk_FUN_0668e878(local_130);
    }
  }
LAB_0667468c:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
LAB_06674c3c:
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


