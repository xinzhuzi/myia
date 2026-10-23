// Ghidra inferred pseudocode; requested=0x30d80ac
// entry=030d80ac end=030d829f

void FUN_030d80ac(undefined8 param_1,long *param_2,long *param_3)

{
  long *plVar1;
  long lVar2;
  long lVar3;
  long local_80;
  long *local_78;
  long local_70;
  long *plStack_68;
  long local_60;
  long *local_58;
  long local_50;
  long *local_48;
  
  lVar2 = *param_3;
  lVar3 = *(long *)(lVar2 + 8);
  if (lVar3 == 0) {
    local_50 = 0;
    local_48 = (long *)0x0;
  }
  else {
    local_48 = *(long **)(lVar2 + 0x10);
    local_50 = lVar3;
    if (local_48 != (long *)0x0) {
      local_48[1] = local_48[1] + 1;
      lVar2 = *param_3;
    }
  }
  local_60 = *(long *)(lVar2 + 0x18);
  local_58 = *(long **)(lVar2 + 0x20);
  if (local_58 != (long *)0x0) {
    local_58[1] = local_58[1] + 1;
  }
  if (((lVar3 != 0 && local_60 != 0) && (*(char *)(lVar3 + 0xd8) == '\x01')) &&
     (lVar2 = *(long *)(local_60 + 0x220), lVar2 != 0)) {
    plStack_68 = *(long **)(local_60 + 0x228);
    local_70 = lVar2;
    if ((plStack_68 != (long *)0x0) &&
       (plStack_68[1] = plStack_68[1] + 1, (*(byte *)(lVar3 + 0xd8) & 1) == 0)) {
                    /* WARNING: Subroutine does not return */
      FUN_004d04d4();
    }
    *(undefined4 *)(lVar2 + 0xf0) = *(undefined4 *)(lVar3 + 0xb0);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (lVar2 + 0xf8,lVar3 + 0xb8);
    plVar1 = plStack_68;
    *(undefined4 *)(lVar2 + 0x110) = *(undefined4 *)(lVar3 + 0xd0);
    *(undefined4 *)(local_70 + 0x118) = *(undefined4 *)(local_50 + 0xe0);
    if (plStack_68 != (long *)0x0) {
      LOAcquire();
      lVar2 = plStack_68[1];
      plStack_68[1] = lVar2 + -1;
      LORelease();
      if (lVar2 == 0) {
        (**(code **)(*plStack_68 + 0x10))(plStack_68);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
      }
    }
  }
  local_80 = *param_3;
  local_78 = (long *)param_3[1];
  if (local_78 != (long *)0x0) {
    local_78[1] = local_78[1] + 1;
  }
  (**(code **)(*param_2 + 0x20))(param_1,param_2,&local_80);
  plVar1 = local_78;
  if (local_78 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_78[1];
    local_78[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_78 + 0x10))(local_78);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = local_58;
  if (local_58 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_58[1];
    local_58[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_58 + 0x10))(local_58);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = local_48;
  if (local_48 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_48[1];
    local_48[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_48 + 0x10))(local_48);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  return;
}


