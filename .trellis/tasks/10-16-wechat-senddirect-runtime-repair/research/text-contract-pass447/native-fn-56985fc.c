// Ghidra inferred pseudocode; requested=0x56985fc
// entry=056985fc end=0569862b

void FUN_056985fc(long param_1)

{
  long *plVar1;
  
  if ((*(byte *)(param_1 + -0x20) & 1) == 0) {
    FUN_056941c8();
    return;
  }
  plVar1 = *(long **)(*(long *)(param_1 + -0x30) + 0x18);
  if (plVar1 != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x05698618. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar1 + 0x30))();
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_0021eccc();
}


