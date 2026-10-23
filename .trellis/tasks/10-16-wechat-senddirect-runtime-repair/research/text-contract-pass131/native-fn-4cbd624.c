// Ghidra inferred pseudocode; requested=0x4cbd624
// entry=04cbd624 end=04cbd713

char * FUN_04cbd624(long param_1)

{
  char *pcVar1;
  size_t sVar2;
  size_t sVar3;
  long lVar4;
  byte bVar5;
  byte bVar6;
  int iVar7;
  long *plVar8;
  char *pcVar9;
  char *pcVar10;
  ulong uVar11;
  
  if (*(int *)(param_1 + 0xc) == 10000) {
    plVar8 = (long *)FUN_04669774();
    pcVar9 = (char *)(**(code **)(*plVar8 + 0x28))();
    pcVar1 = (char *)(param_1 + 0x18);
    bVar5 = *(byte *)(param_1 + 0x2f);
    uVar11 = (ulong)bVar5;
    sVar2 = *(size_t *)(param_1 + 0x20);
    if (-1 < (char)bVar5) {
      sVar2 = uVar11;
    }
    bVar6 = pcVar9[0x17];
    sVar3 = *(size_t *)(pcVar9 + 8);
    if (-1 < (char)bVar6) {
      sVar3 = (ulong)bVar6;
    }
    pcVar10 = pcVar1;
    if (sVar2 == sVar3) {
      pcVar10 = *(char **)pcVar9;
      if (-1 < (char)bVar6) {
        pcVar10 = pcVar9;
      }
      if ((char)bVar5 < '\0') {
        iVar7 = _memcmp(*(void **)(param_1 + 0x18),pcVar10,*(size_t *)(param_1 + 0x20));
        pcVar10 = (char *)(param_1 + 0x30);
        if (iVar7 != 0) {
          pcVar10 = pcVar1;
        }
      }
      else {
        pcVar9 = pcVar1;
        if (bVar5 != 0) {
          do {
            if (*pcVar9 != *pcVar10) {
              return pcVar1;
            }
            pcVar10 = pcVar10 + 1;
            uVar11 = uVar11 - 1;
            pcVar9 = pcVar9 + 1;
          } while (uVar11 != 0);
        }
        pcVar10 = (char *)(param_1 + 0x30);
      }
    }
  }
  else {
    iVar7 = FUN_04cbd748(param_1);
    lVar4 = 0x30;
    if (iVar7 == 0) {
      lVar4 = 0x18;
    }
    pcVar10 = (char *)(param_1 + lVar4);
  }
  return pcVar10;
}


