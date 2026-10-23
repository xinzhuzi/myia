// Ghidra inferred pseudocode; requested=0x4c91334
// entry=04c91334 end=04c91423

void FUN_04c91334(undefined8 param_1,undefined8 param_2,undefined8 *param_3)

{
  long lVar1;
  void *pvVar2;
  size_t sVar3;
  code *pcVar4;
  void *local_78;
  void *local_70;
  long local_68;
  undefined8 local_60;
  undefined8 uStack_58;
  ulong local_50;
  undefined4 local_48;
  
  local_78 = (void *)0x0;
  local_70 = (void *)0x0;
  local_68 = 0;
  pvVar2 = (void *)*param_3;
  sVar3 = param_3[1] - (long)pvVar2;
  if (sVar3 != 0) {
    if ((long)sVar3 < 0) {
      FUN_00801dbc(&local_78);
                    /* WARNING: Does not return */
      pcVar4 = (code *)SoftwareBreakpoint(1,0x4c91424);
      (*pcVar4)();
    }
    local_78 = (void *)__Znwm(sVar3);
    lVar1 = (long)local_78 + sVar3;
    local_68 = lVar1;
    _memcpy(local_78,pvVar2,sVar3);
    local_70 = (void *)lVar1;
  }
  if (*(char *)((long)param_3 + 0x2f) < '\0') {
    FUN_00018d20(&local_60,param_3[3],param_3[4]);
  }
  else {
    uStack_58 = param_3[4];
    local_60 = param_3[3];
    local_50 = param_3[5];
  }
  local_48 = *(undefined4 *)(param_3 + 6);
  FUN_04c91460(param_2,&local_78);
  if ((long)local_50 < 0) {
    __ZdlPvm(local_60,local_50 & 0x7fffffffffffffff);
  }
  if (local_78 != (void *)0x0) {
    local_70 = local_78;
    __ZdlPvm(local_78,local_68 - (long)local_78);
  }
  return;
}


