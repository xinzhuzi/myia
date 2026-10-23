// Ghidra inferred pseudocode; requested=0x4100c94
// entry=04100c94 end=04100deb

void FUN_04100c94(undefined8 param_1,long param_2,undefined8 param_3)

{
  long *plVar1;
  code *pcVar2;
  undefined1 auStack_d0 [8];
  undefined8 local_c8;
  undefined7 local_b8;
  char cStack_b1;
  undefined8 local_a8;
  undefined7 local_98;
  char cStack_91;
  undefined8 local_90;
  undefined7 local_80;
  char cStack_79;
  undefined8 local_78;
  undefined7 local_68;
  char cStack_61;
  long local_60;
  long alStack_58 [3];
  long *local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  FUN_041013c4();
  FUN_02fec014(auStack_d0,param_3);
  local_40 = (long *)0x0;
  local_60 = param_2;
  plVar1 = (long *)__Znwm(0x80);
  *plVar1 = (long)&PTR_FUN_09e5b218;
  FUN_02fec014(plVar1 + 1,auStack_d0);
  plVar1[0xf] = local_60;
  local_40 = plVar1;
  FUN_04101574(param_1,alStack_58);
  if (local_40 == alStack_58) {
    pcVar2 = *(code **)(*local_40 + 0x20);
  }
  else {
    if (local_40 == (long *)0x0) goto LAB_04100d40;
    pcVar2 = *(code **)(*local_40 + 0x28);
  }
  (*pcVar2)();
LAB_04100d40:
  if (cStack_61 < '\0') {
    __ZdlPvm(local_78,CONCAT17(cStack_61,local_68) & 0x7fffffffffffffff);
  }
  if (cStack_79 < '\0') {
    __ZdlPvm(local_90,CONCAT17(cStack_79,local_80) & 0x7fffffffffffffff);
  }
  if (cStack_91 < '\0') {
    __ZdlPvm(local_a8,CONCAT17(cStack_91,local_98) & 0x7fffffffffffffff);
  }
  if (cStack_b1 < '\0') {
    __ZdlPvm(local_c8,CONCAT17(cStack_b1,local_b8) & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


