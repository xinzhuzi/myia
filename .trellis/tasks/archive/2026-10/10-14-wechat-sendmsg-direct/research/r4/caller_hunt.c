// ===== [d0] FUN_00876de0 @ 00876de0 =====

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00876de0(long param_1,char *param_2,long *param_3,undefined8 param_4)

{
  uint uVar1;
  undefined *****pppppuVar2;
  size_t sVar3;
  size_t sVar4;
  byte bVar5;
  undefined1 uVar6;
  uint3 uVar7;
  bool bVar8;
  undefined1 *puVar9;
  uint uVar10;
  int iVar11;
  int iVar12;
  long lVar13;
  long *plVar14;
  undefined8 uVar15;
  undefined *****pppppuVar16;
  char *pcVar17;
  undefined1 *puVar18;
  undefined1 *puVar19;
  long lVar20;
  ulong uVar21;
  size_t sVar22;
  size_t sVar23;
  size_t sVar24;
  size_t sVar25;
  byte bVar26;
  undefined4 uVar27;
  undefined4 uVar28;
  undefined ****local_238 [2];
  undefined7 local_228;
  char cStack_221;
  undefined ****local_220;
  long *local_218;
  undefined1 uStack_191;
  undefined8 local_190;
  undefined8 local_188;
  undefined7 local_180;
  char cStack_179;
  undefined ****local_140;
  undefined1 local_138;
  undefined7 uStack_137;
  undefined ****local_f0;
  long *local_e8;
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
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_09b36c98;
  pppppuVar2 = (undefined *****)(param_1 + 0x208);
  bVar5 = param_2[0x17];
  sVar24 = (size_t)bVar5;
  sVar22 = *(size_t *)(param_2 + 8);
  sVar4 = sVar22;
  if (-1 < (char)bVar5) {
    sVar4 = sVar24;
  }
  bVar26 = *(byte *)(param_1 + 0x21f);
  sVar23 = (size_t)bVar26;
  sVar25 = *(size_t *)(param_1 + 0x210);
  sVar3 = sVar25;
  if (-1 < (char)bVar26) {
    sVar3 = sVar23;
  }
  if (sVar4 == sVar3) {
    pppppuVar16 = (undefined *****)*pppppuVar2;
    if (-1 < (char)bVar26) {
      pppppuVar16 = pppppuVar2;
    }
    if ((char)bVar5 < '\0') {
      iVar11 = _memcmp(*(void **)param_2,pppppuVar16,sVar22);
      if (iVar11 != 0) goto LAB_00876ea4;
    }
    else {
      pcVar17 = param_2;
      uVar21 = sVar24;
      if (bVar5 != 0) {
        do {
          if (*pcVar17 != *(char *)pppppuVar16) goto LAB_00876ea4;
          pppppuVar16 = (undefined *****)((long)pppppuVar16 + 1);
          uVar21 = uVar21 - 1;
          pcVar17 = pcVar17 + 1;
        } while (uVar21 != 0);
      }
    }
  }
  else {
LAB_00876ea4:
    if (*(long *)(param_1 + 0x260) != 0) {
      FUN_008418e4();
    }
    uVar15 = __Znwm(0x48);
    FUN_008416e0(uVar15,param_1);
    lVar13 = *(long *)(param_1 + 0x260);
    *(undefined8 *)(param_1 + 0x260) = uVar15;
    if (lVar13 != 0) {
      __ZdlPvm(lVar13,0x48);
    }
    if (*(char *)(param_1 + 0x21f) < '\0') {
      if (*(long *)(param_1 + 0x210) != 0) goto LAB_00876ef0;
    }
    else if (*(char *)(param_1 + 0x21f) != '\0') {
LAB_00876ef0:
      iVar11 = thunk_FUN_05e1d97c(2);
      if (iVar11 != 0) {
        FUN_0488143c(&local_190);
        plVar14 = local_190;
        if (-1 < cStack_179) {
          plVar14 = &local_190;
        }
        if ((DAT_0a2a63b9 & 1) == 0) {
          _DAT_0a2a63a4 = 0x73656d5f74616863;
          uRam000000000a2a63ac = 0x6569765f65676173;
          DAT_0a2a63b4 = 0x63632e77;
          DAT_0a2a63b8 = 0;
          DAT_0a2a63b9 = 1;
        }
        if ((DAT_0a2a63d3 & 1) == 0) {
          uRam000000000a2a63c8 = 0x614e72657355746e;
          _DAT_0a2a63c0 = 0x6572727543746553;
          DAT_0a2a63d0 = 0x656d;
          DAT_0a2a63d2 = 0;
          DAT_0a2a63d3 = 1;
        }
        FUN_05e1d050(&local_220,2,plVar14,&DAT_0a2a63a4,&DAT_0a2a63c0,0x107,0,0);
        local_140 = (undefined ****)*(undefined ******)(param_1 + 0x208);
        if (-1 < *(char *)(param_1 + 0x21f)) {
          local_140 = (undefined ****)pppppuVar2;
        }
        local_138 = 0;
        if ((DAT_0a2a63ee & 1) == 0) {
          _DAT_0a2a63d4 = 0x7365732074697865;
          uRam000000000a2a63dc = 0x6573752c6e6f6973;
          DAT_0a2a63e4 = 0x5f2528656d616e72;
          DAT_0a2a63ec = 0x29;
          DAT_0a2a63ee = 1;
        }
        uStack_e0 = 0;
        local_e8 = (long *)0x0;
        local_f0 = (undefined ****)&local_140;
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
        FUN_05e1d31c(&local_220,&DAT_0a2a63d4,&local_f0);
        thunk_FUN_05e1d0bc(&local_220);
        if (cStack_179 < '\0') {
          __ZdlPvm(local_190,CONCAT17(cStack_179,local_180) & 0x7fffffffffffffff);
        }
      }
      uVar15 = FUN_06a7d608(*(undefined8 *)(param_1 + 0x240));
      iVar11 = FUN_06a829c4();
      iVar12 = FUN_06a82e80(uVar15);
      if (iVar11 - iVar12 < 200) {
        uVar10 = FUN_0098d5ec(*(undefined8 *)(param_1 + 0x1e8));
      }
      else {
        uVar10 = 0;
      }
      iVar11 = FUN_00077244(*(long *)(param_1 + 0x1e8) + 1000);
      iVar12 = thunk_FUN_05e1d97c(2);
      if (iVar12 == 0) {
LAB_00877448:
        if ((uVar10 & 1) != 0) goto LAB_00877734;
LAB_0087744c:
        if (*(char *)(param_1 + 0x287) < '\0') {
          if (*(long *)(param_1 + 0x278) != 0) goto LAB_0087747c;
          goto LAB_00877734;
        }
        if (*(char *)(param_1 + 0x287) == '\0') goto LAB_00877734;
LAB_0087747c:
        if (((*(int *)(param_1 + 0x288) == 0) || (iVar11 != 0)) || (*(int *)(param_1 + 0x28c) == 0))
        goto LAB_00877734;
        iVar11 = thunk_FUN_05e1d97c(2);
        if (iVar11 != 0) {
          FUN_0488143c(&local_190);
          plVar14 = local_190;
          if (-1 < cStack_179) {
            plVar14 = &local_190;
          }
          if ((DAT_0a2a63b9 & 1) == 0) {
            _DAT_0a2a63a4 = 0x73656d5f74616863;
            uRam000000000a2a63ac = 0x6569765f65676173;
            DAT_0a2a63b4 = 0x63632e77;
            DAT_0a2a63b8 = 0;
            DAT_0a2a63b9 = 1;
          }
          if ((DAT_0a2a63d3 & 1) == 0) {
            uRam000000000a2a63c8 = 0x614e72657355746e;
            _DAT_0a2a63c0 = 0x6572727543746553;
            DAT_0a2a63d0 = 0x656d;
            DAT_0a2a63d2 = 0;
            DAT_0a2a63d3 = 1;
          }
          FUN_05e1d050(&local_220,2,plVar14,&DAT_0a2a63a4,&DAT_0a2a63c0,0x110,0,0);
          FUN_00877af8(local_238,param_1 + 0x270);
          local_140 = local_238[0];
          if (-1 < cStack_221) {
            local_140 = (undefined ****)local_238;
          }
          local_138 = 0;
          if ((DAT_0a2a6466 & 1) == 0) {
            uVar21 = 0;
            do {
              uVar27 = *(undefined4 *)((long)&DAT_08548412 + uVar21);
              uVar7 = CONCAT12((char)((uint)uVar27 >> 8),(short)uVar27) & 0xff00ff;
              uVar28 = *(undefined4 *)((long)&DAT_085483fe + uVar21 % 0x14);
              *(uint *)((long)&DAT_0a2a6429 + uVar21) =
                   CONCAT13((char)((uint)uVar27 >> 0x18) + 0x8aU ^ (byte)((uint)uVar28 >> 0x18),
                            CONCAT12((char)((uint)uVar27 >> 0x10) + 0x8aU ^
                                     (byte)((uint)uVar28 >> 0x10),
                                     CONCAT11((char)(uVar7 >> 0x10) + 0x8aU ^
                                              (byte)((uint)uVar28 >> 8),
                                              (char)uVar7 + 0x8aU ^ (byte)uVar28)));
              uVar21 = uVar21 + 4;
            } while (uVar21 != 0x3c);
            DAT_0a2a6465 = 0;
            DAT_0a2a6466 = 1;
          }
          uStack_e0 = 0;
          local_e8 = (long *)0x0;
          local_f0 = (undefined ****)&local_140;
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
          FUN_05e1d31c(&local_220,&DAT_0a2a6429,&local_f0);
          if (cStack_221 < '\0') {
            __ZdlPvm(local_238[0],CONCAT17(cStack_221,local_228) & 0x7fffffffffffffff);
          }
          thunk_FUN_05e1d0bc(&local_220);
          if (cStack_179 < '\0') {
            __ZdlPvm(local_190,CONCAT17(cStack_179,local_180) & 0x7fffffffffffffff);
          }
        }
        plVar14 = (long *)FUN_04669774();
        (**(code **)(*plVar14 + 0x68))(&local_190);
        (**(code **)(*local_190 + 0x30))(&local_140);
        local_238[0] = (undefined ****)&PTR_FUN_09c53c38;
        local_220 = (undefined ****)&SUB_aaaaaaaaaaaaaaaa;
        local_218 = (long *)&SUB_aaaaaaaaaaaaaaaa;
        FUN_0456f244(&local_220,local_140,local_238);
        plVar14 = local_218;
        local_f0 = local_220;
        local_e8 = local_218;
        if ((local_218 != (long *)0x0) &&
           (local_218[1] = local_218[1] + 1, local_218 != (long *)0x0)) {
          LOAcquire();
          lVar13 = local_218[1];
          local_218[1] = lVar13 + -1;
          LORelease();
          if (lVar13 == 0) {
            (**(code **)(*local_218 + 0x10))(local_218);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar14);
          }
        }
        FUN_0412046c(local_f0,pppppuVar2,param_1 + 0x270);
      }
      else {
        FUN_0488143c(local_238);
        pppppuVar16 = (undefined *****)local_238[0];
        if (-1 < cStack_221) {
          pppppuVar16 = local_238;
        }
        if ((DAT_0a2a63b9 & 1) == 0) {
          _DAT_0a2a63a4 = 0x73656d5f74616863;
          uRam000000000a2a63ac = 0x6569765f65676173;
          DAT_0a2a63b4 = 0x63632e77;
          DAT_0a2a63b8 = 0;
          DAT_0a2a63b9 = 1;
        }
        if ((DAT_0a2a63d3 & 1) == 0) {
          uRam000000000a2a63c8 = 0x614e72657355746e;
          _DAT_0a2a63c0 = 0x6572727543746553;
          DAT_0a2a63d0 = 0x656d;
          DAT_0a2a63d2 = 0;
          DAT_0a2a63d3 = 1;
        }
        FUN_05e1d050(&local_220,2,pppppuVar16,&DAT_0a2a63a4,&DAT_0a2a63c0,0x10e,0,0);
        if (uVar10 == 0) {
          local_140 = (undefined ****)&DAT_0a2a663c;
          if ((DAT_0a2a6642 & 1) == 0) {
            DAT_0a2a663c = 0x736c6166;
            puVar9 = &DAT_0a2a6640;
            puVar18 = &DAT_0a2a6641;
            puVar19 = &DAT_0a2a6642;
            goto LAB_00877250;
          }
        }
        else {
          local_140 = (undefined ****)&DAT_0a2a6634;
          if ((DAT_0a2a6639 & 1) == 0) {
            DAT_0a2a6634._0_2_ = 0x7274;
            DAT_0a2a6634._2_1_ = 0x75;
            puVar18 = &DAT_0a2a6638;
            puVar9 = (undefined1 *)((long)&DAT_0a2a6634 + 3);
            puVar19 = &DAT_0a2a6639;
LAB_00877250:
            *puVar9 = 0x65;
            *puVar18 = 0;
            *puVar19 = 1;
          }
        }
        local_138 = 0;
        local_190 = (long *)0x0;
        if ((DAT_0a2a668b & 1) == 0) {
          uVar21 = 0;
          do {
            uVar27 = *(undefined4 *)((long)&DAT_08548772 + uVar21);
            uVar7 = CONCAT12((char)((uint)uVar27 >> 8),(short)uVar27) & 0xff00ff;
            uVar28 = *(undefined4 *)((long)&DAT_0854875e + uVar21 % 0x14);
            *(uint *)((long)&DAT_0a2a6643 + uVar21) =
                 CONCAT13((char)((uint)uVar27 >> 0x18) + 0x8aU ^ (byte)((uint)uVar28 >> 0x18),
                          CONCAT12((char)((uint)uVar27 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar28 >> 0x10),
                                   CONCAT11((char)(uVar7 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar28 >> 8),
                                            (char)uVar7 + 0x8aU ^ (byte)uVar28)));
            uVar21 = uVar21 + 4;
          } while (uVar21 != 0x48);
          DAT_0a2a668b = 1;
        }
        lVar13 = 8;
        iVar12 = iVar11;
        do {
          lVar20 = lVar13;
          *(undefined1 *)((long)&local_190 + lVar20) =
               *(undefined1 *)((long)&DAT_0a2a6643 + (long)(iVar12 % 10 + 0x23));
          lVar13 = lVar20 + 1;
          uVar1 = iVar12 + 9;
          iVar12 = iVar12 / 10;
        } while (0x12 < uVar1);
        if (iVar11 < 0) {
          *(undefined1 *)((long)&local_190 + lVar20 + 1) = 0x2d;
          lVar13 = lVar20 + 2;
        }
        *(undefined1 *)((long)&local_190 + lVar13) = 0;
        if (9 < lVar13) {
          puVar18 = &uStack_191 + lVar13;
          puVar9 = (undefined1 *)((long)&local_188 + 1);
          do {
            uVar6 = *puVar18;
            *puVar18 = puVar9[-1];
            puVar9[-1] = uVar6;
            bVar8 = puVar9 < puVar18 + -1;
            puVar18 = puVar18 + -1;
            puVar9 = puVar9 + 1;
          } while (bVar8);
        }
        if ((DAT_0a2a6428 & 1) == 0) {
          uVar21 = 0;
          do {
            uVar27 = *(undefined4 *)((long)&DAT_085483c5 + uVar21);
            uVar7 = CONCAT12((char)((uint)uVar27 >> 8),(short)uVar27) & 0xff00ff;
            uVar28 = *(undefined4 *)((long)&DAT_085483b1 + uVar21 % 0x14);
            *(uint *)((long)&DAT_0a2a63ef + uVar21) =
                 CONCAT13((char)((uint)uVar27 >> 0x18) + 0x8aU ^ (byte)((uint)uVar28 >> 0x18),
                          CONCAT12((char)((uint)uVar27 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar28 >> 0x10),
                                   CONCAT11((char)(uVar7 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar28 >> 8),
                                            (char)uVar7 + 0x8aU ^ (byte)uVar28)));
            uVar21 = uVar21 + 4;
          } while (uVar21 != 0x38);
          DAT_0a2a6427 = 0;
          DAT_0a2a6428 = 1;
        }
        local_f0 = (undefined ****)&local_140;
        local_e8 = &local_190;
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
        local_78 = 0;
        uStack_80 = 0;
        local_190 = &local_188;
        FUN_05e1d31c(&local_220,&DAT_0a2a63ef,&local_f0);
        thunk_FUN_05e1d0bc(&local_220);
        if (-1 < cStack_221) goto LAB_00877448;
        __ZdlPvm(local_238[0],CONCAT17(cStack_221,local_228) & 0x7fffffffffffffff);
        if ((uVar10 & 1) == 0) goto LAB_0087744c;
LAB_00877734:
        plVar14 = (long *)FUN_04669774();
        (**(code **)(*plVar14 + 0x68))(&local_190);
        (**(code **)(*local_190 + 0x30))(&local_140);
        local_238[0] = (undefined ****)&PTR_FUN_09c53c38;
        local_220 = (undefined ****)&SUB_aaaaaaaaaaaaaaaa;
        local_218 = (long *)&SUB_aaaaaaaaaaaaaaaa;
        FUN_0456f244(&local_220,local_140,local_238);
        plVar14 = local_218;
        local_f0 = local_220;
        local_e8 = local_218;
        if ((local_218 != (long *)0x0) &&
           (local_218[1] = local_218[1] + 1, local_218 != (long *)0x0)) {
          LOAcquire();
          lVar13 = local_218[1];
          local_218[1] = lVar13 + -1;
          LORelease();
          if (lVar13 == 0) {
            (**(code **)(*local_218 + 0x10))(local_218);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar14);
          }
        }
        FUN_04120a04(local_f0,pppppuVar2);
      }
      plVar14 = local_e8;
      if (local_e8 != (long *)0x0) {
        LOAcquire();
        lVar13 = local_e8[1];
        local_e8[1] = lVar13 + -1;
        LORelease();
        if (lVar13 == 0) {
          (**(code **)(*local_e8 + 0x10))(local_e8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar14);
        }
      }
      plVar14 = (long *)CONCAT71(uStack_137,local_138);
      if (plVar14 != (long *)0x0) {
        LOAcquire();
        lVar13 = plVar14[1];
        plVar14[1] = lVar13 + -1;
        LORelease();
        if (lVar13 == 0) {
          (**(code **)(*plVar14 + 0x10))(plVar14);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar14);
        }
      }
      if (local_188 != (long *)0x0) {
        LOAcquire();
        lVar13 = local_188[1];
        local_188[1] = lVar13 + -1;
        LORelease();
        if (lVar13 == 0) {
          (**(code **)(*local_188 + 0x10))(local_188);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_188);
        }
      }
    }
    if (*(char *)(param_1 + 0x287) < '\0') {
      __ZdlPvm(*(undefined8 *)(param_1 + 0x270),*(ulong *)(param_1 + 0x280) & 0x7fffffffffffffff);
    }
    *(undefined8 *)(param_1 + 0x290) = 0;
    *(undefined8 *)(param_1 + 0x278) = 0;
    *(undefined8 *)(param_1 + 0x270) = 0;
    *(undefined8 *)(param_1 + 0x288) = 0;
    *(undefined8 *)(param_1 + 0x280) = 0;
    if (*(char *)(param_1 + 0x2af) < '\0') {
      __ZdlPvm(*(undefined8 *)(param_1 + 0x298),*(ulong *)(param_1 + 0x2a8) & 0x7fffffffffffffff);
    }
    *(undefined8 *)(param_1 + 0x298) = 0;
    *(undefined8 *)(param_1 + 0x2a0) = 0;
    *(undefined8 *)(param_1 + 0x2a8) = 0;
    *(undefined4 *)(param_1 + 0x2d0) = 0;
    sVar24 = (size_t)(byte)param_2[0x17];
    sVar22 = *(size_t *)(param_2 + 8);
    bVar26 = *(byte *)(param_1 + 0x21f);
    sVar23 = (size_t)bVar26;
    sVar25 = *(size_t *)(param_1 + 0x210);
  }
  sVar4 = sVar22;
  if (-1 < (char)sVar24) {
    sVar4 = sVar24;
  }
  if (-1 < (char)bVar26) {
    sVar25 = sVar23;
  }
  if (sVar4 == sVar25) {
    pppppuVar16 = (undefined *****)*pppppuVar2;
    if (-1 < (char)bVar26) {
      pppppuVar16 = pppppuVar2;
    }
    if ((uint)sVar24 >> 7 == 0) {
      pcVar17 = param_2;
      if ((uint)sVar24 != 0) {
        do {
          if (*pcVar17 != *(char *)pppppuVar16) goto LAB_00877950;
          pppppuVar16 = (undefined *****)((long)pppppuVar16 + 1);
          sVar24 = sVar24 - 1;
          pcVar17 = pcVar17 + 1;
        } while (sVar24 != 0);
      }
    }
    else {
      iVar11 = _memcmp(*(void **)param_2,pppppuVar16,sVar22);
      if (iVar11 != 0) goto LAB_00877950;
    }
    if (((undefined8 *)*param_3 == (undefined8 *)0x0) ||
       (iVar11 = (*(code *)**(undefined8 **)*param_3)(), iVar11 != 0)) goto LAB_008779dc;
  }
