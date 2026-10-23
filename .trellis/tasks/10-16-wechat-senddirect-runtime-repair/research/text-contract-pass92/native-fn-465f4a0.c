// Ghidra inferred pseudocode; requested=0x465f4a0
// entry=0465f4a0 end=0465f537

ulong FUN_0465f4a0(long param_1)

{
  long *plVar1;
  ulong uVar2;
  long lVar3;
  
  if (((*(uint *)(param_1 + 0x30) ^ 0xffffffff) & 3) != 0) {
    return 0;
  }
  plVar1 = *(long **)(param_1 + 8);
  if (plVar1 == (long *)0x0) {
    plVar1 = *(long **)(DAT_0a51ea50 + 8);
  }
  uVar2 = (**(code **)(*plVar1 + 0x28))();
  if ((int)uVar2 != 0) {
    if (*(int *)(param_1 + 0x18) < 1) {
      uVar2 = 1;
    }
    else {
      lVar3 = 0;
      do {
        uVar2 = (**(code **)(**(long **)(*(long *)(param_1 + 0x10) + lVar3 * 8) + 0x28))();
        if ((uVar2 & 1) == 0) {
          return uVar2;
        }
        lVar3 = lVar3 + 1;
      } while (lVar3 < *(int *)(param_1 + 0x18));
    }
  }
  return uVar2;
}


