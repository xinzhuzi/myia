// Ghidra inferred pseudocode; requested=0x4cbf820
// entry=04cbf820 end=04cbf873

void FUN_04cbf820(long param_1)

{
  long *plVar1;
  
  *(undefined8 *)(param_1 + 0x108) = *(undefined8 *)(param_1 + 0xc);
  if (*(char *)(param_1 + 0x240) == '\x01') {
    FUN_04cbebac();
    plVar1 = *(long **)(param_1 + 0x220);
    if (plVar1 != (long *)0x0) {
      (**(code **)(*plVar1 + 0x10))(plVar1,param_1);
    }
    FUN_04cbf994(param_1);
    return;
  }
  return;
}


