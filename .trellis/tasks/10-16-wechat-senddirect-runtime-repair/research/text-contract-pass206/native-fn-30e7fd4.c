// Ghidra inferred pseudocode; requested=0x30e7fd4
// entry=030e7fd4 end=030e8367

undefined1  [16] FUN_030e7fd4(long *param_1,char *param_2,undefined8 param_3,undefined8 param_4)

{
  size_t sVar1;
  byte bVar2;
  char *pcVar3;
  size_t sVar4;
  int iVar5;
  undefined1 *puVar6;
  long *plVar7;
  ulong uVar8;
  undefined8 uVar9;
  undefined8 *puVar10;
  undefined1 *puVar11;
  ulong uVar12;
  ulong uVar13;
  long *plVar14;
  char *pcVar15;
  undefined1 *puVar16;
  undefined1 *puVar17;
  undefined2 uVar18;
  undefined1 auVar19 [16];
  long *local_78;
  undefined1 *local_70;
  undefined1 *puStack_68;
  
  uVar13 = *(ulong *)(param_2 + 8);
  pcVar3 = *(char **)param_2;
  if (-1 < param_2[0x17]) {
    uVar13 = (ulong)(byte)param_2[0x17];
    pcVar3 = param_2;
  }
  puVar6 = (undefined1 *)FUN_000545f0(&local_78,pcVar3,uVar13);
  puVar16 = (undefined1 *)param_1[1];
  if (puVar16 == (undefined1 *)0x0) {
    puVar17 = &SUB_aaaaaaaaaaaaaaaa;
  }
  else {
    uVar9 = CONCAT17(POPCOUNT((char)((ulong)puVar16 >> 0x38)),
                     CONCAT16(POPCOUNT((char)((ulong)puVar16 >> 0x30)),
                              CONCAT15(POPCOUNT((char)((ulong)puVar16 >> 0x28)),
                                       CONCAT14(POPCOUNT((char)((ulong)puVar16 >> 0x20)),
                                                CONCAT13(POPCOUNT((char)((ulong)puVar16 >> 0x18)),
                                                         CONCAT12(POPCOUNT((char)((ulong)puVar16 >>
                                                                                 0x10)),
                                                                  CONCAT11(POPCOUNT((char)((ulong)
                                                  puVar16 >> 8)),POPCOUNT((char)puVar16))))))));
    uVar18 = NEON_uaddlv(uVar9,1);
    uVar13 = CONCAT62((int6)((ulong)uVar9 >> 0x10),uVar18) & 0xffffffff;
    if (uVar13 < 2) {
      puVar17 = (undefined1 *)((ulong)(puVar16 + -1) & (ulong)puVar6);
    }
    else {
      puVar17 = puVar6;
      if (puVar16 <= puVar6) {
        uVar12 = 0;
        if (puVar16 != (undefined1 *)0x0) {
          uVar12 = (ulong)puVar6 / (ulong)puVar16;
        }
        puVar17 = puVar6 + -(uVar12 * (long)puVar16);
      }
    }
    puVar10 = *(undefined8 **)(*param_1 + (long)puVar17 * 8);
    if ((puVar10 != (undefined8 *)0x0) && (plVar7 = (long *)*puVar10, plVar7 != (long *)0x0)) {
      sVar4 = *(size_t *)(param_2 + 8);
      pcVar3 = *(char **)param_2;
      if (-1 < param_2[0x17]) {
        sVar4 = (ulong)(byte)param_2[0x17];
        pcVar3 = param_2;
      }
      do {
        puVar11 = (undefined1 *)plVar7[1];
        if (puVar11 == puVar6) {
          bVar2 = *(byte *)((long)plVar7 + 0x27);
          uVar12 = (ulong)bVar2;
          sVar1 = plVar7[3];
          if (-1 < (char)bVar2) {
            sVar1 = uVar12;
          }
          if (sVar1 == sVar4) {
            plVar14 = plVar7 + 2;
            if ((char)bVar2 < '\0') {
              iVar5 = _memcmp((void *)*plVar14,pcVar3,plVar7[3]);
              if (iVar5 == 0) goto LAB_030e8158;
            }
            else {
              pcVar15 = pcVar3;
              if (bVar2 == 0) {
LAB_030e8158:
                uVar9 = 0;
                local_78 = plVar7;
                goto LAB_030e8348;
              }
              while ((char)*plVar14 == *pcVar15) {
                plVar14 = (long *)((long)plVar14 + 1);
                uVar12 = uVar12 - 1;
                pcVar15 = pcVar15 + 1;
                if (uVar12 == 0) goto LAB_030e8158;
              }
            }
          }
        }
        else {
          if (uVar13 < 2) {
            puVar11 = (undefined1 *)((ulong)puVar11 & (ulong)(puVar16 + -1));
          }
          else if (puVar16 <= puVar11) {
            uVar12 = 0;
            if (puVar16 != (undefined1 *)0x0) {
              uVar12 = (ulong)puVar11 / (ulong)puVar16;
            }
            puVar11 = puVar11 + -(uVar12 * (long)puVar16);
          }
          if (puVar11 != puVar17) break;
        }
        plVar7 = (long *)*plVar7;
      } while (plVar7 != (long *)0x0);
    }
  }
  local_70 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_68 = &SUB_aaaaaaaaaaaaaaaa;
  local_78 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_030e8380(&local_78,param_1,puVar6,param_3,param_4);
  if ((puVar16 != (undefined1 *)0x0) &&
     ((float)(param_1[3] + 1) <= *(float *)(param_1 + 4) * (float)puVar16)) goto LAB_030e82b4;
  uVar13 = 1;
  if ((undefined1 *)0x2 < puVar16) {
    uVar13 = (ulong)(((ulong)puVar16 & (ulong)(puVar16 + -1)) != 0);
  }
  uVar13 = uVar13 | (long)puVar16 << 1;
  uVar12 = (ulong)((float)(param_1[3] + 1) / *(float *)(param_1 + 4));
  if (uVar13 <= uVar12) {
    uVar13 = uVar12;
  }
  if (uVar13 - 1 == 0) {
    uVar13 = 2;
  }
  else if ((uVar13 & uVar13 - 1) != 0) {
    uVar13 = __ZNSt3__112__next_primeEm(uVar13);
  }
  uVar12 = param_1[1];
  if (uVar12 < uVar13) {
LAB_030e8208:
    FUN_001ff188(param_1,uVar13);
  }
  else if (uVar13 < uVar12) {
    uVar8 = (ulong)((float)(ulong)param_1[3] / *(float *)(param_1 + 4));
    if ((uVar12 < 3) ||
       (uVar9 = CONCAT17(POPCOUNT((char)(uVar12 >> 0x38)),
                         CONCAT16(POPCOUNT((char)(uVar12 >> 0x30)),
                                  CONCAT15(POPCOUNT((char)(uVar12 >> 0x28)),
                                           CONCAT14(POPCOUNT((char)(uVar12 >> 0x20)),
                                                    CONCAT13(POPCOUNT((char)(uVar12 >> 0x18)),
                                                             CONCAT12(POPCOUNT((char)(uVar12 >> 0x10
                                                                                     )),
                                                                      CONCAT11(POPCOUNT((char)(
                                                  uVar12 >> 8)),POPCOUNT((char)uVar12)))))))),
       uVar18 = NEON_uaddlv(uVar9,1),
       1 < (CONCAT62((int6)((ulong)uVar9 >> 0x10),uVar18) & 0xffffffff))) {
      uVar8 = __ZNSt3__112__next_primeEm();
    }
    else if (1 < uVar8) {
      uVar8 = 1L << (-LZCOUNT(uVar8 - 1) & 0x3fU);
    }
    if (uVar13 <= uVar8) {
      uVar13 = uVar8;
    }
    if (uVar13 < uVar12) goto LAB_030e8208;
  }
  puVar16 = (undefined1 *)param_1[1];
  if (((ulong)puVar16 & (ulong)(puVar16 + -1)) == 0) {
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
LAB_030e82b4:
  plVar7 = *(long **)(*param_1 + (long)puVar17 * 8);
  if (plVar7 == (long *)0x0) {
    plVar7 = param_1 + 2;
    *local_78 = *plVar7;
    *plVar7 = (long)local_78;
    *(long **)(*param_1 + (long)puVar17 * 8) = plVar7;
    if (*local_78 != 0) {
      puVar6 = *(undefined1 **)(*local_78 + 8);
      if (((ulong)puVar16 & (ulong)(puVar16 + -1)) == 0) {
        puVar6 = (undefined1 *)((ulong)puVar6 & (ulong)(puVar16 + -1));
      }
      else if (puVar16 <= puVar6) {
        uVar13 = 0;
        if (puVar16 != (undefined1 *)0x0) {
          uVar13 = (ulong)puVar6 / (ulong)puVar16;
        }
        puVar6 = puVar6 + -(uVar13 * (long)puVar16);
      }
      *(long **)(*param_1 + (long)puVar6 * 8) = local_78;
    }
  }
  else {
    *local_78 = *plVar7;
    *plVar7 = (long)local_78;
  }
  param_1[3] = param_1[3] + 1;
  uVar9 = 1;
LAB_030e8348:
  auVar19._8_8_ = uVar9;
  auVar19._0_8_ = local_78;
  return auVar19;
}


