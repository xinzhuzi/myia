// Ghidra inferred pseudocode; requested=0x410dc54
// entry=0410dc54 end=041100ff

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0410dc54(int *param_1)

{
  undefined8 ******ppppppuVar1;
  long *plVar2;
  undefined8 *puVar3;
  undefined8 ******ppppppuVar4;
  byte bVar5;
  long lVar6;
  long ******pppppplVar7;
  undefined8 *****pppppuVar8;
  undefined1 *puVar9;
  int iVar10;
  uint uVar11;
  long *plVar12;
  undefined8 uVar13;
  undefined8 uVar14;
  undefined8 *******pppppppuVar15;
  long *******ppppppplVar16;
  code *pcVar17;
  ulong uVar18;
  undefined1 *puVar19;
  undefined1 *puVar20;
  long lVar21;
  undefined8 *puVar22;
  undefined8 *puVar23;
  uint uVar24;
  long *******ppppppplVar25;
  long *******ppppppplVar26;
  long local_568;
  long local_560;
  long *******local_558;
  long *******local_550;
  long *******local_548 [2];
  undefined7 local_538;
  char cStack_531;
  undefined8 *******local_530 [2];
  undefined7 local_520;
  char cStack_519;
  undefined1 *local_518;
  undefined1 *local_510;
  undefined1 *puStack_508;
  undefined1 *local_500;
  undefined1 *local_4f8;
  undefined1 *puStack_4f0;
  long local_4e8;
  long local_4e0;
  long local_4d8;
  long *******local_4d0;
  long *******ppppppplStack_4c8;
  undefined1 *local_4c0;
  undefined1 *local_4b8;
  undefined7 local_4b0;
  undefined1 uStack_4a9;
  undefined1 uStack_4a8;
  undefined7 uStack_4a7;
  undefined1 *local_4a0;
  undefined1 *puStack_498;
  undefined1 *local_490;
  undefined1 *puStack_488;
  undefined8 *local_480;
  undefined7 uStack_478;
  undefined1 local_471;
  undefined4 uStack_470;
  undefined4 uStack_46c;
  undefined4 uStack_468;
  undefined4 uStack_464;
  undefined1 *local_460;
  undefined1 *puStack_458;
  undefined1 *local_450;
  undefined1 *puStack_448;
  undefined1 *puStack_440;
  undefined1 *puStack_438;
  undefined1 *local_430;
  undefined8 uStack_428;
  undefined8 uStack_420;
  undefined8 uStack_418;
  undefined8 local_410;
  undefined8 uStack_408;
  undefined8 uStack_400;
  undefined1 *puStack_3f8;
  undefined8 local_3f0;
  long local_3e8;
  long *local_3e0;
  long *local_3d8;
  undefined8 local_3d0;
  undefined8 uStack_3c8;
  ulong local_3c0;
  long *******local_3b0;
  undefined8 uStack_3a8;
  undefined8 uStack_3a0;
  ulong local_398;
  undefined8 ******local_390;
  undefined8 ******ppppppuStack_388;
  undefined8 local_380;
  undefined8 uStack_378;
  long local_370;
  long lStack_368;
  long *local_360;
  undefined8 uStack_358;
  undefined8 local_350;
  undefined8 uStack_348;
  long *******local_338;
  undefined8 ******local_330;
  undefined8 ******ppppppuStack_328;
  undefined8 ******local_320;
  undefined8 ******local_318;
  undefined8 ******local_310;
  undefined1 auStack_308 [136];
  undefined4 *local_280;
  undefined1 local_278;
  undefined8 *******local_230;
  long *local_228;
  undefined7 local_220;
  char cStack_219;
  long *******local_1e0;
  long *******local_1d8;
  undefined7 local_1d0;
  char cStack_1c9;
  long *******local_190;
  long *******local_188;
  undefined7 local_180;
  char cStack_179;
  long *******local_140;
  long *******ppppppplStack_138;
  undefined8 *******local_130;
  undefined7 uStack_128;
  char cStack_121;
  undefined1 uStack_120;
  undefined7 uStack_11f;
  undefined1 *puStack_118;
  undefined1 *puStack_110;
  undefined1 *puStack_108;
  undefined1 *puStack_100;
  undefined1 *puStack_f8;
  undefined7 local_f0;
  char cStack_e9;
  undefined4 uStack_e8;
  undefined4 uStack_e4;
  undefined4 uStack_e0;
  undefined4 uStack_dc;
  undefined1 *puStack_d8;
  undefined1 *local_d0;
  undefined7 uStack_c8;
  char cStack_c1;
  undefined1 uStack_c0;
  undefined7 uStack_bf;
  undefined1 *local_b8;
  undefined1 *puStack_b0;
  undefined1 *local_a8;
  undefined **local_98;
  code *pcStack_90;
  undefined ***local_80;
  long local_78;
  
  local_78 = *(long *)PTR____stack_chk_guard_09b36c98;
  lStack_368 = _UNK_089beb08;
  local_370 = _DAT_089beb00;
  uStack_358 = _UNK_089beb18;
  local_360 = (long *)_DAT_089beb10;
  uStack_348 = _UNK_089beb28;
  local_350 = _DAT_089beb20;
  uStack_3a8 = 0;
  local_3b0 = (long *******)0x0;
  local_398 = 0;
  uStack_3a0 = 0;
  ppppppuStack_388 = (undefined8 ******)0x0;
  local_390 = (undefined8 ******)0x0;
  uStack_378 = _UNK_089beaf8;
  local_380 = _DAT_089beaf0;
  plVar12 = (long *)__Znwm(0x270);
  plVar12[2] = 0;
  plVar12[1] = 0;
  *plVar12 = (long)&PTR_FUN_09de0f80;
  plVar2 = plVar12 + 3;
  _bzero(plVar2,0x228);
  *(undefined4 *)(plVar12 + 3) = 1;
  plVar12[0x40] = 0;
  plVar12[0x42] = 0;
  plVar12[0x41] = 0;
  *(undefined1 *)(plVar12 + 0x43) = 0;
  plVar12[0x11] = 0;
  plVar12[0x10] = 0;
  plVar12[0x13] = 0;
  plVar12[0x12] = 0;
  plVar12[0x15] = 0;
  plVar12[0x14] = 0;
  plVar12[0x17] = 0;
  plVar12[0x16] = 0;
  plVar12[0x19] = 0;
  plVar12[0x18] = 0;
  plVar12[0x1b] = 0;
  plVar12[0x1a] = 0;
  plVar12[0x1d] = 0;
  plVar12[0x1c] = 0;
  plVar12[0x1f] = 0;
  plVar12[0x1e] = 0;
  plVar12[0x21] = 0;
  plVar12[0x20] = 0;
  plVar12[0x23] = 0;
  plVar12[0x22] = 0;
  plVar12[0x25] = 0;
  plVar12[0x24] = 0;
  plVar12[0x27] = 0;
  plVar12[0x26] = 0;
  plVar12[0x29] = 0;
  plVar12[0x28] = 0;
  plVar12[0x2b] = 0;
  plVar12[0x2a] = 0;
  plVar12[0x2d] = 0;
  plVar12[0x2c] = 0;
  plVar12[0x2f] = 0;
  plVar12[0x2e] = 0;
  plVar12[0x31] = 0;
  plVar12[0x30] = 0;
  plVar12[0x33] = 0;
  plVar12[0x32] = 0;
  plVar12[0x35] = 0;
  plVar12[0x34] = 0;
  plVar12[0x37] = 0;
  plVar12[0x36] = 0;
  plVar12[0x39] = 0;
  plVar12[0x38] = 0;
  plVar12[0x3b] = 0;
  plVar12[0x3a] = 0;
  plVar12[0x3d] = 0;
  plVar12[0x3c] = 0;
  *(undefined8 *)((long)plVar12 + 0x1f1) = 0;
  *(undefined8 *)((long)plVar12 + 0x1e9) = 0;
  *(undefined2 *)(plVar12 + 0x47) = 0;
  plVar12[0x46] = 0;
  plVar12[0x45] = 0;
  plVar12[0x44] = 0;
  plVar12[0x49] = 0;
  plVar12[0x48] = 0;
  plVar12[0x4b] = 0;
  plVar12[0x4a] = 0;
  plVar12[0x4d] = 0;
  plVar12[0x4c] = 0;
  uStack_378 = 0;
  local_380 = 0;
  lStack_368 = 0;
  local_370 = 0;
  uStack_358 = 0;
  local_360 = (long *)0x0;
  uStack_348 = 0;
  local_350 = 0;
  puStack_100 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_118 = &SUB_aaaaaaaaaaaaaaaa;
  uStack_120 = 0xaa;
  uStack_11f = 0xaaaaaaaaaaaaaa;
  puStack_108 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_110 = &SUB_aaaaaaaaaaaaaaaa;
  ppppppplStack_138 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
  local_140 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
  uStack_128 = 0xaaaaaaaaaaaaaa;
  cStack_121 = -0x56;
  local_130 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
  local_98 = &PTR_FUN_09e5b308;
  pcStack_90 = FUN_04a166b0;
  local_80 = &local_98;
  local_390 = (undefined8 ******)plVar2;
  ppppppuStack_388 = (undefined8 ******)plVar12;
  if (DAT_0a51ecb8._7_1_ < '\0') {
    FUN_00018d20(&local_3d0,DAT_0a51eca8,DAT_0a51ecb0);
  }
  else {
    uStack_3c8 = DAT_0a51ecb0;
    local_3d0 = DAT_0a51eca8;
    local_3c0 = CONCAT17(DAT_0a51ecb8._7_1_,(undefined7)DAT_0a51ecb8);
  }
  FUN_041105c4(&local_140,&local_98,1,&local_3d0);
  if ((long)local_3c0 < 0) {
    __ZdlPvm(local_3d0,local_3c0 & 0x7fffffffffffffff);
  }
  if (local_80 == &local_98) {
    pcVar17 = (code *)(*local_80)[4];
LAB_0410de0c:
    (*pcVar17)();
  }
  else if (local_80 != (undefined ***)0x0) {
    pcVar17 = (code *)(*local_80)[5];
    goto LAB_0410de0c;
  }
  FUN_04669774();
  FUN_046728d0(&local_1e0);
  FUN_03016948(&local_190,local_1e0);
  FUN_02fc361c(&local_4d0,local_190,param_1);
  puVar22 = (undefined8 *)((ulong)&local_3b0 | 8);
  local_3b0 = local_4d0;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (puVar22,&ppppppplStack_4c8);
  ppppppuVar4 = ppppppuStack_388;
  local_390 = (undefined8 ******)CONCAT17(uStack_4a9,local_4b0);
  ppppppuVar1 = (undefined8 ******)CONCAT71(uStack_4a7,uStack_4a8);
  if (ppppppuVar1 != (undefined8 ******)0x0) {
    ppppppuVar1[1] = (undefined8 *****)((long)ppppppuVar1[1] + 1);
  }
  if (ppppppuStack_388 != (undefined8 ******)0x0) {
    LOAcquire();
    lVar6 = (long)ppppppuStack_388[1];
    ppppppuStack_388[1] = (undefined8 *****)(lVar6 + -1);
    LORelease();
    if (lVar6 == 0) {
      (**(code **)((long)*ppppppuStack_388 + 0x10))(ppppppuStack_388);
      ppppppuStack_388 = ppppppuVar1;
      __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppuVar4);
      ppppppuVar1 = ppppppuStack_388;
    }
  }
  ppppppuStack_388 = ppppppuVar1;
  local_380._0_5_ = SUB85(local_4a0,0);
  FUN_02fede54(&uStack_378,&puStack_498);
  puVar19 = local_490;
  puVar3 = local_480;
  if ((char)uStack_468 == '\x01') {
    while (puVar3 != (undefined8 *)0x0) {
      puVar23 = (undefined8 *)*puVar3;
      local_490 = puVar19;
      __ZdlPvm(puVar3,0x18);
      puVar19 = local_490;
      puVar3 = puVar23;
    }
    local_490 = (undefined1 *)0x0;
    if (puVar19 != (undefined1 *)0x0) {
      __ZdlPvm(puVar19,(long)puStack_488 << 3);
    }
  }
  plVar2 = (long *)CONCAT71(uStack_4a7,uStack_4a8);
  if (plVar2 != (long *)0x0) {
    LOAcquire();
    lVar6 = plVar2[1];
    plVar2[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*plVar2 + 0x10))(plVar2);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  if ((long)local_4b8 < 0) {
    __ZdlPvm(ppppppplStack_4c8,(ulong)local_4b8 & 0x7fffffffffffffff);
  }
  ppppppplVar16 = local_188;
  if (local_188 != (long *******)0x0) {
    LOAcquire();
    pppppplVar7 = local_188[1];
    local_188[1] = (long ******)((long)pppppplVar7 + -1);
    LORelease();
    if (pppppplVar7 == (long ******)0x0) {
      (*(code *)(*local_188)[2])(local_188);
      __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar16);
    }
  }
  ppppppplVar16 = local_1d8;
  if (local_1d8 != (long *******)0x0) {
    LOAcquire();
    pppppplVar7 = local_1d8[1];
    local_1d8[1] = (long ******)((long)pppppplVar7 + -1);
    LORelease();
    if (pppppplVar7 == (long ******)0x0) {
      (*(code *)(*local_1d8)[2])(local_1d8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar16);
    }
  }
  FUN_04111974(&local_140);
  local_3e0 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_3d8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0466aca8(&local_3e0);
  if ((*(char *)((long)local_390 + 4) == '\x01') && (local_3e0 != (long *)0x0)) {
    uVar13 = (**(code **)(*local_3e0 + 0x18))();
    uVar14 = FUN_04554c10(local_3e0);
    iVar10 = FUN_04a7a3e0(uVar13,uVar14);
    if (iVar10 != 0) {
      if (((ulong)*local_390 & 0x100000000) != 0) goto LAB_0410e170;
LAB_0410dff8:
      iVar10 = thunk_FUN_05e1d97c(4);
      if (iVar10 != 0) {
        FUN_0488143c(&local_190);
        ppppppplVar16 = local_190;
        if (-1 < cStack_179) {
          ppppppplVar16 = (long *******)&local_190;
        }
        if ((DAT_0a43e621 & 1) == 0) {
          uRam000000000a43e618._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[8];
          uRam000000000a43e618._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[9];
          uRam000000000a43e618._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[10];
          uRam000000000a43e618._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xb];
          uRam000000000a43e618._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xc];
          uRam000000000a43e618._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xd];
          uRam000000000a43e618._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xe];
          uRam000000000a43e618._7_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xf];
          DAT_0a43e610 = s_login_service_ccGetAutoLoginInfo_089be4f0[0];
          DAT_0a43e610_1._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[1];
          DAT_0a43e610_1._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[2];
          DAT_0a43e610_1._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[3];
          DAT_0a43e610_1._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[4];
          DAT_0a43e610_1._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[5];
          DAT_0a43e610_1._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[6];
          DAT_0a43e610_1._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[7];
          DAT_0a43e620 = 0;
          DAT_0a43e621 = 1;
        }
        if ((DAT_0a43e903 & 1) == 0) {
          DAT_0a43e8f8._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
          DAT_0a43e8f8._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
          DAT_0a43e8f8._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
          DAT_0a43e8f8._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
          DAT_0a43e8f8._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
          DAT_0a43e8f8._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
          DAT_0a43e8f8._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
          DAT_0a43e8f8._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
          DAT_0a43e900 = 0x2928;
          DAT_0a43e902 = 0;
          DAT_0a43e903 = 1;
        }
        FUN_05e1d050(&local_4d0,4,ppppppplVar16,&DAT_0a43e610,&DAT_0a43e8f8,0x23d,0,0);
        if ((DAT_0a43eb00 & 1) == 0) {
          uVar18 = 0;
          do {
            (&DAT_0a43ead2)[uVar18] = (&DAT_089bf750)[uVar18] + 0x8a ^ (&DAT_089bf740)[uVar18 & 0xf]
            ;
            uVar18 = uVar18 + 1;
          } while (uVar18 != 0x2e);
          DAT_0a43eb00 = 1;
        }
        puStack_d8 = (undefined1 *)0x0;
        uStack_e0 = 0;
        uStack_dc = 0;
        uStack_c8 = 0;
        cStack_c1 = '\0';
        local_d0 = (undefined1 *)0x0;
        puStack_f8 = (undefined1 *)0x0;
        puStack_100 = (undefined1 *)0x0;
        uStack_e8 = 0;
        uStack_e4 = 0;
        local_f0 = 0;
        cStack_e9 = '\0';
        puStack_118 = (undefined1 *)0x0;
        uStack_120 = 0;
        uStack_11f = 0;
        puStack_108 = (undefined1 *)0x0;
        puStack_110 = (undefined1 *)0x0;
        ppppppplStack_138 = (long *******)0x0;
        local_140 = (long *******)0x0;
        uStack_128 = 0;
        cStack_121 = '\0';
        local_130 = (undefined8 *******)0x0;
        FUN_05e1d31c(&local_4d0,&DAT_0a43ead2,&local_140);
        thunk_FUN_05e1d0bc(&local_4d0);
        if (cStack_179 < '\0') {
          __ZdlPvm(local_190,CONCAT17(cStack_179,local_180) & 0x7fffffffffffffff);
        }
      }
      local_338 = local_3b0;
      if ((long)local_398 < 0) {
        FUN_00018d20(&local_330,uStack_3a8,uStack_3a0);
      }
      else {
        ppppppuStack_328 = (undefined8 ******)puVar22[1];
        local_330 = (undefined8 ******)*puVar22;
        local_320 = (undefined8 ******)puVar22[2];
      }
      local_318 = local_390;
      local_310 = ppppppuStack_388;
      pppppuVar8 = (undefined8 *****)0x0;
      if (ppppppuStack_388 != (undefined8 ******)0x0) {
        pppppuVar8 = ppppppuStack_388[1];
        ppppppuStack_388[1] = (undefined8 *****)((long)pppppuVar8 + 1);
      }
      FUN_04112ab8(pppppuVar8,auStack_308,param_1 + 0x1c);
      ppppppplStack_138 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
      local_140 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
      FUN_021efaf0(&local_140,&local_4d0);
      ppppppplVar25 = ppppppplStack_138;
      ppppppplVar16 = local_140;
      local_190 = local_140;
      local_188 = ppppppplStack_138;
      if (ppppppplStack_138 != (long *******)0x0) {
        ppppppplStack_138[1] = (long ******)((long)ppppppplStack_138[1] + 1);
      }
      if ((DAT_0a43e903 & 1) == 0) {
        DAT_0a43e8f8._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
        DAT_0a43e8f8._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
        DAT_0a43e8f8._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
        DAT_0a43e8f8._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
        DAT_0a43e8f8._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
        DAT_0a43e8f8._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
        DAT_0a43e8f8._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
        DAT_0a43e8f8._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
        DAT_0a43e900 = 0x2928;
        DAT_0a43e902 = 0;
        DAT_0a43e903 = 1;
      }
      if ((DAT_0a43e6d6 & 1) == 0) {
        uVar18 = 0;
        do {
          (&DAT_0a43e67b)[uVar18] = (&DAT_089bee1d)[uVar18] + 0x8a ^ (&DAT_089bee0d)[uVar18 & 0xf];
          uVar18 = uVar18 + 1;
        } while (uVar18 != 0x5b);
        DAT_0a43e6d6 = 1;
      }
      FUN_0003bb6c(&local_4d0,&DAT_0a43e8f8,&DAT_0a43e67b,0x240);
      pppppppuVar15 = (undefined8 *******)__Znwm(0xf0);
      FUN_00033c40(pppppppuVar15,FUN_041127f4,FUN_04112920);
      pppppppuVar15[5] = local_338;
      if ((long)local_320 < 0) {
        FUN_00018d20(pppppppuVar15 + 6,local_330,ppppppuStack_328);
      }
      else {
        pppppppuVar15[7] = ppppppuStack_328;
        pppppppuVar15[6] = local_330;
        pppppppuVar15[8] = local_320;
      }
      pppppppuVar15[9] = local_318;
      pppppppuVar15[10] = local_310;
      pppppuVar8 = (undefined8 *****)0x0;
      if (local_310 != (undefined8 ******)0x0) {
        pppppuVar8 = local_310[1];
        local_310[1] = (undefined8 *****)((long)pppppuVar8 + 1);
      }
      FUN_04112ab8(pppppuVar8,pppppppuVar15 + 0xb,auStack_308);
      pppppppuVar15[0x1c] = ppppppplVar16;
      pppppppuVar15[0x1d] = ppppppplVar25;
      if (ppppppplVar25 != (long *******)0x0) {
        ppppppplVar25[1] = (long ******)((long)ppppppplVar25[1] + 1);
      }
      local_230 = pppppppuVar15;
      FUN_04b7141c(&local_4d0,&local_230,0,0);
      FUN_00033d2c(&local_230);
      if (ppppppplVar25 != (long *******)0x0) {
        LOAcquire();
        pppppplVar7 = ppppppplVar25[1];
        ppppppplVar25[1] = (long ******)((long)pppppplVar7 + -1);
        LORelease();
        if (pppppplVar7 == (long ******)0x0) {
          (*(code *)(*ppppppplVar25)[2])(ppppppplVar25);
          __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar25);
        }
      }
      ppppppplVar16 = ppppppplStack_138;
      local_1e0 = local_140;
      local_1d8 = ppppppplStack_138;
      if ((ppppppplStack_138 != (long *******)0x0) &&
         (ppppppplStack_138[1] = (long ******)((long)ppppppplStack_138[1] + 1),
         ppppppplStack_138 != (long *******)0x0)) {
        LOAcquire();
        pppppplVar7 = ppppppplStack_138[1];
        ppppppplStack_138[1] = (long ******)((long)pppppplVar7 + -1);
        LORelease();
        if (pppppplVar7 == (long ******)0x0) {
          (*(code *)(*ppppppplStack_138)[2])(ppppppplStack_138);
          __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar16);
        }
      }
      local_4d0 = local_1e0;
      ppppppplStack_4c8 = local_1d8;
      pppppplVar7 = (long ******)0x0;
      if (local_1d8 != (long *******)0x0) {
        pppppplVar7 = local_1d8[1];
        local_1d8[1] = (long ******)((long)pppppplVar7 + 1);
      }
      local_4c0 = (undefined1 *)0x0;
      FUN_066856fc(pppppplVar7,&local_4d0);
      FUN_0666a844(local_4d0);
      ppppppplVar16 = ppppppplStack_4c8;
      if (ppppppplStack_4c8 != (long *******)0x0) {
        LOAcquire();
        pppppplVar7 = ppppppplStack_4c8[1];
        ppppppplStack_4c8[1] = (long ******)((long)pppppplVar7 + -1);
        LORelease();
        if (pppppplVar7 == (long ******)0x0) {
          (*(code *)(*ppppppplStack_4c8)[2])(ppppppplStack_4c8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar16);
        }
      }
      ppppppplVar16 = local_1d8;
      if (local_1d8 != (long *******)0x0) {
        LOAcquire();
        pppppplVar7 = local_1d8[1];
        local_1d8[1] = (long ******)((long)pppppplVar7 + -1);
        LORelease();
        if (pppppplVar7 == (long ******)0x0) {
          (*(code *)(*local_1d8)[2])(local_1d8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar16);
        }
      }
      FUN_0236d3c4(&local_338);
      FUN_0473e440();
      plVar2 = local_3d8;
      goto joined_r0x0410f924;
    }
    iVar10 = thunk_FUN_05e1d97c(3);
    if (iVar10 != 0) {
      FUN_0488143c(&local_190);
      ppppppplVar16 = local_190;
      if (-1 < cStack_179) {
        ppppppplVar16 = (long *******)&local_190;
      }
      if ((DAT_0a43e621 & 1) == 0) {
        uRam000000000a43e618._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[8];
        uRam000000000a43e618._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[9];
        uRam000000000a43e618._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[10];
        uRam000000000a43e618._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xb];
        uRam000000000a43e618._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xc];
        uRam000000000a43e618._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xd];
        uRam000000000a43e618._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xe];
        uRam000000000a43e618._7_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xf];
        DAT_0a43e610 = s_login_service_ccGetAutoLoginInfo_089be4f0[0];
        DAT_0a43e610_1._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[1];
        DAT_0a43e610_1._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[2];
        DAT_0a43e610_1._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[3];
        DAT_0a43e610_1._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[4];
        DAT_0a43e610_1._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[5];
        DAT_0a43e610_1._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[6];
        DAT_0a43e610_1._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[7];
        DAT_0a43e620 = 0;
        DAT_0a43e621 = 1;
      }
      if ((DAT_0a43e903 & 1) == 0) {
        DAT_0a43e8f8._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
        DAT_0a43e8f8._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
        DAT_0a43e8f8._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
        DAT_0a43e8f8._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
        DAT_0a43e8f8._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
        DAT_0a43e8f8._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
        DAT_0a43e8f8._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
        DAT_0a43e8f8._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
        DAT_0a43e900 = 0x2928;
        DAT_0a43e902 = 0;
        DAT_0a43e903 = 1;
      }
      FUN_05e1d050(&local_4d0,3,ppppppplVar16,&DAT_0a43e610,&DAT_0a43e8f8,0x1a5,0,0);
      if ((DAT_0a43e9af & 1) == 0) {
        uVar18 = 0;
        do {
          (&DAT_0a43e966)[uVar18] = (&DAT_089bf57e)[uVar18] + 0x8a ^ (&DAT_089bf56e)[uVar18 & 0xf];
          uVar18 = uVar18 + 1;
        } while (uVar18 != 0x49);
        DAT_0a43e9af = 1;
      }
      puStack_d8 = (undefined1 *)0x0;
      uStack_e0 = 0;
      uStack_dc = 0;
      uStack_c8 = 0;
      cStack_c1 = '\0';
      local_d0 = (undefined1 *)0x0;
      puStack_f8 = (undefined1 *)0x0;
      puStack_100 = (undefined1 *)0x0;
      uStack_e8 = 0;
      uStack_e4 = 0;
      local_f0 = 0;
      cStack_e9 = '\0';
      puStack_118 = (undefined1 *)0x0;
      uStack_120 = 0;
      uStack_11f = 0;
      puStack_108 = (undefined1 *)0x0;
      puStack_110 = (undefined1 *)0x0;
      ppppppplStack_138 = (long *******)0x0;
      local_140 = (long *******)0x0;
      uStack_128 = 0;
      cStack_121 = '\0';
      local_130 = (undefined8 *******)0x0;
      FUN_05e1d31c(&local_4d0,&DAT_0a43e966,&local_140);
      thunk_FUN_05e1d0bc(&local_4d0);
      if (cStack_179 < '\0') {
        __ZdlPvm(local_190,CONCAT17(cStack_179,local_180) & 0x7fffffffffffffff);
      }
    }
    if ((DAT_0a43e903 & 1) == 0) {
      DAT_0a43e8f8._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
      DAT_0a43e8f8._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
      DAT_0a43e8f8._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
      DAT_0a43e8f8._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
      DAT_0a43e8f8._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
      DAT_0a43e8f8._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
      DAT_0a43e8f8._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
      DAT_0a43e8f8._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
      DAT_0a43e900 = 0x2928;
      DAT_0a43e902 = 0;
      DAT_0a43e903 = 1;
    }
    if ((DAT_0a43e6d6 & 1) == 0) {
      uVar18 = 0;
      do {
        (&DAT_0a43e67b)[uVar18] = (&DAT_089bee1d)[uVar18] + 0x8a ^ (&DAT_089bee0d)[uVar18 & 0xf];
        uVar18 = uVar18 + 1;
      } while (uVar18 != 0x5b);
      DAT_0a43e6d6 = 1;
    }
    FUN_0003bb6c(&local_4d0,&DAT_0a43e8f8,&DAT_0a43e67b,0x1a6);
    lVar6 = __Znwm(0xb0);
    FUN_00033c40(lVar6,FUN_04111af0,FUN_04111f10);
    FUN_04112ab8(lVar6 + 0x28,param_1 + 0x1c);
    local_3e8 = lVar6;
    FUN_04b7141c(&local_4d0,&local_3e8,0,0);
    FUN_00033d2c(&local_3e8);
    uStack_11f = 0xaaaaaaaaaaaaaa;
    uStack_128 = 0xaaaaaaaaaaaaaa;
    puStack_118 = &SUB_aaaaaaaaaaaaaaaa;
    uStack_bf = 0xaaaaaaaaaaaaaa;
    uStack_c8 = 0xaaaaaaaaaaaaaa;
    local_d0 = &SUB_aaaaaaaaaaaaaaaa;
    local_b8 = &SUB_aaaaaaaaaaaaaaaa;
    local_130 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
    uStack_dc = 0xaaaaaaaa;
    local_f0 = 0xaaaaaaaaaaaaaa;
    puStack_f8 = &SUB_aaaaaaaaaaaaaaaa;
    cStack_121 = '\0';
    uStack_120 = 0;
    puStack_110 = &SUB_aaaaaaaaaaaaaa;
    puStack_108 = &DAT_aaaaaaaa00000000;
    puStack_100 = &DAT_aaaaaaaaaaaaaa00;
    cStack_c1 = '\0';
    uStack_c0 = 0;
    puStack_d8 = &DAT_aaaaaaaaaaaaaa00;
    puStack_b0 = &SUB_aaaaaaaaaaaaaa;
    local_a8 = &DAT_aaaaaaaa00000000;
    local_140 = (long *******)0x0;
    ppppppplStack_138 = (long *******)&DAT_aaaaaaaaaaaaaa00;
    uStack_e0 = 0;
    cStack_e9 = '\0';
    uStack_e8 = 0;
    uStack_e4 = 0;
    uVar13 = FUN_04e04488();
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
              (&ppppppplStack_138,uVar13);
    uStack_4a7 = 0xaaaaaaaaaaaaaa;
    local_4b0 = 0xaaaaaaaaaaaaaa;
    local_4a0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_440 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_3f8 = &SUB_aaaaaaaaaaaaaaaa;
    uStack_464 = 0xaaaaaaaa;
    puStack_458 = &SUB_aaaaaaaaaaaaaaaa;
    uStack_478 = 0xaaaaaaaaaaaaaa;
    local_480 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
    local_4b8 = &SUB_aaaaaaaaaaaaaaaa;
    uStack_4a9 = 0;
    uStack_4a8 = 0;
    puStack_498 = &SUB_aaaaaaaaaaaaaa;
    local_490 = &DAT_aaaaaaaa00000000;
    puStack_488 = &DAT_aaaaaaaaaaaaaa00;
    local_450 = &SUB_aaaaaaaaaaaaaa;
    local_460 = &DAT_aaaaaaaaaaaaaa00;
    puStack_438 = &SUB_aaaaaaaaaaaaaa;
    puStack_448 = &DAT_aaaaaaaaaaaaaa00;
    local_430 = &DAT_aaaaaaaa00000000;
    local_4c0 = &DAT_aaaaaaaaaaaaaa00;
    uStack_468 = 0;
    local_471 = 0;
    uStack_470 = 0;
    uStack_46c = 0;
    local_3f0 = 0;
    uStack_400 = 0;
    uStack_408 = 0;
    local_410 = 0;
    uStack_418 = 0;
    uStack_420 = 0;
    uStack_428 = 0;
    local_4d0 = (long *******)0xaaaaaaaa00000006;
    ppppppplStack_4c8 = local_140;
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&local_4c0,&ppppppplStack_138);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&uStack_4a8,&uStack_120);
    local_490 = (undefined1 *)CONCAT44(local_490._4_4_,puStack_108._0_4_);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&puStack_488,&puStack_100);
    uStack_470 = uStack_e8;
    uStack_46c = uStack_e4;
    uStack_468 = uStack_e0;
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(&local_460,&puStack_d8)
    ;
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&puStack_448,&uStack_c0);
    local_430 = (undefined1 *)CONCAT44(local_430._4_4_,local_a8._0_4_);
    FUN_04669774();
    FUN_046728d0(&local_1e0);
    FUN_03016948(&local_190,local_1e0);
    FUN_02fc5d68(local_190,&local_4d0);
