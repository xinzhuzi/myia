// Ghidra inferred pseudocode; requested=0x453f6b0
// entry=0453f6b0 end=0453f6ef

void FUN_0453f6b0(long param_1)

{
  FUN_066859ec(DAT_0a51e9a0);
  if (*(long **)(param_1 + 0x20) != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x0453f6e8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(**(long **)(param_1 + 0x20) + 0x30))();
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_0021eccc();
}


