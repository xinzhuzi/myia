// Ghidra inferred pseudocode; requested=0x4c6ed80
// entry=04c6ed80 end=04c6ef87

void FUN_04c6ed80(undefined8 *param_1,undefined8 param_2,long *param_3)

{
  undefined1 *puVar1;
  long lVar2;
  undefined8 uVar3;
  long lVar4;
  long *plVar5;
  long lVar6;
  undefined8 local_88 [2];
  undefined7 local_78;
  char cStack_71;
  long local_70;
  long *plStack_68;
  long local_60;
  long *local_58;
  long local_50;
  long *local_48;
  undefined1 *local_40;
  long *plStack_38;
  
  local_40 = &SUB_aaaaaaaaaaaaaaaa;
  plStack_38 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_50 = *param_3;
  local_48 = (long *)param_3[1];
  if (local_48 != (long *)0x0) {
    local_48[1] = local_48[1] + 1;
  }
  FUN_04c6b5b8(&local_40,param_2,&local_50);
  plVar5 = local_48;
  if (local_48 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_48[1];
    local_48[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_48 + 0x10))(local_48);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
    }
  }
  lVar4 = *param_3;
  lVar2 = *(long *)(lVar4 + 0x218);
  if ((lVar2 == 0) ||
     (lVar2 = ___dynamic_cast(lVar2,&PTR_DAT_09eb1040,&PTR_DAT_09eb0cc0,0), puVar1 = local_40,
     lVar2 == 0)) {
    *param_1 = 0;
    param_1[1] = 0;
  }
  else {
    local_58 = *(long **)(lVar4 + 0x220);
    lVar4 = 0;
    if (local_58 != (long *)0x0) {
      lVar4 = local_58[1];
      local_58[1] = lVar4 + 1;
    }
    lVar6 = *(long *)(lVar2 + 0x510);
    plVar5 = *(long **)(lVar2 + 0x518);
    if (plVar5 != (long *)0x0) {
      lVar4 = plVar5[1];
      plVar5[1] = lVar4 + 1;
    }
    local_70 = lVar6;
    plStack_68 = plVar5;
    local_60 = lVar2;
    if (lVar6 != 0) {
      uVar3 = FUN_04e2742c(lVar4);
      __ZNSt3__1plIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_12basic_stringIT_T0_T1_EEPKS6_RKS9_
                (local_88,uVar3,lVar6);
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (puVar1 + 0x130,local_88);
      if (cStack_71 < '\0') {
        __ZdlPvm(local_88[0],CONCAT17(cStack_71,local_78) & 0x7fffffffffffffff);
      }
      puVar1 = local_40;
      uVar3 = FUN_04e2742c();
      __ZNSt3__1plIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_12basic_stringIT_T0_T1_EEPKS6_RKS9_
                (local_88,uVar3,lVar6);
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (puVar1 + 0x148,local_88);
      if (cStack_71 < '\0') {
        __ZdlPvm(local_88[0],CONCAT17(cStack_71,local_78) & 0x7fffffffffffffff);
      }
    }
    if (plVar5 != (long *)0x0) {
      LOAcquire();
      lVar2 = plVar5[1];
      plVar5[1] = lVar2 + -1;
      LORelease();
      if (lVar2 == 0) {
        (**(code **)(*plVar5 + 0x10))(plVar5);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
      }
    }
    plVar5 = local_58;
    *(undefined4 *)(local_40 + 8) = 1;
    param_1[1] = plStack_38;
    *param_1 = local_40;
    local_40 = (undefined1 *)0x0;
    plStack_38 = (long *)0x0;
    if (local_58 != (long *)0x0) {
      LOAcquire();
      lVar2 = local_58[1];
      local_58[1] = lVar2 + -1;
      LORelease();
      if (lVar2 == 0) {
        (**(code **)(*local_58 + 0x10))(local_58);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
      }
    }
  }
  plVar5 = plStack_38;
  if (plStack_38 != (long *)0x0) {
    LOAcquire();
    lVar2 = plStack_38[1];
    plStack_38[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*plStack_38 + 0x10))(plStack_38);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
    }
  }
  return;
}


