// Ghidra inferred pseudocode; requested=0x5632480
// entry=05632480 end=056324cb

undefined8 * FUN_05632480(undefined8 *param_1,long param_2)

{
  undefined8 uVar1;
  
  uVar1 = *(undefined8 *)(param_2 + 8);
  *param_1 = &PTR_FUN_09f177b0;
  param_1[1] = uVar1;
  param_1[2] = *(undefined8 *)(param_2 + 0x10);
  FUN_05632bb4(param_1 + 3,param_2 + 0x18);
  *(undefined8 *)(param_2 + 8) = 0;
  *(undefined8 *)(param_2 + 0x10) = 0;
  return param_1;
}


