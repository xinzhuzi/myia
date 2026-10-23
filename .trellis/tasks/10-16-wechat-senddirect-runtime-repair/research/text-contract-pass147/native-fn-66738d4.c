// Ghidra inferred pseudocode; requested=0x66738d4
// entry=066738d4 end=0667395b

void FUN_066738d4(undefined8 *param_1,undefined8 param_2)

{
  code *pcVar1;
  long alStack_48 [3];
  long *local_30;
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_30 = (long *)0x0;
  FUN_06673990(*param_1,param_2,alStack_48);
  if (local_30 == alStack_48) {
    pcVar1 = *(code **)(*local_30 + 0x20);
  }
  else {
    if (local_30 == (long *)0x0) goto LAB_06673930;
    pcVar1 = *(code **)(*local_30 + 0x28);
  }
  (*pcVar1)();
LAB_06673930:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


