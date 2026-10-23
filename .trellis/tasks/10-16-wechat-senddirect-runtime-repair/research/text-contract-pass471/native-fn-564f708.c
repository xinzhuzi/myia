// Ghidra inferred pseudocode; requested=0x564f708
// entry=0564f708 end=0564f79b

undefined8 * FUN_0564f708(undefined8 *param_1,undefined8 param_2)

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
  *param_1 = &PTR_thunk_FUN_0564f828_09f196e8;
  param_1[4] = param_2;
  *(undefined2 *)(param_1 + 5) = 0;
  *(undefined1 *)((long)param_1 + 0x2a) = 0;
  param_1[6] = 0;
  param_1[7] = param_1 + 7;
  param_1[8] = param_1 + 7;
  param_1[9] = 0;
  param_1[10] = param_1 + 10;
  param_1[0xb] = param_1 + 10;
  param_1[0xd] = 0;
  param_1[0xc] = 0;
  param_1[0xf] = 0;
  param_1[0xe] = 0;
  param_1[0x10] = 0;
  *(undefined4 *)(param_1 + 0x11) = 0x3f800000;
  param_1[0x12] = param_1 + 0x12;
  param_1[0x13] = param_1 + 0x12;
  param_1[0x14] = 0;
  return param_1;
}


