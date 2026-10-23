// Ghidra inferred pseudocode; requested=0x56c90b0
// entry=056c90b0 end=056c90cf

void FUN_056c90b0(undefined8 param_1,undefined8 *param_2)

{
  ulong uVar1;
  undefined8 *puVar2;
  
  uVar1 = param_2[1];
  puVar2 = (undefined8 *)*param_2;
  if (-1 < (char)*(byte *)((long)param_2 + 0x17)) {
    uVar1 = (ulong)*(byte *)((long)param_2 + 0x17);
    puVar2 = param_2;
  }
  FUN_0562fd20(param_1,puVar2,uVar1);
  return;
}


