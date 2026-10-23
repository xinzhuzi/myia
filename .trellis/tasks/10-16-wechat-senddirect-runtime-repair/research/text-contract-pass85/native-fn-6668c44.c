// Ghidra inferred pseudocode; requested=0x6668c44
// entry=06668c44 end=06668e2b

void FUN_06668c44(long param_1,long *param_2)

{
  long *plVar1;
  long **pplVar2;
  code *pcVar3;
  long alStack_88 [3];
  long *local_70;
  long alStack_68 [3];
  long *local_50;
  long alStack_48 [3];
  long *local_30;
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_09b36c98;
  __ZNSt3__115recursive_mutex4lockEv(param_1 + 0x10);
  pplVar2 = (long **)(param_2 + 3);
  plVar1 = *pplVar2;
  if (plVar1 == (long *)0x0) {
    pplVar2 = &local_70;
LAB_06668c98:
    *pplVar2 = (long *)0x0;
  }
  else {
    local_70 = plVar1;
    if (plVar1 != param_2) goto LAB_06668c98;
    local_70 = alStack_88;
    (**(code **)(*plVar1 + 0x18))(plVar1,alStack_88);
  }
  if (local_70 == (long *)0x0) {
    pplVar2 = &local_50;
LAB_06668ce0:
    *pplVar2 = (long *)0x0;
  }
  else {
    if (local_70 != alStack_88) {
      pplVar2 = &local_70;
      local_50 = local_70;
      goto LAB_06668ce0;
    }
    local_50 = alStack_68;
    (**(code **)(*local_70 + 0x18))(local_70,alStack_68);
  }
  local_30 = (long *)0x0;
  plVar1 = (long *)__Znwm(0x28);
  *plVar1 = (long)&PTR_FUN_09fb1cb0;
  if (local_50 == (long *)0x0) {
    pplVar2 = (long **)(plVar1 + 4);
LAB_06668d40:
    *pplVar2 = (long *)0x0;
  }
  else {
    if (local_50 != alStack_68) {
      pplVar2 = &local_50;
      plVar1[4] = (long)local_50;
      goto LAB_06668d40;
    }
    plVar1[4] = (long)(plVar1 + 1);
    (**(code **)(*local_50 + 0x18))(local_50);
  }
  local_30 = plVar1;
  FUN_0086463c(alStack_48,param_1 + 0xa8);
  if (local_30 == alStack_48) {
    pcVar3 = *(code **)(*local_30 + 0x20);
LAB_06668d9c:
    (*pcVar3)();
  }
  else if (local_30 != (long *)0x0) {
    pcVar3 = *(code **)(*local_30 + 0x28);
    goto LAB_06668d9c;
  }
  if (local_50 == alStack_68) {
    pcVar3 = *(code **)(*local_50 + 0x20);
LAB_06668dc8:
    (*pcVar3)();
  }
  else if (local_50 != (long *)0x0) {
    pcVar3 = *(code **)(*local_50 + 0x28);
    goto LAB_06668dc8;
  }
  if (local_70 == alStack_88) {
    pcVar3 = *(code **)(*local_70 + 0x20);
  }
  else {
    if (local_70 == (long *)0x0) goto LAB_06668df8;
    pcVar3 = *(code **)(*local_70 + 0x28);
  }
  (*pcVar3)();
LAB_06668df8:
  __ZNSt3__115recursive_mutex6unlockEv(param_1 + 0x10);
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_28) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


