// Ghidra inferred pseudocode; requested=0x4551eac
// entry=04551eac end=04552293

/* WARNING: Removing unreachable block (ram,0x04551fa4) */

void FUN_04551eac(undefined8 *param_1,long *param_2,undefined4 *param_3)

{
  long lVar1;
  long *plVar2;
  undefined4 local_170 [2];
  undefined1 auStack_168 [160];
  undefined8 local_c8;
  undefined8 uStack_c0;
  undefined8 local_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined1 *local_88;
  long *local_80;
  undefined1 *local_78;
  long *local_70;
  long *local_68;
  long *local_60;
  long *local_58;
  long *local_50;
  ulong local_48;
  
  local_170[0] = *param_3;
  FUN_002c688c(auStack_168,param_3 + 2);
  if (*(char *)((long)param_3 + 0xbf) < '\0') {
    FUN_00018d20(&local_c8,*(undefined8 *)(param_3 + 0x2a),*(undefined8 *)(param_3 + 0x2c));
  }
  else {
    uStack_c0 = *(undefined8 *)(param_3 + 0x2c);
    local_c8 = *(undefined8 *)(param_3 + 0x2a);
    local_b8 = *(undefined8 *)(param_3 + 0x2e);
  }
  if (*(char *)((long)param_3 + 0xd7) < '\0') {
    FUN_00018d20(&local_b0,*(undefined8 *)(param_3 + 0x30),*(undefined8 *)(param_3 + 0x32));
  }
  else {
    uStack_a8 = *(undefined8 *)(param_3 + 0x32);
    local_b0 = *(undefined8 *)(param_3 + 0x30);
    local_a0 = *(undefined8 *)(param_3 + 0x34);
  }
  uStack_90 = *(undefined8 *)(param_3 + 0x38);
  local_98 = *(undefined8 *)(param_3 + 0x36);
  local_78 = &SUB_aaaaaaaaaaaaaaaa;
  local_70 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_021efaf0(&local_78,&local_58);
  local_88 = local_78;
  local_80 = local_70;
  lVar1 = 0;
  if (local_70 != (long *)0x0) {
    lVar1 = local_70[1];
    local_70[1] = lVar1 + 1;
  }
  FUN_0456c0c8(lVar1,param_2[0x62],local_170);
  FUN_04669774();
  FUN_0466ad74(&local_68);
  local_48 = local_48 & 0xffffffffffffff;
  local_58 = (long *)((ulong)local_58 & 0xffffffffffffff00);
  FUN_0453df64(local_68,&local_58);
  plVar2 = local_60;
  if (local_60 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_60[1];
    local_60[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_60 + 0x10))(local_60);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  FUN_04553a90(&local_68,param_2);
  local_58 = local_68;
  local_50 = local_60;
  lVar1 = 0;
  if (local_60 != (long *)0x0) {
    lVar1 = local_60[1];
    local_60[1] = lVar1 + 1;
  }
  local_48 = 0;
  FUN_066856fc(lVar1,&local_58);
  FUN_0666a844(local_58);
  plVar2 = local_50;
  if (local_50 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_50[1];
    local_50[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_50 + 0x10))(local_50);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  if (local_60 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_60[1];
    local_60[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_60 + 0x10))(local_60);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_60);
    }
  }
  FUN_04553444(param_2);
  plVar2 = (long *)param_2[0x6a];
  param_2[0x69] = 0;
  param_2[0x6a] = 0;
  if (plVar2 != (long *)0x0) {
    LOAcquire();
    lVar1 = plVar2[1];
    plVar2[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*plVar2 + 0x10))(plVar2);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  plVar2 = (long *)param_2[0x6c];
  param_2[0x6b] = 0;
  param_2[0x6c] = 0;
  if (plVar2 != (long *)0x0) {
    LOAcquire();
    lVar1 = plVar2[1];
    plVar2[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*plVar2 + 0x10))(plVar2);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  FUN_0456c6d8(param_2[0x62],local_170);
  (**(code **)(*param_2 + 0x28))(&local_58,param_2);
  FUN_04537f2c(local_58);
  plVar2 = local_50;
  if (local_50 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_50[1];
    local_50[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_50 + 0x10))(local_50);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  FUN_04551af4(&local_58,param_2);
  FUN_0453b03c(local_58);
  plVar2 = local_50;
  if (local_50 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_50[1];
    local_50[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_50 + 0x10))(local_50);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
      lVar1 = param_2[0x73];
      goto joined_r0x04552178;
    }
  }
  lVar1 = param_2[0x73];
joined_r0x04552178:
  if (lVar1 != 0) {
    FUN_03b09e28();
    plVar2 = (long *)param_2[0x74];
    param_2[0x73] = 0;
    param_2[0x74] = 0;
    if (plVar2 != (long *)0x0) {
      LOAcquire();
      lVar1 = plVar2[1];
      plVar2[1] = lVar1 + -1;
      LORelease();
      if (lVar1 == 0) {
        (**(code **)(*plVar2 + 0x10))(plVar2);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
      }
    }
  }
  local_58 = (long *)0x0;
  FUN_066696dc(local_88,&local_58);
  if (local_58 != (long *)0x0) {
    (**(code **)(*local_58 + 8))();
  }
  plVar2 = local_80;
  if (local_80 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_80[1];
    local_80[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_80 + 0x10))(local_80);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  plVar2 = local_70;
  *param_1 = local_78;
  param_1[1] = local_70;
  if ((local_70 != (long *)0x0) && (local_70[1] = local_70[1] + 1, local_70 != (long *)0x0)) {
    LOAcquire();
    lVar1 = local_70[1];
    local_70[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_70 + 0x10))(local_70);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  FUN_002c6a5c(local_170);
  return;
}


