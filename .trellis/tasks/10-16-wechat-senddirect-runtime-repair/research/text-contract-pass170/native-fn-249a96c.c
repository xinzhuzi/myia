// Ghidra inferred pseudocode; requested=0x249a96c
// entry=0249a96c end=0249aebf

void FUN_0249a96c(undefined8 param_1,long *param_2,undefined8 param_3)

{
  int iVar1;
  long lVar2;
  long *plVar3;
  undefined8 uVar4;
  long *plVar5;
  long *plVar6;
  undefined8 local_88 [2];
  undefined7 local_78;
  char cStack_71;
  long *local_70;
  long *local_68;
  undefined1 *local_60;
  long *local_58;
  undefined1 *local_50;
  long *local_48;
  
  local_50 = (undefined1 *)0x0;
  local_48 = (long *)0x0;
  if (*(int *)(*param_2 + 0x458) != 6) {
    local_60 = &SUB_aaaaaaaaaaaaaaaa;
    local_58 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    FUN_00d6bd24(&local_60,local_88);
    *(undefined4 *)(local_60 + 0xe4) = 0x2a;
    plVar3 = (long *)FUN_04669774();
    uVar4 = (**(code **)(*plVar3 + 0x28))();
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(local_60 + 0x90,uVar4);
    plVar5 = (long *)__Znwm(0x2e0);
    plVar6 = plVar5 + 1;
    *plVar6 = 0;
    plVar5[2] = 0;
    *plVar5 = (long)&PTR_FUN_09c83160;
    plVar3 = plVar5 + 3;
    _bzero(plVar3,0x2c8);
    if (plVar5 != (long *)0x0) {
      *plVar6 = *plVar6 + 1;
    }
    *(long **)(local_60 + 0x5c8) = plVar3;
    plVar6 = *(long **)(local_60 + 0x5d0);
    *(long **)(local_60 + 0x5d0) = plVar5;
    local_70 = plVar3;
    local_68 = plVar5;
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
    plVar3 = local_70;
    FUN_017b5a0c(local_70,param_1);
    FUN_012a58d8(plVar3,*param_2 + 0x78);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (plVar3,*param_2 + 0x138);
    FUN_013a5688(plVar3,*param_2 + 0x150);
    __ZNSt3__19to_stringEi(local_88,*(undefined4 *)(*param_2 + 0x54));
    FUN_017b5a14(plVar3,local_88);
    if (cStack_71 < '\0') {
      __ZdlPvm(local_88[0],CONCAT17(cStack_71,local_78) & 0x7fffffffffffffff);
    }
    FUN_017b5a24(plVar3,*param_2 + 0x30);
    FUN_017b5a1c(plVar3,*param_2 + 0x2d0);
    FUN_01520830(plVar3,*param_2 + 0x2e8);
    FUN_017b5a2c(plVar3,*param_2 + 0x300);
    FUN_017b6288(plVar3,*param_2 + 0x318);
    FUN_017b6290(plVar3,*param_2 + 0x330);
    FUN_04d1b398(plVar3,*param_2 + 0x348);
    FUN_04d1b3a0(plVar3,*param_2 + 0x360);
    FUN_04d1b3a8(plVar3,*(undefined4 *)(*param_2 + 0x378));
    FUN_04d1b3b0(plVar3,*param_2 + 0x380);
    FUN_04d1b3b8(plVar3,*param_2 + 0x398);
    FUN_018fb884(plVar3,*param_2 + 0x3b0);
    FUN_04d1b3c0(plVar3,*param_2 + 0x3c8);
    FUN_04d1b3c8(plVar3,*param_2 + 0x3e0);
    FUN_0136d508(plVar3,*param_2 + 0x3f8);
    FUN_04d1b3d0(plVar3,*param_2 + 0x410);
    iVar1 = 3;
    if (*(int *)(*param_2 + 0x458) != 1) {
      iVar1 = (uint)(*(int *)(*param_2 + 0x458) == 2) << 2;
    }
    FUN_04d1b410(plVar3,iVar1);
    goto LAB_0249adc4;
  }
  local_60 = &SUB_aaaaaaaaaaaaaaaa;
  local_58 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0249c8a0(&local_60,local_88);
  *(undefined8 *)(local_60 + 0xe4) = DAT_087b40d0;
  plVar3 = (long *)FUN_04669774();
  uVar4 = (**(code **)(*plVar3 + 0x28))();
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(local_60 + 0x90,uVar4);
  plVar3 = (long *)__Znwm(0xe0);
  plVar6 = plVar3 + 1;
  *plVar6 = 0;
  plVar3[2] = 0;
  *plVar3 = (long)&PTR_FUN_09d946e0;
  plVar5 = plVar3 + 3;
  plVar3[4] = 0;
  *plVar5 = 0;
  plVar3[6] = 0;
  plVar3[5] = 0;
  plVar3[8] = 0;
  plVar3[7] = 0;
  plVar3[10] = 0;
  plVar3[9] = 0;
  plVar3[0xc] = 0;
  plVar3[0xb] = 0;
  plVar3[0xe] = 0;
  plVar3[0xd] = 0;
  plVar3[0x10] = 0;
  plVar3[0xf] = 0;
  plVar3[0x12] = 0;
  plVar3[0x11] = 0;
  plVar3[0x14] = 0;
  plVar3[0x13] = 0;
  plVar3[0x16] = 0;
  plVar3[0x15] = 0;
  plVar3[0x18] = 0;
  plVar3[0x17] = 0;
  plVar3[0x1a] = 0;
  plVar3[0x19] = 0;
  plVar3[0x1b] = 0;
  local_70 = plVar5;
  local_68 = plVar3;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(plVar5,param_1);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (plVar3 + 6,*param_2 + 0x78);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (plVar3 + 9,*param_2 + 0x300);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (plVar3 + 0xc,*param_2 + 0x318);
  __ZNSt3__19to_stringEi(local_88,*(undefined4 *)(*param_2 + 0x378));
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(plVar3 + 0xf,local_88);
  if (cStack_71 < '\0') {
    __ZdlPvm(local_88[0],CONCAT17(cStack_71,local_78) & 0x7fffffffffffffff);
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (plVar3 + 0x15,*param_2 + 0x3b0);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (plVar3 + 0x18,*param_2 + 0x3c8);
  *(undefined4 *)(plVar3 + 0x1b) = 5;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (plVar3 + 0x12,*param_2 + 0x398);
  if (*(char *)((long)plVar3 + 0xa7) < '\0') {
    if (plVar3[0x13] == 0) goto LAB_0249ad6c;
  }
  else if (*(char *)((long)plVar3 + 0xa7) == '\0') {
LAB_0249ad6c:
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (plVar3 + 0x12,*param_2 + 0x138);
  }
  if (plVar3 != (long *)0x0) {
    *plVar6 = *plVar6 + 1;
  }
  *(long **)(local_60 + 0x640) = plVar5;
  plVar5 = *(long **)(local_60 + 0x648);
  *(long **)(local_60 + 0x648) = plVar3;
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
LAB_0249adc4:
  plVar3 = local_48;
  if (local_58 != (long *)0x0) {
    local_58[1] = local_58[1] + 1;
  }
  local_50 = local_60;
  local_48 = local_58;
  if (plVar3 != (long *)0x0) {
    LOAcquire();
    lVar2 = plVar3[1];
    plVar3[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*plVar3 + 0x10))(plVar3);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  plVar3 = local_68;
  if (local_68 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_68[1];
    local_68[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_68 + 0x10))(local_68);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  plVar3 = local_58;
  if (local_58 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_58[1];
    local_58[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_58 + 0x10))(local_58);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  FUN_0249a3f0(param_3,&local_50);
  plVar3 = local_48;
  if (local_48 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_48[1];
    local_48[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_48 + 0x10))(local_48);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  return;
}


