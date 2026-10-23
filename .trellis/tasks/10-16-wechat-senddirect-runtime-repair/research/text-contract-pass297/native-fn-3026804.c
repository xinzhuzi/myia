// Ghidra inferred pseudocode; requested=0x3026804
// entry=03026804 end=03026ae3

long * FUN_03026804(long *param_1,uint *param_2,undefined8 param_3,undefined8 *param_4)

{
  uint uVar1;
  uint uVar2;
  ulong uVar3;
  long *plVar4;
  undefined1 *puVar5;
  long *plVar6;
  ulong uVar7;
  long lVar8;
  long *plVar9;
  undefined1 *puVar10;
  undefined1 *puVar11;
  uint uVar12;
  undefined1 *puVar13;
  undefined2 uVar14;
  undefined8 uVar15;
  
  uVar1 = *param_2;
  puVar11 = (undefined1 *)(ulong)uVar1;
  puVar13 = (undefined1 *)param_1[1];
  if (puVar13 == (undefined1 *)0x0) {
    puVar5 = &SUB_aaaaaaaaaaaaaaaa;
  }
  else {
    uVar15 = CONCAT17(POPCOUNT((char)((ulong)puVar13 >> 0x38)),
                      CONCAT16(POPCOUNT((char)((ulong)puVar13 >> 0x30)),
                               CONCAT15(POPCOUNT((char)((ulong)puVar13 >> 0x28)),
                                        CONCAT14(POPCOUNT((char)((ulong)puVar13 >> 0x20)),
                                                 CONCAT13(POPCOUNT((char)((ulong)puVar13 >> 0x18)),
                                                          CONCAT12(POPCOUNT((char)((ulong)puVar13 >>
                                                                                  0x10)),
                                                                   CONCAT11(POPCOUNT((char)((ulong)
                                                  puVar13 >> 8)),POPCOUNT((char)puVar13))))))));
    uVar14 = NEON_uaddlv(uVar15,1);
    uVar7 = CONCAT62((int6)((ulong)uVar15 >> 0x10),uVar14) & 0xffffffff;
    uVar12 = (uint)puVar13;
    if (uVar7 < 2) {
      puVar5 = (undefined1 *)(ulong)(uVar12 - 1 & uVar1);
    }
    else {
      puVar5 = puVar11;
      if (puVar13 <= puVar11) {
        uVar2 = 0;
        if (uVar12 != 0) {
          uVar2 = uVar1 / uVar12;
        }
        puVar5 = (undefined1 *)(ulong)(uVar1 - uVar2 * uVar12);
      }
    }
    plVar9 = *(long **)(*param_1 + (long)puVar5 * 8);
    if ((plVar9 != (long *)0x0) && (plVar9 = (long *)*plVar9, plVar9 != (long *)0x0)) {
      do {
        puVar10 = (undefined1 *)plVar9[1];
        if (puVar10 == puVar11) {
          if (*(uint *)(plVar9 + 2) == uVar1) {
            return plVar9;
          }
        }
        else {
          if (uVar7 < 2) {
            puVar10 = (undefined1 *)((ulong)puVar10 & (ulong)(puVar13 + -1));
          }
          else if (puVar13 <= puVar10) {
            uVar3 = 0;
            if (puVar13 != (undefined1 *)0x0) {
              uVar3 = (ulong)puVar10 / (ulong)puVar13;
            }
            puVar10 = puVar10 + -(uVar3 * (long)puVar13);
          }
          if (puVar10 != puVar5) break;
        }
        plVar9 = (long *)*plVar9;
      } while (plVar9 != (long *)0x0);
    }
  }
  plVar9 = param_1 + 2;
  plVar4 = (long *)__Znwm(0x30);
  *plVar4 = 0;
  plVar4[1] = (long)puVar11;
  *(undefined4 *)(plVar4 + 2) = *(undefined4 *)*param_4;
  plVar4[4] = 0;
  plVar4[5] = 0;
  plVar4[3] = 0;
  if ((puVar13 == (undefined1 *)0x0) ||
     (*(float *)(param_1 + 4) * (float)puVar13 < (float)(param_1[3] + 1))) {
    uVar7 = 1;
    if ((undefined1 *)0x2 < puVar13) {
      uVar7 = (ulong)(((ulong)puVar13 & (ulong)(puVar13 + -1)) != 0);
    }
    puVar5 = (undefined1 *)(uVar7 | (long)puVar13 << 1);
    puVar10 = (undefined1 *)(long)((float)(param_1[3] + 1) / *(float *)(param_1 + 4));
    if (puVar5 <= puVar10) {
      puVar5 = puVar10;
    }
    if (puVar5 + -1 == (undefined1 *)0x0) {
      puVar5 = (undefined1 *)0x2;
    }
    else if (((ulong)puVar5 & (ulong)(puVar5 + -1)) != 0) {
      puVar5 = (undefined1 *)__ZNSt3__112__next_primeEm(puVar5);
      puVar13 = (undefined1 *)param_1[1];
    }
    if (puVar13 < puVar5) {
LAB_030269a0:
      FUN_001ff188(param_1,puVar5);
    }
    else if (puVar5 < puVar13) {
      puVar10 = (undefined1 *)(long)((float)(ulong)param_1[3] / *(float *)(param_1 + 4));
      if ((puVar13 < (undefined1 *)0x3) ||
         (uVar15 = CONCAT17(POPCOUNT((char)((ulong)puVar13 >> 0x38)),
                            CONCAT16(POPCOUNT((char)((ulong)puVar13 >> 0x30)),
                                     CONCAT15(POPCOUNT((char)((ulong)puVar13 >> 0x28)),
                                              CONCAT14(POPCOUNT((char)((ulong)puVar13 >> 0x20)),
                                                       CONCAT13(POPCOUNT((char)((ulong)puVar13 >>
                                                                               0x18)),
                                                                CONCAT12(POPCOUNT((char)((ulong)
                                                  puVar13 >> 0x10)),
                                                  CONCAT11(POPCOUNT((char)((ulong)puVar13 >> 8)),
                                                           POPCOUNT((char)puVar13)))))))),
         uVar14 = NEON_uaddlv(uVar15,1),
         1 < (CONCAT62((int6)((ulong)uVar15 >> 0x10),uVar14) & 0xffffffff))) {
        puVar10 = (undefined1 *)__ZNSt3__112__next_primeEm();
      }
      else if ((undefined1 *)0x1 < puVar10) {
        puVar10 = (undefined1 *)(1L << (-LZCOUNT(puVar10 + -1) & 0x3fU));
      }
      if (puVar5 <= puVar10) {
        puVar5 = puVar10;
      }
      if (puVar5 < puVar13) goto LAB_030269a0;
    }
    puVar13 = (undefined1 *)param_1[1];
    if (((ulong)puVar13 & (ulong)(puVar13 + -1)) == 0) {
      puVar5 = (undefined1 *)(ulong)((int)puVar13 - 1U & uVar1);
    }
    else {
      puVar5 = puVar11;
      if (puVar13 <= puVar11) {
        uVar7 = 0;
        if (puVar13 != (undefined1 *)0x0) {
          uVar7 = (ulong)puVar11 / (ulong)puVar13;
        }
        puVar5 = puVar11 + -(uVar7 * (long)puVar13);
      }
    }
  }
  lVar8 = *param_1;
  plVar6 = *(long **)(lVar8 + (long)puVar5 * 8);
  if (plVar6 == (long *)0x0) {
    *plVar4 = *plVar9;
    *plVar9 = (long)plVar4;
    *(long **)(lVar8 + (long)puVar5 * 8) = plVar9;
    if (*plVar4 == 0) goto LAB_03026ab4;
    puVar11 = *(undefined1 **)(*plVar4 + 8);
    if (((ulong)puVar13 & (ulong)(puVar13 + -1)) == 0) {
      puVar11 = (undefined1 *)((ulong)puVar11 & (ulong)(puVar13 + -1));
    }
    else if (puVar13 <= puVar11) {
      uVar7 = 0;
      if (puVar13 != (undefined1 *)0x0) {
        uVar7 = (ulong)puVar11 / (ulong)puVar13;
      }
      puVar11 = puVar11 + -(uVar7 * (long)puVar13);
    }
    plVar6 = (long *)(*param_1 + (long)puVar11 * 8);
  }
  else {
    *plVar4 = *plVar6;
  }
  *plVar6 = (long)plVar4;
LAB_03026ab4:
  param_1[3] = param_1[3] + 1;
  return plVar4;
}


