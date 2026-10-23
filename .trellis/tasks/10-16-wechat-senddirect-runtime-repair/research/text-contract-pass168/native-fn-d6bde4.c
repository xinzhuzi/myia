// Ghidra inferred pseudocode; requested=0xd6bde4
// entry=00d6bde4 end=00d6be63

undefined8 * FUN_00d6bde4(undefined8 *param_1)

{
  undefined8 local_38 [2];
  undefined7 local_28;
  char cStack_21;
  
  param_1[1] = 0;
  param_1[2] = 0;
  *param_1 = &PTR_FUN_09c830a8;
  _bzero(param_1 + 3,0x5d8);
  FUN_00033e1c(local_38);
  FUN_0069a714(param_1 + 3,local_38);
  if (cStack_21 < '\0') {
    __ZdlPvm(local_38[0],CONCAT17(cStack_21,local_28) & 0x7fffffffffffffff);
  }
  param_1[3] = &PTR_FUN_09c830f8;
  param_1[0xbd] = 0;
  param_1[0xbc] = 0;
  return param_1;
}


