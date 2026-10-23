// Ghidra inferred pseudocode; requested=0x2877a18
// entry=02877a18 end=02877b17

undefined8 * FUN_02877a18(undefined8 *param_1)

{
  long *plVar1;
  long lVar2;
  code *pcVar3;
  long *plVar4;
  long *plVar5;
  
  *param_1 = &PTR_thunk_FUN_02877a18_09db21d0;
  plVar4 = (long *)param_1[9];
  if (plVar4 != (long *)0x0) {
    plVar5 = (long *)param_1[10];
    plVar1 = plVar4;
    if (plVar5 != plVar4) {
      do {
        plVar1 = (long *)plVar5[-1];
        plVar5 = plVar5 + -4;
        if (plVar5 == plVar1) {
          pcVar3 = *(code **)(*plVar1 + 0x20);
LAB_02877a5c:
          (*pcVar3)();
        }
        else if (plVar1 != (long *)0x0) {
          pcVar3 = *(code **)(*plVar1 + 0x28);
          goto LAB_02877a5c;
        }
      } while (plVar5 != plVar4);
      plVar1 = (long *)param_1[9];
    }
    param_1[10] = plVar4;
    __ZdlPvm(plVar1,param_1[0xb] - (long)plVar1);
  }
  plVar4 = (long *)param_1[6];
  while (plVar4 != (long *)0x0) {
    lVar2 = *plVar4;
    FUN_02877908(plVar4 + 5);
    if (*(char *)((long)plVar4 + 0x27) < '\0') {
      __ZdlPvm(plVar4[2],plVar4[4] & 0x7fffffffffffffff);
    }
    __ZdlPvm(plVar4,0x98);
    plVar4 = (long *)lVar2;
  }
  lVar2 = param_1[4];
  param_1[4] = 0;
  if (lVar2 != 0) {
    __ZdlPvm(lVar2,param_1[5] << 3);
  }
  if (param_1[2] != 0) {
    __ZNSt3__119__shared_weak_count14__release_weakEv();
  }
  return param_1;
}


