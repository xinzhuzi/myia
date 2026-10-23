// Ghidra inferred pseudocode; requested=0x567f0f4
// entry=0567f0f4 end=0567f17b

undefined8 * FUN_0567f0f4(undefined8 *param_1,undefined8 param_2)

{
  undefined8 *puVar1;
  
  param_1[1] = 0;
  *param_1 = 0;
  param_1[3] = 0;
  param_1[2] = 0;
  puVar1 = (undefined8 *)FUN_0562a69c();
  *puVar1 = &PTR_thunk_FUN_0562a748_09f19788;
  puVar1[3] = 0;
  FUN_0562a8f8(puVar1,0xc);
  *param_1 = &PTR_FUN_09f1b6a8;
  param_1[4] = param_2;
  *(undefined2 *)(param_1 + 5) = 0;
  param_1[6] = param_1 + 6;
  param_1[7] = param_1 + 6;
  param_1[9] = 0;
  param_1[8] = 0;
  param_1[0xb] = 0;
  param_1[10] = 0;
  FUN_00069f7c();
  *(undefined1 *)(param_1 + 0xb) = 0;
  param_1[0xc] = 0;
  return param_1;
}


