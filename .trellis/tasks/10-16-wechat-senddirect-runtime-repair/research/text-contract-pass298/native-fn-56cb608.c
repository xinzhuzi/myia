// Ghidra inferred pseudocode; requested=0x56cb608
// entry=056cb608 end=056cb693

ulong FUN_056cb608(byte *param_1)

{
  byte bVar1;
  ulong uVar2;
  long lVar3;
  char *pcVar4;
  
  bVar1 = *param_1;
  uVar2 = (ulong)bVar1;
  if (bVar1 < 2) {
    if (bVar1 != 0) {
      uVar2 = *(ulong *)(param_1 + 8);
    }
  }
  else {
    if (bVar1 != 2) {
      if (bVar1 == 3) {
        lVar3 = FUN_009abfd4(param_1 + 8);
        if (lVar3 == 0) {
          return 0;
        }
        pcVar4 = (char *)FUN_0008a8b8(param_1 + 8);
      }
      else {
        lVar3 = FUN_009ce4a8(param_1 + 8);
        if (lVar3 == 0) {
          return 0;
        }
        pcVar4 = (char *)FUN_05632b8c(param_1 + 8);
      }
      uVar2 = _atoll(pcVar4);
      return uVar2;
    }
    uVar2 = (ulong)*(double *)(param_1 + 8);
  }
  return uVar2;
}


