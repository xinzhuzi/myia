// Ghidra inferred pseudocode; requested=0x329728c
// entry=0329728c end=0329736b

undefined8 * FUN_0329728c(undefined8 *param_1)

{
  code *pcVar1;
  undefined **local_68 [4];
  long alStack_48 [3];
  long *local_30;
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_09b36c98;
  FUN_02704484(local_68);
  FUN_0270500c(param_1,local_68);
  local_68[0] = &PTR_FUN_09da6148;
  FUN_0562e260(local_68);
  if (local_30 == alStack_48) {
    pcVar1 = *(code **)(*local_30 + 0x20);
  }
  else {
    if (local_30 == (long *)0x0) goto LAB_03297308;
    pcVar1 = *(code **)(*local_30 + 0x28);
  }
  (*pcVar1)();
LAB_03297308:
  FUN_0562e140(local_68);
  *param_1 = &PTR_FUN_09df1c00;
  param_1[0x15] = param_1 + 0x14;
  param_1[0x16] = 0;
  param_1[0x13] = &PTR_FUN_09f24930;
  param_1[0x14] = param_1 + 0x14;
  *(undefined1 *)(param_1 + 0x17) = 0;
  param_1[0x18] = 0;
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_28) {
    return param_1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


