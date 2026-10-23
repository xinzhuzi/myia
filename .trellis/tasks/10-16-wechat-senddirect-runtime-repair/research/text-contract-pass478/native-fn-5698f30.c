// Ghidra inferred pseudocode; requested=0x5698f30
// entry=05698f30 end=05698f43

long FUN_05698f30(long param_1)

{
  long lVar1;
  
  lVar1 = 0;
  if (*(long *)(param_1 + 0x18) != 0) {
    lVar1 = *(long *)(param_1 + 0x18) + -0x180;
  }
  return lVar1;
}


