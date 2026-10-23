// Ghidra inferred pseudocode; requested=0x2fd0768
// entry=02fd0768 end=02fd3977

/* WARNING: Removing unreachable block (ram,0x02fd3918) */
/* WARNING: Removing unreachable block (ram,0x02fd38cc) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_02fd0768(undefined8 *param_1,long param_2,undefined8 param_3,long *******param_4,
                 undefined8 param_5,undefined8 param_6,undefined8 param_7,undefined8 param_8,
                 undefined1 param_9)

{
  undefined8 *******pppppppuVar1;
  long *******ppppppplVar2;
  undefined1 uVar3;
  uint3 uVar4;
  bool bVar5;
  undefined1 *puVar6;
  int iVar7;
  int iVar8;
  long lVar9;
  undefined1 *puVar10;
  undefined8 *puVar11;
  undefined8 uVar12;
  long *plVar13;
  long *plVar14;
  undefined8 uVar15;
  char *pcVar16;
  undefined8 ******ppppppuVar17;
  undefined8 *******pppppppuVar18;
  undefined8 ****ppppuVar19;
  undefined8 ****ppppuVar20;
  undefined8 ****ppppuVar21;
  uint uVar22;
  undefined8 *****pppppuVar23;
  uint uVar24;
  undefined1 *puVar25;
  long lVar26;
  ulong uVar27;
  long lVar28;
  undefined4 uVar29;
  undefined4 uVar30;
  undefined8 *******local_418 [2];
  undefined7 local_408;
  char cStack_401;
  undefined8 local_400;
  undefined1 *puStack_3f8;
  undefined1 *local_3f0;
  undefined1 *puStack_3e8;
  undefined8 ******local_3e0;
  long *local_3d8;
  undefined8 *******local_3d0;
  undefined8 uStack_3c8;
  ulong local_3c0;
  ulong uStack_3b8;
  long *local_3b0;
  long *local_3a8;
  undefined8 *******local_398;
  ulong local_390;
  ulong local_388;
  undefined8 *******local_380;
  undefined1 *puStack_378;
  undefined8 local_370;
  undefined1 *puStack_368;
  undefined1 *puStack_360;
  undefined1 *puStack_358;
  undefined1 *local_350;
  undefined1 local_33a;
  undefined1 local_339;
  long *******local_338;
  undefined1 *local_330;
  undefined1 *local_328;
  undefined8 *******local_320;
  undefined1 *local_318;
  undefined1 *local_310;
  undefined8 local_308;
  undefined8 uStack_300;
  ulong local_2f8;
  undefined8 *******local_2f0;
  ulong local_2e8;
  ulong local_2e0;
  undefined8 *******local_2d8;
  undefined1 *local_2d0;
  undefined1 *local_2c8;
  undefined1 *local_2c0;
  undefined1 *puStack_2b8;
  undefined1 *local_2b0;
  undefined8 uStack_2a8;
  undefined1 auStack_2a0 [8];
  long *local_298;
  undefined8 *******local_290;
  undefined1 *puStack_288;
  undefined1 *local_280;
  undefined8 *******pppppppuStack_278;
  undefined8 ******local_270;
  long *local_268;
  undefined1 uStack_201;
  undefined8 local_200;
  undefined8 local_1f8;
  undefined7 local_1f0;
  char cStack_1e9;
  undefined1 uStack_1b1;
  undefined8 local_1b0;
  undefined8 uStack_1a8;
  undefined8 local_1a0;
  undefined1 *puStack_198;
  undefined1 *local_190;
  undefined1 *local_188;
  undefined1 *local_180;
  undefined1 *puStack_178;
  undefined1 *puStack_170;
  undefined8 uStack_168;
  undefined8 local_160;
  undefined8 local_158;
  undefined7 local_150;
  char cStack_149;
  undefined8 *******local_110;
  undefined8 *puStack_108;
  undefined8 *local_100;
  undefined8 uStack_f8;
  long local_f0;
  undefined8 uStack_e8;
  undefined8 local_e0;
  undefined8 uStack_d8;
  undefined8 local_d0;
  undefined8 uStack_c8;
  undefined8 local_c0;
  undefined8 uStack_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  long local_88;
  
  local_88 = *(long *)PTR____stack_chk_guard_09b36c98;
  iVar7 = thunk_FUN_05e1d97c(2);
  if (iVar7 != 0) {
    FUN_0488143c(&local_160);
    ppppppplVar2 = local_160;
    if (-1 < cStack_149) {
      ppppppplVar2 = (long *******)&local_160;
    }
    if ((DAT_0a3d2361 & 1) == 0) {
      uRam000000000a3d2358._0_1_ = s_login_manager_ccauto_login_close_0889c040[8];
      uRam000000000a3d2358._1_1_ = s_login_manager_ccauto_login_close_0889c040[9];
      uRam000000000a3d2358._2_1_ = s_login_manager_ccauto_login_close_0889c040[10];
      uRam000000000a3d2358._3_1_ = s_login_manager_ccauto_login_close_0889c040[0xb];
      uRam000000000a3d2358._4_1_ = s_login_manager_ccauto_login_close_0889c040[0xc];
      uRam000000000a3d2358._5_1_ = s_login_manager_ccauto_login_close_0889c040[0xd];
      uRam000000000a3d2358._6_1_ = s_login_manager_ccauto_login_close_0889c040[0xe];
      uRam000000000a3d2358._7_1_ = s_login_manager_ccauto_login_close_0889c040[0xf];
      DAT_0a3d2350 = s_login_manager_ccauto_login_close_0889c040[0];
      DAT_0a3d2350_1._0_1_ = s_login_manager_ccauto_login_close_0889c040[1];
      DAT_0a3d2350_1._1_1_ = s_login_manager_ccauto_login_close_0889c040[2];
      DAT_0a3d2350_1._2_1_ = s_login_manager_ccauto_login_close_0889c040[3];
      DAT_0a3d2350_1._3_1_ = s_login_manager_ccauto_login_close_0889c040[4];
      DAT_0a3d2350_1._4_1_ = s_login_manager_ccauto_login_close_0889c040[5];
      DAT_0a3d2350_1._5_1_ = s_login_manager_ccauto_login_close_0889c040[6];
      DAT_0a3d2350_1._6_1_ = s_login_manager_ccauto_login_close_0889c040[7];
      DAT_0a3d2360 = 0;
      DAT_0a3d2361 = 1;
    }
    if ((DAT_0a3d2a23 & 1) == 0) {
      DAT_0a3d2a18 = DAT_0889c418;
      DAT_0a3d2a20 = 0x6874;
      DAT_0a3d2a22 = 0;
      DAT_0a3d2a23 = 1;
    }
    FUN_05e1d050(&local_290,2,ppppppplVar2,&DAT_0a3d2350,&DAT_0a3d2a18,0x344,0,0);
    if ((DAT_0a3d2a23 & 1) == 0) {
      DAT_0a3d2a18 = DAT_0889c418;
      DAT_0a3d2a20 = 0x6874;
      DAT_0a3d2a22 = 0;
      DAT_0a3d2a23 = 1;
    }
    uStack_a8 = 0;
    local_b0 = 0;
    uStack_98 = 0;
    local_a0 = 0;
    uStack_c8 = 0;
    local_d0 = 0;
    uStack_b8 = 0;
    local_c0 = 0;
    uStack_e8 = 0;
    local_f0 = 0;
    uStack_d8 = 0;
    local_e0 = 0;
    puStack_108 = (undefined8 *)0x0;
    local_110 = (undefined8 *******)0x0;
    uStack_f8 = 0;
    local_100 = (undefined8 *)0x0;
    FUN_05e1d31c(&local_290,&DAT_0a3d2a18,&local_110);
    thunk_FUN_05e1d0bc(&local_290);
    if (cStack_149 < '\0') {
      __ZdlPvm(local_160,CONCAT17(cStack_149,local_150) & 0x7fffffffffffffff);
    }
  }
  lVar9 = FUN_04669774();
  *(undefined1 *)(lVar9 + 0x2c8) = 0;
  FUN_0301181c(auStack_2a0,*(undefined8 *)(param_2 + 0x2b0),param_4);
  if (local_298 != (long *)0x0) {
    LOAcquire();
    lVar9 = local_298[1];
    local_298[1] = lVar9 + -1;
    LORelease();
    if (lVar9 == 0) {
      (**(code **)(*local_298 + 0x10))(local_298);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_298);
    }
  }
  puStack_2b8 = &SUB_aaaaaaaaaaaaaaaa;
  local_2c0 = &SUB_aaaaaaaaaaaaaaaa;
  uStack_2a8 = &SUB_aaaaaaaaaaaaaaaa;
  local_2b0 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_050c7168(&local_2c0);
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x100000000);
  if (puStack_2b8 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0x38);
    FUN_050c70c4();
    puStack_2b8 = puVar10;
  }
  puVar10 = puStack_2b8;
  *(uint *)(puStack_2b8 + 0x34) = *(uint *)(puStack_2b8 + 0x34) | 4;
  puVar11 = *(undefined8 **)(puStack_2b8 + 0x18);
  if (puVar11 == &DAT_0a524ad0) {
    puVar11 = (undefined8 *)__Znwm(0x18);
    *puVar11 = 0;
    puVar11[1] = 0;
    puVar11[2] = 0;
    *(undefined8 **)(puVar10 + 0x18) = puVar11;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar11,param_4);
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x100000000);
  if (puStack_2b8 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0x38);
    FUN_050c70c4();
    puStack_2b8 = puVar10;
  }
  puVar10 = puStack_2b8;
  *(uint *)(puStack_2b8 + 0x34) = *(uint *)(puStack_2b8 + 0x34) | 8;
  puVar11 = *(undefined8 **)(puStack_2b8 + 0x20);
  if (puVar11 == &DAT_0a524ad0) {
    puVar11 = (undefined8 *)__Znwm(0x18);
    *puVar11 = 0;
    puVar11[1] = 0;
    puVar11[2] = 0;
    *(undefined8 **)(puVar10 + 0x20) = puVar11;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar11,param_5);
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x100000000);
  if (puStack_2b8 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0x38);
    FUN_050c70c4();
    puStack_2b8 = puVar10;
  }
  puVar10 = puStack_2b8;
  *(uint *)(puStack_2b8 + 0x34) = *(uint *)(puStack_2b8 + 0x34) | 0x10;
  puVar11 = *(undefined8 **)(puStack_2b8 + 0x28);
  if (puVar11 == &DAT_0a524ad0) {
    puVar11 = (undefined8 *)__Znwm(0x18);
    *puVar11 = 0;
    puVar11[1] = 0;
    puVar11[2] = 0;
    *(undefined8 **)(puVar10 + 0x28) = puVar11;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar11,param_6);
  local_2d0 = &SUB_aaaaaaaaaaaaaaaa;
  local_2c8 = &SUB_aaaaaaaaaaaaaaaa;
  local_2d8 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
  FUN_06686abc(&local_2d8,0x10);
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x100000000);
  if (puStack_2b8 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0x38);
    FUN_050c70c4();
    puStack_2b8 = puVar10;
  }
  puVar10 = puStack_2b8;
  *(uint *)(puStack_2b8 + 0x34) = *(uint *)(puStack_2b8 + 0x34) | 1;
  lVar9 = *(long *)(puStack_2b8 + 8);
  if (lVar9 == 0) {
    lVar9 = __Znwm(0x20);
    FUN_04f33be0();
    *(long *)(puVar10 + 8) = lVar9;
  }
  pppppppuVar18 = local_2d8;
  if (-1 < (long)local_2c8) {
    pppppppuVar18 = &local_2d8;
  }
  *(uint *)(lVar9 + 0x18) = *(uint *)(lVar9 + 0x18) | 2;
  puVar11 = *(undefined8 **)(lVar9 + 8);
  if (puVar11 == &DAT_0a524ad0) {
    puVar11 = (undefined8 *)__Znwm(0x18);
    *puVar11 = 0;
    puVar11[1] = 0;
    puVar11[2] = 0;
    *(undefined8 **)(lVar9 + 8) = puVar11;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKcm
            (puVar11,pppppppuVar18,0x10);
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x100000000);
  if (puStack_2b8 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0x38);
    FUN_050c70c4();
    puStack_2b8 = puVar10;
  }
  puVar10 = puStack_2b8;
  *(uint *)(puStack_2b8 + 0x34) = *(uint *)(puStack_2b8 + 0x34) | 1;
  lVar9 = *(long *)(puStack_2b8 + 8);
  if (lVar9 == 0) {
    lVar9 = __Znwm(0x20);
    FUN_04f33be0();
    *(long *)(puVar10 + 8) = lVar9;
  }
  *(uint *)(lVar9 + 0x18) = *(uint *)(lVar9 + 0x18) | 1;
  *(undefined4 *)(lVar9 + 0x10) = 0x10;
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x100000000);
  if (puStack_2b8 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0x38);
    FUN_050c70c4();
    puStack_2b8 = puVar10;
  }
  puVar10 = puStack_2b8;
  *(uint *)(puStack_2b8 + 0x34) = *(uint *)(puStack_2b8 + 0x34) | 2;
  lVar9 = *(long *)(puStack_2b8 + 0x10);
  if (lVar9 == 0) {
    lVar9 = __Znwm(0x20);
    FUN_04f33c1c();
    *(long *)(puVar10 + 0x10) = lVar9;
  }
  *(uint *)(lVar9 + 0x18) = *(uint *)(lVar9 + 0x18) | 1;
  *(undefined4 *)(lVar9 + 0x10) = 0x2c9;
  local_2f0 = (undefined8 *******)0x0;
  local_2e8 = 0;
  local_2e0 = 0;
  local_308 = 0;
  uStack_300 = 0;
  local_2f8 = 0;
  iVar7 = FUN_05a861b4(0x2c9,&local_2f0,&local_308);
  if (0 < iVar7) {
    uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x100000000);
    if (puStack_2b8 == (undefined1 *)0x0) {
      puVar10 = (undefined1 *)__Znwm(0x38);
      FUN_050c70c4();
      puStack_2b8 = puVar10;
    }
    puVar10 = puStack_2b8;
    *(uint *)(puStack_2b8 + 0x34) = *(uint *)(puStack_2b8 + 0x34) | 2;
    lVar9 = *(long *)(puStack_2b8 + 0x10);
    if (lVar9 == 0) {
      lVar9 = __Znwm(0x20);
      FUN_04f33c1c();
      *(long *)(puVar10 + 0x10) = lVar9;
    }
    *(uint *)(lVar9 + 0x18) = *(uint *)(lVar9 + 0x18) | 2;
    lVar28 = *(long *)(lVar9 + 8);
    if (lVar28 == 0) {
      lVar28 = __Znwm(0x20);
      FUN_04f33be0();
      *(long *)(lVar9 + 8) = lVar28;
    }
    uVar27 = local_2e8;
    pppppppuVar18 = local_2f0;
    if (-1 < (long)local_2e0) {
      uVar27 = local_2e0 >> 0x38;
      pppppppuVar18 = &local_2f0;
    }
    *(uint *)(lVar28 + 0x18) = *(uint *)(lVar28 + 0x18) | 2;
    puVar11 = *(undefined8 **)(lVar28 + 8);
    if (puVar11 == &DAT_0a524ad0) {
      puVar11 = (undefined8 *)__Znwm(0x18);
      *puVar11 = 0;
      puVar11[1] = 0;
      puVar11[2] = 0;
      *(undefined8 **)(lVar28 + 8) = puVar11;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKcm
              (puVar11,pppppppuVar18,uVar27);
    uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x100000000);
    if (puStack_2b8 == (undefined1 *)0x0) {
      puVar10 = (undefined1 *)__Znwm(0x38);
      FUN_050c70c4();
      puStack_2b8 = puVar10;
    }
    puVar10 = puStack_2b8;
    *(uint *)(puStack_2b8 + 0x34) = *(uint *)(puStack_2b8 + 0x34) | 2;
    lVar9 = *(long *)(puStack_2b8 + 0x10);
    if (lVar9 == 0) {
      lVar9 = __Znwm(0x20);
      FUN_04f33c1c();
      *(long *)(puVar10 + 0x10) = lVar9;
    }
    *(uint *)(lVar9 + 0x18) = *(uint *)(lVar9 + 0x18) | 2;
    lVar28 = *(long *)(lVar9 + 8);
    if (lVar28 == 0) {
      lVar28 = __Znwm(0x20);
      FUN_04f33be0();
      *(long *)(lVar9 + 8) = lVar28;
    }
    uVar27 = local_2e8;
    if (-1 < (long)local_2e0) {
      uVar27 = local_2e0 >> 0x38;
    }
    *(uint *)(lVar28 + 0x18) = *(uint *)(lVar28 + 0x18) | 1;
    *(int *)(lVar28 + 0x10) = (int)uVar27;
  }
  uVar12 = FUN_04670584(param_3);
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x200000000);
  if (local_2b0 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0xd8);
    FUN_050c7110();
    local_2b0 = puVar10;
  }
  puVar10 = local_2b0;
  *(uint *)(local_2b0 + 0xd0) = *(uint *)(local_2b0 + 0xd0) | 1;
  lVar9 = *(long *)(local_2b0 + 8);
  if (lVar9 == 0) {
    lVar9 = __Znwm(0x38);
    FUN_0465a1bc();
    *(long *)(puVar10 + 8) = lVar9;
  }
  *(uint *)(lVar9 + 0x34) = *(uint *)(lVar9 + 0x34) | 1;
  puVar11 = *(undefined8 **)(lVar9 + 8);
  if (puVar11 == &DAT_0a524ad0) {
    puVar11 = (undefined8 *)__Znwm(0x18);
    *puVar11 = 0;
    puVar11[1] = 0;
    puVar11[2] = 0;
    *(undefined8 **)(lVar9 + 8) = puVar11;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKcm(puVar11,"",1);
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x200000000);
  if (local_2b0 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0xd8);
    FUN_050c7110();
    local_2b0 = puVar10;
  }
  puVar10 = local_2b0;
  *(uint *)(local_2b0 + 0xd0) = *(uint *)(local_2b0 + 0xd0) | 1;
  lVar9 = *(long *)(local_2b0 + 8);
  if (lVar9 == 0) {
    lVar9 = __Znwm(0x38);
    FUN_0465a1bc();
    *(long *)(puVar10 + 8) = lVar9;
  }
  *(uint *)(lVar9 + 0x34) = *(uint *)(lVar9 + 0x34) | 2;
  *(undefined8 *)(lVar9 + 0x10) = uVar12;
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x200000000);
  if (local_2b0 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0xd8);
    FUN_050c7110();
    local_2b0 = puVar10;
  }
  puVar10 = local_2b0;
  *(uint *)(local_2b0 + 0xd0) = *(uint *)(local_2b0 + 0xd0) | 1;
  lVar9 = *(long *)(local_2b0 + 8);
  if (lVar9 == 0) {
    lVar9 = __Znwm(0x38);
    FUN_0465a1bc();
    *(long *)(puVar10 + 8) = lVar9;
  }
  plVar13 = (long *)FUN_04669774();
  (**(code **)(*plVar13 + 0x10))();
  FUN_04672230(&local_290);
  pppppppuVar18 = local_290;
  if (-1 < (long)local_280) {
    pppppppuVar18 = &local_290;
  }
  *(uint *)(lVar9 + 0x34) = *(uint *)(lVar9 + 0x34) | 4;
  puVar11 = *(undefined8 **)(lVar9 + 0x18);
  if (puVar11 == &DAT_0a524ad0) {
    puVar11 = (undefined8 *)__Znwm(0x18);
    *puVar11 = 0;
    puVar11[1] = 0;
    puVar11[2] = 0;
    *(undefined8 **)(lVar9 + 0x18) = puVar11;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKcm
            (puVar11,pppppppuVar18,0x10);
  if ((long)local_280 < 0) {
    __ZdlPvm(local_290,(ulong)local_280 & 0x7fffffffffffffff);
  }
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x200000000);
  if (local_2b0 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0xd8);
    FUN_050c7110();
    local_2b0 = puVar10;
  }
  puVar10 = local_2b0;
  *(uint *)(local_2b0 + 0xd0) = *(uint *)(local_2b0 + 0xd0) | 1;
  lVar9 = *(long *)(local_2b0 + 8);
  if (lVar9 == 0) {
    lVar9 = __Znwm(0x38);
    FUN_0465a1bc();
    *(long *)(puVar10 + 8) = lVar9;
  }
  plVar13 = (long *)FUN_04669774();
  lVar28 = (**(code **)(*plVar13 + 0x10))();
  uVar29 = *(undefined4 *)(lVar28 + 0x60);
  *(uint *)(lVar9 + 0x34) = *(uint *)(lVar9 + 0x34) | 8;
  *(undefined4 *)(lVar9 + 0x28) = uVar29;
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x200000000);
  if (local_2b0 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0xd8);
    FUN_050c7110();
    local_2b0 = puVar10;
  }
  puVar10 = local_2b0;
  *(uint *)(local_2b0 + 0xd0) = *(uint *)(local_2b0 + 0xd0) | 1;
  lVar9 = *(long *)(local_2b0 + 8);
  if (lVar9 == 0) {
    lVar9 = __Znwm(0x38);
    FUN_0465a1bc();
    *(long *)(puVar10 + 8) = lVar9;
  }
  plVar13 = (long *)FUN_04669774();
  lVar28 = (**(code **)(*plVar13 + 0x10))();
  plVar13 = (long *)*(long *)(lVar28 + 0x88);
  if (-1 < *(char *)(lVar28 + 0x9f)) {
    plVar13 = (long *)(lVar28 + 0x88);
  }
  plVar14 = (long *)FUN_04669774();
  lVar28 = (**(code **)(*plVar14 + 0x10))();
  uVar27 = *(ulong *)(lVar28 + 0x90);
  if (-1 < (char)*(byte *)(lVar28 + 0x9f)) {
    uVar27 = (ulong)*(byte *)(lVar28 + 0x9f);
  }
  *(uint *)(lVar9 + 0x34) = *(uint *)(lVar9 + 0x34) | 0x10;
  puVar11 = *(undefined8 **)(lVar9 + 0x20);
  if (puVar11 == &DAT_0a524ad0) {
    puVar11 = (undefined8 *)__Znwm(0x18);
    *puVar11 = 0;
    puVar11[1] = 0;
    puVar11[2] = 0;
    *(undefined8 **)(lVar9 + 0x20) = puVar11;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKcm
            (puVar11,plVar13,uVar27);
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x200000000);
  if (local_2b0 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0xd8);
    FUN_050c7110();
    local_2b0 = puVar10;
  }
  puVar10 = local_2b0;
  *(uint *)(local_2b0 + 0xd0) = *(uint *)(local_2b0 + 0xd0) | 1;
  lVar9 = *(long *)(local_2b0 + 8);
  if (lVar9 == 0) {
    lVar9 = __Znwm(0x38);
    FUN_0465a1bc();
    *(long *)(puVar10 + 8) = lVar9;
  }
  *(uint *)(lVar9 + 0x34) = *(uint *)(lVar9 + 0x34) | 0x20;
  *(undefined4 *)(lVar9 + 0x2c) = 1;
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x200000000);
  if (local_2b0 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0xd8);
    FUN_050c7110();
    local_2b0 = puVar10;
  }
  puVar10 = local_2b0;
  *(uint *)(local_2b0 + 0xd0) = *(uint *)(local_2b0 + 0xd0) | 2;
  lVar9 = *(long *)(local_2b0 + 0x10);
  if (lVar9 == 0) {
    lVar9 = __Znwm(0x48);
    FUN_050c7094();
    *(long *)(puVar10 + 0x10) = lVar9;
  }
  *(uint *)(lVar9 + 0x40) = *(uint *)(lVar9 + 0x40) | 2;
  lVar28 = *(long *)(lVar9 + 0x10);
  if (lVar28 == 0) {
    lVar28 = __Znwm(0x30);
    FUN_050c70e8();
    *(long *)(lVar9 + 0x10) = lVar28;
  }
  *(uint *)(lVar28 + 0x2c) = *(uint *)(lVar28 + 0x2c) | 1;
  puVar11 = *(undefined8 **)(lVar28 + 8);
  if (puVar11 == &DAT_0a524ad0) {
    puVar11 = (undefined8 *)__Znwm(0x18);
    *puVar11 = 0;
    puVar11[1] = 0;
    puVar11[2] = 0;
    *(undefined8 **)(lVar28 + 8) = puVar11;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar11,param_7);
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x200000000);
  if (local_2b0 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0xd8);
    FUN_050c7110();
    local_2b0 = puVar10;
  }
  puVar10 = local_2b0;
  *(uint *)(local_2b0 + 0xd0) = *(uint *)(local_2b0 + 0xd0) | 2;
  lVar9 = *(long *)(local_2b0 + 0x10);
  if (lVar9 == 0) {
    lVar9 = __Znwm(0x48);
    FUN_050c7094();
    *(long *)(puVar10 + 0x10) = lVar9;
  }
  *(uint *)(lVar9 + 0x40) = *(uint *)(lVar9 + 0x40) | 2;
  lVar28 = *(long *)(lVar9 + 0x10);
  if (lVar28 == 0) {
    lVar28 = __Znwm(0x30);
    FUN_050c70e8();
    *(long *)(lVar9 + 0x10) = lVar28;
  }
  *(uint *)(lVar28 + 0x2c) = *(uint *)(lVar28 + 0x2c) | 1;
  puVar11 = *(undefined8 **)(lVar28 + 8);
  if (puVar11 == &DAT_0a524ad0) {
    puVar11 = (undefined8 *)__Znwm(0x18);
    *puVar11 = 0;
    puVar11[1] = 0;
    puVar11[2] = 0;
    *(undefined8 **)(lVar28 + 8) = puVar11;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar11,param_8);
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x200000000);
  if (local_2b0 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0xd8);
    FUN_050c7110();
    local_2b0 = puVar10;
  }
  puVar10 = local_2b0;
  uVar15 = FUN_048817a4();
  *(uint *)(puVar10 + 0xd0) = *(uint *)(puVar10 + 0xd0) | 0x20000;
  puVar11 = *(undefined8 **)(puVar10 + 0x88);
  if (puVar11 == &DAT_0a524ad0) {
    puVar11 = (undefined8 *)__Znwm(0x18);
    *puVar11 = 0;
    puVar11[1] = 0;
    puVar11[2] = 0;
    *(undefined8 **)(puVar10 + 0x88) = puVar11;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc(puVar11,uVar15);
  uVar24 = uStack_2a8._4_4_ | 2;
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x200000000);
  if (local_2b0 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0xd8);
    FUN_050c7110();
    uVar24 = uStack_2a8._4_4_;
    local_2b0 = puVar10;
  }
  *(uint *)(local_2b0 + 0xd0) = *(uint *)(local_2b0 + 0xd0) | 0x800;
  *(undefined4 *)(local_2b0 + 0x44) = 1000;
  uStack_2a8 = (undefined1 *)(CONCAT44(uVar24,(undefined4)uStack_2a8) | 0x200000000);
  if (local_2b0 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0xd8);
    FUN_050c7110();
    local_2b0 = puVar10;
  }
  puVar10 = local_2b0;
  plVar13 = (long *)FUN_04669774();
  lVar9 = (**(code **)(*plVar13 + 0x10))();
  *(uint *)(puVar10 + 0xd0) = *(uint *)(puVar10 + 0xd0) | 0x200;
  puVar11 = *(undefined8 **)(puVar10 + 0x50);
  if (puVar11 == &DAT_0a524ad0) {
    puVar11 = (undefined8 *)__Znwm(0x18);
    *puVar11 = 0;
    puVar11[1] = 0;
    puVar11[2] = 0;
    *(undefined8 **)(puVar10 + 0x50) = puVar11;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar11,lVar9 + 0x68);
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x200000000);
  if (local_2b0 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0xd8);
    FUN_050c7110();
    local_2b0 = puVar10;
  }
  puVar10 = local_2b0;
  plVar13 = (long *)FUN_04669774();
  lVar9 = (**(code **)(*plVar13 + 0x10))();
  plVar13 = (long *)*(long *)(lVar9 + 0xb8);
  if (-1 < *(char *)(lVar9 + 0xcf)) {
    plVar13 = (long *)(lVar9 + 0xb8);
  }
  plVar14 = (long *)FUN_04669774();
  lVar9 = (**(code **)(*plVar14 + 0x10))();
  uVar27 = *(ulong *)(lVar9 + 0xc0);
  if (-1 < (char)*(byte *)(lVar9 + 0xcf)) {
    uVar27 = (ulong)*(byte *)(lVar9 + 0xcf);
  }
  *(uint *)(puVar10 + 0xd0) = *(uint *)(puVar10 + 0xd0) | 0x2000;
  puVar11 = *(undefined8 **)(puVar10 + 0x60);
  if (puVar11 == &DAT_0a524ad0) {
    puVar11 = (undefined8 *)__Znwm(0x18);
    *puVar11 = 0;
    puVar11[1] = 0;
    puVar11[2] = 0;
    *(undefined8 **)(puVar10 + 0x60) = puVar11;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKcm
            (puVar11,plVar13,uVar27);
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x200000000);
  if (local_2b0 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0xd8);
    FUN_050c7110();
    local_2b0 = puVar10;
  }
  puVar10 = local_2b0;
  plVar13 = (long *)FUN_04669774();
  lVar9 = (**(code **)(*plVar13 + 0x10))();
  plVar13 = (long *)*(long *)(lVar9 + 0xa0);
  if (-1 < *(char *)(lVar9 + 0xb7)) {
    plVar13 = (long *)(lVar9 + 0xa0);
  }
  plVar14 = (long *)FUN_04669774();
  lVar9 = (**(code **)(*plVar14 + 0x10))();
  uVar27 = *(ulong *)(lVar9 + 0xa8);
  if (-1 < (char)*(byte *)(lVar9 + 0xb7)) {
    uVar27 = (ulong)*(byte *)(lVar9 + 0xb7);
  }
  *(uint *)(puVar10 + 0xd0) = *(uint *)(puVar10 + 0xd0) | 0x4000;
  puVar11 = *(undefined8 **)(puVar10 + 0x68);
  if (puVar11 == &DAT_0a524ad0) {
    puVar11 = (undefined8 *)__Znwm(0x18);
    *puVar11 = 0;
    puVar11[1] = 0;
    puVar11[2] = 0;
    *(undefined8 **)(puVar10 + 0x68) = puVar11;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKcm
            (puVar11,plVar13,uVar27);
  local_318 = &SUB_aaaaaaaaaaaaaaaa;
  local_310 = &SUB_aaaaaaaaaaaaaaaa;
  local_320 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0474b5d8(&local_320);
  local_330 = &SUB_aaaaaaaaaaaaaaaa;
  local_328 = &SUB_aaaaaaaaaaaaaaaa;
  local_338 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0474f5bc(&local_338);
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x200000000);
  if (local_2b0 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0xd8);
    FUN_050c7110();
    local_2b0 = puVar10;
  }
  puVar6 = local_2b0;
  puVar10 = local_318;
  pppppppuVar18 = local_320;
  if (-1 < (long)local_310) {
    puVar10 = (undefined1 *)((ulong)local_310 >> 0x38);
    pppppppuVar18 = &local_320;
  }
  *(uint *)(local_2b0 + 0xd0) = *(uint *)(local_2b0 + 0xd0) | 0x8000;
  puVar11 = *(undefined8 **)(local_2b0 + 0x70);
  if (puVar11 == &DAT_0a524ad0) {
    puVar11 = (undefined8 *)__Znwm(0x18);
    *puVar11 = 0;
    puVar11[1] = 0;
    puVar11[2] = 0;
    *(undefined8 **)(puVar6 + 0x70) = puVar11;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKcm
            (puVar11,pppppppuVar18,puVar10);
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x200000000);
  if (local_2b0 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0xd8);
    FUN_050c7110();
    local_2b0 = puVar10;
  }
  puVar10 = local_2b0;
  FUN_0474f6d4(&local_290);
  *(uint *)(puVar10 + 0xd0) = *(uint *)(puVar10 + 0xd0) | 0x400;
  puVar11 = *(undefined8 **)(puVar10 + 0x58);
  if (puVar11 == &DAT_0a524ad0) {
    puVar11 = (undefined8 *)__Znwm(0x18);
    *puVar11 = 0;
    puVar11[1] = 0;
    puVar11[2] = 0;
    *(undefined8 **)(puVar10 + 0x58) = puVar11;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar11,&local_290);
  if ((long)local_280 < 0) {
    __ZdlPvm(local_290,(ulong)local_280 & 0x7fffffffffffffff);
  }
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x200000000);
  if (local_2b0 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0xd8);
    FUN_050c7110();
    local_2b0 = puVar10;
  }
  puVar10 = local_2b0;
  FUN_04749dbc(&local_290);
  *(uint *)(puVar10 + 0xd0) = *(uint *)(puVar10 + 0xd0) | 0x40;
  puVar11 = *(undefined8 **)(puVar10 + 0x30);
  if (puVar11 == &DAT_0a524ad0) {
    puVar11 = (undefined8 *)__Znwm(0x18);
    *puVar11 = 0;
    puVar11[1] = 0;
    puVar11[2] = 0;
    *(undefined8 **)(puVar10 + 0x30) = puVar11;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar11,&local_290);
  if ((long)local_280 < 0) {
    __ZdlPvm(local_290,(ulong)local_280 & 0x7fffffffffffffff);
  }
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x200000000);
  if (local_2b0 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0xd8);
    FUN_050c7110();
    local_2b0 = puVar10;
  }
  puVar10 = local_2b0;
  *(uint *)(local_2b0 + 0xd0) = *(uint *)(local_2b0 + 0xd0) | 0x80;
  puVar11 = *(undefined8 **)(local_2b0 + 0x38);
  if (puVar11 == &DAT_0a524ad0) {
    puVar11 = (undefined8 *)__Znwm(0x18);
    *puVar11 = 0;
    puVar11[1] = 0;
    puVar11[2] = 0;
    *(undefined8 **)(puVar10 + 0x38) = puVar11;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar11,&local_338);
  iVar7 = thunk_FUN_05e1d97c(2);
  if (iVar7 != 0) {
    FUN_0488143c(&local_1b0);
    pppppppuVar18 = local_1b0;
    if (-1 < (long)local_1a0) {
      pppppppuVar18 = (undefined8 *******)&local_1b0;
    }
    if ((DAT_0a3d2361 & 1) == 0) {
      uRam000000000a3d2358._0_1_ = s_login_manager_ccauto_login_close_0889c040[8];
      uRam000000000a3d2358._1_1_ = s_login_manager_ccauto_login_close_0889c040[9];
      uRam000000000a3d2358._2_1_ = s_login_manager_ccauto_login_close_0889c040[10];
      uRam000000000a3d2358._3_1_ = s_login_manager_ccauto_login_close_0889c040[0xb];
      uRam000000000a3d2358._4_1_ = s_login_manager_ccauto_login_close_0889c040[0xc];
      uRam000000000a3d2358._5_1_ = s_login_manager_ccauto_login_close_0889c040[0xd];
      uRam000000000a3d2358._6_1_ = s_login_manager_ccauto_login_close_0889c040[0xe];
      uRam000000000a3d2358._7_1_ = s_login_manager_ccauto_login_close_0889c040[0xf];
      DAT_0a3d2350 = s_login_manager_ccauto_login_close_0889c040[0];
      DAT_0a3d2350_1._0_1_ = s_login_manager_ccauto_login_close_0889c040[1];
      DAT_0a3d2350_1._1_1_ = s_login_manager_ccauto_login_close_0889c040[2];
      DAT_0a3d2350_1._2_1_ = s_login_manager_ccauto_login_close_0889c040[3];
      DAT_0a3d2350_1._3_1_ = s_login_manager_ccauto_login_close_0889c040[4];
      DAT_0a3d2350_1._4_1_ = s_login_manager_ccauto_login_close_0889c040[5];
      DAT_0a3d2350_1._5_1_ = s_login_manager_ccauto_login_close_0889c040[6];
      DAT_0a3d2350_1._6_1_ = s_login_manager_ccauto_login_close_0889c040[7];
      DAT_0a3d2360 = 0;
      DAT_0a3d2361 = 1;
    }
    if ((DAT_0a3d2a23 & 1) == 0) {
      DAT_0a3d2a18 = DAT_0889c418;
      DAT_0a3d2a20 = 0x6874;
      DAT_0a3d2a22 = 0;
      DAT_0a3d2a23 = 1;
    }
    FUN_05e1d050(&local_290,2,pppppppuVar18,&DAT_0a3d2350,&DAT_0a3d2a18,0x378,0,0);
    local_160 = local_338;
    if (-1 < (long)local_328) {
      local_160 = (long *******)&local_338;
    }
    local_158._0_1_ = 0;
    if ((DAT_0a3d2b01 & 1) == 0) {
      uRam000000000a3d2af8._0_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x18];
      uRam000000000a3d2af8._1_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x19];
      uRam000000000a3d2af8._2_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x1a];
      uRam000000000a3d2af8._3_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x1b];
      uRam000000000a3d2af8._4_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x1c];
      uRam000000000a3d2af8._5_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x1d];
      uRam000000000a3d2af8._6_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x1e];
      uRam000000000a3d2af8._7_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x1f];
      DAT_0a3d2af0 = s_CheckLoginQRCodePCAccountName____0889c0b0[0x10];
      DAT_0a3d2af0_1._0_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x11];
      DAT_0a3d2af0_1._1_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x12];
      DAT_0a3d2af0_1._2_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x13];
      DAT_0a3d2af0_1._3_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x14];
      DAT_0a3d2af0_1._4_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x15];
      DAT_0a3d2af0_1._5_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x16];
      DAT_0a3d2af0_1._6_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x17];
      DAT_0a3d2b00 = 0;
      DAT_0a3d2b01 = 1;
    }
    local_100 = (undefined8 *)0x0;
    puStack_108 = (undefined8 *)0x0;
    local_110 = (undefined8 *******)&local_160;
    local_f0 = 0;
    uStack_f8 = 0;
    local_e0 = 0;
    uStack_e8 = 0;
    local_d0 = 0;
    uStack_d8 = 0;
    local_c0 = 0;
    uStack_c8 = 0;
    local_b0 = 0;
    uStack_b8 = 0;
    local_a0 = 0;
    uStack_a8 = 0;
    uStack_98 = 0;
    FUN_05e1d31c(&local_290,&DAT_0a3d2af0,&local_110);
    thunk_FUN_05e1d0bc(&local_290);
    if ((long)local_1a0 < 0) {
      __ZdlPvm(local_1b0,(ulong)local_1a0 & 0x7fffffffffffffff);
    }
  }
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x200000000);
  if (local_2b0 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0xd8);
    FUN_050c7110();
    local_2b0 = puVar10;
  }
  puVar10 = local_2b0;
  plVar13 = (long *)FUN_04669774();
  lVar9 = (**(code **)(*plVar13 + 0x10))();
  plVar13 = (long *)*(long *)(lVar9 + 0x88);
  if (-1 < *(char *)(lVar9 + 0x9f)) {
    plVar13 = (long *)(lVar9 + 0x88);
  }
  plVar14 = (long *)FUN_04669774();
  lVar9 = (**(code **)(*plVar14 + 0x10))();
  uVar27 = *(ulong *)(lVar9 + 0x90);
  if (-1 < (char)*(byte *)(lVar9 + 0x9f)) {
    uVar27 = (ulong)*(byte *)(lVar9 + 0x9f);
  }
  *(uint *)(puVar10 + 0xd0) = *(uint *)(puVar10 + 0xd0) | 0x100;
  puVar11 = *(undefined8 **)(puVar10 + 0x48);
  if (puVar11 == &DAT_0a524ad0) {
    puVar11 = (undefined8 *)__Znwm(0x18);
    *puVar11 = 0;
    puVar11[1] = 0;
    puVar11[2] = 0;
    *(undefined8 **)(puVar10 + 0x48) = puVar11;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKcm
            (puVar11,plVar13,uVar27);
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x200000000);
  if (local_2b0 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0xd8);
    FUN_050c7110();
    local_2b0 = puVar10;
  }
  puVar10 = local_2b0;
  FUN_0474a66c(&local_290);
  *(uint *)(puVar10 + 0xd0) = *(uint *)(puVar10 + 0xd0) | 8;
  puVar11 = *(undefined8 **)(puVar10 + 0x20);
  if (puVar11 == &DAT_0a524ad0) {
    puVar11 = (undefined8 *)__Znwm(0x18);
    *puVar11 = 0;
    puVar11[1] = 0;
    puVar11[2] = 0;
    *(undefined8 **)(puVar10 + 0x20) = puVar11;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar11,&local_290);
  if ((long)local_280 < 0) {
    __ZdlPvm(local_290,(ulong)local_280 & 0x7fffffffffffffff);
  }
  uVar24 = uStack_2a8._4_4_ | 2;
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x200000000);
  if (local_2b0 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0xd8);
    FUN_050c7110();
    uVar24 = uStack_2a8._4_4_;
    local_2b0 = puVar10;
  }
  uVar22 = *(uint *)(local_2b0 + 0xd0);
  *(uint *)(local_2b0 + 0xd0) = uVar22 | 0x100000;
  *(undefined4 *)(local_2b0 + 0x84) = 2;
  uStack_2a8 = (undefined1 *)(CONCAT44(uVar24,(undefined4)uStack_2a8) | 0x200000000);
  if (local_2b0 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0xd8);
    FUN_050c7110();
    uVar22 = *(uint *)(puVar10 + 0xd0) | 0x10;
    *(uint *)(puVar10 + 0xd0) = uVar22;
    *(undefined4 *)(puVar10 + 0x40) = 0;
    uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x200000000);
    local_2b0 = puVar10;
    if (puVar10 == (undefined1 *)0x0) {
      puVar10 = (undefined1 *)__Znwm(0xd8);
      FUN_050c7110();
      uVar22 = *(uint *)(puVar10 + 0xd0);
      local_2b0 = puVar10;
    }
  }
  else {
    uVar22 = uVar22 | 0x100010;
    *(uint *)(local_2b0 + 0xd0) = uVar22;
    *(undefined4 *)(local_2b0 + 0x40) = 0;
  }
  puVar10 = local_2b0;
  *(uint *)(local_2b0 + 0xd0) = uVar22 | 2;
  lVar9 = *(long *)(local_2b0 + 0x10);
  if (lVar9 == 0) {
    lVar9 = __Znwm(0x48);
    FUN_050c7094();
    *(long *)(puVar10 + 0x10) = lVar9;
  }
  *(uint *)(lVar9 + 0x40) = *(uint *)(lVar9 + 0x40) | 2;
  lVar28 = *(long *)(lVar9 + 0x10);
  if (lVar28 == 0) {
    lVar28 = __Znwm(0x30);
    FUN_050c70e8();
    *(long *)(lVar9 + 0x10) = lVar28;
  }
  *(uint *)(lVar28 + 0x2c) = *(uint *)(lVar28 + 0x2c) | 8;
  lVar9 = *(long *)(lVar28 + 0x20);
  if (lVar9 == 0) {
    lVar9 = __Znwm(0x20);
    FUN_04f33be0();
    *(long *)(lVar28 + 0x20) = lVar9;
  }
  *(uint *)(lVar9 + 0x18) = *(uint *)(lVar9 + 0x18) | 2;
  puVar11 = *(undefined8 **)(lVar9 + 8);
  if (puVar11 == &DAT_0a524ad0) {
    puVar11 = (undefined8 *)__Znwm(0x18);
    *puVar11 = 0;
    puVar11[1] = 0;
    puVar11[2] = 0;
    *(undefined8 **)(lVar9 + 8) = puVar11;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKcm(puVar11,"",1);
  uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x200000000);
  if (local_2b0 == (undefined1 *)0x0) {
    puVar10 = (undefined1 *)__Znwm(0xd8);
    FUN_050c7110();
    local_2b0 = puVar10;
  }
  puVar10 = local_2b0;
  *(uint *)(local_2b0 + 0xd0) = *(uint *)(local_2b0 + 0xd0) | 2;
  lVar9 = *(long *)(local_2b0 + 0x10);
  if (lVar9 == 0) {
    lVar9 = __Znwm(0x48);
    FUN_050c7094();
    *(long *)(puVar10 + 0x10) = lVar9;
  }
  *(uint *)(lVar9 + 0x40) = *(uint *)(lVar9 + 0x40) | 2;
  lVar28 = *(long *)(lVar9 + 0x10);
  if (lVar28 == 0) {
    lVar28 = __Znwm(0x30);
    FUN_050c70e8();
    *(long *)(lVar9 + 0x10) = lVar28;
  }
  *(uint *)(lVar28 + 0x2c) = *(uint *)(lVar28 + 0x2c) | 8;
  lVar9 = *(long *)(lVar28 + 0x20);
  if (lVar9 == 0) {
    lVar9 = __Znwm(0x20);
    FUN_04f33be0();
    *(long *)(lVar28 + 0x20) = lVar9;
  }
  *(uint *)(lVar9 + 0x18) = *(uint *)(lVar9 + 0x18) | 1;
  *(undefined4 *)(lVar9 + 0x10) = 1;
  local_339 = 1;
  local_350 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_368 = &SUB_aaaaaaaaaaaaaaaa;
  local_370 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_358 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_360 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_378 = &SUB_aaaaaaaaaaaaaaaa;
  local_380 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
  local_33a = param_9;
  FUN_02fd5084(&local_380,param_2,param_4,&local_33a);
  puVar10 = puStack_378;
  if (-1 < (long)local_370) {
    puVar10 = (undefined1 *)((ulong)local_370 >> 0x38);
  }
  if (puVar10 == (undefined1 *)0x0) {
    iVar7 = FUN_048849c0();
    iVar8 = thunk_FUN_05e1d97c(3);
    if (iVar8 != 0) {
      FUN_0488143c(&local_3d0);
      pppppppuVar18 = local_3d0;
      if (-1 < (long)local_3c0) {
        pppppppuVar18 = &local_3d0;
      }
      if ((DAT_0a3d2361 & 1) == 0) {
        uRam000000000a3d2358._0_1_ = s_login_manager_ccauto_login_close_0889c040[8];
        uRam000000000a3d2358._1_1_ = s_login_manager_ccauto_login_close_0889c040[9];
        uRam000000000a3d2358._2_1_ = s_login_manager_ccauto_login_close_0889c040[10];
        uRam000000000a3d2358._3_1_ = s_login_manager_ccauto_login_close_0889c040[0xb];
        uRam000000000a3d2358._4_1_ = s_login_manager_ccauto_login_close_0889c040[0xc];
        uRam000000000a3d2358._5_1_ = s_login_manager_ccauto_login_close_0889c040[0xd];
        uRam000000000a3d2358._6_1_ = s_login_manager_ccauto_login_close_0889c040[0xe];
        uRam000000000a3d2358._7_1_ = s_login_manager_ccauto_login_close_0889c040[0xf];
        DAT_0a3d2350 = s_login_manager_ccauto_login_close_0889c040[0];
        DAT_0a3d2350_1._0_1_ = s_login_manager_ccauto_login_close_0889c040[1];
        DAT_0a3d2350_1._1_1_ = s_login_manager_ccauto_login_close_0889c040[2];
        DAT_0a3d2350_1._2_1_ = s_login_manager_ccauto_login_close_0889c040[3];
        DAT_0a3d2350_1._3_1_ = s_login_manager_ccauto_login_close_0889c040[4];
        DAT_0a3d2350_1._4_1_ = s_login_manager_ccauto_login_close_0889c040[5];
        DAT_0a3d2350_1._5_1_ = s_login_manager_ccauto_login_close_0889c040[6];
        DAT_0a3d2350_1._6_1_ = s_login_manager_ccauto_login_close_0889c040[7];
        DAT_0a3d2360 = 0;
        DAT_0a3d2361 = 1;
      }
      if ((DAT_0a3d2a23 & 1) == 0) {
        DAT_0a3d2a18 = DAT_0889c418;
        DAT_0a3d2a20 = 0x6874;
        DAT_0a3d2a22 = 0;
        DAT_0a3d2a23 = 1;
      }
      FUN_05e1d050(&local_290,3,pppppppuVar18,&DAT_0a3d2350,&DAT_0a3d2a18,0x38e,0,0);
      local_160 = (long *******)*param_4;
      if (-1 < *(char *)((long)param_4 + 0x17)) {
        local_160 = param_4;
      }
      local_158._0_1_ = 0;
      FUN_02fd55b4(&local_400,&puStack_368);
      local_1b0 = local_400;
      if (-1 < (long)local_3f0) {
        local_1b0 = (undefined8 *******)&local_400;
      }
      uStack_1a8 = (undefined8 ******)((ulong)uStack_1a8 & 0xffffffffffffff00);
      if (iVar7 == 0) {
        local_200 = (undefined8 *)&DAT_0a3d3804;
        if ((DAT_0a3d380a & 1) == 0) {
          DAT_0a3d3804 = (undefined4)DAT_0847fe48;
          puVar6 = &DAT_0a3d3808;
          puVar10 = &DAT_0a3d3809;
          puVar25 = &DAT_0a3d380a;
          goto LAB_02fd1dc8;
        }
      }
      else {
        local_200 = (undefined8 *)&DAT_0a3d37fc;
        if ((DAT_0a3d3801 & 1) == 0) {
          DAT_0a3d37fc = 0x7274;
          DAT_0a3d37fe = 0x75;
          puVar10 = &DAT_0a3d3800;
          puVar6 = &DAT_0a3d37ff;
          puVar25 = &DAT_0a3d3801;
LAB_02fd1dc8:
          *puVar6 = 0x65;
          *puVar10 = 0;
          *puVar25 = 1;
        }
      }
      local_1f8._0_1_ = 0;
      if ((DAT_0a3d2b3a & 1) == 0) {
        _DAT_0a3d2b04 = CONCAT44((int)DAT_08784d70,(int)DAT_0889c428);
        uRam000000000a3d2b0c = CONCAT44((int)DAT_0849d5c0,(int)DAT_084ca328);
        _DAT_0a3d2b14 = CONCAT44((int)DAT_08502940,(int)ram0x0885ee80);
        uRam000000000a3d2b1c = CONCAT44((int)DAT_084d8788,(int)DAT_08502a00);
        _DAT_0a3d2b24 = CONCAT44((int)DAT_084fdd98,(int)DAT_084e3ff8);
        uRam000000000a3d2b2c = CONCAT44((int)DAT_08480588,(int)DAT_0878afb0);
        DAT_0a3d2b34 = (undefined4)DAT_0852aa68;
        DAT_0a3d2b38 = 0x5f;
        DAT_0a3d2b3a = 1;
      }
      local_110 = (undefined8 *******)&local_160;
      puStack_108 = &local_1b0;
      local_100 = &local_200;
      local_f0 = 0;
      uStack_f8 = 0;
      local_e0 = 0;
      uStack_e8 = 0;
      local_d0 = 0;
      uStack_d8 = 0;
      local_c0 = 0;
      uStack_c8 = 0;
      local_b0 = 0;
      uStack_b8 = 0;
      local_a0 = 0;
      uStack_a8 = 0;
      uStack_98 = 0;
      FUN_05e1d31c(&local_290,&DAT_0a3d2b04,&local_110);
      if ((long)local_3f0 < 0) {
        __ZdlPvm(local_400,(ulong)local_3f0 & 0x7fffffffffffffff);
      }
      thunk_FUN_05e1d0bc(&local_290);
      if ((long)local_3c0 < 0) {
        __ZdlPvm(local_3d0,local_3c0 & 0x7fffffffffffffff);
      }
    }
    iVar8 = 0;
    if ((int)puStack_368 != 0) {
      iVar8 = iVar7;
    }
    if (iVar8 == 1) {
      lVar9 = FUN_00758940(param_2 + 0x288,param_4);
      if (lVar9 == 0) {
        param_1[5] = 0;
        param_1[4] = 0;
        param_1[1] = 0;
        *param_1 = 0;
        param_1[3] = 0;
        param_1[2] = 0;
        puVar11 = (undefined8 *)__Znwm(0x270);
        puVar11[2] = 0;
        puVar11[1] = 0;
        *puVar11 = &PTR_FUN_09de0f80;
        _bzero(puVar11 + 3,0x228);
        *(undefined4 *)(puVar11 + 3) = 1;
        puVar11[0x40] = 0;
        puVar11[0x42] = 0;
        puVar11[0x41] = 0;
        *(undefined1 *)(puVar11 + 0x43) = 0;
        puVar11[0x11] = 0;
        puVar11[0x10] = 0;
        puVar11[0x13] = 0;
        puVar11[0x12] = 0;
        puVar11[0x15] = 0;
        puVar11[0x14] = 0;
        puVar11[0x17] = 0;
        puVar11[0x16] = 0;
        puVar11[0x19] = 0;
        puVar11[0x18] = 0;
        puVar11[0x1b] = 0;
        puVar11[0x1a] = 0;
        puVar11[0x1d] = 0;
        puVar11[0x1c] = 0;
        puVar11[0x1f] = 0;
        puVar11[0x1e] = 0;
        puVar11[0x21] = 0;
        puVar11[0x20] = 0;
        puVar11[0x23] = 0;
        puVar11[0x22] = 0;
        puVar11[0x25] = 0;
        puVar11[0x24] = 0;
        puVar11[0x27] = 0;
        puVar11[0x26] = 0;
        puVar11[0x29] = 0;
        puVar11[0x28] = 0;
        puVar11[0x2b] = 0;
        puVar11[0x2a] = 0;
        puVar11[0x2d] = 0;
        puVar11[0x2c] = 0;
        puVar11[0x2f] = 0;
        puVar11[0x2e] = 0;
        puVar11[0x31] = 0;
        puVar11[0x30] = 0;
        puVar11[0x33] = 0;
        puVar11[0x32] = 0;
        puVar11[0x35] = 0;
        puVar11[0x34] = 0;
        puVar11[0x37] = 0;
        puVar11[0x36] = 0;
        puVar11[0x39] = 0;
        puVar11[0x38] = 0;
        puVar11[0x3b] = 0;
        puVar11[0x3a] = 0;
        puVar11[0x3d] = 0;
        puVar11[0x3c] = 0;
        *(undefined8 *)((long)puVar11 + 0x1f1) = 0;
        *(undefined8 *)((long)puVar11 + 0x1e9) = 0;
        *(undefined2 *)(puVar11 + 0x47) = 0;
        puVar11[0x46] = 0;
        puVar11[0x45] = 0;
        puVar11[0x44] = 0;
        puVar11[0x49] = 0;
        puVar11[0x48] = 0;
        puVar11[0x4b] = 0;
        puVar11[0x4a] = 0;
        puVar11[0x4d] = 0;
        puVar11[0x4c] = 0;
        param_1[4] = puVar11 + 3;
        param_1[5] = puVar11;
        puStack_178 = &SUB_aaaaaaaaaaaaaaaa;
        local_180 = &SUB_aaaaaaaaaaaaaaaa;
        uStack_168 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_170 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_198 = &SUB_aaaaaaaaaaaaaaaa;
        local_1a0 = (long *)&SUB_aaaaaaaaaaaaaaaa;
        local_188 = &SUB_aaaaaaaaaaaaaaaa;
        local_190 = &SUB_aaaaaaaaaaaaaaaa;
        uStack_1a8 = (undefined8 ******)&SUB_aaaaaaaaaaaaaaaa;
        local_1b0 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
        if ((int)puStack_368 < 3) {
          if ((int)puStack_368 == 1) {
            pcVar16 = (char *)FUN_04e049c8();
            ppppppuVar17 = (undefined8 ******)_strlen(pcVar16);
            if ((undefined8 ******)0x7ffffffffffffff7 < ppppppuVar17) {
LAB_02fd3970:
                    /* WARNING: Subroutine does not return */
              FUN_00018d9c(&local_1b0);
            }
            if ((undefined8 ******)0x16 < ppppppuVar17) {
              uVar27 = 0x19;
              if (((ulong)ppppppuVar17 | 7) != 0x17) {
                uVar27 = ((ulong)ppppppuVar17 | 7) + 1;
              }
              pppppppuVar18 = (undefined8 *******)__Znwm(uVar27);
              goto LAB_02fd27a0;
            }
