// Ghidra inferred pseudocode; requested=0x562a748
// entry=0562a748 end=0562a7d3

undefined8 * FUN_0562a748(undefined8 *param_1)

{
  void *pvVar1;
  long lVar2;
  code *pcVar3;
  long lVar4;
  ulong uVar5;
  
  *param_1 = &PTR_FUN_09f173c8;
  pvVar1 = (void *)param_1[1];
  if (pvVar1 != (void *)0x0) {
    lVar2 = param_1[2];
    if (0x1f < (ulong)(lVar2 - (long)pvVar1)) {
      lVar4 = 0;
      uVar5 = 0;
      do {
        pcVar3 = *(code **)(lVar2 + uVar5 * 8);
        if (pcVar3 != (code *)0x0) {
          (*pcVar3)((long)pvVar1 + lVar4);
          pvVar1 = (void *)param_1[1];
          lVar2 = param_1[2];
        }
        uVar5 = uVar5 + 1;
        lVar4 = lVar4 + 0x20;
      } while (uVar5 < (ulong)(lVar2 - (long)pvVar1) >> 5);
    }
    _free(pvVar1);
    param_1[1] = 0;
  }
  return param_1;
}


