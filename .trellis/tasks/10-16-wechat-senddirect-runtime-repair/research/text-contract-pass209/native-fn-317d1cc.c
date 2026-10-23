// Ghidra inferred pseudocode; requested=0x317d1cc
// entry=0317d1cc end=0317d417

void FUN_0317d1cc(long param_1)

{
  undefined8 *puVar1;
  long lVar2;
  undefined8 *puVar3;
  undefined8 local_318;
  long *local_310;
  undefined8 local_308;
  long *local_300;
  undefined8 local_2f8;
  long *local_2f0;
  undefined8 *local_2e8;
  undefined8 *local_2e0;
  undefined8 *local_2d8;
  undefined8 **ppuStack_2d0;
  undefined1 *local_2c8;
  undefined1 auStack_2c0 [632];
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  FUN_00f57630(auStack_2c0);
  local_2e8 = (undefined8 *)0x0;
  local_2e0 = (undefined8 *)0x0;
  ppuStack_2d0 = &local_2e8;
  local_2c8 = &DAT_aaaaaaaaaaaaaa00;
  local_2d8 = (undefined8 *)0x0;
  local_2e8 = (undefined8 *)__Znwm(0x278);
  puVar3 = local_2e8 + 0x4f;
  local_2e0 = local_2e8;
  local_2d8 = puVar3;
  FUN_00f57630(local_2e8,auStack_2c0);
  local_2e0 = puVar3;
  FUN_0319eef8(param_1 + 0xc0,&local_2e8);
  puVar1 = local_2e8;
  puVar3 = local_2e0;
  if (local_2e8 != (undefined8 *)0x0) {
    while (puVar3 != puVar1) {
      puVar3 = puVar3 + -0x4f;
      (**(code **)*puVar3)(puVar3);
    }
    local_2e0 = puVar1;
    __ZdlPvm(local_2e8,(long)local_2d8 - (long)local_2e8);
  }
  FUN_0466aca8(&local_318);
  FUN_01205740(&local_308,local_318);
  FUN_02891054(&local_2f8,local_308);
  local_2e8 = (undefined8 *)0x0;
  local_2e0 = (undefined8 *)0x0;
  ppuStack_2d0 = &local_2e8;
  local_2c8 = &DAT_aaaaaaaaaaaaaa00;
  local_2d8 = (undefined8 *)0x0;
  local_2e8 = (undefined8 *)__Znwm(0x278);
  puVar3 = local_2e8 + 0x4f;
  local_2e0 = local_2e8;
  local_2d8 = puVar3;
  FUN_00f57630(local_2e8,auStack_2c0);
  local_2e0 = puVar3;
  FUN_03960e34(local_2f8,&local_2e8);
  puVar1 = local_2e8;
  puVar3 = local_2e0;
  if (local_2e8 != (undefined8 *)0x0) {
    while (puVar3 != puVar1) {
      puVar3 = puVar3 + -0x4f;
      (**(code **)*puVar3)(puVar3);
    }
    local_2e0 = puVar1;
    __ZdlPvm(local_2e8,(long)local_2d8 - (long)local_2e8);
  }
  if (local_2f0 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_2f0[1];
    local_2f0[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_2f0 + 0x10))(local_2f0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_2f0);
    }
  }
  if (local_300 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_300[1];
    local_300[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_300 + 0x10))(local_300);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_300);
    }
  }
  if (local_310 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_310[1];
    local_310[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_310 + 0x10))(local_310);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_310);
    }
  }
  FUN_00ac6290(auStack_2c0);
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


