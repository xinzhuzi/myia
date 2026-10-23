// Ghidra inferred pseudocode; requested=0x33c7c
// entry=00033c7c end=00033ccb

undefined8 * FUN_00033c7c(undefined8 *param_1,undefined8 *param_2)

{
  int iVar1;
  int *piVar2;
  undefined8 uVar3;
  
  uVar3 = *param_2;
  *param_2 = 0;
  piVar2 = (int *)*param_1;
  *param_1 = uVar3;
  if (piVar2 != (int *)0x0) {
    LOAcquire();
    iVar1 = *piVar2;
    *piVar2 = iVar1 + -1;
    LORelease();
    if (iVar1 == 1) {
      (**(code **)(piVar2 + 4))(piVar2);
    }
  }
  return param_1;
}


