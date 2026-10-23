// Ghidra inferred pseudocode; requested=0x33c40
// entry=00033c40 end=00033c5b

void FUN_00033c40(undefined4 *param_1,undefined8 param_2,undefined8 param_3)

{
  *param_1 = 1;
  *(undefined8 *)(param_1 + 2) = param_2;
  *(undefined8 *)(param_1 + 4) = param_3;
  *(code **)(param_1 + 6) = FUN_00033c5c;
  return;
}


