// Ghidra inferred pseudocode; requested=0x465ed38
// entry=0465ed38 end=0465edd3

void FUN_0465ed38(undefined8 *param_1)

{
  long *plVar1;
  int iVar2;
  long lVar3;
  
  *param_1 = &PTR_FUN_09e91ee8;
  if ((DAT_0a51ea50 != param_1) && ((long *)param_1[1] != (long *)0x0)) {
    (**(code **)(*(long *)param_1[1] + 8))();
  }
  iVar2 = *(int *)((long)param_1 + 0x1c);
  if (0 < iVar2) {
    lVar3 = 0;
    do {
      plVar1 = *(long **)(param_1[2] + lVar3 * 8);
      if (plVar1 != (long *)0x0) {
        (**(code **)(*plVar1 + 8))();
        iVar2 = *(int *)((long)param_1 + 0x1c);
      }
      lVar3 = lVar3 + 1;
    } while (lVar3 < iVar2);
  }
  if (param_1[2] != 0) {
    __ZdaPv();
  }
  FUN_0001accc(param_1);
  return;
}


