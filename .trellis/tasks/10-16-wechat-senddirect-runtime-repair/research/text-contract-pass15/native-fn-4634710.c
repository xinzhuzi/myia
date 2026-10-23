// Ghidra inferred pseudocode; requested=0x4634710
// entry=04634710 end=04635077

/* WARNING: Type propagation algorithm not settling */

void FUN_04634710(long param_1,long *param_2)

{
  undefined8 *******pppppppuVar1;
  undefined1 uVar2;
  undefined1 **ppuVar3;
  bool bVar4;
  int iVar5;
  undefined8 uVar6;
  long *plVar7;
  undefined1 *puVar8;
  undefined8 *puVar9;
  ulong uVar10;
  uint uVar11;
  undefined8 *puVar12;
  undefined1 *puVar13;
  long lVar14;
  long lVar15;
  undefined8 *puVar16;
  undefined1 *local_420;
  undefined1 *puStack_418;
  undefined8 local_410;
  undefined8 uStack_408;
  undefined1 *local_400;
  undefined8 *******local_3f8;
  undefined1 *local_3f0;
  undefined8 uStack_3e8;
  undefined1 *puStack_3e0;
  undefined1 *local_3d8;
  undefined1 *local_390;
  undefined1 *local_388;
  undefined8 local_380;
  undefined8 *******local_378;
  undefined8 uStack_370;
  ulong local_368;
  undefined4 local_360;
  undefined1 local_359;
  undefined1 *local_358;
  undefined4 local_34c;
  uint local_348;
  undefined4 local_344;
  undefined4 local_338;
  undefined1 auStack_330 [25];
  undefined1 local_317;
  undefined2 local_316;
  uint local_308;
  byte local_2fc;
  undefined4 local_2f8;
  ulong local_2e8;
  undefined1 local_188;
  undefined1 auStack_180 [80];
  undefined8 *local_130;
  undefined8 local_128;
  ulong local_120;
  undefined8 **local_e0;
  undefined1 *puStack_d8;
  undefined8 *local_d0;
  undefined1 *local_c8;
  undefined8 *puStack_c0;
  undefined8 uStack_b8;
  undefined1 *puStack_b0;
  undefined1 *local_a8;
  undefined1 *puStack_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  undefined8 local_78;
  undefined8 uStack_70;
  undefined8 local_68;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  if ((*(byte *)(param_1 + 0x18) & 1) == 0) goto LAB_04634fb8;
  __ZNSt3__15mutex4lockEv(param_1 + 0x80);
  _memset(&local_348,0xaa,0x218);
  FUN_05daa3b0(&local_348);
  local_344 = *(undefined4 *)((long)param_2 + 0xc);
  local_338 = (undefined4)param_2[2];
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(auStack_330,param_2 + 3);
  local_317 = *(undefined1 *)((long)param_2 + 0x31);
  local_316 = *(undefined2 *)((long)param_2 + 0x32);
  uVar6 = FUN_04669774();
  local_308 = FUN_04671ac0(uVar6,*(undefined4 *)((long)param_2 + 0xc));
  local_308 = local_308 ^ 1;
  local_2fc = *(byte *)(param_2 + 0xe);
  if ((local_2fc & 1) != 0) {
    local_2f8 = *(undefined4 *)((long)param_2 + 0x74);
  }
  local_2e8 = (ulong)*(uint *)((long)param_2 + 0xc);
  local_34c = 0;
  local_358 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_04659d5c(&local_358);
  local_359 = 0;
  local_360 = 0;
  (**(code **)(*param_2 + 0x10))(param_2,&local_358,&local_34c,&local_359,&local_360);
  puStack_a0 = &SUB_aaaaaaaaaaaaaaaa;
  uStack_b8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_c0 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
  local_a8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_b0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_d8 = &SUB_aaaaaaaaaaaaaaaa;
  local_e0 = (undefined8 **)&SUB_aaaaaaaaaaaaaaaa;
  local_c8 = &SUB_aaaaaaaaaaaaaaaa;
  local_d0 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_05563108(&local_e0);
  plVar7 = (long *)FUN_04669774();
  puStack_d8 = (undefined1 *)(**(code **)(*plVar7 + 0x20))();
  puStack_a0 = (undefined1 *)((ulong)puStack_a0 | 0x100000000);
  uVar6 = FUN_04659fc8(&local_358);
  iVar5 = FUN_04659fbc(&local_358);
  puStack_a0 = (undefined1 *)((ulong)puStack_a0 | 0x200000000);
  if (local_d0 == &DAT_0a524ad0) {
    local_d0 = (undefined8 *)__Znwm(0x18);
    *local_d0 = 0;
    local_d0[1] = 0;
    local_d0[2] = 0;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKcm
            (local_d0,uVar6,(long)iVar5);
  local_c8 = (undefined1 *)((ulong)local_c8 & 0xffffffff00000000);
  puStack_a0 = (undefined1 *)((ulong)puStack_a0 | 0xc00000000);
  uStack_b8 = (undefined1 *)((ulong)uStack_b8 & 0xffffffffffffff00);
  FUN_04669774();
  FUN_04670788(&local_420);
  if ((long)local_410 < 0) {
    __ZdlPvm(local_420,(ulong)local_410 & 0x7fffffffffffffff);
    if (puStack_418 == (undefined1 *)0x0) goto LAB_046348e0;
  }
  else if (local_410._7_1_ == '\0') {
LAB_046348e0:
    plVar7 = param_2 + 7;
    lVar15 = (long)*(char *)((long)param_2 + 0x4f);
    if (lVar15 < 0) {
      lVar15 = param_2[8];
      if (lVar15 != 0) {
        plVar7 = (long *)*plVar7;
        goto LAB_04634900;
      }
    }
    else if (*(char *)((long)param_2 + 0x4f) != '\0') {
LAB_04634900:
      puStack_a0 = (undefined1 *)((ulong)puStack_a0 | 0x4000000000);
      if (puStack_c0 == &DAT_0a524ad0) {
        puStack_c0 = (undefined8 *)__Znwm(0x18);
        *puStack_c0 = 0;
        puStack_c0[1] = 0;
        puStack_c0[2] = 0;
      }
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKcm
                (puStack_c0,plVar7,lVar15);
    }
  }
  iVar5 = FUN_046351f0(*(undefined4 *)((long)param_2 + 0xc));
  if (iVar5 == 0) {
    uVar6 = FUN_04669774();
    iVar5 = FUN_04671ac0(uVar6,*(undefined4 *)((long)param_2 + 0xc));
    if (iVar5 != 0) {
      puStack_a0 = (undefined1 *)((ulong)puStack_a0 | 0x10000000000);
      uStack_b8._0_4_ = CONCAT13(1,(undefined3)uStack_b8);
      uStack_3e8 = &SUB_aaaaaaaaaaaaaaaa;
      local_3f0 = &SUB_aaaaaaaaaaaaaaaa;
      local_3d8 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_3e0 = &SUB_aaaaaaaaaaaaaaaa;
      uStack_408 = &SUB_aaaaaaaaaaaaaaaa;
      local_410 = &SUB_aaaaaaaaaaaaaaaa;
      local_3f8 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
      local_400 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_418 = &SUB_aaaaaaaaaaaaaaaa;
      local_420 = &SUB_aaaaaaaaaaaaaaaa;
      uVar6 = FUN_04669774();
      FUN_04671c58(&local_420,uVar6,*(undefined4 *)((long)param_2 + 0xc));
      puStack_a0 = (undefined1 *)((ulong)puStack_a0 | 0x40000000000);
      if (local_a8 == (undefined1 *)0x0) {
        puVar8 = (undefined1 *)__Znwm(0x28);
        FUN_055630e8();
        local_a8 = puVar8;
      }
      puVar8 = local_a8;
      *(undefined4 *)(local_a8 + 0x18) = local_420._0_4_;
      *(uint *)(local_a8 + 0x20) = *(uint *)(local_a8 + 0x20) | 3;
      puVar9 = *(undefined8 **)(local_a8 + 8);
      if (puVar9 == &DAT_0a524ad0) {
        puVar9 = (undefined8 *)__Znwm(0x18);
        *puVar9 = 0;
        puVar9[1] = 0;
        puVar9[2] = 0;
        *(undefined8 **)(puVar8 + 8) = puVar9;
      }
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar9,&local_400);
      *(uint *)(puVar8 + 0x20) = *(uint *)(puVar8 + 0x20) | 4;
      puVar9 = *(undefined8 **)(puVar8 + 0x10);
      if (puVar9 == &DAT_0a524ad0) {
        puVar9 = (undefined8 *)__Znwm(0x18);
        *puVar9 = 0;
        puVar9[1] = 0;
        puVar9[2] = 0;
        *(undefined8 **)(puVar8 + 0x10) = puVar9;
      }
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (puVar9,(ulong)&local_420 | 8);
      if ((long)local_3d8 < 0) {
        __ZdlPvm(uStack_3e8,(ulong)local_3d8 & 0x7fffffffffffffff);
      }
      if ((long)local_3f0 < 0) {
        __ZdlPvm(local_400,(ulong)local_3f0 & 0x7fffffffffffffff);
      }
      if ((long)uStack_408 < 0) {
        __ZdlPvm(puStack_418,(ulong)uStack_408 & 0x7fffffffffffffff);
      }
    }
  }
  else {
    puStack_a0 = (undefined1 *)((ulong)puStack_a0 | 0x8000000000);
    uStack_b8._0_3_ = CONCAT12(1,(undefined2)uStack_b8);
    local_3f8 = (undefined8 *******)0x0;
    local_3f0 = (undefined1 *)0x0;
    uStack_3e8 = (undefined1 *)0x0;
    puStack_418 = (undefined1 *)0x0;
    local_420 = (undefined1 *)0x0;
    uStack_408 = (undefined1 *)0x0;
    local_410 = (undefined1 *)0x0;
    local_400 = &DAT_aaaaaaaa00000000;
    FUN_0461ae78(&local_420);
    puStack_a0 = (undefined1 *)((ulong)puStack_a0 | 0x20000000000);
    if (puStack_b0 == (undefined1 *)0x0) {
      puVar8 = (undefined1 *)__Znwm(0x30);
      FUN_055630bc();
      puStack_b0 = puVar8;
    }
    puVar13 = puStack_b0;
    *(uint *)(puStack_b0 + 0x2c) = *(uint *)(puStack_b0 + 0x2c) | 3;
    *(undefined1 **)(puStack_b0 + 8) = local_420;
    puVar8 = puStack_418;
    if (-1 < (long)uStack_408._7_1_) {
      puVar8 = (undefined1 *)((ulong)&local_420 | 8);
    }
    local_128 = 0;
    local_130 = (undefined8 *)0x0;
    local_120 = 0;
    local_378 = (undefined8 *******)0x0;
    uStack_370 = 0;
    local_368 = 0;
    lVar15 = (long)local_410;
    if (-1 < (long)uStack_408) {
      lVar15 = (long)uStack_408._7_1_;
    }
    FUN_00020654(puVar8,lVar15,&local_130);
    pppppppuVar1 = local_3f8;
    if (-1 < (long)uStack_3e8._7_1_) {
      pppppppuVar1 = &local_3f8;
    }
    puVar8 = local_3f0;
    if (-1 < (long)uStack_3e8) {
      puVar8 = (undefined1 *)(long)uStack_3e8._7_1_;
    }
    FUN_00020654(pppppppuVar1,puVar8,&local_378);
    *(uint *)(puVar13 + 0x2c) = *(uint *)(puVar13 + 0x2c) | 4;
    puVar9 = *(undefined8 **)(puVar13 + 0x10);
    if (puVar9 == &DAT_0a524ad0) {
      puVar9 = (undefined8 *)__Znwm(0x18);
      *puVar9 = 0;
      puVar9[1] = 0;
      puVar9[2] = 0;
      *(undefined8 **)(puVar13 + 0x10) = puVar9;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar9,&local_130);
    *(uint *)(puVar13 + 0x2c) = *(uint *)(puVar13 + 0x2c) | 8;
    puVar9 = *(undefined8 **)(puVar13 + 0x18);
    if (puVar9 == &DAT_0a524ad0) {
      puVar9 = (undefined8 *)__Znwm(0x18);
      *puVar9 = 0;
      puVar9[1] = 0;
      puVar9[2] = 0;
      *(undefined8 **)(puVar13 + 0x18) = puVar9;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar9,&local_378);
    local_388 = &SUB_aaaaaaaaaaaaaaaa;
    local_380 = &SUB_aaaaaaaaaaaaaaaa;
    local_390 = &SUB_aaaaaaaaaaaaaaaa;
    FUN_04669774();
    FUN_04670d1c(&local_390);
    uVar11 = (uint)(char)local_380._7_1_;
    puVar8 = local_388;
    if (-1 < (int)uVar11) {
      puVar8 = (undefined1 *)(ulong)local_380._7_1_;
    }
    if (puVar8 != (undefined1 *)0x0) {
      *(uint *)(puVar13 + 0x2c) = *(uint *)(puVar13 + 0x2c) | 0x10;
      puVar9 = *(undefined8 **)(puVar13 + 0x20);
      if (puVar9 == &DAT_0a524ad0) {
        puVar9 = (undefined8 *)__Znwm(0x18);
        *puVar9 = 0;
        puVar9[1] = 0;
        puVar9[2] = 0;
        *(undefined8 **)(puVar13 + 0x20) = puVar9;
      }
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar9,&local_390);
      uVar11 = (uint)local_380._7_1_;
    }
    if ((uVar11 >> 7 & 1) != 0) {
      __ZdlPvm(local_390,(ulong)local_380 & 0x7fffffffffffffff);
    }
    if ((long)local_368 < 0) {
      __ZdlPvm(local_378,local_368 & 0x7fffffffffffffff);
    }
    if ((long)local_120 < 0) {
      __ZdlPvm(local_130,local_120 & 0x7fffffffffffffff);
    }
    FUN_00506b68(&local_420);
  }
  local_420 = (undefined1 *)0x0;
  puStack_418 = (undefined1 *)0x0;
  local_410 = (undefined1 *)0x0;
  FUN_05ab3f60(&local_e0,&local_420);
  puVar8 = puStack_418;
  ppuVar3 = (undefined1 **)local_420;
  if (-1 < (long)local_410) {
    puVar8 = (undefined1 *)((ulong)local_410 >> 0x38);
    ppuVar3 = &local_420;
  }
  FUN_05ded508(auStack_180,ppuVar3,puVar8);
  local_188 = 1;
  if ((long)local_410 < 0) {
    __ZdlPvm(local_420,(ulong)local_410 & 0x7fffffffffffffff);
  }
  FUN_05564928(&local_e0);
  FUN_04659ddc(&local_358);
  uVar10 = (*(code *)PTR_FUN_0a124b90)(&local_348);
  uVar11 = local_348;
  *(uint *)(param_2 + 1) = local_348;
  puVar9 = (undefined8 *)(param_1 + 0x70);
  puVar12 = (undefined8 *)*puVar9;
  while (puVar16 = puVar9, puVar12 != (undefined8 *)0x0) {
    while (puVar9 = puVar12, *(uint *)(puVar9 + 4) <= local_348) {
      if (local_348 <= *(uint *)(puVar9 + 4)) {
        puVar9[5] = param_2;
        goto joined_r0x04634d34;
      }
      puVar12 = (undefined8 *)puVar9[1];
      if ((undefined8 *)puVar9[1] == (undefined8 *)0x0) {
        puVar16 = puVar9 + 1;
        goto LAB_04634cd4;
      }
    }
    puVar12 = (undefined8 *)*puVar9;
  }
