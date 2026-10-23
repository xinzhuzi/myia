// Ghidra inferred pseudocode; requested=0x2671f68
// entry=02671f68 end=0267278b

undefined8
FUN_02671f68(undefined8 param_1,undefined8 param_2,undefined8 param_3,char *param_4,
            undefined8 param_5,uint *param_6,undefined8 param_7)

{
  int iVar1;
  uint uVar2;
  long *plVar3;
  undefined8 uVar4;
  undefined8 *puVar5;
  undefined1 *puVar6;
  int iVar7;
  ulong uVar8;
  long lVar9;
  long lVar10;
  long lVar11;
  long lVar12;
  ulong uVar13;
  undefined8 local_250 [2];
  undefined7 local_240;
  char cStack_239;
  undefined8 local_238;
  long *local_230;
  undefined7 local_228;
  char cStack_221;
  undefined1 *local_220;
  long *plStack_218;
  undefined1 *local_210;
  undefined1 *puStack_208;
  undefined8 local_1f8;
  long *local_1f0;
  ulong local_1e8;
  undefined1 *local_1e0;
  undefined1 *puStack_1d8;
  undefined8 local_1d0;
  undefined1 *local_1c8;
  undefined1 *local_1c0;
  undefined1 *local_1b0;
  undefined1 *puStack_1a8;
  undefined1 *local_1a0;
  undefined1 *puStack_198;
  undefined1 *puStack_190;
  undefined1 *puStack_188;
  undefined1 *local_180;
  undefined1 *puStack_178;
  undefined1 *puStack_170;
  undefined1 *puStack_168;
  undefined1 *local_160;
  undefined1 *puStack_158;
  undefined1 *puStack_150;
  undefined1 *puStack_148;
  undefined1 *local_140;
  undefined1 *puStack_138;
  undefined1 *puStack_130;
  undefined1 *puStack_128;
  undefined1 *local_120;
  undefined1 *puStack_118;
  undefined1 *puStack_110;
  undefined1 *puStack_108;
  undefined1 *local_100;
  undefined1 *puStack_f8;
  undefined1 *puStack_f0;
  undefined1 *puStack_e8;
  undefined1 *local_e0;
  undefined1 *puStack_d8;
  undefined1 *puStack_d0;
  undefined1 *puStack_c8;
  undefined1 *local_c0;
  undefined8 *puStack_b8;
  undefined8 *local_b0;
  undefined1 *puStack_a8;
  undefined1 *local_a0;
  undefined1 *puStack_98;
  undefined1 *puStack_90;
  undefined1 *puStack_88;
  undefined1 *local_80;
  undefined1 *puStack_78;
  undefined1 *puStack_70;
  undefined1 *local_68;
  
  puStack_78 = &SUB_aaaaaaaaaaaaaaaa;
  local_80 = &SUB_aaaaaaaaaaaaaaaa;
  local_68 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_70 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_98 = &SUB_aaaaaaaaaaaaaaaa;
  local_a0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_88 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_90 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_b8 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
  local_c0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_a8 = &SUB_aaaaaaaaaaaaaaaa;
  local_b0 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
  puStack_d8 = &SUB_aaaaaaaaaaaaaaaa;
  local_e0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_c8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_d0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_f8 = &SUB_aaaaaaaaaaaaaaaa;
  local_100 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_e8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_f0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_118 = &SUB_aaaaaaaaaaaaaaaa;
  local_120 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_108 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_110 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_138 = &SUB_aaaaaaaaaaaaaaaa;
  local_140 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_128 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_130 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_158 = &SUB_aaaaaaaaaaaaaaaa;
  local_160 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_148 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_150 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_178 = &SUB_aaaaaaaaaaaaaaaa;
  local_180 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_168 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_170 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_198 = &SUB_aaaaaaaaaaaaaaaa;
  local_1a0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_188 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_190 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1a8 = &SUB_aaaaaaaaaaaaaaaa;
  local_1b0 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0559f0e8(&local_1b0);
  uVar4 = FUN_02673854(param_1,param_2,param_3,param_5,&local_1b0);
  FUN_02673a80(uVar4,&local_1b0,param_5,param_7);
  if (*(long *)(param_4 + 8) == *(long *)(param_4 + 0x10)) goto LAB_0267247c;
  local_1c0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1d8 = &SUB_aaaaaaaaaaaaaaaa;
  local_1e0 = &SUB_aaaaaaaaaaaaaaaa;
  local_1c8 = &SUB_aaaaaaaaaaaaaaaa;
  local_1d0 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0559f7a4(&local_1e0);
  lVar9 = (long)(int)local_1d0;
  if ((int)local_1d0 < local_1d0._4_4_) {
    local_1d0 = (undefined1 *)CONCAT44(local_1d0._4_4_,(int)local_1d0 + 1);
    lVar9 = *(long *)(puStack_1d8 + lVar9 * 8);
  }
  else {
    if (local_1d0._4_4_ == (int)local_1c8) {
      FUN_05ab4038((ulong)&local_1e0 | 8,local_1d0._4_4_ + 1);
    }
    local_1d0._4_4_ = local_1d0._4_4_ + 1;
    lVar9 = __Znwm(0xe8);
    FUN_0559f5c0();
    lVar10 = (long)(int)local_1d0;
    local_1d0 = (undefined1 *)CONCAT44(local_1d0._4_4_,(int)local_1d0 + 1);
    *(long *)(puStack_1d8 + lVar10 * 8) = lVar9;
  }
  if (*param_4 == '\x01') {
    uVar13 = (ulong)*param_6;
    if (((int)*param_6 < 0) ||
       (lVar10 = *(long *)(param_4 + 8),
       uVar8 = (*(long *)(param_4 + 0x10) - lVar10 >> 3) * -0x70a3d70a3d70a3d7,
       uVar8 < uVar13 || uVar8 - uVar13 == 0)) goto LAB_02672254;
    *(uint *)(lVar9 + 0xe0) = *(uint *)(lVar9 + 0xe0) | 1;
    *(undefined4 *)(lVar9 + 0xd8) = 4;
    uVar2 = *param_6;
    iVar1 = *(int *)(lVar9 + 0x40);
    iVar7 = *(int *)(lVar9 + 0x44);
    if (iVar1 < iVar7) {
      *(int *)(lVar9 + 0x40) = iVar1 + 1;
      lVar12 = *(long *)(*(long *)(lVar9 + 0x38) + (long)iVar1 * 8);
    }
    else {
      if (iVar7 == *(int *)(lVar9 + 0x48)) {
        FUN_05ab4038(lVar9 + 0x38,iVar7 + 1);
        iVar7 = *(int *)(lVar9 + 0x44);
      }
      *(int *)(lVar9 + 0x44) = iVar7 + 1;
      lVar12 = __Znwm(0x48);
      FUN_0559f648();
      iVar1 = *(int *)(lVar9 + 0x40);
      *(int *)(lVar9 + 0x40) = iVar1 + 1;
      *(long *)(*(long *)(lVar9 + 0x38) + (long)iVar1 * 8) = lVar12;
    }
    *(uint *)(lVar12 + 0x40) = *(uint *)(lVar12 + 0x40) | 1;
    puVar5 = *(undefined8 **)(lVar12 + 8);
    if (puVar5 == &DAT_0a524ad0) {
      puVar5 = (undefined8 *)__Znwm(0x18);
      *puVar5 = 0;
      puVar5[1] = 0;
      puVar5[2] = 0;
      *(undefined8 **)(lVar12 + 8) = puVar5;
    }
    lVar10 = lVar10 + (long)(int)uVar2 * 200;
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar5,lVar10 + 0x18);
    *(uint *)(lVar12 + 0x40) = *(uint *)(lVar12 + 0x40) | 2;
    puVar5 = *(undefined8 **)(lVar12 + 0x10);
    if (puVar5 == &DAT_0a524ad0) {
      puVar5 = (undefined8 *)__Znwm(0x18);
      *puVar5 = 0;
      puVar5[1] = 0;
      puVar5[2] = 0;
      *(undefined8 **)(lVar12 + 0x10) = puVar5;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar5,lVar10 + 0x30);
    *(uint *)(lVar12 + 0x40) = *(uint *)(lVar12 + 0x40) | 4;
    puVar5 = *(undefined8 **)(lVar12 + 0x18);
    if (puVar5 == &DAT_0a524ad0) {
      puVar5 = (undefined8 *)__Znwm(0x18);
      *puVar5 = 0;
      puVar5[1] = 0;
      puVar5[2] = 0;
      *(undefined8 **)(lVar12 + 0x18) = puVar5;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar5,lVar10 + 0x48);
    FUN_0002bd88(&local_1f8,lVar10);
    FUN_0002def0(&local_220,&local_1f8);
    *(uint *)(lVar12 + 0x40) = *(uint *)(lVar12 + 0x40) | 8;
    puVar5 = *(undefined8 **)(lVar12 + 0x20);
    if (puVar5 == &DAT_0a524ad0) {
      puVar5 = (undefined8 *)__Znwm(0x18);
      *puVar5 = 0;
      puVar5[1] = 0;
      puVar5[2] = 0;
      *(undefined8 **)(lVar12 + 0x20) = puVar5;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar5,&local_220);
    if ((long)local_210 < 0) {
      __ZdlPvm(local_220,(ulong)local_210 & 0x7fffffffffffffff);
    }
    FUN_0002b440(&local_1f8);
    __ZNSt3__19to_stringEi(&local_220,5);
    *(uint *)(lVar12 + 0x40) = *(uint *)(lVar12 + 0x40) | 0x10;
    puVar5 = *(undefined8 **)(lVar12 + 0x28);
    if (puVar5 == &DAT_0a524ad0) {
      puVar5 = (undefined8 *)__Znwm(0x18);
      *puVar5 = 0;
      puVar5[1] = 0;
      puVar5[2] = 0;
      *(undefined8 **)(lVar12 + 0x28) = puVar5;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar5,&local_220);
    if ((long)local_210 < 0) {
      __ZdlPvm(local_220,(ulong)local_210 & 0x7fffffffffffffff);
    }
    uVar4 = *(undefined8 *)(lVar10 + 0xc0);
    *(uint *)(lVar12 + 0x40) = *(uint *)(lVar12 + 0x40) | 0x40;
    *(undefined8 *)(lVar12 + 0x30) = uVar4;
  }
  else {
    if (*param_4 == '\0') {
      *(uint *)(lVar9 + 0xe0) = *(uint *)(lVar9 + 0xe0) | 1;
      *(undefined4 *)(lVar9 + 0xd8) = 1;
      lVar12 = *(long *)(param_4 + 0x10);
      for (lVar10 = *(long *)(param_4 + 8); lVar10 != lVar12; lVar10 = lVar10 + 200) {
        iVar1 = *(int *)(lVar9 + 0x10);
        iVar7 = *(int *)(lVar9 + 0x14);
        if (iVar1 < iVar7) {
          *(int *)(lVar9 + 0x10) = iVar1 + 1;
          lVar11 = *(long *)(*(long *)(lVar9 + 8) + (long)iVar1 * 8);
        }
        else {
          if (iVar7 == *(int *)(lVar9 + 0x18)) {
            FUN_05ab4038(lVar9 + 8,iVar7 + 1);
            iVar7 = *(int *)(lVar9 + 0x14);
          }
          *(int *)(lVar9 + 0x14) = iVar7 + 1;
          lVar11 = __Znwm(0x28);
          FUN_0559f628();
          iVar1 = *(int *)(lVar9 + 0x10);
          *(int *)(lVar9 + 0x10) = iVar1 + 1;
          *(long *)(*(long *)(lVar9 + 8) + (long)iVar1 * 8) = lVar11;
        }
        *(uint *)(lVar11 + 0x24) = *(uint *)(lVar11 + 0x24) | 1;
        puVar5 = *(undefined8 **)(lVar11 + 8);
        if (puVar5 == &DAT_0a524ad0) {
          puVar5 = (undefined8 *)__Znwm(0x18);
          *puVar5 = 0;
          puVar5[1] = 0;
          puVar5[2] = 0;
          *(undefined8 **)(lVar11 + 8) = puVar5;
        }
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (puVar5,lVar10 + 0x18);
        *(uint *)(lVar11 + 0x24) = *(uint *)(lVar11 + 0x24) | 2;
        puVar5 = *(undefined8 **)(lVar11 + 0x10);
        if (puVar5 == &DAT_0a524ad0) {
          puVar5 = (undefined8 *)__Znwm(0x18);
          *puVar5 = 0;
          puVar5[1] = 0;
          puVar5[2] = 0;
          *(undefined8 **)(lVar11 + 0x10) = puVar5;
        }
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (puVar5,lVar10 + 0x30);
        *(uint *)(lVar11 + 0x24) = *(uint *)(lVar11 + 0x24) | 4;
        puVar5 = *(undefined8 **)(lVar11 + 0x18);
        if (puVar5 == &DAT_0a524ad0) {
          puVar5 = (undefined8 *)__Znwm(0x18);
          *puVar5 = 0;
          puVar5[1] = 0;
          puVar5[2] = 0;
          *(undefined8 **)(lVar11 + 0x18) = puVar5;
        }
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (puVar5,lVar10 + 0x48);
      }
    }
LAB_02672254:
    uVar13 = 0;
  }
  if (0 < (int)local_1d0) {
    local_1f8 = 0;
    local_1f0 = (long *)0x0;
    local_1e8 = 0;
    FUN_05ab3f60(&local_1e0,&local_1f8);
    local_68 = (undefined1 *)((ulong)local_68 | 0x8000000);
    if (local_b0 == &DAT_0a524ad0) {
      local_b0 = (undefined8 *)__Znwm(0x18);
      *local_b0 = 0;
      local_b0[1] = 0;
      local_b0[2] = 0;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(local_b0,&local_1f8);
    plStack_218 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    local_220 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_208 = &SUB_aaaaaaaaaaaaaaaa;
    local_210 = &SUB_aaaaaaaaaaaaaaaa;
    FUN_0559f584(&local_220);
    lVar9 = __ZNSt3__16chrono12system_clock3nowEv();
    plStack_218 = (long *)(lVar9 / 1000);
    puStack_208 = (undefined1 *)((ulong)puStack_208 | 0x300000000);
    if (local_210 == (undefined1 *)0x0) {
      puVar6 = (undefined1 *)__Znwm(0x28);
      FUN_0559f598();
      local_210 = puVar6;
    }
    puVar6 = local_210;
    uVar8 = *(ulong *)(param_6 + 4);
    if (-1 < (char)*(byte *)((long)param_6 + 0x1f)) {
      uVar8 = (ulong)*(byte *)((long)param_6 + 0x1f);
    }
    if (uVar8 == 0) {
      FUN_06686abc(local_250,0x10);
      FUN_06688334(&local_238,local_250,0);
      *(uint *)(puVar6 + 0x24) = *(uint *)(puVar6 + 0x24) | 1;
      puVar5 = *(undefined8 **)(puVar6 + 8);
      if (puVar5 == &DAT_0a524ad0) {
        puVar5 = (undefined8 *)__Znwm(0x18);
        *puVar5 = 0;
        puVar5[1] = 0;
        puVar5[2] = 0;
        *(undefined8 **)(puVar6 + 8) = puVar5;
      }
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar5,&local_238);
      if (cStack_221 < '\0') {
        __ZdlPvm(local_238,CONCAT17(cStack_221,local_228) & 0x7fffffffffffffff);
      }
      if (cStack_239 < '\0') {
        __ZdlPvm(local_250[0],CONCAT17(cStack_239,local_240) & 0x7fffffffffffffff);
      }
      uVar8 = 1;
    }
    else {
      *(uint *)(local_210 + 0x24) = *(uint *)(local_210 + 0x24) | 1;
      puVar5 = *(undefined8 **)(local_210 + 8);
      if (puVar5 == &DAT_0a524ad0) {
        puVar5 = (undefined8 *)__Znwm(0x18);
        *puVar5 = 0;
        puVar5[1] = 0;
        puVar5[2] = 0;
        *(undefined8 **)(puVar6 + 8) = puVar5;
      }
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar5,param_6 + 2);
      uVar8 = (ulong)param_6[1];
    }
    *(uint *)(puVar6 + 0x24) = *(uint *)(puVar6 + 0x24) | 6;
    *(ulong *)(puVar6 + 0x10) = uVar13;
    *(ulong *)(puVar6 + 0x18) = uVar8;
    FUN_05ab4028(&local_238,&local_220);
    local_68 = (undefined1 *)((ulong)local_68 | 0x4000000);
    if (puStack_b8 == &DAT_0a524ad0) {
      puStack_b8 = (undefined8 *)__Znwm(0x18);
      *puStack_b8 = 0;
      puStack_b8[1] = 0;
      puStack_b8[2] = 0;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puStack_b8,&local_238);
    if (cStack_221 < '\0') {
      __ZdlPvm(local_238,CONCAT17(cStack_221,local_228) & 0x7fffffffffffffff);
    }
    FUN_055db200(&local_220);
    if ((long)local_1e8 < 0) {
      __ZdlPvm(local_1f8,local_1e8 & 0x7fffffffffffffff);
    }
  }
  FUN_055e6f30(&local_1e0);
