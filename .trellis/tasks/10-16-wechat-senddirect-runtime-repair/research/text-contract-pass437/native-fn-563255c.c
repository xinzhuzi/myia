// Ghidra inferred pseudocode; requested=0x563255c
// entry=0563255c end=056325d3

void FUN_0563255c(undefined8 *param_1)

{
  long *plVar1;
  code *pcVar2;
  undefined8 *puVar3;
  
  *param_1 = &PTR_FUN_09f177b0;
  puVar3 = param_1 + 3;
  *puVar3 = &PTR_FUN_09da5788;
  FUN_0562e260(puVar3);
  plVar1 = (long *)param_1[0xb];
  if (plVar1 == param_1 + 8) {
    pcVar2 = *(code **)(*plVar1 + 0x20);
  }
  else {
    if (plVar1 == (long *)0x0) goto LAB_056325bc;
    pcVar2 = *(code **)(*plVar1 + 0x28);
  }
  (*pcVar2)();
LAB_056325bc:
  FUN_0562e140(puVar3);
  FUN_0001accc(param_1);
  return;
}


