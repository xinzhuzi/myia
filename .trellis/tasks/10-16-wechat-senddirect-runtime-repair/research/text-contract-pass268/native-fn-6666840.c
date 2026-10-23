// Ghidra inferred pseudocode; requested=0x6666840
// entry=06666840 end=06666c33

long FUN_06666840(undefined8 param_1,undefined8 *param_2,undefined8 param_3,long param_4,
                 undefined1 **param_5)

{
  long lVar1;
  undefined8 *puVar2;
  undefined8 *puVar3;
  undefined1 **ppuVar4;
  long *plVar5;
  undefined8 uVar6;
  undefined1 ***pppuVar7;
  code *pcVar8;
  undefined1 *local_140;
  undefined1 *puStack_138;
  undefined1 *local_130;
  undefined1 *local_120;
  undefined1 *local_118;
  undefined1 *local_110;
  undefined1 *puStack_108;
  undefined1 *puStack_100;
  undefined1 **local_f8;
  undefined1 *local_f0;
  undefined1 *puStack_e8;
  undefined1 *local_e0;
  undefined1 *puStack_d8;
  undefined1 *local_d0;
  undefined1 *apuStack_c0 [3];
  undefined1 **local_a8;
  long local_a0;
  long lStack_98;
  undefined1 *local_90;
  undefined1 *puStack_88;
  undefined1 *local_80;
  long alStack_78 [3];
  long *local_60;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_118 = &SUB_aaaaaaaaaaaaaaaa;
  __ZNSt3__17promiseIvEC1Ev(&local_118);
  local_120 = &SUB_aaaaaaaaaaaaaaaa;
  __ZNSt3__17promiseIvE10get_futureEv(&local_120,&local_118);
  puStack_138 = &SUB_aaaaaaaaaaaaaaaa;
  local_130 = &SUB_aaaaaaaaaaaaaaaa;
  local_140 = &SUB_aaaaaaaaaaaaaaaa;
  if (*(char *)((long)param_2 + 0x17) < '\0') {
    if (param_2[1] == 0) goto LAB_066668e0;
    FUN_00018d20(&local_140,*param_2);
  }
  else if (*(char *)((long)param_2 + 0x17) == '\0') {
LAB_066668e0:
    FUN_06662b28(&local_140);
  }
  else {
    puStack_138 = (undefined1 *)param_2[1];
    local_140 = (undefined1 *)*param_2;
    local_130 = (undefined1 *)param_2[2];
  }
  lVar1 = __Znwm(0x48);
  FUN_06666214(lVar1,param_1,&local_140);
  puVar2 = (undefined8 *)__Znwm(0x48);
  *puVar2 = &PTR_FUN_09fb1840;
  puVar2[1] = 0;
  puVar3 = (undefined8 *)__Znwm(0x20);
  *puVar3 = &PTR_FUN_09fb1b48;
  puVar3[1] = &local_118;
  puVar3[3] = puVar3;
  puVar2[2] = puVar3;
  puVar2[3] = puVar3;
  puVar2[4] = FUN_025bf788;
  puVar2[5] = FUN_025bf3d8;
  puVar2[6] = 0;
  puVar2[7] = FUN_025bf7a0;
  FUN_06661db0(lVar1,0,puVar2,0,0);
  local_d0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_e8 = &SUB_aaaaaaaaaaaaaaaa;
  local_f0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_d8 = &SUB_aaaaaaaaaaaaaaaa;
  local_e0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_108 = &SUB_aaaaaaaaaaaaaaaa;
  local_110 = &SUB_aaaaaaaaaaaaaaaa;
  local_f8 = (undefined1 **)&SUB_aaaaaaaaaaaaaaaa;
  puStack_100 = &SUB_aaaaaaaaaaaaaaaa;
  pppuVar7 = (undefined1 ***)(param_5 + 3);
  ppuVar4 = *pppuVar7;
  if (ppuVar4 == (undefined1 **)0x0) {
    pppuVar7 = &local_f8;
LAB_066669a8:
    *pppuVar7 = (undefined1 **)0x0;
  }
  else {
    local_f8 = ppuVar4;
    if (ppuVar4 != param_5) goto LAB_066669a8;
    local_f8 = &local_110;
    (**(code **)(*ppuVar4 + 0x18))(ppuVar4,&local_110);
  }
  local_f0 = (undefined1 *)lVar1;
  puStack_e8 = (undefined1 *)param_4;
  if ((long)local_130 < 0) {
    FUN_00018d20(&local_e0,local_140,puStack_138);
  }
  else {
    puStack_d8 = puStack_138;
    local_e0 = local_140;
    local_d0 = local_130;
  }
  puVar2 = (undefined8 *)__Znwm(8);
  if (local_f8 == (undefined1 **)0x0) {
    pppuVar7 = &local_a8;
LAB_06666a2c:
    *pppuVar7 = (undefined1 **)0x0;
  }
  else {
    if (local_f8 != &local_110) {
      pppuVar7 = &local_f8;
      local_a8 = local_f8;
      goto LAB_06666a2c;
    }
    local_a8 = apuStack_c0;
    (**(code **)(*local_f8 + 0x18))(local_f8,apuStack_c0);
  }
  lStack_98 = (long)puStack_e8;
  local_a0 = (long)local_f0;
  puStack_88 = puStack_d8;
  local_90 = local_e0;
  local_80 = local_d0;
  local_e0 = (undefined1 *)0x0;
  puStack_d8 = (undefined1 *)0x0;
  local_d0 = (undefined1 *)0x0;
  local_60 = (long *)0x0;
  plVar5 = (long *)__Znwm(0x50);
  *plVar5 = (long)&PTR_FUN_09fb1bc8;
  if (local_a8 == (undefined1 **)0x0) {
    pppuVar7 = (undefined1 ***)(plVar5 + 4);
LAB_06666aa8:
    *pppuVar7 = (undefined1 **)0x0;
  }
  else {
    if (local_a8 != apuStack_c0) {
      pppuVar7 = &local_a8;
      plVar5[4] = (long)local_a8;
      goto LAB_06666aa8;
    }
    plVar5[4] = (long)(plVar5 + 1);
    (**(code **)(*local_a8 + 0x18))(local_a8);
  }
  plVar5[6] = lStack_98;
  plVar5[5] = local_a0;
  plVar5[8] = (long)puStack_88;
  plVar5[7] = (long)local_90;
  plVar5[9] = (long)local_80;
  local_90 = (undefined1 *)0x0;
  puStack_88 = (undefined1 *)0x0;
  local_80 = (undefined1 *)0x0;
  local_60 = plVar5;
  uVar6 = FUN_066887c0(&local_140,alStack_78);
  if (local_60 == alStack_78) {
    pcVar8 = *(code **)(*local_60 + 0x20);
LAB_06666b24:
    (*pcVar8)();
  }
  else if (local_60 != (long *)0x0) {
    pcVar8 = *(code **)(*local_60 + 0x28);
    goto LAB_06666b24;
  }
  if ((long)local_80 < 0) {
    __ZdlPvm(local_90,(ulong)local_80 & 0x7fffffffffffffff);
  }
  if (local_a8 == apuStack_c0) {
    pcVar8 = *(code **)(*local_a8 + 0x20);
LAB_06666b68:
    (*pcVar8)();
  }
  else if (local_a8 != (undefined1 **)0x0) {
    pcVar8 = *(code **)(*local_a8 + 0x28);
    goto LAB_06666b68;
  }
  uVar6 = FUN_06688954(uVar6,param_3,param_4);
  *puVar2 = uVar6;
  *(undefined8 **)(lVar1 + 0x20) = puVar2;
  __ZNSt3__117__assoc_sub_state4waitEv(local_120);
  if ((long)local_d0 < 0) {
    __ZdlPvm(local_e0,(ulong)local_d0 & 0x7fffffffffffffff);
  }
  if (local_f8 == &local_110) {
    pcVar8 = *(code **)(*local_f8 + 0x20);
  }
  else {
    if (local_f8 == (undefined1 **)0x0) goto LAB_06666bd0;
    pcVar8 = *(code **)(*local_f8 + 0x28);
  }
  (*pcVar8)();
LAB_06666bd0:
  if ((long)local_130 < 0) {
    __ZdlPvm(local_140,(ulong)local_130 & 0x7fffffffffffffff);
  }
  __ZNSt3__16futureIvED1Ev(&local_120);
  __ZNSt3__17promiseIvED1Ev(&local_118);
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_58) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return lVar1;
}


