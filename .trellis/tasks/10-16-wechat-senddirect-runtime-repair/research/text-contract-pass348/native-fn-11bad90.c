// Ghidra inferred pseudocode; requested=0x11bad90
// entry=011bad90 end=011bba2b

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_011bad90(long param_1,byte *param_2)

{
  uint uVar1;
  undefined8 *****pppppuVar2;
  undefined8 *puVar3;
  undefined1 uVar4;
  uint3 uVar5;
  bool bVar6;
  int iVar7;
  char *pcVar8;
  size_t sVar9;
  long *plVar10;
  long lVar11;
  code *pcVar12;
  undefined1 *puVar13;
  undefined1 *puVar14;
  long lVar15;
  ulong uVar16;
  int iVar17;
  undefined4 uVar18;
  undefined4 uVar19;
  int *local_288;
  undefined1 *puStack_280;
  undefined1 *local_278;
  undefined1 *local_270;
  undefined1 *puStack_268;
  undefined8 local_260 [2];
  undefined7 local_250;
  char cStack_249;
  undefined8 local_248 [2];
  undefined8 local_238 [2];
  undefined8 ****local_228 [2];
  undefined7 local_218;
  char cStack_211;
  long alStack_210 [3];
  long *local_1f8;
  long alStack_1f0 [3];
  long *local_1d8;
  undefined **local_1d0;
  long lStack_1c8;
  undefined8 local_1b8;
  undefined8 local_1b0;
  undefined8 local_1a8;
  undefined7 local_1a0;
  char cStack_199;
  long *local_160;
  long *local_158;
  long alStack_150 [3];
  long *local_138;
  long alStack_130 [3];
  long *local_118;
  long alStack_110 [3];
  long *local_f8;
  undefined8 uStack_f0;
  undefined8 local_e8;
  long local_e0;
  int *local_d0;
  undefined1 *puStack_c8;
  undefined1 *local_c0;
  undefined1 *local_b8;
  undefined1 *puStack_b0;
  undefined8 uStack_a8;
  undefined8 uStack_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 uStack_80;
  undefined8 uStack_78;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 uStack_60;
  undefined8 local_58;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  iVar7 = thunk_FUN_05e1d97c(2);
  if (iVar7 != 0) {
    FUN_0488143c(&local_1b0);
    puVar3 = local_1b0;
    if (-1 < cStack_199) {
      puVar3 = &local_1b0;
    }
    if ((DAT_0a2e5404 & 1) == 0) {
      uRam000000000a2e53f8._0_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[8];
      uRam000000000a2e53f8._1_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[9];
      uRam000000000a2e53f8._2_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[10];
      uRam000000000a2e53f8._3_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0xb];
      uRam000000000a2e53f8._4_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0xc];
      uRam000000000a2e53f8._5_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0xd];
      uRam000000000a2e53f8._6_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0xe];
      uRam000000000a2e53f8._7_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0xf];
      DAT_0a2e53f0 = s_login_view_modelDoCheckLoginQRCo_086185f0[0];
      DAT_0a2e53f0_1._0_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[1];
      DAT_0a2e53f0_1._1_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[2];
      DAT_0a2e53f0_1._2_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[3];
      DAT_0a2e53f0_1._3_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[4];
      DAT_0a2e53f0_1._4_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[5];
      DAT_0a2e53f0_1._5_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[6];
      DAT_0a2e53f0_1._6_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[7];
      DAT_0a2e5400 = (undefined4)DAT_084c8608;
      DAT_0a2e5404 = 1;
    }
    if ((DAT_0a2e5672 & 1) == 0) {
      uRam000000000a2e5668._0_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x88];
      uRam000000000a2e5668._1_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x89];
      uRam000000000a2e5668._2_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8a];
      uRam000000000a2e5668._3_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8b];
      uRam000000000a2e5668._4_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8c];
      uRam000000000a2e5668._5_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8d];
      uRam000000000a2e5668._6_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8e];
      uRam000000000a2e5668._7_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8f];
      DAT_0a2e5660 = s_login_view_modelDoCheckLoginQRCo_086185f0[0x80];
      DAT_0a2e5660_1._0_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x81];
      DAT_0a2e5660_1._1_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x82];
      DAT_0a2e5660_1._2_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x83];
      DAT_0a2e5660_1._3_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x84];
      DAT_0a2e5660_1._4_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x85];
      DAT_0a2e5660_1._5_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x86];
      DAT_0a2e5660_1._6_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x87];
      DAT_0a2e5670 = 0x65;
      DAT_0a2e5672 = 1;
    }
    FUN_05e1d050(&local_160,2,puVar3,&DAT_0a2e53f0,&DAT_0a2e5660,0x2b5,0,0);
    if ((DAT_0a2e5672 & 1) == 0) {
      uRam000000000a2e5668._0_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x88];
      uRam000000000a2e5668._1_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x89];
      uRam000000000a2e5668._2_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8a];
      uRam000000000a2e5668._3_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8b];
      uRam000000000a2e5668._4_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8c];
      uRam000000000a2e5668._5_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8d];
      uRam000000000a2e5668._6_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8e];
      uRam000000000a2e5668._7_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8f];
      DAT_0a2e5660 = s_login_view_modelDoCheckLoginQRCo_086185f0[0x80];
      DAT_0a2e5660_1._0_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x81];
      DAT_0a2e5660_1._1_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x82];
      DAT_0a2e5660_1._2_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x83];
      DAT_0a2e5660_1._3_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x84];
      DAT_0a2e5660_1._4_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x85];
      DAT_0a2e5660_1._5_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x86];
      DAT_0a2e5660_1._6_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x87];
      DAT_0a2e5670 = 0x65;
      DAT_0a2e5672 = 1;
    }
    uStack_68 = 0;
    local_70 = 0;
    local_58 = 0;
    uStack_60 = 0;
    uStack_88 = 0;
    local_90 = 0;
    uStack_78 = 0;
    uStack_80 = 0;
    uStack_a8 = 0;
    puStack_b0 = (undefined1 *)0x0;
    uStack_98 = 0;
    uStack_a0 = 0;
    puStack_c8 = (undefined1 *)0x0;
    local_d0 = (int *)0x0;
    local_b8 = (undefined1 *)0x0;
    local_c0 = (undefined1 *)0x0;
    FUN_05e1d31c(&local_160,&DAT_0a2e5660,&local_d0);
    thunk_FUN_05e1d0bc(&local_160);
    if (cStack_199 < '\0') {
      __ZdlPvm(local_1b0,CONCAT17(cStack_199,local_1a0) & 0x7fffffffffffffff);
    }
  }
  if (*(char *)(param_1 + 0x3a2) == '\x01') {
    iVar7 = thunk_FUN_05e1d97c(2);
    if (iVar7 == 0) goto LAB_011bb614;
    FUN_0488143c(&local_1b0);
    puVar3 = local_1b0;
    if (-1 < cStack_199) {
      puVar3 = &local_1b0;
    }
    if ((DAT_0a2e5404 & 1) == 0) {
      uRam000000000a2e53f8._0_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[8];
      uRam000000000a2e53f8._1_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[9];
      uRam000000000a2e53f8._2_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[10];
      uRam000000000a2e53f8._3_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0xb];
      uRam000000000a2e53f8._4_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0xc];
      uRam000000000a2e53f8._5_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0xd];
      uRam000000000a2e53f8._6_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0xe];
      uRam000000000a2e53f8._7_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0xf];
      DAT_0a2e53f0 = s_login_view_modelDoCheckLoginQRCo_086185f0[0];
      DAT_0a2e53f0_1._0_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[1];
      DAT_0a2e53f0_1._1_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[2];
      DAT_0a2e53f0_1._2_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[3];
      DAT_0a2e53f0_1._3_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[4];
      DAT_0a2e53f0_1._4_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[5];
      DAT_0a2e53f0_1._5_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[6];
      DAT_0a2e53f0_1._6_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[7];
      DAT_0a2e5400 = (undefined4)DAT_084c8608;
      DAT_0a2e5404 = 1;
    }
    if ((DAT_0a2e5672 & 1) == 0) {
      uRam000000000a2e5668._0_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x88];
      uRam000000000a2e5668._1_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x89];
      uRam000000000a2e5668._2_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8a];
      uRam000000000a2e5668._3_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8b];
      uRam000000000a2e5668._4_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8c];
      uRam000000000a2e5668._5_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8d];
      uRam000000000a2e5668._6_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8e];
      uRam000000000a2e5668._7_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8f];
      DAT_0a2e5660 = s_login_view_modelDoCheckLoginQRCo_086185f0[0x80];
      DAT_0a2e5660_1._0_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x81];
      DAT_0a2e5660_1._1_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x82];
      DAT_0a2e5660_1._2_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x83];
      DAT_0a2e5660_1._3_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x84];
      DAT_0a2e5660_1._4_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x85];
      DAT_0a2e5660_1._5_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x86];
      DAT_0a2e5660_1._6_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x87];
      DAT_0a2e5670 = 0x65;
      DAT_0a2e5672 = 1;
    }
    FUN_05e1d050(&local_160,2,puVar3,&DAT_0a2e53f0,&DAT_0a2e5660,0x2b7,0,0);
    if ((DAT_0a2e569a & 1) == 0) {
      _DAT_0a2e5674 = CONCAT44((int)DAT_084d4aa8,(int)DAT_084d86b0);
      uRam000000000a2e567c = CONCAT44((int)ram0x08618480,(int)DAT_085a5de8);
      _DAT_0a2e5684 = CONCAT44((int)DAT_084de6a8,(int)DAT_084de6a0);
      uRam000000000a2e568c = CONCAT44((int)DAT_085d7520,(int)DAT_084d8468);
      DAT_0a2e5694 = (undefined4)DAT_084c9958;
      DAT_0a2e5698 = 0x2e;
      DAT_0a2e569a = 1;
    }
    uStack_68 = 0;
    local_70 = 0;
    local_58 = 0;
    uStack_60 = 0;
    uStack_88 = 0;
    local_90 = 0;
    uStack_78 = 0;
    uStack_80 = 0;
    uStack_a8 = 0;
    puStack_b0 = (undefined1 *)0x0;
    uStack_98 = 0;
    uStack_a0 = 0;
    puStack_c8 = (undefined1 *)0x0;
    local_d0 = (int *)0x0;
    local_b8 = (undefined1 *)0x0;
    local_c0 = (undefined1 *)0x0;
    FUN_05e1d31c(&local_160,&DAT_0a2e5674,&local_d0);
  }
  else {
    if ((*param_2 & 1) != 0) {
      iVar7 = thunk_FUN_05e1d97c(2);
      if (iVar7 != 0) {
        FUN_0488143c(local_228);
        pppppuVar2 = (undefined8 *****)local_228[0];
        if (-1 < cStack_211) {
          pppppuVar2 = local_228;
        }
        if ((DAT_0a2e5404 & 1) == 0) {
          uRam000000000a2e53f8._0_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[8];
          uRam000000000a2e53f8._1_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[9];
          uRam000000000a2e53f8._2_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[10];
          uRam000000000a2e53f8._3_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0xb];
          uRam000000000a2e53f8._4_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0xc];
          uRam000000000a2e53f8._5_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0xd];
          uRam000000000a2e53f8._6_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0xe];
          uRam000000000a2e53f8._7_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0xf];
          DAT_0a2e53f0 = s_login_view_modelDoCheckLoginQRCo_086185f0[0];
          DAT_0a2e53f0_1._0_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[1];
          DAT_0a2e53f0_1._1_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[2];
          DAT_0a2e53f0_1._2_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[3];
          DAT_0a2e53f0_1._3_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[4];
          DAT_0a2e53f0_1._4_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[5];
          DAT_0a2e53f0_1._5_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[6];
          DAT_0a2e53f0_1._6_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[7];
          DAT_0a2e5400 = (undefined4)DAT_084c8608;
          DAT_0a2e5404 = 1;
        }
        if ((DAT_0a2e5672 & 1) == 0) {
          uRam000000000a2e5668._0_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x88];
          uRam000000000a2e5668._1_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x89];
          uRam000000000a2e5668._2_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8a];
          uRam000000000a2e5668._3_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8b];
          uRam000000000a2e5668._4_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8c];
          uRam000000000a2e5668._5_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8d];
          uRam000000000a2e5668._6_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8e];
          uRam000000000a2e5668._7_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8f];
          DAT_0a2e5660 = s_login_view_modelDoCheckLoginQRCo_086185f0[0x80];
          DAT_0a2e5660_1._0_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x81];
          DAT_0a2e5660_1._1_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x82];
          DAT_0a2e5660_1._2_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x83];
          DAT_0a2e5660_1._3_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x84];
          DAT_0a2e5660_1._4_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x85];
          DAT_0a2e5660_1._5_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x86];
          DAT_0a2e5660_1._6_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x87];
          DAT_0a2e5670 = 0x65;
          DAT_0a2e5672 = 1;
        }
        FUN_05e1d050(&local_160,2,pppppuVar2,&DAT_0a2e53f0,&DAT_0a2e5660,0x2c1,0,0);
        iVar7 = *(int *)(param_2 + 4);
        local_1b0 = (undefined8 *)0x0;
        if ((DAT_0a2e5767 & 1) == 0) {
          uVar16 = 0;
          do {
            uVar18 = *(undefined4 *)((long)&DAT_08618f46 + uVar16);
            uVar5 = CONCAT12((char)((uint)uVar18 >> 8),(short)uVar18) & 0xff00ff;
            uVar19 = *(undefined4 *)((long)&DAT_08618f32 + uVar16 % 0x14);
            *(uint *)((long)&DAT_0a2e571f + uVar16) =
                 CONCAT13((char)((uint)uVar18 >> 0x18) + 0x8aU ^ (byte)((uint)uVar19 >> 0x18),
                          CONCAT12((char)((uint)uVar18 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar19 >> 0x10),
                                   CONCAT11((char)(uVar5 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar19 >> 8),
                                            (char)uVar5 + 0x8aU ^ (byte)uVar19)));
            uVar16 = uVar16 + 4;
          } while (uVar16 != 0x48);
          DAT_0a2e5767 = 1;
        }
        lVar11 = 8;
        iVar17 = iVar7;
        do {
          lVar15 = lVar11;
          *(undefined1 *)((long)&local_1b0 + lVar15) =
               *(undefined1 *)((long)&DAT_0a2e571f + (long)(iVar17 % 10 + 0x23));
          lVar11 = lVar15 + 1;
          uVar1 = iVar17 + 9;
          iVar17 = iVar17 / 10;
        } while (0x12 < uVar1);
        if (iVar7 < 0) {
          *(undefined1 *)((long)&local_1b0 + lVar15 + 1) = 0x2d;
          lVar11 = lVar15 + 2;
        }
        *(undefined1 *)((long)&local_1b0 + lVar11) = 0;
        if (9 < lVar11) {
          puVar13 = (undefined1 *)((long)&local_1b8 + lVar11 + 7);
          puVar14 = (undefined1 *)((long)&local_1a8 + 1);
          do {
            uVar4 = *puVar13;
            *puVar13 = puVar14[-1];
            puVar14[-1] = uVar4;
            bVar6 = puVar14 < puVar13 + -1;
            puVar13 = puVar13 + -1;
            puVar14 = puVar14 + 1;
          } while (bVar6);
        }
        if ((DAT_0a2e56dc & 1) == 0) {
          _DAT_0a2e56b8 = CONCAT44((int)ram0x08618580,(int)DAT_08502968);
          uRam000000000a2e56c0 = CONCAT44((int)DAT_08618588,(int)DAT_085a9d78);
          _DAT_0a2e56c8 = CONCAT44((int)DAT_084c9958,(int)DAT_0855a638);
          uRam000000000a2e56d0 = CONCAT44((int)DAT_086185a0,(int)DAT_08618598);
          DAT_0a2e56d8 = (undefined4)DAT_086185a8;
          DAT_0a2e56dc = 1;
        }
        local_c0 = (undefined1 *)0x0;
        puStack_c8 = (undefined1 *)0x0;
        local_d0 = (int *)&local_1b0;
        puStack_b0 = (undefined1 *)0x0;
        local_b8 = (undefined1 *)0x0;
        uStack_a0 = 0;
        uStack_a8 = 0;
        local_90 = 0;
        uStack_98 = 0;
        uStack_80 = 0;
        uStack_88 = 0;
        local_70 = 0;
        uStack_78 = 0;
        uStack_60 = 0;
        uStack_68 = 0;
        local_58 = 0;
        local_1b0 = &local_1a8;
        FUN_05e1d31c(&local_160,&DAT_0a2e56b8,&local_d0);
        thunk_FUN_05e1d0bc(&local_160);
        if (cStack_211 < '\0') {
          __ZdlPvm(local_228[0],CONCAT17(cStack_211,local_218) & 0x7fffffffffffffff);
        }
      }
      uVar16 = *(ulong *)(param_2 + 0x28);
      if (-1 < (char)param_2[0x37]) {
        uVar16 = (ulong)param_2[0x37];
      }
      if (uVar16 != 0) {
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (param_1 + 0x178,param_2 + 0x20);
      }
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
                (param_1 + 0x1c0,"");
      iVar7 = *(int *)(param_2 + 4);
      if (iVar7 < 2) {
        if (iVar7 == 0) {
          if (*(char *)(param_1 + 0x239) == '\x01') {
            *(undefined1 *)(param_1 + 0x238) = 0;
            uVar18 = 2;
            if (*(char *)(param_1 + 0x23a) != '\0') {
              uVar18 = 3;
            }
            *(undefined4 *)(param_1 + 0x44) = 4;
            *(undefined4 *)(param_1 + 0x48) = uVar18;
            *(undefined4 *)(param_1 + 0x4c) = 3;
            FUN_011b519c(param_1);
          }
        }
        else if (iVar7 == 1) {
          __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                    (param_1 + 0x1c0,param_2 + 0x68);
          *(undefined4 *)(param_1 + 0x44) = 4;
          if (*(char *)(param_1 + 0x239) == '\x01') {
            uVar18 = 2;
            if (*(char *)(param_1 + 0x23a) != '\0') {
              uVar18 = 3;
            }
          }
          else {
            uVar18 = 1;
          }
          *(undefined4 *)(param_1 + 0x48) = uVar18;
          *(undefined4 *)(param_1 + 0x4c) = 3;
          lVar11 = (long)*(char *)(param_1 + 0x1d7);
          if (lVar11 < 0) {
            lVar11 = *(long *)(param_1 + 0x1c8);
          }
          FUN_011b519c(param_1);
          if (lVar11 != 0) goto LAB_011bb614;
        }
      }
      else {
        if (iVar7 == 2) {
          FUN_06fdf1f8(param_1 + 0x360);
          lVar11 = *(long *)(param_1 + 0x10);
          local_e8 = *(undefined8 *)(lVar11 + 8);
          local_e0 = *(long *)(lVar11 + 0x10);
          if (local_e0 != 0) {
            lVar11 = *(long *)(local_e0 + 0x10);
            *(long *)(local_e0 + 0x10) = lVar11 + 1;
          }
          local_158 = (long *)__Znwm(lVar11,0x20);
          local_158[2] = 0;
          *local_158 = (long)&PTR_FUN_09bf2c18;
          local_158[1] = 0;
          local_160 = local_158 + 3;
          *(undefined1 *)local_160 = 0;
          local_138 = (long *)0x0;
          local_118 = (long *)0x0;
          local_f8 = (long *)0x0;
          uStack_f0 = 0;
          pcVar8 = (char *)FUN_04e04548();
          if (pcVar8 == (char *)0x0) {
            sVar9 = 0xffffffff;
          }
          else {
            sVar9 = _strlen(pcVar8);
          }
          local_d0 = (int *)FUN_06ef8028(pcVar8,sVar9);
          FUN_0048b630(&local_160,&local_d0);
          if (*local_d0 != -1) {
            if (*local_d0 != 0) {
              LOAcquire();
              iVar7 = *local_d0;
              *local_d0 = iVar7 + -1;
              LORelease();
              if (iVar7 != 1) goto LAB_011bb690;
            }
            FUN_06ea14cc(local_d0,2,8);
          }
LAB_011bb690:
          if (local_e0 != 0) {
            __ZNSt3__119__shared_weak_count14__release_weakEv();
          }
          if (local_f8 == alStack_110) {
            pcVar12 = *(code **)(*local_f8 + 0x20);
LAB_011bb6c8:
            (*pcVar12)();
          }
          else if (local_f8 != (long *)0x0) {
            pcVar12 = *(code **)(*local_f8 + 0x28);
            goto LAB_011bb6c8;
          }
          if (local_118 == alStack_130) {
            pcVar12 = *(code **)(*local_118 + 0x20);
LAB_011bb6f8:
            (*pcVar12)();
          }
          else if (local_118 != (long *)0x0) {
            pcVar12 = *(code **)(*local_118 + 0x28);
            goto LAB_011bb6f8;
          }
          if (local_138 == alStack_150) {
            pcVar12 = *(code **)(*local_138 + 0x20);
LAB_011bb728:
            (*pcVar12)();
          }
          else if (local_138 != (long *)0x0) {
            pcVar12 = *(code **)(*local_138 + 0x28);
            goto LAB_011bb728;
          }
          plVar10 = local_158;
          if (local_158 != (long *)0x0) {
            LOAcquire();
            lVar11 = local_158[1];
            local_158[1] = lVar11 + -1;
            LORelease();
            if (lVar11 == 0) {
              (**(code **)(*local_158 + 0x10))(local_158);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
            }
          }
          *(undefined8 *)(param_1 + 0x44) = 0x400000004;
          *(undefined4 *)(param_1 + 0x4c) = 6;
          FUN_06fdf1f8(param_1 + 0x340);
          FUN_011b519c(param_1);
          if (((*(byte *)(param_1 + 0x3a0) & 1) != 0) || ((*(byte *)(param_1 + 0x3a1) & 1) != 0))
          goto LAB_011bb614;
          *(undefined1 *)(param_1 + 0x3a1) = 1;
          puStack_b0 = &SUB_aaaaaaaaaaaaaaaa;
          puStack_c8 = &SUB_aaaaaaaaaaaaaaaa;
          local_d0 = (int *)&SUB_aaaaaaaaaaaaaaaa;
          local_b8 = &SUB_aaaaaaaaaaaaaaaa;
          local_c0 = &SUB_aaaaaaaaaaaaaaaa;
          plVar10 = (long *)FUN_04669774();
          (**(code **)(*plVar10 + 0x88))(local_248);
          FUN_011b4650(local_238,local_248[0]);
          FUN_00255b9c(local_228,"");
          FUN_00255b9c(local_260,"");
          FUN_041009a0(&local_160,local_238[0],local_228,local_260);
          local_1d0 = &PTR_FUN_09cb4858;
          local_1b8 = &local_1d0;
          local_1d8 = (long *)0x0;
          local_1f8 = (long *)0x0;
          if ((DAT_0a2e5672 & 1) == 0) {
            uRam000000000a2e5668._0_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x88];
            uRam000000000a2e5668._1_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x89];
            uRam000000000a2e5668._2_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8a];
            uRam000000000a2e5668._3_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8b];
            uRam000000000a2e5668._4_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8c];
            uRam000000000a2e5668._5_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8d];
            uRam000000000a2e5668._6_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8e];
            uRam000000000a2e5668._7_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8f];
            DAT_0a2e5660 = s_login_view_modelDoCheckLoginQRCo_086185f0[0x80];
            DAT_0a2e5660_1._0_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x81];
            DAT_0a2e5660_1._1_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x82];
            DAT_0a2e5660_1._2_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x83];
            DAT_0a2e5660_1._3_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x84];
            DAT_0a2e5660_1._4_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x85];
            DAT_0a2e5660_1._5_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x86];
            DAT_0a2e5660_1._6_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x87];
            DAT_0a2e5670 = 0x65;
            DAT_0a2e5672 = 1;
          }
          if ((DAT_0a2e53e3 & 1) == 0) {
            uVar16 = 0;
            do {
              uVar18 = *(undefined4 *)((long)&DAT_08618987 + uVar16);
              uVar19 = *(undefined4 *)((long)&DAT_08618973 + uVar16 % 0x14);
              *(uint *)((long)&DAT_0a2e5390 + uVar16) =
                   CONCAT13((byte)((uint)uVar19 >> 0x18) ^ (byte)((uint)uVar18 >> 0x18),
                            CONCAT12((byte)((uint)uVar19 >> 0x10) ^ (byte)((uint)uVar18 >> 0x10),
                                     CONCAT11((byte)((uint)uVar19 >> 8) ^ (byte)((uint)uVar18 >> 8),
                                              (byte)uVar19 ^ (byte)uVar18)));
              uVar16 = uVar16 + 4;
            } while (uVar16 != 0x50);
            DAT_0a2e53e0 = 0x6363;
            DAT_0a2e53e2 = 0;
            DAT_0a2e53e3 = 1;
          }
          lStack_1c8 = param_1;
          FUN_0003bb6c(&local_1b0,&DAT_0a2e5660,&DAT_0a2e5390,0x2f2);
          FUN_002b3cdc(&local_d0,&local_160,&local_1d0,alStack_1f0,alStack_210,&local_1b0);
          if (local_1f8 == alStack_210) {
            pcVar12 = *(code **)(*local_1f8 + 0x20);
LAB_011bb928:
            (*pcVar12)();
          }
          else if (local_1f8 != (long *)0x0) {
            pcVar12 = *(code **)(*local_1f8 + 0x28);
            goto LAB_011bb928;
          }
          if (local_1d8 == alStack_1f0) {
            pcVar12 = *(code **)(*local_1d8 + 0x20);
LAB_011bb954:
            (*pcVar12)();
          }
          else if (local_1d8 != (long *)0x0) {
            pcVar12 = *(code **)(*local_1d8 + 0x28);
            goto LAB_011bb954;
          }
          if (local_1b8 == &local_1d0) {
            pcVar12 = (code *)(*local_1b8)[4];
LAB_011bb980:
            (*pcVar12)();
          }
          else if (local_1b8 != (undefined ***)0x0) {
            pcVar12 = (code *)(*local_1b8)[5];
            goto LAB_011bb980;
          }
          FUN_0021dbd0(&local_160);
          if (cStack_249 < '\0') {
            __ZdlPvm(local_260[0],CONCAT17(cStack_249,local_250) & 0x7fffffffffffffff);
          }
          if (cStack_211 < '\0') {
            __ZdlPvm(local_228[0],CONCAT17(cStack_211,local_218) & 0x7fffffffffffffff);
          }
          FUN_00129f68(local_238);
          FUN_00129f68(local_248);
          local_288 = local_d0;
          puStack_280 = puStack_c8;
          local_278 = local_c0;
          if (local_c0 != (undefined1 *)0x0) {
            *(long *)(local_c0 + 8) = *(long *)(local_c0 + 8) + 1;
          }
          local_270 = local_b8;
          puStack_268 = puStack_b0;
          lVar11 = 0;
          if (puStack_b0 != (undefined1 *)0x0) {
            lVar11 = *(long *)(puStack_b0 + 8);
            *(long *)(puStack_b0 + 8) = lVar11 + 1;
          }
          FUN_04b1ca4c(lVar11,param_1 + 0x268,0x32c,&local_288);
          FUN_0021dacc(&local_288);
          FUN_0021dacc(&local_d0);
          goto LAB_011bb614;
        }
        if ((iVar7 == 3) || (iVar7 == 4)) {
          FUN_011b77bc(param_1);
          goto LAB_011bb614;
        }
      }
      FUN_011b68c8(param_1);
      goto LAB_011bb614;
    }
    FUN_011b68c8(param_1);
    iVar7 = thunk_FUN_05e1d97c(4);
    if (iVar7 == 0) goto LAB_011bb614;
    FUN_0488143c(&local_1b0);
    puVar3 = local_1b0;
    if (-1 < cStack_199) {
      puVar3 = &local_1b0;
    }
    if ((DAT_0a2e5404 & 1) == 0) {
      uRam000000000a2e53f8._0_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[8];
      uRam000000000a2e53f8._1_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[9];
      uRam000000000a2e53f8._2_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[10];
      uRam000000000a2e53f8._3_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0xb];
      uRam000000000a2e53f8._4_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0xc];
      uRam000000000a2e53f8._5_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0xd];
      uRam000000000a2e53f8._6_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0xe];
      uRam000000000a2e53f8._7_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0xf];
      DAT_0a2e53f0 = s_login_view_modelDoCheckLoginQRCo_086185f0[0];
      DAT_0a2e53f0_1._0_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[1];
      DAT_0a2e53f0_1._1_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[2];
      DAT_0a2e53f0_1._2_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[3];
      DAT_0a2e53f0_1._3_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[4];
      DAT_0a2e53f0_1._4_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[5];
      DAT_0a2e53f0_1._5_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[6];
      DAT_0a2e53f0_1._6_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[7];
      DAT_0a2e5400 = (undefined4)DAT_084c8608;
      DAT_0a2e5404 = 1;
    }
    if ((DAT_0a2e5672 & 1) == 0) {
      uRam000000000a2e5668._0_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x88];
      uRam000000000a2e5668._1_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x89];
      uRam000000000a2e5668._2_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8a];
      uRam000000000a2e5668._3_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8b];
      uRam000000000a2e5668._4_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8c];
      uRam000000000a2e5668._5_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8d];
      uRam000000000a2e5668._6_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8e];
      uRam000000000a2e5668._7_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x8f];
      DAT_0a2e5660 = s_login_view_modelDoCheckLoginQRCo_086185f0[0x80];
      DAT_0a2e5660_1._0_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x81];
      DAT_0a2e5660_1._1_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x82];
      DAT_0a2e5660_1._2_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x83];
      DAT_0a2e5660_1._3_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x84];
      DAT_0a2e5660_1._4_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x85];
      DAT_0a2e5660_1._5_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x86];
      DAT_0a2e5660_1._6_1_ = s_login_view_modelDoCheckLoginQRCo_086185f0[0x87];
      DAT_0a2e5670 = 0x65;
      DAT_0a2e5672 = 1;
    }
    FUN_05e1d050(&local_160,4,puVar3,&DAT_0a2e53f0,&DAT_0a2e5660,0x2be,0,0);
    if ((DAT_0a2e56b5 & 1) == 0) {
      _DAT_0a2e569c = CONCAT44((int)ram0x08618580,(int)DAT_08502968);
      uRam000000000a2e56a4 = CONCAT44((int)DAT_08618588,(int)DAT_085a9d78);
      DAT_0a2e56ac = CONCAT44((int)DAT_08618590,(int)DAT_08503690);
      DAT_0a2e56b4 = 0;
      DAT_0a2e56b5 = 1;
    }
    uStack_68 = 0;
    local_70 = 0;
    local_58 = 0;
    uStack_60 = 0;
    uStack_88 = 0;
    local_90 = 0;
    uStack_78 = 0;
    uStack_80 = 0;
    uStack_a8 = 0;
    puStack_b0 = (undefined1 *)0x0;
    uStack_98 = 0;
    uStack_a0 = 0;
    puStack_c8 = (undefined1 *)0x0;
    local_d0 = (int *)0x0;
    local_b8 = (undefined1 *)0x0;
    local_c0 = (undefined1 *)0x0;
    FUN_05e1d31c(&local_160,&DAT_0a2e569c,&local_d0);
  }
  thunk_FUN_05e1d0bc(&local_160);
  if (cStack_199 < '\0') {
    __ZdlPvm(local_1b0,CONCAT17(cStack_199,local_1a0) & 0x7fffffffffffffff);
  }
LAB_011bb614:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


