// Ghidra inferred pseudocode; requested=0x56a15c0
// entry=056a15c0 end=056a1607

void FUN_056a15c0(long param_1)

{
  if (*(long *)(param_1 + 0x10) != 0) {
    FUN_056a10a0();
    FUN_0591d3bc(*(undefined8 *)(param_1 + 0x10));
    *(undefined8 *)(param_1 + 0x10) = 0;
    FUN_0569fbe0(param_1,param_1 + 0x58);
    FUN_05630588(param_1 + 0x58);
    return;
  }
  return;
}