LAB_00877950:
  FUN_01fad090(*(undefined8 *)(param_1 + 0x240));
  iVar11 = FUN_04bb368c(pppppuVar2);
  iVar12 = FUN_04bb368c(param_2);
  if (iVar11 != iVar12) {
    FUN_00940c50(*(undefined8 *)(param_1 + 0x1e8));
  }
  if (*(long *)(param_1 + 0x268) != 0) {
    FUN_06fd6414();
    *(undefined8 *)(param_1 + 0x268) = 0;
  }
  uVar15 = __Znwm(0xa8);
  thunk_FUN_01fa6ed8(uVar15,*(undefined8 *)(param_1 + 0x240),param_1 + 0x1d8);
  *(undefined8 *)(param_1 + 0x268) = uVar15;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(pppppuVar2,param_2);
  FUN_0096a74c(*(undefined8 *)(param_1 + 0x1e8),pppppuVar2,param_3,param_4,
               *(int *)(param_1 + 0x2d4) == 0);
  FUN_007d208c(*(undefined8 *)(param_1 + 0x2b0));
LAB_008779dc:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_70) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}



// ===== [d0] FUN_008dd260 @ 008dd260 =====

/* WARNING: Removing unreachable block (ram,0x008dd8a8) */
/* WARNING: Type propagation algorithm not settling */

