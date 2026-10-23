// Ghidra inferred pseudocode; requested=0x30c39bc
// entry=030c39bc end=030c3a2f

long FUN_030c39bc(long param_1,long param_2)

{
  int iVar1;
  ulong uVar2;
  
  uVar2 = *(ulong *)(param_2 + 8);
  if (uVar2 != 0x80000000088ad330) {
    if (-1 < (long)uVar2) {
      return 0;
    }
    iVar1 = _strcmp((char *)(uVar2 & 0x7fffffffffffffff),"_3ab0f0e7");
    if (iVar1 != 0) {
      return 0;
    }
  }
  return param_1 + 8;
}


