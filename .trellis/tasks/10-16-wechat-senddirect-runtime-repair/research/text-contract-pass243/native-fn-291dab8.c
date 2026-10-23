// Ghidra inferred pseudocode; requested=0x291dab8
// entry=0291dab8 end=0291f943

/* WARNING: Removing unreachable block (ram,0x0291f568) */
/* WARNING: Removing unreachable block (ram,0x0291e124) */
/* WARNING: Removing unreachable block (ram,0x0291e56c) */
/* WARNING: Removing unreachable block (ram,0x0291ec1c) */
/* WARNING: Removing unreachable block (ram,0x0291e0c8) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0291dab8(undefined8 *param_1,undefined8 param_2,char *****param_3,undefined8 *param_4)

{
  char ***pppcVar1;
  char *****pppppcVar2;
  char cVar3;
  uint3 uVar4;
  char **ppcVar5;
  int iVar6;
  ulong uVar7;
  char *pcVar8;
  undefined8 uVar9;
  size_t sVar10;
  byte *pbVar11;
  undefined8 *****pppppuVar12;
  char ****ppppcVar13;
  char ****ppppcVar14;
  char ****ppppcVar15;
  undefined4 uVar16;
  undefined4 uVar17;
  undefined8 ****local_228 [2];
  undefined7 local_218;
  char cStack_211;
  char ****local_210;
  char ***local_208;
  char **local_200;
  undefined8 local_1f8;
  char ****local_1f0;
  char ***pppcStack_1e8;
  char **local_1e0;
  undefined1 *local_1d8;
  undefined1 *local_1d0;
  undefined8 ****ppppuStack_1c8;
  size_t sStack_1c0;
  ulong local_1b8;
  undefined1 *local_1b0;
  char ****local_160;
  char ***local_158;
  char **local_150;
  undefined8 local_148;
  char ***local_140;
  ulong uStack_138;
  ulong local_130;
  undefined1 *local_128;
  char ****ppppcStack_120;
  char ***local_118;
  char **ppcStack_110;
  undefined8 local_108;
  undefined1 *puStack_100;
  undefined8 ****local_f0;
  size_t sStack_e8;
  undefined8 local_e0;
  undefined8 uStack_d8;
  undefined8 local_d0;
  undefined8 uStack_c8;
  undefined8 uStack_c0;
  undefined8 uStack_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 uStack_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 uStack_80;
  undefined8 uStack_78;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  puStack_100 = &DAT_aaaaaaaaaaaaaa00;
  uStack_138 = 0;
  local_130 = 0;
  local_140 = (char ***)0x0;
  local_128 = &DAT_aaaaaaaa00000000;
  local_118 = (char ***)0x0;
  ppcStack_110 = (char **)0x0;
  ppppcStack_120 = (char ****)0x0;
  local_108 = 0xaaaaaa00aaaaaa00;
  if ((DAT_0a3a65c0 & 1) == 0) {
    if ((DAT_0a3a54e8 & 1) == 0) {
      DAT_0a3a54e0 = s_group_idmore_texchat_id_08585928._16_8_;
      DAT_0a3a54e8 = 1;
    }
    DAT_0a3a65b8 = &DAT_0a3a54e0;
    DAT_0a3a65c0 = 1;
  }
  local_158 = (char ***)0x0;
  local_150 = (char **)0x0;
  local_148 = 0x8000000000000000;
  cVar3 = *(char *)param_3;
  local_160 = (char ****)param_3;
  if (cVar3 == '\x01') {
    ppppcVar13 = param_3[1] + 1;
    ppppcVar15 = (char ****)*ppppcVar13;
    ppppcVar14 = ppppcVar13;
    if (ppppcVar15 != (char ****)0x0) {
      do {
        uVar7 = __ZNKSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE7compareEPKc
                          (ppppcVar15 + 4,DAT_0a3a65b8);
        if (-1 < (int)uVar7) {
          ppppcVar14 = ppppcVar15;
        }
        ppppcVar15 = *(char *****)((long)ppppcVar15 + (uVar7 >> 0x1c & 8));
      } while (ppppcVar15 != (char ****)0x0);
      if ((ppppcVar14 != ppppcVar13) &&
         (iVar6 = __ZNKSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE7compareEPKc
                            (ppppcVar14 + 4,DAT_0a3a65b8), iVar6 < 1)) {
        ppppcVar13 = ppppcVar14;
      }
    }
    cVar3 = *(char *)param_3;
    local_158 = (char ***)ppppcVar13;
LAB_0291dc1c:
    pppcStack_1e8 = (char ***)0x0;
    local_1e0 = (char **)0x0;
    local_1d8 = (undefined1 *)0x8000000000000000;
    if (cVar3 == '\x02') goto LAB_0291dc48;
    if (cVar3 == '\x01') {
      pppcStack_1e8 = (char ***)(param_3[1] + 1);
    }
    else {
      local_1d8 = (undefined1 *)0x1;
    }
  }
  else {
    if (cVar3 != '\x02') {
      local_148 = 1;
      goto LAB_0291dc1c;
    }
    local_150 = (char **)param_3[1][1];
LAB_0291dc48:
    local_1d8 = (undefined1 *)0x8000000000000000;
    pppcStack_1e8 = (char ***)0x0;
    local_1e0 = (char **)param_3[1][1];
  }
  local_1f0 = (char ****)param_3;
  uVar7 = FUN_00b19c98(&local_160,&local_1f0);
  if (((uVar7 & 1) == 0) && (pcVar8 = (char *)FUN_00b19b70(&local_160), *pcVar8 == '\x03')) {
    uVar9 = FUN_00b19b70(&local_160);
    local_1f0 = (char ****)0x0;
    pppcStack_1e8 = (char ***)0x0;
    local_1e0 = (char **)0x0;
    FUN_0074a99c(uVar9,&local_1f0);
    local_130 = (ulong)local_1e0;
    uStack_138 = (ulong)pppcStack_1e8;
    local_140 = (char ***)local_1f0;
    pppcVar1 = pppcStack_1e8;
    if (-1 < (long)local_1e0) {
      pppcVar1 = (char ***)((ulong)local_1e0 >> 0x38);
    }
    if (pppcVar1 == (char ***)0x0) {
      iVar6 = thunk_FUN_05e1d97c(3);
      if (iVar6 != 0) {
        FUN_0488143c(&local_210);
        pppppcVar2 = (char *****)local_210;
        if (-1 < (long)local_200) {
          pppppcVar2 = &local_210;
        }
        if ((DAT_0a3a556a & 1) == 0) {
          _DAT_0a3a5544 = CONCAT44((int)DAT_084a66c8,(int)DAT_08486a48);
          uRam000000000a3a554c = CONCAT44((int)DAT_084a66a8,(int)DAT_084a8ea0);
          _DAT_0a3a5554 = CONCAT44((int)DAT_08617fc8,(int)DAT_084a66b0);
          uRam000000000a3a555c = CONCAT44((int)DAT_084967c0,(int)DAT_08489770);
          DAT_0a3a5564 = (undefined4)DAT_084ccd80;
          DAT_0a3a5568 = 99;
          DAT_0a3a556a = 1;
        }
        if ((DAT_0a3a55c7 & 1) == 0) {
          DAT_0a3a55b8._0_1_ = s_Validatesolv_0874dd00[0];
          DAT_0a3a55b8._1_1_ = s_Validatesolv_0874dd00[1];
          DAT_0a3a55b8._2_1_ = s_Validatesolv_0874dd00[2];
          DAT_0a3a55b8._3_1_ = s_Validatesolv_0874dd00[3];
          DAT_0a3a55b8._4_1_ = s_Validatesolv_0874dd00[4];
          DAT_0a3a55b8._5_1_ = s_Validatesolv_0874dd00[5];
          DAT_0a3a55b8._6_1_ = s_Validatesolv_0874dd00[6];
          DAT_0a3a55b8._7_1_ = s_Validatesolv_0874dd00[7];
          DAT_0a3a55c0 = (undefined4)ram0x084f2cf0;
          DAT_0a3a55c4 = 0x736d;
          DAT_0a3a55c6 = 0;
          DAT_0a3a55c7 = 1;
        }
        FUN_05e1d050(&local_1f0,3,pppppcVar2,&DAT_0a3a5544,&DAT_0a3a55b8,0xd7,0,0);
        if ((DAT_0a3a5695 & 1) == 0) {
          uVar7 = 0;
          do {
            uVar16 = *(undefined4 *)((long)&DAT_08825c9d + uVar7);
            uVar4 = CONCAT12((char)((uint)uVar16 >> 8),(short)uVar16) & 0xff00ff;
            uVar17 = *(undefined4 *)((long)&DAT_08825c89 + uVar7 % 0x14);
            *(uint *)((long)&DAT_0a3a5652 + uVar7) =
                 CONCAT13((char)((uint)uVar16 >> 0x18) + 0x8aU ^ (byte)((uint)uVar17 >> 0x18),
                          CONCAT12((char)((uint)uVar16 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar17 >> 0x10),
                                   CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar17 >> 8),
                                            (char)uVar4 + 0x8aU ^ (byte)uVar17)));
            uVar7 = uVar7 + 4;
          } while (uVar7 != 0x40);
          DAT_0a3a5692 = 0x7974;
          DAT_0a3a5694 = 0;
          DAT_0a3a5695 = 1;
        }
        uStack_88 = 0;
        local_90 = 0;
        uStack_78 = 0;
        uStack_80 = 0;
        uStack_a8 = 0;
        local_b0 = 0;
        uStack_98 = 0;
        uStack_a0 = 0;
        uStack_c8 = 0;
        local_d0 = 0;
        uStack_b8 = 0;
        uStack_c0 = 0;
        sStack_e8 = 0;
        local_f0 = (undefined8 *****)0x0;
        uStack_d8 = 0;
        local_e0 = 0;
        FUN_05e1d31c(&local_1f0,&DAT_0a3a5652,&local_f0);
        thunk_FUN_05e1d0bc(&local_1f0);
        if ((long)local_200 < 0) {
          __ZdlPvm(local_210,(ulong)local_200 & 0x7fffffffffffffff);
        }
      }
      if ((DAT_0a3a56be & 1) == 0) {
        _DAT_0a3a5698 = CONCAT44((int)DAT_0870b770,(int)ram0x084f2cf0);
        uRam000000000a3a56a0 = CONCAT44((int)DAT_084a80a0,(int)DAT_0880e448);
        _DAT_0a3a56a8 = CONCAT44((int)DAT_087364e0,(int)DAT_08820bf0);
        uRam000000000a3a56b0 = CONCAT44((int)DAT_08518818,(int)DAT_08487d20);
        DAT_0a3a56b8 = (undefined4)DAT_0849d5c0;
        DAT_0a3a56bc = 0x79;
        DAT_0a3a56be = 1;
      }
      sVar10 = _strlen(&DAT_0a3a5698);
      if (0x7ffffffffffffff7 < sVar10) {
                    /* WARNING: Subroutine does not return */
        FUN_00018d9c(&local_f0);
      }
      if (sVar10 < 0x17) {
        local_e0 = CONCAT17((char)sVar10,(undefined7)local_e0);
        pppppuVar12 = &local_f0;
        if (sVar10 != 0) goto LAB_0291e504;
      }
      else {
        uVar7 = 0x19;
        if ((sVar10 | 7) != 0x17) {
          uVar7 = (sVar10 | 7) + 1;
        }
        pppppuVar12 = (undefined8 *****)__Znwm(uVar7);
        local_e0 = uVar7 | 0x8000000000000000;
        local_f0 = pppppuVar12;
        sStack_e8 = sVar10;
LAB_0291e504:
        _memcpy(pppppuVar12,&DAT_0a3a5698,sVar10);
      }
      *(undefined1 *)((long)pppppuVar12 + sVar10) = 0;
      pppcStack_1e8 = (char ***)&DAT_aaaaaaaaaaaaaa00;
      local_1e0 = (char **)&DAT_aaaaaaaaaaaaaa00;
      local_1d8 = &DAT_aaaaaaaaaaaaaa00;
      local_1d0 = &DAT_aaaaaaaaaaaaaa00;
      local_1f0 = (char ****)&DAT_aaaaaaaaaaaaaa00;
      sStack_1c0 = sStack_e8;
      ppppuStack_1c8 = local_f0;
      local_1b8 = local_e0;
      local_1b0 = &DAT_aaaaaaaaaaaaaa01;
      local_210 = (char ****)*param_4;
      *param_4 = 0;
      (*(code *)local_210[1])(local_210,&local_1f0);
      goto LAB_0291e0f4;
    }
    if ((DAT_0a3a65d0 & 1) == 0) {
      if ((DAT_0a3a54fd & 1) == 0) {
        DAT_0a3a54f0._0_1_ = s_message_sg_d_0866d0f8[0];
        DAT_0a3a54f0._1_1_ = s_message_sg_d_0866d0f8[1];
        DAT_0a3a54f0._2_1_ = s_message_sg_d_0866d0f8[2];
        DAT_0a3a54f0._3_1_ = s_message_sg_d_0866d0f8[3];
        DAT_0a3a54f0._4_1_ = s_message_sg_d_0866d0f8[4];
        DAT_0a3a54f0._5_1_ = s_message_sg_d_0866d0f8[5];
        DAT_0a3a54f0._6_1_ = s_message_sg_d_0866d0f8[6];
        DAT_0a3a54f0._7_1_ = s_message_sg_d_0866d0f8[7];
        DAT_0a3a54f8 = (undefined4)DAT_08489788;
        DAT_0a3a54fc = 0;
        DAT_0a3a54fd = 1;
      }
      DAT_0a3a65c8 = &DAT_0a3a54f0;
      DAT_0a3a65d0 = 1;
    }
    local_158 = (char ***)0x0;
    local_150 = (char **)0x0;
    local_148 = 0x8000000000000000;
    cVar3 = *(char *)param_3;
    if (cVar3 == '\x01') {
      ppppcVar13 = param_3[1] + 1;
      ppppcVar15 = (char ****)*ppppcVar13;
      ppppcVar14 = ppppcVar13;
      local_160 = (char ****)param_3;
      if (ppppcVar15 != (char ****)0x0) {
        do {
          uVar7 = __ZNKSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE7compareEPKc
                            (ppppcVar15 + 4,DAT_0a3a65c8);
          if (-1 < (int)uVar7) {
            ppppcVar14 = ppppcVar15;
          }
          ppppcVar15 = *(char *****)((long)ppppcVar15 + (uVar7 >> 0x1c & 8));
        } while (ppppcVar15 != (char ****)0x0);
        if ((ppppcVar14 != ppppcVar13) &&
           (iVar6 = __ZNKSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE7compareEPKc
                              (ppppcVar14 + 4,DAT_0a3a65c8), iVar6 < 1)) {
          ppppcVar13 = ppppcVar14;
        }
      }
      cVar3 = *(char *)param_3;
      local_158 = (char ***)ppppcVar13;
LAB_0291e4a0:
      pppcStack_1e8 = (char ***)0x0;
      local_1e0 = (char **)0x0;
      local_1d8 = (undefined1 *)0x8000000000000000;
      if (cVar3 == '\x02') goto LAB_0291e4cc;
      if (cVar3 == '\x01') {
        pppcStack_1e8 = (char ***)(param_3[1] + 1);
      }
      else {
        local_1d8 = (undefined1 *)0x1;
      }
    }
    else {
      if (cVar3 != '\x02') {
        local_148 = 1;
        local_160 = (char ****)param_3;
        goto LAB_0291e4a0;
      }
      local_150 = (char **)param_3[1][1];
      local_160 = (char ****)param_3;
LAB_0291e4cc:
      local_1d8 = (undefined1 *)0x8000000000000000;
      pppcStack_1e8 = (char ***)0x0;
      local_1e0 = (char **)param_3[1][1];
    }
    local_1f0 = (char ****)param_3;
    iVar6 = FUN_00b19c98(&local_160,&local_1f0);
    if (iVar6 != 0) {
      iVar6 = thunk_FUN_05e1d97c(3);
      if (iVar6 != 0) {
        FUN_0488143c(&local_210);
        pppppcVar2 = (char *****)local_210;
        if (-1 < (long)local_200) {
          pppppcVar2 = &local_210;
        }
        if ((DAT_0a3a556a & 1) == 0) {
          _DAT_0a3a5544 = CONCAT44((int)DAT_084a66c8,(int)DAT_08486a48);
          uRam000000000a3a554c = CONCAT44((int)DAT_084a66a8,(int)DAT_084a8ea0);
          _DAT_0a3a5554 = CONCAT44((int)DAT_08617fc8,(int)DAT_084a66b0);
          uRam000000000a3a555c = CONCAT44((int)DAT_084967c0,(int)DAT_08489770);
          DAT_0a3a5564 = (undefined4)DAT_084ccd80;
          DAT_0a3a5568 = 99;
          DAT_0a3a556a = 1;
        }
        if ((DAT_0a3a55c7 & 1) == 0) {
          DAT_0a3a55b8._0_1_ = s_Validatesolv_0874dd00[0];
          DAT_0a3a55b8._1_1_ = s_Validatesolv_0874dd00[1];
          DAT_0a3a55b8._2_1_ = s_Validatesolv_0874dd00[2];
          DAT_0a3a55b8._3_1_ = s_Validatesolv_0874dd00[3];
          DAT_0a3a55b8._4_1_ = s_Validatesolv_0874dd00[4];
          DAT_0a3a55b8._5_1_ = s_Validatesolv_0874dd00[5];
          DAT_0a3a55b8._6_1_ = s_Validatesolv_0874dd00[6];
          DAT_0a3a55b8._7_1_ = s_Validatesolv_0874dd00[7];
          DAT_0a3a55c0 = (undefined4)ram0x084f2cf0;
          DAT_0a3a55c4 = 0x736d;
          DAT_0a3a55c6 = 0;
          DAT_0a3a55c7 = 1;
        }
        FUN_05e1d050(&local_1f0,3,pppppcVar2,&DAT_0a3a5544,&DAT_0a3a55b8,0xe1,0,0);
        if ((DAT_0a3a5701 & 1) == 0) {
          uVar7 = 0;
          do {
            uVar16 = *(undefined4 *)((long)&DAT_08825d2e + uVar7);
            uVar4 = CONCAT12((char)((uint)uVar16 >> 8),(short)uVar16) & 0xff00ff;
            uVar17 = *(undefined4 *)((long)&DAT_08825d1a + uVar7 % 0x14);
            *(uint *)((long)&DAT_0a3a56bf + uVar7) =
                 CONCAT13((char)((uint)uVar16 >> 0x18) + 0x8aU ^ (byte)((uint)uVar17 >> 0x18),
                          CONCAT12((char)((uint)uVar16 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar17 >> 0x10),
                                   CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar17 >> 8),
                                            (char)uVar4 + 0x8aU ^ (byte)uVar17)));
            uVar7 = uVar7 + 4;
          } while (uVar7 != 0x40);
          DAT_0a3a56ff = 100;
          DAT_0a3a5701 = 1;
        }
        uStack_88 = 0;
        local_90 = 0;
        uStack_78 = 0;
        uStack_80 = 0;
        uStack_a8 = 0;
        local_b0 = 0;
        uStack_98 = 0;
        uStack_a0 = 0;
        uStack_c8 = 0;
        local_d0 = 0;
        uStack_b8 = 0;
        uStack_c0 = 0;
        sStack_e8 = 0;
        local_f0 = (undefined8 *****)0x0;
        uStack_d8 = 0;
        local_e0 = 0;
        FUN_05e1d31c(&local_1f0,&DAT_0a3a56bf,&local_f0);
        thunk_FUN_05e1d0bc(&local_1f0);
        if ((long)local_200 < 0) {
          __ZdlPvm(local_210,(ulong)local_200 & 0x7fffffffffffffff);
        }
      }
      if ((DAT_0a3a5729 & 1) == 0) {
        _DAT_0a3a5704 = CONCAT44((int)DAT_0870b770,(int)ram0x084f2cf0);
        uRam000000000a3a570c = CONCAT44((int)DAT_0848f630,(int)DAT_0880a0b0);
        _DAT_0a3a5714 = CONCAT44((int)DAT_08815a38,(int)DAT_08536f80);
        uRam000000000a3a571c = CONCAT44((int)DAT_08481210,(int)DAT_084cadd8);
        DAT_0a3a5724 = (undefined4)DAT_08575ae8;
        DAT_0a3a5728 = 0;
        DAT_0a3a5729 = 1;
      }
      sVar10 = _strlen(&DAT_0a3a5704);
      if (0x7ffffffffffffff7 < sVar10) {
                    /* WARNING: Subroutine does not return */
        FUN_00018d9c(&local_f0);
      }
      if (sVar10 < 0x17) {
        local_e0 = CONCAT17((char)sVar10,(undefined7)local_e0);
        pppppuVar12 = &local_f0;
        if (sVar10 != 0) goto LAB_0291ebb4;
      }
      else {
        uVar7 = 0x19;
        if ((sVar10 | 7) != 0x17) {
          uVar7 = (sVar10 | 7) + 1;
        }
        pppppuVar12 = (undefined8 *****)__Znwm(uVar7);
        local_e0 = uVar7 | 0x8000000000000000;
        local_f0 = pppppuVar12;
        sStack_e8 = sVar10;
LAB_0291ebb4:
        _memcpy(pppppuVar12,&DAT_0a3a5704,sVar10);
      }
      *(undefined1 *)((long)pppppuVar12 + sVar10) = 0;
      pppcStack_1e8 = (char ***)&DAT_aaaaaaaaaaaaaa00;
      local_1e0 = (char **)&DAT_aaaaaaaaaaaaaa00;
      local_1d8 = &DAT_aaaaaaaaaaaaaa00;
      local_1d0 = &DAT_aaaaaaaaaaaaaa00;
      local_1f0 = (char ****)&DAT_aaaaaaaaaaaaaa00;
      sStack_1c0 = sStack_e8;
      ppppuStack_1c8 = local_f0;
      local_1b8 = local_e0;
      local_1b0 = &DAT_aaaaaaaaaaaaaa01;
      local_210 = (char ****)*param_4;
      *param_4 = 0;
      (*(code *)local_210[1])(local_210,&local_1f0);
      goto LAB_0291e0f4;
    }
    pbVar11 = (byte *)FUN_00b19b70(&local_160);
    if (*pbVar11 - 5 < 2) {
      uVar9 = FUN_00b19b70(&local_160);
      local_1f0 = (char ****)((ulong)local_1f0 & 0xffffffff00000000);
      FUN_00bbfa44(uVar9,&local_1f0);
      local_128 = (undefined1 *)CONCAT44(local_128._4_4_,local_1f0._0_4_);
LAB_0291e894:
      if ((DAT_0a3a65e0 & 1) == 0) {
        if ((DAT_0a3a5513 & 1) == 0) {
          uRam000000000a3a5508 = _UNK_08824cb8;
          _DAT_0a3a5500 = _DAT_08824cb0;
          DAT_0a3a5510 = 0x3436;
          DAT_0a3a5512 = 0;
          DAT_0a3a5513 = 1;
        }
        DAT_0a3a65d8 = &DAT_0a3a5500;
        DAT_0a3a65e0 = 1;
      }
      local_158 = (char ***)0x0;
      local_150 = (char **)0x0;
      local_148 = 0x8000000000000000;
      if (*(char *)param_3 == '\x01') {
        ppppcVar13 = param_3[1] + 1;
        ppppcVar15 = (char ****)*ppppcVar13;
        ppppcVar14 = ppppcVar13;
        local_160 = (char ****)param_3;
        if (ppppcVar15 != (char ****)0x0) {
          do {
            uVar7 = __ZNKSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE7compareEPKc
                              (ppppcVar15 + 4,DAT_0a3a65d8);
            if (-1 < (int)uVar7) {
              ppppcVar14 = ppppcVar15;
            }
            ppppcVar15 = *(char *****)((long)ppppcVar15 + (uVar7 >> 0x1c & 8));
          } while (ppppcVar15 != (char ****)0x0);
          if ((ppppcVar14 != ppppcVar13) &&
             (iVar6 = __ZNKSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE7compareEPKc
                                (ppppcVar14 + 4,DAT_0a3a65d8), iVar6 < 1)) {
            ppppcVar13 = ppppcVar14;
          }
        }
      }
      else {
        ppppcVar13 = (char ****)local_158;
        if (*(char *)param_3 == '\x02') {
          local_150 = (char **)param_3[1][1];
          local_160 = (char ****)param_3;
        }
        else {
          local_148 = 1;
          local_160 = (char ****)param_3;
        }
      }
      local_158 = (char ***)ppppcVar13;
      if ((DAT_0a3a65f0 & 1) == 0) {
        if ((DAT_0a3a5524 & 1) == 0) {
          DAT_0a3a5518._0_1_ = s_content_refer_icon__084f26e0[0];
          DAT_0a3a5518._1_1_ = s_content_refer_icon__084f26e0[1];
          DAT_0a3a5518._2_1_ = s_content_refer_icon__084f26e0[2];
          DAT_0a3a5518._3_1_ = s_content_refer_icon__084f26e0[3];
          DAT_0a3a5518._4_1_ = s_content_refer_icon__084f26e0[4];
          DAT_0a3a5518._5_1_ = s_content_refer_icon__084f26e0[5];
          DAT_0a3a5518._6_1_ = s_content_refer_icon__084f26e0[6];
          DAT_0a3a5518._7_1_ = s_content_refer_icon__084f26e0[7];
          DAT_0a3a5520 = (undefined4)DAT_08572320;
          DAT_0a3a5524 = 1;
        }
        DAT_0a3a65e8 = &DAT_0a3a5518;
        DAT_0a3a65f0 = 1;
      }
      local_208 = (char ***)0x0;
      local_200 = (char **)0x0;
      local_1f8 = 0x8000000000000000;
      cVar3 = *(char *)param_3;
      local_210 = (char ****)param_3;
      if (cVar3 == '\x01') {
        ppppcVar13 = param_3[1] + 1;
        ppppcVar15 = (char ****)*ppppcVar13;
        ppppcVar14 = ppppcVar13;
        if (ppppcVar15 != (char ****)0x0) {
          do {
            uVar7 = __ZNKSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE7compareEPKc
                              (ppppcVar15 + 4,DAT_0a3a65e8);
            if (-1 < (int)uVar7) {
              ppppcVar14 = ppppcVar15;
            }
            ppppcVar15 = *(char *****)((long)ppppcVar15 + (uVar7 >> 0x1c & 8));
          } while (ppppcVar15 != (char ****)0x0);
          if ((ppppcVar14 != ppppcVar13) &&
             (iVar6 = __ZNKSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE7compareEPKc
                                (ppppcVar14 + 4,DAT_0a3a65e8), iVar6 < 1)) {
            ppppcVar13 = ppppcVar14;
          }
        }
        cVar3 = *(char *)param_3;
        local_208 = (char ***)ppppcVar13;
LAB_0291f054:
        pppcStack_1e8 = (char ***)0x0;
        local_1e0 = (char **)0x0;
        local_1d8 = (undefined1 *)0x8000000000000000;
        if (cVar3 == '\x02') goto LAB_0291f080;
        if (cVar3 == '\x01') {
          pppcStack_1e8 = (char ***)(param_3[1] + 1);
        }
        else {
          local_1d8 = (undefined1 *)0x1;
        }
      }
      else {
        if (cVar3 != '\x02') {
          local_1f8 = 1;
          goto LAB_0291f054;
        }
        local_200 = (char **)param_3[1][1];
LAB_0291f080:
        local_1d8 = (undefined1 *)0x8000000000000000;
        pppcStack_1e8 = (char ***)0x0;
        local_1e0 = (char **)param_3[1][1];
      }
      local_1f0 = (char ****)param_3;
      uVar7 = FUN_00b19c98(&local_160,&local_1f0);
      if (((uVar7 & 1) == 0) && (pcVar8 = (char *)FUN_00b19b70(&local_160), *pcVar8 == '\x03')) {
        FUN_00b19b70(&local_160);
        FUN_00bc3698(&local_f0);
        sVar10 = sStack_e8;
        if (-1 < (long)local_e0) {
          sVar10 = (long)local_e0._7_1_;
        }
        if ((long)local_e0._7_1_ < 0) {
          __ZdlPvm(local_f0,local_e0 & 0x7fffffffffffffff);
        }
        if (sVar10 == 0) goto LAB_0291f138;
        uVar9 = FUN_00b19b70(&local_160);
        local_1f0 = (char ****)0x0;
        pppcStack_1e8 = (char ***)0x0;
        local_1e0 = (char **)0x0;
        FUN_0074a99c(uVar9,&local_1f0);
        if ((long)ppcStack_110 < 0) {
          __ZdlPvm(ppppcStack_120,(ulong)ppcStack_110 & 0x7fffffffffffffff);
        }
LAB_0291f21c:
        if ((DAT_0a3a6600 & 1) == 0) {
          if ((DAT_0a3a5540 & 1) == 0) {
            uRam000000000a3a5538._0_1_ = s_my_group_nicknammessage_subtype_088053a0[0x18];
            uRam000000000a3a5538._1_1_ = s_my_group_nicknammessage_subtype_088053a0[0x19];
            uRam000000000a3a5538._2_1_ = s_my_group_nicknammessage_subtype_088053a0[0x1a];
            uRam000000000a3a5538._3_1_ = s_my_group_nicknammessage_subtype_088053a0[0x1b];
            uRam000000000a3a5538._4_1_ = s_my_group_nicknammessage_subtype_088053a0[0x1c];
            uRam000000000a3a5538._5_1_ = s_my_group_nicknammessage_subtype_088053a0[0x1d];
            uRam000000000a3a5538._6_1_ = s_my_group_nicknammessage_subtype_088053a0[0x1e];
            uRam000000000a3a5538._7_1_ = s_my_group_nicknammessage_subtype_088053a0[0x1f];
            DAT_0a3a5530 = s_my_group_nicknammessage_subtype_088053a0[0x10];
            DAT_0a3a5530_1._0_1_ = s_my_group_nicknammessage_subtype_088053a0[0x11];
            DAT_0a3a5530_1._1_1_ = s_my_group_nicknammessage_subtype_088053a0[0x12];
            DAT_0a3a5530_1._2_1_ = s_my_group_nicknammessage_subtype_088053a0[0x13];
            DAT_0a3a5530_1._3_1_ = s_my_group_nicknammessage_subtype_088053a0[0x14];
            DAT_0a3a5530_1._4_1_ = s_my_group_nicknammessage_subtype_088053a0[0x15];
            DAT_0a3a5530_1._5_1_ = s_my_group_nicknammessage_subtype_088053a0[0x16];
            DAT_0a3a5530_1._6_1_ = s_my_group_nicknammessage_subtype_088053a0[0x17];
            DAT_0a3a5540 = 1;
          }
          DAT_0a3a65f8 = &DAT_0a3a5530;
          DAT_0a3a6600 = 1;
        }
        local_158 = (char ***)0x0;
        local_150 = (char **)0x0;
        local_148 = 0x8000000000000000;
        cVar3 = *(char *)param_3;
        ppppcStack_120 = local_1f0;
        local_118 = pppcStack_1e8;
        ppcStack_110 = local_1e0;
        if (cVar3 == '\x01') {
          ppppcVar13 = param_3[1] + 1;
          ppppcVar15 = (char ****)*ppppcVar13;
          ppppcVar14 = ppppcVar13;
          local_160 = (char ****)param_3;
          if (ppppcVar15 != (char ****)0x0) {
            do {
              uVar7 = __ZNKSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE7compareEPKc
                                (ppppcVar15 + 4,DAT_0a3a65f8);
              if (-1 < (int)uVar7) {
                ppppcVar14 = ppppcVar15;
              }
              ppppcVar15 = *(char *****)((long)ppppcVar15 + (uVar7 >> 0x1c & 8));
            } while (ppppcVar15 != (char ****)0x0);
            if ((ppppcVar14 != ppppcVar13) &&
               (iVar6 = __ZNKSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE7compareEPKc
                                  (ppppcVar14 + 4,DAT_0a3a65f8), iVar6 < 1)) {
              ppppcVar13 = ppppcVar14;
            }
          }
          cVar3 = *(char *)param_3;
          local_158 = (char ***)ppppcVar13;
LAB_0291f5d4:
          pppcStack_1e8 = (char ***)0x0;
          local_1e0 = (char **)0x0;
          local_1d8 = (undefined1 *)0x8000000000000000;
          if (cVar3 == '\x02') goto LAB_0291f600;
          if (cVar3 == '\x01') {
            pppcStack_1e8 = (char ***)(param_3[1] + 1);
          }
          else {
            local_1d8 = (undefined1 *)0x1;
          }
        }
        else {
          if (cVar3 != '\x02') {
            local_148 = 1;
            local_160 = (char ****)param_3;
            goto LAB_0291f5d4;
          }
          local_150 = (char **)param_3[1][1];
          local_160 = (char ****)param_3;
LAB_0291f600:
          local_1d8 = (undefined1 *)0x8000000000000000;
          pppcStack_1e8 = (char ***)0x0;
          local_1e0 = (char **)param_3[1][1];
        }
        local_1f0 = (char ****)param_3;
        uVar7 = FUN_00b19c98(&local_160,&local_1f0);
        if ((uVar7 & 1) == 0) {
          pbVar11 = (byte *)FUN_00b19b70(&local_160);
          if (*pbVar11 - 5 < 2) {
            uVar9 = FUN_00b19b70(&local_160);
            local_1f0 = (char ****)((ulong)local_1f0 & 0xffffffff00000000);
            FUN_00bbfa44(uVar9,&local_1f0);
            local_108._0_5_ = CONCAT14(1,local_1f0._0_4_);
          }
          else {
            pcVar8 = (char *)FUN_00b19b70(&local_160);
            if (*pcVar8 == '\x03') {
              FUN_00b19b70(&local_160);
              FUN_00bc3698(&local_1f0);
              uVar16 = FUN_04b567f0(&local_1f0,0);
              local_108._0_5_ = CONCAT14(1,uVar16);
              if ((long)local_1e0 < 0) {
                __ZdlPvm(local_1f0,(ulong)local_1e0 & 0x7fffffffffffffff);
              }
              iVar6 = thunk_FUN_05e1d97c(3);
              if (iVar6 != 0) {
                FUN_0488143c(&local_210);
                pppppcVar2 = (char *****)local_210;
                if (-1 < (long)local_200) {
                  pppppcVar2 = &local_210;
                }
                if ((DAT_0a3a556a & 1) == 0) {
                  _DAT_0a3a5544 = CONCAT44((int)DAT_084a66c8,(int)DAT_08486a48);
                  uRam000000000a3a554c = CONCAT44((int)DAT_084a66a8,(int)DAT_084a8ea0);
                  _DAT_0a3a5554 = CONCAT44((int)DAT_08617fc8,(int)DAT_084a66b0);
                  uRam000000000a3a555c = CONCAT44((int)DAT_084967c0,(int)DAT_08489770);
                  DAT_0a3a5564 = (undefined4)DAT_084ccd80;
                  DAT_0a3a5568 = 99;
                  DAT_0a3a556a = 1;
                }
                if ((DAT_0a3a55c7 & 1) == 0) {
                  DAT_0a3a55b8._0_1_ = s_Validatesolv_0874dd00[0];
                  DAT_0a3a55b8._1_1_ = s_Validatesolv_0874dd00[1];
                  DAT_0a3a55b8._2_1_ = s_Validatesolv_0874dd00[2];
                  DAT_0a3a55b8._3_1_ = s_Validatesolv_0874dd00[3];
                  DAT_0a3a55b8._4_1_ = s_Validatesolv_0874dd00[4];
                  DAT_0a3a55b8._5_1_ = s_Validatesolv_0874dd00[5];
                  DAT_0a3a55b8._6_1_ = s_Validatesolv_0874dd00[6];
                  DAT_0a3a55b8._7_1_ = s_Validatesolv_0874dd00[7];
                  DAT_0a3a55c0 = (undefined4)ram0x084f2cf0;
                  DAT_0a3a55c4 = 0x736d;
                  DAT_0a3a55c6 = 0;
                  DAT_0a3a55c7 = 1;
                }
                FUN_05e1d050(&local_1f0,3,pppppcVar2,&DAT_0a3a5544,&DAT_0a3a55b8,0x10d,0,0);
                if ((DAT_0a3a58bd & 1) == 0) {
                  uVar7 = 0;
                  do {
                    uVar16 = *(undefined4 *)((long)&DAT_08825f71 + uVar7);
                    uVar4 = CONCAT12((char)((uint)uVar16 >> 8),(short)uVar16) & 0xff00ff;
                    uVar17 = *(undefined4 *)((long)&DAT_08825f5d + uVar7 % 0x14);
                    *(uint *)((long)&DAT_0a3a5884 + uVar7) =
                         CONCAT13((char)((uint)uVar16 >> 0x18) + 0x8aU ^
                                  (byte)((uint)uVar17 >> 0x18),
                                  CONCAT12((char)((uint)uVar16 >> 0x10) + 0x8aU ^
                                           (byte)((uint)uVar17 >> 0x10),
                                           CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^
                                                    (byte)((uint)uVar17 >> 8),
                                                    (char)uVar4 + 0x8aU ^ (byte)uVar17)));
                    uVar7 = uVar7 + 4;
                  } while (uVar7 != 0x38);
                  DAT_0a3a58bc = 0;
                  DAT_0a3a58bd = 1;
                }
                uStack_88 = 0;
                local_90 = 0;
                uStack_78 = 0;
                uStack_80 = 0;
                uStack_a8 = 0;
                local_b0 = 0;
                uStack_98 = 0;
                uStack_a0 = 0;
                uStack_c8 = 0;
                local_d0 = 0;
                uStack_b8 = 0;
                uStack_c0 = 0;
                sStack_e8 = 0;
                local_f0 = (undefined8 *****)0x0;
                uStack_d8 = 0;
                local_e0 = 0;
                FUN_05e1d31c(&local_1f0,&DAT_0a3a5884,&local_f0);
                thunk_FUN_05e1d0bc(&local_1f0);
                if ((long)local_200 < 0) {
                  __ZdlPvm(local_210,(ulong)local_200 & 0x7fffffffffffffff);
                }
              }
            }
          }
        }
        ppcVar5 = ppcStack_110;
        param_1[1] = uStack_138;
        *param_1 = local_140;
        param_1[2] = local_130;
        local_140 = (char ***)0x0;
        uStack_138 = 0;
        local_130 = 0;
        *(undefined4 *)(param_1 + 3) = local_128._0_4_;
        param_1[5] = local_118;
        param_1[4] = ppppcStack_120;
        ppppcStack_120 = (char ****)0x0;
        local_118 = (char ***)0x0;
        ppcStack_110 = (char **)0x0;
        *(undefined1 *)(param_1 + 8) = puStack_100._0_1_;
        param_1[6] = ppcVar5;
        param_1[7] = local_108;
        *(undefined1 *)(param_1 + 9) = 1;
        goto joined_r0x0291f908;
      }
