// Ghidra inferred pseudocode; requested=0x2877ec4
// entry=02877ec4 end=0287829f

undefined1  [16] FUN_02877ec4(long *param_1,char *param_2,undefined8 param_3,undefined8 *param_4)

{
  size_t sVar1;
  byte bVar2;
  char *pcVar3;
  size_t sVar4;
  int iVar5;
  undefined1 *puVar6;
  long *plVar7;
  long *plVar8;
  ulong uVar9;
  undefined8 uVar10;
  undefined8 *puVar11;
  undefined1 *puVar12;
  ulong uVar13;
  long *plVar14;
  ulong uVar15;
  char *pcVar16;
  undefined1 *puVar17;
  undefined1 *puVar18;
  undefined2 uVar19;
  long lVar20;
  long lVar21;
  undefined1 auVar22 [16];
  long *local_78;
  long *plStack_70;
  undefined1 *local_68;
  
  uVar15 = *(ulong *)(param_2 + 8);
  pcVar3 = *(char **)param_2;
  if (-1 < param_2[0x17]) {
    uVar15 = (ulong)(byte)param_2[0x17];
    pcVar3 = param_2;
  }
  puVar6 = (undefined1 *)FUN_000545f0(&local_78,pcVar3,uVar15);
  puVar17 = (undefined1 *)param_1[1];
  if (puVar17 == (undefined1 *)0x0) {
    puVar18 = &SUB_aaaaaaaaaaaaaaaa;
  }
  else {
    uVar10 = CONCAT17(POPCOUNT((char)((ulong)puVar17 >> 0x38)),
                      CONCAT16(POPCOUNT((char)((ulong)puVar17 >> 0x30)),
                               CONCAT15(POPCOUNT((char)((ulong)puVar17 >> 0x28)),
                                        CONCAT14(POPCOUNT((char)((ulong)puVar17 >> 0x20)),
                                                 CONCAT13(POPCOUNT((char)((ulong)puVar17 >> 0x18)),
                                                          CONCAT12(POPCOUNT((char)((ulong)puVar17 >>
                                                                                  0x10)),
                                                                   CONCAT11(POPCOUNT((char)((ulong)
                                                  puVar17 >> 8)),POPCOUNT((char)puVar17))))))));
    uVar19 = NEON_uaddlv(uVar10,1);
    uVar15 = CONCAT62((int6)((ulong)uVar10 >> 0x10),uVar19) & 0xffffffff;
    if (uVar15 < 2) {
      puVar18 = (undefined1 *)((ulong)(puVar17 + -1) & (ulong)puVar6);
    }
    else {
      puVar18 = puVar6;
      if (puVar17 <= puVar6) {
        uVar13 = 0;
        if (puVar17 != (undefined1 *)0x0) {
          uVar13 = (ulong)puVar6 / (ulong)puVar17;
        }
        puVar18 = puVar6 + -(uVar13 * (long)puVar17);
      }
    }
    puVar11 = *(undefined8 **)(*param_1 + (long)puVar18 * 8);
    if ((puVar11 != (undefined8 *)0x0) && (plVar7 = (long *)*puVar11, plVar7 != (long *)0x0)) {
      sVar4 = *(size_t *)(param_2 + 8);
      pcVar3 = *(char **)param_2;
      if (-1 < param_2[0x17]) {
        sVar4 = (ulong)(byte)param_2[0x17];
        pcVar3 = param_2;
      }
      do {
        puVar12 = (undefined1 *)plVar7[1];
        if (puVar12 == puVar6) {
          bVar2 = *(byte *)((long)plVar7 + 0x27);
          uVar13 = (ulong)bVar2;
          sVar1 = plVar7[3];
          if (-1 < (char)bVar2) {
            sVar1 = uVar13;
          }
          if (sVar1 == sVar4) {
            plVar8 = plVar7 + 2;
            if ((char)bVar2 < '\0') {
              iVar5 = _memcmp((void *)*plVar8,pcVar3,plVar7[3]);
              if (iVar5 == 0) goto LAB_02878040;
            }
            else {
              pcVar16 = pcVar3;
              if (bVar2 == 0) {
LAB_02878040:
                uVar10 = 0;
                local_78 = plVar7;
                goto LAB_02878280;
              }
              while ((char)*plVar8 == *pcVar16) {
                plVar8 = (long *)((long)plVar8 + 1);
                uVar13 = uVar13 - 1;
                pcVar16 = pcVar16 + 1;
                if (uVar13 == 0) goto LAB_02878040;
              }
            }
          }
        }
        else {
          if (uVar15 < 2) {
            puVar12 = (undefined1 *)((ulong)puVar12 & (ulong)(puVar17 + -1));
          }
          else if (puVar17 <= puVar12) {
            uVar13 = 0;
            if (puVar17 != (undefined1 *)0x0) {
              uVar13 = (ulong)puVar12 / (ulong)puVar17;
            }
            puVar12 = puVar12 + -(uVar13 * (long)puVar17);
          }
          if (puVar12 != puVar18) break;
        }
        plVar7 = (long *)*plVar7;
      } while (plVar7 != (long *)0x0);
    }
  }
  plVar7 = param_1 + 2;
  local_68 = &SUB_aaaaaaaaaaaaaaaa;
  plVar8 = (long *)__Znwm(0x98);
  local_68 = (undefined1 *)((ulong)local_68 & 0xffffffffffffff00);
  *plVar8 = 0;
  plVar8[1] = (long)puVar6;
  plVar14 = (long *)*param_4;
  local_78 = plVar8;
  plStack_70 = plVar7;
  if (*(char *)((long)plVar14 + 0x17) < '\0') {
    FUN_00018d20(plVar8 + 2,*plVar14,plVar14[1]);
  }
  else {
    lVar21 = plVar14[1];
    lVar20 = *plVar14;
    plVar8[4] = plVar14[2];
    plVar8[3] = lVar21;
    plVar8[2] = lVar20;
  }
  plVar8[0x12] = 0;
  plVar8[0x11] = 0;
  plVar8[0x10] = 0;
  plVar8[0xf] = 0;
  plVar8[0xe] = 0;
  plVar8[0xd] = 0;
  plVar8[0xc] = 0;
  plVar8[0xb] = 0;
  plVar8[10] = 0;
  plVar8[9] = 0;
  plVar8[8] = 0;
  plVar8[7] = 0;
  plVar8[6] = 0;
  plVar8[5] = 0;
  local_68 = (undefined1 *)CONCAT71(local_68._1_7_,1);
  if ((puVar17 != (undefined1 *)0x0) &&
     ((float)(param_1[3] + 1) <= *(float *)(param_1 + 4) * (float)puVar17)) goto LAB_028781f4;
  uVar15 = 1;
  if ((undefined1 *)0x2 < puVar17) {
    uVar15 = (ulong)(((ulong)puVar17 & (ulong)(puVar17 + -1)) != 0);
  }
  uVar15 = uVar15 | (long)puVar17 << 1;
  uVar13 = (ulong)((float)(param_1[3] + 1) / *(float *)(param_1 + 4));
  if (uVar15 <= uVar13) {
    uVar15 = uVar13;
  }
  if (uVar15 - 1 == 0) {
    uVar15 = 2;
  }
  else if ((uVar15 & uVar15 - 1) != 0) {
    uVar15 = __ZNSt3__112__next_primeEm(uVar15);
  }
  uVar13 = param_1[1];
  if (uVar13 < uVar15) {
LAB_02878148:
    FUN_001ff188(param_1,uVar15);
  }
  else if (uVar15 < uVar13) {
    uVar9 = (ulong)((float)(ulong)param_1[3] / *(float *)(param_1 + 4));
    if ((uVar13 < 3) ||
       (uVar10 = CONCAT17(POPCOUNT((char)(uVar13 >> 0x38)),
                          CONCAT16(POPCOUNT((char)(uVar13 >> 0x30)),
                                   CONCAT15(POPCOUNT((char)(uVar13 >> 0x28)),
                                            CONCAT14(POPCOUNT((char)(uVar13 >> 0x20)),
                                                     CONCAT13(POPCOUNT((char)(uVar13 >> 0x18)),
                                                              CONCAT12(POPCOUNT((char)(uVar13 >>
                                                                                      0x10)),
                                                                       CONCAT11(POPCOUNT((char)(
                                                  uVar13 >> 8)),POPCOUNT((char)uVar13)))))))),
       uVar19 = NEON_uaddlv(uVar10,1),
       1 < (CONCAT62((int6)((ulong)uVar10 >> 0x10),uVar19) & 0xffffffff))) {
      uVar9 = __ZNSt3__112__next_primeEm();
    }
    else if (1 < uVar9) {
      uVar9 = 1L << (-LZCOUNT(uVar9 - 1) & 0x3fU);
    }
    if (uVar15 <= uVar9) {
      uVar15 = uVar9;
    }
    if (uVar15 < uVar13) goto LAB_02878148;
  }
  puVar17 = (undefined1 *)param_1[1];
  if (((ulong)puVar17 & (ulong)(puVar17 + -1)) == 0) {
    puVar18 = (undefined1 *)((ulong)(puVar17 + -1) & (ulong)puVar6);
  }
  else {
    puVar18 = puVar6;
    if (puVar17 <= puVar6) {
      uVar15 = 0;
      if (puVar17 != (undefined1 *)0x0) {
        uVar15 = (ulong)puVar6 / (ulong)puVar17;
      }
      puVar18 = puVar6 + -(uVar15 * (long)puVar17);
    }
  }
LAB_028781f4:
  plVar8 = *(long **)(*param_1 + (long)puVar18 * 8);
  if (plVar8 == (long *)0x0) {
    *local_78 = param_1[2];
    param_1[2] = (long)local_78;
    *(long **)(*param_1 + (long)puVar18 * 8) = plVar7;
    if (*local_78 != 0) {
      puVar6 = *(undefined1 **)(*local_78 + 8);
      if (((ulong)puVar17 & (ulong)(puVar17 + -1)) == 0) {
        puVar6 = (undefined1 *)((ulong)puVar6 & (ulong)(puVar17 + -1));
      }
      else if (puVar17 <= puVar6) {
        uVar15 = 0;
        if (puVar17 != (undefined1 *)0x0) {
          uVar15 = (ulong)puVar6 / (ulong)puVar17;
        }
        puVar6 = puVar6 + -(uVar15 * (long)puVar17);
      }
      *(long **)(*param_1 + (long)puVar6 * 8) = local_78;
    }
  }
  else {
    *local_78 = *plVar8;
    *plVar8 = (long)local_78;
  }
  param_1[3] = param_1[3] + 1;
  uVar10 = 1;
LAB_02878280:
  auVar22._8_8_ = uVar10;
  auVar22._0_8_ = local_78;
  return auVar22;
}