LAB_0267247c:
  local_1e0 = (undefined1 *)0x0;
  puStack_1d8 = (undefined1 *)0x0;
  local_1d0 = (undefined1 *)0x0;
  FUN_05ab3f60(&local_1b0,&local_1e0);
  FUN_0466aca8(&local_238);
  FUN_01205740(&local_1f8,local_238);
  FUN_02662244(&local_220,local_1f8);
  uVar4 = FUN_0265e9b8(local_220,param_2,0x3eb,&local_1e0,param_3,4);
  plVar3 = plStack_218;
  if (plStack_218 != (long *)0x0) {
    LOAcquire();
    lVar9 = plStack_218[1];
    plStack_218[1] = lVar9 + -1;
    LORelease();
    if (lVar9 == 0) {
      (**(code **)(*plStack_218 + 0x10))(plStack_218);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  plVar3 = local_1f0;
  if (local_1f0 != (long *)0x0) {
    LOAcquire();
    lVar9 = local_1f0[1];
    local_1f0[1] = lVar9 + -1;
    LORelease();
    if (lVar9 == 0) {
      (**(code **)(*local_1f0 + 0x10))(local_1f0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  if (local_230 != (long *)0x0) {
    LOAcquire();
    lVar9 = local_230[1];
    local_230[1] = lVar9 + -1;
    LORelease();
    if (lVar9 == 0) {
      (**(code **)(*local_230 + 0x10))(local_230);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_230);
    }
  }
  if ((long)local_1d0 < 0) {
    __ZdlPvm(local_1e0,(ulong)local_1d0 & 0x7fffffffffffffff);
  }
  thunk_FUN_055ad7d4(&local_1b0);
  return uVar4;
}


