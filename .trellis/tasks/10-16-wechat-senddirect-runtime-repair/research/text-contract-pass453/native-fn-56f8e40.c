// Ghidra inferred pseudocode; requested=0x56f8e40
// entry=056f8e40 end=056f8ee7

void FUN_056f8e40(long param_1)

{
  long lVar1;
  undefined8 uVar2;
  undefined1 auStack_78 [80];
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar1 = *(long *)(param_1 + 0xa0);
  if (lVar1 == 0) {
    FUN_0563f1a8(auStack_78,*(undefined8 *)(param_1 + 0x28),0,0);
    FUN_05646694(param_1 + 0x50,auStack_78);
    thunk_FUN_05646544(auStack_78);
    if (*(long *)(param_1 + 0x68) == 0) {
      lVar1 = *(long *)(param_1 + 0xa0);
      if (lVar1 == 0) {
        uVar2 = 0;
        goto LAB_056f8eb0;
      }
    }
    else {
      lVar1 = FUN_0564668c(param_1 + 0x50);
      *(long *)(param_1 + 0xa0) = lVar1;
      uVar2 = 0;
      if (lVar1 == 0) goto LAB_056f8eb0;
    }
  }
  uVar2 = *(undefined8 *)(lVar1 + 0x260);
LAB_056f8eb0:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail(uVar2);
}