LAB_0410fcb8:
    ppppppplVar16 = local_188;
    if (local_188 != (long *******)0x0) {
      LOAcquire();
      pppppplVar7 = local_188[1];
      local_188[1] = (long ******)((long)pppppplVar7 + -1);
      LORelease();
      if (pppppplVar7 == (long ******)0x0) {
        (*(code *)(*local_188)[2])(local_188);
        __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar16);
      }
    }
    ppppppplVar16 = local_1d8;
    if (local_1d8 != (long *******)0x0) {
      LOAcquire();
      pppppplVar7 = local_1d8[1];
      local_1d8[1] = (long ******)((long)pppppplVar7 + -1);
      LORelease();
      if (pppppplVar7 == (long ******)0x0) {
        (*(code *)(*local_1d8)[2])(local_1d8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar16);
      }
    }
    FUN_002c6a5c(&local_4d0);
    if ((long)puStack_b0 < 0) {
      __ZdlPvm(CONCAT71(uStack_bf,uStack_c0),(ulong)puStack_b0 & 0x7fffffffffffffff);
    }
    if (cStack_c1 < '\0') {
      __ZdlPvm(puStack_d8,CONCAT17(cStack_c1,uStack_c8) & 0x7fffffffffffffff);
    }
    if (cStack_e9 < '\0') {
      __ZdlPvm(puStack_100,CONCAT17(cStack_e9,local_f0) & 0x7fffffffffffffff);
    }
    if ((long)puStack_110 < 0) {
      __ZdlPvm(CONCAT71(uStack_11f,uStack_120),(ulong)puStack_110 & 0x7fffffffffffffff);
    }
    plVar2 = local_3d8;
    if (cStack_121 < '\0') {
      __ZdlPvm(ppppppplStack_138,CONCAT17(cStack_121,uStack_128) & 0x7fffffffffffffff);
      plVar2 = local_3d8;
    }
  }
  else {
    if (*(char *)((long)local_390 + 4) == '\0') goto LAB_0410dff8;
LAB_0410e170:
    if ((DAT_0a43e903 & 1) == 0) {
      DAT_0a43e8f8._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
      DAT_0a43e8f8._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
      DAT_0a43e8f8._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
      DAT_0a43e8f8._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
      DAT_0a43e8f8._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
      DAT_0a43e8f8._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
      DAT_0a43e8f8._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
      DAT_0a43e8f8._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
      DAT_0a43e900 = 0x2928;
      DAT_0a43e902 = 0;
      DAT_0a43e903 = 1;
    }
    if ((DAT_0a43e6d6 & 1) == 0) {
      uVar18 = 0;
      do {
        (&DAT_0a43e67b)[uVar18] = (&DAT_089bee1d)[uVar18] + 0x8a ^ (&DAT_089bee0d)[uVar18 & 0xf];
        uVar18 = uVar18 + 1;
      } while (uVar18 != 0x5b);
      DAT_0a43e6d6 = 1;
    }
    FUN_0003bb6c(&local_4d0,&DAT_0a43e8f8,&DAT_0a43e67b,0x1ba);
    lVar6 = __Znwm(0x30);
    FUN_00033c40(lVar6,FUN_002cd8a4,FUN_0005f488);
    *(code **)(lVar6 + 0x20) = FUN_0411070c;
    local_4d8 = lVar6;
    FUN_04b6ee84(&local_4d0,&local_4d8);
    uVar13 = FUN_00033d2c(&local_4d8);
    if (*param_1 == 0) {
      FUN_04102784(uVar13,&local_380);
    }
    FUN_0466aca8(&local_4d0);
    uVar18 = FUN_0454e944(local_4d0);
    ppppppplVar16 = ppppppplStack_4c8;
    if (ppppppplStack_4c8 == (long *******)0x0) {
LAB_0410e298:
      if ((uVar18 & 1) != 0) goto LAB_0410e29c;
LAB_0410ea5c:
      uVar24 = 1;
    }
    else {
      LOAcquire();
      pppppplVar7 = ppppppplStack_4c8[1];
      ppppppplStack_4c8[1] = (long ******)((long)pppppplVar7 + -1);
      LORelease();
      if (pppppplVar7 != (long ******)0x0) goto LAB_0410e298;
      (*(code *)(*ppppppplStack_4c8)[2])(ppppppplStack_4c8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar16);
      if ((uVar18 & 1) == 0) goto LAB_0410ea5c;
LAB_0410e29c:
      if ((DAT_0a43e903 & 1) == 0) {
        DAT_0a43e8f8._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
        DAT_0a43e8f8._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
        DAT_0a43e8f8._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
        DAT_0a43e8f8._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
        DAT_0a43e8f8._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
        DAT_0a43e8f8._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
        DAT_0a43e8f8._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
        DAT_0a43e8f8._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
        DAT_0a43e900 = 0x2928;
        DAT_0a43e902 = 0;
        DAT_0a43e903 = 1;
      }
      if ((DAT_0a43e6d6 & 1) == 0) {
        uVar18 = 0;
        do {
          (&DAT_0a43e67b)[uVar18] = (&DAT_089bee1d)[uVar18] + 0x8a ^ (&DAT_089bee0d)[uVar18 & 0xf];
          uVar18 = uVar18 + 1;
        } while (uVar18 != 0x5b);
        DAT_0a43e6d6 = 1;
      }
      FUN_0003bb6c(&local_4d0,&DAT_0a43e8f8,&DAT_0a43e67b,0x1cd);
      lVar6 = __Znwm(0xe0);
      FUN_00033c40(lVar6,FUN_04111ffc,FUN_04112478);
      *(long ********)(lVar6 + 0x28) = local_3b0;
      if ((long)local_398 < 0) {
        FUN_00018d20(lVar6 + 0x30,uStack_3a8,uStack_3a0);
      }
      else {
        uVar13 = *puVar22;
        *(undefined8 *)(lVar6 + 0x38) = puVar22[1];
        *(undefined8 *)(lVar6 + 0x30) = uVar13;
        *(undefined8 *)(lVar6 + 0x40) = puVar22[2];
      }
      *(undefined8 *******)(lVar6 + 0x48) = local_390;
      *(undefined8 *******)(lVar6 + 0x50) = ppppppuStack_388;
      pppppuVar8 = (undefined8 *****)0x0;
      if (ppppppuStack_388 != (undefined8 ******)0x0) {
        pppppuVar8 = ppppppuStack_388[1];
        ppppppuStack_388[1] = (undefined8 *****)((long)pppppuVar8 + 1);
      }
      FUN_04112ab8(pppppuVar8,lVar6 + 0x58,param_1 + 0x1c);
      local_4e0 = lVar6;
      FUN_04b7141c(&local_4d0,&local_4e0,0,0);
      FUN_00033d2c(&local_4e0);
      FUN_04669774();
      iVar10 = FUN_046728ec();
      if (iVar10 == -1) {
        iVar10 = thunk_FUN_05e1d97c(4);
        if (iVar10 != 0) {
          FUN_0488143c(&local_190);
          ppppppplVar16 = local_190;
          if (-1 < cStack_179) {
            ppppppplVar16 = (long *******)&local_190;
          }
          if ((DAT_0a43e621 & 1) == 0) {
            uRam000000000a43e618._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[8];
            uRam000000000a43e618._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[9];
            uRam000000000a43e618._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[10];
            uRam000000000a43e618._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xb];
            uRam000000000a43e618._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xc];
            uRam000000000a43e618._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xd];
            uRam000000000a43e618._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xe];
            uRam000000000a43e618._7_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xf];
            DAT_0a43e610 = s_login_service_ccGetAutoLoginInfo_089be4f0[0];
            DAT_0a43e610_1._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[1];
            DAT_0a43e610_1._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[2];
            DAT_0a43e610_1._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[3];
            DAT_0a43e610_1._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[4];
            DAT_0a43e610_1._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[5];
            DAT_0a43e610_1._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[6];
            DAT_0a43e610_1._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[7];
            DAT_0a43e620 = 0;
            DAT_0a43e621 = 1;
          }
          if ((DAT_0a43e903 & 1) == 0) {
            DAT_0a43e8f8._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
            DAT_0a43e8f8._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
            DAT_0a43e8f8._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
            DAT_0a43e8f8._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
            DAT_0a43e8f8._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
            DAT_0a43e8f8._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
            DAT_0a43e8f8._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
            DAT_0a43e8f8._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
            DAT_0a43e900 = 0x2928;
            DAT_0a43e902 = 0;
            DAT_0a43e903 = 1;
          }
          FUN_05e1d050(&local_4d0,4,ppppppplVar16,&DAT_0a43e610,&DAT_0a43e8f8,0x1da,0,0);
          if ((DAT_0a43e9d5 & 1) == 0) {
            uVar18 = 0;
            do {
              (&DAT_0a43e9b0)[uVar18] =
                   (&DAT_089bf5d7)[uVar18] + 0x8a ^ (&DAT_089bf5c7)[uVar18 & 0xf];
              uVar18 = uVar18 + 1;
            } while (uVar18 != 0x25);
            DAT_0a43e9d5 = 1;
          }
          puStack_d8 = (undefined1 *)0x0;
          uStack_e0 = 0;
          uStack_dc = 0;
          uStack_c8 = 0;
          cStack_c1 = '\0';
          local_d0 = (undefined1 *)0x0;
          puStack_f8 = (undefined1 *)0x0;
          puStack_100 = (undefined1 *)0x0;
          uStack_e8 = 0;
          uStack_e4 = 0;
          local_f0 = 0;
          cStack_e9 = '\0';
          puStack_118 = (undefined1 *)0x0;
          uStack_120 = 0;
          uStack_11f = 0;
          puStack_108 = (undefined1 *)0x0;
          puStack_110 = (undefined1 *)0x0;
          ppppppplStack_138 = (long *******)0x0;
          local_140 = (long *******)0x0;
          uStack_128 = 0;
          cStack_121 = '\0';
          local_130 = (undefined8 *******)0x0;
          FUN_05e1d31c(&local_4d0,&DAT_0a43e9b0,&local_140);
          thunk_FUN_05e1d0bc(&local_4d0);
          if (cStack_179 < '\0') {
            __ZdlPvm(local_190,CONCAT17(cStack_179,local_180) & 0x7fffffffffffffff);
          }
        }
        if ((DAT_0a43e903 & 1) == 0) {
          DAT_0a43e8f8._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
          DAT_0a43e8f8._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
          DAT_0a43e8f8._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
          DAT_0a43e8f8._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
          DAT_0a43e8f8._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
          DAT_0a43e8f8._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
          DAT_0a43e8f8._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
          DAT_0a43e8f8._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
          DAT_0a43e900 = 0x2928;
          DAT_0a43e902 = 0;
          DAT_0a43e903 = 1;
        }
        if ((DAT_0a43e6d6 & 1) == 0) {
          uVar18 = 0;
          do {
            (&DAT_0a43e67b)[uVar18] = (&DAT_089bee1d)[uVar18] + 0x8a ^ (&DAT_089bee0d)[uVar18 & 0xf]
            ;
            uVar18 = uVar18 + 1;
          } while (uVar18 != 0x5b);
          DAT_0a43e6d6 = 1;
        }
        FUN_0003bb6c(&local_4d0,&DAT_0a43e8f8,&DAT_0a43e67b,0x1db);
        lVar6 = __Znwm(0xb0);
        FUN_00033c40(lVar6,FUN_041124ac,FUN_041124b4);
        FUN_04112ab8(lVar6 + 0x28,param_1 + 0x1c);
        local_4e8 = lVar6;
        FUN_04b7141c(&local_4d0,&local_4e8,0,0);
        FUN_00033d2c(&local_4e8);
        uStack_11f = 0xaaaaaaaaaaaaaa;
        uStack_128 = 0xaaaaaaaaaaaaaa;
        puStack_118 = &SUB_aaaaaaaaaaaaaaaa;
        uStack_bf = 0xaaaaaaaaaaaaaa;
        uStack_c8 = 0xaaaaaaaaaaaaaa;
        local_d0 = &SUB_aaaaaaaaaaaaaaaa;
        local_b8 = &SUB_aaaaaaaaaaaaaaaa;
        local_130 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
        uStack_dc = 0xaaaaaaaa;
        local_f0 = 0xaaaaaaaaaaaaaa;
        puStack_f8 = &SUB_aaaaaaaaaaaaaaaa;
        cStack_121 = '\0';
        uStack_120 = 0;
        puStack_110 = &SUB_aaaaaaaaaaaaaa;
        puStack_108 = &DAT_aaaaaaaa00000000;
        puStack_100 = &DAT_aaaaaaaaaaaaaa00;
        cStack_c1 = '\0';
        uStack_c0 = 0;
        puStack_d8 = &DAT_aaaaaaaaaaaaaa00;
        puStack_b0 = &SUB_aaaaaaaaaaaaaa;
        local_a8 = &DAT_aaaaaaaa00000000;
        local_140 = (long *******)0x0;
        ppppppplStack_138 = (long *******)&DAT_aaaaaaaaaaaaaa00;
        uStack_e0 = 0;
        cStack_e9 = '\0';
        uStack_e8 = 0;
        uStack_e4 = 0;
        uVar13 = FUN_04e04428();
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
                  (&ppppppplStack_138,uVar13);
        uStack_4a7 = 0xaaaaaaaaaaaaaa;
        local_4b0 = 0xaaaaaaaaaaaaaa;
        local_4a0 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_440 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_3f8 = &SUB_aaaaaaaaaaaaaaaa;
        uStack_464 = 0xaaaaaaaa;
        puStack_458 = &SUB_aaaaaaaaaaaaaaaa;
        uStack_478 = 0xaaaaaaaaaaaaaa;
        local_480 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
        local_4b8 = &SUB_aaaaaaaaaaaaaaaa;
        uStack_4a9 = 0;
        uStack_4a8 = 0;
        puStack_498 = &SUB_aaaaaaaaaaaaaa;
        local_490 = &DAT_aaaaaaaa00000000;
        puStack_488 = &DAT_aaaaaaaaaaaaaa00;
        local_450 = &SUB_aaaaaaaaaaaaaa;
        local_460 = &DAT_aaaaaaaaaaaaaa00;
        puStack_438 = &SUB_aaaaaaaaaaaaaa;
        puStack_448 = &DAT_aaaaaaaaaaaaaa00;
        local_430 = &DAT_aaaaaaaa00000000;
        local_4c0 = &DAT_aaaaaaaaaaaaaa00;
        uStack_468 = 0;
        local_471 = 0;
        uStack_470 = 0;
        uStack_46c = 0;
        local_3f0 = 0;
        uStack_400 = 0;
        uStack_408 = 0;
        local_410 = 0;
        uStack_418 = 0;
        uStack_420 = 0;
        uStack_428 = 0;
        local_4d0 = (long *******)0xaaaaaaaa00000006;
        ppppppplStack_4c8 = local_140;
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (&local_4c0,&ppppppplStack_138);
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (&uStack_4a8,&uStack_120);
        local_490 = (undefined1 *)CONCAT44(local_490._4_4_,puStack_108._0_4_);
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (&puStack_488,&puStack_100);
        uStack_470 = uStack_e8;
        uStack_46c = uStack_e4;
        uStack_468 = uStack_e0;
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (&local_460,&puStack_d8);
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (&puStack_448,&uStack_c0);
        local_430 = (undefined1 *)CONCAT44(local_430._4_4_,local_a8._0_4_);
        FUN_04669774();
        FUN_046728d0(&local_1e0);
        FUN_03016948(&local_190,local_1e0);
        FUN_02fc5d68(local_190,&local_4d0);
        goto LAB_0410fcb8;
      }
      uVar24 = (uint)(iVar10 == 0);
    }
    bVar5 = local_380._4_1_;
    local_4f8 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_4f0 = &SUB_aaaaaaaaaaaaaaaa;
    local_500 = &SUB_aaaaaaaaaaaaaaaa;
    FUN_0466aca8(&local_4d0);
    local_140 = (long *******)CONCAT44(local_140._4_4_,2);
    FUN_045513b4(&local_500,local_4d0,&local_140);
    ppppppplVar16 = ppppppplStack_4c8;
    if (ppppppplStack_4c8 != (long *******)0x0) {
      LOAcquire();
      pppppplVar7 = ppppppplStack_4c8[1];
      ppppppplStack_4c8[1] = (long ******)((long)pppppplVar7 + -1);
      LORelease();
      if (pppppplVar7 == (long ******)0x0) {
        (*(code *)(*ppppppplStack_4c8)[2])(ppppppplStack_4c8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar16);
      }
    }
    local_510 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_508 = &SUB_aaaaaaaaaaaaaaaa;
    local_518 = &SUB_aaaaaaaaaaaaaaaa;
    FUN_0002c368(&local_4d0,&local_500,"contact",7);
    FUN_0002c368(&local_518,&local_4d0,"contact.db",10);
    FUN_0002b440(&local_4d0);
    uVar11 = thunk_FUN_000311e8(&local_518);
    iVar10 = thunk_FUN_05e1d97c(2);
    if (iVar10 != 0) {
      FUN_0488143c(local_530);
      pppppppuVar15 = local_530[0];
      if (-1 < cStack_519) {
        pppppppuVar15 = local_530;
      }
      if ((DAT_0a43e621 & 1) == 0) {
        uRam000000000a43e618._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[8];
        uRam000000000a43e618._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[9];
        uRam000000000a43e618._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[10];
        uRam000000000a43e618._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xb];
        uRam000000000a43e618._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xc];
        uRam000000000a43e618._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xd];
        uRam000000000a43e618._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xe];
        uRam000000000a43e618._7_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xf];
        DAT_0a43e610 = s_login_service_ccGetAutoLoginInfo_089be4f0[0];
        DAT_0a43e610_1._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[1];
        DAT_0a43e610_1._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[2];
        DAT_0a43e610_1._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[3];
        DAT_0a43e610_1._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[4];
        DAT_0a43e610_1._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[5];
        DAT_0a43e610_1._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[6];
        DAT_0a43e610_1._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[7];
        DAT_0a43e620 = 0;
        DAT_0a43e621 = 1;
      }
      if ((DAT_0a43e903 & 1) == 0) {
        DAT_0a43e8f8._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
        DAT_0a43e8f8._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
        DAT_0a43e8f8._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
        DAT_0a43e8f8._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
        DAT_0a43e8f8._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
        DAT_0a43e8f8._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
        DAT_0a43e8f8._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
        DAT_0a43e8f8._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
        DAT_0a43e900 = 0x2928;
        DAT_0a43e902 = 0;
        DAT_0a43e903 = 1;
      }
      FUN_05e1d050(&local_4d0,2,pppppppuVar15,&DAT_0a43e610,&DAT_0a43e8f8,0x1f6,0,0);
      FUN_04980e70(local_548,param_1 + 2);
      local_190 = local_548[0];
      if (-1 < cStack_531) {
        local_190 = (long *******)local_548;
      }
      local_188 = (long *******)((ulong)local_188 & 0xffffffffffffff00);
      if (uVar11 == 0) {
        local_1e0 = (long *******)&DAT_0a43e884;
        if ((DAT_0a43e88a & 1) == 0) {
          DAT_0a43e884 = (undefined4)DAT_0847fe48;
          puVar9 = &DAT_0a43e888;
          puVar19 = &DAT_0a43e889;
          puVar20 = &DAT_0a43e88a;
          goto LAB_0410ecbc;
        }
      }
      else {
        local_1e0 = (long *******)&DAT_0a43e87c;
        if ((DAT_0a43e881 & 1) == 0) {
          DAT_0a43e87c = 0x7274;
          DAT_0a43e87e = 0x75;
          puVar19 = &DAT_0a43e880;
          puVar9 = &DAT_0a43e87f;
          puVar20 = &DAT_0a43e881;
LAB_0410ecbc:
          *puVar9 = 0x65;
          *puVar19 = 0;
          *puVar20 = 1;
        }
      }
      local_1d8 = (long *******)((ulong)local_1d8 & 0xffffffffffffff00);
      if (bVar5 == 0) {
        local_230 = (undefined8 *******)&DAT_0a43e884;
        if ((DAT_0a43e88a & 1) == 0) {
          DAT_0a43e884 = (undefined4)DAT_0847fe48;
          puVar9 = &DAT_0a43e888;
          puVar19 = &DAT_0a43e889;
          puVar20 = &DAT_0a43e88a;
          goto LAB_0410ed44;
        }
      }
      else {
        local_230 = (undefined8 *******)&DAT_0a43e87c;
        if ((DAT_0a43e881 & 1) == 0) {
          DAT_0a43e87c = 0x7274;
          DAT_0a43e87e = 0x75;
          puVar19 = &DAT_0a43e880;
          puVar9 = &DAT_0a43e87f;
          puVar20 = &DAT_0a43e881;
LAB_0410ed44:
          *puVar9 = 0x65;
          *puVar19 = 0;
          *puVar20 = 1;
        }
      }
      local_228 = (long *)((ulong)local_228 & 0xffffffffffffff00);
      if (uVar24 == 0) {
        local_280 = &DAT_0a43e884;
        if ((DAT_0a43e88a & 1) == 0) {
          DAT_0a43e884 = (undefined4)DAT_0847fe48;
          puVar9 = &DAT_0a43e888;
          puVar19 = &DAT_0a43e889;
          puVar20 = &DAT_0a43e88a;
          goto LAB_0410edcc;
        }
      }
      else {
        local_280 = (undefined4 *)&DAT_0a43e87c;
        if ((DAT_0a43e881 & 1) == 0) {
          DAT_0a43e87c = 0x7274;
          DAT_0a43e87e = 0x75;
          puVar19 = &DAT_0a43e880;
          puVar9 = &DAT_0a43e87f;
          puVar20 = &DAT_0a43e881;
LAB_0410edcc:
          *puVar9 = 0x65;
          *puVar19 = 0;
          *puVar20 = 1;
        }
      }
      local_278 = 0;
      if ((DAT_0a43ea31 & 1) == 0) {
        uVar18 = 0;
        do {
          (&DAT_0a43e9d6)[uVar18] = (&DAT_089bf60c)[uVar18] + 0x8a ^ (&DAT_089bf5fc)[uVar18 & 0xf];
          uVar18 = uVar18 + 1;
        } while (uVar18 != 0x5b);
        DAT_0a43ea31 = 1;
      }
      local_140 = (long *******)&local_190;
      ppppppplStack_138 = (long *******)&local_1e0;
      local_130 = &local_230;
      uStack_128 = SUB87(&local_280,0);
      cStack_121 = (char)((ulong)&local_280 >> 0x38);
      puStack_118 = (undefined1 *)0x0;
      uStack_120 = 0;
      uStack_11f = 0;
      puStack_108 = (undefined1 *)0x0;
      puStack_110 = (undefined1 *)0x0;
      puStack_f8 = (undefined1 *)0x0;
      puStack_100 = (undefined1 *)0x0;
      uStack_e8 = 0;
      uStack_e4 = 0;
      local_f0 = 0;
      cStack_e9 = '\0';
      puStack_d8 = (undefined1 *)0x0;
      uStack_e0 = 0;
      uStack_dc = 0;
      uStack_c8 = 0;
      cStack_c1 = '\0';
      local_d0 = (undefined1 *)0x0;
      FUN_05e1d31c(&local_4d0,&DAT_0a43e9d6,&local_140);
      if (cStack_531 < '\0') {
        __ZdlPvm(local_548[0],CONCAT17(cStack_531,local_538) & 0x7fffffffffffffff);
      }
      thunk_FUN_05e1d0bc(&local_4d0);
      if (cStack_519 < '\0') {
        __ZdlPvm(local_530[0],CONCAT17(cStack_519,local_520) & 0x7fffffffffffffff);
      }
    }
    FUN_0002b440(&local_518);
    FUN_0002b440(&local_500);
    if ((((uint)bVar5 | uVar11 ^ 0xffffffff) & 1) == 0) {
      uVar11 = uVar24;
    }
    if ((uVar11 & 1) == 0) {
      iVar10 = thunk_FUN_05e1d97c(2);
      if (iVar10 != 0) {
        FUN_0488143c(&local_190);
        ppppppplVar16 = local_190;
        if (-1 < cStack_179) {
          ppppppplVar16 = (long *******)&local_190;
        }
        if ((DAT_0a43e621 & 1) == 0) {
          uRam000000000a43e618._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[8];
          uRam000000000a43e618._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[9];
          uRam000000000a43e618._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[10];
          uRam000000000a43e618._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xb];
          uRam000000000a43e618._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xc];
          uRam000000000a43e618._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xd];
          uRam000000000a43e618._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xe];
          uRam000000000a43e618._7_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xf];
          DAT_0a43e610 = s_login_service_ccGetAutoLoginInfo_089be4f0[0];
          DAT_0a43e610_1._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[1];
          DAT_0a43e610_1._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[2];
          DAT_0a43e610_1._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[3];
          DAT_0a43e610_1._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[4];
          DAT_0a43e610_1._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[5];
          DAT_0a43e610_1._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[6];
          DAT_0a43e610_1._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[7];
          DAT_0a43e620 = 0;
          DAT_0a43e621 = 1;
        }
        if ((DAT_0a43e903 & 1) == 0) {
          DAT_0a43e8f8._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
          DAT_0a43e8f8._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
          DAT_0a43e8f8._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
          DAT_0a43e8f8._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
          DAT_0a43e8f8._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
          DAT_0a43e8f8._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
          DAT_0a43e8f8._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
          DAT_0a43e8f8._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
          DAT_0a43e900 = 0x2928;
          DAT_0a43e902 = 0;
          DAT_0a43e903 = 1;
        }
        FUN_05e1d050(&local_4d0,2,ppppppplVar16,&DAT_0a43e610,&DAT_0a43e8f8,0x205,0,0);
        if ((DAT_0a43ea4a & 1) == 0) {
          uVar18 = 0;
          do {
            (&DAT_0a43ea32)[uVar18] = (&DAT_089bf677)[uVar18] + 0x8a ^ (&DAT_089bf667)[uVar18 & 0xf]
            ;
            uVar18 = uVar18 + 1;
          } while (uVar18 != 0x18);
          DAT_0a43ea4a = 1;
        }
        puStack_d8 = (undefined1 *)0x0;
        uStack_e0 = 0;
        uStack_dc = 0;
        uStack_c8 = 0;
        cStack_c1 = '\0';
        local_d0 = (undefined1 *)0x0;
        puStack_f8 = (undefined1 *)0x0;
        puStack_100 = (undefined1 *)0x0;
        uStack_e8 = 0;
        uStack_e4 = 0;
        local_f0 = 0;
        cStack_e9 = '\0';
        puStack_118 = (undefined1 *)0x0;
        uStack_120 = 0;
        uStack_11f = 0;
        puStack_108 = (undefined1 *)0x0;
        puStack_110 = (undefined1 *)0x0;
        ppppppplStack_138 = (long *******)0x0;
        local_140 = (long *******)0x0;
        uStack_128 = 0;
        cStack_121 = '\0';
        local_130 = (undefined8 *******)0x0;
        FUN_05e1d31c(&local_4d0,&DAT_0a43ea32,&local_140);
        thunk_FUN_05e1d0bc(&local_4d0);
        if (cStack_179 < '\0') {
          __ZdlPvm(local_190,CONCAT17(cStack_179,local_180) & 0x7fffffffffffffff);
        }
      }
