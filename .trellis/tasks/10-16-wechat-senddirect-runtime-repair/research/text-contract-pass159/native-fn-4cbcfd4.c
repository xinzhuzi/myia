// Ghidra inferred pseudocode; requested=0x4cbcfd4
// entry=04cbcfd4 end=04cbd017

void FUN_04cbcfd4(long param_1,undefined4 param_2)

{
  int iVar1;
  
  *(undefined4 *)(param_1 + 0x10) = param_2;
  *(undefined8 *)(param_1 + 0x108) = *(undefined8 *)(param_1 + 0xc);
  if ((*(long *)(param_1 + 0x220) != 0) && (iVar1 = FUN_04a29d84(), iVar1 != 0)) {
    *(undefined4 *)(*(long *)(param_1 + 0x220) + 0xc) = param_2;
  }
  return;
}