void FUN_008dd260(long *param_1,long param_2)

{
  long *******ppppppplVar1;
  undefined ********ppppppppuVar2;
  byte bVar3;
  long lVar4;
  int iVar5;
  uint uVar6;
  undefined8 uVar7;
  long *plVar8;
  long *plVar9;
  undefined4 uVar10;
  ulong uVar11;
  undefined1 *puVar12;
  undefined1 **ppuVar13;
  undefined1 *puVar14;
  undefined1 *puVar15;
  long lVar16;
  undefined *puVar17;
  long lVar18;
  long *local_228;
  undefined **local_220;
  long *local_218;
  undefined ********local_210;
  long *local_208;
  undefined7 local_200;
  char cStack_1f9;
  long *******local_1f8;
  long *local_1f0;
  undefined1 *local_1e8;
  undefined ********local_1e0;
  long *local_1d8;
  undefined7 local_1d0;
  char cStack_1c9;
  undefined1 *local_150;
  undefined1 *puStack_148;
  undefined8 local_140;
  undefined ********local_138;
  long *local_130;
  undefined ********local_e8;
  long *local_e0;
  ulong uStack_d8;
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
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 local_70;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  FUN_00134818();
  FUN_008f4250(param_1,param_2);
  (**(code **)(*param_1 + 0x228))(param_1);
  plVar9 = param_1 + 0x37;
  puStack_148 = &SUB_aaaaaaaaaaaaaaaa;
  local_140 = &SUB_aaaaaaaaaaaaaaaa;
  local_150 = &SUB_aaaaaaaaaaaaaaaa;
  if (*(char *)((long)param_1 + 0x1cf) < '\0') {
    FUN_00018d20(&local_150,param_1[0x37],param_1[0x38]);
  }
  else {
    puStack_148 = (undefined1 *)param_1[0x38];
    local_150 = (undefined1 *)*plVar9;
    local_140 = (undefined1 *)param_1[0x39];
  }
  uVar7 = FUN_0001accc(param_2);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(plVar9,uVar7);
  (**(code **)param_1[0x42])(param_1 + 0x42);
  if (*(char *)((long)param_1 + 0x2f7) < '\0') {
    *(undefined1 *)param_1[0x5c] = 0;
    param_1[0x5d] = 0;
  }
  else {
    *(undefined1 *)(param_1 + 0x5c) = 0;
    *(undefined1 *)((long)param_1 + 0x2f7) = 0;
  }
  iVar5 = FUN_0092c86c();
  if (iVar5 != 0) {
    plVar8 = (long *)FUN_04669774();
    (**(code **)(*plVar8 + 0x68))(&local_1f8);
    (*(code *)(*local_1f8)[6])(&local_138);
    local_210 = (undefined ********)&PTR_FUN_09bf7c08;
    local_1e0 = (undefined ********)&SUB_aaaaaaaaaaaaaaaa;
    local_1d8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    FUN_0456f244(&local_1e0,local_138,&local_210);
    plVar8 = local_1d8;
    local_e8 = local_1e0;
    local_e0 = local_1d8;
    if ((local_1d8 != (long *)0x0) && (local_1d8[1] = local_1d8[1] + 1, local_1d8 != (long *)0x0)) {
      LOAcquire();
      lVar4 = local_1d8[1];
      local_1d8[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*local_1d8 + 0x10))(local_1d8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
      }
    }
    uVar6 = FUN_04276ab0(local_e8);
    plVar8 = local_e0;
    if (local_e0 != (long *)0x0) {
      LOAcquire();
      lVar4 = local_e0[1];
      local_e0[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*local_e0 + 0x10))(local_e0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
      }
    }
    plVar8 = local_130;
    if (local_130 != (long *)0x0) {
      LOAcquire();
      lVar4 = local_130[1];
      local_130[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*local_130 + 0x10))(local_130);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
      }
    }
    plVar8 = local_1f0;
    if (local_1f0 != (long *)0x0) {
      LOAcquire();
      lVar4 = local_1f0[1];
      local_1f0[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*local_1f0 + 0x10))(local_1f0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
      }
    }
    *(uint *)((long)param_1 + 0x1d4) = uVar6 & ((int)uVar6 >> 0x1f ^ 0xffffffffU);
  }
  iVar5 = thunk_FUN_05e1d97c(2);
  if (iVar5 != 0) {
    FUN_0488143c(&local_1f8);
    ppppppplVar1 = local_1f8;
    if (-1 < (long)local_1e8) {
      ppppppplVar1 = (long *******)&local_1f8;
    }
    if ((DAT_0a2a9fd7 & 1) == 0) {
      uVar11 = 0;
      do {
        (&DAT_0a2a9fc2)[uVar11] = (&DAT_0855166a)[uVar11] + 0x8a ^ (&DAT_0855165a)[uVar11 & 0xf];
        uVar11 = uVar11 + 1;
      } while (uVar11 != 0x15);
      DAT_0a2a9fd7 = 1;
    }
    if ((DAT_0a2aa013 & 1) == 0) {
      DAT_0a2aa008._0_1_ = 'R';
      DAT_0a2aa008._1_1_ = 'e';
      DAT_0a2aa008._2_1_ = 'l';
      DAT_0a2aa008._3_1_ = 'o';
      DAT_0a2aa008._4_1_ = 'a';
      DAT_0a2aa008._5_1_ = 'd';
      DAT_0a2aa008._6_1_ = 'D';
      DAT_0a2aa008._7_1_ = 'a';
      DAT_0a2aa010 = 0x6174;
      DAT_0a2aa012 = 0;
      DAT_0a2aa013 = 1;
    }
    FUN_05e1d050(&local_1e0,2,ppppppplVar1,&DAT_0a2a9fc2,&DAT_0a2aa008,0x104,0,0);
    FUN_04980e70(&local_210,plVar9);
    local_138 = local_210;
    if (-1 < cStack_1f9) {
      local_138 = (undefined ********)&local_210;
    }
    local_130 = (long *)((ulong)local_130 & 0xffffffffffffff00);
    if ((DAT_0a2aa027 & 1) == 0) {
      DAT_0a2aa018._0_1_ = 'r';
      DAT_0a2aa018._1_1_ = 'e';
      DAT_0a2aa018._2_1_ = 'l';
      DAT_0a2aa018._3_1_ = 'o';
      DAT_0a2aa018._4_1_ = 'a';
      DAT_0a2aa018._5_1_ = 'd';
      DAT_0a2aa018._6_1_ = ' ';
      DAT_0a2aa018._7_1_ = 'd';
      DAT_0a2aa020 = 0x3a617461;
      DAT_0a2aa024 = 0x5f25;
      DAT_0a2aa026 = 0;
      DAT_0a2aa027 = 1;
    }
    uStack_d8 = 0;
    local_e0 = (long *)0x0;
    local_e8 = (undefined ********)&local_138;
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
    uStack_78 = 0;
    local_80 = 0;
    local_70 = 0;
    FUN_05e1d31c(&local_1e0,&DAT_0a2aa018,&local_e8);
    if (cStack_1f9 < '\0') {
      __ZdlPvm(local_210,CONCAT17(cStack_1f9,local_200) & 0x7fffffffffffffff);
    }
    thunk_FUN_05e1d0bc(&local_1e0);
    if ((long)local_1e8 < 0) {
      __ZdlPvm(local_1f8,(ulong)local_1e8 & 0x7fffffffffffffff);
    }
  }
  iVar5 = FUN_04bb3558(plVar9);
  if (iVar5 == 0) {
    if (*(char *)((long)param_1 + 0x1f7) < '\0') {
      *(undefined1 *)param_1[0x3c] = 0;
      param_1[0x3d] = 0;
    }
    else {
      *(undefined1 *)(param_1 + 0x3c) = 0;
      *(undefined1 *)((long)param_1 + 0x1f7) = 0;
    }
  }
  else {
    puVar12 = (undefined1 *)(ulong)local_140._7_1_;
    puVar14 = puStack_148;
    if (-1 < (long)local_140) {
      puVar14 = puVar12;
    }
    bVar3 = *(byte *)((long)param_1 + 0x1cf);
    puVar15 = (undefined1 *)param_1[0x38];
    if (-1 < (char)bVar3) {
      puVar15 = (undefined1 *)(ulong)bVar3;
    }
    if (puVar14 == puVar15) {
      plVar8 = (long *)*plVar9;
      if (-1 < (char)bVar3) {
        plVar8 = plVar9;
      }
      if ((long)local_140 < 0) {
        iVar5 = _memcmp(local_150,plVar8,(size_t)puStack_148);
        if (iVar5 != 0) goto LAB_008dd6d8;
      }
      else if (local_140._7_1_ != 0) {
        ppuVar13 = &local_150;
        do {
          if (*(char *)ppuVar13 != (char)*plVar8) goto LAB_008dd6d8;
          ppuVar13 = (undefined1 **)((long)ppuVar13 + 1);
          plVar8 = (long *)((long)plVar8 + 1);
          puVar12 = puVar12 + -1;
        } while (puVar12 != (undefined1 *)0x0);
      }
    }
    else {
LAB_008dd6d8:
      FUN_0474715c();
      __ZNSt3__19to_stringEy(&local_1e0);
      plVar8 = (long *)FUN_04669774();
      (**(code **)(*plVar8 + 0x20))();
      __ZNSt3__19to_stringEy(&local_e8);
      plVar8 = local_e0;
      ppppppppuVar2 = local_e8;
      if (-1 < (long)uStack_d8) {
        plVar8 = (long *)(uStack_d8 >> 0x38);
        ppppppppuVar2 = (undefined ********)&local_e8;
      }
      plVar8 = (long *)__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
                                 (&local_1e0,ppppppppuVar2,plVar8);
      lVar4 = *plVar8;
      lVar18 = plVar8[2];
      lVar16 = plVar8[1];
      plVar8[1] = 0;
      plVar8[2] = 0;
      *plVar8 = 0;
      if (*(char *)((long)param_1 + 0x1f7) < '\0') {
        __ZdlPvm(param_1[0x3c],param_1[0x3e] & 0x7fffffffffffffff);
      }
      param_1[0x3c] = lVar4;
      param_1[0x3e] = lVar18;
      param_1[0x3d] = lVar16;
      if (cStack_1c9 < '\0') {
        __ZdlPvm(local_1e0,CONCAT17(cStack_1c9,local_1d0) & 0x7fffffffffffffff);
      }
      local_e8 = (undefined ********)&SUB_aaaaaaaaaaaaaaaa;
      local_e0 = (long *)&SUB_aaaaaaaaaaaaaaaa;
      plVar8 = (long *)FUN_04669774();
      (**(code **)(*plVar8 + 0x68))(&local_210);
      (*(code *)(*local_210)[7])(&local_1f8);
      local_220 = &PTR_FUN_09c567e0;
      local_1e0 = (undefined ********)&SUB_aaaaaaaaaaaaaaaa;
      local_1d8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
      FUN_044e6b1c(&local_1e0,local_1f8,&local_220);
      plVar8 = local_1d8;
      local_138 = local_1e0;
      local_130 = local_1d8;
      if ((local_1d8 != (long *)0x0) && (local_1d8[1] = local_1d8[1] + 1, local_1d8 != (long *)0x0))
      {
        LOAcquire();
        lVar4 = local_1d8[1];
        local_1d8[1] = lVar4 + -1;
        LORelease();
        if (lVar4 == 0) {
          (**(code **)(*local_1d8 + 0x10))(local_1d8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
        }
      }
      FUN_044fb300(&local_e8,local_138,plVar9);
      plVar8 = local_130;
      if (local_130 != (long *)0x0) {
        LOAcquire();
        lVar4 = local_130[1];
        local_130[1] = lVar4 + -1;
        LORelease();
        if (lVar4 == 0) {
          (**(code **)(*local_130 + 0x10))(local_130);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
        }
      }
      if (local_1f0 != (long *)0x0) {
        LOAcquire();
        lVar4 = local_1f0[1];
        local_1f0[1] = lVar4 + -1;
        LORelease();
        if (lVar4 == 0) {
          (**(code **)(*local_1f0 + 0x10))(local_1f0);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_1f0);
        }
      }
      if (local_208 == (long *)0x0) {
LAB_008dd890:
        if (local_e8 != (undefined ********)0x0) goto LAB_008dd898;
LAB_008dd8f4:
        uVar10 = 0;
        plVar8 = local_e0;
      }
      else {
        LOAcquire();
        lVar4 = local_208[1];
        local_208[1] = lVar4 + -1;
        LORelease();
        if (lVar4 != 0) goto LAB_008dd890;
        (**(code **)(*local_208 + 0x10))(local_208);
        __ZNSt3__119__shared_weak_count14__release_weakEv(local_208);
        if (local_e8 == (undefined ********)0x0) goto LAB_008dd8f4;
LAB_008dd898:
        uVar10 = *(undefined4 *)(local_e8 + 0x66);
        plVar8 = local_e0;
      }
      local_e0 = plVar8;
      if (plVar8 != (long *)0x0) {
        LOAcquire();
        lVar4 = plVar8[1];
        plVar8[1] = lVar4 + -1;
        LORelease();
        if (lVar4 == 0) {
          (**(code **)(*plVar8 + 0x10))(plVar8,uVar10);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
        }
      }
      FUN_04aa5b20(plVar9,uVar10,param_1 + 0x3c,0x1b);
    }
  }
  lVar4 = FUN_009abfd4(param_1[0x46] + 0x170);
  if (lVar4 != 0) {
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (lVar4 + 0x58,param_1 + 0x3c);
  }
  FUN_008de03c(param_1,param_2);
  local_218 = (long *)__Znwm(0x58);
  local_218[1] = 0;
  local_218[2] = 0;
  *local_218 = (long)&PTR_FUN_09c56890;
  puVar17 = *(undefined **)(param_2 + 0x20);
  local_220 = (undefined **)(local_218 + 3);
  local_218[4] = *(long *)(param_2 + 0x28);
  *local_220 = puVar17;
  local_218[9] = 0;
  local_218[8] = 0;
  local_218[10] = 0;
  plVar8 = local_218 + 6;
  local_218[7] = 0;
  *plVar8 = 0;
  uVar6 = *(uint *)(param_2 + 0x1c);
  local_218[5] = *(long *)(param_2 + 0x30);
  *(uint *)((long)local_218 + 0x4c) = uVar6;
  if (plVar8 != (long *)(param_2 + 400)) {
    FUN_003ef6d8(plVar8,*(long *)(param_2 + 400),*(long *)(param_2 + 0x198),
                 *(long *)(param_2 + 0x198) - *(long *)(param_2 + 400) >> 5);
    uVar6 = *(uint *)(param_2 + 0x1c);
  }
  iVar5 = 0;
  if (*(uint *)(param_2 + 0x188) <= uVar6) {
    iVar5 = uVar6 - *(uint *)(param_2 + 0x188);
  }
  *(int *)(local_220 + 7) = iVar5;
  FUN_00876de0(param_1[0x46],plVar9,(long *)(param_2 + 0x218),&local_220);
  local_1f0 = (long *)0x0;
  local_1e8 = &DAT_aaaaaaaaaaaaaa00;
  local_1f8 = (long *******)&DAT_aaaaaaaaaaaaaa01;
  lVar4 = *(long *)(param_2 + 0x218);
  if ((lVar4 == 0) ||
     (lVar4 = ___dynamic_cast(lVar4,&PTR_DAT_09c60390,&PTR_DAT_09c603b8,0), lVar4 == 0)) {
    local_228 = (long *)0x0;
  }
  else {
    local_228 = *(long **)(param_2 + 0x220);
    lVar4 = 0;
    if (local_228 != (long *)0x0) {
      lVar4 = local_228[1];
      local_228[1] = lVar4 + 1;
    }
    local_1f0 = (long *)FUN_009ce4a8(lVar4);
  }
  FUN_0085b29c(param_1[0x4c],plVar9,&local_1f8);
  puVar12 = (undefined1 *)(ulong)local_140._7_1_;
  puVar14 = puStack_148;
  if (-1 < (long)local_140) {
    puVar14 = puVar12;
  }
  bVar3 = *(byte *)((long)param_1 + 0x1cf);
  puVar15 = (undefined1 *)param_1[0x38];
  if (-1 < (char)bVar3) {
    puVar15 = (undefined1 *)(ulong)bVar3;
  }
  if (puVar14 == puVar15) {
    plVar8 = (long *)*plVar9;
    if (-1 < (char)bVar3) {
      plVar8 = plVar9;
    }
    if ((long)local_140 < 0) {
      iVar5 = _memcmp(local_150,plVar8,(size_t)puStack_148);
      if (iVar5 != 0) goto LAB_008ddaf0;
    }
    else if (local_140._7_1_ != 0) {
      ppuVar13 = &local_150;
      do {
        if (*(char *)ppuVar13 != (char)*plVar8) goto LAB_008ddaf0;
        ppuVar13 = (undefined1 **)((long)ppuVar13 + 1);
        plVar8 = (long *)((long)plVar8 + 1);
        puVar12 = puVar12 + -1;
      } while (puVar12 != (undefined1 *)0x0);
    }
  }
  else {
LAB_008ddaf0:
    FUN_008de31c(param_1,1);
  }
  if (*(char *)((long)param_1 + 0x27c) == '\x01') {
    *(undefined1 *)((long)param_1 + 0x27c) = 0;
  }
  FUN_00410c38(param_1[0x4d],param_2);
  FUN_06a03d00(param_1[0x44],0);
  FUN_06a03d00(param_1[0x4d],0);
  FUN_008de400(param_1);
  FUN_008de548(param_1);
  *(undefined1 *)(param_1 + 0x5a) = 0;
  plVar9 = (long *)param_1[0x54];
  if (plVar9 != (long *)0x0) {
    (**(code **)(*plVar9 + 0x68))(plVar9,0);
  }
  if ((long *)param_1[0x4e] != (long *)0x0) {
    (**(code **)(*(long *)param_1[0x4e] + 0x1f0))();
  }
  if (param_1[0x50] != 0) {
    FUN_06a03d00(param_1[0x50],1);
  }
  if (param_1[0x55] != 0) {
    FUN_06a032b4();
  }
  FUN_069faca0(param_1,1);
  iVar5 = thunk_FUN_05e1d97c(2);
  if (iVar5 == 0) goto LAB_008dddac;
  FUN_0488143c(&local_210);
  ppppppppuVar2 = local_210;
  if (-1 < cStack_1f9) {
    ppppppppuVar2 = (undefined ********)&local_210;
  }
  if ((DAT_0a2a9fd7 & 1) == 0) {
    uVar11 = 0;
    do {
      (&DAT_0a2a9fc2)[uVar11] = (&DAT_0855166a)[uVar11] + 0x8a ^ (&DAT_0855165a)[uVar11 & 0xf];
      uVar11 = uVar11 + 1;
    } while (uVar11 != 0x15);
    DAT_0a2a9fd7 = 1;
  }
  if ((DAT_0a2aa013 & 1) == 0) {
    DAT_0a2aa008._0_1_ = 'R';
    DAT_0a2aa008._1_1_ = 'e';
    DAT_0a2aa008._2_1_ = 'l';
    DAT_0a2aa008._3_1_ = 'o';
    DAT_0a2aa008._4_1_ = 'a';
    DAT_0a2aa008._5_1_ = 'd';
    DAT_0a2aa008._6_1_ = 'D';
    DAT_0a2aa008._7_1_ = 'a';
    DAT_0a2aa010 = 0x6174;
    DAT_0a2aa012 = 0;
    DAT_0a2aa013 = 1;
  }
  FUN_05e1d050(&local_1e0,2,ppppppppuVar2,&DAT_0a2a9fc2,&DAT_0a2aa008,0x140,0,0);
  iVar5 = FUN_069fac90(param_1);
  if (iVar5 == 0) {
    local_138 = (undefined ********)&DAT_0a2aa56c;
    if ((DAT_0a2aa572 & 1) == 0) {
      DAT_0a2aa56c = 0x736c6166;
      puVar12 = &DAT_0a2aa570;
      puVar14 = &DAT_0a2aa571;
      puVar15 = &DAT_0a2aa572;
      goto LAB_008ddcdc;
    }
  }
  else {
    local_138 = (undefined ********)&DAT_0a2aa566;
    if ((DAT_0a2aa56b & 1) == 0) {
      DAT_0a2aa566 = 0x7274;
      DAT_0a2aa568 = 0x75;
      puVar14 = &DAT_0a2aa56a;
      puVar12 = &DAT_0a2aa569;
      puVar15 = &DAT_0a2aa56b;
LAB_008ddcdc:
      *puVar12 = 0x65;
      *puVar14 = 0;
      *puVar15 = 1;
    }
  }
  local_130 = (long *)((ulong)local_130 & 0xffffffffffffff00);
  if ((DAT_0a2aa03e & 1) == 0) {
    uVar11 = 0;
    do {
      (&DAT_0a2aa028)[uVar11] = (&DAT_08551714)[uVar11] + 0x8a ^ (&DAT_08551704)[uVar11 & 0xf];
      uVar11 = uVar11 + 1;
    } while (uVar11 != 0x16);
    DAT_0a2aa03e = 1;
  }
  uStack_d8 = 0;
  local_e0 = (long *)0x0;
  local_e8 = (undefined ********)&local_138;
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
  uStack_78 = 0;
  local_80 = 0;
  local_70 = 0;
  FUN_05e1d31c(&local_1e0,&DAT_0a2aa028,&local_e8);
  thunk_FUN_05e1d0bc(&local_1e0);
  if (cStack_1f9 < '\0') {
    __ZdlPvm(local_210,CONCAT17(cStack_1f9,local_200) & 0x7fffffffffffffff);
  }
