// Ghidra inferred pseudocode; requested=0x56f8d94
// entry=056f8d94 end=056f8e2b

void FUN_056f8d94(long param_1,undefined8 param_2)

{
  long lVar1;
  undefined1 auStack_78 [80];
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar1 = *(long *)(param_1 + 0xa0);
  if (lVar1 == 0) {
    FUN_0563f1a8(auStack_78,*(undefined8 *)(param_1 + 0x28),param_2,0);
    FUN_05646694(param_1 + 0x50,auStack_78);
    thunk_FUN_05646544(auStack_78);
    if (*(long *)(param_1 + 0x68) == 0) {
      lVar1 = *(long *)(param_1 + 0xa0);
    }
    else {
      lVar1 = FUN_0564668c(param_1 + 0x50);
      *(long *)(param_1 + 0xa0) = lVar1;
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail(lVar1);
}


