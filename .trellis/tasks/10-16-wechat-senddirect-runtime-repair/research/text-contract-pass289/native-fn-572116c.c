// Ghidra inferred pseudocode; requested=0x572116c
// entry=0572116c end=0572120b

long * FUN_0572116c(long *param_1)

{
  long lVar1;
  ulong *puVar2;
  long *plVar3;
  long lVar4;
  
  if (param_1[1] != 0) {
    (*(code *)PTR__free_0a120898)();
    param_1[1] = 0;
  }
  puVar2 = (ulong *)*param_1;
  plVar3 = (long *)puVar2[0xb];
  if (plVar3 != (long *)0x0) {
    do {
      if (*plVar3 != 0) {
        (*(code *)PTR__free_0a120898)();
      }
      plVar3 = (long *)plVar3[1];
    } while (plVar3 != (long *)0x0);
    puVar2 = (ulong *)*param_1;
  }
  lVar1 = *(long *)((long)puVar2 + (0x10 - (*puVar2 >> 8)));
  while (lVar1 != 0) {
    lVar4 = *(long *)(lVar1 + 0x10);
    (*(code *)PTR__free_0a120898)(lVar1);
    lVar1 = lVar4;
  }
  *param_1 = 0;
  return param_1;
}


