// Ghidra inferred pseudocode; requested=0x66703f8
// entry=066703f8 end=06670437

void FUN_066703f8(undefined8 param_1,long param_2)

{
  undefined8 *puVar1;
  
  puVar1 = (undefined8 *)__Znwm(0x18);
  *puVar1 = &PTR_FUN_09fb2290;
  puVar1[1] = param_1;
  if (param_2 == 0) {
    param_2 = -1;
  }
  puVar1[2] = param_2;
  return;
}


