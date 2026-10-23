// Ghidra inferred pseudocode; requested=0x66860b0
// entry=066860b0 end=0668612f

undefined8 * FUN_066860b0(undefined8 *param_1)

{
  undefined8 *puVar1;
  
  *param_1 = &PTR_thunk_FUN_0668614c_09fb30b8;
  puVar1 = (undefined8 *)__Znwm(0xa0);
  puVar1[0xb] = 0;
  puVar1[10] = 0;
  puVar1[0xd] = 0;
  puVar1[0xc] = 0;
  puVar1[0xf] = 0;
  puVar1[0xe] = 0;
  puVar1[0x11] = 0;
  puVar1[0x10] = 0;
  puVar1[0x13] = 0;
  puVar1[0x12] = 0;
  puVar1[9] = 0;
  puVar1[8] = 0;
  *puVar1 = 0x32aaaba7;
  puVar1[2] = 0;
  puVar1[1] = 0;
  puVar1[4] = 0;
  puVar1[3] = 0;
  puVar1[6] = 0;
  puVar1[5] = 0;
  puVar1[7] = 0;
  __ZNSt3__115recursive_mutexC1Ev();
  puVar1[0x10] = 0;
  puVar1[0x11] = puVar1 + 0x10;
  puVar1[0x12] = 0;
  *(undefined2 *)(puVar1 + 0x13) = 0;
  param_1[1] = puVar1;
  return param_1;
}


