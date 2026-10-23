// Ghidra inferred pseudocode; requested=0x2684bf0
// entry=02684bf0 end=02685677

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_02684bf0(long param_1,long param_2)

{
  uint uVar1;
  undefined8 ******ppppppuVar2;
  undefined1 uVar3;
  uint3 uVar4;
  bool bVar5;
  int iVar6;
  long lVar7;
  long ******pppppplVar8;
  undefined8 *puVar9;
  undefined1 *puVar10;
  undefined1 *puVar11;
  long lVar12;
  undefined1 *puVar13;
  ulong uVar14;
  int iVar15;
  undefined4 uVar16;
  undefined4 uVar17;
  undefined8 *****local_308 [2];
  undefined7 local_2f8;
  char cStack_2f1;
  undefined1 auStack_2f0 [144];
  undefined1 *local_260;
  undefined1 local_258 [71];
  undefined1 uStack_211;
  undefined8 local_210;
  undefined1 local_208 [72];
  long *****local_1c0;
  undefined8 local_1b8;
  undefined7 local_1b0;
  char cStack_1a9;
  undefined1 uStack_171;
  undefined8 local_170;
  undefined8 uStack_168;
  undefined1 *local_160;
  undefined1 uStack_121;
  undefined8 local_120;
  undefined8 local_118;
  undefined7 local_110;
  char cStack_109;
  undefined8 *local_d0;
  undefined8 *puStack_c8;
  long *****ppppplStack_c0;
  undefined8 *local_b8;
  undefined1 **ppuStack_b0;
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
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  iVar6 = thunk_FUN_05e1d97c(2);
  if (iVar6 != 0) {
    FUN_0488143c(local_308);
    ppppppuVar2 = (undefined8 ******)local_308[0];
    if (-1 < cStack_2f1) {
      ppppppuVar2 = local_308;
    }
    if ((DAT_0a391bc3 & 1) == 0) {
      uRam000000000a391bb8._0_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x18];
      uRam000000000a391bb8._1_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x19];
      uRam000000000a391bb8._2_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1a];
      uRam000000000a391bb8._3_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1b];
      uRam000000000a391bb8._4_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1c];
      uRam000000000a391bb8._5_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1d];
      uRam000000000a391bb8._6_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1e];
      uRam000000000a391bb8._7_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1f];
      DAT_0a391bb0 = s_ai_assisasst_talchatbot_manager__087e3420[0x10];
      DAT_0a391bb0_1._0_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x11];
      DAT_0a391bb0_1._1_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x12];
      DAT_0a391bb0_1._2_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x13];
      DAT_0a391bb0_1._3_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x14];
      DAT_0a391bb0_1._4_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x15];
      DAT_0a391bb0_1._5_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x16];
      DAT_0a391bb0_1._6_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x17];
      DAT_0a391bc0 = 0x6363;
      DAT_0a391bc2 = 0;
      DAT_0a391bc3 = 1;
    }
    if ((DAT_0a392b32 & 1) == 0) {
      uRam000000000a392b28._0_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x28];
      uRam000000000a392b28._1_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x29];
      uRam000000000a392b28._2_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x2a];
      uRam000000000a392b28._3_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x2b];
      uRam000000000a392b28._4_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x2c];
      uRam000000000a392b28._5_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x2d];
      uRam000000000a392b28._6_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x2e];
      uRam000000000a392b28._7_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x2f];
      DAT_0a392b20 = s_DestroyChatSessiStartDestroyTime_087e3540[0x20];
      DAT_0a392b20_1._0_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x21];
      DAT_0a392b20_1._1_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x22];
      DAT_0a392b20_1._2_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x23];
      DAT_0a392b20_1._3_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x24];
      DAT_0a392b20_1._4_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x25];
      DAT_0a392b20_1._5_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x26];
      DAT_0a392b20_1._6_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x27];
      DAT_0a392b30 = 0x67;
      DAT_0a392b32 = 1;
    }
    FUN_05e1d050(auStack_2f0,2,ppppppuVar2,&DAT_0a391bb0,&DAT_0a392b20,0x83e,0,0);
    pppppplVar8 = *(long *******)(param_2 + 0x20);
    local_120 = (long ******)*pppppplVar8;
    if (-1 < *(char *)((long)pppppplVar8 + 0x17)) {
      local_120 = pppppplVar8;
    }
    local_118._0_1_ = 0;
    iVar6 = *(int *)(param_2 + 0x10);
    local_170 = (undefined8 *)0x0;
    if ((DAT_0a394c3a & 1) == 0) {
      uVar14 = 0;
      do {
        uVar16 = *(undefined4 *)((long)&DAT_087e9335 + uVar14);
        uVar4 = CONCAT12((char)((uint)uVar16 >> 8),(short)uVar16) & 0xff00ff;
        uVar17 = *(undefined4 *)((long)&DAT_087e9321 + uVar14 % 0x14);
        *(uint *)((long)&DAT_0a394bf2 + uVar14) =
             CONCAT13((char)((uint)uVar16 >> 0x18) + 0x69U ^ (byte)((uint)uVar17 >> 0x18),
                      CONCAT12((char)((uint)uVar16 >> 0x10) + 0x69U ^ (byte)((uint)uVar17 >> 0x10),
                               CONCAT11((char)(uVar4 >> 0x10) + 0x69U ^ (byte)((uint)uVar17 >> 8),
                                        (char)uVar4 + 0x69U ^ (byte)uVar17)));
        uVar14 = uVar14 + 4;
      } while (uVar14 != 0x48);
      DAT_0a394c3a = 1;
    }
    lVar7 = 8;
    iVar15 = iVar6;
    do {
      lVar12 = lVar7;
      *(undefined1 *)((long)&local_170 + lVar12) =
           *(undefined1 *)((long)&DAT_0a394bf2 + (long)(iVar15 % 10 + 0x23));
      lVar7 = lVar12 + 1;
      uVar1 = iVar15 + 9;
      iVar15 = iVar15 / 10;
    } while (0x12 < uVar1);
    if (iVar6 < 0) {
      *(undefined1 *)((long)&local_170 + lVar12 + 1) = 0x2d;
      lVar7 = lVar12 + 2;
    }
    *(undefined1 *)((long)&local_170 + lVar7) = 0;
    if (9 < lVar7) {
      puVar11 = &uStack_171 + lVar7;
      puVar10 = (undefined1 *)((long)&uStack_168 + 1);
      do {
        uVar3 = *puVar11;
        *puVar11 = puVar10[-1];
        puVar10[-1] = uVar3;
        bVar5 = puVar10 < puVar11 + -1;
        puVar11 = puVar11 + -1;
        puVar10 = puVar10 + 1;
      } while (bVar5);
    }
    local_170 = &uStack_168;
    local_1c0 = (long *****)0x0;
    lVar7 = 0;
    uVar14 = *(ulong *)(param_2 + 0x18);
    do {
      lVar12 = lVar7;
      *(undefined1 *)((long)&local_1b8 + lVar12) = (&DAT_0a394c15)[uVar14 % 10];
      bVar5 = 9 < uVar14;
      lVar7 = lVar12 + 1;
      uVar14 = uVar14 / 10;
    } while (bVar5);
    *(undefined1 *)((long)&local_1b8 + lVar12 + 1) = 0;
    if (8 < lVar12 + 8U) {
      puVar11 = (undefined1 *)((long)&local_1b8 + lVar12);
      puVar10 = (undefined1 *)((long)&local_1b8 + 1);
      do {
        uVar3 = *puVar11;
        *puVar11 = puVar10[-1];
        puVar10[-1] = uVar3;
        bVar5 = puVar10 < puVar11 + -1;
        puVar11 = puVar11 + -1;
        puVar10 = puVar10 + 1;
      } while (bVar5);
    }
    local_1c0 = (long *****)&local_1b8;
    iVar6 = *(int *)(param_2 + 0x14);
    local_210 = (undefined1 *)0x0;
    lVar7 = 8;
    iVar15 = iVar6;
    do {
      lVar12 = lVar7;
      local_208[lVar12 + -8] = *(undefined1 *)((long)&DAT_0a394bf2 + (long)(iVar15 % 10 + 0x23));
      lVar7 = lVar12 + 1;
      uVar1 = iVar15 + 9;
      iVar15 = iVar15 / 10;
    } while (0x12 < uVar1);
    if (iVar6 < 0) {
      local_208[lVar12 + -7] = 0x2d;
      lVar7 = lVar12 + 2;
    }
    local_208[lVar7 + -8] = 0;
    if (9 < lVar7) {
      puVar11 = local_208;
      puVar10 = &uStack_211 + lVar7;
      do {
        puVar11 = puVar11 + 1;
        uVar3 = *puVar10;
        puVar13 = puVar10 + -1;
        *puVar10 = puVar11[-1];
        puVar11[-1] = uVar3;
        puVar10 = puVar13;
      } while (puVar11 < puVar13);
    }
    local_210 = local_208;
    uVar14 = (ulong)*(char *)(*(long *)(param_2 + 8) + 0x17);
    if ((long)uVar14 < 0) {
      uVar14 = *(ulong *)(*(long *)(param_2 + 8) + 8);
    }
    local_260 = local_258;
    lVar7 = 0;
    do {
      lVar12 = lVar7;
      local_258[lVar12] = (&DAT_0a394c15)[uVar14 % 10];
      bVar5 = 9 < uVar14;
      uVar14 = uVar14 / 10;
      lVar7 = lVar12 + 1;
    } while (bVar5);
    local_258[lVar12 + 1] = 0;
    if (8 < lVar12 + 8U) {
      puVar11 = local_258;
      puVar10 = local_258 + lVar12;
      do {
        puVar11 = puVar11 + 1;
        uVar3 = *puVar10;
        puVar13 = puVar10 + -1;
        *puVar10 = puVar11[-1];
        puVar11[-1] = uVar3;
        puVar10 = puVar13;
      } while (puVar11 < puVar13);
    }
    if ((DAT_0a392b81 & 1) == 0) {
      uVar14 = 0;
      do {
        uVar16 = *(undefined4 *)((long)&DAT_087e6544 + uVar14);
        uVar4 = CONCAT12((char)((uint)uVar16 >> 8),(short)uVar16) & 0xff00ff;
        uVar17 = *(undefined4 *)((long)&DAT_087e6530 + uVar14 % 0x14);
        *(uint *)((long)&DAT_0a392b33 + uVar14) =
             CONCAT13((char)((uint)uVar16 >> 0x18) + 0x8aU ^ (byte)((uint)uVar17 >> 0x18),
                      CONCAT12((char)((uint)uVar16 >> 0x10) + 0x8aU ^ (byte)((uint)uVar17 >> 0x10),
                               CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^ (byte)((uint)uVar17 >> 8),
                                        (char)uVar4 + 0x8aU ^ (byte)uVar17)));
        uVar14 = uVar14 + 4;
      } while (uVar14 != 0x4c);
      DAT_0a392b7f = 0x5f;
      DAT_0a392b81 = 1;
    }
    local_d0 = &local_120;
    puStack_c8 = &local_170;
    ppppplStack_c0 = (long *****)&local_1c0;
    local_b8 = &local_210;
    ppuStack_b0 = &local_260;
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
    local_58 = 0;
    FUN_05e1d31c(auStack_2f0,&DAT_0a392b33,&local_d0);
    thunk_FUN_05e1d0bc(auStack_2f0);
    if (cStack_2f1 < '\0') {
      __ZdlPvm(local_308[0],CONCAT17(cStack_2f1,local_2f8) & 0x7fffffffffffffff);
    }
  }
  uStack_168 = &SUB_aaaaaaaaaaaaaaaa;
  local_160 = &SUB_aaaaaaaaaaaaaaaa;
  local_170 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
  puVar9 = *(undefined8 **)(param_2 + 0x20);
  if (*(char *)((long)puVar9 + 0x17) < '\0') {
    FUN_00018d20(&local_170,*puVar9,puVar9[1]);
  }
  else {
    uStack_168 = (undefined1 *)puVar9[1];
    local_170 = (undefined8 *)*puVar9;
    local_160 = (undefined1 *)puVar9[2];
  }
  lVar7 = FUN_026ac6ac(param_1 + 0x898,&local_170);
  if ((lVar7 != 0) && (*(long *)(lVar7 + 0xa0) != 0)) {
    lVar7 = FUN_02685728(param_1,&local_170);
  }
  iVar6 = *(int *)(param_2 + 0x10);
  if (iVar6 < 0x7d3) {
    if (iVar6 == 0x3ea) {
      FUN_026864ec(param_1,&local_170,*(undefined8 *)(param_2 + 8));
      goto LAB_0268562c;
    }
    if (iVar6 == 0x7d1) {
      FUN_0267ea34(param_1,&local_170,*(undefined8 *)(param_2 + 8));
      goto LAB_0268562c;
    }
    if (iVar6 == 0x7d2) {
      FUN_0267f930(param_1,&local_170,*(undefined8 *)(param_2 + 8));
      goto LAB_0268562c;
    }
LAB_026851c4:
    iVar6 = thunk_FUN_05e1d97c(3);
    if (iVar6 == 0) goto LAB_0268562c;
    FUN_0488143c(&local_1c0);
    pppppplVar8 = (long ******)local_1c0;
    if (-1 < cStack_1a9) {
      pppppplVar8 = &local_1c0;
    }
    if ((DAT_0a391bc3 & 1) == 0) {
      uRam000000000a391bb8._0_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x18];
      uRam000000000a391bb8._1_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x19];
      uRam000000000a391bb8._2_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1a];
      uRam000000000a391bb8._3_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1b];
      uRam000000000a391bb8._4_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1c];
      uRam000000000a391bb8._5_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1d];
      uRam000000000a391bb8._6_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1e];
      uRam000000000a391bb8._7_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1f];
      DAT_0a391bb0 = s_ai_assisasst_talchatbot_manager__087e3420[0x10];
      DAT_0a391bb0_1._0_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x11];
      DAT_0a391bb0_1._1_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x12];
      DAT_0a391bb0_1._2_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x13];
      DAT_0a391bb0_1._3_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x14];
      DAT_0a391bb0_1._4_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x15];
      DAT_0a391bb0_1._5_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x16];
      DAT_0a391bb0_1._6_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x17];
      DAT_0a391bc0 = 0x6363;
      DAT_0a391bc2 = 0;
      DAT_0a391bc3 = 1;
    }
    if ((DAT_0a392b32 & 1) == 0) {
      uRam000000000a392b28._0_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x28];
      uRam000000000a392b28._1_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x29];
      uRam000000000a392b28._2_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x2a];
      uRam000000000a392b28._3_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x2b];
      uRam000000000a392b28._4_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x2c];
      uRam000000000a392b28._5_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x2d];
      uRam000000000a392b28._6_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x2e];
      uRam000000000a392b28._7_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x2f];
      DAT_0a392b20 = s_DestroyChatSessiStartDestroyTime_087e3540[0x20];
      DAT_0a392b20_1._0_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x21];
      DAT_0a392b20_1._1_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x22];
      DAT_0a392b20_1._2_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x23];
      DAT_0a392b20_1._3_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x24];
      DAT_0a392b20_1._4_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x25];
      DAT_0a392b20_1._5_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x26];
      DAT_0a392b20_1._6_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x27];
      DAT_0a392b30 = 0x67;
      DAT_0a392b32 = 1;
    }
    FUN_05e1d050(auStack_2f0,3,pppppplVar8,&DAT_0a391bb0,&DAT_0a392b20,0x861,0,0);
    iVar6 = *(int *)(param_2 + 0x10);
    local_120 = (long ******)0x0;
    if ((DAT_0a394c3a & 1) == 0) {
      uVar14 = 0;
      do {
        uVar16 = *(undefined4 *)((long)&DAT_087e9335 + uVar14);
        uVar4 = CONCAT12((char)((uint)uVar16 >> 8),(short)uVar16) & 0xff00ff;
        uVar17 = *(undefined4 *)((long)&DAT_087e9321 + uVar14 % 0x14);
        *(uint *)((long)&DAT_0a394bf2 + uVar14) =
             CONCAT13((char)((uint)uVar16 >> 0x18) + 0x69U ^ (byte)((uint)uVar17 >> 0x18),
                      CONCAT12((char)((uint)uVar16 >> 0x10) + 0x69U ^ (byte)((uint)uVar17 >> 0x10),
                               CONCAT11((char)(uVar4 >> 0x10) + 0x69U ^ (byte)((uint)uVar17 >> 8),
                                        (char)uVar4 + 0x69U ^ (byte)uVar17)));
        uVar14 = uVar14 + 4;
      } while (uVar14 != 0x48);
      DAT_0a394c3a = 1;
    }
    lVar7 = 8;
    iVar15 = iVar6;
    do {
      lVar12 = lVar7;
      *(undefined1 *)((long)&local_120 + lVar12) =
           *(undefined1 *)((long)&DAT_0a394bf2 + (long)(iVar15 % 10 + 0x23));
      lVar7 = lVar12 + 1;
      uVar1 = iVar15 + 9;
      iVar15 = iVar15 / 10;
    } while (0x12 < uVar1);
    if (iVar6 < 0) {
      *(undefined1 *)((long)&local_120 + lVar12 + 1) = 0x2d;
      lVar7 = lVar12 + 2;
    }
    *(undefined1 *)((long)&local_120 + lVar7) = 0;
    if (9 < lVar7) {
      puVar11 = &uStack_121 + lVar7;
      puVar10 = (undefined1 *)((long)&local_118 + 1);
      do {
        uVar3 = *puVar11;
        *puVar11 = puVar10[-1];
        puVar10[-1] = uVar3;
        bVar5 = puVar10 < puVar11 + -1;
        puVar11 = puVar11 + -1;
        puVar10 = puVar10 + 1;
      } while (bVar5);
    }
    if ((DAT_0a392bd5 & 1) == 0) {
      _DAT_0a392bb0 = CONCAT44((int)DAT_0856e330,(int)ram0x085213e0);
      uRam000000000a392bb8 = CONCAT44((int)ram0x087e2c38,(int)DAT_084d82d8);
      _DAT_0a392bc0 = CONCAT44((int)DAT_085b05f0,(int)DAT_087e2cd0);
      uRam000000000a392bc8 = CONCAT44((int)ram0x08492778,(int)DAT_087e2f88);
      DAT_0a392bd0 = (undefined4)DAT_084f1788;
      DAT_0a392bd4 = 0;
      DAT_0a392bd5 = 1;
    }
    ppppplStack_c0 = (long *****)0x0;
    puStack_c8 = (undefined8 *)0x0;
    local_d0 = &local_120;
    ppuStack_b0 = (undefined1 **)0x0;
    local_b8 = (undefined8 *)0x0;
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
    local_58 = 0;
    local_120 = (long ******)&local_118;
    FUN_05e1d31c(auStack_2f0,&DAT_0a392bb0,&local_d0);
    thunk_FUN_05e1d0bc(auStack_2f0);
    if (-1 < cStack_1a9) goto LAB_0268562c;
    uVar14 = CONCAT17(cStack_1a9,local_1b0);
    pppppplVar8 = (long ******)local_1c0;
  }
  else {
    if (iVar6 == 0x7d3) {
      FUN_026859b0(param_1,&local_170,*(undefined8 *)(param_2 + 8));
      goto LAB_0268562c;
    }
    if (iVar6 != 0x7d4) {
      if (iVar6 == 0x7d5) {
        FUN_02686020(lVar7,&local_170,*(undefined8 *)(param_2 + 8));
        goto LAB_0268562c;
      }
      goto LAB_026851c4;
    }
    iVar6 = thunk_FUN_05e1d97c(2);
    if (iVar6 == 0) goto LAB_0268562c;
    FUN_0488143c(&local_120);
    pppppplVar8 = local_120;
    if (-1 < cStack_109) {
      pppppplVar8 = (long ******)&local_120;
    }
    if ((DAT_0a391bc3 & 1) == 0) {
      uRam000000000a391bb8._0_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x18];
      uRam000000000a391bb8._1_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x19];
      uRam000000000a391bb8._2_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1a];
      uRam000000000a391bb8._3_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1b];
      uRam000000000a391bb8._4_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1c];
      uRam000000000a391bb8._5_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1d];
      uRam000000000a391bb8._6_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1e];
      uRam000000000a391bb8._7_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1f];
      DAT_0a391bb0 = s_ai_assisasst_talchatbot_manager__087e3420[0x10];
      DAT_0a391bb0_1._0_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x11];
      DAT_0a391bb0_1._1_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x12];
      DAT_0a391bb0_1._2_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x13];
      DAT_0a391bb0_1._3_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x14];
      DAT_0a391bb0_1._4_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x15];
      DAT_0a391bb0_1._5_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x16];
      DAT_0a391bb0_1._6_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x17];
      DAT_0a391bc0 = 0x6363;
      DAT_0a391bc2 = 0;
      DAT_0a391bc3 = 1;
    }
    if ((DAT_0a392b32 & 1) == 0) {
      uRam000000000a392b28._0_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x28];
      uRam000000000a392b28._1_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x29];
      uRam000000000a392b28._2_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x2a];
      uRam000000000a392b28._3_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x2b];
      uRam000000000a392b28._4_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x2c];
      uRam000000000a392b28._5_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x2d];
      uRam000000000a392b28._6_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x2e];
      uRam000000000a392b28._7_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x2f];
      DAT_0a392b20 = s_DestroyChatSessiStartDestroyTime_087e3540[0x20];
      DAT_0a392b20_1._0_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x21];
      DAT_0a392b20_1._1_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x22];
      DAT_0a392b20_1._2_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x23];
      DAT_0a392b20_1._3_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x24];
      DAT_0a392b20_1._4_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x25];
      DAT_0a392b20_1._5_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x26];
      DAT_0a392b20_1._6_1_ = s_DestroyChatSessiStartDestroyTime_087e3540[0x27];
      DAT_0a392b30 = 0x67;
      DAT_0a392b32 = 1;
    }
    FUN_05e1d050(auStack_2f0,2,pppppplVar8,&DAT_0a391bb0,&DAT_0a392b20,0x85d,0,0);
    if ((DAT_0a392bad & 1) == 0) {
      _DAT_0a392b84 = CONCAT44((int)DAT_0856e330,(int)ram0x085213e0);
      uRam000000000a392b8c = CONCAT44((int)ram0x087e2c38,(int)DAT_084d82d8);
      _DAT_0a392b94 = CONCAT44((int)DAT_08487d20,(int)DAT_08563370);
      uRam000000000a392b9c = CONCAT44((int)DAT_08518840,(int)DAT_08518838);
      DAT_0a392ba4 = CONCAT44((int)DAT_087e2f80,(int)DAT_087e2f78);
      DAT_0a392bac = 0;
      DAT_0a392bad = 1;
    }
    local_68 = 0;
    uStack_70 = 0;
    local_58 = 0;
    uStack_60 = 0;
    local_88 = 0;
    uStack_90 = 0;
    local_78 = 0;
    uStack_80 = 0;
    local_a8 = 0;
    ppuStack_b0 = (undefined1 **)0x0;
    local_98 = 0;
    uStack_a0 = 0;
    puStack_c8 = (undefined8 *)0x0;
    local_d0 = (undefined8 *)0x0;
    local_b8 = (undefined8 *)0x0;
    ppppplStack_c0 = (long *****)0x0;
    FUN_05e1d31c(auStack_2f0,&DAT_0a392b84,&local_d0);
    thunk_FUN_05e1d0bc(auStack_2f0);
    if (-1 < cStack_109) goto LAB_0268562c;
    uVar14 = CONCAT17(cStack_109,local_110);
    pppppplVar8 = local_120;
  }
  __ZdlPvm(pppppplVar8,uVar14 & 0x7fffffffffffffff);
LAB_0268562c:
  if ((long)local_160 < 0) {
    __ZdlPvm(local_170,(ulong)local_160 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


