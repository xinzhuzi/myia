// Ghidra inferred pseudocode; requested=0x4c8ce4c
// entry=04c8ce4c end=04c8cf0f

undefined8 * FUN_04c8ce4c(undefined8 *param_1,undefined8 *param_2)

{
  void *pvVar1;
  size_t sVar2;
  code *pcVar3;
  void *pvVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  
  *param_1 = &PTR_FUN_09eacef0;
  param_1[2] = 0;
  *(undefined4 *)(param_1 + 1) = 0;
  param_1[3] = 0;
  param_1[4] = 0;
  pvVar1 = (void *)*param_2;
  sVar2 = param_2[1] - (long)pvVar1;
  if (sVar2 != 0) {
    if ((long)sVar2 < 0) {
      FUN_00801dbc(param_1 + 2);
                    /* WARNING: Does not return */
      pcVar3 = (code *)SoftwareBreakpoint(1,0x4c8cf10);
      (*pcVar3)();
    }
    pvVar4 = (void *)__Znwm(sVar2);
    param_1[2] = pvVar4;
    param_1[3] = pvVar4;
    param_1[4] = (long)pvVar4 + sVar2;
    _memcpy(pvVar4,pvVar1,sVar2);
    param_1[3] = (long)pvVar4 + sVar2;
  }
  if (*(char *)((long)param_2 + 0x2f) < '\0') {
    FUN_00018d20(param_1 + 5,param_2[3],param_2[4]);
  }
  else {
    uVar6 = param_2[4];
    uVar5 = param_2[3];
    param_1[7] = param_2[5];
    param_1[6] = uVar6;
    param_1[5] = uVar5;
  }
  *(undefined4 *)(param_1 + 8) = *(undefined4 *)(param_2 + 6);
  return param_1;
}


