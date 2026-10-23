// Ghidra inferred pseudocode; requested=0x3182084
// entry=03182084 end=03183927

/* WARNING: Removing unreachable block (ram,0x0318381c) */
/* WARNING: Removing unreachable block (ram,0x0318382c) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_03182084(long param_1,long *param_2)

{
  undefined1 uVar1;
  uint3 uVar2;
  undefined8 ***pppuVar3;
  long *plVar4;
  bool bVar5;
  long lVar6;
  undefined1 *puVar7;
  undefined8 ***pppuVar8;
  int iVar9;
  uint uVar10;
  long lVar11;
  undefined8 ****ppppuVar12;
  undefined8 uVar13;
  long *plVar14;
  code *pcVar15;
  ulong uVar16;
  long lVar17;
  undefined1 *puVar18;
  undefined8 *puVar19;
  undefined1 *puVar20;
  ulong uVar21;
  long *plVar22;
  undefined4 uVar23;
  undefined4 uVar24;
  long local_408;
  long lStack_400;
  ulong local_3f8;
  long local_3f0;
  long *local_3e8;
  undefined8 ***local_3e0;
  undefined8 local_3d8;
  undefined8 uStack_3d0;
  ulong local_3c8;
  undefined1 *local_3c0;
  long *local_3b8;
  long local_3b0;
  long *local_3a8;
  long local_3a0;
  long *local_398;
  undefined8 ***local_390 [2];
  undefined7 local_380;
  char cStack_379;
  undefined8 ***local_378 [2];
  undefined7 local_368;
  char cStack_361;
  long local_360;
  long *plStack_358;
  undefined8 local_350;
  undefined1 *puStack_348;
  undefined1 *local_340;
  undefined1 *puStack_338;
  undefined1 *local_330;
  long *local_328;
  long local_320;
  long *local_318;
  undefined8 local_310 [2];
  undefined7 local_300;
  char cStack_2f9;
  long local_280;
  long *local_278;
  long alStack_270 [3];
  long *local_258;
  long alStack_250 [3];
  long *local_238;
  undefined8 ***local_230;
  undefined1 local_228;
  undefined7 local_220;
  char cStack_219;
  undefined8 ***local_1e0;
  undefined8 local_1d8;
  undefined7 local_1d0;
  char cStack_1c9;
  undefined8 ***local_190;
  undefined8 local_188;
  undefined7 local_180;
  char cStack_179;
  undefined8 ***local_140;
  undefined1 local_138;
  undefined7 uStack_137;
  undefined7 local_130;
  char cStack_129;
  undefined8 ***local_f0;
  undefined8 ***pppuStack_e8;
  undefined8 ***local_e0;
  undefined8 ***pppuStack_d8;
  undefined8 local_d0;
  undefined8 uStack_c8;
  undefined8 uStack_c0;
  undefined8 uStack_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 uStack_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 uStack_80;
  undefined8 local_78;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar11 = FUN_03221ac0(*(long *)(param_1 + 0xb20) + 0x60);
  if (lVar11 != 0) {
    local_280 = 0;
    local_278 = (long *)0x0;
    plVar22 = *(long **)(lVar11 + 0x28);
    plVar14 = *(long **)(lVar11 + 0x30);
    if (plVar22 != plVar14) {
LAB_031820e4:
      iVar9 = FUN_030f320c(*plVar22);
      if ((iVar9 == 0) || (uVar10 = FUN_030f320c(*plVar22), 3 < uVar10)) {
        iVar9 = FUN_030f320c(*plVar22);
        if (iVar9 != 0) goto code_r0x0318210c;
        lVar11 = *plVar22;
        local_278 = (long *)plVar22[1];
        if (local_278 != (long *)0x0) {
          local_278[1] = local_278[1] + 1;
        }
        local_280 = lVar11;
        iVar9 = thunk_FUN_05e1d97c(2);
        if (iVar9 != 0) {
          FUN_0488143c(&local_190);
          ppppuVar12 = (undefined8 ****)local_190;
          if (-1 < cStack_179) {
            ppppuVar12 = &local_190;
          }
          if ((DAT_0a3dd363 & 1) == 0) {
            uVar16 = 0;
            do {
              (&DAT_0a3dd350)[uVar16] =
                   (&DAT_088bce97)[uVar16] + 0x8a ^ (&DAT_088bce87)[uVar16 & 0xf];
              uVar16 = uVar16 + 1;
            } while (uVar16 != 0x13);
            DAT_0a3dd363 = 1;
          }
          if ((DAT_0a3e0376 & 1) == 0) {
            _DAT_0a3e0360 = CONCAT44((int)DAT_088ba9e0,(int)DAT_08482fd0);
            uRam000000000a3e0368 = CONCAT44((int)DAT_084c7820,(int)DAT_08483880);
            DAT_0a3e0370 = (undefined4)DAT_085b0718;
            DAT_0a3e0374 = 0x65;
            DAT_0a3e0376 = 1;
          }
          FUN_05e1d050(local_310,2,ppppuVar12,&DAT_0a3dd350,&DAT_0a3e0360,"/A/CoreFoundation",0,0);
          lVar11 = local_280;
          FUN_030f1f08(&local_1e0,local_280);
          local_140 = local_1e0;
          if (-1 < cStack_1c9) {
            local_140 = &local_1e0;
          }
          local_138 = 0;
          if ((DAT_0a3e03be & 1) == 0) {
            _DAT_0a3e0394 = CONCAT44((int)DAT_08480af8,(int)DAT_0848be60);
            uRam000000000a3e039c = CONCAT44((int)DAT_0882a318,(int)DAT_088ba9f0);
            _DAT_0a3e03a4 = CONCAT44((int)DAT_087e2df0,(int)DAT_08487d08);
            uRam000000000a3e03ac = CONCAT44((int)ram0x085635f0,(int)DAT_0852a998);
            DAT_0a3e03b4 = CONCAT44((int)DAT_08502950,(int)DAT_0848f630);
            DAT_0a3e03bc = 0x5f;
            DAT_0a3e03be = 1;
          }
          local_e0 = (undefined8 ****)0x0;
          pppuStack_e8 = (undefined8 ****)0x0;
          local_f0 = &local_140;
          local_d0 = 0;
          pppuStack_d8 = (undefined8 ****)0x0;
          uStack_c0 = 0;
          uStack_c8 = 0;
          local_b0 = 0;
          uStack_b8 = 0;
          uStack_a0 = 0;
          uStack_a8 = 0;
          local_90 = 0;
          uStack_98 = 0;
          uStack_80 = 0;
          uStack_88 = 0;
          local_78 = 0;
          FUN_05e1d31c(local_310,&DAT_0a3e0394,&local_f0);
          if (cStack_1c9 < '\0') {
            __ZdlPvm(local_1e0,CONCAT17(cStack_1c9,local_1d0) & 0x7fffffffffffffff);
          }
          thunk_FUN_05e1d0bc(local_310);
          if (cStack_179 < '\0') {
            __ZdlPvm(local_190,CONCAT17(cStack_179,local_180) & 0x7fffffffffffffff);
          }
        }
        if (lVar11 != 0) {
          local_320 = *(long *)(lVar11 + 0x18);
          local_318 = *(long **)(lVar11 + 0x20);
          lVar6 = 0;
          if (local_318 != (long *)0x0) {
            lVar6 = local_318[1];
            local_318[1] = lVar6 + 1;
          }
          iVar9 = thunk_FUN_05e1d97c(lVar6,2);
          if (iVar9 != 0) {
            FUN_0488143c(&local_230);
            ppppuVar12 = (undefined8 ****)local_230;
            if (-1 < cStack_219) {
              ppppuVar12 = &local_230;
            }
            if ((DAT_0a3dd363 & 1) == 0) {
              uVar16 = 0;
              do {
                (&DAT_0a3dd350)[uVar16] =
                     (&DAT_088bce97)[uVar16] + 0x8a ^ (&DAT_088bce87)[uVar16 & 0xf];
                uVar16 = uVar16 + 1;
              } while (uVar16 != 0x13);
              DAT_0a3dd363 = 1;
            }
            if ((DAT_0a3e0376 & 1) == 0) {
              _DAT_0a3e0360 = CONCAT44((int)DAT_088ba9e0,(int)DAT_08482fd0);
              uRam000000000a3e0368 = CONCAT44((int)DAT_084c7820,(int)DAT_08483880);
              DAT_0a3e0370 = (undefined4)DAT_085b0718;
              DAT_0a3e0374 = 0x65;
              DAT_0a3e0376 = 1;
            }
            FUN_05e1d050(local_310,2,ppppuVar12,&DAT_0a3dd350,&DAT_0a3e0360,"ation",0,0);
            lVar11 = local_280;
            FUN_030f1f08(&local_350,local_280);
            local_140 = local_350;
            if (-1 < (long)local_340) {
              local_140 = (undefined8 ***)&local_350;
            }
            local_138 = 0;
            if (local_320 == 0) {
              uVar16 = 0;
            }
            else {
              uVar16 = (ulong)*(uint *)(local_320 + 0xc);
            }
            local_190 = (undefined8 ***)0x0;
            if ((DAT_0a3e2eba & 1) == 0) {
              uVar21 = 0;
              do {
                uVar23 = *(undefined4 *)((long)&DAT_088c56c9 + uVar21);
                uVar2 = CONCAT12((char)((uint)uVar23 >> 8),(short)uVar23) & 0xff00ff;
                uVar24 = *(undefined4 *)((long)&DAT_088c56b5 + uVar21 % 0x14);
                *(uint *)((long)&DAT_0a3e2e72 + uVar21) =
                     CONCAT13((char)((uint)uVar23 >> 0x18) + 0x69U ^ (byte)((uint)uVar24 >> 0x18),
                              CONCAT12((char)((uint)uVar23 >> 0x10) + 0x69U ^
                                       (byte)((uint)uVar24 >> 0x10),
                                       CONCAT11((char)(uVar2 >> 0x10) + 0x69U ^
                                                (byte)((uint)uVar24 >> 8),
                                                (char)uVar2 + 0x69U ^ (byte)uVar24)));
                uVar21 = uVar21 + 4;
              } while (uVar21 != 0x48);
              DAT_0a3e2eba = 1;
            }
            lVar6 = 0;
            do {
              lVar17 = lVar6;
              uVar10 = (uint)uVar16;
              *(undefined1 *)((long)&local_188 + lVar17) =
                   *(undefined1 *)
                    ((long)&DAT_0a3e2e72 + (ulong)(uVar10 + (int)(uVar16 / 10) * -10 + 0x23));
              uVar16 = uVar16 / 10;
              lVar6 = lVar17 + 1;
            } while (9 < uVar10);
            *(undefined1 *)((long)&local_188 + lVar17 + 1) = 0;
            if (8 < lVar17 + 8U) {
              puVar18 = (undefined1 *)((long)&local_188 + lVar17);
              puVar7 = (undefined1 *)((long)&local_188 + 1);
              do {
                uVar1 = *puVar18;
                *puVar18 = puVar7[-1];
                puVar7[-1] = uVar1;
                bVar5 = puVar7 < puVar18 + -1;
                puVar18 = puVar18 + -1;
                puVar7 = puVar7 + 1;
              } while (bVar5);
            }
            local_190 = (undefined8 ***)&local_188;
            if (local_320 == 0) {
              uVar16 = 0;
            }
            else {
              uVar16 = (ulong)*(uint *)(local_320 + 0x10);
            }
            local_1e0 = (undefined8 ***)&local_1d8;
            lVar6 = 0;
            do {
              lVar17 = lVar6;
              uVar10 = (uint)uVar16;
              *(undefined1 *)((long)&local_1d8 + lVar17) =
                   *(undefined1 *)
                    ((long)&DAT_0a3e2e72 + (ulong)(uVar10 + (int)(uVar16 / 10) * -10 + 0x23));
              lVar6 = lVar17 + 1;
              uVar16 = uVar16 / 10;
            } while (9 < uVar10);
            *(undefined1 *)((long)&local_1d8 + lVar17 + 1) = 0;
            if (8 < lVar17 + 8U) {
              puVar18 = (undefined1 *)((long)&local_1d8 + lVar17);
              puVar7 = (undefined1 *)((long)&local_1d8 + 1);
              do {
                uVar1 = *puVar18;
                *puVar18 = puVar7[-1];
                puVar7[-1] = uVar1;
                bVar5 = puVar7 < puVar18 + -1;
                puVar18 = puVar18 + -1;
                puVar7 = puVar7 + 1;
              } while (bVar5);
            }
            if ((DAT_0a3e0426 & 1) == 0) {
              uVar16 = 0;
              do {
                uVar23 = *(undefined4 *)((long)&DAT_088c17ba + uVar16);
                uVar2 = CONCAT12((char)((uint)uVar23 >> 8),(short)uVar23) & 0xff00ff;
                uVar24 = *(undefined4 *)((long)&DAT_088c17a6 + uVar16 % 0x14);
                *(uint *)((long)&DAT_0a3e03e2 + uVar16) =
                     CONCAT13((char)((uint)uVar23 >> 0x18) + 0x69U ^ (byte)((uint)uVar24 >> 0x18),
                              CONCAT12((char)((uint)uVar23 >> 0x10) + 0x69U ^
                                       (byte)((uint)uVar24 >> 0x10),
                                       CONCAT11((char)(uVar2 >> 0x10) + 0x69U ^
                                                (byte)((uint)uVar24 >> 8),
                                                (char)uVar2 + 0x69U ^ (byte)uVar24)));
                uVar16 = uVar16 + 4;
              } while (uVar16 != 0x44);
              DAT_0a3e0426 = 1;
            }
            local_f0 = &local_140;
            pppuStack_e8 = &local_190;
            local_e0 = &local_1e0;
            local_d0 = 0;
            pppuStack_d8 = (undefined8 ****)0x0;
            uStack_c0 = 0;
            uStack_c8 = 0;
            local_b0 = 0;
            uStack_b8 = 0;
            uStack_a0 = 0;
            uStack_a8 = 0;
            local_90 = 0;
            uStack_98 = 0;
            uStack_80 = 0;
            uStack_88 = 0;
            local_78 = 0;
            FUN_05e1d31c(local_310,&DAT_0a3e03e2,&local_f0);
            if ((long)local_340 < 0) {
              __ZdlPvm(local_350,(ulong)local_340 & 0x7fffffffffffffff);
            }
            thunk_FUN_05e1d0bc(local_310);
            if (cStack_219 < '\0') {
              __ZdlPvm(local_230,CONCAT17(cStack_219,local_220) & 0x7fffffffffffffff);
            }
          }
          plVar22 = local_278;
          puStack_338 = &SUB_aaaaaaaaaaaaaaaa;
          local_340 = &SUB_aaaaaaaaaaaaaaaa;
          local_328 = (long *)&SUB_aaaaaaaaaaaaaaaa;
          local_330 = &SUB_aaaaaaaaaaaaaaaa;
          puStack_348 = &SUB_aaaaaaaaaaaaaaaa;
          local_350 = (undefined8 ****)&SUB_aaaaaaaaaaaaaaaa;
          plStack_358 = local_278;
          if (local_278 != (long *)0x0) {
            local_278[1] = local_278[1] + 1;
          }
          local_360 = lVar11;
          FUN_031ce06c(&local_350,param_1,&local_360);
          if (plVar22 != (long *)0x0) {
            LOAcquire();
            lVar11 = plVar22[1];
            plVar22[1] = lVar11 + -1;
            LORelease();
            if (lVar11 == 0) {
              (**(code **)(*plVar22 + 0x10))(plVar22);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar22);
            }
          }
          plVar14 = local_318;
          local_320 = *(long *)(local_280 + 0x18);
          plVar22 = *(long **)(local_280 + 0x20);
          if (plVar22 != (long *)0x0) {
            plVar4 = plVar22 + 1;
            *plVar4 = *plVar4 + 1;
            *plVar4 = *plVar4 + 1;
          }
          plVar4 = plVar22;
          if (local_318 != (long *)0x0) {
            LOAcquire();
            lVar11 = local_318[1];
            local_318[1] = lVar11 + -1;
            LORelease();
            if (lVar11 == 0) {
              lVar11 = *local_318;
              local_318 = plVar22;
              (**(code **)(lVar11 + 0x10))(plVar14);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar14);
              plVar4 = local_318;
            }
          }
          local_318 = plVar4;
          if (plVar22 != (long *)0x0) {
            LOAcquire();
            lVar11 = plVar22[1];
            plVar22[1] = lVar11 + -1;
            LORelease();
            if (lVar11 == 0) {
              (**(code **)(*plVar22 + 0x10))(plVar22);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar22);
            }
          }
          uVar13 = thunk_FUN_05e1d97c(2);
          local_3a0 = local_280;
          if ((int)uVar13 != 0) {
            FUN_0488143c(local_378);
            ppppuVar12 = (undefined8 ****)local_378[0];
            if (-1 < cStack_361) {
              ppppuVar12 = local_378;
            }
            if ((DAT_0a3dd363 & 1) == 0) {
              uVar16 = 0;
              do {
                (&DAT_0a3dd350)[uVar16] =
                     (&DAT_088bce97)[uVar16] + 0x8a ^ (&DAT_088bce87)[uVar16 & 0xf];
                uVar16 = uVar16 + 1;
              } while (uVar16 != 0x13);
              DAT_0a3dd363 = 1;
            }
            if ((DAT_0a3e0376 & 1) == 0) {
              _DAT_0a3e0360 = CONCAT44((int)DAT_088ba9e0,(int)DAT_08482fd0);
              uRam000000000a3e0368 = CONCAT44((int)DAT_084c7820,(int)DAT_08483880);
              DAT_0a3e0370 = (undefined4)DAT_085b0718;
              DAT_0a3e0374 = 0x65;
              DAT_0a3e0376 = 1;
            }
            FUN_05e1d050(local_310,2,ppppuVar12,&DAT_0a3dd350,&DAT_0a3e0360,"n",0,0);
            lVar11 = local_280;
            FUN_030f1f08(local_390,local_280);
            local_140 = local_390[0];
            if (-1 < cStack_379) {
              local_140 = local_390;
            }
            local_138 = 0;
            if (local_320 == 0) {
              uVar16 = 0;
            }
            else {
              uVar16 = (ulong)*(uint *)(local_320 + 0xc);
            }
            local_190 = (undefined8 ***)0x0;
            if ((DAT_0a3e2eba & 1) == 0) {
              uVar21 = 0;
              do {
                uVar23 = *(undefined4 *)((long)&DAT_088c56c9 + uVar21);
                uVar2 = CONCAT12((char)((uint)uVar23 >> 8),(short)uVar23) & 0xff00ff;
                uVar24 = *(undefined4 *)((long)&DAT_088c56b5 + uVar21 % 0x14);
                *(uint *)((long)&DAT_0a3e2e72 + uVar21) =
                     CONCAT13((char)((uint)uVar23 >> 0x18) + 0x69U ^ (byte)((uint)uVar24 >> 0x18),
                              CONCAT12((char)((uint)uVar23 >> 0x10) + 0x69U ^
                                       (byte)((uint)uVar24 >> 0x10),
                                       CONCAT11((char)(uVar2 >> 0x10) + 0x69U ^
                                                (byte)((uint)uVar24 >> 8),
                                                (char)uVar2 + 0x69U ^ (byte)uVar24)));
                uVar21 = uVar21 + 4;
              } while (uVar21 != 0x48);
              DAT_0a3e2eba = 1;
            }
            lVar6 = 0;
            do {
              lVar17 = lVar6;
              uVar10 = (uint)uVar16;
              *(undefined1 *)((long)&local_188 + lVar17) =
                   *(undefined1 *)
                    ((long)&DAT_0a3e2e72 + (ulong)(uVar10 + (int)(uVar16 / 10) * -10 + 0x23));
              uVar16 = uVar16 / 10;
              lVar6 = lVar17 + 1;
            } while (9 < uVar10);
            *(undefined1 *)((long)&local_188 + lVar17 + 1) = 0;
            if (8 < lVar17 + 8U) {
              puVar18 = (undefined1 *)((long)&local_188 + lVar17);
              puVar7 = (undefined1 *)((long)&local_188 + 1);
              do {
                uVar1 = *puVar18;
                *puVar18 = puVar7[-1];
                puVar7[-1] = uVar1;
                bVar5 = puVar7 < puVar18 + -1;
                puVar18 = puVar18 + -1;
                puVar7 = puVar7 + 1;
              } while (bVar5);
            }
            local_190 = (undefined8 ***)&local_188;
            if (local_320 == 0) {
              uVar16 = 0;
            }
            else {
              uVar16 = (ulong)*(uint *)(local_320 + 0x10);
            }
            local_1e0 = (undefined8 ***)&local_1d8;
            lVar6 = 0;
            do {
              lVar17 = lVar6;
              uVar10 = (uint)uVar16;
              *(undefined1 *)((long)&local_1d8 + lVar17) =
                   *(undefined1 *)
                    ((long)&DAT_0a3e2e72 + (ulong)(uVar10 + (int)(uVar16 / 10) * -10 + 0x23));
              lVar6 = lVar17 + 1;
              uVar16 = uVar16 / 10;
            } while (9 < uVar10);
            *(undefined1 *)((long)&local_1d8 + lVar17 + 1) = 0;
            if (8 < lVar17 + 8U) {
              puVar18 = (undefined1 *)((long)&local_1d8 + lVar17);
              puVar7 = (undefined1 *)((long)&local_1d8 + 1);
              do {
                uVar1 = *puVar18;
                *puVar18 = puVar7[-1];
                puVar7[-1] = uVar1;
                bVar5 = puVar7 < puVar18 + -1;
                puVar18 = puVar18 + -1;
                puVar7 = puVar7 + 1;
              } while (bVar5);
            }
            if ((int)local_350 == 0 && local_350._4_4_ == 0) {
              local_230 = (undefined8 ***)&DAT_0a3e2ecc;
              if ((DAT_0a3e2ed2 & 1) == 0) {
                DAT_0a3e2ecc = (undefined4)DAT_0847fe48;
                puVar7 = &DAT_0a3e2ed0;
                puVar18 = &DAT_0a3e2ed1;
                puVar20 = &DAT_0a3e2ed2;
                goto LAB_03182f74;
              }
            }
            else {
              local_230 = (undefined8 ***)&DAT_0a3e2ec4;
              if ((DAT_0a3e2ec9 & 1) == 0) {
                DAT_0a3e2ec4 = 0x7274;
                DAT_0a3e2ec6 = 0x75;
                puVar18 = &DAT_0a3e2ec8;
                puVar7 = &DAT_0a3e2ec7;
                puVar20 = &DAT_0a3e2ec9;
LAB_03182f74:
                *puVar7 = 0x65;
                *puVar18 = 0;
                *puVar20 = 1;
              }
            }
            local_228 = 0;
            if ((DAT_0a3e0477 & 1) == 0) {
              uVar16 = 0;
              do {
                uVar23 = *(undefined4 *)((long)&DAT_088c1812 + uVar16);
                uVar2 = CONCAT12((char)((uint)uVar23 >> 8),(short)uVar23) & 0xff00ff;
                uVar24 = *(undefined4 *)((long)&DAT_088c17fe + uVar16 % 0x14);
                *(uint *)((long)&DAT_0a3e0427 + uVar16) =
                     CONCAT13((char)((uint)uVar23 >> 0x18) + 0x69U ^ (byte)((uint)uVar24 >> 0x18),
                              CONCAT12((char)((uint)uVar23 >> 0x10) + 0x69U ^
                                       (byte)((uint)uVar24 >> 0x10),
                                       CONCAT11((char)(uVar2 >> 0x10) + 0x69U ^
                                                (byte)((uint)uVar24 >> 8),
                                                (char)uVar2 + 0x69U ^ (byte)uVar24)));
                uVar16 = uVar16 + 4;
              } while (uVar16 != 0x50);
              DAT_0a3e0477 = 1;
            }
            local_f0 = &local_140;
            pppuStack_e8 = &local_190;
            local_e0 = &local_1e0;
            pppuStack_d8 = &local_230;
            uStack_c8 = 0;
            local_d0 = 0;
            uStack_b8 = 0;
            uStack_c0 = 0;
            uStack_a8 = 0;
            local_b0 = 0;
            uStack_98 = 0;
            uStack_a0 = 0;
            uStack_88 = 0;
            local_90 = 0;
            local_78 = 0;
            uStack_80 = 0;
            FUN_05e1d31c(local_310,&DAT_0a3e0427,&local_f0);
            if (cStack_379 < '\0') {
              __ZdlPvm(local_390[0],CONCAT17(cStack_379,local_380) & 0x7fffffffffffffff);
            }
            uVar13 = thunk_FUN_05e1d0bc(local_310);
            local_3a0 = lVar11;
            if (cStack_361 < '\0') {
              uVar13 = __ZdlPvm(local_378[0],CONCAT17(cStack_361,local_368) & 0x7fffffffffffffff);
            }
          }
          lVar11 = *(long *)(param_1 + 0xb20);
          local_398 = local_278;
          if (local_278 != (long *)0x0) {
            local_278[1] = local_278[1] + 1;
          }
          FUN_031cae30(uVar13,lVar11 + 0x60,&local_3a0,local_3a0 + 0x38);
          plVar22 = local_398;
          if (local_398 != (long *)0x0) {
            LOAcquire();
            lVar11 = local_398[1];
            local_398[1] = lVar11 + -1;
            LORelease();
            if (lVar11 == 0) {
              (**(code **)(*local_398 + 0x10))(local_398);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar22);
            }
          }
          lVar11 = local_280;
          if (((int)local_350 == 0 && local_350._4_4_ == 0) &&
             (uVar16 = FUN_030f321c(local_280), (uVar16 & 1) != 0)) {
            FUN_030f3214(lVar11,4);
            lVar6 = *(long *)(param_1 + 0xb20);
            local_3f0 = lVar11;
            local_3e8 = local_278;
            if (local_278 != (long *)0x0) {
              local_278[1] = local_278[1] + 1;
            }
            uVar13 = FUN_030f31fc(local_310,lVar11);
            FUN_03181628(uVar13,lVar6 + 0x88,&local_3f0,local_310);
            if (cStack_2f9 < '\0') {
              __ZdlPvm(local_310[0],CONCAT17(cStack_2f9,local_300) & 0x7fffffffffffffff);
            }
            plVar22 = local_3e8;
            if (local_3e8 != (long *)0x0) {
              LOAcquire();
              lVar11 = local_3e8[1];
              local_3e8[1] = lVar11 + -1;
              LORelease();
              if (lVar11 == 0) {
                (**(code **)(*local_3e8 + 0x10))(local_3e8);
                __ZNSt3__119__shared_weak_count14__release_weakEv(plVar22);
              }
            }
            local_f0 = (undefined8 ***)&SUB_aaaaaaaaaaaaaaaa;
            pppuStack_e8 = (undefined8 ***)&SUB_aaaaaaaaaaaaaaaa;
            FUN_04669774();
            FUN_0466ad74(&local_140);
            pppuVar3 = local_140;
            if ((DAT_0a3e0376 & 1) == 0) {
              _DAT_0a3e0360 = CONCAT44((int)DAT_088ba9e0,(int)DAT_08482fd0);
              uRam000000000a3e0368 = CONCAT44((int)DAT_084c7820,(int)DAT_08483880);
              DAT_0a3e0370 = (undefined4)DAT_085b0718;
              DAT_0a3e0374 = 0x65;
              DAT_0a3e0376 = 1;
            }
            if ((DAT_0a3dd403 & 1) == 0) {
              uVar16 = 0;
              do {
                (&DAT_0a3dd39e)[uVar16] =
                     (&DAT_088bcf0a)[uVar16] + 0x8a ^ (&DAT_088bcefa)[uVar16 & 0xf];
                uVar16 = uVar16 + 1;
              } while (uVar16 != 0x65);
              DAT_0a3dd403 = 1;
            }
            FUN_0003bb6c(local_310,&DAT_0a3e0360,&DAT_0a3dd39e,0x1051);
            plVar22 = local_278;
            lVar11 = local_280;
            if (local_278 != (long *)0x0) {
              local_278[1] = local_278[1] + 1;
            }
            if (*(char *)((long)param_2 + 0x17) < '\0') {
              FUN_00018d20(&local_408,*param_2,param_2[1]);
            }
            else {
              lStack_400 = param_2[1];
              local_408 = *param_2;
              local_3f8 = param_2[2];
            }
            local_238 = (long *)0x0;
            plVar14 = (long *)__Znwm(0x38);
            plVar14[2] = (long)plVar22;
            plVar14[1] = lVar11;
            *plVar14 = (long)&PTR_FUN_09def270;
            plVar14[3] = param_1;
            if ((long)local_3f8 < 0) {
              FUN_00018d20(plVar14 + 4,local_408,lStack_400);
            }
            else {
              plVar14[5] = lStack_400;
              plVar14[4] = local_408;
              plVar14[6] = local_3f8;
            }
            if (plVar22 != (long *)0x0) {
              plVar22[1] = plVar22[1] + 1;
            }
            local_258 = (long *)0x0;
            local_238 = plVar14;
            local_258 = (long *)__Znwm(0x20);
            *local_258 = (long)&PTR_FUN_09def2f0;
            local_258[1] = lVar11;
            local_258[2] = (long)plVar22;
            local_258[3] = param_1;
            FUN_0453d344(&local_f0,pppuVar3,local_310,alStack_250,alStack_270,0);
            if (local_258 == alStack_270) {
              pcVar15 = *(code **)(*local_258 + 0x20);
LAB_031837cc:
              (*pcVar15)();
            }
            else if (local_258 != (long *)0x0) {
              pcVar15 = *(code **)(*local_258 + 0x28);
              goto LAB_031837cc;
            }
            if (local_238 == alStack_250) {
              pcVar15 = *(code **)(*local_238 + 0x20);
LAB_031837f8:
              (*pcVar15)();
            }
            else if (local_238 != (long *)0x0) {
              pcVar15 = *(code **)(*local_238 + 0x28);
              goto LAB_031837f8;
            }
            if ((long)local_3f8 < 0) {
              __ZdlPvm(local_408,local_3f8 & 0x7fffffffffffffff);
            }
            plVar22 = (long *)CONCAT71(uStack_137,local_138);
            if (plVar22 != (long *)0x0) {
              LOAcquire();
              lVar11 = plVar22[1];
              plVar22[1] = lVar11 + -1;
              LORelease();
              if (lVar11 == 0) {
                (**(code **)(*plVar22 + 0x10))(plVar22);
                __ZNSt3__119__shared_weak_count14__release_weakEv(plVar22);
              }
            }
            pppuVar3 = pppuStack_e8;
            if ((undefined8 ****)pppuStack_e8 != (undefined8 ****)0x0) {
              ppppuVar12 = (undefined8 ****)(pppuStack_e8 + 1);
              *ppppuVar12 = (undefined8 ***)((long)*ppppuVar12 + 1);
              *ppppuVar12 = (undefined8 ***)((long)*ppppuVar12 + 1);
            }
            plVar22 = *(long **)(local_280 + 0x58);
            *(undefined8 ****)(local_280 + 0x50) = local_f0;
            *(undefined8 ****)(local_280 + 0x58) = pppuStack_e8;
            if (plVar22 != (long *)0x0) {
              LOAcquire();
              lVar11 = plVar22[1];
              plVar22[1] = lVar11 + -1;
              LORelease();
              if (lVar11 == 0) {
                (**(code **)(*plVar22 + 0x10))(plVar22);
                __ZNSt3__119__shared_weak_count14__release_weakEv(plVar22);
              }
            }
            if ((undefined8 ****)pppuVar3 != (undefined8 ****)0x0) {
              LOAcquire();
              pppuVar8 = (undefined8 ***)pppuVar3[1];
              pppuVar3[1] = (undefined8 ***)((long)pppuVar8 + -1);
              LORelease();
              if (pppuVar8 == (undefined8 ***)0x0) {
                (*(code *)(*pppuVar3)[2])(pppuVar3);
                __ZNSt3__119__shared_weak_count14__release_weakEv(pppuVar3);
              }
            }
            pppuVar3 = pppuStack_e8;
            if ((undefined8 ****)pppuStack_e8 != (undefined8 ****)0x0) {
              LOAcquire();
              pppuVar8 = (undefined8 ***)pppuStack_e8[1];
              pppuStack_e8[1] = (undefined8 ***)((long)pppuVar8 + -1);
              LORelease();
              if (pppuVar8 == (undefined8 ***)0x0) {
                (*(code *)(*pppuStack_e8)[2])(pppuStack_e8);
                __ZNSt3__119__shared_weak_count14__release_weakEv(pppuVar3);
              }
            }
          }
          else {
            iVar9 = thunk_FUN_05e1d97c(4);
            local_3b0 = local_280;
            if (iVar9 != 0) {
              FUN_0488143c(&local_190);
              ppppuVar12 = (undefined8 ****)local_190;
              if (-1 < cStack_179) {
                ppppuVar12 = &local_190;
              }
              if ((DAT_0a3dd363 & 1) == 0) {
                uVar16 = 0;
                do {
                  (&DAT_0a3dd350)[uVar16] =
                       (&DAT_088bce97)[uVar16] + 0x8a ^ (&DAT_088bce87)[uVar16 & 0xf];
                  uVar16 = uVar16 + 1;
                } while (uVar16 != 0x13);
                DAT_0a3dd363 = 1;
              }
              if ((DAT_0a3e0376 & 1) == 0) {
                _DAT_0a3e0360 = CONCAT44((int)DAT_088ba9e0,(int)DAT_08482fd0);
                uRam000000000a3e0368 = CONCAT44((int)DAT_084c7820,(int)DAT_08483880);
                DAT_0a3e0370 = (undefined4)DAT_085b0718;
                DAT_0a3e0374 = 0x65;
                DAT_0a3e0376 = 1;
              }
              FUN_05e1d050(local_310,4,ppppuVar12,&DAT_0a3dd350,&DAT_0a3e0360,"",0,0);
              lVar11 = local_280;
              FUN_030f1f08(&local_1e0,local_280);
              local_140 = local_1e0;
              if (-1 < cStack_1c9) {
                local_140 = &local_1e0;
              }
              local_138 = 0;
              if ((DAT_0a3e04aa & 1) == 0) {
                _DAT_0a3e0478 = CONCAT44((int)DAT_084ec280,(int)DAT_08486a48);
                uRam000000000a3e0480 = CONCAT44((int)DAT_084ee568,(int)DAT_084e3ff8);
                _DAT_0a3e0488 = CONCAT44((int)DAT_084fc108,(int)DAT_08538cf0);
                uRam000000000a3e0490 = CONCAT44((int)DAT_087f8a18,(int)DAT_08490810);
                _DAT_0a3e0498 = CONCAT44((int)DAT_084a66b0,(int)DAT_085095c0);
                uRam000000000a3e04a0 = CONCAT44((int)DAT_08606108,(int)DAT_08698728);
                DAT_0a3e04a8 = 0x65;
                DAT_0a3e04aa = 1;
              }
              local_e0 = (undefined8 ****)0x0;
              pppuStack_e8 = (undefined8 ****)0x0;
              local_f0 = &local_140;
              local_d0 = 0;
              pppuStack_d8 = (undefined8 ****)0x0;
              uStack_c0 = 0;
              uStack_c8 = 0;
              local_b0 = 0;
              uStack_b8 = 0;
              uStack_a0 = 0;
              uStack_a8 = 0;
              local_90 = 0;
              uStack_98 = 0;
              uStack_80 = 0;
              uStack_88 = 0;
              local_78 = 0;
              FUN_05e1d31c(local_310,&DAT_0a3e0478,&local_f0);
              if (cStack_1c9 < '\0') {
                __ZdlPvm(local_1e0,CONCAT17(cStack_1c9,local_1d0) & 0x7fffffffffffffff);
              }
              thunk_FUN_05e1d0bc(local_310);
              local_3b0 = lVar11;
              if (cStack_179 < '\0') {
                __ZdlPvm(local_190,CONCAT17(cStack_179,local_180) & 0x7fffffffffffffff);
              }
            }
            local_3a8 = local_278;
            if (local_278 != (long *)0x0) {
              local_278[1] = local_278[1] + 1;
            }
            local_3e0 = local_350;
            if ((long)puStack_338 < 0) {
              FUN_00018d20(&local_3d8,puStack_348,local_340);
            }
            else {
              puVar19 = (undefined8 *)((ulong)&local_350 | 8);
              uStack_3d0 = puVar19[1];
              local_3d8 = *puVar19;
              local_3c8 = puVar19[2];
            }
            local_3c0 = local_330;
            local_3b8 = local_328;
            lVar11 = 0;
            if (local_328 != (long *)0x0) {
              lVar11 = local_328[1];
              local_328[1] = lVar11 + 1;
            }
            FUN_0488b574(lVar11,&local_3b0,&local_3e0);
            plVar22 = local_3b8;
            if (local_3b8 != (long *)0x0) {
              LOAcquire();
              lVar11 = local_3b8[1];
              local_3b8[1] = lVar11 + -1;
              LORelease();
              if (lVar11 == 0) {
                (**(code **)(*local_3b8 + 0x10))(local_3b8);
                __ZNSt3__119__shared_weak_count14__release_weakEv(plVar22);
              }
            }
            if ((long)local_3c8 < 0) {
              __ZdlPvm(local_3d8,local_3c8 & 0x7fffffffffffffff);
            }
            plVar22 = local_3a8;
            if (local_3a8 != (long *)0x0) {
              LOAcquire();
              lVar11 = local_3a8[1];
              local_3a8[1] = lVar11 + -1;
              LORelease();
              if (lVar11 == 0) {
                (**(code **)(*local_3a8 + 0x10))(local_3a8);
                __ZNSt3__119__shared_weak_count14__release_weakEv(plVar22);
              }
            }
            FUN_03182084(param_1,param_2);
          }
          plVar22 = local_328;
          if (local_328 != (long *)0x0) {
            LOAcquire();
            lVar11 = local_328[1];
            local_328[1] = lVar11 + -1;
            LORelease();
            if (lVar11 == 0) {
              (**(code **)(*local_328 + 0x10))(local_328);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar22);
            }
          }
          if ((long)puStack_338 < 0) {
            __ZdlPvm(puStack_348,(ulong)puStack_338 & 0x7fffffffffffffff);
          }
          plVar22 = local_318;
          if (local_318 != (long *)0x0) {
            LOAcquire();
            lVar11 = local_318[1];
            local_318[1] = lVar11 + -1;
            LORelease();
            if (lVar11 == 0) {
              (**(code **)(*local_318 + 0x10))(local_318);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar22);
            }
          }
          goto LAB_03183678;
        }
        goto LAB_031824dc;
      }
      iVar9 = thunk_FUN_05e1d97c(2);
      if (iVar9 != 0) {
        FUN_0488143c(&local_190);
        ppppuVar12 = (undefined8 ****)local_190;
        if (-1 < cStack_179) {
          ppppuVar12 = &local_190;
        }
        if ((DAT_0a3dd363 & 1) == 0) {
          uVar16 = 0;
          do {
            (&DAT_0a3dd350)[uVar16] = (&DAT_088bce97)[uVar16] + 0x8a ^ (&DAT_088bce87)[uVar16 & 0xf]
            ;
            uVar16 = uVar16 + 1;
          } while (uVar16 != 0x13);
          DAT_0a3dd363 = 1;
        }
        if ((DAT_0a3e0376 & 1) == 0) {
          _DAT_0a3e0360 = CONCAT44((int)DAT_088ba9e0,(int)DAT_08482fd0);
          uRam000000000a3e0368 = CONCAT44((int)DAT_084c7820,(int)DAT_08483880);
          DAT_0a3e0370 = (undefined4)DAT_085b0718;
          DAT_0a3e0374 = 0x65;
          DAT_0a3e0376 = 1;
        }
        FUN_05e1d050(local_310,2,ppppuVar12,&DAT_0a3dd350,&DAT_0a3e0360,"ersions/A/CoreFoundation",0
                     ,0);
        FUN_030f1f08(&local_1e0,*plVar22);
        local_140 = local_1e0;
        if (-1 < cStack_1c9) {
          local_140 = &local_1e0;
        }
        local_138 = 0;
        if ((DAT_0a3e0392 & 1) == 0) {
          _DAT_0a3e0378 = CONCAT44((int)DAT_084cae10,(int)DAT_084a8ea0);
          uRam000000000a3e0380 = CONCAT44((int)DAT_084fdd78,(int)DAT_0849a618);
          DAT_0a3e0388 = CONCAT44((int)DAT_088ba9e8,(int)DAT_084cadd8);
          DAT_0a3e0390 = 0x67;
          DAT_0a3e0392 = 1;
        }
        local_e0 = (undefined8 ****)0x0;
        pppuStack_e8 = (undefined8 ****)0x0;
        local_f0 = &local_140;
        local_d0 = 0;
        pppuStack_d8 = (undefined8 ****)0x0;
        uStack_c0 = 0;
        uStack_c8 = 0;
        local_b0 = 0;
        uStack_b8 = 0;
        uStack_a0 = 0;
        uStack_a8 = 0;
        local_90 = 0;
        uStack_98 = 0;
        uStack_80 = 0;
        uStack_88 = 0;
        local_78 = 0;
        FUN_05e1d31c(local_310,&DAT_0a3e0378,&local_f0);
        if (cStack_1c9 < '\0') {
          __ZdlPvm(local_1e0,CONCAT17(cStack_1c9,local_1d0) & 0x7fffffffffffffff);
        }
        thunk_FUN_05e1d0bc(local_310);
        if (cStack_179 < '\0') {
          uVar16 = CONCAT17(cStack_179,local_180);
          ppppuVar12 = (undefined8 ****)local_190;
          goto LAB_0318269c;
        }
      }
      goto LAB_03183678;
    }
LAB_031824dc:
    iVar9 = thunk_FUN_05e1d97c(2);
    if (iVar9 != 0) {
      FUN_0488143c(&local_140);
      ppppuVar12 = (undefined8 ****)local_140;
      if (-1 < cStack_129) {
        ppppuVar12 = &local_140;
      }
      if ((DAT_0a3dd363 & 1) == 0) {
        uVar16 = 0;
        do {
          (&DAT_0a3dd350)[uVar16] = (&DAT_088bce97)[uVar16] + 0x8a ^ (&DAT_088bce87)[uVar16 & 0xf];
          uVar16 = uVar16 + 1;
        } while (uVar16 != 0x13);
        DAT_0a3dd363 = 1;
      }
      if ((DAT_0a3e0376 & 1) == 0) {
        _DAT_0a3e0360 = CONCAT44((int)DAT_088ba9e0,(int)DAT_08482fd0);
        uRam000000000a3e0368 = CONCAT44((int)DAT_084c7820,(int)DAT_08483880);
        DAT_0a3e0370 = (undefined4)DAT_085b0718;
        DAT_0a3e0374 = 0x65;
        DAT_0a3e0376 = 1;
      }
      FUN_05e1d050(local_310,2,ppppuVar12,&DAT_0a3dd350,&DAT_0a3e0360,"eFoundation",0,0);
      if ((DAT_0a3e03e1 & 1) == 0) {
        _DAT_0a3e03c0 = CONCAT44((int)DAT_084a04e8,(int)DAT_084c7770);
        uRam000000000a3e03c8 = CONCAT44((int)DAT_086cac68,(int)DAT_085b4510);
        _DAT_0a3e03d0 = CONCAT44((int)DAT_084a8ea0,(int)DAT_088ba9f8);
        uRam000000000a3e03d8 = CONCAT44((int)DAT_0849a618,(int)DAT_0849a568);
        DAT_0a3e03e0 = 0;
        DAT_0a3e03e1 = 1;
      }
      uStack_88 = 0;
      local_90 = 0;
      local_78 = 0;
      uStack_80 = 0;
      uStack_a8 = 0;
      local_b0 = 0;
      uStack_98 = 0;
      uStack_a0 = 0;
      uStack_c8 = 0;
      local_d0 = 0;
      uStack_b8 = 0;
      uStack_c0 = 0;
      pppuStack_e8 = (undefined8 ****)0x0;
      local_f0 = (undefined8 ****)0x0;
      pppuStack_d8 = (undefined8 ****)0x0;
      local_e0 = (undefined8 ****)0x0;
      FUN_05e1d31c(local_310,&DAT_0a3e03c0,&local_f0);
      thunk_FUN_05e1d0bc(local_310);
      if (cStack_129 < '\0') {
        uVar16 = CONCAT17(cStack_129,local_130);
        ppppuVar12 = (undefined8 ****)local_140;
LAB_0318269c:
        __ZdlPvm(ppppuVar12,uVar16 & 0x7fffffffffffffff);
      }
    }
LAB_03183678:
    plVar22 = local_278;
    if (local_278 != (long *)0x0) {
      LOAcquire();
      lVar11 = local_278[1];
      local_278[1] = lVar11 + -1;
      LORelease();
      if (lVar11 == 0) {
        (**(code **)(*local_278 + 0x10))(local_278);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar22);
      }
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
code_r0x0318210c:
  plVar22 = plVar22 + 2;
  if (plVar22 == plVar14) goto LAB_031824dc;
  goto LAB_031820e4;
}


