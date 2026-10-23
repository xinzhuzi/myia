// Ghidra inferred pseudocode; requested=0x5699d70
// entry=05699d70 end=05699df7

undefined8 FUN_05699d70(long param_1)

{
  long *plVar1;
  ulong uVar2;
  undefined8 uVar3;
  
  if ((*(byte *)(param_1 + 0x198) & 1) == 0) {
    uVar2 = FUN_056a0008(param_1);
  }
  else {
    plVar1 = *(long **)(*(long *)(param_1 + 0x188) + 0x18);
    if (plVar1 == (long *)0x0) goto LAB_05699df4;
    uVar2 = (**(code **)(*plVar1 + 0x30))();
  }
  if ((uVar2 & 1) == 0) {
    if ((*(byte *)(param_1 + 0x198) & 1) == 0) {
      FUN_056a15c0(param_1);
    }
    else {
      plVar1 = *(long **)(*(long *)(param_1 + 0x188) + 0x38);
      if (plVar1 == (long *)0x0) {
LAB_05699df4:
                    /* WARNING: Subroutine does not return */
        FUN_0021eccc();
      }
      (**(code **)(*plVar1 + 0x30))();
    }
    uVar3 = 0;
  }
  else {
    uVar3 = 1;
  }
  return uVar3;
}


