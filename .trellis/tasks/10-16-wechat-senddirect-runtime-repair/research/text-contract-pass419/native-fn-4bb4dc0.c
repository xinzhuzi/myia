// Ghidra inferred pseudocode; requested=0x4bb4dc0
// entry=04bb4dc0 end=04bb4e7b

bool FUN_04bb4dc0(char *param_1)

{
  size_t sVar1;
  size_t sVar2;
  byte bVar3;
  bool bVar4;
  int iVar5;
  char *pcVar6;
  ulong uVar7;
  
  FUN_04bb4e7c();
  bVar3 = param_1[0x17];
  uVar7 = (ulong)bVar3;
  sVar1 = *(size_t *)(param_1 + 8);
  if (-1 < (char)bVar3) {
    sVar1 = uVar7;
  }
  sVar2 = DAT_0a4a5288;
  if (-1 < (char)DAT_0a4a5297) {
    sVar2 = (ulong)DAT_0a4a5297;
  }
  if (sVar1 == sVar2) {
    pcVar6 = DAT_0a4a5280;
    if (-1 < (char)DAT_0a4a5297) {
      pcVar6 = (char *)&DAT_0a4a5280;
    }
    if ((char)bVar3 < '\0') {
      iVar5 = _memcmp(*(void **)param_1,pcVar6,*(size_t *)(param_1 + 8));
      bVar4 = iVar5 == 0;
    }
    else if (bVar3 == 0) {
      bVar4 = true;
    }
    else {
      do {
        uVar7 = uVar7 - 1;
        bVar4 = *param_1 == *pcVar6;
        if (!bVar4) {
          return bVar4;
        }
        pcVar6 = pcVar6 + 1;
        param_1 = param_1 + 1;
      } while (uVar7 != 0);
    }
  }
  else {
    bVar4 = false;
  }
  return bVar4;
}


