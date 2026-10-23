// Ghidra inferred pseudocode; requested=0x292ef9c
// entry=0292ef9c end=0292f93b

/* WARNING: Removing unreachable block (ram,0x0292f478) */
/* WARNING: Removing unreachable block (ram,0x0292f490) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0292ef9c(long param_1)

{
  uint uVar1;
  undefined8 *******pppppppuVar2;
  undefined1 uVar3;
  long *plVar4;
  bool bVar5;
  long lVar6;
  int iVar7;
  undefined8 uVar8;
  undefined8 *puVar9;
  ulong uVar10;
  undefined1 *puVar11;
  ulong uVar12;
  long lVar13;
  int iVar14;
  byte *pbVar15;
  undefined1 *puVar16;
  undefined1 *puVar17;
  undefined1 *puVar18;
  undefined1 *puVar19;
  bool bVar20;
  undefined1 uVar21;
  undefined8 *******local_518 [2];
  undefined7 local_508;
  char cStack_501;
  undefined8 local_500;
  undefined1 *puStack_4f8;
  undefined8 local_4f0;
  undefined1 *local_4e8;
  undefined1 *local_4e0;
  undefined1 *puStack_4d8;
  undefined1 *puStack_4d0;
  undefined1 *local_4c8;
  undefined1 *local_4c0;
  undefined1 *local_408;
  byte local_288;
  long *******local_280;
  undefined1 *puStack_278;
  undefined1 *local_270;
  undefined8 local_268;
  undefined1 *local_260;
  undefined1 *puStack_258;
  undefined1 *puStack_250;
  undefined1 *local_248;
  undefined1 *local_240;
  undefined4 local_230;
  undefined3 uStack_22c;
  undefined4 local_228;
  undefined3 uStack_224;
  undefined8 local_220;
  long *local_218;
  undefined8 local_210;
  undefined1 *puStack_208;
  undefined1 *local_200;
  undefined1 *puStack_1f8;
  undefined1 *local_1f0;
  long *local_1e8;
  undefined1 uStack_1d9;
  undefined8 local_1d8;
  undefined8 local_1d0;
  undefined7 local_1c8;
  char cStack_1c1;
  long *******local_188;
  undefined1 local_180;
  long local_138;
  undefined1 local_130;
  long *local_e8;
  long *******ppppppplStack_e0;
  undefined8 *local_d8;
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
  undefined8 uStack_70;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  puStack_1f8 = &SUB_aaaaaaaaaaaaaaaa;
  local_200 = &SUB_aaaaaaaaaaaaaaaa;
  local_1e8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_1f0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_208 = &SUB_aaaaaaaaaaaaaaaa;
  local_210 = &SUB_aaaaaaaaaaaaaaaa;
  uVar8 = *(undefined8 *)(param_1 + 0x60);
  local_220 = *(undefined8 *)(param_1 + 0x30);
  local_218 = *(long **)(param_1 + 0x38);
  if (local_218 != (long *)0x0) {
    local_218[1] = local_218[1] + 1;
  }
  FUN_0317ded4(&local_210,uVar8,&local_220);
  plVar4 = local_218;
  if (local_218 != (long *)0x0) {
    LOAcquire();
    lVar6 = local_218[1];
    local_218[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*local_218 + 0x10))(local_218);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if ((int)local_210 == 0 && local_210._4_4_ == 0) {
    local_228 = 0xaaaaaaaa;
    uStack_224 = 0xaaaaaa;
    local_230 = 0xaaaaaaaa;
    uStack_22c = 0xaaaaaa;
    local_240 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_258 = &SUB_aaaaaaaaaaaaaaaa;
    local_260 = &SUB_aaaaaaaaaaaaaaaa;
    local_248 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_250 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_278 = &SUB_aaaaaaaaaaaaaaaa;
    local_280 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
    local_268 = &SUB_aaaaaaaaaaaaaaaa;
    local_270 = &SUB_aaaaaaaaaaaaaaaa;
    FUN_0086e43c(&local_280,local_1f0);
    puVar19 = local_268;
    puVar17 = &DAT_aaaaaaaaaaaaaa00;
    if ((char)local_240 == '\x01') {
      uVar10 = (ulong)local_268 & 0xffffffff;
      _memcpy(&local_500,&DAT_08825740,0x280);
      FUN_03190538(&local_500,*(undefined8 *)(param_1 + 0x60),param_1 + 0x40,local_268._4_4_,uVar10)
      ;
      puVar18 = (undefined1 *)((ulong)puVar19 >> 8 & 0xffffff);
      bVar20 = (local_288 & 1) == 0;
      if (bVar20) {
        local_408 = (undefined1 *)0x0;
      }
      else {
        FUN_00ac6290(&local_500);
        puVar17 = local_408;
      }
      bVar20 = !bVar20;
      uVar21 = 1;
      puVar19 = local_408;
    }
    else {
      uVar21 = 0;
      uVar10 = 0;
      bVar20 = false;
      puVar19 = (undefined1 *)0x0;
      puVar18 = &SUB_aaaaaaaaaaaaaa;
    }
    iVar7 = thunk_FUN_05e1d97c(2);
    if (iVar7 != 0) {
      FUN_0488143c(local_518);
      pppppppuVar2 = local_518[0];
      if (-1 < cStack_501) {
        pppppppuVar2 = local_518;
      }
      if ((DAT_0a3a556a & 1) == 0) {
        _DAT_0a3a5544 = CONCAT44((int)DAT_084a66c8,(int)DAT_08486a48);
        uRam000000000a3a554c = CONCAT44((int)DAT_084a66a8,(int)DAT_084a8ea0);
        _DAT_0a3a5554 = CONCAT44((int)DAT_08617fc8,(int)DAT_084a66b0);
        uRam000000000a3a555c = CONCAT44((int)DAT_084967c0,(int)DAT_08489770);
        DAT_0a3a5564 = (undefined4)DAT_084ccd80;
        DAT_0a3a5568 = 99;
        DAT_0a3a556a = 1;
      }
      if ((DAT_0a3a61fb & 1) == 0) {
        DAT_0a3a61f0._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
        DAT_0a3a61f0._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
        DAT_0a3a61f0._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
        DAT_0a3a61f0._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
        DAT_0a3a61f0._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
        DAT_0a3a61f0._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
        DAT_0a3a61f0._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
        DAT_0a3a61f0._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
        DAT_0a3a61f8 = 0x2928;
        DAT_0a3a61fa = 0;
        DAT_0a3a61fb = 1;
      }
      FUN_05e1d050(&local_500,2,pppppppuVar2,&DAT_0a3a5544,&DAT_0a3a61f0,0x193,0,0);
      local_138 = *(long *)(param_1 + 0x18);
      if (-1 < *(char *)(param_1 + 0x2f)) {
        local_138 = param_1 + 0x18;
      }
      local_130 = 0;
      local_188 = *(long ********)(param_1 + 0x40);
      if (-1 < *(char *)(param_1 + 0x57)) {
        local_188 = (long *******)(param_1 + 0x40);
      }
      local_180 = 0;
      iVar7 = *(int *)(param_1 + 0x58);
      local_1d8 = (undefined8 *)0x0;
      if ((DAT_0a3a617a & 1) == 0) {
        uVar12 = 0;
        do {
          (&DAT_0a3a6132)[uVar12] = (&DAT_08826e85)[uVar12] + 0x69 ^ (&DAT_08826e75)[uVar12 & 0xf];
          uVar12 = uVar12 + 1;
        } while (uVar12 != 0x48);
        DAT_0a3a617a = 1;
      }
      lVar6 = 8;
      iVar14 = iVar7;
      do {
        lVar13 = lVar6;
        *(undefined1 *)((long)&local_1d8 + lVar13) = (&DAT_0a3a6132)[iVar14 % 10 + 0x23];
        lVar6 = lVar13 + 1;
        uVar1 = iVar14 + 9;
        iVar14 = iVar14 / 10;
      } while (0x12 < uVar1);
      if (iVar7 < 0) {
        *(undefined1 *)((long)&local_1d8 + lVar13 + 1) = 0x2d;
        lVar6 = lVar13 + 2;
      }
      *(undefined1 *)((long)&local_1d8 + lVar6) = 0;
      if (9 < lVar6) {
        puVar11 = &uStack_1d9 + lVar6;
        puVar16 = (undefined1 *)((long)&local_1d0 + 1);
        do {
          uVar3 = *puVar11;
          *puVar11 = puVar16[-1];
          puVar16[-1] = uVar3;
          bVar5 = puVar16 < puVar11 + -1;
          puVar11 = puVar11 + -1;
          puVar16 = puVar16 + 1;
        } while (bVar5);
      }
      if ((DAT_0a3a627d & 1) == 0) {
        uVar12 = 0;
        do {
          (&DAT_0a3a6240)[uVar12] = (&DAT_088272d6)[uVar12] + 0x69 ^ (&DAT_088272c6)[uVar12 & 0xf];
          uVar12 = uVar12 + 1;
        } while (uVar12 != 0x3d);
        DAT_0a3a627d = 1;
      }
      local_e8 = &local_138;
      ppppppplStack_e0 = (long *******)&local_188;
      local_d8 = &local_1d8;
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
      uStack_70 = 0;
      local_1d8 = &local_1d0;
      FUN_05e1d31c(&local_500,&DAT_0a3a6240,&local_e8);
      thunk_FUN_05e1d0bc(&local_500);
      if (cStack_501 < '\0') {
        __ZdlPvm(local_518[0],CONCAT17(cStack_501,local_508) & 0x7fffffffffffffff);
      }
    }
    pbVar15 = *(byte **)(param_1 + 8);
    local_500._0_5_ = CONCAT41(local_228,1);
    local_500 = (undefined1 *)CONCAT44(CONCAT31(uStack_224,local_228._3_1_),(undefined4)local_500);
    puStack_4f8 = (undefined1 *)((ulong)puVar17 & 0xffffffffffffff00 | (ulong)puVar19 & 0xff);
    local_4f0._0_5_ = CONCAT41(local_230,bVar20);
    local_4f0 = (undefined1 *)CONCAT44(CONCAT31(uStack_22c,local_230._3_1_),(undefined4)local_4f0);
    local_4e8 = (undefined1 *)(uVar10 & 0xff | (long)puVar18 << 8);
    local_4e0 = (undefined1 *)CONCAT71(local_4e0._1_7_,uVar21);
    puStack_4d8 = (undefined1 *)((ulong)puStack_4d8 & 0xffffffffffffff00);
    local_4c0 = (undefined1 *)((ulong)local_4c0 & 0xffffffffffffff00);
    if ((*pbVar15 & 1) == 0) {
      *pbVar15 = 1;
      local_e8 = *(long **)(pbVar15 + 8);
      pbVar15[8] = 0;
      pbVar15[9] = 0;
      pbVar15[10] = 0;
      pbVar15[0xb] = 0;
      pbVar15[0xc] = 0;
      pbVar15[0xd] = 0;
      pbVar15[0xe] = 0;
      pbVar15[0xf] = 0;
      local_138 = 0;
      (*(code *)local_e8[1])(local_e8,&local_500);
      FUN_00033d2c(&local_e8);
      FUN_00033d2c(&local_138);
      if ((((ulong)local_4c0 & 1) != 0) && ((long)local_4c8 < 0)) {
        __ZdlPvm(puStack_4d8,(ulong)local_4c8 & 0x7fffffffffffffff);
      }
    }
    plVar4 = local_1e8;
    if ((char)local_240 == '\x01') {
      if ((long)local_248 < 0) {
        __ZdlPvm(puStack_258,(ulong)local_248 & 0x7fffffffffffffff);
      }
      plVar4 = local_1e8;
      if ((long)local_270 < 0) {
        __ZdlPvm(local_280,(ulong)local_270 & 0x7fffffffffffffff);
        plVar4 = local_1e8;
      }
    }
  }
  else {
    iVar7 = thunk_FUN_05e1d97c(4);
    if (iVar7 != 0) {
      FUN_0488143c(&local_1d8);
      puVar9 = local_1d8;
      if (-1 < cStack_1c1) {
        puVar9 = &local_1d8;
      }
      if ((DAT_0a3a556a & 1) == 0) {
        _DAT_0a3a5544 = CONCAT44((int)DAT_084a66c8,(int)DAT_08486a48);
        uRam000000000a3a554c = CONCAT44((int)DAT_084a66a8,(int)DAT_084a8ea0);
        _DAT_0a3a5554 = CONCAT44((int)DAT_08617fc8,(int)DAT_084a66b0);
        uRam000000000a3a555c = CONCAT44((int)DAT_084967c0,(int)DAT_08489770);
        DAT_0a3a5564 = (undefined4)DAT_084ccd80;
        DAT_0a3a5568 = 99;
        DAT_0a3a556a = 1;
      }
      if ((DAT_0a3a61fb & 1) == 0) {
        DAT_0a3a61f0._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
        DAT_0a3a61f0._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
        DAT_0a3a61f0._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
        DAT_0a3a61f0._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
        DAT_0a3a61f0._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
        DAT_0a3a61f0._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
        DAT_0a3a61f0._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
        DAT_0a3a61f0._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
        DAT_0a3a61f8 = 0x2928;
        DAT_0a3a61fa = 0;
        DAT_0a3a61fb = 1;
      }
      FUN_05e1d050(&local_500,4,puVar9,&DAT_0a3a5544,&DAT_0a3a61f0,0x186,0,0);
      local_138 = *(long *)(param_1 + 0x18);
      if (-1 < *(char *)(param_1 + 0x2f)) {
        local_138 = param_1 + 0x18;
      }
      local_130 = 0;
      FUN_023a403c(&local_280,&local_210);
      local_188 = local_280;
      if (-1 < (long)local_270) {
        local_188 = (long *******)&local_280;
      }
      local_180 = 0;
      if ((DAT_0a3a6225 & 1) == 0) {
        uVar10 = 0;
        do {
          (&DAT_0a3a61fc)[uVar10] = (&DAT_08827274)[uVar10] + 0x69 ^ (&DAT_08827264)[uVar10 & 0xf];
          uVar10 = uVar10 + 1;
        } while (uVar10 != 0x29);
        DAT_0a3a6225 = 1;
      }
      local_e8 = &local_138;
      ppppppplStack_e0 = (long *******)&local_188;
      uStack_d0 = 0;
      local_d8 = (undefined8 *)0x0;
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
      uStack_70 = 0;
      local_78 = 0;
      FUN_05e1d31c(&local_500,&DAT_0a3a61fc,&local_e8);
      if ((long)local_270 < 0) {
        __ZdlPvm(local_280,(ulong)local_270 & 0x7fffffffffffffff);
      }
      thunk_FUN_05e1d0bc(&local_500);
      if (cStack_1c1 < '\0') {
        __ZdlPvm(local_1d8,CONCAT17(cStack_1c1,local_1c8) & 0x7fffffffffffffff);
      }
    }
    pbVar15 = *(byte **)(param_1 + 8);
    FUN_023a403c(&local_e8,&local_210);
    if ((DAT_0a3a623f & 1) == 0) {
      uVar10 = 0;
      do {
        (&DAT_0a3a6226)[uVar10] = (&DAT_088272ad)[uVar10] + 0x69 ^ (&DAT_0882729d)[uVar10 & 0xf];
        uVar10 = uVar10 + 1;
      } while (uVar10 != 0x19);
      DAT_0a3a623f = 1;
    }
    puVar9 = (undefined8 *)
             __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6insertEmPKc
                       (&local_e8,0,&DAT_0a3a6226);
    puVar19 = (undefined1 *)*puVar9;
    puVar17 = (undefined1 *)puVar9[1];
    puVar16 = (undefined1 *)puVar9[2];
    puVar9[1] = 0;
    puVar9[2] = 0;
    *puVar9 = 0;
    local_4c8 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_4d0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_4f8 = &DAT_aaaaaaaaaaaaaa00;
    local_4f0 = &DAT_aaaaaaaaaaaaaa00;
    local_4e8 = &DAT_aaaaaaaaaaaaaa00;
    local_4e0 = &DAT_aaaaaaaaaaaaaa00;
    puStack_4d8 = &DAT_aaaaaaaaaaaaaa00;
    local_4c0 = &DAT_aaaaaaaaaaaaaa00;
    local_500 = &DAT_aaaaaaaaaaaaaa00;
    puVar18 = puVar19;
    puVar11 = puVar16;
    if ((long)puVar16 < 0) {
      FUN_00018d20(&puStack_4d8,puVar19);
      puVar18 = puStack_4d8;
      puVar17 = puStack_4d0;
      puVar11 = local_4c8;
    }
    local_4c8 = puVar11;
    puStack_4d0 = puVar17;
    puStack_4d8 = puVar18;
    uVar10 = 1;
    local_4c0 = (undefined1 *)CONCAT71(local_4c0._1_7_,1);
    if ((*pbVar15 & 1) == 0) {
      *pbVar15 = 1;
      local_138 = *(long *)(pbVar15 + 8);
      pbVar15[8] = 0;
      pbVar15[9] = 0;
      pbVar15[10] = 0;
      pbVar15[0xb] = 0;
      pbVar15[0xc] = 0;
      pbVar15[0xd] = 0;
      pbVar15[0xe] = 0;
      pbVar15[0xf] = 0;
      local_188 = (long *******)0x0;
      (**(code **)(local_138 + 8))(local_138,&local_500);
      FUN_00033d2c(&local_138);
      FUN_00033d2c(&local_188);
      uVar10 = (ulong)local_4c0 & 0xff;
    }
    if (((uVar10 & 1) != 0) && ((long)local_4c8 < 0)) {
      __ZdlPvm(puStack_4d8,(ulong)local_4c8 & 0x7fffffffffffffff);
    }
    plVar4 = local_1e8;
    if ((long)puVar16 < 0) {
      __ZdlPvm(puVar19,(ulong)puVar16 & 0x7fffffffffffffff);
      plVar4 = local_1e8;
    }
  }
  local_1e8 = plVar4;
  if (plVar4 != (long *)0x0) {
    LOAcquire();
    lVar6 = plVar4[1];
    plVar4[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*plVar4 + 0x10))(plVar4);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if ((long)puStack_1f8 < 0) {
    __ZdlPvm(puStack_208,(ulong)puStack_1f8 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_68) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


