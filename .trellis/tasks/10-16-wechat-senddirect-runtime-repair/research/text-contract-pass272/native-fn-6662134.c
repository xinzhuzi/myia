// Ghidra inferred pseudocode; requested=0x6662134
// entry=06662134 end=06662183

void FUN_06662134(long param_1)

{
  long *plVar1;
  code *pcVar2;
  
  plVar1 = *(long **)(param_1 + 0x20);
  if (plVar1 == (long *)(param_1 + 8)) {
    pcVar2 = *(code **)(*plVar1 + 0x20);
  }
  else {
    if (plVar1 == (long *)0x0) goto LAB_06662170;
    pcVar2 = *(code **)(*plVar1 + 0x28);
  }
  (*pcVar2)();
LAB_06662170:
  __ZdlPvm(param_1,0x28);
  return;
}


