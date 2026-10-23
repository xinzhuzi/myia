// Ghidra inferred pseudocode; requested=0x32961a4
// entry=032961a4 end=0329697f

/* WARNING: Type propagation algorithm not settling */

ulong FUN_032961a4(long param_1)

{
  undefined8 *******pppppppuVar1;
  undefined4 uVar2;
  undefined1 uVar3;
  undefined8 *puVar4;
  char *******pppppppcVar5;
  undefined1 *puVar6;
  int iVar7;
  long lVar8;
  ulong uVar9;
  long lVar10;
  ulong uVar11;
  undefined1 *puVar12;
  uint uVar13;
  undefined8 *puVar14;
  undefined8 *puVar15;
  undefined1 *puVar16;
  undefined8 *puVar17;
  undefined8 uVar18;
  long lVar19;
  char *******pppppppcVar20;
  char *******local_5c8 [2];
  undefined7 local_5b8;
  char cStack_5b1;
  undefined8 *******local_5b0 [2];
  undefined7 local_5a0;
  char cStack_599;
  undefined1 *local_598;
  undefined1 *local_590;
  undefined1 *local_588;
  undefined4 *local_580;
  undefined1 local_578;
  long local_530;
  undefined1 local_528;
  undefined1 *local_4e0;
  undefined1 local_4d8 [72];
  long local_490;
  undefined1 local_488;
  char ******local_440;
  undefined8 local_438;
  char ******local_3f0;
  undefined1 local_3e8;
  char *******local_3a0;
  undefined1 *local_398;
  undefined8 local_390;
  undefined **local_350;
  undefined8 *******local_348;
  undefined8 *******local_340;
  undefined8 local_338;
  char *******local_d8;
  char *******local_d0;
  char *******local_c8;
  long *plStack_c0;
  undefined1 **local_b8;
  long *plStack_b0;
  undefined4 **local_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 local_60;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar19 = *(long *)(param_1 + 0x28);
  lVar10 = *(long *)(param_1 + 8);
  local_350 = (undefined **)(lVar10 + 0x18);
  lVar8 = FUN_019a94a4(*(undefined8 *)(param_1 + 0x10),local_350,&DAT_08b7a8b8,&local_350,&local_d8)
  ;
  uVar2 = *(undefined4 *)(lVar8 + 0x28);
  *(uint *)(lVar10 + 0x204) = *(uint *)(lVar10 + 0x204) | 1;
  *(undefined4 *)(lVar10 + 0x198) = uVar2;
  lVar10 = *(long *)(param_1 + 8);
  local_350 = (undefined **)(lVar10 + 0x30);
  lVar8 = FUN_019a94a4(*(undefined8 *)(param_1 + 0x10),local_350,&DAT_08b7a8b8,&local_350,&local_d8)
  ;
  uVar2 = *(undefined4 *)(lVar8 + 0x28);
  *(uint *)(lVar10 + 0x204) = *(uint *)(lVar10 + 0x204) | 2;
  *(undefined4 *)(lVar10 + 0x19c) = uVar2;
  lVar10 = *(long *)(param_1 + 8);
  local_350 = (undefined **)(lVar10 + 0x48);
  lVar8 = FUN_019a94a4(*(undefined8 *)(param_1 + 0x10),local_350,&DAT_08b7a8b8,&local_350,&local_d8)
  ;
  *(undefined4 *)(lVar10 + 0x110) = *(undefined4 *)(lVar8 + 0x28);
  *(undefined1 *)(*(long *)(param_1 + 8) + 0x218) = **(undefined1 **)(param_1 + 0x18);
  FUN_04cbf820();
  FUN_04cbfb58(*(undefined8 *)(param_1 + 8));
  local_590 = &SUB_aaaaaaaaaaaaaaaa;
  local_588 = &SUB_aaaaaaaaaaaaaaaa;
  local_598 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_030251cc(&local_598,*(undefined8 *)(param_1 + 0x20));
  uVar18 = *(undefined8 *)(lVar19 + 8);
  local_d0 = (char *******)0x0;
  local_c8 = (char *******)0x0;
  local_d8 = (char *******)0x0;
  local_d0 = (char *******)FUN_02e86b60(&local_d8,*(undefined8 *)(param_1 + 8));
  local_390 = 0;
  local_3a0 = (char *******)0x983dbd0;
  local_398 = (undefined1 *)0x0;
  FUN_056c90b0(&local_350,&local_598);
  FUN_0562fe5c(&local_3a0,&local_350);
  FUN_0562fd84(&local_350);
  local_348 = &local_348;
  local_338 = 0;
  local_350 = &PTR_FUN_09f24930;
  local_340 = local_348;
  uVar9 = FUN_03296b1c(uVar18,&local_d8,&local_3a0,&local_350);
  FUN_056fa768(&local_350);
  FUN_0562fd84(&local_3a0);
  pppppppcVar5 = local_d8;
  pppppppcVar20 = local_d0;
  if (local_d8 != (char *******)0x0) {
    while (pppppppcVar20 != pppppppcVar5) {
      pppppppcVar20 = pppppppcVar20 + -0x4f;
      (*(code *)**pppppppcVar20)(pppppppcVar20);
    }
    local_d0 = pppppppcVar5;
    __ZdlPvm(local_d8,(long)local_c8 - (long)local_d8);
  }
  if ((uVar9 & 1) == 0) {
    lVar10 = *(long *)(param_1 + 8);
  }
  else {
    lVar10 = *(long *)(param_1 + 8);
    if (**(char **)(param_1 + 0x18) == '\x01') {
      *(int *)(lVar10 + 0xf4) = (int)**(undefined8 **)(lVar10 + 0x208);
    }
  }
  uVar18 = *(undefined8 *)(param_1 + 0x20);
  FUN_00f57630(&local_350,lVar10);
  local_d8 = (char *******)0x0;
  local_d0 = (char *******)0x0;
  local_c8 = (char *******)0x0;
  local_3a0 = (char *******)&local_d8;
  local_398 = &DAT_aaaaaaaaaaaaaa00;
  local_d8 = (char *******)__Znwm(0x278);
  pppppppcVar20 = local_d8 + 0x4f;
  local_d0 = local_d8;
  local_c8 = pppppppcVar20;
  FUN_00f57630(local_d8,&local_350);
  local_d0 = pppppppcVar20;
  FUN_03263cd4(lVar19,uVar18,&local_d8);
  pppppppcVar5 = local_d8;
  pppppppcVar20 = local_d0;
  if (local_d8 != (char *******)0x0) {
    while (pppppppcVar20 != pppppppcVar5) {
      pppppppcVar20 = pppppppcVar20 + -0x4f;
      (*(code *)**pppppppcVar20)(pppppppcVar20);
    }
    local_d0 = pppppppcVar5;
    __ZdlPvm(local_d8,(long)local_c8 - (long)local_d8);
  }
  FUN_00ac6290(&local_350);
  iVar7 = thunk_FUN_05e1d97c(2);
  if (iVar7 == 0) goto joined_r0x03296914;
  FUN_0488143c(local_5b0);
  pppppppuVar1 = local_5b0[0];
  if (-1 < cStack_599) {
    pppppppuVar1 = local_5b0;
  }
  if ((DAT_0a3e46b7 & 1) == 0) {
    uVar11 = 0;
    do {
      (&DAT_0a3e46a4)[uVar11] = (&DAT_088ca7e4)[uVar11] + 0x8a ^ (&DAT_088ca7d4)[uVar11 & 0xf];
      uVar11 = uVar11 + 1;
    } while (uVar11 != 0x13);
    DAT_0a3e46b7 = 1;
  }
  if ((DAT_0a3e63c3 & 1) == 0) {
    DAT_0a3e63b8._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
    DAT_0a3e63b8._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
    DAT_0a3e63b8._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
    DAT_0a3e63b8._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
    DAT_0a3e63b8._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
    DAT_0a3e63b8._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
    DAT_0a3e63b8._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
    DAT_0a3e63b8._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
    DAT_0a3e63c0 = 0x2928;
    DAT_0a3e63c2 = 0;
    DAT_0a3e63c3 = 1;
  }
  FUN_05e1d050(&local_350,2,pppppppuVar1,&DAT_0a3e46a4,&DAT_0a3e63b8,0x395,0,0);
  FUN_04cbe4cc(local_5c8,*(undefined8 *)(param_1 + 8));
  local_3a0 = local_5c8[0];
  if (-1 < cStack_5b1) {
    local_3a0 = (char *******)local_5c8;
  }
  local_398 = (undefined1 *)((ulong)local_398 & 0xffffffffffffff00);
  if (**(char **)(param_1 + 0x18) == '\x01') {
    local_3f0 = (char ******)&DAT_0a3e6344;
    if ((DAT_0a3e6349 & 1) == 0) {
      DAT_0a3e6344 = 0x7274;
      DAT_0a3e6346 = 0x75;
      puVar12 = &DAT_0a3e6348;
      puVar6 = &DAT_0a3e6347;
      puVar16 = &DAT_0a3e6349;
LAB_032965dc:
      *puVar6 = 0x65;
      *puVar12 = 0;
      *puVar16 = 1;
    }
  }
  else {
    local_3f0 = (char ******)&DAT_0a3e634c;
    if ((DAT_0a3e6352 & 1) == 0) {
      DAT_0a3e634c = (undefined4)DAT_0847fe48;
      puVar6 = &DAT_0a3e6350;
      puVar12 = &DAT_0a3e6351;
      puVar16 = &DAT_0a3e6352;
      goto LAB_032965dc;
    }
  }
  local_3e8 = 0;
  uVar13 = *(uint *)(*(long *)(param_1 + 8) + 0x198);
  local_440 = (char ******)0x0;
  if ((DAT_0a3e6342 & 1) == 0) {
    uVar11 = 0;
    do {
      (&DAT_0a3e62fa)[uVar11] = (&DAT_088cd869)[uVar11] + 0x69 ^ (&DAT_088cd859)[uVar11 & 0xf];
      uVar11 = uVar11 + 1;
    } while (uVar11 != 0x48);
    DAT_0a3e6342 = 1;
  }
  uVar11 = (ulong)uVar13;
  lVar10 = 0;
  do {
    lVar8 = lVar10;
    uVar13 = (uint)uVar11;
    *(undefined1 *)((long)&local_438 + lVar8) =
         (&DAT_0a3e62fa)[uVar13 + (int)(uVar11 / 10) * -10 + 0x23];
    uVar11 = uVar11 / 10;
    lVar10 = lVar8 + 1;
  } while (9 < uVar13);
  *(undefined1 *)((long)&local_438 + lVar8 + 1) = 0;
  if (8 < lVar8 + 8U) {
    puVar14 = (undefined8 *)((long)&local_438 + lVar8);
    puVar4 = &local_438;
    do {
      puVar17 = (undefined8 *)((long)puVar4 + 1);
      uVar3 = *(undefined1 *)puVar14;
      puVar15 = (undefined8 *)((long)puVar14 + -1);
      *(undefined1 *)puVar14 = *(undefined1 *)puVar4;
      *(undefined1 *)puVar4 = uVar3;
      puVar14 = puVar15;
      puVar4 = puVar17;
    } while (puVar17 < puVar15);
  }
  local_440 = (char ******)&local_438;
  lVar10 = *(long *)(param_1 + 8);
  local_490 = *(long *)(lVar10 + 0x18);
  if (-1 < *(char *)(lVar10 + 0x2f)) {
    local_490 = lVar10 + 0x18;
  }
  local_488 = 0;
  lVar8 = 0;
  uVar11 = (ulong)*(uint *)(lVar10 + 0x19c);
  do {
    lVar19 = lVar8;
    uVar13 = (uint)uVar11;
    local_4d8[lVar19] = (&DAT_0a3e62fa)[uVar13 + (int)(uVar11 / 10) * -10 + 0x23];
    lVar8 = lVar19 + 1;
    uVar11 = uVar11 / 10;
  } while (9 < uVar13);
  local_4e0 = local_4d8;
  local_4d8[lVar19 + 1] = 0;
  if (8 < lVar19 + 8U) {
    puVar12 = local_4d8;
    puVar6 = local_4d8 + lVar19;
    do {
      puVar12 = puVar12 + 1;
      uVar3 = *puVar6;
      puVar16 = puVar6 + -1;
      *puVar6 = puVar12[-1];
      puVar12[-1] = uVar3;
      puVar6 = puVar16;
    } while (puVar12 < puVar16);
  }
  local_530 = *(long *)(lVar10 + 0x30);
  if (-1 < *(char *)(lVar10 + 0x47)) {
    local_530 = lVar10 + 0x30;
  }
  local_528 = 0;
  if ((int)uVar9 == 0) {
    local_580 = &DAT_0a3e634c;
    if ((DAT_0a3e6352 & 1) == 0) {
      DAT_0a3e634c = (undefined4)DAT_0847fe48;
      puVar6 = &DAT_0a3e6350;
      puVar12 = &DAT_0a3e6351;
      puVar16 = &DAT_0a3e6352;
      goto LAB_03296818;
    }
  }
  else {
    local_580 = (undefined4 *)&DAT_0a3e6344;
    if ((DAT_0a3e6349 & 1) == 0) {
      DAT_0a3e6344 = 0x7274;
      DAT_0a3e6346 = 0x75;
      puVar12 = &DAT_0a3e6348;
      puVar6 = &DAT_0a3e6347;
      puVar16 = &DAT_0a3e6349;
LAB_03296818:
      *puVar6 = 0x65;
      *puVar12 = 0;
      *puVar16 = 1;
    }
  }
  local_578 = 0;
  if ((DAT_0a3e6659 & 1) == 0) {
    uVar11 = 0;
    do {
      (&DAT_0a3e6614)[uVar11] = (&DAT_088cde62)[uVar11] + 0x69 ^ (&DAT_088cde52)[uVar11 & 0xf];
      uVar11 = uVar11 + 1;
    } while (uVar11 != 0x45);
    DAT_0a3e6659 = 1;
  }
  local_d8 = (char *******)&local_3a0;
  local_d0 = &local_3f0;
  local_c8 = &local_440;
  plStack_c0 = &local_490;
  local_b8 = &local_4e0;
  plStack_b0 = &local_530;
  local_a8 = &local_580;
  uStack_98 = 0;
  local_a0 = 0;
  uStack_88 = 0;
  local_90 = 0;
  uStack_78 = 0;
  local_80 = 0;
  uStack_68 = 0;
  local_70 = 0;
  local_60 = 0;
  FUN_05e1d31c(&local_350,&DAT_0a3e6614,&local_d8);
  if (cStack_5b1 < '\0') {
    __ZdlPvm(local_5c8[0],CONCAT17(cStack_5b1,local_5b8) & 0x7fffffffffffffff);
  }
  thunk_FUN_05e1d0bc(&local_350);
  if (cStack_599 < '\0') {
    __ZdlPvm(local_5b0[0],CONCAT17(cStack_599,local_5a0) & 0x7fffffffffffffff);
  }
joined_r0x03296914:
  if ((long)local_588 < 0) {
    __ZdlPvm(local_598,(ulong)local_588 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_58) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return uVar9;
}


