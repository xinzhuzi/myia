// Ghidra inferred pseudocode; requested=0x2fea968
// entry=02fea968 end=02feb3cf

/* WARNING: Removing unreachable block (ram,0x02feb170) */
/* WARNING: Removing unreachable block (ram,0x02feae48) */
/* WARNING: Removing unreachable block (ram,0x02feb1b8) */
/* WARNING: Removing unreachable block (ram,0x02feb298) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_02fea968(long param_1)

{
  undefined1 *puVar1;
  undefined1 *puVar2;
  ulong uVar3;
  undefined4 uVar4;
  int iVar5;
  long *plVar6;
  undefined8 uVar7;
  long *plVar8;
  undefined8 *puVar9;
  undefined8 *puVar10;
  long lVar11;
  long lVar12;
  long *plVar13;
  long *local_3b0;
  undefined8 uStack_3a8;
  undefined8 local_3a0;
  ulong local_398;
  long *local_390;
  long *plStack_388;
  undefined8 local_380;
  ulong local_378;
  long local_370;
  long lStack_368;
  long *local_360;
  undefined8 uStack_358;
  undefined8 local_350;
  ulong uStack_348;
  undefined8 *local_338;
  undefined1 *local_330;
  undefined1 *local_328;
  long local_320;
  undefined1 *local_318;
  long *local_310;
  char local_2f8;
  long *local_2f0;
  undefined1 *puStack_2e8;
  undefined1 *local_2e0;
  undefined1 *puStack_2d8;
  long *local_2d0;
  long *local_2c8;
  undefined4 local_2c0;
  undefined8 local_2bc;
  undefined4 local_2b4;
  long *local_2b0;
  undefined1 *puStack_2a8;
  undefined1 *local_2a0;
  undefined1 *puStack_298;
  long *local_290;
  long *plStack_288;
  undefined8 uStack_280;
  undefined8 uStack_278;
  undefined8 local_270;
  undefined8 uStack_268;
  undefined8 uStack_260;
  undefined8 uStack_258;
  undefined8 local_250;
  undefined8 uStack_248;
  undefined8 uStack_240;
  undefined8 uStack_238;
  undefined8 local_230;
  undefined8 uStack_228;
  undefined8 uStack_220;
  undefined8 uStack_218;
  undefined8 local_210;
  undefined8 uStack_208;
  undefined8 uStack_200;
  undefined8 uStack_1f8;
  undefined8 local_1f0;
  undefined8 uStack_1e8;
  undefined8 uStack_1e0;
  undefined8 uStack_1d8;
  long local_1d0;
  undefined8 uStack_1c8;
  undefined8 uStack_1c0;
  undefined8 uStack_1b8;
  undefined8 local_1b0;
  undefined8 uStack_1a8;
  undefined8 uStack_1a0;
  undefined8 uStack_198;
  undefined8 local_190;
  undefined8 uStack_188;
  undefined8 uStack_180;
  undefined8 uStack_178;
  undefined8 local_170;
  undefined8 uStack_168;
  undefined8 uStack_160;
  undefined8 uStack_158;
  undefined1 *local_150;
  undefined8 uStack_148;
  undefined8 local_140;
  undefined8 local_138;
  undefined1 *local_130;
  long lStack_128;
  undefined8 uStack_120;
  undefined8 uStack_118;
  undefined8 local_110;
  undefined8 uStack_108;
  undefined8 uStack_100;
  undefined8 local_f8;
  undefined8 local_f0;
  undefined8 uStack_e8;
  undefined8 uStack_e0;
  undefined8 uStack_d8;
  undefined8 local_d0;
  undefined8 uStack_c8;
  undefined8 local_b8;
  undefined8 uStack_b0;
  undefined8 local_a8;
  long *local_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  long *local_80;
  long *local_78;
  long local_70;
  long *local_68;
  
  local_330 = &SUB_aaaaaaaaaaaaaaaa;
  local_338 = (undefined8 *)(param_1 + 0xb8);
  uVar4 = __ZSt19uncaught_exceptionsv();
  local_330 = (undefined1 *)CONCAT44(local_330._4_4_,uVar4);
  lStack_368 = _UNK_0889ca70;
  local_370 = _DAT_0889ca68;
  uStack_358 = _UNK_0889ca80;
  local_360 = _DAT_0889ca78;
  uStack_348 = _UNK_0889ca90;
  local_350 = _DAT_0889ca88;
  uStack_3a8 = _UNK_0889ca30;
  local_3b0 = _DAT_0889ca28;
  local_398 = _UNK_0889ca40;
  local_3a0 = _DAT_0889ca38;
  plStack_388 = (long *)_UNK_0889ca50;
  local_390 = (long *)_DAT_0889ca48;
  local_378 = _UNK_0889ca60;
  local_380 = _DAT_0889ca58;
  local_70 = 0;
  local_68 = (long *)0x0;
  if (((*(long *)(param_1 + 0x10) == 0) ||
      (local_68 = (long *)__ZNSt3__119__shared_weak_count4lockEv(), local_68 == (long *)0x0)) ||
     (lVar12 = *(long *)(param_1 + 8), local_70 = lVar12, lVar12 == 0)) {
    local_2b0 = DAT_0889c2b0;
    local_2a0 = (undefined1 *)0x0;
    puStack_2a8 = (undefined1 *)0x0;
    local_290 = (long *)0x0;
    puStack_298 = (undefined1 *)0x0;
    plStack_288 = (long *)0x0;
    plVar6 = (long *)__Znwm(0x270);
    plVar13 = plVar6 + 1;
    plVar6[2] = 0;
    *plVar13 = 0;
    *plVar6 = (long)&PTR_FUN_09de0f80;
    plVar8 = plVar6 + 3;
    _bzero(plVar8,0x228);
    *(undefined4 *)(plVar6 + 3) = 1;
    plVar6[0x40] = 0;
    plVar6[0x42] = 0;
    plVar6[0x41] = 0;
    *(undefined1 *)(plVar6 + 0x43) = 0;
    plVar6[0x11] = 0;
    plVar6[0x10] = 0;
    plVar6[0x13] = 0;
    plVar6[0x12] = 0;
    plVar6[0x15] = 0;
    plVar6[0x14] = 0;
    plVar6[0x17] = 0;
    plVar6[0x16] = 0;
    plVar6[0x19] = 0;
    plVar6[0x18] = 0;
    plVar6[0x1b] = 0;
    plVar6[0x1a] = 0;
    plVar6[0x1d] = 0;
    plVar6[0x1c] = 0;
    plVar6[0x1f] = 0;
    plVar6[0x1e] = 0;
    plVar6[0x21] = 0;
    plVar6[0x20] = 0;
    plVar6[0x23] = 0;
    plVar6[0x22] = 0;
    plVar6[0x25] = 0;
    plVar6[0x24] = 0;
    plVar6[0x27] = 0;
    plVar6[0x26] = 0;
    plVar6[0x29] = 0;
    plVar6[0x28] = 0;
    plVar6[0x2b] = 0;
    plVar6[0x2a] = 0;
    plVar6[0x2d] = 0;
    plVar6[0x2c] = 0;
    plVar6[0x2f] = 0;
    plVar6[0x2e] = 0;
    plVar6[0x31] = 0;
    plVar6[0x30] = 0;
    plVar6[0x33] = 0;
    plVar6[0x32] = 0;
    plVar6[0x35] = 0;
    plVar6[0x34] = 0;
    plVar6[0x37] = 0;
    plVar6[0x36] = 0;
    plVar6[0x39] = 0;
    plVar6[0x38] = 0;
    plVar6[0x3b] = 0;
    plVar6[0x3a] = 0;
    plVar6[0x3d] = 0;
    plVar6[0x3c] = 0;
    *(undefined8 *)((long)plVar6 + 0x1f1) = 0;
    *(undefined8 *)((long)plVar6 + 0x1e9) = 0;
    *(undefined2 *)(plVar6 + 0x47) = 0;
    plVar6[0x46] = 0;
    plVar6[0x45] = 0;
    plVar6[0x44] = 0;
    plVar6[0x49] = 0;
    plVar6[0x48] = 0;
    plVar6[0x4b] = 0;
    plVar6[0x4a] = 0;
    plVar6[0x4d] = 0;
    plVar6[0x4c] = 0;
    local_3b0 = local_2b0;
    uStack_3a8 = 0;
    local_3a0 = 0;
    local_398 = 0;
    local_390 = plVar8;
    plStack_388 = plVar6;
    local_290 = plVar8;
    plStack_288 = plVar6;
    if (plVar6 == (long *)0x0) {
      local_380 = (ulong)local_380._5_3_ << 0x28;
      local_378 = (ulong)local_378._1_7_ << 8;
      uStack_348 = (ulong)uStack_348._1_7_ << 8;
    }
    else {
      *plVar13 = *plVar13 + 1;
      local_380 = (ulong)local_380._5_3_ << 0x28;
      local_378 = (ulong)local_378._1_7_ << 8;
      uStack_348 = (ulong)uStack_348._1_7_ << 8;
      LOAcquire();
      lVar12 = *plVar13;
      *plVar13 = lVar12 + -1;
      LORelease();
      if (lVar12 == 0) {
        (**(code **)(*plVar6 + 0x10))(plVar6);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
      }
    }
    if ((long)puStack_298 < 0) {
      __ZdlPvm(puStack_2a8,(ulong)puStack_298 & 0x7fffffffffffffff);
    }
    goto LAB_02feb2a8;
  }
  uStack_88 = 0;
  local_90 = 0;
  local_78 = (long *)0x0;
  local_80 = (long *)0x0;
  uStack_98 = 0;
  local_a0 = (long *)0x0;
  plVar6 = (long *)__Znwm(0x270);
  puVar10 = (undefined8 *)((ulong)&local_a0 | 8);
  plVar6[2] = 0;
  plVar6[1] = 0;
  *plVar6 = (long)&PTR_FUN_09de0f80;
  plVar8 = plVar6 + 3;
  _bzero(plVar8,0x228);
  *(undefined4 *)(plVar6 + 3) = 1;
  plVar6[0x40] = 0;
  plVar6[0x42] = 0;
  plVar6[0x41] = 0;
  *(undefined1 *)(plVar6 + 0x43) = 0;
  plVar6[0x11] = 0;
  plVar6[0x10] = 0;
  plVar6[0x13] = 0;
  plVar6[0x12] = 0;
  plVar6[0x15] = 0;
  plVar6[0x14] = 0;
  plVar6[0x17] = 0;
  plVar6[0x16] = 0;
  plVar6[0x19] = 0;
  plVar6[0x18] = 0;
  plVar6[0x1b] = 0;
  plVar6[0x1a] = 0;
  plVar6[0x1d] = 0;
  plVar6[0x1c] = 0;
  plVar6[0x1f] = 0;
  plVar6[0x1e] = 0;
  plVar6[0x21] = 0;
  plVar6[0x20] = 0;
  plVar6[0x23] = 0;
  plVar6[0x22] = 0;
  plVar6[0x25] = 0;
  plVar6[0x24] = 0;
  plVar6[0x27] = 0;
  plVar6[0x26] = 0;
  plVar6[0x29] = 0;
  plVar6[0x28] = 0;
  plVar6[0x2b] = 0;
  plVar6[0x2a] = 0;
  plVar6[0x2d] = 0;
  plVar6[0x2c] = 0;
  plVar6[0x2f] = 0;
  plVar6[0x2e] = 0;
  plVar6[0x31] = 0;
  plVar6[0x30] = 0;
  plVar6[0x33] = 0;
  plVar6[0x32] = 0;
  plVar6[0x35] = 0;
  plVar6[0x34] = 0;
  plVar6[0x37] = 0;
  plVar6[0x36] = 0;
  plVar6[0x39] = 0;
  plVar6[0x38] = 0;
  plVar6[0x3b] = 0;
  plVar6[0x3a] = 0;
  plVar6[0x3d] = 0;
  plVar6[0x3c] = 0;
  *(undefined8 *)((long)plVar6 + 0x1f1) = 0;
  *(undefined8 *)((long)plVar6 + 0x1e9) = 0;
  *(undefined2 *)(plVar6 + 0x47) = 0;
  plVar6[0x46] = 0;
  plVar6[0x45] = 0;
  plVar6[0x44] = 0;
  plVar6[0x49] = 0;
  plVar6[0x48] = 0;
  plVar6[0x4b] = 0;
  plVar6[0x4a] = 0;
  plVar6[0x4d] = 0;
  plVar6[0x4c] = 0;
  local_80 = plVar8;
  local_78 = plVar6;
  if (*(int *)(param_1 + 0x48) == 1) {
    local_328 = (undefined1 *)0x0;
    local_320 = 0;
    local_318 = (undefined1 *)0x0;
    local_b8 = 0;
    uStack_b0 = 0;
    local_a8 = 0;
    puStack_298 = &SUB_aaaaaaaaaaaaaaaa;
    local_2a0 = &SUB_aaaaaaaaaaaaaaaa;
    plStack_288 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    local_290 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    puStack_2a8 = &SUB_aaaaaaaaaaaaaaaa;
    local_2b0 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    FUN_02fdf1c4(&local_2b0,lVar12,1,param_1 + 0x50,&local_328,&local_b8,param_1 + 0x88,
                 *(undefined8 *)(param_1 + 0x68),param_1 + 0xa0);
    lVar11 = *(long *)(param_1 + 0x68);
    if (lVar11 == 0) {
      plVar8 = (long *)FUN_04669774();
      lVar11 = (**(code **)(*plVar8 + 0x40))();
    }
    FUN_02fd7104(&local_2f0,lVar12,&local_2b0,param_1 + 0x50,lVar11);
    local_a0 = local_2f0;
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar10,&puStack_2e8);
    plVar8 = local_78;
    if (local_2c8 != (long *)0x0) {
      local_2c8[1] = local_2c8[1] + 1;
    }
    local_80 = local_2d0;
    local_78 = local_2c8;
    if (plVar8 != (long *)0x0) {
      LOAcquire();
      lVar12 = plVar8[1];
      plVar8[1] = lVar12 + -1;
      LORelease();
      if (lVar12 == 0) {
        (**(code **)(*plVar8 + 0x10))(plVar8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
      }
    }
    plVar8 = local_2c8;
    if (local_2c8 != (long *)0x0) {
      LOAcquire();
      lVar12 = local_2c8[1];
      local_2c8[1] = lVar12 + -1;
      LORelease();
      if (lVar12 == 0) {
        (**(code **)(*local_2c8 + 0x10))(local_2c8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
      }
    }
    if ((long)puStack_2d8 < 0) {
      __ZdlPvm(puStack_2e8,(ulong)puStack_2d8 & 0x7fffffffffffffff);
    }
    local_80[0xd] = lVar11;
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (local_80 + 0xe,param_1 + 0x50);
    plVar8 = plStack_288;
    if (plStack_288 != (long *)0x0) {
      LOAcquire();
      lVar12 = plStack_288[1];
      plStack_288[1] = lVar12 + -1;
      LORelease();
      if (lVar12 == 0) {
        (**(code **)(*plStack_288 + 0x10))(plStack_288);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
      }
    }
    puVar1 = local_328;
    puVar2 = local_318;
    if ((long)puStack_298 < 0) {
      __ZdlPvm(puStack_2a8,(ulong)puStack_298 & 0x7fffffffffffffff);
      puVar1 = local_328;
      puVar2 = local_318;
    }
joined_r0x02feae28:
    if ((long)puVar2 < 0) {
      __ZdlPvm(puVar1,(ulong)puVar2 & 0x7fffffffffffffff);
    }
  }
  else if (*(int *)(param_1 + 0x48) == 0) {
    uVar7 = FUN_04669774();
    FUN_02fd02c8(&local_2b0,lVar12,uVar7);
    local_a0 = local_2b0;
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar10,&puStack_2a8);
    plVar8 = local_78;
    if (plStack_288 != (long *)0x0) {
      plStack_288[1] = plStack_288[1] + 1;
    }
    local_80 = local_290;
    local_78 = plStack_288;
    if (plVar8 != (long *)0x0) {
      LOAcquire();
      lVar12 = plVar8[1];
      plVar8[1] = lVar12 + -1;
      LORelease();
      if (lVar12 == 0) {
        (**(code **)(*plVar8 + 0x10))(plVar8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
      }
    }
    plVar8 = plStack_288;
    puVar1 = puStack_2a8;
    puVar2 = puStack_298;
    if (plStack_288 != (long *)0x0) {
      LOAcquire();
      lVar12 = plStack_288[1];
      plStack_288[1] = lVar12 + -1;
      LORelease();
      if (lVar12 == 0) {
        (**(code **)(*plStack_288 + 0x10))(plStack_288);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
        puVar1 = puStack_2a8;
        puVar2 = puStack_298;
      }
    }
    goto joined_r0x02feae28;
  }
  if (*(char *)((long)local_80 + 4) == '\x01') {
    thunk_FUN_000a5900();
    local_138 = 0;
    uStack_148 = 0;
    local_140 = 0;
    local_130 = &DAT_aaaaaaaaaaaaaa00;
    puStack_2a8 = (undefined1 *)0x0;
    local_2b0 = (long *)0x0;
    puStack_298 = (undefined1 *)0x0;
    local_2a0 = (undefined1 *)0x0;
    plStack_288 = (long *)0x0;
    local_290 = (long *)0x0;
    uStack_278 = 0;
    uStack_280 = 0;
    uStack_268 = 0;
    local_270 = 0;
    uStack_258 = 0;
    uStack_260 = 0;
    uStack_248 = 0;
    local_250 = 0;
    uStack_238 = 0;
    uStack_240 = 0;
    uStack_228 = 0;
    local_230 = 0;
    uStack_218 = 0;
    uStack_220 = 0;
    uStack_208 = 0;
    local_210 = 0;
    uStack_1f8 = 0;
    uStack_200 = 0;
    uStack_1e8 = 0;
    local_1f0 = 0;
    uStack_1d8 = 0;
    uStack_1e0 = 0;
    uStack_1c8 = 0;
    local_1d0 = 0;
    uStack_1b8 = 0;
    uStack_1c0 = 0;
    uStack_1a8 = 0;
    local_1b0 = 0;
    uStack_198 = 0;
    uStack_1a0 = 0;
    uStack_188 = 0;
    local_190 = 0;
    uStack_178 = 0;
    uStack_180 = 0;
    uStack_168 = 0;
    local_170 = 0;
    uStack_158 = 0;
    uStack_160 = 0;
    local_150 = &DAT_aaaaaaaaaaaaaa00;
    local_110 = 0;
    uStack_118 = 0;
    uStack_100 = 0;
    uStack_108 = 0;
    uStack_120 = 0;
    lStack_128 = 0;
    local_f8 = 0xaaaaaaaaaaaa0000;
    uStack_e8 = 0;
    local_f0 = 0;
    uStack_d8 = 0;
    uStack_e0 = 0;
    uStack_c8 = 0;
    local_d0 = 0;
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&uStack_278,local_80 + 0x11);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&uStack_260,local_80 + 0x14);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&uStack_248,local_80 + 0x17);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&local_230,local_80 + 0x1a);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&uStack_218,local_80 + 0x1d);
    puStack_298 = (undefined1 *)local_80[0xd];
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&local_2b0,local_80 + 0xe);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&local_290,local_80 + 0x20);
    plVar8 = local_80;
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&uStack_1e8,local_80 + 0x29);
    local_1d0 = plVar8[0x2c];
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&uStack_1c8,plVar8 + 0x2d);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&local_1b0,plVar8 + 0x30);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&uStack_198,plVar8 + 0x33);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&uStack_180,plVar8 + 0x36);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&uStack_168,plVar8 + 0x39);
    local_150 = (undefined1 *)CONCAT71(local_150._1_7_,(char)plVar8[0x3c]);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&uStack_148,plVar8 + 0x3d);
    local_130 = (undefined1 *)CONCAT71(local_130._1_7_,(char)plVar8[0x40]);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&uStack_200,local_80 + 0x23);
    if (&lStack_128 != local_80 + 0x41) {
      FUN_00496aac(&lStack_128,local_80[0x41],local_80[0x42],
                   (local_80[0x42] - local_80[0x41] >> 3) * -0x5555555555555555);
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&local_110,local_80 + 0x26);
    local_f8 = CONCAT62(local_f8._2_6_,(short)local_80[0x44]);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&local_f0,local_80 + 0x45);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&uStack_d8,local_80 + 0x48);
    puStack_2d8 = &SUB_aaaaaaaaaaaaaaaa;
    local_2e0 = &SUB_aaaaaaaaaaaaaaaa;
    local_2c8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    local_2d0 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    puStack_2e8 = &SUB_aaaaaaaaaaaaaaaa;
    local_2f0 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    local_2bc = &SUB_aaaaaaaaaaaaaaaa;
    local_2c0 = 0xffffffff;
    local_2b4 = 0xaaaaaaaa;
    uVar7 = FUN_04669774();
    FUN_0466dfb8(&local_2f0,uVar7,&local_2b0);
    if (*(int *)(param_1 + 0x48) == 0) {
      FUN_02fe7d3c(&local_328);
      FUN_02fede54((ulong)&local_2f0 | 8,&local_328);
      lVar12 = local_320;
      if (local_2f8 == '\x01') {
        while (local_310 != (long *)0x0) {
          lVar11 = *local_310;
          local_320 = lVar12;
          __ZdlPvm(local_310,0x18);
          lVar12 = local_320;
          local_310 = (long *)lVar11;
        }
        local_320 = 0;
        if (lVar12 != 0) {
          __ZdlPvm(lVar12,(long)local_318 << 3);
        }
      }
    }
    local_3b0 = local_a0;
    puVar9 = (undefined8 *)((ulong)&local_3b0 | 8);
    uVar7 = *puVar10;
    puVar9[1] = puVar10[1];
    *puVar9 = uVar7;
    puVar9[2] = puVar10[2];
    local_390 = local_80;
    plStack_388 = local_78;
    if (local_78 != (long *)0x0) {
      local_78[1] = local_78[1] + 1;
    }
    local_380._0_5_ = SUB85(local_2f0,0);
    uVar3 = local_378 >> 0x20;
    local_378 = local_378 & 0xffffffffffffff00;
    uStack_348 = uStack_348 & 0xffffffffffffff00;
    if (local_2bc._4_1_ == '\x01') {
      local_378 = CONCAT44((int)uVar3,puStack_2e8._0_4_);
      FUN_02fea310(&local_370,&local_2e0);
      uStack_348 = CONCAT71(uStack_348._1_7_,1);
      puVar1 = local_2e0;
      plVar8 = local_2d0;
      if (((ulong)local_2bc & 0x100000000) != 0) {
        while (plVar8 != (long *)0x0) {
          plVar6 = (long *)*plVar8;
          local_2e0 = puVar1;
          __ZdlPvm(plVar8,0x18);
          puVar1 = local_2e0;
          plVar8 = plVar6;
        }
        local_2e0 = (undefined1 *)0x0;
        if (puVar1 != (undefined1 *)0x0) {
          __ZdlPvm(puVar1,(long)puStack_2d8 << 3);
        }
      }
    }
    FUN_02feb8bc(&local_2b0);
    plVar8 = local_78;
  }
  else {
    plStack_288 = (long *)0x0;
    local_290 = (long *)0x0;
    uStack_278 = 0;
    uStack_280 = 0;
    puStack_2a8 = (undefined1 *)0x0;
    local_2b0 = (long *)0x0;
    puStack_298 = (undefined1 *)0x0;
    local_2a0 = (undefined1 *)0x0;
    puVar9 = (undefined8 *)((ulong)&local_3b0 | 8);
    uVar7 = *puVar10;
    puVar9[1] = puVar10[1];
    *puVar9 = uVar7;
    puVar9[2] = puVar10[2];
    if (local_78 != (long *)0x0) {
      local_78[1] = local_78[1] + 1;
    }
    local_380 = local_380 & 0xffffff0000000000;
    local_378 = local_378 & 0xffffffffffffff00;
    uStack_348 = uStack_348 & 0xffffffffffffff00;
    local_3b0 = local_a0;
    local_390 = local_80;
    plStack_388 = local_78;
    plVar8 = local_78;
  }
  local_78 = plVar8;
  if (plVar8 != (long *)0x0) {
    LOAcquire();
    lVar12 = plVar8[1];
    plVar8[1] = lVar12 + -1;
    LORelease();
    if (lVar12 == 0) {
      (**(code **)(*plVar8 + 0x10))(plVar8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    }
  }
LAB_02feb2a8:
  plVar8 = local_68;
  if (local_68 != (long *)0x0) {
    LOAcquire();
    lVar12 = local_68[1];
    local_68[1] = lVar12 + -1;
    LORelease();
    if (lVar12 == 0) {
      (**(code **)(*local_68 + 0x10))(local_68);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    }
  }
  FUN_02feb6e4((undefined8 *)(param_1 + 0xb8),&local_3b0);
  lVar12 = local_370;
  plVar8 = local_360;
  if ((char)uStack_348 == '\x01') {
    while (plVar8 != (long *)0x0) {
      lVar11 = *plVar8;
      local_370 = lVar12;
      __ZdlPvm(plVar8,0x18);
      lVar12 = local_370;
      plVar8 = (long *)lVar11;
    }
    local_370 = 0;
    if (lVar12 != 0) {
      __ZdlPvm(lVar12,lStack_368 << 3);
    }
  }
  plVar8 = plStack_388;
  if (plStack_388 != (long *)0x0) {
    LOAcquire();
    lVar12 = plStack_388[1];
    plStack_388[1] = lVar12 + -1;
    LORelease();
    if (lVar12 == 0) {
      (**(code **)(*plStack_388 + 0x10))(plStack_388);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    }
  }
  if ((long)local_398 < 0) {
    __ZdlPvm(uStack_3a8,local_398 & 0x7fffffffffffffff);
  }
  iVar5 = __ZSt19uncaught_exceptionsv();
  if ((int)local_330 < iVar5) {
    local_2b0 = (long *)0x0;
    FUN_06669050(*local_338,&local_2b0);
    if (local_2b0 != (long *)0x0) {
      (**(code **)(*local_2b0 + 8))();
    }
  }
  return;
}


