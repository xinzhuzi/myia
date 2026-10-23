// Ghidra inferred pseudocode; requested=0x2672934
// entry=02672934 end=02672c77

undefined8
FUN_02672934(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
            undefined8 param_5,long param_6,undefined8 param_7)

{
  ulong uVar1;
  int iVar2;
  uint uVar3;
  uint uVar4;
  undefined8 uVar5;
  long lVar6;
  undefined1 *puVar7;
  undefined8 *puVar8;
  undefined8 local_1f8;
  long *local_1f0;
  undefined8 local_1e8;
  long *local_1e0;
  undefined8 local_1d8;
  long *local_1d0;
  undefined7 local_1c8;
  char cStack_1c1;
  undefined1 *local_1c0;
  undefined1 *puStack_1b8;
  undefined1 *local_1b0;
  undefined1 *puStack_1a8;
  undefined1 *local_1a0;
  undefined1 *puStack_198;
  undefined1 *local_190;
  undefined1 *puStack_188;
  undefined1 *puStack_180;
  undefined1 *puStack_178;
  undefined1 *local_170;
  undefined1 *puStack_168;
  undefined1 *puStack_160;
  undefined1 *puStack_158;
  undefined1 *local_150;
  undefined1 *puStack_148;
  undefined1 *puStack_140;
  undefined1 *puStack_138;
  undefined1 *local_130;
  undefined8 *puStack_128;
  undefined1 *puStack_120;
  undefined1 *puStack_118;
  undefined1 *local_110;
  undefined1 *puStack_108;
  undefined1 *puStack_100;
  undefined1 *puStack_f8;
  undefined1 *local_f0;
  undefined1 *puStack_e8;
  undefined1 *puStack_e0;
  undefined1 *puStack_d8;
  undefined1 *local_d0;
  undefined1 *puStack_c8;
  undefined1 *puStack_c0;
  undefined1 *puStack_b8;
  undefined1 *local_b0;
  undefined8 *puStack_a8;
  undefined1 *puStack_a0;
  undefined1 *puStack_98;
  undefined1 *local_90;
  undefined1 *puStack_88;
  undefined1 *puStack_80;
  undefined1 *puStack_78;
  undefined1 *local_70;
  undefined1 *puStack_68;
  undefined1 *puStack_60;
  undefined1 *local_58;
  
  puStack_68 = &SUB_aaaaaaaaaaaaaaaa;
  local_70 = &SUB_aaaaaaaaaaaaaaaa;
  local_58 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_60 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_88 = &SUB_aaaaaaaaaaaaaaaa;
  local_90 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_78 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_80 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_a8 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
  local_b0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_98 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_a0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_c8 = &SUB_aaaaaaaaaaaaaaaa;
  local_d0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_b8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_c0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_e8 = &SUB_aaaaaaaaaaaaaaaa;
  local_f0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_d8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_e0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_108 = &SUB_aaaaaaaaaaaaaaaa;
  local_110 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_f8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_100 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_128 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
  local_130 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_118 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_120 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_148 = &SUB_aaaaaaaaaaaaaaaa;
  local_150 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_138 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_140 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_168 = &SUB_aaaaaaaaaaaaaaaa;
  local_170 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_158 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_160 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_188 = &SUB_aaaaaaaaaaaaaaaa;
  local_190 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_178 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_180 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_198 = &SUB_aaaaaaaaaaaaaaaa;
  local_1a0 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0559f0e8(&local_1a0);
  FUN_02673854(param_1,param_2,param_4,param_5,&local_1a0);
  local_58 = (undefined1 *)((ulong)local_58 | 0x100);
  if (puStack_128 == &DAT_0a524ad0) {
    puStack_128 = (undefined8 *)__Znwm(0x18);
    *puStack_128 = 0;
    puStack_128[1] = 0;
    puStack_128[2] = 0;
  }
  uVar5 = __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                    (puStack_128,param_3);
  FUN_02673a80(uVar5,&local_1a0,param_5,param_7);
  uVar1 = *(ulong *)(param_6 + 0x10);
  if (-1 < (char)*(byte *)(param_6 + 0x1f)) {
    uVar1 = (ulong)*(byte *)(param_6 + 0x1f);
  }
  if (uVar1 != 0) {
    puStack_1b8 = &SUB_aaaaaaaaaaaaaaaa;
    local_1c0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_1a8 = &SUB_aaaaaaaaaaaaaaaa;
    local_1b0 = &SUB_aaaaaaaaaaaaaaaa;
    FUN_0559f584(&local_1c0);
    lVar6 = __ZNSt3__16chrono12system_clock3nowEv();
    puStack_1b8 = (undefined1 *)(lVar6 / 1000);
    puStack_1a8 = (undefined1 *)((ulong)puStack_1a8 | 0x300000000);
    if (local_1b0 == (undefined1 *)0x0) {
      puVar7 = (undefined1 *)__Znwm(0x28);
      FUN_0559f598();
      local_1b0 = puVar7;
    }
    puVar7 = local_1b0;
    *(uint *)(local_1b0 + 0x24) = *(uint *)(local_1b0 + 0x24) | 1;
    puVar8 = *(undefined8 **)(local_1b0 + 8);
    if (puVar8 == &DAT_0a524ad0) {
      puVar8 = (undefined8 *)__Znwm(0x18);
      *puVar8 = 0;
      puVar8[1] = 0;
      puVar8[2] = 0;
      *(undefined8 **)(puVar7 + 8) = puVar8;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar8,param_6 + 8);
    iVar2 = *(int *)(param_6 + 4);
    uVar3 = *(uint *)(puVar7 + 0x24);
    *(uint *)(puVar7 + 0x24) = uVar3 | 2;
    *(ulong *)(puVar7 + 0x10) = (ulong)(iVar2 - 1);
    uVar4 = *(uint *)(param_6 + 4);
    *(uint *)(puVar7 + 0x24) = uVar3 | 6;
    *(ulong *)(puVar7 + 0x18) = (ulong)uVar4;
    FUN_05ab4028(&local_1d8,&local_1c0);
    local_58 = (undefined1 *)((ulong)local_58 | 0x4000000);
    if (puStack_a8 == &DAT_0a524ad0) {
      puStack_a8 = (undefined8 *)__Znwm(0x18);
      *puStack_a8 = 0;
      puStack_a8[1] = 0;
      puStack_a8[2] = 0;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puStack_a8,&local_1d8);
    if (cStack_1c1 < '\0') {
      __ZdlPvm(local_1d8,CONCAT17(cStack_1c1,local_1c8) & 0x7fffffffffffffff);
    }
    FUN_055db200(&local_1c0);
  }
  local_1c0 = (undefined1 *)0x0;
  puStack_1b8 = (undefined1 *)0x0;
  local_1b0 = (undefined1 *)0x0;
  FUN_05ab3f60(&local_1a0,&local_1c0);
  FUN_0466aca8(&local_1f8);
  FUN_01205740(&local_1e8,local_1f8);
  FUN_02662244(&local_1d8,local_1e8);
  uVar5 = FUN_0265e9b8(local_1d8,param_2,0x3eb,&local_1c0,param_4,4);
  if (local_1d0 != (long *)0x0) {
    LOAcquire();
    lVar6 = local_1d0[1];
    local_1d0[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*local_1d0 + 0x10))(local_1d0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_1d0);
    }
  }
  if (local_1e0 != (long *)0x0) {
    LOAcquire();
    lVar6 = local_1e0[1];
    local_1e0[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*local_1e0 + 0x10))(local_1e0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_1e0);
    }
  }
  if (local_1f0 != (long *)0x0) {
    LOAcquire();
    lVar6 = local_1f0[1];
    local_1f0[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*local_1f0 + 0x10))(local_1f0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_1f0);
    }
  }
  if ((long)local_1b0 < 0) {
    __ZdlPvm(local_1c0,(ulong)local_1b0 & 0x7fffffffffffffff);
  }
  thunk_FUN_055ad7d4(&local_1a0);
  return uVar5;
}


