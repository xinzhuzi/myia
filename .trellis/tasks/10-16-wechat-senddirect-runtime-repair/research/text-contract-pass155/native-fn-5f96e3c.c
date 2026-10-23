// Ghidra inferred pseudocode; requested=0x5f96e3c
// entry=05f96e3c end=05f9708f

void FUN_05f96e3c(undefined8 *param_1,long param_2)

{
  undefined8 *puVar1;
  undefined1 *puVar2;
  ulong uVar3;
  undefined8 *puVar4;
  undefined8 *puVar5;
  ulong uVar6;
  undefined1 *puVar7;
  undefined1 *puVar8;
  ulong uVar9;
  undefined1 *puVar10;
  undefined8 uVar11;
  undefined8 uVar12;
  undefined8 uVar13;
  undefined8 uVar14;
  undefined8 uVar15;
  undefined8 uVar16;
  undefined8 uVar17;
  
  if ((*(uint *)(param_2 + 0x60) >> 4 & 1) == 0) {
    if ((*(uint *)(param_2 + 0x60) >> 3 & 1) == 0) {
      *param_1 = 0;
      param_1[1] = 0;
      param_1[2] = 0;
      return;
    }
    puVar10 = *(undefined1 **)(param_2 + 0x10);
    puVar7 = *(undefined1 **)(param_2 + 0x20);
    uVar9 = (long)puVar7 - (long)puVar10;
    if (0x7ffffffffffffff7 < uVar9) {
LAB_05f9708c:
                    /* WARNING: Subroutine does not return */
      _abort();
    }
    if (uVar9 < 0x17) {
      *(char *)((long)param_1 + 0x17) = (char)uVar9;
    }
    else {
      uVar6 = (uVar9 & 0xfffffffffffffff8) + 8;
      if ((uVar9 | 7) != 0x17) {
        uVar6 = uVar9 | 7;
      }
      puVar1 = (undefined8 *)__Znwm(uVar6 + 1);
      param_1[1] = uVar9;
      param_1[2] = uVar6 + 1 | 0x8000000000000000;
      *param_1 = puVar1;
      param_1 = puVar1;
    }
    if (puVar10 == puVar7) {
LAB_05f9703c:
      *(undefined1 *)param_1 = 0;
      return;
    }
    if ((0x3f < uVar9) && (0x3f < (ulong)((long)param_1 - (long)puVar10))) {
      uVar3 = uVar9 & 0xffffffffffffffc0;
      puVar1 = (undefined8 *)((long)param_1 + uVar3);
      puVar4 = (undefined8 *)(puVar10 + 0x20);
      puVar5 = param_1 + 4;
      uVar6 = uVar3;
      do {
        uVar11 = puVar4[-4];
        uVar13 = puVar4[-1];
        uVar12 = puVar4[-2];
        uVar15 = puVar4[1];
        uVar14 = *puVar4;
        uVar17 = puVar4[3];
        uVar16 = puVar4[2];
        puVar5[-3] = puVar4[-3];
        puVar5[-4] = uVar11;
        puVar5[-1] = uVar13;
        puVar5[-2] = uVar12;
        puVar5[1] = uVar15;
        *puVar5 = uVar14;
        puVar5[3] = uVar17;
        puVar5[2] = uVar16;
        uVar6 = uVar6 - 0x40;
        puVar4 = puVar4 + 8;
        puVar5 = puVar5 + 8;
      } while (uVar6 != 0);
      param_1 = puVar1;
      puVar10 = puVar10 + uVar3;
      if (uVar9 == uVar3) goto LAB_05f97070;
    }
    do {
      puVar2 = puVar10 + 1;
      puVar1 = (undefined8 *)((long)param_1 + 1);
      *(undefined1 *)param_1 = *puVar10;
      param_1 = puVar1;
      puVar10 = puVar2;
    } while (puVar2 != puVar7);
  }
  else {
    puVar10 = *(undefined1 **)(param_2 + 0x58);
    puVar2 = *(undefined1 **)(param_2 + 0x30);
    puVar7 = puVar10;
    if (puVar10 < puVar2) {
      *(undefined1 **)(param_2 + 0x58) = puVar2;
      puVar7 = puVar2;
    }
    puVar8 = *(undefined1 **)(param_2 + 0x28);
    uVar9 = (long)puVar7 - (long)puVar8;
    if (0x7ffffffffffffff7 < uVar9) goto LAB_05f9708c;
    if (uVar9 < 0x17) {
      *(char *)((long)param_1 + 0x17) = (char)uVar9;
    }
    else {
      uVar6 = (uVar9 & 0xfffffffffffffff8) + 8;
      if ((uVar9 | 7) != 0x17) {
        uVar6 = uVar9 | 7;
      }
      puVar1 = (undefined8 *)__Znwm(uVar6 + 1);
      param_1[1] = uVar9;
      param_1[2] = uVar6 + 1 | 0x8000000000000000;
      *param_1 = puVar1;
      param_1 = puVar1;
    }
    if (puVar8 == puVar7) goto LAB_05f9703c;
    if (puVar10 <= puVar2) {
      puVar10 = puVar2;
    }
    uVar9 = (long)puVar10 - (long)puVar8;
    if ((0x3f < uVar9) && (0x3f < (ulong)((long)param_1 - (long)puVar8))) {
      uVar3 = uVar9 & 0xffffffffffffffc0;
      puVar1 = (undefined8 *)((long)param_1 + uVar3);
      puVar4 = (undefined8 *)(puVar8 + 0x20);
      puVar5 = param_1 + 4;
      uVar6 = uVar3;
      do {
        uVar11 = puVar4[-4];
        uVar13 = puVar4[-1];
        uVar12 = puVar4[-2];
        uVar15 = puVar4[1];
        uVar14 = *puVar4;
        uVar17 = puVar4[3];
        uVar16 = puVar4[2];
        puVar5[-3] = puVar4[-3];
        puVar5[-4] = uVar11;
        puVar5[-1] = uVar13;
        puVar5[-2] = uVar12;
        puVar5[1] = uVar15;
        *puVar5 = uVar14;
        puVar5[3] = uVar17;
        puVar5[2] = uVar16;
        uVar6 = uVar6 - 0x40;
        puVar4 = puVar4 + 8;
        puVar5 = puVar5 + 8;
      } while (uVar6 != 0);
      param_1 = puVar1;
      puVar8 = puVar8 + uVar3;
      if (uVar9 == uVar3) goto LAB_05f97070;
    }
    do {
      puVar10 = puVar8 + 1;
      puVar1 = (undefined8 *)((long)param_1 + 1);
      *(undefined1 *)param_1 = *puVar8;
      param_1 = puVar1;
      puVar8 = puVar10;
    } while (puVar10 != puVar7);
  }
LAB_05f97070:
  *(undefined1 *)puVar1 = 0;
  return;
}


