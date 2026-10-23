// Ghidra inferred pseudocode; requested=0x317f1ec
// entry=0317f1ec end=0318138b

/* WARNING: Removing unreachable block (ram,0x03181310) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

bool FUN_0317f1ec(long param_1,long *param_2)

{
  long *******ppppppplVar1;
  long *plVar2;
  undefined1 uVar3;
  uint3 uVar4;
  bool bVar5;
  bool bVar6;
  long *****ppppplVar7;
  undefined8 ******ppppppuVar8;
  undefined1 *puVar9;
  int iVar10;
  uint uVar11;
  undefined8 *******pppppppuVar12;
  long lVar13;
  undefined8 *puVar14;
  undefined8 uVar15;
  undefined8 uVar16;
  ulong uVar17;
  long *******ppppppplVar18;
  undefined1 *puVar19;
  long lVar20;
  ulong uVar21;
  undefined1 *puVar22;
  long *plVar23;
  long *plVar24;
  long *******ppppppplVar25;
  long ******pppppplVar26;
  undefined4 uVar27;
  undefined4 uVar28;
  long ******pppppplVar29;
  long ******pppppplVar30;
  undefined4 uVar31;
  undefined4 uVar32;
  undefined4 uVar33;
  undefined4 uVar34;
  undefined4 uVar35;
  long local_348;
  long *local_340;
  undefined8 *******local_338 [2];
  undefined7 local_328;
  char cStack_321;
  long local_320;
  long *plStack_318;
  undefined8 local_310;
  undefined1 *puStack_308;
  undefined1 *local_300;
  undefined1 *puStack_2f8;
  undefined1 *local_2f0;
  long *local_2e8;
  long *local_2e0;
  long *local_2d8;
  long *local_2d0;
  long *******local_2c8;
  long *******local_2c0;
  long *******local_2b8;
  undefined8 local_2b0;
  undefined8 uStack_2a8;
  undefined8 uStack_2a0;
  undefined8 uStack_298;
  undefined8 local_290;
  long *******local_280;
  undefined8 *******pppppppuStack_278;
  long ******local_270;
  undefined1 *puStack_268;
  undefined1 *local_260;
  undefined1 *puStack_258;
  undefined1 *puStack_250;
  undefined1 *local_248;
  undefined1 *local_240;
  long *******local_1f0;
  undefined1 local_1e8;
  undefined7 local_1e0;
  char cStack_1d9;
  undefined8 *******local_1a0;
  undefined8 local_198;
  undefined7 local_190;
  char cStack_189;
  long *******local_150;
  undefined8 local_148;
  undefined7 local_140;
  char cStack_139;
  long *******local_100;
  undefined8 *******pppppppuStack_f8;
  long *******ppppppplStack_f0;
  undefined8 uStack_e8;
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
  long local_78;
  
  local_78 = *(long *)PTR____stack_chk_guard_09b36c98;
  if (*param_2 == param_2[1]) {
    iVar10 = thunk_FUN_05e1d97c(4);
    if (iVar10 != 0) {
      FUN_0488143c(&local_150);
      ppppppplVar18 = local_150;
      if (-1 < cStack_139) {
        ppppppplVar18 = (long *******)&local_150;
      }
      if ((DAT_0a3dd363 & 1) == 0) {
        uVar17 = 0;
        do {
          (&DAT_0a3dd350)[uVar17] = (&DAT_088bce97)[uVar17] + 0x8a ^ (&DAT_088bce87)[uVar17 & 0xf];
          uVar17 = uVar17 + 1;
        } while (uVar17 != 0x13);
        DAT_0a3dd363 = 1;
      }
      if ((DAT_0a3dd4f9 & 1) == 0) {
        _DAT_0a3dd4e4 = CONCAT44((int)DAT_088ba9b8,(int)DAT_08503670);
        uRam000000000a3dd4ec = CONCAT44((int)DAT_084b0670,(int)DAT_084916e8);
        DAT_0a3dd4f4 = (undefined4)DAT_08480ab8;
        DAT_0a3dd4f8 = 0;
        DAT_0a3dd4f9 = 1;
      }
      FUN_05e1d050(&local_280,4,ppppppplVar18,&DAT_0a3dd350,&DAT_0a3dd4e4,0x1b0,0,0);
      if ((DAT_0a3dd528 & 1) == 0) {
        uVar17 = 0;
        do {
          (&DAT_0a3dd4fa)[uVar17] = (&DAT_088bd0fa)[uVar17] + 0x8a ^ (&DAT_088bd0ea)[uVar17 & 0xf];
          uVar17 = uVar17 + 1;
        } while (uVar17 != 0x2e);
        DAT_0a3dd528 = 1;
      }
      local_98 = 0;
      uStack_a0 = 0;
      local_88 = 0;
      uStack_90 = 0;
      local_b8 = 0;
      uStack_c0 = 0;
      local_a8 = 0;
      uStack_b0 = 0;
      local_d8 = 0;
      uStack_e0 = 0;
      local_c8 = 0;
      uStack_d0 = 0;
      pppppppuStack_f8 = (undefined8 *******)0x0;
      local_100 = (long *******)0x0;
      uStack_e8 = 0;
      ppppppplStack_f0 = (long *******)0x0;
      FUN_05e1d31c(&local_280,&DAT_0a3dd4fa,&local_100);
      thunk_FUN_05e1d0bc(&local_280);
      if (cStack_139 < '\0') {
        __ZdlPvm(local_150,CONCAT17(cStack_139,local_140) & 0x7fffffffffffffff);
      }
    }
    bVar5 = false;
    goto LAB_03181344;
  }
  iVar10 = thunk_FUN_05e1d97c(2);
  if (iVar10 != 0) {
    FUN_0488143c(&local_1a0);
    pppppppuVar12 = local_1a0;
    if (-1 < cStack_189) {
      pppppppuVar12 = &local_1a0;
    }
    if ((DAT_0a3dd363 & 1) == 0) {
      uVar17 = 0;
      do {
        (&DAT_0a3dd350)[uVar17] = (&DAT_088bce97)[uVar17] + 0x8a ^ (&DAT_088bce87)[uVar17 & 0xf];
        uVar17 = uVar17 + 1;
      } while (uVar17 != 0x13);
      DAT_0a3dd363 = 1;
    }
    if ((DAT_0a3dd4f9 & 1) == 0) {
      _DAT_0a3dd4e4 = CONCAT44((int)DAT_088ba9b8,(int)DAT_08503670);
      uRam000000000a3dd4ec = CONCAT44((int)DAT_084b0670,(int)DAT_084916e8);
      DAT_0a3dd4f4 = (undefined4)DAT_08480ab8;
      DAT_0a3dd4f8 = 0;
      DAT_0a3dd4f9 = 1;
    }
    FUN_05e1d050(&local_280,2,pppppppuVar12,&DAT_0a3dd350,&DAT_0a3dd4e4,0x1b3,0,0);
    lVar13 = *param_2;
    lVar20 = param_2[1];
    local_150 = (long *******)0x0;
    local_150 = (long *******)&local_148;
    if ((DAT_0a3e2eba & 1) == 0) {
      uVar17 = 0;
      do {
        uVar31 = *(undefined4 *)((long)&DAT_088c56c9 + uVar17);
        uVar4 = CONCAT12((char)((uint)uVar31 >> 8),(short)uVar31) & 0xff00ff;
        uVar35 = *(undefined4 *)((long)&DAT_088c56b5 + uVar17 % 0x14);
        *(uint *)((long)&DAT_0a3e2e72 + uVar17) =
             CONCAT13((char)((uint)uVar31 >> 0x18) + 0x69U ^ (byte)((uint)uVar35 >> 0x18),
                      CONCAT12((char)((uint)uVar31 >> 0x10) + 0x69U ^ (byte)((uint)uVar35 >> 0x10),
                               CONCAT11((char)(uVar4 >> 0x10) + 0x69U ^ (byte)((uint)uVar35 >> 8),
                                        (char)uVar4 + 0x69U ^ (byte)uVar35)));
        uVar17 = uVar17 + 4;
      } while (uVar17 != 0x48);
      DAT_0a3e2eba = 1;
    }
    uVar17 = lVar20 - lVar13 >> 4;
    lVar13 = 0;
    do {
      lVar20 = lVar13;
      *(undefined1 *)((long)&local_148 + lVar20) = (&DAT_0a3e2e95)[uVar17 % 10];
      bVar5 = 9 < uVar17;
      uVar17 = uVar17 / 10;
      lVar13 = lVar20 + 1;
    } while (bVar5);
    *(undefined1 *)((long)&local_148 + lVar20 + 1) = 0;
    if (8 < lVar20 + 8U) {
      puVar19 = (undefined1 *)((long)&local_148 + lVar20);
      puVar9 = (undefined1 *)((long)&local_148 + 1);
      do {
        uVar3 = *puVar19;
        *puVar19 = puVar9[-1];
        puVar9[-1] = uVar3;
        bVar5 = puVar9 < puVar19 + -1;
        puVar19 = puVar19 + -1;
        puVar9 = puVar9 + 1;
      } while (bVar5);
    }
    if ((DAT_0a3dd550 & 1) == 0) {
      uVar17 = 0;
      do {
        (&DAT_0a3dd529)[uVar17] = (&DAT_088bd138)[uVar17] + 0x8a ^ (&DAT_088bd128)[uVar17 & 0xf];
        uVar17 = uVar17 + 1;
      } while (uVar17 != 0x27);
      DAT_0a3dd550 = 1;
    }
    ppppppplStack_f0 = (long *******)0x0;
    pppppppuStack_f8 = (undefined8 *******)0x0;
    local_100 = (long *******)&local_150;
    uStack_e0 = 0;
    uStack_e8 = 0;
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
    local_88 = 0;
    FUN_05e1d31c(&local_280,&DAT_0a3dd529,&local_100);
    thunk_FUN_05e1d0bc(&local_280);
    if (cStack_189 < '\0') {
      __ZdlPvm(local_1a0,CONCAT17(cStack_189,local_190) & 0x7fffffffffffffff);
    }
  }
  uVar16 = DAT_08480ab8;
  uStack_2a8 = 0;
  local_2b0 = 0;
  uStack_298 = 0;
  uStack_2a0 = 0;
  local_290 = 0xaaaaaaaa3f800000;
  local_2c8 = (long *******)0x0;
  local_2c0 = (long *******)0x0;
  local_2b8 = (long *******)0x0;
  local_2e0 = (long *)0x0;
  local_2d8 = (long *)0x0;
  local_2d0 = (long *)0x0;
  plVar24 = (long *)*param_2;
  plVar2 = (long *)param_2[1];
  if (plVar24 == plVar2) {
    bVar5 = true;
  }
  else {
    uVar35 = (undefined4)DAT_088ba9b8;
    uVar33 = (undefined4)DAT_08503670;
    uVar31 = (undefined4)DAT_084916e8;
    uVar27 = (undefined4)DAT_084b0670;
    bVar5 = true;
    do {
      uVar28 = (undefined4)uVar16;
      if ((long *)*plVar24 == (long *)0x0) {
        iVar10 = thunk_FUN_05e1d97c(4);
        if (iVar10 != 0) {
          FUN_0488143c(&local_150);
          ppppppplVar18 = local_150;
          if (-1 < cStack_139) {
            ppppppplVar18 = (long *******)&local_150;
          }
          if ((DAT_0a3dd363 & 1) == 0) {
            uVar17 = 0;
            do {
              (&DAT_0a3dd350)[uVar17] =
                   (&DAT_088bce97)[uVar17] + 0x8a ^ (&DAT_088bce87)[uVar17 & 0xf];
              uVar17 = uVar17 + 1;
            } while (uVar17 != 0x13);
            DAT_0a3dd363 = 1;
          }
          if ((DAT_0a3dd4f9 & 1) == 0) {
            DAT_0a3dd4f8 = 0;
            DAT_0a3dd4f9 = 1;
            _DAT_0a3dd4e4 = CONCAT44(uVar35,uVar33);
            uRam000000000a3dd4ec = CONCAT44(uVar27,uVar31);
            DAT_0a3dd4f4 = uVar28;
          }
          FUN_05e1d050(&local_280,4,ppppppplVar18,&DAT_0a3dd350,&DAT_0a3dd4e4,0x1c0,0,0);
          if ((DAT_0a3dd57b & 1) == 0) {
            uVar17 = 0;
            do {
              (&DAT_0a3dd551)[uVar17] =
                   (&DAT_088bd16f)[uVar17] + 0x8a ^ (&DAT_088bd15f)[uVar17 & 0xf];
              uVar17 = uVar17 + 1;
            } while (uVar17 != 0x2a);
            DAT_0a3dd57b = 1;
          }
          local_98 = 0;
          uStack_a0 = 0;
          local_88 = 0;
          uStack_90 = 0;
          local_b8 = 0;
          uStack_c0 = 0;
          local_a8 = 0;
          uStack_b0 = 0;
          local_d8 = 0;
          uStack_e0 = 0;
          local_c8 = 0;
          uStack_d0 = 0;
          pppppppuStack_f8 = (undefined8 *******)0x0;
          local_100 = (long *******)0x0;
          uStack_e8 = 0;
          ppppppplStack_f0 = (long *******)0x0;
          FUN_05e1d31c(&local_280,&DAT_0a3dd551,&local_100);
          thunk_FUN_05e1d0bc(&local_280);
          if (cStack_139 < '\0') {
            __ZdlPvm(local_150,CONCAT17(cStack_139,local_140) & 0x7fffffffffffffff);
          }
        }
        bVar5 = false;
      }
      else {
        (**(code **)(*(long *)*plVar24 + 0x10))();
        uVar17 = FUN_048a1fac();
        if ((uVar17 & 1) == 0) {
          iVar10 = thunk_FUN_05e1d97c(2);
          if (iVar10 != 0) {
            FUN_0488143c(&local_310);
            puVar14 = local_310;
            if (-1 < (long)local_300) {
              puVar14 = &local_310;
            }
            if ((DAT_0a3dd363 & 1) == 0) {
              uVar17 = 0;
              do {
                (&DAT_0a3dd350)[uVar17] =
                     (&DAT_088bce97)[uVar17] + 0x8a ^ (&DAT_088bce87)[uVar17 & 0xf];
                uVar17 = uVar17 + 1;
              } while (uVar17 != 0x13);
              DAT_0a3dd363 = 1;
            }
            if ((DAT_0a3dd4f9 & 1) == 0) {
              DAT_0a3dd4f8 = 0;
              DAT_0a3dd4f9 = 1;
              _DAT_0a3dd4e4 = CONCAT44(uVar35,uVar33);
              uRam000000000a3dd4ec = CONCAT44(uVar27,uVar31);
              DAT_0a3dd4f4 = uVar28;
            }
            FUN_05e1d050(&local_280,2,puVar14,&DAT_0a3dd350,&DAT_0a3dd4e4,0x1c8,0,0);
            uVar17 = (**(code **)(*(long *)*plVar24 + 0x10))();
            local_150 = (long *******)0x0;
            if ((DAT_0a3e2eba & 1) == 0) {
              uVar21 = 0;
              do {
                uVar34 = *(undefined4 *)((long)&DAT_088c56c9 + uVar21);
                uVar4 = CONCAT12((char)((uint)uVar34 >> 8),(short)uVar34) & 0xff00ff;
                uVar32 = *(undefined4 *)((long)&DAT_088c56b5 + uVar21 % 0x14);
                *(uint *)((long)&DAT_0a3e2e72 + uVar21) =
                     CONCAT13((char)((uint)uVar34 >> 0x18) + 0x69U ^ (byte)((uint)uVar32 >> 0x18),
                              CONCAT12((char)((uint)uVar34 >> 0x10) + 0x69U ^
                                       (byte)((uint)uVar32 >> 0x10),
                                       CONCAT11((char)(uVar4 >> 0x10) + 0x69U ^
                                                (byte)((uint)uVar32 >> 8),
                                                (char)uVar4 + 0x69U ^ (byte)uVar32)));
                uVar21 = uVar21 + 4;
              } while (uVar21 != 0x48);
              DAT_0a3e2eba = 1;
            }
            lVar13 = 0;
            do {
              lVar20 = lVar13;
              uVar11 = (uint)uVar17;
              *(undefined1 *)((long)&local_148 + lVar20) =
                   *(undefined1 *)
                    ((long)&DAT_0a3e2e72 +
                    (ulong)(uVar11 + (int)((uVar17 & 0xffffffff) / 10) * -10 + 0x23));
              uVar17 = (uVar17 & 0xffffffff) / 10;
              lVar13 = lVar20 + 1;
            } while (9 < uVar11);
            *(undefined1 *)((long)&local_148 + lVar20 + 1) = 0;
            if (8 < lVar20 + 8U) {
              puVar19 = (undefined1 *)((long)&local_148 + lVar20);
              puVar9 = (undefined1 *)((long)&local_148 + 1);
              do {
                uVar3 = *puVar19;
                *puVar19 = puVar9[-1];
                puVar9[-1] = uVar3;
                bVar6 = puVar9 < puVar19 + -1;
                puVar19 = puVar19 + -1;
                puVar9 = puVar9 + 1;
              } while (bVar6);
            }
            local_150 = (long *******)&local_148;
            uVar17 = (**(code **)(*(long *)*plVar24 + 0x18))();
            if ((DAT_0a3e2eba & 1) == 0) {
              uVar21 = 0;
              do {
                uVar34 = *(undefined4 *)((long)&DAT_088c56c9 + uVar21);
                uVar4 = CONCAT12((char)((uint)uVar34 >> 8),(short)uVar34) & 0xff00ff;
                uVar32 = *(undefined4 *)((long)&DAT_088c56b5 + uVar21 % 0x14);
                *(uint *)((long)&DAT_0a3e2e72 + uVar21) =
                     CONCAT13((char)((uint)uVar34 >> 0x18) + 0x69U ^ (byte)((uint)uVar32 >> 0x18),
                              CONCAT12((char)((uint)uVar34 >> 0x10) + 0x69U ^
                                       (byte)((uint)uVar32 >> 0x10),
                                       CONCAT11((char)(uVar4 >> 0x10) + 0x69U ^
                                                (byte)((uint)uVar32 >> 8),
                                                (char)uVar4 + 0x69U ^ (byte)uVar32)));
                uVar21 = uVar21 + 4;
              } while (uVar21 != 0x48);
              DAT_0a3e2eba = 1;
            }
            lVar13 = 0;
            do {
              lVar20 = lVar13;
              uVar11 = (uint)uVar17;
              *(undefined1 *)((long)&local_198 + lVar20) =
                   *(undefined1 *)
                    ((long)&DAT_0a3e2e72 +
                    (ulong)(uVar11 + (int)((uVar17 & 0xffffffff) / 10) * -10 + 0x23));
              uVar17 = (uVar17 & 0xffffffff) / 10;
              lVar13 = lVar20 + 1;
            } while (9 < uVar11);
            *(undefined1 *)((long)&local_198 + lVar20 + 1) = 0;
            if (8 < lVar20 + 8U) {
              puVar19 = (undefined1 *)((long)&local_198 + lVar20);
              puVar9 = (undefined1 *)((long)&local_198 + 1);
              do {
                uVar3 = *puVar19;
                *puVar19 = puVar9[-1];
                puVar9[-1] = uVar3;
                bVar6 = puVar9 < puVar19 + -1;
                puVar19 = puVar19 + -1;
                puVar9 = puVar9 + 1;
              } while (bVar6);
            }
            ppppppplVar18 = (long *******)(*plVar24 + 0x90);
            local_1f0 = (long *******)*ppppppplVar18;
            if (-1 < *(char *)(*plVar24 + 0xa7)) {
              local_1f0 = ppppppplVar18;
            }
            local_1e8 = 0;
            if ((DAT_0a3dd5ce & 1) == 0) {
              uVar17 = 0;
              do {
                (&DAT_0a3dd57c)[uVar17] =
                     (&DAT_088bd1a9)[uVar17] + 0x8a ^ (&DAT_088bd199)[uVar17 & 0xf];
                uVar17 = uVar17 + 1;
              } while (uVar17 != 0x52);
              DAT_0a3dd5ce = 1;
            }
            ppppppplStack_f0 = (long *******)&local_1f0;
            uStack_e0 = 0;
            uStack_e8 = 0;
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
            local_88 = 0;
            local_1a0 = (undefined8 *******)&local_198;
            local_100 = (long *******)&local_150;
            pppppppuStack_f8 = &local_1a0;
            FUN_05e1d31c(&local_280,&DAT_0a3dd57c,&local_100);
            thunk_FUN_05e1d0bc(&local_280);
            if ((long)local_300 < 0) {
              __ZdlPvm(local_310,(ulong)local_300 & 0x7fffffffffffffff);
            }
          }
          puStack_2f8 = &SUB_aaaaaaaaaaaaaaaa;
          local_300 = &SUB_aaaaaaaaaaaaaaaa;
          local_2e8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
          local_2f0 = &SUB_aaaaaaaaaaaaaaaa;
          puStack_308 = &SUB_aaaaaaaaaaaaaaaa;
          local_310 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
          local_320 = *plVar24;
          plVar23 = (long *)plVar24[1];
          if (plVar23 != (long *)0x0) {
            plVar23[1] = plVar23[1] + 1;
          }
          plStack_318 = plVar23;
          FUN_0317df64(&local_310,param_1,&local_320,1);
          if (plVar23 != (long *)0x0) {
            LOAcquire();
            lVar13 = plVar23[1];
            plVar23[1] = lVar13 + -1;
            LORelease();
            if (lVar13 == 0) {
              (**(code **)(*plVar23 + 0x10))(plVar23);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar23);
            }
          }
          if ((int)local_310 != 0 || local_310._4_4_ != 0) {
            iVar10 = thunk_FUN_05e1d97c(4);
            if (iVar10 != 0) {
              FUN_0488143c(local_338);
              pppppppuVar12 = local_338[0];
              if (-1 < cStack_321) {
                pppppppuVar12 = local_338;
              }
              if ((DAT_0a3dd363 & 1) == 0) {
                uVar17 = 0;
                do {
                  (&DAT_0a3dd350)[uVar17] =
                       (&DAT_088bce97)[uVar17] + 0x8a ^ (&DAT_088bce87)[uVar17 & 0xf];
                  uVar17 = uVar17 + 1;
                } while (uVar17 != 0x13);
                DAT_0a3dd363 = 1;
              }
              if ((DAT_0a3dd4f9 & 1) == 0) {
                DAT_0a3dd4f8 = 0;
                DAT_0a3dd4f9 = 1;
                _DAT_0a3dd4e4 = CONCAT44(uVar35,uVar33);
                uRam000000000a3dd4ec = CONCAT44(uVar27,uVar31);
                DAT_0a3dd4f4 = uVar28;
              }
              FUN_05e1d050(&local_280,4,pppppppuVar12,&DAT_0a3dd350,&DAT_0a3dd4e4,0x1cc,0,0);
              uVar17 = (**(code **)(*(long *)*plVar24 + 0x10))();
              local_150 = (long *******)0x0;
              if ((DAT_0a3e2eba & 1) == 0) {
                uVar21 = 0;
                do {
                  uVar28 = *(undefined4 *)((long)&DAT_088c56c9 + uVar21);
                  uVar4 = CONCAT12((char)((uint)uVar28 >> 8),(short)uVar28) & 0xff00ff;
                  uVar34 = *(undefined4 *)((long)&DAT_088c56b5 + uVar21 % 0x14);
                  *(uint *)((long)&DAT_0a3e2e72 + uVar21) =
                       CONCAT13((char)((uint)uVar28 >> 0x18) + 0x69U ^ (byte)((uint)uVar34 >> 0x18),
                                CONCAT12((char)((uint)uVar28 >> 0x10) + 0x69U ^
                                         (byte)((uint)uVar34 >> 0x10),
                                         CONCAT11((char)(uVar4 >> 0x10) + 0x69U ^
                                                  (byte)((uint)uVar34 >> 8),
                                                  (char)uVar4 + 0x69U ^ (byte)uVar34)));
                  uVar21 = uVar21 + 4;
                } while (uVar21 != 0x48);
                DAT_0a3e2eba = 1;
              }
              lVar13 = 0;
              do {
                lVar20 = lVar13;
                uVar11 = (uint)uVar17;
                *(undefined1 *)((long)&local_148 + lVar20) =
                     *(undefined1 *)
                      ((long)&DAT_0a3e2e72 +
                      (ulong)(uVar11 + (int)((uVar17 & 0xffffffff) / 10) * -10 + 0x23));
                uVar17 = (uVar17 & 0xffffffff) / 10;
                lVar13 = lVar20 + 1;
              } while (9 < uVar11);
              *(undefined1 *)((long)&local_148 + lVar20 + 1) = 0;
              if (8 < lVar20 + 8U) {
                puVar19 = (undefined1 *)((long)&local_148 + lVar20);
                puVar9 = (undefined1 *)((long)&local_148 + 1);
                do {
                  uVar3 = *puVar19;
                  *puVar19 = puVar9[-1];
                  puVar9[-1] = uVar3;
                  bVar5 = puVar9 < puVar19 + -1;
                  puVar19 = puVar19 + -1;
                  puVar9 = puVar9 + 1;
                } while (bVar5);
              }
              local_150 = (long *******)&local_148;
              uVar17 = (**(code **)(*(long *)*plVar24 + 0x18))();
              if ((DAT_0a3e2eba & 1) == 0) {
                uVar21 = 0;
                do {
                  uVar28 = *(undefined4 *)((long)&DAT_088c56c9 + uVar21);
                  uVar4 = CONCAT12((char)((uint)uVar28 >> 8),(short)uVar28) & 0xff00ff;
                  uVar34 = *(undefined4 *)((long)&DAT_088c56b5 + uVar21 % 0x14);
                  *(uint *)((long)&DAT_0a3e2e72 + uVar21) =
                       CONCAT13((char)((uint)uVar28 >> 0x18) + 0x69U ^ (byte)((uint)uVar34 >> 0x18),
                                CONCAT12((char)((uint)uVar28 >> 0x10) + 0x69U ^
                                         (byte)((uint)uVar34 >> 0x10),
                                         CONCAT11((char)(uVar4 >> 0x10) + 0x69U ^
                                                  (byte)((uint)uVar34 >> 8),
                                                  (char)uVar4 + 0x69U ^ (byte)uVar34)));
                  uVar21 = uVar21 + 4;
                } while (uVar21 != 0x48);
                DAT_0a3e2eba = 1;
              }
              lVar13 = 0;
              do {
                lVar20 = lVar13;
                uVar11 = (uint)uVar17;
                *(undefined1 *)((long)&local_198 + lVar20) =
                     *(undefined1 *)
                      ((long)&DAT_0a3e2e72 +
                      (ulong)(uVar11 + (int)((uVar17 & 0xffffffff) / 10) * -10 + 0x23));
                uVar17 = (uVar17 & 0xffffffff) / 10;
                lVar13 = lVar20 + 1;
              } while (9 < uVar11);
              *(undefined1 *)((long)&local_198 + lVar20 + 1) = 0;
              if (8 < lVar20 + 8U) {
                puVar19 = (undefined1 *)((long)&local_198 + lVar20);
                puVar9 = (undefined1 *)((long)&local_198 + 1);
                do {
                  uVar3 = *puVar19;
                  *puVar19 = puVar9[-1];
                  puVar9[-1] = uVar3;
                  bVar5 = puVar9 < puVar19 + -1;
                  puVar19 = puVar19 + -1;
                  puVar9 = puVar9 + 1;
                } while (bVar5);
              }
              ppppppplVar18 = (long *******)(*plVar24 + 0x90);
              local_1f0 = (long *******)*ppppppplVar18;
              if (-1 < *(char *)(*plVar24 + 0xa7)) {
                local_1f0 = ppppppplVar18;
              }
              local_1e8 = 0;
              if ((DAT_0a3dd613 & 1) == 0) {
                uVar17 = 0;
                do {
                  (&DAT_0a3dd5cf)[uVar17] =
                       (&DAT_088bd20b)[uVar17] + 0x8a ^ (&DAT_088bd1fb)[uVar17 & 0xf];
                  uVar17 = uVar17 + 1;
                } while (uVar17 != 0x44);
                DAT_0a3dd613 = 1;
              }
              ppppppplStack_f0 = (long *******)&local_1f0;
              uStack_e0 = 0;
              uStack_e8 = 0;
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
              local_88 = 0;
              local_1a0 = (undefined8 *******)&local_198;
              local_100 = (long *******)&local_150;
              pppppppuStack_f8 = &local_1a0;
              FUN_05e1d31c(&local_280,&DAT_0a3dd5cf,&local_100);
              thunk_FUN_05e1d0bc(&local_280);
              if (cStack_321 < '\0') {
                __ZdlPvm(local_338[0],CONCAT17(cStack_321,local_328) & 0x7fffffffffffffff);
              }
            }
            bVar5 = false;
          }
          local_240 = &SUB_aaaaaaaaaaaaaaaa;
          puStack_258 = &SUB_aaaaaaaaaaaaaaaa;
          local_260 = &SUB_aaaaaaaaaaaaaaaa;
          local_248 = &SUB_aaaaaaaaaaaaaaaa;
          puStack_250 = &SUB_aaaaaaaaaaaaaaaa;
          pppppppuStack_278 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
          local_280 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
          puStack_268 = &SUB_aaaaaaaaaaaaaaaa;
          local_270 = (long ******)&SUB_aaaaaaaaaaaaaaaa;
          FUN_0086e43c(&local_280,local_2f0);
          if ((char)local_240 == '\x01') {
            lVar13 = FUN_03213fd8(&local_2b0,&local_280);
            if (lVar13 == 0) {
              pppppppuStack_f8 = (undefined8 *******)__Znwm(0x70);
              pppppppuStack_f8[1] = (undefined8 ******)0x0;
              pppppppuStack_f8[2] = (undefined8 ******)0x0;
              *pppppppuStack_f8 = (undefined8 ******)&PTR_FUN_09dee760;
              pppppppuStack_f8[6] = (undefined8 ******)0x0;
              pppppppuStack_f8[5] = (undefined8 ******)0x0;
              pppppppuStack_f8[8] = (undefined8 ******)0x0;
              pppppppuStack_f8[7] = (undefined8 ******)0x0;
              pppppppuStack_f8[10] = (undefined8 ******)0x0;
              pppppppuStack_f8[9] = (undefined8 ******)0x0;
              pppppppuStack_f8[0xc] = (undefined8 ******)0x0;
              pppppppuStack_f8[0xb] = (undefined8 ******)0x0;
              pppppppuStack_f8[0xd] = (undefined8 ******)0x0;
              local_100 = pppppppuStack_f8 + 3;
              pppppppuStack_f8[4] = (undefined8 ******)0x0;
              *local_100 = (long ******)0x0;
              lVar13 = FUN_03214318(&local_2b0,&local_280,&local_280,&local_100);
              ppppppplVar18 = local_2c0;
              if (local_2c0 < local_2b8) {
                if ((long)local_270 < 0) {
                  FUN_00018d20(local_2c0,local_280,pppppppuStack_278);
                }
                else {
                  local_2c0[2] = local_270;
                  local_2c0[1] = (long ******)pppppppuStack_278;
                  *local_2c0 = (long ******)local_280;
                }
                local_2c0 = ppppppplVar18 + 3;
              }
              else {
                local_2c0 = (long *******)FUN_0002df44(&local_2c8,&local_280);
              }
              pppppppuVar12 = pppppppuStack_f8;
              if (pppppppuStack_f8 != (undefined8 *******)0x0) {
                LOAcquire();
                ppppppuVar8 = pppppppuStack_f8[1];
                pppppppuStack_f8[1] = (undefined8 ******)((long)ppppppuVar8 + -1);
                LORelease();
                if (ppppppuVar8 == (undefined8 ******)0x0) {
                  (*(code *)(*pppppppuStack_f8)[2])(pppppppuStack_f8);
                  __ZNSt3__119__shared_weak_count14__release_weakEv(pppppppuVar12);
                }
              }
            }
            if (((ulong)local_240 & 1) == 0) {
                    /* WARNING: Subroutine does not return */
              FUN_004d04d4();
            }
            lVar13 = *(long *)(lVar13 + 0x28);
            puVar14 = *(undefined8 **)(lVar13 + 0x28);
            if (puVar14 < *(undefined8 **)(lVar13 + 0x30)) {
              if ((long)local_270 < 0) {
                FUN_00018d20(puVar14,local_280,pppppppuStack_278);
              }
              else {
                puVar14[2] = local_270;
                puVar14[1] = pppppppuStack_278;
                *puVar14 = local_280;
              }
              puVar14[4] = local_260;
              puVar14[3] = puStack_268;
              if ((long)local_248 < 0) {
                FUN_00018d20(puVar14 + 5,puStack_258,puStack_250);
              }
              else {
                puVar14[7] = local_248;
                puVar14[6] = puStack_250;
                puVar14[5] = puStack_258;
              }
              puVar14 = puVar14 + 8;
              *(undefined8 **)(lVar13 + 0x28) = puVar14;
            }
            else {
              puVar14 = (undefined8 *)FUN_03213c1c(lVar13 + 0x20,&local_280);
            }
            *(undefined8 **)(lVar13 + 0x28) = puVar14;
            plVar23 = local_2e8;
            if (((ulong)local_240 & 1) != 0) {
LAB_031802c8:
              if ((long)local_248 < 0) {
                __ZdlPvm(puStack_258,(ulong)local_248 & 0x7fffffffffffffff);
              }
              plVar23 = local_2e8;
              if ((long)local_270 < 0) {
                __ZdlPvm(local_280,(ulong)local_270 & 0x7fffffffffffffff);
                plVar23 = local_2e8;
              }
            }
          }
          else {
            plVar23 = local_2e8;
            if ((char)local_240 != '\0') goto LAB_031802c8;
          }
          local_2e8 = plVar23;
          if (plVar23 != (long *)0x0) {
            LOAcquire();
            lVar13 = plVar23[1];
            plVar23[1] = lVar13 + -1;
            LORelease();
            if (lVar13 == 0) {
              (**(code **)(*plVar23 + 0x10))(plVar23);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar23);
            }
          }
          if ((long)puStack_2f8 < 0) {
            __ZdlPvm(puStack_308,(ulong)puStack_2f8 & 0x7fffffffffffffff);
          }
        }
        else {
          local_280 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
          pppppppuStack_278 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
          local_100 = (long *******)CONCAT71(local_100._1_7_,1);
          pppppppuVar12 = (undefined8 *******)__Znwm(0xf8);
          FUN_03214718(pppppppuVar12,plVar24,&local_100);
          local_280 = pppppppuVar12 + 3;
          pppppppuStack_278 = pppppppuVar12;
          lVar13 = FUN_03213fd8(&local_2b0,pppppppuVar12 + 10);
          if (lVar13 == 0) {
            pppppppuStack_f8 = (undefined8 *******)__Znwm(0x70);
            pppppppuStack_f8[1] = (undefined8 ******)0x0;
            pppppppuStack_f8[2] = (undefined8 ******)0x0;
            *pppppppuStack_f8 = (undefined8 ******)&PTR_FUN_09dee760;
            pppppppuStack_f8[6] = (undefined8 ******)0x0;
            pppppppuStack_f8[5] = (undefined8 ******)0x0;
            pppppppuStack_f8[8] = (undefined8 ******)0x0;
            pppppppuStack_f8[7] = (undefined8 ******)0x0;
            pppppppuStack_f8[10] = (undefined8 ******)0x0;
            pppppppuStack_f8[9] = (undefined8 ******)0x0;
            pppppppuStack_f8[0xc] = (undefined8 ******)0x0;
            pppppppuStack_f8[0xb] = (undefined8 ******)0x0;
            pppppppuStack_f8[0xd] = (undefined8 ******)0x0;
            local_100 = pppppppuStack_f8 + 3;
            pppppppuStack_f8[4] = (undefined8 ******)0x0;
            *local_100 = (undefined8 ******)0x0;
            lVar13 = FUN_03214318(&local_2b0,pppppppuVar12 + 10,pppppppuVar12 + 10,&local_100);
            ppppppplVar18 = local_2c0;
            if (local_2c0 < local_2b8) {
              if (*(char *)((long)pppppppuVar12 + 0x67) < '\0') {
                FUN_00018d20(local_2c0,pppppppuVar12[10],pppppppuVar12[0xb]);
              }
              else {
                pppppplVar30 = pppppppuVar12[0xb];
                pppppplVar29 = pppppppuVar12[10];
                local_2c0[2] = pppppppuVar12[0xc];
                local_2c0[1] = pppppplVar30;
                *local_2c0 = pppppplVar29;
              }
              local_2c0 = ppppppplVar18 + 3;
            }
            else {
              local_2c0 = (long *******)FUN_0002df44(&local_2c8,pppppppuVar12 + 10);
            }
            pppppppuVar12 = pppppppuStack_f8;
            if (pppppppuStack_f8 != (undefined8 *******)0x0) {
              LOAcquire();
              ppppppuVar8 = pppppppuStack_f8[1];
              pppppppuStack_f8[1] = (undefined8 ******)((long)ppppppuVar8 + -1);
              LORelease();
              if (ppppppuVar8 == (undefined8 ******)0x0) {
                (*(code *)(*pppppppuStack_f8)[2])(pppppppuStack_f8);
                __ZNSt3__119__shared_weak_count14__release_weakEv(pppppppuVar12);
              }
            }
          }
          pppppplVar29 = *(long *******)(lVar13 + 0x28);
          pppppplVar30 = *(long *******)(lVar13 + 0x30);
          if (pppppplVar30 != (long ******)0x0) {
            pppppplVar26 = pppppplVar30 + 1;
            *pppppplVar26 = (long *****)((long)*pppppplVar26 + 1);
            *pppppplVar26 = (long *****)((long)*pppppplVar26 + 1);
          }
          pppppplVar26 = local_280[0x1b];
          local_280[0x1a] = pppppplVar29;
          local_280[0x1b] = pppppplVar30;
          if (pppppplVar26 != (long ******)0x0) {
            LOAcquire();
            ppppplVar7 = pppppplVar26[1];
            pppppplVar26[1] = (long *****)((long)ppppplVar7 + -1);
            LORelease();
            if (ppppplVar7 == (long *****)0x0) {
              (*(code *)(*pppppplVar26)[2])(pppppplVar26);
              __ZNSt3__119__shared_weak_count14__release_weakEv(pppppplVar26);
            }
          }
          if (pppppplVar30 != (long ******)0x0) {
            LOAcquire();
            ppppplVar7 = pppppplVar30[1];
            pppppplVar30[1] = (long *****)((long)ppppplVar7 + -1);
            LORelease();
            if (ppppplVar7 == (long *****)0x0) {
              (*(code *)(*pppppplVar30)[2])(pppppplVar30);
              __ZNSt3__119__shared_weak_count14__release_weakEv(pppppplVar30);
            }
          }
          lVar13 = *(long *)(lVar13 + 0x28);
          local_100 = local_280;
          pppppppuStack_f8 = pppppppuStack_278;
          if (pppppppuStack_278 != (undefined8 *******)0x0) {
            pppppppuStack_278[2] = (undefined8 ******)((long)pppppppuStack_278[2] + 1);
          }
          puVar14 = *(undefined8 **)(lVar13 + 8);
          if (puVar14 < *(undefined8 **)(lVar13 + 0x10)) {
            *puVar14 = local_280;
            puVar14[1] = pppppppuStack_278;
            *(undefined8 **)(lVar13 + 8) = puVar14 + 2;
          }
          else {
            uVar15 = FUN_032147c4(lVar13,&local_100);
            *(undefined8 *)(lVar13 + 8) = uVar15;
            if (pppppppuStack_f8 != (undefined8 *******)0x0) {
              __ZNSt3__119__shared_weak_count14__release_weakEv();
            }
          }
          if (local_2d8 < local_2d0) {
            *local_2d8 = (long)local_280;
            local_2d8[1] = (long)pppppppuStack_278;
            if (pppppppuStack_278 != (undefined8 *******)0x0) {
              pppppppuStack_278[1] = (undefined8 ******)((long)pppppppuStack_278[1] + 1);
            }
            local_2d8 = local_2d8 + 2;
          }
          else {
            local_2d8 = (long *)FUN_0320cce0(&local_2e0,&local_280);
          }
          pppppppuVar12 = pppppppuStack_278;
          if (pppppppuStack_278 != (undefined8 *******)0x0) {
            LOAcquire();
            ppppppuVar8 = pppppppuStack_278[1];
            pppppppuStack_278[1] = (undefined8 ******)((long)ppppppuVar8 + -1);
            LORelease();
            if (ppppppuVar8 == (undefined8 ******)0x0) {
              (*(code *)(*pppppppuStack_278)[2])(pppppppuStack_278);
              __ZNSt3__119__shared_weak_count14__release_weakEv(pppppppuVar12);
            }
          }
        }
      }
      plVar24 = plVar24 + 2;
    } while (plVar24 != plVar2);
  }
  uVar16 = thunk_FUN_05e1d97c(2);
  plVar24 = local_2e0;
  plVar2 = local_2d8;
  if ((int)uVar16 != 0) {
    FUN_0488143c(&local_1f0);
    ppppppplVar18 = local_1f0;
    if (-1 < cStack_1d9) {
      ppppppplVar18 = (long *******)&local_1f0;
    }
    if ((DAT_0a3dd363 & 1) == 0) {
      uVar17 = 0;
      do {
        (&DAT_0a3dd350)[uVar17] = (&DAT_088bce97)[uVar17] + 0x8a ^ (&DAT_088bce87)[uVar17 & 0xf];
        uVar17 = uVar17 + 1;
      } while (uVar17 != 0x13);
      DAT_0a3dd363 = 1;
    }
    if ((DAT_0a3dd4f9 & 1) == 0) {
      _DAT_0a3dd4e4 = CONCAT44((int)DAT_088ba9b8,(int)DAT_08503670);
      uRam000000000a3dd4ec = CONCAT44((int)DAT_084b0670,(int)DAT_084916e8);
      DAT_0a3dd4f4 = (undefined4)DAT_08480ab8;
      DAT_0a3dd4f8 = 0;
      DAT_0a3dd4f9 = 1;
    }
    FUN_05e1d050(&local_280,2,ppppppplVar18,&DAT_0a3dd350,&DAT_0a3dd4e4,0x1ec,0,0);
    local_150 = (long *******)0x0;
    if ((DAT_0a3e2eba & 1) == 0) {
      uVar17 = 0;
      do {
        uVar31 = *(undefined4 *)((long)&DAT_088c56c9 + uVar17);
        uVar4 = CONCAT12((char)((uint)uVar31 >> 8),(short)uVar31) & 0xff00ff;
        uVar35 = *(undefined4 *)((long)&DAT_088c56b5 + uVar17 % 0x14);
        *(uint *)((long)&DAT_0a3e2e72 + uVar17) =
             CONCAT13((char)((uint)uVar31 >> 0x18) + 0x69U ^ (byte)((uint)uVar35 >> 0x18),
                      CONCAT12((char)((uint)uVar31 >> 0x10) + 0x69U ^ (byte)((uint)uVar35 >> 0x10),
                               CONCAT11((char)(uVar4 >> 0x10) + 0x69U ^ (byte)((uint)uVar35 >> 8),
                                        (char)uVar4 + 0x69U ^ (byte)uVar35)));
        uVar17 = uVar17 + 4;
      } while (uVar17 != 0x48);
      DAT_0a3e2eba = 1;
    }
    uVar17 = ((long)local_2c0 - (long)local_2c8 >> 3) * -0x5555555555555555;
    lVar13 = 0;
    do {
      lVar20 = lVar13;
      *(undefined1 *)((long)&local_148 + lVar20) = (&DAT_0a3e2e95)[uVar17 % 10];
      bVar6 = 9 < uVar17;
      uVar17 = uVar17 / 10;
      lVar13 = lVar20 + 1;
    } while (bVar6);
    *(undefined1 *)((long)&local_148 + lVar20 + 1) = 0;
    if (8 < lVar20 + 8U) {
      puVar19 = (undefined1 *)((long)&local_148 + lVar20);
      puVar9 = (undefined1 *)((long)&local_148 + 1);
      do {
        uVar3 = *puVar19;
        *puVar19 = puVar9[-1];
        puVar9[-1] = uVar3;
        bVar6 = puVar9 < puVar19 + -1;
        puVar19 = puVar19 + -1;
        puVar9 = puVar9 + 1;
      } while (bVar6);
    }
    local_150 = (long *******)&local_148;
    local_1a0 = (undefined8 *******)&local_198;
    lVar13 = 0;
    uVar17 = (long)local_2d8 - (long)local_2e0 >> 4;
    do {
      lVar20 = lVar13;
      *(undefined1 *)((long)&local_198 + lVar20) = (&DAT_0a3e2e95)[uVar17 % 10];
      bVar6 = 9 < uVar17;
      lVar13 = lVar20 + 1;
      uVar17 = uVar17 / 10;
    } while (bVar6);
    *(undefined1 *)((long)&local_198 + lVar20 + 1) = 0;
    if (8 < lVar20 + 8U) {
      puVar19 = (undefined1 *)((long)&local_198 + lVar20);
      puVar9 = (undefined1 *)((long)&local_198 + 1);
      do {
        uVar3 = *puVar19;
        *puVar19 = puVar9[-1];
        puVar9[-1] = uVar3;
        bVar6 = puVar9 < puVar19 + -1;
        puVar19 = puVar19 + -1;
        puVar9 = puVar9 + 1;
      } while (bVar6);
    }
    if ((DAT_0a3dd650 & 1) == 0) {
      uVar17 = 0;
      do {
        (&DAT_0a3dd614)[uVar17] = (&DAT_088bd25f)[uVar17] + 0x8a ^ (&DAT_088bd24f)[uVar17 & 0xf];
        uVar17 = uVar17 + 1;
      } while (uVar17 != 0x3c);
      DAT_0a3dd650 = 1;
    }
    local_100 = (long *******)&local_150;
    pppppppuStack_f8 = &local_1a0;
    uStack_e8 = 0;
    ppppppplStack_f0 = (long *******)0x0;
    local_d8 = 0;
    uStack_e0 = 0;
    local_c8 = 0;
    uStack_d0 = 0;
    local_b8 = 0;
    uStack_c0 = 0;
    local_a8 = 0;
    uStack_b0 = 0;
    local_98 = 0;
    uStack_a0 = 0;
    local_88 = 0;
    uStack_90 = 0;
    FUN_05e1d31c(&local_280,&DAT_0a3dd614,&local_100);
    uVar16 = thunk_FUN_05e1d0bc(&local_280);
    plVar24 = local_2e0;
    plVar2 = local_2d8;
    if (cStack_1d9 < '\0') {
      uVar16 = __ZdlPvm(local_1f0,CONCAT17(cStack_1d9,local_1e0) & 0x7fffffffffffffff);
      plVar24 = local_2e0;
      plVar2 = local_2d8;
    }
  }
  for (; plVar23 = local_2d8, plVar24 != local_2d8; plVar24 = plVar24 + 2) {
    lVar20 = *(long *)(param_1 + 0xb20);
    local_348 = *plVar24;
    local_340 = (long *)plVar24[1];
    lVar13 = local_348;
    if (local_340 != (long *)0x0) {
      local_340[1] = local_340[1] + 1;
      lVar13 = *plVar24;
    }
    local_2d8 = plVar2;
    uVar16 = FUN_03181628(uVar16,lVar20 + 0x60,&local_348,lVar13 + 0x38);
    plVar2 = local_340;
    if (local_340 != (long *)0x0) {
      LOAcquire();
      lVar13 = local_340[1];
      local_340[1] = lVar13 + -1;
      LORelease();
      if (lVar13 == 0) {
        (**(code **)(*local_340 + 0x10))(local_340);
        uVar16 = __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
      }
    }
    plVar2 = local_2d8;
    local_2d8 = plVar23;
  }
  local_2d8 = plVar2;
  iVar10 = thunk_FUN_05e1d97c(2);
  if (iVar10 != 0) {
    FUN_0488143c(&local_1f0);
    ppppppplVar18 = local_1f0;
    if (-1 < cStack_1d9) {
      ppppppplVar18 = (long *******)&local_1f0;
    }
    if ((DAT_0a3dd363 & 1) == 0) {
      uVar17 = 0;
      do {
        (&DAT_0a3dd350)[uVar17] = (&DAT_088bce97)[uVar17] + 0x8a ^ (&DAT_088bce87)[uVar17 & 0xf];
        uVar17 = uVar17 + 1;
      } while (uVar17 != 0x13);
      DAT_0a3dd363 = 1;
    }
    if ((DAT_0a3dd4f9 & 1) == 0) {
      _DAT_0a3dd4e4 = CONCAT44((int)DAT_088ba9b8,(int)DAT_08503670);
      uRam000000000a3dd4ec = CONCAT44((int)DAT_084b0670,(int)DAT_084916e8);
      DAT_0a3dd4f4 = (undefined4)DAT_08480ab8;
      DAT_0a3dd4f8 = 0;
      DAT_0a3dd4f9 = 1;
    }
    FUN_05e1d050(&local_280,2,ppppppplVar18,&DAT_0a3dd350,&DAT_0a3dd4e4,0x1f2,0,0);
    local_150 = (long *******)0x0;
    if ((DAT_0a3e2eba & 1) == 0) {
      uVar17 = 0;
      do {
        uVar31 = *(undefined4 *)((long)&DAT_088c56c9 + uVar17);
        uVar4 = CONCAT12((char)((uint)uVar31 >> 8),(short)uVar31) & 0xff00ff;
        uVar35 = *(undefined4 *)((long)&DAT_088c56b5 + uVar17 % 0x14);
        *(uint *)((long)&DAT_0a3e2e72 + uVar17) =
             CONCAT13((char)((uint)uVar31 >> 0x18) + 0x69U ^ (byte)((uint)uVar35 >> 0x18),
                      CONCAT12((char)((uint)uVar31 >> 0x10) + 0x69U ^ (byte)((uint)uVar35 >> 0x10),
                               CONCAT11((char)(uVar4 >> 0x10) + 0x69U ^ (byte)((uint)uVar35 >> 8),
                                        (char)uVar4 + 0x69U ^ (byte)uVar35)));
        uVar17 = uVar17 + 4;
      } while (uVar17 != 0x48);
      DAT_0a3e2eba = 1;
    }
    uVar17 = (long)local_2d8 - (long)local_2e0 >> 4;
    lVar13 = 0;
    do {
      lVar20 = lVar13;
      *(undefined1 *)((long)&local_148 + lVar20) = (&DAT_0a3e2e95)[uVar17 % 10];
      bVar6 = 9 < uVar17;
      uVar17 = uVar17 / 10;
      lVar13 = lVar20 + 1;
    } while (bVar6);
    *(undefined1 *)((long)&local_148 + lVar20 + 1) = 0;
    if (8 < lVar20 + 8U) {
      puVar19 = (undefined1 *)((long)&local_148 + lVar20);
      puVar9 = (undefined1 *)((long)&local_148 + 1);
      do {
        uVar3 = *puVar19;
        *puVar19 = puVar9[-1];
        puVar9[-1] = uVar3;
        bVar6 = puVar9 < puVar19 + -1;
        puVar19 = puVar19 + -1;
        puVar9 = puVar9 + 1;
      } while (bVar6);
    }
    local_150 = (long *******)&local_148;
    local_1a0 = (undefined8 *******)&local_198;
    lVar13 = 0;
    uVar17 = ((long)local_2c0 - (long)local_2c8 >> 3) * -0x5555555555555555;
    do {
      lVar20 = lVar13;
      *(undefined1 *)((long)&local_198 + lVar20) = (&DAT_0a3e2e95)[uVar17 % 10];
      bVar6 = 9 < uVar17;
      lVar13 = lVar20 + 1;
      uVar17 = uVar17 / 10;
    } while (bVar6);
    *(undefined1 *)((long)&local_198 + lVar20 + 1) = 0;
    if (8 < lVar20 + 8U) {
      puVar19 = (undefined1 *)((long)&local_198 + lVar20);
      puVar9 = (undefined1 *)((long)&local_198 + 1);
      do {
        uVar3 = *puVar19;
        *puVar19 = puVar9[-1];
        puVar9[-1] = uVar3;
        bVar6 = puVar9 < puVar19 + -1;
        puVar19 = puVar19 + -1;
        puVar9 = puVar9 + 1;
      } while (bVar6);
    }
    if ((DAT_0a3dd698 & 1) == 0) {
      uVar17 = 0;
      do {
        (&DAT_0a3dd651)[uVar17] = (&DAT_088bd2ab)[uVar17] + 0x8a ^ (&DAT_088bd29b)[uVar17 & 0xf];
        uVar17 = uVar17 + 1;
      } while (uVar17 != 0x47);
      DAT_0a3dd698 = 1;
    }
    local_100 = (long *******)&local_150;
    pppppppuStack_f8 = &local_1a0;
    uStack_e8 = 0;
    ppppppplStack_f0 = (long *******)0x0;
    local_d8 = 0;
    uStack_e0 = 0;
    local_c8 = 0;
    uStack_d0 = 0;
    local_b8 = 0;
    uStack_c0 = 0;
    local_a8 = 0;
    uStack_b0 = 0;
    local_98 = 0;
    uStack_a0 = 0;
    local_88 = 0;
    uStack_90 = 0;
    FUN_05e1d31c(&local_280,&DAT_0a3dd651,&local_100);
    thunk_FUN_05e1d0bc(&local_280);
    if (cStack_1d9 < '\0') {
      __ZdlPvm(local_1f0,CONCAT17(cStack_1d9,local_1e0) & 0x7fffffffffffffff);
    }
  }
  ppppppplVar18 = local_2c0;
  uVar16 = DAT_08480ab8;
  if (local_2c8 != local_2c0) {
    uVar35 = (undefined4)DAT_088ba9b8;
    uVar33 = (undefined4)DAT_08503670;
    uVar31 = (undefined4)DAT_084916e8;
    uVar27 = (undefined4)DAT_084b0670;
    ppppppplVar25 = local_2c8;
    do {
      lVar13 = FUN_03213fd8(&local_2b0,ppppppplVar25);
      iVar10 = thunk_FUN_05e1d97c(2);
      if (iVar10 != 0) {
        FUN_0488143c(&local_1f0);
        ppppppplVar1 = local_1f0;
        if (-1 < cStack_1d9) {
          ppppppplVar1 = (long *******)&local_1f0;
        }
        if ((DAT_0a3dd363 & 1) == 0) {
          uVar17 = 0;
          do {
            (&DAT_0a3dd350)[uVar17] = (&DAT_088bce97)[uVar17] + 0x8a ^ (&DAT_088bce87)[uVar17 & 0xf]
            ;
            uVar17 = uVar17 + 1;
          } while (uVar17 != 0x13);
          DAT_0a3dd363 = 1;
        }
        if ((DAT_0a3dd4f9 & 1) == 0) {
          DAT_0a3dd4f4 = (undefined4)uVar16;
          DAT_0a3dd4f8 = 0;
          DAT_0a3dd4f9 = 1;
          _DAT_0a3dd4e4 = CONCAT44(uVar35,uVar33);
          uRam000000000a3dd4ec = CONCAT44(uVar27,uVar31);
        }
        FUN_05e1d050(&local_280,2,ppppppplVar1,&DAT_0a3dd350,&DAT_0a3dd4e4,0x1f8,0,0);
        local_150 = (long *******)*ppppppplVar25;
        if (-1 < *(char *)((long)ppppppplVar25 + 0x17)) {
          local_150 = ppppppplVar25;
        }
        local_148._0_1_ = 0;
        if (lVar13 == 0) {
          uVar17 = 0;
        }
        else {
          uVar17 = (*(long **)(lVar13 + 0x28))[1] - **(long **)(lVar13 + 0x28) >> 4;
        }
        if ((DAT_0a3e2eba & 1) == 0) {
          uVar21 = 0;
          do {
            uVar28 = *(undefined4 *)((long)&DAT_088c56c9 + uVar21);
            uVar4 = CONCAT12((char)((uint)uVar28 >> 8),(short)uVar28) & 0xff00ff;
            uVar34 = *(undefined4 *)((long)&DAT_088c56b5 + uVar21 % 0x14);
            *(uint *)((long)&DAT_0a3e2e72 + uVar21) =
                 CONCAT13((char)((uint)uVar28 >> 0x18) + 0x69U ^ (byte)((uint)uVar34 >> 0x18),
                          CONCAT12((char)((uint)uVar28 >> 0x10) + 0x69U ^
                                   (byte)((uint)uVar34 >> 0x10),
                                   CONCAT11((char)(uVar4 >> 0x10) + 0x69U ^
                                            (byte)((uint)uVar34 >> 8),
                                            (char)uVar4 + 0x69U ^ (byte)uVar34)));
            uVar21 = uVar21 + 4;
          } while (uVar21 != 0x48);
          DAT_0a3e2eba = 1;
        }
        lVar13 = 0;
        do {
          lVar20 = lVar13;
          *(undefined1 *)((long)&local_198 + lVar20) = (&DAT_0a3e2e95)[uVar17 % 10];
          bVar6 = 9 < uVar17;
          uVar17 = uVar17 / 10;
          lVar13 = lVar20 + 1;
        } while (bVar6);
        *(undefined1 *)((long)&local_198 + lVar20 + 1) = 0;
        if (8 < lVar20 + 8U) {
          puVar19 = (undefined1 *)((long)&local_198 + lVar20);
          puVar9 = (undefined1 *)((long)&local_198 + 1);
          do {
            uVar3 = *puVar19;
            *puVar19 = puVar9[-1];
            puVar9[-1] = uVar3;
            bVar6 = puVar9 < puVar19 + -1;
            puVar19 = puVar19 + -1;
            puVar9 = puVar9 + 1;
          } while (bVar6);
        }
        if ((DAT_0a3dd6e5 & 1) == 0) {
          uVar17 = 0;
          do {
            (&DAT_0a3dd699)[uVar17] = (&DAT_088bd302)[uVar17] + 0x8a ^ (&DAT_088bd2f2)[uVar17 & 0xf]
            ;
            uVar17 = uVar17 + 1;
          } while (uVar17 != 0x4c);
          DAT_0a3dd6e5 = 1;
        }
        local_100 = (long *******)&local_150;
        uStack_e8 = 0;
        ppppppplStack_f0 = (long *******)0x0;
        local_d8 = 0;
        uStack_e0 = 0;
        local_c8 = 0;
        uStack_d0 = 0;
        local_b8 = 0;
        uStack_c0 = 0;
        local_a8 = 0;
        uStack_b0 = 0;
        local_98 = 0;
        uStack_a0 = 0;
        local_88 = 0;
        uStack_90 = 0;
        local_1a0 = (undefined8 *******)&local_198;
        pppppppuStack_f8 = &local_1a0;
        FUN_05e1d31c(&local_280,&DAT_0a3dd699,&local_100);
        thunk_FUN_05e1d0bc(&local_280);
        if (cStack_1d9 < '\0') {
          __ZdlPvm(local_1f0,CONCAT17(cStack_1d9,local_1e0) & 0x7fffffffffffffff);
        }
      }
      FUN_03182084(param_1,ppppppplVar25);
      ppppppplVar25 = ppppppplVar25 + 3;
    } while (ppppppplVar25 != ppppppplVar18);
  }
  iVar10 = thunk_FUN_05e1d97c(2);
  if (iVar10 != 0) {
    FUN_0488143c(&local_1a0);
    pppppppuVar12 = local_1a0;
    if (-1 < cStack_189) {
      pppppppuVar12 = &local_1a0;
    }
    if ((DAT_0a3dd363 & 1) == 0) {
      uVar17 = 0;
      do {
        (&DAT_0a3dd350)[uVar17] = (&DAT_088bce97)[uVar17] + 0x8a ^ (&DAT_088bce87)[uVar17 & 0xf];
        uVar17 = uVar17 + 1;
      } while (uVar17 != 0x13);
      DAT_0a3dd363 = 1;
    }
    if ((DAT_0a3dd4f9 & 1) == 0) {
      _DAT_0a3dd4e4 = CONCAT44((int)DAT_088ba9b8,(int)DAT_08503670);
      uRam000000000a3dd4ec = CONCAT44((int)DAT_084b0670,(int)DAT_084916e8);
      DAT_0a3dd4f4 = (undefined4)DAT_08480ab8;
      DAT_0a3dd4f8 = 0;
      DAT_0a3dd4f9 = 1;
    }
    FUN_05e1d050(&local_280,2,pppppppuVar12,&DAT_0a3dd350,&DAT_0a3dd4e4,0x1fc,0,0);
    if (bVar5) {
      local_150 = (long *******)&DAT_0a3e2ec4;
      if ((DAT_0a3e2ec9 & 1) == 0) {
        DAT_0a3e2ec4 = 0x7274;
        DAT_0a3e2ec6 = 0x75;
        puVar19 = &DAT_0a3e2ec8;
        puVar9 = &DAT_0a3e2ec7;
        puVar22 = &DAT_0a3e2ec9;
LAB_0318119c:
        *puVar9 = 0x65;
        *puVar19 = 0;
        *puVar22 = 1;
      }
    }
    else {
      local_150 = (long *******)&DAT_0a3e2ecc;
      if ((DAT_0a3e2ed2 & 1) == 0) {
        DAT_0a3e2ecc = (undefined4)DAT_0847fe48;
        puVar9 = &DAT_0a3e2ed0;
        puVar19 = &DAT_0a3e2ed1;
        puVar22 = &DAT_0a3e2ed2;
        goto LAB_0318119c;
      }
    }
    local_148._0_1_ = 0;
    if ((DAT_0a3dd70a & 1) == 0) {
      uVar17 = 0;
      do {
        (&DAT_0a3dd6e6)[uVar17] = (&DAT_088bd35e)[uVar17] + 0x8a ^ (&DAT_088bd34e)[uVar17 & 0xf];
        uVar17 = uVar17 + 1;
      } while (uVar17 != 0x24);
      DAT_0a3dd70a = 1;
    }
    ppppppplStack_f0 = (long *******)0x0;
    pppppppuStack_f8 = (undefined8 *******)0x0;
    local_100 = (long *******)&local_150;
    uStack_e0 = 0;
    uStack_e8 = 0;
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
    local_88 = 0;
    FUN_05e1d31c(&local_280,&DAT_0a3dd6e6,&local_100);
    thunk_FUN_05e1d0bc(&local_280);
    if (cStack_189 < '\0') {
      __ZdlPvm(local_1a0,CONCAT17(cStack_189,local_190) & 0x7fffffffffffffff);
    }
  }
  plVar2 = local_2e0;
  plVar24 = local_2d8;
  if (local_2e0 != (long *)0x0) {
    for (; plVar24 != plVar2; plVar24 = plVar24 + -2) {
      plVar23 = (long *)plVar24[-1];
      if (plVar23 != (long *)0x0) {
        LOAcquire();
        lVar13 = plVar23[1];
        plVar23[1] = lVar13 + -1;
        LORelease();
        if (lVar13 == 0) {
          (**(code **)(*plVar23 + 0x10))(plVar23);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar23);
        }
      }
    }
    local_2d8 = plVar2;
    __ZdlPvm(local_2e0,(long)local_2d0 - (long)local_2e0);
  }
  if (local_2c8 != (long *******)0x0) {
    for (; local_2c0 != local_2c8; local_2c0 = local_2c0 + -3) {
    }
    local_2c0 = local_2c8;
    __ZdlPvm(local_2c8,(long)local_2b8 - (long)local_2c8);
  }
  FUN_00999678(&local_2b0);
LAB_03181344:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_78) {
    return bVar5;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


