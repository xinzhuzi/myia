// Ghidra inferred pseudocode; requested=0x5daa3b0
// entry=05daa3b0 end=05daa3c3

void FUN_05daa3b0(undefined8 param_1)

{
  int iVar1;
  
  iVar1 = (int)DAT_0a124b88;
  LOAcquire();
  DAT_0a124b88._0_4_ = (int)DAT_0a124b88 + 1;
  LORelease();
  FUN_05daa21c(param_1,iVar1);
  return;
}


