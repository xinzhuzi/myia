// Ghidra inferred pseudocode; requested=0x4666b54
// entry=04666b54 end=04666e47

undefined8 * FUN_04666b54(undefined8 *param_1,undefined8 param_2)

{
  ulong uVar1;
  long *plVar2;
  long lVar3;
  undefined8 *puVar4;
  undefined8 uVar5;
  long *plVar6;
  undefined8 uVar7;
  undefined8 local_70;
  long *plStack_68;
  undefined1 uStack_51;
  
  *param_1 = &PTR____cxa_pure_virtual_09e92338;
  FUN_0027b118(param_1 + 1);
  FUN_04676914(param_1 + 3);
  FUN_04676914(param_1 + 5);
  *param_1 = &PTR_thunk_FUN_04667014_09e92400;
  local_70 = (ulong)local_70._4_4_ << 0x20;
  FUN_046783cc(param_1 + 7,&local_70);
  local_70 = local_70 & 0xffffffffffffff00;
  FUN_00287f00(param_1 + 9,&local_70);
  FUN_04678d8c(param_1 + 0xb);
  param_1[0xd] = 0;
  param_1[0xe] = 0;
  puVar4 = (undefined8 *)__Znwm(0x48);
  puVar4[1] = 0;
  puVar4[2] = 0;
  *puVar4 = &PTR_FUN_09e87830;
  puVar4[6] = 0;
  puVar4[5] = 0;
  puVar4[7] = 0;
  puVar4[8] = 0;
  puVar4[4] = 0;
  puVar4[3] = 0;
  *(undefined4 *)(puVar4 + 7) = 0x3f800000;
  param_1[0x11] = 0;
  param_1[0xf] = puVar4 + 3;
  param_1[0x10] = puVar4;
  param_1[0x12] = 0;
  puVar4 = (undefined8 *)__Znwm(0x70);
  puVar4[1] = 0;
  puVar4[2] = 0;
  *puVar4 = &PTR_FUN_09e87880;
  puVar4[8] = 0;
  puVar4[7] = 0;
  puVar4[10] = 0;
  puVar4[9] = 0;
  puVar4[0xc] = 0;
  puVar4[0xb] = 0;
  puVar4[6] = 0;
  puVar4[5] = 0;
  puVar4[4] = 0;
  puVar4[3] = 0;
  *(undefined4 *)(puVar4 + 7) = 0x3f800000;
  puVar4[9] = 0;
  puVar4[8] = 0;
  puVar4[0xb] = 0;
  puVar4[10] = 0;
  *(undefined4 *)(puVar4 + 0xc) = 0x3f800000;
  puVar4[0xd] = 0;
  param_1[0x13] = puVar4 + 3;
  param_1[0x14] = puVar4;
  uVar5 = __Znwm(1);
  FUN_0001accc();
  param_1[0x16] = 0;
  param_1[0x15] = uVar5;
  param_1[0x17] = 0;
  *(undefined1 *)(param_1 + 0x18) = 0;
  FUN_046770e8(param_1 + 0x19,param_2);
  param_1[0x4b] = 0;
  param_1[0x4a] = 0;
  param_1[0x4d] = 0;
  param_1[0x4c] = 0;
  uVar5 = __Znwm(0x18);
  FUN_0002b2c0();
  param_1[0x4e] = uVar5;
  param_1[0x4f] = 0;
  param_1[0x51] = 0;
  param_1[0x50] = 0;
  puVar4 = (undefined8 *)__Znwm(0x60);
  puVar4[1] = 0;
  puVar4[2] = 0;
  *puVar4 = &PTR_FUN_09e92808;
  uVar5 = thunk_FUN_0453b674(puVar4 + 3);
  param_1[0x52] = uVar5;
  param_1[0x53] = puVar4;
  param_1[0x55] = 0;
  param_1[0x54] = 0;
  *(undefined4 *)(param_1 + 0x56) = 0;
  *(undefined1 *)(param_1 + 0x59) = 0;
  param_1[0x58] = 0;
  param_1[0x57] = 0;
  *(undefined8 *)((long)param_1 + 0x2d4) = 0;
  *(undefined8 *)((long)param_1 + 0x2cc) = 0;
  *(undefined8 *)((long)param_1 + 0x2e4) = 0;
  *(undefined8 *)((long)param_1 + 0x2dc) = 0;
  *(undefined8 *)((long)param_1 + 0x2f4) = 0;
  *(undefined8 *)((long)param_1 + 0x2ec) = 0;
  *(undefined8 *)((long)param_1 + 0x2f9) = 0;
  FUN_04679560(&local_70,&uStack_51);
  plVar2 = plStack_68;
  uVar1 = local_70;
  local_70 = 0;
  plStack_68 = (long *)0x0;
  plVar6 = (long *)param_1[0x12];
  param_1[0x12] = plVar2;
  param_1[0x11] = uVar1;
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
  plVar2 = plStack_68;
  if (plStack_68 != (long *)0x0) {
    LOAcquire();
    lVar3 = plStack_68[1];
    plStack_68[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*plStack_68 + 0x10))(plStack_68);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  uVar7 = param_1[0xf];
  uVar5 = FUN_04a1779c();
  FUN_0456f23c(uVar7,uVar5);
  uVar7 = param_1[0x13];
  uVar5 = FUN_04a0d4a0();
  FUN_013a6570(uVar7,uVar5);
  FUN_04a705fc(&local_70);
  plVar2 = plStack_68;
  uVar5 = local_70;
  local_70 = 0;
  plStack_68 = (long *)0x0;
  plVar6 = (long *)param_1[0x17];
  param_1[0x17] = plVar2;
  param_1[0x16] = uVar5;
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
  plVar2 = plStack_68;
  if (plStack_68 != (long *)0x0) {
    LOAcquire();
    lVar3 = plStack_68[1];
    plStack_68[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*plStack_68 + 0x10))(plStack_68);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  return param_1;
}


