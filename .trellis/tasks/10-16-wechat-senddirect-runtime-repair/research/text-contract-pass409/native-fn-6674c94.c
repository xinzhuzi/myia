// Ghidra inferred pseudocode; requested=0x6674c94
// entry=06674c94 end=06674d27

void FUN_06674c94(undefined4 param_1)

{
  code *pcVar1;
  undefined **local_48;
  undefined4 local_40;
  undefined ***local_30;
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_48 = &PTR_FUN_09fb27f0;
  local_40 = param_1;
  local_30 = &local_48;
  FUN_0666ab58(&local_48);
  if (local_30 == &local_48) {
    pcVar1 = (code *)(*local_30)[4];
  }
  else {
    if (local_30 == (undefined ***)0x0) goto LAB_06674cfc;
    pcVar1 = (code *)(*local_30)[5];
  }
  (*pcVar1)();
LAB_06674cfc:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


