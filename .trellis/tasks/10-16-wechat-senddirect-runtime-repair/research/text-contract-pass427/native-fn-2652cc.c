// Ghidra inferred pseudocode; requested=0x2652cc
// entry=002652cc end=00265327

undefined8 * FUN_002652cc(undefined8 *param_1,undefined8 *param_2)

{
  long lVar1;
  long *plVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  
  uVar4 = param_2[1];
  uVar3 = *param_2;
  *param_2 = 0;
  param_2[1] = 0;
  plVar2 = (long *)param_1[1];
  param_1[1] = uVar4;
  *param_1 = uVar3;
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
  return param_1;
}


