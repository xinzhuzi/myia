// Ghidra inferred pseudocode; requested=0x567c340
// entry=0567c340 end=0567c3bb

undefined8 * FUN_0567c340(undefined8 *param_1,undefined8 param_2)

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
  FUN_05685b8c(param_1 + 4,param_2);
  *param_1 = &PTR_FUN_09f1b1b0;
  param_1[4] = &PTR_FUN_09f1b228;
  *(undefined1 *)((long)param_1 + 0x81) = 0;
  return param_1;
}


