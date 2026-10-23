// Ghidra inferred pseudocode; requested=0x562e260
// entry=0562e260 end=0562e287

void FUN_0562e260(long *param_1)

{
  int iVar1;
  int *piVar2;
  
  piVar2 = (int *)param_1[1];
  if (piVar2 != (int *)0x0) {
    LOAcquire();
    iVar1 = *piVar2;
    *piVar2 = iVar1 + -1;
    LORelease();
    if (iVar1 == 1) {
                    /* WARNING: Could not recover jumptable at 0x0562e280. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(*param_1 + 0x10))();
      return;
    }
  }
  return;
}


