// Ghidra inferred pseudocode; requested=0x5697ec8
// entry=05697ec8 end=05697eeb

void FUN_05697ec8(long param_1)

{
  long *plVar1;
  
  plVar1 = *(long **)(*(long *)(param_1 + 8) + 0x98);
  if (plVar1 != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x05697edc. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar1 + 0x30))();
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_0021eccc();
}


