// Ghidra inferred pseudocode; requested=0x453dbd4
// entry=0453dbd4 end=0453dd4b

void FUN_0453dbd4(long param_1,long *param_2)

{
  long *plVar1;
  undefined8 *puVar2;
  long **pplVar3;
  code *pcVar4;
  long alStack_48 [3];
  long *local_30;
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_09b36c98;
  pplVar3 = (long **)(param_2 + 3);
  plVar1 = *pplVar3;
  if (DAT_0a51e9a0 == 0) {
    if (plVar1 == (long *)0x0) {
      *(undefined8 *)(param_1 + 0x18) = 0;
    }
    else if (plVar1 == param_2) {
      *(long *)(param_1 + 0x18) = param_1;
      (**(code **)(*plVar1 + 0x18))(plVar1,param_1);
    }
    else {
      *(long **)(param_1 + 0x18) = plVar1;
      *pplVar3 = (long *)0x0;
    }
    goto LAB_0453dd20;
  }
  if (plVar1 == (long *)0x0) {
    pplVar3 = &local_30;
LAB_0453dc48:
    *pplVar3 = (long *)0x0;
  }
  else {
    local_30 = plVar1;
    if (plVar1 != param_2) goto LAB_0453dc48;
    local_30 = alStack_48;
    (**(code **)(*plVar1 + 0x18))(plVar1,alStack_48);
  }
  *(undefined8 *)(param_1 + 0x18) = 0;
  puVar2 = (undefined8 *)__Znwm(0x28);
  *puVar2 = &PTR_FUN_09e86df8;
  if (local_30 == (long *)0x0) {
    puVar2[4] = 0;
  }
  else if (local_30 == alStack_48) {
    puVar2[4] = puVar2 + 1;
    (**(code **)(*local_30 + 0x18))(local_30);
  }
  else {
    puVar2[4] = local_30;
    local_30 = (long *)0x0;
  }
  *(undefined8 **)(param_1 + 0x18) = puVar2;
  if (local_30 == alStack_48) {
    pcVar4 = *(code **)(*local_30 + 0x20);
  }
  else {
    if (local_30 == (long *)0x0) goto LAB_0453dd20;
    pcVar4 = *(code **)(*local_30 + 0x28);
  }
  (*pcVar4)();
LAB_0453dd20:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_28) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


