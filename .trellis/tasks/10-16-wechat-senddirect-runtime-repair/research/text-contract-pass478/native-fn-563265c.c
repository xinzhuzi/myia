// Ghidra inferred pseudocode; requested=0x563265c
// entry=0563265c end=0563274f

long FUN_0563265c(long param_1,long param_2)

{
  long *plVar1;
  code *pcVar2;
  undefined8 uVar3;
  long alStack_48 [3];
  long *local_30;
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_09b36c98;
  uVar3 = *(undefined8 *)(param_2 + 0x10);
  *(undefined8 *)(param_1 + 8) = *(undefined8 *)(param_2 + 8);
  *(undefined8 *)(param_1 + 0x10) = uVar3;
  FUN_0562e1a0(param_1 + 0x18,param_2 + 0x18);
  uVar3 = *(undefined8 *)(param_2 + 0x30);
  *(undefined8 *)(param_1 + 0x38) = *(undefined8 *)(param_2 + 0x38);
  *(undefined8 *)(param_1 + 0x30) = uVar3;
  plVar1 = *(long **)(param_2 + 0x58);
  if (plVar1 == (long *)0x0) {
    local_30 = (long *)0x0;
  }
  else if (plVar1 == (long *)(param_2 + 0x40)) {
    local_30 = alStack_48;
    (**(code **)(*plVar1 + 0x18))(plVar1,alStack_48);
  }
  else {
    local_30 = (long *)(**(code **)(*plVar1 + 0x10))();
  }
  FUN_056278dc(alStack_48,param_1 + 0x40);
  if (local_30 == alStack_48) {
    pcVar2 = *(code **)(*local_30 + 0x20);
  }
  else {
    if (local_30 == (long *)0x0) goto LAB_05632720;
    pcVar2 = *(code **)(*local_30 + 0x28);
  }
  (*pcVar2)();
LAB_05632720:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_28) {
    return param_1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


