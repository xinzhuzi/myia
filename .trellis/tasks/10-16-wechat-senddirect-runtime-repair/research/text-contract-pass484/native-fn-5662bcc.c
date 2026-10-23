// Ghidra inferred pseudocode; requested=0x5662bcc
// entry=05662bcc end=05662c33

void FUN_05662bcc(undefined8 *param_1,ulong param_2)

{
  void *pvVar1;
  
  if ((param_2 >> 0x14 == 0) && (0xfffff < (ulong)param_1[1])) {
    _free((void *)*param_1);
    *param_1 = 0;
  }
  pvVar1 = (void *)*param_1;
  if (param_2 < (ulong)param_1[1]) {
    if (pvVar1 != (void *)0x0) {
      return;
    }
  }
  else if (pvVar1 != (void *)0x0) {
    _free(pvVar1);
  }
  pvVar1 = _malloc(param_2);
  *param_1 = pvVar1;
  param_1[1] = param_2;
  return;
}


