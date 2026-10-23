// Ghidra inferred pseudocode; requested=0x2fc5d68
// entry=02fc5d68 end=02fc6473

void FUN_02fc5d68(long param_1,undefined4 *param_2)

{
  undefined1 uVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  undefined8 *puVar4;
  long lVar5;
  long *plVar6;
  undefined1 *puVar7;
  code *pcVar8;
  ulong uVar9;
  undefined8 uVar10;
  long *plVar11;
  undefined1 *local_470;
  undefined1 *local_468;
  undefined4 local_460 [2];
  undefined1 auStack_458 [160];
  undefined8 local_3b8;
  undefined8 uStack_3b0;
  undefined8 local_3a8;
  undefined8 local_3a0;
  undefined8 uStack_398;
  undefined8 local_390;
  undefined8 local_388;
  undefined8 uStack_380;
  undefined1 auStack_378 [32];
  long local_358;
  long *local_350;
  undefined1 *local_348;
  undefined1 *local_340;
  undefined1 *local_338;
  long *local_330;
  undefined8 local_328;
  undefined8 uStack_320;
  undefined7 local_318;
  char cStack_311;
  undefined8 local_310;
  undefined8 uStack_308;
  ulong local_300;
  undefined8 local_2f8;
  undefined8 uStack_2f0;
  undefined8 local_2e8;
  undefined8 local_2e0;
  undefined8 *local_2d8;
  undefined1 auStack_2d0 [8];
  long local_2c8;
  undefined1 auStack_2c0 [232];
  undefined8 local_1d8;
  undefined1 *local_1d0;
  long *local_1c8;
  undefined1 *local_1c0;
  long *local_1b8;
  undefined8 local_1b0;
  long *local_1a8;
  undefined8 local_1a0 [29];
  undefined1 *local_b8;
  long *local_b0;
  undefined1 *local_a8;
  long *local_a0;
  long alStack_98 [3];
  long *local_80;
  undefined **local_78;
  undefined1 *puStack_70;
  long *local_68;
  undefined ***local_60;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_338 = &SUB_aaaaaaaaaaaaaaaa;
  local_330 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0466aca8(&local_338);
  if (local_338 != (undefined1 *)0x0) {
    local_338[0x39] = 1;
  }
  if ((*(byte *)(param_1 + 0x138) & 1) != 0) goto LAB_02fc6324;
  local_348 = &SUB_aaaaaaaaaaaaaaaa;
  local_340 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_02fc5ae4(&local_348,param_1);
  FUN_04669774();
  FUN_0466ad74(&local_358);
  if ((DAT_0a3d2577 & 1) == 0) {
    DAT_0a3d2568._0_1_ = s_CriticalSeri_0848ba50[0];
    DAT_0a3d2568._1_1_ = s_CriticalSeri_0848ba50[1];
    DAT_0a3d2568._2_1_ = s_CriticalSeri_0848ba50[2];
    DAT_0a3d2568._3_1_ = s_CriticalSeri_0848ba50[3];
    DAT_0a3d2568._4_1_ = s_CriticalSeri_0848ba50[4];
    DAT_0a3d2568._5_1_ = s_CriticalSeri_0848ba50[5];
    DAT_0a3d2568._6_1_ = s_CriticalSeri_0848ba50[6];
    DAT_0a3d2568._7_1_ = s_CriticalSeri_0848ba50[7];
    DAT_0a3d2570 = (undefined4)DAT_086e61d8;
    DAT_0a3d2574 = 0x7475;
    DAT_0a3d2576 = 0;
    DAT_0a3d2577 = 1;
  }
  if ((DAT_0a3d2546 & 1) == 0) {
    uVar9 = 0;
    do {
      uVar2 = *(undefined4 *)((long)&DAT_0889d3e6 + uVar9);
      uVar3 = *(undefined4 *)((long)&DAT_0889d3d2 + uVar9 % 0x14);
      *(uint *)((long)&DAT_0a3d24e5 + uVar9) =
           CONCAT13((char)((uint)uVar2 >> 0x18) + 0x8aU ^ (byte)((uint)uVar3 >> 0x18),
                    CONCAT12((char)((uint)uVar2 >> 0x10) + 0x8aU ^ (byte)((uint)uVar3 >> 0x10),
                             CONCAT11((char)((uint)uVar2 >> 8) + 0x8aU ^ (byte)((uint)uVar3 >> 8),
                                      (char)uVar2 + 0x8aU ^ (byte)uVar3)));
      uVar9 = uVar9 + 4;
    } while (uVar9 != 0x60);
    DAT_0a3d2545 = 0;
    DAT_0a3d2546 = 1;
  }
  FUN_0003bb6c(auStack_378,&DAT_0a3d2568,&DAT_0a3d24e5,0x148);
  local_470 = local_348;
  local_468 = local_340;
  if (local_340 != (undefined1 *)0x0) {
    *(long *)(local_340 + 0x10) = *(long *)(local_340 + 0x10) + 1;
  }
  local_460[0] = *param_2;
  FUN_002c688c(auStack_458,param_2 + 2);
  if (*(char *)((long)param_2 + 0xbf) < '\0') {
    FUN_00018d20(&local_3b8,*(undefined8 *)(param_2 + 0x2a),*(undefined8 *)(param_2 + 0x2c));
  }
  else {
    uStack_3b0 = *(undefined8 *)(param_2 + 0x2c);
    local_3b8 = *(undefined8 *)(param_2 + 0x2a);
    local_3a8 = *(undefined8 *)(param_2 + 0x2e);
  }
  if (*(char *)((long)param_2 + 0xd7) < '\0') {
    FUN_00018d20(&local_3a0,*(undefined8 *)(param_2 + 0x30),*(undefined8 *)(param_2 + 0x32));
  }
  else {
    uStack_398 = *(undefined8 *)(param_2 + 0x32);
    local_3a0 = *(undefined8 *)(param_2 + 0x30);
    local_390 = *(undefined8 *)(param_2 + 0x34);
  }
  uStack_380 = *(undefined8 *)(param_2 + 0x38);
  local_388 = *(undefined8 *)(param_2 + 0x36);
  uVar10 = *(undefined8 *)(local_358 + 8);
  FUN_0453d700(&local_328,auStack_378);
  if (cStack_311 < '\0') {
    FUN_00018d20(&local_310,local_328,uStack_320);
  }
  else {
    uStack_308 = uStack_320;
    local_310 = local_328;
    local_300 = CONCAT17(cStack_311,local_318);
  }
  local_2e8 = 0;
  uStack_2f0 = 0;
  local_2f8 = 0;
  local_2e0 = 0x80000000ffffffff;
  local_2d8 = &local_310;
  FUN_02fec2dc(auStack_2d0,&local_470);
  local_1b8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_1c0 = &SUB_aaaaaaaaaaaaaaaa;
  local_1d8 = uVar10;
  FUN_021efaf0(&local_1c0,&local_1b0);
  local_b0 = local_1b8;
  local_b8 = local_1c0;
  uVar10 = local_1d8;
  puVar4 = local_2d8;
  local_1d0 = local_1c0;
  local_1c8 = local_1b8;
  if (local_1b8 != (long *)0x0) {
    local_1b8[1] = local_1b8[1] + 1;
  }
  local_a8 = &SUB_aaaaaaaaaaaaaaaa;
  local_a0 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_02fec2dc(&local_1b0,auStack_2d0);
  if (local_b0 != (long *)0x0) {
    local_b0[1] = local_b0[1] + 1;
  }
  local_80 = (long *)0x0;
  plVar6 = (long *)__Znwm(0x110);
  *plVar6 = (long)&PTR_FUN_09de0c80;
  FUN_02fec2dc(plVar6 + 1,&local_1b0);
  plVar6[0x20] = (long)local_b8;
  plVar6[0x21] = (long)local_b0;
  if (local_b0 != (long *)0x0) {
    local_b0[1] = local_b0[1] + 1;
  }
  local_80 = plVar6;
  FUN_06684b8c(&local_a8,uVar10,puVar4,alStack_98);
  if (local_80 == alStack_98) {
    pcVar8 = *(code **)(*local_80 + 0x20);
LAB_02fc60b0:
    (*pcVar8)();
  }
  else if (local_80 != (long *)0x0) {
    pcVar8 = *(code **)(*local_80 + 0x28);
    goto LAB_02fc60b0;
  }
  plVar6 = local_b0;
  if (local_b0 != (long *)0x0) {
    LOAcquire();
    lVar5 = local_b0[1];
    local_b0[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*local_b0 + 0x10))(local_b0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  FUN_002c6a5c(local_1a0);
  if (local_1a8 != (long *)0x0) {
    __ZNSt3__119__shared_weak_count14__release_weakEv();
  }
  plVar6 = local_a0;
  if (local_a0 != (long *)0x0) {
    plVar11 = local_a0 + 2;
    *plVar11 = *plVar11 + 1;
    *plVar11 = *plVar11 + 1;
  }
  local_78 = &PTR_FUN_09de0d00;
  puStack_70 = local_a8;
  local_68 = local_a0;
  local_60 = &local_78;
  FUN_06668c44(local_1d0,&local_78);
  if (local_60 == &local_78) {
    pcVar8 = (code *)(*local_60)[4];
LAB_02fc6158:
    (*pcVar8)();
  }
  else if (local_60 != (undefined ***)0x0) {
    pcVar8 = (code *)(*local_60)[5];
    goto LAB_02fc6158;
  }
  if (plVar6 != (long *)0x0) {
    __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
  }
  plVar6 = local_a0;
  if (local_a0 != (long *)0x0) {
    LOAcquire();
    lVar5 = local_a0[1];
    local_a0[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*local_a0 + 0x10))(local_a0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  plVar6 = local_1c8;
  if (local_1c8 != (long *)0x0) {
    LOAcquire();
    lVar5 = local_1c8[1];
    local_1c8[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*local_1c8 + 0x10))(local_1c8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  plVar6 = local_1b8;
  puVar7 = local_1c0;
  if ((local_1b8 != (long *)0x0) && (local_1b8[1] = local_1b8[1] + 1, local_1b8 != (long *)0x0)) {
    LOAcquire();
    lVar5 = local_1b8[1];
    local_1b8[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*local_1b8 + 0x10))(local_1b8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  FUN_002c6a5c(auStack_2c0);
  if (local_2c8 != 0) {
    __ZNSt3__119__shared_weak_count14__release_weakEv();
  }
  if ((long)local_300 < 0) {
    __ZdlPvm(local_310,local_300 & 0x7fffffffffffffff);
  }
  if (cStack_311 < '\0') {
    __ZdlPvm(local_328,CONCAT17(cStack_311,local_318) & 0x7fffffffffffffff);
  }
  if (*(char *)(param_1 + 0x138) == '\x01') {
    if (plVar6 != (long *)0x0) {
      plVar6[1] = plVar6[1] + 1;
    }
    plVar11 = *(long **)(param_1 + 0x130);
    *(undefined1 **)(param_1 + 0x128) = puVar7;
    *(long **)(param_1 + 0x130) = plVar6;
    if (plVar11 != (long *)0x0) {
      LOAcquire();
      lVar5 = plVar11[1];
      plVar11[1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*plVar11 + 0x10))(plVar11);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar11);
      }
    }
  }
  else {
    *(undefined1 **)(param_1 + 0x128) = puVar7;
    *(long **)(param_1 + 0x130) = plVar6;
    if (plVar6 != (long *)0x0) {
      plVar6[1] = plVar6[1] + 1;
    }
    *(undefined1 *)(param_1 + 0x138) = 1;
  }
  if (plVar6 != (long *)0x0) {
    LOAcquire();
    lVar5 = plVar6[1];
    plVar6[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*plVar6 + 0x10))(plVar6);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  FUN_002c6a5c(local_460);
  if (local_468 != (undefined1 *)0x0) {
    __ZNSt3__119__shared_weak_count14__release_weakEv();
  }
  if (local_350 != (long *)0x0) {
    LOAcquire();
    lVar5 = local_350[1];
    local_350[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*local_350 + 0x10))(local_350);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_350);
    }
  }
  if (local_340 != (undefined1 *)0x0) {
    __ZNSt3__119__shared_weak_count14__release_weakEv();
  }
