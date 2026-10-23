// Ghidra inferred pseudocode; requested=0x4cbfbbc
// entry=04cbfbbc end=04cbfc0b

void FUN_04cbfbbc(undefined8 *param_1,undefined8 param_2)

{
  undefined8 *puVar1;
  undefined8 uVar2;
  
  puVar1 = (undefined8 *)__Znwm(0x290);
  puVar1[1] = 0;
  puVar1[2] = 0;
  *puVar1 = &PTR_FUN_09c92390;
  uVar2 = FUN_00f57630(puVar1 + 3,param_2);
  *param_1 = uVar2;
  param_1[1] = puVar1;
  return;
}


