// Ghidra inferred pseudocode; requested=0x5656890
// entry=05656890 end=056568bf

void FUN_05656890(long *param_1)

{
  long *plVar1;
  
  plVar1 = (long *)param_1[3];
  if (plVar1 == param_1) {
                    /* WARNING: Could not recover jumptable at 0x056568b8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar1 + 0x20))();
    return;
  }
  if (plVar1 != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x056568ac. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar1 + 0x28))();
    return;
  }
  return;
}


