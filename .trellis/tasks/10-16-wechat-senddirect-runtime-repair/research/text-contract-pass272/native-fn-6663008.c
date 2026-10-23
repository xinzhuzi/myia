// Ghidra inferred pseudocode; requested=0x6663008
// entry=06663008 end=06663037

ulong FUN_06663008(long param_1)

{
  int *piVar1;
  int iVar2;
  long lVar3;
  
  lVar3 = FUN_06663038();
  piVar1 = (int *)(param_1 + 0x104);
  LOAcquire();
  iVar2 = *piVar1;
  *piVar1 = iVar2 + 1;
  LORelease();
  return CONCAT44((int)((ulong)piVar1 >> 0x20),iVar2) | lVar3 << 0x20;
}


