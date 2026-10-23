// Ghidra inferred pseudocode; requested=0x30ef9e0
// entry=030ef9e0 end=030efc2f

undefined8 * FUN_030ef9e0(undefined8 *param_1,long *param_2,undefined1 param_3)

{
  undefined8 uVar1;
  long *plVar2;
  long lVar3;
  long *plVar4;
  long *plVar5;
  long *plVar6;
  undefined8 local_60;
  long *plStack_58;
  
  *param_1 = &PTR_thunk_FUN_030f34f8_09de9528;
  param_1[1] = *param_2;
  lVar3 = param_2[1];
  param_1[2] = lVar3;
  if (lVar3 != 0) {
    *(long *)(lVar3 + 8) = *(long *)(lVar3 + 8) + 1;
  }
  param_1[4] = 0;
  param_1[3] = 0;
  param_1[6] = 0;
  param_1[5] = 0;
  param_1[8] = 0;
  param_1[7] = 0;
  param_1[0xd] = 0;
  param_1[10] = 0;
  param_1[9] = 0;
  param_1[0xc] = 0;
  param_1[0xb] = 0;
  FUN_021efaf0(param_1 + 0xe,&local_60);
  FUN_021efaf0(param_1 + 0x10,&local_60);
  FUN_021efaf0(param_1 + 0x12,&local_60);
  FUN_021efaf0(param_1 + 0x14,&local_60);
  *(undefined1 *)(param_1 + 0x16) = param_3;
  param_1[0x1b] = 0;
  param_1[0x1a] = 0;
  *(undefined8 *)((long)param_1 + 0xbc) = 0;
  *(undefined8 *)((long)param_1 + 0xb4) = 0;
  *(undefined8 *)((long)param_1 + 0xcc) = 0;
  *(undefined8 *)((long)param_1 + 0xc4) = 0;
  FUN_030efce4(&local_60,param_1);
  plVar2 = plStack_58;
  uVar1 = local_60;
  local_60 = 0;
  plStack_58 = (long *)0x0;
  plVar6 = (long *)param_1[4];
  param_1[4] = plVar2;
  param_1[3] = uVar1;
  if (plVar6 != (long *)0x0) {
    LOAcquire();
    lVar3 = plVar6[1];
    plVar6[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*plVar6 + 0x10))(plVar6);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  plVar2 = plStack_58;
  if (plStack_58 != (long *)0x0) {
    LOAcquire();
    lVar3 = plStack_58[1];
    plStack_58[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*plStack_58 + 0x10))(plStack_58);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 7,*param_2 + 0x90);
  plVar2 = (long *)__Znwm(0xc0);
  plVar5 = plVar2 + 1;
  *plVar5 = 0;
  plVar2[2] = 0;
  *plVar2 = (long)&PTR_FUN_09de95e0;
  plVar6 = plVar2 + 3;
  plVar2[4] = 0;
  *plVar6 = 0;
  plVar2[10] = 0;
  plVar2[9] = 0;
  plVar2[0xc] = 0;
  plVar2[0xb] = 0;
  plVar2[8] = 0;
  plVar2[7] = 0;
  plVar2[6] = 0;
  plVar2[5] = 0;
  plVar2[0x12] = 0;
  plVar2[0x11] = 0;
  plVar2[0x10] = 0;
  plVar2[0xf] = 0;
  plVar2[0xe] = 0;
  plVar2[0xd] = 0;
  plVar2[0x13] = 0;
  *(undefined1 *)plVar6 = 1;
  *(undefined8 *)((long)plVar2 + 0x56) = 0;
  *(undefined8 *)((long)plVar2 + 0x4e) = 0;
  *(undefined8 *)((long)plVar2 + 0x4c) = 0;
  *(undefined8 *)((long)plVar2 + 0x44) = 0;
  *(undefined8 *)((long)plVar2 + 0x3c) = 0;
  *(undefined8 *)((long)plVar2 + 0x34) = 0;
  *(undefined8 *)((long)plVar2 + 0x2c) = 0;
  *(undefined8 *)((long)plVar2 + 0x24) = 0;
  plVar2[0xf] = 0;
  plVar2[0xe] = 0;
  plVar2[0x11] = 0;
  plVar2[0x10] = 0;
  *(undefined2 *)(plVar2 + 0x12) = 0;
  *(undefined4 *)((long)plVar2 + 0x9c) = 1;
  plVar2[0x15] = 0;
  plVar2[0x14] = 0;
  plVar2[0x17] = 0;
  plVar2[0x16] = 0;
  if (plVar2 != (long *)0x0) {
    *plVar5 = *plVar5 + 1;
  }
  plVar4 = (long *)param_1[6];
  param_1[5] = plVar6;
  param_1[6] = plVar2;
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
  if (plVar2 != (long *)0x0) {
    LOAcquire();
    lVar3 = *plVar5;
    *plVar5 = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*plVar2 + 0x10))();
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  return param_1;
}


