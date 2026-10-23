// Ghidra inferred pseudocode; requested=0x4a2965c
// entry=04a2965c end=04a2969f

bool FUN_04a2965c(long param_1)

{
  uint uVar1;
  
  uVar1 = *(int *)(param_1 + 0xc) - 0x2a;
  if (uVar1 < 0x1a && (1 << (ulong)(uVar1 & 0x1f) & 0x3000001U) != 0) {
    return true;
  }
  return *(int *)(param_1 + 0xc) == 0x31 && *(int *)(param_1 + 0x10) == 0x32;
}


