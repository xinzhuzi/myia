// Ghidra inferred pseudocode; requested=0x335c4ec
// entry=0335c4ec end=0335c5a3

void FUN_0335c4ec(long param_1)

{
  char cVar1;
  long lVar2;
  long *plVar3;
  
  if (param_1 == 0) {
    return;
  }
  plVar3 = *(long **)(param_1 + 0x2d8);
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
  plVar3 = *(long **)(param_1 + 0x2c8);
  if (plVar3 != (long *)0x0) {
    LOAcquire();
    lVar2 = plVar3[1];
    plVar3[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*plVar3 + 0x10))(plVar3);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
      cVar1 = *(char *)(param_1 + 0x2b7);
      goto joined_r0x0335c54c;
    }
  }
  cVar1 = *(char *)(param_1 + 0x2b7);
joined_r0x0335c54c:
  if (cVar1 < '\0') {
    __ZdlPvm(*(undefined8 *)(param_1 + 0x2a0),*(ulong *)(param_1 + 0x2b0) & 0x7fffffffffffffff);
  }
  FUN_00ac6290(param_1 + 0x28);
  __ZdlPvm(param_1,0x2e0);
  return;
}


