// Ghidra inferred pseudocode; requested=0x319a6a8
// entry=0319a6a8 end=0319ae73

void FUN_0319a6a8(undefined8 *param_1,long param_2,uint *param_3,uint *param_4)

{
  undefined8 ******ppppppuVar1;
  undefined1 uVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  int iVar5;
  ulong uVar6;
  undefined1 *puVar7;
  uint uVar8;
  long lVar9;
  undefined1 *puVar10;
  undefined1 *puVar11;
  long lVar12;
  undefined8 *****local_278 [2];
  undefined7 local_268;
  char cStack_261;
  undefined8 *****local_260;
  undefined1 *puStack_258;
  undefined1 *local_250;
  undefined8 local_248 [2];
  undefined7 local_238;
  char cStack_231;
  undefined8 *****local_1b8;
  undefined1 local_1b0;
  undefined7 local_1a8;
  char cStack_1a1;
  undefined1 *local_168;
  undefined1 local_160 [72];
  undefined1 *local_118;
  undefined1 local_110 [72];
  undefined1 **local_c8;
  undefined1 **ppuStack_c0;
  undefined8 *****local_b8;
  undefined8 uStack_b0;
  undefined8 uStack_a8;
  undefined8 uStack_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 local_60;
  undefined8 uStack_58;
  undefined8 local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar12 = *(long *)(param_2 + 0xb20);
  FUN_030e3df8(local_248,*param_3,*param_4);
  lVar12 = FUN_00da468c(lVar12 + 0x28,local_248);
  if (cStack_231 < '\0') {
    __ZdlPvm(local_248[0],CONCAT17(cStack_231,local_238) & 0x7fffffffffffffff);
  }
  if (lVar12 == 0) {
    iVar5 = thunk_FUN_05e1d97c(4);
    if (iVar5 != 0) {
      FUN_0488143c(&local_1b8);
      ppppppuVar1 = (undefined8 ******)local_1b8;
      if (-1 < cStack_1a1) {
        ppppppuVar1 = &local_1b8;
      }
      if ((DAT_0a3dd363 & 1) == 0) {
        uVar6 = 0;
        do {
          (&DAT_0a3dd350)[uVar6] = (&DAT_088bce97)[uVar6] + 0x8a ^ (&DAT_088bce87)[uVar6 & 0xf];
          uVar6 = uVar6 + 1;
        } while (uVar6 != 0x13);
        DAT_0a3dd363 = 1;
      }
      if ((DAT_0a3de31b & 1) == 0) {
        DAT_0a3de310._0_1_ = s_GetHandlonTh_08854480[0];
        DAT_0a3de310._1_1_ = s_GetHandlonTh_08854480[1];
        DAT_0a3de310._2_1_ = s_GetHandlonTh_08854480[2];
        DAT_0a3de310._3_1_ = s_GetHandlonTh_08854480[3];
        DAT_0a3de310._4_1_ = s_GetHandlonTh_08854480[4];
        DAT_0a3de310._5_1_ = s_GetHandlonTh_08854480[5];
        DAT_0a3de310._6_1_ = s_GetHandlonTh_08854480[6];
        DAT_0a3de310._7_1_ = s_GetHandlonTh_08854480[7];
        DAT_0a3de318 = 0x7265;
        DAT_0a3de31a = 0;
        DAT_0a3de31b = 1;
      }
      FUN_05e1d050(local_248,4,ppppppuVar1,&DAT_0a3dd350,&DAT_0a3de310,0x654,0,0);
      uVar8 = *param_3;
      local_118 = (undefined1 *)0x0;
      if ((DAT_0a3e2eba & 1) == 0) {
        uVar6 = 0;
        do {
          uVar3 = *(undefined4 *)((long)&DAT_088c56c9 + uVar6);
          uVar4 = *(undefined4 *)((long)&DAT_088c56b5 + uVar6 % 0x14);
          *(uint *)((long)&DAT_0a3e2e72 + uVar6) =
               CONCAT13((char)((uint)uVar3 >> 0x18) + 0x69U ^ (byte)((uint)uVar4 >> 0x18),
                        CONCAT12((char)((uint)uVar3 >> 0x10) + 0x69U ^ (byte)((uint)uVar4 >> 0x10),
                                 CONCAT11((char)((uint)uVar3 >> 8) + 0x69U ^
                                          (byte)((uint)uVar4 >> 8),(char)uVar3 + 0x69U ^ (byte)uVar4
                                         )));
          uVar6 = uVar6 + 4;
        } while (uVar6 != 0x48);
        DAT_0a3e2eba = 1;
      }
      uVar6 = (ulong)uVar8;
      lVar12 = 0;
      do {
        lVar9 = lVar12;
        uVar8 = (uint)uVar6;
        local_110[lVar9] =
             *(undefined1 *)((long)&DAT_0a3e2e72 + (ulong)(uVar8 + (int)(uVar6 / 10) * -10 + 0x23));
        uVar6 = uVar6 / 10;
        lVar12 = lVar9 + 1;
      } while (9 < uVar8);
      local_110[lVar9 + 1] = 0;
      if (8 < lVar9 + 8U) {
        puVar10 = local_110;
        puVar7 = local_110 + lVar9;
        do {
          puVar10 = puVar10 + 1;
          uVar2 = *puVar7;
          puVar11 = puVar7 + -1;
          *puVar7 = puVar10[-1];
          puVar10[-1] = uVar2;
          puVar7 = puVar11;
        } while (puVar10 < puVar11);
      }
      local_118 = local_110;
      local_168 = local_160;
      lVar12 = 0;
      uVar6 = (ulong)*param_4;
      do {
        lVar9 = lVar12;
        uVar8 = (uint)uVar6;
        local_160[lVar9] =
             *(undefined1 *)((long)&DAT_0a3e2e72 + (ulong)(uVar8 + (int)(uVar6 / 10) * -10 + 0x23));
        lVar12 = lVar9 + 1;
        uVar6 = uVar6 / 10;
      } while (9 < uVar8);
      local_160[lVar9 + 1] = 0;
      if (8 < lVar9 + 8U) {
        puVar10 = local_160;
        puVar7 = local_160 + lVar9;
        do {
          puVar10 = puVar10 + 1;
          uVar2 = *puVar7;
          puVar11 = puVar7 + -1;
          *puVar7 = puVar10[-1];
          puVar10[-1] = uVar2;
          puVar7 = puVar11;
        } while (puVar10 < puVar11);
      }
      if ((DAT_0a3de346 & 1) == 0) {
        uVar6 = 0;
        do {
          (&DAT_0a3de31c)[uVar6] = (&DAT_088be360)[uVar6] + 0x8a ^ (&DAT_088be350)[uVar6 & 0xf];
          uVar6 = uVar6 + 1;
        } while (uVar6 != 0x2a);
        DAT_0a3de346 = 1;
      }
      local_c8 = &local_118;
      ppuStack_c0 = &local_168;
      uStack_b0 = 0;
      local_b8 = (undefined8 ******)0x0;
      uStack_a0 = 0;
      uStack_a8 = 0;
      local_90 = 0;
      uStack_98 = 0;
      local_80 = 0;
      uStack_88 = 0;
      local_70 = 0;
      uStack_78 = 0;
      local_60 = 0;
      uStack_68 = 0;
      local_50 = 0;
      uStack_58 = 0;
      FUN_05e1d31c(local_248,&DAT_0a3de31c,&local_c8);
      thunk_FUN_05e1d0bc(local_248);
      if (cStack_1a1 < '\0') {
        __ZdlPvm(local_1b8,CONCAT17(cStack_1a1,local_1a8) & 0x7fffffffffffffff);
      }
    }
    *param_1 = 0;
    param_1[1] = 0;
  }
  else {
    puStack_258 = &SUB_aaaaaaaaaaaaaaaa;
    local_250 = &SUB_aaaaaaaaaaaaaaaa;
    local_260 = (undefined8 *****)&SUB_aaaaaaaaaaaaaaaa;
    if (*(char *)(lVar12 + 0x3f) < '\0') {
      FUN_00018d20(&local_260,*(undefined8 *)(lVar12 + 0x28),*(undefined8 *)(lVar12 + 0x30));
    }
    else {
      puStack_258 = *(undefined1 **)(lVar12 + 0x30);
      local_260 = *(undefined8 ******)(lVar12 + 0x28);
      local_250 = *(undefined1 **)(lVar12 + 0x38);
    }
    lVar12 = FUN_03217130(*(undefined8 *)(param_2 + 0xb20),&local_260);
    if (lVar12 == 0) {
      iVar5 = thunk_FUN_05e1d97c(4);
      if (iVar5 != 0) {
        FUN_0488143c(local_278);
        ppppppuVar1 = (undefined8 ******)local_278[0];
        if (-1 < cStack_261) {
          ppppppuVar1 = local_278;
        }
        if ((DAT_0a3dd363 & 1) == 0) {
          uVar6 = 0;
          do {
            (&DAT_0a3dd350)[uVar6] = (&DAT_088bce97)[uVar6] + 0x8a ^ (&DAT_088bce87)[uVar6 & 0xf];
            uVar6 = uVar6 + 1;
          } while (uVar6 != 0x13);
          DAT_0a3dd363 = 1;
        }
        if ((DAT_0a3de31b & 1) == 0) {
          DAT_0a3de310._0_1_ = s_GetHandlonTh_08854480[0];
          DAT_0a3de310._1_1_ = s_GetHandlonTh_08854480[1];
          DAT_0a3de310._2_1_ = s_GetHandlonTh_08854480[2];
          DAT_0a3de310._3_1_ = s_GetHandlonTh_08854480[3];
          DAT_0a3de310._4_1_ = s_GetHandlonTh_08854480[4];
          DAT_0a3de310._5_1_ = s_GetHandlonTh_08854480[5];
          DAT_0a3de310._6_1_ = s_GetHandlonTh_08854480[6];
          DAT_0a3de310._7_1_ = s_GetHandlonTh_08854480[7];
          DAT_0a3de318 = 0x7265;
          DAT_0a3de31a = 0;
          DAT_0a3de31b = 1;
        }
        FUN_05e1d050(local_248,4,ppppppuVar1,&DAT_0a3dd350,&DAT_0a3de310,0x65d,0,0);
        uVar8 = *param_3;
        local_118 = (undefined1 *)0x0;
        if ((DAT_0a3e2eba & 1) == 0) {
          uVar6 = 0;
          do {
            uVar3 = *(undefined4 *)((long)&DAT_088c56c9 + uVar6);
            uVar4 = *(undefined4 *)((long)&DAT_088c56b5 + uVar6 % 0x14);
            *(uint *)((long)&DAT_0a3e2e72 + uVar6) =
                 CONCAT13((char)((uint)uVar3 >> 0x18) + 0x69U ^ (byte)((uint)uVar4 >> 0x18),
                          CONCAT12((char)((uint)uVar3 >> 0x10) + 0x69U ^ (byte)((uint)uVar4 >> 0x10)
                                   ,CONCAT11((char)((uint)uVar3 >> 8) + 0x69U ^
                                             (byte)((uint)uVar4 >> 8),
                                             (char)uVar3 + 0x69U ^ (byte)uVar4)));
            uVar6 = uVar6 + 4;
          } while (uVar6 != 0x48);
          DAT_0a3e2eba = 1;
        }
        uVar6 = (ulong)uVar8;
        lVar12 = 0;
        do {
          lVar9 = lVar12;
          uVar8 = (uint)uVar6;
          local_110[lVar9] =
               *(undefined1 *)
                ((long)&DAT_0a3e2e72 + (ulong)(uVar8 + (int)(uVar6 / 10) * -10 + 0x23));
          uVar6 = uVar6 / 10;
          lVar12 = lVar9 + 1;
        } while (9 < uVar8);
        local_110[lVar9 + 1] = 0;
        if (8 < lVar9 + 8U) {
          puVar10 = local_110;
          puVar7 = local_110 + lVar9;
          do {
            puVar10 = puVar10 + 1;
            uVar2 = *puVar7;
            puVar11 = puVar7 + -1;
            *puVar7 = puVar10[-1];
            puVar10[-1] = uVar2;
            puVar7 = puVar11;
          } while (puVar10 < puVar11);
        }
        local_118 = local_110;
        local_168 = local_160;
        lVar12 = 0;
        uVar6 = (ulong)*param_4;
        do {
          lVar9 = lVar12;
          uVar8 = (uint)uVar6;
          local_160[lVar9] =
               *(undefined1 *)
                ((long)&DAT_0a3e2e72 + (ulong)(uVar8 + (int)(uVar6 / 10) * -10 + 0x23));
          lVar12 = lVar9 + 1;
          uVar6 = uVar6 / 10;
        } while (9 < uVar8);
        local_160[lVar9 + 1] = 0;
        if (8 < lVar9 + 8U) {
          puVar10 = local_160;
          puVar7 = local_160 + lVar9;
          do {
            puVar10 = puVar10 + 1;
            uVar2 = *puVar7;
            puVar11 = puVar7 + -1;
            *puVar7 = puVar10[-1];
            puVar10[-1] = uVar2;
            puVar7 = puVar11;
          } while (puVar10 < puVar11);
        }
        local_1b8 = local_260;
        if (-1 < (long)local_250) {
          local_1b8 = &local_260;
        }
        local_1b0 = 0;
        if ((DAT_0a3de382 & 1) == 0) {
          uVar6 = 0;
          do {
            (&DAT_0a3de347)[uVar6] = (&DAT_088be39a)[uVar6] + 0x8a ^ (&DAT_088be38a)[uVar6 & 0xf];
            uVar6 = uVar6 + 1;
          } while (uVar6 != 0x3b);
          DAT_0a3de382 = 1;
        }
        local_c8 = &local_118;
        ppuStack_c0 = &local_168;
        local_b8 = &local_1b8;
        uStack_a8 = 0;
        uStack_b0 = 0;
        uStack_98 = 0;
        uStack_a0 = 0;
        uStack_88 = 0;
        local_90 = 0;
        uStack_78 = 0;
        local_80 = 0;
        uStack_68 = 0;
        local_70 = 0;
        uStack_58 = 0;
        local_60 = 0;
        local_50 = 0;
        FUN_05e1d31c(local_248,&DAT_0a3de347,&local_c8);
        thunk_FUN_05e1d0bc(local_248);
        if (cStack_261 < '\0') {
          __ZdlPvm(local_278[0],CONCAT17(cStack_261,local_268) & 0x7fffffffffffffff);
        }
      }
      *param_1 = 0;
      param_1[1] = 0;
    }
    else {
      lVar9 = *(long *)(lVar12 + 0x30);
      *param_1 = *(undefined8 *)(lVar12 + 0x28);
      param_1[1] = lVar9;
      if (lVar9 != 0) {
        *(long *)(lVar9 + 8) = *(long *)(lVar9 + 8) + 1;
      }
    }
    if ((long)local_250 < 0) {
      __ZdlPvm(local_260,(ulong)local_250 & 0x7fffffffffffffff);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


