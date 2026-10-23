// Ghidra inferred pseudocode; requested=0x5626fd0
// entry=05626fd0 end=05626fd3

void thunk_FUN_056324e0(undefined8 *param_1)

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
    if (plVar1 == (long *)0x0) goto LAB_05632540;
    pcVar2 = *(code **)(*plVar1 + 0x28);
  }
  (*pcVar2)();
LAB_05632540:
  FUN_0562e140(puVar3);
  FUN_0001accc(param_1);
  return;
}


