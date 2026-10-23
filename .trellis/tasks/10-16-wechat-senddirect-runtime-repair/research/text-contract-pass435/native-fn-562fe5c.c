// Ghidra inferred pseudocode; requested=0x562fe5c
// entry=0562fe5c end=0562fedb

void FUN_0562fe5c(undefined8 *param_1,undefined8 *param_2)

{
  int iVar1;
  int *piVar2;
  undefined8 uVar3;
  
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
  uVar3 = *param_2;
  param_1[1] = param_2[1];
  *param_1 = uVar3;
  param_1[2] = param_2[2];
  param_2[1] = 0;
  param_2[2] = 0;
  *param_2 = "";
  return;
}


