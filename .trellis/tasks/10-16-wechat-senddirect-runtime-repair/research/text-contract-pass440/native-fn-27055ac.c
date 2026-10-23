// Ghidra inferred pseudocode; requested=0x27055ac
// entry=027055ac end=027056cb

long FUN_027055ac(long param_1,long param_2)

{
  long *plVar1;
  code *pcVar2;
  long alStack_58 [3];
  long *local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  FUN_056c2124();
  FUN_0562fddc(param_1 + 0x38,param_2 + 0x38);
  FUN_0562fddc(param_1 + 0x50,param_2 + 0x50);
  *(undefined1 *)(param_1 + 0x68) = *(undefined1 *)(param_2 + 0x68);
  FUN_0562fddc(param_1 + 0x70,param_2 + 0x70);
  plVar1 = *(long **)(param_2 + 0xa0);
  if (plVar1 == (long *)0x0) {
    local_40 = (long *)0x0;
  }
  else if (plVar1 == (long *)(param_2 + 0x88)) {
    local_40 = alStack_58;
    (**(code **)(*plVar1 + 0x18))(plVar1,alStack_58);
  }
  else {
    local_40 = (long *)(**(code **)(*plVar1 + 0x10))();
  }
  FUN_027056cc(alStack_58,param_1 + 0x88);
  if (local_40 == alStack_58) {
    pcVar2 = *(code **)(*local_40 + 0x20);
  }
  else {
    if (local_40 == (long *)0x0) goto LAB_02705688;
    pcVar2 = *(code **)(*local_40 + 0x28);
  }
  (*pcVar2)();
LAB_02705688:
  *(undefined8 *)(param_1 + 0xa8) = *(undefined8 *)(param_2 + 0xa8);
  *(long *)(param_1 + 8) = param_1 + 0x28;
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return param_1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


