// Ghidra inferred pseudocode; requested=0x292d940
// entry=0292d940 end=0292da37

long FUN_0292d940(long param_1)

{
  char cVar1;
  long lVar2;
  long *plVar3;
  
  plVar3 = *(long **)(param_1 + 0x60);
  if (plVar3 == (long *)0x0) {
LAB_0292d968:
    cVar1 = *(char *)(param_1 + 0x4f);
  }
  else {
    LOAcquire();
    lVar2 = plVar3[1];
    plVar3[1] = lVar2 + -1;
    LORelease();
    if (lVar2 != 0) goto LAB_0292d968;
    (**(code **)(*plVar3 + 0x10))(plVar3);
    __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    cVar1 = *(char *)(param_1 + 0x4f);
  }
  if (cVar1 < '\0') {
    __ZdlPvm(*(undefined8 *)(param_1 + 0x38),*(ulong *)(param_1 + 0x48) & 0x7fffffffffffffff);
  }
  plVar3 = *(long **)(param_1 + 0x30);
  if (plVar3 != (long *)0x0) {
    LOAcquire();
    lVar2 = plVar3[1];
    plVar3[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*plVar3 + 0x10))(plVar3);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
      cVar1 = *(char *)(param_1 + 0x27);
      goto joined_r0x0292d99c;
    }
  }
  cVar1 = *(char *)(param_1 + 0x27);
joined_r0x0292d99c:
  if (cVar1 < '\0') {
    __ZdlPvm(*(undefined8 *)(param_1 + 0x10),*(ulong *)(param_1 + 0x20) & 0x7fffffffffffffff);
  }
  plVar3 = *(long **)(param_1 + 8);
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
  return param_1;
}


