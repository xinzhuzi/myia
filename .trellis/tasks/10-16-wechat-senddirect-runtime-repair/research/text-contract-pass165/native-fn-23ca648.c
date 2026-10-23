// Ghidra inferred pseudocode; requested=0x23ca648
// entry=023ca648 end=023ca6eb

undefined8 * FUN_023ca648(undefined8 *param_1)

{
  undefined8 local_38 [2];
  undefined7 local_28;
  char cStack_21;
  
  param_1[1] = 0;
  param_1[2] = 0;
  *param_1 = &PTR_FUN_09d8e608;
  _bzero(param_1 + 3,0x650);
  FUN_00033e1c(local_38);
  FUN_0069a714(param_1 + 3,local_38);
  if (cStack_21 < '\0') {
    __ZdlPvm(local_38[0],CONCAT17(cStack_21,local_28) & 0x7fffffffffffffff);
  }
  *(undefined4 *)(param_1 + 200) = 0;
  param_1[199] = 0;
  param_1[0xc6] = 0;
  param_1[0xc5] = 0;
  param_1[0xc4] = 0;
  param_1[0xc3] = 0;
  param_1[0xc2] = 0;
  param_1[0xc1] = 0;
  param_1[0xc0] = 0;
  param_1[0xbf] = 0;
  param_1[0xbe] = 0;
  param_1[0xbd] = 0;
  param_1[0xbc] = 0;
  param_1[3] = &PTR_FUN_09eb2918;
  param_1[0xca] = 0;
  param_1[0xc9] = 0;
  param_1[0xcc] = 0;
  param_1[0xcb] = 0;
  return param_1;
}


