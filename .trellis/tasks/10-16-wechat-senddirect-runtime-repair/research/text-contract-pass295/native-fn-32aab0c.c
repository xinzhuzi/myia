// Ghidra inferred pseudocode; requested=0x32aab0c
// entry=032aab0c end=032ab5e7

undefined8 FUN_032aab0c(long param_1)

{
  undefined8 *****pppppuVar1;
  long *plVar2;
  undefined1 uVar3;
  long *****ppppplVar4;
  bool bVar5;
  int iVar6;
  undefined8 uVar7;
  ulong uVar8;
  long ****pppplVar9;
  uint uVar10;
  long ****pppplVar11;
  undefined1 *puVar12;
  undefined1 *puVar13;
  long lVar14;
  long lVar15;
  long *****ppppplVar16;
  undefined8 ****local_748 [2];
  undefined7 local_738;
  char cStack_731;
  undefined8 ****local_730 [2];
  undefined7 local_720;
  char cStack_719;
  undefined1 *local_718;
  undefined1 *local_710;
  undefined1 *local_708;
  undefined8 ****local_700;
  undefined1 local_6f8;
  undefined7 local_6f0;
  char cStack_6e9;
  long ***local_6b0;
  undefined8 local_6a8;
  char *local_660;
  ulong local_658;
  undefined8 uStack_650;
  undefined **local_610 [22];
  undefined **local_560;
  undefined **ppuStack_558;
  undefined **local_550;
  undefined **local_548;
  undefined **local_540;
  undefined **local_538;
  undefined **local_530;
  undefined **local_528;
  byte local_4b0 [8];
  undefined1 auStack_4a8 [632];
  undefined1 *local_230;
  undefined1 *puStack_228;
  undefined1 *puStack_220;
  undefined1 *puStack_218;
  undefined1 *local_210;
  undefined1 *puStack_208;
  undefined1 *puStack_200;
  undefined1 *puStack_1f8;
  undefined1 *local_1f0;
  undefined1 *puStack_1e8;
  undefined1 *puStack_1e0;
  undefined1 *puStack_1d8;
  undefined1 *local_1d0;
  undefined1 *puStack_1c8;
  undefined1 *puStack_1c0;
  undefined1 *puStack_1b8;
  undefined1 *local_1b0;
  undefined1 *puStack_1a8;
  undefined1 *puStack_1a0;
  undefined1 *puStack_198;
  undefined1 *local_190;
  undefined1 *puStack_188;
  undefined1 *puStack_180;
  undefined1 *puStack_178;
  undefined1 *local_170;
  undefined1 *puStack_168;
  undefined1 *puStack_160;
  undefined1 *puStack_158;
  undefined1 *local_150;
  undefined1 *puStack_148;
  undefined1 *puStack_140;
  undefined1 *puStack_138;
  undefined1 *local_130;
  undefined1 *puStack_128;
  undefined1 *puStack_120;
  undefined1 *puStack_118;
  undefined1 *local_110;
  undefined1 *puStack_108;
  undefined1 *puStack_100;
  undefined1 *puStack_f8;
  undefined1 *local_f0;
  undefined1 *puStack_e8;
  undefined1 *puStack_e0;
  undefined1 *puStack_d8;
  char **local_c8;
  long ****local_c0;
  long ****local_b8;
  long lStack_b0;
  undefined8 uStack_a8;
  undefined8 uStack_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 local_60;
  undefined8 uStack_58;
  undefined8 local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar15 = *(long *)(param_1 + 0x18);
  local_710 = &SUB_aaaaaaaaaaaaaaaa;
  local_708 = &SUB_aaaaaaaaaaaaaaaa;
  local_718 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_030251cc(&local_718,*(undefined8 *)(param_1 + 8));
  puStack_e8 = &SUB_aaaaaaaaaaaaaaaa;
  local_f0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_d8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_e0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_108 = &SUB_aaaaaaaaaaaaaaaa;
  local_110 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_f8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_100 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_128 = &SUB_aaaaaaaaaaaaaaaa;
  local_130 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_118 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_120 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_148 = &SUB_aaaaaaaaaaaaaaaa;
  local_150 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_138 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_140 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_168 = &SUB_aaaaaaaaaaaaaaaa;
  local_170 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_158 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_160 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_188 = &SUB_aaaaaaaaaaaaaaaa;
  local_190 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_178 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_180 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1a8 = &SUB_aaaaaaaaaaaaaaaa;
  local_1b0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_198 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1a0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1c8 = &SUB_aaaaaaaaaaaaaaaa;
  local_1d0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1b8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1c0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1e8 = &SUB_aaaaaaaaaaaaaaaa;
  local_1f0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1d8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1e0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_208 = &SUB_aaaaaaaaaaaaaaaa;
  local_210 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1f8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_200 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_228 = &SUB_aaaaaaaaaaaaaaaa;
  local_230 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_218 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_220 = &SUB_aaaaaaaaaaaaaaaa;
  local_560 = &PTR____cxa_pure_virtual_09da57d8;
  FUN_056cbbe8(local_610,&PTR_PTR_09f24220);
  local_610[0] = &PTR_FUN_09f23fe8;
  local_560 = &PTR_FUN_09f24040;
  ppuStack_558 = &PTR_FUN_09f24080;
  local_550 = &PTR_FUN_09f240c0;
  local_548 = &PTR_FUN_09f24100;
  local_540 = &PTR_FUN_09f24140;
  local_538 = &PTR_FUN_09f24180;
  local_530 = &PTR_FUN_09f241c0;
  local_528 = &PTR_FUN_09f24200;
  uVar7 = FUN_04cbaf80();
  FUN_056fa6fc(local_610,uVar7,0xf4);
  FUN_026fc2c4(local_4b0,*(undefined8 *)(param_1 + 0x10));
  FUN_056c9dac(&local_230,&ppuStack_558,local_4b0);
  FUN_056cd5a8(local_4b0);
  FUN_056fa308(local_610);
  _memcpy(local_4b0,&DAT_088ca190,0x280);
  uVar7 = *(undefined8 *)(lVar15 + 8);
  local_658 = 0;
  uStack_650 = 0;
  local_660 = "";
  FUN_056c90b0(local_610,&local_718);
  FUN_0562fe5c(&local_660,local_610);
  FUN_0562fd84(local_610);
  lStack_b0 = 0;
  local_c8 = &PTR_FUN_09da5e40;
  local_c0 = (long ****)&local_c0;
  local_b8 = (long ****)&local_c0;
  FUN_056cd3ec(local_610);
  FUN_0328714c(local_4b0,uVar7,&local_660,&local_230,&local_c8,local_610);
  FUN_056cd5a8(local_610);
  if (lStack_b0 != 0) {
    pppplVar9 = (long ****)local_c0[1];
    pppplVar11 = (long ****)*local_b8;
    pppplVar11[1] = (long ***)pppplVar9;
    *pppplVar9 = (long ***)pppplVar11;
    lStack_b0 = 0;
    ppppplVar4 = (long *****)local_b8;
    while (ppppplVar4 != &local_c0) {
      ppppplVar16 = (long *****)ppppplVar4[1];
      FUN_056cf45c(ppppplVar4 + 2);
      __ZdlPvm(ppppplVar4,0x160);
      ppppplVar4 = ppppplVar16;
    }
  }
  FUN_0562fd84(&local_660);
  if ((local_4b0[0] & 1) == 0) {
    iVar6 = thunk_FUN_05e1d97c(3);
    if (iVar6 != 0) {
      FUN_0488143c(&local_700);
      pppppuVar1 = (undefined8 *****)local_700;
      if (-1 < cStack_6e9) {
        pppppuVar1 = &local_700;
      }
      if ((DAT_0a3e46b7 & 1) == 0) {
        uVar8 = 0;
        do {
          (&DAT_0a3e46a4)[uVar8] = (&DAT_088ca7e4)[uVar8] + 0x8a ^ (&DAT_088ca7d4)[uVar8 & 0xf];
          uVar8 = uVar8 + 1;
        } while (uVar8 != 0x13);
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
      FUN_05e1d050(local_610,3,pppppuVar1,&DAT_0a3e46a4,&DAT_0a3e63b8,0x810,0,0);
      plVar2 = *(long **)(param_1 + 8);
      local_660 = (char *)*plVar2;
      if (-1 < *(char *)((long)plVar2 + 0x17)) {
        local_660 = (char *)plVar2;
      }
      local_658 = local_658 & 0xffffffffffffff00;
      uVar10 = **(uint **)(param_1 + 0x10);
      local_6b0 = (long ***)&local_6a8;
      if ((DAT_0a3e6342 & 1) == 0) {
        uVar8 = 0;
        do {
          (&DAT_0a3e62fa)[uVar8] = (&DAT_088cd869)[uVar8] + 0x69 ^ (&DAT_088cd859)[uVar8 & 0xf];
          uVar8 = uVar8 + 1;
        } while (uVar8 != 0x48);
        DAT_0a3e6342 = 1;
      }
      uVar8 = (ulong)uVar10;
      lVar15 = 0;
      do {
        lVar14 = lVar15;
        uVar10 = (uint)uVar8;
        *(undefined1 *)((long)&local_6a8 + lVar14) =
             (&DAT_0a3e62fa)[uVar10 + (int)(uVar8 / 10) * -10 + 0x23];
        uVar8 = uVar8 / 10;
        lVar15 = lVar14 + 1;
      } while (9 < uVar10);
      *(undefined1 *)((long)&local_6a8 + lVar14 + 1) = 0;
      if (8 < lVar14 + 8U) {
        puVar12 = (undefined1 *)((long)&local_6a8 + lVar14);
        puVar13 = (undefined1 *)((long)&local_6a8 + 1);
        do {
          uVar3 = *puVar12;
          *puVar12 = puVar13[-1];
          puVar13[-1] = uVar3;
          bVar5 = puVar13 < puVar12 + -1;
          puVar12 = puVar12 + -1;
          puVar13 = puVar13 + 1;
        } while (bVar5);
      }
      if ((DAT_0a3e6bf2 & 1) == 0) {
        uVar8 = 0;
        do {
          (&DAT_0a3e6bd5)[uVar8] = (&DAT_088ce6d2)[uVar8] + 0x69 ^ (&DAT_088ce6c2)[uVar8 & 0xf];
          uVar8 = uVar8 + 1;
        } while (uVar8 != 0x1d);
        DAT_0a3e6bf2 = 1;
      }
      local_c8 = &local_660;
      local_c0 = &local_6b0;
      lStack_b0 = 0;
      local_b8 = (long ****)0x0;
      uStack_a0 = 0;
      uStack_a8 = 0;
      local_90 = 0;
      uStack_98 = 0;
      local_80 = 0;
      uStack_88 = 0;
      local_70 = 0;
      uStack_78 = 0;
      local_60 = 0;
      uStack_68 = 0;
      local_50 = 0;
      uStack_58 = 0;
      FUN_05e1d31c(local_610,&DAT_0a3e6bd5,&local_c8);
LAB_032ab2c8:
      thunk_FUN_05e1d0bc(local_610);
      if (cStack_6e9 < '\0') {
        __ZdlPvm(local_700,CONCAT17(cStack_6e9,local_6f0) & 0x7fffffffffffffff);
      }
    }
  }
  else {
    FUN_02a0eb88(*(undefined8 *)(param_1 + 0x20),auStack_4a8);
    if ((**(char **)(param_1 + 0x28) != '\x01') ||
       (uVar8 = FUN_03280514(lVar15,*(undefined8 *)(param_1 + 0x20)), (uVar8 & 1) != 0)) {
      iVar6 = thunk_FUN_05e1d97c(2);
      if (iVar6 != 0) {
        FUN_0488143c(local_730);
        pppppuVar1 = (undefined8 *****)local_730[0];
        if (-1 < cStack_719) {
          pppppuVar1 = local_730;
        }
        if ((DAT_0a3e46b7 & 1) == 0) {
          uVar8 = 0;
          do {
            (&DAT_0a3e46a4)[uVar8] = (&DAT_088ca7e4)[uVar8] + 0x8a ^ (&DAT_088ca7d4)[uVar8 & 0xf];
            uVar8 = uVar8 + 1;
          } while (uVar8 != 0x13);
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
        FUN_05e1d050(local_610,2,pppppuVar1,&DAT_0a3e46a4,&DAT_0a3e63b8,0x81a,0,0);
        plVar2 = *(long **)(param_1 + 8);
        local_660 = (char *)*plVar2;
        if (-1 < *(char *)((long)plVar2 + 0x17)) {
          local_660 = (char *)plVar2;
        }
        local_658 = local_658 & 0xffffffffffffff00;
        uVar10 = **(uint **)(param_1 + 0x10);
        local_6b0 = (long ***)&local_6a8;
        if ((DAT_0a3e6342 & 1) == 0) {
          uVar8 = 0;
          do {
            (&DAT_0a3e62fa)[uVar8] = (&DAT_088cd869)[uVar8] + 0x69 ^ (&DAT_088cd859)[uVar8 & 0xf];
            uVar8 = uVar8 + 1;
          } while (uVar8 != 0x48);
          DAT_0a3e6342 = 1;
        }
        uVar8 = (ulong)uVar10;
        lVar15 = 0;
        do {
          lVar14 = lVar15;
          uVar10 = (uint)uVar8;
          *(undefined1 *)((long)&local_6a8 + lVar14) =
               (&DAT_0a3e62fa)[uVar10 + (int)(uVar8 / 10) * -10 + 0x23];
          uVar8 = uVar8 / 10;
          lVar15 = lVar14 + 1;
        } while (9 < uVar10);
        *(undefined1 *)((long)&local_6a8 + lVar14 + 1) = 0;
        if (8 < lVar14 + 8U) {
          puVar12 = (undefined1 *)((long)&local_6a8 + lVar14);
          puVar13 = (undefined1 *)((long)&local_6a8 + 1);
          do {
            uVar3 = *puVar12;
            *puVar12 = puVar13[-1];
            puVar13[-1] = uVar3;
            bVar5 = puVar13 < puVar12 + -1;
            puVar12 = puVar12 + -1;
            puVar13 = puVar13 + 1;
          } while (bVar5);
        }
        FUN_04cbe440(local_748,*(undefined8 *)(param_1 + 0x20));
        local_700 = local_748[0];
        if (-1 < cStack_731) {
          local_700 = local_748;
        }
        local_6f8 = 0;
        if ((DAT_0a3e6c33 & 1) == 0) {
          uVar8 = 0;
          do {
            (&DAT_0a3e6c13)[uVar8] = (&DAT_088ce72e)[uVar8] + 0x69 ^ (&DAT_088ce71e)[uVar8 & 0xf];
            uVar8 = uVar8 + 1;
          } while (uVar8 != 0x20);
          DAT_0a3e6c33 = 1;
        }
        local_c8 = &local_660;
        local_c0 = &local_6b0;
        local_b8 = (long ****)&local_700;
        uStack_a8 = 0;
        lStack_b0 = 0;
        uStack_98 = 0;
        uStack_a0 = 0;
        uStack_88 = 0;
        local_90 = 0;
        uStack_78 = 0;
        local_80 = 0;
        uStack_68 = 0;
        local_70 = 0;
        uStack_58 = 0;
        local_60 = 0;
        local_50 = 0;
        FUN_05e1d31c(local_610,&DAT_0a3e6c13,&local_c8);
        if (cStack_731 < '\0') {
          __ZdlPvm(local_748[0],CONCAT17(cStack_731,local_738) & 0x7fffffffffffffff);
        }
        thunk_FUN_05e1d0bc(local_610);
        if (cStack_719 < '\0') {
          __ZdlPvm(local_730[0],CONCAT17(cStack_719,local_720) & 0x7fffffffffffffff);
        }
      }
      uVar7 = 1;
      goto LAB_032ab578;
    }
    iVar6 = thunk_FUN_05e1d97c(4);
    if (iVar6 != 0) {
      FUN_0488143c(&local_700);
      pppppuVar1 = (undefined8 *****)local_700;
      if (-1 < cStack_6e9) {
        pppppuVar1 = &local_700;
      }
      if ((DAT_0a3e46b7 & 1) == 0) {
        uVar8 = 0;
        do {
          (&DAT_0a3e46a4)[uVar8] = (&DAT_088ca7e4)[uVar8] + 0x8a ^ (&DAT_088ca7d4)[uVar8 & 0xf];
          uVar8 = uVar8 + 1;
        } while (uVar8 != 0x13);
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
      FUN_05e1d050(local_610,4,pppppuVar1,&DAT_0a3e46a4,&DAT_0a3e63b8,0x816,0,0);
      plVar2 = *(long **)(param_1 + 8);
      local_660 = (char *)*plVar2;
      if (-1 < *(char *)((long)plVar2 + 0x17)) {
        local_660 = (char *)plVar2;
      }
      local_658 = local_658 & 0xffffffffffffff00;
      uVar10 = **(uint **)(param_1 + 0x10);
      local_6b0 = (long ***)&local_6a8;
      if ((DAT_0a3e6342 & 1) == 0) {
        uVar8 = 0;
        do {
          (&DAT_0a3e62fa)[uVar8] = (&DAT_088cd869)[uVar8] + 0x69 ^ (&DAT_088cd859)[uVar8 & 0xf];
          uVar8 = uVar8 + 1;
        } while (uVar8 != 0x48);
        DAT_0a3e6342 = 1;
      }
      uVar8 = (ulong)uVar10;
      lVar15 = 0;
      do {
        lVar14 = lVar15;
        uVar10 = (uint)uVar8;
        *(undefined1 *)((long)&local_6a8 + lVar14) =
             (&DAT_0a3e62fa)[uVar10 + (int)(uVar8 / 10) * -10 + 0x23];
        uVar8 = uVar8 / 10;
        lVar15 = lVar14 + 1;
      } while (9 < uVar10);
      *(undefined1 *)((long)&local_6a8 + lVar14 + 1) = 0;
      if (8 < lVar14 + 8U) {
        puVar12 = (undefined1 *)((long)&local_6a8 + lVar14);
        puVar13 = (undefined1 *)((long)&local_6a8 + 1);
        do {
          uVar3 = *puVar12;
          *puVar12 = puVar13[-1];
          puVar13[-1] = uVar3;
          bVar5 = puVar13 < puVar12 + -1;
          puVar12 = puVar12 + -1;
          puVar13 = puVar13 + 1;
        } while (bVar5);
      }
      if ((DAT_0a3e6c12 & 1) == 0) {
        uVar8 = 0;
        do {
          (&DAT_0a3e6bf3)[uVar8] = (&DAT_088ce6ff)[uVar8] + 0x69 ^ (&DAT_088ce6ef)[uVar8 & 0xf];
          uVar8 = uVar8 + 1;
        } while (uVar8 != 0x1f);
        DAT_0a3e6c12 = 1;
      }
      local_c8 = &local_660;
      local_c0 = &local_6b0;
      lStack_b0 = 0;
      local_b8 = (long ****)0x0;
      uStack_a0 = 0;
      uStack_a8 = 0;
      local_90 = 0;
      uStack_98 = 0;
      local_80 = 0;
      uStack_88 = 0;
      local_70 = 0;
      uStack_78 = 0;
      local_60 = 0;
      uStack_68 = 0;
      local_50 = 0;
      uStack_58 = 0;
      FUN_05e1d31c(local_610,&DAT_0a3e6bf3,&local_c8);
      goto LAB_032ab2c8;
    }
  }
  uVar7 = 0;
LAB_032ab578:
  if (local_4b0[0] == 1) {
    FUN_00ac6290(auStack_4a8);
  }
  FUN_056cd5a8(&local_230);
  if ((long)local_708 < 0) {
    __ZdlPvm(local_718,(ulong)local_708 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return uVar7;
}


