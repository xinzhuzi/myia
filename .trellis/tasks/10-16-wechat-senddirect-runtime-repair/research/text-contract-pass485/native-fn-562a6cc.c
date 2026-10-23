// Ghidra inferred pseudocode; requested=0x562a6cc
// entry=0562a6cc end=0562a747

void FUN_0562a6cc(long param_1)

{
  void *pvVar1;
  long lVar2;
  code *pcVar3;
  long lVar4;
  ulong uVar5;
  
  pvVar1 = *(void **)(param_1 + 8);
  if (pvVar1 != (void *)0x0) {
    lVar2 = *(long *)(param_1 + 0x10);
    if (0x1f < (ulong)(lVar2 - (long)pvVar1)) {
      lVar4 = 0;
      uVar5 = 0;
      do {
        pcVar3 = *(code **)(lVar2 + uVar5 * 8);
        if (pcVar3 != (code *)0x0) {
          (*pcVar3)((long)pvVar1 + lVar4);
          pvVar1 = *(void **)(param_1 + 8);
          lVar2 = *(long *)(param_1 + 0x10);
        }
        uVar5 = uVar5 + 1;
        lVar4 = lVar4 + 0x20;
      } while (uVar5 < (ulong)(lVar2 - (long)pvVar1) >> 5);
    }
    _free(pvVar1);
    *(undefined8 *)(param_1 + 8) = 0;
  }
  return;
}


