// Ghidra inferred pseudocode; requested=0x6fe12fc
// entry=06fe12fc end=06fe1333

void FUN_06fe12fc(undefined8 *param_1,undefined8 *param_2)

{
  uint uVar1;
  int *piVar2;
  
  uVar1 = 10;
  *(undefined4 *)(param_1 + 1) = 10;
  piVar2 = (int *)*param_2;
  *param_1 = piVar2;
  if (*piVar2 - 1U < 0xfffffffe) {
    LOAcquire();
    *piVar2 = *piVar2 + 1;
    LORelease();
    uVar1 = *(uint *)(param_1 + 1) & 0xbfffffff;
  }
  *(uint *)(param_1 + 1) = uVar1;
  return;
}