LAB_04634cd4:
  puVar12 = (undefined8 *)__Znwm(0x30);
  *(uint *)(puVar12 + 4) = uVar11;
  puVar12[5] = 0;
  *puVar12 = 0;
  puVar12[1] = 0;
  puVar12[2] = puVar9;
  *puVar16 = puVar12;
  puVar9 = puVar12;
  if (**(long **)(param_1 + 0x68) != 0) {
    *(long *)(param_1 + 0x68) = **(long **)(param_1 + 0x68);
    puVar9 = (undefined8 *)*puVar16;
  }
  FUN_0002413c(*(undefined8 *)(param_1 + 0x70),puVar9);
  *(long *)(param_1 + 0x78) = *(long *)(param_1 + 0x78) + 1;
  puVar12[5] = param_2;
joined_r0x04634d34:
  if (((uVar10 & 1) == 0) && (iVar5 = thunk_FUN_05e1d97c(4), iVar5 != 0)) {
    FUN_0488143c(&local_378);
    pppppppuVar1 = local_378;
    if (-1 < (long)local_368) {
      pppppppuVar1 = &local_378;
    }
    if ((DAT_0a45cea6 & 1) == 0) {
      uVar10 = 0;
      do {
        (&DAT_0a45ce91)[uVar10] = (&DAT_08a10f2b)[uVar10] + 0x8a ^ (&DAT_08a10f1b)[uVar10 & 0xf];
        uVar10 = uVar10 + 1;
      } while (uVar10 != 0x15);
      DAT_0a45cea6 = 1;
    }
    if ((DAT_0a45d292 & 1) == 0) {
      DAT_0a45d288._0_1_ = s__TaskGroStartTasp_Co_088a6270[8];
      DAT_0a45d288._1_1_ = s__TaskGroStartTasp_Co_088a6270[9];
      DAT_0a45d288._2_1_ = s__TaskGroStartTasp_Co_088a6270[10];
      DAT_0a45d288._3_1_ = s__TaskGroStartTasp_Co_088a6270[0xb];
      DAT_0a45d288._4_1_ = s__TaskGroStartTasp_Co_088a6270[0xc];
      DAT_0a45d288._5_1_ = s__TaskGroStartTasp_Co_088a6270[0xd];
      DAT_0a45d288._6_1_ = s__TaskGroStartTasp_Co_088a6270[0xe];
      DAT_0a45d288._7_1_ = s__TaskGroStartTasp_Co_088a6270[0xf];
      DAT_0a45d290 = 0x6b;
      DAT_0a45d292 = 1;
    }
    FUN_05e1d050(&local_420,4,pppppppuVar1,&DAT_0a45ce91,&DAT_0a45d288,0x253,0,0);
    local_130 = &local_128;
    if ((DAT_0a45d389 & 1) == 0) {
      uVar10 = 0;
      do {
        (&DAT_0a45d341)[uVar10] = (&DAT_08a116aa)[uVar10] + 0x8a ^ (&DAT_08a1169a)[uVar10 & 0xf];
        uVar10 = uVar10 + 1;
      } while (uVar10 != 0x48);
      DAT_0a45d389 = 1;
    }
    uVar10 = (ulong)local_348;
    lVar15 = 0;
    do {
      lVar14 = lVar15;
      uVar11 = (uint)uVar10;
      *(undefined1 *)((long)&local_128 + lVar14) =
           (&DAT_0a45d341)[uVar11 + (int)(uVar10 / 10) * -10 + 0x23];
      uVar10 = uVar10 / 10;
      lVar15 = lVar14 + 1;
    } while (9 < uVar11);
    *(undefined1 *)((long)&local_128 + lVar14 + 1) = 0;
    if (8 < lVar14 + 8U) {
      puVar8 = (undefined1 *)((long)&local_128 + lVar14);
      puVar13 = (undefined1 *)((long)&local_128 + 1);
      do {
        uVar2 = *puVar8;
        *puVar8 = puVar13[-1];
        puVar13[-1] = uVar2;
        bVar4 = puVar13 < puVar8 + -1;
        puVar8 = puVar8 + -1;
        puVar13 = puVar13 + 1;
      } while (bVar4);
    }
    if ((DAT_0a45d2aa & 1) == 0) {
      uVar10 = 0;
      do {
        (&DAT_0a45d293)[uVar10] = (&DAT_08a11591)[uVar10] + 0x8a ^ (&DAT_08a11581)[uVar10 & 0xf];
        uVar10 = uVar10 + 1;
      } while (uVar10 != 0x17);
      DAT_0a45d2aa = 1;
    }
    local_d0 = (undefined8 *)0x0;
    puStack_d8 = (undefined1 *)0x0;
    local_e0 = &local_130;
    puStack_c0 = (undefined8 *)0x0;
    local_c8 = (undefined1 *)0x0;
    puStack_b0 = (undefined1 *)0x0;
    uStack_b8 = (undefined1 *)0x0;
    puStack_a0 = (undefined1 *)0x0;
    local_a8 = (undefined1 *)0x0;
    uStack_90 = 0;
    local_98 = 0;
    uStack_80 = 0;
    local_88 = 0;
    uStack_70 = 0;
    local_78 = 0;
    local_68 = 0;
    FUN_05e1d31c(&local_420,&DAT_0a45d293,&local_e0);
    thunk_FUN_05e1d0bc(&local_420);
    if ((long)local_368 < 0) {
      __ZdlPvm(local_378,local_368 & 0x7fffffffffffffff);
    }
  }
  FUN_046364ec(&local_348);
  __ZNSt3__15mutex6unlockEv(param_1 + 0x80);
LAB_04634fb8:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


