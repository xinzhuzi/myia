// Ghidra inferred pseudocode; requested=0x567f1a0
// entry=0567f1a0 end=0567f21f

void FUN_0567f1a0(long param_1)

{
  long *plVar1;
  long *plVar2;
  long lVar3;
  
  if (*(long *)(param_1 + 0x40) != 0) {
    plVar1 = *(long **)(param_1 + 0x38);
    plVar2 = *(long **)(*(long *)(param_1 + 0x30) + 8);
    lVar3 = *plVar1;
    *(long **)(lVar3 + 8) = plVar2;
    *plVar2 = lVar3;
    *(undefined8 *)(param_1 + 0x40) = 0;
    while (plVar1 != (long *)(param_1 + 0x30)) {
      plVar2 = (long *)plVar1[1];
      (**(code **)plVar1[2])();
      __ZdlPvm(plVar1,400);
      plVar1 = plVar2;
    }
  }
  FUN_0562a748(param_1);
  return;
}