LAB_008dddac:
  lVar4 = FUN_06a02b54(param_1[0x49]);
  if (lVar4 != 0) {
    ___dynamic_cast(lVar4,&PTR_DAT_09fb57d0,&PTR_DAT_09fb5d48,0);
  }
  iVar5 = FUN_069f06fc();
  if (iVar5 == 0) {
    FUN_008ded90(param_1,0);
  }
  if (local_228 != (long *)0x0) {
    LOAcquire();
    lVar4 = local_228[1];
    local_228[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*local_228 + 0x10))(local_228);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_228);
    }
  }
  plVar9 = local_218;
  if (local_218 != (long *)0x0) {
    LOAcquire();
    lVar4 = local_218[1];
    local_218[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*local_218 + 0x10))(local_218);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar9);
    }
  }
  if ((long)local_140 < 0) {
    __ZdlPvm(local_150,(ulong)local_140 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}



// ===== [d0] FUN_008372c8 @ 008372c8 =====

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_008372c8(long param_1,uint param_2,char *param_3,undefined8 param_4)

{
  uint uVar1;
  undefined1 uVar2;
  uint3 uVar3;
  long lVar4;
  int iVar5;
  int iVar6;
  undefined8 uVar7;
  size_t sVar8;
  undefined8 ******ppppppuVar9;
  ulong uVar10;
  undefined1 *puVar11;
  undefined1 *puVar12;
  undefined1 *puVar13;
  uint uVar14;
  long lVar15;
  long *plVar16;
  undefined4 uVar17;
  undefined4 uVar18;
  undefined8 uVar19;
  undefined8 uVar20;
  undefined8 uVar21;
  undefined8 *****local_418 [2];
  undefined7 local_408;
  char cStack_401;
  undefined8 *****local_400;
  long lStack_3f8;
  long local_3f0;
  undefined8 uStack_3e8;
  undefined4 local_3e0;
  undefined8 *****local_3d0;
  long lStack_3c8;
  long local_3c0;
  undefined8 uStack_3b8;
  undefined4 local_3b0;
  long local_3a0;
  long lStack_398;
  long local_390;
  undefined8 uStack_388;
  undefined4 local_380;
  undefined1 uStack_379;
  undefined8 local_378;
  undefined1 local_370 [72];
  undefined8 *****local_328;
  size_t local_320;
  undefined8 local_318;
  undefined4 local_310;
  undefined8 *****local_308;
  size_t local_300;
  undefined8 local_2f8;
  undefined4 local_2f0;
  long *local_100;
  undefined8 *local_f8;
  undefined8 local_f0;
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
  undefined8 local_80;
  long local_78;
  
  local_78 = *(long *)PTR____stack_chk_guard_09b36c98;
  uVar7 = FUN_00efc934();
  FUN_00efe67c(uVar7,0);
  if ((param_2 == 2) && (iVar5 = FUN_0080d3c0(), iVar5 != 0)) {
    if ((*(long **)(param_1 + 0x198) == (long *)0x0) ||
       (iVar5 = (**(code **)(**(long **)(param_1 + 0x198) + 0x200))(), iVar5 != 0)) {
      local_328 = (undefined8 *****)((ulong)local_328 & 0xffffffffffffff00);
      _bzero(&local_320,0x228);
      FUN_008372c8(param_1,0,&local_328,0);
      if ((char)local_328 == '\x01') {
        if (local_100 != (long *)0x0) {
          LOAcquire();
          lVar4 = local_100[1];
          local_100[1] = lVar4 + -1;
          LORelease();
          if (lVar4 == 0) {
            (**(code **)(*local_100 + 0x10))(local_100);
            __ZNSt3__119__shared_weak_count14__release_weakEv(local_100);
          }
        }
        FUN_001ef570(&local_320);
      }
    }
    FUN_0080d3f0();
    goto LAB_00837fa4;
  }
  if (*(long **)(param_1 + 0x198) == (long *)0x0) {
    iVar5 = 0;
  }
  else {
    iVar5 = (**(code **)(**(long **)(param_1 + 0x198) + 0x200))();
  }
  if ((param_2 == 2) && (iVar5 != 2)) {
    FUN_002badd0(DAT_0a52bdd0);
    uVar7 = FUN_0080a194();
    if ((DAT_0a2a4be2 & 1) == 0) {
      DAT_0a2a4bd8._0_1_ = 'f';
      DAT_0a2a4bd8._1_1_ = 'u';
      DAT_0a2a4bd8._2_1_ = 'n';
      DAT_0a2a4bd8._3_1_ = 'c';
      DAT_0a2a4bd8._4_1_ = '_';
      DAT_0a2a4bd8._5_1_ = 't';
      DAT_0a2a4bd8._6_1_ = 'y';
      DAT_0a2a4bd8._7_1_ = 'p';
      DAT_0a2a4be0 = 0x65;
      DAT_0a2a4be2 = 1;
    }
    sVar8 = _strlen((char *)&DAT_0a2a4bd8);
    if (0x7ffffffffffffff7 < sVar8) {
                    /* WARNING: Subroutine does not return */
      FUN_00018d9c(&local_328);
    }
    if (sVar8 < 0x17) {
      local_318 = CONCAT17((char)sVar8,(undefined7)local_318);
      ppppppuVar9 = &local_328;
      if (sVar8 != 0) goto LAB_008375b8;
    }
    else {
      uVar10 = 0x19;
      if ((sVar8 | 7) != 0x17) {
        uVar10 = (sVar8 | 7) + 1;
      }
      ppppppuVar9 = (undefined8 ******)__Znwm(uVar10);
      local_318 = uVar10 | 0x8000000000000000;
      local_328 = ppppppuVar9;
      local_320 = sVar8;
LAB_008375b8:
      _memcpy(ppppppuVar9,&DAT_0a2a4bd8,sVar8);
    }
    *(undefined1 *)((long)ppppppuVar9 + sVar8) = 0;
    local_310 = 8;
    if ((DAT_0a2a4bf4 & 1) == 0) {
      DAT_0a2a4be8._0_1_ = 'u';
      DAT_0a2a4be8._1_1_ = 'n';
      DAT_0a2a4be8._2_1_ = 'r';
      DAT_0a2a4be8._3_1_ = 'e';
      DAT_0a2a4be8._4_1_ = 'a';
      DAT_0a2a4be8._5_1_ = 'd';
      DAT_0a2a4be8._6_1_ = '_';
      DAT_0a2a4be8._7_1_ = 't';
      DAT_0a2a4bf0 = 0x657079;
      DAT_0a2a4bf4 = 1;
    }
    sVar8 = _strlen((char *)&DAT_0a2a4be8);
    if (0x7ffffffffffffff7 < sVar8) {
                    /* WARNING: Subroutine does not return */
      FUN_00018d9c(&local_308);
    }
    if (sVar8 < 0x17) {
      local_2f8 = CONCAT17((char)sVar8,(undefined7)local_2f8);
      ppppppuVar9 = &local_308;
      if (sVar8 != 0) goto LAB_00837674;
    }
    else {
      uVar10 = 0x19;
      if ((sVar8 | 7) != 0x17) {
        uVar10 = (sVar8 | 7) + 1;
      }
      ppppppuVar9 = (undefined8 ******)__Znwm(uVar10);
      local_2f8 = uVar10 | 0x8000000000000000;
      local_308 = ppppppuVar9;
      local_300 = sVar8;
LAB_00837674:
      _memcpy(ppppppuVar9,&DAT_0a2a4be8,sVar8);
    }
    *(undefined1 *)((long)ppppppuVar9 + sVar8) = 0;
    local_2f0 = 0xffffffff;
    lStack_398 = 0;
    local_3a0 = 0;
    uStack_388 = 0;
    local_390 = 0;
    local_380 = 0x3f800000;
    FUN_0083f02c(&local_3a0,&local_328,&local_328);
    FUN_0083f02c(&local_3a0,&local_308,&local_308);
    FUN_01bb281c(uVar7,1,&local_3a0);
    lVar4 = local_3a0;
    plVar16 = (long *)local_390;
    while (plVar16 != (long *)0x0) {
      lVar15 = *plVar16;
      local_3a0 = lVar4;
      if (*(char *)((long)plVar16 + 0x27) < '\0') {
        __ZdlPvm(plVar16[2],plVar16[4] & 0x7fffffffffffffff);
      }
      __ZdlPvm(plVar16,0x30);
      lVar4 = local_3a0;
      plVar16 = (long *)lVar15;
    }
    local_3a0 = 0;
    if (lVar4 != 0) {
      __ZdlPvm(lVar4,lStack_398 << 3);
    }
    if ((long)local_2f8 < 0) {
      uVar10 = local_2f8 & 0x7fffffffffffffff;
      ppppppuVar9 = (undefined8 ******)local_308;
LAB_008377d4:
      __ZdlPvm(ppppppuVar9,uVar10);
    }
LAB_008377d8:
    if ((long)local_318 < 0) {
      uVar10 = local_318 & 0x7fffffffffffffff;
      ppppppuVar9 = (undefined8 ******)local_328;
LAB_008377ec:
      __ZdlPvm(ppppppuVar9,uVar10);
    }
  }
  else {
    if ((param_2 == 0) && (iVar5 == 2)) {
      FUN_002badd0(DAT_0a52bdd0);
      uVar7 = FUN_0080a194();
      if ((DAT_0a2a4be2 & 1) == 0) {
        DAT_0a2a4bd8._0_1_ = 'f';
        DAT_0a2a4bd8._1_1_ = 'u';
        DAT_0a2a4bd8._2_1_ = 'n';
        DAT_0a2a4bd8._3_1_ = 'c';
        DAT_0a2a4bd8._4_1_ = '_';
        DAT_0a2a4bd8._5_1_ = 't';
        DAT_0a2a4bd8._6_1_ = 'y';
        DAT_0a2a4bd8._7_1_ = 'p';
        DAT_0a2a4be0 = 0x65;
        DAT_0a2a4be2 = 1;
      }
      sVar8 = _strlen((char *)&DAT_0a2a4bd8);
      if (0x7ffffffffffffff7 < sVar8) {
                    /* WARNING: Subroutine does not return */
        FUN_00018d9c(&local_328);
      }
      if (sVar8 < 0x17) {
        local_318 = CONCAT17((char)sVar8,(undefined7)local_318);
        ppppppuVar9 = &local_328;
        if (sVar8 != 0) goto LAB_00837768;
      }
      else {
        uVar10 = 0x19;
        if ((sVar8 | 7) != 0x17) {
          uVar10 = (sVar8 | 7) + 1;
        }
        ppppppuVar9 = (undefined8 ******)__Znwm(uVar10);
        local_318 = uVar10 | 0x8000000000000000;
        local_328 = ppppppuVar9;
        local_320 = sVar8;
LAB_00837768:
        _memcpy(ppppppuVar9,&DAT_0a2a4bd8,sVar8);
      }
      *(undefined1 *)((long)ppppppuVar9 + sVar8) = 0;
      local_310 = 6;
      lStack_3c8 = 0;
      local_3d0 = (undefined8 ******)0x0;
      uStack_3b8 = 0;
      local_3c0 = 0;
      local_3b0 = 0x3f800000;
      FUN_0083f02c(&local_3d0,&local_328,&local_328);
      FUN_01bb281c(uVar7,1,&local_3d0);
      ppppppuVar9 = (undefined8 ******)local_3d0;
      plVar16 = (long *)local_3c0;
      while (plVar16 != (long *)0x0) {
        lVar4 = *plVar16;
        local_3d0 = ppppppuVar9;
        if (*(char *)((long)plVar16 + 0x27) < '\0') {
          __ZdlPvm(plVar16[2],plVar16[4] & 0x7fffffffffffffff);
        }
        __ZdlPvm(plVar16,0x30);
        ppppppuVar9 = (undefined8 ******)local_3d0;
        plVar16 = (long *)lVar4;
      }
      local_3d0 = (undefined8 *****)0x0;
      if (ppppppuVar9 != (undefined8 ******)0x0) {
        uVar10 = lStack_3c8 << 3;
        goto LAB_008377d4;
      }
      goto LAB_008377d8;
    }
    if ((param_2 != 2) && (iVar5 == 2)) {
      FUN_002badd0(DAT_0a52bdd0);
      uVar7 = FUN_0080a194();
      lStack_3f8 = 0;
      local_400 = (undefined8 ******)0x0;
      uStack_3e8 = 0;
      local_3f0 = 0;
      local_3e0 = 0x3f800000;
      FUN_01bb281c(uVar7,0xc,&local_400);
      ppppppuVar9 = (undefined8 ******)local_400;
      plVar16 = (long *)local_3f0;
      while (plVar16 != (long *)0x0) {
        lVar4 = *plVar16;
        local_400 = ppppppuVar9;
        if (*(char *)((long)plVar16 + 0x27) < '\0') {
          __ZdlPvm(plVar16[2],plVar16[4] & 0x7fffffffffffffff);
        }
        __ZdlPvm(plVar16,0x30);
        ppppppuVar9 = (undefined8 ******)local_400;
        plVar16 = (long *)lVar4;
      }
      local_400 = (undefined8 *****)0x0;
      if (ppppppuVar9 == (undefined8 ******)0x0) goto LAB_008377f0;
      uVar10 = lStack_3f8 << 3;
      goto LAB_008377ec;
    }
  }
LAB_008377f0:
  lVar4 = FUN_00836288(param_1,param_2);
  if ((param_2 == 2) && (lVar4 == 0)) {
    FUN_00835208(param_1,2);
    lVar4 = FUN_00836288(param_1,2);
  }
  if (lVar4 == 0) {
    iVar5 = thunk_FUN_05e1d97c(4);
    if (iVar5 != 0) {
      FUN_0488143c(local_418);
      ppppppuVar9 = (undefined8 ******)local_418[0];
      if (-1 < cStack_401) {
        ppppppuVar9 = local_418;
      }
      if ((DAT_0a2a4b74 & 1) == 0) {
        uRam000000000a2a4b68._0_1_ = 'a';
        uRam000000000a2a4b68._1_1_ = 'i';
        uRam000000000a2a4b68._2_1_ = 'l';
        uRam000000000a2a4b68._3_1_ = '_';
        uRam000000000a2a4b68._4_1_ = 'v';
        uRam000000000a2a4b68._5_1_ = 'i';
        uRam000000000a2a4b68._6_1_ = 'e';
        uRam000000000a2a4b68._7_1_ = 'w';
        DAT_0a2a4b60 = 'c';
        DAT_0a2a4b60_1._0_1_ = 'h';
        DAT_0a2a4b60_1._1_1_ = 'a';
        DAT_0a2a4b60_1._2_1_ = 't';
        DAT_0a2a4b60_1._3_1_ = '_';
        DAT_0a2a4b60_1._4_1_ = 'd';
        DAT_0a2a4b60_1._5_1_ = 'e';
        DAT_0a2a4b60_1._6_1_ = 't';
        DAT_0a2a4b70 = 0x63632e;
        DAT_0a2a4b74 = 1;
      }
      if ((DAT_0a2a4c08 & 1) == 0) {
        uVar10 = 0;
        do {
          (&DAT_0a2a4bf5)[uVar10] = (&DAT_085440dd)[uVar10] + 0x69 ^ (&DAT_085440cd)[uVar10 & 0xf];
          uVar10 = uVar10 + 1;
        } while (uVar10 != 0x13);
        DAT_0a2a4c08 = 1;
      }
      FUN_05e1d050(&local_328,4,ppppppuVar9,&DAT_0a2a4b60,&DAT_0a2a4bf5,0x15b,0,0);
      local_378 = (undefined1 *)0x0;
      if ((DAT_0a2a500e & 1) == 0) {
        uVar10 = 0;
        do {
          uVar17 = *(undefined4 *)((long)&DAT_085447c3 + uVar10);
          uVar3 = CONCAT12((char)((uint)uVar17 >> 8),(short)uVar17) & 0xff00ff;
          uVar18 = *(undefined4 *)((long)&DAT_085447af + uVar10 % 0x14);
          *(uint *)((long)&DAT_0a2a4fc6 + uVar10) =
               CONCAT13((char)((uint)uVar17 >> 0x18) + 0x8aU ^ (byte)((uint)uVar18 >> 0x18),
                        CONCAT12((char)((uint)uVar17 >> 0x10) + 0x8aU ^ (byte)((uint)uVar18 >> 0x10)
                                 ,CONCAT11((char)(uVar3 >> 0x10) + 0x8aU ^ (byte)((uint)uVar18 >> 8)
                                           ,(char)uVar3 + 0x8aU ^ (byte)uVar18)));
          uVar10 = uVar10 + 4;
        } while (uVar10 != 0x48);
        DAT_0a2a500e = 1;
      }
      lVar4 = 8;
      uVar14 = param_2;
      do {
        lVar15 = lVar4;
        local_370[lVar15 + -8] =
             *(undefined1 *)((long)&DAT_0a2a4fc6 + (long)((int)uVar14 % 10 + 0x23));
        lVar4 = lVar15 + 1;
        uVar1 = uVar14 + 9;
        uVar14 = (int)uVar14 / 10;
      } while (0x12 < uVar1);
      if ((int)param_2 < 0) {
        local_370[lVar15 + -7] = 0x2d;
        lVar4 = lVar15 + 2;
      }
      local_370[lVar4 + -8] = 0;
      if (9 < lVar4) {
        puVar13 = local_370;
        puVar11 = &uStack_379 + lVar4;
        do {
          puVar13 = puVar13 + 1;
          uVar2 = *puVar11;
          puVar12 = puVar11 + -1;
          *puVar11 = puVar13[-1];
          puVar13[-1] = uVar2;
          puVar11 = puVar12;
        } while (puVar13 < puVar12);
      }
      if ((DAT_0a2a4c2c & 1) == 0) {
        _DAT_0a2a4c0c = 0x2073692065676170;
        uRam000000000a2a4c14 = 0x2c7274706c6c756e;
        _DAT_0a2a4c1c = 0x79745f6567617020;
        uRam000000000a2a4c24 = 0x5f25203d206570;
        DAT_0a2a4c2c = 1;
      }
      uStack_e8 = 0;
      local_f0 = 0;
      local_f8 = &local_378;
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
      local_80 = 0;
      local_378 = local_370;
      FUN_05e1d31c(&local_328,&DAT_0a2a4c0c,&local_f8);
      thunk_FUN_05e1d0bc(&local_328);
      if (cStack_401 < '\0') {
        __ZdlPvm(local_418[0],CONCAT17(cStack_401,local_408) & 0x7fffffffffffffff);
      }
    }
  }
  else {
    lVar15 = *(long *)(param_1 + 0x198);
    if (lVar15 != lVar4) {
      *(long *)(param_1 + 0x198) = lVar4;
      FUN_06b0c484(*(undefined8 *)(param_1 + 400));
      lVar15 = *(long *)(param_1 + 0x198);
    }
    uVar7 = FUN_069fb09c(*(undefined8 *)(param_1 + 400));
    FUN_069fbaf0(lVar15,uVar7);
    plVar16 = *(long **)(param_1 + 0x198);
    uVar7 = FUN_0122bb54(param_1);
    (**(code **)(*plVar16 + 0x208))
              (plVar16,uVar7,*(uint *)(*(long *)(*(long *)(param_1 + 0x188) + 0x28) + 8) >> 0xf & 1)
    ;
    if ((param_2 & 0xfffffffe) == 2) {
      FUN_06a00764(param_1,7);
    }
    if (*param_3 == '\x01') {
      (**(code **)(**(long **)(param_1 + 0x198) + 0x1f0))(*(long **)(param_1 + 0x198),param_3 + 8);
    }
    if (param_2 == 0) {
      FUN_001587f4(param_1,0);
      if (iVar5 != 0) {
        FUN_002badd0(DAT_0a52bdd0);
        uVar7 = FUN_008380f4();
        FUN_01bd7060(uVar7,0,param_4);
      }
    }
    else {
      FUN_001587f4(param_1,1);
    }
    iVar5 = FUN_06b0c530(*(undefined8 *)(param_1 + 400));
    if (0 < iVar5) {
      iVar5 = 0;
      uVar7 = 0x2069202c7274706c;
      uVar21 = 0;
      uVar20 = 0;
      uVar19 = 0x5f25203d;
      do {
        plVar16 = (long *)FUN_06b0c524(*(undefined8 *)(param_1 + 400),iVar5);
        if (plVar16 == (long *)0x0) {
          iVar6 = thunk_FUN_05e1d97c(4);
          if (iVar6 != 0) {
            FUN_0488143c(local_418);
            ppppppuVar9 = (undefined8 ******)local_418[0];
            if (-1 < cStack_401) {
              ppppppuVar9 = local_418;
            }
            if ((DAT_0a2a4b74 & 1) == 0) {
              uRam000000000a2a4b68._0_1_ = 'a';
              uRam000000000a2a4b68._1_1_ = 'i';
              uRam000000000a2a4b68._2_1_ = 'l';
              uRam000000000a2a4b68._3_1_ = '_';
              uRam000000000a2a4b68._4_1_ = 'v';
              uRam000000000a2a4b68._5_1_ = 'i';
              uRam000000000a2a4b68._6_1_ = 'e';
              uRam000000000a2a4b68._7_1_ = 'w';
              DAT_0a2a4b60 = 'c';
              DAT_0a2a4b60_1._0_1_ = 'h';
              DAT_0a2a4b60_1._1_1_ = 'a';
              DAT_0a2a4b60_1._2_1_ = 't';
              DAT_0a2a4b60_1._3_1_ = '_';
              DAT_0a2a4b60_1._4_1_ = 'd';
              DAT_0a2a4b60_1._5_1_ = 'e';
              DAT_0a2a4b60_1._6_1_ = 't';
              DAT_0a2a4b70 = 0x63632e;
              DAT_0a2a4b74 = 1;
            }
            if ((DAT_0a2a4c08 & 1) == 0) {
              uVar10 = 0;
              do {
                (&DAT_0a2a4bf5)[uVar10] =
                     (&DAT_085440dd)[uVar10] + 0x69 ^ (&DAT_085440cd)[uVar10 & 0xf];
                uVar10 = uVar10 + 1;
              } while (uVar10 != 0x13);
              DAT_0a2a4c08 = 1;
            }
            FUN_05e1d050(&local_328,4,ppppppuVar9,&DAT_0a2a4b60,&DAT_0a2a4bf5,0x17d,0,0,uVar19,
                         uVar20,uVar7,uVar21);
            local_378 = (undefined1 *)0x0;
            if ((DAT_0a2a500e & 1) == 0) {
              uVar10 = 0;
              do {
                uVar17 = *(undefined4 *)((long)&DAT_085447c3 + uVar10);
                uVar3 = CONCAT12((char)((uint)uVar17 >> 8),(short)uVar17) & 0xff00ff;
                uVar18 = *(undefined4 *)((long)&DAT_085447af + uVar10 % 0x14);
                *(uint *)((long)&DAT_0a2a4fc6 + uVar10) =
                     CONCAT13((char)((uint)uVar17 >> 0x18) + 0x8aU ^ (byte)((uint)uVar18 >> 0x18),
                              CONCAT12((char)((uint)uVar17 >> 0x10) + 0x8aU ^
                                       (byte)((uint)uVar18 >> 0x10),
                                       CONCAT11((char)(uVar3 >> 0x10) + 0x8aU ^
                                                (byte)((uint)uVar18 >> 8),
                                                (char)uVar3 + 0x8aU ^ (byte)uVar18)));
                uVar10 = uVar10 + 4;
              } while (uVar10 != 0x48);
              DAT_0a2a500e = 1;
            }
            lVar4 = 0;
            iVar6 = iVar5;
            do {
              lVar15 = lVar4;
              local_370[lVar15] = *(undefined1 *)((long)&DAT_0a2a4fc6 + (long)(iVar6 % 10 + 0x23));
              uVar14 = iVar6 + 9;
              lVar4 = lVar15 + 1;
              iVar6 = iVar6 / 10;
            } while (0x12 < uVar14);
            local_370[lVar15 + 1] = 0;
            if (8 < lVar15 + 8U) {
              puVar11 = local_370 + lVar15;
              puVar13 = local_370;
              do {
                puVar13 = puVar13 + 1;
                uVar2 = *puVar11;
                puVar12 = puVar11 + -1;
                *puVar11 = puVar13[-1];
                puVar13[-1] = uVar2;
                puVar11 = puVar12;
              } while (puVar13 < puVar12);
            }
            if ((DAT_0a2a4c4d & 1) == 0) {
              DAT_0a2a4c48 = (undefined4)uVar19;
              DAT_0a2a4c4c = 0;
              DAT_0a2a4c4d = 1;
              _DAT_0a2a4c30 = 0x6761705f74616863;
              uRam000000000a2a4c38 = 0x6c756e2073692065;
              DAT_0a2a4c40 = uVar7;
            }
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
            uStack_88 = 0;
            local_90 = 0;
            local_80 = 0;
            local_378 = local_370;
            local_f8 = &local_378;
            FUN_05e1d31c(&local_328,&DAT_0a2a4c30,&local_f8);
            thunk_FUN_05e1d0bc(&local_328);
            if (cStack_401 < '\0') {
              __ZdlPvm(local_418[0],CONCAT17(cStack_401,local_408) & 0x7fffffffffffffff);
            }
          }
        }
        else {
          (**(code **)(*plVar16 + 0x1f8))(plVar16,param_2);
        }
        iVar5 = iVar5 + 1;
        iVar6 = FUN_06b0c530(*(undefined8 *)(param_1 + 400));
      } while (iVar5 < iVar6);
    }
    FUN_001313d0(param_1,param_2);
    iVar5 = (**(code **)(**(long **)(param_1 + 0x198) + 0x200))();
    if ((iVar5 != 3) && (*(char *)(param_1 + 0x1cc) == '\x01')) {
      FUN_00838268(param_1,3);
      *(undefined1 *)(param_1 + 0x1cc) = 0;
    }
  }
LAB_00837fa4:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_78) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}



