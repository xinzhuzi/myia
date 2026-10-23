// Ghidra inferred pseudocode; requested=0x3065454
// entry=03065454 end=03065583

undefined8 * FUN_03065454(undefined8 *param_1,undefined8 *param_2)

{
  long lVar1;
  
  param_1[2] = 0;
  *param_1 = &PTR_thunk_FUN_0303ff18_09de8768;
  param_1[1] = 0;
  FUN_066860b0(param_1 + 3);
  FUN_06685c88(param_1 + 5);
  param_1[3] = &PTR_FUN_09de5be0;
  FUN_066860b0(param_1 + 0x12);
  FUN_06685c88(param_1 + 0x14);
  param_1[0x12] = &PTR_FUN_09de5c40;
  FUN_066860b0(param_1 + 0x21);
  FUN_06685c88(param_1 + 0x23);
  param_1[0x21] = &PTR_FUN_09de5be0;
  FUN_066860b0(param_1 + 0x30);
  FUN_06685c88(param_1 + 0x32);
  param_1[0x30] = &PTR_FUN_09de5ca0;
  FUN_066860b0(param_1 + 0x3f);
  FUN_06685c88(param_1 + 0x41);
  param_1[0x3f] = &PTR_FUN_09de5d00;
  FUN_066860b0(param_1 + 0x4e);
  FUN_06685c88(param_1 + 0x50);
  param_1[0x4e] = &PTR_FUN_09de5d60;
  FUN_066860b0(param_1 + 0x5d);
  FUN_06685c88(param_1 + 0x5f);
  param_1[0x5d] = &PTR_FUN_09de5dc0;
  lVar1 = param_2[1];
  param_1[0x6c] = *param_2;
  param_1[0x6d] = lVar1;
  if (lVar1 != 0) {
    *(long *)(lVar1 + 0x10) = *(long *)(lVar1 + 0x10) + 1;
  }
  lVar1 = param_2[3];
  param_1[0x6e] = param_2[2];
  param_1[0x6f] = lVar1;
  if (lVar1 != 0) {
    *(long *)(lVar1 + 0x10) = *(long *)(lVar1 + 0x10) + 1;
  }
  return param_1;
}