LAB_0410f17c:
      uVar24 = 1;
    }
    else {
      uVar18 = FUN_03b2e8fc();
      if ((uVar18 & 1) == 0) {
        FUN_03b2db9c();
        goto LAB_0410f17c;
      }
      local_228 = (long *)&SUB_aaaaaaaaaaaaaaaa;
      local_230 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
      FUN_0467228c(&local_230);
      if (local_230 == (undefined8 *******)0x0) {
        iVar10 = thunk_FUN_05e1d97c(3);
        if (iVar10 != 0) {
          FUN_0488143c(&local_190);
          ppppppplVar16 = local_190;
          if (-1 < cStack_179) {
            ppppppplVar16 = (long *******)&local_190;
          }
          if ((DAT_0a43e621 & 1) == 0) {
            uRam000000000a43e618._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[8];
            uRam000000000a43e618._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[9];
            uRam000000000a43e618._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[10];
            uRam000000000a43e618._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xb];
            uRam000000000a43e618._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xc];
            uRam000000000a43e618._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xd];
            uRam000000000a43e618._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xe];
            uRam000000000a43e618._7_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xf];
            DAT_0a43e610 = s_login_service_ccGetAutoLoginInfo_089be4f0[0];
            DAT_0a43e610_1._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[1];
            DAT_0a43e610_1._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[2];
            DAT_0a43e610_1._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[3];
            DAT_0a43e610_1._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[4];
            DAT_0a43e610_1._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[5];
            DAT_0a43e610_1._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[6];
            DAT_0a43e610_1._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[7];
            DAT_0a43e620 = 0;
            DAT_0a43e621 = 1;
          }
          if ((DAT_0a43e903 & 1) == 0) {
            DAT_0a43e8f8._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
            DAT_0a43e8f8._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
            DAT_0a43e8f8._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
            DAT_0a43e8f8._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
            DAT_0a43e8f8._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
            DAT_0a43e8f8._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
            DAT_0a43e8f8._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
            DAT_0a43e8f8._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
            DAT_0a43e900 = 0x2928;
            DAT_0a43e902 = 0;
            DAT_0a43e903 = 1;
          }
          FUN_05e1d050(&local_4d0,3,ppppppplVar16,&DAT_0a43e610,&DAT_0a43e8f8,0x213,0,0);
          if ((DAT_0a43ea82 & 1) == 0) {
            uRam000000000a43ea78._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x38];
            uRam000000000a43ea78._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x39];
            uRam000000000a43ea78._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x3a];
            uRam000000000a43ea78._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x3b];
            uRam000000000a43ea78._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x3c];
            uRam000000000a43ea78._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x3d];
            uRam000000000a43ea78._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x3e];
            uRam000000000a43ea78._7_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x3f];
            DAT_0a43ea70 = s_login_service_ccGetAutoLoginInfo_089be4f0[0x30];
            DAT_0a43ea70_1._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x31];
            DAT_0a43ea70_1._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x32];
            DAT_0a43ea70_1._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x33];
            DAT_0a43ea70_1._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x34];
            DAT_0a43ea70_1._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x35];
            DAT_0a43ea70_1._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x36];
            DAT_0a43ea70_1._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x37];
            DAT_0a43ea80 = 0x76;
            DAT_0a43ea82 = 1;
          }
          puStack_d8 = (undefined1 *)0x0;
          uStack_e0 = 0;
          uStack_dc = 0;
          uStack_c8 = 0;
          cStack_c1 = '\0';
          local_d0 = (undefined1 *)0x0;
          puStack_f8 = (undefined1 *)0x0;
          puStack_100 = (undefined1 *)0x0;
          uStack_e8 = 0;
          uStack_e4 = 0;
          local_f0 = 0;
          cStack_e9 = '\0';
          puStack_118 = (undefined1 *)0x0;
          uStack_120 = 0;
          uStack_11f = 0;
          puStack_108 = (undefined1 *)0x0;
          puStack_110 = (undefined1 *)0x0;
          ppppppplStack_138 = (long *******)0x0;
          local_140 = (long *******)0x0;
          uStack_128 = 0;
          cStack_121 = '\0';
          local_130 = (undefined8 *******)0x0;
          FUN_05e1d31c(&local_4d0,&DAT_0a43ea70,&local_140);
          thunk_FUN_05e1d0bc(&local_4d0);
          if (cStack_179 < '\0') {
            __ZdlPvm(local_190,CONCAT17(cStack_179,local_180) & 0x7fffffffffffffff);
          }
        }
        uVar24 = 0;
      }
      else {
        FUN_0466aca8(&local_4d0);
        uVar11 = FUN_04556680(local_4d0);
        ppppppplVar16 = ppppppplStack_4c8;
        if (ppppppplStack_4c8 != (long *******)0x0) {
          LOAcquire();
          pppppplVar7 = ppppppplStack_4c8[1];
          ppppppplStack_4c8[1] = (long ******)((long)pppppplVar7 + -1);
          LORelease();
          if (pppppplVar7 == (long ******)0x0) {
            (*(code *)(*ppppppplStack_4c8)[2])(ppppppplStack_4c8);
            __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar16);
          }
        }
        iVar10 = thunk_FUN_05e1d97c(2);
        uVar24 = uVar11 ^ 1;
        if (iVar10 != 0) {
          FUN_0488143c(&local_1e0);
          ppppppplVar16 = local_1e0;
          if (-1 < cStack_1c9) {
            ppppppplVar16 = (long *******)&local_1e0;
          }
          if ((DAT_0a43e621 & 1) == 0) {
            uRam000000000a43e618._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[8];
            uRam000000000a43e618._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[9];
            uRam000000000a43e618._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[10];
            uRam000000000a43e618._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xb];
            uRam000000000a43e618._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xc];
            uRam000000000a43e618._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xd];
            uRam000000000a43e618._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xe];
            uRam000000000a43e618._7_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xf];
            DAT_0a43e610 = s_login_service_ccGetAutoLoginInfo_089be4f0[0];
            DAT_0a43e610_1._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[1];
            DAT_0a43e610_1._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[2];
            DAT_0a43e610_1._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[3];
            DAT_0a43e610_1._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[4];
            DAT_0a43e610_1._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[5];
            DAT_0a43e610_1._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[6];
            DAT_0a43e610_1._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[7];
            DAT_0a43e620 = 0;
            DAT_0a43e621 = 1;
          }
          if ((DAT_0a43e903 & 1) == 0) {
            DAT_0a43e8f8._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
            DAT_0a43e8f8._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
            DAT_0a43e8f8._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
            DAT_0a43e8f8._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
            DAT_0a43e8f8._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
            DAT_0a43e8f8._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
            DAT_0a43e8f8._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
            DAT_0a43e8f8._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
            DAT_0a43e900 = 0x2928;
            DAT_0a43e902 = 0;
            DAT_0a43e903 = 1;
          }
          FUN_05e1d050(&local_4d0,2,ppppppplVar16,&DAT_0a43e610,&DAT_0a43e8f8,0x211,0,0);
          if (uVar11 == 0) {
            local_190 = (long *******)&DAT_0a43e884;
            if ((DAT_0a43e88a & 1) == 0) {
              DAT_0a43e884 = (undefined4)DAT_0847fe48;
              puVar9 = &DAT_0a43e888;
              puVar19 = &DAT_0a43e889;
              puVar20 = &DAT_0a43e88a;
              goto LAB_0411001c;
            }
          }
          else {
            local_190 = (long *******)&DAT_0a43e87c;
            if ((DAT_0a43e881 & 1) == 0) {
              DAT_0a43e87c = 0x7274;
              DAT_0a43e87e = 0x75;
              puVar19 = &DAT_0a43e880;
              puVar9 = &DAT_0a43e87f;
              puVar20 = &DAT_0a43e881;
LAB_0411001c:
              *puVar9 = 0x65;
              *puVar19 = 0;
              *puVar20 = 1;
            }
          }
          local_188 = (long *******)((ulong)local_188 & 0xffffffffffffff00);
          if ((DAT_0a43ea62 & 1) == 0) {
            uRam000000000a43ea58._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x28];
            uRam000000000a43ea58._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x29];
            uRam000000000a43ea58._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x2a];
            uRam000000000a43ea58._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x2b];
            uRam000000000a43ea58._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x2c];
            uRam000000000a43ea58._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x2d];
            uRam000000000a43ea58._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x2e];
            uRam000000000a43ea58._7_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x2f];
            DAT_0a43ea50 = s_login_service_ccGetAutoLoginInfo_089be4f0[0x20];
            DAT_0a43ea50_1._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x21];
            DAT_0a43ea50_1._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x22];
            DAT_0a43ea50_1._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x23];
            DAT_0a43ea50_1._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x24];
            DAT_0a43ea50_1._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x25];
            DAT_0a43ea50_1._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x26];
            DAT_0a43ea50_1._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x27];
            DAT_0a43ea60 = 0x5f;
            DAT_0a43ea62 = 1;
          }
          local_130 = (undefined8 *******)0x0;
          ppppppplStack_138 = (long *******)0x0;
          local_140 = (long *******)&local_190;
          uStack_120 = 0;
          uStack_11f = 0;
          uStack_128 = 0;
          cStack_121 = '\0';
          puStack_110 = (undefined1 *)0x0;
          puStack_118 = (undefined1 *)0x0;
          puStack_100 = (undefined1 *)0x0;
          puStack_108 = (undefined1 *)0x0;
          local_f0 = 0;
          cStack_e9 = '\0';
          puStack_f8 = (undefined1 *)0x0;
          uStack_e0 = 0;
          uStack_dc = 0;
          uStack_e8 = 0;
          uStack_e4 = 0;
          local_d0 = (undefined1 *)0x0;
          puStack_d8 = (undefined1 *)0x0;
          uStack_c8 = 0;
          cStack_c1 = '\0';
          FUN_05e1d31c(&local_4d0,&DAT_0a43ea50,&local_140);
          thunk_FUN_05e1d0bc(&local_4d0);
          if (cStack_1c9 < '\0') {
            __ZdlPvm(local_1e0,CONCAT17(cStack_1c9,local_1d0) & 0x7fffffffffffffff);
          }
        }
      }
      plVar2 = local_228;
      if (local_228 != (long *)0x0) {
        LOAcquire();
        lVar6 = local_228[1];
        local_228[1] = lVar6 + -1;
        LORelease();
        if (lVar6 == 0) {
          (**(code **)(*local_228 + 0x10))(local_228);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
        }
      }
    }
    *(char *)((long)local_390 + 5) = (char)uVar24;
    iVar10 = thunk_FUN_05e1d97c(2);
    if (iVar10 == 0) {
LAB_0410f37c:
      if ((uVar24 & 1) != 0) goto LAB_0410f380;
LAB_0410f740:
      ppppppplVar16 = (long *******)__Znwm(0x20);
      ppppppplVar25 = ppppppplVar16 + 1;
      *ppppppplVar25 = (long ******)0x0;
      ppppppplVar16[2] = (long ******)0x0;
      *ppppppplVar16 = (long ******)&PTR_FUN_09e5b3b8;
      ppppppplVar26 = ppppppplVar16 + 3;
      *(undefined1 *)ppppppplVar26 = 0;
      local_4d0 = ppppppplVar26;
      ppppppplStack_4c8 = ppppppplVar16;
      uVar13 = FUN_04669774();
      if (ppppppplVar16 != (long *******)0x0) {
        *ppppppplVar25 = (long ******)((long)*ppppppplVar25 + 1);
      }
      local_558 = ppppppplVar26;
      local_550 = ppppppplVar16;
      FUN_04672de0(uVar13,&local_558);
      ppppppplVar16 = local_550;
      if (local_550 != (long *******)0x0) {
        LOAcquire();
        pppppplVar7 = local_550[1];
        local_550[1] = (long ******)((long)pppppplVar7 + -1);
        LORelease();
        if (pppppplVar7 == (long ******)0x0) {
          (*(code *)(*local_550)[2])(local_550);
          __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar16);
        }
      }
      ppppppplVar16 = ppppppplStack_4c8;
      if (ppppppplStack_4c8 != (long *******)0x0) {
        LOAcquire();
        pppppplVar7 = ppppppplStack_4c8[1];
        ppppppplStack_4c8[1] = (long ******)((long)pppppplVar7 + -1);
        LORelease();
        if (pppppplVar7 == (long ******)0x0) {
          (*(code *)(*ppppppplStack_4c8)[2])(ppppppplStack_4c8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar16);
        }
      }
    }
    else {
      FUN_0488143c(&local_230);
      pppppppuVar15 = local_230;
      if (-1 < cStack_219) {
        pppppppuVar15 = &local_230;
      }
      if ((DAT_0a43e621 & 1) == 0) {
        uRam000000000a43e618._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[8];
        uRam000000000a43e618._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[9];
        uRam000000000a43e618._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[10];
        uRam000000000a43e618._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xb];
        uRam000000000a43e618._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xc];
        uRam000000000a43e618._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xd];
        uRam000000000a43e618._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xe];
        uRam000000000a43e618._7_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xf];
        DAT_0a43e610 = s_login_service_ccGetAutoLoginInfo_089be4f0[0];
        DAT_0a43e610_1._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[1];
        DAT_0a43e610_1._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[2];
        DAT_0a43e610_1._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[3];
        DAT_0a43e610_1._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[4];
        DAT_0a43e610_1._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[5];
        DAT_0a43e610_1._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[6];
        DAT_0a43e610_1._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[7];
        DAT_0a43e620 = 0;
        DAT_0a43e621 = 1;
      }
      if ((DAT_0a43e903 & 1) == 0) {
        DAT_0a43e8f8._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
        DAT_0a43e8f8._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
        DAT_0a43e8f8._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
        DAT_0a43e8f8._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
        DAT_0a43e8f8._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
        DAT_0a43e8f8._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
        DAT_0a43e8f8._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
        DAT_0a43e8f8._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
        DAT_0a43e900 = 0x2928;
        DAT_0a43e902 = 0;
        DAT_0a43e903 = 1;
      }
      FUN_05e1d050(&local_4d0,2,pppppppuVar15,&DAT_0a43e610,&DAT_0a43e8f8,0x218,0,0);
      FUN_04669774();
      ppppppplVar16 = (long *******)FUN_04670680();
      local_190 = (long *******)*ppppppplVar16;
      if (-1 < *(char *)((long)ppppppplVar16 + 0x17)) {
        local_190 = ppppppplVar16;
      }
      local_188 = (long *******)((ulong)local_188 & 0xffffffffffffff00);
      if (uVar24 == 0) {
        local_1e0 = (long *******)&DAT_0a43e884;
        if ((DAT_0a43e88a & 1) == 0) {
          DAT_0a43e884 = (undefined4)DAT_0847fe48;
          puVar9 = &DAT_0a43e888;
          puVar19 = &DAT_0a43e889;
          puVar20 = &DAT_0a43e88a;
          goto LAB_0410f2c4;
        }
      }
      else {
        local_1e0 = (long *******)&DAT_0a43e87c;
        if ((DAT_0a43e881 & 1) == 0) {
          DAT_0a43e87c = 0x7274;
          DAT_0a43e87e = 0x75;
          puVar19 = &DAT_0a43e880;
          puVar9 = &DAT_0a43e87f;
          puVar20 = &DAT_0a43e881;
LAB_0410f2c4:
          *puVar9 = 0x65;
          *puVar19 = 0;
          *puVar20 = 1;
        }
      }
      local_1d8 = (long *******)((ulong)local_1d8 & 0xffffffffffffff00);
      if ((DAT_0a43eaaa & 1) == 0) {
        uVar18 = 0;
        do {
          (&DAT_0a43ea83)[uVar18] = (&DAT_089bf6e3)[uVar18] + 0x8a ^ (&DAT_089bf6d3)[uVar18 & 0xf];
          uVar18 = uVar18 + 1;
        } while (uVar18 != 0x27);
        DAT_0a43eaaa = 1;
      }
      local_140 = (long *******)&local_190;
      ppppppplStack_138 = (long *******)&local_1e0;
      uStack_128 = 0;
      cStack_121 = '\0';
      local_130 = (undefined8 *******)0x0;
      puStack_118 = (undefined1 *)0x0;
      uStack_120 = 0;
      uStack_11f = 0;
      puStack_108 = (undefined1 *)0x0;
      puStack_110 = (undefined1 *)0x0;
      puStack_f8 = (undefined1 *)0x0;
      puStack_100 = (undefined1 *)0x0;
      uStack_e8 = 0;
      uStack_e4 = 0;
      local_f0 = 0;
      cStack_e9 = '\0';
      puStack_d8 = (undefined1 *)0x0;
      uStack_e0 = 0;
      uStack_dc = 0;
      uStack_c8 = 0;
      cStack_c1 = '\0';
      local_d0 = (undefined1 *)0x0;
      FUN_05e1d31c(&local_4d0,&DAT_0a43ea83,&local_140);
      thunk_FUN_05e1d0bc(&local_4d0);
      if (-1 < cStack_219) goto LAB_0410f37c;
      __ZdlPvm(local_230,CONCAT17(cStack_219,local_220) & 0x7fffffffffffffff);
      if ((uVar24 & 1) == 0) goto LAB_0410f740;
