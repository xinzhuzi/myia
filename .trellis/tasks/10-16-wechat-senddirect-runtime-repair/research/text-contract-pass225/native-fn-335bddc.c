// Ghidra inferred pseudocode; requested=0x335bddc
// entry=0335bddc end=0335be6b

void FUN_0335bddc(undefined8 *param_1)

{
  long *plVar1;
  long lVar2;
  undefined1 auStack_2b0 [632];
  long *local_38;
  
  FUN_00f57630(auStack_2b0);
  plVar1 = (long *)__Znwm(0x290);
  *plVar1 = (long)&PTR_FUN_09df3920;
  lVar2 = FUN_02a0cf30(plVar1 + 1,auStack_2b0);
  plVar1[0x50] = (long)&PTR_DAT_09eb0530;
  plVar1[0x51] = lVar2;
  local_38 = plVar1;
  FUN_00ac6290(auStack_2b0);
  FUN_066696dc(*param_1,&local_38);
  if (local_38 != (long *)0x0) {
    (**(code **)(*local_38 + 8))();
  }
  return;
}


