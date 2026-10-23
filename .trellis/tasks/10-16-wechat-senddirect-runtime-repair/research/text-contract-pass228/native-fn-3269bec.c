// Ghidra inferred pseudocode; requested=0x3269bec
// entry=03269bec end=0326a0f3

void FUN_03269bec(undefined8 param_1,long param_2)

{
  bool bVar1;
  undefined8 ******ppppppuVar2;
  undefined1 uVar3;
  int iVar4;
  long *plVar5;
  ulong uVar6;
  long lVar7;
  ulong uVar8;
  undefined1 *puVar9;
  uint uVar10;
  undefined1 *puVar11;
  long lVar12;
  undefined1 *puVar13;
  undefined8 *****local_270 [2];
  undefined7 local_260;
  char cStack_259;
  undefined8 local_258 [2];
  undefined7 local_248;
  char cStack_241;
  undefined1 *local_1c8;
  undefined1 local_1c0 [72];
  undefined1 *local_178;
  undefined1 local_170 [72];
  undefined1 *local_128;
  undefined1 local_120 [72];
  undefined1 **local_d8;
  undefined1 **ppuStack_d0;
  undefined1 **local_c8;
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
  undefined8 uStack_68;
  undefined8 local_60;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  plVar5 = (long *)FUN_04669774();
  uVar6 = (**(code **)(*plVar5 + 0x50))();
  lVar7 = FUN_04a2bbbc();
  if (lVar7 + (uVar6 & 0xffffffff) < (ulong)*(uint *)(param_2 + 0x114)) {
    iVar4 = thunk_FUN_05e1d97c(3);
    if (iVar4 != 0) {
      FUN_0488143c(local_270);
      ppppppuVar2 = (undefined8 ******)local_270[0];
      if (-1 < cStack_259) {
        ppppppuVar2 = local_270;
      }
      if ((DAT_0a3e46b7 & 1) == 0) {
        uVar8 = 0;
        do {
          (&DAT_0a3e46a4)[uVar8] = (&DAT_088ca7e4)[uVar8] + 0x8a ^ (&DAT_088ca7d4)[uVar8 & 0xf];
          uVar8 = uVar8 + 1;
        } while (uVar8 != 0x13);
        DAT_0a3e46b7 = 1;
      }
      if ((DAT_0a3e4f1c & 1) == 0) {
        uVar8 = 0;
        do {
          (&DAT_0a3e4f07)[uVar8] = (&DAT_088cb8fe)[uVar8] + 0x69 ^ (&DAT_088cb8ee)[uVar8 & 0xf];
          uVar8 = uVar8 + 1;
        } while (uVar8 != 0x15);
        DAT_0a3e4f1c = 1;
      }
      FUN_05e1d050(local_258,3,ppppppuVar2,&DAT_0a3e46a4,&DAT_0a3e4f07,0x358,0,0);
      uVar10 = *(uint *)(param_2 + 0x114);
      local_128 = (undefined1 *)0x0;
      if ((DAT_0a3e6342 & 1) == 0) {
        uVar8 = 0;
        do {
          (&DAT_0a3e62fa)[uVar8] = (&DAT_088cd869)[uVar8] + 0x69 ^ (&DAT_088cd859)[uVar8 & 0xf];
          uVar8 = uVar8 + 1;
        } while (uVar8 != 0x48);
        DAT_0a3e6342 = 1;
      }
      uVar8 = (ulong)uVar10;
      lVar7 = 0;
      do {
        lVar12 = lVar7;
        uVar10 = (uint)uVar8;
        local_120[lVar12] = (&DAT_0a3e62fa)[uVar10 + (int)(uVar8 / 10) * -10 + 0x23];
        uVar8 = uVar8 / 10;
        lVar7 = lVar12 + 1;
      } while (9 < uVar10);
      local_120[lVar12 + 1] = 0;
      if (8 < lVar12 + 8U) {
        puVar13 = local_120;
        puVar9 = local_120 + lVar12;
        do {
          puVar13 = puVar13 + 1;
          uVar3 = *puVar9;
          puVar11 = puVar9 + -1;
          *puVar9 = puVar13[-1];
          puVar13[-1] = uVar3;
          puVar9 = puVar11;
        } while (puVar13 < puVar11);
      }
      local_128 = local_120;
      local_178 = (undefined1 *)0x0;
      lVar7 = 0;
      uVar8 = *(ulong *)(param_2 + 0x100);
      do {
        lVar12 = lVar7;
        local_170[lVar12] = (&DAT_0a3e631d)[uVar8 % 10];
        bVar1 = 9 < uVar8;
        lVar7 = lVar12 + 1;
        uVar8 = uVar8 / 10;
      } while (bVar1);
      local_170[lVar12 + 1] = 0;
      if (8 < lVar12 + 8U) {
        puVar13 = local_170;
        puVar9 = local_170 + lVar12;
        do {
          puVar13 = puVar13 + 1;
          uVar3 = *puVar9;
          puVar11 = puVar9 + -1;
          *puVar9 = puVar13[-1];
          puVar13[-1] = uVar3;
          puVar9 = puVar11;
        } while (puVar13 < puVar11);
      }
      local_178 = local_170;
      local_1c8 = local_1c0;
      lVar7 = 0;
      uVar8 = uVar6;
      do {
        lVar12 = lVar7;
        uVar10 = (uint)uVar8;
        local_1c0[lVar12] = (&DAT_0a3e62fa)[uVar10 + (int)((uVar8 & 0xffffffff) / 10) * -10 + 0x23];
        lVar7 = lVar12 + 1;
        uVar8 = (uVar8 & 0xffffffff) / 10;
      } while (9 < uVar10);
      local_1c0[lVar12 + 1] = 0;
      if (8 < lVar12 + 8U) {
        puVar13 = local_1c0;
        puVar9 = local_1c0 + lVar12;
        do {
          puVar13 = puVar13 + 1;
          uVar3 = *puVar9;
          puVar11 = puVar9 + -1;
          *puVar9 = puVar13[-1];
          puVar13[-1] = uVar3;
          puVar9 = puVar11;
        } while (puVar13 < puVar11);
      }
      if ((DAT_0a3e4f5a & 1) == 0) {
        uVar8 = 0;
        do {
          (&DAT_0a3e4f1d)[uVar8] = (&DAT_088cb923)[uVar8] + 0x8a ^ (&DAT_088cb913)[uVar8 & 0xf];
          uVar8 = uVar8 + 1;
        } while (uVar8 != 0x3d);
        DAT_0a3e4f5a = 1;
      }
      local_d8 = &local_128;
      ppuStack_d0 = &local_178;
      local_c8 = &local_1c8;
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
      uStack_68 = 0;
      local_70 = 0;
      local_60 = 0;
      FUN_05e1d31c(local_258,&DAT_0a3e4f1d,&local_d8);
      thunk_FUN_05e1d0bc(local_258);
      if (cStack_259 < '\0') {
        __ZdlPvm(local_270[0],CONCAT17(cStack_259,local_260) & 0x7fffffffffffffff);
      }
    }
    thunk_FUN_04cbd748(param_2);
    if ((DAT_0a3e4f6f & 1) == 0) {
      uVar8 = 0;
      do {
        (&DAT_0a3e4f5b)[uVar8] = (&DAT_088cb970)[uVar8] + 0x8a ^ (&DAT_088cb960)[uVar8 & 0xf];
        uVar8 = uVar8 + 1;
      } while (uVar8 != 0x14);
      DAT_0a3e4f6f = 1;
    }
    FUN_00067f80(local_258,&DAT_0a3e4f5b);
    FUN_04af3aa8(&DAT_00008030,local_258,1);
    if (cStack_241 < '\0') {
      __ZdlPvm(local_258[0],CONCAT17(cStack_241,local_248) & 0x7fffffffffffffff);
    }
    *(ulong *)(param_2 + 0x100) = (uVar6 & 0xffffffff) * 1000;
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


