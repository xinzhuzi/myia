// Ghidra inferred pseudocode; requested=0x335c0f0
// entry=0335c0f0 end=0335c1b3

void FUN_0335c0f0(long param_1)

{
  char cVar1;
  long lVar2;
  long *plVar3;
  
  if (param_1 == 0) {
    return;
  }
  plVar3 = *(long **)(param_1 + 0x60);
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
  plVar3 = *(long **)(param_1 + 0x50);
  if (plVar3 != (long *)0x0) {
    LOAcquire();
    lVar2 = plVar3[1];
    plVar3[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*plVar3 + 0x10))(plVar3);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
      cVar1 = *(char *)(param_1 + 0x47);
      goto joined_r0x0335c154;
    }
  }
  cVar1 = *(char *)(param_1 + 0x47);
joined_r0x0335c154:
  if (cVar1 < '\0') {
    __ZdlPvm(*(undefined8 *)(param_1 + 0x30),*(ulong *)(param_1 + 0x40) & 0x7fffffffffffffff);
  }
  __ZdlPvm(param_1,0x68);
  return;
}


