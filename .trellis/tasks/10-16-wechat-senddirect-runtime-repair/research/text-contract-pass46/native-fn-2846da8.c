// Ghidra inferred pseudocode; requested=0x2846da8
// entry=02846da8 end=0284804f

/* WARNING: Removing unreachable block (ram,0x02847a8c) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_02846da8(undefined8 *param_1,int param_2,long param_3)

{
  uint uVar1;
  undefined8 ******ppppppuVar2;
  undefined1 uVar3;
  uint3 uVar4;
  bool bVar5;
  int iVar6;
  long *plVar7;
  undefined8 *puVar8;
  undefined1 *puVar9;
  undefined8 uVar10;
  long *plVar11;
  long lVar12;
  undefined1 *puVar13;
  undefined1 *puVar14;
  long lVar15;
  ulong uVar16;
  ulong uVar17;
  int iVar18;
  undefined8 *puVar19;
  undefined8 ******ppppppuVar20;
  uint uVar21;
  undefined4 uVar22;
  undefined4 uVar23;
  undefined8 local_3f0;
  undefined8 *****pppppuStack_3e8;
  undefined1 *local_3e0;
  undefined1 *puStack_3d8;
  undefined1 *local_3d0;
  long *local_3c8;
  undefined8 *****local_3b8 [2];
  undefined7 local_3a8;
  char cStack_3a1;
  undefined8 *****local_3a0 [2];
  undefined7 local_390;
  char cStack_389;
  undefined8 local_388;
  undefined8 local_380;
  undefined8 local_378;
  ulong local_370;
  undefined1 local_368;
  undefined4 local_364;
  undefined4 local_2f8;
  int local_2f4;
  undefined1 *local_2f0;
  ulong uStack_2e8;
  ulong local_2e0;
  ulong uStack_2d8;
  undefined8 local_2d0;
  long lStack_2c8;
  undefined8 local_2c0;
  undefined8 uStack_2b8;
  undefined8 local_2b0;
  undefined8 uStack_2a8;
  undefined8 local_2a0;
  undefined8 uStack_298;
  undefined8 local_290;
  ulong uStack_288;
  undefined8 local_280;
  undefined8 uStack_278;
  ulong local_270;
  undefined8 uStack_268;
  undefined4 local_260;
  undefined4 uStack_25c;
  undefined4 uStack_258;
  int iStack_254;
  undefined4 local_250;
  undefined4 uStack_24c;
  undefined8 uStack_248;
  undefined1 *local_240;
  undefined1 *puStack_238;
  long *local_230;
  undefined1 *local_228;
  undefined8 local_220;
  undefined8 local_218;
  undefined8 local_210;
  undefined1 uStack_1c9;
  undefined8 local_1c8;
  undefined8 local_1c0;
  undefined8 *****local_178;
  undefined1 local_170;
  undefined7 local_168;
  char cStack_161;
  undefined1 uStack_129;
  undefined8 local_128;
  undefined1 local_120 [72];
  undefined8 *local_d8;
  undefined8 *****local_d0;
  undefined8 *puStack_c8;
  undefined8 *puStack_c0;
  undefined8 local_b8;
  undefined8 uStack_b0;
  undefined8 uStack_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined8 uStack_88;
  undefined8 uStack_80;
  undefined8 local_78;
  undefined8 uStack_70;
  undefined8 uStack_68;
  undefined8 local_60;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  plVar7 = (long *)FUN_04669774();
  puVar19 = param_1 + 4;
  param_1[5] = 0;
  *puVar19 = 0;
  param_1[1] = 0;
  *param_1 = 0;
  param_1[3] = 0;
  param_1[2] = 0;
  puVar8 = (undefined8 *)__Znwm(0x20);
  puVar8[1] = 0;
  puVar8[2] = 0;
  *puVar8 = &PTR_FUN_09db1d40;
  puVar8[3] = 0;
  param_1[4] = puVar8 + 3;
  param_1[5] = puVar8;
  local_220 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_238 = &SUB_aaaaaaaaaaaaaaaa;
  local_240 = &SUB_aaaaaaaaaaaaaaaa;
  local_228 = &SUB_aaaaaaaaaaaaaaaa;
  local_230 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0513028c(&local_240);
  if (local_230 != (long *)0x0) {
    (**(code **)(*local_230 + 8))();
  }
  local_228 = (undefined1 *)CONCAT44(local_228._4_4_,param_2);
  local_220 = (undefined1 *)
              (CONCAT44(local_220._4_4_,(uint)local_220 & 0xfffffff8 | (uint)(param_3 != 0) << 2) |
              3);
  local_230 = (long *)param_3;
  if (puStack_238 == (undefined1 *)0x0) {
    puVar9 = (undefined1 *)__Znwm(0x38);
    FUN_0465a1bc();
    puStack_238 = puVar9;
  }
  FUN_0461b850(puStack_238);
  local_2f0 = &DAT_aaaaaaaa00000000;
  uStack_24c = 0xaaaaaaaa;
  uStack_248 = 0;
  local_2c0 = 0;
  lStack_2c8 = 0;
  local_2b0 = 0;
  uStack_2b8 = 0;
  local_2a0 = 0;
  uStack_2a8 = 0;
  local_290 = 0;
  uStack_298 = 0;
  local_280 = 0;
  uStack_288 = 0;
  local_270 = 0;
  uStack_278 = 0;
  local_260 = 0;
  uStack_268 = 0;
  iStack_254 = 0;
  local_250 = 0;
  uStack_25c = 0;
  uStack_258 = 0;
  local_2f8 = 0x6e;
  uStack_2e8 = *(ulong *)(param_3 + 0x20) & 0xffffffff;
  local_2e0 = *(ulong *)(param_3 + 0x20) >> 0x20;
  local_2d0 = 0;
  uStack_2d8 = 0;
  local_2f4 = param_2;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (&uStack_298,*(undefined8 *)(param_3 + 0x10));
  iVar6 = thunk_FUN_05e1d97c(2);
  if (iVar6 != 0) {
    FUN_0488143c(&local_3f0);
    puVar8 = (undefined8 *)local_3f0;
    if (-1 < (long)local_3e0) {
      puVar8 = &local_3f0;
    }
    if ((DAT_0a39dcf7 & 1) == 0) {
      DAT_0a39dce8._0_1_ = s_byp_hand_byp_08804940[0];
      DAT_0a39dce8._1_1_ = s_byp_hand_byp_08804940[1];
      DAT_0a39dce8._2_1_ = s_byp_hand_byp_08804940[2];
      DAT_0a39dce8._3_1_ = s_byp_hand_byp_08804940[3];
      DAT_0a39dce8._4_1_ = s_byp_hand_byp_08804940[4];
      DAT_0a39dce8._5_1_ = s_byp_hand_byp_08804940[5];
      DAT_0a39dce8._6_1_ = s_byp_hand_byp_08804940[6];
      DAT_0a39dce8._7_1_ = s_byp_hand_byp_08804940[7];
      DAT_0a39dcf0 = (undefined4)DAT_08549b60;
      DAT_0a39dcf4 = 0x6363;
      DAT_0a39dcf6 = 0;
      DAT_0a39dcf7 = 1;
    }
    if ((DAT_0a39dd14 & 1) == 0) {
      uRam000000000a39dd08 = _UNK_088049f8;
      _DAT_0a39dd00 = _DAT_088049f0;
      DAT_0a39dd10 = (undefined4)DAT_085b0660;
      DAT_0a39dd14 = 1;
    }
    FUN_05e1d050(&local_388,2,puVar8,&DAT_0a39dce8,&DAT_0a39dd00,0x2a,0,0);
    local_128 = (undefined1 *)0x0;
    if ((DAT_0a39df51 & 1) == 0) {
      uVar17 = 0;
      do {
        uVar22 = *(undefined4 *)((long)&DAT_08804e86 + uVar17);
        uVar4 = CONCAT12((char)((uint)uVar22 >> 8),(short)uVar22) & 0xff00ff;
        uVar23 = *(undefined4 *)((long)&DAT_08804e72 + uVar17 % 0x14);
        *(uint *)((long)&DAT_0a39df09 + uVar17) =
             CONCAT13((char)((uint)uVar22 >> 0x18) + 0x8aU ^ (byte)((uint)uVar23 >> 0x18),
                      CONCAT12((char)((uint)uVar22 >> 0x10) + 0x8aU ^ (byte)((uint)uVar23 >> 0x10),
                               CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^ (byte)((uint)uVar23 >> 8),
                                        (char)uVar4 + 0x8aU ^ (byte)uVar23)));
        uVar17 = uVar17 + 4;
      } while (uVar17 != 0x48);
      DAT_0a39df51 = 1;
    }
    lVar12 = 8;
    iVar6 = param_2;
    do {
      lVar15 = lVar12;
      local_120[lVar15 + -8] = *(undefined1 *)((long)&DAT_0a39df09 + (long)(iVar6 % 10 + 0x23));
      lVar12 = lVar15 + 1;
      uVar21 = iVar6 + 9;
      iVar6 = iVar6 / 10;
    } while (0x12 < uVar21);
    if (param_2 < 0) {
      local_120[lVar15 + -7] = 0x2d;
      lVar12 = lVar15 + 2;
    }
    local_120[lVar12 + -8] = 0;
    if (9 < lVar12) {
      puVar9 = local_120;
      puVar14 = &uStack_129 + lVar12;
      do {
        puVar9 = puVar9 + 1;
        uVar3 = *puVar14;
        puVar13 = puVar14 + -1;
        *puVar14 = puVar9[-1];
        puVar9[-1] = uVar3;
        puVar14 = puVar13;
      } while (puVar9 < puVar13);
    }
    local_128 = local_120;
    FUN_04980e70(local_3a0,*(undefined8 *)(param_3 + 8));
    local_178 = local_3a0[0];
    if (-1 < cStack_389) {
      local_178 = local_3a0;
    }
    local_170 = 0;
    FUN_04980e70(local_3b8,*(undefined8 *)(param_3 + 0x10));
    local_1c8 = (undefined8 ******)local_3b8[0];
    if (-1 < cStack_3a1) {
      local_1c8 = local_3b8;
    }
    local_1c0._0_1_ = 0;
    plVar11 = *(long **)(param_3 + 0x18);
    local_218 = (long *)*plVar11;
    if (-1 < *(char *)((long)plVar11 + 0x17)) {
      local_218 = plVar11;
    }
    local_210._0_1_ = 0;
    if ((DAT_0a39dd5f & 1) == 0) {
      uVar17 = 0;
      do {
        uVar22 = *(undefined4 *)((long)&DAT_08804b88 + uVar17);
        uVar23 = *(undefined4 *)((long)&DAT_08804b74 + uVar17 % 0x14);
        *(uint *)((long)&DAT_0a39dd15 + uVar17) =
             CONCAT13((byte)((uint)uVar23 >> 0x18) ^ (byte)((uint)uVar22 >> 0x18),
                      CONCAT12((byte)((uint)uVar23 >> 0x10) ^ (byte)((uint)uVar22 >> 0x10),
                               CONCAT11((byte)((uint)uVar23 >> 8) ^ (byte)((uint)uVar22 >> 8),
                                        (byte)uVar23 ^ (byte)uVar22)));
        uVar17 = uVar17 + 4;
      } while (uVar17 != 0x48);
      DAT_0a39dd5d = 0x5f;
      DAT_0a39dd5f = 1;
    }
    local_d8 = &local_128;
    local_d0 = &local_178;
    puStack_c8 = &local_1c8;
    puStack_c0 = &local_218;
    uStack_b0 = 0;
    local_b8 = 0;
    uStack_a0 = 0;
    uStack_a8 = 0;
    uStack_90 = 0;
    local_98 = 0;
    uStack_80 = 0;
    uStack_88 = 0;
    uStack_70 = 0;
    local_78 = 0;
    local_60 = 0;
    uStack_68 = 0;
    FUN_05e1d31c(&local_388,&DAT_0a39dd15,&local_d8);
    if (cStack_3a1 < '\0') {
      __ZdlPvm(local_3b8[0],CONCAT17(cStack_3a1,local_3a8) & 0x7fffffffffffffff);
    }
    if (cStack_389 < '\0') {
      __ZdlPvm(local_3a0[0],CONCAT17(cStack_389,local_390) & 0x7fffffffffffffff);
    }
    thunk_FUN_05e1d0bc(&local_388);
    if ((long)local_3e0 < 0) {
      __ZdlPvm(local_3f0,(ulong)local_3e0 & 0x7fffffffffffffff);
    }
  }
  puStack_3d8 = &SUB_aaaaaaaaaaaaaaaa;
  local_3e0 = &SUB_aaaaaaaaaaaaaaaa;
  local_3c8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_3d0 = &SUB_aaaaaaaaaaaaaaaa;
  pppppuStack_3e8 = (undefined8 *****)&SUB_aaaaaaaaaaaaaaaa;
  local_3f0 = &SUB_aaaaaaaaaaaaaaaa;
  uVar10 = (**(code **)(*plVar7 + 0x18))(plVar7);
  puStack_c8 = (undefined8 *)((ulong)puStack_c8 & 0xffffffffffffff);
  local_d8 = (undefined8 *)((ulong)local_d8 & 0xffffffffffffff00);
  local_388 = DAT_0875d510;
  local_364 = 0;
  local_378 = 0;
  local_370 = 0;
  local_380 = 0;
  local_368 = 0;
  FUN_028481ec(&local_3f0,uVar10,&local_240,&local_d8,&local_388);
  if ((long)local_370 < 0) {
    __ZdlPvm(local_380,local_370 & 0x7fffffffffffffff);
  }
  if ((int)local_3f0 == 0 && local_3f0._4_4_ == 0) {
    lVar12 = *(long *)(local_3d0 + 8);
    if (lVar12 == 0) {
      lVar12 = *(long *)(DAT_0a520f60 + 8);
    }
    uVar21 = (uint)(*(int *)(lVar12 + 0x10) == 0);
  }
  else {
    uVar21 = 0;
  }
  *param_1 = local_3f0;
  ppppppuVar20 = (undefined8 ******)((ulong)&local_3f0 | 8);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_1 + 1,ppppppuVar20)
  ;
  if (uVar21 == 0) {
    iVar6 = thunk_FUN_05e1d97c(4);
    if (iVar6 != 0) {
      FUN_0488143c(local_3a0);
      ppppppuVar2 = (undefined8 ******)local_3a0[0];
      if (-1 < cStack_389) {
        ppppppuVar2 = local_3a0;
      }
      if ((DAT_0a39dcf7 & 1) == 0) {
        DAT_0a39dce8._0_1_ = s_byp_hand_byp_08804940[0];
        DAT_0a39dce8._1_1_ = s_byp_hand_byp_08804940[1];
        DAT_0a39dce8._2_1_ = s_byp_hand_byp_08804940[2];
        DAT_0a39dce8._3_1_ = s_byp_hand_byp_08804940[3];
        DAT_0a39dce8._4_1_ = s_byp_hand_byp_08804940[4];
        DAT_0a39dce8._5_1_ = s_byp_hand_byp_08804940[5];
        DAT_0a39dce8._6_1_ = s_byp_hand_byp_08804940[6];
        DAT_0a39dce8._7_1_ = s_byp_hand_byp_08804940[7];
        DAT_0a39dcf0 = (undefined4)DAT_08549b60;
        DAT_0a39dcf4 = 0x6363;
        DAT_0a39dcf6 = 0;
        DAT_0a39dcf7 = 1;
      }
      if ((DAT_0a39dd14 & 1) == 0) {
        uRam000000000a39dd08 = _UNK_088049f8;
        _DAT_0a39dd00 = _DAT_088049f0;
        DAT_0a39dd10 = (undefined4)DAT_085b0660;
        DAT_0a39dd14 = 1;
      }
      FUN_05e1d050(&local_388,4,ppppppuVar2,&DAT_0a39dce8,&DAT_0a39dd00,0x30,0,0);
      local_128 = (undefined1 *)0x0;
      if ((DAT_0a39df51 & 1) == 0) {
        uVar17 = 0;
        do {
          uVar22 = *(undefined4 *)((long)&DAT_08804e86 + uVar17);
          uVar4 = CONCAT12((char)((uint)uVar22 >> 8),(short)uVar22) & 0xff00ff;
          uVar23 = *(undefined4 *)((long)&DAT_08804e72 + uVar17 % 0x14);
          *(uint *)((long)&DAT_0a39df09 + uVar17) =
               CONCAT13((char)((uint)uVar22 >> 0x18) + 0x8aU ^ (byte)((uint)uVar23 >> 0x18),
                        CONCAT12((char)((uint)uVar22 >> 0x10) + 0x8aU ^ (byte)((uint)uVar23 >> 0x10)
                                 ,CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^ (byte)((uint)uVar23 >> 8)
                                           ,(char)uVar4 + 0x8aU ^ (byte)uVar23)));
          uVar17 = uVar17 + 4;
        } while (uVar17 != 0x48);
        DAT_0a39df51 = 1;
      }
      lVar12 = 8;
      iVar6 = local_3f0._4_4_;
      do {
        lVar15 = lVar12;
        local_120[lVar15 + -8] = *(undefined1 *)((long)&DAT_0a39df09 + (long)(iVar6 % 10 + 0x23));
        lVar12 = lVar15 + 1;
        uVar1 = iVar6 + 9;
        iVar6 = iVar6 / 10;
      } while (0x12 < uVar1);
      if ((long)local_3f0 < 0) {
        local_120[lVar15 + -7] = 0x2d;
        lVar12 = lVar15 + 2;
      }
      local_120[lVar12 + -8] = 0;
      if (9 < lVar12) {
        puVar9 = local_120;
        puVar14 = &uStack_129 + lVar12;
        do {
          puVar9 = puVar9 + 1;
          uVar3 = *puVar14;
          puVar13 = puVar14 + -1;
          *puVar14 = puVar9[-1];
          puVar9[-1] = uVar3;
          puVar14 = puVar13;
        } while (puVar9 < puVar13);
      }
      local_128 = local_120;
      local_178 = pppppuStack_3e8;
      if (-1 < (long)puStack_3d8) {
        local_178 = ppppppuVar20;
      }
      local_170 = 0;
      lVar12 = *(long *)(local_3d0 + 8);
      if (lVar12 == 0) {
        lVar12 = *(long *)(DAT_0a520f60 + 8);
      }
      iVar6 = *(int *)(lVar12 + 0x10);
      local_1c8 = (undefined8 ******)0x0;
      lVar12 = 8;
      iVar18 = iVar6;
      do {
        lVar15 = lVar12;
        *(undefined1 *)((long)&local_1c8 + lVar15) =
             *(undefined1 *)((long)&DAT_0a39df09 + (long)(iVar18 % 10 + 0x23));
        lVar12 = lVar15 + 1;
        uVar1 = iVar18 + 9;
        iVar18 = iVar18 / 10;
      } while (0x12 < uVar1);
      if (iVar6 < 0) {
        *(undefined1 *)((long)&local_1c8 + lVar15 + 1) = 0x2d;
        lVar12 = lVar15 + 2;
      }
      *(undefined1 *)((long)&local_1c8 + lVar12) = 0;
      if (9 < lVar12) {
        puVar9 = &uStack_1c9 + lVar12;
        puVar14 = (undefined1 *)((long)&local_1c0 + 1);
        do {
          uVar3 = *puVar9;
          *puVar9 = puVar14[-1];
          puVar14[-1] = uVar3;
          bVar5 = puVar14 < puVar9 + -1;
          puVar9 = puVar9 + -1;
          puVar14 = puVar14 + 1;
        } while (bVar5);
      }
      local_1c8 = (undefined8 ******)&local_1c0;
      local_218 = (long *)0x0;
      lVar12 = 8;
      iVar6 = (int)local_3f0;
      do {
        lVar15 = lVar12;
        *(undefined1 *)((long)&local_218 + lVar15) =
             *(undefined1 *)((long)&DAT_0a39df09 + (long)(iVar6 % 10 + 0x23));
        lVar12 = lVar15 + 1;
        uVar1 = iVar6 + 9;
        iVar6 = iVar6 / 10;
      } while (0x12 < uVar1);
      if ((int)local_3f0 < 0) {
        *(undefined1 *)((long)&local_218 + lVar15 + 1) = 0x2d;
        lVar12 = lVar15 + 2;
      }
      *(undefined1 *)((long)&local_218 + lVar12) = 0;
      if (9 < lVar12) {
        puVar9 = (undefined1 *)((long)&local_220 + lVar12 + 7);
        puVar14 = (undefined1 *)((long)&local_210 + 1);
        do {
          uVar3 = *puVar9;
          *puVar9 = puVar14[-1];
          puVar14[-1] = uVar3;
          bVar5 = puVar14 < puVar9 + -1;
          puVar9 = puVar9 + -1;
          puVar14 = puVar14 + 1;
        } while (bVar5);
      }
      if ((DAT_0a39dd98 & 1) == 0) {
        _DAT_0a39dd60 = CONCAT44((int)ram0x08804948,(int)DAT_08546648);
        uRam000000000a39dd68 = CONCAT44((int)DAT_0847fde0,(int)DAT_08804950);
        _DAT_0a39dd70 = CONCAT44((int)DAT_08804958,(int)DAT_08503640);
        uRam000000000a39dd78 = CONCAT44((int)DAT_084e32c8,(int)ram0x084e4a40);
        _DAT_0a39dd80 = CONCAT44((int)DAT_084e3ff8,(int)DAT_0875d1b0);
        uRam000000000a39dd88 = CONCAT44((int)DAT_0855a590,(int)DAT_08610dd0);
        DAT_0a39dd90 = CONCAT44((int)DAT_084d1ec0,(int)DAT_08489788);
        DAT_0a39dd98 = 1;
      }
      local_d8 = &local_128;
      local_d0 = &local_178;
      puStack_c8 = &local_1c8;
      puStack_c0 = &local_218;
      uStack_b0 = 0;
      local_b8 = 0;
      uStack_a0 = 0;
      uStack_a8 = 0;
      uStack_90 = 0;
      local_98 = 0;
      uStack_80 = 0;
      uStack_88 = 0;
      uStack_70 = 0;
      local_78 = 0;
      local_60 = 0;
      uStack_68 = 0;
      local_218 = &local_210;
      FUN_05e1d31c(&local_388,&DAT_0a39dd60,&local_d8);
      thunk_FUN_05e1d0bc(&local_388);
      if (cStack_389 < '\0') {
        __ZdlPvm(local_3a0[0],CONCAT17(cStack_389,local_390) & 0x7fffffffffffffff);
      }
    }
  }
  else {
    uVar17 = *(ulong *)(local_3d0 + 0x10);
    if (uVar17 == 0) {
      iVar6 = thunk_FUN_05e1d97c(4);
      if (iVar6 != 0) {
        FUN_0488143c(local_3a0);
        ppppppuVar2 = (undefined8 ******)local_3a0[0];
        if (-1 < cStack_389) {
          ppppppuVar2 = local_3a0;
        }
        if ((DAT_0a39dcf7 & 1) == 0) {
          DAT_0a39dce8._0_1_ = s_byp_hand_byp_08804940[0];
          DAT_0a39dce8._1_1_ = s_byp_hand_byp_08804940[1];
          DAT_0a39dce8._2_1_ = s_byp_hand_byp_08804940[2];
          DAT_0a39dce8._3_1_ = s_byp_hand_byp_08804940[3];
          DAT_0a39dce8._4_1_ = s_byp_hand_byp_08804940[4];
          DAT_0a39dce8._5_1_ = s_byp_hand_byp_08804940[5];
          DAT_0a39dce8._6_1_ = s_byp_hand_byp_08804940[6];
          DAT_0a39dce8._7_1_ = s_byp_hand_byp_08804940[7];
          DAT_0a39dcf0 = (undefined4)DAT_08549b60;
          DAT_0a39dcf4 = 0x6363;
          DAT_0a39dcf6 = 0;
          DAT_0a39dcf7 = 1;
        }
        if ((DAT_0a39dd14 & 1) == 0) {
          uRam000000000a39dd08 = _UNK_088049f8;
          _DAT_0a39dd00 = _DAT_088049f0;
          DAT_0a39dd10 = (undefined4)DAT_085b0660;
          DAT_0a39dd14 = 1;
        }
        FUN_05e1d050(&local_388,4,ppppppuVar2,&DAT_0a39dce8,&DAT_0a39dd00,0x38,0,0);
        local_128 = (undefined1 *)0x0;
        if ((DAT_0a39df51 & 1) == 0) {
          uVar17 = 0;
          do {
            uVar22 = *(undefined4 *)((long)&DAT_08804e86 + uVar17);
            uVar4 = CONCAT12((char)((uint)uVar22 >> 8),(short)uVar22) & 0xff00ff;
            uVar23 = *(undefined4 *)((long)&DAT_08804e72 + uVar17 % 0x14);
            *(uint *)((long)&DAT_0a39df09 + uVar17) =
                 CONCAT13((char)((uint)uVar22 >> 0x18) + 0x8aU ^ (byte)((uint)uVar23 >> 0x18),
                          CONCAT12((char)((uint)uVar22 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar23 >> 0x10),
                                   CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar23 >> 8),
                                            (char)uVar4 + 0x8aU ^ (byte)uVar23)));
            uVar17 = uVar17 + 4;
          } while (uVar17 != 0x48);
          DAT_0a39df51 = 1;
        }
        lVar12 = 8;
        iVar6 = local_3f0._4_4_;
        do {
          lVar15 = lVar12;
          local_120[lVar15 + -8] = *(undefined1 *)((long)&DAT_0a39df09 + (long)(iVar6 % 10 + 0x23));
          lVar12 = lVar15 + 1;
          uVar1 = iVar6 + 9;
          iVar6 = iVar6 / 10;
        } while (0x12 < uVar1);
        if ((long)local_3f0 < 0) {
          local_120[lVar15 + -7] = 0x2d;
          lVar12 = lVar15 + 2;
        }
        local_120[lVar12 + -8] = 0;
        if (9 < lVar12) {
          puVar9 = local_120;
          puVar14 = &uStack_129 + lVar12;
          do {
            puVar9 = puVar9 + 1;
            uVar3 = *puVar14;
            puVar13 = puVar14 + -1;
            *puVar14 = puVar9[-1];
            puVar9[-1] = uVar3;
            puVar14 = puVar13;
          } while (puVar9 < puVar13);
        }
        local_128 = local_120;
        local_178 = pppppuStack_3e8;
        if (-1 < (long)puStack_3d8) {
          local_178 = ppppppuVar20;
        }
        local_170 = 0;
        lVar12 = *(long *)(local_3d0 + 8);
        if (lVar12 == 0) {
          lVar12 = *(long *)(DAT_0a520f60 + 8);
        }
        iVar6 = *(int *)(lVar12 + 0x10);
        local_1c8 = (undefined8 ******)0x0;
        lVar12 = 8;
        iVar18 = iVar6;
        do {
          lVar15 = lVar12;
          *(undefined1 *)((long)&local_1c8 + lVar15) =
               *(undefined1 *)((long)&DAT_0a39df09 + (long)(iVar18 % 10 + 0x23));
          lVar12 = lVar15 + 1;
          uVar1 = iVar18 + 9;
          iVar18 = iVar18 / 10;
        } while (0x12 < uVar1);
        if (iVar6 < 0) {
          *(undefined1 *)((long)&local_1c8 + lVar15 + 1) = 0x2d;
          lVar12 = lVar15 + 2;
        }
        *(undefined1 *)((long)&local_1c8 + lVar12) = 0;
        if (9 < lVar12) {
          puVar9 = &uStack_1c9 + lVar12;
          puVar14 = (undefined1 *)((long)&local_1c0 + 1);
          do {
            uVar3 = *puVar9;
            *puVar9 = puVar14[-1];
            puVar14[-1] = uVar3;
            bVar5 = puVar14 < puVar9 + -1;
            puVar9 = puVar9 + -1;
            puVar14 = puVar14 + 1;
          } while (bVar5);
        }
        local_1c8 = (undefined8 ******)&local_1c0;
        local_218 = (long *)0x0;
        lVar12 = 8;
        iVar6 = (int)local_3f0;
        do {
          lVar15 = lVar12;
          *(undefined1 *)((long)&local_218 + lVar15) =
               *(undefined1 *)((long)&DAT_0a39df09 + (long)(iVar6 % 10 + 0x23));
          lVar12 = lVar15 + 1;
          uVar1 = iVar6 + 9;
          iVar6 = iVar6 / 10;
        } while (0x12 < uVar1);
        if ((int)local_3f0 < 0) {
          *(undefined1 *)((long)&local_218 + lVar15 + 1) = 0x2d;
          lVar12 = lVar15 + 2;
        }
        *(undefined1 *)((long)&local_218 + lVar12) = 0;
        if (9 < lVar12) {
          puVar9 = (undefined1 *)((long)&local_220 + lVar12 + 7);
          puVar14 = (undefined1 *)((long)&local_210 + 1);
          do {
            uVar3 = *puVar9;
            *puVar9 = puVar14[-1];
            puVar14[-1] = uVar3;
            bVar5 = puVar14 < puVar9 + -1;
            puVar9 = puVar9 + -1;
            puVar14 = puVar14 + 1;
          } while (bVar5);
        }
        if ((DAT_0a39de07 & 1) == 0) {
          uVar17 = 0;
          do {
            uVar22 = *(undefined4 *)((long)&DAT_08804c69 + uVar17);
            uVar4 = CONCAT12((char)((uint)uVar22 >> 8),(short)uVar22) & 0xff00ff;
            uVar23 = *(undefined4 *)((long)&DAT_08804c55 + uVar17 % 0x14);
            *(uint *)((long)&DAT_0a39ddc0 + uVar17) =
                 CONCAT13((char)((uint)uVar22 >> 0x18) + 0x8aU ^ (byte)((uint)uVar23 >> 0x18),
                          CONCAT12((char)((uint)uVar22 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar23 >> 0x10),
                                   CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar23 >> 8),
                                            (char)uVar4 + 0x8aU ^ (byte)uVar23)));
            uVar17 = uVar17 + 4;
          } while (uVar17 != 0x44);
          DAT_0a39de04 = 0x5f25;
          DAT_0a39de06 = 0;
          DAT_0a39de07 = 1;
        }
        local_d8 = &local_128;
        local_d0 = &local_178;
        puStack_c8 = &local_1c8;
        puStack_c0 = &local_218;
        uStack_b0 = 0;
        local_b8 = 0;
        uStack_a0 = 0;
        uStack_a8 = 0;
        uStack_90 = 0;
        local_98 = 0;
        uStack_80 = 0;
        uStack_88 = 0;
        uStack_70 = 0;
        local_78 = 0;
        local_60 = 0;
        uStack_68 = 0;
        local_218 = &local_210;
        FUN_05e1d31c(&local_388,&DAT_0a39ddc0,&local_d8);
        thunk_FUN_05e1d0bc(&local_388);
        if (cStack_389 < '\0') {
          __ZdlPvm(local_3a0[0],CONCAT17(cStack_389,local_390) & 0x7fffffffffffffff);
        }
      }
      *(undefined8 *)*puVar19 = 0;
    }
    else {
      iVar6 = thunk_FUN_05e1d97c(2);
      if (iVar6 != 0) {
        FUN_0488143c(&local_178);
        ppppppuVar20 = (undefined8 ******)local_178;
        if (-1 < cStack_161) {
          ppppppuVar20 = &local_178;
        }
        if ((DAT_0a39dcf7 & 1) == 0) {
          DAT_0a39dce8._0_1_ = s_byp_hand_byp_08804940[0];
          DAT_0a39dce8._1_1_ = s_byp_hand_byp_08804940[1];
          DAT_0a39dce8._2_1_ = s_byp_hand_byp_08804940[2];
          DAT_0a39dce8._3_1_ = s_byp_hand_byp_08804940[3];
          DAT_0a39dce8._4_1_ = s_byp_hand_byp_08804940[4];
          DAT_0a39dce8._5_1_ = s_byp_hand_byp_08804940[5];
          DAT_0a39dce8._6_1_ = s_byp_hand_byp_08804940[6];
          DAT_0a39dce8._7_1_ = s_byp_hand_byp_08804940[7];
          DAT_0a39dcf0 = (undefined4)DAT_08549b60;
          DAT_0a39dcf4 = 0x6363;
          DAT_0a39dcf6 = 0;
          DAT_0a39dcf7 = 1;
        }
        if ((DAT_0a39dd14 & 1) == 0) {
          uRam000000000a39dd08 = _UNK_088049f8;
          _DAT_0a39dd00 = _DAT_088049f0;
          DAT_0a39dd10 = (undefined4)DAT_085b0660;
          DAT_0a39dd14 = 1;
        }
        FUN_05e1d050(&local_388,2,ppppppuVar20,&DAT_0a39dce8,&DAT_0a39dd00,0x34,0,0);
        local_128 = (undefined1 *)0x0;
        local_128 = local_120;
        if ((DAT_0a39df51 & 1) == 0) {
          uVar16 = 0;
          do {
            uVar22 = *(undefined4 *)((long)&DAT_08804e86 + uVar16);
            uVar4 = CONCAT12((char)((uint)uVar22 >> 8),(short)uVar22) & 0xff00ff;
            uVar23 = *(undefined4 *)((long)&DAT_08804e72 + uVar16 % 0x14);
            *(uint *)((long)&DAT_0a39df09 + uVar16) =
                 CONCAT13((char)((uint)uVar22 >> 0x18) + 0x8aU ^ (byte)((uint)uVar23 >> 0x18),
                          CONCAT12((char)((uint)uVar22 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar23 >> 0x10),
                                   CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar23 >> 8),
                                            (char)uVar4 + 0x8aU ^ (byte)uVar23)));
            uVar16 = uVar16 + 4;
          } while (uVar16 != 0x48);
          DAT_0a39df51 = 1;
        }
        lVar12 = 0;
        uVar16 = uVar17;
        do {
          lVar15 = lVar12;
          local_120[lVar15] = *(undefined1 *)(uVar16 % 10 + 0xa39df2c);
          bVar5 = 9 < uVar16;
          lVar12 = lVar15 + 1;
          uVar16 = uVar16 / 10;
        } while (bVar5);
        local_120[lVar15 + 1] = 0;
        if (8 < lVar15 + 8U) {
          puVar9 = local_120;
          puVar14 = local_120 + lVar15;
          do {
            puVar9 = puVar9 + 1;
            uVar3 = *puVar14;
            puVar13 = puVar14 + -1;
            *puVar14 = puVar9[-1];
            puVar9[-1] = uVar3;
            puVar14 = puVar13;
          } while (puVar9 < puVar13);
        }
        if ((DAT_0a39ddbf & 1) == 0) {
          _DAT_0a39dd9c = CONCAT44((int)ram0x08804948,(int)DAT_08546648);
          uRam000000000a39dda4 = CONCAT44((int)DAT_0860f288,(int)DAT_08804950);
          _DAT_0a39ddac = CONCAT44((int)DAT_08804960,(int)DAT_08489290);
          uRam000000000a39ddb4 = CONCAT44((int)DAT_084ec458,(int)DAT_08480a88);
          DAT_0a39ddbc = 0x5f25;
          DAT_0a39ddbe = 0;
          DAT_0a39ddbf = 1;
        }
        puStack_c8 = (undefined8 *)0x0;
        local_d0 = (undefined8 ******)0x0;
        local_d8 = &local_128;
        local_b8 = 0;
        puStack_c0 = (undefined8 *)0x0;
        uStack_a8 = 0;
        uStack_b0 = 0;
        local_98 = 0;
        uStack_a0 = 0;
        uStack_88 = 0;
        uStack_90 = 0;
        local_78 = 0;
        uStack_80 = 0;
        uStack_68 = 0;
        uStack_70 = 0;
        local_60 = 0;
        FUN_05e1d31c(&local_388,&DAT_0a39dd9c,&local_d8);
        thunk_FUN_05e1d0bc(&local_388);
        if (cStack_161 < '\0') {
          __ZdlPvm(local_178,CONCAT17(cStack_161,local_168) & 0x7fffffffffffffff);
        }
      }
      *(ulong *)*puVar19 = uVar17;
    }
  }
  uStack_2d8 = (ulong)uVar21;
  local_2d0 = *(undefined8 *)param_1[4];
  lStack_2c8 = (long)*(int *)((long)param_1 + 4);
  FUN_04af307c(&local_2f8,0);
  plVar7 = local_3c8;
  if (local_3c8 != (long *)0x0) {
    LOAcquire();
    lVar12 = local_3c8[1];
    local_3c8[1] = lVar12 + -1;
    LORelease();
    if (lVar12 == 0) {
      (**(code **)(*local_3c8 + 0x10))(local_3c8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
    }
  }
  if ((long)puStack_3d8 < 0) {
    __ZdlPvm(pppppuStack_3e8,(ulong)puStack_3d8 & 0x7fffffffffffffff);
  }
  if (iStack_254 < 0) {
    __ZdlPvm(uStack_268,CONCAT44(iStack_254,uStack_258) & 0x7fffffffffffffff);
  }
  if ((long)local_270 < 0) {
    __ZdlPvm(local_280,local_270 & 0x7fffffffffffffff);
  }
  if ((long)uStack_288 < 0) {
    __ZdlPvm(uStack_298,uStack_288 & 0x7fffffffffffffff);
  }
  FUN_0513bc40(&local_240);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