LAB_02fd2778:
            local_1a0 = (long *)CONCAT17((char)ppppppuVar17,(undefined7)local_1a0);
            pppppppuVar18 = (undefined8 *******)&local_1b0;
            if (ppppppuVar17 != (undefined8 ******)0x0) goto LAB_02fd27b4;
LAB_02fd27c4:
            *(undefined1 *)((long)pppppppuVar18 + (long)ppppppuVar17) = 0;
          }
          else {
            if ((int)puStack_368 == 2) {
              pcVar16 = (char *)FUN_04e04908();
              ppppppuVar17 = (undefined8 ******)_strlen(pcVar16);
              if ((undefined8 ******)0x7ffffffffffffff7 < ppppppuVar17) goto LAB_02fd3970;
              if (ppppppuVar17 < (undefined8 ******)0x17) goto LAB_02fd2778;
              uVar27 = 0x19;
              if (((ulong)ppppppuVar17 | 7) != 0x17) {
                uVar27 = ((ulong)ppppppuVar17 | 7) + 1;
              }
              pppppppuVar18 = (undefined8 *******)__Znwm(uVar27);
              goto LAB_02fd27a0;
            }
LAB_02fd22f0:
            iVar7 = thunk_FUN_05e1d97c(4);
            if (iVar7 != 0) {
              FUN_0488143c(&local_200);
              puVar11 = local_200;
              if (-1 < cStack_1e9) {
                puVar11 = &local_200;
              }
              if ((DAT_0a3d2361 & 1) == 0) {
                uRam000000000a3d2358._0_1_ = s_login_manager_ccauto_login_close_0889c040[8];
                uRam000000000a3d2358._1_1_ = s_login_manager_ccauto_login_close_0889c040[9];
                uRam000000000a3d2358._2_1_ = s_login_manager_ccauto_login_close_0889c040[10];
                uRam000000000a3d2358._3_1_ = s_login_manager_ccauto_login_close_0889c040[0xb];
                uRam000000000a3d2358._4_1_ = s_login_manager_ccauto_login_close_0889c040[0xc];
                uRam000000000a3d2358._5_1_ = s_login_manager_ccauto_login_close_0889c040[0xd];
                uRam000000000a3d2358._6_1_ = s_login_manager_ccauto_login_close_0889c040[0xe];
                uRam000000000a3d2358._7_1_ = s_login_manager_ccauto_login_close_0889c040[0xf];
                DAT_0a3d2350 = s_login_manager_ccauto_login_close_0889c040[0];
                DAT_0a3d2350_1._0_1_ = s_login_manager_ccauto_login_close_0889c040[1];
                DAT_0a3d2350_1._1_1_ = s_login_manager_ccauto_login_close_0889c040[2];
                DAT_0a3d2350_1._2_1_ = s_login_manager_ccauto_login_close_0889c040[3];
                DAT_0a3d2350_1._3_1_ = s_login_manager_ccauto_login_close_0889c040[4];
                DAT_0a3d2350_1._4_1_ = s_login_manager_ccauto_login_close_0889c040[5];
                DAT_0a3d2350_1._5_1_ = s_login_manager_ccauto_login_close_0889c040[6];
                DAT_0a3d2350_1._6_1_ = s_login_manager_ccauto_login_close_0889c040[7];
                DAT_0a3d2360 = 0;
                DAT_0a3d2361 = 1;
              }
              if ((DAT_0a3d3894 & 1) == 0) {
                _DAT_0a3d3878 = CONCAT44((int)DAT_0889c430,(int)DAT_084d5770);
                uRam000000000a3d3880 = CONCAT44((int)DAT_0847fe38,(int)DAT_084d8880);
                DAT_0a3d3888 = CONCAT44((int)DAT_0889c438,(int)DAT_084809c8);
                DAT_0a3d3890 = (undefined4)DAT_084a2f38;
                DAT_0a3d3894 = 1;
              }
              FUN_05e1d050(&local_290,4,puVar11,&DAT_0a3d2350,&DAT_0a3d3878,0x86,0,0);
              local_160 = (long *******)0x0;
              local_160 = (long *******)&local_158;
              if ((DAT_0a3d37f2 & 1) == 0) {
                uVar27 = 0;
                do {
                  uVar29 = *(undefined4 *)((long)&DAT_0889efbe + uVar27);
                  uVar4 = CONCAT12((char)((uint)uVar29 >> 8),(short)uVar29) & 0xff00ff;
                  uVar30 = *(undefined4 *)((long)&DAT_0889efaa + uVar27 % 0x14);
                  *(uint *)((long)&DAT_0a3d37aa + uVar27) =
                       CONCAT13((char)((uint)uVar29 >> 0x18) + 0x69U ^ (byte)((uint)uVar30 >> 0x18),
                                CONCAT12((char)((uint)uVar29 >> 0x10) + 0x69U ^
                                         (byte)((uint)uVar30 >> 0x10),
                                         CONCAT11((char)(uVar4 >> 0x10) + 0x69U ^
                                                  (byte)((uint)uVar30 >> 8),
                                                  (char)uVar4 + 0x69U ^ (byte)uVar30)));
                  uVar27 = uVar27 + 4;
                } while (uVar27 != 0x48);
                DAT_0a3d37f2 = 1;
              }
              uVar27 = (ulong)puStack_368 & 0xffffffff;
              lVar28 = 0;
              do {
                lVar26 = lVar28;
                uVar24 = (uint)uVar27;
                *(undefined1 *)((long)&local_158 + lVar26) =
                     *(undefined1 *)
                      ((long)&DAT_0a3d37aa + (ulong)(uVar24 + (int)(uVar27 / 10) * -10 + 0x23));
                uVar27 = uVar27 / 10;
                lVar28 = lVar26 + 1;
              } while (9 < uVar24);
              *(undefined1 *)((long)&local_158 + lVar26 + 1) = 0;
              if (8 < lVar26 + 8U) {
                puVar10 = (undefined1 *)((long)&local_158 + lVar26);
                puVar6 = (undefined1 *)((long)&local_158 + 1);
                do {
                  uVar3 = *puVar10;
                  *puVar10 = puVar6[-1];
                  puVar6[-1] = uVar3;
                  bVar5 = puVar6 < puVar10 + -1;
                  puVar10 = puVar10 + -1;
                  puVar6 = puVar6 + 1;
                } while (bVar5);
              }
              if ((DAT_0a3d38b6 & 1) == 0) {
                _DAT_0a3d3898 = CONCAT44((int)DAT_08482f58,(int)DAT_0852d530);
                uRam000000000a3d38a0 = CONCAT44((int)DAT_084a4f70,(int)DAT_08771580);
                DAT_0a3d38a8 = CONCAT44((int)DAT_0889c440,(int)DAT_084ca318);
                DAT_0a3d38b0 = (undefined4)DAT_085eaf20;
                DAT_0a3d38b4 = 0x5f;
                DAT_0a3d38b6 = 1;
              }
              local_100 = (undefined8 *)0x0;
              puStack_108 = (undefined8 *)0x0;
              local_110 = (undefined8 *******)&local_160;
              local_f0 = 0;
              uStack_f8 = 0;
              local_e0 = 0;
              uStack_e8 = 0;
              local_d0 = 0;
              uStack_d8 = 0;
              local_c0 = 0;
              uStack_c8 = 0;
              local_b0 = 0;
              uStack_b8 = 0;
              local_a0 = 0;
              uStack_a8 = 0;
              uStack_98 = 0;
              FUN_05e1d31c(&local_290,&DAT_0a3d3898,&local_110);
              thunk_FUN_05e1d0bc(&local_290);
              if (cStack_1e9 < '\0') {
                __ZdlPvm(local_200,CONCAT17(cStack_1e9,local_1f0) & 0x7fffffffffffffff);
              }
            }
            iVar7 = thunk_FUN_05e1d97c(4);
            if (iVar7 != 0) {
              FUN_0488143c(&local_160);
              ppppppplVar2 = local_160;
              if (-1 < cStack_149) {
                ppppppplVar2 = (long *******)&local_160;
              }
              if ((DAT_0a3d2361 & 1) == 0) {
                uRam000000000a3d2358._0_1_ = s_login_manager_ccauto_login_close_0889c040[8];
                uRam000000000a3d2358._1_1_ = s_login_manager_ccauto_login_close_0889c040[9];
                uRam000000000a3d2358._2_1_ = s_login_manager_ccauto_login_close_0889c040[10];
                uRam000000000a3d2358._3_1_ = s_login_manager_ccauto_login_close_0889c040[0xb];
                uRam000000000a3d2358._4_1_ = s_login_manager_ccauto_login_close_0889c040[0xc];
                uRam000000000a3d2358._5_1_ = s_login_manager_ccauto_login_close_0889c040[0xd];
                uRam000000000a3d2358._6_1_ = s_login_manager_ccauto_login_close_0889c040[0xe];
                uRam000000000a3d2358._7_1_ = s_login_manager_ccauto_login_close_0889c040[0xf];
                DAT_0a3d2350 = s_login_manager_ccauto_login_close_0889c040[0];
                DAT_0a3d2350_1._0_1_ = s_login_manager_ccauto_login_close_0889c040[1];
                DAT_0a3d2350_1._1_1_ = s_login_manager_ccauto_login_close_0889c040[2];
                DAT_0a3d2350_1._2_1_ = s_login_manager_ccauto_login_close_0889c040[3];
                DAT_0a3d2350_1._3_1_ = s_login_manager_ccauto_login_close_0889c040[4];
                DAT_0a3d2350_1._4_1_ = s_login_manager_ccauto_login_close_0889c040[5];
                DAT_0a3d2350_1._5_1_ = s_login_manager_ccauto_login_close_0889c040[6];
                DAT_0a3d2350_1._6_1_ = s_login_manager_ccauto_login_close_0889c040[7];
                DAT_0a3d2360 = 0;
                DAT_0a3d2361 = 1;
              }
              if ((DAT_0a3d3894 & 1) == 0) {
                _DAT_0a3d3878 = CONCAT44((int)DAT_0889c430,(int)DAT_084d5770);
                uRam000000000a3d3880 = CONCAT44((int)DAT_0847fe38,(int)DAT_084d8880);
                DAT_0a3d3888 = CONCAT44((int)DAT_0889c438,(int)DAT_084809c8);
                DAT_0a3d3890 = (undefined4)DAT_084a2f38;
                DAT_0a3d3894 = 1;
              }
              FUN_05e1d050(&local_290,4,ppppppplVar2,&DAT_0a3d2350,&DAT_0a3d3878,0x87,0,0);
              uStack_a8 = 0;
              local_b0 = 0;
              uStack_98 = 0;
              local_a0 = 0;
              uStack_c8 = 0;
              local_d0 = 0;
              uStack_b8 = 0;
              local_c0 = 0;
              uStack_e8 = 0;
              local_f0 = 0;
              uStack_d8 = 0;
              local_e0 = 0;
              puStack_108 = (undefined8 *)0x0;
              local_110 = (undefined8 *******)0x0;
              uStack_f8 = 0;
              local_100 = (undefined8 *)0x0;
              FUN_05e1d31c(&local_290,"",&local_110);
              thunk_FUN_05e1d0bc(&local_290);
              if (cStack_149 < '\0') {
                __ZdlPvm(local_160,CONCAT17(cStack_149,local_150) & 0x7fffffffffffffff);
              }
            }
            uStack_1a8 = (undefined8 ******)0x0;
            local_1b0 = (undefined8 *******)0x0;
            local_1a0 = (long *)0x0;
          }
        }
        else {
          if ((int)puStack_368 == 3) {
            pcVar16 = (char *)FUN_04e04908();
            ppppppuVar17 = (undefined8 ******)_strlen(pcVar16);
            if ((undefined8 ******)0x7ffffffffffffff7 < ppppppuVar17) goto LAB_02fd3970;
            if (ppppppuVar17 < (undefined8 ******)0x17) goto LAB_02fd2778;
            uVar27 = 0x19;
            if (((ulong)ppppppuVar17 | 7) != 0x17) {
              uVar27 = ((ulong)ppppppuVar17 | 7) + 1;
            }
            pppppppuVar18 = (undefined8 *******)__Znwm(uVar27);
LAB_02fd27a0:
            local_1a0 = (long *)(uVar27 | 0x8000000000000000);
            local_1b0 = pppppppuVar18;
            uStack_1a8 = ppppppuVar17;
LAB_02fd27b4:
            _memmove(pppppppuVar18,pcVar16,(size_t)ppppppuVar17);
            goto LAB_02fd27c4;
          }
          if ((int)puStack_368 != 4) goto LAB_02fd22f0;
          pppppppuStack_278 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
          local_280 = &SUB_aaaaaaaaaaaaaaaa;
          local_268 = (long *)&SUB_aaaaaaaaaaaaaaaa;
          local_270 = (undefined8 ******)&SUB_aaaaaaaaaaaaaaaa;
          puStack_288 = &SUB_aaaaaaaaaaaaaaaa;
          local_290 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
          FUN_04884608(&local_290,&puStack_360);
          if ((long)local_268 < 0) {
            FUN_00018d20(&local_1b0,pppppppuStack_278,local_270);
            if ((long)local_268 < 0) {
              __ZdlPvm(pppppppuStack_278,(ulong)local_268 & 0x7fffffffffffffff);
            }
          }
          else {
            uStack_1a8 = local_270;
            local_1b0 = pppppppuStack_278;
            local_1a0 = local_268;
          }
          if ((long)local_280 < 0) {
            __ZdlPvm(local_290,(ulong)local_280 & 0x7fffffffffffffff);
          }
        }
        puStack_198 = (undefined1 *)((ulong)puStack_198 & 0xffffffff00000000);
        local_180 = (undefined1 *)0x0;
        local_190 = (undefined1 *)0x0;
        local_188 = (undefined1 *)0x0;
        FUN_0002b2c0(&puStack_178);
        puStack_198 = (undefined1 *)CONCAT44(puStack_198._4_4_,(int)puStack_368);
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(&local_190,param_4)
        ;
        if ((int)puStack_368 == 4) {
          FUN_048845f4(&local_290,&puStack_360);
        }
        else {
          FUN_0002b2c0(&local_290);
        }
        FUN_0002b4f8(&puStack_178,&local_290);
        FUN_0002b440(&local_290);
        lVar28 = param_1[4];
        if (*(char *)(lVar28 + 0x60) == '\x01') {
          __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                    (lVar28 + 0x10,&local_1b0);
          *(undefined4 *)(lVar28 + 0x28) = puStack_198._0_4_;
          __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                    (lVar28 + 0x30,&local_190);
          FUN_0002b480(lVar28 + 0x48,&puStack_178);
        }
        else {
          FUN_011c8eb4(lVar28 + 0x10,&local_1b0);
          *(undefined1 *)(lVar28 + 0x60) = 1;
        }
        *(undefined4 *)param_1 = 0xfffffe0c;
        if (*(int *)((long)param_1 + 4) == 0) {
          *(undefined4 *)((long)param_1 + 4) = 0xfffffffa;
        }
        FUN_0002b440(&puStack_178);
        if ((long)local_180 < 0) {
          __ZdlPvm(local_190,(ulong)local_180 & 0x7fffffffffffffff);
        }
        if ((long)local_1a0 < 0) {
          uVar27 = (ulong)local_1a0 & 0x7fffffffffffffff;
          pppppppuVar18 = local_1b0;
          goto LAB_02fd28dc;
        }
      }
      else {
        iVar7 = thunk_FUN_05e1d97c(2);
        if (iVar7 != 0) {
          FUN_0488143c(&local_200);
          puVar11 = local_200;
          if (-1 < cStack_1e9) {
            puVar11 = &local_200;
          }
          if ((DAT_0a3d2361 & 1) == 0) {
            uRam000000000a3d2358._0_1_ = s_login_manager_ccauto_login_close_0889c040[8];
            uRam000000000a3d2358._1_1_ = s_login_manager_ccauto_login_close_0889c040[9];
            uRam000000000a3d2358._2_1_ = s_login_manager_ccauto_login_close_0889c040[10];
            uRam000000000a3d2358._3_1_ = s_login_manager_ccauto_login_close_0889c040[0xb];
            uRam000000000a3d2358._4_1_ = s_login_manager_ccauto_login_close_0889c040[0xc];
            uRam000000000a3d2358._5_1_ = s_login_manager_ccauto_login_close_0889c040[0xd];
            uRam000000000a3d2358._6_1_ = s_login_manager_ccauto_login_close_0889c040[0xe];
            uRam000000000a3d2358._7_1_ = s_login_manager_ccauto_login_close_0889c040[0xf];
            DAT_0a3d2350 = s_login_manager_ccauto_login_close_0889c040[0];
            DAT_0a3d2350_1._0_1_ = s_login_manager_ccauto_login_close_0889c040[1];
            DAT_0a3d2350_1._1_1_ = s_login_manager_ccauto_login_close_0889c040[2];
            DAT_0a3d2350_1._2_1_ = s_login_manager_ccauto_login_close_0889c040[3];
            DAT_0a3d2350_1._3_1_ = s_login_manager_ccauto_login_close_0889c040[4];
            DAT_0a3d2350_1._4_1_ = s_login_manager_ccauto_login_close_0889c040[5];
            DAT_0a3d2350_1._5_1_ = s_login_manager_ccauto_login_close_0889c040[6];
            DAT_0a3d2350_1._6_1_ = s_login_manager_ccauto_login_close_0889c040[7];
            DAT_0a3d2360 = 0;
            DAT_0a3d2361 = 1;
          }
          if ((DAT_0a3d2a23 & 1) == 0) {
            DAT_0a3d2a18 = DAT_0889c418;
            DAT_0a3d2a20 = 0x6874;
            DAT_0a3d2a22 = 0;
            DAT_0a3d2a23 = 1;
          }
          FUN_05e1d050(&local_290,2,puVar11,&DAT_0a3d2350,&DAT_0a3d2a18,0x393,0,0);
          local_160 = (long *******)*param_4;
          if (-1 < *(char *)((long)param_4 + 0x17)) {
            local_160 = param_4;
          }
          local_158._0_1_ = 0;
          FUN_02fd55b4(&local_3d0,&puStack_368);
          local_1b0 = local_3d0;
          if (-1 < (long)local_3c0) {
            local_1b0 = &local_3d0;
          }
          uStack_1a8 = (undefined8 ******)((ulong)uStack_1a8 & 0xffffffffffffff00);
          if ((DAT_0a3d2b84 & 1) == 0) {
            uVar27 = 0;
            do {
              uVar29 = *(undefined4 *)((long)&DAT_0889dce9 + uVar27);
              uVar4 = CONCAT12((char)((uint)uVar29 >> 8),(short)uVar29) & 0xff00ff;
              uVar30 = *(undefined4 *)((long)&DAT_0889dcd5 + uVar27 % 0x14);
              *(uint *)((long)&DAT_0a3d2b3b + uVar27) =
                   CONCAT13((char)((uint)uVar29 >> 0x18) + 0x8aU ^ (byte)((uint)uVar30 >> 0x18),
                            CONCAT12((char)((uint)uVar29 >> 0x10) + 0x8aU ^
                                     (byte)((uint)uVar30 >> 0x10),
                                     CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^
                                              (byte)((uint)uVar30 >> 8),
                                              (char)uVar4 + 0x8aU ^ (byte)uVar30)));
              uVar27 = uVar27 + 4;
            } while (uVar27 != 0x48);
            DAT_0a3d2b83 = 0;
            DAT_0a3d2b84 = 1;
          }
          local_110 = (undefined8 *******)&local_160;
          puStack_108 = &local_1b0;
          uStack_f8 = 0;
          local_100 = (undefined8 *)0x0;
          uStack_e8 = 0;
          local_f0 = 0;
          uStack_d8 = 0;
          local_e0 = 0;
          uStack_c8 = 0;
          local_d0 = 0;
          uStack_b8 = 0;
          local_c0 = 0;
          uStack_a8 = 0;
          local_b0 = 0;
          uStack_98 = 0;
          local_a0 = 0;
          FUN_05e1d31c(&local_290,&DAT_0a3d2b3b,&local_110);
          if ((long)local_3c0 < 0) {
            __ZdlPvm(local_3d0,local_3c0 & 0x7fffffffffffffff);
          }
          thunk_FUN_05e1d0bc(&local_290);
          if (cStack_1e9 < '\0') {
            __ZdlPvm(local_200,CONCAT17(cStack_1e9,local_1f0) & 0x7fffffffffffffff);
          }
        }
        FUN_000424e0(&local_290,param_2 + 0x288,lVar9);
        pppppppuVar18 = local_290;
        local_290 = (undefined8 *******)0x0;
        if (pppppppuVar18 != (undefined8 *******)0x0) {
          if (((char)local_280 == '\x01') && (*(char *)((long)pppppppuVar18 + 0x27) < '\0')) {
            __ZdlPvm(pppppppuVar18[2],(ulong)pppppppuVar18[4] & 0x7fffffffffffffff);
          }
          uVar27 = 0x28;
LAB_02fd28dc:
          __ZdlPvm(pppppppuVar18,uVar27);
        }
      }
      if (lVar9 == 0) goto LAB_02fd3690;
    }
  }
  else {
    uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x200000000);
    if (local_2b0 == (undefined1 *)0x0) {
      puVar10 = (undefined1 *)__Znwm(0xd8);
      FUN_050c7110();
      local_2b0 = puVar10;
    }
    puVar10 = local_2b0;
    *(uint *)(local_2b0 + 0xd0) = *(uint *)(local_2b0 + 0xd0) | 2;
    lVar9 = *(long *)(local_2b0 + 0x10);
    if (lVar9 == 0) {
      lVar9 = __Znwm(0x48);
      FUN_050c7094();
      *(long *)(puVar10 + 0x10) = lVar9;
    }
    *(uint *)(lVar9 + 0x40) = *(uint *)(lVar9 + 0x40) | 0x10;
    lVar28 = *(long *)(lVar9 + 0x28);
    if (lVar28 == 0) {
      lVar28 = __Znwm(0x20);
      FUN_04f33be0();
      *(long *)(lVar9 + 0x28) = lVar28;
      if (lVar28 == 0) goto LAB_02fd28e4;
    }
    puVar10 = puStack_378;
    pppppppuVar18 = local_380;
    if (-1 < (long)local_370) {
      puVar10 = (undefined1 *)((ulong)local_370 >> 0x38);
      pppppppuVar18 = &local_380;
    }
    *(uint *)(lVar28 + 0x18) = *(uint *)(lVar28 + 0x18) | 2;
    puVar11 = *(undefined8 **)(lVar28 + 8);
    if (puVar11 == &DAT_0a524ad0) {
      puVar11 = (undefined8 *)__Znwm(0x18);
      *puVar11 = 0;
      puVar11[1] = 0;
      puVar11[2] = 0;
      *(undefined8 **)(lVar28 + 8) = puVar11;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKcm
              (puVar11,pppppppuVar18,puVar10);
    uVar24 = (uint)puStack_378;
    if (-1 < (long)local_370) {
      uVar24 = (uint)local_370._7_1_;
    }
    *(uint *)(lVar28 + 0x18) = *(uint *)(lVar28 + 0x18) | 1;
    *(uint *)(lVar28 + 0x10) = uVar24;
  }
