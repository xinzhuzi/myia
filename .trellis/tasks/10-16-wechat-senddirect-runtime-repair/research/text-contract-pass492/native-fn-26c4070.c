// Ghidra inferred pseudocode; requested=0x26c4070
// entry=026c4070 end=026c408b

void FUN_026c4070(undefined8 *param_1,undefined8 param_2,undefined8 *param_3)

{
  undefined8 uVar1;
  long lVar2;
  
  uVar1 = *param_3;
  lVar2 = param_3[1];
  if (lVar2 != 0) {
    *(long *)(lVar2 + 8) = *(long *)(lVar2 + 8) + 1;
  }
  *param_1 = uVar1;
  param_1[1] = lVar2;
  return;
}


