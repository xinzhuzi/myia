// Ghidra inferred pseudocode; requested=0x4678644
// entry=046785bc end=0467866f

undefined8 * FUN_046785bc(undefined8 *param_1,undefined4 *param_2)

{
  undefined8 *puVar1;
  
  param_1[1] = 0;
  param_1[2] = 0;
  param_1[4] = 0;
  *param_1 = &PTR_thunk_FUN_04678c94_09e92928;
  param_1[3] = param_1 + 4;
  param_1[5] = 0;
  param_1[7] = 0;
  param_1[6] = param_1 + 7;
  param_1[0xb] = 0;
  param_1[10] = 0;
  param_1[8] = 0;
  param_1[9] = param_1 + 10;
  *(undefined1 *)(param_1 + 0xc) = 0;
  puVar1 = (undefined8 *)__Znwm(0x20);
  puVar1[2] = 0;
  *puVar1 = &PTR_FUN_09bf2c18;
  puVar1[1] = 0;
  *(undefined1 *)(puVar1 + 3) = 1;
  param_1[0xd] = puVar1 + 3;
  param_1[0xe] = puVar1;
  *param_1 = &PTR_thunk_FUN_04678c94_09e928a8;
  *(undefined4 *)(param_1 + 0xf) = *param_2;
  return param_1;
}


