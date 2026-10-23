// Ghidra inferred pseudocode; requested=0x562fd84
// entry=0562fd84 end=0562fddb

undefined8 * FUN_0562fd84(undefined8 *param_1)

{
  int iVar1;
  int *piVar2;
  
  piVar2 = (int *)param_1[2];
  if ((int *)((long)&MACH_HEADER.magic + 1) < piVar2) {
    LOAcquire();
    iVar1 = *piVar2;
    *piVar2 = iVar1 + -1;
    LORelease();
    if (iVar1 == 1) {
      _free((void *)param_1[2]);
      param_1[1] = 0;
      param_1[2] = 0;
      *param_1 = "";
    }
  }
  return param_1;
}


