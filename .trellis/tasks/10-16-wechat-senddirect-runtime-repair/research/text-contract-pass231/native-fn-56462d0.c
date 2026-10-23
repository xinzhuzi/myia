// Ghidra inferred pseudocode; requested=0x56462d0
// entry=056462d0 end=0564634b

undefined8 FUN_056462d0(long *param_1,long param_2)

{
  int iVar1;
  undefined8 uVar2;
  long *plVar3;
  long *local_28;
  
  uVar2 = (**(code **)(*param_1 + 0x50))();
  if ((int)uVar2 != 0) {
    plVar3 = *(long **)(param_2 + 0x18);
    local_28 = param_1;
    if (plVar3 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
      FUN_0021eccc();
    }
    iVar1 = (**(code **)(*plVar3 + 0x30))(plVar3,&local_28);
    if (iVar1 == 0) {
      (**(code **)(*param_1 + 0x60))(param_1);
      uVar2 = 0;
    }
    else {
      uVar2 = FUN_05694fd0(param_1);
    }
  }
  return uVar2;
}


