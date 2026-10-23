// Ghidra inferred pseudocode; requested=0x56c252c
// entry=056c252c end=056c25bf

undefined8 FUN_056c252c(long param_1)

{
  long *plVar1;
  long lVar2;
  undefined8 uVar3;
  
  if (*(char *)(param_1 + 0x20) == '\x01') {
    uVar3 = __ZNSt3__112__get_sp_mutEPKv(param_1 + 0x10);
    __ZNSt3__18__sp_mut4lockEv();
    plVar1 = *(long **)(param_1 + 0x18);
    *(undefined8 *)(param_1 + 0x10) = 0;
    *(undefined8 *)(param_1 + 0x18) = 0;
    __ZNSt3__18__sp_mut6unlockEv(uVar3);
    if (plVar1 != (long *)0x0) {
      LOAcquire();
      lVar2 = plVar1[1];
      plVar1[1] = lVar2 + -1;
      LORelease();
      if (lVar2 == 0) {
        (**(code **)(*plVar1 + 0x10))(plVar1);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
      }
    }
    *(undefined1 *)(param_1 + 0x20) = 0;
  }
  return *(undefined8 *)(param_1 + 8);
}


