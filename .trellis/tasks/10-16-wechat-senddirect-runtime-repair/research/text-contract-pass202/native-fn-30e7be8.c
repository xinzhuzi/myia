// Ghidra inferred pseudocode; requested=0x30e7be8
// entry=030e7be8 end=030e7fb7

undefined1  [16] FUN_030e7be8(long *param_1,char *param_2,long *param_3,long *param_4)

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
  ulong uVar14;
  char *pcVar15;
  undefined1 *puVar16;
  undefined1 *puVar17;
  undefined2 uVar18;
  long lVar19;
  undefined1 auVar20 [16];
  long *local_78;
  long *plStack_70;
  undefined1 *local_68;
  
  uVar14 = *(ulong *)(param_2 + 8);
  pcVar3 = *(char **)param_2;
  if (-1 < param_2[0x17]) {
    uVar14 = (ulong)(byte)param_2[0x17];
    pcVar3 = param_2;
  }
  puVar6 = (undefined1 *)FUN_000545f0(&local_78,pcVar3,uVar14);
  puVar16 = (undefined1 *)param_1[1];
  if (puVar16 == (undefined1 *)0x0) {
    puVar17 = &SUB_aaaaaaaaaaaaaaaa;
  }
  else {
    uVar10 = CONCAT17(POPCOUNT((char)((ulong)puVar16 >> 0x38)),
                      CONCAT16(POPCOUNT((char)((ulong)puVar16 >> 0x30)),
                               CONCAT15(POPCOUNT((char)((ulong)puVar16 >> 0x28)),
                                        CONCAT14(POPCOUNT((char)((ulong)puVar16 >> 0x20)),
                                                 CONCAT13(POPCOUNT((char)((ulong)puVar16 >> 0x18)),
                                                          CONCAT12(POPCOUNT((char)((ulong)puVar16 >>
                                                                                  0x10)),
                                                                   CONCAT11(POPCOUNT((char)((ulong)
                                                  puVar16 >> 8)),POPCOUNT((char)puVar16))))))));
    uVar18 = NEON_uaddlv(uVar10,1);
    uVar14 = CONCAT62((int6)((ulong)uVar10 >> 0x10),uVar18) & 0xffffffff;
    if (uVar14 < 2) {
      puVar17 = (undefined1 *)((ulong)(puVar16 + -1) & (ulong)puVar6);
    }
    else {
      puVar17 = puVar6;
      if (puVar16 <= puVar6) {
        uVar13 = 0;
        if (puVar16 != (undefined1 *)0x0) {
          uVar13 = (ulong)puVar6 / (ulong)puVar16;
        }
        puVar17 = puVar6 + -(uVar13 * (long)puVar16);
      }
    }
    puVar11 = *(undefined8 **)(*param_1 + (long)puVar17 * 8);
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
              if (iVar5 == 0) goto LAB_030e7d70;
            }
            else {
              pcVar15 = pcVar3;
              if (bVar2 == 0) {
LAB_030e7d70:
                uVar10 = 0;
                local_78 = plVar7;
                goto LAB_030e7f98;
              }
              while ((char)*plVar8 == *pcVar15) {
                plVar8 = (long *)((long)plVar8 + 1);
                uVar13 = uVar13 - 1;
                pcVar15 = pcVar15 + 1;
                if (uVar13 == 0) goto LAB_030e7d70;
              }
            }
          }
        }
        else {
          if (uVar14 < 2) {
            puVar12 = (undefined1 *)((ulong)puVar12 & (ulong)(puVar16 + -1));
          }
          else if (puVar16 <= puVar12) {
            uVar13 = 0;
            if (puVar16 != (undefined1 *)0x0) {
              uVar13 = (ulong)puVar12 / (ulong)puVar16;
            }
            puVar12 = puVar12 + -(uVar13 * (long)puVar16);
          }
          if (puVar12 != puVar17) break;
        }
        plVar7 = (long *)*plVar7;
      } while (plVar7 != (long *)0x0);
    }
  }
  plVar7 = param_1 + 2;
  local_68 = &SUB_aaaaaaaaaaaaaaaa;
  plVar8 = (long *)__Znwm(0x38);
  local_68 = (undefined1 *)((ulong)local_68 & 0xffffffffffffff00);
  *plVar8 = 0;
  plVar8[1] = (long)puVar6;
  local_78 = plVar8;
  plStack_70 = plVar7;
  if (*(char *)((long)param_3 + 0x17) < '\0') {
    FUN_00018d20(plVar8 + 2,*param_3,param_3[1]);
  }
  else {
    lVar19 = *param_3;
    plVar8[3] = param_3[1];
    plVar8[2] = lVar19;
    plVar8[4] = param_3[2];
  }
  lVar19 = *param_4;
  plVar8[6] = param_4[1];
  plVar8[5] = lVar19;
  *param_4 = 0;
  param_4[1] = 0;
  local_68 = (undefined1 *)CONCAT71(local_68._1_7_,1);
  if ((puVar16 != (undefined1 *)0x0) &&
     ((float)(param_1[3] + 1) <= *(float *)(param_1 + 4) * (float)puVar16)) goto LAB_030e7f0c;
  uVar14 = 1;
  if ((undefined1 *)0x2 < puVar16) {
    uVar14 = (ulong)(((ulong)puVar16 & (ulong)(puVar16 + -1)) != 0);
  }
  uVar14 = uVar14 | (long)puVar16 << 1;
  uVar13 = (ulong)((float)(param_1[3] + 1) / *(float *)(param_1 + 4));
  if (uVar14 <= uVar13) {
    uVar14 = uVar13;
  }
  if (uVar14 - 1 == 0) {
    uVar14 = 2;
  }
  else if ((uVar14 & uVar14 - 1) != 0) {
    uVar14 = __ZNSt3__112__next_primeEm(uVar14);
  }
  uVar13 = param_1[1];
  if (uVar13 < uVar14) {
LAB_030e7e60:
    FUN_001ff188(param_1,uVar14);
  }
  else if (uVar14 < uVar13) {
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
       uVar18 = NEON_uaddlv(uVar10,1),
       1 < (CONCAT62((int6)((ulong)uVar10 >> 0x10),uVar18) & 0xffffffff))) {
      uVar9 = __ZNSt3__112__next_primeEm();
    }
    else if (1 < uVar9) {
      uVar9 = 1L << (-LZCOUNT(uVar9 - 1) & 0x3fU);
    }
    if (uVar14 <= uVar9) {
      uVar14 = uVar9;
    }
    if (uVar14 < uVar13) goto LAB_030e7e60;
  }
  puVar16 = (undefined1 *)param_1[1];
  if (((ulong)puVar16 & (ulong)(puVar16 + -1)) == 0) {
    puVar17 = (undefined1 *)((ulong)(puVar16 + -1) & (ulong)puVar6);
  }
  else {
    puVar17 = puVar6;
    if (puVar16 <= puVar6) {
      uVar14 = 0;
      if (puVar16 != (undefined1 *)0x0) {
        uVar14 = (ulong)puVar6 / (ulong)puVar16;
      }
      puVar17 = puVar6 + -(uVar14 * (long)puVar16);
    }
  }
LAB_030e7f0c:
  plVar8 = *(long **)(*param_1 + (long)puVar17 * 8);
  if (plVar8 == (long *)0x0) {
    *local_78 = param_1[2];
    param_1[2] = (long)local_78;
    *(long **)(*param_1 + (long)puVar17 * 8) = plVar7;
    if (*local_78 != 0) {
      puVar6 = *(undefined1 **)(*local_78 + 8);
      if (((ulong)puVar16 & (ulong)(puVar16 + -1)) == 0) {
        puVar6 = (undefined1 *)((ulong)puVar6 & (ulong)(puVar16 + -1));
      }
      else if (puVar16 <= puVar6) {
        uVar14 = 0;
        if (puVar16 != (undefined1 *)0x0) {
          uVar14 = (ulong)puVar6 / (ulong)puVar16;
        }
        puVar6 = puVar6 + -(uVar14 * (long)puVar16);
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
LAB_030e7f98:
  auVar20._8_8_ = uVar10;
  auVar20._0_8_ = local_78;
  return auVar20;
}


