// Ghidra inferred pseudocode; requested=0xda468c
// entry=00da468c end=00da4817

long * FUN_00da468c(long *param_1,char *param_2)

{
  size_t sVar1;
  byte bVar2;
  ulong uVar3;
  char *pcVar4;
  size_t sVar5;
  int iVar6;
  ulong uVar7;
  long *plVar8;
  ulong uVar9;
  long *plVar10;
  char *pcVar11;
  ulong uVar12;
  ulong uVar13;
  ulong uVar14;
  undefined2 uVar15;
  undefined8 uVar16;
  undefined1 uStack_51;
  
  uVar7 = *(ulong *)(param_2 + 8);
  pcVar4 = *(char **)param_2;
  if (-1 < param_2[0x17]) {
    uVar7 = (ulong)(byte)param_2[0x17];
    pcVar4 = param_2;
  }
  uVar7 = FUN_000545f0(&uStack_51,pcVar4,uVar7);
  uVar12 = param_1[1];
  if (uVar12 != 0) {
    uVar16 = CONCAT17(POPCOUNT((char)(uVar12 >> 0x38)),
                      CONCAT16(POPCOUNT((char)(uVar12 >> 0x30)),
                               CONCAT15(POPCOUNT((char)(uVar12 >> 0x28)),
                                        CONCAT14(POPCOUNT((char)(uVar12 >> 0x20)),
                                                 CONCAT13(POPCOUNT((char)(uVar12 >> 0x18)),
                                                          CONCAT12(POPCOUNT((char)(uVar12 >> 0x10)),
                                                                   CONCAT11(POPCOUNT((char)(uVar12 
                                                  >> 8)),POPCOUNT((char)uVar12))))))));
    uVar15 = NEON_uaddlv(uVar16,1);
    uVar13 = CONCAT62((int6)((ulong)uVar16 >> 0x10),uVar15) & 0xffffffff;
    if (uVar13 < 2) {
      uVar14 = uVar12 - 1 & uVar7;
    }
    else {
      uVar14 = uVar7;
      if (uVar12 <= uVar7) {
        uVar14 = 0;
        if (uVar12 != 0) {
          uVar14 = uVar7 / uVar12;
        }
        uVar14 = uVar7 - uVar14 * uVar12;
      }
    }
    plVar8 = *(long **)(*param_1 + uVar14 * 8);
    if (plVar8 != (long *)0x0) {
      plVar8 = (long *)*plVar8;
      if (plVar8 == (long *)0x0) {
        return (long *)0x0;
      }
      sVar5 = *(size_t *)(param_2 + 8);
      pcVar4 = *(char **)param_2;
      if (-1 < param_2[0x17]) {
        sVar5 = (ulong)(byte)param_2[0x17];
        pcVar4 = param_2;
      }
      do {
        uVar9 = plVar8[1];
        if (uVar9 == uVar7) {
          bVar2 = *(byte *)((long)plVar8 + 0x27);
          uVar9 = (ulong)bVar2;
          sVar1 = plVar8[3];
          if (-1 < (char)bVar2) {
            sVar1 = uVar9;
          }
          if (sVar1 == sVar5) {
            plVar10 = plVar8 + 2;
            if ((char)bVar2 < '\0') {
              iVar6 = _memcmp((void *)*plVar10,pcVar4,plVar8[3]);
              if (iVar6 == 0) {
                return plVar8;
              }
            }
            else {
              pcVar11 = pcVar4;
              if (bVar2 == 0) {
                return plVar8;
              }
              while ((char)*plVar10 == *pcVar11) {
                plVar10 = (long *)((long)plVar10 + 1);
                uVar9 = uVar9 - 1;
                pcVar11 = pcVar11 + 1;
                if (uVar9 == 0) {
                  return plVar8;
                }
              }
            }
          }
        }
        else {
          if (uVar13 < 2) {
            uVar9 = uVar9 & uVar12 - 1;
          }
          else if (uVar12 <= uVar9) {
            uVar3 = 0;
            if (uVar12 != 0) {
              uVar3 = uVar9 / uVar12;
            }
            uVar9 = uVar9 - uVar3 * uVar12;
          }
          if (uVar9 != uVar14) {
            return (long *)0x0;
          }
        }
        plVar8 = (long *)*plVar8;
        if (plVar8 == (long *)0x0) {
          return (long *)0x0;
        }
      } while( true );
    }
  }
  return (long *)0x0;
}