LAB_02fd28e4:
  local_398 = (undefined8 *******)0x0;
  local_390 = 0;
  local_388 = 0;
  FUN_02216c5c(&local_398,0);
  uVar27 = local_390;
  if (-1 < (long)local_388) {
    uVar27 = local_388 >> 0x38;
  }
  if (uVar27 != 0) {
    uStack_2a8 = (undefined1 *)((ulong)uStack_2a8 | 0x200000000);
    if (local_2b0 == (undefined1 *)0x0) {
      puVar10 = (undefined1 *)__Znwm(0xd8);
      FUN_050c7110();
      local_2b0 = puVar10;
    }
    puVar10 = local_2b0;
    *(uint *)(local_2b0 + 0xd0) = *(uint *)(local_2b0 + 0xd0) | 0x400000;
    lVar9 = *(long *)(local_2b0 + 0xa8);
    if (lVar9 == 0) {
      lVar9 = __Znwm(0x20);
      FUN_04f33be0();
      *(long *)(puVar10 + 0xa8) = lVar9;
    }
    uVar27 = local_390;
    pppppppuVar18 = local_398;
    if (-1 < (long)local_388) {
      uVar27 = local_388 >> 0x38;
      pppppppuVar18 = &local_398;
    }
    *(uint *)(lVar9 + 0x18) = *(uint *)(lVar9 + 0x18) | 2;
    puVar11 = *(undefined8 **)(lVar9 + 8);
    if (puVar11 == &DAT_0a524ad0) {
      puVar11 = (undefined8 *)__Znwm(0x18);
      *puVar11 = 0;
      puVar11[1] = 0;
      puVar11[2] = 0;
      *(undefined8 **)(lVar9 + 8) = puVar11;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKcm
              (puVar11,pppppppuVar18,uVar27);
    uVar27 = local_390;
    if (-1 < (long)local_388) {
      uVar27 = local_388 >> 0x38;
    }
    *(uint *)(lVar9 + 0x18) = *(uint *)(lVar9 + 0x18) | 1;
    *(int *)(lVar9 + 0x10) = (int)uVar27;
  }
  uStack_3b8 = 0;
  local_3c0 = 0;
  local_3a8 = (long *)0x0;
  local_3b0 = (long *)0x0;
  uStack_3c8 = 0;
  local_3d0 = (undefined8 *******)0x0;
  plVar13 = (long *)__Znwm(0x270);
  plVar13[2] = 0;
  plVar13[1] = 0;
  *plVar13 = (long)&PTR_FUN_09de0f80;
  _bzero(plVar13 + 3,0x228);
  *(undefined4 *)(plVar13 + 3) = 1;
  plVar13[0x40] = 0;
  plVar13[0x42] = 0;
  plVar13[0x41] = 0;
  *(undefined1 *)(plVar13 + 0x43) = 0;
  plVar13[0x11] = 0;
  plVar13[0x10] = 0;
  plVar13[0x13] = 0;
  plVar13[0x12] = 0;
  plVar13[0x15] = 0;
  plVar13[0x14] = 0;
  plVar13[0x17] = 0;
  plVar13[0x16] = 0;
  plVar13[0x19] = 0;
  plVar13[0x18] = 0;
  plVar13[0x1b] = 0;
  plVar13[0x1a] = 0;
  plVar13[0x1d] = 0;
  plVar13[0x1c] = 0;
  plVar13[0x1f] = 0;
  plVar13[0x1e] = 0;
  plVar13[0x21] = 0;
  plVar13[0x20] = 0;
  plVar13[0x23] = 0;
  plVar13[0x22] = 0;
  plVar13[0x25] = 0;
  plVar13[0x24] = 0;
  plVar13[0x27] = 0;
  plVar13[0x26] = 0;
  plVar13[0x29] = 0;
  plVar13[0x28] = 0;
  plVar13[0x2b] = 0;
  plVar13[0x2a] = 0;
  plVar13[0x2d] = 0;
  plVar13[0x2c] = 0;
  plVar13[0x2f] = 0;
  plVar13[0x2e] = 0;
  plVar13[0x31] = 0;
  plVar13[0x30] = 0;
  plVar13[0x33] = 0;
  plVar13[0x32] = 0;
  plVar13[0x35] = 0;
  plVar13[0x34] = 0;
  plVar13[0x37] = 0;
  plVar13[0x36] = 0;
  plVar13[0x39] = 0;
  plVar13[0x38] = 0;
  plVar13[0x3b] = 0;
  plVar13[0x3a] = 0;
  plVar13[0x3d] = 0;
  plVar13[0x3c] = 0;
  *(undefined8 *)((long)plVar13 + 0x1f1) = 0;
  *(undefined8 *)((long)plVar13 + 0x1e9) = 0;
  *(undefined2 *)(plVar13 + 0x47) = 0;
  plVar13[0x46] = 0;
  plVar13[0x45] = 0;
  plVar13[0x44] = 0;
  plVar13[0x49] = 0;
  plVar13[0x48] = 0;
  plVar13[0x4b] = 0;
  plVar13[0x4a] = 0;
  plVar13[0x4d] = 0;
  plVar13[0x4c] = 0;
  puStack_3e8 = &SUB_aaaaaaaaaaaaaaaa;
  local_3f0 = &SUB_aaaaaaaaaaaaaaaa;
  local_3d8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_3e0 = (undefined8 ******)&SUB_aaaaaaaaaaaaaaaa;
  puStack_3f8 = &SUB_aaaaaaaaaaaaaaaa;
  local_400 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
  local_3b0 = plVar13 + 3;
  local_3a8 = plVar13;
  uVar15 = FUN_0466a318(param_3);
  pppppppuVar18 = DAT_0875d510;
  local_290 = DAT_0875d510;
  local_270._1_7_ = (uint7)((ulong)local_270 >> 8) & 0xffffff;
  local_280 = (undefined1 *)0x0;
  pppppppuStack_278 = (undefined8 *******)0x0;
  puStack_288 = (undefined1 *)0x0;
  local_270 = (undefined8 ******)((ulong)local_270._1_7_ << 8);
  FUN_02fd585c(&local_400,uVar15,&local_2c0,&local_2d8,&local_290);
  if ((long)pppppppuStack_278 < 0) {
    __ZdlPvm(puStack_288,(ulong)pppppppuStack_278 & 0x7fffffffffffffff);
  }
  *(int *)(local_3b0 + 1) = local_400._4_4_;
  uVar15 = thunk_FUN_05e1d97c(2);
  if ((int)uVar15 == 0) {
LAB_02fd2e8c:
  }
  else {
    FUN_0488143c(local_418);
    pppppppuVar1 = local_418[0];
    if (-1 < cStack_401) {
      pppppppuVar1 = local_418;
    }
    if ((DAT_0a3d2361 & 1) == 0) {
      uRam000000000a3d2358._0_1_ = s_login_manager_ccauto_login_close_0889c040[8];
      uRam000000000a3d2358._1_1_ = s_login_manager_ccauto_login_close_0889c040[9];
      uRam000000000a3d2358._2_1_ = s_login_manager_ccauto_login_close_0889c040[10];
      uRam000000000a3d2358._3_1_ = s_login_manager_ccauto_login_close_0889c040[0xb];
      uRam000000000a3d2358._4_1_ = s_login_manager_ccauto_login_close_0889c040[0xc];
      uRam000000000a3d2358._5_1_ = s_login_manager_ccauto_login_close_0889c040[0xd];
      uRam000000000a3d2358._6_1_ = s_login_manager_ccauto_login_close_0889c040[0xe];
      uRam000000000a3d2358._7_1_ = s_login_manager_ccauto_login_close_0889c040[0xf];
      DAT_0a3d2350 = s_login_manager_ccauto_login_close_0889c040[0];
      DAT_0a3d2350_1._0_1_ = s_login_manager_ccauto_login_close_0889c040[1];
      DAT_0a3d2350_1._1_1_ = s_login_manager_ccauto_login_close_0889c040[2];
      DAT_0a3d2350_1._2_1_ = s_login_manager_ccauto_login_close_0889c040[3];
      DAT_0a3d2350_1._3_1_ = s_login_manager_ccauto_login_close_0889c040[4];
      DAT_0a3d2350_1._4_1_ = s_login_manager_ccauto_login_close_0889c040[5];
      DAT_0a3d2350_1._5_1_ = s_login_manager_ccauto_login_close_0889c040[6];
      DAT_0a3d2350_1._6_1_ = s_login_manager_ccauto_login_close_0889c040[7];
      DAT_0a3d2360 = 0;
      DAT_0a3d2361 = 1;
    }
    if ((DAT_0a3d2a23 & 1) == 0) {
      DAT_0a3d2a18 = DAT_0889c418;
      DAT_0a3d2a20 = 0x6874;
      DAT_0a3d2a22 = 0;
      DAT_0a3d2a23 = 1;
    }
    FUN_05e1d050(&local_290,2,pppppppuVar1,&DAT_0a3d2350,&DAT_0a3d2a18,0x3af,0,0);
    local_160 = (long *******)*param_4;
    if (-1 < *(char *)((long)param_4 + 0x17)) {
      local_160 = param_4;
    }
    local_158._0_1_ = 0;
    local_1b0 = (undefined8 *******)0x0;
    if ((DAT_0a3d37f2 & 1) == 0) {
      uVar27 = 0;
      do {
        uVar29 = *(undefined4 *)((long)&DAT_0889efbe + uVar27);
        uVar4 = CONCAT12((char)((uint)uVar29 >> 8),(short)uVar29) & 0xff00ff;
        uVar30 = *(undefined4 *)((long)&DAT_0889efaa + uVar27 % 0x14);
        *(uint *)((long)&DAT_0a3d37aa + uVar27) =
             CONCAT13((char)((uint)uVar29 >> 0x18) + 0x69U ^ (byte)((uint)uVar30 >> 0x18),
                      CONCAT12((char)((uint)uVar29 >> 0x10) + 0x69U ^ (byte)((uint)uVar30 >> 0x10),
                               CONCAT11((char)(uVar4 >> 0x10) + 0x69U ^ (byte)((uint)uVar30 >> 8),
                                        (char)uVar4 + 0x69U ^ (byte)uVar30)));
        uVar27 = uVar27 + 4;
      } while (uVar27 != 0x48);
      DAT_0a3d37f2 = 1;
    }
    lVar9 = 8;
    iVar7 = (int)local_400;
    do {
      lVar28 = lVar9;
      *(undefined1 *)((long)&local_1b0 + lVar28) =
           *(undefined1 *)((long)&DAT_0a3d37aa + (long)(iVar7 % 10 + 0x23));
      lVar9 = lVar28 + 1;
      uVar24 = iVar7 + 9;
      iVar7 = iVar7 / 10;
    } while (0x12 < uVar24);
    if ((int)local_400 < 0) {
      *(undefined1 *)((long)&local_1b0 + lVar28 + 1) = 0x2d;
      lVar9 = lVar28 + 2;
    }
    *(undefined1 *)((long)&local_1b0 + lVar9) = 0;
    if (9 < lVar9) {
      puVar10 = &uStack_1b1 + lVar9;
      puVar6 = (undefined1 *)((long)&uStack_1a8 + 1);
      do {
        uVar3 = *puVar10;
        *puVar10 = puVar6[-1];
        puVar6[-1] = uVar3;
        bVar5 = puVar6 < puVar10 + -1;
        puVar10 = puVar10 + -1;
        puVar6 = puVar6 + 1;
      } while (bVar5);
    }
    local_1b0 = (undefined8 *******)&uStack_1a8;
    local_200 = (undefined8 *)0x0;
    lVar9 = 8;
    iVar7 = local_400._4_4_;
    do {
      lVar28 = lVar9;
      *(undefined1 *)((long)&local_200 + lVar28) =
           *(undefined1 *)((long)&DAT_0a3d37aa + (long)(iVar7 % 10 + 0x23));
      lVar9 = lVar28 + 1;
      uVar24 = iVar7 + 9;
      iVar7 = iVar7 / 10;
    } while (0x12 < uVar24);
    if ((long)local_400 < 0) {
      *(undefined1 *)((long)&local_200 + lVar28 + 1) = 0x2d;
      lVar9 = lVar28 + 2;
    }
    *(undefined1 *)((long)&local_200 + lVar9) = 0;
    if (9 < lVar9) {
      puVar10 = &uStack_201 + lVar9;
      puVar6 = (undefined1 *)((long)&local_1f8 + 1);
      do {
        uVar3 = *puVar10;
        *puVar10 = puVar6[-1];
        puVar6[-1] = uVar3;
        bVar5 = puVar6 < puVar10 + -1;
        puVar10 = puVar10 + -1;
        puVar6 = puVar6 + 1;
      } while (bVar5);
    }
    if ((DAT_0a3d2bbc & 1) == 0) {
      _DAT_0a3d2b88 = CONCAT44((int)DAT_0889c450,(int)DAT_0889c448);
      uRam000000000a3d2b90 = CONCAT44((int)ram0x087922c0,(int)DAT_084e4b08);
      _DAT_0a3d2b98 = CONCAT44((int)DAT_084d86b0,(int)DAT_084d4aa0);
      uRam000000000a3d2ba0 = CONCAT44((int)DAT_084d77a0,(int)DAT_084e4760);
      _DAT_0a3d2ba8 = CONCAT44((int)DAT_084f5f38,(int)DAT_085028a0);
      uRam000000000a3d2bb0 = CONCAT44((int)DAT_08487498,(int)DAT_084d77a0);
      DAT_0a3d2bb8 = (undefined4)DAT_084fbc10;
      DAT_0a3d2bbc = 1;
    }
    local_110 = (undefined8 *******)&local_160;
    puStack_108 = &local_1b0;
    local_100 = &local_200;
    local_f0 = 0;
    uStack_f8 = 0;
    local_e0 = 0;
    uStack_e8 = 0;
    local_d0 = 0;
    uStack_d8 = 0;
    local_c0 = 0;
    uStack_c8 = 0;
    local_b0 = 0;
    uStack_b8 = 0;
    local_a0 = 0;
    uStack_a8 = 0;
    uStack_98 = 0;
    local_200 = &local_1f8;
    FUN_05e1d31c(&local_290,&DAT_0a3d2b88,&local_110);
    uVar15 = thunk_FUN_05e1d0bc(&local_290);
    if (-1 < cStack_401) goto LAB_02fd2e8c;
    uVar15 = __ZdlPvm(local_418[0],CONCAT17(cStack_401,local_408) & 0x7fffffffffffffff);
  }
  if ((int)local_400 == 0) {
    pppppuVar23 = local_3e0[2];
    if (pppppuVar23 == (undefined8 *****)0x0) {
      pppppuVar23 = *(undefined8 ******)(DAT_0a520ca0 + 0x10);
    }
    ppppuVar19 = pppppuVar23[0x12];
    plVar13 = (long *)FUN_0466a318(param_3);
    (**(code **)(*plVar13 + 0x90))(plVar13,((ulong)ppppuVar19 & 1) == 0);
    plVar13 = (long *)FUN_0466a318(param_3);
    pppppuVar23 = local_3e0[4];
    if (pppppuVar23 == (undefined8 *****)0x0) {
      pppppuVar23 = *(undefined8 ******)(DAT_0a520ca0 + 0x20);
    }
    uVar15 = (**(code **)(*plVar13 + 0x88))(plVar13,*(undefined4 *)(pppppuVar23 + 6));
  }
  if (local_400._4_4_ == -0x12d) {
    pppppuVar23 = local_3e0[4];
    if (pppppuVar23 == (undefined8 *****)0x0) {
      ppppuVar19 = *(undefined8 *****)(*(long *)(DAT_0a520ca0 + 0x20) + 0x18);
      if (ppppuVar19 != (undefined8 ****)0x0) goto LAB_02fd2f44;
LAB_02fd3800:
      ppppuVar19 = *(undefined8 *****)(DAT_0a520c78 + 0x18);
      if (pppppuVar23 != (undefined8 *****)0x0) goto LAB_02fd2f4c;
LAB_02fd3818:
      ppppuVar20 = *(undefined8 *****)(*(long *)(DAT_0a520ca0 + 0x20) + 0x10);
      if (ppppuVar20 != (undefined8 ****)0x0) goto LAB_02fd2f54;
LAB_02fd3830:
      ppppuVar20 = *(undefined8 *****)(DAT_0a520c78 + 0x10);
      if (pppppuVar23 != (undefined8 *****)0x0) goto LAB_02fd2f58;
LAB_02fd3844:
      ppppuVar21 = *(undefined8 *****)(*(long *)(DAT_0a520ca0 + 0x20) + 8);
    }
    else {
      ppppuVar19 = pppppuVar23[3];
      if (ppppuVar19 == (undefined8 ****)0x0) goto LAB_02fd3800;
LAB_02fd2f44:
      if (pppppuVar23 == (undefined8 *****)0x0) goto LAB_02fd3818;
LAB_02fd2f4c:
      ppppuVar20 = pppppuVar23[2];
      if (ppppuVar20 == (undefined8 ****)0x0) goto LAB_02fd3830;
LAB_02fd2f54:
      if (pppppuVar23 == (undefined8 *****)0x0) goto LAB_02fd3844;
LAB_02fd2f58:
      ppppuVar21 = pppppuVar23[1];
    }
    if (ppppuVar21 == (undefined8 ****)0x0) {
      ppppuVar21 = *(undefined8 *****)(DAT_0a520c78 + 8);
    }
    FUN_02fd60f4(uVar15,param_3,1,ppppuVar19,ppppuVar20,ppppuVar21);
    uVar15 = FUN_0466a318(param_3);
    local_110 = pppppppuVar18;
    local_f0._1_7_ = (uint7)((ulong)local_f0 >> 8) & 0xffffff;
    local_100 = (undefined8 *)0x0;
    uStack_f8 = 0;
    puStack_108 = (undefined8 *)0x0;
    local_f0 = (ulong)local_f0._1_7_ << 8;
    FUN_02fd585c(&local_290,uVar15,&local_2c0,&local_2d8,&local_110);
    local_400 = local_290;
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              ((ulong)&local_400 | 8,&puStack_288);
    plVar13 = local_3d8;
    if (local_268 != (long *)0x0) {
      local_268[1] = local_268[1] + 1;
    }
    local_3e0 = local_270;
    local_3d8 = local_268;
    plVar14 = local_268;
    if (plVar13 != (long *)0x0) {
      LOAcquire();
      lVar9 = plVar13[1];
      plVar13[1] = lVar9 + -1;
      LORelease();
      if (lVar9 == 0) {
        (**(code **)(*plVar13 + 0x10))(plVar13);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
        plVar14 = local_268;
      }
    }
    local_268 = plVar14;
    if (plVar14 != (long *)0x0) {
      LOAcquire();
      lVar9 = *(long *)((long)plVar14 + 8U);
      *(long *)((long)plVar14 + 8U) = lVar9 + -1;
      LORelease();
      if (lVar9 == 0) {
        (**(code **)(*plVar14 + 0x10))(plVar14);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar14);
      }
    }
    if ((long)pppppppuStack_278 < 0) {
      __ZdlPvm(puStack_288,(ulong)pppppppuStack_278 & 0x7fffffffffffffff);
    }
    iVar7 = thunk_FUN_05e1d97c(4);
    if (iVar7 != 0) {
      FUN_0488143c(&local_200);
      puVar11 = local_200;
      if (-1 < cStack_1e9) {
        puVar11 = &local_200;
      }
      if ((DAT_0a3d2361 & 1) == 0) {
        uRam000000000a3d2358._0_1_ = s_login_manager_ccauto_login_close_0889c040[8];
        uRam000000000a3d2358._1_1_ = s_login_manager_ccauto_login_close_0889c040[9];
        uRam000000000a3d2358._2_1_ = s_login_manager_ccauto_login_close_0889c040[10];
        uRam000000000a3d2358._3_1_ = s_login_manager_ccauto_login_close_0889c040[0xb];
        uRam000000000a3d2358._4_1_ = s_login_manager_ccauto_login_close_0889c040[0xc];
        uRam000000000a3d2358._5_1_ = s_login_manager_ccauto_login_close_0889c040[0xd];
        uRam000000000a3d2358._6_1_ = s_login_manager_ccauto_login_close_0889c040[0xe];
        uRam000000000a3d2358._7_1_ = s_login_manager_ccauto_login_close_0889c040[0xf];
        DAT_0a3d2350 = s_login_manager_ccauto_login_close_0889c040[0];
        DAT_0a3d2350_1._0_1_ = s_login_manager_ccauto_login_close_0889c040[1];
        DAT_0a3d2350_1._1_1_ = s_login_manager_ccauto_login_close_0889c040[2];
        DAT_0a3d2350_1._2_1_ = s_login_manager_ccauto_login_close_0889c040[3];
        DAT_0a3d2350_1._3_1_ = s_login_manager_ccauto_login_close_0889c040[4];
        DAT_0a3d2350_1._4_1_ = s_login_manager_ccauto_login_close_0889c040[5];
        DAT_0a3d2350_1._5_1_ = s_login_manager_ccauto_login_close_0889c040[6];
        DAT_0a3d2350_1._6_1_ = s_login_manager_ccauto_login_close_0889c040[7];
        DAT_0a3d2360 = 0;
        DAT_0a3d2361 = 1;
      }
      if ((DAT_0a3d2a23 & 1) == 0) {
        DAT_0a3d2a18 = DAT_0889c418;
        DAT_0a3d2a20 = 0x6874;
        DAT_0a3d2a22 = 0;
        DAT_0a3d2a23 = 1;
      }
      FUN_05e1d050(&local_290,4,puVar11,&DAT_0a3d2350,&DAT_0a3d2a18,0x3bd,0,0);
      local_160 = (long *******)0x0;
      if ((DAT_0a3d37f2 & 1) == 0) {
        uVar27 = 0;
        do {
          uVar29 = *(undefined4 *)((long)&DAT_0889efbe + uVar27);
          uVar4 = CONCAT12((char)((uint)uVar29 >> 8),(short)uVar29) & 0xff00ff;
          uVar30 = *(undefined4 *)((long)&DAT_0889efaa + uVar27 % 0x14);
          *(uint *)((long)&DAT_0a3d37aa + uVar27) =
               CONCAT13((char)((uint)uVar29 >> 0x18) + 0x69U ^ (byte)((uint)uVar30 >> 0x18),
                        CONCAT12((char)((uint)uVar29 >> 0x10) + 0x69U ^ (byte)((uint)uVar30 >> 0x10)
                                 ,CONCAT11((char)(uVar4 >> 0x10) + 0x69U ^ (byte)((uint)uVar30 >> 8)
                                           ,(char)uVar4 + 0x69U ^ (byte)uVar30)));
          uVar27 = uVar27 + 4;
        } while (uVar27 != 0x48);
        DAT_0a3d37f2 = 1;
      }
      lVar9 = 8;
      iVar7 = (int)local_400;
      do {
        lVar28 = lVar9;
        *(undefined1 *)((long)&local_160 + lVar28) =
             *(undefined1 *)((long)&DAT_0a3d37aa + (long)(iVar7 % 10 + 0x23));
        lVar9 = lVar28 + 1;
        uVar24 = iVar7 + 9;
        iVar7 = iVar7 / 10;
      } while (0x12 < uVar24);
      if ((int)local_400 < 0) {
        *(undefined1 *)((long)&local_160 + lVar28 + 1) = 0x2d;
        lVar9 = lVar28 + 2;
      }
      *(undefined1 *)((long)&local_160 + lVar9) = 0;
      if (9 < lVar9) {
        puVar10 = (undefined1 *)((long)&uStack_168 + lVar9 + 7);
        puVar6 = (undefined1 *)((long)&local_158 + 1);
        do {
          uVar3 = *puVar10;
          *puVar10 = puVar6[-1];
          puVar6[-1] = uVar3;
          bVar5 = puVar6 < puVar10 + -1;
          puVar10 = puVar10 + -1;
          puVar6 = puVar6 + 1;
        } while (bVar5);
      }
      local_160 = (long *******)&local_158;
      local_1b0 = (undefined8 *******)0x0;
      lVar9 = 8;
      iVar7 = local_400._4_4_;
      do {
        lVar28 = lVar9;
        *(undefined1 *)((long)&local_1b0 + lVar28) =
             *(undefined1 *)((long)&DAT_0a3d37aa + (long)(iVar7 % 10 + 0x23));
        lVar9 = lVar28 + 1;
        uVar24 = iVar7 + 9;
        iVar7 = iVar7 / 10;
      } while (0x12 < uVar24);
      if ((long)local_400 < 0) {
        *(undefined1 *)((long)&local_1b0 + lVar28 + 1) = 0x2d;
        lVar9 = lVar28 + 2;
      }
      *(undefined1 *)((long)&local_1b0 + lVar9) = 0;
      if (9 < lVar9) {
        puVar10 = &uStack_1b1 + lVar9;
        puVar6 = (undefined1 *)((long)&uStack_1a8 + 1);
        do {
          uVar3 = *puVar10;
          *puVar10 = puVar6[-1];
          puVar6[-1] = uVar3;
          bVar5 = puVar6 < puVar10 + -1;
          puVar10 = puVar10 + -1;
          puVar6 = puVar6 + 1;
        } while (bVar5);
      }
      if ((DAT_0a3d2bfb & 1) == 0) {
        uVar27 = 0;
        do {
          uVar29 = *(undefined4 *)((long)&DAT_0889dd8e + uVar27);
          uVar4 = CONCAT12((char)((uint)uVar29 >> 8),(short)uVar29) & 0xff00ff;
          uVar30 = *(undefined4 *)((long)&DAT_0889dd7a + uVar27 % 0x14);
          *(uint *)((long)&DAT_0a3d2bbd + uVar27) =
               CONCAT13((char)((uint)uVar29 >> 0x18) + 0x8aU ^ (byte)((uint)uVar30 >> 0x18),
                        CONCAT12((char)((uint)uVar29 >> 0x10) + 0x8aU ^ (byte)((uint)uVar30 >> 0x10)
                                 ,CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^ (byte)((uint)uVar30 >> 8)
                                           ,(char)uVar4 + 0x8aU ^ (byte)uVar30)));
          uVar27 = uVar27 + 4;
        } while (uVar27 != 0x3c);
        DAT_0a3d2bf9 = 0x5f;
        DAT_0a3d2bfb = 1;
      }
      local_110 = (undefined8 *******)&local_160;
      puStack_108 = &local_1b0;
      uStack_f8 = 0;
      local_100 = (undefined8 *)0x0;
      uStack_e8 = 0;
      local_f0 = 0;
      uStack_d8 = 0;
      local_e0 = 0;
      uStack_c8 = 0;
      local_d0 = 0;
      uStack_b8 = 0;
      local_c0 = 0;
      uStack_a8 = 0;
      local_b0 = 0;
      uStack_98 = 0;
      local_a0 = 0;
      local_1b0 = (undefined8 *******)&uStack_1a8;
      FUN_05e1d31c(&local_290,&DAT_0a3d2bbd,&local_110);
      thunk_FUN_05e1d0bc(&local_290);
      if (cStack_1e9 < '\0') {
        __ZdlPvm(local_200,CONCAT17(cStack_1e9,local_1f0) & 0x7fffffffffffffff);
      }
    }
  }
  if ((local_400._4_4_ == -0x131) && (iVar7 = FUN_0461b060(), iVar7 != 0)) {
    uVar15 = FUN_0466a318(param_3);
    local_110 = pppppppuVar18;
    local_f0._1_7_ = (uint7)((ulong)local_f0 >> 8) & 0xffffff;
    local_100 = (undefined8 *)0x0;
    uStack_f8 = 0;
    puStack_108 = (undefined8 *)0x0;
    local_f0 = (ulong)local_f0._1_7_ << 8;
    FUN_02fd585c(&local_290,uVar15,&local_2c0,&local_2d8,&local_110);
    local_400 = local_290;
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              ((ulong)&local_400 | 8,&puStack_288);
    plVar13 = local_3d8;
    if (local_268 != (long *)0x0) {
      local_268[1] = local_268[1] + 1;
    }
    local_3e0 = local_270;
    local_3d8 = local_268;
    if (plVar13 != (long *)0x0) {
      LOAcquire();
      lVar9 = plVar13[1];
      plVar13[1] = lVar9 + -1;
      LORelease();
      if (lVar9 == 0) {
        (**(code **)(*plVar13 + 0x10))(plVar13);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
      }
    }
    plVar13 = local_268;
    if (local_268 != (long *)0x0) {
      LOAcquire();
      lVar9 = local_268[1];
      local_268[1] = lVar9 + -1;
      LORelease();
      if (lVar9 == 0) {
        (**(code **)(*local_268 + 0x10))(local_268);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
      }
    }
    if ((long)pppppppuStack_278 < 0) {
      __ZdlPvm(puStack_288,(ulong)pppppppuStack_278 & 0x7fffffffffffffff);
    }
    iVar7 = thunk_FUN_05e1d97c(4);
    if (iVar7 != 0) {
      FUN_0488143c(&local_160);
      ppppppplVar2 = local_160;
      if (-1 < cStack_149) {
        ppppppplVar2 = (long *******)&local_160;
      }
      if ((DAT_0a3d2361 & 1) == 0) {
        uRam000000000a3d2358._0_1_ = s_login_manager_ccauto_login_close_0889c040[8];
        uRam000000000a3d2358._1_1_ = s_login_manager_ccauto_login_close_0889c040[9];
        uRam000000000a3d2358._2_1_ = s_login_manager_ccauto_login_close_0889c040[10];
        uRam000000000a3d2358._3_1_ = s_login_manager_ccauto_login_close_0889c040[0xb];
        uRam000000000a3d2358._4_1_ = s_login_manager_ccauto_login_close_0889c040[0xc];
        uRam000000000a3d2358._5_1_ = s_login_manager_ccauto_login_close_0889c040[0xd];
        uRam000000000a3d2358._6_1_ = s_login_manager_ccauto_login_close_0889c040[0xe];
        uRam000000000a3d2358._7_1_ = s_login_manager_ccauto_login_close_0889c040[0xf];
        DAT_0a3d2350 = s_login_manager_ccauto_login_close_0889c040[0];
        DAT_0a3d2350_1._0_1_ = s_login_manager_ccauto_login_close_0889c040[1];
        DAT_0a3d2350_1._1_1_ = s_login_manager_ccauto_login_close_0889c040[2];
        DAT_0a3d2350_1._2_1_ = s_login_manager_ccauto_login_close_0889c040[3];
        DAT_0a3d2350_1._3_1_ = s_login_manager_ccauto_login_close_0889c040[4];
        DAT_0a3d2350_1._4_1_ = s_login_manager_ccauto_login_close_0889c040[5];
        DAT_0a3d2350_1._5_1_ = s_login_manager_ccauto_login_close_0889c040[6];
        DAT_0a3d2350_1._6_1_ = s_login_manager_ccauto_login_close_0889c040[7];
        DAT_0a3d2360 = 0;
        DAT_0a3d2361 = 1;
      }
      if ((DAT_0a3d2a23 & 1) == 0) {
        DAT_0a3d2a18 = DAT_0889c418;
        DAT_0a3d2a20 = 0x6874;
        DAT_0a3d2a22 = 0;
        DAT_0a3d2a23 = 1;
      }
      FUN_05e1d050(&local_290,4,ppppppplVar2,&DAT_0a3d2350,&DAT_0a3d2a18,0x3c2,0,0);
      if ((DAT_0a3d2c24 & 1) == 0) {
        _DAT_0a3d2bfc = CONCAT44((int)DAT_0889c450,(int)DAT_0889c448);
        uRam000000000a3d2c04 = CONCAT44((int)DAT_085d4ef0,(int)DAT_084e4b08);
        _DAT_0a3d2c0c = CONCAT44((int)DAT_0889c340,(int)DAT_0889c338);
        uRam000000000a3d2c14 = CONCAT44((int)DAT_085a4d80,(int)DAT_084d8970);
        DAT_0a3d2c1c = CONCAT44((int)DAT_084e4848,(int)DAT_085b5838);
        DAT_0a3d2c24 = 1;
      }
      uStack_a8 = 0;
      local_b0 = 0;
      uStack_98 = 0;
      local_a0 = 0;
      uStack_c8 = 0;
      local_d0 = 0;
      uStack_b8 = 0;
      local_c0 = 0;
      uStack_e8 = 0;
      local_f0 = 0;
      uStack_d8 = 0;
      local_e0 = 0;
      puStack_108 = (undefined8 *)0x0;
      local_110 = (undefined8 *******)0x0;
      uStack_f8 = 0;
      local_100 = (undefined8 *)0x0;
      FUN_05e1d31c(&local_290,&DAT_0a3d2bfc,&local_110);
      thunk_FUN_05e1d0bc(&local_290);
      if (cStack_149 < '\0') {
        __ZdlPvm(local_160,CONCAT17(cStack_149,local_150) & 0x7fffffffffffffff);
      }
    }
    FUN_0461b728();
  }
  plVar13 = (long *)FUN_04669774();
  plVar13 = (long *)(**(code **)(*plVar13 + 0x18))();
  (**(code **)(*plVar13 + 0xd8))(plVar13,0,(int)local_400 == 0 && local_400._4_4_ == 0);
  FUN_02fd7104(param_1,param_2,&local_400,param_4,uVar12);
  plVar13 = local_3d8;
  if (local_3d8 != (long *)0x0) {
    LOAcquire();
    lVar9 = local_3d8[1];
    local_3d8[1] = lVar9 + -1;
    LORelease();
    if (lVar9 == 0) {
      (**(code **)(*local_3d8 + 0x10))(local_3d8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
    }
  }
  plVar13 = local_3a8;
  if ((long)puStack_3e8 < 0) {
    __ZdlPvm(puStack_3f8,(ulong)puStack_3e8 & 0x7fffffffffffffff);
    plVar13 = local_3a8;
  }
  local_3a8 = plVar13;
  if (plVar13 != (long *)0x0) {
    LOAcquire();
    lVar9 = *(long *)((long)plVar13 + 8U);
    *(long *)((long)plVar13 + 8U) = lVar9 + -1;
    LORelease();
    if (lVar9 == 0) {
      (**(code **)(*plVar13 + 0x10))(plVar13);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
    }
  }
  if ((long)uStack_3b8 < 0) {
    __ZdlPvm(uStack_3c8,uStack_3b8 & 0x7fffffffffffffff);
  }
  if ((long)local_388 < 0) {
    __ZdlPvm(local_398,local_388 & 0x7fffffffffffffff);
  }
LAB_02fd3690:
  FUN_0002b440(&puStack_360);
  if ((long)local_370 < 0) {
    __ZdlPvm(local_380,(ulong)local_370 & 0x7fffffffffffffff);
  }
  if ((long)local_328 < 0) {
    __ZdlPvm(local_338,(ulong)local_328 & 0x7fffffffffffffff);
  }
  if ((long)local_310 < 0) {
    __ZdlPvm(local_320,(ulong)local_310 & 0x7fffffffffffffff);
  }
  if ((long)local_2f8 < 0) {
    __ZdlPvm(local_308,local_2f8 & 0x7fffffffffffffff);
  }
  if ((long)local_2e0 < 0) {
    __ZdlPvm(local_2f0,local_2e0 & 0x7fffffffffffffff);
  }
  if ((long)local_2c8 < 0) {
    __ZdlPvm(local_2d8,(ulong)local_2c8 & 0x7fffffffffffffff);
  }
  FUN_050d3114(&local_2c0);
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_88) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