LAB_02fc6324:
  local_1b0 = *(undefined8 *)(param_1 + 0x128);
  local_1a8 = *(long **)(param_1 + 0x130);
  lVar5 = 0;
  if (local_1a8 != (long *)0x0) {
    lVar5 = local_1a8[1];
    local_1a8[1] = lVar5 + 1;
  }
  local_1a0[0] = 0;
  FUN_066856fc(lVar5,&local_1b0);
  puVar7 = (undefined1 *)FUN_022d9f40(&local_1b0);
  plVar6 = local_1a8;
  if (local_1a8 != (long *)0x0) {
    LOAcquire();
    lVar5 = local_1a8[1];
    local_1a8[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*local_1a8 + 0x10))(local_1a8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  uVar1 = *puVar7;
  if (*(char *)(param_1 + 0x138) == '\x01') {
    plVar6 = *(long **)(param_1 + 0x130);
    if (plVar6 != (long *)0x0) {
      LOAcquire();
      lVar5 = plVar6[1];
      plVar6[1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*plVar6 + 0x10))(plVar6);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
      }
    }
    *(undefined1 *)(param_1 + 0x138) = 0;
  }
  plVar6 = local_330;
  if (local_330 != (long *)0x0) {
    LOAcquire();
    lVar5 = local_330[1];
    local_330[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*local_330 + 0x10))(local_330);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail(uVar1);
}


