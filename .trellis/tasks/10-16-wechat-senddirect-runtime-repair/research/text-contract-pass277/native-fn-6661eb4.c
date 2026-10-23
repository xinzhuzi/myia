// Ghidra inferred pseudocode; requested=0x6661eb4
// entry=06661eb4 end=06661f1f

void FUN_06661eb4(undefined8 *param_1)

{
  long *plVar1;
  code *pcVar2;
  long *plVar3;
  
  *param_1 = &PTR_FUN_09fb1840;
  plVar3 = (long *)param_1[2];
  if (plVar3 == (long *)0x0) goto LAB_06661f10;
  plVar1 = (long *)plVar3[3];
  if (plVar1 == plVar3) {
    pcVar2 = *(code **)(*plVar1 + 0x20);
LAB_06661efc:
    (*pcVar2)();
  }
  else if (plVar1 != (long *)0x0) {
    pcVar2 = *(code **)(*plVar1 + 0x28);
    goto LAB_06661efc;
  }
  __ZdlPvm(plVar3,0x20);
LAB_06661f10:
  __ZdlPvm(param_1,0x48);
  return;
}


