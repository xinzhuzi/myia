// Ghidra inferred pseudocode; requested=0x668082c
// entry=0668082c end=06680887

void FUN_0668082c(long param_1)

{
  int iVar1;
  
  FUN_066741a4(*(long *)(param_1 + 8) + 0xa8,0xffffffffffffffff);
  iVar1 = FUN_06674168(*(long *)(param_1 + 8) + 0xa8);
  if (iVar1 == 3) {
    if ((*(byte *)(*(long *)(param_1 + 8) + 0x150) & 1) == 0) {
      FUN_0667fc38(*(long *)(param_1 + 8),1);
      return;
    }
  }
  return;
}


