// Ghidra inferred pseudocode; requested=0x3296ddc
// entry=03296ddc end=03296e93

void FUN_03296ddc(undefined8 param_1,long *param_2)

{
  code *pcVar1;
  undefined **local_68 [4];
  long alStack_48 [3];
  long *local_30;
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_09b36c98;
  (**(code **)(*param_2 + 0x18))(local_68);
  FUN_0329728c(param_1,local_68);
  local_68[0] = &PTR_FUN_09da6148;
  FUN_0562e260(local_68);
  if (local_30 == alStack_48) {
    pcVar1 = *(code **)(*local_30 + 0x20);
  }
  else {
    if (local_30 == (long *)0x0) goto LAB_03296e60;
    pcVar1 = *(code **)(*local_30 + 0x28);
  }
  (*pcVar1)();
LAB_03296e60:
  FUN_0562e140(local_68);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


