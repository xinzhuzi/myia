// Ghidra inferred pseudocode; requested=0x453c20c
// entry=0453c20c end=0453c42b

void FUN_0453c20c(undefined8 param_1,long param_2,long param_3,undefined8 param_4,undefined8 param_5
                 ,undefined8 param_6)

{
  ulong uVar1;
  undefined8 uVar2;
  undefined1 ***pppuVar3;
  code *pcVar4;
  undefined8 local_e8;
  undefined8 uStack_e0;
  undefined7 local_d8;
  char cStack_d1;
  undefined8 local_d0;
  undefined8 uStack_c8;
  ulong local_c0;
  undefined8 local_b8;
  undefined8 uStack_b0;
  undefined8 local_a8;
  undefined8 local_a0;
  undefined1 *apuStack_90 [3];
  undefined1 **local_78;
  undefined1 *local_70;
  undefined1 *puStack_68;
  undefined1 *puStack_60;
  undefined1 **local_58 [2];
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  if ((param_3 == 0) || (uVar1 = FUN_06682d08(param_3 + 8), (uVar1 & 1) != 0)) {
    uVar2 = *(undefined8 *)(param_2 + 8);
    if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
      FUN_0453bd60(param_1,uVar2,param_4,param_6);
      return;
    }
    goto LAB_0453c428;
  }
  puStack_68 = &SUB_aaaaaaaaaaaaaaaa;
  local_70 = &SUB_aaaaaaaaaaaaaaaa;
  local_58[0] = (undefined1 **)&SUB_aaaaaaaaaaaaaaaa;
  puStack_60 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0453dbd4(&local_70,param_5);
  FUN_0453dd8c(&local_e8,param_4,param_6);
  if (cStack_d1 < '\0') {
    FUN_00018d20(&local_d0,local_e8,uStack_e0);
  }
  else {
    uStack_c8 = uStack_e0;
    local_d0 = local_e8;
    local_c0 = CONCAT17(cStack_d1,local_d8);
  }
  local_a8 = 0;
  uStack_b0 = 0;
  local_b8 = 0;
  local_a0 = 0x80000000ffffffff;
  if (local_58[0] == (undefined1 **)0x0) {
    pppuVar3 = &local_78;
LAB_0453c330:
    *pppuVar3 = (undefined1 **)0x0;
  }
  else {
    if (local_58[0] != &local_70) {
      pppuVar3 = local_58;
      local_78 = local_58[0];
      goto LAB_0453c330;
    }
    local_78 = apuStack_90;
    (**(code **)(*local_58[0] + 0x18))(local_58[0],apuStack_90);
  }
  FUN_06684b8c(param_1,param_3,&local_d0,apuStack_90);
  if (local_78 == apuStack_90) {
    pcVar4 = *(code **)(*local_78 + 0x20);
LAB_0453c38c:
    (*pcVar4)();
  }
  else if (local_78 != (undefined1 **)0x0) {
    pcVar4 = *(code **)(*local_78 + 0x28);
    goto LAB_0453c38c;
  }
  if ((long)local_c0 < 0) {
    __ZdlPvm(local_d0,local_c0 & 0x7fffffffffffffff);
  }
  if (cStack_d1 < '\0') {
    __ZdlPvm(local_e8,CONCAT17(cStack_d1,local_d8) & 0x7fffffffffffffff);
  }
  if (local_58[0] == &local_70) {
    pcVar4 = *(code **)(*local_58[0] + 0x20);
LAB_0453c3f4:
    uVar2 = (*pcVar4)();
  }
  else {
    uVar2 = 0;
    if (local_58[0] != (undefined1 **)0x0) {
      pcVar4 = *(code **)(*local_58[0] + 0x28);
      goto LAB_0453c3f4;
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
LAB_0453c428:
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail(uVar2);
}


