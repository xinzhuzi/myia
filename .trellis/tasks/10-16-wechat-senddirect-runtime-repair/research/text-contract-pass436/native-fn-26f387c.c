// Ghidra inferred pseudocode; requested=0x26f387c
// entry=026f387c end=026f393b

undefined8 * FUN_026f387c(undefined8 *param_1,undefined8 param_2)

{
  undefined8 local_98 [12];
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  *param_1 = &PTR_FUN_09f177b0;
  local_98[0] = 0;
  FUN_0562e128(param_1 + 3,local_98);
  param_1[3] = &PTR_FUN_09da5788;
  FUN_000404d0(param_1 + 6,0);
  param_1[0xb] = 0;
  FUN_056c9134(local_98,param_2);
  FUN_05632750(param_1,local_98);
  FUN_0563255c(local_98);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return param_1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


