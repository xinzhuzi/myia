// Ghidra inferred pseudocode; requested=0x318edb0
// entry=0318edb0 end=0318f247

/* WARNING: Removing unreachable block (ram,0x0318f204) */
/* WARNING: Removing unreachable block (ram,0x0318f1ec) */
/* WARNING: Removing unreachable block (ram,0x0318f224) */

void FUN_0318edb0(undefined8 param_1,long *param_2)

{
  long *plVar1;
  long *plVar2;
  byte bVar3;
  long lVar4;
  undefined8 uVar5;
  undefined1 *local_880;
  undefined1 *puStack_878;
  undefined1 *local_870;
  undefined1 *puStack_868;
  undefined1 *local_860;
  long *local_858;
  undefined1 *local_850;
  long *local_848;
  undefined1 auStack_840 [632];
  char local_5c8;
  undefined1 *local_5c0;
  undefined1 *puStack_5b8;
  undefined1 *local_5b0;
  undefined8 local_5a8;
  undefined1 *local_5a0;
  undefined1 *puStack_598;
  undefined1 *puStack_590;
  undefined1 *local_588;
  undefined1 *local_580;
  undefined4 local_4a8;
  undefined1 *local_340;
  long *local_338;
  byte local_c8;
  undefined1 *local_c0;
  undefined1 *puStack_b8;
  undefined1 *local_b0;
  undefined8 local_a8;
  undefined1 *local_a0;
  undefined1 *puStack_98;
  undefined1 *puStack_90;
  undefined1 *local_88;
  undefined1 *local_80;
  undefined1 *local_70;
  long *local_68;
  undefined1 *local_60;
  undefined1 *puStack_58;
  undefined1 *local_50;
  undefined1 *puStack_48;
  undefined1 *local_40;
  long *local_38;
  
  puStack_48 = &SUB_aaaaaaaaaaaaaaaa;
  local_50 = &SUB_aaaaaaaaaaaaaaaa;
  local_38 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_40 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_58 = &SUB_aaaaaaaaaaaaaaaa;
  local_60 = &SUB_aaaaaaaaaaaaaaaa;
  local_340 = (undefined1 *)*param_2;
  plVar2 = (long *)param_2[1];
  if (plVar2 == (long *)0x0) {
    local_338 = (long *)0x0;
  }
  else {
    plVar1 = plVar2 + 1;
    *plVar1 = *plVar1 + 1;
    *plVar1 = *plVar1 + 1;
    local_338 = plVar2;
  }
  local_70 = local_340;
  local_68 = plVar2;
  FUN_0317df64(&local_60,param_1,&local_340,0);
  if (plVar2 != (long *)0x0) {
    LOAcquire();
    lVar4 = plVar2[1];
    plVar2[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*plVar2 + 0x10))(plVar2);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  plVar2 = local_68;
  if (local_68 != (long *)0x0) {
    LOAcquire();
    lVar4 = local_68[1];
    local_68[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*local_68 + 0x10))(local_68);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  local_80 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_98 = &SUB_aaaaaaaaaaaaaaaa;
  local_a0 = &SUB_aaaaaaaaaaaaaaaa;
  local_88 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_90 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_b8 = &SUB_aaaaaaaaaaaaaaaa;
  local_c0 = &SUB_aaaaaaaaaaaaaaaa;
  local_a8 = &SUB_aaaaaaaaaaaaaaaa;
  local_b0 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0086e43c(&local_c0,local_40);
  if ((char)local_80 == '\x01') {
    _memcpy(&local_340,&DAT_088bcb40,0x280);
    FUN_03190538(&local_340,param_1,&local_c0,local_a8._4_4_,(ulong)local_a8 & 0xffffffff);
    bVar3 = local_c8;
    if (local_c8 == 1) {
      _memcpy(&local_5c0,&DAT_088bc4c0,0x278);
      FUN_00f57630(&local_5c0,&local_340);
      local_4a8 = 5;
      FUN_03190d30(auStack_840,param_1,&local_5c0,4,1);
      if (local_5c8 == '\x01') {
        FUN_00ac6290(auStack_840);
      }
      FUN_00ac6290(&local_5c0);
      bVar3 = local_c8 & 1;
    }
    if (bVar3 != 0) {
      FUN_00ac6290(&local_340);
    }
  }
  local_850 = &SUB_aaaaaaaaaaaaaaaa;
  local_848 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0077bdd0(&local_850,&local_340);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (local_850 + 0x90,*param_2 + 0x90);
  *(undefined4 *)(local_850 + 0xe4) = 10000;
  uVar5 = FUN_04ded0e8();
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
            (local_850 + 0x5c8,uVar5);
  plVar2 = local_848;
  *(undefined4 *)(local_850 + 0x7c) = 1;
  puStack_868 = &SUB_aaaaaaaaaaaaaaaa;
  local_870 = &SUB_aaaaaaaaaaaaaaaa;
  local_858 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_860 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_878 = &SUB_aaaaaaaaaaaaaaaa;
  local_880 = &SUB_aaaaaaaaaaaaaaaa;
  if (local_848 == (long *)0x0) {
    local_338 = (long *)0x0;
  }
  else {
    plVar1 = local_848 + 1;
    *plVar1 = *plVar1 + 1;
    local_338 = local_848;
    *plVar1 = *plVar1 + 1;
  }
  local_340 = local_850;
  FUN_0317df64(&local_880,param_1,&local_340,0);
  if (plVar2 != (long *)0x0) {
    LOAcquire();
    lVar4 = plVar2[1];
    plVar2[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*plVar2 + 0x10))(plVar2);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  if (plVar2 != (long *)0x0) {
    LOAcquire();
    lVar4 = plVar2[1];
    plVar2[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*plVar2 + 0x10))(plVar2);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  local_580 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_598 = &SUB_aaaaaaaaaaaaaaaa;
  local_5a0 = &SUB_aaaaaaaaaaaaaaaa;
  local_588 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_590 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_5b8 = &SUB_aaaaaaaaaaaaaaaa;
  local_5c0 = &SUB_aaaaaaaaaaaaaaaa;
  local_5a8 = &SUB_aaaaaaaaaaaaaaaa;
  local_5b0 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0086e43c(&local_5c0,local_860);
  if ((char)local_580 == '\x01') {
    _memcpy(&local_340,&DAT_088bcb40,0x280);
    FUN_03190538(&local_340,param_1,&local_5c0,local_5a8._4_4_,(ulong)local_5a8 & 0xffffffff);
    if (local_c8 == 1) {
      FUN_0317d1cc(param_1,&local_340);
      local_c8 = local_c8 & 1;
    }
    if (local_c8 != 0) {
      FUN_00ac6290(&local_340);
    }
    plVar2 = local_858;
    if (((ulong)local_580 & 1) == 0) goto joined_r0x0318f0f4;
  }
  else {
    plVar2 = local_858;
    if ((char)local_580 == '\0') goto joined_r0x0318f0f4;
  }
  if ((long)local_588 < 0) {
    __ZdlPvm(puStack_598,(ulong)local_588 & 0x7fffffffffffffff);
  }
  plVar2 = local_858;
  if ((long)local_5b0 < 0) {
    __ZdlPvm(local_5c0,(ulong)local_5b0 & 0x7fffffffffffffff);
    plVar2 = local_858;
  }
joined_r0x0318f0f4:
  local_858 = plVar2;
  if (plVar2 != (long *)0x0) {
    LOAcquire();
    lVar4 = plVar2[1];
    plVar2[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*plVar2 + 0x10))(plVar2);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  if ((long)puStack_868 < 0) {
    __ZdlPvm(puStack_878,(ulong)puStack_868 & 0x7fffffffffffffff);
  }
  plVar2 = local_848;
  if (local_848 != (long *)0x0) {
    LOAcquire();
    lVar4 = local_848[1];
    local_848[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*local_848 + 0x10))(local_848);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  plVar2 = local_38;
  if (local_38 != (long *)0x0) {
    LOAcquire();
    lVar4 = local_38[1];
    local_38[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*local_38 + 0x10))(local_38);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  return;
}


