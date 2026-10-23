// Ghidra inferred pseudocode; requested=0x305cff0
// entry=0305cff0 end=0305d12f

void FUN_0305cff0(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 *param_4,
                 undefined8 *param_5)

{
  code *pcVar1;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  ulong local_80;
  undefined8 local_78;
  undefined8 local_70;
  undefined8 uStack_68;
  ulong local_60;
  undefined8 local_58;
  undefined1 uStack_49;
  long alStack_48 [3];
  long *local_30;
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_a0 = param_2;
  uStack_98 = param_3;
  if (*(char *)((long)param_4 + 0x17) < '\0') {
    FUN_00018d20(&local_90,*param_4,param_4[1]);
  }
  else {
    uStack_88 = param_4[1];
    local_90 = *param_4;
    local_80 = param_4[2];
  }
  local_78 = *param_5;
  if (*(char *)((long)param_5 + 0x1f) < '\0') {
    FUN_00018d20(&local_70,param_5[1],param_5[2]);
  }
  else {
    uStack_68 = param_5[2];
    local_70 = param_5[1];
    local_60 = param_5[3];
  }
  local_58 = param_5[4];
  FUN_0305d234(alStack_48,&local_a0,&uStack_49);
  FUN_0666ab58(param_1);
  if (local_30 == alStack_48) {
    pcVar1 = *(code **)(*local_30 + 0x20);
  }
  else {
    if (local_30 == (long *)0x0) goto LAB_0305d0c8;
    pcVar1 = *(code **)(*local_30 + 0x28);
  }
  (*pcVar1)();
LAB_0305d0c8:
  if ((long)local_60 < 0) {
    __ZdlPvm(local_70,local_60 & 0x7fffffffffffffff);
  }
  if ((long)local_80 < 0) {
    __ZdlPvm(local_90,local_80 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


