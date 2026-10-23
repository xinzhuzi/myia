// Ghidra inferred pseudocode; requested=0x66683cc
// entry=066683cc end=06668427

void FUN_066683cc(long param_1)

{
  long *plVar1;
  
  FUN_06662554(*(undefined8 *)(param_1 + 0x28));
  if (*(long *)(param_1 + 0x30) == 0) {
    FUN_06688584(param_1 + 0x38);
    plVar1 = *(long **)(param_1 + 0x20);
  }
  else {
    plVar1 = *(long **)(param_1 + 0x20);
  }
  if (plVar1 != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x06668404. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar1 + 0x30))();
    return;
  }
  FUN_06666628(*(undefined8 *)(param_1 + 0x28));
  return;
}


