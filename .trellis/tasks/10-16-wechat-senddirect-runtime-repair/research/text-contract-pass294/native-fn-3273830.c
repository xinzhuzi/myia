// Ghidra inferred pseudocode; requested=0x3273830
// entry=03273830 end=032738ff

undefined8
FUN_03273830(long param_1,long param_2,long param_3,undefined4 param_4,undefined1 param_5)

{
  undefined8 uVar1;
  code *pcVar2;
  undefined1 local_5d;
  undefined4 local_5c;
  long alStack_58 [3];
  long *local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_5d = param_5;
  local_5c = param_4;
  local_40 = (long *)__Znwm(0x30);
  *local_40 = (long)&PTR_FUN_09df2480;
  local_40[1] = param_3;
  local_40[2] = (long)&local_5c;
  local_40[3] = param_1;
  local_40[4] = param_2;
  local_40[5] = (long)&local_5d;
  uVar1 = FUN_03aeddb4(param_1,alStack_58);
  if (local_40 == alStack_58) {
    pcVar2 = *(code **)(*local_40 + 0x20);
  }
  else {
    if (local_40 == (long *)0x0) goto LAB_032738cc;
    pcVar2 = *(code **)(*local_40 + 0x28);
  }
  (*pcVar2)();
LAB_032738cc:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return uVar1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


