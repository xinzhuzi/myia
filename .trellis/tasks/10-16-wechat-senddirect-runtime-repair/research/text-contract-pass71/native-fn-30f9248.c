// Ghidra inferred pseudocode; requested=0x30f9248
// entry=030f9248 end=030fa907

/* WARNING: Removing unreachable block (ram,0x030f9b60) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_030f9248(long *param_1,undefined8 param_2,long *param_3)

{
  undefined8 *******pppppppuVar1;
  undefined1 uVar2;
  uint3 uVar3;
  long *plVar4;
  bool bVar5;
  long lVar6;
  long ******pppppplVar7;
  int iVar8;
  undefined4 uVar9;
  ulong uVar10;
  undefined8 *puVar11;
  long *plVar12;
  undefined8 uVar13;
  long *******ppppppplVar14;
  char cVar15;
  undefined1 *puVar16;
  undefined1 *puVar17;
  ulong uVar18;
  undefined1 *puVar19;
  uint uVar20;
  long lVar21;
  int iVar22;
  long lVar23;
  long lVar24;
  undefined4 uVar25;
  long local_3c0;
  long *local_3b8;
  long *******local_3b0 [2];
  undefined7 local_3a0;
  char cStack_399;
  long *******local_398 [2];
  undefined7 local_388;
  char cStack_381;
  long local_380;
  long *local_378;
  undefined8 local_370;
  undefined1 *puStack_368;
  undefined1 *local_360;
  undefined1 *puStack_358;
  undefined1 *local_350;
  long *local_348;
  undefined1 *local_340;
  undefined1 *puStack_338;
  undefined8 local_330;
  undefined1 *puStack_328;
  undefined1 *local_320;
  undefined1 *local_318;
  long *local_310;
  long *******local_308;
  ulong local_300;
  ulong local_2f8;
  uint local_2f0;
  undefined4 uStack_2ec;
  long *local_2e8;
  long local_280;
  long *local_278;
  undefined8 *******local_270;
  undefined8 local_268;
  undefined7 local_260;
  char cStack_259;
  long *******local_220;
  undefined8 local_218;
  undefined7 local_210;
  char cStack_209;
  undefined1 uStack_1d1;
  undefined8 local_1d0;
  undefined8 local_1c8;
  undefined7 local_1c0;
  char cStack_1b9;
  undefined1 uStack_181;
  undefined8 local_180;
  undefined1 local_178 [72];
  long *******local_130;
  undefined1 local_128;
  undefined7 uStack_127;
  undefined7 local_120;
  char cStack_119;
  long *******local_e0;
  long *plStack_d8;
  undefined8 *local_d0;
  long *******ppppppplStack_c8;
  undefined8 *******local_c0;
  undefined8 uStack_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 local_70;
  undefined8 uStack_68;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar23 = *(long *)(*param_3 + 0x18);
  local_278 = *(long **)(*param_3 + 0x20);
  lVar6 = 0;
  if (local_278 != (long *)0x0) {
    lVar6 = local_278[1];
    local_278[1] = lVar6 + 1;
  }
  param_1[3] = (long)&SUB_aaaaaaaaaaaaaaaa;
  param_1[2] = (long)&SUB_aaaaaaaaaaaaaaaa;
  param_1[5] = (long)&SUB_aaaaaaaaaaaaaaaa;
  param_1[4] = (long)&SUB_aaaaaaaaaaaaaaaa;
  param_1[1] = (long)&SUB_aaaaaaaaaaaaaaaa;
  *param_1 = (long)&SUB_aaaaaaaaaaaaaaaa;
  local_280 = lVar23;
  FUN_0304f1cc(lVar6,param_1,0,0);
  iVar8 = FUN_04bb6cd4(lVar23 + 0x30);
  if ((iVar8 == 0) || (uVar10 = FUN_04a2eed8(lVar23), (uVar10 & 1) != 0)) {
    if (lVar23 != 0) {
      puStack_328 = &SUB_aaaaaaaaaaaaaaaa;
      local_330 = &SUB_aaaaaaaaaaaaaaaa;
      local_318 = &SUB_aaaaaaaaaaaaaaaa;
      local_320 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_338 = &SUB_aaaaaaaaaaaaaaaa;
      local_340 = &SUB_aaaaaaaaaaaaaaaa;
      FUN_0465bdac(&local_340);
      local_318 = (undefined1 *)((ulong)local_318 | 1);
      local_320 = (undefined1 *)CONCAT44(local_320._4_4_,1);
      lVar6 = (long)(int)local_330;
      if ((int)local_330 < local_330._4_4_) {
        local_330 = (undefined1 *)CONCAT44(local_330._4_4_,(int)local_330 + 1);
        lVar6 = *(long *)(puStack_338 + lVar6 * 8);
      }
      else {
        if (local_330._4_4_ == (int)puStack_328) {
          FUN_05ab4038((ulong)&local_340 | 8,local_330._4_4_ + 1);
        }
        local_330._4_4_ = local_330._4_4_ + 1;
        lVar6 = __Znwm(0x38);
        FUN_0465bd88();
        lVar24 = (long)(int)local_330;
        local_330 = (undefined1 *)CONCAT44(local_330._4_4_,(int)local_330 + 1);
        *(long *)(puStack_338 + lVar24 * 8) = lVar6;
      }
      *(uint *)(lVar6 + 0x34) = *(uint *)(lVar6 + 0x34) | 2;
      puVar11 = *(undefined8 **)(lVar6 + 0x10);
      if (puVar11 == &DAT_0a524ad0) {
        puVar11 = (undefined8 *)__Znwm(0x18);
        *puVar11 = 0;
        puVar11[1] = 0;
        puVar11[2] = 0;
        *(undefined8 **)(lVar6 + 0x10) = puVar11;
      }
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (puVar11,lVar23 + 0x130);
      *(uint *)(lVar6 + 0x34) = *(uint *)(lVar6 + 0x34) | 1;
      lVar24 = *(long *)(lVar6 + 8);
      if (lVar24 == 0) {
        lVar24 = __Znwm(0x18);
        FUN_04f33c00();
        *(long *)(lVar6 + 8) = lVar24;
      }
      *(uint *)(lVar24 + 0x14) = *(uint *)(lVar24 + 0x14) | 1;
      puVar11 = *(undefined8 **)(lVar24 + 8);
      if (puVar11 == &DAT_0a524ad0) {
        puVar11 = (undefined8 *)__Znwm(0x18);
        *puVar11 = 0;
        puVar11[1] = 0;
        puVar11[2] = 0;
        *(undefined8 **)(lVar24 + 8) = puVar11;
      }
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (puVar11,lVar23 + 0x30);
      uVar9 = *(undefined4 *)(lVar23 + 0xc);
      uVar20 = *(uint *)(lVar6 + 0x34);
      *(uint *)(lVar6 + 0x34) = uVar20 | 4;
      *(undefined4 *)(lVar6 + 0x18) = uVar9;
      uVar9 = *(undefined4 *)(lVar23 + 0x114);
      *(uint *)(lVar6 + 0x34) = uVar20 | 0xc;
      *(undefined4 *)(lVar6 + 0x1c) = uVar9;
      FUN_030f2168(&local_310,*param_3);
      uVar9 = FUN_00033fcc(&local_310);
      *(uint *)(lVar6 + 0x34) = *(uint *)(lVar6 + 0x34) | 0x10;
      *(undefined4 *)(lVar6 + 0x28) = uVar9;
      if ((long)local_300 < 0) {
        __ZdlPvm(local_310,local_300 & 0x7fffffffffffffff);
        cVar15 = *(char *)(lVar23 + 0x177);
        if (-1 < cVar15) goto LAB_030f96c4;
LAB_030f96e4:
        if (*(long *)(lVar23 + 0x168) != 0) {
LAB_030f96ec:
          *(uint *)(lVar6 + 0x34) = *(uint *)(lVar6 + 0x34) | 0x20;
          puVar11 = *(undefined8 **)(lVar6 + 0x20);
          if (puVar11 == &DAT_0a524ad0) {
            puVar11 = (undefined8 *)__Znwm(0x18);
            *puVar11 = 0;
            puVar11[1] = 0;
            puVar11[2] = 0;
            *(undefined8 **)(lVar6 + 0x20) = puVar11;
          }
          __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                    (puVar11,lVar23 + 0x160);
        }
      }
      else {
        cVar15 = *(char *)(lVar23 + 0x177);
        if (cVar15 < '\0') goto LAB_030f96e4;
LAB_030f96c4:
        if (cVar15 != '\0') goto LAB_030f96ec;
      }
      puStack_358 = &SUB_aaaaaaaaaaaaaaaa;
      local_360 = &SUB_aaaaaaaaaaaaaaaa;
      local_348 = (long *)&SUB_aaaaaaaaaaaaaaaa;
      local_350 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_368 = &SUB_aaaaaaaaaaaaaaaa;
      local_370 = &SUB_aaaaaaaaaaaaaaaa;
      plVar12 = (long *)FUN_04669774();
      uVar13 = (**(code **)(*plVar12 + 0x18))();
      local_d0 = (undefined8 *)((ulong)local_d0 & 0xffffffffffffff);
      local_e0 = (long *******)((ulong)local_e0 & 0xffffffffffffff00);
      local_310 = DAT_0875d510;
      uStack_2ec = 0;
      local_300 = 0;
      local_2f8 = 0;
      local_308 = (long *******)0x0;
      local_2f0 = local_2f0 & 0xffffff00;
      FUN_030bee20(&local_370,uVar13,&local_340,&local_e0,&local_310);
      if ((long)local_2f8 < 0) {
        __ZdlPvm(local_308,local_2f8 & 0x7fffffffffffffff);
      }
      if (((int)local_370 == 0 && local_370._4_4_ == 0) && (*(int *)(local_350 + 0x28) != 0)) {
        lVar23 = **(long **)(local_350 + 0x10);
        if (*(int *)(lVar23 + 0x10) == 0) {
          plVar12 = *(long **)(*param_3 + 8);
          if (plVar12 == (long *)0x0) {
            local_310 = (long *)0x0;
            local_308 = (long *******)0x0;
          }
          else {
            local_308 = *(long ********)(*param_3 + 0x10);
            local_310 = plVar12;
            if (local_308 != (long *******)0x0) {
              local_308[1] = (long ******)((long)local_308[1] + 1);
            }
          }
          iVar8 = (**(code **)(*plVar12 + 0x20))();
          ppppppplVar14 = local_308;
          if (local_308 != (long *******)0x0) {
            LOAcquire();
            pppppplVar7 = local_308[1];
            local_308[1] = (long ******)((long)pppppplVar7 + -1);
            LORelease();
            if (pppppplVar7 == (long ******)0x0) {
              (*(code *)(*local_308)[2])(local_308);
              __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar14);
            }
          }
          lVar6 = local_280;
          *(undefined8 *)(local_280 + 0xf8) = *(undefined8 *)(lVar23 + 0x28);
          *(undefined4 *)(local_280 + 0x118) = 2;
          if (iVar8 == 2) {
            FUN_0466aca8(&local_130);
            FUN_01205740(&local_e0,local_130);
            FUN_0268f370(&local_310,local_e0);
            local_380 = lVar6;
            local_378 = local_278;
            lVar6 = 0;
            if (local_278 != (long *)0x0) {
              lVar6 = local_278[1];
              local_278[1] = lVar6 + 1;
            }
            FUN_031ee1a4(lVar6,local_310,&local_380,1,1);
            plVar12 = local_378;
            if (local_378 != (long *)0x0) {
              LOAcquire();
              lVar6 = local_378[1];
              local_378[1] = lVar6 + -1;
              LORelease();
              if (lVar6 == 0) {
                (**(code **)(*local_378 + 0x10))(local_378);
                __ZNSt3__119__shared_weak_count14__release_weakEv(plVar12);
              }
            }
            ppppppplVar14 = local_308;
            if (local_308 != (long *******)0x0) {
              LOAcquire();
              pppppplVar7 = local_308[1];
              local_308[1] = (long ******)((long)pppppplVar7 + -1);
              LORelease();
              if (pppppplVar7 == (long ******)0x0) {
                (*(code *)(*local_308)[2])(local_308);
                __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar14);
              }
            }
            plVar12 = plStack_d8;
            if (plStack_d8 != (long *)0x0) {
              LOAcquire();
              lVar6 = plStack_d8[1];
              plStack_d8[1] = lVar6 + -1;
              LORelease();
              if (lVar6 == 0) {
                (**(code **)(*plStack_d8 + 0x10))(plStack_d8);
                __ZNSt3__119__shared_weak_count14__release_weakEv(plVar12);
              }
            }
            plVar12 = (long *)CONCAT71(uStack_127,local_128);
            if (plVar12 != (long *)0x0) {
              LOAcquire();
              lVar6 = plVar12[1];
              plVar12[1] = lVar6 + -1;
              LORelease();
              if (lVar6 == 0) {
                (**(code **)(*plVar12 + 0x10))(plVar12);
                __ZNSt3__119__shared_weak_count14__release_weakEv(plVar12);
              }
            }
          }
          iVar8 = thunk_FUN_05e1d97c(2);
          if (iVar8 != 0) {
            FUN_0488143c(local_398);
            ppppppplVar14 = local_398[0];
            if (-1 < cStack_381) {
              ppppppplVar14 = (long *******)local_398;
            }
            if ((DAT_0a3d9c2e & 1) == 0) {
              _DAT_0a3d9c10 = CONCAT44((int)DAT_0849d6a0,(int)DAT_084aa8c0);
              uRam000000000a3d9c18 = CONCAT44((int)DAT_0848f630,(int)DAT_085095a8);
              DAT_0a3d9c20 = CONCAT44((int)DAT_08492398,(int)DAT_086d9ac8);
              DAT_0a3d9c28 = (undefined4)DAT_08596728;
              DAT_0a3d9c2c = 99;
              DAT_0a3d9c2e = 1;
            }
            if ((DAT_0a3d9ccc & 1) == 0) {
              _DAT_0a3d9cb0 = CONCAT44((int)DAT_088a7260,(int)DAT_087e2f50);
              uRam000000000a3d9cb8 = CONCAT44((int)DAT_08485e90,(int)DAT_084a8110);
              DAT_0a3d9cc0 = CONCAT44((int)DAT_0863e0f0,(int)DAT_088a7268);
              DAT_0a3d9cc8 = (undefined4)DAT_0847fdb8;
              DAT_0a3d9ccc = 1;
            }
            FUN_05e1d050(&local_310,2,ppppppplVar14,&DAT_0a3d9c10,&DAT_0a3d9cb0,0x6d,0,0);
            lVar6 = local_280;
            FUN_04cbe440(local_3b0,local_280);
            local_130 = local_3b0[0];
            if (-1 < cStack_399) {
              local_130 = (long *******)local_3b0;
            }
            local_128 = 0;
            uVar10 = *(ulong *)(lVar23 + 0x28);
            local_180 = (undefined1 *)0x0;
            if ((DAT_0a3d9e26 & 1) == 0) {
              uVar18 = 0;
              do {
                uVar9 = *(undefined4 *)((long)&DAT_088b16e6 + uVar18);
                uVar3 = CONCAT12((char)((uint)uVar9 >> 8),(short)uVar9) & 0xff00ff;
                uVar25 = *(undefined4 *)((long)&DAT_088b16d2 + uVar18 % 0x14);
                *(uint *)((long)&DAT_0a3d9dde + uVar18) =
                     CONCAT13((char)((uint)uVar9 >> 0x18) + 0x8aU ^ (byte)((uint)uVar25 >> 0x18),
                              CONCAT12((char)((uint)uVar9 >> 0x10) + 0x8aU ^
                                       (byte)((uint)uVar25 >> 0x10),
                                       CONCAT11((char)(uVar3 >> 0x10) + 0x8aU ^
                                                (byte)((uint)uVar25 >> 8),
                                                (char)uVar3 + 0x8aU ^ (byte)uVar25)));
                uVar18 = uVar18 + 4;
              } while (uVar18 != 0x48);
              DAT_0a3d9e26 = 1;
            }
            lVar24 = 0;
            do {
              lVar21 = lVar24;
              local_178[lVar21] = *(undefined1 *)(uVar10 % 10 + 0xa3d9e01);
              bVar5 = 9 < uVar10;
              uVar10 = uVar10 / 10;
              lVar24 = lVar21 + 1;
            } while (bVar5);
            local_178[lVar21 + 1] = 0;
            if (8 < lVar21 + 8U) {
              puVar19 = local_178;
              puVar16 = local_178 + lVar21;
              do {
                puVar19 = puVar19 + 1;
                uVar2 = *puVar16;
                puVar17 = puVar16 + -1;
                *puVar16 = puVar19[-1];
                puVar19[-1] = uVar2;
                puVar16 = puVar17;
              } while (puVar19 < puVar17);
            }
            local_180 = local_178;
            local_1d0 = (long *******)0x0;
            lVar24 = 0;
            uVar10 = (ulong)*(uint *)(lVar6 + 0x114);
            do {
              lVar6 = lVar24;
              uVar20 = (uint)uVar10;
              *(undefined1 *)((long)&local_1c8 + lVar6) =
                   *(undefined1 *)
                    ((long)&DAT_0a3d9dde + (ulong)(uVar20 + (int)(uVar10 / 10) * -10 + 0x23));
              lVar24 = lVar6 + 1;
              uVar10 = uVar10 / 10;
            } while (9 < uVar20);
            *(undefined1 *)((long)&local_1c8 + lVar6 + 1) = 0;
            if (8 < lVar6 + 8U) {
              puVar19 = (undefined1 *)((long)&local_1c8 + lVar6);
              puVar16 = (undefined1 *)((long)&local_1c8 + 1);
              do {
                uVar2 = *puVar19;
                *puVar19 = puVar16[-1];
                puVar16[-1] = uVar2;
                bVar5 = puVar16 < puVar19 + -1;
                puVar19 = puVar19 + -1;
                puVar16 = puVar16 + 1;
              } while (bVar5);
            }
            local_1d0 = (long *******)&local_1c8;
            local_220 = (long *******)0x0;
            lVar6 = 0;
            uVar10 = (ulong)*(uint *)(lVar23 + 0x1c);
            do {
              lVar24 = lVar6;
              uVar20 = (uint)uVar10;
              *(undefined1 *)((long)&local_218 + lVar24) =
                   *(undefined1 *)
                    ((long)&DAT_0a3d9dde + (ulong)(uVar20 + (int)(uVar10 / 10) * -10 + 0x23));
              lVar6 = lVar24 + 1;
              uVar10 = uVar10 / 10;
            } while (9 < uVar20);
            *(undefined1 *)((long)&local_218 + lVar24 + 1) = 0;
            if (8 < lVar24 + 8U) {
              puVar19 = (undefined1 *)((long)&local_218 + lVar24);
              puVar16 = (undefined1 *)((long)&local_218 + 1);
              do {
                uVar2 = *puVar19;
                *puVar19 = puVar16[-1];
                puVar16[-1] = uVar2;
                bVar5 = puVar16 < puVar19 + -1;
                puVar19 = puVar19 + -1;
                puVar16 = puVar16 + 1;
              } while (bVar5);
            }
            local_220 = (long *******)&local_218;
            local_270 = (undefined8 *******)&local_268;
            lVar6 = 0;
            uVar10 = (ulong)*(uint *)(lVar23 + 0x20);
            do {
              lVar23 = lVar6;
              uVar20 = (uint)uVar10;
              *(undefined1 *)((long)&local_268 + lVar23) =
                   *(undefined1 *)
                    ((long)&DAT_0a3d9dde + (ulong)(uVar20 + (int)(uVar10 / 10) * -10 + 0x23));
              lVar6 = lVar23 + 1;
              uVar10 = uVar10 / 10;
            } while (9 < uVar20);
            *(undefined1 *)((long)&local_268 + lVar23 + 1) = 0;
            if (8 < lVar23 + 8U) {
              puVar19 = (undefined1 *)((long)&local_268 + lVar23);
              puVar16 = (undefined1 *)((long)&local_268 + 1);
              do {
                uVar2 = *puVar19;
                *puVar19 = puVar16[-1];
                puVar16[-1] = uVar2;
                bVar5 = puVar16 < puVar19 + -1;
                puVar19 = puVar19 + -1;
                puVar16 = puVar16 + 1;
              } while (bVar5);
            }
            if ((DAT_0a3d9d49 & 1) == 0) {
              uVar10 = 0;
              do {
                uVar9 = *(undefined4 *)((long)&DAT_088b1435 + uVar10);
                uVar3 = CONCAT12((char)((uint)uVar9 >> 8),(short)uVar9) & 0xff00ff;
                uVar25 = *(undefined4 *)((long)&DAT_088b1421 + uVar10 % 0x14);
                *(uint *)((long)&DAT_0a3d9ce1 + uVar10) =
                     CONCAT13((char)((uint)uVar9 >> 0x18) + 0x8aU ^ (byte)((uint)uVar25 >> 0x18),
                              CONCAT12((char)((uint)uVar9 >> 0x10) + 0x8aU ^
                                       (byte)((uint)uVar25 >> 0x10),
                                       CONCAT11((char)(uVar3 >> 0x10) + 0x8aU ^
                                                (byte)((uint)uVar25 >> 8),
                                                (char)uVar3 + 0x8aU ^ (byte)uVar25)));
                uVar10 = uVar10 + 4;
              } while (uVar10 != 0x68);
              DAT_0a3d9d49 = 1;
            }
            local_e0 = (long *******)&local_130;
            plStack_d8 = &local_180;
            local_d0 = &local_1d0;
            ppppppplStack_c8 = (long *******)&local_220;
            local_c0 = &local_270;
            local_b0 = 0;
            uStack_b8 = 0;
            local_a0 = 0;
            uStack_a8 = 0;
            local_90 = 0;
            uStack_98 = 0;
            local_80 = 0;
            uStack_88 = 0;
            local_70 = 0;
            uStack_78 = 0;
            uStack_68 = 0;
            FUN_05e1d31c(&local_310,&DAT_0a3d9ce1,&local_e0);
            if (cStack_399 < '\0') {
              __ZdlPvm(local_3b0[0],CONCAT17(cStack_399,local_3a0) & 0x7fffffffffffffff);
            }
            thunk_FUN_05e1d0bc(&local_310);
            if (cStack_381 < '\0') {
              uVar10 = CONCAT17(cStack_381,local_388);
              ppppppplVar14 = local_398[0];
              goto LAB_030fa22c;
            }
          }
        }
        else {
          iVar8 = thunk_FUN_05e1d97c(4);
          if (iVar8 != 0) {
            FUN_0488143c(&local_1d0);
            ppppppplVar14 = local_1d0;
            if (-1 < cStack_1b9) {
              ppppppplVar14 = (long *******)&local_1d0;
            }
            if ((DAT_0a3d9c2e & 1) == 0) {
              _DAT_0a3d9c10 = CONCAT44((int)DAT_0849d6a0,(int)DAT_084aa8c0);
              uRam000000000a3d9c18 = CONCAT44((int)DAT_0848f630,(int)DAT_085095a8);
              DAT_0a3d9c20 = CONCAT44((int)DAT_08492398,(int)DAT_086d9ac8);
              DAT_0a3d9c28 = (undefined4)DAT_08596728;
              DAT_0a3d9c2c = 99;
              DAT_0a3d9c2e = 1;
            }
            if ((DAT_0a3d9ccc & 1) == 0) {
              _DAT_0a3d9cb0 = CONCAT44((int)DAT_088a7260,(int)DAT_087e2f50);
              uRam000000000a3d9cb8 = CONCAT44((int)DAT_08485e90,(int)DAT_084a8110);
              DAT_0a3d9cc0 = CONCAT44((int)DAT_0863e0f0,(int)DAT_088a7268);
              DAT_0a3d9cc8 = (undefined4)DAT_0847fdb8;
              DAT_0a3d9ccc = 1;
            }
            FUN_05e1d050(&local_310,4,ppppppplVar14,&DAT_0a3d9c10,&DAT_0a3d9cb0,0x6f,0,0);
            FUN_04cbe440(&local_220,local_280);
            local_130 = local_220;
            if (-1 < cStack_209) {
              local_130 = (long *******)&local_220;
            }
            local_128 = 0;
            iVar8 = *(int *)(lVar23 + 0x10);
            local_180 = (undefined1 *)0x0;
            if ((DAT_0a3d9e26 & 1) == 0) {
              uVar10 = 0;
              do {
                uVar9 = *(undefined4 *)((long)&DAT_088b16e6 + uVar10);
                uVar3 = CONCAT12((char)((uint)uVar9 >> 8),(short)uVar9) & 0xff00ff;
                uVar25 = *(undefined4 *)((long)&DAT_088b16d2 + uVar10 % 0x14);
                *(uint *)((long)&DAT_0a3d9dde + uVar10) =
                     CONCAT13((char)((uint)uVar9 >> 0x18) + 0x8aU ^ (byte)((uint)uVar25 >> 0x18),
                              CONCAT12((char)((uint)uVar9 >> 0x10) + 0x8aU ^
                                       (byte)((uint)uVar25 >> 0x10),
                                       CONCAT11((char)(uVar3 >> 0x10) + 0x8aU ^
                                                (byte)((uint)uVar25 >> 8),
                                                (char)uVar3 + 0x8aU ^ (byte)uVar25)));
                uVar10 = uVar10 + 4;
              } while (uVar10 != 0x48);
              DAT_0a3d9e26 = 1;
            }
            lVar23 = 8;
            iVar22 = iVar8;
            do {
              lVar6 = lVar23;
              local_178[lVar6 + -8] =
                   *(undefined1 *)((long)&DAT_0a3d9dde + (long)(iVar22 % 10 + 0x23));
              lVar23 = lVar6 + 1;
              uVar20 = iVar22 + 9;
              iVar22 = iVar22 / 10;
            } while (0x12 < uVar20);
            if (iVar8 < 0) {
              local_178[lVar6 + -7] = 0x2d;
              lVar23 = lVar6 + 2;
            }
            local_178[lVar23 + -8] = 0;
            if (9 < lVar23) {
              puVar19 = local_178;
              puVar16 = &uStack_181 + lVar23;
              do {
                puVar19 = puVar19 + 1;
                uVar2 = *puVar16;
                puVar17 = puVar16 + -1;
                *puVar16 = puVar19[-1];
                puVar19[-1] = uVar2;
                puVar16 = puVar17;
              } while (puVar19 < puVar17);
            }
            if ((DAT_0a3d9d7b & 1) == 0) {
              _DAT_0a3d9d4c = CONCAT44((int)DAT_0849d6a0,(int)DAT_084aa8c0);
              uRam000000000a3d9d54 = CONCAT44((int)DAT_0848f630,(int)DAT_088b0cf8);
              _DAT_0a3d9d5c = CONCAT44((int)DAT_08521c18,(int)DAT_08502950);
              uRam000000000a3d9d64 = CONCAT44((int)DAT_084caf60,(int)DAT_0853ae30);
              DAT_0a3d9d6c = CONCAT44((int)ram0x087922c0,(int)DAT_08503688);
              DAT_0a3d9d74 = (undefined4)DAT_08610dd0;
              DAT_0a3d9d78 = 0x5f25;
              DAT_0a3d9d7a = 0;
              DAT_0a3d9d7b = 1;
            }
            local_e0 = (long *******)&local_130;
            plStack_d8 = &local_180;
            ppppppplStack_c8 = (long *******)0x0;
            local_d0 = (undefined8 *)0x0;
            uStack_b8 = 0;
            local_c0 = (undefined8 *******)0x0;
            uStack_a8 = 0;
            local_b0 = 0;
            uStack_98 = 0;
            local_a0 = 0;
            uStack_88 = 0;
            local_90 = 0;
            uStack_78 = 0;
            local_80 = 0;
            uStack_68 = 0;
            local_70 = 0;
            local_180 = local_178;
            FUN_05e1d31c(&local_310,&DAT_0a3d9d4c,&local_e0);
            if (cStack_209 < '\0') {
              __ZdlPvm(local_220,CONCAT17(cStack_209,local_210) & 0x7fffffffffffffff);
            }
            thunk_FUN_05e1d0bc(&local_310);
            if (cStack_1b9 < '\0') {
              uVar10 = CONCAT17(cStack_1b9,local_1c0);
              ppppppplVar14 = local_1d0;
LAB_030fa22c:
              __ZdlPvm(ppppppplVar14,uVar10 & 0x7fffffffffffffff);
            }
          }
        }
      }
      *param_1 = (long)local_370;
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (param_1 + 1,(ulong)&local_370 | 8);
      if (*(int *)(local_280 + 0x118) != 2) {
        *(undefined4 *)(local_280 + 0x118) = 5;
        iVar8 = thunk_FUN_05e1d97c(4);
        if (iVar8 != 0) {
          FUN_0488143c(&local_270);
          pppppppuVar1 = local_270;
          if (-1 < cStack_259) {
            pppppppuVar1 = &local_270;
          }
          if ((DAT_0a3d9c2e & 1) == 0) {
            _DAT_0a3d9c10 = CONCAT44((int)DAT_0849d6a0,(int)DAT_084aa8c0);
            uRam000000000a3d9c18 = CONCAT44((int)DAT_0848f630,(int)DAT_085095a8);
            DAT_0a3d9c20 = CONCAT44((int)DAT_08492398,(int)DAT_086d9ac8);
            DAT_0a3d9c28 = (undefined4)DAT_08596728;
            DAT_0a3d9c2c = 99;
            DAT_0a3d9c2e = 1;
          }
          if ((DAT_0a3d9ccc & 1) == 0) {
            _DAT_0a3d9cb0 = CONCAT44((int)DAT_088a7260,(int)DAT_087e2f50);
            uRam000000000a3d9cb8 = CONCAT44((int)DAT_08485e90,(int)DAT_084a8110);
            DAT_0a3d9cc0 = CONCAT44((int)DAT_0863e0f0,(int)DAT_088a7268);
            DAT_0a3d9cc8 = (undefined4)DAT_0847fdb8;
            DAT_0a3d9ccc = 1;
          }
          FUN_05e1d050(&local_310,4,pppppppuVar1,&DAT_0a3d9c10,&DAT_0a3d9cb0,0x7a,0,0);
          FUN_04cbe440(local_398,local_280);
          local_130 = local_398[0];
          if (-1 < cStack_381) {
            local_130 = (long *******)local_398;
          }
          local_128 = 0;
          local_180 = (undefined1 *)0x0;
          if ((DAT_0a3d9e26 & 1) == 0) {
            uVar10 = 0;
            do {
              uVar9 = *(undefined4 *)((long)&DAT_088b16e6 + uVar10);
              uVar3 = CONCAT12((char)((uint)uVar9 >> 8),(short)uVar9) & 0xff00ff;
              uVar25 = *(undefined4 *)((long)&DAT_088b16d2 + uVar10 % 0x14);
              *(uint *)((long)&DAT_0a3d9dde + uVar10) =
                   CONCAT13((char)((uint)uVar9 >> 0x18) + 0x8aU ^ (byte)((uint)uVar25 >> 0x18),
                            CONCAT12((char)((uint)uVar9 >> 0x10) + 0x8aU ^
                                     (byte)((uint)uVar25 >> 0x10),
                                     CONCAT11((char)(uVar3 >> 0x10) + 0x8aU ^
                                              (byte)((uint)uVar25 >> 8),
                                              (char)uVar3 + 0x8aU ^ (byte)uVar25)));
              uVar10 = uVar10 + 4;
            } while (uVar10 != 0x48);
            DAT_0a3d9e26 = 1;
          }
          lVar23 = 8;
          iVar8 = (int)local_370;
          do {
            lVar6 = lVar23;
            local_178[lVar6 + -8] = *(undefined1 *)((long)&DAT_0a3d9dde + (long)(iVar8 % 10 + 0x23))
            ;
            lVar23 = lVar6 + 1;
            uVar20 = iVar8 + 9;
            iVar8 = iVar8 / 10;
          } while (0x12 < uVar20);
          if ((int)local_370 < 0) {
            local_178[lVar6 + -7] = 0x2d;
            lVar23 = lVar6 + 2;
          }
          local_178[lVar23 + -8] = 0;
          if (9 < lVar23) {
            puVar19 = local_178;
            puVar16 = &uStack_181 + lVar23;
            do {
              puVar19 = puVar19 + 1;
              uVar2 = *puVar16;
              puVar17 = puVar16 + -1;
              *puVar16 = puVar19[-1];
              puVar19[-1] = uVar2;
              puVar16 = puVar17;
            } while (puVar19 < puVar17);
          }
          local_180 = local_178;
          local_1d0 = (long *******)0x0;
          lVar23 = 8;
          iVar8 = local_370._4_4_;
          do {
            lVar6 = lVar23;
            *(undefined1 *)((long)&local_1d0 + lVar6) =
                 *(undefined1 *)((long)&DAT_0a3d9dde + (long)(iVar8 % 10 + 0x23));
            lVar23 = lVar6 + 1;
            uVar20 = iVar8 + 9;
            iVar8 = iVar8 / 10;
          } while (0x12 < uVar20);
          if ((long)local_370 < 0) {
            *(undefined1 *)((long)&local_1d0 + lVar6 + 1) = 0x2d;
            lVar23 = lVar6 + 2;
          }
          *(undefined1 *)((long)&local_1d0 + lVar23) = 0;
          if (9 < lVar23) {
            puVar19 = &uStack_1d1 + lVar23;
            puVar16 = (undefined1 *)((long)&local_1c8 + 1);
            do {
              uVar2 = *puVar19;
              *puVar19 = puVar16[-1];
              puVar16[-1] = uVar2;
              bVar5 = puVar16 < puVar19 + -1;
              puVar19 = puVar19 + -1;
              puVar16 = puVar16 + 1;
            } while (bVar5);
          }
          local_1d0 = (long *******)&local_1c8;
          local_220 = (long *******)0x0;
          local_220 = (long *******)&local_218;
          lVar23 = 0;
          uVar10 = (ulong)*(uint *)(local_350 + 0x28);
          do {
            lVar6 = lVar23;
            uVar20 = (uint)uVar10;
            *(undefined1 *)((long)&local_218 + lVar6) =
                 *(undefined1 *)
                  ((long)&DAT_0a3d9dde + (ulong)(uVar20 + (int)(uVar10 / 10) * -10 + 0x23));
            lVar23 = lVar6 + 1;
            uVar10 = uVar10 / 10;
          } while (9 < uVar20);
          *(undefined1 *)((long)&local_218 + lVar6 + 1) = 0;
          if (8 < lVar6 + 8U) {
            puVar19 = (undefined1 *)((long)&local_218 + lVar6);
            puVar16 = (undefined1 *)((long)&local_218 + 1);
            do {
              uVar2 = *puVar19;
              *puVar19 = puVar16[-1];
              puVar16[-1] = uVar2;
              bVar5 = puVar16 < puVar19 + -1;
              puVar19 = puVar19 + -1;
              puVar16 = puVar16 + 1;
            } while (bVar5);
          }
          if ((DAT_0a3d9dcb & 1) == 0) {
            uVar10 = 0;
            do {
              uVar9 = *(undefined4 *)((long)&DAT_088b14f4 + uVar10);
              uVar3 = CONCAT12((char)((uint)uVar9 >> 8),(short)uVar9) & 0xff00ff;
              uVar25 = *(undefined4 *)((long)&DAT_088b14e0 + uVar10 % 0x14);
              *(uint *)((long)&DAT_0a3d9d7c + uVar10) =
                   CONCAT13((char)((uint)uVar9 >> 0x18) + 0x8aU ^ (byte)((uint)uVar25 >> 0x18),
                            CONCAT12((char)((uint)uVar9 >> 0x10) + 0x8aU ^
                                     (byte)((uint)uVar25 >> 0x10),
                                     CONCAT11((char)(uVar3 >> 0x10) + 0x8aU ^
                                              (byte)((uint)uVar25 >> 8),
                                              (char)uVar3 + 0x8aU ^ (byte)uVar25)));
              uVar10 = uVar10 + 4;
            } while (uVar10 != 0x4c);
            DAT_0a3d9dc8 = 0x5f25;
            DAT_0a3d9dca = 0;
            DAT_0a3d9dcb = 1;
          }
          local_e0 = (long *******)&local_130;
          plStack_d8 = &local_180;
          local_d0 = &local_1d0;
          ppppppplStack_c8 = (long *******)&local_220;
          uStack_b8 = 0;
          local_c0 = (undefined8 *******)0x0;
          uStack_a8 = 0;
          local_b0 = 0;
          uStack_98 = 0;
          local_a0 = 0;
          uStack_88 = 0;
          local_90 = 0;
          uStack_78 = 0;
          local_80 = 0;
          uStack_68 = 0;
          local_70 = 0;
          FUN_05e1d31c(&local_310,&DAT_0a3d9d7c,&local_e0);
          if (cStack_381 < '\0') {
            __ZdlPvm(local_398[0],CONCAT17(cStack_381,local_388) & 0x7fffffffffffffff);
          }
          thunk_FUN_05e1d0bc(&local_310);
          if (cStack_259 < '\0') {
            __ZdlPvm(local_270,CONCAT17(cStack_259,local_260) & 0x7fffffffffffffff);
          }
        }
        FUN_030f6650(&local_310,1,2,(int)*param_1,*(undefined4 *)((long)param_1 + 4));
        *param_1 = (long)local_310;
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (param_1 + 1,&local_308);
        if (local_2e8 != (long *)0x0) {
          local_2e8[1] = local_2e8[1] + 1;
        }
        plVar12 = (long *)param_1[5];
        param_1[4] = CONCAT44(uStack_2ec,local_2f0);
        param_1[5] = (long)local_2e8;
        if (plVar12 != (long *)0x0) {
          LOAcquire();
          lVar23 = plVar12[1];
          plVar12[1] = lVar23 + -1;
          LORelease();
          if (lVar23 == 0) {
            (**(code **)(*plVar12 + 0x10))(plVar12);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar12);
          }
        }
        if (local_2e8 != (long *)0x0) {
          LOAcquire();
          lVar23 = local_2e8[1];
          local_2e8[1] = lVar23 + -1;
          LORelease();
          if (lVar23 == 0) {
            (**(code **)(*local_2e8 + 0x10))(local_2e8);
            __ZNSt3__119__shared_weak_count14__release_weakEv(local_2e8);
          }
        }
        if ((long)local_2f8 < 0) {
          __ZdlPvm(local_308,local_2f8 & 0x7fffffffffffffff);
        }
      }
      local_3c0 = local_280;
      local_3b8 = local_278;
      lVar23 = local_280;
      if (local_278 != (long *)0x0) {
        lVar23 = local_278[1];
        local_278[1] = lVar23 + 1;
      }
      FUN_030daf78(lVar23,param_2,&local_3c0,1,1);
      plVar4 = local_3b8;
      plVar12 = local_348;
      if (local_3b8 != (long *)0x0) {
        LOAcquire();
        lVar23 = local_3b8[1];
        local_3b8[1] = lVar23 + -1;
        LORelease();
        if (lVar23 == 0) {
          (**(code **)(*local_3b8 + 0x10))(local_3b8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
          plVar12 = local_348;
        }
      }
      local_348 = plVar12;
      if (plVar12 != (long *)0x0) {
        LOAcquire();
        lVar23 = *(long *)((long)plVar12 + 8U);
        *(long *)((long)plVar12 + 8U) = lVar23 + -1;
        LORelease();
        if (lVar23 == 0) {
          (**(code **)(*plVar12 + 0x10))(plVar12);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar12);
        }
      }
      if ((long)puStack_358 < 0) {
        __ZdlPvm(puStack_368,(ulong)puStack_358 & 0x7fffffffffffffff);
      }
      FUN_0465d634(&local_340);
      goto LAB_030fa858;
    }
    iVar8 = thunk_FUN_05e1d97c(4);
    if (iVar8 == 0) goto LAB_030fa858;
    FUN_0488143c(&local_130);
    ppppppplVar14 = local_130;
    if (-1 < cStack_119) {
      ppppppplVar14 = (long *******)&local_130;
    }
    if ((DAT_0a3d9c2e & 1) == 0) {
      _DAT_0a3d9c10 = CONCAT44((int)DAT_0849d6a0,(int)DAT_084aa8c0);
      uRam000000000a3d9c18 = CONCAT44((int)DAT_0848f630,(int)DAT_085095a8);
      DAT_0a3d9c20 = CONCAT44((int)DAT_08492398,(int)DAT_086d9ac8);
      DAT_0a3d9c28 = (undefined4)DAT_08596728;
      DAT_0a3d9c2c = 99;
      DAT_0a3d9c2e = 1;
    }
    if ((DAT_0a3d9ccc & 1) == 0) {
      _DAT_0a3d9cb0 = CONCAT44((int)DAT_088a7260,(int)DAT_087e2f50);
      uRam000000000a3d9cb8 = CONCAT44((int)DAT_08485e90,(int)DAT_084a8110);
      DAT_0a3d9cc0 = CONCAT44((int)DAT_0863e0f0,(int)DAT_088a7268);
      DAT_0a3d9cc8 = (undefined4)DAT_0847fdb8;
      DAT_0a3d9ccc = 1;
    }
    FUN_05e1d050(&local_310,4,ppppppplVar14,&DAT_0a3d9c10,&DAT_0a3d9cb0,0x4b,0,0);
    if ((DAT_0a3d9ce0 & 1) == 0) {
      uRam000000000a3d9cd8._0_1_ = s_message_is_null_088b0d00[8];
      uRam000000000a3d9cd8._1_1_ = s_message_is_null_088b0d00[9];
      uRam000000000a3d9cd8._2_1_ = s_message_is_null_088b0d00[10];
      uRam000000000a3d9cd8._3_1_ = s_message_is_null_088b0d00[0xb];
      uRam000000000a3d9cd8._4_1_ = s_message_is_null_088b0d00[0xc];
      uRam000000000a3d9cd8._5_1_ = s_message_is_null_088b0d00[0xd];
      uRam000000000a3d9cd8._6_1_ = s_message_is_null_088b0d00[0xe];
      uRam000000000a3d9cd8._7_1_ = s_message_is_null_088b0d00[0xf];
      DAT_0a3d9cd0 = s_message_is_null_088b0d00[0];
      DAT_0a3d9cd0_1._0_1_ = s_message_is_null_088b0d00[1];
      DAT_0a3d9cd0_1._1_1_ = s_message_is_null_088b0d00[2];
      DAT_0a3d9cd0_1._2_1_ = s_message_is_null_088b0d00[3];
      DAT_0a3d9cd0_1._3_1_ = s_message_is_null_088b0d00[4];
      DAT_0a3d9cd0_1._4_1_ = s_message_is_null_088b0d00[5];
      DAT_0a3d9cd0_1._5_1_ = s_message_is_null_088b0d00[6];
      DAT_0a3d9cd0_1._6_1_ = s_message_is_null_088b0d00[7];
      DAT_0a3d9ce0 = 1;
    }
    uStack_78 = 0;
    local_80 = 0;
    uStack_68 = 0;
    local_70 = 0;
    uStack_98 = 0;
    local_a0 = 0;
    uStack_88 = 0;
    local_90 = 0;
    uStack_b8 = 0;
    local_c0 = (undefined8 *******)0x0;
    uStack_a8 = 0;
    local_b0 = 0;
    plStack_d8 = (long *)0x0;
    local_e0 = (long *******)0x0;
    ppppppplStack_c8 = (long *******)0x0;
    local_d0 = (undefined8 *)0x0;
    FUN_05e1d31c(&local_310,&DAT_0a3d9cd0,&local_e0);
    thunk_FUN_05e1d0bc(&local_310);
    if (-1 < cStack_119) goto LAB_030fa858;
    ppppppplVar14 = local_130;
    uVar10 = CONCAT17(cStack_119,local_120);
  }
  else {
    *(undefined4 *)(lVar23 + 0x118) = 5;
    FUN_030f6650(&local_310,1,1,(int)*param_1,*(undefined4 *)((long)param_1 + 4));
    *param_1 = (long)local_310;
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_1 + 1,&local_308)
    ;
    if (local_2e8 != (long *)0x0) {
      local_2e8[1] = local_2e8[1] + 1;
    }
    plVar12 = (long *)param_1[5];
    param_1[4] = CONCAT44(uStack_2ec,local_2f0);
    param_1[5] = (long)local_2e8;
    if (plVar12 != (long *)0x0) {
      LOAcquire();
      lVar23 = plVar12[1];
      plVar12[1] = lVar23 + -1;
      LORelease();
      if (lVar23 == 0) {
        (**(code **)(*plVar12 + 0x10))(plVar12);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar12);
      }
    }
    if (local_2e8 != (long *)0x0) {
      LOAcquire();
      lVar23 = local_2e8[1];
      local_2e8[1] = lVar23 + -1;
      LORelease();
      if (lVar23 == 0) {
        (**(code **)(*local_2e8 + 0x10))(local_2e8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(local_2e8);
      }
    }
    ppppppplVar14 = local_308;
    uVar10 = local_2f8;
    if (-1 < (long)local_2f8) goto LAB_030fa858;
  }
  __ZdlPvm(ppppppplVar14,uVar10 & 0x7fffffffffffffff);
LAB_030fa858:
  plVar12 = local_278;
  if (local_278 != (long *)0x0) {
    LOAcquire();
    lVar23 = local_278[1];
    local_278[1] = lVar23 + -1;
    LORelease();
    if (lVar23 == 0) {
      (**(code **)(*local_278 + 0x10))(local_278);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar12);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_58) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


