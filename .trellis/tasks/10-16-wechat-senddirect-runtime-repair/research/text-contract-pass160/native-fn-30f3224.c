// Ghidra inferred pseudocode; requested=0x30f3224
// entry=030f3224 end=030f348b

undefined8 * FUN_030f3224(undefined8 *param_1,long *param_2)

{
  undefined1 *puVar1;
  long lVar2;
  long lVar3;
  long *plVar4;
  undefined8 *puVar5;
  long *plVar6;
  undefined1 *local_50;
  long *local_48;
  long local_40;
  long *plStack_38;
  
  local_40 = *param_2;
  plVar4 = (long *)param_2[1];
  lVar2 = local_40;
  if (plVar4 != (long *)0x0) {
    lVar2 = plVar4[1];
    plVar4[1] = lVar2 + 1;
  }
  plStack_38 = plVar4;
  FUN_030ef9e0(lVar2,param_1,&local_40,0);
  if (plVar4 != (long *)0x0) {
    LOAcquire();
    lVar2 = plVar4[1];
    plVar4[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*plVar4 + 0x10))(plVar4);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  *param_1 = &PTR_thunk_FUN_030f34f8_09de9548;
  local_50 = &SUB_aaaaaaaaaaaaaaaa;
  local_48 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_039ee5e4(&local_50,*param_2 + 0xe8);
  puVar1 = local_50;
  plVar4 = (long *)__Znwm(0x290);
  plVar4[1] = 0;
  plVar4[2] = 0;
  *plVar4 = (long)&PTR_FUN_09c92390;
  lVar2 = FUN_00f57630(plVar4 + 3,puVar1);
  plVar6 = (long *)plVar4[0x48];
  plVar4[0x48] = 0;
  plVar4[0x47] = 0;
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
  puVar5 = (undefined8 *)__Znwm(0x128);
  puVar5[1] = 0;
  puVar5[2] = 0;
  *puVar5 = &PTR_FUN_09dd9070;
  puVar5[6] = 0;
  puVar5[5] = 0;
  puVar5[8] = 0;
  puVar5[7] = 0;
  puVar5[10] = 0;
  puVar5[9] = 0;
  puVar5[0xc] = 0;
  puVar5[0xb] = 0;
  puVar5[0xe] = 0;
  puVar5[0xd] = 0;
  puVar5[0x10] = 0;
  puVar5[0xf] = 0;
  puVar5[0x12] = 0;
  puVar5[0x11] = 0;
  puVar5[0x14] = 0;
  puVar5[0x13] = 0;
  puVar5[0x16] = 0;
  puVar5[0x15] = 0;
  puVar5[0x18] = 0;
  puVar5[0x17] = 0;
  puVar5[0x1a] = 0;
  puVar5[0x19] = 0;
  puVar5[0x1c] = 0;
  puVar5[0x1b] = 0;
  puVar5[0x1e] = 0;
  puVar5[0x1d] = 0;
  puVar5[0x20] = 0;
  puVar5[0x1f] = 0;
  puVar5[4] = 0;
  puVar5[3] = 0;
  puVar5[0x22] = 0;
  puVar5[0x21] = 0;
  puVar5[0x24] = 0;
  puVar5[0x23] = 0;
  *(undefined8 **)(lVar2 + 0x230) = puVar5 + 3;
  plVar6 = *(long **)(lVar2 + 0x238);
  *(undefined8 **)(lVar2 + 0x238) = puVar5;
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
  FUN_04cbc3ac(lVar2,1);
  if (plVar4 != (long *)0x0) {
    plVar4[1] = plVar4[1] + 1;
  }
  plVar6 = (long *)param_1[4];
  param_1[3] = lVar2;
  param_1[4] = plVar4;
  if (plVar6 != (long *)0x0) {
    LOAcquire();
    lVar2 = plVar6[1];
    plVar6[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*plVar6 + 0x10))(plVar6);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  if (plVar4 != (long *)0x0) {
    LOAcquire();
    lVar2 = plVar4[1];
    plVar4[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*plVar4 + 0x10))(plVar4);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  plVar4 = local_48;
  if (local_48 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_48[1];
    local_48[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_48 + 0x10))(local_48);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  return param_1;
}


