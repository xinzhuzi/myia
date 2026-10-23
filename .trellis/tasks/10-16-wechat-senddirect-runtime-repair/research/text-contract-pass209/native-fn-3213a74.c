// Ghidra inferred pseudocode; requested=0x3213a74
// entry=03213a74 end=03213a93

void FUN_03213a74(long param_1,ulong *param_2,undefined8 *param_3,undefined8 param_4)

{
  long *plVar1;
  code *UNRECOVERED_JUMPTABLE;
  
  UNRECOVERED_JUMPTABLE = (code *)*param_2;
  plVar1 = (long *)(param_1 + ((long)param_2[1] >> 1));
  if ((param_2[1] & 1) != 0) {
    UNRECOVERED_JUMPTABLE = *(code **)(*plVar1 + ((ulong)UNRECOVERED_JUMPTABLE & 0xffffffff));
  }
                    /* WARNING: Could not recover jumptable at 0x03213a90. Too many branches */
                    /* WARNING: Treating indirect jump as call */
  (*UNRECOVERED_JUMPTABLE)(plVar1,*param_3,param_4);
  return;
}


