// Ghidra inferred pseudocode; requested=0x564f828
// entry=0564f828 end=0564f96f

void FUN_0564f828(long param_1)

{
  long *plVar1;
  long *plVar2;
  long lVar3;
  
  if (*(long *)(param_1 + 0xa0) != 0) {
    plVar1 = *(long **)(param_1 + 0x98);
    plVar2 = *(long **)(*(long *)(param_1 + 0x90) + 8);
    lVar3 = *plVar1;
    *(long **)(lVar3 + 8) = plVar2;
    *plVar2 = lVar3;
    *(undefined8 *)(param_1 + 0xa0) = 0;
    while (plVar1 != (long *)(param_1 + 0x90)) {
      plVar2 = (long *)plVar1[1];
      (**(code **)plVar1[2])();
      __ZdlPvm(plVar1,400);
      plVar1 = plVar2;
    }
  }
  plVar1 = (long *)*(long *)(param_1 + 0x78);
  while (plVar1 != (long *)0x0) {
    lVar3 = *plVar1;
    __ZdlPvm(plVar1,0x20);
    plVar1 = (long *)lVar3;
  }
  lVar3 = *(long *)(param_1 + 0x68);
  *(undefined8 *)(param_1 + 0x68) = 0;
  if (lVar3 != 0) {
    __ZdlPvm(lVar3,*(long *)(param_1 + 0x70) << 3);
  }
  if (*(long *)(param_1 + 0x60) != 0) {
    plVar1 = *(long **)(param_1 + 0x58);
    plVar2 = *(long **)(*(long *)(param_1 + 0x50) + 8);
    lVar3 = *plVar1;
    *(long **)(lVar3 + 8) = plVar2;
    *plVar2 = lVar3;
    *(undefined8 *)(param_1 + 0x60) = 0;
    while (plVar1 != (long *)(param_1 + 0x50)) {
      plVar2 = (long *)plVar1[1];
      FUN_056caefc(plVar1 + 6);
      __ZdlPvm(plVar1,0xa0);
      plVar1 = plVar2;
    }
  }
  if (*(long *)(param_1 + 0x48) != 0) {
    plVar1 = *(long **)(param_1 + 0x40);
    plVar2 = *(long **)(*(long *)(param_1 + 0x38) + 8);
    lVar3 = *plVar1;
    *(long **)(lVar3 + 8) = plVar2;
    *plVar2 = lVar3;
    *(undefined8 *)(param_1 + 0x48) = 0;
    while (plVar1 != (long *)(param_1 + 0x38)) {
      plVar2 = (long *)plVar1[1];
      __ZdlPvm(plVar1,0x18);
      plVar1 = plVar2;
    }
  }
  FUN_0562a748(param_1);
  return;
}


