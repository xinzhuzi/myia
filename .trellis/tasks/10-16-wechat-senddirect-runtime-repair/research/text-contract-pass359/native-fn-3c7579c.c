// Ghidra inferred pseudocode; requested=0x3c7579c
// entry=03c7579c end=03c758c3

undefined8
FUN_03c7579c(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 *param_4)

{
  ulong uVar1;
  long *plVar2;
  long *plVar3;
  long lVar4;
  
  if (DAT_0a51e640 != (long *)0x0) {
    (**(code **)(*DAT_0a51e640 + 0x30))();
    plVar2 = DAT_0a51e640;
    plVar3 = &DAT_0a51e628;
    DAT_0a51e640 = (long *)0x0;
    if (plVar2 == &DAT_0a51e628) {
      lVar4 = 0x20;
    }
    else {
      if (plVar2 == (long *)0x0) goto LAB_03c7580c;
      lVar4 = 0x28;
      plVar3 = plVar2;
    }
    (**(code **)(*plVar3 + lVar4))();
  }
LAB_03c7580c:
  uVar1 = DAT_0a4266c8;
  if (-1 < (char)DAT_0a4266d0._7_1_) {
    uVar1 = (ulong)DAT_0a4266d0._7_1_;
  }
  if (uVar1 != 0) {
    uVar1 = DAT_0a426698;
    if (-1 < (char)DAT_0a4266a0._7_1_) {
      uVar1 = (ulong)DAT_0a4266a0._7_1_;
    }
    if (uVar1 != 0) {
      uVar1 = DAT_0a4266b0;
      if (-1 < (char)DAT_0a4266b8._7_1_) {
        uVar1 = (ulong)DAT_0a4266b8._7_1_;
      }
      if (uVar1 != 0) {
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (param_1,&DAT_0a4266c0);
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (param_2,&DAT_0a426690);
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (param_3,&DAT_0a4266a8);
        *param_4 = DAT_0a4266d8;
        return 1;
      }
    }
  }
  return 0;
}


