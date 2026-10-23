// Ghidra inferred pseudocode; requested=0x564e844
// entry=0564e844 end=0564e8bb

undefined8 * FUN_0564e844(undefined8 *param_1,undefined8 param_2)

{
  undefined8 *puVar1;
  
  param_1[1] = 0;
  *param_1 = 0;
  param_1[3] = 0;
  param_1[2] = 0;
  puVar1 = (undefined8 *)FUN_0562a69c();
  *puVar1 = &PTR_thunk_FUN_0562a748_09f194c8;
  puVar1[3] = 0;
  FUN_0562a8f8(puVar1,6);
  *param_1 = &PTR_thunk_FUN_0562a748_09f1c718;
  FUN_0565a31c(param_1 + 4,param_2);
  *param_1 = &PTR_FUN_09f193f0;
  param_1[4] = &PTR_FUN_09f19450;
  return param_1;
}


