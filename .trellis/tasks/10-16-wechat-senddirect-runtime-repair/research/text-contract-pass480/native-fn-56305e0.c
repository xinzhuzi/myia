// Ghidra inferred pseudocode; requested=0x56305e0
// entry=056305e0 end=05630687

void FUN_056305e0(undefined8 *param_1,long param_2)

{
  int iVar1;
  undefined4 *puVar2;
  int *piVar3;
  
  piVar3 = (int *)param_1[2];
  if ((int *)((long)&MACH_HEADER.magic + 1) < piVar3) {
    LOAcquire();
    iVar1 = *piVar3;
    *piVar3 = iVar1 + -1;
    LORelease();
    if ((ulong)param_1[1] <= param_2 - 1U) {
      if (iVar1 == 1) {
        _free((void *)param_1[2]);
        *param_1 = "";
        param_1[1] = 0;
      }
      goto joined_r0x05630654;
    }
    if (iVar1 < 2) {
      *(undefined4 *)param_1[2] = 1;
      goto LAB_05630678;
    }
  }
  else {
joined_r0x05630654:
    if (param_2 == 0) {
      param_1[2] = 0;
      goto LAB_05630678;
    }
  }
  puVar2 = _malloc(param_2 + 5);
  param_1[2] = puVar2;
  if (puVar2 != (undefined4 *)0x0) {
    *puVar2 = 1;
  }
LAB_05630678:
  param_1[1] = param_2;
  return;
}


