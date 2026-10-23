// Ghidra inferred pseudocode; requested=0x22166d0
// entry=022166d0 end=022166ef

void FUN_022166d0(void)

{
  long *plVar1;
  
  plVar1 = DAT_0a360b58;
  if (DAT_0a360b58 != (long *)0x0) {
    DAT_0a360b58 = (long *)0x0;
                    /* WARNING: Could not recover jumptable at 0x022166e8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
    (**(code **)(*plVar1 + 8))();
    return;
  }
  return;
}


