// Ghidra inferred pseudocode; requested=0x465dbc0
// entry=0465dbc0 end=0465dc2b

ulong FUN_0465dbc0(long param_1)

{
  ulong uVar1;
  long lVar2;
  
  if ((*(byte *)(param_1 + 0x28) & 1) == 0) {
    return 0;
  }
  if (*(int *)(param_1 + 0x10) < 1) {
    uVar1 = 1;
  }
  else {
    lVar2 = 0;
    do {
      uVar1 = (**(code **)(**(long **)(*(long *)(param_1 + 8) + lVar2 * 8) + 0x28))();
      if ((uVar1 & 1) == 0) {
        return uVar1;
      }
      lVar2 = lVar2 + 1;
    } while (lVar2 < *(int *)(param_1 + 0x10));
  }
  return uVar1;
}


