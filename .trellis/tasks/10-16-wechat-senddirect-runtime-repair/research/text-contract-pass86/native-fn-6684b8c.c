// Ghidra inferred pseudocode; requested=0x6684b8c
// entry=06684b8c end=06684c7b

void FUN_06684b8c(undefined8 param_1,undefined8 param_2,undefined8 param_3,long *param_4)

{
  code *pcVar1;
  long *plVar2;
  long **pplVar3;
  undefined1 auStack_78 [24];
  undefined8 local_60;
  long alStack_58 [3];
  long *local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  pplVar3 = (long **)(param_4 + 3);
  plVar2 = *pplVar3;
  if (plVar2 == (long *)0x0) {
    pplVar3 = &local_40;
LAB_06684bd4:
    *pplVar3 = (long *)0x0;
  }
  else {
    local_40 = plVar2;
    if (plVar2 != param_4) goto LAB_06684bd4;
    local_40 = alStack_58;
    (**(code **)(*plVar2 + 0x18))(plVar2,alStack_58);
  }
  local_60 = 0;
  FUN_066846b8(param_1,param_2,param_3,alStack_58,auStack_78);
  if (local_40 == alStack_58) {
    pcVar1 = *(code **)(*local_40 + 0x20);
  }
  else {
    if (local_40 == (long *)0x0) goto LAB_06684c4c;
    pcVar1 = *(code **)(*local_40 + 0x28);
  }
  (*pcVar1)();
LAB_06684c4c:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_38) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


