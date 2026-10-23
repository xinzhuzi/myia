// Ghidra inferred pseudocode; requested=0x668614c
// entry=0668614c end=066862a7

undefined8 * FUN_0668614c(undefined8 *param_1)

{
  long lVar1;
  long lVar2;
  undefined8 uVar3;
  long *plVar4;
  long *plVar5;
  long *plVar6;
  
  *param_1 = &PTR_thunk_FUN_0668614c_09fb30b8;
  uVar3 = param_1[1];
  __ZNSt3__15mutex4lockEv(uVar3);
  lVar2 = param_1[1];
  plVar5 = (long *)*(long *)(lVar2 + 0x80);
  while (plVar4 = plVar5, plVar4 != (long *)0x0) {
    plVar5 = (long *)*plVar4;
    if ((*(uint *)(plVar4 + 7) >> 1 & 1) == 0) {
      *(uint *)(plVar4 + 7) = *(uint *)(plVar4 + 7) | 2;
      if (plVar4[6] != 0) {
        FUN_06685fd0(plVar4[6],param_1);
        lVar2 = param_1[1];
      }
      *(undefined1 *)(lVar2 + 0x99) = 1;
    }
  }
  __ZNSt3__15mutex6unlockEv(uVar3);
  lVar2 = param_1[1];
  __ZNSt3__115recursive_mutex4lockEv(lVar2 + 0x40);
  if (*(long *)(param_1[1] + 0x90) == 0) {
    __ZNSt3__115recursive_mutex6unlockEv(lVar2 + 0x40);
    lVar2 = param_1[1];
    if (lVar2 != 0) {
      plVar5 = *(long **)(lVar2 + 0x80);
      if (plVar5 != (long *)0x0) {
        do {
          plVar6 = (long *)*plVar5;
          plVar4 = (long *)plVar5[10];
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
          __ZdlPvm(plVar5,0x60);
          plVar5 = plVar6;
        } while (plVar6 != (long *)0x0);
        *(undefined8 *)(lVar2 + 0x80) = 0;
        *(long **)(lVar2 + 0x88) = (long *)(lVar2 + 0x80);
      }
      __ZNSt3__115recursive_mutexD1Ev(lVar2 + 0x40);
      uVar3 = __ZNSt3__15mutexD1Ev(lVar2);
      __ZdlPvm(uVar3,0xa0);
    }
  }
  else {
    *(undefined1 *)(param_1[1] + 0x98) = 1;
    __ZNSt3__115recursive_mutex6unlockEv(lVar2 + 0x40);
  }
  return param_1;
}


