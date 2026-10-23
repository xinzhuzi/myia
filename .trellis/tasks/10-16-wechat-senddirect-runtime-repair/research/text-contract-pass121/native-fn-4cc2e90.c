// Ghidra inferred pseudocode; requested=0x4cc2e90
// entry=04cc2e90 end=04cc2ee7

void FUN_04cc2e90(undefined8 *param_1,long param_2,long param_3)

{
  long lVar1;
  undefined1 auStack_38 [24];
  
  lVar1 = *(long *)(param_2 + 8);
  param_1[2] = 0;
  *param_1 = "";
  param_1[1] = 0;
  FUN_056c90b0(auStack_38,param_3 + lVar1);
  FUN_0562fe5c(param_1,auStack_38);
  FUN_0562fd84(auStack_38);
  return;
}


