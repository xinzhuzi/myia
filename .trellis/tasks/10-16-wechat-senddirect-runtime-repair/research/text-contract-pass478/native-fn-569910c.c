// Ghidra inferred pseudocode; requested=0x569910c
// entry=0569910c end=05699147

void FUN_0569910c(long param_1,undefined8 param_2,undefined4 param_3)

{
  long *plVar1;
  undefined4 local_14;
  
  plVar1 = *(long **)(*(long *)(param_1 + 8) + 0x138);
  local_14 = param_3;
  if (plVar1 != (long *)0x0) {
    (**(code **)(*plVar1 + 0x30))(plVar1,param_2,&local_14);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_0021eccc();
}


