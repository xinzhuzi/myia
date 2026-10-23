// Ghidra inferred pseudocode; requested=0x453c7ac
// entry=0453c7ac end=0453cbeb

void FUN_0453c7ac(undefined8 param_1,long param_2,long param_3,undefined8 param_4,undefined8 param_5
                 ,undefined8 param_6,undefined8 param_7)

{
  ulong uVar1;
  undefined8 uVar2;
  long *plVar3;
  undefined1 ***pppuVar4;
  code *pcVar5;
  undefined1 *local_170;
  undefined1 *puStack_168;
  undefined1 *local_160;
  undefined1 *puStack_158;
  undefined1 *local_150;
  undefined1 *puStack_148;
  undefined1 *local_140;
  undefined1 *local_138;
  undefined1 *puStack_130;
  undefined1 *local_128;
  undefined1 *local_120;
  undefined1 *puStack_118;
  undefined1 *local_110;
  undefined1 *apuStack_108 [3];
  undefined1 **local_f0;
  undefined1 *apuStack_e8 [3];
  undefined1 **local_d0 [2];
  long alStack_c0 [3];
  long *local_a8;
  undefined1 *local_a0;
  undefined1 *puStack_98;
  undefined1 *puStack_90;
  undefined1 **local_88;
  undefined1 *local_80;
  undefined1 *puStack_78;
  undefined1 *puStack_70;
  undefined1 **local_68 [2];
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  if ((param_3 == 0) || (uVar1 = FUN_06682d08(param_3 + 8), (uVar1 & 1) != 0)) {
    uVar2 = *(undefined8 *)(param_2 + 8);
    if (*(long *)PTR____stack_chk_guard_09b36c98 == local_58) {
      FUN_0453bd60(param_1,uVar2,param_4,param_7);
      return;
    }
    goto LAB_0453cbe8;
  }
  puStack_78 = &SUB_aaaaaaaaaaaaaaaa;
  local_80 = &SUB_aaaaaaaaaaaaaaaa;
  local_68[0] = (undefined1 **)&SUB_aaaaaaaaaaaaaaaa;
  puStack_70 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0453dbd4(&local_80,param_5);
  puStack_98 = &SUB_aaaaaaaaaaaaaaaa;
  local_a0 = &SUB_aaaaaaaaaaaaaaaa;
  local_88 = (undefined1 **)&SUB_aaaaaaaaaaaaaaaa;
  puStack_90 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0453dbd4(&local_a0,param_6);
  puStack_130 = &SUB_aaaaaaaaaaaaaaaa;
  local_128 = &SUB_aaaaaaaaaaaaaaaa;
  local_138 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0453dd8c(&local_138,param_4,param_7);
  local_140 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_158 = &SUB_aaaaaaaaaaaaaaaa;
  local_160 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_148 = &SUB_aaaaaaaaaaaaaaaa;
  local_150 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_168 = &SUB_aaaaaaaaaaaaaaaa;
  local_170 = &SUB_aaaaaaaaaaaaaaaa;
  if ((long)local_128 < 0) {
    FUN_00018d20(&local_170,local_138,puStack_130);
    puStack_158 = (undefined1 *)0x0;
    puStack_148 = (undefined1 *)0x0;
    local_150 = (undefined1 *)0x0;
    local_140 = (undefined1 *)0x80000000ffffffff;
    if (-1 < (long)local_128) goto LAB_0453c908;
    FUN_00018d20(&local_120,local_138,puStack_130);
  }
  else {
    puStack_168 = puStack_130;
    local_170 = local_138;
    local_160 = local_128;
LAB_0453c908:
    local_140 = (undefined1 *)0x80000000ffffffff;
    puStack_148 = (undefined1 *)0x0;
    local_150 = (undefined1 *)0x0;
    puStack_158 = (undefined1 *)0x0;
    puStack_118 = puStack_130;
    local_120 = local_138;
    local_110 = local_128;
  }
  if (local_68[0] == (undefined1 **)0x0) {
    pppuVar4 = &local_f0;
LAB_0453c944:
    *pppuVar4 = (undefined1 **)0x0;
  }
  else {
    if (local_68[0] != &local_80) {
      pppuVar4 = local_68;
      local_f0 = local_68[0];
      goto LAB_0453c944;
    }
    local_f0 = apuStack_108;
    (**(code **)(*local_68[0] + 0x18))(local_68[0],apuStack_108);
  }
  if (local_88 == (undefined1 **)0x0) {
    pppuVar4 = local_d0;
LAB_0453c98c:
    *pppuVar4 = (undefined1 **)0x0;
  }
  else {
    if (local_88 != &local_a0) {
      pppuVar4 = &local_88;
      local_d0[0] = local_88;
      goto LAB_0453c98c;
    }
    local_d0[0] = apuStack_e8;
    (**(code **)(*local_88 + 0x18))(local_88,apuStack_e8);
  }
  local_a8 = (long *)0x0;
  plVar3 = (long *)__Znwm(0x60);
  *plVar3 = (long)&PTR_FUN_09e86fa8;
  plVar3[2] = (long)puStack_118;
  plVar3[1] = (long)local_120;
  plVar3[3] = (long)local_110;
  local_120 = (undefined1 *)0x0;
  puStack_118 = (undefined1 *)0x0;
  local_110 = (undefined1 *)0x0;
  if (local_f0 == (undefined1 **)0x0) {
    pppuVar4 = (undefined1 ***)(plVar3 + 7);
LAB_0453ca00:
    *pppuVar4 = (undefined1 **)0x0;
  }
  else {
    if (local_f0 != apuStack_108) {
      pppuVar4 = &local_f0;
      plVar3[7] = (long)local_f0;
      goto LAB_0453ca00;
    }
    plVar3[7] = (long)(plVar3 + 4);
    (**(code **)(*local_f0 + 0x18))();
  }
  if (local_d0[0] == (undefined1 **)0x0) {
    pppuVar4 = (undefined1 ***)(plVar3 + 0xb);
LAB_0453ca40:
    *pppuVar4 = (undefined1 **)0x0;
  }
  else {
    if (local_d0[0] != apuStack_e8) {
      pppuVar4 = local_d0;
      plVar3[0xb] = (long)local_d0[0];
      goto LAB_0453ca40;
    }
    plVar3[0xb] = (long)(plVar3 + 8);
    (**(code **)(*local_d0[0] + 0x18))();
  }
  local_a8 = plVar3;
  FUN_06684b8c(param_1,param_3,&local_170,alStack_c0);
  if (local_a8 == alStack_c0) {
    pcVar5 = *(code **)(*local_a8 + 0x20);
LAB_0453ca9c:
    (*pcVar5)();
  }
  else if (local_a8 != (long *)0x0) {
    pcVar5 = *(code **)(*local_a8 + 0x28);
    goto LAB_0453ca9c;
  }
  if (local_d0[0] == apuStack_e8) {
    pcVar5 = *(code **)(*local_d0[0] + 0x20);
LAB_0453cac4:
    (*pcVar5)();
  }
  else if (local_d0[0] != (undefined1 **)0x0) {
    pcVar5 = *(code **)(*local_d0[0] + 0x28);
    goto LAB_0453cac4;
  }
  if (local_f0 == apuStack_108) {
    pcVar5 = *(code **)(*local_f0 + 0x20);
LAB_0453caec:
    (*pcVar5)();
  }
  else if (local_f0 != (undefined1 **)0x0) {
    pcVar5 = *(code **)(*local_f0 + 0x28);
    goto LAB_0453caec;
  }
  if ((long)local_110 < 0) {
    __ZdlPvm(local_120,(ulong)local_110 & 0x7fffffffffffffff);
  }
  if ((long)local_160 < 0) {
    __ZdlPvm(local_170,(ulong)local_160 & 0x7fffffffffffffff);
  }
  if ((long)local_128 < 0) {
    __ZdlPvm(local_138,(ulong)local_128 & 0x7fffffffffffffff);
  }
  if (local_88 == &local_a0) {
    pcVar5 = *(code **)(*local_88 + 0x20);
LAB_0453cb74:
    (*pcVar5)();
  }
  else if (local_88 != (undefined1 **)0x0) {
    pcVar5 = *(code **)(*local_88 + 0x28);
    goto LAB_0453cb74;
  }
  if (local_68[0] == &local_80) {
    pcVar5 = *(code **)(*local_68[0] + 0x20);
LAB_0453cba0:
    uVar2 = (*pcVar5)();
  }
  else {
    uVar2 = 0;
    if (local_68[0] != (undefined1 **)0x0) {
      pcVar5 = *(code **)(*local_68[0] + 0x28);
      goto LAB_0453cba0;
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_58) {
    return;
  }
LAB_0453cbe8:
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail(uVar2);
}


