// Ghidra inferred pseudocode; requested=0x4bb5f30
// entry=04bb5f30 end=04bb6007

bool FUN_04bb5f30(char *param_1)

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
  ulong uVar10;
  
  uVar10 = *(ulong *)(param_1 + 8);
  if (-1 < param_1[0x17]) {
    uVar10 = (ulong)(byte)param_1[0x17];
  }
  if (uVar10 != 0) {
    plVar7 = (long *)FUN_04669774();
    pcVar8 = (char *)(**(code **)(*plVar7 + 0x28))();
    bVar3 = param_1[0x17];
    uVar10 = (ulong)bVar3;
    sVar1 = *(size_t *)(param_1 + 8);
    if (-1 < (char)bVar3) {
      sVar1 = uVar10;
    }
    bVar4 = pcVar8[0x17];
    sVar2 = *(size_t *)(pcVar8 + 8);
    if (-1 < (char)bVar4) {
      sVar2 = (ulong)bVar4;
    }
    if (sVar1 == sVar2) {
      pcVar9 = *(char **)pcVar8;
      if (-1 < (char)bVar4) {
        pcVar9 = pcVar8;
      }
      if ((char)bVar3 < '\0') {
        iVar6 = _memcmp(*(void **)param_1,pcVar9,*(size_t *)(param_1 + 8));
        bVar5 = iVar6 == 0;
      }
      else if (bVar3 == 0) {
        bVar5 = true;
      }
      else {
        do {
          uVar10 = uVar10 - 1;
          bVar5 = *param_1 == *pcVar9;
          if (!bVar5) {
            return bVar5;
          }
          pcVar9 = pcVar9 + 1;
          param_1 = param_1 + 1;
        } while (uVar10 != 0);
      }
    }
    else {
      bVar5 = false;
    }
    return bVar5;
  }
  return false;
}


