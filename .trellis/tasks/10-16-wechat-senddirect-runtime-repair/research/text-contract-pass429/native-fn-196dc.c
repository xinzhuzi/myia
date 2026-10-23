// Ghidra inferred pseudocode; requested=0x196dc
// entry=000196dc end=00019857

void FUN_000196dc(long *param_1,ulong param_2)

{
  ulong uVar1;
  undefined1 *puVar2;
  void *pvVar3;
  undefined1 *puVar4;
  long lVar5;
  undefined1 *puVar6;
  ulong uVar7;
  undefined8 *puVar8;
  ulong uVar9;
  ulong uVar10;
  undefined1 *puVar11;
  undefined8 *puVar12;
  undefined1 *puVar13;
  void *pvVar14;
  long lVar15;
  undefined8 uVar16;
  undefined8 uVar17;
  undefined8 uVar18;
  undefined8 uVar19;
  undefined8 uVar20;
  undefined8 uVar21;
  undefined8 uVar22;
  
  pvVar3 = (void *)param_1[1];
  if (param_2 <= (ulong)(param_1[2] - (long)pvVar3)) {
    pvVar14 = pvVar3;
    if (param_2 != 0) {
      pvVar14 = (void *)((long)pvVar3 + param_2);
      _bzero(pvVar3,param_2);
    }
    param_1[1] = (long)pvVar14;
    return;
  }
  lVar15 = *param_1;
  uVar1 = (long)pvVar3 + (param_2 - lVar15);
  if ((long)uVar1 < 0) {
                    /* WARNING: Subroutine does not return */
    FUN_00018e5c(param_1);
  }
  uVar7 = param_1[2] - lVar15;
  uVar10 = uVar7 * 2;
  if (uVar10 < uVar1 || uVar10 - uVar1 == 0) {
    uVar10 = uVar1;
  }
  if (0x3ffffffffffffffe < uVar7) {
    uVar10 = 0x7fffffffffffffff;
  }
  if (uVar10 == 0) {
    lVar5 = 0;
  }
  else {
    lVar5 = __Znwm(uVar10);
  }
  puVar13 = (undefined1 *)((long)pvVar3 + (lVar5 - lVar15));
  puVar2 = puVar13 + param_2;
  _bzero(puVar13,param_2);
  puVar6 = (undefined1 *)*param_1;
  puVar4 = (undefined1 *)param_1[1];
  uVar1 = (long)puVar4 - (long)puVar6;
  if (uVar1 == 0) goto LAB_0001980c;
  puVar11 = puVar4;
  if ((uVar1 < 0x40) || (puVar4 + (lVar15 - (lVar5 + (long)pvVar3)) < (undefined1 *)0x40)) {
LAB_000197f8:
    do {
      puVar11 = puVar11 + -1;
      puVar13 = puVar13 + -1;
      *puVar13 = *puVar11;
    } while (puVar11 != puVar6);
  }
  else {
    uVar9 = uVar1 & 0xffffffffffffffc0;
    puVar11 = puVar4 + -uVar9;
    puVar13 = puVar13 + -uVar9;
    puVar8 = (undefined8 *)(puVar4 + -0x20);
    puVar12 = (undefined8 *)((long)pvVar3 + (lVar5 - lVar15) + -0x20);
    uVar7 = uVar9;
    do {
      uVar18 = *puVar8;
      uVar17 = puVar8[3];
      uVar16 = puVar8[2];
      uVar22 = puVar8[-3];
      uVar21 = puVar8[-4];
      uVar20 = puVar8[-1];
      uVar19 = puVar8[-2];
      puVar12[1] = puVar8[1];
      *puVar12 = uVar18;
      puVar12[3] = uVar17;
      puVar12[2] = uVar16;
      puVar12[-3] = uVar22;
      puVar12[-4] = uVar21;
      puVar12[-1] = uVar20;
      puVar12[-2] = uVar19;
      puVar8 = puVar8 + -8;
      puVar12 = puVar12 + -8;
      uVar7 = uVar7 - 0x40;
    } while (uVar7 != 0);
    if (uVar1 != uVar9) goto LAB_000197f8;
  }
  puVar6 = (undefined1 *)*param_1;
LAB_0001980c:
  *param_1 = (long)puVar13;
  param_1[1] = (long)puVar2;
  lVar15 = param_1[2];
  param_1[2] = lVar5 + uVar10;
  if (puVar6 == (undefined1 *)0x0) {
    return;
  }
  __ZdlPvm(puVar6,lVar15 - (long)puVar6);
  return;
}


