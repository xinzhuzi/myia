// Ghidra inferred pseudocode; requested=0x5ded378
// entry=05ded378 end=05ded3c3

void FUN_05ded378(long param_1,long param_2,int param_3)

{
  ulong uVar1;
  
  uVar1 = *(long *)(param_1 + 8) + param_2;
  FUN_05ded3c4(param_1,uVar1);
  if (param_3 != 0) {
    if (uVar1 <= *(ulong *)(param_1 + 0x10)) {
      uVar1 = *(ulong *)(param_1 + 0x10);
    }
    *(ulong *)(param_1 + 0x10) = uVar1;
  }
  return;
}


