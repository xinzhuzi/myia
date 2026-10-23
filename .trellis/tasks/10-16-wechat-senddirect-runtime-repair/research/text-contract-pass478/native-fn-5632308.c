// Ghidra inferred pseudocode; requested=0x5632308
// entry=05632308 end=05632363

undefined8 * FUN_05632308(undefined8 *param_1,undefined8 param_2,undefined8 param_3)

{
  undefined8 local_28;
  
  *param_1 = &PTR_FUN_09f177b0;
  param_1[1] = param_2;
  param_1[2] = param_3;
  local_28 = 0;
  FUN_0562e128(param_1 + 3,&local_28);
  param_1[3] = &PTR_FUN_09da5788;
  param_1[6] = 0;
  param_1[7] = 0;
  param_1[0xb] = 0;
  return param_1;
}


