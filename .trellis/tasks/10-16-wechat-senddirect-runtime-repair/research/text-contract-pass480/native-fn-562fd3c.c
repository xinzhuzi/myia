// Ghidra inferred pseudocode; requested=0x562fd3c
// entry=0562fd3c end=0562fd5f

void FUN_0562fd3c(undefined8 *param_1,undefined8 *param_2)

{
  undefined8 uVar1;
  int *piVar2;
  
  uVar1 = param_2[1];
  *param_1 = *param_2;
  param_1[1] = uVar1;
  piVar2 = (int *)param_2[2];
  param_1[2] = piVar2;
  if ((int *)((long)&MACH_HEADER.magic + 1) < piVar2) {
    LOAcquire();
    *piVar2 = *piVar2 + 1;
    LORelease();
  }
  return;
}


