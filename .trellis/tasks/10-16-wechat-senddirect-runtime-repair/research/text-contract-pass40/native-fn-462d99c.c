// Ghidra inferred pseudocode; requested=0x462d99c
// entry=0462d99c end=0462d9f3

undefined8 FUN_0462d99c(undefined8 param_1,undefined8 param_2)

{
  undefined8 uVar1;
  undefined8 local_38;
  undefined8 uStack_30;
  ulong local_28;
  
  local_38 = 0;
  uStack_30 = 0;
  local_28 = 0;
  uVar1 = FUN_05cb50ec(param_2,&local_38);
  if ((long)local_28 < 0) {
    __ZdlPvm(local_38,local_28 & 0x7fffffffffffffff);
  }
  return uVar1;
}


