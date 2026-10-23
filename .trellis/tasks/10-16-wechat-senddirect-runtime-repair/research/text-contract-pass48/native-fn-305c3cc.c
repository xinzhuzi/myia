// Ghidra inferred pseudocode; requested=0x305c3cc
// entry=0305c3cc end=0305c45b

undefined4 * FUN_0305c3cc(undefined4 *param_1,undefined4 param_2,undefined4 param_3)

{
  long lVar1;
  undefined8 *puVar2;
  undefined8 uVar3;
  long *plVar4;
  
  *param_1 = param_2;
  param_1[1] = param_3;
  *(undefined8 *)(param_1 + 4) = 0;
  *(undefined8 *)(param_1 + 2) = 0;
  *(undefined8 *)(param_1 + 8) = 0;
  *(undefined8 *)(param_1 + 6) = 0;
  *(undefined8 *)(param_1 + 10) = 0;
  puVar2 = (undefined8 *)__Znwm(0x80);
  puVar2[1] = 0;
  puVar2[2] = 0;
  *puVar2 = &PTR_FUN_09de5678;
  uVar3 = FUN_050ef52c(puVar2 + 3);
  plVar4 = *(long **)(param_1 + 10);
  *(undefined8 *)(param_1 + 8) = uVar3;
  *(undefined8 **)(param_1 + 10) = puVar2;
  if (plVar4 != (long *)0x0) {
    LOAcquire();
    lVar1 = plVar4[1];
    plVar4[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*plVar4 + 0x10))(plVar4);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  return param_1;
}