// ===== [d0] FUN_0083e394 @ 0083e394 =====

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0083e394(long param_1,char *param_2)

{
  undefined8 ***pppuVar1;
  long *plVar2;
  int iVar3;
  long lVar4;
  undefined8 uVar5;
  ulong uVar6;
  long lVar7;
  char local_648 [8];
  undefined1 auStack_640 [536];
  undefined8 local_428;
  long *local_420;
  undefined8 local_418;
  char local_410 [8];
  undefined1 auStack_408 [536];
  undefined8 local_1f0;
  long *local_1e8;
  undefined8 **local_1e0 [2];
  undefined7 local_1d0;
  char cStack_1c9;
  undefined8 **local_1c8 [2];
  undefined7 local_1b8;
  char cStack_1b1;
  undefined8 **local_1b0;
  ulong uStack_1a8;
  undefined8 **local_120;
  ulong uStack_118;
  undefined7 local_110;
  char cStack_109;
  undefined8 **local_d0;
  undefined8 uStack_c8;
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
  undefined8 uStack_70;
  undefined8 local_68;
  undefined8 uStack_60;
  undefined8 local_58;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  _bzero(local_648,0x230);
  if (*param_2 != '\x01') {
    lVar7 = *(long *)(param_1 + 8);
    if ((*(long **)(lVar7 + 0x198) == (long *)0x0) ||
       (iVar3 = (**(code **)(**(long **)(lVar7 + 0x198) + 0x200))(), iVar3 != 0)) {
      uVar5 = FUN_00a82fdc(*(undefined8 *)(lVar7 + 0x1a8));
      FUN_008372c8(lVar7,0,local_648,uVar5);
    }
    goto LAB_0083e890;
  }
  FUN_003c56c4(auStack_640,param_2 + 8);
  local_428 = *(undefined8 *)(param_2 + 0x220);
  local_420 = *(long **)(param_2 + 0x228);
  if (local_420 != (long *)0x0) {
    local_420[1] = local_420[1] + 1;
  }
  local_648[0] = '\x01';
  lVar7 = *(long *)(param_1 + 8);
  iVar3 = thunk_FUN_05e1d97c(2);
  if (iVar3 != 0) {
    FUN_0488143c(local_1c8);
    pppuVar1 = (undefined8 ***)local_1c8[0];
    if (-1 < cStack_1b1) {
      pppuVar1 = local_1c8;
    }
    if ((DAT_0a2a4b74 & 1) == 0) {
      uRam000000000a2a4b68._0_1_ = 'a';
      uRam000000000a2a4b68._1_1_ = 'i';
      uRam000000000a2a4b68._2_1_ = 'l';
      uRam000000000a2a4b68._3_1_ = '_';
      uRam000000000a2a4b68._4_1_ = 'v';
      uRam000000000a2a4b68._5_1_ = 'i';
      uRam000000000a2a4b68._6_1_ = 'e';
      uRam000000000a2a4b68._7_1_ = 'w';
      DAT_0a2a4b60 = 'c';
      DAT_0a2a4b60_1._0_1_ = 'h';
      DAT_0a2a4b60_1._1_1_ = 'a';
      DAT_0a2a4b60_1._2_1_ = 't';
      DAT_0a2a4b60_1._3_1_ = '_';
      DAT_0a2a4b60_1._4_1_ = 'd';
      DAT_0a2a4b60_1._5_1_ = 'e';
      DAT_0a2a4b60_1._6_1_ = 't';
      DAT_0a2a4b70 = 0x63632e;
      DAT_0a2a4b74 = 1;
    }
    if ((DAT_0a2a5033 & 1) == 0) {
      DAT_0a2a5028._0_1_ = 'o';
      DAT_0a2a5028._1_1_ = 'p';
      DAT_0a2a5028._2_1_ = 'e';
      DAT_0a2a5028._3_1_ = 'r';
      DAT_0a2a5028._4_1_ = 'a';
      DAT_0a2a5028._5_1_ = 't';
      DAT_0a2a5028._6_1_ = 'o';
      DAT_0a2a5028._7_1_ = 'r';
      DAT_0a2a5030 = 0x2928;
      DAT_0a2a5032 = 0;
      DAT_0a2a5033 = 1;
    }
    FUN_05e1d050(&local_1b0,2,pppuVar1,&DAT_0a2a4b60,&DAT_0a2a5028,0x113,0,0);
    FUN_0001accc(auStack_640);
    FUN_04980e70(local_1e0);
    local_120 = local_1e0[0];
    if (-1 < cStack_1c9) {
      local_120 = local_1e0;
    }
    uStack_118 = uStack_118 & 0xffffffffffffff00;
    if ((DAT_0a2a5113 & 1) == 0) {
      uVar6 = 0;
      do {
        (&DAT_0a2a50fc)[uVar6] = (&DAT_08544d93)[uVar6] + 0x69 ^ (&DAT_08544d83)[uVar6 & 0xf];
        uVar6 = uVar6 + 1;
      } while (uVar6 != 0x17);
      DAT_0a2a5113 = 1;
    }
    uStack_c0 = 0;
    uStack_c8 = 0;
    local_d0 = &local_120;
    uStack_b0 = 0;
    local_b8 = 0;
    uStack_a0 = 0;
    local_a8 = 0;
    uStack_90 = 0;
    local_98 = 0;
    uStack_80 = 0;
    local_88 = 0;
    uStack_70 = 0;
    local_78 = 0;
    uStack_60 = 0;
    local_68 = 0;
    local_58 = 0;
    FUN_05e1d31c(&local_1b0,&DAT_0a2a50fc,&local_d0);
    if (cStack_1c9 < '\0') {
      __ZdlPvm(local_1e0[0],CONCAT17(cStack_1c9,local_1d0) & 0x7fffffffffffffff);
    }
    thunk_FUN_05e1d0bc(&local_1b0);
    if (cStack_1b1 < '\0') {
      __ZdlPvm(local_1c8[0],CONCAT17(cStack_1b1,local_1b8) & 0x7fffffffffffffff);
    }
  }
  FUN_0001accc(auStack_640);
  uVar6 = FUN_04bb3ffc();
  if ((uVar6 & 1) == 0) {
    FUN_0001accc(auStack_640);
    iVar3 = FUN_04bb4f0c();
    if (iVar3 == 0) {
LAB_0083e870:
      uVar5 = 1;
      goto LAB_0083e874;
    }
    lVar4 = FUN_00836288(lVar7,3);
    if (lVar4 == 0) {
      uVar5 = thunk_FUN_05e1d97c(4);
      if ((int)uVar5 != 0) {
        FUN_0488143c(&local_120);
        pppuVar1 = (undefined8 ***)local_120;
        if (-1 < cStack_109) {
          pppuVar1 = &local_120;
        }
        if ((DAT_0a2a4b74 & 1) == 0) {
          uRam000000000a2a4b68._0_1_ = 'a';
          uRam000000000a2a4b68._1_1_ = 'i';
          uRam000000000a2a4b68._2_1_ = 'l';
          uRam000000000a2a4b68._3_1_ = '_';
          uRam000000000a2a4b68._4_1_ = 'v';
          uRam000000000a2a4b68._5_1_ = 'i';
          uRam000000000a2a4b68._6_1_ = 'e';
          uRam000000000a2a4b68._7_1_ = 'w';
          DAT_0a2a4b60 = 'c';
          DAT_0a2a4b60_1._0_1_ = 'h';
          DAT_0a2a4b60_1._1_1_ = 'a';
          DAT_0a2a4b60_1._2_1_ = 't';
          DAT_0a2a4b60_1._3_1_ = '_';
          DAT_0a2a4b60_1._4_1_ = 'd';
          DAT_0a2a4b60_1._5_1_ = 'e';
          DAT_0a2a4b60_1._6_1_ = 't';
          DAT_0a2a4b70 = 0x63632e;
          DAT_0a2a4b74 = 1;
        }
        if ((DAT_0a2a5033 & 1) == 0) {
          DAT_0a2a5028._0_1_ = 'o';
          DAT_0a2a5028._1_1_ = 'p';
          DAT_0a2a5028._2_1_ = 'e';
          DAT_0a2a5028._3_1_ = 'r';
          DAT_0a2a5028._4_1_ = 'a';
          DAT_0a2a5028._5_1_ = 't';
          DAT_0a2a5028._6_1_ = 'o';
          DAT_0a2a5028._7_1_ = 'r';
          DAT_0a2a5030 = 0x2928;
          DAT_0a2a5032 = 0;
          DAT_0a2a5033 = 1;
        }
        FUN_05e1d050(&local_1b0,4,pppuVar1,&DAT_0a2a4b60,&DAT_0a2a5028,0x124,0,0);
        if ((DAT_0a2a512b & 1) == 0) {
          uVar6 = 0;
          do {
            (&DAT_0a2a5114)[uVar6] = (&DAT_08544dba)[uVar6] + 0x69 ^ (&DAT_08544daa)[uVar6 & 0xf];
            uVar6 = uVar6 + 1;
          } while (uVar6 != 0x17);
          DAT_0a2a512b = 1;
        }
        local_68 = 0;
        uStack_70 = 0;
        local_58 = 0;
        uStack_60 = 0;
        local_88 = 0;
        uStack_90 = 0;
        local_78 = 0;
        uStack_80 = 0;
        local_a8 = 0;
        uStack_b0 = 0;
        local_98 = 0;
        uStack_a0 = 0;
        uStack_c8 = 0;
        local_d0 = (undefined8 ***)0x0;
        local_b8 = 0;
        uStack_c0 = 0;
        FUN_05e1d31c(&local_1b0,&DAT_0a2a5114,&local_d0);
        uVar5 = thunk_FUN_05e1d0bc(&local_1b0);
        if (cStack_109 < '\0') {
          uVar5 = __ZdlPvm(local_120,CONCAT17(cStack_109,local_110) & 0x7fffffffffffffff);
        }
      }
      FUN_0083b468(uVar5,0);
      goto LAB_0083e870;
    }
    iVar3 = FUN_008f8a20(lVar4);
    if (iVar3 == 0) {
      local_d0 = (undefined8 **)FUN_0083b2ac;
      uStack_c8 = 0;
      local_1c8[0] = (undefined8 **)FUN_00040430(lVar7 + 0x1d0);
      FUN_000404d8(&local_1b0,local_1c8,*(undefined8 *)(lVar7 + 0x1d8));
      FUN_000403ac(local_1c8);
      uStack_118 = uStack_1a8;
      local_120 = local_1b0;
      uVar5 = __Znwm(0x270);
      FUN_0083ee94(uVar5,FUN_0083eb08,&local_d0,&local_120,local_648);
      local_418 = uVar5;
      FUN_008f8a28(lVar4,&local_418);
      FUN_00033d2c(&local_418);
      FUN_000403ac(&local_120);
    }
    else {
      _bzero(local_410,0x230);
      if (local_648[0] == '\x01') {
        FUN_003c56c4(auStack_408,auStack_640);
        local_1f0 = local_428;
        local_1e8 = local_420;
        if (local_420 != (long *)0x0) {
          local_420[1] = local_420[1] + 1;
        }
        local_410[0] = '\x01';
      }
      FUN_0083b2ac(lVar7,local_410,0);
      plVar2 = local_1e8;
      if (local_410[0] == '\x01') {
        if (local_1e8 != (long *)0x0) {
          LOAcquire();
          lVar4 = local_1e8[1];
          local_1e8[1] = lVar4 + -1;
          LORelease();
          if (lVar4 == 0) {
            (**(code **)(*local_1e8 + 0x10))(local_1e8);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
          }
        }
        FUN_001ef570(auStack_408);
        local_410[0] = '\0';
      }
    }
  }
  else {
    uVar5 = 2;
LAB_0083e874:
    FUN_008372c8(lVar7,uVar5,local_648,0);
  }
  FUN_008392d0(lVar7,lVar7);
LAB_0083e890:
  plVar2 = local_420;
  if (local_648[0] == '\x01') {
    if (local_420 != (long *)0x0) {
      LOAcquire();
      lVar7 = local_420[1];
      local_420[1] = lVar7 + -1;
      LORelease();
      if (lVar7 == 0) {
        (**(code **)(*local_420 + 0x10))(local_420);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
      }
    }
    FUN_001ef570(auStack_640);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}



