// Ghidra inferred pseudocode; requested=0x5971c24
// entry=05971c24 end=05971d67

undefined8
FUN_05971c24(long param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
            undefined8 param_5,undefined8 param_6,undefined8 param_7,undefined8 param_8,
            undefined8 param_9,undefined2 param_10,undefined8 param_11)

{
  long lVar1;
  long *plVar2;
  ulong uVar3;
  undefined8 uVar4;
  
  if (*(long *)(param_1 + 0x20) == 0) {
    plVar2 = (long *)0x0;
  }
  else {
    plVar2 = (long *)__ZNSt3__119__shared_weak_count4lockEv();
    if (((plVar2 != (long *)0x0) && (*(long *)(param_1 + 0x18) != 0)) &&
       (uVar3 = FUN_05980a6c(*(long *)(param_1 + 0x18),param_2,param_3,param_4,param_5,param_6,
                             param_7,param_8,param_9,param_10), (uVar3 & 1) != 0)) {
      uVar4 = 1;
      goto LAB_05971d1c;
    }
  }
  uVar4 = FUN_0594c390(*(undefined8 *)(param_1 + 0x10));
  uVar4 = FUN_0597d26c(uVar4,param_2,param_3,param_4,param_5,param_6,param_7,param_8,param_9,
                       param_10,param_11);
  if (plVar2 == (long *)0x0) {
    return uVar4;
  }
LAB_05971d1c:
  LOAcquire();
  lVar1 = plVar2[1];
  plVar2[1] = lVar1 + -1;
  LORelease();
  if (lVar1 == 0) {
    (**(code **)(*plVar2 + 0x10))(plVar2);
    __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
  }
  return uVar4;
}


