// Ghidra inferred pseudocode; requested=0x563fe60
// entry=0563fe60 end=0564000f

void FUN_0563fe60(undefined8 *param_1,undefined8 param_2,undefined8 param_3)

{
  long *plVar1;
  uint uVar2;
  long lVar3;
  long *plVar4;
  ulong uVar5;
  undefined1 auStack_a0 [24];
  long local_88;
  long *aplStack_80 [3];
  undefined1 auStack_68 [8];
  undefined8 local_60;
  long *local_50;
  long *local_48;
  
  local_50 = (long *)0x0;
  local_48 = (long *)0x0;
  uVar2 = (uint)param_3 & 0xff;
  if (uVar2 < 2) {
    FUN_05643aa4(&local_88,auStack_a0);
    local_50 = (long *)0x0;
    plVar4 = aplStack_80[0];
    if (local_88 != 0) {
      local_50 = (long *)(local_88 + 0x38);
    }
  }
  else if (uVar2 == 4) {
    plVar4 = (long *)__Znwm(0x290);
    plVar4[1] = 0;
    plVar4[2] = 0;
    *plVar4 = (long)&PTR_FUN_09f185f8;
    FUN_05648aec(plVar4 + 3);
    local_50 = plVar4 + 3;
  }
  else {
    plVar4 = (long *)__Znwm(0x280);
    plVar4[1] = 0;
    plVar4[2] = 0;
    *plVar4 = (long)&PTR_FUN_09f18648;
    plVar1 = plVar4 + 3;
    _bzero(plVar1,0x268);
    FUN_056455cc(plVar1);
    plVar4[3] = (long)&PTR_FUN_09f18ce8;
    local_50 = plVar1;
  }
  local_48 = plVar4;
  if (local_50 == (long *)0x0) {
    FUN_0562fcb4(auStack_a0);
    FUN_05632e9c(&local_88,7,5,auStack_a0);
    FUN_05627b10(param_2,&local_88);
    FUN_03b35c00(auStack_68,local_60);
    FUN_0562fd84(aplStack_80);
    FUN_0562fd84(auStack_a0);
    *param_1 = 0;
    param_1[1] = 0;
  }
  else {
    FUN_05696034(local_50,param_2);
    plVar4 = local_50;
    uVar5 = FUN_05640094(param_2,param_3,local_50);
    if ((uVar5 & 1) != 0) {
      *param_1 = plVar4;
      param_1[1] = local_48;
      return;
    }
    *param_1 = 0;
    param_1[1] = 0;
    plVar4 = local_48;
  }
  if (plVar4 != (long *)0x0) {
    LOAcquire();
    lVar3 = plVar4[1];
    plVar4[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*plVar4 + 0x10))(plVar4);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  return;
}


