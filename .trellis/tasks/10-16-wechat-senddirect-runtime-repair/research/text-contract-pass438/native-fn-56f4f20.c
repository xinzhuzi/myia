// Ghidra inferred pseudocode; requested=0x56f4f20
// entry=056f4f20 end=056f4f6b

void FUN_056f4f20(long *param_1,undefined8 param_2,undefined8 param_3)

{
  long *plVar1;
  
  plVar1 = (long *)(**(code **)(*param_1 + 0x10))();
  if (plVar1 != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x056f4f5c. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar1 + 0x58))(plVar1,param_2,param_3);
    return;
  }
  return;
}


