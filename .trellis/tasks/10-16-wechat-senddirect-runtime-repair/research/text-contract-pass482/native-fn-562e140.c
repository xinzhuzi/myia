// Ghidra inferred pseudocode; requested=0x562e140
// entry=0562e140 end=0562e19f

undefined8 * FUN_0562e140(undefined8 *param_1)

{
  long lVar1;
  long *plVar2;
  
  *param_1 = &PTR____cxa_pure_virtual_09da6188;
  plVar2 = (long *)param_1[2];
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


