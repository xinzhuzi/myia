// Ghidra inferred pseudocode; requested=0x6683424
// entry=06683424 end=0668343f

void FUN_06683424(long param_1,ulong *param_2,undefined8 *param_3)

{
  long *plVar1;
  code *UNRECOVERED_JUMPTABLE;
  
  UNRECOVERED_JUMPTABLE = (code *)*param_2;
  plVar1 = (long *)(param_1 + ((long)param_2[1] >> 1));
  if ((param_2[1] & 1) != 0) {
    UNRECOVERED_JUMPTABLE = *(code **)(*plVar1 + ((ulong)UNRECOVERED_JUMPTABLE & 0xffffffff));
  }
                    /* WARNING: Could not recover jumptable at 0x0668343c. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*UNRECOVERED_JUMPTABLE)(plVar1,*param_3);
  return;
}


