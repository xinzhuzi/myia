// Ghidra inferred pseudocode; requested=0x30bda14
// entry=030bda14 end=030bec47

/* WARNING: Removing unreachable block (ram,0x030be02c) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_030bda14(long *param_1,undefined8 param_2,long *param_3)

{
  undefined1 uVar1;
  long *plVar2;
  bool bVar3;
  long lVar4;
  long lVar5;
  int iVar6;
  undefined4 uVar7;
  ulong uVar8;
  undefined8 *puVar9;
  long *plVar10;
  undefined8 uVar11;
  undefined8 *******pppppppuVar12;
  char cVar13;
  undefined1 *puVar14;
  undefined1 *puVar15;
  undefined1 *puVar16;
  long lVar17;
  uint uVar18;
  ulong uVar19;
  int iVar20;
  long lVar21;
  long local_3b0;
  long *local_3a8;
  undefined8 *******local_3a0 [2];
  undefined7 local_390;
  char cStack_389;
  undefined8 *******local_388 [2];
  undefined7 local_378;
  char cStack_371;
  long local_370;
  undefined8 local_368;
  ulong local_360;
  ulong local_358;
  uint local_350;
  undefined4 uStack_34c;
  long *local_348;
  undefined8 local_2e0;
  undefined1 *puStack_2d8;
  undefined1 *local_2d0;
  undefined1 *puStack_2c8;
  undefined1 *local_2c0;
  long *local_2b8;
  undefined1 *local_2b0;
  undefined1 *puStack_2a8;
  undefined8 local_2a0;
  undefined1 *puStack_298;
  undefined1 *local_290;
  undefined1 *local_288;
  long local_278;
  long *local_270;
  undefined8 *******local_268;
  undefined8 local_260;
  undefined7 local_258;
  char cStack_251;
  undefined8 *******local_218;
  undefined8 local_210;
  undefined7 local_208;
  char cStack_201;
  undefined1 uStack_1c9;
  undefined8 local_1c8;
  undefined8 local_1c0;
  undefined7 local_1b8;
  char cStack_1b1;
  undefined1 uStack_179;
  undefined8 local_178;
  undefined1 local_170 [72];
  undefined8 *******local_128;
  undefined1 local_120;
  undefined8 *******local_d8;
  undefined8 *puStack_d0;
  undefined8 *local_c8;
  undefined8 *******pppppppuStack_c0;
  undefined8 *******local_b8;
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
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar5 = *(long *)(*param_3 + 0x18);
  local_270 = *(long **)(*param_3 + 0x20);
  lVar4 = 0;
  if (local_270 != (long *)0x0) {
    lVar4 = local_270[1];
    local_270[1] = lVar4 + 1;
  }
  param_1[3] = (long)&SUB_aaaaaaaaaaaaaaaa;
  param_1[2] = (long)&SUB_aaaaaaaaaaaaaaaa;
  param_1[5] = (long)&SUB_aaaaaaaaaaaaaaaa;
  param_1[4] = (long)&SUB_aaaaaaaaaaaaaaaa;
  param_1[1] = (long)&SUB_aaaaaaaaaaaaaaaa;
  *param_1 = (long)&SUB_aaaaaaaaaaaaaaaa;
  local_278 = lVar5;
  FUN_0304f1cc(lVar4,param_1,0,0);
  iVar6 = FUN_04bb6cd4(lVar5 + 0x30);
  if ((iVar6 != 0) && (uVar8 = FUN_04a2eed8(lVar5), (uVar8 & 1) == 0)) {
    *(undefined4 *)(lVar5 + 0x118) = 5;
    FUN_030f6650(&local_370,1,1,(int)*param_1,*(undefined4 *)((long)param_1 + 4));
    *param_1 = local_370;
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_1 + 1,&local_368)
    ;
    if (local_348 != (long *)0x0) {
      local_348[1] = local_348[1] + 1;
    }
    plVar10 = (long *)param_1[5];
    param_1[4] = CONCAT44(uStack_34c,local_350);
    param_1[5] = (long)local_348;
    if (plVar10 != (long *)0x0) {
      LOAcquire();
      lVar5 = plVar10[1];
      plVar10[1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*plVar10 + 0x10))(plVar10);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
      }
    }
    if (local_348 != (long *)0x0) {
      LOAcquire();
      lVar5 = local_348[1];
      local_348[1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*local_348 + 0x10))(local_348);
        __ZNSt3__119__shared_weak_count14__release_weakEv(local_348);
      }
    }
    if ((long)local_358 < 0) {
      __ZdlPvm(local_368,local_358 & 0x7fffffffffffffff);
    }
    goto LAB_030beb50;
  }
  puStack_298 = &SUB_aaaaaaaaaaaaaaaa;
  local_2a0 = &SUB_aaaaaaaaaaaaaaaa;
  local_288 = &SUB_aaaaaaaaaaaaaaaa;
  local_290 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_2a8 = &SUB_aaaaaaaaaaaaaaaa;
  local_2b0 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0465bdac(&local_2b0);
  local_288 = (undefined1 *)((ulong)local_288 | 1);
  local_290 = (undefined1 *)CONCAT44(local_290._4_4_,1);
  lVar4 = (long)(int)local_2a0;
  if ((int)local_2a0 < local_2a0._4_4_) {
    local_2a0 = (undefined1 *)CONCAT44(local_2a0._4_4_,(int)local_2a0 + 1);
    lVar4 = *(long *)(puStack_2a8 + lVar4 * 8);
  }
  else {
    if (local_2a0._4_4_ == (int)puStack_298) {
      FUN_05ab4038((ulong)&local_2b0 | 8,local_2a0._4_4_ + 1);
    }
    local_2a0._4_4_ = local_2a0._4_4_ + 1;
    lVar4 = __Znwm(0x38);
    FUN_0465bd88();
    lVar21 = (long)(int)local_2a0;
    local_2a0 = (undefined1 *)CONCAT44(local_2a0._4_4_,(int)local_2a0 + 1);
    *(long *)(puStack_2a8 + lVar21 * 8) = lVar4;
  }
  *(uint *)(lVar4 + 0x34) = *(uint *)(lVar4 + 0x34) | 2;
  puVar9 = *(undefined8 **)(lVar4 + 0x10);
  if (puVar9 == &DAT_0a524ad0) {
    puVar9 = (undefined8 *)__Znwm(0x18);
    *puVar9 = 0;
    puVar9[1] = 0;
    puVar9[2] = 0;
    *(undefined8 **)(lVar4 + 0x10) = puVar9;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar9,lVar5 + 0x130);
  *(uint *)(lVar4 + 0x34) = *(uint *)(lVar4 + 0x34) | 1;
  lVar21 = *(long *)(lVar4 + 8);
  if (lVar21 == 0) {
    lVar21 = __Znwm(0x18);
    FUN_04f33c00();
    *(long *)(lVar4 + 8) = lVar21;
  }
  *(uint *)(lVar21 + 0x14) = *(uint *)(lVar21 + 0x14) | 1;
  puVar9 = *(undefined8 **)(lVar21 + 8);
  if (puVar9 == &DAT_0a524ad0) {
    puVar9 = (undefined8 *)__Znwm(0x18);
    *puVar9 = 0;
    puVar9[1] = 0;
    puVar9[2] = 0;
    *(undefined8 **)(lVar21 + 8) = puVar9;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar9,lVar5 + 0x30);
  uVar7 = *(undefined4 *)(lVar5 + 0xc);
  uVar18 = *(uint *)(lVar4 + 0x34);
  *(uint *)(lVar4 + 0x34) = uVar18 | 4;
  *(undefined4 *)(lVar4 + 0x18) = uVar7;
  uVar7 = *(undefined4 *)(lVar5 + 0x114);
  *(uint *)(lVar4 + 0x34) = uVar18 | 0xc;
  *(undefined4 *)(lVar4 + 0x1c) = uVar7;
  FUN_030f2168(&local_370,*param_3);
  uVar7 = FUN_00033fcc(&local_370);
  *(uint *)(lVar4 + 0x34) = *(uint *)(lVar4 + 0x34) | 0x10;
  *(undefined4 *)(lVar4 + 0x28) = uVar7;
  if ((long)local_360 < 0) {
    __ZdlPvm(local_370,local_360 & 0x7fffffffffffffff);
    cVar13 = *(char *)(lVar5 + 0x177);
    if (-1 < cVar13) goto LAB_030bdc24;
LAB_030bdc44:
    if (*(long *)(lVar5 + 0x168) != 0) {
LAB_030bdc4c:
      *(uint *)(lVar4 + 0x34) = *(uint *)(lVar4 + 0x34) | 0x20;
      puVar9 = *(undefined8 **)(lVar4 + 0x20);
      if (puVar9 == &DAT_0a524ad0) {
        puVar9 = (undefined8 *)__Znwm(0x18);
        *puVar9 = 0;
        puVar9[1] = 0;
        puVar9[2] = 0;
        *(undefined8 **)(lVar4 + 0x20) = puVar9;
      }
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar9,lVar5 + 0x160)
      ;
    }
  }
  else {
    cVar13 = *(char *)(lVar5 + 0x177);
    if (cVar13 < '\0') goto LAB_030bdc44;
LAB_030bdc24:
    if (cVar13 != '\0') goto LAB_030bdc4c;
  }
  puStack_2c8 = &SUB_aaaaaaaaaaaaaaaa;
  local_2d0 = &SUB_aaaaaaaaaaaaaaaa;
  local_2b8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_2c0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_2d8 = &SUB_aaaaaaaaaaaaaaaa;
  local_2e0 = &SUB_aaaaaaaaaaaaaaaa;
  plVar10 = (long *)FUN_04669774();
  uVar11 = (**(code **)(*plVar10 + 0x18))();
  local_c8 = (undefined8 *)((ulong)local_c8 & 0xffffffffffffff);
  local_d8 = (undefined8 *******)((ulong)local_d8 & 0xffffffffffffff00);
  local_370 = DAT_0875d510;
  uStack_34c = 0;
  local_360 = 0;
  local_358 = 0;
  local_368 = 0;
  local_350 = local_350 & 0xffffff00;
  FUN_030bee20(&local_2e0,uVar11,&local_2b0,&local_d8,&local_370);
  if ((long)local_358 < 0) {
    __ZdlPvm(local_368,local_358 & 0x7fffffffffffffff);
  }
  if (((int)local_2e0 == 0 && local_2e0._4_4_ == 0) && (*(int *)(local_2c0 + 0x28) != 0)) {
    lVar4 = **(long **)(local_2c0 + 0x10);
    if (*(int *)(lVar4 + 0x10) == 0) {
      *(undefined4 *)(lVar5 + 0x118) = 2;
      *(undefined8 *)(lVar5 + 0xf8) = *(undefined8 *)(lVar4 + 0x28);
      iVar6 = thunk_FUN_05e1d97c(2);
      if (iVar6 != 0) {
        FUN_0488143c(local_388);
        pppppppuVar12 = local_388[0];
        if (-1 < cStack_371) {
          pppppppuVar12 = local_388;
        }
        if ((DAT_0a3d86c9 & 1) == 0) {
          uVar8 = 0;
          do {
            (&DAT_0a3d86ad)[uVar8] = (&DAT_088ad3fc)[uVar8] + 0x8a ^ (&DAT_088ad3ec)[uVar8 & 0xf];
            uVar8 = uVar8 + 1;
          } while (uVar8 != 0x1c);
          DAT_0a3d86c9 = 1;
        }
        if ((DAT_0a3d8740 & 1) == 0) {
          _DAT_0a3d8724 = CONCAT44((int)DAT_088a7260,(int)DAT_087e2f50);
          uRam000000000a3d872c = CONCAT44((int)DAT_08485e90,(int)DAT_084a8110);
          DAT_0a3d8734 = CONCAT44((int)DAT_0863e0f0,(int)DAT_088a7268);
          DAT_0a3d873c = (undefined4)DAT_0847fdb8;
          DAT_0a3d8740 = 1;
        }
        FUN_05e1d050(&local_370,2,pppppppuVar12,&DAT_0a3d86ad,&DAT_0a3d8724,0x6a,0,0);
        lVar5 = local_278;
        FUN_04cbe440(local_3a0,local_278);
        local_128 = local_3a0[0];
        if (-1 < cStack_389) {
          local_128 = local_3a0;
        }
        local_120 = 0;
        uVar8 = *(ulong *)(lVar4 + 0x28);
        local_178 = (undefined1 *)0x0;
        if ((DAT_0a3d8966 & 1) == 0) {
          uVar19 = 0;
          do {
            (&DAT_0a3d891e)[uVar19] = (&DAT_088ad8be)[uVar19] + 0x8a ^ (&DAT_088ad8ae)[uVar19 & 0xf]
            ;
            uVar19 = uVar19 + 1;
          } while (uVar19 != 0x48);
          DAT_0a3d8966 = 1;
        }
        lVar21 = 0;
        do {
          lVar17 = lVar21;
          local_170[lVar17] = *(undefined1 *)(uVar8 % 10 + 0xa3d8941);
          bVar3 = 9 < uVar8;
          uVar8 = uVar8 / 10;
          lVar21 = lVar17 + 1;
        } while (bVar3);
        local_170[lVar17 + 1] = 0;
        if (8 < lVar17 + 8U) {
          puVar14 = local_170;
          puVar15 = local_170 + lVar17;
          do {
            puVar14 = puVar14 + 1;
            uVar1 = *puVar15;
            puVar16 = puVar15 + -1;
            *puVar15 = puVar14[-1];
            puVar14[-1] = uVar1;
            puVar15 = puVar16;
          } while (puVar14 < puVar16);
        }
        local_178 = local_170;
        local_1c8 = (undefined8 *******)0x0;
        lVar21 = 0;
        uVar8 = (ulong)*(uint *)(lVar5 + 0x114);
        do {
          lVar17 = lVar21;
          uVar18 = (uint)uVar8;
          *(undefined1 *)((long)&local_1c0 + lVar17) =
               (&DAT_0a3d891e)[uVar18 + (int)(uVar8 / 10) * -10 + 0x23];
          lVar21 = lVar17 + 1;
          uVar8 = uVar8 / 10;
        } while (9 < uVar18);
        *(undefined1 *)((long)&local_1c0 + lVar17 + 1) = 0;
        if (8 < lVar17 + 8U) {
          puVar14 = (undefined1 *)((long)&local_1c0 + lVar17);
          puVar15 = (undefined1 *)((long)&local_1c0 + 1);
          do {
            uVar1 = *puVar14;
            *puVar14 = puVar15[-1];
            puVar15[-1] = uVar1;
            bVar3 = puVar15 < puVar14 + -1;
            puVar14 = puVar14 + -1;
            puVar15 = puVar15 + 1;
          } while (bVar3);
        }
        local_1c8 = (undefined8 *******)&local_1c0;
        local_218 = (undefined8 *******)0x0;
        lVar21 = 0;
        uVar8 = (ulong)*(uint *)(lVar4 + 0x1c);
        do {
          lVar17 = lVar21;
          uVar18 = (uint)uVar8;
          *(undefined1 *)((long)&local_210 + lVar17) =
               (&DAT_0a3d891e)[uVar18 + (int)(uVar8 / 10) * -10 + 0x23];
          lVar21 = lVar17 + 1;
          uVar8 = uVar8 / 10;
        } while (9 < uVar18);
        *(undefined1 *)((long)&local_210 + lVar17 + 1) = 0;
        if (8 < lVar17 + 8U) {
          puVar14 = (undefined1 *)((long)&local_210 + lVar17);
          puVar15 = (undefined1 *)((long)&local_210 + 1);
          do {
            uVar1 = *puVar14;
            *puVar14 = puVar15[-1];
            puVar15[-1] = uVar1;
            bVar3 = puVar15 < puVar14 + -1;
            puVar14 = puVar14 + -1;
            puVar15 = puVar15 + 1;
          } while (bVar3);
        }
        local_218 = (undefined8 *******)&local_210;
        local_268 = (undefined8 *******)&local_260;
        lVar21 = 0;
        uVar8 = (ulong)*(uint *)(lVar4 + 0x20);
        do {
          lVar4 = lVar21;
          uVar18 = (uint)uVar8;
          *(undefined1 *)((long)&local_260 + lVar4) =
               (&DAT_0a3d891e)[uVar18 + (int)(uVar8 / 10) * -10 + 0x23];
          lVar21 = lVar4 + 1;
          uVar8 = uVar8 / 10;
        } while (9 < uVar18);
        *(undefined1 *)((long)&local_260 + lVar4 + 1) = 0;
        if (8 < lVar4 + 8U) {
          puVar14 = (undefined1 *)((long)&local_260 + lVar4);
          puVar15 = (undefined1 *)((long)&local_260 + 1);
          do {
            uVar1 = *puVar14;
            *puVar14 = puVar15[-1];
            puVar15[-1] = uVar1;
            bVar3 = puVar15 < puVar14 + -1;
            puVar14 = puVar14 + -1;
            puVar15 = puVar15 + 1;
          } while (bVar3);
        }
        if ((DAT_0a3d87a7 & 1) == 0) {
          uVar8 = 0;
          do {
            (&DAT_0a3d8741)[uVar8] = (&DAT_088ad4e4)[uVar8] + 0x8a ^ (&DAT_088ad4d4)[uVar8 & 0xf];
            uVar8 = uVar8 + 1;
          } while (uVar8 != 0x66);
          DAT_0a3d87a7 = 1;
        }
        local_d8 = &local_128;
        puStack_d0 = &local_178;
        local_c8 = &local_1c8;
        pppppppuStack_c0 = &local_218;
        local_b8 = &local_268;
        local_a8 = 0;
        uStack_b0 = 0;
        local_98 = 0;
        uStack_a0 = 0;
        local_88 = 0;
        uStack_90 = 0;
        local_78 = 0;
        uStack_80 = 0;
        local_68 = 0;
        uStack_70 = 0;
        uStack_60 = 0;
        FUN_05e1d31c(&local_370,&DAT_0a3d8741,&local_d8);
        if (cStack_389 < '\0') {
          __ZdlPvm(local_3a0[0],CONCAT17(cStack_389,local_390) & 0x7fffffffffffffff);
        }
        thunk_FUN_05e1d0bc(&local_370);
        if (cStack_371 < '\0') {
          uVar8 = CONCAT17(cStack_371,local_378);
          pppppppuVar12 = local_388[0];
          goto LAB_030be5c8;
        }
      }
    }
    else {
      iVar6 = thunk_FUN_05e1d97c(4);
      if (iVar6 != 0) {
        FUN_0488143c(&local_1c8);
        pppppppuVar12 = local_1c8;
        if (-1 < cStack_1b1) {
          pppppppuVar12 = (undefined8 *******)&local_1c8;
        }
        if ((DAT_0a3d86c9 & 1) == 0) {
          uVar8 = 0;
          do {
            (&DAT_0a3d86ad)[uVar8] = (&DAT_088ad3fc)[uVar8] + 0x8a ^ (&DAT_088ad3ec)[uVar8 & 0xf];
            uVar8 = uVar8 + 1;
          } while (uVar8 != 0x1c);
          DAT_0a3d86c9 = 1;
        }
        if ((DAT_0a3d8740 & 1) == 0) {
          _DAT_0a3d8724 = CONCAT44((int)DAT_088a7260,(int)DAT_087e2f50);
          uRam000000000a3d872c = CONCAT44((int)DAT_08485e90,(int)DAT_084a8110);
          DAT_0a3d8734 = CONCAT44((int)DAT_0863e0f0,(int)DAT_088a7268);
          DAT_0a3d873c = (undefined4)DAT_0847fdb8;
          DAT_0a3d8740 = 1;
        }
        FUN_05e1d050(&local_370,4,pppppppuVar12,&DAT_0a3d86ad,&DAT_0a3d8724,0x6c,0,0);
        lVar5 = local_278;
        FUN_04cbe440(&local_218,local_278);
        local_128 = local_218;
        if (-1 < cStack_201) {
          local_128 = &local_218;
        }
        local_120 = 0;
        iVar6 = *(int *)(lVar4 + 0x10);
        local_178 = (undefined1 *)0x0;
        if ((DAT_0a3d8966 & 1) == 0) {
          uVar8 = 0;
          do {
            (&DAT_0a3d891e)[uVar8] = (&DAT_088ad8be)[uVar8] + 0x8a ^ (&DAT_088ad8ae)[uVar8 & 0xf];
            uVar8 = uVar8 + 1;
          } while (uVar8 != 0x48);
          DAT_0a3d8966 = 1;
        }
        lVar4 = 8;
        iVar20 = iVar6;
        do {
          lVar21 = lVar4;
          local_170[lVar21 + -8] = (&DAT_0a3d891e)[iVar20 % 10 + 0x23];
          lVar4 = lVar21 + 1;
          uVar18 = iVar20 + 9;
          iVar20 = iVar20 / 10;
        } while (0x12 < uVar18);
        if (iVar6 < 0) {
          local_170[lVar21 + -7] = 0x2d;
          lVar4 = lVar21 + 2;
        }
        local_170[lVar4 + -8] = 0;
        if (9 < lVar4) {
          puVar14 = local_170;
          puVar15 = &uStack_179 + lVar4;
          do {
            puVar14 = puVar14 + 1;
            uVar1 = *puVar15;
            puVar16 = puVar15 + -1;
            *puVar15 = puVar14[-1];
            puVar14[-1] = uVar1;
            puVar15 = puVar16;
          } while (puVar14 < puVar16);
        }
        if ((DAT_0a3d87d5 & 1) == 0) {
          uVar8 = 0;
          do {
            (&DAT_0a3d87a8)[uVar8] = (&DAT_088ad55a)[uVar8] + 0x8a ^ (&DAT_088ad54a)[uVar8 & 0xf];
            uVar8 = uVar8 + 1;
          } while (uVar8 != 0x2d);
          DAT_0a3d87d5 = 1;
        }
        local_d8 = &local_128;
        puStack_d0 = &local_178;
        pppppppuStack_c0 = (undefined8 *******)0x0;
        local_c8 = (undefined8 *)0x0;
        uStack_b0 = 0;
        local_b8 = (undefined8 *******)0x0;
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
        local_178 = local_170;
        FUN_05e1d31c(&local_370,&DAT_0a3d87a8,&local_d8);
        if (cStack_201 < '\0') {
          __ZdlPvm(local_218,CONCAT17(cStack_201,local_208) & 0x7fffffffffffffff);
        }
        thunk_FUN_05e1d0bc(&local_370);
        if (cStack_1b1 < '\0') {
          uVar8 = CONCAT17(cStack_1b1,local_1b8);
          pppppppuVar12 = local_1c8;
LAB_030be5c8:
          __ZdlPvm(pppppppuVar12,uVar8 & 0x7fffffffffffffff);
        }
      }
    }
  }
  *param_1 = (long)local_2e0;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 1,(ulong)&local_2e0 | 8);
  local_3b0 = lVar5;
  if (*(int *)(lVar5 + 0x118) != 2) {
    *(undefined4 *)(lVar5 + 0x118) = 5;
    iVar6 = thunk_FUN_05e1d97c(4);
    if (iVar6 != 0) {
      FUN_0488143c(&local_268);
      pppppppuVar12 = local_268;
      if (-1 < cStack_251) {
        pppppppuVar12 = &local_268;
      }
      if ((DAT_0a3d86c9 & 1) == 0) {
        uVar8 = 0;
        do {
          (&DAT_0a3d86ad)[uVar8] = (&DAT_088ad3fc)[uVar8] + 0x8a ^ (&DAT_088ad3ec)[uVar8 & 0xf];
          uVar8 = uVar8 + 1;
        } while (uVar8 != 0x1c);
        DAT_0a3d86c9 = 1;
      }
      if ((DAT_0a3d8740 & 1) == 0) {
        _DAT_0a3d8724 = CONCAT44((int)DAT_088a7260,(int)DAT_087e2f50);
        uRam000000000a3d872c = CONCAT44((int)DAT_08485e90,(int)DAT_084a8110);
        DAT_0a3d8734 = CONCAT44((int)DAT_0863e0f0,(int)DAT_088a7268);
        DAT_0a3d873c = (undefined4)DAT_0847fdb8;
        DAT_0a3d8740 = 1;
      }
      FUN_05e1d050(&local_370,4,pppppppuVar12,&DAT_0a3d86ad,&DAT_0a3d8724,0x77,0,0);
      FUN_04cbe440(local_388,local_278);
      local_128 = local_388[0];
      if (-1 < cStack_371) {
        local_128 = local_388;
      }
      local_120 = 0;
      local_178 = (undefined1 *)0x0;
      if ((DAT_0a3d8966 & 1) == 0) {
        uVar8 = 0;
        do {
          (&DAT_0a3d891e)[uVar8] = (&DAT_088ad8be)[uVar8] + 0x8a ^ (&DAT_088ad8ae)[uVar8 & 0xf];
          uVar8 = uVar8 + 1;
        } while (uVar8 != 0x48);
        DAT_0a3d8966 = 1;
      }
      lVar5 = 8;
      iVar6 = (int)local_2e0;
      do {
        lVar4 = lVar5;
        local_170[lVar4 + -8] = (&DAT_0a3d891e)[iVar6 % 10 + 0x23];
        lVar5 = lVar4 + 1;
        uVar18 = iVar6 + 9;
        iVar6 = iVar6 / 10;
      } while (0x12 < uVar18);
      if ((int)local_2e0 < 0) {
        local_170[lVar4 + -7] = 0x2d;
        lVar5 = lVar4 + 2;
      }
      local_170[lVar5 + -8] = 0;
      if (9 < lVar5) {
        puVar14 = local_170;
        puVar15 = &uStack_179 + lVar5;
        do {
          puVar14 = puVar14 + 1;
          uVar1 = *puVar15;
          puVar16 = puVar15 + -1;
          *puVar15 = puVar14[-1];
          puVar14[-1] = uVar1;
          puVar15 = puVar16;
        } while (puVar14 < puVar16);
      }
      local_178 = local_170;
      local_1c8 = (undefined8 *******)0x0;
      lVar5 = 8;
      iVar6 = local_2e0._4_4_;
      do {
        lVar4 = lVar5;
        *(undefined1 *)((long)&local_1c8 + lVar4) = (&DAT_0a3d891e)[iVar6 % 10 + 0x23];
        lVar5 = lVar4 + 1;
        uVar18 = iVar6 + 9;
        iVar6 = iVar6 / 10;
      } while (0x12 < uVar18);
      if ((long)local_2e0 < 0) {
        *(undefined1 *)((long)&local_1c8 + lVar4 + 1) = 0x2d;
        lVar5 = lVar4 + 2;
      }
      *(undefined1 *)((long)&local_1c8 + lVar5) = 0;
      if (9 < lVar5) {
        puVar14 = &uStack_1c9 + lVar5;
        puVar15 = (undefined1 *)((long)&local_1c0 + 1);
        do {
          uVar1 = *puVar14;
          *puVar14 = puVar15[-1];
          puVar15[-1] = uVar1;
          bVar3 = puVar15 < puVar14 + -1;
          puVar14 = puVar14 + -1;
          puVar15 = puVar15 + 1;
        } while (bVar3);
      }
      local_1c8 = (undefined8 *******)&local_1c0;
      local_218 = (undefined8 *******)0x0;
      local_218 = (undefined8 *******)&local_210;
      lVar5 = 0;
      uVar8 = (ulong)*(uint *)(local_2c0 + 0x28);
      do {
        lVar4 = lVar5;
        uVar18 = (uint)uVar8;
        *(undefined1 *)((long)&local_210 + lVar4) =
             (&DAT_0a3d891e)[uVar18 + (int)(uVar8 / 10) * -10 + 0x23];
        lVar5 = lVar4 + 1;
        uVar8 = uVar8 / 10;
      } while (9 < uVar18);
      *(undefined1 *)((long)&local_210 + lVar4 + 1) = 0;
      if (8 < lVar4 + 8U) {
        puVar14 = (undefined1 *)((long)&local_210 + lVar4);
        puVar15 = (undefined1 *)((long)&local_210 + 1);
        do {
          uVar1 = *puVar14;
          *puVar14 = puVar15[-1];
          puVar15[-1] = uVar1;
          bVar3 = puVar15 < puVar14 + -1;
          puVar14 = puVar14 + -1;
          puVar15 = puVar15 + 1;
        } while (bVar3);
      }
      if ((DAT_0a3d8823 & 1) == 0) {
        uVar8 = 0;
        do {
          (&DAT_0a3d87d6)[uVar8] = (&DAT_088ad597)[uVar8] + 0x8a ^ (&DAT_088ad587)[uVar8 & 0xf];
          uVar8 = uVar8 + 1;
        } while (uVar8 != 0x4d);
        DAT_0a3d8823 = 1;
      }
      local_d8 = &local_128;
      puStack_d0 = &local_178;
      local_c8 = &local_1c8;
      pppppppuStack_c0 = &local_218;
      uStack_b0 = 0;
      local_b8 = (undefined8 *******)0x0;
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
      FUN_05e1d31c(&local_370,&DAT_0a3d87d6,&local_d8);
      if (cStack_371 < '\0') {
        __ZdlPvm(local_388[0],CONCAT17(cStack_371,local_378) & 0x7fffffffffffffff);
      }
      thunk_FUN_05e1d0bc(&local_370);
      if (cStack_251 < '\0') {
        __ZdlPvm(local_268,CONCAT17(cStack_251,local_258) & 0x7fffffffffffffff);
      }
    }
    FUN_030f6650(&local_370,3,0xc,(int)*param_1,*(undefined4 *)((long)param_1 + 4));
    *param_1 = local_370;
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_1 + 1,&local_368)
    ;
    if (local_348 != (long *)0x0) {
      local_348[1] = local_348[1] + 1;
    }
    plVar10 = (long *)param_1[5];
    param_1[4] = CONCAT44(uStack_34c,local_350);
    param_1[5] = (long)local_348;
    if (plVar10 != (long *)0x0) {
      LOAcquire();
      lVar5 = plVar10[1];
      plVar10[1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*plVar10 + 0x10))(plVar10);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
      }
    }
    if (local_348 != (long *)0x0) {
      LOAcquire();
      lVar5 = *(long *)((long)local_348 + 8U);
      *(long *)((long)local_348 + 8U) = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*local_348 + 0x10))(local_348);
        __ZNSt3__119__shared_weak_count14__release_weakEv(local_348);
      }
    }
    local_3b0 = local_278;
    if ((long)local_358 < 0) {
      __ZdlPvm(local_368,local_358 & 0x7fffffffffffffff);
      local_3b0 = local_278;
    }
  }
  local_3a8 = local_270;
  lVar5 = 0;
  if (local_270 != (long *)0x0) {
    lVar5 = local_270[1];
    local_270[1] = lVar5 + 1;
  }
  FUN_030daf78(lVar5,param_2,&local_3b0,1,1);
  plVar2 = local_3a8;
  plVar10 = local_2b8;
  if (local_3a8 != (long *)0x0) {
    LOAcquire();
    lVar5 = local_3a8[1];
    local_3a8[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*local_3a8 + 0x10))(local_3a8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
      plVar10 = local_2b8;
    }
  }
  local_2b8 = plVar10;
  if (plVar10 != (long *)0x0) {
    LOAcquire();
    lVar5 = *(long *)((long)plVar10 + 8U);
    *(long *)((long)plVar10 + 8U) = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*plVar10 + 0x10))(plVar10);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
    }
  }
  if ((long)puStack_2c8 < 0) {
    __ZdlPvm(puStack_2d8,(ulong)puStack_2c8 & 0x7fffffffffffffff);
  }
  FUN_0465d634(&local_2b0);
LAB_030beb50:
  plVar10 = local_270;
  if (local_270 != (long *)0x0) {
    LOAcquire();
    lVar5 = local_270[1];
    local_270[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*local_270 + 0x10))(local_270);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_58) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


