// Ghidra inferred pseudocode; requested=0x465d634
// entry=0465d634 end=0465d6ab

void FUN_0465d634(undefined8 *param_1)

{
  long *plVar1;
  int iVar2;
  long lVar3;
  
  *param_1 = &PTR_FUN_09e91df8;
  iVar2 = *(int *)((long)param_1 + 0x14);
  if (0 < iVar2) {
    lVar3 = 0;
    do {
      plVar1 = *(long **)(param_1[1] + lVar3 * 8);
      if (plVar1 != (long *)0x0) {
        (**(code **)(*plVar1 + 8))();
        iVar2 = *(int *)((long)param_1 + 0x14);
      }
      lVar3 = lVar3 + 1;
    } while (lVar3 < iVar2);
  }
  if (param_1[1] != 0) {
    __ZdaPv();
  }
  FUN_0001accc(param_1);
  return;
}


