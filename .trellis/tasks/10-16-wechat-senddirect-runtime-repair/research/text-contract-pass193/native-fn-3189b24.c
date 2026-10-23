// Ghidra inferred pseudocode; requested=0x3189b24
// entry=03189b24 end=0318cfdb

/* WARNING: Removing unreachable block (ram,0x0318cda8) */
/* WARNING: Removing unreachable block (ram,0x0318c5f4) */
/* WARNING: Removing unreachable block (ram,0x0318cddc) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_03189b24(undefined8 *param_1,long param_2,long *param_3)

{
  undefined8 *puVar1;
  undefined1 uVar2;
  uint3 uVar3;
  undefined8 *puVar4;
  bool bVar5;
  undefined1 *puVar6;
  long lVar7;
  long lVar8;
  long ******pppppplVar9;
  int iVar10;
  undefined8 *puVar11;
  long *******ppppppplVar12;
  long *plVar13;
  ulong uVar14;
  undefined1 *puVar15;
  long lVar16;
  undefined1 *puVar17;
  long *plVar18;
  long *******ppppppplVar19;
  long *plVar20;
  undefined4 uVar21;
  undefined4 uVar22;
  undefined4 uVar23;
  undefined4 uVar24;
  undefined4 uVar25;
  undefined4 uVar26;
  long *******local_478;
  long *local_470;
  undefined7 local_468;
  char cStack_461;
  long *******local_460;
  long *local_458;
  undefined7 local_450;
  char cStack_449;
  long local_448;
  long *local_440;
  long *local_438;
  long *local_430;
  long *local_428;
  long *******local_420;
  long lStack_418;
  long *local_410;
  undefined8 uStack_408;
  undefined8 local_400;
  undefined8 local_3f0;
  undefined8 uStack_3e8;
  ulong local_3e0;
  long *******local_3d0;
  long *******local_3c8;
  undefined1 *local_3c0;
  long *local_3b8;
  long *local_3b0;
  long *local_3a8;
  long *local_3a0;
  undefined1 auStack_398 [8];
  undefined8 local_390;
  undefined7 local_380;
  char cStack_379;
  long *local_370;
  long *local_368;
  long *local_360;
  long *local_358;
  long *local_350;
  undefined1 auStack_348 [8];
  undefined8 local_340;
  undefined7 local_330;
  char cStack_329;
  long *local_320;
  long *local_318;
  long *local_310;
  long *******local_308;
  ulong local_300;
  ulong local_2f8;
  undefined8 *local_2f0;
  undefined8 *local_2e8;
  undefined8 *local_2e0;
  long *local_2d8;
  long *local_2d0;
  long *local_2c8;
  undefined1 *local_2c0;
  undefined1 *puStack_2b8;
  undefined1 *local_2b0;
  long *******ppppppplStack_2a8;
  long *local_2a0;
  undefined1 *puStack_298;
  undefined1 *local_290;
  undefined1 *local_288;
  long *******local_280;
  long *plStack_278;
  ulong local_270;
  undefined7 local_268;
  char cStack_261;
  long lStack_260;
  long *local_258;
  long lStack_250;
  ulong local_248;
  byte local_240;
  undefined8 local_238;
  undefined8 local_1f0;
  undefined8 uStack_1e8;
  undefined1 *local_1e0;
  undefined1 *puStack_1d8;
  undefined1 *local_1d0;
  long *local_1c8;
  long *******local_1a0;
  undefined8 local_198;
  long *******local_150;
  undefined8 local_148;
  undefined7 local_140;
  byte bStack_139;
  long *******local_100;
  long *******ppppppplStack_f8;
  undefined8 *local_f0;
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
  undefined8 local_90;
  undefined8 uStack_88;
  long local_78;
  
  local_78 = *(long *)PTR____stack_chk_guard_09b36c98;
  param_1[3] = &SUB_aaaaaaaaaaaaaaaa;
  param_1[2] = &SUB_aaaaaaaaaaaaaaaa;
  param_1[5] = &SUB_aaaaaaaaaaaaaaaa;
  param_1[4] = &SUB_aaaaaaaaaaaaaaaa;
  param_1[1] = &SUB_aaaaaaaaaaaaaaaa;
  *param_1 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0304f1cc(param_1,0,0);
  if (*param_3 == 0) {
    iVar10 = thunk_FUN_05e1d97c(4);
    if (iVar10 != 0) {
      FUN_0488143c(&local_150);
      ppppppplVar12 = local_150;
      if (-1 < (char)bStack_139) {
        ppppppplVar12 = (long *******)&local_150;
      }
      if ((DAT_0a3dd363 & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3dd350)[uVar14] = (&DAT_088bce97)[uVar14] + 0x8a ^ (&DAT_088bce87)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x13);
        DAT_0a3dd363 = 1;
      }
      if ((DAT_0a3ddada & 1) == 0) {
        _DAT_0a3ddac0 = CONCAT44((int)DAT_088baa00,(int)DAT_087ef190);
        uRam000000000a3ddac8 = CONCAT44((int)DAT_084a8110,(int)DAT_0852d550);
        DAT_0a3ddad0 = CONCAT44((int)DAT_088baa08,(int)DAT_084e7040);
        DAT_0a3ddad8 = 0x62;
        DAT_0a3ddada = 1;
      }
      FUN_05e1d050(&local_280,4,ppppppplVar12,&DAT_0a3dd350,&DAT_0a3ddac0,0x2db,0,0);
      if ((DAT_0a3ddb0c & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3ddadb)[uVar14] = (&DAT_088bd853)[uVar14] + 0x8a ^ (&DAT_088bd843)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x31);
        DAT_0a3ddb0c = 1;
      }
      uStack_98 = 0;
      local_a0 = 0;
      uStack_88 = 0;
      local_90 = 0;
      uStack_b8 = 0;
      local_c0 = 0;
      uStack_a8 = 0;
      local_b0 = 0;
      uStack_d8 = 0;
      local_e0 = 0;
      uStack_c8 = 0;
      local_d0 = 0;
      ppppppplStack_f8 = (long *******)0x0;
      local_100 = (long *******)0x0;
      uStack_e8 = 0;
      local_f0 = (undefined8 *)0x0;
      FUN_05e1d31c(&local_280,&DAT_0a3ddadb,&local_100);
      thunk_FUN_05e1d0bc(&local_280);
      if ((char)bStack_139 < '\0') {
        __ZdlPvm(local_150,CONCAT17(bStack_139,local_140) & 0x7fffffffffffffff);
      }
    }
    FUN_030f6640(&local_280,1,1);
    lVar7 = param_1[4];
    FUN_030f67ac(lVar7,&local_280);
    *(undefined8 *)(lVar7 + 0x48) = local_238;
    *(undefined4 *)((long)param_1 + 4) = 0;
    if ((local_240 & 1) == 0) {
      *(undefined4 *)param_1 = 4;
    }
    else {
      if ((long)local_248 < 0) {
        __ZdlPvm(local_258,local_248 & 0x7fffffffffffffff);
      }
      if ((long)local_270 < 0) {
        __ZdlPvm(local_280,local_270 & 0x7fffffffffffffff);
      }
      *(undefined4 *)param_1 = 4;
      if (*(int *)((long)param_1 + 4) != 0) goto LAB_0318cfa0;
    }
    *(undefined4 *)((long)param_1 + 4) = 400;
    goto LAB_0318cfa0;
  }
  iVar10 = thunk_FUN_05e1d97c(2);
  if (iVar10 != 0) {
    FUN_0488143c(&local_1f0);
    ppppppplVar12 = local_1f0;
    if (-1 < (long)local_1e0) {
      ppppppplVar12 = (long *******)&local_1f0;
    }
    if ((DAT_0a3dd363 & 1) == 0) {
      uVar14 = 0;
      do {
        (&DAT_0a3dd350)[uVar14] = (&DAT_088bce97)[uVar14] + 0x8a ^ (&DAT_088bce87)[uVar14 & 0xf];
        uVar14 = uVar14 + 1;
      } while (uVar14 != 0x13);
      DAT_0a3dd363 = 1;
    }
    if ((DAT_0a3ddada & 1) == 0) {
      _DAT_0a3ddac0 = CONCAT44((int)DAT_088baa00,(int)DAT_087ef190);
      uRam000000000a3ddac8 = CONCAT44((int)DAT_084a8110,(int)DAT_0852d550);
      DAT_0a3ddad0 = CONCAT44((int)DAT_088baa08,(int)DAT_084e7040);
      DAT_0a3ddad8 = 0x62;
      DAT_0a3ddada = 1;
    }
    FUN_05e1d050(&local_280,2,ppppppplVar12,&DAT_0a3dd350,&DAT_0a3ddac0,0x2e0,0,0);
    lVar7 = *(long *)*param_3;
    lVar8 = ((long *)*param_3)[1];
    local_150 = (long *******)0x0;
    local_150 = (long *******)&local_148;
    if ((DAT_0a3e2eba & 1) == 0) {
      uVar14 = 0;
      do {
        uVar23 = *(undefined4 *)((long)&DAT_088c56c9 + uVar14);
        uVar3 = CONCAT12((char)((uint)uVar23 >> 8),(short)uVar23) & 0xff00ff;
        uVar26 = *(undefined4 *)((long)&DAT_088c56b5 + uVar14 % 0x14);
        *(uint *)((long)&DAT_0a3e2e72 + uVar14) =
             CONCAT13((char)((uint)uVar23 >> 0x18) + 0x69U ^ (byte)((uint)uVar26 >> 0x18),
                      CONCAT12((char)((uint)uVar23 >> 0x10) + 0x69U ^ (byte)((uint)uVar26 >> 0x10),
                               CONCAT11((char)(uVar3 >> 0x10) + 0x69U ^ (byte)((uint)uVar26 >> 8),
                                        (char)uVar3 + 0x69U ^ (byte)uVar26)));
        uVar14 = uVar14 + 4;
      } while (uVar14 != 0x48);
      DAT_0a3e2eba = 1;
    }
    uVar14 = lVar8 - lVar7 >> 4;
    lVar7 = 0;
    do {
      lVar8 = lVar7;
      *(undefined1 *)((long)&local_148 + lVar8) = (&DAT_0a3e2e95)[uVar14 % 10];
      bVar5 = 9 < uVar14;
      uVar14 = uVar14 / 10;
      lVar7 = lVar8 + 1;
    } while (bVar5);
    *(undefined1 *)((long)&local_148 + lVar8 + 1) = 0;
    if (8 < lVar8 + 8U) {
      puVar15 = (undefined1 *)((long)&local_148 + lVar8);
      puVar6 = (undefined1 *)((long)&local_148 + 1);
      do {
        uVar2 = *puVar15;
        *puVar15 = puVar6[-1];
        puVar6[-1] = uVar2;
        bVar5 = puVar6 < puVar15 + -1;
        puVar15 = puVar15 + -1;
        puVar6 = puVar6 + 1;
      } while (bVar5);
    }
    if (*(char *)(*param_3 + 0x18) == '\x01') {
      local_1a0 = (long *******)&DAT_0a3e2ec4;
      if ((DAT_0a3e2ec9 & 1) == 0) {
        DAT_0a3e2ec4 = 0x7274;
        DAT_0a3e2ec6 = 0x75;
        puVar15 = &DAT_0a3e2ec8;
        puVar6 = &DAT_0a3e2ec7;
        puVar17 = &DAT_0a3e2ec9;
LAB_0318a030:
        *puVar6 = 0x65;
        *puVar15 = 0;
        *puVar17 = 1;
      }
    }
    else {
      local_1a0 = (long *******)&DAT_0a3e2ecc;
      if ((DAT_0a3e2ed2 & 1) == 0) {
        DAT_0a3e2ecc = (undefined4)DAT_0847fe48;
        puVar6 = &DAT_0a3e2ed0;
        puVar15 = &DAT_0a3e2ed1;
        puVar17 = &DAT_0a3e2ed2;
        goto LAB_0318a030;
      }
    }
    local_198._0_1_ = 0;
    if ((DAT_0a3ddb51 & 1) == 0) {
      uVar14 = 0;
      do {
        (&DAT_0a3ddb0d)[uVar14] = (&DAT_088bd894)[uVar14] + 0x8a ^ (&DAT_088bd884)[uVar14 & 0xf];
        uVar14 = uVar14 + 1;
      } while (uVar14 != 0x44);
      DAT_0a3ddb51 = 1;
    }
    local_100 = (long *******)&local_150;
    ppppppplStack_f8 = (long *******)&local_1a0;
    uStack_e8 = 0;
    local_f0 = (undefined8 *)0x0;
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
    uStack_88 = 0;
    local_90 = 0;
    FUN_05e1d31c(&local_280,&DAT_0a3ddb0d,&local_100);
    thunk_FUN_05e1d0bc(&local_280);
    if ((long)local_1e0 < 0) {
      __ZdlPvm(local_1f0,(ulong)local_1e0 & 0x7fffffffffffffff);
    }
  }
  puStack_298 = &SUB_aaaaaaaaaaaaaaaa;
  local_2a0 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_288 = &SUB_aaaaaaaaaaaaaaaa;
  local_290 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_2b8 = &SUB_aaaaaaaaaaaaaaaa;
  local_2c0 = &SUB_aaaaaaaaaaaaaaaa;
  ppppppplStack_2a8 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
  local_2b0 = &SUB_aaaaaaaaaaaaaaaa;
  if ((DAT_0a3ddada & 1) == 0) {
    _DAT_0a3ddac0 = CONCAT44((int)DAT_088baa00,(int)DAT_087ef190);
    uRam000000000a3ddac8 = CONCAT44((int)DAT_084a8110,(int)DAT_0852d550);
    DAT_0a3ddad0 = CONCAT44((int)DAT_088baa08,(int)DAT_084e7040);
    DAT_0a3ddad8 = 0x62;
    DAT_0a3ddada = 1;
  }
  if ((DAT_0a3dd403 & 1) == 0) {
    uVar14 = 0;
    do {
      (&DAT_0a3dd39e)[uVar14] = (&DAT_088bcf0a)[uVar14] + 0x8a ^ (&DAT_088bcefa)[uVar14 & 0xf];
      uVar14 = uVar14 + 1;
    } while (uVar14 != 0x65);
    DAT_0a3dd403 = 1;
  }
  FUN_0003bb6c(&local_280,&DAT_0a3ddac0,&DAT_0a3dd39e,0x2e1);
  if ((DAT_0a3ddada & 1) == 0) {
    _DAT_0a3ddac0 = CONCAT44((int)DAT_088baa00,(int)DAT_087ef190);
    uRam000000000a3ddac8 = CONCAT44((int)DAT_084a8110,(int)DAT_0852d550);
    DAT_0a3ddad0 = CONCAT44((int)DAT_088baa08,(int)DAT_084e7040);
    DAT_0a3ddad8 = 0x62;
    DAT_0a3ddada = 1;
  }
  local_2c0 = (undefined1 *)CONCAT44(local_2c0._4_4_,2);
  local_2a0 = plStack_278;
  ppppppplStack_2a8 = local_280;
  local_2b0 = (undefined1 *)0x0;
  puStack_298 = (undefined1 *)0x0;
  local_288 = (undefined1 *)0x0;
  local_290 = (undefined1 *)0x0;
  puStack_2b8 = (undefined1 *)FUN_0474715c();
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
            (&puStack_298,&DAT_0a3ddac0);
  local_2d0 = (long *)0x0;
  local_2d8 = (long *)0x0;
  local_2c8 = (long *)0x0;
  local_2f0 = (undefined8 *)0x0;
  local_2e8 = (undefined8 *)0x0;
  local_2e0 = (undefined8 *)0x0;
  local_300 = 0;
  local_2f8 = 0;
  local_308 = (long *******)0x0;
  FUN_0318d57c(&local_2d8,((long *)*param_3)[1] - *(long *)*param_3 >> 4);
  FUN_02e7db78(&local_2f0,((long *)*param_3)[1] - *(long *)*param_3 >> 4);
  puVar11 = *(undefined8 **)*param_3;
  puVar1 = (undefined8 *)((undefined8 *)*param_3)[1];
  if (puVar11 != puVar1) {
    uVar26 = (undefined4)DAT_088baa00;
    uVar22 = (undefined4)DAT_087ef190;
    uVar23 = (undefined4)DAT_0852d550;
    uVar21 = (undefined4)DAT_084a8110;
    uVar24 = (undefined4)DAT_084e7040;
    uVar25 = (undefined4)DAT_088baa08;
    do {
      local_438 = (long *)0x0;
      if (puVar11[1] != 0) {
        local_430 = (long *)__ZNSt3__119__shared_weak_count4lockEv();
        if (local_430 == (long *)0x0) {
          if (local_438 != (long *)0x0) {
            local_310 = (long *)0x0;
            goto LAB_0318a3c0;
          }
        }
        else {
          local_438 = (long *)*puVar11;
          if (local_438 != (long *)0x0) {
            local_430[1] = local_430[1] + 1;
            local_310 = local_430;
LAB_0318a3c0:
            local_458 = (long *)&SUB_aaaaaaaaaaaaaaaa;
            local_460 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
            local_318 = local_438;
            FUN_0318d680(&local_460,param_2,&local_318);
            plVar13 = local_310;
            if (local_310 == (long *)0x0) {
LAB_0318a3e4:
              if (local_460 != (long *******)0x0) goto LAB_0318a3ec;
LAB_0318a590:
              iVar10 = thunk_FUN_05e1d97c(4);
              plVar13 = local_458;
              if (iVar10 != 0) {
                FUN_0488143c(&local_1f0);
                ppppppplVar12 = local_1f0;
                if (-1 < (long)local_1e0) {
                  ppppppplVar12 = (long *******)&local_1f0;
                }
                if ((DAT_0a3dd363 & 1) == 0) {
                  uVar14 = 0;
                  do {
                    (&DAT_0a3dd350)[uVar14] =
                         (&DAT_088bce97)[uVar14] + 0x8a ^ (&DAT_088bce87)[uVar14 & 0xf];
                    uVar14 = uVar14 + 1;
                  } while (uVar14 != 0x13);
                  DAT_0a3dd363 = 1;
                }
                if ((DAT_0a3ddada & 1) == 0) {
                  DAT_0a3ddad8 = 0x62;
                  DAT_0a3ddada = 1;
                  _DAT_0a3ddac0 = CONCAT44(uVar26,uVar22);
                  uRam000000000a3ddac8 = CONCAT44(uVar21,uVar23);
                  DAT_0a3ddad0 = CONCAT44(uVar25,uVar24);
                }
                FUN_05e1d050(&local_280,4,ppppppplVar12,&DAT_0a3dd350,&DAT_0a3ddac0,0x2f1,0,0);
                FUN_030f1f08(&local_420,local_438);
                local_150 = local_420;
                if (-1 < (long)local_410) {
                  local_150 = (long *******)&local_420;
                }
                local_148._0_1_ = 0;
                local_1a0 = (long *******)local_438[7];
                if (-1 < *(char *)((long)local_438 + 0x4f)) {
                  local_1a0 = (long *******)(local_438 + 7);
                }
                local_198._0_1_ = 0;
                if ((DAT_0a3ddb93 & 1) == 0) {
                  uVar14 = 0;
                  do {
                    (&DAT_0a3ddb52)[uVar14] =
                         (&DAT_088bd8e8)[uVar14] + 0x8a ^ (&DAT_088bd8d8)[uVar14 & 0xf];
                    uVar14 = uVar14 + 1;
                  } while (uVar14 != 0x41);
                  DAT_0a3ddb93 = 1;
                }
                local_100 = (long *******)&local_150;
                ppppppplStack_f8 = (long *******)&local_1a0;
                uStack_e8 = 0;
                local_f0 = (undefined8 *)0x0;
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
                uStack_88 = 0;
                local_90 = 0;
                FUN_05e1d31c(&local_280,&DAT_0a3ddb52,&local_100);
                if ((long)local_410 < 0) {
                  __ZdlPvm(local_420,(ulong)local_410 & 0x7fffffffffffffff);
                }
                thunk_FUN_05e1d0bc(&local_280);
                ppppppplVar12 = local_1f0;
                puVar15 = local_1e0;
                plVar13 = local_458;
                if (-1 < (long)local_1e0) goto joined_r0x0318ac64;
                goto LAB_0318ac58;
              }
            }
            else {
              LOAcquire();
              lVar7 = local_310[1];
              local_310[1] = lVar7 + -1;
              LORelease();
              if (lVar7 != 0) goto LAB_0318a3e4;
              (**(code **)(*local_310 + 0x10))(local_310);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
              if (local_460 == (long *******)0x0) goto LAB_0318a590;
LAB_0318a3ec:
              puStack_1d8 = &SUB_aaaaaaaaaaaaaaaa;
              local_1e0 = &SUB_aaaaaaaaaaaaaaaa;
              local_1c8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
              local_1d0 = &SUB_aaaaaaaaaaaaaaaa;
              uStack_1e8 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
              local_1f0 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
              FUN_0304f1cc(&local_1f0,0,0);
              local_478 = (long *******)local_438[1];
              if (local_478 == (long *******)0x0) {
                local_478 = (long *******)0x0;
                local_470 = (long *)0x0;
LAB_0318a744:
                local_3a8 = local_438;
                local_3a0 = local_430;
                if (local_430 != (long *)0x0) {
                  local_430[1] = local_430[1] + 1;
                }
                FUN_030d39d8(auStack_398,local_460,&local_3a8);
                plVar13 = local_370;
                if (local_370 != (long *)0x0) {
                  LOAcquire();
                  lVar7 = local_370[1];
                  local_370[1] = lVar7 + -1;
                  LORelease();
                  if (lVar7 == 0) {
                    (**(code **)(*local_370 + 0x10))(local_370);
                    __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
                  }
                }
                plVar13 = local_3a0;
                if (cStack_379 < '\0') {
                  __ZdlPvm(local_390,CONCAT17(cStack_379,local_380) & 0x7fffffffffffffff);
                  plVar13 = local_3a0;
                }
                local_3a0 = plVar13;
                if (plVar13 != (long *)0x0) {
                  LOAcquire();
                  lVar7 = plVar13[1];
                  plVar13[1] = lVar7 + -1;
                  LORelease();
                  if (lVar7 == 0) {
                    (**(code **)(*plVar13 + 0x10))(plVar13);
                    __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
                  }
                }
                local_3b8 = local_438;
                local_3b0 = local_430;
                if (local_430 != (long *)0x0) {
                  local_430[1] = local_430[1] + 1;
                }
                (*(code *)(*local_460)[3])(&local_280,local_460,&local_3b8);
                local_1f0 = local_280;
                __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                          (&uStack_1e8,&plStack_278);
                plVar13 = local_1c8;
                if (local_258 != (long *)0x0) {
                  local_258[1] = local_258[1] + 1;
                }
                local_1d0 = (undefined1 *)lStack_260;
                local_1c8 = local_258;
                plVar18 = local_258;
                if (plVar13 != (long *)0x0) {
                  LOAcquire();
                  lVar7 = plVar13[1];
                  plVar13[1] = lVar7 + -1;
                  LORelease();
                  if (lVar7 == 0) {
                    (**(code **)(*plVar13 + 0x10))(plVar13);
                    __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
                    plVar18 = local_258;
                  }
                }
                local_258 = plVar18;
                if (plVar18 != (long *)0x0) {
                  LOAcquire();
                  lVar7 = plVar18[1];
                  plVar18[1] = lVar7 + -1;
                  LORelease();
                  if (lVar7 == 0) {
                    (**(code **)(*plVar18 + 0x10))(plVar18);
                    __ZNSt3__119__shared_weak_count14__release_weakEv(plVar18);
                  }
                }
                plVar13 = local_3b0;
                if (cStack_261 < '\0') {
                  __ZdlPvm(plStack_278,CONCAT17(cStack_261,local_268) & 0x7fffffffffffffff);
                  plVar13 = local_3b0;
                }
              }
              else {
                local_470 = (long *)local_438[2];
                if (local_470 != (long *)0x0) {
                  local_470[1] = local_470[1] + 1;
                }
                iVar10 = (*(code *)(*local_478)[4])();
                if (iVar10 != 1) goto LAB_0318a744;
                local_358 = local_438;
                local_350 = local_430;
                if (local_430 != (long *)0x0) {
                  local_430[1] = local_430[1] + 1;
                }
                FUN_030d31f0(auStack_348,local_460,&local_358);
                plVar13 = local_320;
                if (local_320 != (long *)0x0) {
                  LOAcquire();
                  lVar7 = local_320[1];
                  local_320[1] = lVar7 + -1;
                  LORelease();
                  if (lVar7 == 0) {
                    (**(code **)(*local_320 + 0x10))(local_320);
                    __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
                  }
                }
                if (cStack_329 < '\0') {
                  __ZdlPvm(local_340,CONCAT17(cStack_329,local_330) & 0x7fffffffffffffff);
                }
                plVar13 = local_350;
                if (local_350 != (long *)0x0) {
                  LOAcquire();
                  lVar7 = local_350[1];
                  local_350[1] = lVar7 + -1;
                  LORelease();
                  if (lVar7 == 0) {
                    (**(code **)(*local_350 + 0x10))(local_350);
                    __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
                  }
                }
                local_368 = local_438;
                local_360 = local_430;
                if (local_430 != (long *)0x0) {
                  local_430[1] = local_430[1] + 1;
                }
                (*(code *)(*local_460)[5])(&local_280,local_460,&local_368);
                local_1f0 = local_280;
                __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                          (&uStack_1e8,&plStack_278);
                plVar13 = local_1c8;
                if (local_258 != (long *)0x0) {
                  local_258[1] = local_258[1] + 1;
                }
                local_1d0 = (undefined1 *)lStack_260;
                local_1c8 = local_258;
                plVar18 = local_258;
                if (plVar13 != (long *)0x0) {
                  LOAcquire();
                  lVar7 = plVar13[1];
                  plVar13[1] = lVar7 + -1;
                  LORelease();
                  if (lVar7 == 0) {
                    (**(code **)(*plVar13 + 0x10))(plVar13);
                    __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
                    plVar18 = local_258;
                  }
                }
                local_258 = plVar18;
                if (plVar18 != (long *)0x0) {
                  LOAcquire();
                  lVar7 = *(long *)((long)plVar18 + 8U);
                  *(long *)((long)plVar18 + 8U) = lVar7 + -1;
                  LORelease();
                  if (lVar7 == 0) {
                    (**(code **)(*plVar18 + 0x10))(plVar18);
                    __ZNSt3__119__shared_weak_count14__release_weakEv(plVar18);
                  }
                }
                plVar13 = local_360;
                if (cStack_261 < '\0') {
                  __ZdlPvm(plStack_278,CONCAT17(cStack_261,local_268) & 0x7fffffffffffffff);
                  plVar13 = local_360;
                }
              }
              if (plVar13 != (long *)0x0) {
                LOAcquire();
                lVar7 = plVar13[1];
                plVar13[1] = lVar7 + -1;
                LORelease();
                if (lVar7 == 0) {
                  (**(code **)(*plVar13 + 0x10))(plVar13);
                  __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
                }
              }
              if ((int)local_1f0 == 0 && local_1f0._4_4_ == 0) {
                FUN_030f3eec(local_438);
                ppppppplVar12 = (long *******)local_438[3];
                plVar13 = (long *)local_438[4];
                if (plVar13 != (long *)0x0) {
                  plVar13[1] = plVar13[1] + 1;
                }
                local_280 = ppppppplVar12;
                plStack_278 = plVar13;
                if (ppppppplVar12 != (long *******)0x0) {
                  uVar14 = local_300;
                  if (-1 < (long)local_2f8) {
                    uVar14 = local_2f8 >> 0x38;
                  }
                  if (uVar14 == 0) {
                    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                              (&local_308,local_438 + 7);
                  }
                  if (local_2d0 < local_2c8) {
                    *local_2d0 = (long)local_438;
                    local_2d0[1] = (long)local_430;
                    if (local_430 != (long *)0x0) {
                      local_430[1] = local_430[1] + 1;
                    }
                    local_2d0 = local_2d0 + 2;
                  }
                  else {
                    local_2d0 = (long *)FUN_0320cce0(&local_2d8,&local_438);
                  }
                  puVar4 = local_2e8;
                  if (local_2e8 < local_2e0) {
                    FUN_00f57630(local_2e8,ppppppplVar12);
                    local_2e8 = puVar4 + 0x4f;
                  }
                  else {
                    local_2e8 = (undefined8 *)FUN_02e86b60(&local_2f0,ppppppplVar12);
                  }
                }
                if (plVar13 != (long *)0x0) {
                  LOAcquire();
                  lVar7 = plVar13[1];
                  plVar13[1] = lVar7 + -1;
                  LORelease();
                  if (lVar7 == 0) {
                    (**(code **)(*plVar13 + 0x10))(plVar13);
                    __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
                  }
                }
              }
              else {
                iVar10 = thunk_FUN_05e1d97c(4);
                if (iVar10 != 0) {
                  FUN_0488143c(&local_420);
                  ppppppplVar12 = local_420;
                  if (-1 < (long)local_410) {
                    ppppppplVar12 = (long *******)&local_420;
                  }
                  if ((DAT_0a3dd363 & 1) == 0) {
                    uVar14 = 0;
                    do {
                      (&DAT_0a3dd350)[uVar14] =
                           (&DAT_088bce97)[uVar14] + 0x8a ^ (&DAT_088bce87)[uVar14 & 0xf];
                      uVar14 = uVar14 + 1;
                    } while (uVar14 != 0x13);
                    DAT_0a3dd363 = 1;
                  }
                  if ((DAT_0a3ddada & 1) == 0) {
                    DAT_0a3ddad0 = CONCAT44(uVar25,uVar24);
                    DAT_0a3ddad8 = 0x62;
                    DAT_0a3ddada = 1;
                    _DAT_0a3ddac0 = CONCAT44(uVar26,uVar22);
                    uRam000000000a3ddac8 = CONCAT44(uVar21,uVar23);
                  }
                  FUN_05e1d050(&local_280,4,ppppppplVar12,&DAT_0a3dd350,&DAT_0a3ddac0,0x303,0,0);
                  FUN_030f1f08(&local_3d0,local_438);
                  local_150 = local_3d0;
                  if (-1 < (long)local_3c0) {
                    local_150 = (long *******)&local_3d0;
                  }
                  local_148._0_1_ = 0;
                  local_1a0 = (long *******)local_438[7];
                  if (-1 < *(char *)((long)local_438 + 0x4f)) {
                    local_1a0 = (long *******)(local_438 + 7);
                  }
                  local_198._0_1_ = 0;
                  if ((DAT_0a3ddbd0 & 1) == 0) {
                    uVar14 = 0;
                    do {
                      (&DAT_0a3ddb94)[uVar14] =
                           (&DAT_088bd939)[uVar14] + 0x8a ^ (&DAT_088bd929)[uVar14 & 0xf];
                      uVar14 = uVar14 + 1;
                    } while (uVar14 != 0x3c);
                    DAT_0a3ddbd0 = 1;
                  }
                  local_100 = (long *******)&local_150;
                  ppppppplStack_f8 = (long *******)&local_1a0;
                  uStack_e8 = 0;
                  local_f0 = (undefined8 *)0x0;
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
                  uStack_88 = 0;
                  local_90 = 0;
                  FUN_05e1d31c(&local_280,&DAT_0a3ddb94,&local_100);
                  if ((long)local_3c0 < 0) {
                    __ZdlPvm(local_3d0,(ulong)local_3c0 & 0x7fffffffffffffff);
                  }
                  thunk_FUN_05e1d0bc(&local_280);
                  if ((long)local_410 < 0) {
                    __ZdlPvm(local_420,(ulong)local_410 & 0x7fffffffffffffff);
                  }
                }
              }
              plVar18 = local_470;
              plVar13 = local_1c8;
              if (local_470 != (long *)0x0) {
                LOAcquire();
                lVar7 = local_470[1];
                local_470[1] = lVar7 + -1;
                LORelease();
                if (lVar7 == 0) {
                  (**(code **)(*local_470 + 0x10))(local_470);
                  __ZNSt3__119__shared_weak_count14__release_weakEv(plVar18);
                  plVar13 = local_1c8;
                }
              }
              local_1c8 = plVar13;
              if (plVar13 != (long *)0x0) {
                LOAcquire();
                lVar7 = plVar13[1];
                plVar13[1] = lVar7 + -1;
                LORelease();
                if (lVar7 == 0) {
                  (**(code **)(*plVar13 + 0x10))(plVar13);
                  __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
                }
              }
              ppppppplVar12 = uStack_1e8;
              puVar15 = puStack_1d8;
              plVar13 = local_458;
              if ((long)puStack_1d8 < 0) {
LAB_0318ac58:
                __ZdlPvm(ppppppplVar12,(ulong)puVar15 & 0x7fffffffffffffff);
                plVar13 = local_458;
              }
            }
joined_r0x0318ac64:
            local_458 = plVar13;
            if (plVar13 != (long *)0x0) {
              LOAcquire();
              lVar7 = plVar13[1];
              plVar13[1] = lVar7 + -1;
              LORelease();
              if (lVar7 == 0) {
                (**(code **)(*plVar13 + 0x10))(plVar13);
                __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
              }
            }
            if (local_430 == (long *)0x0) goto LAB_0318a364;
          }
          plVar13 = local_430;
          LOAcquire();
          lVar7 = local_430[1];
          local_430[1] = lVar7 + -1;
          LORelease();
          if (lVar7 == 0) {
            (**(code **)(*local_430 + 0x10))();
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
          }
        }
      }
LAB_0318a364:
      puVar11 = puVar11 + 2;
    } while (puVar11 != puVar1);
  }
  if (local_2f0 == local_2e8) {
LAB_0318bbb4:
    iVar10 = thunk_FUN_05e1d97c(4);
    if (iVar10 != 0) {
      FUN_0488143c(&local_1f0);
      ppppppplVar12 = local_1f0;
      if (-1 < (long)local_1e0) {
        ppppppplVar12 = (long *******)&local_1f0;
      }
      if ((DAT_0a3dd363 & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3dd350)[uVar14] = (&DAT_088bce97)[uVar14] + 0x8a ^ (&DAT_088bce87)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x13);
        DAT_0a3dd363 = 1;
      }
      if ((DAT_0a3ddada & 1) == 0) {
        _DAT_0a3ddac0 = CONCAT44((int)DAT_088baa00,(int)DAT_087ef190);
        uRam000000000a3ddac8 = CONCAT44((int)DAT_084a8110,(int)DAT_0852d550);
        DAT_0a3ddad0 = CONCAT44((int)DAT_088baa08,(int)DAT_084e7040);
        DAT_0a3ddad8 = 0x62;
        DAT_0a3ddada = 1;
      }
      FUN_05e1d050(&local_280,4,ppppppplVar12,&DAT_0a3dd350,&DAT_0a3ddac0,0x314,0,0);
      local_150 = local_308;
      if (-1 < (long)local_2f8) {
        local_150 = (long *******)&local_308;
      }
      local_148._0_1_ = 0;
      lVar7 = *(long *)*param_3;
      lVar8 = ((long *)*param_3)[1];
      local_1a0 = (long *******)0x0;
      local_1a0 = (long *******)&local_198;
      if ((DAT_0a3e2eba & 1) == 0) {
        uVar14 = 0;
        do {
          uVar23 = *(undefined4 *)((long)&DAT_088c56c9 + uVar14);
          uVar3 = CONCAT12((char)((uint)uVar23 >> 8),(short)uVar23) & 0xff00ff;
          uVar26 = *(undefined4 *)((long)&DAT_088c56b5 + uVar14 % 0x14);
          *(uint *)((long)&DAT_0a3e2e72 + uVar14) =
               CONCAT13((char)((uint)uVar23 >> 0x18) + 0x69U ^ (byte)((uint)uVar26 >> 0x18),
                        CONCAT12((char)((uint)uVar23 >> 0x10) + 0x69U ^ (byte)((uint)uVar26 >> 0x10)
                                 ,CONCAT11((char)(uVar3 >> 0x10) + 0x69U ^ (byte)((uint)uVar26 >> 8)
                                           ,(char)uVar3 + 0x69U ^ (byte)uVar26)));
          uVar14 = uVar14 + 4;
        } while (uVar14 != 0x48);
        DAT_0a3e2eba = 1;
      }
      uVar14 = lVar8 - lVar7 >> 4;
      lVar7 = 0;
      do {
        lVar8 = lVar7;
        *(undefined1 *)((long)&local_198 + lVar8) = (&DAT_0a3e2e95)[uVar14 % 10];
        bVar5 = 9 < uVar14;
        uVar14 = uVar14 / 10;
        lVar7 = lVar8 + 1;
      } while (bVar5);
      *(undefined1 *)((long)&local_198 + lVar8 + 1) = 0;
      if (8 < lVar8 + 8U) {
        puVar15 = (undefined1 *)((long)&local_198 + lVar8);
        puVar6 = (undefined1 *)((long)&local_198 + 1);
        do {
          uVar2 = *puVar15;
          *puVar15 = puVar6[-1];
          puVar6[-1] = uVar2;
          bVar5 = puVar6 < puVar15 + -1;
          puVar15 = puVar15 + -1;
          puVar6 = puVar6 + 1;
        } while (bVar5);
      }
      if ((DAT_0a3ddc1a & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3ddbd1)[uVar14] = (&DAT_088bd985)[uVar14] + 0x8a ^ (&DAT_088bd975)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x49);
        DAT_0a3ddc1a = 1;
      }
      local_100 = (long *******)&local_150;
      ppppppplStack_f8 = (long *******)&local_1a0;
      uStack_e8 = 0;
      local_f0 = (undefined8 *)0x0;
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
      uStack_88 = 0;
      local_90 = 0;
      FUN_05e1d31c(&local_280,&DAT_0a3ddbd1,&local_100);
      thunk_FUN_05e1d0bc(&local_280);
      if ((long)local_1e0 < 0) {
        __ZdlPvm(local_1f0,(ulong)local_1e0 & 0x7fffffffffffffff);
      }
    }
    FUN_030f6640(&local_280,1,1);
    lVar7 = param_1[4];
    FUN_030f67ac(lVar7,&local_280);
    *(undefined8 *)(lVar7 + 0x48) = local_238;
    *(undefined4 *)((long)param_1 + 4) = 0;
    if ((local_240 & 1) == 0) {
      *(undefined4 *)param_1 = 4;
    }
    else {
      if ((long)local_248 < 0) {
        __ZdlPvm(local_258,local_248 & 0x7fffffffffffffff);
      }
      if ((long)local_270 < 0) {
        __ZdlPvm(local_280,local_270 & 0x7fffffffffffffff);
      }
      *(undefined4 *)param_1 = 4;
      if (*(int *)((long)param_1 + 4) != 0) goto LAB_0318ce74;
    }
    *(undefined4 *)((long)param_1 + 4) = 400;
  }
  else {
    uVar14 = local_300;
    if (-1 < (long)local_2f8) {
      uVar14 = local_2f8 >> 0x38;
    }
    if (uVar14 == 0) goto LAB_0318bbb4;
    iVar10 = thunk_FUN_05e1d97c(2);
    if (iVar10 != 0) {
      FUN_0488143c(&local_420);
      ppppppplVar12 = local_420;
      if (-1 < (long)local_410) {
        ppppppplVar12 = (long *******)&local_420;
      }
      if ((DAT_0a3dd363 & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3dd350)[uVar14] = (&DAT_088bce97)[uVar14] + 0x8a ^ (&DAT_088bce87)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x13);
        DAT_0a3dd363 = 1;
      }
      if ((DAT_0a3ddada & 1) == 0) {
        _DAT_0a3ddac0 = CONCAT44((int)DAT_088baa00,(int)DAT_087ef190);
        uRam000000000a3ddac8 = CONCAT44((int)DAT_084a8110,(int)DAT_0852d550);
        DAT_0a3ddad0 = CONCAT44((int)DAT_088baa08,(int)DAT_084e7040);
        DAT_0a3ddad8 = 0x62;
        DAT_0a3ddada = 1;
      }
      FUN_05e1d050(&local_280,2,ppppppplVar12,&DAT_0a3dd350,&DAT_0a3ddac0,0x31a,0,0);
      local_150 = local_308;
      if (-1 < (long)local_2f8) {
        local_150 = (long *******)&local_308;
      }
      local_148._0_1_ = 0;
      local_1a0 = (long *******)0x0;
      if ((DAT_0a3e2eba & 1) == 0) {
        uVar14 = 0;
        do {
          uVar23 = *(undefined4 *)((long)&DAT_088c56c9 + uVar14);
          uVar3 = CONCAT12((char)((uint)uVar23 >> 8),(short)uVar23) & 0xff00ff;
          uVar26 = *(undefined4 *)((long)&DAT_088c56b5 + uVar14 % 0x14);
          *(uint *)((long)&DAT_0a3e2e72 + uVar14) =
               CONCAT13((char)((uint)uVar23 >> 0x18) + 0x69U ^ (byte)((uint)uVar26 >> 0x18),
                        CONCAT12((char)((uint)uVar23 >> 0x10) + 0x69U ^ (byte)((uint)uVar26 >> 0x10)
                                 ,CONCAT11((char)(uVar3 >> 0x10) + 0x69U ^ (byte)((uint)uVar26 >> 8)
                                           ,(char)uVar3 + 0x69U ^ (byte)uVar26)));
          uVar14 = uVar14 + 4;
        } while (uVar14 != 0x48);
        DAT_0a3e2eba = 1;
      }
      uVar14 = ((long)local_2e8 - (long)local_2f0 >> 3) * -0x6474a8819ec8e951;
      lVar7 = 0;
      do {
        lVar8 = lVar7;
        *(undefined1 *)((long)&local_198 + lVar8) = (&DAT_0a3e2e95)[uVar14 % 10];
        bVar5 = 9 < uVar14;
        uVar14 = uVar14 / 10;
        lVar7 = lVar8 + 1;
      } while (bVar5);
      *(undefined1 *)((long)&local_198 + lVar8 + 1) = 0;
      if (8 < lVar8 + 8U) {
        puVar15 = (undefined1 *)((long)&local_198 + lVar8);
        puVar6 = (undefined1 *)((long)&local_198 + 1);
        do {
          uVar2 = *puVar15;
          *puVar15 = puVar6[-1];
          puVar6[-1] = uVar2;
          bVar5 = puVar6 < puVar15 + -1;
          puVar15 = puVar15 + -1;
          puVar6 = puVar6 + 1;
        } while (bVar5);
      }
      local_1a0 = (long *******)&local_198;
      local_1f0 = (long *******)&uStack_1e8;
      lVar7 = 0;
      uVar14 = ((long *)*param_3)[1] - *(long *)*param_3 >> 4;
      do {
        lVar8 = lVar7;
        *(undefined1 *)((long)&uStack_1e8 + lVar8) = (&DAT_0a3e2e95)[uVar14 % 10];
        bVar5 = 9 < uVar14;
        lVar7 = lVar8 + 1;
        uVar14 = uVar14 / 10;
      } while (bVar5);
      *(undefined1 *)((long)&uStack_1e8 + lVar8 + 1) = 0;
      if (8 < lVar8 + 8U) {
        puVar15 = (undefined1 *)((long)&uStack_1e8 + lVar8);
        puVar6 = (undefined1 *)((long)&uStack_1e8 + 1);
        do {
          uVar2 = *puVar15;
          *puVar15 = puVar6[-1];
          puVar6[-1] = uVar2;
          bVar5 = puVar6 < puVar15 + -1;
          puVar15 = puVar15 + -1;
          puVar6 = puVar6 + 1;
        } while (bVar5);
      }
      if ((DAT_0a3ddc64 & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3ddc1b)[uVar14] = (&DAT_088bd9de)[uVar14] + 0x8a ^ (&DAT_088bd9ce)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x49);
        DAT_0a3ddc64 = 1;
      }
      local_100 = (long *******)&local_150;
      ppppppplStack_f8 = (long *******)&local_1a0;
      local_f0 = &local_1f0;
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
      local_90 = 0;
      uStack_98 = 0;
      uStack_88 = 0;
      FUN_05e1d31c(&local_280,&DAT_0a3ddc1b,&local_100);
      thunk_FUN_05e1d0bc(&local_280);
      if ((long)local_410 < 0) {
        __ZdlPvm(local_420,(ulong)local_410 & 0x7fffffffffffffff);
      }
    }
    if ((DAT_0a3ddc71 & 1) == 0) {
      DAT_0a3ddc68._0_1_ = s_prepared__count_ler__088baa10[0];
      DAT_0a3ddc68._1_1_ = s_prepared__count_ler__088baa10[1];
      DAT_0a3ddc68._2_1_ = s_prepared__count_ler__088baa10[2];
      DAT_0a3ddc68._3_1_ = s_prepared__count_ler__088baa10[3];
      DAT_0a3ddc68._4_1_ = s_prepared__count_ler__088baa10[4];
      DAT_0a3ddc68._5_1_ = s_prepared__count_ler__088baa10[5];
      DAT_0a3ddc68._6_1_ = s_prepared__count_ler__088baa10[6];
      DAT_0a3ddc68._7_1_ = s_prepared__count_ler__088baa10[7];
      DAT_0a3ddc70 = 0;
      DAT_0a3ddc71 = 1;
    }
    FUN_00ebbf48(&local_2c0,&DAT_0a3ddc68,0);
    local_3c8 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
    local_3c0 = &SUB_aaaaaaaaaaaaaaaa;
    local_3d0 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
    FUN_032d0e64(&local_280,*(undefined8 *)(param_2 + 0xb78),&local_2f0,&local_308);
    FUN_0318dd3c(&local_3d0,&local_100,&local_280);
    plVar13 = plStack_278;
    if (plStack_278 != (long *)0x0) {
      LOAcquire();
      lVar7 = plStack_278[1];
      plStack_278[1] = lVar7 + -1;
      LORelease();
      if (lVar7 == 0) {
        (**(code **)(*plStack_278 + 0x10))(plStack_278);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
      }
    }
    if ((DAT_0a3ddc90 & 1) == 0) {
      uVar14 = 0;
      do {
        (&DAT_0a3ddc72)[uVar14] = (&DAT_088bda50)[uVar14] + 0x8a ^ (&DAT_088bda40)[uVar14 & 0xf];
        uVar14 = uVar14 + 1;
      } while (uVar14 != 0x1e);
      DAT_0a3ddc90 = 1;
    }
    __ZNSt3__1plIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_12basic_stringIT_T0_T1_EEPKS6_RKS9_
              (&local_100,&DAT_0a3ddc72,&local_308);
    if ((DAT_0a3ddca1 & 1) == 0) {
      DAT_0a3ddc98._0_1_ = s_prepared__count_ler__088baa10[8];
      DAT_0a3ddc98._1_1_ = s_prepared__count_ler__088baa10[9];
      DAT_0a3ddc98._2_1_ = s_prepared__count_ler__088baa10[10];
      DAT_0a3ddc98._3_1_ = s_prepared__count_ler__088baa10[0xb];
      DAT_0a3ddc98._4_1_ = s_prepared__count_ler__088baa10[0xc];
      DAT_0a3ddc98._5_1_ = s_prepared__count_ler__088baa10[0xd];
      DAT_0a3ddc98._6_1_ = s_prepared__count_ler__088baa10[0xe];
      DAT_0a3ddc98._7_1_ = s_prepared__count_ler__088baa10[0xf];
      DAT_0a3ddca0 = 0;
      DAT_0a3ddca1 = 1;
    }
    puVar11 = (undefined8 *)
              __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKc
                        (&local_100,&DAT_0a3ddc98);
    plStack_278 = (long *)puVar11[1];
    local_280 = (long *******)*puVar11;
    local_270 = puVar11[2];
    puVar11[1] = 0;
    puVar11[2] = 0;
    *puVar11 = 0;
    __ZNSt3__19to_stringEm
              (&local_150,((long)local_2e8 - (long)local_2f0 >> 3) * -0x6474a8819ec8e951);
    uVar14 = CONCAT71(local_148._1_7_,(undefined1)local_148);
    ppppppplVar12 = local_150;
    if (-1 < (char)bStack_139) {
      uVar14 = (ulong)bStack_139;
      ppppppplVar12 = (long *******)&local_150;
    }
    puVar11 = (undefined8 *)
              __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
                        (&local_280,ppppppplVar12,uVar14);
    uStack_3e8 = puVar11[1];
    local_3f0 = *puVar11;
    local_3e0 = puVar11[2];
    puVar11[1] = 0;
    puVar11[2] = 0;
    *puVar11 = 0;
    FUN_02ac5bf8(&local_2c0,&local_3f0,0);
    if ((long)local_3e0 < 0) {
      __ZdlPvm(local_3f0,local_3e0 & 0x7fffffffffffffff);
    }
    if ((char)bStack_139 < '\0') {
      __ZdlPvm(local_150,CONCAT17(bStack_139,local_140) & 0x7fffffffffffffff);
    }
    if ((long)local_270 < 0) {
      __ZdlPvm(local_280,local_270 & 0x7fffffffffffffff);
    }
    iVar10 = thunk_FUN_05e1d97c(2);
    if (iVar10 != 0) {
      FUN_0488143c(&local_420);
      ppppppplVar12 = local_420;
      if (-1 < (long)local_410) {
        ppppppplVar12 = (long *******)&local_420;
      }
      if ((DAT_0a3dd363 & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3dd350)[uVar14] = (&DAT_088bce97)[uVar14] + 0x8a ^ (&DAT_088bce87)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x13);
        DAT_0a3dd363 = 1;
      }
      if ((DAT_0a3ddada & 1) == 0) {
        _DAT_0a3ddac0 = CONCAT44((int)DAT_088baa00,(int)DAT_087ef190);
        uRam000000000a3ddac8 = CONCAT44((int)DAT_084a8110,(int)DAT_0852d550);
        DAT_0a3ddad0 = CONCAT44((int)DAT_088baa08,(int)DAT_084e7040);
        DAT_0a3ddad8 = 0x62;
        DAT_0a3ddada = 1;
      }
      FUN_05e1d050(&local_280,2,ppppppplVar12,&DAT_0a3dd350,&DAT_0a3ddac0,800,0,0);
      local_150 = local_308;
      if (-1 < (long)local_2f8) {
        local_150 = (long *******)&local_308;
      }
      local_148._0_1_ = 0;
      local_1a0 = (long *******)0x0;
      if ((DAT_0a3e2eba & 1) == 0) {
        uVar14 = 0;
        do {
          uVar23 = *(undefined4 *)((long)&DAT_088c56c9 + uVar14);
          uVar3 = CONCAT12((char)((uint)uVar23 >> 8),(short)uVar23) & 0xff00ff;
          uVar26 = *(undefined4 *)((long)&DAT_088c56b5 + uVar14 % 0x14);
          *(uint *)((long)&DAT_0a3e2e72 + uVar14) =
               CONCAT13((char)((uint)uVar23 >> 0x18) + 0x69U ^ (byte)((uint)uVar26 >> 0x18),
                        CONCAT12((char)((uint)uVar23 >> 0x10) + 0x69U ^ (byte)((uint)uVar26 >> 0x10)
                                 ,CONCAT11((char)(uVar3 >> 0x10) + 0x69U ^ (byte)((uint)uVar26 >> 8)
                                           ,(char)uVar3 + 0x69U ^ (byte)uVar26)));
          uVar14 = uVar14 + 4;
        } while (uVar14 != 0x48);
        DAT_0a3e2eba = 1;
      }
      uVar14 = ((long)local_2e8 - (long)local_2f0 >> 3) * -0x6474a8819ec8e951;
      lVar7 = 0;
      do {
        lVar8 = lVar7;
        *(undefined1 *)((long)&local_198 + lVar8) = (&DAT_0a3e2e95)[uVar14 % 10];
        bVar5 = 9 < uVar14;
        uVar14 = uVar14 / 10;
        lVar7 = lVar8 + 1;
      } while (bVar5);
      *(undefined1 *)((long)&local_198 + lVar8 + 1) = 0;
      if (8 < lVar8 + 8U) {
        puVar15 = (undefined1 *)((long)&local_198 + lVar8);
        puVar6 = (undefined1 *)((long)&local_198 + 1);
        do {
          uVar2 = *puVar15;
          *puVar15 = puVar6[-1];
          puVar6[-1] = uVar2;
          bVar5 = puVar6 < puVar15 + -1;
          puVar15 = puVar15 + -1;
          puVar6 = puVar6 + 1;
        } while (bVar5);
      }
      local_1a0 = (long *******)&local_198;
      local_1f0 = (long *******)&uStack_1e8;
      lVar7 = 0;
      uVar14 = ((long)local_3c8 - (long)local_3d0 >> 3) * -0x6474a8819ec8e951;
      do {
        lVar8 = lVar7;
        *(undefined1 *)((long)&uStack_1e8 + lVar8) = (&DAT_0a3e2e95)[uVar14 % 10];
        bVar5 = 9 < uVar14;
        lVar7 = lVar8 + 1;
        uVar14 = uVar14 / 10;
      } while (bVar5);
      *(undefined1 *)((long)&uStack_1e8 + lVar8 + 1) = 0;
      if (8 < lVar8 + 8U) {
        puVar15 = (undefined1 *)((long)&uStack_1e8 + lVar8);
        puVar6 = (undefined1 *)((long)&uStack_1e8 + 1);
        do {
          uVar2 = *puVar15;
          *puVar15 = puVar6[-1];
          puVar6[-1] = uVar2;
          bVar5 = puVar6 < puVar15 + -1;
          puVar15 = puVar15 + -1;
          puVar6 = puVar6 + 1;
        } while (bVar5);
      }
      if ((DAT_0a3ddcf6 & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3ddca2)[uVar14] = (&DAT_088bda97)[uVar14] + 0x8a ^ (&DAT_088bda87)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x54);
        DAT_0a3ddcf6 = 1;
      }
      local_100 = (long *******)&local_150;
      ppppppplStack_f8 = (long *******)&local_1a0;
      local_f0 = &local_1f0;
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
      local_90 = 0;
      uStack_98 = 0;
      uStack_88 = 0;
      FUN_05e1d31c(&local_280,&DAT_0a3ddca2,&local_100);
      thunk_FUN_05e1d0bc(&local_280);
      if ((long)local_410 < 0) {
        __ZdlPvm(local_420,(ulong)local_410 & 0x7fffffffffffffff);
      }
    }
    ppppppplVar19 = local_3c8;
    lStack_418 = 0;
    local_420 = (long *******)0x0;
    uStack_408 = 0;
    local_410 = (long *)0x0;
    local_400 = 0xaaaaaaaa3f800000;
    for (ppppppplVar12 = local_3d0; ppppppplVar12 != ppppppplVar19;
        ppppppplVar12 = ppppppplVar12 + 0x4f) {
      local_280 = ppppppplVar12 + 0x4c;
      lVar7 = FUN_03214bf4(&local_420,local_280,&DAT_08b7a8b8,&local_280,&local_100);
      FUN_0318de00(lVar7 + 0x28,ppppppplVar12);
    }
    local_438 = (long *)0x0;
    local_430 = (long *)0x0;
    local_428 = (long *)0x0;
    FUN_0110ddc8(&local_438,(long)local_2d0 - (long)local_2d8 >> 4);
    plVar13 = local_2d0;
    if (local_2d8 == local_2d0) {
LAB_0318bf48:
      if (local_438 == local_430) goto LAB_0318c1a8;
      if ((DAT_0a3ddd94 & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3ddd7f)[uVar14] = (&DAT_088bdba1)[uVar14] + 0x8a ^ (&DAT_088bdb91)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x15);
        DAT_0a3ddd94 = 1;
      }
      FUN_00ebbf48(&local_2c0,&DAT_0a3ddd7f,0);
      lVar7 = *param_3;
      if (*(char *)(lVar7 + 0x50) == '\x01') {
        FUN_03214a20(lVar7 + 0x38,&local_438);
        iVar10 = thunk_FUN_05e1d97c(2);
        if (iVar10 != 0) {
          FUN_0488143c(&local_1f0);
          ppppppplVar12 = local_1f0;
          if (-1 < (long)local_1e0) {
            ppppppplVar12 = (long *******)&local_1f0;
          }
          if ((DAT_0a3dd363 & 1) == 0) {
            uVar14 = 0;
            do {
              (&DAT_0a3dd350)[uVar14] =
                   (&DAT_088bce97)[uVar14] + 0x8a ^ (&DAT_088bce87)[uVar14 & 0xf];
              uVar14 = uVar14 + 1;
            } while (uVar14 != 0x13);
            DAT_0a3dd363 = 1;
          }
          if ((DAT_0a3ddada & 1) == 0) {
            _DAT_0a3ddac0 = CONCAT44((int)DAT_088baa00,(int)DAT_087ef190);
            uRam000000000a3ddac8 = CONCAT44((int)DAT_084a8110,(int)DAT_0852d550);
            DAT_0a3ddad0 = CONCAT44((int)DAT_088baa08,(int)DAT_084e7040);
            DAT_0a3ddad8 = 0x62;
            DAT_0a3ddada = 1;
          }
          FUN_05e1d050(&local_280,2,ppppppplVar12,&DAT_0a3dd350,&DAT_0a3ddac0,0x34c,0,0);
          FUN_005fc8cc(&local_150,*(long *)(*param_3 + 0x40) - *(long *)(*param_3 + 0x38) >> 6,10);
          FUN_005fc8cc(&local_1a0,*(long *)(*param_3 + 0x28) - *(long *)(*param_3 + 0x20) >> 6,10);
          if ((DAT_0a3dddf2 & 1) == 0) {
            uVar14 = 0;
            do {
              (&DAT_0a3ddd95)[uVar14] =
                   (&DAT_088bdbc6)[uVar14] + 0x8a ^ (&DAT_088bdbb6)[uVar14 & 0xf];
              uVar14 = uVar14 + 1;
            } while (uVar14 != 0x5d);
            DAT_0a3dddf2 = 1;
          }
          local_100 = (long *******)&local_150;
          ppppppplStack_f8 = (long *******)&local_1a0;
          uStack_e8 = 0;
          local_f0 = (undefined8 *)0x0;
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
          uStack_88 = 0;
          local_90 = 0;
          FUN_05e1d31c(&local_280,&DAT_0a3ddd95,&local_100);
LAB_0318cb84:
          thunk_FUN_05e1d0bc(&local_280);
          if ((long)local_1e0 < 0) {
            __ZdlPvm(local_1f0,(ulong)local_1e0 & 0x7fffffffffffffff);
          }
        }
      }
      else {
        plVar20 = *(long **)(lVar7 + 0x28);
        plVar13 = local_430;
        for (plVar18 = *(long **)(lVar7 + 0x20); local_430 = plVar13, plVar18 != plVar20;
            plVar18 = plVar18 + 8) {
          if (plVar13 < local_428) {
            if (*(char *)((long)plVar18 + 0x17) < '\0') {
              FUN_00018d20(plVar13,*plVar18,plVar18[1]);
            }
            else {
              lVar8 = plVar18[1];
              lVar7 = *plVar18;
              plVar13[2] = plVar18[2];
              plVar13[1] = lVar8;
              *plVar13 = lVar7;
            }
            lVar7 = plVar18[3];
            plVar13[4] = plVar18[4];
            plVar13[3] = lVar7;
            if (*(char *)((long)plVar18 + 0x3f) < '\0') {
              FUN_00018d20(plVar13 + 5,plVar18[5],plVar18[6]);
            }
            else {
              lVar8 = plVar18[6];
              lVar7 = plVar18[5];
              plVar13[7] = plVar18[7];
              plVar13[6] = lVar8;
              plVar13[5] = lVar7;
            }
            plVar13 = plVar13 + 8;
          }
          else {
            plVar13 = (long *)FUN_03213c1c(&local_438,plVar18);
          }
        }
        iVar10 = thunk_FUN_05e1d97c(2);
        if (iVar10 != 0) {
          FUN_0488143c(&local_1f0);
          ppppppplVar12 = local_1f0;
          if (-1 < (long)local_1e0) {
            ppppppplVar12 = (long *******)&local_1f0;
          }
          if ((DAT_0a3dd363 & 1) == 0) {
            uVar14 = 0;
            do {
              (&DAT_0a3dd350)[uVar14] =
                   (&DAT_088bce97)[uVar14] + 0x8a ^ (&DAT_088bce87)[uVar14 & 0xf];
              uVar14 = uVar14 + 1;
            } while (uVar14 != 0x13);
            DAT_0a3dd363 = 1;
          }
          if ((DAT_0a3ddada & 1) == 0) {
            _DAT_0a3ddac0 = CONCAT44((int)DAT_088baa00,(int)DAT_087ef190);
            uRam000000000a3ddac8 = CONCAT44((int)DAT_084a8110,(int)DAT_0852d550);
            DAT_0a3ddad0 = CONCAT44((int)DAT_088baa08,(int)DAT_084e7040);
            DAT_0a3ddad8 = 0x62;
            DAT_0a3ddada = 1;
          }
          FUN_05e1d050(&local_280,2,ppppppplVar12,&DAT_0a3dd350,&DAT_0a3ddac0,0x353,0,0);
          FUN_005fc8cc(&local_150,*(long *)(*param_3 + 0x28) - *(long *)(*param_3 + 0x20) >> 6,10);
          FUN_005fc8cc(&local_1a0,(long)local_430 - (long)local_438 >> 6,10);
          if ((DAT_0a3dde41 & 1) == 0) {
            uVar14 = 0;
            do {
              (&DAT_0a3dddf3)[uVar14] =
                   (&DAT_088bdc33)[uVar14] + 0x8a ^ (&DAT_088bdc23)[uVar14 & 0xf];
              uVar14 = uVar14 + 1;
            } while (uVar14 != 0x4e);
            DAT_0a3dde41 = 1;
          }
          local_100 = (long *******)&local_150;
          ppppppplStack_f8 = (long *******)&local_1a0;
          uStack_e8 = 0;
          local_f0 = (undefined8 *)0x0;
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
          uStack_88 = 0;
          local_90 = 0;
          FUN_05e1d31c(&local_280,&DAT_0a3dddf3,&local_100);
          thunk_FUN_05e1d0bc(&local_280);
          if ((long)local_1e0 < 0) {
            __ZdlPvm(local_1f0,(ulong)local_1e0 & 0x7fffffffffffffff);
          }
        }
        if (0x40 < (ulong)((long)local_430 - (long)local_438)) {
          FUN_0466aca8(&local_150);
          FUN_01205740(&local_100,local_150);
          FUN_0317f064(&local_280,local_100);
          FUN_03525950(local_280,&local_438,1,0);
          FUN_00129f68(&local_280);
          FUN_00129f68(&local_100);
          FUN_00129f68(&local_150);
          if ((DAT_0a3dde59 & 1) == 0) {
            uVar14 = 0;
            do {
              (&DAT_0a3dde42)[uVar14] =
                   (&DAT_088bdc91)[uVar14] + 0x8a ^ (&DAT_088bdc81)[uVar14 & 0xf];
              uVar14 = uVar14 + 1;
            } while (uVar14 != 0x17);
            DAT_0a3dde59 = 1;
          }
          FUN_00ebbf48(&local_2c0,&DAT_0a3dde42,0);
          iVar10 = thunk_FUN_05e1d97c(2);
          if (iVar10 != 0) {
            FUN_0488143c(&local_1f0);
            ppppppplVar12 = local_1f0;
            if (-1 < (long)local_1e0) {
              ppppppplVar12 = (long *******)&local_1f0;
            }
            if ((DAT_0a3dd363 & 1) == 0) {
              uVar14 = 0;
              do {
                (&DAT_0a3dd350)[uVar14] =
                     (&DAT_088bce97)[uVar14] + 0x8a ^ (&DAT_088bce87)[uVar14 & 0xf];
                uVar14 = uVar14 + 1;
              } while (uVar14 != 0x13);
              DAT_0a3dd363 = 1;
            }
            if ((DAT_0a3ddada & 1) == 0) {
              _DAT_0a3ddac0 = CONCAT44((int)DAT_088baa00,(int)DAT_087ef190);
              uRam000000000a3ddac8 = CONCAT44((int)DAT_084a8110,(int)DAT_0852d550);
              DAT_0a3ddad0 = CONCAT44((int)DAT_088baa08,(int)DAT_084e7040);
              DAT_0a3ddad8 = 0x62;
              DAT_0a3ddada = 1;
            }
            FUN_05e1d050(&local_280,2,ppppppplVar12,&DAT_0a3dd350,&DAT_0a3ddac0,0x357,0,0);
            local_150 = local_308;
            if (-1 < (long)local_2f8) {
              local_150 = (long *******)&local_308;
            }
            local_148._0_1_ = 0;
            FUN_005fc8cc(&local_1a0,(long)local_430 - (long)local_438 >> 6,10);
            if ((DAT_0a3dde9c & 1) == 0) {
              uVar14 = 0;
              do {
                (&DAT_0a3dde5a)[uVar14] =
                     (&DAT_088bdcb8)[uVar14] + 0x8a ^ (&DAT_088bdca8)[uVar14 & 0xf];
                uVar14 = uVar14 + 1;
              } while (uVar14 != 0x42);
              DAT_0a3dde9c = 1;
            }
            local_100 = (long *******)&local_150;
            ppppppplStack_f8 = (long *******)&local_1a0;
            uStack_e8 = 0;
            local_f0 = (undefined8 *)0x0;
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
            uStack_88 = 0;
            local_90 = 0;
            FUN_05e1d31c(&local_280,&DAT_0a3dde5a,&local_100);
            goto LAB_0318cb84;
          }
        }
      }
      iVar10 = thunk_FUN_05e1d97c(2);
      if (iVar10 != 0) {
        FUN_0488143c(&local_1f0);
        ppppppplVar12 = local_1f0;
        if (-1 < (long)local_1e0) {
          ppppppplVar12 = (long *******)&local_1f0;
        }
        if ((DAT_0a3dd363 & 1) == 0) {
          uVar14 = 0;
          do {
            (&DAT_0a3dd350)[uVar14] = (&DAT_088bce97)[uVar14] + 0x8a ^ (&DAT_088bce87)[uVar14 & 0xf]
            ;
            uVar14 = uVar14 + 1;
          } while (uVar14 != 0x13);
          DAT_0a3dd363 = 1;
        }
        if ((DAT_0a3ddada & 1) == 0) {
          _DAT_0a3ddac0 = CONCAT44((int)DAT_088baa00,(int)DAT_087ef190);
          uRam000000000a3ddac8 = CONCAT44((int)DAT_084a8110,(int)DAT_0852d550);
          DAT_0a3ddad0 = CONCAT44((int)DAT_088baa08,(int)DAT_084e7040);
          DAT_0a3ddad8 = 0x62;
          DAT_0a3ddada = 1;
        }
        FUN_05e1d050(&local_280,2,ppppppplVar12,&DAT_0a3dd350,&DAT_0a3ddac0,0x35b,0,0);
        local_150 = local_308;
        if (-1 < (long)local_2f8) {
          local_150 = (long *******)&local_308;
        }
        local_148._0_1_ = 0;
        FUN_005fc8cc(&local_1a0,((long *)*param_3)[1] - *(long *)*param_3 >> 4,10);
        if ((DAT_0a3ddedc & 1) == 0) {
          uVar14 = 0;
          do {
            (&DAT_0a3dde9d)[uVar14] = (&DAT_088bdd0a)[uVar14] + 0x8a ^ (&DAT_088bdcfa)[uVar14 & 0xf]
            ;
            uVar14 = uVar14 + 1;
          } while (uVar14 != 0x3f);
          DAT_0a3ddedc = 1;
        }
        local_100 = (long *******)&local_150;
        ppppppplStack_f8 = (long *******)&local_1a0;
        uStack_e8 = 0;
        local_f0 = (undefined8 *)0x0;
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
        uStack_88 = 0;
        local_90 = 0;
        FUN_05e1d31c(&local_280,&DAT_0a3dde9d,&local_100);
        thunk_FUN_05e1d0bc(&local_280);
        if ((long)local_1e0 < 0) {
          __ZdlPvm(local_1f0,(ulong)local_1e0 & 0x7fffffffffffffff);
        }
      }
    }
    else {
      uVar26 = (undefined4)DAT_088baa00;
      uVar24 = (undefined4)DAT_087ef190;
      uVar23 = (undefined4)DAT_0852d550;
      uVar21 = (undefined4)DAT_084a8110;
      uVar22 = (undefined4)DAT_088baa08;
      uVar25 = (undefined4)DAT_084e7040;
      bVar5 = true;
      plVar18 = local_2d8;
      do {
        lVar7 = *(long *)(*plVar18 + 0x18);
        local_440 = *(long **)(*plVar18 + 0x20);
        lVar8 = 0;
        if (local_440 != (long *)0x0) {
          lVar8 = local_440[1];
          local_440[1] = lVar8 + 1;
        }
        local_448 = lVar7;
        if (lVar7 != 0) {
          lVar8 = FUN_032150fc(lVar8,&local_420,(long *******)(lVar7 + 0x260));
          lVar16 = (long)*(char *)(lVar7 + 0x277);
          if (lVar16 < 0) {
            lVar16 = *(long *)(lVar7 + 0x268);
          }
          if ((lVar16 == 0 || lVar8 == 0) || (*(int *)(lVar8 + 0x11c) == 0)) {
            iVar10 = thunk_FUN_05e1d97c(4);
            if (iVar10 == 0) {
              bVar5 = false;
            }
            else {
              FUN_0488143c(&local_460);
              ppppppplVar12 = local_460;
              if (-1 < cStack_449) {
                ppppppplVar12 = (long *******)&local_460;
              }
              if ((DAT_0a3dd363 & 1) == 0) {
                uVar14 = 0;
                do {
                  (&DAT_0a3dd350)[uVar14] =
                       (&DAT_088bce97)[uVar14] + 0x8a ^ (&DAT_088bce87)[uVar14 & 0xf];
                  uVar14 = uVar14 + 1;
                } while (uVar14 != 0x13);
                DAT_0a3dd363 = 1;
              }
              if ((DAT_0a3ddada & 1) == 0) {
                DAT_0a3ddad8 = 0x62;
                DAT_0a3ddada = 1;
                _DAT_0a3ddac0 = CONCAT44(uVar26,uVar24);
                uRam000000000a3ddac8 = CONCAT44(uVar21,uVar23);
                DAT_0a3ddad0 = CONCAT44(uVar22,uVar25);
              }
              FUN_05e1d050(&local_280,4,ppppppplVar12,&DAT_0a3dd350,&DAT_0a3ddac0,0x33b,0,0);
              FUN_030f1f08(&local_478,*plVar18);
              local_150 = local_478;
              if (-1 < cStack_461) {
                local_150 = (long *******)&local_478;
              }
              local_148._0_1_ = 0;
              local_1a0 = local_308;
              if (-1 < (long)local_2f8) {
                local_1a0 = (long *******)&local_308;
              }
              local_198._0_1_ = 0;
              local_1f0 = *(long ********)(lVar7 + 0x260);
              if (-1 < *(char *)(lVar7 + 0x277)) {
                local_1f0 = (long *******)(lVar7 + 0x260);
              }
              uStack_1e8 = (long *******)((ulong)uStack_1e8 & 0xffffffffffffff00);
              if ((DAT_0a3ddd3c & 1) == 0) {
                uVar14 = 0;
                do {
                  (&DAT_0a3ddcf7)[uVar14] =
                       (&DAT_088bdafb)[uVar14] + 0x8a ^ (&DAT_088bdaeb)[uVar14 & 0xf];
                  uVar14 = uVar14 + 1;
                } while (uVar14 != 0x45);
                DAT_0a3ddd3c = 1;
              }
              local_100 = (long *******)&local_150;
              ppppppplStack_f8 = (long *******)&local_1a0;
              local_f0 = &local_1f0;
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
              local_90 = 0;
              uStack_98 = 0;
              uStack_88 = 0;
              FUN_05e1d31c(&local_280,&DAT_0a3ddcf7,&local_100);
              if (cStack_461 < '\0') {
                __ZdlPvm(local_478,CONCAT17(cStack_461,local_468) & 0x7fffffffffffffff);
              }
              thunk_FUN_05e1d0bc(&local_280);
              if (cStack_449 < '\0') {
                __ZdlPvm(local_460,CONCAT17(cStack_449,local_450) & 0x7fffffffffffffff);
              }
              bVar5 = false;
            }
          }
          else {
            ppppppplVar12 = (long *******)__Znwm(0x290);
            ppppppplVar19 = ppppppplVar12 + 1;
            *ppppppplVar19 = (long ******)0x0;
            ppppppplVar12[2] = (long ******)0x0;
            *ppppppplVar12 = (long ******)&PTR_FUN_09c92390;
            local_100 = (long *******)FUN_00f57630(ppppppplVar12 + 3,lVar8 + 0x28);
            lVar7 = *plVar18;
            if (ppppppplVar12 != (long *******)0x0) {
              *ppppppplVar19 = (long ******)((long)*ppppppplVar19 + 1);
              *ppppppplVar19 = (long ******)((long)*ppppppplVar19 + 1);
            }
            plVar20 = *(long **)(lVar7 + 0x20);
            *(long ********)(lVar7 + 0x18) = local_100;
            *(long ********)(lVar7 + 0x20) = ppppppplVar12;
            ppppppplStack_f8 = ppppppplVar12;
            if (plVar20 != (long *)0x0) {
              LOAcquire();
              lVar7 = plVar20[1];
              plVar20[1] = lVar7 + -1;
              LORelease();
              if (lVar7 == 0) {
                (**(code **)(*plVar20 + 0x10))(plVar20);
                __ZNSt3__119__shared_weak_count14__release_weakEv(plVar20);
              }
            }
            if (ppppppplVar12 != (long *******)0x0) {
              LOAcquire();
              pppppplVar9 = *ppppppplVar19;
              *ppppppplVar19 = (long ******)((long)pppppplVar9 + -1);
              LORelease();
              if (pppppplVar9 == (long ******)0x0) {
                (*(code *)(*ppppppplVar12)[2])(ppppppplVar12);
                __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar12);
              }
            }
            thunk_FUN_04d310bc(&local_280,local_100);
            if (local_430 < local_428) {
              local_430[2] = local_270;
              local_430[1] = (long)plStack_278;
              *local_430 = (long)local_280;
              local_270 = 0;
              plStack_278 = (long *)0x0;
              local_280 = (long *******)0x0;
              local_430[4] = lStack_260;
              local_430[3] = CONCAT17(cStack_261,local_268);
              local_430[6] = lStack_250;
              local_430[5] = (long)local_258;
              local_430[7] = local_248;
              lStack_250 = 0;
              local_248 = 0;
              local_258 = (long *)0x0;
              local_430 = local_430 + 8;
              ppppppplVar12 = ppppppplStack_f8;
            }
            else {
              local_430 = (long *)FUN_0321528c(&local_438,&local_280);
              if ((long)local_248 < 0) {
                __ZdlPvm(local_258,local_248 & 0x7fffffffffffffff);
              }
              ppppppplVar12 = ppppppplStack_f8;
              if ((long)local_270 < 0) {
                __ZdlPvm(local_280,local_270 & 0x7fffffffffffffff);
                ppppppplVar12 = ppppppplStack_f8;
              }
            }
            ppppppplStack_f8 = ppppppplVar12;
            if (ppppppplVar12 != (long *******)0x0) {
              LOAcquire();
              pppppplVar9 = ppppppplVar12[1];
              ppppppplVar12[1] = (long ******)((long)pppppplVar9 + -1);
              LORelease();
              if (pppppplVar9 == (long ******)0x0) {
                (*(code *)(*ppppppplVar12)[2])(ppppppplVar12);
                __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar12);
              }
            }
          }
        }
        plVar20 = local_440;
        if (local_440 != (long *)0x0) {
          LOAcquire();
          lVar7 = local_440[1];
          local_440[1] = lVar7 + -1;
          LORelease();
          if (lVar7 == 0) {
            (**(code **)(*local_440 + 0x10))(local_440);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar20);
          }
        }
        plVar18 = plVar18 + 2;
      } while (plVar18 != plVar13);
      if (bVar5) goto LAB_0318bf48;
LAB_0318c1a8:
      iVar10 = thunk_FUN_05e1d97c(4);
      if (iVar10 != 0) {
        FUN_0488143c(&local_460);
        ppppppplVar12 = local_460;
        if (-1 < cStack_449) {
          ppppppplVar12 = (long *******)&local_460;
        }
        if ((DAT_0a3dd363 & 1) == 0) {
          uVar14 = 0;
          do {
            (&DAT_0a3dd350)[uVar14] = (&DAT_088bce97)[uVar14] + 0x8a ^ (&DAT_088bce87)[uVar14 & 0xf]
            ;
            uVar14 = uVar14 + 1;
          } while (uVar14 != 0x13);
          DAT_0a3dd363 = 1;
        }
        if ((DAT_0a3ddada & 1) == 0) {
          _DAT_0a3ddac0 = CONCAT44((int)DAT_088baa00,(int)DAT_087ef190);
          uRam000000000a3ddac8 = CONCAT44((int)DAT_084a8110,(int)DAT_0852d550);
          DAT_0a3ddad0 = CONCAT44((int)DAT_088baa08,(int)DAT_084e7040);
          DAT_0a3ddad8 = 0x62;
          DAT_0a3ddada = 1;
        }
        FUN_05e1d050(&local_280,4,ppppppplVar12,&DAT_0a3dd350,&DAT_0a3ddac0,0x340,0,0);
        local_150 = local_308;
        if (-1 < (long)local_2f8) {
          local_150 = (long *******)&local_308;
        }
        local_148._0_1_ = 0;
        local_1a0 = (long *******)0x0;
        if ((DAT_0a3e2eba & 1) == 0) {
          uVar14 = 0;
          do {
            uVar23 = *(undefined4 *)((long)&DAT_088c56c9 + uVar14);
            uVar3 = CONCAT12((char)((uint)uVar23 >> 8),(short)uVar23) & 0xff00ff;
            uVar26 = *(undefined4 *)((long)&DAT_088c56b5 + uVar14 % 0x14);
            *(uint *)((long)&DAT_0a3e2e72 + uVar14) =
                 CONCAT13((char)((uint)uVar23 >> 0x18) + 0x69U ^ (byte)((uint)uVar26 >> 0x18),
                          CONCAT12((char)((uint)uVar23 >> 0x10) + 0x69U ^
                                   (byte)((uint)uVar26 >> 0x10),
                                   CONCAT11((char)(uVar3 >> 0x10) + 0x69U ^
                                            (byte)((uint)uVar26 >> 8),
                                            (char)uVar3 + 0x69U ^ (byte)uVar26)));
            uVar14 = uVar14 + 4;
          } while (uVar14 != 0x48);
          DAT_0a3e2eba = 1;
        }
        uVar14 = ((long)local_2e8 - (long)local_2f0 >> 3) * -0x6474a8819ec8e951;
        lVar7 = 0;
        do {
          lVar8 = lVar7;
          *(undefined1 *)((long)&local_198 + lVar8) = (&DAT_0a3e2e95)[uVar14 % 10];
          bVar5 = 9 < uVar14;
          uVar14 = uVar14 / 10;
          lVar7 = lVar8 + 1;
        } while (bVar5);
        *(undefined1 *)((long)&local_198 + lVar8 + 1) = 0;
        if (8 < lVar8 + 8U) {
          puVar15 = (undefined1 *)((long)&local_198 + lVar8);
          puVar6 = (undefined1 *)((long)&local_198 + 1);
          do {
            uVar2 = *puVar15;
            *puVar15 = puVar6[-1];
            puVar6[-1] = uVar2;
            bVar5 = puVar6 < puVar15 + -1;
            puVar15 = puVar15 + -1;
            puVar6 = puVar6 + 1;
          } while (bVar5);
        }
        local_1a0 = (long *******)&local_198;
        local_1f0 = (long *******)&uStack_1e8;
        lVar7 = 0;
        uVar14 = (long)local_430 - (long)local_438 >> 6;
        do {
          lVar8 = lVar7;
          *(undefined1 *)((long)&uStack_1e8 + lVar8) = (&DAT_0a3e2e95)[uVar14 % 10];
          bVar5 = 9 < uVar14;
          lVar7 = lVar8 + 1;
          uVar14 = uVar14 / 10;
        } while (bVar5);
        *(undefined1 *)((long)&uStack_1e8 + lVar8 + 1) = 0;
        if (8 < lVar8 + 8U) {
          puVar15 = (undefined1 *)((long)&uStack_1e8 + lVar8);
          puVar6 = (undefined1 *)((long)&uStack_1e8 + 1);
          do {
            uVar2 = *puVar15;
            *puVar15 = puVar6[-1];
            puVar6[-1] = uVar2;
            bVar5 = puVar6 < puVar15 + -1;
            puVar15 = puVar15 + -1;
            puVar6 = puVar6 + 1;
          } while (bVar5);
        }
        if ((DAT_0a3ddd7e & 1) == 0) {
          uVar14 = 0;
          do {
            (&DAT_0a3ddd3d)[uVar14] = (&DAT_088bdb50)[uVar14] + 0x8a ^ (&DAT_088bdb40)[uVar14 & 0xf]
            ;
            uVar14 = uVar14 + 1;
          } while (uVar14 != 0x41);
          DAT_0a3ddd7e = 1;
        }
        local_100 = (long *******)&local_150;
        ppppppplStack_f8 = (long *******)&local_1a0;
        local_f0 = &local_1f0;
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
        local_90 = 0;
        uStack_98 = 0;
        uStack_88 = 0;
        FUN_05e1d31c(&local_280,&DAT_0a3ddd3d,&local_100);
        thunk_FUN_05e1d0bc(&local_280);
        if (cStack_449 < '\0') {
          __ZdlPvm(local_460,CONCAT17(cStack_449,local_450) & 0x7fffffffffffffff);
        }
      }
      FUN_030f6640(&local_280,1,1);
      lVar7 = param_1[4];
      FUN_030f67ac(lVar7,&local_280);
      *(undefined8 *)(lVar7 + 0x48) = local_238;
      *(undefined4 *)((long)param_1 + 4) = 0;
      if ((local_240 & 1) == 0) {
        *(undefined4 *)param_1 = 4;
      }
      else {
        if ((long)local_248 < 0) {
          __ZdlPvm(local_258,local_248 & 0x7fffffffffffffff);
        }
        if ((long)local_270 < 0) {
          __ZdlPvm(local_280,local_270 & 0x7fffffffffffffff);
        }
        *(undefined4 *)param_1 = 4;
        if (*(int *)((long)param_1 + 4) != 0) goto LAB_0318cd8c;
      }
      *(undefined4 *)((long)param_1 + 4) = 400;
    }
LAB_0318cd8c:
    ppppppplVar12 = local_420;
    plVar13 = local_410;
    if (local_438 != (long *)0x0) {
      for (; local_430 != local_438; local_430 = local_430 + -8) {
      }
      local_430 = local_438;
      __ZdlPvm(local_438,(long)local_428 - (long)local_438);
      ppppppplVar12 = local_420;
      plVar13 = local_410;
    }
    while (plVar13 != (long *)0x0) {
      lVar7 = *plVar13;
      local_420 = ppppppplVar12;
      FUN_00ac6290(plVar13 + 5);
      if (*(char *)((long)plVar13 + 0x27) < '\0') {
        __ZdlPvm(plVar13[2],plVar13[4] & 0x7fffffffffffffff);
      }
      __ZdlPvm(plVar13,0x2a0);
      ppppppplVar12 = local_420;
      plVar13 = (long *)lVar7;
    }
    local_420 = (long *******)0x0;
    if (ppppppplVar12 != (long *******)0x0) {
      __ZdlPvm(ppppppplVar12,lStack_418 << 3);
    }
    ppppppplVar19 = local_3d0;
    ppppppplVar12 = local_3c8;
    if (local_3d0 != (long *******)0x0) {
      while (ppppppplVar12 != ppppppplVar19) {
        ppppppplVar12 = ppppppplVar12 + -0x4f;
        (*(code *)**ppppppplVar12)(ppppppplVar12);
      }
      local_3c8 = ppppppplVar19;
      __ZdlPvm(local_3d0,(long)local_3c0 - (long)local_3d0);
    }
  }
LAB_0318ce74:
  if ((long)local_2f8 < 0) {
    __ZdlPvm(local_308,local_2f8 & 0x7fffffffffffffff);
  }
  puVar1 = local_2f0;
  puVar11 = local_2e8;
  if (local_2f0 != (undefined8 *)0x0) {
    while (puVar11 != puVar1) {
      puVar11 = puVar11 + -0x4f;
      (**(code **)*puVar11)(puVar11);
    }
    local_2e8 = puVar1;
    __ZdlPvm(local_2f0,(long)local_2e0 - (long)local_2f0);
  }
  plVar18 = local_2d8;
  plVar13 = local_2d0;
  if (local_2d8 != (long *)0x0) {
    for (; plVar13 != plVar18; plVar13 = plVar13 + -2) {
      plVar20 = (long *)plVar13[-1];
      if (plVar20 != (long *)0x0) {
        LOAcquire();
        lVar7 = plVar20[1];
        plVar20[1] = lVar7 + -1;
        LORelease();
        if (lVar7 == 0) {
          (**(code **)(*plVar20 + 0x10))(plVar20);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar20);
        }
      }
    }
    local_2d0 = plVar18;
    __ZdlPvm(local_2d8,(long)local_2c8 - (long)local_2d8);
  }
  if ((long)local_288 < 0) {
    __ZdlPvm(puStack_298,(ulong)local_288 & 0x7fffffffffffffff);
  }
LAB_0318cfa0:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_78) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


