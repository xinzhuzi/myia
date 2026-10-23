// Ghidra inferred pseudocode; requested=0x2ab8f80
// entry=02ab8f80 end=02ab8fcf

void FUN_02ab8f80(undefined8 *param_1,undefined8 param_2)

{
  undefined8 *puVar1;
  undefined8 uVar2;
  
  puVar1 = (undefined8 *)__Znwm(0x3f8);
  puVar1[1] = 0;
  puVar1[2] = 0;
  *puVar1 = &PTR_FUN_09dafb50;
  uVar2 = FUN_0233200c(puVar1 + 3,param_2);
  *param_1 = uVar2;
  param_1[1] = puVar1;
  return;
}


