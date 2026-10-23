// Ghidra inferred pseudocode; requested=0x317df64
// entry=0317df64 end=0317e123

void FUN_0317df64(undefined8 param_1,long param_2,long *param_3,undefined8 param_4)

{
  long *plVar1;
  long *plVar2;
  long lVar3;
  long *plVar4;
  undefined8 uVar5;
  long *plVar6;
  undefined1 uStack_81;
  long *local_80;
  long *local_78;
  long *local_70;
  long *local_68;
  long local_60;
  long *local_58;
  
  local_70 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_68 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  plVar4 = (long *)__Znwm(0xf8);
  plVar6 = plVar4 + 1;
  *plVar6 = 0;
  plVar4[2] = 0;
  *plVar4 = (long)&PTR_FUN_09ddab98;
  plVar1 = plVar4 + 3;
  local_60 = *param_3;
  local_58 = (long *)param_3[1];
  lVar3 = 0;
  if (local_58 != (long *)0x0) {
    lVar3 = local_58[1];
    local_58[1] = lVar3 + 1;
  }
  uVar5 = thunk_FUN_030ef9e0(lVar3,plVar1,&local_60,param_4);
  plVar2 = local_58;
  if (local_58 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_58[1];
    local_58[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_58 + 0x10))(local_58);
      uVar5 = __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  lVar3 = *(long *)(param_2 + 0xb20);
  if (plVar4 != (long *)0x0) {
    *plVar6 = *plVar6 + 1;
  }
  local_80 = plVar1;
  local_78 = plVar4;
  local_70 = plVar1;
  local_68 = plVar4;
  FUN_03181628(uVar5,lVar3 + 0x60,&local_80,plVar4 + 10);
  plVar1 = local_78;
  if (local_78 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_78[1];
    local_78[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_78 + 0x10))(local_78);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = local_70;
  FUN_03182084(param_2,local_70 + 7);
  local_60 = plVar1[0xe];
  local_58 = (long *)plVar1[0xf];
  if (local_58 != (long *)0x0) {
    local_58[1] = local_58[1] + 1;
  }
  FUN_03189980(param_1,&uStack_81,&local_60);
  plVar1 = local_58;
  if (local_58 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_58[1];
    local_58[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_58 + 0x10))(local_58);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = local_68;
  if (local_68 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_68[1];
    local_68[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_68 + 0x10))(local_68);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  return;
}


