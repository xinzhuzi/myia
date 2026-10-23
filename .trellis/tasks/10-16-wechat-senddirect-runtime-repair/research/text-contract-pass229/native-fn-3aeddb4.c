// Ghidra inferred pseudocode; requested=0x3aeddb4
// entry=03aeddb4 end=03aede8f

void FUN_03aeddb4(long param_1,long *param_2)

{
  long *plVar1;
  code *pcVar2;
  undefined8 uVar3;
  long alStack_48 [3];
  long *local_30;
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_09b36c98;
  plVar1 = (long *)param_2[3];
  if (plVar1 == (long *)0x0) {
    uVar3 = 1;
  }
  else {
    uVar3 = *(undefined8 *)(param_1 + 8);
    if (plVar1 == param_2) {
      local_30 = alStack_48;
      (**(code **)(*plVar1 + 0x18))(plVar1,alStack_48);
    }
    else {
      local_30 = (long *)(**(code **)(*plVar1 + 0x10))();
    }
    uVar3 = FUN_056f412c(uVar3,alStack_48);
    if (local_30 == alStack_48) {
      pcVar2 = *(code **)(*local_30 + 0x20);
    }
    else {
      if (local_30 == (long *)0x0) goto LAB_03aede64;
      pcVar2 = *(code **)(*local_30 + 0x28);
    }
    (*pcVar2)(local_30);
  }
LAB_03aede64:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail(uVar3);
}


