// Ghidra inferred pseudocode; requested=0x317e410
// entry=0317e410 end=0317ef23

/* WARNING: Removing unreachable block (ram,0x0317ecd4) */
/* WARNING: Removing unreachable block (ram,0x0317ed08) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN_0317e410(undefined8 param_1,long *param_2)

{
  long *******ppppppplVar1;
  undefined8 *******pppppppuVar2;
  long *plVar3;
  undefined1 uVar4;
  undefined4 uVar5;
  uint3 uVar6;
  undefined8 uVar7;
  undefined8 *puVar8;
  undefined1 **ppuVar9;
  undefined1 *puVar10;
  int iVar11;
  uint uVar12;
  long lVar13;
  ulong uVar14;
  ulong uVar15;
  undefined1 *puVar16;
  long lVar17;
  undefined1 *puVar18;
  long *plVar19;
  long *plVar20;
  undefined4 uVar21;
  undefined4 uVar22;
  undefined4 uVar23;
  undefined4 uVar24;
  undefined4 uVar25;
  undefined4 local_354;
  undefined8 *******local_348 [2];
  undefined7 local_338;
  char cStack_331;
  undefined1 *local_330;
  undefined1 *puStack_328;
  undefined1 *local_320;
  undefined1 *puStack_318;
  undefined1 *local_310;
  undefined1 *puStack_308;
  undefined1 *puStack_300;
  undefined1 *local_2f8;
  undefined1 *local_2f0;
  long local_2e0;
  long *plStack_2d8;
  undefined8 local_2d0;
  undefined1 *puStack_2c8;
  undefined1 *local_2c0;
  undefined1 *puStack_2b8;
  undefined1 *local_2b0;
  long *local_2a8;
  undefined8 *local_298;
  undefined8 *local_290;
  undefined8 *local_288;
  undefined8 local_280;
  long *local_278;
  undefined1 *local_1f0;
  undefined1 local_1e8 [72];
  undefined1 *local_1a0;
  undefined1 local_198 [72];
  long *******local_150;
  undefined1 local_148;
  undefined7 uStack_147;
  undefined7 local_140;
  char cStack_139;
  long *******local_100;
  undefined1 **ppuStack_f8;
  undefined1 **local_f0;
  undefined8 local_e8;
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
  
  uVar7 = DAT_088ba9b0;
  local_78 = *(long *)PTR____stack_chk_guard_09b36c98;
  plVar20 = (long *)*param_2;
  plVar3 = (long *)param_2[1];
  if (plVar20 == plVar3) {
    iVar11 = thunk_FUN_05e1d97c(4);
    if (iVar11 != 0) {
      FUN_0488143c(&local_150);
      ppppppplVar1 = local_150;
      if (-1 < cStack_139) {
        ppppppplVar1 = (long *******)&local_150;
      }
      if ((DAT_0a3dd363 & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3dd350)[uVar14] = (&DAT_088bce97)[uVar14] + 0x8a ^ (&DAT_088bce87)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x13);
        DAT_0a3dd363 = 1;
      }
      if ((DAT_0a3dd48f & 1) == 0) {
        _DAT_0a3dd478 = CONCAT44((int)DAT_088a71e8,(int)DAT_08503670);
        uRam000000000a3dd480 = CONCAT44((int)ram0x088ba9a8,(int)DAT_0848f630);
        DAT_0a3dd488 = (undefined4)DAT_088ba9b0;
        DAT_0a3dd48c = 0x656e;
        DAT_0a3dd48e = 0;
        DAT_0a3dd48f = 1;
      }
      FUN_05e1d050(&local_280,4,ppppppplVar1,&DAT_0a3dd350,&DAT_0a3dd478,0x18c,0,0);
      if ((DAT_0a3dd4ae & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3dd490)[uVar14] = (&DAT_088bd052)[uVar14] + 0x8a ^ (&DAT_088bd042)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x1e);
        DAT_0a3dd4ae = 1;
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
      ppuStack_f8 = (undefined1 **)0x0;
      local_100 = (long *******)0x0;
      local_e8 = 0;
      local_f0 = (undefined1 **)0x0;
      FUN_05e1d31c(&local_280,&DAT_0a3dd490,&local_100);
      thunk_FUN_05e1d0bc(&local_280);
      if (cStack_139 < '\0') {
        __ZdlPvm(local_150,CONCAT17(cStack_139,local_140) & 0x7fffffffffffffff);
      }
    }
    local_354 = 0;
  }
  else {
    local_298 = (undefined8 *)0x0;
    local_290 = (undefined8 *)0x0;
    local_288 = (undefined8 *)0x0;
    uVar21 = (undefined4)DAT_088a71e8;
    uVar25 = (undefined4)DAT_08503670;
    uVar5 = (undefined4)DAT_0848f630;
    uVar24 = (undefined4)ram0x088ba9a8;
    local_354 = 1;
    do {
      lVar13 = *plVar20;
      if (lVar13 == 0) {
        iVar11 = thunk_FUN_05e1d97c(4);
        if (iVar11 != 0) {
          FUN_0488143c(&local_150);
          ppppppplVar1 = local_150;
          if (-1 < cStack_139) {
            ppppppplVar1 = (long *******)&local_150;
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
          if ((DAT_0a3dd48f & 1) == 0) {
            DAT_0a3dd48c = 0x656e;
            DAT_0a3dd48e = 0;
            DAT_0a3dd48f = 1;
            _DAT_0a3dd478 = CONCAT44(uVar21,uVar25);
            uRam000000000a3dd480 = CONCAT44(uVar24,uVar5);
            DAT_0a3dd488 = (int)uVar7;
          }
          FUN_05e1d050(&local_280,4,ppppppplVar1,&DAT_0a3dd350,&DAT_0a3dd478,0x195,0,0);
          if ((DAT_0a3dd4c9 & 1) == 0) {
            uVar14 = 0;
            do {
              (&DAT_0a3dd4af)[uVar14] =
                   (&DAT_088bd080)[uVar14] + 0x8a ^ (&DAT_088bd070)[uVar14 & 0xf];
              uVar14 = uVar14 + 1;
            } while (uVar14 != 0x1a);
            DAT_0a3dd4c9 = 1;
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
          ppuStack_f8 = (undefined1 **)0x0;
          local_100 = (long *******)0x0;
          local_e8 = 0;
          local_f0 = (undefined1 **)0x0;
          FUN_05e1d31c(&local_280,&DAT_0a3dd4af,&local_100);
          thunk_FUN_05e1d0bc(&local_280);
          if (cStack_139 < '\0') {
            __ZdlPvm(local_150,CONCAT17(cStack_139,local_140) & 0x7fffffffffffffff);
          }
        }
        local_354 = 0;
      }
      else {
        puStack_2b8 = &SUB_aaaaaaaaaaaaaaaa;
        local_2c0 = &SUB_aaaaaaaaaaaaaaaa;
        local_2a8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
        local_2b0 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_2c8 = &SUB_aaaaaaaaaaaaaaaa;
        local_2d0 = &SUB_aaaaaaaaaaaaaaaa;
        plVar19 = (long *)plVar20[1];
        if (plVar19 != (long *)0x0) {
          plVar19[1] = plVar19[1] + 1;
        }
        local_2e0 = lVar13;
        plStack_2d8 = plVar19;
        FUN_0317df64(&local_2d0,param_1,&local_2e0,1);
        if (plVar19 != (long *)0x0) {
          LOAcquire();
          lVar13 = plVar19[1];
          plVar19[1] = lVar13 + -1;
          LORelease();
          if (lVar13 == 0) {
            (**(code **)(*plVar19 + 0x10))(plVar19);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar19);
          }
        }
        local_2f0 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_308 = &SUB_aaaaaaaaaaaaaaaa;
        local_310 = &SUB_aaaaaaaaaaaaaaaa;
        local_2f8 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_300 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_328 = &SUB_aaaaaaaaaaaaaaaa;
        local_330 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_318 = &SUB_aaaaaaaaaaaaaaaa;
        local_320 = &SUB_aaaaaaaaaaaaaaaa;
        FUN_0086e43c(&local_330,local_2b0);
        puVar8 = local_290;
        if ((char)local_2f0 == '\x01') {
          if (local_290 < local_288) {
            if ((long)local_320 < 0) {
              FUN_00018d20(local_290,local_330,puStack_328);
            }
            else {
              local_290[2] = local_320;
              local_290[1] = puStack_328;
              *local_290 = local_330;
            }
            puVar8[4] = local_310;
            puVar8[3] = puStack_318;
            if ((long)local_2f8 < 0) {
              FUN_00018d20(puVar8 + 5,puStack_308,puStack_300);
            }
            else {
              puVar8[7] = local_2f8;
              puVar8[6] = puStack_300;
              puVar8[5] = puStack_308;
            }
            local_290 = puVar8 + 8;
          }
          else {
            local_290 = (undefined8 *)FUN_03213c1c(&local_298,&local_330);
          }
        }
        if ((int)local_2d0 != 0 || local_2d0._4_4_ != 0) {
          iVar11 = thunk_FUN_05e1d97c(4);
          if (iVar11 != 0) {
            FUN_0488143c(local_348);
            pppppppuVar2 = local_348[0];
            if (-1 < cStack_331) {
              pppppppuVar2 = local_348;
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
            if ((DAT_0a3dd48f & 1) == 0) {
              DAT_0a3dd48c = 0x656e;
              DAT_0a3dd48e = 0;
              DAT_0a3dd48f = 1;
              _DAT_0a3dd478 = CONCAT44(uVar21,uVar25);
              uRam000000000a3dd480 = CONCAT44(uVar24,uVar5);
              DAT_0a3dd488 = (int)uVar7;
            }
            FUN_05e1d050(&local_280,4,pppppppuVar2,&DAT_0a3dd350,&DAT_0a3dd478,0x1a0,0,0);
            plVar19 = (long *)*plVar20;
            local_150 = (long *******)plVar19[0x12];
            if (-1 < *(char *)((long)plVar19 + 0xa7)) {
              local_150 = (long *******)(plVar19 + 0x12);
            }
            local_148 = 0;
            uVar14 = (**(code **)(*plVar19 + 0x10))();
            local_1a0 = (undefined1 *)0x0;
            if ((DAT_0a3e2eba & 1) == 0) {
              uVar15 = 0;
              do {
                uVar22 = *(undefined4 *)((long)&DAT_088c56c9 + uVar15);
                uVar6 = CONCAT12((char)((uint)uVar22 >> 8),(short)uVar22) & 0xff00ff;
                uVar23 = *(undefined4 *)((long)&DAT_088c56b5 + uVar15 % 0x14);
                *(uint *)((long)&DAT_0a3e2e72 + uVar15) =
                     CONCAT13((char)((uint)uVar22 >> 0x18) + 0x69U ^ (byte)((uint)uVar23 >> 0x18),
                              CONCAT12((char)((uint)uVar22 >> 0x10) + 0x69U ^
                                       (byte)((uint)uVar23 >> 0x10),
                                       CONCAT11((char)(uVar6 >> 0x10) + 0x69U ^
                                                (byte)((uint)uVar23 >> 8),
                                                (char)uVar6 + 0x69U ^ (byte)uVar23)));
                uVar15 = uVar15 + 4;
              } while (uVar15 != 0x48);
              DAT_0a3e2eba = 1;
            }
            lVar13 = 0;
            do {
              lVar17 = lVar13;
              uVar12 = (uint)uVar14;
              local_198[lVar17] =
                   *(undefined1 *)
                    ((long)&DAT_0a3e2e72 +
                    (ulong)(uVar12 + (int)((uVar14 & 0xffffffff) / 10) * -10 + 0x23));
              uVar14 = (uVar14 & 0xffffffff) / 10;
              lVar13 = lVar17 + 1;
            } while (9 < uVar12);
            local_198[lVar17 + 1] = 0;
            if (8 < lVar17 + 8U) {
              puVar18 = local_198 + lVar17;
              puVar10 = local_198;
              do {
                puVar10 = puVar10 + 1;
                uVar4 = *puVar18;
                puVar16 = puVar18 + -1;
                *puVar18 = puVar10[-1];
                puVar10[-1] = uVar4;
                puVar18 = puVar16;
              } while (puVar10 < puVar16);
            }
            local_1a0 = local_198;
            uVar14 = (**(code **)(*(long *)*plVar20 + 0x18))();
            if ((DAT_0a3e2eba & 1) == 0) {
              uVar15 = 0;
              do {
                uVar22 = *(undefined4 *)((long)&DAT_088c56c9 + uVar15);
                uVar6 = CONCAT12((char)((uint)uVar22 >> 8),(short)uVar22) & 0xff00ff;
                uVar23 = *(undefined4 *)((long)&DAT_088c56b5 + uVar15 % 0x14);
                *(uint *)((long)&DAT_0a3e2e72 + uVar15) =
                     CONCAT13((char)((uint)uVar22 >> 0x18) + 0x69U ^ (byte)((uint)uVar23 >> 0x18),
                              CONCAT12((char)((uint)uVar22 >> 0x10) + 0x69U ^
                                       (byte)((uint)uVar23 >> 0x10),
                                       CONCAT11((char)(uVar6 >> 0x10) + 0x69U ^
                                                (byte)((uint)uVar23 >> 8),
                                                (char)uVar6 + 0x69U ^ (byte)uVar23)));
                uVar15 = uVar15 + 4;
              } while (uVar15 != 0x48);
              DAT_0a3e2eba = 1;
            }
            lVar13 = 0;
            do {
              lVar17 = lVar13;
              uVar12 = (uint)uVar14;
              local_1e8[lVar17] =
                   *(undefined1 *)
                    ((long)&DAT_0a3e2e72 +
                    (ulong)(uVar12 + (int)((uVar14 & 0xffffffff) / 10) * -10 + 0x23));
              uVar14 = (uVar14 & 0xffffffff) / 10;
              lVar13 = lVar17 + 1;
            } while (9 < uVar12);
            local_1e8[lVar17 + 1] = 0;
            if (8 < lVar17 + 8U) {
              puVar18 = local_1e8 + lVar17;
              puVar10 = local_1e8;
              do {
                puVar10 = puVar10 + 1;
                uVar4 = *puVar18;
                puVar16 = puVar18 + -1;
                *puVar18 = puVar10[-1];
                puVar10[-1] = uVar4;
                puVar18 = puVar16;
              } while (puVar10 < puVar16);
            }
            if ((DAT_0a3dd4e1 & 1) == 0) {
              uVar14 = 0;
              do {
                (&DAT_0a3dd4ca)[uVar14] =
                     (&DAT_088bd0aa)[uVar14] + 0x8a ^ (&DAT_088bd09a)[uVar14 & 0xf];
                uVar14 = uVar14 + 1;
              } while (uVar14 != 0x17);
              DAT_0a3dd4e1 = 1;
            }
            local_100 = (long *******)&local_150;
            uStack_e0 = 0;
            local_e8 = 0;
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
            local_1f0 = local_1e8;
            ppuStack_f8 = &local_1a0;
            local_f0 = &local_1f0;
            FUN_05e1d31c(&local_280,&DAT_0a3dd4ca,&local_100);
            thunk_FUN_05e1d0bc(&local_280);
            if (cStack_331 < '\0') {
              __ZdlPvm(local_348[0],CONCAT17(cStack_331,local_338) & 0x7fffffffffffffff);
            }
          }
          local_354 = 0;
        }
        plVar19 = local_2a8;
        if ((char)local_2f0 == '\x01') {
          if ((long)local_2f8 < 0) {
            __ZdlPvm(puStack_308,(ulong)local_2f8 & 0x7fffffffffffffff);
          }
          plVar19 = local_2a8;
          if ((long)local_320 < 0) {
            __ZdlPvm(local_330,(ulong)local_320 & 0x7fffffffffffffff);
            plVar19 = local_2a8;
          }
        }
        local_2a8 = plVar19;
        if (plVar19 != (long *)0x0) {
          LOAcquire();
          lVar13 = plVar19[1];
          plVar19[1] = lVar13 + -1;
          LORelease();
          if (lVar13 == 0) {
            (**(code **)(*plVar19 + 0x10))(plVar19);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar19);
          }
        }
        if ((long)puStack_2b8 < 0) {
          __ZdlPvm(puStack_2c8,(ulong)puStack_2b8 & 0x7fffffffffffffff);
        }
      }
      plVar20 = plVar20 + 2;
    } while (plVar20 != plVar3);
    if (0x10 < (ulong)(param_2[1] - *param_2)) {
      FUN_0466aca8(&local_150);
      FUN_01205740(&local_100,local_150);
      FUN_0317f064(&local_280,local_100);
      FUN_03525950(local_280,&local_298,1,1);
      if (local_278 != (long *)0x0) {
        LOAcquire();
        lVar13 = local_278[1];
        local_278[1] = lVar13 + -1;
        LORelease();
        if (lVar13 == 0) {
          (**(code **)(*local_278 + 0x10))(local_278);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_278);
        }
      }
      ppuVar9 = ppuStack_f8;
      if (ppuStack_f8 != (undefined1 **)0x0) {
        LOAcquire();
        puVar10 = ppuStack_f8[1];
        ppuStack_f8[1] = puVar10 + -1;
        LORelease();
        if (puVar10 == (undefined1 *)0x0) {
          (**(code **)(*ppuVar9 + 0x10))(ppuVar9);
          __ZNSt3__119__shared_weak_count14__release_weakEv(ppuVar9);
        }
      }
      plVar20 = (long *)CONCAT71(uStack_147,local_148);
      if (plVar20 != (long *)0x0) {
        LOAcquire();
        lVar13 = plVar20[1];
        plVar20[1] = lVar13 + -1;
        LORelease();
        if (lVar13 == 0) {
          (**(code **)(*plVar20 + 0x10))(plVar20);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar20);
        }
      }
    }
    if (local_298 != (undefined8 *)0x0) {
      for (; local_290 != local_298; local_290 = local_290 + -8) {
      }
      local_290 = local_298;
      __ZdlPvm(local_298,(long)local_288 - (long)local_298);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_78) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return local_354;
}


