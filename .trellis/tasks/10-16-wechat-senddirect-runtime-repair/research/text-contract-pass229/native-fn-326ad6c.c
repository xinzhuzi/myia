// Ghidra inferred pseudocode; requested=0x326ad6c
// entry=0326ad6c end=0326af27

/* WARNING: Removing unreachable block (ram,0x0326ae84) */
/* WARNING: Removing unreachable block (ram,0x0326aeb4) */

undefined8 FUN_0326ad6c(long param_1,undefined8 *param_2)

{
  int iVar1;
  code *pcVar2;
  undefined8 uVar3;
  undefined1 *local_78;
  undefined1 *local_70;
  undefined1 *local_68;
  long local_60;
  long local_58;
  long local_50;
  long *local_48;
  undefined8 local_40;
  undefined8 uStack_38;
  undefined8 local_30;
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_70 = &SUB_aaaaaaaaaaaaaaaa;
  local_68 = &SUB_aaaaaaaaaaaaaaaa;
  local_78 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_030251cc(&local_78,param_2);
  iVar1 = FUN_03aed984(param_1,&local_78);
  if (iVar1 == 0) {
    local_48 = (long *)__Znwm(0x20);
    *local_48 = (long)&PTR_FUN_09df2d80;
    local_48[1] = param_1;
    local_48[2] = (long)&local_78;
    local_48[3] = (long)param_2;
    uVar3 = FUN_03aeddb4(param_1,&local_60);
    if (local_48 == &local_60) {
      pcVar2 = *(code **)(*local_48 + 0x20);
    }
    else {
      if (local_48 == (long *)0x0) goto joined_r0x0326af0c;
      pcVar2 = *(code **)(*local_48 + 0x28);
    }
    (*pcVar2)();
  }
  else {
    if (*(char *)((long)param_2 + 0x17) < '\0') {
      FUN_00018d20(&local_40,*param_2,param_2[1]);
    }
    else {
      uStack_38 = param_2[1];
      local_40 = *param_2;
      local_30 = param_2[2];
    }
    FUN_0029ae04(&local_60,&local_40,1);
    FUN_0327fdd8(param_1,1,&local_60);
    if (local_60 != 0) {
      for (; local_58 != local_60; local_58 = local_58 + -0x18) {
      }
      local_58 = local_60;
      __ZdlPvm(local_60,local_50 - local_60);
    }
    uVar3 = 1;
  }
joined_r0x0326af0c:
  if ((long)local_68 < 0) {
    __ZdlPvm(local_78,(ulong)local_68 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_28) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return uVar3;
}


