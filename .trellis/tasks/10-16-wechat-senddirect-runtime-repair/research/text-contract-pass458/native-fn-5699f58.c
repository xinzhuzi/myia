// Ghidra inferred pseudocode; requested=0x5699f58
// entry=05699f58 end=05699fa7

void FUN_05699f58(long param_1,undefined8 param_2,undefined4 param_3)

{
  long *plVar1;
  undefined4 local_14;
  
  if ((*(byte *)(param_1 + 0x198) & 1) == 0) {
    FUN_056a1844();
    return;
  }
  plVar1 = *(long **)(*(long *)(param_1 + 0x188) + 0xf8);
  local_14 = param_3;
  if (plVar1 != (long *)0x0) {
    (**(code **)(*plVar1 + 0x30))(plVar1,param_2,&local_14);
    return;
  }
                    /* WARNING: Subroutine does not return */
  FUN_0021eccc();
}


