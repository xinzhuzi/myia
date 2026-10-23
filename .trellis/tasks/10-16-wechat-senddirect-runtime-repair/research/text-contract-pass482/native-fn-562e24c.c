// Ghidra inferred pseudocode; requested=0x562e24c
// entry=0562e24c end=0562e25f

void FUN_0562e24c(long param_1)

{
  int *piVar1;
  
  piVar1 = *(int **)(param_1 + 8);
  if (piVar1 != (int *)0x0) {
    LOAcquire();
    *piVar1 = *piVar1 + 1;
    LORelease();
  }
  return;
}


