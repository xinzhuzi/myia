// Ghidra inferred pseudocode; requested=0x335c1b4
// entry=0335c1b4 end=0335c3b7

/* WARNING: Removing unreachable block (ram,0x0335c2dc) */
/* WARNING: Removing unreachable block (ram,0x0335c2b0) */
/* WARNING: Removing unreachable block (ram,0x0335c31c) */

void FUN_0335c1b4(long param_1)

{
  long *plVar1;
  long lVar2;
  undefined1 uVar3;
  int iVar4;
  undefined4 uVar5;
  undefined8 *puVar6;
  long lVar7;
  undefined8 uVar8;
  undefined8 local_350;
  long *local_348;
  undefined8 local_340;
  long *plStack_338;
  undefined1 auStack_330 [632];
  undefined8 local_b8;
  undefined8 uStack_b0;
  undefined7 local_a8;
  undefined1 uStack_a1;
  undefined1 *local_a0;
  undefined1 *puStack_98;
  undefined1 *puStack_90;
  undefined1 *local_88;
  undefined8 local_80;
  undefined1 *puStack_78;
  undefined1 *local_70;
  undefined1 *local_68;
  undefined1 *local_60;
  undefined1 *puStack_58;
  undefined1 *puStack_50;
  undefined1 *local_48;
  
  FUN_02a0cf30(auStack_330,param_1 + 0x28);
  uVar3 = *(undefined1 *)(param_1 + 0x2b8);
  plStack_338 = *(long **)(param_1 + 0x2c8);
  uVar8 = *(undefined8 *)(param_1 + 0x2c0);
  *(undefined8 *)(param_1 + 0x2c8) = 0;
  *(undefined8 *)(param_1 + 0x2c0) = 0;
  local_350 = *(undefined8 *)(param_1 + 0x2d0);
  local_348 = *(long **)(param_1 + 0x2d8);
  lVar2 = 0;
  if (local_348 != (long *)0x0) {
    lVar2 = local_348[1];
    local_348[1] = lVar2 + 1;
  }
  local_340 = uVar8;
  lVar2 = FUN_0474715c(lVar2);
  uVar3 = FUN_0326a144(uVar8,auStack_330,param_1 + 0x2a0,uVar3);
  iVar4 = FUN_03b032cc(0);
  if (iVar4 != 0) {
    puStack_58 = &SUB_aaaaaaaaaaaaaaaa;
    local_60 = &SUB_aaaaaaaaaaaaaaaa;
    local_48 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_50 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_78 = &SUB_aaaaaaaaaaaaaaaa;
    local_80 = &SUB_aaaaaaaaaaaaaaaa;
    local_68 = &SUB_aaaaaaaaaaaaaaaa;
    local_70 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_98 = &SUB_aaaaaaaaaaaaaaaa;
    local_a0 = &SUB_aaaaaaaaaaaaaaaa;
    local_88 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_90 = &SUB_aaaaaaaaaaaaaaaa;
    uVar5 = FUN_03aedf54(uVar8);
    FUN_03aec858(&local_b8,uVar8);
    local_a0 = (undefined1 *)CONCAT44(local_a0._4_4_,uVar5);
    puVar6 = (undefined8 *)((ulong)&local_a0 | 8);
    puVar6[1] = uStack_b0;
    *puVar6 = local_b8;
    puVar6[2] = CONCAT17(uStack_a1,local_a8);
    puStack_78 = (undefined1 *)0x0;
    puStack_58 = (undefined1 *)0x0;
    puStack_50 = (undefined1 *)0x0;
    local_60 = (undefined1 *)0x0;
    local_48 = (undefined1 *)((ulong)local_48 & 0xffffffffffff0000);
    local_70 = (undefined1 *)0x100000001;
    local_68 = (undefined1 *)CONCAT71((int7)((ulong)local_68 >> 8),uVar3);
    local_80 = (undefined1 *)CONCAT44((int)((ulong)local_80 >> 0x20),1);
    lVar7 = FUN_0474715c();
    puStack_78 = (undefined1 *)(lVar7 - lVar2);
    FUN_03b03320(&local_a0);
  }
  FUN_0335c414(&local_350,auStack_330);
  plVar1 = local_348;
  if (local_348 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_348[1];
    local_348[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_348 + 0x10))(local_348);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = plStack_338;
  if (plStack_338 != (long *)0x0) {
    LOAcquire();
    lVar2 = plStack_338[1];
    plStack_338[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*plStack_338 + 0x10))(plStack_338);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  FUN_00ac6290(auStack_330);
  return;
}


