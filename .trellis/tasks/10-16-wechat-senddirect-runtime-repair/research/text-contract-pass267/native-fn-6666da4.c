// Ghidra inferred pseudocode; requested=0x6666da4
// entry=06666da4 end=06666e8f

undefined8 FUN_06666da4(undefined8 param_1,undefined8 param_2,long *param_3)

{
  long *plVar1;
  undefined8 uVar2;
  long **pplVar3;
  code *pcVar4;
  long alStack_58 [3];
  long *local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  pplVar3 = (long **)(param_3 + 3);
  plVar1 = *pplVar3;
  if (plVar1 == (long *)0x0) {
    pplVar3 = &local_40;
LAB_06666df4:
    *pplVar3 = (long *)0x0;
  }
  else {
    local_40 = plVar1;
    if (plVar1 != param_3) goto LAB_06666df4;
    local_40 = alStack_58;
    (**(code **)(*plVar1 + 0x18))(plVar1,alStack_58);
  }
  uVar2 = FUN_06666840(0,param_1,0,param_2,alStack_58);
  if (local_40 == alStack_58) {
    pcVar4 = *(code **)(*local_40 + 0x20);
  }
  else {
    if (local_40 == (long *)0x0) goto LAB_06666e5c;
    pcVar4 = *(code **)(*local_40 + 0x28);
  }
  (*pcVar4)();
LAB_06666e5c:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_38) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return uVar2;
}


