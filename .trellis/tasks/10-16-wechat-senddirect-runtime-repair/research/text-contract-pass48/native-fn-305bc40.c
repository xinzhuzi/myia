// Ghidra inferred pseudocode; requested=0x305bc40
// entry=0305bc40 end=0305c117

void FUN_0305bc40(long *param_1,undefined8 *param_2,long param_3)

{
  undefined4 uVar1;
  long *plVar2;
  long lVar3;
  int iVar4;
  long *plVar5;
  long *plVar6;
  undefined *puVar7;
  undefined8 *puVar8;
  long *plVar9;
  code *pcVar10;
  undefined8 uVar11;
  long lVar12;
  long lVar13;
  long *local_198;
  long *local_190;
  long *local_188;
  long *local_180;
  undefined1 auStack_178 [96];
  undefined8 local_118;
  undefined8 uStack_110;
  ulong local_108;
  undefined8 local_100;
  undefined8 local_f8;
  undefined8 uStack_f0;
  ulong local_e8;
  undefined8 local_e0;
  long *local_d8;
  long *local_d0;
  long *local_c8;
  long *local_c0;
  long *local_b8;
  long *local_b0;
  undefined **local_a8;
  long *plStack_a0;
  long *local_98;
  undefined ***local_90;
  long alStack_88 [3];
  long *local_70;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  plVar5 = (long *)__Znwm(0x48);
  plVar2 = plVar5 + 1;
  *plVar2 = 0;
  plVar5[2] = 0;
  *plVar5 = (long)&PTR_FUN_09de5720;
  plVar6 = plVar5 + 3;
  FUN_0305c3cc(plVar6,0,0);
  local_b8 = plVar6;
  local_b0 = plVar5;
  local_180 = (long *)__Znwm(0x20);
  plVar9 = local_180 + 1;
  *plVar9 = 0;
  local_180[2] = 0;
  *local_180 = (long)&PTR_FUN_09c20b80;
  local_188 = local_180 + 3;
  *(int *)local_188 = 0;
  local_d8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_d0 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  uVar11 = *param_2;
  if (plVar5 != (long *)0x0) {
    *plVar2 = *plVar2 + 1;
  }
  plVar2 = plVar9;
  if (local_180 != (long *)0x0) {
    plVar2 = (long *)*plVar9;
    *plVar9 = (long)plVar2 + 1;
  }
  local_198 = plVar6;
  local_190 = plVar5;
  local_c8 = local_188;
  local_c0 = local_180;
  FUN_05107c20(plVar2,auStack_178,param_3);
  if (*(char *)(param_3 + 0x77) < '\0') {
    FUN_00018d20(&local_118,*(undefined8 *)(param_3 + 0x60),*(undefined8 *)(param_3 + 0x68));
  }
  else {
    uStack_110 = *(undefined8 *)(param_3 + 0x68);
    local_118 = *(undefined8 *)(param_3 + 0x60);
    local_108 = *(ulong *)(param_3 + 0x70);
  }
  local_100 = *(undefined8 *)(param_3 + 0x78);
  if (*(char *)(param_3 + 0x97) < '\0') {
    FUN_00018d20(&local_f8,*(undefined8 *)(param_3 + 0x80),*(undefined8 *)(param_3 + 0x88));
  }
  else {
    uStack_f0 = *(undefined8 *)(param_3 + 0x88);
    local_f8 = *(undefined8 *)(param_3 + 0x80);
    local_e8 = *(ulong *)(param_3 + 0x90);
  }
  local_e0 = *(undefined8 *)(param_3 + 0x98);
  local_70 = (long *)0x0;
  plVar6 = (long *)__Znwm(200);
  *plVar6 = (long)&PTR_FUN_09de5770;
  FUN_0305cb00(plVar6 + 1,&local_198);
  local_70 = plVar6;
  FUN_06684b8c(&local_d8,uVar11,param_2 + 1,alStack_88);
  if (local_70 == alStack_88) {
    pcVar10 = *(code **)(*local_70 + 0x20);
LAB_0305bdf4:
    (*pcVar10)();
  }
  else if (local_70 != (long *)0x0) {
    pcVar10 = *(code **)(*local_70 + 0x28);
    goto LAB_0305bdf4;
  }
  if ((long)local_e8 < 0) {
    __ZdlPvm(local_f8,local_e8 & 0x7fffffffffffffff);
  }
  if ((long)local_108 < 0) {
    __ZdlPvm(local_118,local_108 & 0x7fffffffffffffff);
  }
  FUN_05107e00(auStack_178);
  plVar6 = local_180;
  if (local_180 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_180[1];
    local_180[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_180 + 0x10))(local_180);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  plVar6 = local_190;
  if (local_190 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_190[1];
    local_190[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_190 + 0x10))(local_190);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  plVar6 = (long *)param_2[4];
  uVar1 = *(undefined4 *)(param_2 + 8);
  if (local_d0 != (long *)0x0) {
    local_d0[1] = local_d0[1] + 1;
  }
  local_a8 = &PTR_FUN_09de5a38;
  plStack_a0 = local_d8;
  local_98 = local_d0;
  local_90 = &local_a8;
  uVar11 = (**(code **)(*plVar6 + 0x18))(plVar6,uVar1,&local_a8);
  if (local_90 == &local_a8) {
    pcVar10 = (code *)(*local_90)[4];
  }
  else {
    if (local_90 == (undefined ***)0x0) goto LAB_0305bf0c;
    pcVar10 = (code *)(*local_90)[5];
  }
  (*pcVar10)();
LAB_0305bf0c:
  (**(code **)(*local_d8 + 0x20))();
  plVar6 = local_b8;
  if ((int)*local_c8 == 0) {
    puVar7 = PTR___ZTIv_09b36ac0;
    if ((long *)param_2[9] != (long *)0x0) {
      puVar7 = (undefined *)(**(code **)(*(long *)param_2[9] + 0x18))();
    }
    iVar4 = _strcmp((char *)(*(ulong *)(puVar7 + 8) & 0x7fffffffffffffff),"_cb1c678e");
    if ((iVar4 != 0) || (lVar3 = param_2[9], lVar3 == -8)) {
      puVar8 = (undefined8 *)___cxa_allocate_exception(8);
      *puVar8 = 0;
      puVar8 = (undefined8 *)__ZNSt8bad_castC2Ev();
      *puVar8 = &PTR___ZNSt8bad_castD2Ev_09fb3078;
                    /* WARNING: Subroutine does not return */
      ___cxa_throw(puVar8,&PTR_DAT_09fb3090,__ZNSt8bad_castD2Ev);
    }
    *param_1 = *(long *)(lVar3 + 8);
    if (*(char *)(lVar3 + 0x27) < '\0') {
      FUN_00018d20(param_1 + 1,*(undefined8 *)(lVar3 + 0x10),*(undefined8 *)(lVar3 + 0x18));
    }
    else {
      lVar13 = *(long *)(lVar3 + 0x18);
      lVar12 = *(long *)(lVar3 + 0x10);
      param_1[3] = *(long *)(lVar3 + 0x20);
      param_1[2] = lVar13;
      param_1[1] = lVar12;
    }
    lVar12 = *(long *)(lVar3 + 0x30);
    param_1[4] = *(long *)(lVar3 + 0x28);
    param_1[5] = lVar12;
  }
  else {
    *param_1 = *local_b8;
    if (*(char *)((long)local_b8 + 0x1f) < '\0') {
      FUN_00018d20(param_1 + 1,local_b8[1],local_b8[2]);
    }
    else {
      lVar12 = local_b8[2];
      lVar3 = local_b8[1];
      param_1[3] = local_b8[3];
      param_1[2] = lVar12;
      param_1[1] = lVar3;
    }
    lVar12 = plVar6[5];
    param_1[4] = plVar6[4];
    param_1[5] = lVar12;
  }
  if (lVar12 != 0) {
    *(long *)(lVar12 + 8) = *(long *)(lVar12 + 8) + 1;
  }
  (**(code **)(*(long *)param_2[4] + 0x20))((long *)param_2[4],uVar11);
  plVar6 = local_d0;
  if (local_d0 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_d0[1];
    local_d0[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_d0 + 0x10))(local_d0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  plVar6 = local_c0;
  if (local_c0 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_c0[1];
    local_c0[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_c0 + 0x10))(local_c0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  plVar6 = local_b0;
  if (local_b0 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_b0[1];
    local_b0[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_b0 + 0x10))(local_b0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_68) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


