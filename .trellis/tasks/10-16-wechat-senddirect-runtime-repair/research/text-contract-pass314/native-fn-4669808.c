// Ghidra inferred pseudocode; requested=0x4669808
// entry=04669808 end=0466989b

void FUN_04669808(undefined8 param_1,undefined8 *param_2)

{
  code *pcVar1;
  undefined **local_48;
  undefined8 uStack_40;
  undefined8 local_38;
  undefined ***local_30;
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_38 = *param_2;
  local_48 = &PTR_FUN_09e92b98;
  uStack_40 = param_1;
  local_30 = &local_48;
  FUN_0176724c(&local_48);
  if (local_30 == &local_48) {
    pcVar1 = (code *)(*local_30)[4];
  }
  else {
    if (local_30 == (undefined ***)0x0) goto LAB_04669870;
    pcVar1 = (code *)(*local_30)[5];
  }
  (*pcVar1)();
LAB_04669870:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