LAB_0410f380:
      if (*param_1 == 1) {
        iVar10 = thunk_FUN_05e1d97c(4);
        if (iVar10 != 0) {
          FUN_0488143c(&local_190);
          ppppppplVar16 = local_190;
          if (-1 < cStack_179) {
            ppppppplVar16 = (long *******)&local_190;
          }
          if ((DAT_0a43e621 & 1) == 0) {
            uRam000000000a43e618._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[8];
            uRam000000000a43e618._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[9];
            uRam000000000a43e618._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[10];
            uRam000000000a43e618._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xb];
            uRam000000000a43e618._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xc];
            uRam000000000a43e618._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xd];
            uRam000000000a43e618._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xe];
            uRam000000000a43e618._7_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0xf];
            DAT_0a43e610 = s_login_service_ccGetAutoLoginInfo_089be4f0[0];
            DAT_0a43e610_1._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[1];
            DAT_0a43e610_1._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[2];
            DAT_0a43e610_1._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[3];
            DAT_0a43e610_1._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[4];
            DAT_0a43e610_1._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[5];
            DAT_0a43e610_1._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[6];
            DAT_0a43e610_1._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[7];
            DAT_0a43e620 = 0;
            DAT_0a43e621 = 1;
          }
          if ((DAT_0a43e903 & 1) == 0) {
            DAT_0a43e8f8._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
            DAT_0a43e8f8._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
            DAT_0a43e8f8._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
            DAT_0a43e8f8._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
            DAT_0a43e8f8._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
            DAT_0a43e8f8._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
            DAT_0a43e8f8._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
            DAT_0a43e8f8._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
            DAT_0a43e900 = 0x2928;
            DAT_0a43e902 = 0;
            DAT_0a43e903 = 1;
          }
          FUN_05e1d050(&local_4d0,4,ppppppplVar16,&DAT_0a43e610,&DAT_0a43e8f8,0x220,0,0);
          if ((DAT_0a43ead1 & 1) == 0) {
            uVar18 = 0;
            do {
              (&DAT_0a43eaab)[uVar18] =
                   (&DAT_089bf71a)[uVar18] + 0x8a ^ (&DAT_089bf70a)[uVar18 & 0xf];
              uVar18 = uVar18 + 1;
            } while (uVar18 != 0x26);
            DAT_0a43ead1 = 1;
          }
          puStack_d8 = (undefined1 *)0x0;
          uStack_e0 = 0;
          uStack_dc = 0;
          uStack_c8 = 0;
          cStack_c1 = '\0';
          local_d0 = (undefined1 *)0x0;
          puStack_f8 = (undefined1 *)0x0;
          puStack_100 = (undefined1 *)0x0;
          uStack_e8 = 0;
          uStack_e4 = 0;
          local_f0 = 0;
          cStack_e9 = '\0';
          puStack_118 = (undefined1 *)0x0;
          uStack_120 = 0;
          uStack_11f = 0;
          puStack_108 = (undefined1 *)0x0;
          puStack_110 = (undefined1 *)0x0;
          ppppppplStack_138 = (long *******)0x0;
          local_140 = (long *******)0x0;
          uStack_128 = 0;
          cStack_121 = '\0';
          local_130 = (undefined8 *******)0x0;
          FUN_05e1d31c(&local_4d0,&DAT_0a43eaab,&local_140);
          thunk_FUN_05e1d0bc(&local_4d0);
          if (cStack_179 < '\0') {
            __ZdlPvm(local_190,CONCAT17(cStack_179,local_180) & 0x7fffffffffffffff);
          }
        }
        if ((DAT_0a43e903 & 1) == 0) {
          DAT_0a43e8f8._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
          DAT_0a43e8f8._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
          DAT_0a43e8f8._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
          DAT_0a43e8f8._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
          DAT_0a43e8f8._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
          DAT_0a43e8f8._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
          DAT_0a43e8f8._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
          DAT_0a43e8f8._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
          DAT_0a43e900 = 0x2928;
          DAT_0a43e902 = 0;
          DAT_0a43e903 = 1;
        }
        if ((DAT_0a43e6d6 & 1) == 0) {
          uVar18 = 0;
          do {
            (&DAT_0a43e67b)[uVar18] = (&DAT_089bee1d)[uVar18] + 0x8a ^ (&DAT_089bee0d)[uVar18 & 0xf]
            ;
            uVar18 = uVar18 + 1;
          } while (uVar18 != 0x5b);
          DAT_0a43e6d6 = 1;
        }
        FUN_0003bb6c(&local_4d0,&DAT_0a43e8f8,&DAT_0a43e67b,0x221);
        lVar6 = __Znwm(0xb0);
        FUN_00033c40(lVar6,FUN_041125e0,FUN_041125e8);
        FUN_04112ab8(lVar6 + 0x28,param_1 + 0x1c);
        local_560 = lVar6;
        FUN_04b7141c(&local_4d0,&local_560,0,0);
        FUN_00033d2c(&local_560);
        uStack_11f = 0xaaaaaaaaaaaaaa;
        uStack_128 = 0xaaaaaaaaaaaaaa;
        puStack_118 = &SUB_aaaaaaaaaaaaaaaa;
        uStack_bf = 0xaaaaaaaaaaaaaa;
        uStack_c8 = 0xaaaaaaaaaaaaaa;
        local_d0 = &SUB_aaaaaaaaaaaaaaaa;
        local_b8 = &SUB_aaaaaaaaaaaaaaaa;
        local_130 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
        uStack_dc = 0xaaaaaaaa;
        local_f0 = 0xaaaaaaaaaaaaaa;
        puStack_f8 = &SUB_aaaaaaaaaaaaaaaa;
        cStack_121 = '\0';
        uStack_120 = 0;
        puStack_110 = &SUB_aaaaaaaaaaaaaa;
        puStack_108 = &DAT_aaaaaaaa00000000;
        puStack_100 = &DAT_aaaaaaaaaaaaaa00;
        cStack_c1 = '\0';
        uStack_c0 = 0;
        puStack_d8 = &DAT_aaaaaaaaaaaaaa00;
        puStack_b0 = &SUB_aaaaaaaaaaaaaa;
        local_a8 = &DAT_aaaaaaaa00000000;
        local_140 = (long *******)0x0;
        ppppppplStack_138 = (long *******)&DAT_aaaaaaaaaaaaaa00;
        uStack_e0 = 0;
        cStack_e9 = '\0';
        uStack_e8 = 0;
        uStack_e4 = 0;
        uVar13 = FUN_04e045a8();
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
                  (&ppppppplStack_138,uVar13);
        uStack_4a7 = 0xaaaaaaaaaaaaaa;
        local_4b0 = 0xaaaaaaaaaaaaaa;
        local_4a0 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_440 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_3f8 = &SUB_aaaaaaaaaaaaaaaa;
        uStack_464 = 0xaaaaaaaa;
        puStack_458 = &SUB_aaaaaaaaaaaaaaaa;
        uStack_478 = 0xaaaaaaaaaaaaaa;
        local_480 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
        local_4b8 = &SUB_aaaaaaaaaaaaaaaa;
        uStack_4a9 = 0;
        uStack_4a8 = 0;
        puStack_498 = &SUB_aaaaaaaaaaaaaa;
        local_490 = &DAT_aaaaaaaa00000000;
        puStack_488 = &DAT_aaaaaaaaaaaaaa00;
        local_450 = &SUB_aaaaaaaaaaaaaa;
        local_460 = &DAT_aaaaaaaaaaaaaa00;
        puStack_438 = &SUB_aaaaaaaaaaaaaa;
        puStack_448 = &DAT_aaaaaaaaaaaaaa00;
        local_430 = &DAT_aaaaaaaa00000000;
        local_4c0 = &DAT_aaaaaaaaaaaaaa00;
        uStack_468 = 0;
        local_471 = 0;
        uStack_470 = 0;
        uStack_46c = 0;
        local_3f0 = 0;
        uStack_400 = 0;
        uStack_408 = 0;
        local_410 = 0;
        uStack_418 = 0;
        uStack_420 = 0;
        uStack_428 = 0;
        local_4d0 = (long *******)0xaaaaaaaa00000006;
        ppppppplStack_4c8 = local_140;
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (&local_4c0,&ppppppplStack_138);
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (&uStack_4a8,&uStack_120);
        local_490 = (undefined1 *)CONCAT44(local_490._4_4_,puStack_108._0_4_);
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (&puStack_488,&puStack_100);
        uStack_470 = uStack_e8;
        uStack_46c = uStack_e4;
        uStack_468 = uStack_e0;
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (&local_460,&puStack_d8);
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (&puStack_448,&uStack_c0);
        local_430 = (undefined1 *)CONCAT44(local_430._4_4_,local_a8._0_4_);
        FUN_04669774();
        FUN_046728d0(&local_1e0);
        FUN_03016948(&local_190,local_1e0);
        FUN_02fc5d68(local_190,&local_4d0);
        goto LAB_0410fcb8;
      }
    }
    if ((DAT_0a43e903 & 1) == 0) {
      DAT_0a43e8f8._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
      DAT_0a43e8f8._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
      DAT_0a43e8f8._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
      DAT_0a43e8f8._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
      DAT_0a43e8f8._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
      DAT_0a43e8f8._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
      DAT_0a43e8f8._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
      DAT_0a43e8f8._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
      DAT_0a43e900 = 0x2928;
      DAT_0a43e902 = 0;
      DAT_0a43e903 = 1;
    }
    if ((DAT_0a43e6d6 & 1) == 0) {
      uVar18 = 0;
      do {
        (&DAT_0a43e67b)[uVar18] = (&DAT_089bee1d)[uVar18] + 0x8a ^ (&DAT_089bee0d)[uVar18 & 0xf];
        uVar18 = uVar18 + 1;
      } while (uVar18 != 0x5b);
      DAT_0a43e6d6 = 1;
    }
    FUN_0003bb6c(&local_4d0,&DAT_0a43e8f8,&DAT_0a43e67b,0x232);
    lVar6 = __Znwm(0xe0);
    FUN_00033c40(lVar6,FUN_041126d4,FUN_041127c0);
    *(long ********)(lVar6 + 0x28) = local_3b0;
    if ((long)local_398 < 0) {
      FUN_00018d20(lVar6 + 0x30,uStack_3a8,uStack_3a0);
    }
    else {
      uVar13 = *puVar22;
      *(undefined8 *)(lVar6 + 0x38) = puVar22[1];
      *(undefined8 *)(lVar6 + 0x30) = uVar13;
      *(undefined8 *)(lVar6 + 0x40) = puVar22[2];
    }
    *(undefined8 *******)(lVar6 + 0x48) = local_390;
    *(undefined8 *******)(lVar6 + 0x50) = ppppppuStack_388;
    pppppuVar8 = (undefined8 *****)0x0;
    if (ppppppuStack_388 != (undefined8 ******)0x0) {
      pppppuVar8 = ppppppuStack_388[1];
      ppppppuStack_388[1] = (undefined8 *****)((long)pppppuVar8 + 1);
    }
    FUN_04112ab8(pppppuVar8,lVar6 + 0x58,param_1 + 0x1c);
    local_568 = lVar6;
    FUN_04b7141c(&local_4d0,&local_568,0,0);
    FUN_00033d2c(&local_568);
    plVar2 = local_3d8;
  }
