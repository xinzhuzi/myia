// Ghidra inferred pseudocode; requested=0x33fcc
// entry=00033fcc end=00033ff3

undefined8 FUN_00033fcc(undefined8 *param_1)

{
  undefined8 uVar1;
  
  if (-1 < *(char *)((long)param_1 + 0x17)) {
    uVar1 = FUN_0009ebf8();
    return uVar1;
  }
  if ((ulong)param_1[1] >> 0x1f != 0) {
    return 0;
  }
  uVar1 = FUN_0009ebf8(*param_1);
  return uVar1;
}


