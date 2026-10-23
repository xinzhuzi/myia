// Ghidra inferred pseudocode; requested=0x6681860
// entry=06681860 end=066819b7

void FUN_06681860(undefined8 param_1,undefined8 param_2,undefined8 param_3,long *param_4,
                 long *param_5)

{
  long *plVar1;
  long **pplVar2;
  code *pcVar3;
  long alStack_78 [3];
  long *local_60;
  long alStack_58 [3];
  long *local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  pplVar2 = (long **)(param_4 + 3);
  plVar1 = *pplVar2;
  if (plVar1 == (long *)0x0) {
    pplVar2 = &local_40;
LAB_066818b0:
    *pplVar2 = (long *)0x0;
  }
  else {
    local_40 = plVar1;
    if (plVar1 != param_4) goto LAB_066818b0;
    local_40 = alStack_58;
    (**(code **)(*plVar1 + 0x18))(plVar1,alStack_58);
  }
  pplVar2 = (long **)(param_5 + 3);
  plVar1 = *pplVar2;
  if (plVar1 == (long *)0x0) {
    pplVar2 = &local_60;
LAB_066818fc:
    *pplVar2 = (long *)0x0;
  }
  else {
    local_60 = plVar1;
    if (plVar1 != param_5) goto LAB_066818fc;
    local_60 = alStack_78;
    (**(code **)(*plVar1 + 0x18))(plVar1,alStack_78);
  }
  FUN_0667e0e4(param_2,param_3,alStack_58,alStack_78);
  if (local_60 == alStack_78) {
    pcVar3 = *(code **)(*local_60 + 0x20);
LAB_06681958:
    (*pcVar3)();
  }
  else if (local_60 != (long *)0x0) {
    pcVar3 = *(code **)(*local_60 + 0x28);
    goto LAB_06681958;
  }
  if (local_40 == alStack_58) {
    pcVar3 = *(code **)(*local_40 + 0x20);
  }
  else {
    if (local_40 == (long *)0x0) goto LAB_06681988;
    pcVar3 = *(code **)(*local_40 + 0x28);
  }
  (*pcVar3)();
LAB_06681988:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_38) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


