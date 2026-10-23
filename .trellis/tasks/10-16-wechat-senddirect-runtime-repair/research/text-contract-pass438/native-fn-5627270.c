// Ghidra inferred pseudocode; requested=0x5627270
// entry=05627270 end=056273ab

long FUN_05627270(long param_1,long param_2)

{
  long *plVar1;
  code *pcVar2;
  undefined8 uVar3;
  long local_58;
  undefined8 uStack_50;
  long *local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  FUN_0562e1a0();
  uVar3 = *(undefined8 *)(param_2 + 0x18);
  *(undefined8 *)(param_1 + 0x20) = *(undefined8 *)(param_2 + 0x20);
  *(undefined8 *)(param_1 + 0x18) = uVar3;
  plVar1 = *(long **)(param_2 + 0x40);
  if (plVar1 == (long *)0x0) {
    local_40 = (long *)0x0;
  }
  else if (plVar1 == (long *)(param_2 + 0x28)) {
    local_40 = &local_58;
    (**(code **)(*plVar1 + 0x18))(plVar1,&local_58);
  }
  else {
    local_40 = (long *)(**(code **)(*plVar1 + 0x10))();
  }
  FUN_056278dc(&local_58,param_1 + 0x28);
  if (local_40 == &local_58) {
    pcVar2 = *(code **)(*local_40 + 0x20);
LAB_05627324:
    (*pcVar2)();
  }
  else if (local_40 != (long *)0x0) {
    pcVar2 = *(code **)(*local_40 + 0x28);
    goto LAB_05627324;
  }
  local_58 = 0;
  FUN_0562e288(param_2,&local_58);
  FUN_000404d0(&local_58,0);
  *(undefined8 *)(param_2 + 0x20) = uStack_50;
  *(long *)(param_2 + 0x18) = local_58;
  plVar1 = *(long **)(param_2 + 0x40);
  *(undefined8 *)(param_2 + 0x40) = 0;
  if (plVar1 == (long *)(param_2 + 0x28)) {
    pcVar2 = *(code **)(*plVar1 + 0x20);
  }
  else {
    if (plVar1 == (long *)0x0) goto LAB_05627378;
    pcVar2 = *(code **)(*plVar1 + 0x28);
  }
  (*pcVar2)();
LAB_05627378:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return param_1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


