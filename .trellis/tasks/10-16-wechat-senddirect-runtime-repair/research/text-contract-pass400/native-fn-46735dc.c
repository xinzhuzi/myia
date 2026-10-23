// Ghidra inferred pseudocode; requested=0x46735dc
// entry=046735dc end=04674f3f

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_046735dc(long param_1,uint *param_2)

{
  undefined8 ****ppppuVar1;
  uint uVar2;
  undefined1 uVar3;
  uint3 uVar4;
  bool bVar5;
  long lVar6;
  int iVar7;
  undefined8 uVar8;
  undefined8 *puVar9;
  long *plVar10;
  code *pcVar11;
  uint uVar12;
  undefined1 *puVar13;
  undefined1 *puVar14;
  ulong uVar15;
  long lVar16;
  undefined4 uVar17;
  undefined4 uVar18;
  undefined8 local_3f0;
  undefined8 uStack_3e8;
  ulong local_3e0;
  undefined8 local_3d0;
  undefined8 uStack_3c8;
  ulong local_3c0;
  undefined8 local_3b0;
  undefined8 uStack_3a8;
  ulong local_3a0;
  undefined8 local_390;
  undefined8 uStack_388;
  ulong local_380;
  undefined8 ***local_378;
  long *local_370;
  undefined7 local_368;
  char cStack_361;
  undefined8 local_360;
  undefined8 uStack_358;
  ulong local_350;
  undefined8 local_340;
  undefined8 uStack_338;
  ulong local_330;
  undefined8 local_320;
  undefined8 uStack_318;
  ulong local_310;
  undefined **local_300;
  code *pcStack_2f8;
  undefined ***local_2e8;
  undefined **local_2e0;
  code *pcStack_2d8;
  undefined ***local_2c8;
  undefined **local_2c0;
  code *pcStack_2b8;
  undefined ***local_2a8;
  undefined **local_2a0;
  code *pcStack_298;
  undefined ***local_288;
  undefined **local_280;
  code *pcStack_278;
  undefined ***local_268;
  undefined8 ***local_260;
  undefined1 *puStack_258;
  undefined1 *local_250;
  undefined1 *puStack_248;
  undefined1 *local_240;
  undefined1 *puStack_238;
  undefined1 *puStack_230;
  undefined1 *puStack_228;
  undefined1 *local_220;
  undefined **local_210;
  code *pcStack_208;
  undefined ***local_1f8;
  undefined **local_1f0;
  code *local_1e8;
  undefined ***local_1d8;
  undefined8 *local_1d0;
  undefined8 uStack_1c8;
  undefined1 *puStack_1c0;
  undefined1 *puStack_1b8;
  undefined1 *local_1b0;
  undefined1 *puStack_1a8;
  undefined1 *puStack_1a0;
  undefined1 *puStack_198;
  undefined1 *local_190;
  undefined8 ***local_180;
  long *plStack_178;
  undefined1 *local_170;
  undefined1 *puStack_168;
  undefined1 *local_160;
  undefined1 *puStack_158;
  undefined1 *puStack_150;
  undefined1 *puStack_148;
  undefined1 *local_140;
  undefined8 **local_f0;
  long *plStack_e8;
  undefined8 uStack_e0;
  undefined8 local_d8;
  undefined8 uStack_d0;
  undefined8 local_c8;
  undefined8 uStack_c0;
  undefined8 local_b8;
  undefined8 uStack_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  undefined8 local_78;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  iVar7 = thunk_FUN_05e1d97c(2);
  if (iVar7 != 0) {
    FUN_0488143c(&local_260);
    ppppuVar1 = (undefined8 ****)local_260;
    if (-1 < (long)local_250) {
      ppppuVar1 = &local_260;
    }
    if ((DAT_0a45df8a & 1) == 0) {
      DAT_0a45df80._0_1_ = s_input_ackernel_cpadV_08a133a0[8];
      DAT_0a45df80._1_1_ = s_input_ackernel_cpadV_08a133a0[9];
      DAT_0a45df80._2_1_ = s_input_ackernel_cpadV_08a133a0[10];
      DAT_0a45df80._3_1_ = s_input_ackernel_cpadV_08a133a0[0xb];
      DAT_0a45df80._4_1_ = s_input_ackernel_cpadV_08a133a0[0xc];
      DAT_0a45df80._5_1_ = s_input_ackernel_cpadV_08a133a0[0xd];
      DAT_0a45df80._6_1_ = s_input_ackernel_cpadV_08a133a0[0xe];
      DAT_0a45df80._7_1_ = s_input_ackernel_cpadV_08a133a0[0xf];
      DAT_0a45df88 = 99;
      DAT_0a45df8a = 1;
    }
    if ((DAT_0a45e49d & 1) == 0) {
      _DAT_0a45e488 = CONCAT44((int)DAT_085465e8,(int)DAT_088899e8);
      uRam000000000a45e490 = CONCAT44((int)DAT_084d82b0,(int)DAT_087f2358);
      DAT_0a45e498 = (undefined4)DAT_084d82b8;
      DAT_0a45e49c = 0;
      DAT_0a45e49d = 1;
    }
    FUN_05e1d050(&local_180,2,ppppuVar1,&DAT_0a45df80,&DAT_0a45e488,0x4a5,0,0);
    uVar12 = *param_2;
    local_1d0 = (undefined8 **)0x0;
    local_1d0 = &uStack_1c8;
    if ((DAT_0a45e65a & 1) == 0) {
      uVar15 = 0;
      do {
        uVar17 = *(undefined4 *)((long)&DAT_08a1498d + uVar15);
        uVar4 = CONCAT12((char)((uint)uVar17 >> 8),(short)uVar17) & 0xff00ff;
        uVar18 = *(undefined4 *)((long)&DAT_08a14979 + uVar15 % 0x14);
        *(uint *)((long)&DAT_0a45e612 + uVar15) =
             CONCAT13((char)((uint)uVar17 >> 0x18) + 0x8aU ^ (byte)((uint)uVar18 >> 0x18),
                      CONCAT12((char)((uint)uVar17 >> 0x10) + 0x8aU ^ (byte)((uint)uVar18 >> 0x10),
                               CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^ (byte)((uint)uVar18 >> 8),
                                        (char)uVar4 + 0x8aU ^ (byte)uVar18)));
        uVar15 = uVar15 + 4;
      } while (uVar15 != 0x48);
      DAT_0a45e65a = 1;
    }
    uVar15 = (ulong)uVar12;
    lVar6 = 0;
    do {
      lVar16 = lVar6;
      uVar12 = (uint)uVar15;
      *(undefined1 *)((long)&uStack_1c8 + lVar16) =
           *(undefined1 *)((long)&DAT_0a45e612 + (ulong)(uVar12 + (int)(uVar15 / 10) * -10 + 0x23));
      uVar15 = uVar15 / 10;
      lVar6 = lVar16 + 1;
    } while (9 < uVar12);
    *(undefined1 *)((long)&uStack_1c8 + lVar16 + 1) = 0;
    if (8 < lVar16 + 8U) {
      puVar13 = (undefined1 *)((long)&uStack_1c8 + lVar16);
      puVar14 = (undefined1 *)((long)&uStack_1c8 + 1);
      do {
        uVar3 = *puVar13;
        *puVar13 = puVar14[-1];
        puVar14[-1] = uVar3;
        bVar5 = puVar14 < puVar13 + -1;
        puVar13 = puVar13 + -1;
        puVar14 = puVar14 + 1;
      } while (bVar5);
    }
    if ((DAT_0a45e4c6 & 1) == 0) {
      _DAT_0a45e4a0 = CONCAT44((int)DAT_084d8630,(int)DAT_0889c248);
      uRam000000000a45e4a8 = CONCAT44((int)DAT_084e14f8,(int)DAT_08a13500);
      _DAT_0a45e4b0 = CONCAT44((int)DAT_086e5d08,(int)DAT_08a13508);
      uRam000000000a45e4b8 = CONCAT44((int)ram0x084e31f0,(int)DAT_088546d8);
      DAT_0a45e4c0 = (undefined4)DAT_084c85d8;
      DAT_0a45e4c4 = 0x5f;
      DAT_0a45e4c6 = 1;
    }
    uStack_e0 = 0;
    plStack_e8 = (long *)0x0;
    local_f0 = &local_1d0;
    uStack_d0 = 0;
    local_d8 = 0;
    uStack_c0 = 0;
    local_c8 = 0;
    uStack_b0 = 0;
    local_b8 = 0;
    uStack_a0 = 0;
    local_a8 = 0;
    uStack_90 = 0;
    local_98 = 0;
    uStack_80 = 0;
    local_88 = 0;
    local_78 = 0;
    FUN_05e1d31c(&local_180,&DAT_0a45e4a0,&local_f0);
    thunk_FUN_05e1d0bc(&local_180);
    if ((long)local_250 < 0) {
      __ZdlPvm(local_260,(ulong)local_250 & 0x7fffffffffffffff);
    }
  }
  local_190 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1a8 = &SUB_aaaaaaaaaaaaaaaa;
  local_1b0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_198 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1a0 = &SUB_aaaaaaaaaaaaaaaa;
  uStack_1c8 = &SUB_aaaaaaaaaaaaaaaa;
  local_1d0 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
  puStack_1b8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1c0 = &SUB_aaaaaaaaaaaaaaaa;
  local_1f0 = &PTR_FUN_09e5b308;
  local_1e8 = FUN_04a166b0;
  local_1d8 = &local_1f0;
  if (DAT_0a51ece8._7_1_ < '\0') {
    FUN_00018d20(&local_320,DAT_0a51ecd8,DAT_0a51ece0);
  }
  else {
    uStack_318 = DAT_0a51ece0;
    local_320 = DAT_0a51ecd8;
    local_310 = CONCAT17(DAT_0a51ece8._7_1_,(undefined7)DAT_0a51ece8);
  }
  FUN_041105c4(&local_1d0,&local_1f0,2,&local_320);
  if ((long)local_310 < 0) {
    __ZdlPvm(local_320,local_310 & 0x7fffffffffffffff);
  }
  if (local_1d8 == &local_1f0) {
    pcVar11 = (code *)(*local_1d8)[4];
LAB_046739a0:
    (*pcVar11)();
  }
  else if (local_1d8 != (undefined ***)0x0) {
    pcVar11 = (code *)(*local_1d8)[5];
    goto LAB_046739a0;
  }
  if (*(long *)(param_1 + 0x2b8) != 0) {
    iVar7 = thunk_FUN_05e1d97c(2);
    if (iVar7 != 0) {
      FUN_0488143c(&local_260);
      ppppuVar1 = (undefined8 ****)local_260;
      if (-1 < (long)local_250) {
        ppppuVar1 = &local_260;
      }
      if ((DAT_0a45df8a & 1) == 0) {
        DAT_0a45df80._0_1_ = s_input_ackernel_cpadV_08a133a0[8];
        DAT_0a45df80._1_1_ = s_input_ackernel_cpadV_08a133a0[9];
        DAT_0a45df80._2_1_ = s_input_ackernel_cpadV_08a133a0[10];
        DAT_0a45df80._3_1_ = s_input_ackernel_cpadV_08a133a0[0xb];
        DAT_0a45df80._4_1_ = s_input_ackernel_cpadV_08a133a0[0xc];
        DAT_0a45df80._5_1_ = s_input_ackernel_cpadV_08a133a0[0xd];
        DAT_0a45df80._6_1_ = s_input_ackernel_cpadV_08a133a0[0xe];
        DAT_0a45df80._7_1_ = s_input_ackernel_cpadV_08a133a0[0xf];
        DAT_0a45df88 = 99;
        DAT_0a45df8a = 1;
      }
      if ((DAT_0a45e49d & 1) == 0) {
        _DAT_0a45e488 = CONCAT44((int)DAT_085465e8,(int)DAT_088899e8);
        uRam000000000a45e490 = CONCAT44((int)DAT_084d82b0,(int)DAT_087f2358);
        DAT_0a45e498 = (undefined4)DAT_084d82b8;
        DAT_0a45e49c = 0;
        DAT_0a45e49d = 1;
      }
      FUN_05e1d050(&local_180,2,ppppuVar1,&DAT_0a45df80,&DAT_0a45e488,0x4ae,0,0);
      if ((DAT_0a45e4e2 & 1) == 0) {
        _DAT_0a45e4c8 = CONCAT44((int)DAT_084d8630,(int)DAT_0889c248);
        uRam000000000a45e4d0 = CONCAT44((int)DAT_087e2d38,(int)DAT_08a13510);
        DAT_0a45e4d8 = CONCAT44((int)DAT_0853f980,(int)DAT_084e49f0);
        DAT_0a45e4e0 = 0x70;
        DAT_0a45e4e2 = 1;
      }
      local_88 = 0;
      uStack_90 = 0;
      local_78 = 0;
      uStack_80 = 0;
      local_a8 = 0;
      uStack_b0 = 0;
      local_98 = 0;
      uStack_a0 = 0;
      local_c8 = 0;
      uStack_d0 = 0;
      local_b8 = 0;
      uStack_c0 = 0;
      plStack_e8 = (long *)0x0;
      local_f0 = (undefined8 ***)0x0;
      local_d8 = 0;
      uStack_e0 = 0;
      FUN_05e1d31c(&local_180,&DAT_0a45e4c8,&local_f0);
      thunk_FUN_05e1d0bc(&local_180);
      if ((long)local_250 < 0) {
        __ZdlPvm(local_260,(ulong)local_250 & 0x7fffffffffffffff);
      }
    }
    FUN_04673144();
  }
  uVar2 = *param_2;
  uVar12 = *(uint *)(param_1 + 0x2b0);
  FUN_04668f94(param_1,4);
  iVar7 = thunk_FUN_05e1d97c(2);
  if (iVar7 != 0) {
    FUN_0488143c(&local_260);
    ppppuVar1 = (undefined8 ****)local_260;
    if (-1 < (long)local_250) {
      ppppuVar1 = &local_260;
    }
    if ((DAT_0a45df8a & 1) == 0) {
      DAT_0a45df80._0_1_ = s_input_ackernel_cpadV_08a133a0[8];
      DAT_0a45df80._1_1_ = s_input_ackernel_cpadV_08a133a0[9];
      DAT_0a45df80._2_1_ = s_input_ackernel_cpadV_08a133a0[10];
      DAT_0a45df80._3_1_ = s_input_ackernel_cpadV_08a133a0[0xb];
      DAT_0a45df80._4_1_ = s_input_ackernel_cpadV_08a133a0[0xc];
      DAT_0a45df80._5_1_ = s_input_ackernel_cpadV_08a133a0[0xd];
      DAT_0a45df80._6_1_ = s_input_ackernel_cpadV_08a133a0[0xe];
      DAT_0a45df80._7_1_ = s_input_ackernel_cpadV_08a133a0[0xf];
      DAT_0a45df88 = 99;
      DAT_0a45df8a = 1;
    }
    if ((DAT_0a45e49d & 1) == 0) {
      _DAT_0a45e488 = CONCAT44((int)DAT_085465e8,(int)DAT_088899e8);
      uRam000000000a45e490 = CONCAT44((int)DAT_084d82b0,(int)DAT_087f2358);
      DAT_0a45e498 = (undefined4)DAT_084d82b8;
      DAT_0a45e49c = 0;
      DAT_0a45e49d = 1;
    }
    FUN_05e1d050(&local_180,2,ppppuVar1,&DAT_0a45df80,&DAT_0a45e488,0x4c5,0,0);
    if ((DAT_0a45e4fd & 1) == 0) {
      _DAT_0a45e4e4 = CONCAT44((int)DAT_084d8630,(int)DAT_0889c248);
      uRam000000000a45e4ec = CONCAT44((int)DAT_08a13518,(int)DAT_08a13510);
      DAT_0a45e4f4 = CONCAT44((int)DAT_085465e8,(int)DAT_084d7880);
      DAT_0a45e4fc = 0;
      DAT_0a45e4fd = 1;
    }
    local_88 = 0;
    uStack_90 = 0;
    local_78 = 0;
    uStack_80 = 0;
    local_a8 = 0;
    uStack_b0 = 0;
    local_98 = 0;
    uStack_a0 = 0;
    local_c8 = 0;
    uStack_d0 = 0;
    local_b8 = 0;
    uStack_c0 = 0;
    plStack_e8 = (long *)0x0;
    local_f0 = (undefined8 ***)0x0;
    local_d8 = 0;
    uStack_e0 = 0;
    FUN_05e1d31c(&local_180,&DAT_0a45e4e4,&local_f0);
    thunk_FUN_05e1d0bc(&local_180);
    if ((long)local_250 < 0) {
      __ZdlPvm(local_260,(ulong)local_250 & 0x7fffffffffffffff);
    }
  }
  local_140 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_158 = &SUB_aaaaaaaaaaaaaaaa;
  local_160 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_148 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_150 = &SUB_aaaaaaaaaaaaaaaa;
  plStack_178 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_180 = (undefined8 ***)&SUB_aaaaaaaaaaaaaaaa;
  puStack_168 = &SUB_aaaaaaaaaaaaaaaa;
  local_170 = &SUB_aaaaaaaaaaaaaaaa;
  local_210 = &PTR_FUN_09e5b308;
  pcStack_208 = FUN_04a166b0;
  local_1f8 = &local_210;
  if (DAT_0a51ee08._7_1_ < '\0') {
    FUN_00018d20(&local_340,DAT_0a51edf8,DAT_0a51ee00);
  }
  else {
    uStack_338 = DAT_0a51ee00;
    local_340 = DAT_0a51edf8;
    local_330 = CONCAT17(DAT_0a51ee08._7_1_,(undefined7)DAT_0a51ee08);
  }
  FUN_041105c4(&local_180,&local_210,2,&local_340);
  if ((long)local_330 < 0) {
    __ZdlPvm(local_340,local_330 & 0x7fffffffffffffff);
  }
  if (local_1f8 == &local_210) {
    pcVar11 = (code *)(*local_1f8)[4];
LAB_04673d78:
    (*pcVar11)();
  }
  else if (local_1f8 != (undefined ***)0x0) {
    pcVar11 = (code *)(*local_1f8)[5];
    goto LAB_04673d78;
  }
  iVar7 = FUN_0478cd04(*param_2);
  if (iVar7 == 0) {
    uVar8 = 1;
  }
  else {
    uVar8 = FUN_04675280(1000);
  }
  FUN_04111974(&local_180);
  if (((uVar12 & 0xfffffffe) == 2) && ((uVar2 & 0xfffffffb) != 1)) {
    local_220 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_238 = &SUB_aaaaaaaaaaaaaaaa;
    local_240 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_228 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_230 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_258 = &SUB_aaaaaaaaaaaaaaaa;
    local_260 = (undefined8 ***)&SUB_aaaaaaaaaaaaaaaa;
    puStack_248 = &SUB_aaaaaaaaaaaaaaaa;
    local_250 = &SUB_aaaaaaaaaaaaaaaa;
    local_280 = &PTR_FUN_09e5b308;
    pcStack_278 = FUN_04a166b0;
    local_268 = &local_280;
    if (DAT_0a51eda8._7_1_ < '\0') {
      FUN_00018d20(&local_360,DAT_0a51ed98,DAT_0a51eda0);
    }
    else {
      uStack_358 = DAT_0a51eda0;
      local_360 = DAT_0a51ed98;
      local_350 = CONCAT17(DAT_0a51eda8._7_1_,(undefined7)DAT_0a51eda8);
    }
    FUN_041105c4(&local_260,&local_280,2,&local_360);
    if ((long)local_350 < 0) {
      __ZdlPvm(local_360,local_350 & 0x7fffffffffffffff);
    }
    if (local_268 == &local_280) {
      pcVar11 = (code *)(*local_268)[4];
LAB_04673e60:
      (*pcVar11)();
    }
    else if (local_268 != (undefined ***)0x0) {
      pcVar11 = (code *)(*local_268)[5];
      goto LAB_04673e60;
    }
    iVar7 = thunk_FUN_05e1d97c(2);
    if (iVar7 != 0) {
      FUN_0488143c(&local_378);
      ppppuVar1 = (undefined8 ****)local_378;
      if (-1 < cStack_361) {
        ppppuVar1 = &local_378;
      }
      if ((DAT_0a45df8a & 1) == 0) {
        DAT_0a45df80._0_1_ = s_input_ackernel_cpadV_08a133a0[8];
        DAT_0a45df80._1_1_ = s_input_ackernel_cpadV_08a133a0[9];
        DAT_0a45df80._2_1_ = s_input_ackernel_cpadV_08a133a0[10];
        DAT_0a45df80._3_1_ = s_input_ackernel_cpadV_08a133a0[0xb];
        DAT_0a45df80._4_1_ = s_input_ackernel_cpadV_08a133a0[0xc];
        DAT_0a45df80._5_1_ = s_input_ackernel_cpadV_08a133a0[0xd];
        DAT_0a45df80._6_1_ = s_input_ackernel_cpadV_08a133a0[0xe];
        DAT_0a45df80._7_1_ = s_input_ackernel_cpadV_08a133a0[0xf];
        DAT_0a45df88 = 99;
        DAT_0a45df8a = 1;
      }
      if ((DAT_0a45e49d & 1) == 0) {
        _DAT_0a45e488 = CONCAT44((int)DAT_085465e8,(int)DAT_088899e8);
        uRam000000000a45e490 = CONCAT44((int)DAT_084d82b0,(int)DAT_087f2358);
        DAT_0a45e498 = (undefined4)DAT_084d82b8;
        DAT_0a45e49c = 0;
        DAT_0a45e49d = 1;
      }
      FUN_05e1d050(&local_180,2,ppppuVar1,&DAT_0a45df80,&DAT_0a45e488,0x4d4,0,0);
      if ((DAT_0a45e518 & 1) == 0) {
        _DAT_0a45e500 = CONCAT44((int)DAT_084d8630,(int)DAT_0889c248);
        uRam000000000a45e508 = CONCAT44((int)DAT_08a13528,(int)DAT_08a13520);
        DAT_0a45e510 = CONCAT44((int)DAT_08509948,(int)DAT_08546610);
        DAT_0a45e518 = 1;
      }
      local_88 = 0;
      uStack_90 = 0;
      local_78 = 0;
      uStack_80 = 0;
      local_a8 = 0;
      uStack_b0 = 0;
      local_98 = 0;
      uStack_a0 = 0;
      local_c8 = 0;
      uStack_d0 = 0;
      local_b8 = 0;
      uStack_c0 = 0;
      plStack_e8 = (long *)0x0;
      local_f0 = (undefined8 ***)0x0;
      local_d8 = 0;
      uStack_e0 = 0;
      FUN_05e1d31c(&local_180,&DAT_0a45e500,&local_f0);
      thunk_FUN_05e1d0bc(&local_180);
      if (cStack_361 < '\0') {
        __ZdlPvm(local_378,CONCAT17(cStack_361,local_368) & 0x7fffffffffffffff);
      }
    }
    FUN_046758cc(param_1,param_2);
    FUN_04111974(&local_260);
  }
  local_220 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_238 = &SUB_aaaaaaaaaaaaaaaa;
  local_240 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_228 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_230 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_258 = &SUB_aaaaaaaaaaaaaaaa;
  local_260 = (undefined8 ***)&SUB_aaaaaaaaaaaaaaaa;
  puStack_248 = &SUB_aaaaaaaaaaaaaaaa;
  local_250 = &SUB_aaaaaaaaaaaaaaaa;
  local_2a0 = &PTR_FUN_09e5b308;
  pcStack_298 = FUN_04a166b0;
  local_288 = &local_2a0;
  if (DAT_0a51edc0._7_1_ < '\0') {
    FUN_00018d20(&local_390,DAT_0a51edb0,DAT_0a51edb8);
  }
  else {
    uStack_388 = DAT_0a51edb8;
    local_390 = DAT_0a51edb0;
    local_380 = CONCAT17(DAT_0a51edc0._7_1_,(undefined7)DAT_0a51edc0);
  }
  FUN_041105c4(&local_260,&local_2a0,2,&local_390);
  if ((long)local_380 < 0) {
    __ZdlPvm(local_390,local_380 & 0x7fffffffffffffff);
  }
  if (local_288 == &local_2a0) {
    pcVar11 = (code *)(*local_288)[4];
LAB_0467409c:
    (*pcVar11)();
  }
  else if (local_288 != (undefined ***)0x0) {
    pcVar11 = (code *)(*local_288)[5];
    goto LAB_0467409c;
  }
  iVar7 = thunk_FUN_05e1d97c(2);
  if (iVar7 != 0) {
    FUN_0488143c(&local_378);
    ppppuVar1 = (undefined8 ****)local_378;
    if (-1 < cStack_361) {
      ppppuVar1 = &local_378;
    }
    if ((DAT_0a45df8a & 1) == 0) {
      DAT_0a45df80._0_1_ = s_input_ackernel_cpadV_08a133a0[8];
      DAT_0a45df80._1_1_ = s_input_ackernel_cpadV_08a133a0[9];
      DAT_0a45df80._2_1_ = s_input_ackernel_cpadV_08a133a0[10];
      DAT_0a45df80._3_1_ = s_input_ackernel_cpadV_08a133a0[0xb];
      DAT_0a45df80._4_1_ = s_input_ackernel_cpadV_08a133a0[0xc];
      DAT_0a45df80._5_1_ = s_input_ackernel_cpadV_08a133a0[0xd];
      DAT_0a45df80._6_1_ = s_input_ackernel_cpadV_08a133a0[0xe];
      DAT_0a45df80._7_1_ = s_input_ackernel_cpadV_08a133a0[0xf];
      DAT_0a45df88 = 99;
      DAT_0a45df8a = 1;
    }
    if ((DAT_0a45e49d & 1) == 0) {
      _DAT_0a45e488 = CONCAT44((int)DAT_085465e8,(int)DAT_088899e8);
      uRam000000000a45e490 = CONCAT44((int)DAT_084d82b0,(int)DAT_087f2358);
      DAT_0a45e498 = (undefined4)DAT_084d82b8;
      DAT_0a45e49c = 0;
      DAT_0a45e49d = 1;
    }
    FUN_05e1d050(&local_180,2,ppppuVar1,&DAT_0a45df80,&DAT_0a45e488,0x4da,0,0);
    if ((DAT_0a45e53e & 1) == 0) {
      _DAT_0a45e51c = CONCAT44((int)DAT_084d8630,(int)DAT_0889c248);
      uRam000000000a45e524 = CONCAT44((int)DAT_08a13538,(int)DAT_08a13530);
      _DAT_0a45e52c = CONCAT44((int)DAT_08996e20,(int)DAT_08a13540);
      uRam000000000a45e534 = CONCAT44((int)DAT_084e14f8,(int)DAT_08996e28);
      DAT_0a45e53c = 0x74;
      DAT_0a45e53e = 1;
    }
    local_88 = 0;
    uStack_90 = 0;
    local_78 = 0;
    uStack_80 = 0;
    local_a8 = 0;
    uStack_b0 = 0;
    local_98 = 0;
    uStack_a0 = 0;
    local_c8 = 0;
    uStack_d0 = 0;
    local_b8 = 0;
    uStack_c0 = 0;
    plStack_e8 = (long *)0x0;
    local_f0 = (undefined8 ***)0x0;
    local_d8 = 0;
    uStack_e0 = 0;
    FUN_05e1d31c(&local_180,&DAT_0a45e51c,&local_f0);
    thunk_FUN_05e1d0bc(&local_180);
    if (cStack_361 < '\0') {
      __ZdlPvm(local_378,CONCAT17(cStack_361,local_368) & 0x7fffffffffffffff);
    }
  }
  local_170 = &SUB_aaaaaaaaaaaaaaaa;
  plStack_178 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_180 = (undefined8 ***)&SUB_aaaaaaaaaaaaaaaa;
  puVar9 = (undefined8 *)(**(code **)(*DAT_0a45df38 + 0x28))();
  if (*(char *)((long)puVar9 + 0x17) < '\0') {
    FUN_00018d20(&local_180,*puVar9,puVar9[1]);
  }
  else {
    plStack_178 = (long *)puVar9[1];
    local_180 = (undefined8 ***)*puVar9;
    local_170 = (undefined1 *)puVar9[2];
  }
  FUN_0466fbd0(DAT_0a45df38,&local_180);
  if ((long)local_170 < 0) {
    __ZdlPvm(local_180,(ulong)local_170 & 0x7fffffffffffffff);
  }
  FUN_04111974(&local_260);
  local_220 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_238 = &SUB_aaaaaaaaaaaaaaaa;
  local_240 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_228 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_230 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_258 = &SUB_aaaaaaaaaaaaaaaa;
  local_260 = (undefined8 ***)&SUB_aaaaaaaaaaaaaaaa;
  puStack_248 = &SUB_aaaaaaaaaaaaaaaa;
  local_250 = &SUB_aaaaaaaaaaaaaaaa;
  local_2c0 = &PTR_FUN_09e5b308;
  pcStack_2b8 = FUN_04a166b0;
  local_2a8 = &local_2c0;
  if (DAT_0a51edd8._7_1_ < '\0') {
    FUN_00018d20(&local_3b0,DAT_0a51edc8,DAT_0a51edd0);
  }
  else {
    uStack_3a8 = DAT_0a51edd0;
    local_3b0 = DAT_0a51edc8;
    local_3a0 = CONCAT17(DAT_0a51edd8._7_1_,(undefined7)DAT_0a51edd8);
  }
  FUN_041105c4(&local_260,&local_2c0,2,&local_3b0);
  if ((long)local_3a0 < 0) {
    __ZdlPvm(local_3b0,local_3a0 & 0x7fffffffffffffff);
  }
  if (local_2a8 == &local_2c0) {
    pcVar11 = (code *)(*local_2a8)[4];
LAB_04674358:
    (*pcVar11)();
  }
  else if (local_2a8 != (undefined ***)0x0) {
    pcVar11 = (code *)(*local_2a8)[5];
    goto LAB_04674358;
  }
  iVar7 = thunk_FUN_05e1d97c(2);
  if (iVar7 != 0) {
    FUN_0488143c(&local_378);
    ppppuVar1 = (undefined8 ****)local_378;
    if (-1 < cStack_361) {
      ppppuVar1 = &local_378;
    }
    if ((DAT_0a45df8a & 1) == 0) {
      DAT_0a45df80._0_1_ = s_input_ackernel_cpadV_08a133a0[8];
      DAT_0a45df80._1_1_ = s_input_ackernel_cpadV_08a133a0[9];
      DAT_0a45df80._2_1_ = s_input_ackernel_cpadV_08a133a0[10];
      DAT_0a45df80._3_1_ = s_input_ackernel_cpadV_08a133a0[0xb];
      DAT_0a45df80._4_1_ = s_input_ackernel_cpadV_08a133a0[0xc];
      DAT_0a45df80._5_1_ = s_input_ackernel_cpadV_08a133a0[0xd];
      DAT_0a45df80._6_1_ = s_input_ackernel_cpadV_08a133a0[0xe];
      DAT_0a45df80._7_1_ = s_input_ackernel_cpadV_08a133a0[0xf];
      DAT_0a45df88 = 99;
      DAT_0a45df8a = 1;
    }
    if ((DAT_0a45e49d & 1) == 0) {
      _DAT_0a45e488 = CONCAT44((int)DAT_085465e8,(int)DAT_088899e8);
      uRam000000000a45e490 = CONCAT44((int)DAT_084d82b0,(int)DAT_087f2358);
      DAT_0a45e498 = (undefined4)DAT_084d82b8;
      DAT_0a45e49c = 0;
      DAT_0a45e49d = 1;
    }
    FUN_05e1d050(&local_180,2,ppppuVar1,&DAT_0a45df80,&DAT_0a45e488,0x4e2,0,0);
    if ((DAT_0a45e55d & 1) == 0) {
      _DAT_0a45e540 = CONCAT44((int)DAT_084d8630,(int)DAT_0889c248);
      uRam000000000a45e548 = CONCAT44((int)DAT_08a13550,(int)DAT_08a13548);
      DAT_0a45e550 = CONCAT44((int)DAT_08829b40,(int)DAT_08632a28);
      DAT_0a45e558 = (undefined4)DAT_085465e8;
      DAT_0a45e55c = 0;
      DAT_0a45e55d = 1;
    }
    local_88 = 0;
    uStack_90 = 0;
    local_78 = 0;
    uStack_80 = 0;
    local_a8 = 0;
    uStack_b0 = 0;
    local_98 = 0;
    uStack_a0 = 0;
    local_c8 = 0;
    uStack_d0 = 0;
    local_b8 = 0;
    uStack_c0 = 0;
    plStack_e8 = (long *)0x0;
    local_f0 = (undefined8 ***)0x0;
    local_d8 = 0;
    uStack_e0 = 0;
    FUN_05e1d31c(&local_180,&DAT_0a45e540,&local_f0);
    thunk_FUN_05e1d0bc(&local_180);
    if (cStack_361 < '\0') {
      __ZdlPvm(local_378,CONCAT17(cStack_361,local_368) & 0x7fffffffffffffff);
    }
  }
  (**(code **)(*DAT_0a45df38 + 0x68))(&local_180);
  plVar10 = plStack_178;
  local_378 = local_180;
  local_370 = plStack_178;
  if (plStack_178 != (long *)0x0) {
    plStack_178[1] = plStack_178[1] + 1;
    if (plStack_178 != (long *)0x0) {
      LOAcquire();
      lVar6 = plStack_178[1];
      plStack_178[1] = lVar6 + -1;
      LORelease();
      if (lVar6 == 0) {
        (**(code **)(*plStack_178 + 0x10))(plStack_178);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
      }
    }
  }
  FUN_04551be0(&local_f0,local_378,param_2);
  local_180 = (undefined8 ***)local_f0;
  plStack_178 = plStack_e8;
  lVar6 = 0;
  if (plStack_e8 != (long *)0x0) {
    lVar6 = plStack_e8[1];
    plStack_e8[1] = lVar6 + 1;
  }
  local_170 = (undefined1 *)0x0;
  FUN_066856fc(lVar6,&local_180);
  FUN_0666a844(local_180);
  plVar10 = plStack_178;
  if (plStack_178 != (long *)0x0) {
    LOAcquire();
    lVar6 = plStack_178[1];
    plStack_178[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*plStack_178 + 0x10))(plStack_178);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
    }
  }
  plVar10 = plStack_e8;
  if (plStack_e8 != (long *)0x0) {
    LOAcquire();
    lVar6 = plStack_e8[1];
    plStack_e8[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*plStack_e8 + 0x10))(plStack_e8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
    }
  }
  plVar10 = local_370;
  if (local_370 != (long *)0x0) {
    LOAcquire();
    lVar6 = local_370[1];
    local_370[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*local_370 + 0x10))(local_370);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
    }
  }
  FUN_04111974(&local_260);
  iVar7 = thunk_FUN_05e1d97c(2);
  if (iVar7 != 0) {
    FUN_0488143c(&local_260);
    ppppuVar1 = (undefined8 ****)local_260;
    if (-1 < (long)local_250) {
      ppppuVar1 = &local_260;
    }
    if ((DAT_0a45df8a & 1) == 0) {
      DAT_0a45df80._0_1_ = s_input_ackernel_cpadV_08a133a0[8];
      DAT_0a45df80._1_1_ = s_input_ackernel_cpadV_08a133a0[9];
      DAT_0a45df80._2_1_ = s_input_ackernel_cpadV_08a133a0[10];
      DAT_0a45df80._3_1_ = s_input_ackernel_cpadV_08a133a0[0xb];
      DAT_0a45df80._4_1_ = s_input_ackernel_cpadV_08a133a0[0xc];
      DAT_0a45df80._5_1_ = s_input_ackernel_cpadV_08a133a0[0xd];
      DAT_0a45df80._6_1_ = s_input_ackernel_cpadV_08a133a0[0xe];
      DAT_0a45df80._7_1_ = s_input_ackernel_cpadV_08a133a0[0xf];
      DAT_0a45df88 = 99;
      DAT_0a45df8a = 1;
    }
    if ((DAT_0a45e49d & 1) == 0) {
      _DAT_0a45e488 = CONCAT44((int)DAT_085465e8,(int)DAT_088899e8);
      uRam000000000a45e490 = CONCAT44((int)DAT_084d82b0,(int)DAT_087f2358);
      DAT_0a45e498 = (undefined4)DAT_084d82b8;
      DAT_0a45e49c = 0;
      DAT_0a45e49d = 1;
    }
    FUN_05e1d050(&local_180,2,ppppuVar1,&DAT_0a45df80,&DAT_0a45e488,0x4e8,0,0);
    if ((DAT_0a45e571 & 1) == 0) {
      uRam000000000a45e568._0_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x68];
      uRam000000000a45e568._1_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x69];
      uRam000000000a45e568._2_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x6a];
      uRam000000000a45e568._3_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x6b];
      uRam000000000a45e568._4_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x6c];
      uRam000000000a45e568._5_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x6d];
      uRam000000000a45e568._6_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x6e];
      uRam000000000a45e568._7_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x6f];
      DAT_0a45e560 = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x60];
      DAT_0a45e560_1._0_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x61];
      DAT_0a45e560_1._1_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x62];
      DAT_0a45e560_1._2_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[99];
      DAT_0a45e560_1._3_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[100];
      DAT_0a45e560_1._4_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x65];
      DAT_0a45e560_1._5_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x66];
      DAT_0a45e560_1._6_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x67];
      DAT_0a45e570 = 0;
      DAT_0a45e571 = 1;
    }
    local_88 = 0;
    uStack_90 = 0;
    local_78 = 0;
    uStack_80 = 0;
    local_a8 = 0;
    uStack_b0 = 0;
    local_98 = 0;
    uStack_a0 = 0;
    local_c8 = 0;
    uStack_d0 = 0;
    local_b8 = 0;
    uStack_c0 = 0;
    plStack_e8 = (long *)0x0;
    local_f0 = (undefined8 ***)0x0;
    local_d8 = 0;
    uStack_e0 = 0;
    FUN_05e1d31c(&local_180,&DAT_0a45e560,&local_f0);
    thunk_FUN_05e1d0bc(&local_180);
    if ((long)local_250 < 0) {
      __ZdlPvm(local_260,(ulong)local_250 & 0x7fffffffffffffff);
    }
  }
  local_140 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_158 = &SUB_aaaaaaaaaaaaaaaa;
  local_160 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_148 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_150 = &SUB_aaaaaaaaaaaaaaaa;
  plStack_178 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_180 = (undefined8 ***)&SUB_aaaaaaaaaaaaaaaa;
  puStack_168 = &SUB_aaaaaaaaaaaaaaaa;
  local_170 = &SUB_aaaaaaaaaaaaaaaa;
  local_2e0 = &PTR_FUN_09e5b308;
  pcStack_2d8 = FUN_04a166b0;
  local_2c8 = &local_2e0;
  if (DAT_0a51edf0._7_1_ < '\0') {
    FUN_00018d20(&local_3d0,DAT_0a51ede0,DAT_0a51ede8);
  }
  else {
    uStack_3c8 = DAT_0a51ede8;
    local_3d0 = DAT_0a51ede0;
    local_3c0 = CONCAT17(DAT_0a51edf0._7_1_,(undefined7)DAT_0a51edf0);
  }
  FUN_041105c4(&local_180,&local_2e0,2,&local_3d0);
  if ((long)local_3c0 < 0) {
    __ZdlPvm(local_3d0,local_3c0 & 0x7fffffffffffffff);
  }
  if (local_2c8 == &local_2e0) {
    pcVar11 = (code *)(*local_2c8)[4];
LAB_04674810:
    (*pcVar11)();
  }
  else if (local_2c8 != (undefined ***)0x0) {
    pcVar11 = (code *)(*local_2c8)[5];
    goto LAB_04674810;
  }
  iVar7 = FUN_04cb6948(*param_2);
  if (iVar7 != 0) {
    uVar8 = FUN_04675280(2000);
  }
  FUN_04111974(&local_180);
  local_220 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_238 = &SUB_aaaaaaaaaaaaaaaa;
  local_240 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_228 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_230 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_258 = &SUB_aaaaaaaaaaaaaaaa;
  local_260 = (undefined8 ***)&SUB_aaaaaaaaaaaaaaaa;
  puStack_248 = &SUB_aaaaaaaaaaaaaaaa;
  local_250 = &SUB_aaaaaaaaaaaaaaaa;
  local_300 = &PTR_FUN_09e5b308;
  pcStack_2f8 = FUN_04a166b0;
  local_2e8 = &local_300;
  if (DAT_0a51ee20._7_1_ < '\0') {
    FUN_00018d20(&local_3f0,DAT_0a51ee10,DAT_0a51ee18);
  }
  else {
    uStack_3e8 = DAT_0a51ee18;
    local_3f0 = DAT_0a51ee10;
    local_3e0 = CONCAT17(DAT_0a51ee20._7_1_,(undefined7)DAT_0a51ee20);
  }
  FUN_041105c4(&local_260,&local_300,2,&local_3f0);
  if ((long)local_3e0 < 0) {
    __ZdlPvm(local_3f0,local_3e0 & 0x7fffffffffffffff);
  }
  if (local_2e8 == &local_300) {
    pcVar11 = (code *)(*local_2e8)[4];
  }
  else {
    if (local_2e8 == (undefined ***)0x0) goto LAB_046748dc;
    pcVar11 = (code *)(*local_2e8)[5];
  }
  (*pcVar11)();
