// Ghidra inferred pseudocode; requested=0x453f630
// entry=0453f630 end=0453f65f

void FUN_0453f630(long param_1)

{
  long *plVar1;
  
  plVar1 = *(long **)(param_1 + 0x20);
  if (plVar1 == (long *)(param_1 + 8)) {
                    /* WARNING: Could not recover jumptable at 0x0453f658. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar1 + 0x20))();
    return;
  }
  if (plVar1 != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x0453f64c. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar1 + 0x28))();
    return;
  }
  return;
}


