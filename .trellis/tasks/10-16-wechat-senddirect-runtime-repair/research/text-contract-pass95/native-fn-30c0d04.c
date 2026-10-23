// Ghidra inferred pseudocode; requested=0x30c0d04
// entry=030c0d04 end=030c0deb

void FUN_030c0d04(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
                 undefined8 param_5,undefined8 param_6,long *param_7)

{
  long lVar1;
  long lVar2;
  long *local_58;
  
  local_58 = (long *)__Znwm(0x38);
  lVar2 = *param_7;
  *local_58 = (long)&PTR_FUN_09de80d0;
  local_58[1] = lVar2;
  if (*(char *)((long)param_7 + 0x1f) < '\0') {
    FUN_00018d20(local_58 + 2,param_7[1],param_7[2]);
  }
  else {
    lVar2 = param_7[1];
    local_58[3] = param_7[2];
    local_58[2] = lVar2;
    local_58[4] = param_7[3];
  }
  lVar2 = param_7[5];
  local_58[5] = param_7[4];
  local_58[6] = lVar2;
  lVar1 = 0;
  if (lVar2 != 0) {
    lVar1 = *(long *)(lVar2 + 8);
    *(long *)(lVar2 + 8) = lVar1 + 1;
  }
  FUN_066853a4(lVar1,param_1,param_2,param_3,param_4,param_5,param_6,&local_58);
  if (local_58 != (long *)0x0) {
    (**(code **)(*local_58 + 8))();
  }
  return;
}


