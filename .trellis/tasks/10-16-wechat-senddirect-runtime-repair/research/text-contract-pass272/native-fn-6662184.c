// Ghidra inferred pseudocode; requested=0x6662184
// entry=06662184 end=066621a3

void FUN_06662184(long param_1)

{
  if (*(long **)(param_1 + 0x20) != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x06662194. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(**(long **)(param_1 + 0x20) + 0x30))();
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_0021eccc();
}


