// Ghidra inferred pseudocode; requested=0x5699084
// entry=05699084 end=056990bf

void FUN_05699084(long param_1,undefined8 param_2,undefined4 param_3)

{
  long *plVar1;
  undefined4 local_14;
  
  plVar1 = *(long **)(*(long *)(param_1 + 8) + 0xf8);
  local_14 = param_3;
  if (plVar1 != (long *)0x0) {
    (**(code **)(*plVar1 + 0x30))(plVar1,param_2,&local_14);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_0021eccc();
}


