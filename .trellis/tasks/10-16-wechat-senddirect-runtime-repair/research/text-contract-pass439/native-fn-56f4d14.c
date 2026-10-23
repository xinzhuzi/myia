// Ghidra inferred pseudocode; requested=0x56f4d14
// entry=056f4d14 end=056f4d57

void FUN_056f4d14(long *param_1,undefined8 param_2)

{
  long *plVar1;
  
  plVar1 = (long *)(**(code **)(*param_1 + 0x10))();
  if (plVar1 != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x056f4d48. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar1 + 0x10))(plVar1,param_2);
    return;
  }
  return;
}