LAB_0291f138:
      pppcStack_1e8 = (char ***)0x0;
      local_1e0 = (char **)0x0;
      local_1d8 = (undefined1 *)0x8000000000000000;
      if (*(char *)param_3 == '\x02') {
        local_1e0 = (char **)param_3[1][1];
      }
      else if (*(char *)param_3 == '\x01') {
        pppcStack_1e8 = (char ***)(param_3[1] + 1);
      }
      else {
        local_1d8 = (undefined1 *)0x1;
      }
      local_1f0 = (char ****)param_3;
      uVar7 = FUN_00b19c98(&local_210,&local_1f0);
      if (((uVar7 & 1) == 0) && (pcVar8 = (char *)FUN_00b19b70(&local_210), *pcVar8 == '\x03')) {
        FUN_00b19b70(&local_210);
        FUN_00bc3698(&local_f0);
        sVar10 = sStack_e8;
        if (-1 < (long)local_e0) {
          sVar10 = (long)local_e0._7_1_;
        }
        if ((long)local_e0._7_1_ < 0) {
          __ZdlPvm(local_f0,local_e0 & 0x7fffffffffffffff);
        }
        if (sVar10 != 0) {
          FUN_00b19b70(&local_210);
          FUN_00bc3698(&local_1f0);
          if ((long)ppcStack_110 < 0) {
            __ZdlPvm(ppppcStack_120,(ulong)ppcStack_110 & 0x7fffffffffffffff);
          }
          puStack_100 = (undefined1 *)CONCAT71(puStack_100._1_7_,1);
          goto LAB_0291f21c;
        }
      }
      iVar6 = thunk_FUN_05e1d97c(3);
      if (iVar6 != 0) {
        FUN_0488143c(local_228);
        pppppuVar12 = (undefined8 *****)local_228[0];
        if (-1 < cStack_211) {
          pppppuVar12 = local_228;
        }
        if ((DAT_0a3a556a & 1) == 0) {
          _DAT_0a3a5544 = CONCAT44((int)DAT_084a66c8,(int)DAT_08486a48);
          uRam000000000a3a554c = CONCAT44((int)DAT_084a66a8,(int)DAT_084a8ea0);
          _DAT_0a3a5554 = CONCAT44((int)DAT_08617fc8,(int)DAT_084a66b0);
          uRam000000000a3a555c = CONCAT44((int)DAT_084967c0,(int)DAT_08489770);
          DAT_0a3a5564 = (undefined4)DAT_084ccd80;
          DAT_0a3a5568 = 99;
          DAT_0a3a556a = 1;
        }
        if ((DAT_0a3a55c7 & 1) == 0) {
          DAT_0a3a55b8._0_1_ = s_Validatesolv_0874dd00[0];
          DAT_0a3a55b8._1_1_ = s_Validatesolv_0874dd00[1];
          DAT_0a3a55b8._2_1_ = s_Validatesolv_0874dd00[2];
          DAT_0a3a55b8._3_1_ = s_Validatesolv_0874dd00[3];
          DAT_0a3a55b8._4_1_ = s_Validatesolv_0874dd00[4];
          DAT_0a3a55b8._5_1_ = s_Validatesolv_0874dd00[5];
          DAT_0a3a55b8._6_1_ = s_Validatesolv_0874dd00[6];
          DAT_0a3a55b8._7_1_ = s_Validatesolv_0874dd00[7];
          DAT_0a3a55c0 = (undefined4)ram0x084f2cf0;
          DAT_0a3a55c4 = 0x736d;
          DAT_0a3a55c6 = 0;
          DAT_0a3a55c7 = 1;
        }
        FUN_05e1d050(&local_1f0,3,pppppuVar12,&DAT_0a3a5544,&DAT_0a3a55b8,0xff,0,0);
        if ((DAT_0a3a5833 & 1) == 0) {
          uVar7 = 0;
          do {
            uVar16 = *(undefined4 *)((long)&DAT_08825ea4 + uVar7);
            uVar4 = CONCAT12((char)((uint)uVar16 >> 8),(short)uVar16) & 0xff00ff;
            uVar17 = *(undefined4 *)((long)&DAT_08825e90 + uVar7 % 0x14);
            *(uint *)((long)&DAT_0a3a57dd + uVar7) =
                 CONCAT13((char)((uint)uVar16 >> 0x18) + 0x8aU ^ (byte)((uint)uVar17 >> 0x18),
                          CONCAT12((char)((uint)uVar16 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar17 >> 0x10),
                                   CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar17 >> 8),
                                            (char)uVar4 + 0x8aU ^ (byte)uVar17)));
            uVar7 = uVar7 + 4;
          } while (uVar7 != 0x54);
          DAT_0a3a5831 = 100;
          DAT_0a3a5833 = 1;
        }
        uStack_88 = 0;
        local_90 = 0;
        uStack_78 = 0;
        uStack_80 = 0;
        uStack_a8 = 0;
        local_b0 = 0;
        uStack_98 = 0;
        uStack_a0 = 0;
        uStack_c8 = 0;
        local_d0 = 0;
        uStack_b8 = 0;
        uStack_c0 = 0;
        sStack_e8 = 0;
        local_f0 = (undefined8 *****)0x0;
        uStack_d8 = 0;
        local_e0 = 0;
        FUN_05e1d31c(&local_1f0,&DAT_0a3a57dd,&local_f0);
        thunk_FUN_05e1d0bc(&local_1f0);
        if (cStack_211 < '\0') {
          __ZdlPvm(local_228[0],CONCAT17(cStack_211,local_218) & 0x7fffffffffffffff);
        }
      }
      if ((DAT_0a3a5883 & 1) == 0) {
        uVar7 = 0;
        do {
          uVar16 = *(undefined4 *)((long)&DAT_08825f0e + uVar7);
          uVar4 = CONCAT12((char)((uint)uVar16 >> 8),(short)uVar16) & 0xff00ff;
          uVar17 = *(undefined4 *)((long)&DAT_08825efa + uVar7 % 0x14);
          *(uint *)((long)&DAT_0a3a5834 + uVar7) =
               CONCAT13((char)((uint)uVar16 >> 0x18) + 0x8aU ^ (byte)((uint)uVar17 >> 0x18),
                        CONCAT12((char)((uint)uVar16 >> 0x10) + 0x8aU ^ (byte)((uint)uVar17 >> 0x10)
                                 ,CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^ (byte)((uint)uVar17 >> 8)
                                           ,(char)uVar4 + 0x8aU ^ (byte)uVar17)));
          uVar7 = uVar7 + 4;
        } while (uVar7 != 0x4c);
        DAT_0a3a5880 = 0x7974;
        DAT_0a3a5882 = 0;
        DAT_0a3a5883 = 1;
      }
      FUN_00255b9c(&local_f0,&DAT_0a3a5834);
      FUN_02921ee8(&local_1f0);
      FUN_02921e94(param_4,&local_1f0);
    }
    else {
      pcVar8 = (char *)FUN_00b19b70(&local_160);
      if (*pcVar8 == '\x03') {
        FUN_00b19b70(&local_160);
        FUN_00bc3698(&local_1f0);
        uVar16 = FUN_04b567f0(&local_1f0,0);
        local_128 = (undefined1 *)CONCAT44(local_128._4_4_,uVar16);
        if ((long)local_1e0 < 0) {
          __ZdlPvm(local_1f0,(ulong)local_1e0 & 0x7fffffffffffffff);
        }
        iVar6 = thunk_FUN_05e1d97c(3);
        if (iVar6 != 0) {
          FUN_0488143c(&local_210);
          pppppcVar2 = (char *****)local_210;
          if (-1 < (long)local_200) {
            pppppcVar2 = &local_210;
          }
          if ((DAT_0a3a556a & 1) == 0) {
            _DAT_0a3a5544 = CONCAT44((int)DAT_084a66c8,(int)DAT_08486a48);
            uRam000000000a3a554c = CONCAT44((int)DAT_084a66a8,(int)DAT_084a8ea0);
            _DAT_0a3a5554 = CONCAT44((int)DAT_08617fc8,(int)DAT_084a66b0);
            uRam000000000a3a555c = CONCAT44((int)DAT_084967c0,(int)DAT_08489770);
            DAT_0a3a5564 = (undefined4)DAT_084ccd80;
            DAT_0a3a5568 = 99;
            DAT_0a3a556a = 1;
          }
          if ((DAT_0a3a55c7 & 1) == 0) {
            DAT_0a3a55b8._0_1_ = s_Validatesolv_0874dd00[0];
            DAT_0a3a55b8._1_1_ = s_Validatesolv_0874dd00[1];
            DAT_0a3a55b8._2_1_ = s_Validatesolv_0874dd00[2];
            DAT_0a3a55b8._3_1_ = s_Validatesolv_0874dd00[3];
            DAT_0a3a55b8._4_1_ = s_Validatesolv_0874dd00[4];
            DAT_0a3a55b8._5_1_ = s_Validatesolv_0874dd00[5];
            DAT_0a3a55b8._6_1_ = s_Validatesolv_0874dd00[6];
            DAT_0a3a55b8._7_1_ = s_Validatesolv_0874dd00[7];
            DAT_0a3a55c0 = (undefined4)ram0x084f2cf0;
            DAT_0a3a55c4 = 0x736d;
            DAT_0a3a55c6 = 0;
            DAT_0a3a55c7 = 1;
          }
          FUN_05e1d050(&local_1f0,3,pppppcVar2,&DAT_0a3a5544,&DAT_0a3a55b8,0xe9,0,0);
          if ((DAT_0a3a5762 & 1) == 0) {
            _DAT_0a3a572c = CONCAT44((int)DAT_0870b770,(int)ram0x084f2cf0);
            uRam000000000a3a5734 = CONCAT44((int)DAT_0848f630,(int)DAT_0880a0b0);
            _DAT_0a3a573c = CONCAT44((int)DAT_08815a38,(int)DAT_08536f80);
            uRam000000000a3a5744 = CONCAT44((int)DAT_08823700,(int)DAT_085d7518);
            _DAT_0a3a574c = CONCAT44((int)DAT_0856a018,(int)DAT_084cd9d0);
            uRam000000000a3a5754 = CONCAT44((int)DAT_085a0d20,(int)DAT_084c9d78);
            DAT_0a3a575c = (undefined4)ram0x085321b8;
            DAT_0a3a5760 = 0x67;
            DAT_0a3a5762 = 1;
          }
          uStack_88 = 0;
          local_90 = 0;
          uStack_78 = 0;
          uStack_80 = 0;
          uStack_a8 = 0;
          local_b0 = 0;
          uStack_98 = 0;
          uStack_a0 = 0;
          uStack_c8 = 0;
          local_d0 = 0;
          uStack_b8 = 0;
          uStack_c0 = 0;
          sStack_e8 = 0;
          local_f0 = (undefined8 *****)0x0;
          uStack_d8 = 0;
          local_e0 = 0;
          FUN_05e1d31c(&local_1f0,&DAT_0a3a572c,&local_f0);
          thunk_FUN_05e1d0bc(&local_1f0);
          if ((long)local_200 < 0) {
            __ZdlPvm(local_210,(ulong)local_200 & 0x7fffffffffffffff);
          }
        }
        goto LAB_0291e894;
      }
      iVar6 = thunk_FUN_05e1d97c(3);
      if (iVar6 != 0) {
        FUN_0488143c(&local_210);
        pppppcVar2 = (char *****)local_210;
        if (-1 < (long)local_200) {
          pppppcVar2 = &local_210;
        }
        if ((DAT_0a3a556a & 1) == 0) {
          _DAT_0a3a5544 = CONCAT44((int)DAT_084a66c8,(int)DAT_08486a48);
          uRam000000000a3a554c = CONCAT44((int)DAT_084a66a8,(int)DAT_084a8ea0);
          _DAT_0a3a5554 = CONCAT44((int)DAT_08617fc8,(int)DAT_084a66b0);
          uRam000000000a3a555c = CONCAT44((int)DAT_084967c0,(int)DAT_08489770);
          DAT_0a3a5564 = (undefined4)DAT_084ccd80;
          DAT_0a3a5568 = 99;
          DAT_0a3a556a = 1;
        }
        if ((DAT_0a3a55c7 & 1) == 0) {
          DAT_0a3a55b8._0_1_ = s_Validatesolv_0874dd00[0];
          DAT_0a3a55b8._1_1_ = s_Validatesolv_0874dd00[1];
          DAT_0a3a55b8._2_1_ = s_Validatesolv_0874dd00[2];
          DAT_0a3a55b8._3_1_ = s_Validatesolv_0874dd00[3];
          DAT_0a3a55b8._4_1_ = s_Validatesolv_0874dd00[4];
          DAT_0a3a55b8._5_1_ = s_Validatesolv_0874dd00[5];
          DAT_0a3a55b8._6_1_ = s_Validatesolv_0874dd00[6];
          DAT_0a3a55b8._7_1_ = s_Validatesolv_0874dd00[7];
          DAT_0a3a55c0 = (undefined4)ram0x084f2cf0;
          DAT_0a3a55c4 = 0x736d;
          DAT_0a3a55c6 = 0;
          DAT_0a3a55c7 = 1;
        }
        FUN_05e1d050(&local_1f0,3,pppppcVar2,&DAT_0a3a5544,&DAT_0a3a55b8,0xeb,0,0);
        if ((DAT_0a3a57ac & 1) == 0) {
          uVar7 = 0;
          do {
            uVar16 = *(undefined4 *)((long)&DAT_08825e07 + uVar7);
            uVar4 = CONCAT12((char)((uint)uVar16 >> 8),(short)uVar16) & 0xff00ff;
            uVar17 = *(undefined4 *)((long)&DAT_08825df3 + uVar7 % 0x14);
            *(uint *)((long)&DAT_0a3a5763 + uVar7) =
                 CONCAT13((char)((uint)uVar16 >> 0x18) + 0x8aU ^ (byte)((uint)uVar17 >> 0x18),
                          CONCAT12((char)((uint)uVar16 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar17 >> 0x10),
                                   CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar17 >> 8),
                                            (char)uVar4 + 0x8aU ^ (byte)uVar17)));
            uVar7 = uVar7 + 4;
          } while (uVar7 != 0x48);
          DAT_0a3a57ab = 0;
          DAT_0a3a57ac = 1;
        }
        uStack_88 = 0;
        local_90 = 0;
        uStack_78 = 0;
        uStack_80 = 0;
        uStack_a8 = 0;
        local_b0 = 0;
        uStack_98 = 0;
        uStack_a0 = 0;
        uStack_c8 = 0;
        local_d0 = 0;
        uStack_b8 = 0;
        uStack_c0 = 0;
        sStack_e8 = 0;
        local_f0 = (undefined8 *****)0x0;
        uStack_d8 = 0;
        local_e0 = 0;
        FUN_05e1d31c(&local_1f0,&DAT_0a3a5763,&local_f0);
        thunk_FUN_05e1d0bc(&local_1f0);
        if ((long)local_200 < 0) {
          __ZdlPvm(local_210,(ulong)local_200 & 0x7fffffffffffffff);
        }
      }
      if ((DAT_0a3a57dc & 1) == 0) {
        _DAT_0a3a57b0 = CONCAT44((int)DAT_0870b770,(int)ram0x084f2cf0);
        uRam000000000a3a57b8 = CONCAT44((int)DAT_0848f630,(int)DAT_0880a0b0);
        _DAT_0a3a57c0 = CONCAT44((int)DAT_08815a38,(int)DAT_08536f80);
        uRam000000000a3a57c8 = CONCAT44((int)DAT_08532070,(int)DAT_08532068);
        DAT_0a3a57d0 = CONCAT44((int)DAT_084d8370,(int)DAT_087d2180);
        DAT_0a3a57d8 = (undefined4)ram0x0873a920;
        DAT_0a3a57dc = 1;
      }
      FUN_00255b9c(&local_f0,&DAT_0a3a57b0);
      FUN_02921ee8(&local_1f0);
      FUN_02921e94(param_4,&local_1f0);
    }
    if (((char)local_1b0 == '\x01') && ((long)local_1b8 < 0)) {
      __ZdlPvm(ppppuStack_1c8,local_1b8 & 0x7fffffffffffffff);
    }
  }
  else {
    iVar6 = thunk_FUN_05e1d97c(3);
    if (iVar6 != 0) {
      FUN_0488143c(&local_210);
      pppppcVar2 = (char *****)local_210;
      if (-1 < (long)local_200) {
        pppppcVar2 = &local_210;
      }
      if ((DAT_0a3a556a & 1) == 0) {
        _DAT_0a3a5544 = CONCAT44((int)DAT_084a66c8,(int)DAT_08486a48);
        uRam000000000a3a554c = CONCAT44((int)DAT_084a66a8,(int)DAT_084a8ea0);
        _DAT_0a3a5554 = CONCAT44((int)DAT_08617fc8,(int)DAT_084a66b0);
        uRam000000000a3a555c = CONCAT44((int)DAT_084967c0,(int)DAT_08489770);
        DAT_0a3a5564 = (undefined4)DAT_084ccd80;
        DAT_0a3a5568 = 99;
        DAT_0a3a556a = 1;
      }
      if ((DAT_0a3a55c7 & 1) == 0) {
        DAT_0a3a55b8._0_1_ = s_Validatesolv_0874dd00[0];
        DAT_0a3a55b8._1_1_ = s_Validatesolv_0874dd00[1];
        DAT_0a3a55b8._2_1_ = s_Validatesolv_0874dd00[2];
        DAT_0a3a55b8._3_1_ = s_Validatesolv_0874dd00[3];
        DAT_0a3a55b8._4_1_ = s_Validatesolv_0874dd00[4];
        DAT_0a3a55b8._5_1_ = s_Validatesolv_0874dd00[5];
        DAT_0a3a55b8._6_1_ = s_Validatesolv_0874dd00[6];
        DAT_0a3a55b8._7_1_ = s_Validatesolv_0874dd00[7];
        DAT_0a3a55c0 = (undefined4)ram0x084f2cf0;
        DAT_0a3a55c4 = 0x736d;
        DAT_0a3a55c6 = 0;
        DAT_0a3a55c7 = 1;
      }
      FUN_05e1d050(&local_1f0,3,pppppcVar2,&DAT_0a3a5544,&DAT_0a3a55b8,0xd1,0,0);
      if ((DAT_0a3a561a & 1) == 0) {
        uVar7 = 0;
        do {
          uVar16 = *(undefined4 *)((long)&DAT_08825bee + uVar7);
          uVar4 = CONCAT12((char)((uint)uVar16 >> 8),(short)uVar16) & 0xff00ff;
          uVar17 = *(undefined4 *)((long)&DAT_08825bda + uVar7 % 0x14);
          *(uint *)((long)&DAT_0a3a55c8 + uVar7) =
               CONCAT13((char)((uint)uVar16 >> 0x18) + 0x8aU ^ (byte)((uint)uVar17 >> 0x18),
                        CONCAT12((char)((uint)uVar16 >> 0x10) + 0x8aU ^ (byte)((uint)uVar17 >> 0x10)
                                 ,CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^ (byte)((uint)uVar17 >> 8)
                                           ,(char)uVar4 + 0x8aU ^ (byte)uVar17)));
          uVar7 = uVar7 + 4;
        } while (uVar7 != 0x50);
        DAT_0a3a5618 = 0x67;
        DAT_0a3a561a = 1;
      }
      uStack_88 = 0;
      local_90 = 0;
      uStack_78 = 0;
      uStack_80 = 0;
      uStack_a8 = 0;
      local_b0 = 0;
      uStack_98 = 0;
      uStack_a0 = 0;
      uStack_c8 = 0;
      local_d0 = 0;
      uStack_b8 = 0;
      uStack_c0 = 0;
      sStack_e8 = 0;
      local_f0 = (undefined8 *****)0x0;
      uStack_d8 = 0;
      local_e0 = 0;
      FUN_05e1d31c(&local_1f0,&DAT_0a3a55c8,&local_f0);
      thunk_FUN_05e1d0bc(&local_1f0);
      if ((long)local_200 < 0) {
        __ZdlPvm(local_210,(ulong)local_200 & 0x7fffffffffffffff);
      }
    }
    if ((DAT_0a3a5651 & 1) == 0) {
      _DAT_0a3a561c = CONCAT44((int)DAT_0870b770,(int)ram0x084f2cf0);
      uRam000000000a3a5624 = CONCAT44((int)DAT_084a80a0,(int)DAT_0880e448);
      _DAT_0a3a562c = CONCAT44((int)DAT_0855bb38,(int)DAT_08820bf0);
      uRam000000000a3a5634 = CONCAT44((int)DAT_08530658,(int)DAT_084897e0);
      _DAT_0a3a563c = CONCAT44((int)DAT_087364e0,(int)DAT_084ca330);
      uRam000000000a3a5644 = CONCAT44((int)DAT_0880a0a8,(int)DAT_08518818);
      DAT_0a3a564c = (undefined4)ram0x0847fe58;
      DAT_0a3a5650 = 0;
      DAT_0a3a5651 = 1;
    }
    sVar10 = _strlen(&DAT_0a3a561c);
    if (0x7ffffffffffffff7 < sVar10) {
                    /* WARNING: Subroutine does not return */
      FUN_00018d9c(&local_f0);
    }
    if (sVar10 < 0x17) {
      local_e0 = CONCAT17((char)sVar10,(undefined7)local_e0);
      pppppuVar12 = &local_f0;
      if (sVar10 != 0) goto LAB_0291e060;
    }
    else {
      uVar7 = 0x19;
      if ((sVar10 | 7) != 0x17) {
        uVar7 = (sVar10 | 7) + 1;
      }
      pppppuVar12 = (undefined8 *****)__Znwm(uVar7);
      local_e0 = uVar7 | 0x8000000000000000;
      local_f0 = pppppuVar12;
      sStack_e8 = sVar10;
LAB_0291e060:
      _memcpy(pppppuVar12,&DAT_0a3a561c,sVar10);
    }
    *(undefined1 *)((long)pppppuVar12 + sVar10) = 0;
    pppcStack_1e8 = (char ***)&DAT_aaaaaaaaaaaaaa00;
    local_1e0 = (char **)&DAT_aaaaaaaaaaaaaa00;
    local_1d8 = &DAT_aaaaaaaaaaaaaa00;
    local_1d0 = &DAT_aaaaaaaaaaaaaa00;
    local_1f0 = (char ****)&DAT_aaaaaaaaaaaaaa00;
    sStack_1c0 = sStack_e8;
    ppppuStack_1c8 = local_f0;
    local_1b8 = local_e0;
    local_1b0 = &DAT_aaaaaaaaaaaaaa01;
    local_210 = (char ****)*param_4;
    *param_4 = 0;
    (*(code *)local_210[1])(local_210,&local_1f0);
LAB_0291e0f4:
    FUN_00033d2c(&local_210);
    if (((char)local_1b0 == '\x01') && ((long)local_1b8 < 0)) {
      __ZdlPvm(ppppuStack_1c8,local_1b8 & 0x7fffffffffffffff);
    }
  }
  *(undefined1 *)param_1 = 0;
  *(undefined1 *)(param_1 + 9) = 0;
  if ((long)ppcStack_110 < 0) {
    __ZdlPvm(ppppcStack_120,(ulong)ppcStack_110 & 0x7fffffffffffffff);
  }
joined_r0x0291f908:
  if ((long)local_130 < 0) {
    __ZdlPvm(local_140,local_130 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_68) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


