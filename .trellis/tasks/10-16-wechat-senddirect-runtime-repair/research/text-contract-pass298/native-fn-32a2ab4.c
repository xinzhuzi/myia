// Ghidra inferred pseudocode; requested=0x32a2ab4
// entry=032a2ab4 end=032a2da3

long * FUN_032a2ab4(long *param_1,uint *param_2,undefined4 *param_3,long *param_4)

{
  uint uVar1;
  uint uVar2;
  long *plVar3;
  ulong uVar4;
  ulong uVar5;
  long *plVar6;
  ulong uVar7;
  long lVar8;
  long *plVar9;
  undefined1 *puVar10;
  undefined1 *puVar11;
  uint uVar12;
  undefined1 *puVar13;
  undefined1 *puVar14;
  undefined2 uVar15;
  undefined8 uVar16;
  
  uVar1 = *param_2;
  puVar11 = (undefined1 *)(ulong)uVar1;
  puVar13 = (undefined1 *)param_1[1];
  if (puVar13 == (undefined1 *)0x0) {
    puVar14 = &SUB_aaaaaaaaaaaaaaaa;
  }
  else {
    uVar16 = CONCAT17(POPCOUNT((char)((ulong)puVar13 >> 0x38)),
                      CONCAT16(POPCOUNT((char)((ulong)puVar13 >> 0x30)),
                               CONCAT15(POPCOUNT((char)((ulong)puVar13 >> 0x28)),
                                        CONCAT14(POPCOUNT((char)((ulong)puVar13 >> 0x20)),
                                                 CONCAT13(POPCOUNT((char)((ulong)puVar13 >> 0x18)),
                                                          CONCAT12(POPCOUNT((char)((ulong)puVar13 >>
                                                                                  0x10)),
                                                                   CONCAT11(POPCOUNT((char)((ulong)
                                                  puVar13 >> 8)),POPCOUNT((char)puVar13))))))));
    uVar15 = NEON_uaddlv(uVar16,1);
    uVar5 = CONCAT62((int6)((ulong)uVar16 >> 0x10),uVar15) & 0xffffffff;
    uVar12 = (uint)puVar13;
    if (uVar5 < 2) {
      puVar14 = (undefined1 *)(ulong)(uVar12 - 1 & uVar1);
    }
    else {
      puVar14 = puVar11;
      if (puVar13 <= puVar11) {
        uVar2 = 0;
        if (uVar12 != 0) {
          uVar2 = uVar1 / uVar12;
        }
        puVar14 = (undefined1 *)(ulong)(uVar1 - uVar2 * uVar12);
      }
    }
    plVar9 = *(long **)(*param_1 + (long)puVar14 * 8);
    if ((plVar9 != (long *)0x0) && (plVar9 = (long *)*plVar9, plVar9 != (long *)0x0)) {
      do {
        puVar10 = (undefined1 *)plVar9[1];
        if (puVar10 == puVar11) {
          if (*(uint *)(plVar9 + 2) == uVar1) {
            return plVar9;
          }
        }
        else {
          if (uVar5 < 2) {
            puVar10 = (undefined1 *)((ulong)puVar10 & (ulong)(puVar13 + -1));
          }
          else if (puVar13 <= puVar10) {
            uVar7 = 0;
            if (puVar13 != (undefined1 *)0x0) {
              uVar7 = (ulong)puVar10 / (ulong)puVar13;
            }
            puVar10 = puVar10 + -(uVar7 * (long)puVar13);
          }
          if (puVar10 != puVar14) break;
        }
        plVar9 = (long *)*plVar9;
      } while (plVar9 != (long *)0x0);
    }
  }
  plVar9 = param_1 + 2;
  plVar3 = (long *)__Znwm(0x30);
  *plVar3 = 0;
  plVar3[1] = (long)puVar11;
  *(undefined4 *)(plVar3 + 2) = *param_3;
  lVar8 = *param_4;
  plVar3[4] = param_4[1];
  plVar3[3] = lVar8;
  plVar3[5] = param_4[2];
  param_4[1] = 0;
  param_4[2] = 0;
  *param_4 = 0;
  if ((puVar13 == (undefined1 *)0x0) ||
     (*(float *)(param_1 + 4) * (float)puVar13 < (float)(param_1[3] + 1))) {
    uVar5 = 1;
    if ((undefined1 *)0x2 < puVar13) {
      uVar5 = (ulong)(((ulong)puVar13 & (ulong)(puVar13 + -1)) != 0);
    }
    uVar5 = uVar5 | (long)puVar13 << 1;
    uVar7 = (ulong)((float)(param_1[3] + 1) / *(float *)(param_1 + 4));
    if (uVar5 <= uVar7) {
      uVar5 = uVar7;
    }
    if (uVar5 - 1 == 0) {
      uVar5 = 2;
    }
    else if ((uVar5 & uVar5 - 1) != 0) {
      uVar5 = __ZNSt3__112__next_primeEm(uVar5);
    }
    uVar7 = param_1[1];
    if (uVar7 < uVar5) {
LAB_032a2c58:
      FUN_001ff188(param_1,uVar5);
    }
    else if (uVar5 < uVar7) {
      uVar4 = (ulong)((float)(ulong)param_1[3] / *(float *)(param_1 + 4));
      if ((uVar7 < 3) ||
         (uVar16 = CONCAT17(POPCOUNT((char)(uVar7 >> 0x38)),
                            CONCAT16(POPCOUNT((char)(uVar7 >> 0x30)),
                                     CONCAT15(POPCOUNT((char)(uVar7 >> 0x28)),
                                              CONCAT14(POPCOUNT((char)(uVar7 >> 0x20)),
                                                       CONCAT13(POPCOUNT((char)(uVar7 >> 0x18)),
                                                                CONCAT12(POPCOUNT((char)(uVar7 >> 
                                                  0x10)),CONCAT11(POPCOUNT((char)(uVar7 >> 8)),
                                                                  POPCOUNT((char)uVar7)))))))),
         uVar15 = NEON_uaddlv(uVar16,1),
         1 < (CONCAT62((int6)((ulong)uVar16 >> 0x10),uVar15) & 0xffffffff))) {
        uVar4 = __ZNSt3__112__next_primeEm();
      }
      else if (1 < uVar4) {
        uVar4 = 1L << (-LZCOUNT(uVar4 - 1) & 0x3fU);
      }
      if (uVar5 <= uVar4) {
        uVar5 = uVar4;
      }
      if (uVar5 < uVar7) goto LAB_032a2c58;
    }
    puVar13 = (undefined1 *)param_1[1];
    if (((ulong)puVar13 & (ulong)(puVar13 + -1)) == 0) {
      puVar14 = (undefined1 *)(ulong)((int)puVar13 - 1U & uVar1);
    }
    else {
      puVar14 = puVar11;
      if (puVar13 <= puVar11) {
        uVar5 = 0;
        if (puVar13 != (undefined1 *)0x0) {
          uVar5 = (ulong)puVar11 / (ulong)puVar13;
        }
        puVar14 = puVar11 + -(uVar5 * (long)puVar13);
      }
    }
  }
  lVar8 = *param_1;
  plVar6 = *(long **)(lVar8 + (long)puVar14 * 8);
  if (plVar6 == (long *)0x0) {
    *plVar3 = *plVar9;
    *plVar9 = (long)plVar3;
    *(long **)(lVar8 + (long)puVar14 * 8) = plVar9;
    if (*plVar3 == 0) goto LAB_032a2d74;
    puVar11 = *(undefined1 **)(*plVar3 + 8);
    if (((ulong)puVar13 & (ulong)(puVar13 + -1)) == 0) {
      puVar11 = (undefined1 *)((ulong)puVar11 & (ulong)(puVar13 + -1));
    }
    else if (puVar13 <= puVar11) {
      uVar5 = 0;
      if (puVar13 != (undefined1 *)0x0) {
        uVar5 = (ulong)puVar11 / (ulong)puVar13;
      }
      puVar11 = puVar11 + -(uVar5 * (long)puVar13);
    }
    plVar6 = (long *)(*param_1 + (long)puVar11 * 8);
  }
  else {
    *plVar3 = *plVar6;
  }
  *plVar6 = (long)plVar3;
LAB_032a2d74:
  param_1[3] = param_1[3] + 1;
  return plVar3;
}