LAB_046748dc:
  iVar7 = thunk_FUN_05e1d97c(2);
  if (iVar7 != 0) {
    FUN_0488143c(&local_378);
    ppppuVar1 = (undefined8 ****)local_378;
    if (-1 < cStack_361) {
      ppppuVar1 = &local_378;
    }
    if ((DAT_0a45df8a & 1) == 0) {
      DAT_0a45df80._0_1_ = s_input_ackernel_cpadV_08a133a0[8];
      DAT_0a45df80._1_1_ = s_input_ackernel_cpadV_08a133a0[9];
      DAT_0a45df80._2_1_ = s_input_ackernel_cpadV_08a133a0[10];
      DAT_0a45df80._3_1_ = s_input_ackernel_cpadV_08a133a0[0xb];
      DAT_0a45df80._4_1_ = s_input_ackernel_cpadV_08a133a0[0xc];
      DAT_0a45df80._5_1_ = s_input_ackernel_cpadV_08a133a0[0xd];
      DAT_0a45df80._6_1_ = s_input_ackernel_cpadV_08a133a0[0xe];
      DAT_0a45df80._7_1_ = s_input_ackernel_cpadV_08a133a0[0xf];
      DAT_0a45df88 = 99;
      DAT_0a45df8a = 1;
    }
    if ((DAT_0a45e49d & 1) == 0) {
      _DAT_0a45e488 = CONCAT44((int)DAT_085465e8,(int)DAT_088899e8);
      uRam000000000a45e490 = CONCAT44((int)DAT_084d82b0,(int)DAT_087f2358);
      DAT_0a45e498 = (undefined4)DAT_084d82b8;
      DAT_0a45e49c = 0;
      DAT_0a45e49d = 1;
    }
    FUN_05e1d050(&local_180,2,ppppuVar1,&DAT_0a45df80,&DAT_0a45e488,0x4f2,0,0);
    if ((DAT_0a45e58b & 1) == 0) {
      _DAT_0a45e574 = CONCAT44((int)DAT_084d8630,(int)DAT_0889c248);
      uRam000000000a45e57c = CONCAT44((int)DAT_08a13560,(int)DAT_08a13558);
      DAT_0a45e584 = (undefined4)DAT_08a13568;
      DAT_0a45e588 = 0x756f;
      DAT_0a45e58a = 0;
      DAT_0a45e58b = 1;
    }
    local_88 = 0;
    uStack_90 = 0;
    local_78 = 0;
    uStack_80 = 0;
    local_a8 = 0;
    uStack_b0 = 0;
    local_98 = 0;
    uStack_a0 = 0;
    local_c8 = 0;
    uStack_d0 = 0;
    local_b8 = 0;
    uStack_c0 = 0;
    plStack_e8 = (long *)0x0;
    local_f0 = (undefined8 ***)0x0;
    local_d8 = 0;
    uStack_e0 = 0;
    FUN_05e1d31c(&local_180,&DAT_0a45e574,&local_f0);
    thunk_FUN_05e1d0bc(&local_180);
    if (cStack_361 < '\0') {
      __ZdlPvm(local_378,CONCAT17(cStack_361,local_368) & 0x7fffffffffffffff);
    }
  }
  (**(code **)(*DAT_0a45df38 + 0x68))(&local_180);
  plVar10 = plStack_178;
  local_378 = local_180;
  local_370 = plStack_178;
  if (plStack_178 != (long *)0x0) {
    plStack_178[1] = plStack_178[1] + 1;
    if (plStack_178 != (long *)0x0) {
      LOAcquire();
      lVar6 = plStack_178[1];
      plStack_178[1] = lVar6 + -1;
      LORelease();
      if (lVar6 == 0) {
        (**(code **)(*plStack_178 + 0x10))(plStack_178);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
      }
    }
  }
  FUN_04551eac(&local_f0,local_378,param_2);
  local_180 = (undefined8 ***)local_f0;
  plStack_178 = plStack_e8;
  lVar6 = 0;
  if (plStack_e8 != (long *)0x0) {
    lVar6 = plStack_e8[1];
    plStack_e8[1] = lVar6 + 1;
  }
  local_170 = (undefined1 *)0x0;
  FUN_066856fc(lVar6,&local_180);
  FUN_0666a844(local_180);
  plVar10 = plStack_178;
  if (plStack_178 != (long *)0x0) {
    LOAcquire();
    lVar6 = plStack_178[1];
    plStack_178[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*plStack_178 + 0x10))(plStack_178);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
    }
  }
  plVar10 = plStack_e8;
  if (plStack_e8 != (long *)0x0) {
    LOAcquire();
    lVar6 = plStack_e8[1];
    plStack_e8[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*plStack_e8 + 0x10))(plStack_e8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
    }
  }
  plVar10 = local_370;
  if (local_370 != (long *)0x0) {
    LOAcquire();
    lVar6 = local_370[1];
    local_370[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*local_370 + 0x10))(local_370);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
    }
  }
  FUN_04111974(&local_260);
  iVar7 = thunk_FUN_05e1d97c(2);
  if (iVar7 != 0) {
    FUN_0488143c(&local_260);
    ppppuVar1 = (undefined8 ****)local_260;
    if (-1 < (long)local_250) {
      ppppuVar1 = &local_260;
    }
    if ((DAT_0a45df8a & 1) == 0) {
      DAT_0a45df80._0_1_ = s_input_ackernel_cpadV_08a133a0[8];
      DAT_0a45df80._1_1_ = s_input_ackernel_cpadV_08a133a0[9];
      DAT_0a45df80._2_1_ = s_input_ackernel_cpadV_08a133a0[10];
      DAT_0a45df80._3_1_ = s_input_ackernel_cpadV_08a133a0[0xb];
      DAT_0a45df80._4_1_ = s_input_ackernel_cpadV_08a133a0[0xc];
      DAT_0a45df80._5_1_ = s_input_ackernel_cpadV_08a133a0[0xd];
      DAT_0a45df80._6_1_ = s_input_ackernel_cpadV_08a133a0[0xe];
      DAT_0a45df80._7_1_ = s_input_ackernel_cpadV_08a133a0[0xf];
      DAT_0a45df88 = 99;
      DAT_0a45df8a = 1;
    }
    if ((DAT_0a45e49d & 1) == 0) {
      _DAT_0a45e488 = CONCAT44((int)DAT_085465e8,(int)DAT_088899e8);
      uRam000000000a45e490 = CONCAT44((int)DAT_084d82b0,(int)DAT_087f2358);
      DAT_0a45e498 = (undefined4)DAT_084d82b8;
      DAT_0a45e49c = 0;
      DAT_0a45e49d = 1;
    }
    FUN_05e1d050(&local_180,2,ppppuVar1,&DAT_0a45df80,&DAT_0a45e488,0x4f8,0,0);
    if ((DAT_0a45e5a3 & 1) == 0) {
      uRam000000000a45e598._0_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x78];
      uRam000000000a45e598._1_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x79];
      uRam000000000a45e598._2_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x7a];
      uRam000000000a45e598._3_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x7b];
      uRam000000000a45e598._4_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x7c];
      uRam000000000a45e598._5_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x7d];
      uRam000000000a45e598._6_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x7e];
      uRam000000000a45e598._7_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x7f];
      DAT_0a45e590 = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x70];
      DAT_0a45e590_1._0_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x71];
      DAT_0a45e590_1._1_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x72];
      DAT_0a45e590_1._2_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x73];
      DAT_0a45e590_1._3_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x74];
      DAT_0a45e590_1._4_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x75];
      DAT_0a45e590_1._5_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x76];
      DAT_0a45e590_1._6_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x77];
      DAT_0a45e5a0 = 0x746e;
      DAT_0a45e5a2 = 0;
      DAT_0a45e5a3 = 1;
    }
    local_88 = 0;
    uStack_90 = 0;
    local_78 = 0;
    uStack_80 = 0;
    local_a8 = 0;
    uStack_b0 = 0;
    local_98 = 0;
    uStack_a0 = 0;
    local_c8 = 0;
    uStack_d0 = 0;
    local_b8 = 0;
    uStack_c0 = 0;
    plStack_e8 = (long *)0x0;
    local_f0 = (undefined8 ***)0x0;
    local_d8 = 0;
    uStack_e0 = 0;
    FUN_05e1d31c(&local_180,&DAT_0a45e590,&local_f0);
    thunk_FUN_05e1d0bc(&local_180);
    if ((long)local_250 < 0) {
      __ZdlPvm(local_260,(ulong)local_250 & 0x7fffffffffffffff);
    }
  }
  FUN_0466f25c(&local_f0,DAT_0a45df38);
  local_180 = (undefined8 ***)local_f0;
  plStack_178 = plStack_e8;
  lVar6 = 0;
  if (plStack_e8 != (long *)0x0) {
    lVar6 = plStack_e8[1];
    plStack_e8[1] = lVar6 + 1;
  }
  local_170 = (undefined1 *)0x0;
  FUN_066856fc(lVar6,&local_180);
  FUN_0666a844(local_180);
  plVar10 = plStack_178;
  if (plStack_178 != (long *)0x0) {
    LOAcquire();
    lVar6 = plStack_178[1];
    plStack_178[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*plStack_178 + 0x10))(plStack_178);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
    }
  }
  plVar10 = plStack_e8;
  if (plStack_e8 != (long *)0x0) {
    LOAcquire();
    lVar6 = plStack_e8[1];
    plStack_e8[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*plStack_e8 + 0x10))(plStack_e8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
    }
  }
  iVar7 = thunk_FUN_05e1d97c(2);
  if (iVar7 != 0) {
    FUN_0488143c(&local_260);
    ppppuVar1 = (undefined8 ****)local_260;
    if (-1 < (long)local_250) {
      ppppuVar1 = &local_260;
    }
    if ((DAT_0a45df8a & 1) == 0) {
      DAT_0a45df80._0_1_ = s_input_ackernel_cpadV_08a133a0[8];
      DAT_0a45df80._1_1_ = s_input_ackernel_cpadV_08a133a0[9];
      DAT_0a45df80._2_1_ = s_input_ackernel_cpadV_08a133a0[10];
      DAT_0a45df80._3_1_ = s_input_ackernel_cpadV_08a133a0[0xb];
      DAT_0a45df80._4_1_ = s_input_ackernel_cpadV_08a133a0[0xc];
      DAT_0a45df80._5_1_ = s_input_ackernel_cpadV_08a133a0[0xd];
      DAT_0a45df80._6_1_ = s_input_ackernel_cpadV_08a133a0[0xe];
      DAT_0a45df80._7_1_ = s_input_ackernel_cpadV_08a133a0[0xf];
      DAT_0a45df88 = 99;
      DAT_0a45df8a = 1;
    }
    if ((DAT_0a45e49d & 1) == 0) {
      _DAT_0a45e488 = CONCAT44((int)DAT_085465e8,(int)DAT_088899e8);
      uRam000000000a45e490 = CONCAT44((int)DAT_084d82b0,(int)DAT_087f2358);
      DAT_0a45e498 = (undefined4)DAT_084d82b8;
      DAT_0a45e49c = 0;
      DAT_0a45e49d = 1;
    }
    FUN_05e1d050(&local_180,2,ppppuVar1,&DAT_0a45df80,&DAT_0a45e488,0x4fe,0,0);
    if ((DAT_0a45e5c0 & 1) == 0) {
      uRam000000000a45e5b8._0_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x88];
      uRam000000000a45e5b8._1_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x89];
      uRam000000000a45e5b8._2_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x8a];
      uRam000000000a45e5b8._3_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x8b];
      uRam000000000a45e5b8._4_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x8c];
      uRam000000000a45e5b8._5_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x8d];
      uRam000000000a45e5b8._6_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x8e];
      uRam000000000a45e5b8._7_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x8f];
      DAT_0a45e5b0 = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x80];
      DAT_0a45e5b0_1._0_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x81];
      DAT_0a45e5b0_1._1_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x82];
      DAT_0a45e5b0_1._2_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x83];
      DAT_0a45e5b0_1._3_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x84];
      DAT_0a45e5b0_1._4_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x85];
      DAT_0a45e5b0_1._5_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x86];
      DAT_0a45e5b0_1._6_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x87];
      DAT_0a45e5c0 = 1;
    }
    local_88 = 0;
    uStack_90 = 0;
    local_78 = 0;
    uStack_80 = 0;
    local_a8 = 0;
    uStack_b0 = 0;
    local_98 = 0;
    uStack_a0 = 0;
    local_c8 = 0;
    uStack_d0 = 0;
    local_b8 = 0;
    uStack_c0 = 0;
    plStack_e8 = (long *)0x0;
    local_f0 = (undefined8 ***)0x0;
    local_d8 = 0;
    uStack_e0 = 0;
    FUN_05e1d31c(&local_180,&DAT_0a45e5b0,&local_f0);
    thunk_FUN_05e1d0bc(&local_180);
    if ((long)local_250 < 0) {
      __ZdlPvm(local_260,(ulong)local_250 & 0x7fffffffffffffff);
    }
  }
  plVar10 = (long *)(**(code **)(*DAT_0a45df38 + 0x18))();
  (**(code **)(*plVar10 + 0x70))(plVar10,0);
  FUN_04668f94(param_1,1);
  FUN_046760d8(param_1,param_2);
  FUN_04111974(&local_1d0);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_68) {
    return uVar8;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


