// Ghidra inferred pseudocode; requested=0x466ad74
// entry=0466ad74 end=0466ad93

void FUN_0466ad74(undefined8 *param_1,long param_2)

{
  long lVar1;
  
  lVar1 = *(long *)(param_2 + 0x298);
  *param_1 = *(undefined8 *)(param_2 + 0x290);
  param_1[1] = lVar1;
  if (lVar1 != 0) {
    *(long *)(lVar1 + 8) = *(long *)(lVar1 + 8) + 1;
  }
  return;
}