joined_r0x0410f924:
  local_3d8 = plVar2;
  if (plVar2 != (long *)0x0) {
    LOAcquire();
    lVar6 = plVar2[1];
    plVar2[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*plVar2 + 0x10))(plVar2);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  lVar6 = local_370;
  plVar2 = local_360;
  if ((char)uStack_348 == '\x01') {
    while (plVar2 != (long *)0x0) {
      lVar21 = *plVar2;
      local_370 = lVar6;
      __ZdlPvm(plVar2,0x18);
      lVar6 = local_370;
      plVar2 = (long *)lVar21;
    }
    local_370 = 0;
    if (lVar6 != 0) {
      __ZdlPvm(lVar6,lStack_368 << 3);
    }
  }
  if (ppppppuStack_388 != (undefined8 ******)0x0) {
    LOAcquire();
    pppppuVar8 = ppppppuStack_388[1];
    ppppppuStack_388[1] = (undefined8 *****)((long)pppppuVar8 + -1);
    LORelease();
    if (pppppuVar8 == (undefined8 *****)0x0) {
      (*(code *)(*ppppppuStack_388)[2])(ppppppuStack_388);
      __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppuStack_388);
    }
  }
  if ((long)local_398 < 0) {
    __ZdlPvm(uStack_3a8,local_398 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_78) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


