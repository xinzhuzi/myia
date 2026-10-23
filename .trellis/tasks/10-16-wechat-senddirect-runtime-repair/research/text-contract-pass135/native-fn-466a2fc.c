// Ghidra inferred pseudocode; requested=0x466a2fc
// entry=0466a2fc end=0466a317

void FUN_0466a2fc(undefined8 *param_1,long param_2)

{
  long lVar1;
  
  lVar1 = *(long *)(param_2 + 0x70);
  *param_1 = *(undefined8 *)(param_2 + 0x68);
  param_1[1] = lVar1;
  if (lVar1 != 0) {
    *(long *)(lVar1 + 8) = *(long *)(lVar1 + 8) + 1;
  }
  return;
}


