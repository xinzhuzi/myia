// Ghidra inferred pseudocode; requested=0x4c7ffe0
// entry=04c7ffa4 end=04c800af

void FUN_04c7ffa4(undefined8 *param_1,undefined8 param_2,long *param_3)

{
  long *plVar1;
  long lVar2;
  undefined1 *local_70;
  long *local_68;
  long local_60;
  long *local_58;
  undefined1 *local_50;
  long *plStack_48;
  undefined1 uStack_31;
  
  local_50 = &SUB_aaaaaaaaaaaaaaaa;
  plStack_48 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0077bdd0(&local_50,&uStack_31);
  *(undefined4 *)(local_50 + 0xe4) = 1;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (local_50 + 0x5c8,*param_3 + 0x148);
  local_60 = *param_3;
  local_58 = (long *)param_3[1];
  if (local_58 != (long *)0x0) {
    local_58[1] = local_58[1] + 1;
  }
  local_70 = local_50;
  local_68 = plStack_48;
  lVar2 = 0;
  if (plStack_48 != (long *)0x0) {
    lVar2 = plStack_48[1];
    plStack_48[1] = lVar2 + 1;
  }
  FUN_04c6c5d0(lVar2,param_2,&local_60,&local_70);
  plVar1 = local_68;
  if (local_68 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_68[1];
    local_68[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_68 + 0x10))(local_68);
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
  param_1[1] = plStack_48;
  *param_1 = local_50;
  return;
}


