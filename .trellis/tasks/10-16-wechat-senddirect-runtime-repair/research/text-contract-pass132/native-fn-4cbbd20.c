// Ghidra inferred pseudocode; requested=0x4cbbd20
// entry=04cbbd20 end=04cbc337

/* WARNING: Removing unreachable block (ram,0x04cbc320) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_04cbbd20(long param_1,ulong param_2)

{
  undefined8 ******ppppppuVar1;
  undefined1 uVar2;
  uint3 uVar3;
  long lVar4;
  int iVar5;
  undefined8 *puVar6;
  undefined1 *puVar7;
  uint uVar8;
  undefined1 *puVar9;
  long lVar10;
  undefined1 *puVar11;
  ulong uVar12;
  long *plVar13;
  undefined4 uVar14;
  undefined4 uVar15;
  undefined1 *local_270 [2];
  undefined7 local_260;
  char cStack_259;
  undefined8 *****local_258 [2];
  undefined7 local_248;
  char cStack_241;
  undefined1 auStack_240 [144];
  undefined1 *local_1b0;
  undefined1 local_1a8 [72];
  undefined1 *local_160;
  undefined1 local_158 [72];
  undefined1 *local_110;
  undefined1 local_108;
  undefined1 **local_c0;
  undefined1 **ppuStack_b8;
  undefined1 **local_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  undefined8 local_78;
  undefined8 uStack_70;
  undefined8 local_68;
  undefined8 uStack_60;
  undefined8 local_58;
  undefined8 uStack_50;
  undefined8 local_48;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  if (*(int *)(param_1 + 0xc) != (int)param_2) {
    FUN_04cbd624(param_1);
    iVar5 = FUN_04bb6cd4();
    if (iVar5 == 0) {
      if ((*(int *)(param_1 + 0xc) != 0) && (iVar5 = thunk_FUN_05e1d97c(4), iVar5 != 0)) {
        FUN_0488143c(&local_110);
        if ((DAT_0a4ad97b & 1) == 0) {
          DAT_0a4ad970._0_1_ = s_message_SetSendeSetType_08ad4560[0];
          DAT_0a4ad970._1_1_ = s_message_SetSendeSetType_08ad4560[1];
          DAT_0a4ad970._2_1_ = s_message_SetSendeSetType_08ad4560[2];
          DAT_0a4ad970._3_1_ = s_message_SetSendeSetType_08ad4560[3];
          DAT_0a4ad970._4_1_ = s_message_SetSendeSetType_08ad4560[4];
          DAT_0a4ad970._5_1_ = s_message_SetSendeSetType_08ad4560[5];
          DAT_0a4ad970._6_1_ = s_message_SetSendeSetType_08ad4560[6];
          DAT_0a4ad970._7_1_ = s_message_SetSendeSetType_08ad4560[7];
          DAT_0a4ad978 = 0x6363;
          DAT_0a4ad97a = 0;
          DAT_0a4ad97b = 1;
        }
        if ((DAT_0a4adb00 & 1) == 0) {
          DAT_0a4adaf8._0_1_ = s_message_SetSendeSetType_08ad4560[0x10];
          DAT_0a4adaf8._1_1_ = s_message_SetSendeSetType_08ad4560[0x11];
          DAT_0a4adaf8._2_1_ = s_message_SetSendeSetType_08ad4560[0x12];
          DAT_0a4adaf8._3_1_ = s_message_SetSendeSetType_08ad4560[0x13];
          DAT_0a4adaf8._4_1_ = s_message_SetSendeSetType_08ad4560[0x14];
          DAT_0a4adaf8._5_1_ = s_message_SetSendeSetType_08ad4560[0x15];
          DAT_0a4adaf8._6_1_ = s_message_SetSendeSetType_08ad4560[0x16];
          DAT_0a4adaf8._7_1_ = s_message_SetSendeSetType_08ad4560[0x17];
          DAT_0a4adb00 = 1;
        }
        FUN_05e1d050(auStack_240,4,&local_110,&DAT_0a4ad970,&DAT_0a4adaf8,0x239,0,0);
        if ((DAT_0a4adb4c & 1) == 0) {
          _DAT_0a4adb2c = CONCAT44((int)DAT_08486a50,(int)DAT_08486a48);
          uRam000000000a4adb34 = CONCAT44((int)DAT_084e3f80,(int)DAT_08489788);
          _DAT_0a4adb3c = CONCAT44((int)DAT_08ad4578,(int)DAT_084c7770);
          uRam000000000a4adb44 = CONCAT44((int)DAT_086e8508,(int)DAT_084abdf0);
          DAT_0a4adb4c = 1;
        }
        local_58 = 0;
        uStack_60 = 0;
        local_48 = 0;
        uStack_50 = 0;
        local_78 = 0;
        uStack_80 = 0;
        local_68 = 0;
        uStack_70 = 0;
        local_98 = 0;
        uStack_a0 = 0;
        local_88 = 0;
        uStack_90 = 0;
        ppuStack_b8 = (undefined1 **)0x0;
        local_c0 = (undefined1 **)0x0;
        local_a8 = 0;
        local_b0 = (undefined1 **)0x0;
        FUN_05e1d31c(auStack_240,&DAT_0a4adb2c,&local_c0);
        thunk_FUN_05e1d0bc(auStack_240);
      }
    }
    else {
      iVar5 = thunk_FUN_05e1d97c(3);
      if (iVar5 != 0) {
        FUN_0488143c(local_258);
        ppppppuVar1 = (undefined8 ******)local_258[0];
        if (-1 < cStack_241) {
          ppppppuVar1 = local_258;
        }
        if ((DAT_0a4ad97b & 1) == 0) {
          DAT_0a4ad970._0_1_ = s_message_SetSendeSetType_08ad4560[0];
          DAT_0a4ad970._1_1_ = s_message_SetSendeSetType_08ad4560[1];
          DAT_0a4ad970._2_1_ = s_message_SetSendeSetType_08ad4560[2];
          DAT_0a4ad970._3_1_ = s_message_SetSendeSetType_08ad4560[3];
          DAT_0a4ad970._4_1_ = s_message_SetSendeSetType_08ad4560[4];
          DAT_0a4ad970._5_1_ = s_message_SetSendeSetType_08ad4560[5];
          DAT_0a4ad970._6_1_ = s_message_SetSendeSetType_08ad4560[6];
          DAT_0a4ad970._7_1_ = s_message_SetSendeSetType_08ad4560[7];
          DAT_0a4ad978 = 0x6363;
          DAT_0a4ad97a = 0;
          DAT_0a4ad97b = 1;
        }
        if ((DAT_0a4adb00 & 1) == 0) {
          DAT_0a4adaf8._0_1_ = s_message_SetSendeSetType_08ad4560[0x10];
          DAT_0a4adaf8._1_1_ = s_message_SetSendeSetType_08ad4560[0x11];
          DAT_0a4adaf8._2_1_ = s_message_SetSendeSetType_08ad4560[0x12];
          DAT_0a4adaf8._3_1_ = s_message_SetSendeSetType_08ad4560[0x13];
          DAT_0a4adaf8._4_1_ = s_message_SetSendeSetType_08ad4560[0x14];
          DAT_0a4adaf8._5_1_ = s_message_SetSendeSetType_08ad4560[0x15];
          DAT_0a4adaf8._6_1_ = s_message_SetSendeSetType_08ad4560[0x16];
          DAT_0a4adaf8._7_1_ = s_message_SetSendeSetType_08ad4560[0x17];
          DAT_0a4adb00 = 1;
        }
        FUN_05e1d050(auStack_240,3,ppppppuVar1,&DAT_0a4ad970,&DAT_0a4adaf8,0x237,0,0);
        FUN_04cbe4cc(local_270,param_1);
        local_110 = local_270[0];
        if (-1 < cStack_259) {
          local_110 = (undefined1 *)local_270;
        }
        local_108 = 0;
        uVar8 = *(uint *)(param_1 + 0xc);
        local_160 = (undefined1 *)0x0;
        if ((DAT_0a4adbd0 & 1) == 0) {
          uVar12 = 0;
          do {
            uVar14 = *(undefined4 *)((long)&DAT_08ad519e + uVar12);
            uVar3 = CONCAT12((char)((uint)uVar14 >> 8),(short)uVar14) & 0xff00ff;
            uVar15 = *(undefined4 *)((long)&DAT_08ad518a + uVar12 % 0x14);
            *(uint *)((long)&DAT_0a4adb88 + uVar12) =
                 CONCAT13((char)((uint)uVar14 >> 0x18) + 0x8aU ^ (byte)((uint)uVar15 >> 0x18),
                          CONCAT12((char)((uint)uVar14 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar15 >> 0x10),
                                   CONCAT11((char)(uVar3 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar15 >> 8),
                                            (char)uVar3 + 0x8aU ^ (byte)uVar15)));
            uVar12 = uVar12 + 4;
          } while (uVar12 != 0x48);
          DAT_0a4adbd0 = 1;
        }
        uVar12 = (ulong)uVar8;
        lVar4 = 0;
        do {
          lVar10 = lVar4;
          uVar8 = (uint)uVar12;
          local_158[lVar10] =
               *(undefined1 *)
                ((long)&DAT_0a4adb88 + (ulong)(uVar8 + (int)(uVar12 / 10) * -10 + 0x23));
          uVar12 = uVar12 / 10;
          lVar4 = lVar10 + 1;
        } while (9 < uVar8);
        local_158[lVar10 + 1] = 0;
        if (8 < lVar10 + 8U) {
          puVar11 = local_158;
          puVar7 = local_158 + lVar10;
          do {
            puVar11 = puVar11 + 1;
            uVar2 = *puVar7;
            puVar9 = puVar7 + -1;
            *puVar7 = puVar11[-1];
            puVar11[-1] = uVar2;
            puVar7 = puVar9;
          } while (puVar11 < puVar9);
        }
        local_160 = local_158;
        local_1b0 = local_1a8;
        lVar4 = 0;
        uVar12 = param_2;
        do {
          lVar10 = lVar4;
          uVar8 = (uint)uVar12;
          local_1a8[lVar10] =
               *(undefined1 *)
                ((long)&DAT_0a4adb88 +
                (ulong)(uVar8 + (int)((uVar12 & 0xffffffff) / 10) * -10 + 0x23));
          lVar4 = lVar10 + 1;
          uVar12 = (uVar12 & 0xffffffff) / 10;
        } while (9 < uVar8);
        local_1a8[lVar10 + 1] = 0;
        if (8 < lVar10 + 8U) {
          puVar11 = local_1a8;
          puVar7 = local_1a8 + lVar10;
          do {
            puVar11 = puVar11 + 1;
            uVar2 = *puVar7;
            puVar9 = puVar7 + -1;
            *puVar7 = puVar11[-1];
            puVar11[-1] = uVar2;
            puVar7 = puVar9;
          } while (puVar11 < puVar9);
        }
        if ((DAT_0a4adb2b & 1) == 0) {
          _DAT_0a4adb04 = CONCAT44((int)DAT_084ec280,(int)DAT_08486a48);
          uRam000000000a4adb0c = CONCAT44((int)DAT_08502948,(int)DAT_084e3ff8);
          _DAT_0a4adb14 = CONCAT44((int)DAT_084caf78,(int)DAT_088a05b0);
          uRam000000000a4adb1c = CONCAT44((int)DAT_084fdd78,(int)DAT_084d7818);
          DAT_0a4adb24 = (undefined4)DAT_08502a28;
          DAT_0a4adb28 = 0x5f25;
          DAT_0a4adb2a = 0;
          DAT_0a4adb2b = 1;
        }
        local_c0 = &local_110;
        ppuStack_b8 = &local_160;
        local_b0 = &local_1b0;
        uStack_a0 = 0;
        local_a8 = 0;
        uStack_90 = 0;
        local_98 = 0;
        uStack_80 = 0;
        local_88 = 0;
        uStack_70 = 0;
        local_78 = 0;
        uStack_60 = 0;
        local_68 = 0;
        uStack_50 = 0;
        local_58 = 0;
        local_48 = 0;
        FUN_05e1d31c(auStack_240,&DAT_0a4adb04,&local_c0);
        if (cStack_259 < '\0') {
          __ZdlPvm(local_270[0],CONCAT17(cStack_259,local_260) & 0x7fffffffffffffff);
        }
        thunk_FUN_05e1d0bc(auStack_240);
        if (cStack_241 < '\0') {
          __ZdlPvm(local_258[0],CONCAT17(cStack_241,local_248) & 0x7fffffffffffffff);
        }
      }
    }
  }
  *(int *)(param_1 + 0xc) = (int)param_2;
  *(undefined8 *)(param_1 + 0x108) = *(undefined8 *)(param_1 + 0xc);
  FUN_04cbebac(param_1);
  if (*(long *)(param_1 + 0x230) == 0) {
    puVar6 = (undefined8 *)__Znwm(0x128);
    puVar6[1] = 0;
    puVar6[2] = 0;
    *puVar6 = &PTR_FUN_09dd9070;
    puVar6[6] = 0;
    puVar6[5] = 0;
    puVar6[8] = 0;
    puVar6[7] = 0;
    puVar6[10] = 0;
    puVar6[9] = 0;
    puVar6[0xc] = 0;
    puVar6[0xb] = 0;
    puVar6[0xe] = 0;
    puVar6[0xd] = 0;
    puVar6[0x10] = 0;
    puVar6[0xf] = 0;
    puVar6[0x12] = 0;
    puVar6[0x11] = 0;
    puVar6[0x14] = 0;
    puVar6[0x13] = 0;
    puVar6[0x16] = 0;
    puVar6[0x15] = 0;
    puVar6[0x18] = 0;
    puVar6[0x17] = 0;
    puVar6[0x1a] = 0;
    puVar6[0x19] = 0;
    puVar6[0x1c] = 0;
    puVar6[0x1b] = 0;
    puVar6[0x1e] = 0;
    puVar6[0x1d] = 0;
    puVar6[0x20] = 0;
    puVar6[0x1f] = 0;
    plVar13 = *(long **)(param_1 + 0x238);
    *(undefined8 **)(param_1 + 0x238) = puVar6;
    puVar6[4] = 0;
    puVar6[3] = 0;
    puVar6[0x22] = 0;
    puVar6[0x21] = 0;
    puVar6[0x24] = 0;
    puVar6[0x23] = 0;
    *(undefined8 **)(param_1 + 0x230) = puVar6 + 3;
    if (plVar13 != (long *)0x0) {
      LOAcquire();
      lVar4 = plVar13[1];
      plVar13[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*plVar13 + 0x10))(plVar13);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
      }
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_38) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


