// Ghidra inferred pseudocode; requested=0x265e9b8
// entry=0265e9b8 end=0265f333

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

ulong FUN_0265e9b8(long param_1,long ******param_2,int param_3,long param_4,long *param_5,
                  int param_6)

{
  uint uVar1;
  long *plVar2;
  long ******pppppplVar3;
  undefined8 ******ppppppuVar4;
  undefined1 uVar5;
  uint3 uVar6;
  bool bVar7;
  int iVar8;
  ulong uVar9;
  undefined1 *puVar10;
  undefined1 *puVar11;
  long lVar12;
  long lVar13;
  undefined1 *puVar14;
  ulong uVar15;
  undefined4 uVar16;
  undefined4 uVar17;
  undefined8 *****local_2c0 [2];
  undefined7 local_2b0;
  char cStack_2a9;
  undefined8 *****local_2a8;
  undefined8 local_2a0;
  undefined8 local_298;
  undefined1 *local_290;
  undefined8 *puStack_288;
  undefined8 local_280;
  undefined1 *puStack_278;
  undefined8 *local_270;
  undefined1 *puStack_268;
  undefined1 auStack_260 [144];
  undefined8 *****local_1d0;
  undefined8 local_1c8;
  undefined7 local_1c0;
  char cStack_1b9;
  undefined1 uStack_181;
  undefined8 local_180;
  undefined1 local_178 [72];
  long *****local_130;
  undefined1 local_128;
  undefined7 local_120;
  char cStack_119;
  long *****local_e0;
  undefined8 *puStack_d8;
  undefined8 *****local_d0;
  undefined8 uStack_c8;
  undefined8 uStack_c0;
  undefined8 uStack_b8;
  undefined8 uStack_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  undefined8 local_78;
  undefined8 uStack_70;
  undefined8 local_68;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  if (*(long *)(param_1 + 0x20) == 0) {
    iVar8 = thunk_FUN_05e1d97c(3);
    if (iVar8 != 0) {
      FUN_0488143c(&local_130);
      pppppplVar3 = (long ******)local_130;
      if (-1 < cStack_119) {
        pppppplVar3 = &local_130;
      }
      if ((DAT_0a391342 & 1) == 0) {
        uRam000000000a391338._0_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[8];
        uRam000000000a391338._1_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[9];
        uRam000000000a391338._2_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[10];
        uRam000000000a391338._3_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[0xb];
        uRam000000000a391338._4_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[0xc];
        uRam000000000a391338._5_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[0xd];
        uRam000000000a391338._6_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[0xe];
        uRam000000000a391338._7_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[0xf];
        DAT_0a391330 = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[0];
        DAT_0a391330_1._0_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[1];
        DAT_0a391330_1._1_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[2];
        DAT_0a391330_1._2_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[3];
        DAT_0a391330_1._3_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[4];
        DAT_0a391330_1._4_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[5];
        DAT_0a391330_1._5_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[6];
        DAT_0a391330_1._6_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[7];
        DAT_0a391340 = 99;
        DAT_0a391342 = 1;
      }
      if ((DAT_0a3915c0 & 1) == 0) {
        DAT_0a3915b8._0_1_ = s_parent_iSendMsg_085977d0[8];
        DAT_0a3915b8._1_1_ = s_parent_iSendMsg_085977d0[9];
        DAT_0a3915b8._2_1_ = s_parent_iSendMsg_085977d0[10];
        DAT_0a3915b8._3_1_ = s_parent_iSendMsg_085977d0[0xb];
        DAT_0a3915b8._4_1_ = s_parent_iSendMsg_085977d0[0xc];
        DAT_0a3915b8._5_1_ = s_parent_iSendMsg_085977d0[0xd];
        DAT_0a3915b8._6_1_ = s_parent_iSendMsg_085977d0[0xe];
        DAT_0a3915b8._7_1_ = s_parent_iSendMsg_085977d0[0xf];
        DAT_0a3915c0 = 1;
      }
      FUN_05e1d050(auStack_260,3,pppppplVar3,&DAT_0a391330,&DAT_0a3915b8,0xb2,0,0);
      if ((DAT_0a3915fa & 1) == 0) {
        _DAT_0a3915c4 = CONCAT44((int)DAT_087e1b20,(int)ram0x087e1b18);
        uRam000000000a3915cc = CONCAT44((int)DAT_087e1b90,(int)DAT_0849b068);
        _DAT_0a3915d4 = CONCAT44((int)DAT_0866e318,(int)DAT_085929b8);
        uRam000000000a3915dc = CONCAT44((int)DAT_085ef2f8,(int)DAT_085ef2f0);
        _DAT_0a3915e4 = CONCAT44((int)DAT_087e1bb8,(int)DAT_087e1c00);
        uRam000000000a3915ec = CONCAT44((int)DAT_084f2d58,(int)DAT_084cae88);
        DAT_0a3915f4 = (undefined4)ram0x08484500;
        DAT_0a3915f8 = 100;
        DAT_0a3915fa = 1;
      }
      local_78 = 0;
      uStack_80 = 0;
      local_68 = 0;
      uStack_70 = 0;
      local_98 = 0;
      uStack_a0 = 0;
      local_88 = 0;
      uStack_90 = 0;
      uStack_b8 = 0;
      uStack_c0 = 0;
      local_a8 = 0;
      uStack_b0 = 0;
      puStack_d8 = (undefined8 *)0x0;
      local_e0 = (long *****)0x0;
      uStack_c8 = 0;
      local_d0 = (undefined8 ******)0x0;
      FUN_05e1d31c(auStack_260,&DAT_0a3915c4,&local_e0);
      thunk_FUN_05e1d0bc(auStack_260);
      if (cStack_119 < '\0') {
        __ZdlPvm(local_130,CONCAT17(cStack_119,local_120) & 0x7fffffffffffffff);
      }
    }
    uVar9 = 0;
    goto LAB_0265f2f8;
  }
  puStack_278 = &SUB_aaaaaaaaaaaaaaaa;
  local_280 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_268 = &SUB_aaaaaaaaaaaaaaaa;
  local_270 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
  puStack_288 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
  local_290 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_05607970(&local_290);
  local_280 = (undefined1 *)CONCAT44(local_280._4_4_,param_3);
  puStack_268 = (undefined1 *)((ulong)puStack_268 | 0x1100000000);
  if (local_270 == &DAT_0a524ad0) {
    local_270 = (undefined8 *)__Znwm(0x18);
    *local_270 = 0;
    local_270[1] = 0;
    local_270[2] = 0;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(local_270,param_2);
  uVar9 = *(ulong *)(param_4 + 8);
  if (-1 < (char)*(byte *)(param_4 + 0x17)) {
    uVar9 = (ulong)*(byte *)(param_4 + 0x17);
  }
  if (uVar9 != 0) {
    puStack_268 = (undefined1 *)((ulong)puStack_268 | 0x200000000);
    if (puStack_288 == &DAT_0a524ad0) {
      puStack_288 = (undefined8 *)__Znwm(0x18);
      *puStack_288 = 0;
      puStack_288[1] = 0;
      puStack_288[2] = 0;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puStack_288,param_4);
  }
  if (param_6 != 0) {
    puStack_268 = (undefined1 *)((ulong)puStack_268 | 0x800000000);
    local_280 = (undefined1 *)CONCAT44(param_6,(undefined4)local_280);
  }
  local_2a8 = (undefined8 ******)0x0;
  local_2a0 = 0;
  local_298 = 0;
  FUN_05ab3f60(&local_290,&local_2a8);
  ppppppuVar4 = (undefined8 ******)local_2a8;
  uVar1 = (uint)local_2a0;
  if (-1 < (long)local_298) {
    ppppppuVar4 = &local_2a8;
    uVar1 = (uint)local_298._7_1_;
  }
  plVar2 = (long *)*param_5;
  if (-1 < *(char *)((long)param_5 + 0x17)) {
    plVar2 = param_5;
  }
  uVar9 = (**(code **)(**(long **)(param_1 + 0x20) + 0x20))
                    (*(long **)(param_1 + 0x20),ppppppuVar4,uVar1,plVar2);
  if (uVar9 == 0) {
    iVar8 = thunk_FUN_05e1d97c(3);
    if (iVar8 != 0) {
      FUN_0488143c(&local_1d0);
      ppppppuVar4 = (undefined8 ******)local_1d0;
      if (-1 < cStack_1b9) {
        ppppppuVar4 = &local_1d0;
      }
      if ((DAT_0a391342 & 1) == 0) {
        uRam000000000a391338._0_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[8];
        uRam000000000a391338._1_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[9];
        uRam000000000a391338._2_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[10];
        uRam000000000a391338._3_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[0xb];
        uRam000000000a391338._4_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[0xc];
        uRam000000000a391338._5_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[0xd];
        uRam000000000a391338._6_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[0xe];
        uRam000000000a391338._7_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[0xf];
        DAT_0a391330 = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[0];
        DAT_0a391330_1._0_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[1];
        DAT_0a391330_1._1_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[2];
        DAT_0a391330_1._2_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[3];
        DAT_0a391330_1._3_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[4];
        DAT_0a391330_1._4_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[5];
        DAT_0a391330_1._5_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[6];
        DAT_0a391330_1._6_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[7];
        DAT_0a391340 = 99;
        DAT_0a391342 = 1;
      }
      if ((DAT_0a3915c0 & 1) == 0) {
        DAT_0a3915b8._0_1_ = s_parent_iSendMsg_085977d0[8];
        DAT_0a3915b8._1_1_ = s_parent_iSendMsg_085977d0[9];
        DAT_0a3915b8._2_1_ = s_parent_iSendMsg_085977d0[10];
        DAT_0a3915b8._3_1_ = s_parent_iSendMsg_085977d0[0xb];
        DAT_0a3915b8._4_1_ = s_parent_iSendMsg_085977d0[0xc];
        DAT_0a3915b8._5_1_ = s_parent_iSendMsg_085977d0[0xd];
        DAT_0a3915b8._6_1_ = s_parent_iSendMsg_085977d0[0xe];
        DAT_0a3915b8._7_1_ = s_parent_iSendMsg_085977d0[0xf];
        DAT_0a3915c0 = 1;
      }
      FUN_05e1d050(auStack_260,3,ppppppuVar4,&DAT_0a391330,&DAT_0a3915b8,200,0,0);
      local_130 = *param_2;
      if (-1 < *(char *)((long)param_2 + 0x17)) {
        local_130 = (long *****)param_2;
      }
      local_128 = 0;
      local_180 = (undefined1 *)0x0;
      if ((DAT_0a39190f & 1) == 0) {
        uVar15 = 0;
        do {
          uVar16 = *(undefined4 *)((long)&DAT_087e253a + uVar15);
          uVar6 = CONCAT12((char)((uint)uVar16 >> 8),(short)uVar16) & 0xff00ff;
          uVar17 = *(undefined4 *)((long)&DAT_087e2526 + uVar15 % 0x14);
          *(uint *)((long)&DAT_0a3918c7 + uVar15) =
               CONCAT13((char)((uint)uVar16 >> 0x18) + 0x8aU ^ (byte)((uint)uVar17 >> 0x18),
                        CONCAT12((char)((uint)uVar16 >> 0x10) + 0x8aU ^ (byte)((uint)uVar17 >> 0x10)
                                 ,CONCAT11((char)(uVar6 >> 0x10) + 0x8aU ^ (byte)((uint)uVar17 >> 8)
                                           ,(char)uVar6 + 0x8aU ^ (byte)uVar17)));
          uVar15 = uVar15 + 4;
        } while (uVar15 != 0x48);
        DAT_0a39190f = 1;
      }
      lVar13 = 8;
      iVar8 = param_3;
      do {
        lVar12 = lVar13;
        local_178[lVar12 + -8] = *(undefined1 *)((long)&DAT_0a3918c7 + (long)(iVar8 % 10 + 0x23));
        lVar13 = lVar12 + 1;
        uVar1 = iVar8 + 9;
        iVar8 = iVar8 / 10;
      } while (0x12 < uVar1);
      if (param_3 < 0) {
        local_178[lVar12 + -7] = 0x2d;
        lVar13 = lVar12 + 2;
      }
      local_178[lVar13 + -8] = 0;
      if (9 < lVar13) {
        puVar11 = local_178;
        puVar10 = &uStack_181 + lVar13;
        do {
          puVar11 = puVar11 + 1;
          uVar5 = *puVar10;
          puVar14 = puVar10 + -1;
          *puVar10 = puVar11[-1];
          puVar11[-1] = uVar5;
          puVar10 = puVar14;
        } while (puVar11 < puVar14);
      }
      if ((DAT_0a391674 & 1) == 0) {
        uVar15 = 0;
        do {
          uVar16 = *(undefined4 *)((long)&DAT_087e2121 + uVar15);
          uVar6 = CONCAT12((char)((uint)uVar16 >> 8),(short)uVar16) & 0xff00ff;
          uVar17 = *(undefined4 *)((long)&DAT_087e210d + uVar15 % 0x14);
          *(uint *)((long)&DAT_0a39163b + uVar15) =
               CONCAT13((char)((uint)uVar16 >> 0x18) + 0x8aU ^ (byte)((uint)uVar17 >> 0x18),
                        CONCAT12((char)((uint)uVar16 >> 0x10) + 0x8aU ^ (byte)((uint)uVar17 >> 0x10)
                                 ,CONCAT11((char)(uVar6 >> 0x10) + 0x8aU ^ (byte)((uint)uVar17 >> 8)
                                           ,(char)uVar6 + 0x8aU ^ (byte)uVar17)));
          uVar15 = uVar15 + 4;
        } while (uVar15 != 0x38);
        DAT_0a391673 = 0;
        DAT_0a391674 = 1;
      }
      local_e0 = (long *****)&local_130;
      puStack_d8 = &local_180;
      uStack_c8 = 0;
      local_d0 = (undefined8 ******)0x0;
      uStack_b8 = 0;
      uStack_c0 = 0;
      local_a8 = 0;
      uStack_b0 = 0;
      local_98 = 0;
      uStack_a0 = 0;
      local_88 = 0;
      uStack_90 = 0;
      local_78 = 0;
      uStack_80 = 0;
      local_68 = 0;
      uStack_70 = 0;
      local_180 = local_178;
      FUN_05e1d31c(auStack_260,&DAT_0a39163b,&local_e0);
      thunk_FUN_05e1d0bc(auStack_260);
      if (cStack_1b9 < '\0') {
        uVar15 = CONCAT17(cStack_1b9,local_1c0);
        local_2c0[0] = local_1d0;
        goto LAB_0265f2d0;
      }
    }
  }
  else {
    iVar8 = thunk_FUN_05e1d97c(2);
    if (iVar8 != 0) {
      FUN_0488143c(local_2c0);
      ppppppuVar4 = (undefined8 ******)local_2c0[0];
      if (-1 < cStack_2a9) {
        ppppppuVar4 = local_2c0;
      }
      if ((DAT_0a391342 & 1) == 0) {
        uRam000000000a391338._0_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[8];
        uRam000000000a391338._1_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[9];
        uRam000000000a391338._2_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[10];
        uRam000000000a391338._3_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[0xb];
        uRam000000000a391338._4_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[0xc];
        uRam000000000a391338._5_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[0xd];
        uRam000000000a391338._6_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[0xe];
        uRam000000000a391338._7_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[0xf];
        DAT_0a391330 = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[0];
        DAT_0a391330_1._0_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[1];
        DAT_0a391330_1._1_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[2];
        DAT_0a391330_1._2_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[3];
        DAT_0a391330_1._3_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[4];
        DAT_0a391330_1._4_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[5];
        DAT_0a391330_1._5_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[6];
        DAT_0a391330_1._6_1_ = s_ai_sdk_manager_cSetAudioFmtParam_087e1ac0[7];
        DAT_0a391340 = 99;
        DAT_0a391342 = 1;
      }
      if ((DAT_0a3915c0 & 1) == 0) {
        DAT_0a3915b8._0_1_ = s_parent_iSendMsg_085977d0[8];
        DAT_0a3915b8._1_1_ = s_parent_iSendMsg_085977d0[9];
        DAT_0a3915b8._2_1_ = s_parent_iSendMsg_085977d0[10];
        DAT_0a3915b8._3_1_ = s_parent_iSendMsg_085977d0[0xb];
        DAT_0a3915b8._4_1_ = s_parent_iSendMsg_085977d0[0xc];
        DAT_0a3915b8._5_1_ = s_parent_iSendMsg_085977d0[0xd];
        DAT_0a3915b8._6_1_ = s_parent_iSendMsg_085977d0[0xe];
        DAT_0a3915b8._7_1_ = s_parent_iSendMsg_085977d0[0xf];
        DAT_0a3915c0 = 1;
      }
      FUN_05e1d050(auStack_260,2,ppppppuVar4,&DAT_0a391330,&DAT_0a3915b8,0xc6,0,0);
      local_130 = *param_2;
      if (-1 < *(char *)((long)param_2 + 0x17)) {
        local_130 = (long *****)param_2;
      }
      local_128 = 0;
      local_180 = (undefined1 *)0x0;
      if ((DAT_0a39190f & 1) == 0) {
        uVar15 = 0;
        do {
          uVar16 = *(undefined4 *)((long)&DAT_087e253a + uVar15);
          uVar6 = CONCAT12((char)((uint)uVar16 >> 8),(short)uVar16) & 0xff00ff;
          uVar17 = *(undefined4 *)((long)&DAT_087e2526 + uVar15 % 0x14);
          *(uint *)((long)&DAT_0a3918c7 + uVar15) =
               CONCAT13((char)((uint)uVar16 >> 0x18) + 0x8aU ^ (byte)((uint)uVar17 >> 0x18),
                        CONCAT12((char)((uint)uVar16 >> 0x10) + 0x8aU ^ (byte)((uint)uVar17 >> 0x10)
                                 ,CONCAT11((char)(uVar6 >> 0x10) + 0x8aU ^ (byte)((uint)uVar17 >> 8)
                                           ,(char)uVar6 + 0x8aU ^ (byte)uVar17)));
          uVar15 = uVar15 + 4;
        } while (uVar15 != 0x48);
        DAT_0a39190f = 1;
      }
      lVar13 = 8;
      iVar8 = param_3;
      do {
        lVar12 = lVar13;
        local_178[lVar12 + -8] = *(undefined1 *)((long)&DAT_0a3918c7 + (long)(iVar8 % 10 + 0x23));
        lVar13 = lVar12 + 1;
        uVar1 = iVar8 + 9;
        iVar8 = iVar8 / 10;
      } while (0x12 < uVar1);
      if (param_3 < 0) {
        local_178[lVar12 + -7] = 0x2d;
        lVar13 = lVar12 + 2;
      }
      local_178[lVar13 + -8] = 0;
      if (9 < lVar13) {
        puVar11 = local_178;
        puVar10 = &uStack_181 + lVar13;
        do {
          puVar11 = puVar11 + 1;
          uVar5 = *puVar10;
          puVar14 = puVar10 + -1;
          *puVar10 = puVar11[-1];
          puVar11[-1] = uVar5;
          puVar10 = puVar14;
        } while (puVar11 < puVar14);
      }
      local_180 = local_178;
      local_1d0 = (undefined8 *****)&local_1c8;
      lVar13 = 0;
      uVar15 = uVar9;
      do {
        lVar12 = lVar13;
        *(undefined1 *)((long)&local_1c8 + lVar12) = *(undefined1 *)(uVar15 % 10 + 0xa3918ea);
        bVar7 = 9 < uVar15;
        lVar13 = lVar12 + 1;
        uVar15 = uVar15 / 10;
      } while (bVar7);
      *(undefined1 *)((long)&local_1c8 + lVar12 + 1) = 0;
      if (8 < lVar12 + 8U) {
        puVar11 = (undefined1 *)((long)&local_1c8 + lVar12);
        puVar10 = (undefined1 *)((long)&local_1c8 + 1);
        do {
          uVar5 = *puVar11;
          *puVar11 = puVar10[-1];
          puVar10[-1] = uVar5;
          bVar7 = puVar10 < puVar11 + -1;
          puVar11 = puVar11 + -1;
          puVar10 = puVar10 + 1;
        } while (bVar7);
      }
      if ((DAT_0a39163a & 1) == 0) {
        uVar15 = 0;
        do {
          uVar16 = *(undefined4 *)((long)&DAT_087e20ce + uVar15);
          uVar6 = CONCAT12((char)((uint)uVar16 >> 8),(short)uVar16) & 0xff00ff;
          uVar17 = *(undefined4 *)((long)&DAT_087e20ba + uVar15 % 0x14);
          *(uint *)((long)&DAT_0a3915fb + uVar15) =
               CONCAT13((char)((uint)uVar16 >> 0x18) + 0x8aU ^ (byte)((uint)uVar17 >> 0x18),
                        CONCAT12((char)((uint)uVar16 >> 0x10) + 0x8aU ^ (byte)((uint)uVar17 >> 0x10)
                                 ,CONCAT11((char)(uVar6 >> 0x10) + 0x8aU ^ (byte)((uint)uVar17 >> 8)
                                           ,(char)uVar6 + 0x8aU ^ (byte)uVar17)));
          uVar15 = uVar15 + 4;
        } while (uVar15 != 0x3c);
        DAT_0a391637 = 0x5f25;
        DAT_0a391639 = 0;
        DAT_0a39163a = 1;
      }
      local_e0 = (long *****)&local_130;
      puStack_d8 = &local_180;
      local_d0 = &local_1d0;
      uStack_c0 = 0;
      uStack_c8 = 0;
      uStack_b0 = 0;
      uStack_b8 = 0;
      uStack_a0 = 0;
      local_a8 = 0;
      uStack_90 = 0;
      local_98 = 0;
      uStack_80 = 0;
      local_88 = 0;
      uStack_70 = 0;
      local_78 = 0;
      local_68 = 0;
      FUN_05e1d31c(auStack_260,&DAT_0a3915fb,&local_e0);
      thunk_FUN_05e1d0bc(auStack_260);
      if (cStack_2a9 < '\0') {
        uVar15 = CONCAT17(cStack_2a9,local_2b0);
LAB_0265f2d0:
        __ZdlPvm(local_2c0[0],uVar15 & 0x7fffffffffffffff);
      }
    }
  }
  if ((long)local_298 < 0) {
    __ZdlPvm(local_2a8,local_298 & 0x7fffffffffffffff);
  }
  FUN_0560d07c(&local_290);
LAB_0265f2f8:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_58) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return uVar9;
}


