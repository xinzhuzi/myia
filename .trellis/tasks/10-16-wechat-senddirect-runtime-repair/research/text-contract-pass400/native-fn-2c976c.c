// Ghidra inferred pseudocode; requested=0x2c976c
// entry=002c976c end=002cb2f7

/* WARNING: Removing unreachable block (ram,0x002ca6f0) */
/* WARNING: Removing unreachable block (ram,0x002ca660) */
/* WARNING: Removing unreachable block (ram,0x002ca36c) */
/* WARNING: Removing unreachable block (ram,0x002c9f38) */
/* WARNING: Removing unreachable block (ram,0x002c9b98) */
/* WARNING: Removing unreachable block (ram,0x002ca534) */
/* WARNING: Removing unreachable block (ram,0x002ca83c) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_002c976c(undefined4 param_1,undefined8 param_2)

{
  undefined8 **ppuVar1;
  int *******pppppppiVar2;
  undefined *puVar3;
  undefined **ppuVar4;
  undefined1 uVar5;
  byte bVar6;
  uint3 uVar7;
  undefined **ppuVar8;
  undefined **ppuVar9;
  bool bVar10;
  int iVar11;
  long lVar12;
  size_t sVar13;
  undefined8 *******pppppppuVar14;
  long *plVar15;
  int ******ppppppiVar16;
  undefined1 *puVar17;
  code *pcVar18;
  undefined8 *****pppppuVar19;
  ulong uVar20;
  long lVar21;
  undefined1 *puVar22;
  undefined8 *puVar23;
  undefined8 uVar24;
  int *******pppppppiVar25;
  undefined4 uVar26;
  undefined4 uVar27;
  undefined8 *******local_428 [2];
  undefined7 local_418;
  char cStack_411;
  long local_410;
  undefined8 local_408;
  undefined8 uStack_400;
  ulong local_3f8;
  undefined1 *local_3f0;
  undefined1 *puStack_3e8;
  undefined1 *local_3e0;
  undefined1 *puStack_3d8;
  undefined1 *puStack_3d0;
  undefined1 *puStack_3c8;
  undefined1 *local_3c0;
  undefined1 *puStack_3b8;
  undefined1 *puStack_3b0;
  undefined1 *puStack_3a8;
  undefined1 *local_3a0;
  undefined1 *puStack_398;
  rlimit local_388;
  long local_378;
  undefined1 *local_370;
  long local_368;
  undefined1 *local_360;
  undefined4 local_354;
  undefined8 *******local_350;
  undefined8 **ppuStack_348;
  undefined1 *local_340;
  undefined8 *******pppppppuStack_338;
  undefined8 local_330;
  undefined8 uStack_328;
  undefined8 local_320;
  undefined8 uStack_318;
  undefined8 local_310;
  undefined8 uStack_308;
  undefined8 local_300;
  undefined8 uStack_2f8;
  undefined8 local_2f0;
  undefined8 uStack_2e8;
  undefined8 local_2e0;
  undefined8 uStack_2d8;
  undefined **local_2c0;
  undefined **ppuStack_2b8;
  ulong local_2b0;
  undefined ***local_2a8;
  undefined8 ******local_2a0;
  undefined8 **ppuStack_298;
  ulong local_290;
  undefined8 local_288;
  undefined4 local_280;
  undefined4 uStack_27c;
  undefined4 uStack_278;
  int iStack_274;
  undefined4 local_270;
  undefined4 uStack_26c;
  undefined8 local_268;
  undefined8 local_260;
  ulong uStack_258;
  undefined1 *local_250;
  undefined8 uStack_248;
  undefined8 local_240;
  undefined8 uStack_238;
  undefined8 uStack_230;
  undefined8 uStack_228;
  undefined8 local_220;
  undefined8 uStack_218;
  undefined8 uStack_210;
  undefined8 uStack_208;
  undefined8 local_200;
  undefined8 uStack_1f8;
  undefined8 uStack_1f0;
  undefined8 uStack_1e8;
  undefined1 *local_1e0;
  int *******local_1d0;
  undefined1 *puStack_1c8;
  undefined1 *local_1c0;
  undefined1 *puStack_1b8;
  long *local_1b0;
  int *local_1a8;
  undefined1 *local_1a0;
  undefined1 *puStack_198;
  undefined1 *puStack_190;
  undefined1 *puStack_188;
  undefined1 **local_180;
  undefined8 *local_170;
  undefined8 uStack_168;
  undefined1 *puStack_160;
  undefined1 *puStack_158;
  undefined1 *local_150;
  undefined1 *puStack_148;
  undefined1 *puStack_140;
  undefined1 *puStack_138;
  undefined1 *local_130;
  undefined1 *puStack_128;
  undefined1 *puStack_120;
  undefined1 *puStack_118;
  undefined1 *local_110;
  undefined8 ******local_100;
  undefined8 uStack_f8;
  undefined8 local_f0;
  undefined8 uStack_e8;
  undefined8 local_e0;
  undefined8 uStack_d8;
  undefined8 uStack_d0;
  undefined8 uStack_c8;
  undefined8 local_c0;
  undefined8 uStack_b8;
  undefined8 uStack_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 uStack_90;
  undefined8 uStack_88;
  long local_78;
  
  local_78 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_354 = param_1;
  FUN_0002267c();
  local_2c0 = (undefined **)&DAT_aaaaaaaa00000000;
  ppuStack_2b8 = (undefined **)0x0;
  local_2b0 = ram0x08486a90;
  FUN_0003bc08(&local_2c0);
  uVar24 = 0xffffffff;
  FUN_0003bf98(0xffffffff);
  FUN_0003c024(FUN_002cc6a4);
  FUN_06e981f0(FUN_002cc79c);
  FUN_0473c400();
  iVar11 = FUN_0473ccfc();
  if (iVar11 == 0) goto LAB_002caa80;
  local_360 = &SUB_aaaaaaaaaaaaaaaa;
  lVar12 = __Znwm(0x30);
  FUN_00033c40(lVar12,FUN_002cd8a4,FUN_0005f488);
  *(code **)(lVar12 + 0x20) = FUN_0473d240;
  local_368 = lVar12;
  FUN_00033b68(&local_360,&local_368);
  FUN_00033d2c(&local_368);
  local_370 = &SUB_aaaaaaaaaaaaaaaa;
  lVar12 = __Znwm(0x30);
  FUN_00033c40(lVar12,FUN_002cd8a4,FUN_0005f488);
  *(code **)(lVar12 + 0x20) = FUN_04a7d20c;
  local_378 = lVar12;
  FUN_00033b68(&local_370,&local_378);
  FUN_00033d2c(&local_378);
  uStack_258 = 0;
  local_2b0 = 0;
  ppuStack_2b8 = (undefined **)0x0;
  local_2a0 = (undefined8 ******)0x0;
  local_2a8 = (undefined ***)0x0;
  local_290 = 0;
  ppuStack_298 = (undefined8 **)0x0;
  local_280 = 0;
  local_288 = 0;
  iStack_274 = 0;
  local_270 = 0;
  uStack_27c = 0;
  uStack_278 = 0;
  local_2c0 = (undefined **)&DAT_aaaaaaaa00000000;
  uStack_26c = 6;
  local_268 = 0;
  local_260 = 0;
  local_250 = &DAT_aaaaaaaa00000000;
  FUN_0473c74c(&local_100,5);
  FUN_0002def0(&local_350,&local_100);
  puVar23 = (undefined8 *)((ulong)&local_2c0 | 8);
  if ((long)local_2a8 < 0) {
    __ZdlPvm(ppuStack_2b8,(ulong)local_2a8 & 0x7fffffffffffffff);
  }
  puVar23[1] = ppuStack_348;
  *puVar23 = local_350;
  puVar23[2] = local_340;
  local_340 = (undefined1 *)((ulong)local_340 & 0xffffffffffffff);
  local_350 = (undefined8 *******)((ulong)local_350 & 0xffffffffffffff00);
  FUN_0002b440(&local_100);
  local_270 = (undefined4)DAT_084e3298;
  uStack_26c = (undefined4)((ulong)DAT_084e3298 >> 0x20);
  local_2c0 = (undefined **)((ulong)local_2c0 & 0xffffffff00000000);
  FUN_0473d27c(&local_100);
  FUN_0002def0(&local_350,&local_100);
  if ((long)local_290 < 0) {
    __ZdlPvm(local_2a0,local_290 & 0x7fffffffffffffff);
  }
  ppuStack_298 = ppuStack_348;
  local_2a0 = local_350;
  local_290 = (ulong)local_340;
  local_340 = (undefined1 *)((ulong)local_340 & 0xffffffffffffff);
  local_350 = (undefined8 *******)((ulong)local_350 & 0xffffffffffffff00);
  FUN_0002b440(&local_100);
  if ((DAT_0a28029b & 1) == 0) {
    uVar20 = 0;
    do {
      uVar26 = *(undefined4 *)((long)&DAT_084e3c96 + uVar20);
      uVar7 = CONCAT12((char)((uint)uVar26 >> 8),(short)uVar26) & 0xff00ff;
      uVar27 = *(undefined4 *)((long)&DAT_084e3c82 + uVar20 % 0x14);
      *(uint *)((long)&DAT_0a28021a + uVar20) =
           CONCAT13((char)((uint)uVar26 >> 0x18) + 0x8aU ^ (byte)((uint)uVar27 >> 0x18),
                    CONCAT12((char)((uint)uVar26 >> 0x10) + 0x8aU ^ (byte)((uint)uVar27 >> 0x10),
                             CONCAT11((char)(uVar7 >> 0x10) + 0x8aU ^ (byte)((uint)uVar27 >> 8),
                                      (char)uVar7 + 0x8aU ^ (byte)uVar27)));
      uVar20 = uVar20 + 4;
    } while (uVar20 != 0x80);
    DAT_0a28029a = 0;
    DAT_0a28029b = 1;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
            (&local_288,&DAT_0a28021a);
  FUN_05e246f8(&local_2c0);
  FUN_05e2493c(0);
  thunk_FUN_05e1d96c(2);
  if ((long)uStack_258 < 0) {
    __ZdlPvm(local_268,uStack_258 & 0x7fffffffffffffff);
  }
  if (iStack_274 < 0) {
    __ZdlPvm(local_288,CONCAT44(iStack_274,uStack_278) & 0x7fffffffffffffff);
  }
  if ((long)local_290 < 0) {
    __ZdlPvm(local_2a0,local_290 & 0x7fffffffffffffff);
  }
  if ((long)local_2a8 < 0) {
    __ZdlPvm(ppuStack_2b8,(ulong)local_2a8 & 0x7fffffffffffffff);
  }
  iVar11 = thunk_FUN_05e1d97c(2);
  if (iVar11 != 0) {
    FUN_0488143c(&local_100);
    if ((DAT_0a27fee7 & 1) == 0) {
      DAT_0a27fed8._0_1_ = s_wechat_main__084e3218[0];
      DAT_0a27fed8._1_1_ = s_wechat_main__084e3218[1];
      DAT_0a27fed8._2_1_ = s_wechat_main__084e3218[2];
      DAT_0a27fed8._3_1_ = s_wechat_main__084e3218[3];
      DAT_0a27fed8._4_1_ = s_wechat_main__084e3218[4];
      DAT_0a27fed8._5_1_ = s_wechat_main__084e3218[5];
      DAT_0a27fed8._6_1_ = s_wechat_main__084e3218[6];
      DAT_0a27fed8._7_1_ = s_wechat_main__084e3218[7];
      DAT_0a27fee0 = (undefined4)ram0x084e3220;
      DAT_0a27fee4 = 0x6363;
      DAT_0a27fee6 = 0;
      DAT_0a27fee7 = 1;
    }
    if ((DAT_0a27ffa4 & 1) == 0) {
      DAT_0a27ff98._0_1_ = s_wechat_main__084e3218[0];
      DAT_0a27ff98._1_1_ = s_wechat_main__084e3218[1];
      DAT_0a27ff98._2_1_ = s_wechat_main__084e3218[2];
      DAT_0a27ff98._3_1_ = s_wechat_main__084e3218[3];
      DAT_0a27ff98._4_1_ = s_wechat_main__084e3218[4];
      DAT_0a27ff98._5_1_ = s_wechat_main__084e3218[5];
      DAT_0a27ff98._6_1_ = s_wechat_main__084e3218[6];
      DAT_0a27ff98._7_1_ = s_wechat_main__084e3218[7];
      DAT_0a27ffa0 = (undefined4)ram0x0848d960;
      DAT_0a27ffa4 = 1;
    }
    FUN_05e1d050(&local_2c0,2,&local_100,&DAT_0a27fed8,&DAT_0a27ff98,0x1f9,0,0);
    if ((DAT_0a27ffb6 & 1) == 0) {
      DAT_0a27ffa8._0_1_ = s_init_xlog_ok_084e32a0[0];
      DAT_0a27ffa8._1_1_ = s_init_xlog_ok_084e32a0[1];
      DAT_0a27ffa8._2_1_ = s_init_xlog_ok_084e32a0[2];
      DAT_0a27ffa8._3_1_ = s_init_xlog_ok_084e32a0[3];
      DAT_0a27ffa8._4_1_ = s_init_xlog_ok_084e32a0[4];
      DAT_0a27ffa8._5_1_ = s_init_xlog_ok_084e32a0[5];
      DAT_0a27ffa8._6_1_ = s_init_xlog_ok_084e32a0[6];
      DAT_0a27ffa8._7_1_ = s_init_xlog_ok_084e32a0[7];
      DAT_0a27ffb0 = (undefined4)ram0x084e32a8;
      DAT_0a27ffb4 = 0x2e;
      DAT_0a27ffb6 = 1;
    }
    uStack_2e8 = 0;
    local_2f0 = 0;
    uStack_2d8 = 0;
    local_2e0 = 0;
    uStack_308 = 0;
    local_310 = 0;
    uStack_2f8 = 0;
    local_300 = 0;
    uStack_328 = 0;
    local_330 = 0;
    uStack_318 = 0;
    local_320 = 0;
    ppuStack_348 = (undefined8 **)0x0;
    local_350 = (undefined8 *******)0x0;
    pppppppuStack_338 = (undefined8 *******)0x0;
    local_340 = (undefined1 *)0x0;
    FUN_05e1d31c(&local_2c0,&DAT_0a27ffa8,&local_350);
    thunk_FUN_05e1d0bc(&local_2c0);
  }
  FUN_0487ff08();
  FUN_048803ac();
  local_388.rlim_cur = (rlim_t)&SUB_aaaaaaaaaaaaaaaa;
  local_388.rlim_max = (rlim_t)&SUB_aaaaaaaaaaaaaaaa;
  iVar11 = _getrlimit(8,&local_388);
  if (iVar11 == 0) {
    bVar10 = (undefined1 *)0x1fff < local_388.rlim_cur;
    local_388.rlim_cur = local_388.rlim_max;
    if ("orks/GSS.framework/Versions/A/GSS" < (char *)(local_388.rlim_max + -1) || bVar10) {
      local_388.rlim_cur = 0x2000;
    }
    iVar11 = _setrlimit(8,&local_388);
    if ((iVar11 != 0) && (iVar11 = thunk_FUN_05e1d97c(2), iVar11 != 0)) {
      FUN_0488143c(&local_100);
      if ((DAT_0a27fee7 & 1) == 0) {
        DAT_0a27fed8._0_1_ = s_wechat_main__084e3218[0];
        DAT_0a27fed8._1_1_ = s_wechat_main__084e3218[1];
        DAT_0a27fed8._2_1_ = s_wechat_main__084e3218[2];
        DAT_0a27fed8._3_1_ = s_wechat_main__084e3218[3];
        DAT_0a27fed8._4_1_ = s_wechat_main__084e3218[4];
        DAT_0a27fed8._5_1_ = s_wechat_main__084e3218[5];
        DAT_0a27fed8._6_1_ = s_wechat_main__084e3218[6];
        DAT_0a27fed8._7_1_ = s_wechat_main__084e3218[7];
        DAT_0a27fee0 = (undefined4)ram0x084e3220;
        DAT_0a27fee4 = 0x6363;
        DAT_0a27fee6 = 0;
        DAT_0a27fee7 = 1;
      }
      if ((DAT_0a27ffa4 & 1) == 0) {
        DAT_0a27ff98._0_1_ = s_wechat_main__084e3218[0];
        DAT_0a27ff98._1_1_ = s_wechat_main__084e3218[1];
        DAT_0a27ff98._2_1_ = s_wechat_main__084e3218[2];
        DAT_0a27ff98._3_1_ = s_wechat_main__084e3218[3];
        DAT_0a27ff98._4_1_ = s_wechat_main__084e3218[4];
        DAT_0a27ff98._5_1_ = s_wechat_main__084e3218[5];
        DAT_0a27ff98._6_1_ = s_wechat_main__084e3218[6];
        DAT_0a27ff98._7_1_ = s_wechat_main__084e3218[7];
        DAT_0a27ffa0 = (undefined4)ram0x0848d960;
        DAT_0a27ffa4 = 1;
      }
      FUN_05e1d050(&local_2c0,2,&local_100,&DAT_0a27fed8,&DAT_0a27ff98,0x20f,0,0);
      if ((DAT_0a27ffdc & 1) == 0) {
        _DAT_0a27ffb8 = CONCAT44((int)DAT_0848afe8,(int)DAT_0848afe0);
        uRam000000000a27ffc0 = CONCAT44((int)DAT_0848c098,(int)DAT_0848c0c8);
        _DAT_0a27ffc8 = CONCAT44((int)DAT_0848c0a8,(int)DAT_0848c0a0);
        uRam000000000a27ffd0 = CONCAT44((int)DAT_0848c0b8,(int)DAT_0848c0b0);
        DAT_0a27ffd8 = (undefined4)DAT_0848c0c0;
        DAT_0a27ffdc = 1;
      }
      uStack_2e8 = 0;
      local_2f0 = 0;
      uStack_2d8 = 0;
      local_2e0 = 0;
      uStack_308 = 0;
      local_310 = 0;
      uStack_2f8 = 0;
      local_300 = 0;
      uStack_328 = 0;
      local_330 = 0;
      uStack_318 = 0;
      local_320 = 0;
      ppuStack_348 = (undefined8 **)0x0;
      local_350 = (undefined8 *******)0x0;
      pppppppuStack_338 = (undefined8 *******)0x0;
      local_340 = (undefined1 *)0x0;
      FUN_05e1d31c(&local_2c0,&DAT_0a27ffb8,&local_350);
      goto LAB_002c9f28;
    }
  }
  else {
    iVar11 = thunk_FUN_05e1d97c(2);
    if (iVar11 != 0) {
      FUN_0488143c(&local_100);
      if ((DAT_0a27fee7 & 1) == 0) {
        DAT_0a27fed8._0_1_ = s_wechat_main__084e3218[0];
        DAT_0a27fed8._1_1_ = s_wechat_main__084e3218[1];
        DAT_0a27fed8._2_1_ = s_wechat_main__084e3218[2];
        DAT_0a27fed8._3_1_ = s_wechat_main__084e3218[3];
        DAT_0a27fed8._4_1_ = s_wechat_main__084e3218[4];
        DAT_0a27fed8._5_1_ = s_wechat_main__084e3218[5];
        DAT_0a27fed8._6_1_ = s_wechat_main__084e3218[6];
        DAT_0a27fed8._7_1_ = s_wechat_main__084e3218[7];
        DAT_0a27fee0 = (undefined4)ram0x084e3220;
        DAT_0a27fee4 = 0x6363;
        DAT_0a27fee6 = 0;
        DAT_0a27fee7 = 1;
      }
      if ((DAT_0a27ffa4 & 1) == 0) {
        DAT_0a27ff98._0_1_ = s_wechat_main__084e3218[0];
        DAT_0a27ff98._1_1_ = s_wechat_main__084e3218[1];
        DAT_0a27ff98._2_1_ = s_wechat_main__084e3218[2];
        DAT_0a27ff98._3_1_ = s_wechat_main__084e3218[3];
        DAT_0a27ff98._4_1_ = s_wechat_main__084e3218[4];
        DAT_0a27ff98._5_1_ = s_wechat_main__084e3218[5];
        DAT_0a27ff98._6_1_ = s_wechat_main__084e3218[6];
        DAT_0a27ff98._7_1_ = s_wechat_main__084e3218[7];
        DAT_0a27ffa0 = (undefined4)ram0x0848d960;
        DAT_0a27ffa4 = 1;
      }
      FUN_05e1d050(&local_2c0,2,&local_100,&DAT_0a27fed8,&DAT_0a27ff98,0x212,0,0);
      if ((DAT_0a280004 & 1) == 0) {
        _DAT_0a27ffe0 = CONCAT44((int)DAT_0848afe8,(int)DAT_0848afe0);
        uRam000000000a27ffe8 = CONCAT44((int)DAT_0848c098,(int)DAT_0848aff0);
        _DAT_0a27fff0 = CONCAT44((int)DAT_0848c0a8,(int)DAT_0848c0a0);
        uRam000000000a27fff8 = CONCAT44((int)DAT_0848c0b8,(int)DAT_0848c0b0);
        DAT_0a280000 = (undefined4)DAT_0848c0c0;
        DAT_0a280004 = 1;
      }
      uStack_2e8 = 0;
      local_2f0 = 0;
      uStack_2d8 = 0;
      local_2e0 = 0;
      uStack_308 = 0;
      local_310 = 0;
      uStack_2f8 = 0;
      local_300 = 0;
      uStack_328 = 0;
      local_330 = 0;
      uStack_318 = 0;
      local_320 = 0;
      ppuStack_348 = (undefined8 **)0x0;
      local_350 = (undefined8 *******)0x0;
      pppppppuStack_338 = (undefined8 *******)0x0;
      local_340 = (undefined1 *)0x0;
      FUN_05e1d31c(&local_2c0,&DAT_0a27ffe0,&local_350);
LAB_002c9f28:
      thunk_FUN_05e1d0bc(&local_2c0);
    }
  }
  _getrlimit(8,&local_388);
  iVar11 = thunk_FUN_05e1d97c(2);
  if (iVar11 != 0) {
    FUN_0488143c(&local_1d0);
    pppppppiVar2 = local_1d0;
    if (-1 < (long)local_1c0) {
      pppppppiVar2 = (int *******)&local_1d0;
    }
    if ((DAT_0a27fee7 & 1) == 0) {
      DAT_0a27fed8._0_1_ = s_wechat_main__084e3218[0];
      DAT_0a27fed8._1_1_ = s_wechat_main__084e3218[1];
      DAT_0a27fed8._2_1_ = s_wechat_main__084e3218[2];
      DAT_0a27fed8._3_1_ = s_wechat_main__084e3218[3];
      DAT_0a27fed8._4_1_ = s_wechat_main__084e3218[4];
      DAT_0a27fed8._5_1_ = s_wechat_main__084e3218[5];
      DAT_0a27fed8._6_1_ = s_wechat_main__084e3218[6];
      DAT_0a27fed8._7_1_ = s_wechat_main__084e3218[7];
      DAT_0a27fee0 = (undefined4)ram0x084e3220;
      DAT_0a27fee4 = 0x6363;
      DAT_0a27fee6 = 0;
      DAT_0a27fee7 = 1;
    }
    if ((DAT_0a27ffa4 & 1) == 0) {
      DAT_0a27ff98._0_1_ = s_wechat_main__084e3218[0];
      DAT_0a27ff98._1_1_ = s_wechat_main__084e3218[1];
      DAT_0a27ff98._2_1_ = s_wechat_main__084e3218[2];
      DAT_0a27ff98._3_1_ = s_wechat_main__084e3218[3];
      DAT_0a27ff98._4_1_ = s_wechat_main__084e3218[4];
      DAT_0a27ff98._5_1_ = s_wechat_main__084e3218[5];
      DAT_0a27ff98._6_1_ = s_wechat_main__084e3218[6];
      DAT_0a27ff98._7_1_ = s_wechat_main__084e3218[7];
      DAT_0a27ffa0 = (undefined4)ram0x0848d960;
      DAT_0a27ffa4 = 1;
    }
    FUN_05e1d050(&local_2c0,2,pppppppiVar2,&DAT_0a27fed8,&DAT_0a27ff98,0x216,0,0);
    local_100 = (undefined8 ******)0x0;
    if ((DAT_0a280167 & 1) == 0) {
      uVar20 = 0;
      do {
        uVar26 = *(undefined4 *)((long)&DAT_084e3a3c + uVar20);
        uVar7 = CONCAT12((char)((uint)uVar26 >> 8),(short)uVar26) & 0xff00ff;
        uVar27 = *(undefined4 *)((long)&DAT_084e3a28 + uVar20 % 0x14);
        *(uint *)((long)&DAT_0a28011f + uVar20) =
             CONCAT13((char)((uint)uVar26 >> 0x18) + 0x8aU ^ (byte)((uint)uVar27 >> 0x18),
                      CONCAT12((char)((uint)uVar26 >> 0x10) + 0x8aU ^ (byte)((uint)uVar27 >> 0x10),
                               CONCAT11((char)(uVar7 >> 0x10) + 0x8aU ^ (byte)((uint)uVar27 >> 8),
                                        (char)uVar7 + 0x8aU ^ (byte)uVar27)));
        uVar20 = uVar20 + 4;
      } while (uVar20 != 0x48);
      DAT_0a280167 = 1;
    }
    puVar17 = (undefined1 *)local_388.rlim_cur;
    lVar12 = 0;
    do {
      lVar21 = lVar12;
      *(undefined1 *)((long)&uStack_f8 + lVar21) = *(undefined1 *)((ulong)puVar17 % 10 + 0xa280142);
      bVar10 = (undefined1 *)0x9 < puVar17;
      puVar17 = (undefined1 *)((ulong)puVar17 / 10);
      lVar12 = lVar21 + 1;
    } while (bVar10);
    *(undefined1 *)((long)&uStack_f8 + lVar21 + 1) = 0;
    if (8 < lVar21 + 8U) {
      puVar17 = (undefined1 *)((long)&uStack_f8 + lVar21);
      puVar22 = (undefined1 *)((long)&uStack_f8 + 1);
      do {
        uVar5 = *puVar17;
        *puVar17 = puVar22[-1];
        puVar22[-1] = uVar5;
        bVar10 = puVar22 < puVar17 + -1;
        puVar17 = puVar17 + -1;
        puVar22 = puVar22 + 1;
      } while (bVar10);
    }
    local_100 = (undefined8 ******)&uStack_f8;
    local_170 = &uStack_168;
    lVar12 = 0;
    puVar17 = (undefined1 *)local_388.rlim_max;
    do {
      lVar21 = lVar12;
      *(undefined1 *)((long)&uStack_168 + lVar21) = *(undefined1 *)((ulong)puVar17 % 10 + 0xa280142)
      ;
      bVar10 = (undefined1 *)0x9 < puVar17;
      lVar12 = lVar21 + 1;
      puVar17 = (undefined1 *)((ulong)puVar17 / 10);
    } while (bVar10);
    *(undefined1 *)((long)&uStack_168 + lVar21 + 1) = 0;
    if (8 < lVar21 + 8U) {
      puVar17 = (undefined1 *)((long)&uStack_168 + lVar21);
      puVar22 = (undefined1 *)((long)&uStack_168 + 1);
      do {
        uVar5 = *puVar17;
        *puVar17 = puVar22[-1];
        puVar22[-1] = uVar5;
        bVar10 = puVar22 < puVar17 + -1;
        puVar17 = puVar17 + -1;
        puVar22 = puVar22 + 1;
      } while (bVar10);
    }
    if ((DAT_0a280023 & 1) == 0) {
      _DAT_0a280008 = CONCAT44((int)DAT_084e32b8,(int)DAT_084e32b0);
      uRam000000000a280010 = CONCAT44((int)DAT_084d87b8,(int)DAT_084e32c0);
      DAT_0a280018 = CONCAT44((int)DAT_084e32d0,(int)DAT_084e32c8);
      DAT_0a280020 = 0x5f25;
      DAT_0a280022 = 0;
      DAT_0a280023 = 1;
    }
    local_350 = &local_100;
    ppuStack_348 = &local_170;
    pppppppuStack_338 = (undefined8 *******)0x0;
    local_340 = (undefined1 *)0x0;
    uStack_328 = 0;
    local_330 = 0;
    uStack_318 = 0;
    local_320 = 0;
    uStack_308 = 0;
    local_310 = 0;
    uStack_2f8 = 0;
    local_300 = 0;
    uStack_2e8 = 0;
    local_2f0 = 0;
    uStack_2d8 = 0;
    local_2e0 = 0;
    FUN_05e1d31c(&local_2c0,&DAT_0a280008,&local_350);
    thunk_FUN_05e1d0bc(&local_2c0);
    if ((long)local_1c0 < 0) {
      __ZdlPvm(local_1d0,(ulong)local_1c0 & 0x7fffffffffffffff);
    }
  }
  FUN_046dd184();
  thunk_FUN_0003e800();
  _SetMMMojoConfiguration(1000);
  local_110 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_128 = &SUB_aaaaaaaaaaaaaaaa;
  local_130 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_118 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_120 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_148 = &SUB_aaaaaaaaaaaaaaaa;
  local_150 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_138 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_140 = &SUB_aaaaaaaaaaaaaaaa;
  uStack_168 = &SUB_aaaaaaaaaaaaaaaa;
  local_170 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
  puStack_158 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_160 = &SUB_aaaaaaaaaaaaaaaa;
  thunk_FUN_0001f100(&local_170);
  FUN_000405bc(FUN_0124addc);
  puStack_398 = &SUB_aaaaaaaaaaaaaaaa;
  local_3a0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_3b8 = &SUB_aaaaaaaaaaaaaaaa;
  local_3c0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_3a8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_3b0 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_00085bc0(&local_3c0,1);
  puStack_3d8 = &SUB_aaaaaaaaaaaaaaaa;
  local_3e0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_3c8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_3d0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_3e8 = &SUB_aaaaaaaaaaaaaaaa;
  local_3f0 = &SUB_aaaaaaaaaaaaaaaa;
  thunk_FUN_0005db28(&local_3f0,0);
  FUN_0124ae4c(&local_3f0);
  uVar20 = FUN_0473bb8c();
  if ((uVar20 & 1) == 0) {
    uVar24 = 0xffffffff;
  }
  else {
    FUN_0473c74c(&local_350,4);
    FUN_0002def0(&local_2c0,&local_350);
    FUN_048e3cec(&local_2c0);
    if ((long)local_2b0 < 0) {
      __ZdlPvm(local_2c0,local_2b0 & 0x7fffffffffffffff);
    }
    FUN_0002b440(&local_350);
    uVar24 = FUN_0002270c();
    local_408 = 0;
    uStack_400 = 0;
    local_3f8 = 0;
    FUN_000235d4(&local_2c0);
    ppuVar9 = ppuStack_2b8;
    ppuVar8 = local_2c0;
    if (local_2c0 != (undefined **)0x0) {
      for (; local_2c0 != ppuStack_2b8; ppuStack_2b8 = ppuStack_2b8 + -3) {
      }
      ppuStack_2b8 = local_2c0;
      __ZdlPvm(local_2c0,local_2b0 - (long)local_2c0);
    }
    if (ppuVar8 == ppuVar9) {
      iVar11 = thunk_FUN_05e1d97c(2);
      if (iVar11 != 0) {
        FUN_0488143c(&local_100);
        if ((DAT_0a27fee7 & 1) == 0) {
          DAT_0a27fed8._0_1_ = s_wechat_main__084e3218[0];
          DAT_0a27fed8._1_1_ = s_wechat_main__084e3218[1];
          DAT_0a27fed8._2_1_ = s_wechat_main__084e3218[2];
          DAT_0a27fed8._3_1_ = s_wechat_main__084e3218[3];
          DAT_0a27fed8._4_1_ = s_wechat_main__084e3218[4];
          DAT_0a27fed8._5_1_ = s_wechat_main__084e3218[5];
          DAT_0a27fed8._6_1_ = s_wechat_main__084e3218[6];
          DAT_0a27fed8._7_1_ = s_wechat_main__084e3218[7];
          DAT_0a27fee0 = (undefined4)ram0x084e3220;
          DAT_0a27fee4 = 0x6363;
          DAT_0a27fee6 = 0;
          DAT_0a27fee7 = 1;
        }
        if ((DAT_0a27ffa4 & 1) == 0) {
          DAT_0a27ff98._0_1_ = s_wechat_main__084e3218[0];
          DAT_0a27ff98._1_1_ = s_wechat_main__084e3218[1];
          DAT_0a27ff98._2_1_ = s_wechat_main__084e3218[2];
          DAT_0a27ff98._3_1_ = s_wechat_main__084e3218[3];
          DAT_0a27ff98._4_1_ = s_wechat_main__084e3218[4];
          DAT_0a27ff98._5_1_ = s_wechat_main__084e3218[5];
          DAT_0a27ff98._6_1_ = s_wechat_main__084e3218[6];
          DAT_0a27ff98._7_1_ = s_wechat_main__084e3218[7];
          DAT_0a27ffa0 = (undefined4)ram0x0848d960;
          DAT_0a27ffa4 = 1;
        }
        FUN_05e1d050(&local_2c0,2,&local_100,&DAT_0a27fed8,&DAT_0a27ff98,0x24d,0,0);
        if ((DAT_0a280030 & 1) == 0) {
          DAT_0a280028[0] = s_no_args_084e32d8[0];
          DAT_0a280028[1] = s_no_args_084e32d8[1];
          DAT_0a280028[2] = s_no_args_084e32d8[2];
          DAT_0a280028[3] = s_no_args_084e32d8[3];
          DAT_0a280028[4] = s_no_args_084e32d8[4];
          DAT_0a280028[5] = s_no_args_084e32d8[5];
          DAT_0a280028[6] = s_no_args_084e32d8[6];
          DAT_0a280028[7] = s_no_args_084e32d8[7];
          DAT_0a280030 = 1;
        }
        uStack_2e8 = 0;
        local_2f0 = 0;
        uStack_2d8 = 0;
        local_2e0 = 0;
        uStack_308 = 0;
        local_310 = 0;
        uStack_2f8 = 0;
        local_300 = 0;
        uStack_328 = 0;
        local_330 = 0;
        uStack_318 = 0;
        local_320 = 0;
        ppuStack_348 = (undefined8 **)0x0;
        local_350 = (undefined8 *******)0x0;
        pppppppuStack_338 = (undefined8 *******)0x0;
        local_340 = (undefined1 *)0x0;
        FUN_05e1d31c(&local_2c0,DAT_0a280028,&local_350);
        thunk_FUN_05e1d0bc(&local_2c0);
      }
    }
    else {
      FUN_000235d4(&local_2c0,uVar24);
      ppuVar9 = ppuStack_2b8;
      for (ppuVar8 = local_2c0; ppuVar8 != ppuVar9; ppuVar8 = ppuVar8 + 3) {
        if ((DAT_0a280026 & 1) == 0) {
          DAT_0a280024 = 0x20;
          DAT_0a280026 = 1;
        }
        bVar6 = *(byte *)((long)ppuVar8 + 0x17);
        puVar3 = ppuVar8[1];
        if (-1 < (char)bVar6) {
          puVar3 = (undefined *)(ulong)bVar6;
        }
        sVar13 = _strlen((char *)&DAT_0a280024);
        local_350 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
        ppuStack_348 = (undefined8 **)&SUB_aaaaaaaaaaaaaaaa;
        local_340 = &SUB_aaaaaaaaaaaaaaaa;
        ppuVar1 = (undefined8 **)(puVar3 + sVar13);
        if ((undefined8 **)0x7ffffffffffffff7 < ppuVar1) {
                    /* WARNING: Subroutine does not return */
          FUN_00018d9c(&local_350);
        }
        if (ppuVar1 < (undefined8 **)((long)&MACH_HEADER.sizeofcmds + 3)) {
          ppuStack_348 = (undefined8 **)0x0;
          local_350 = (undefined8 *******)0x0;
          pppppppuVar14 = &local_350;
          local_340 = (undefined1 *)((long)ppuVar1 << 0x38);
        }
        else {
          uVar20 = 0x19;
          if (((ulong)ppuVar1 | 7) != 0x17) {
            uVar20 = ((ulong)ppuVar1 | 7) + 1;
          }
          pppppppuVar14 = (undefined8 *******)__Znwm(uVar20);
          local_340 = (undefined1 *)(uVar20 | 0x8000000000000000);
          ppuStack_348 = ppuVar1;
          local_350 = pppppppuVar14;
        }
        if (puVar3 != (undefined *)0x0) {
          ppuVar4 = (undefined **)*ppuVar8;
          if (-1 < (char)bVar6) {
            ppuVar4 = ppuVar8;
          }
          _memmove(pppppppuVar14,ppuVar4,(size_t)puVar3);
        }
        if (sVar13 != 0) {
          _memmove((undefined *)((long)pppppppuVar14 + (long)puVar3),&DAT_0a280024,sVar13);
        }
        ((undefined *)((long)pppppppuVar14 + (long)puVar3))[sVar13] = 0;
        ppuVar1 = ppuStack_348;
        pppppppuVar14 = local_350;
        if (-1 < (long)local_340) {
          ppuVar1 = (undefined8 **)((ulong)local_340 >> 0x38);
          pppppppuVar14 = &local_350;
        }
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
                  (&local_408,pppppppuVar14,ppuVar1);
        if ((long)local_340 < 0) {
          __ZdlPvm(local_350,(ulong)local_340 & 0x7fffffffffffffff);
        }
      }
      if (local_2c0 != (undefined **)0x0) {
        for (; ppuStack_2b8 != local_2c0; ppuStack_2b8 = ppuStack_2b8 + -3) {
        }
        ppuStack_2b8 = local_2c0;
        __ZdlPvm(local_2c0,local_2b0 - (long)local_2c0);
      }
    }
    FUN_000235d4(&local_2c0,uVar24);
    uVar20 = FUN_00286154(&local_408,local_2c0 != ppuStack_2b8);
    if (local_2c0 != (undefined **)0x0) {
      for (; ppuStack_2b8 != local_2c0; ppuStack_2b8 = ppuStack_2b8 + -3) {
      }
      ppuStack_2b8 = local_2c0;
      __ZdlPvm(local_2c0,local_2b0 - (long)local_2c0);
    }
    if ((uVar20 & 1) == 0) {
      uVar24 = 0xffffffff;
    }
    else {
      FUN_04062e70();
      FUN_04062f38();
      iVar11 = thunk_FUN_05e1d97c(2);
      if (iVar11 != 0) {
        FUN_0488143c(&local_100);
        if ((DAT_0a27fee7 & 1) == 0) {
          DAT_0a27fed8._0_1_ = s_wechat_main__084e3218[0];
          DAT_0a27fed8._1_1_ = s_wechat_main__084e3218[1];
          DAT_0a27fed8._2_1_ = s_wechat_main__084e3218[2];
          DAT_0a27fed8._3_1_ = s_wechat_main__084e3218[3];
          DAT_0a27fed8._4_1_ = s_wechat_main__084e3218[4];
          DAT_0a27fed8._5_1_ = s_wechat_main__084e3218[5];
          DAT_0a27fed8._6_1_ = s_wechat_main__084e3218[6];
          DAT_0a27fed8._7_1_ = s_wechat_main__084e3218[7];
          DAT_0a27fee0 = (undefined4)ram0x084e3220;
          DAT_0a27fee4 = 0x6363;
          DAT_0a27fee6 = 0;
          DAT_0a27fee7 = 1;
        }
        if ((DAT_0a27ffa4 & 1) == 0) {
          DAT_0a27ff98._0_1_ = s_wechat_main__084e3218[0];
          DAT_0a27ff98._1_1_ = s_wechat_main__084e3218[1];
          DAT_0a27ff98._2_1_ = s_wechat_main__084e3218[2];
          DAT_0a27ff98._3_1_ = s_wechat_main__084e3218[3];
          DAT_0a27ff98._4_1_ = s_wechat_main__084e3218[4];
          DAT_0a27ff98._5_1_ = s_wechat_main__084e3218[5];
          DAT_0a27ff98._6_1_ = s_wechat_main__084e3218[6];
          DAT_0a27ff98._7_1_ = s_wechat_main__084e3218[7];
          DAT_0a27ffa0 = (undefined4)ram0x0848d960;
          DAT_0a27ffa4 = 1;
        }
        FUN_05e1d050(&local_2c0,2,&local_100,&DAT_0a27fed8,&DAT_0a27ff98,0x2bf,0,0);
        if ((DAT_0a280050 & 1) == 0) {
          uRam000000000a280048._0_1_ = s_user_disable_gpupre_wechat_main_084e33a0[0x18];
          uRam000000000a280048._1_1_ = s_user_disable_gpupre_wechat_main_084e33a0[0x19];
          uRam000000000a280048._2_1_ = s_user_disable_gpupre_wechat_main_084e33a0[0x1a];
          uRam000000000a280048._3_1_ = s_user_disable_gpupre_wechat_main_084e33a0[0x1b];
          uRam000000000a280048._4_1_ = s_user_disable_gpupre_wechat_main_084e33a0[0x1c];
          uRam000000000a280048._5_1_ = s_user_disable_gpupre_wechat_main_084e33a0[0x1d];
          uRam000000000a280048._6_1_ = s_user_disable_gpupre_wechat_main_084e33a0[0x1e];
          uRam000000000a280048._7_1_ = s_user_disable_gpupre_wechat_main_084e33a0[0x1f];
          DAT_0a280040 = s_user_disable_gpupre_wechat_main_084e33a0[0x10];
          DAT_0a280040_1._0_1_ = s_user_disable_gpupre_wechat_main_084e33a0[0x11];
          DAT_0a280040_1._1_1_ = s_user_disable_gpupre_wechat_main_084e33a0[0x12];
          DAT_0a280040_1._2_1_ = s_user_disable_gpupre_wechat_main_084e33a0[0x13];
          DAT_0a280040_1._3_1_ = s_user_disable_gpupre_wechat_main_084e33a0[0x14];
          DAT_0a280040_1._4_1_ = s_user_disable_gpupre_wechat_main_084e33a0[0x15];
          DAT_0a280040_1._5_1_ = s_user_disable_gpupre_wechat_main_084e33a0[0x16];
          DAT_0a280040_1._6_1_ = s_user_disable_gpupre_wechat_main_084e33a0[0x17];
          DAT_0a280050 = 1;
        }
        uStack_2e8 = 0;
        local_2f0 = 0;
        uStack_2d8 = 0;
        local_2e0 = 0;
        uStack_308 = 0;
        local_310 = 0;
        uStack_2f8 = 0;
        local_300 = 0;
        uStack_328 = 0;
        local_330 = 0;
        uStack_318 = 0;
        local_320 = 0;
        ppuStack_348 = (undefined8 **)0x0;
        local_350 = (undefined8 *******)0x0;
        pppppppuStack_338 = (undefined8 *******)0x0;
        local_340 = (undefined1 *)0x0;
        FUN_05e1d31c(&local_2c0,&DAT_0a280040,&local_350);
        thunk_FUN_05e1d0bc(&local_2c0);
      }
      uVar26 = local_354;
      _SetMMMojoConfiguration(0);
      _InitializeMMMojo(uVar26,param_2);
      if ((DAT_0a28007a & 1) == 0) {
        DAT_0a280070._0_1_ = s_AdjustDpQT_D_084e32e0[0];
        DAT_0a280070._1_1_ = s_AdjustDpQT_D_084e32e0[1];
        DAT_0a280070._2_1_ = s_AdjustDpQT_D_084e32e0[2];
        DAT_0a280070._3_1_ = s_AdjustDpQT_D_084e32e0[3];
        DAT_0a280070._4_1_ = s_AdjustDpQT_D_084e32e0[4];
        DAT_0a280070._5_1_ = s_AdjustDpQT_D_084e32e0[5];
        DAT_0a280070._6_1_ = s_AdjustDpQT_D_084e32e0[6];
        DAT_0a280070._7_1_ = s_AdjustDpQT_D_084e32e0[7];
        DAT_0a280078 = 0x69;
        DAT_0a28007a = 1;
      }
      FUN_06ed0084(&local_2c0,&DAT_0a280070,0xffffffff);
      if ((DAT_0a28006d & 1) == 0) {
        _DAT_0a280054 = CONCAT44((int)DAT_084e32f0,(int)ram0x084e32e8);
        uRam000000000a28005c = CONCAT44((int)DAT_084e3300,(int)DAT_084e32f8);
        DAT_0a280064 = CONCAT44((int)DAT_0848be70,(int)DAT_084e3308);
        DAT_0a28006c = 0;
        DAT_0a28006d = 1;
      }
      FUN_06e9271c(&DAT_0a280054,&local_2c0);
      if (*(int *)local_2c0 != -1) {
        if (*(int *)local_2c0 != 0) {
          LOAcquire();
          iVar11 = *(int *)local_2c0;
          *(int *)local_2c0 = iVar11 + -1;
          LORelease();
          if (iVar11 != 1) goto LAB_002ca95c;
        }
        FUN_06ea14cc(local_2c0,1,8);
      }
LAB_002ca95c:
      FUN_06fbd560(0x14,1);
      FUN_06fbd560(4,1);
      FUN_06fbd560(0xd,1);
      FUN_06c63f1c(5);
      FUN_002c8ed8(0);
      lVar12 = __Znwm(0x18);
      thunk_FUN_002b6c10(lVar12,&local_354,param_2);
      local_410 = lVar12;
      FUN_06c647e4(1);
      FUN_0216705c();
      uVar24 = FUN_04062e70();
      FUN_04065594(uVar24,&local_408);
      FUN_020da3b8();
      local_180 = (undefined1 **)&SUB_aaaaaaaaaaaaaaaa;
      puStack_198 = &SUB_aaaaaaaaaaaaaaaa;
      local_1a0 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_188 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_190 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_1b8 = &SUB_aaaaaaaaaaaaaaaa;
      local_1c0 = &SUB_aaaaaaaaaaaaaaaa;
      local_1a8 = (int *)&SUB_aaaaaaaaaaaaaaaa;
      local_1b0 = (long *)&SUB_aaaaaaaaaaaaaaaa;
      puStack_1c8 = &SUB_aaaaaaaaaaaaaaaa;
      local_1d0 = (int *******)&SUB_aaaaaaaaaaaaaaaa;
      FUN_002cc9e0(&local_1d0);
      local_2c0 = &PTR_FUN_09bf9218;
      ppuStack_2b8 = (undefined **)FUN_012471ec;
      local_2a8 = &local_2c0;
      FUN_002cd998(&local_2c0,&puStack_198);
      if (local_2a8 == &local_2c0) {
        pcVar18 = (code *)(*local_2a8)[4];
LAB_002caac4:
        (*pcVar18)();
      }
      else if (local_2a8 != (undefined ***)0x0) {
        pcVar18 = (code *)(*local_2a8)[5];
        goto LAB_002caac4;
      }
      uStack_218 = _UNK_084e3468;
      local_220 = _DAT_084e3460;
      uStack_208 = _UNK_084e3478;
      uStack_210 = _DAT_084e3470;
      uStack_1f8 = _UNK_084e3488;
      local_200 = _DAT_084e3480;
      uStack_1e8 = _UNK_084e3498;
      uStack_1f0 = _DAT_084e3490;
      uStack_258 = _UNK_084e3428;
      local_260 = _DAT_084e3420;
      uStack_248 = _UNK_084e3438;
      local_250 = _DAT_084e3430;
      uStack_238 = _UNK_084e3448;
      local_240 = _DAT_084e3440;
      uStack_228 = _UNK_084e3458;
      uStack_230 = _DAT_084e3450;
      ppuStack_298 = _UNK_084e33e8;
      local_2a0 = _DAT_084e33e0;
      local_288 = _UNK_084e33f8;
      local_290 = _DAT_084e33f0;
      uStack_278 = (undefined4)_UNK_084e3408;
      iStack_274 = (int)((ulong)_UNK_084e3408 >> 0x20);
      local_280 = (undefined4)_DAT_084e3400;
      uStack_27c = (undefined4)((ulong)_DAT_084e3400 >> 0x20);
      local_268 = _UNK_084e3418;
      local_270 = (undefined4)_DAT_084e3410;
      uStack_26c = (undefined4)((ulong)_DAT_084e3410 >> 0x20);
      ppuStack_2b8 = _UNK_084e33c8;
      local_2c0 = _DAT_084e33c0;
      local_2a8 = (undefined ***)_UNK_084e33d8;
      local_2b0 = _DAT_084e33d0;
      local_1e0 = &SUB_aaaaaaaaaaaaaaaa;
      thunk_FUN_020cd4b0(&local_2c0,&local_1d0);
      FUN_002b732c(lVar12);
      FUN_0211324c();
      if ((DAT_0a27ffa4 & 1) == 0) {
        DAT_0a27ff98._0_1_ = s_wechat_main__084e3218[0];
        DAT_0a27ff98._1_1_ = s_wechat_main__084e3218[1];
        DAT_0a27ff98._2_1_ = s_wechat_main__084e3218[2];
        DAT_0a27ff98._3_1_ = s_wechat_main__084e3218[3];
        DAT_0a27ff98._4_1_ = s_wechat_main__084e3218[4];
        DAT_0a27ff98._5_1_ = s_wechat_main__084e3218[5];
        DAT_0a27ff98._6_1_ = s_wechat_main__084e3218[6];
        DAT_0a27ff98._7_1_ = s_wechat_main__084e3218[7];
        DAT_0a27ffa0 = (undefined4)ram0x0848d960;
        DAT_0a27ffa4 = 1;
      }
      if ((DAT_0a2800cf & 1) == 0) {
        uVar20 = 0;
        do {
          uVar26 = *(undefined4 *)((long)&DAT_084e3921 + uVar20);
          uVar7 = CONCAT12((char)((uint)uVar26 >> 8),(short)uVar26) & 0xff00ff;
          uVar27 = *(undefined4 *)((long)&DAT_084e390d + uVar20 % 0x14);
          *(uint *)((long)&DAT_0a28007b + uVar20) =
               CONCAT13((char)((uint)uVar26 >> 0x18) + 0x8aU ^ (byte)((uint)uVar27 >> 0x18),
                        CONCAT12((char)((uint)uVar26 >> 0x10) + 0x8aU ^ (byte)((uint)uVar27 >> 0x10)
                                 ,CONCAT11((char)(uVar7 >> 0x10) + 0x8aU ^ (byte)((uint)uVar27 >> 8)
                                           ,(char)uVar7 + 0x8aU ^ (byte)uVar27)));
          uVar20 = uVar20 + 4;
        } while (uVar20 != 0x54);
        DAT_0a2800cf = 1;
      }
      FUN_0003bb6c(&local_350,&DAT_0a27ff98,&DAT_0a28007b,0x307);
      FUN_0005dbf0(&local_3f0,&local_350);
      iVar11 = thunk_FUN_05e1d97c(2);
      if (iVar11 != 0) {
        FUN_0488143c(local_428);
        pppppppuVar14 = local_428[0];
        if (-1 < cStack_411) {
          pppppppuVar14 = local_428;
        }
        if ((DAT_0a27fee7 & 1) == 0) {
          DAT_0a27fed8._0_1_ = s_wechat_main__084e3218[0];
          DAT_0a27fed8._1_1_ = s_wechat_main__084e3218[1];
          DAT_0a27fed8._2_1_ = s_wechat_main__084e3218[2];
          DAT_0a27fed8._3_1_ = s_wechat_main__084e3218[3];
          DAT_0a27fed8._4_1_ = s_wechat_main__084e3218[4];
          DAT_0a27fed8._5_1_ = s_wechat_main__084e3218[5];
          DAT_0a27fed8._6_1_ = s_wechat_main__084e3218[6];
          DAT_0a27fed8._7_1_ = s_wechat_main__084e3218[7];
          DAT_0a27fee0 = (undefined4)ram0x084e3220;
          DAT_0a27fee4 = 0x6363;
          DAT_0a27fee6 = 0;
          DAT_0a27fee7 = 1;
        }
        if ((DAT_0a27ffa4 & 1) == 0) {
          DAT_0a27ff98._0_1_ = s_wechat_main__084e3218[0];
          DAT_0a27ff98._1_1_ = s_wechat_main__084e3218[1];
          DAT_0a27ff98._2_1_ = s_wechat_main__084e3218[2];
          DAT_0a27ff98._3_1_ = s_wechat_main__084e3218[3];
          DAT_0a27ff98._4_1_ = s_wechat_main__084e3218[4];
          DAT_0a27ff98._5_1_ = s_wechat_main__084e3218[5];
          DAT_0a27ff98._6_1_ = s_wechat_main__084e3218[6];
          DAT_0a27ff98._7_1_ = s_wechat_main__084e3218[7];
          DAT_0a27ffa0 = (undefined4)ram0x0848d960;
          DAT_0a27ffa4 = 1;
        }
        FUN_05e1d050(&local_350,2,pppppppuVar14,&DAT_0a27fed8,&DAT_0a27ff98,0x30a,0,0);
        if ((DAT_0a2800e7 & 1) == 0) {
          _DAT_0a2800d0 = CONCAT44((int)DAT_084e3310,(int)DAT_084a2ea0);
          uRam000000000a2800d8 = CONCAT44((int)DAT_08486578,(int)DAT_084d5890);
          DAT_0a2800e0 = (undefined4)DAT_084e3318;
          DAT_0a2800e4 = 0x7469;
          DAT_0a2800e6 = 0;
          DAT_0a2800e7 = 1;
        }
        uStack_98 = 0;
        local_a0 = 0;
        uStack_88 = 0;
        uStack_90 = 0;
        uStack_b8 = 0;
        local_c0 = 0;
        uStack_a8 = 0;
        uStack_b0 = 0;
        uStack_d8 = 0;
        local_e0 = 0;
        uStack_c8 = 0;
        uStack_d0 = 0;
        uStack_f8 = (undefined8 ****)0x0;
        local_100 = (undefined8 ******)0x0;
        uStack_e8 = 0;
        local_f0 = 0;
        FUN_05e1d31c(&local_350,&DAT_0a2800d0,&local_100);
        thunk_FUN_05e1d0bc(&local_350);
        if (cStack_411 < '\0') {
          __ZdlPvm(local_428[0],CONCAT17(cStack_411,local_418) & 0x7fffffffffffffff);
        }
      }
      plVar15 = (long *)FUN_011a8d5c();
      (**(code **)(*plVar15 + 0x60))();
      iVar11 = thunk_FUN_05e1d97c(2);
      if (iVar11 != 0) {
        FUN_0488143c(local_428);
        pppppppuVar14 = local_428[0];
        if (-1 < cStack_411) {
          pppppppuVar14 = local_428;
        }
        if ((DAT_0a27fee7 & 1) == 0) {
          DAT_0a27fed8._0_1_ = s_wechat_main__084e3218[0];
          DAT_0a27fed8._1_1_ = s_wechat_main__084e3218[1];
          DAT_0a27fed8._2_1_ = s_wechat_main__084e3218[2];
          DAT_0a27fed8._3_1_ = s_wechat_main__084e3218[3];
          DAT_0a27fed8._4_1_ = s_wechat_main__084e3218[4];
          DAT_0a27fed8._5_1_ = s_wechat_main__084e3218[5];
          DAT_0a27fed8._6_1_ = s_wechat_main__084e3218[6];
          DAT_0a27fed8._7_1_ = s_wechat_main__084e3218[7];
          DAT_0a27fee0 = (undefined4)ram0x084e3220;
          DAT_0a27fee4 = 0x6363;
          DAT_0a27fee6 = 0;
          DAT_0a27fee7 = 1;
        }
        if ((DAT_0a27ffa4 & 1) == 0) {
          DAT_0a27ff98._0_1_ = s_wechat_main__084e3218[0];
          DAT_0a27ff98._1_1_ = s_wechat_main__084e3218[1];
          DAT_0a27ff98._2_1_ = s_wechat_main__084e3218[2];
          DAT_0a27ff98._3_1_ = s_wechat_main__084e3218[3];
          DAT_0a27ff98._4_1_ = s_wechat_main__084e3218[4];
          DAT_0a27ff98._5_1_ = s_wechat_main__084e3218[5];
          DAT_0a27ff98._6_1_ = s_wechat_main__084e3218[6];
          DAT_0a27ff98._7_1_ = s_wechat_main__084e3218[7];
          DAT_0a27ffa0 = (undefined4)ram0x0848d960;
          DAT_0a27ffa4 = 1;
        }
        FUN_05e1d050(&local_350,2,pppppppuVar14,&DAT_0a27fed8,&DAT_0a27ff98,0x30c,0,0);
        if ((DAT_0a2800fe & 1) == 0) {
          _DAT_0a2800e8 = CONCAT44((int)DAT_084e3328,(int)DAT_084e3320);
          uRam000000000a2800f0 = CONCAT44((int)DAT_084caec0,(int)DAT_084e3330);
          DAT_0a2800f8 = (undefined4)DAT_084e3338;
          DAT_0a2800fc = 0x74;
          DAT_0a2800fe = 1;
        }
        uStack_98 = 0;
        local_a0 = 0;
        uStack_88 = 0;
        uStack_90 = 0;
        uStack_b8 = 0;
        local_c0 = 0;
        uStack_a8 = 0;
        uStack_b0 = 0;
        uStack_d8 = 0;
        local_e0 = 0;
        uStack_c8 = 0;
        uStack_d0 = 0;
        uStack_f8 = (undefined8 ****)0x0;
        local_100 = (undefined8 ******)0x0;
        uStack_e8 = 0;
        local_f0 = 0;
        FUN_05e1d31c(&local_350,&DAT_0a2800e8,&local_100);
        thunk_FUN_05e1d0bc(&local_350);
        if (cStack_411 < '\0') {
          __ZdlPvm(local_428[0],CONCAT17(cStack_411,local_418) & 0x7fffffffffffffff);
        }
      }
      lVar12 = local_410;
      local_410 = 0;
      if (lVar12 != 0) {
        uVar24 = thunk_FUN_002b7288();
        __ZdlPvm(uVar24,0x18);
      }
      iVar11 = thunk_FUN_05e1d97c(2);
      if (iVar11 != 0) {
        FUN_0488143c(local_428);
        pppppppuVar14 = local_428[0];
        if (-1 < cStack_411) {
          pppppppuVar14 = local_428;
        }
        if ((DAT_0a27fee7 & 1) == 0) {
          DAT_0a27fed8._0_1_ = s_wechat_main__084e3218[0];
          DAT_0a27fed8._1_1_ = s_wechat_main__084e3218[1];
          DAT_0a27fed8._2_1_ = s_wechat_main__084e3218[2];
          DAT_0a27fed8._3_1_ = s_wechat_main__084e3218[3];
          DAT_0a27fed8._4_1_ = s_wechat_main__084e3218[4];
          DAT_0a27fed8._5_1_ = s_wechat_main__084e3218[5];
          DAT_0a27fed8._6_1_ = s_wechat_main__084e3218[6];
          DAT_0a27fed8._7_1_ = s_wechat_main__084e3218[7];
          DAT_0a27fee0 = (undefined4)ram0x084e3220;
          DAT_0a27fee4 = 0x6363;
          DAT_0a27fee6 = 0;
          DAT_0a27fee7 = 1;
        }
        if ((DAT_0a27ffa4 & 1) == 0) {
          DAT_0a27ff98._0_1_ = s_wechat_main__084e3218[0];
          DAT_0a27ff98._1_1_ = s_wechat_main__084e3218[1];
          DAT_0a27ff98._2_1_ = s_wechat_main__084e3218[2];
          DAT_0a27ff98._3_1_ = s_wechat_main__084e3218[3];
          DAT_0a27ff98._4_1_ = s_wechat_main__084e3218[4];
          DAT_0a27ff98._5_1_ = s_wechat_main__084e3218[5];
          DAT_0a27ff98._6_1_ = s_wechat_main__084e3218[6];
          DAT_0a27ff98._7_1_ = s_wechat_main__084e3218[7];
          DAT_0a27ffa0 = (undefined4)ram0x0848d960;
          DAT_0a27ffa4 = 1;
        }
        FUN_05e1d050(&local_350,2,pppppppuVar14,&DAT_0a27fed8,&DAT_0a27ff98,0x312,0,0);
        if ((DAT_0a28010b & 1) == 0) {
          DAT_0a280100._0_1_ = s_app_Uninkernel_URequ_084e3340[0];
          DAT_0a280100._1_1_ = s_app_Uninkernel_URequ_084e3340[1];
          DAT_0a280100._2_1_ = s_app_Uninkernel_URequ_084e3340[2];
          DAT_0a280100._3_1_ = s_app_Uninkernel_URequ_084e3340[3];
          DAT_0a280100._4_1_ = s_app_Uninkernel_URequ_084e3340[4];
          DAT_0a280100._5_1_ = s_app_Uninkernel_URequ_084e3340[5];
          DAT_0a280100._6_1_ = s_app_Uninkernel_URequ_084e3340[6];
          DAT_0a280100._7_1_ = s_app_Uninkernel_URequ_084e3340[7];
          DAT_0a280108 = 0x7469;
          DAT_0a28010a = 0;
          DAT_0a28010b = 1;
        }
        uStack_98 = 0;
        local_a0 = 0;
        uStack_88 = 0;
        uStack_90 = 0;
        uStack_b8 = 0;
        local_c0 = 0;
        uStack_a8 = 0;
        uStack_b0 = 0;
        uStack_d8 = 0;
        local_e0 = 0;
        uStack_c8 = 0;
        uStack_d0 = 0;
        uStack_f8 = (undefined8 ****)0x0;
        local_100 = (undefined8 ******)0x0;
        uStack_e8 = 0;
        local_f0 = 0;
        FUN_05e1d31c(&local_350,&DAT_0a280100,&local_100);
        thunk_FUN_05e1d0bc(&local_350);
        if (cStack_411 < '\0') {
          __ZdlPvm(local_428[0],CONCAT17(cStack_411,local_418) & 0x7fffffffffffffff);
        }
      }
      pppppppuStack_338 = (undefined8 *******)0x0;
      FUN_020f6178(&local_350);
      if ((undefined8 ********)pppppppuStack_338 == &local_350) {
        pppppuVar19 = (*pppppppuStack_338)[4];
LAB_002cb044:
        (*(code *)pppppuVar19)();
      }
      else if (pppppppuStack_338 != (undefined8 *******)0x0) {
        pppppuVar19 = (*pppppppuStack_338)[5];
        goto LAB_002cb044;
      }
      FUN_04671338();
      FUN_02112ab8(1);
      FUN_06079930();
      FUN_020f7390();
      iVar11 = thunk_FUN_05e1d97c(2);
      if (iVar11 != 0) {
        FUN_0488143c(local_428);
        pppppppuVar14 = local_428[0];
        if (-1 < cStack_411) {
          pppppppuVar14 = local_428;
        }
        if ((DAT_0a27fee7 & 1) == 0) {
          DAT_0a27fed8._0_1_ = s_wechat_main__084e3218[0];
          DAT_0a27fed8._1_1_ = s_wechat_main__084e3218[1];
          DAT_0a27fed8._2_1_ = s_wechat_main__084e3218[2];
          DAT_0a27fed8._3_1_ = s_wechat_main__084e3218[3];
          DAT_0a27fed8._4_1_ = s_wechat_main__084e3218[4];
          DAT_0a27fed8._5_1_ = s_wechat_main__084e3218[5];
          DAT_0a27fed8._6_1_ = s_wechat_main__084e3218[6];
          DAT_0a27fed8._7_1_ = s_wechat_main__084e3218[7];
          DAT_0a27fee0 = (undefined4)ram0x084e3220;
          DAT_0a27fee4 = 0x6363;
          DAT_0a27fee6 = 0;
          DAT_0a27fee7 = 1;
        }
        if ((DAT_0a27ffa4 & 1) == 0) {
          DAT_0a27ff98._0_1_ = s_wechat_main__084e3218[0];
          DAT_0a27ff98._1_1_ = s_wechat_main__084e3218[1];
          DAT_0a27ff98._2_1_ = s_wechat_main__084e3218[2];
          DAT_0a27ff98._3_1_ = s_wechat_main__084e3218[3];
          DAT_0a27ff98._4_1_ = s_wechat_main__084e3218[4];
          DAT_0a27ff98._5_1_ = s_wechat_main__084e3218[5];
          DAT_0a27ff98._6_1_ = s_wechat_main__084e3218[6];
          DAT_0a27ff98._7_1_ = s_wechat_main__084e3218[7];
          DAT_0a27ffa0 = (undefined4)ram0x0848d960;
          DAT_0a27ffa4 = 1;
        }
        FUN_05e1d050(&local_350,2,pppppppuVar14,&DAT_0a27fed8,&DAT_0a27ff98,0x31d,0,0);
        if ((DAT_0a28011e & 1) == 0) {
          DAT_0a280110._0_1_ = s_app_Uninkernel_URequ_084e3340[8];
          DAT_0a280110._1_1_ = s_app_Uninkernel_URequ_084e3340[9];
          DAT_0a280110._2_1_ = s_app_Uninkernel_URequ_084e3340[10];
          DAT_0a280110._3_1_ = s_app_Uninkernel_URequ_084e3340[0xb];
          DAT_0a280110._4_1_ = s_app_Uninkernel_URequ_084e3340[0xc];
          DAT_0a280110._5_1_ = s_app_Uninkernel_URequ_084e3340[0xd];
          DAT_0a280110._6_1_ = s_app_Uninkernel_URequ_084e3340[0xe];
          DAT_0a280110._7_1_ = s_app_Uninkernel_URequ_084e3340[0xf];
          DAT_0a280118 = (undefined4)DAT_084e3338;
          DAT_0a28011c = 0x74;
          DAT_0a28011e = 1;
        }
        uStack_98 = 0;
        local_a0 = 0;
        uStack_88 = 0;
        uStack_90 = 0;
        uStack_b8 = 0;
        local_c0 = 0;
        uStack_a8 = 0;
        uStack_b0 = 0;
        uStack_d8 = 0;
        local_e0 = 0;
        uStack_c8 = 0;
        uStack_d0 = 0;
        uStack_f8 = (undefined8 ****)0x0;
        local_100 = (undefined8 ******)0x0;
        uStack_e8 = 0;
        local_f0 = 0;
        FUN_05e1d31c(&local_350,&DAT_0a280110,&local_100);
        thunk_FUN_05e1d0bc(&local_350);
        if (cStack_411 < '\0') {
          __ZdlPvm(local_428[0],CONCAT17(cStack_411,local_418) & 0x7fffffffffffffff);
        }
      }
      thunk_FUN_020cd764(&local_2c0);
      if (local_180 == &puStack_198) {
        pcVar18 = *(code **)(*local_180 + 0x20);
LAB_002cb1c0:
        (*pcVar18)();
      }
      else if (local_180 != (undefined1 **)0x0) {
        pcVar18 = *(code **)(*local_180 + 0x28);
        goto LAB_002cb1c0;
      }
      if (*local_1a8 != -1) {
        if (*local_1a8 != 0) {
          LOAcquire();
          iVar11 = *local_1a8;
          *local_1a8 = iVar11 + -1;
          LORelease();
          if (iVar11 != 1) goto LAB_002cb1f8;
        }
        FUN_06ea14cc(local_1a8,2,8);
      }
LAB_002cb1f8:
      if (local_1b0 == (long *)((ulong)&local_1d0 | 8)) {
        pcVar18 = *(code **)(*local_1b0 + 0x20);
LAB_002cb224:
        (*pcVar18)();
      }
      else if (local_1b0 != (long *)0x0) {
        pcVar18 = *(code **)(*local_1b0 + 0x28);
        goto LAB_002cb224;
      }
      pppppppiVar2 = local_1d0;
      if (*(int *)local_1d0 != -1) {
        if (*(int *)local_1d0 != 0) {
          LOAcquire();
          iVar11 = *(int *)local_1d0;
          *(int *)local_1d0 = iVar11 + -1;
          LORelease();
          if (iVar11 != 1) goto LAB_002cb264;
        }
        iVar11 = *(int *)((long)local_1d0 + 0xc);
        if (iVar11 != *(int *)(local_1d0 + 1)) {
          pppppppiVar25 = local_1d0 + (long)iVar11 + 1;
          lVar12 = (long)*(int *)(local_1d0 + 1) * 8 + (long)iVar11 * -8;
          do {
            ppppppiVar16 = *pppppppiVar25;
            if (*(int *)ppppppiVar16 != -1) {
              if (*(int *)ppppppiVar16 != 0) {
                LOAcquire();
                iVar11 = *(int *)ppppppiVar16;
                *(int *)ppppppiVar16 = iVar11 + -1;
                LORelease();
                if (iVar11 != 1) goto LAB_002cb2b4;
                ppppppiVar16 = *pppppppiVar25;
              }
              FUN_06ea14cc(ppppppiVar16,2,8);
            }
LAB_002cb2b4:
            pppppppiVar25 = pppppppiVar25 + -1;
            lVar12 = lVar12 + 8;
          } while (lVar12 != 0);
        }
        _free(pppppppiVar2);
      }
LAB_002cb264:
      if (local_410 != 0) {
        uVar24 = thunk_FUN_002b7288();
        __ZdlPvm(uVar24,0x18);
      }
      _ShutdownMMMojo();
      uVar24 = 0;
    }
    if ((long)local_3f8 < 0) {
      __ZdlPvm(local_408,local_3f8 & 0x7fffffffffffffff);
    }
  }
  FUN_0005dba8(&local_3f0);
  FUN_00085c20(&local_3c0);
  FUN_0001f378(&local_170);
  FUN_05e24800();
  FUN_05e24848();
  FUN_00033bec(&local_370);
  FUN_00033bec(&local_360);
LAB_002caa80:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_78) {
    return uVar24;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


