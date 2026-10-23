// Ghidra inferred pseudocode; requested=0x66637cc
// entry=066637cc end=066639c3

void FUN_066637cc(long *param_1,undefined8 *param_2)

{
  bool bVar1;
  ulong uVar2;
  undefined4 uVar3;
  long lVar4;
  long lVar5;
  ulong uVar6;
  ulong uVar7;
  long lVar8;
  undefined8 *puVar9;
  undefined8 *puVar10;
  undefined8 *puVar11;
  undefined4 uVar12;
  undefined8 uVar13;
  undefined8 uVar14;
  
  puVar11 = (undefined8 *)param_1[1];
  if (puVar11 < (undefined8 *)param_1[2]) {
    uVar14 = param_2[1];
    uVar13 = *param_2;
    puVar11[2] = param_2[2];
    puVar11[1] = uVar14;
    *puVar11 = uVar13;
    puVar11 = puVar11 + 3;
  }
  else {
    lVar4 = (long)puVar11 - *param_1 >> 3;
    uVar2 = lVar4 * -0x5555555555555555 + 1;
    if (0xaaaaaaaaaaaaaaa < uVar2) {
      FUN_06666fd0(param_1);
LAB_066639c0:
                    /* WARNING: Subroutine does not return */
      FUN_001e96c0();
    }
    lVar5 = param_1[2] - *param_1 >> 3;
    uVar7 = lVar5 * 0x5555555555555556;
    if (uVar7 < uVar2 || uVar7 - uVar2 == 0) {
      uVar7 = uVar2;
    }
    if (0x555555555555554 < (ulong)(lVar5 * -0x5555555555555555)) {
      uVar7 = 0xaaaaaaaaaaaaaaa;
    }
    if (uVar7 == 0) {
      lVar5 = 0;
    }
    else {
      if (0xaaaaaaaaaaaaaaa < uVar7) goto LAB_066639c0;
      lVar5 = __Znwm(uVar7 * 0x18);
    }
    puVar9 = (undefined8 *)(lVar5 + lVar4 * 8);
    uVar14 = param_2[1];
    uVar13 = *param_2;
    puVar9[2] = param_2[2];
    puVar9[1] = uVar14;
    *puVar9 = uVar13;
    puVar11 = puVar9 + 3;
    lVar4 = *param_1;
    lVar8 = param_1[1];
    if (lVar8 != lVar4) {
      do {
        uVar14 = *(undefined8 *)(lVar8 + -0x10);
        uVar13 = *(undefined8 *)(lVar8 + -0x18);
        puVar10 = (undefined8 *)(lVar8 + -8);
        lVar8 = lVar8 + -0x18;
        puVar9[-1] = *puVar10;
        puVar9[-2] = uVar14;
        puVar9[-3] = uVar13;
        puVar9 = puVar9 + -3;
      } while (lVar8 != lVar4);
      lVar4 = *param_1;
    }
    *param_1 = (long)puVar9;
    param_1[1] = (long)puVar11;
    lVar8 = param_1[2];
    param_1[2] = lVar5 + uVar7 * 0x18;
    if (lVar4 != 0) {
      __ZdlPvm(lVar4,lVar8 - lVar4);
    }
  }
  param_1[1] = (long)puVar11;
  lVar4 = *param_1;
  if (0x18 < (long)puVar11 - lVar4) {
    uVar6 = ((ulong)((long)puVar11 - lVar4) >> 3) * -0x5555555555555555 - 2 >> 1;
    puVar9 = (undefined8 *)(lVar4 + uVar6 * 0x18);
    uVar2 = puVar11[-2];
    uVar7 = puVar11[-1];
    bVar1 = uVar2 < (ulong)puVar9[1];
    if (puVar9[2] != uVar7) {
      bVar1 = uVar7 < (ulong)puVar9[2];
    }
    if (bVar1) {
      uVar3 = *(undefined4 *)(puVar11 + -3);
      uVar12 = *(undefined4 *)((long)puVar11 + -0x14);
      puVar11 = puVar11 + -3;
      do {
        puVar10 = puVar9;
        uVar14 = puVar10[1];
        uVar13 = *puVar10;
        puVar11[2] = puVar10[2];
        puVar11[1] = uVar14;
        *puVar11 = uVar13;
        if (uVar6 == 0) break;
        uVar6 = uVar6 - 1 >> 1;
        puVar9 = (undefined8 *)(lVar4 + uVar6 * 0x18);
        bVar1 = uVar2 < (ulong)puVar9[1];
        if (puVar9[2] != uVar7) {
          bVar1 = uVar7 < (ulong)puVar9[2];
        }
        puVar11 = puVar10;
      } while (bVar1);
      *(undefined4 *)puVar10 = uVar3;
      *(undefined4 *)((long)puVar10 + 4) = uVar12;
      puVar10[1] = uVar2;
      puVar10[2] = uVar7;
    }
  }
  return;
}


