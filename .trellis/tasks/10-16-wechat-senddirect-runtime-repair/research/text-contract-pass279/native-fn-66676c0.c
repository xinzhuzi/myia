// Ghidra inferred pseudocode; requested=0x66676c0
// entry=066676c0 end=06667877

void FUN_066676c0(undefined8 *param_1,long param_2,undefined8 param_3,long param_4)

{
  bool bVar1;
  ulong uVar2;
  ulong uVar3;
  long lVar4;
  undefined4 uVar5;
  undefined1 uVar6;
  undefined1 uVar7;
  undefined1 uVar8;
  undefined8 *puVar9;
  undefined8 *puVar10;
  ulong uVar11;
  undefined8 *puVar12;
  ulong uVar13;
  ulong uVar14;
  undefined1 uVar15;
  ulong uVar16;
  undefined8 uVar17;
  undefined8 uVar18;
  
  if (param_4 < 2) {
    return;
  }
  uVar5 = *(undefined4 *)param_1;
  uVar15 = *(undefined1 *)((long)param_1 + 4);
  uVar6 = *(undefined1 *)((long)param_1 + 5);
  uVar7 = *(undefined1 *)((long)param_1 + 6);
  uVar8 = *(undefined1 *)((long)param_1 + 7);
  uVar14 = param_1[1];
  uVar13 = param_1[2];
  puVar9 = param_1;
  uVar16 = 0;
  do {
    puVar12 = puVar9 + uVar16 * 3 + 3;
    uVar3 = uVar16 << 1 | 1;
    uVar2 = uVar16 * 2 + 2;
    uVar11 = uVar3;
    if ((long)uVar2 < param_4) {
      bVar1 = (ulong)puVar9[uVar16 * 3 + 7] < (ulong)puVar9[uVar16 * 3 + 4];
      if (puVar9[uVar16 * 3 + 5] != puVar9[uVar16 * 3 + 8]) {
        bVar1 = (ulong)puVar9[uVar16 * 3 + 8] < (ulong)puVar9[uVar16 * 3 + 5];
      }
      lVar4 = 0x18;
      if (!bVar1) {
        lVar4 = 0;
      }
      puVar12 = (undefined8 *)((long)puVar12 + lVar4);
      uVar11 = uVar2;
      if (!bVar1) {
        uVar11 = uVar3;
      }
    }
    uVar18 = puVar12[1];
    uVar17 = *puVar12;
    puVar9[2] = puVar12[2];
    puVar9[1] = uVar18;
    *puVar9 = uVar17;
    puVar9 = puVar12;
    uVar16 = uVar11;
  } while ((long)uVar11 <= (long)(param_4 - 2U >> 1));
  if (puVar12 == (undefined8 *)(param_2 + -0x18)) {
    *(undefined4 *)puVar12 = uVar5;
  }
  else {
    uVar18 = *(undefined8 *)(param_2 + -0x10);
    uVar17 = *(undefined8 *)(param_2 + -0x18);
    puVar12[2] = *(undefined8 *)(param_2 + -8);
    puVar12[1] = uVar18;
    *puVar12 = uVar17;
    *(undefined4 *)(param_2 + -0x18) = uVar5;
    *(undefined1 *)(param_2 + -0x14) = uVar15;
    *(undefined1 *)(param_2 + -0x13) = uVar6;
    *(undefined1 *)(param_2 + -0x12) = uVar7;
    *(undefined1 *)(param_2 + -0x11) = uVar8;
    uVar16 = (long)puVar12 + (0x18 - (long)param_1);
    *(ulong *)(param_2 + -0x10) = uVar14;
    *(ulong *)(param_2 + -8) = uVar13;
    if ((long)uVar16 < 0x19) {
      return;
    }
    uVar16 = (uVar16 >> 3) * -0x5555555555555555 - 2 >> 1;
    puVar9 = param_1 + uVar16 * 3;
    uVar14 = puVar12[1];
    uVar13 = puVar12[2];
    bVar1 = uVar14 < (ulong)puVar9[1];
    if (puVar9[2] != uVar13) {
      bVar1 = uVar13 < (ulong)puVar9[2];
    }
    if (!bVar1) {
      return;
    }
    uVar5 = *(undefined4 *)puVar12;
    uVar15 = *(undefined1 *)((long)puVar12 + 4);
    uVar6 = *(undefined1 *)((long)puVar12 + 5);
    uVar7 = *(undefined1 *)((long)puVar12 + 6);
    uVar8 = *(undefined1 *)((long)puVar12 + 7);
    puVar10 = puVar12;
    do {
      puVar12 = puVar9;
      uVar18 = puVar12[1];
      uVar17 = *puVar12;
      puVar10[2] = puVar12[2];
      puVar10[1] = uVar18;
      *puVar10 = uVar17;
      if (uVar16 == 0) break;
      uVar16 = uVar16 - 1 >> 1;
      puVar9 = param_1 + uVar16 * 3;
      bVar1 = uVar14 < (ulong)puVar9[1];
      if (puVar9[2] != uVar13) {
        bVar1 = uVar13 < (ulong)puVar9[2];
      }
      puVar10 = puVar12;
    } while (bVar1);
    *(undefined4 *)puVar12 = uVar5;
  }
  *(undefined1 *)((long)puVar12 + 4) = uVar15;
  *(undefined1 *)((long)puVar12 + 5) = uVar6;
  *(undefined1 *)((long)puVar12 + 6) = uVar7;
  *(undefined1 *)((long)puVar12 + 7) = uVar8;
  puVar12[1] = uVar14;
  puVar12[2] = uVar13;
  return;
}


