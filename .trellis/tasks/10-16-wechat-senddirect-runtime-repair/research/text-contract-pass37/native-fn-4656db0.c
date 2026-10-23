// Ghidra inferred pseudocode; requested=0x4656db0
// entry=04656db0 end=04656dc7

void FUN_04656db0(long param_1)

{
  if (*(long **)(param_1 + 8) != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x04656dc0. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(**(long **)(param_1 + 8) + 0x38))();
    return;
  }
  return;
}


