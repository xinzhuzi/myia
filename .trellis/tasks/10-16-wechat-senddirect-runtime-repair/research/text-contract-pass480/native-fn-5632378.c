// Ghidra inferred pseudocode; requested=0x5632378
// entry=05632378 end=056323b7

undefined8 * FUN_05632378(undefined8 *param_1,long param_2)

{
  undefined8 uVar1;
  undefined8 uVar2;
  
  uVar1 = *(undefined8 *)(param_2 + 8);
  uVar2 = *(undefined8 *)(param_2 + 0x10);
  *param_1 = &PTR_FUN_09f177b0;
  param_1[1] = uVar1;
  param_1[2] = uVar2;
  FUN_05627558(param_1 + 3,param_2 + 0x18);
  return param_1;
}


