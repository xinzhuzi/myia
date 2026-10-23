// Ghidra inferred pseudocode; requested=0x4a290c4
// entry=04a290c4 end=04a290df

bool FUN_04a290c4(long param_1)

{
  int iVar1;
  
  iVar1 = *(int *)(param_1 + 0xc);
  return (iVar1 == 3 || iVar1 == 0xd) || iVar1 == 0x27;
}


