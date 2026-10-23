// Ghidra inferred pseudocode; requested=0x2b35f8
// entry=002b35f8 end=002b35fb

long thunk_FUN_002b355c(long param_1,undefined8 param_2,undefined8 param_3)

{
  undefined8 *puVar1;
  undefined8 uVar2;
  
  puVar1 = (undefined8 *)FUN_06fd38a8();
  puVar1[2] = &DAT_0a232128;
  *puVar1 = &PTR_FUN_09bf7f90;
  FUN_002b3f8c(puVar1 + 3,param_3);
  uVar2 = __Znwm(0x18);
  FUN_002ce5e4(uVar2,param_1);
  *(undefined8 *)(param_1 + 0x68) = uVar2;
  return param_1;
}


