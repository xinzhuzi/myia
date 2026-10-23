// Ghidra inferred pseudocode; requested=0x46353a8
// entry=046353a8 end=0463575f

void FUN_046353a8(long param_1,ulong param_2)

{
  undefined8 **ppuVar1;
  undefined1 uVar2;
  long lVar3;
  bool bVar4;
  int iVar5;
  undefined8 *puVar6;
  undefined8 *puVar7;
  ulong uVar8;
  undefined8 *puVar9;
  undefined8 *puVar10;
  undefined1 *puVar11;
  undefined1 *puVar12;
  undefined1 *puVar13;
  long lVar14;
  uint uVar15;
  undefined8 *local_1b0 [2];
  undefined7 local_1a0;
  char cStack_199;
  undefined1 auStack_198 [144];
  undefined1 *local_108;
  undefined1 local_100 [72];
  undefined1 **local_b8;
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
  undefined8 uStack_58;
  undefined8 local_50;
  undefined8 uStack_48;
  undefined8 local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  if ((*(byte *)(param_1 + 0x18) & 1) == 0) goto LAB_04635730;
  __ZNSt3__15mutex4lockEv(param_1 + 0x80);
  (*(code *)PTR_FUN_0a124b98)(param_2);
  puVar6 = (undefined8 *)(param_1 + 0x70);
  puVar10 = (undefined8 *)*puVar6;
  puVar9 = puVar6;
  if (puVar10 == (undefined8 *)0x0) {
LAB_04635440:
    iVar5 = thunk_FUN_05e1d97c(4);
    if (iVar5 != 0) {
      FUN_0488143c(local_1b0);
      ppuVar1 = (undefined8 **)local_1b0[0];
      if (-1 < cStack_199) {
        ppuVar1 = local_1b0;
      }
      if ((DAT_0a45cea6 & 1) == 0) {
        uVar8 = 0;
        do {
          (&DAT_0a45ce91)[uVar8] = (&DAT_08a10f2b)[uVar8] + 0x8a ^ (&DAT_08a10f1b)[uVar8 & 0xf];
          uVar8 = uVar8 + 1;
        } while (uVar8 != 0x15);
        DAT_0a45cea6 = 1;
      }
      if ((DAT_0a45d2b9 & 1) == 0) {
        DAT_0a45d2b0 = DAT_0897e0a0;
        DAT_0a45d2b8 = 0;
        DAT_0a45d2b9 = 1;
      }
      FUN_05e1d050(auStack_198,4,ppuVar1,&DAT_0a45ce91,&DAT_0a45d2b0,0x260,0,0);
      local_108 = local_100;
      if ((DAT_0a45d389 & 1) == 0) {
        uVar8 = 0;
        do {
          (&DAT_0a45d341)[uVar8] = (&DAT_08a116aa)[uVar8] + 0x8a ^ (&DAT_08a1169a)[uVar8 & 0xf];
          uVar8 = uVar8 + 1;
        } while (uVar8 != 0x48);
        DAT_0a45d389 = 1;
      }
      lVar3 = 0;
      do {
        lVar14 = lVar3;
        uVar15 = (uint)param_2;
        local_100[lVar14] =
             (&DAT_0a45d341)[uVar15 + (int)((param_2 & 0xffffffff) / 10) * -10 + 0x23];
        lVar3 = lVar14 + 1;
        param_2 = (param_2 & 0xffffffff) / 10;
      } while (9 < uVar15);
      local_100[lVar14 + 1] = 0;
      if (8 < lVar14 + 8U) {
        puVar13 = local_100;
        puVar11 = local_100 + lVar14;
        do {
          puVar13 = puVar13 + 1;
          uVar2 = *puVar11;
          puVar12 = puVar11 + -1;
          *puVar11 = puVar13[-1];
          puVar13[-1] = uVar2;
          puVar11 = puVar12;
        } while (puVar13 < puVar12);
      }
      if ((DAT_0a45d2e0 & 1) == 0) {
        uVar8 = 0;
        do {
          (&DAT_0a45d2ba)[uVar8] = (&DAT_08a115d1)[uVar8] + 0x8a ^ (&DAT_08a115c1)[uVar8 & 0xf];
          uVar8 = uVar8 + 1;
        } while (uVar8 != 0x26);
        DAT_0a45d2e0 = 1;
      }
      uStack_a8 = 0;
      local_b0 = 0;
      local_b8 = &local_108;
      uStack_98 = 0;
      local_a0 = 0;
      uStack_88 = 0;
      local_90 = 0;
      uStack_78 = 0;
      local_80 = 0;
      uStack_68 = 0;
      local_70 = 0;
      uStack_58 = 0;
      local_60 = 0;
      uStack_48 = 0;
      local_50 = 0;
      local_40 = 0;
      FUN_05e1d31c(auStack_198,&DAT_0a45d2ba,&local_b8);
      thunk_FUN_05e1d0bc(auStack_198);
      if (cStack_199 < '\0') {
        uVar8 = CONCAT17(cStack_199,local_1a0) & 0x7fffffffffffffff;
        puVar10 = local_1b0[0];
        goto LAB_04635724;
      }
    }
  }
  else {
    do {
      uVar15 = (uint)param_2;
      if (*(uint *)(puVar10 + 4) >= uVar15) {
        puVar9 = puVar10;
      }
      puVar10 = (undefined8 *)puVar10[*(uint *)(puVar10 + 4) < uVar15];
    } while (puVar10 != (undefined8 *)0x0);
    if (puVar9 == puVar6) goto LAB_04635440;
    puVar10 = puVar6;
    if (*(uint *)(puVar9 + 4) <= uVar15) {
      puVar10 = puVar9;
    }
    if (puVar6 == puVar10) goto LAB_04635440;
    if ((long *)puVar10[5] != (long *)0x0) {
      (**(code **)(*(long *)puVar10[5] + 8))();
    }
    puVar9 = puVar10;
    puVar6 = (undefined8 *)puVar10[1];
    if ((undefined8 *)puVar10[1] == (undefined8 *)0x0) {
      do {
        puVar7 = (undefined8 *)puVar9[2];
        bVar4 = (undefined8 *)*puVar7 != puVar9;
        puVar9 = puVar7;
      } while (bVar4);
    }
    else {
      do {
        puVar7 = puVar6;
        puVar6 = (undefined8 *)*puVar7;
      } while ((undefined8 *)*puVar7 != (undefined8 *)0x0);
    }
    if (*(undefined8 **)(param_1 + 0x68) == puVar10) {
      *(undefined8 **)(param_1 + 0x68) = puVar7;
    }
    *(long *)(param_1 + 0x78) = *(long *)(param_1 + 0x78) + -1;
    FUN_00024618(*(undefined8 *)(param_1 + 0x70),puVar10);
    uVar8 = 0x30;
LAB_04635724:
    __ZdlPvm(puVar10,uVar8);
  }
  __ZNSt3__15mutex6unlockEv(param_1 + 0x80);
LAB_04635730:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


