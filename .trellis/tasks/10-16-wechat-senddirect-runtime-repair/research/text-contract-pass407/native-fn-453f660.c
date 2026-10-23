// Ghidra inferred pseudocode; requested=0x453f660
// entry=0453f660 end=0453f6af

void FUN_0453f660(long param_1)

{
  long *plVar1;
  code *pcVar2;
  
  plVar1 = *(long **)(param_1 + 0x20);
  if (plVar1 == (long *)(param_1 + 8)) {
    pcVar2 = *(code **)(*plVar1 + 0x20);
  }
  else {
    if (plVar1 == (long *)0x0) goto LAB_0453f69c;
    pcVar2 = *(code **)(*plVar1 + 0x28);
  }
  (*pcVar2)();
LAB_0453f69c:
  __ZdlPvm(param_1,0x28);
  return;
}


