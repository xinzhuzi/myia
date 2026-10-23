// Ghidra inferred pseudocode; requested=0x30d9d38
// entry=030d9d38 end=030d9d83

void FUN_030d9d38(undefined8 *param_1)

{
  undefined8 *puVar1;
  
  param_1[5] = 0;
  param_1[4] = 0;
  param_1[1] = 0;
  *param_1 = 0;
  param_1[3] = 0;
  param_1[2] = 0;
  puVar1 = (undefined8 *)__Znwm(0x20);
  puVar1[1] = 0;
  puVar1[2] = 0;
  *puVar1 = &PTR_FUN_09de5018;
  param_1[4] = puVar1 + 3;
  param_1[5] = puVar1;
  return;
}


