// Ghidra inferred pseudocode; requested=0x5656650
// entry=05656650 end=0565667f

void FUN_05656650(long *param_1)

{
  long *plVar1;
  
  plVar1 = (long *)param_1[3];
  if (plVar1 == param_1) {
                    /* WARNING: Could not recover jumptable at 0x05656678. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar1 + 0x20))();
    return;
  }
  if (plVar1 != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x0565666c. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar1 + 0x28))();
    return;
  }
  return;
}


