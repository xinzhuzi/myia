// Ghidra inferred pseudocode; requested=0x5ce5494
// entry=05ce540c end=05ce54cb

void FUN_05ce540c(long param_1)

{
  undefined8 *puVar1;
  
  puVar1 = *(undefined8 **)(param_1 + 0x10);
  if (puVar1 != &DAT_0a524ad0 && puVar1 != (undefined8 *)0x0) {
    if (*(char *)((long)puVar1 + 0x17) < '\0') {
      __ZdlPv(*puVar1);
    }
    __ZdlPv(puVar1);
  }
  puVar1 = *(undefined8 **)(param_1 + 0x20);
  if (puVar1 != &DAT_0a524ad0 && puVar1 != (undefined8 *)0x0) {
    if (*(char *)((long)puVar1 + 0x17) < '\0') {
      __ZdlPv(*puVar1);
    }
    __ZdlPv(puVar1);
  }
  if (DAT_0a5250d8 != param_1) {
    if (*(long **)(param_1 + 0x30) != (long *)0x0) {
      (**(code **)(**(long **)(param_1 + 0x30) + 8))();
    }
    if (*(long **)(param_1 + 0x38) != (long *)0x0) {
                    /* WARNING: Could not recover jumptable at 0x05ce54b8. Too many branches */
                    /* WARNING: Treating indirect jump as call */
      (**(code **)(**(long **)(param_1 + 0x38) + 8))();
      return;
    }
  }
  return;
}


