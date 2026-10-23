// Ghidra inferred pseudocode; requested=0x465da58
// entry=0465da58 end=0465dacb

void FUN_0465da58(long param_1,undefined8 param_2)

{
  long lVar1;
  
  if ((*(byte *)(param_1 + 0x28) & 1) != 0) {
    FUN_05ab4e34(1,*(undefined4 *)(param_1 + 0x20),param_2);
  }
  if (0 < *(int *)(param_1 + 0x10)) {
    lVar1 = 0;
    do {
      FUN_05ab50f0(2,*(undefined8 *)(*(long *)(param_1 + 8) + lVar1 * 8),param_2);
      lVar1 = lVar1 + 1;
    } while (lVar1 < *(int *)(param_1 + 0x10));
  }
  return;
}


