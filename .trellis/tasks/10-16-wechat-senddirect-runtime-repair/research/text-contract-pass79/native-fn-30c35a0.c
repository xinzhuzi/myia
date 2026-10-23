// Ghidra inferred pseudocode; requested=0x30c35a0
// entry=030c35a0 end=030c370f

void FUN_030c35a0(undefined8 *param_1,long *param_2)

{
  long *plVar1;
  long lVar2;
  long *plVar3;
  long lVar4;
  long *plVar5;
  long local_60;
  long lStack_58;
  ulong local_50;
  long local_48;
  long *local_40;
  long *local_38;
  
  local_38 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  lVar4 = *param_2;
  if (*(char *)((long)param_2 + 0x1f) < '\0') {
    FUN_00018d20(&local_60,param_2[1],param_2[2]);
  }
  else {
    lStack_58 = param_2[2];
    local_60 = param_2[1];
    local_50 = param_2[3];
  }
  local_48 = param_2[4];
  local_40 = (long *)param_2[5];
  lVar2 = 0;
  if (local_40 != (long *)0x0) {
    lVar2 = local_40[1];
    local_40[1] = lVar2 + 1;
  }
  plVar3 = (long *)__Znwm(lVar2,0x48);
  *plVar3 = (long)&PTR_FUN_09de8330;
  plVar5 = plVar3 + 1;
  *plVar5 = lVar4;
  if ((long)local_50 < 0) {
    FUN_00018d20(plVar3 + 2,local_60,lStack_58);
  }
  else {
    plVar3[3] = lStack_58;
    plVar3[2] = local_60;
    plVar3[4] = local_50;
  }
  plVar1 = local_40;
  plVar3[5] = local_48;
  plVar3[6] = (long)local_40;
  local_38 = plVar3;
  if (local_40 == (long *)0x0) {
    plVar3[7] = (long)&PTR_DAT_09de8108;
    plVar3[8] = (long)plVar5;
  }
  else {
    local_40[1] = local_40[1] + 1;
    plVar3[7] = (long)&PTR_DAT_09de8108;
    plVar3[8] = (long)plVar5;
    if (local_40 != (long *)0x0) {
      LOAcquire();
      lVar4 = local_40[1];
      local_40[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*local_40 + 0x10))(local_40);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
      }
    }
  }
  if ((long)local_50 < 0) {
    __ZdlPvm(local_60,local_50 & 0x7fffffffffffffff);
  }
  FUN_066696dc(*param_1,&local_38);
  if (local_38 != (long *)0x0) {
    (**(code **)(*local_38 + 8))();
  }
  return;
}


