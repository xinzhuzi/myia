// Ghidra inferred pseudocode; requested=0x4cbd748
// entry=04cbd748 end=04cbd833

bool FUN_04cbd748(long param_1)

{
  size_t sVar1;
  size_t sVar2;
  byte bVar3;
  byte bVar4;
  bool bVar5;
  int iVar6;
  long *plVar7;
  char *pcVar8;
  char *pcVar9;
  char *pcVar10;
  ulong uVar11;
  
  if (*(int *)(param_1 + 0xc) != 10000) {
    uVar11 = *(ulong *)(param_1 + 0x20);
    if (-1 < (char)*(byte *)(param_1 + 0x2f)) {
      uVar11 = (ulong)*(byte *)(param_1 + 0x2f);
    }
    if (uVar11 != 0) {
      plVar7 = (long *)FUN_04669774();
      pcVar8 = (char *)(**(code **)(*plVar7 + 0x28))();
      bVar3 = *(byte *)(param_1 + 0x2f);
      uVar11 = (ulong)bVar3;
      sVar1 = *(size_t *)(param_1 + 0x20);
      if (-1 < (char)bVar3) {
        sVar1 = uVar11;
      }
      bVar4 = pcVar8[0x17];
      sVar2 = *(size_t *)(pcVar8 + 8);
      if (-1 < (char)bVar4) {
        sVar2 = (ulong)bVar4;
      }
      if (sVar1 == sVar2) {
        pcVar10 = (char *)(param_1 + 0x18);
        pcVar9 = *(char **)pcVar8;
        if (-1 < (char)bVar4) {
          pcVar9 = pcVar8;
        }
        if ((char)bVar3 < '\0') {
          iVar6 = _memcmp(*(void **)pcVar10,pcVar9,*(size_t *)(param_1 + 0x20));
          bVar5 = iVar6 == 0;
        }
        else if (bVar3 == 0) {
          bVar5 = true;
        }
        else {
          do {
            uVar11 = uVar11 - 1;
            bVar5 = *pcVar10 == *pcVar9;
            if (!bVar5) {
              return bVar5;
            }
            pcVar9 = pcVar9 + 1;
            pcVar10 = pcVar10 + 1;
          } while (uVar11 != 0);
        }
      }
      else {
        bVar5 = false;
      }
      return bVar5;
    }
  }
  return false;
}


