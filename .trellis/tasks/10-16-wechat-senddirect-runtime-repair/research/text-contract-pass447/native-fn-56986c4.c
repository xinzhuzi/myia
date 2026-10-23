// Ghidra inferred pseudocode; requested=0x56986c4
// entry=056986c4 end=056986f3

void FUN_056986c4(long param_1)

{
  long *plVar1;
  
  if ((*(byte *)(param_1 + -0x20) & 1) == 0) {
    FUN_05695028();
    return;
  }
  plVar1 = *(long **)(*(long *)(param_1 + -0x30) + 0x58);
  if (plVar1 != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x056986e0. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar1 + 0x30))();
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_0021eccc();
}


