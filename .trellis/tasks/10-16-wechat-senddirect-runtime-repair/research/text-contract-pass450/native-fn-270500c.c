// Ghidra inferred pseudocode; requested=0x270500c
// entry=0270500c end=027050d3

undefined8 * FUN_0270500c(undefined8 *param_1)

{
  code *pcVar1;
  undefined **local_68 [4];
  long alStack_48 [3];
  long *local_30;
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_09b36c98;
  FUN_02704484(local_68);
  FUN_056f5320(param_1,local_68);
  local_68[0] = &PTR_FUN_09da6148;
  FUN_0562e260(local_68);
  if (local_30 == alStack_48) {
    pcVar1 = *(code **)(*local_30 + 0x20);
  }
  else {
    if (local_30 == (long *)0x0) goto LAB_02705088;
    pcVar1 = *(code **)(*local_30 + 0x28);
  }
  (*pcVar1)();
LAB_02705088:
  FUN_0562e140(local_68);
  *param_1 = &PTR_FUN_09da6390;
  FUN_056d6210(param_1 + 0xb);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_28) {
    return param_1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


