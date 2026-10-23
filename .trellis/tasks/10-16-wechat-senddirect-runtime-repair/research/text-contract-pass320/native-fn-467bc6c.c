// Ghidra inferred pseudocode; requested=0x467bc6c
// entry=0467bc6c end=0467c0f3

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0467bc6c(long param_1)

{
  bool bVar1;
  undefined8 ******ppppppuVar2;
  undefined1 uVar3;
  undefined4 uVar4;
  uint3 uVar5;
  undefined8 *puVar6;
  undefined1 **ppuVar7;
  long lVar8;
  int iVar9;
  ulong uVar10;
  undefined1 *puVar11;
  undefined1 *puVar12;
  undefined1 *puVar13;
  ulong uVar14;
  long lVar15;
  long *plVar16;
  undefined8 *puVar17;
  long lVar18;
  undefined4 uVar19;
  undefined8 local_230;
  long *local_228;
  undefined8 *****local_220 [2];
  undefined7 local_210;
  char cStack_209;
  undefined8 *****local_208 [2];
  undefined7 local_1f8;
  char cStack_1f1;
  undefined8 local_1f0;
  undefined1 *puStack_1e8;
  undefined1 *local_1e0;
  undefined1 *puStack_1d8;
  undefined8 *local_1d0;
  undefined1 *puStack_1c8;
  undefined4 local_1c0;
  undefined8 local_1bc;
  undefined4 local_1b4;
  undefined1 *local_158;
  undefined1 local_150 [72];
  undefined8 *****local_108;
  undefined1 local_100;
  undefined8 *****local_b8;
  undefined1 **local_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 uStack_98;
  undefined8 uStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  undefined8 uStack_78;
  undefined8 uStack_70;
  undefined8 local_68;
  undefined8 uStack_60;
  undefined8 uStack_58;
  undefined8 uStack_50;
  undefined8 local_48;
  undefined8 uStack_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  FUN_000401d8(*(undefined8 *)(param_1 + 0x28));
  lVar18 = *(long *)(param_1 + 0x28);
  local_230 = *(undefined8 *)(param_1 + 0x220);
  local_228 = *(long **)(param_1 + 0x228);
  lVar8 = 0;
  if (local_228 != (long *)0x0) {
    lVar8 = local_228[1];
    local_228[1] = lVar8 + 1;
  }
  iVar9 = thunk_FUN_05e1d97c(lVar8,2);
  if (iVar9 != 0) {
    FUN_0488143c(local_208);
    ppppppuVar2 = (undefined8 ******)local_208[0];
    if (-1 < cStack_1f1) {
      ppppppuVar2 = local_208;
    }
    if ((DAT_0a45df8a & 1) == 0) {
      DAT_0a45df80._0_1_ = s_input_ackernel_cpadV_08a133a0[8];
      DAT_0a45df80._1_1_ = s_input_ackernel_cpadV_08a133a0[9];
      DAT_0a45df80._2_1_ = s_input_ackernel_cpadV_08a133a0[10];
      DAT_0a45df80._3_1_ = s_input_ackernel_cpadV_08a133a0[0xb];
      DAT_0a45df80._4_1_ = s_input_ackernel_cpadV_08a133a0[0xc];
      DAT_0a45df80._5_1_ = s_input_ackernel_cpadV_08a133a0[0xd];
      DAT_0a45df80._6_1_ = s_input_ackernel_cpadV_08a133a0[0xe];
      DAT_0a45df80._7_1_ = s_input_ackernel_cpadV_08a133a0[0xf];
      DAT_0a45df88 = 99;
      DAT_0a45df8a = 1;
    }
    if ((DAT_0a45e7d3 & 1) == 0) {
      DAT_0a45e7c8._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
      DAT_0a45e7c8._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
      DAT_0a45e7c8._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
      DAT_0a45e7c8._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
      DAT_0a45e7c8._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
      DAT_0a45e7c8._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
      DAT_0a45e7c8._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
      DAT_0a45e7c8._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
      DAT_0a45e7d0 = 0x2928;
      DAT_0a45e7d2 = 0;
      DAT_0a45e7d3 = 1;
    }
    FUN_05e1d050(&local_1f0,2,ppppppuVar2,&DAT_0a45df80,&DAT_0a45e7c8,0x450,0,0);
    FUN_04980e70(local_220,param_1 + 0x30);
    local_108 = local_220[0];
    if (-1 < cStack_209) {
      local_108 = local_220;
    }
    local_100 = 0;
    uVar10 = *(ulong *)(param_1 + 0x48);
    local_158 = local_150;
    if ((DAT_0a45e65a & 1) == 0) {
      uVar14 = 0;
      do {
        uVar19 = *(undefined4 *)((long)&DAT_08a1498d + uVar14);
        uVar5 = CONCAT12((char)((uint)uVar19 >> 8),(short)uVar19) & 0xff00ff;
        uVar4 = *(undefined4 *)((long)&DAT_08a14979 + uVar14 % 0x14);
        *(uint *)((long)&DAT_0a45e612 + uVar14) =
             CONCAT13((char)((uint)uVar19 >> 0x18) + 0x8aU ^ (byte)((uint)uVar4 >> 0x18),
                      CONCAT12((char)((uint)uVar19 >> 0x10) + 0x8aU ^ (byte)((uint)uVar4 >> 0x10),
                               CONCAT11((char)(uVar5 >> 0x10) + 0x8aU ^ (byte)((uint)uVar4 >> 8),
                                        (char)uVar5 + 0x8aU ^ (byte)uVar4)));
        uVar14 = uVar14 + 4;
      } while (uVar14 != 0x48);
      DAT_0a45e65a = 1;
    }
    lVar8 = 0;
    do {
      lVar15 = lVar8;
      local_150[lVar15] = *(undefined1 *)(uVar10 % 10 + 0xa45e635);
      bVar1 = 9 < uVar10;
      uVar10 = uVar10 / 10;
      lVar8 = lVar15 + 1;
    } while (bVar1);
    local_150[lVar15 + 1] = 0;
    if (8 < lVar15 + 8U) {
      puVar13 = local_150;
      puVar11 = local_150 + lVar15;
      do {
        puVar13 = puVar13 + 1;
        uVar3 = *puVar11;
        puVar12 = puVar11 + -1;
        *puVar11 = puVar13[-1];
        puVar13[-1] = uVar3;
        puVar11 = puVar12;
      } while (puVar13 < puVar12);
    }
    if ((DAT_0a45e86c & 1) == 0) {
      _DAT_0a45e854 = CONCAT44((int)DAT_0877e100,(int)ram0x08909df8);
      uRam000000000a45e85c = CONCAT44((int)DAT_084e3ff8,(int)DAT_084d4a88);
      DAT_0a45e864 = CONCAT44((int)ram0x084c9468,(int)ram0x08a13588);
      DAT_0a45e86c = 1;
    }
    local_b8 = &local_108;
    local_b0 = &local_158;
    uStack_a0 = 0;
    local_a8 = 0;
    uStack_90 = 0;
    uStack_98 = 0;
    uStack_80 = 0;
    local_88 = 0;
    uStack_70 = 0;
    uStack_78 = 0;
    uStack_60 = 0;
    local_68 = 0;
    uStack_50 = 0;
    uStack_58 = 0;
    uStack_40 = 0;
    local_48 = 0;
    FUN_05e1d31c(&local_1f0,&DAT_0a45e854,&local_b8);
    if (cStack_209 < '\0') {
      __ZdlPvm(local_220[0],CONCAT17(cStack_209,local_210) & 0x7fffffffffffffff);
    }
    thunk_FUN_05e1d0bc(&local_1f0);
    if (cStack_1f1 < '\0') {
      __ZdlPvm(local_208[0],CONCAT17(cStack_1f1,local_1f8) & 0x7fffffffffffffff);
    }
  }
  local_b8 = (undefined8 *****)&SUB_aaaaaaaaaaaaaaaa;
  local_b0 = (undefined1 **)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0467c394(&local_b8,&local_1f0,param_1 + 0x30);
  if (local_b0 != (undefined1 **)0x0) {
    local_b0[1] = (undefined1 *)((long)local_b0[1] + 1);
  }
  plVar16 = *(long **)(lVar18 + 0x70);
  *(undefined8 ******)(lVar18 + 0x68) = local_b8;
  *(undefined1 ***)(lVar18 + 0x70) = local_b0;
  if (plVar16 != (long *)0x0) {
    LOAcquire();
    lVar8 = plVar16[1];
    plVar16[1] = lVar8 + -1;
    LORelease();
    if (lVar8 == 0) {
      (**(code **)(*plVar16 + 0x10))(plVar16);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar16);
    }
  }
  FUN_0454e290(local_b8);
  FUN_04553f7c(local_b8,lVar18 + 0x278);
  puStack_1d8 = &SUB_aaaaaaaaaaaaaaaa;
  local_1e0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1c8 = &SUB_aaaaaaaaaaaaaaaa;
  local_1d0 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
  local_1c0 = 0xffffffff;
  local_1b4 = 0xaaaaaaaa;
  local_1f0 = 0xaaaaaa0000000000;
  puStack_1e8 = &DAT_aaaaaaaaaaaaaa00;
  local_1bc = 0xaaaaaa00aaaaaaaa;
  FUN_0467c174(&local_230,&local_1f0);
  puVar13 = local_1e0;
  puVar6 = local_1d0;
  if (local_1bc._4_1_ == '\x01') {
    while (puVar6 != (undefined8 *)0x0) {
      puVar17 = (undefined8 *)*puVar6;
      local_1e0 = puVar13;
      __ZdlPvm(puVar6,0x18);
      puVar13 = local_1e0;
      puVar6 = puVar17;
    }
    local_1e0 = (undefined1 *)0x0;
    if (puVar13 != (undefined1 *)0x0) {
      __ZdlPvm(puVar13,(long)puStack_1d8 << 3);
    }
  }
  ppuVar7 = local_b0;
  if (local_b0 != (undefined1 **)0x0) {
    LOAcquire();
    lVar8 = (long)local_b0[1];
    local_b0[1] = (undefined1 *)(lVar8 + -1);
    LORelease();
    if (lVar8 == 0) {
      (**(code **)((long)*local_b0 + 0x10))(local_b0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(ppuVar7);
    }
  }
  plVar16 = local_228;
  if (local_228 != (long *)0x0) {
    LOAcquire();
    lVar8 = local_228[1];
    local_228[1] = lVar8 + -1;
    LORelease();
    if (lVar8 == 0) {
      (**(code **)(*local_228 + 0x10))(local_228);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar16);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


