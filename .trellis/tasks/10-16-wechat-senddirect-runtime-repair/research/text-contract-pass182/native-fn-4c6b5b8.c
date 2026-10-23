// Ghidra inferred pseudocode; requested=0x4c6b5b8
// entry=04c6b5b8 end=04c6bf63

void FUN_04c6b5b8(long *param_1,long param_2,long *param_3)

{
  undefined8 *puVar1;
  void *pvVar2;
  uint uVar3;
  size_t sVar4;
  code *pcVar5;
  undefined1 uVar6;
  undefined4 uVar7;
  int iVar8;
  undefined8 *puVar9;
  void *pvVar10;
  ulong uVar11;
  undefined8 uVar12;
  long *plVar13;
  long lVar14;
  long lVar15;
  long *plVar16;
  long *plVar17;
  undefined1 local_120;
  undefined7 uStack_11f;
  long *local_118;
  undefined7 local_110;
  char cStack_109;
  long local_108;
  long *plStack_100;
  long *local_f8;
  long *local_f0;
  ulong local_e8;
  long local_e0;
  long *local_d8;
  ulong local_d0;
  undefined1 *local_c8;
  long *local_c0;
  undefined1 *puStack_b8;
  long local_b0;
  long *local_a8;
  undefined1 *local_a0;
  long *plStack_98;
  undefined1 *local_90;
  void *local_88;
  void *local_80;
  void *local_78;
  undefined1 *local_70;
  long *local_68;
  
  *param_1 = (long)&SUB_aaaaaaaaaaaaaaaa;
  param_1[1] = (long)&SUB_aaaaaaaaaaaaaaaa;
  puVar9 = (undefined8 *)__Znwm(0x678);
  puVar9[1] = 0;
  puVar9[2] = 0;
  *puVar9 = &PTR_FUN_09cb06b8;
  puVar1 = puVar9 + 3;
  _bzero(puVar1,0x660);
  FUN_00fdb850(puVar1);
  puVar9[3] = &PTR_thunk_FUN_01512138_09eba160;
  *(undefined2 *)((long)puVar9 + 0x62f) = 0;
  *(undefined2 *)((long)puVar9 + 0x647) = 0;
  *(undefined1 *)((long)puVar9 + 0x65f) = 0;
  *(undefined4 *)(puVar9 + 0xcc) = 0;
  puVar9[0xcd] = 0;
  *(undefined4 *)(puVar9 + 0xce) = 0;
  *(undefined1 *)(puVar9 + 0xbd) = 0;
  puVar9[0xb4] = 0;
  puVar9[0xb3] = 0;
  puVar9[0xb6] = 0;
  puVar9[0xb5] = 0;
  puVar9[0xb8] = 0;
  puVar9[0xb7] = 0;
  puVar9[0xba] = 0;
  puVar9[0xb9] = 0;
  puVar9[0xbc] = 0;
  puVar9[0xbb] = 0;
  *(undefined8 *)((long)puVar9 + 0x607) = 0;
  *(undefined8 *)((long)puVar9 + 0x60f) = 0;
  *(undefined8 *)((long)puVar9 + 0x5ff) = 0;
  *(undefined2 *)((long)puVar9 + 0x617) = 0;
  *param_1 = (long)puVar1;
  param_1[1] = (long)puVar9;
  local_70 = &SUB_aaaaaaaaaaaaaaaa;
  local_68 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_039ee5e4(&local_70,*param_3);
  local_88 = (void *)0x0;
  local_80 = (void *)0x0;
  local_78 = (void *)0x0;
  pvVar2 = *(void **)(param_2 + 0x10);
  sVar4 = *(long *)(param_2 + 0x18) - (long)pvVar2;
  if (sVar4 == 0) {
    pvVar10 = (void *)0x0;
  }
  else {
    if ((long)sVar4 < 0) {
      FUN_00801dbc(&local_88);
                    /* WARNING: Does not return */
      pcVar5 = (code *)SoftwareBreakpoint(1,0x4c6bf64);
      (*pcVar5)();
    }
    pvVar10 = (void *)__Znwm(sVar4);
    local_88 = pvVar10;
    local_78 = (void *)((long)pvVar10 + sVar4);
    _memcpy(pvVar10,pvVar2,sVar4);
    local_80 = (void *)((long)pvVar10 + sVar4);
  }
  FUN_0153c914(puVar9 + 0xb7,pvVar10,local_80,(long)local_80 - (long)pvVar10 >> 2);
  if (local_88 != (void *)0x0) {
    local_80 = local_88;
    __ZdlPvm(local_88,(long)local_78 - (long)local_88);
  }
  lVar15 = *param_1;
  lVar14 = *param_3;
  *(undefined4 *)(lVar15 + 0x5c4) = *(undefined4 *)(lVar14 + 0xa8);
  *(undefined4 *)(lVar15 + 0x5c0) = *(undefined4 *)(lVar14 + 0x74);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (lVar15 + 0x5d0,lVar14 + 0x58);
  lVar14 = *param_3;
  if (*(char *)(lVar14 + 0x1cf) < '\0') {
    FUN_00018d20(&local_a0,*(undefined8 *)(lVar14 + 0x1b8),*(undefined8 *)(lVar14 + 0x1c0));
  }
  else {
    plStack_98 = *(long **)(lVar14 + 0x1c0);
    local_a0 = *(undefined1 **)(lVar14 + 0x1b8);
    local_90 = *(undefined1 **)(lVar14 + 0x1c8);
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(lVar15 + 0x5e8,&local_a0)
  ;
  if ((long)local_90 < 0) {
    __ZdlPvm(local_a0,(ulong)local_90 & 0x7fffffffffffffff);
  }
  uVar3 = *(uint *)(*param_3 + 8);
  uVar11 = (ulong)uVar3;
  if (uVar3 == 0x31) {
    uVar11 = (ulong)*(uint *)(*param_3 + 0xc) << 0x20 | 0x31;
  }
  uVar7 = FUN_04a82b0c(uVar11);
  *(undefined4 *)(lVar15 + 8) = uVar7;
  lVar14 = *param_3;
  if (*(int *)(lVar14 + 8) == 0x31) {
    if ((*(long *)(lVar14 + 0x218) == 0) ||
       (local_a0 = (undefined1 *)
                   ___dynamic_cast(*(long *)(lVar14 + 0x218),&PTR_DAT_09eb1040,&PTR_DAT_09eb0cc0,0),
       local_a0 == (undefined1 *)0x0)) {
      local_a0 = (undefined1 *)0x0;
      plStack_98 = (long *)0x0;
    }
    else {
      plStack_98 = *(long **)(lVar14 + 0x220);
      if (plStack_98 != (long *)0x0) {
        plStack_98[1] = plStack_98[1] + 1;
      }
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (lVar15 + 0x70,local_a0 + 0x460);
    plVar13 = plStack_98;
    if (plStack_98 != (long *)0x0) {
      LOAcquire();
      lVar14 = plStack_98[1];
      plStack_98[1] = lVar14 + -1;
      LORelease();
      if (lVar14 == 0) {
        (**(code **)(*plStack_98 + 0x10))(plStack_98);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
      }
    }
    lVar15 = *param_1;
    lVar14 = *param_3;
  }
  FUN_04a87ae4(&local_a0,lVar14);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(lVar15 + 0xb8,&local_a0);
  if ((long)local_90 < 0) {
    __ZdlPvm(local_a0,(ulong)local_90 & 0x7fffffffffffffff);
  }
  lVar14 = *param_1;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (lVar14 + 0x330,*param_3 + 0x58);
  if (*(int *)(*param_3 + 0xa8) == 0) {
    plVar13 = (long *)FUN_04669774();
    uVar12 = (**(code **)(*plVar13 + 0x50))();
    FUN_04c6c19c(&local_a0,uVar12,uVar12);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (lVar14 + 0x118,&local_a0);
  }
  else {
    FUN_04c6c19c(&local_a0);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (lVar14 + 0x118,&local_a0);
  }
  if ((long)local_90 < 0) {
    __ZdlPvm(local_a0,(ulong)local_90 & 0x7fffffffffffffff);
  }
  FUN_04d3b824(&local_a0,*param_3);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(lVar14 + 0xe8,&local_a0);
  if ((long)local_90 < 0) {
    __ZdlPvm(local_a0,(ulong)local_90 & 0x7fffffffffffffff);
  }
  lVar15 = *param_3;
  *(undefined4 *)(lVar14 + 0x348) = *(undefined4 *)(lVar15 + 0x74);
  *(undefined8 *)(lVar14 + 0x5b8) = *(undefined8 *)(lVar15 + 0xa0);
  *(undefined4 *)(lVar14 + 0x34c) = *(undefined4 *)(lVar15 + 0xa8);
  uVar6 = FUN_04d3ab14();
  *(undefined1 *)(lVar14 + 1000) = uVar6;
  uVar6 = FUN_04d3a9e8(*param_3);
  *(undefined1 *)(lVar14 + 0x3e9) = uVar6;
  uVar7 = FUN_01f238b8(*param_3);
  *(undefined4 *)(lVar14 + 0x438) = uVar7;
  uVar12 = FUN_04554588(*param_3);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(lVar14 + 0x3f0,uVar12);
  *(undefined8 *)(lVar14 + 0x368) = *(undefined8 *)(*param_3 + 0x90);
  local_a8 = (long *)param_1[1];
  if (local_a8 != (long *)0x0) {
    local_a8[1] = local_a8[1] + 1;
  }
  local_b0 = lVar14;
  FUN_04a86ba0(&local_a0,&local_b0,*(undefined4 *)(*(long *)(lVar14 + 0x5a8) + -4));
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(lVar14 + 0x10,&local_a0);
  if ((long)local_90 < 0) {
    __ZdlPvm(local_a0,(ulong)local_90 & 0x7fffffffffffffff);
  }
  plVar13 = local_a8;
  if (local_a8 != (long *)0x0) {
    LOAcquire();
    lVar14 = local_a8[1];
    local_a8[1] = lVar14 + -1;
    LORelease();
    if (lVar14 == 0) {
      (**(code **)(*local_a8 + 0x10))(local_a8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
    }
  }
  lVar14 = *param_1;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (lVar14 + 0x40,lVar14 + 0x10);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (lVar14 + 0x600,*param_3 + 0x10);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (lVar14 + 0x618,*param_3 + 0x28);
  plStack_98 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_90 = &SUB_aaaaaaaaaaaaaaaa;
  local_a0 = &SUB_aaaaaaaaaaaaaaaa;
  lVar14 = *param_3;
  if (*(char *)(lVar14 + 0x57) < '\0') {
    FUN_00018d20(&local_a0,*(undefined8 *)(lVar14 + 0x40),*(undefined8 *)(lVar14 + 0x48));
  }
  else {
    plStack_98 = *(long **)(lVar14 + 0x48);
    local_a0 = *(undefined1 **)(lVar14 + 0x40);
    local_90 = *(undefined1 **)(lVar14 + 0x50);
  }
  plVar13 = plStack_98;
  if (-1 < (long)local_90) {
    plVar13 = (long *)((ulong)local_90 >> 0x38);
  }
  if (plVar13 == (long *)0x0) {
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&local_a0,*param_3 + 0x10);
  }
  local_c0 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  puStack_b8 = &SUB_aaaaaaaaaaaaaaaa;
  local_c8 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0466aca8(&local_120);
  FUN_01205740(&local_f8,CONCAT71(uStack_11f,local_120));
  FUN_0230000c(&local_e0,local_f8);
  FUN_02abe604(&local_c8,local_e0,&local_a0);
  if (local_d8 != (long *)0x0) {
    LOAcquire();
    lVar14 = local_d8[1];
    local_d8[1] = lVar14 + -1;
    LORelease();
    if (lVar14 == 0) {
      (**(code **)(*local_d8 + 0x10))(local_d8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_d8);
    }
  }
  if (local_f0 != (long *)0x0) {
    LOAcquire();
    lVar14 = local_f0[1];
    local_f0[1] = lVar14 + -1;
    LORelease();
    if (lVar14 == 0) {
      (**(code **)(*local_f0 + 0x10))(local_f0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_f0);
    }
  }
  if (local_118 != (long *)0x0) {
    LOAcquire();
    lVar14 = local_118[1];
    local_118[1] = lVar14 + -1;
    LORelease();
    if (lVar14 == 0) {
      (**(code **)(*local_118 + 0x10))(local_118);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_118);
    }
  }
  lVar14 = *param_1;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (lVar14 + 0x100,local_c8 + 0x108);
  plVar13 = (long *)__Znwm(0x60);
  plVar17 = plVar13 + 1;
  *plVar17 = 0;
  plVar13[2] = 0;
  *plVar13 = (long)&PTR_FUN_09c91ee0;
  plVar16 = plVar13 + 3;
  plVar13[4] = 0;
  *plVar16 = 0;
  plVar13[6] = 0;
  plVar13[5] = 0;
  plVar13[8] = 0;
  plVar13[7] = 0;
  plVar13[10] = 0;
  plVar13[9] = 0;
  plVar13[0xb] = 0;
  local_f8 = plVar16;
  local_f0 = plVar13;
  FUN_04bb6ddc(&local_e0,&local_a0);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(plVar13 + 9,&local_e0);
  if ((long)local_d0 < 0) {
    __ZdlPvm(local_e0,local_d0 & 0x7fffffffffffffff);
  }
  iVar8 = FUN_04bb5794(&local_a0);
  if (iVar8 != 0) {
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(plVar16,&local_a0);
  }
  if (plVar13 != (long *)0x0) {
    *plVar17 = *plVar17 + 1;
    *plVar17 = *plVar17 + 1;
    *plVar17 = *plVar17 + 1;
  }
  *(long **)(lVar14 + 0x440) = plVar16;
  plVar16 = *(long **)(lVar14 + 0x448);
  *(long **)(lVar14 + 0x448) = plVar13;
  if (plVar16 != (long *)0x0) {
    LOAcquire();
    lVar14 = plVar16[1];
    plVar16[1] = lVar14 + -1;
    LORelease();
    if (lVar14 == 0) {
      (**(code **)(*plVar16 + 0x10))(plVar16);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar16);
    }
  }
  plVar16 = local_f0;
  if (plVar13 != (long *)0x0) {
    LOAcquire();
    lVar14 = plVar13[1];
    plVar13[1] = lVar14 + -1;
    LORelease();
    if (lVar14 == 0) {
      (**(code **)(*plVar13 + 0x10))(plVar13);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
      LOAcquire();
      lVar14 = *plVar17;
      *plVar17 = lVar14 + -1;
      LORelease();
    }
    else {
      LOAcquire();
      lVar14 = *plVar17;
      *plVar17 = lVar14 + -1;
      LORelease();
    }
    plVar16 = local_f0;
    if (lVar14 == 0) {
      (**(code **)(*plVar13 + 0x10))(plVar13);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
      plVar16 = local_f0;
    }
  }
  if (plVar16 != (long *)0x0) {
    LOAcquire();
    lVar14 = plVar16[1];
    plVar16[1] = lVar14 + -1;
    LORelease();
    if (lVar14 == 0) {
      local_f0 = plVar16;
      (**(code **)(*plVar16 + 0x10))(plVar16);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar16);
    }
  }
  local_e0 = 0;
  local_d8 = (long *)0x0;
  local_d0 = 0;
  local_f8 = (long *)0x0;
  local_f0 = (long *)0x0;
  local_e8 = 0;
  iVar8 = FUN_02750ad8(*param_3,&local_e0,&local_f8);
  if (iVar8 != 0) {
    plVar13 = local_d8;
    if (-1 < (long)local_d0) {
      plVar13 = (long *)(local_d0 >> 0x38);
    }
    lVar14 = *param_1;
    if (plVar13 != (long *)0x0) {
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (lVar14 + 0xb8,&local_e0);
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (lVar14 + 0x100,&local_f8);
    local_108 = *(long *)(lVar14 + 0x440);
    plVar13 = *(long **)(lVar14 + 0x448);
    if (plVar13 != (long *)0x0) {
      plVar13[1] = plVar13[1] + 1;
    }
    plStack_100 = plVar13;
    if (local_108 != 0) {
      cStack_109 = '\0';
      local_120 = 0;
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (local_108 + 0x30,&local_120);
      if (cStack_109 < '\0') {
        __ZdlPvm(CONCAT71(uStack_11f,local_120),CONCAT17(cStack_109,local_110) & 0x7fffffffffffffff)
        ;
      }
    }
    if (plVar13 != (long *)0x0) {
      LOAcquire();
      lVar14 = plVar13[1];
      plVar13[1] = lVar14 + -1;
      LORelease();
      if (lVar14 == 0) {
        (**(code **)(*plVar13 + 0x10))(plVar13);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
      }
    }
  }
  if ((long)local_e8 < 0) {
    __ZdlPvm(local_f8,local_e8 & 0x7fffffffffffffff);
  }
  if ((long)local_d0 < 0) {
    __ZdlPvm(local_e0,local_d0 & 0x7fffffffffffffff);
  }
  local_e0 = *(long *)(*param_3 + 0x228);
  local_d8 = *(long **)(*param_3 + 0x230);
  if (local_d8 != (long *)0x0) {
    local_d8[1] = local_d8[1] + 1;
  }
  if (local_e0 != 0) {
    local_f8 = *(long **)(local_e0 + 0x58);
    plVar13 = *(long **)(local_e0 + 0x60);
    if (plVar13 != (long *)0x0) {
      plVar13[1] = plVar13[1] + 1;
    }
    local_f0 = plVar13;
    if (local_f8 != (long *)0x0) {
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(*param_1 + 0x350);
    }
    if (plVar13 != (long *)0x0) {
      LOAcquire();
      lVar14 = plVar13[1];
      plVar13[1] = lVar14 + -1;
      LORelease();
      if (lVar14 == 0) {
        (**(code **)(*plVar13 + 0x10))(plVar13);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
      }
    }
  }
  plVar13 = local_d8;
  if (local_d8 != (long *)0x0) {
    LOAcquire();
    lVar14 = local_d8[1];
    local_d8[1] = lVar14 + -1;
    LORelease();
    if (lVar14 == 0) {
      (**(code **)(*local_d8 + 0x10))(local_d8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
    }
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (*param_1 + 0x630,param_2 + 0x28);
  plVar13 = local_c0;
  if (local_c0 != (long *)0x0) {
    LOAcquire();
    lVar14 = local_c0[1];
    local_c0[1] = lVar14 + -1;
    LORelease();
    if (lVar14 == 0) {
      (**(code **)(*local_c0 + 0x10))(local_c0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
    }
  }
  if ((long)local_90 < 0) {
    __ZdlPvm(local_a0,(ulong)local_90 & 0x7fffffffffffffff);
  }
  plVar13 = local_68;
  if (local_68 != (long *)0x0) {
    LOAcquire();
    lVar14 = local_68[1];
    local_68[1] = lVar14 + -1;
    LORelease();
    if (lVar14 == 0) {
      (**(code **)(*local_68 + 0x10))(local_68);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
    }
  }
  return;
}


