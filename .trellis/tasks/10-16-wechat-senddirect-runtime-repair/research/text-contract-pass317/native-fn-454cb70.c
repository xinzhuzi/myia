// Ghidra inferred pseudocode; requested=0x454cb70
// entry=0454cb70 end=0454dbd3

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

long * FUN_0454cb70(long *param_1,long param_2)

{
  undefined1 uVar1;
  uint3 uVar2;
  bool bVar3;
  long lVar4;
  int iVar5;
  uint uVar6;
  undefined8 *puVar7;
  long lVar8;
  undefined8 uVar9;
  ulong uVar10;
  size_t sVar11;
  undefined8 *******pppppppuVar12;
  code *pcVar13;
  undefined1 *puVar14;
  undefined1 *puVar15;
  ulong uVar16;
  long *plVar17;
  byte bVar18;
  byte bVar21;
  byte bVar25;
  byte bVar29;
  byte bVar33;
  byte bVar37;
  byte bVar41;
  byte bVar45;
  undefined4 uVar49;
  undefined4 uVar50;
  long lVar51;
  long lVar52;
  long lVar53;
  long lVar54;
  long lVar55;
  long lVar56;
  undefined1 *local_430;
  long *local_428;
  undefined1 auStack_420 [496];
  long *local_230;
  undefined1 auStack_228 [8];
  long *local_220;
  undefined8 *******local_218 [2];
  undefined7 local_208;
  char cStack_201;
  long alStack_200 [3];
  long *local_1e8;
  undefined8 *******local_1e0;
  undefined8 local_1d8;
  undefined7 local_1d0;
  char cStack_1c9;
  undefined8 *******local_190;
  long *plStack_188;
  undefined8 local_180;
  undefined8 local_178;
  undefined8 local_170;
  undefined8 uStack_168;
  undefined8 uStack_160;
  undefined8 uStack_158;
  undefined8 *******local_100;
  long *plStack_f8;
  undefined8 uStack_f0;
  undefined8 local_e8;
  undefined8 uStack_e0;
  undefined8 local_d8;
  undefined8 uStack_d0;
  undefined8 local_c8;
  undefined8 uStack_c0;
  undefined8 local_b8;
  undefined8 uStack_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined8 local_88;
  long local_78;
  byte bVar19;
  byte bVar20;
  byte bVar22;
  byte bVar23;
  byte bVar24;
  byte bVar26;
  byte bVar27;
  byte bVar28;
  byte bVar30;
  byte bVar31;
  byte bVar32;
  byte bVar34;
  byte bVar35;
  byte bVar36;
  byte bVar38;
  byte bVar39;
  byte bVar40;
  byte bVar42;
  byte bVar43;
  byte bVar44;
  byte bVar46;
  byte bVar47;
  byte bVar48;
  
  local_78 = *(long *)PTR____stack_chk_guard_09b36c98;
  param_1[1] = 0;
  param_1[2] = 0;
  *param_1 = (long)&PTR_FUN_09e87768;
  puVar7 = (undefined8 *)__Znwm(0x48);
  puVar7[4] = 0;
  puVar7[3] = 0;
  param_1[3] = (long)(puVar7 + 3);
  param_1[4] = (long)puVar7;
  puVar7[1] = 0;
  puVar7[2] = 0;
  *puVar7 = &PTR_FUN_09e87830;
  puVar7[6] = 0;
  puVar7[5] = 0;
  puVar7[7] = 0;
  puVar7[8] = 0;
  *(undefined4 *)(puVar7 + 7) = 0x3f800000;
  puVar7 = (undefined8 *)__Znwm(0x70);
  puVar7[1] = 0;
  puVar7[2] = 0;
  *puVar7 = &PTR_FUN_09e87880;
  puVar7[8] = 0;
  puVar7[7] = 0;
  puVar7[10] = 0;
  puVar7[9] = 0;
  puVar7[0xc] = 0;
  puVar7[0xb] = 0;
  puVar7[6] = 0;
  puVar7[5] = 0;
  puVar7[4] = 0;
  puVar7[3] = 0;
  *(undefined4 *)(puVar7 + 7) = 0x3f800000;
  puVar7[9] = 0;
  puVar7[8] = 0;
  puVar7[0xb] = 0;
  puVar7[10] = 0;
  *(undefined4 *)(puVar7 + 0xc) = 0x3f800000;
  puVar7[0xd] = 0;
  param_1[5] = (long)(puVar7 + 3);
  param_1[6] = (long)puVar7;
  *(undefined2 *)(param_1 + 7) = 0;
  FUN_04bdac14(param_1 + 8);
  param_1[0x5a] = 0;
  param_1[0x57] = 0;
  param_1[0x56] = 0;
  param_1[0x59] = 0;
  param_1[0x58] = 0;
  param_1[0x53] = 0;
  param_1[0x52] = 0;
  param_1[0x55] = 0;
  param_1[0x54] = 0;
  param_1[0x4f] = 0;
  param_1[0x4e] = 0;
  param_1[0x51] = 0;
  param_1[0x50] = 0;
  param_1[0x4b] = 0;
  param_1[0x4a] = 0;
  param_1[0x4d] = 0;
  param_1[0x4c] = 0;
  param_1[0x47] = 0;
  param_1[0x46] = 0;
  param_1[0x49] = 0;
  param_1[0x48] = 0;
  param_1[0x43] = 0;
  param_1[0x42] = 0;
  param_1[0x45] = 0;
  param_1[0x44] = 0;
  param_1[0x3f] = 0;
  param_1[0x3e] = 0;
  param_1[0x41] = 0;
  param_1[0x40] = 0;
  param_1[0x3b] = 0;
  param_1[0x3a] = 0;
  param_1[0x3d] = 0;
  param_1[0x3c] = 0;
  param_1[0x37] = 0;
  param_1[0x36] = 0;
  param_1[0x39] = 0;
  param_1[0x38] = 0;
  param_1[0x33] = 0;
  param_1[0x32] = 0;
  param_1[0x35] = 0;
  param_1[0x34] = 0;
  param_1[0x31] = 0;
  param_1[0x30] = 0;
  *(undefined4 *)(param_1 + 0x5b) = 0x3f800000;
  param_1[0x5d] = 0;
  param_1[0x5c] = 0;
  param_1[0x5f] = 0;
  param_1[0x5e] = 0;
  *(undefined4 *)(param_1 + 0x60) = 0x3f800000;
  lVar8 = __Znwm(0x10);
  FUN_000404d0();
  param_1[0x61] = lVar8;
  lVar8 = __Znwm(1);
  param_1[0x62] = lVar8;
  param_1[100] = 0;
  param_1[99] = 0;
  param_1[0x66] = 0;
  param_1[0x65] = 0;
  param_1[0x68] = 0;
  param_1[0x67] = 0;
  param_1[0x6a] = 0;
  param_1[0x69] = 0;
  param_1[0x6c] = 0;
  param_1[0x6b] = 0;
  param_1[0x6e] = 0;
  param_1[0x6d] = 0;
  param_1[0x70] = 0;
  param_1[0x6f] = 0;
  param_1[0x72] = 0;
  param_1[0x71] = 0;
  param_1[0x74] = 0;
  param_1[0x73] = 0;
  param_1[0x76] = 0;
  param_1[0x75] = 0;
  FUN_0006a3dc(param_1 + 0x77);
  param_1[0x82] = 0;
  param_1[0x81] = 0;
  param_1[0x84] = 0;
  param_1[0x83] = 0;
  param_1[0x80] = 0;
  param_1[0x7f] = 0;
  *(undefined4 *)(param_1 + 0x85) = 0x3f800000;
  param_1[0x87] = 0;
  param_1[0x86] = 0;
  param_1[0x89] = 0;
  param_1[0x88] = 0;
  *(undefined4 *)(param_1 + 0x8a) = 0x3f800000;
  param_1[0x8c] = 0;
  param_1[0x8b] = 0;
  param_1[0x8e] = 0;
  param_1[0x8d] = 0;
  *(undefined4 *)(param_1 + 0x8f) = 0x3f800000;
  *(undefined2 *)(param_1 + 0x90) = 0;
  *(undefined4 *)((long)param_1 + 0x484) = 2;
  param_1[0x92] = 0;
  param_1[0x91] = 0;
  lVar8 = param_1[3];
  uVar9 = FUN_04a177a8();
  FUN_0456f23c(lVar8,uVar9);
  lVar8 = param_1[5];
  uVar9 = FUN_04a0d4d4();
  FUN_013a6570(lVar8,uVar9);
  FUN_0454554c(param_1 + 0x57,param_2,param_2 + 0x18);
  *(undefined1 *)(param_1 + 7) = 1;
  (**(code **)(*param_1 + 0x28))(&local_190,param_1);
  FUN_04535304(local_190,param_2);
  plVar17 = plStack_188;
  if (plStack_188 != (long *)0x0) {
    LOAcquire();
    lVar8 = plStack_188[1];
    plStack_188[1] = lVar8 + -1;
    LORelease();
    if (lVar8 == 0) {
      (**(code **)(*plStack_188 + 0x10))(plStack_188);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar17);
    }
  }
  param_1[8] = *(long *)(param_2 + 0x18);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 0xc,param_2 + 0x20);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_1 + 9,param_2);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 0xf,param_2 + 0xe8);
  (**(code **)(*param_1 + 0x28))(&local_190,param_1);
  lVar8 = FUN_04536938(local_190,&DAT_0a455e50,0);
  if (plStack_188 != (long *)0x0) {
    LOAcquire();
    lVar4 = plStack_188[1];
    plStack_188[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*plStack_188 + 0x10))(plStack_188);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plStack_188);
    }
  }
  param_1[0x23] = lVar8;
  FUN_0454e014(&local_190,param_1);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 0x24,&local_190);
  if ((long)local_180 < 0) {
    __ZdlPvm(local_190,local_180 & 0x7fffffffffffffff);
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 0x30,param_2 + 0x38);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 0x39,param_2 + 0x50);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 0x3c,param_2 + 0x68);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 0x3f,param_2 + 0x80);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 0x36,param_2 + 0x100);
  iVar5 = thunk_FUN_05e1d97c(2);
  if (iVar5 != 0) {
    FUN_0488143c(local_218);
    pppppppuVar12 = local_218[0];
    if (-1 < cStack_201) {
      pppppppuVar12 = local_218;
    }
    if ((DAT_0a455f21 & 1) == 0) {
      uRam000000000a455f18 = _UNK_089ffce8;
      _DAT_0a455f10 = _DAT_089ffce0;
      DAT_0a455f20 = 0;
      DAT_0a455f21 = 1;
    }
    if ((DAT_0a455f44 & 1) == 0) {
      uRam000000000a455f38 = _UNK_089ffcf8;
      _DAT_0a455f30 = _DAT_089ffcf0;
      DAT_0a455f40 = (undefined4)DAT_084b03a8;
      DAT_0a455f44 = 1;
    }
    FUN_05e1d050(&local_190,2,pppppppuVar12,&DAT_0a455f10,&DAT_0a455f30,0x49,0,0);
    uVar10 = FUN_00033f98(param_1 + 0x36);
    local_1e0 = (undefined8 *******)&local_1d8;
    if ((DAT_0a4564b0 & 1) == 0) {
      uVar16 = 0;
      do {
        uVar49 = *(undefined4 *)((long)&DAT_08a00aab + uVar16);
        uVar2 = CONCAT12((char)((uint)uVar49 >> 8),(short)uVar49) & 0xff00ff;
        uVar50 = *(undefined4 *)((long)&DAT_08a00a97 + uVar16 % 0x14);
        *(uint *)((long)&DAT_0a456468 + uVar16) =
             CONCAT13((char)((uint)uVar49 >> 0x18) + 0x8aU ^ (byte)((uint)uVar50 >> 0x18),
                      CONCAT12((char)((uint)uVar49 >> 0x10) + 0x8aU ^ (byte)((uint)uVar50 >> 0x10),
                               CONCAT11((char)(uVar2 >> 0x10) + 0x8aU ^ (byte)((uint)uVar50 >> 8),
                                        (char)uVar2 + 0x8aU ^ (byte)uVar50)));
        uVar16 = uVar16 + 4;
      } while (uVar16 != 0x48);
      DAT_0a4564b0 = 1;
    }
    lVar8 = 0;
    do {
      lVar4 = lVar8;
      uVar6 = (uint)uVar10;
      *(undefined1 *)((long)&local_1d8 + lVar4) =
           *(undefined1 *)
            ((long)&DAT_0a456468 + (ulong)(uVar6 + (int)((uVar10 & 0xffffffff) / 10) * -10 + 0x23));
      uVar10 = (uVar10 & 0xffffffff) / 10;
      lVar8 = lVar4 + 1;
    } while (9 < uVar6);
    *(undefined1 *)((long)&local_1d8 + lVar4 + 1) = 0;
    if (8 < lVar4 + 8U) {
      puVar14 = (undefined1 *)((long)&local_1d8 + lVar4);
      puVar15 = (undefined1 *)((long)&local_1d8 + 1);
      do {
        uVar1 = *puVar14;
        *puVar14 = puVar15[-1];
        puVar15[-1] = uVar1;
        bVar3 = puVar15 < puVar14 + -1;
        puVar14 = puVar14 + -1;
        puVar15 = puVar15 + 1;
      } while (bVar3);
    }
    if ((DAT_0a455f53 & 1) == 0) {
      DAT_0a455f48 = DAT_089ffb48;
      DAT_0a455f50 = 0x5f25;
      DAT_0a455f52 = 0;
      DAT_0a455f53 = 1;
    }
    uStack_f0 = 0;
    plStack_f8 = (long *)0x0;
    local_100 = &local_1e0;
    uStack_e0 = 0;
    local_e8 = 0;
    uStack_d0 = 0;
    local_d8 = 0;
    uStack_c0 = 0;
    local_c8 = 0;
    uStack_b0 = 0;
    local_b8 = 0;
    uStack_a0 = 0;
    local_a8 = 0;
    uStack_90 = 0;
    local_98 = 0;
    local_88 = 0;
    FUN_05e1d31c(&local_190,&DAT_0a455f48,&local_100);
    thunk_FUN_05e1d0bc(&local_190);
    if (cStack_201 < '\0') {
      __ZdlPvm(local_218[0],CONCAT17(cStack_201,local_208) & 0x7fffffffffffffff);
    }
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 0x42,param_2 + 0x98);
  plVar17 = param_1 + 0x4b;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(plVar17,param_2 + 0xb0);
  if (*(char *)((long)param_1 + 0x26f) < '\0') {
    plVar17 = (long *)*plVar17;
  }
  uVar10 = *(ulong *)(param_2 + 0xb8);
  if (-1 < (char)*(byte *)(param_2 + 199)) {
    uVar10 = (ulong)*(byte *)(param_2 + 199);
  }
  plStack_188 = (long *)_UNK_089ffd08;
  local_190 = _DAT_089ffd00;
  local_178 = _UNK_089ffd18;
  local_180 = _DAT_089ffd10;
  if (uVar10 != 0) {
    if (uVar10 - 0x21 < 0xffffffffffffffe7) {
      uVar16 = 0;
    }
    else {
      bVar21 = (byte)((ulong)_DAT_089ffd00 >> 8);
      bVar25 = (byte)((ulong)_DAT_089ffd00 >> 0x10);
      bVar29 = (byte)((ulong)_DAT_089ffd00 >> 0x18);
      bVar33 = (byte)((ulong)_DAT_089ffd00 >> 0x20);
      bVar37 = (byte)((ulong)_DAT_089ffd00 >> 0x28);
      bVar41 = (byte)((ulong)_DAT_089ffd00 >> 0x30);
      bVar45 = (byte)((ulong)_DAT_089ffd00 >> 0x38);
      bVar18 = (byte)_UNK_089ffd08;
      bVar22 = (byte)(_UNK_089ffd08 >> 8);
      bVar26 = (byte)(_UNK_089ffd08 >> 0x10);
      bVar30 = (byte)(_UNK_089ffd08 >> 0x18);
      bVar34 = (byte)(_UNK_089ffd08 >> 0x20);
      bVar38 = (byte)(_UNK_089ffd08 >> 0x28);
      bVar42 = (byte)(_UNK_089ffd08 >> 0x30);
      bVar46 = (byte)(_UNK_089ffd08 >> 0x38);
      bVar19 = (byte)_DAT_089ffd10;
      bVar23 = (byte)((ulong)_DAT_089ffd10 >> 8);
      bVar27 = (byte)((ulong)_DAT_089ffd10 >> 0x10);
      bVar31 = (byte)((ulong)_DAT_089ffd10 >> 0x18);
      bVar35 = (byte)((ulong)_DAT_089ffd10 >> 0x20);
      bVar39 = (byte)((ulong)_DAT_089ffd10 >> 0x28);
      bVar43 = (byte)((ulong)_DAT_089ffd10 >> 0x30);
      bVar47 = (byte)((ulong)_DAT_089ffd10 >> 0x38);
      bVar20 = (byte)_UNK_089ffd18;
      bVar24 = (byte)((ulong)_UNK_089ffd18 >> 8);
      bVar28 = (byte)((ulong)_UNK_089ffd18 >> 0x10);
      bVar32 = (byte)((ulong)_UNK_089ffd18 >> 0x18);
      bVar36 = (byte)((ulong)_UNK_089ffd18 >> 0x20);
      bVar40 = (byte)((ulong)_UNK_089ffd18 >> 0x28);
      bVar44 = (byte)((ulong)_UNK_089ffd18 >> 0x30);
      bVar48 = (byte)((ulong)_UNK_089ffd18 >> 0x38);
      if (0x3f < uVar10) {
        plVar17 = plVar17 + 4;
        do {
          lVar4 = plVar17[-3];
          lVar8 = plVar17[-4];
          lVar52 = plVar17[-1];
          lVar51 = plVar17[-2];
          lVar54 = plVar17[1];
          lVar53 = *plVar17;
          lVar56 = plVar17[3];
          lVar55 = plVar17[2];
          plVar17[-3] = CONCAT17((byte)((ulong)lVar4 >> 0x38) ^ bVar46,
                                 CONCAT16((byte)((ulong)lVar4 >> 0x30) ^ bVar42,
                                          CONCAT15((byte)((ulong)lVar4 >> 0x28) ^ bVar38,
                                                   CONCAT14((byte)((ulong)lVar4 >> 0x20) ^ bVar34,
                                                            CONCAT13((byte)((ulong)lVar4 >> 0x18) ^
                                                                     bVar30,CONCAT12((byte)((ulong)
                                                  lVar4 >> 0x10) ^ bVar26,
                                                  CONCAT11((byte)((ulong)lVar4 >> 8) ^ bVar22,
                                                           (byte)lVar4 ^ bVar18)))))));
          plVar17[-4] = CONCAT17((byte)((ulong)lVar8 >> 0x38) ^ bVar45,
                                 CONCAT16((byte)((ulong)lVar8 >> 0x30) ^ bVar41,
                                          CONCAT15((byte)((ulong)lVar8 >> 0x28) ^ bVar37,
                                                   CONCAT14((byte)((ulong)lVar8 >> 0x20) ^ bVar33,
                                                            CONCAT13((byte)((ulong)lVar8 >> 0x18) ^
                                                                     bVar29,CONCAT12((byte)((ulong)
                                                  lVar8 >> 0x10) ^ bVar25,
                                                  CONCAT11((byte)((ulong)lVar8 >> 8) ^ bVar21,
                                                           (byte)lVar8 ^ (byte)_DAT_089ffd00)))))));
          plVar17[-1] = CONCAT17((byte)((ulong)lVar52 >> 0x38) ^ bVar48,
                                 CONCAT16((byte)((ulong)lVar52 >> 0x30) ^ bVar44,
                                          CONCAT15((byte)((ulong)lVar52 >> 0x28) ^ bVar40,
                                                   CONCAT14((byte)((ulong)lVar52 >> 0x20) ^ bVar36,
                                                            CONCAT13((byte)((ulong)lVar52 >> 0x18) ^
                                                                     bVar32,CONCAT12((byte)((ulong)
                                                  lVar52 >> 0x10) ^ bVar28,
                                                  CONCAT11((byte)((ulong)lVar52 >> 8) ^ bVar24,
                                                           (byte)lVar52 ^ bVar20)))))));
          plVar17[-2] = CONCAT17((byte)((ulong)lVar51 >> 0x38) ^ bVar47,
                                 CONCAT16((byte)((ulong)lVar51 >> 0x30) ^ bVar43,
                                          CONCAT15((byte)((ulong)lVar51 >> 0x28) ^ bVar39,
                                                   CONCAT14((byte)((ulong)lVar51 >> 0x20) ^ bVar35,
                                                            CONCAT13((byte)((ulong)lVar51 >> 0x18) ^
                                                                     bVar31,CONCAT12((byte)((ulong)
                                                  lVar51 >> 0x10) ^ bVar27,
                                                  CONCAT11((byte)((ulong)lVar51 >> 8) ^ bVar23,
                                                           (byte)lVar51 ^ bVar19)))))));
          plVar17[1] = CONCAT17((byte)((ulong)lVar54 >> 0x38) ^ (byte)((ulong)uStack_168 >> 0x38),
                                CONCAT16((byte)((ulong)lVar54 >> 0x30) ^
                                         (byte)((ulong)uStack_168 >> 0x30),
                                         CONCAT15((byte)((ulong)lVar54 >> 0x28) ^
                                                  (byte)((ulong)uStack_168 >> 0x28),
                                                  CONCAT14((byte)((ulong)lVar54 >> 0x20) ^
                                                           (byte)((ulong)uStack_168 >> 0x20),
                                                           CONCAT13((byte)((ulong)lVar54 >> 0x18) ^
                                                                    (byte)((ulong)uStack_168 >> 0x18
                                                                          ),CONCAT12((byte)((ulong)
                                                  lVar54 >> 0x10) ^
                                                  (byte)((ulong)uStack_168 >> 0x10),
                                                  CONCAT11((byte)((ulong)lVar54 >> 8) ^
                                                           (byte)((ulong)uStack_168 >> 8),
                                                           (byte)lVar54 ^ (byte)uStack_168)))))));
          *plVar17 = CONCAT17((byte)((ulong)lVar53 >> 0x38) ^ (byte)((ulong)local_170 >> 0x38),
                              CONCAT16((byte)((ulong)lVar53 >> 0x30) ^
                                       (byte)((ulong)local_170 >> 0x30),
                                       CONCAT15((byte)((ulong)lVar53 >> 0x28) ^
                                                (byte)((ulong)local_170 >> 0x28),
                                                CONCAT14((byte)((ulong)lVar53 >> 0x20) ^
                                                         (byte)((ulong)local_170 >> 0x20),
                                                         CONCAT13((byte)((ulong)lVar53 >> 0x18) ^
                                                                  (byte)((ulong)local_170 >> 0x18),
                                                                  CONCAT12((byte)((ulong)lVar53 >>
                                                                                 0x10) ^
                                                                           (byte)((ulong)local_170
                                                                                 >> 0x10),
                                                                           CONCAT11((byte)((ulong)
                                                  lVar53 >> 8) ^ (byte)((ulong)local_170 >> 8),
                                                  (byte)lVar53 ^ (byte)local_170)))))));
          plVar17[3] = CONCAT17((byte)((ulong)lVar56 >> 0x38) ^ (byte)((ulong)uStack_158 >> 0x38),
                                CONCAT16((byte)((ulong)lVar56 >> 0x30) ^
                                         (byte)((ulong)uStack_158 >> 0x30),
                                         CONCAT15((byte)((ulong)lVar56 >> 0x28) ^
                                                  (byte)((ulong)uStack_158 >> 0x28),
                                                  CONCAT14((byte)((ulong)lVar56 >> 0x20) ^
                                                           (byte)((ulong)uStack_158 >> 0x20),
                                                           CONCAT13((byte)((ulong)lVar56 >> 0x18) ^
                                                                    (byte)((ulong)uStack_158 >> 0x18
                                                                          ),CONCAT12((byte)((ulong)
                                                  lVar56 >> 0x10) ^
                                                  (byte)((ulong)uStack_158 >> 0x10),
                                                  CONCAT11((byte)((ulong)lVar56 >> 8) ^
                                                           (byte)((ulong)uStack_158 >> 8),
                                                           (byte)lVar56 ^ (byte)uStack_158)))))));
          plVar17[2] = CONCAT17((byte)((ulong)lVar55 >> 0x38) ^ (byte)((ulong)uStack_160 >> 0x38),
                                CONCAT16((byte)((ulong)lVar55 >> 0x30) ^
                                         (byte)((ulong)uStack_160 >> 0x30),
                                         CONCAT15((byte)((ulong)lVar55 >> 0x28) ^
                                                  (byte)((ulong)uStack_160 >> 0x28),
                                                  CONCAT14((byte)((ulong)lVar55 >> 0x20) ^
                                                           (byte)((ulong)uStack_160 >> 0x20),
                                                           CONCAT13((byte)((ulong)lVar55 >> 0x18) ^
                                                                    (byte)((ulong)uStack_160 >> 0x18
                                                                          ),CONCAT12((byte)((ulong)
                                                  lVar55 >> 0x10) ^
                                                  (byte)((ulong)uStack_160 >> 0x10),
                                                  CONCAT11((byte)((ulong)lVar55 >> 8) ^
                                                           (byte)((ulong)uStack_160 >> 8),
                                                           (byte)lVar55 ^ (byte)uStack_160)))))));
          plVar17 = plVar17 + 8;
        } while( true );
      }
      uVar16 = uVar10 & 0x38;
      lVar8 = *plVar17;
      *plVar17 = CONCAT17((byte)((ulong)lVar8 >> 0x38) ^ bVar45,
                          CONCAT16((byte)((ulong)lVar8 >> 0x30) ^ bVar41,
                                   CONCAT15((byte)((ulong)lVar8 >> 0x28) ^ bVar37,
                                            CONCAT14((byte)((ulong)lVar8 >> 0x20) ^ bVar33,
                                                     CONCAT13((byte)((ulong)lVar8 >> 0x18) ^ bVar29,
                                                              CONCAT12((byte)((ulong)lVar8 >> 0x10)
                                                                       ^ bVar25,CONCAT11((byte)((
                                                  ulong)lVar8 >> 8) ^ bVar21,
                                                  (byte)lVar8 ^ (byte)_DAT_089ffd00)))))));
      if (uVar16 != 8) {
        lVar8 = plVar17[1];
        plVar17[1] = CONCAT17((byte)((ulong)lVar8 >> 0x38) ^ bVar46,
                              CONCAT16((byte)((ulong)lVar8 >> 0x30) ^ bVar42,
                                       CONCAT15((byte)((ulong)lVar8 >> 0x28) ^ bVar38,
                                                CONCAT14((byte)((ulong)lVar8 >> 0x20) ^ bVar34,
                                                         CONCAT13((byte)((ulong)lVar8 >> 0x18) ^
                                                                  bVar30,CONCAT12((byte)((ulong)
                                                  lVar8 >> 0x10) ^ bVar26,
                                                  CONCAT11((byte)((ulong)lVar8 >> 8) ^ bVar22,
                                                           (byte)lVar8 ^ bVar18)))))));
        if (uVar16 != 0x10) {
          lVar8 = plVar17[2];
          plVar17[2] = CONCAT17((byte)((ulong)lVar8 >> 0x38) ^ bVar47,
                                CONCAT16((byte)((ulong)lVar8 >> 0x30) ^ bVar43,
                                         CONCAT15((byte)((ulong)lVar8 >> 0x28) ^ bVar39,
                                                  CONCAT14((byte)((ulong)lVar8 >> 0x20) ^ bVar35,
                                                           CONCAT13((byte)((ulong)lVar8 >> 0x18) ^
                                                                    bVar31,CONCAT12((byte)((ulong)
                                                  lVar8 >> 0x10) ^ bVar27,
                                                  CONCAT11((byte)((ulong)lVar8 >> 8) ^ bVar23,
                                                           (byte)lVar8 ^ bVar19)))))));
          if (uVar16 != 0x18) {
            lVar8 = plVar17[3];
            plVar17[3] = CONCAT17((byte)((ulong)lVar8 >> 0x38) ^ bVar48,
                                  CONCAT16((byte)((ulong)lVar8 >> 0x30) ^ bVar44,
                                           CONCAT15((byte)((ulong)lVar8 >> 0x28) ^ bVar40,
                                                    CONCAT14((byte)((ulong)lVar8 >> 0x20) ^ bVar36,
                                                             CONCAT13((byte)((ulong)lVar8 >> 0x18) ^
                                                                      bVar32,CONCAT12((byte)((ulong)
                                                  lVar8 >> 0x10) ^ bVar28,
                                                  CONCAT11((byte)((ulong)lVar8 >> 8) ^ bVar24,
                                                           (byte)lVar8 ^ bVar20)))))));
          }
        }
      }
      if (uVar10 == uVar16) goto LAB_0454d184;
    }
    do {
      *(byte *)((long)plVar17 + uVar16) =
           *(byte *)((long)plVar17 + uVar16) ^ *(byte *)((long)&local_190 + (uVar16 & 0x1f));
      uVar16 = uVar16 + 1;
    } while (uVar10 != uVar16);
  }
LAB_0454d184:
  if (param_1 + 0x4e != (long *)(param_2 + 0x188)) {
    FUN_00496aac(param_1 + 0x4e,*(long *)(param_2 + 0x188),*(long *)(param_2 + 400),
                 (*(long *)(param_2 + 400) - *(long *)(param_2 + 0x188) >> 3) * -0x5555555555555555)
    ;
  }
  *(undefined2 *)(param_1 + 0x90) = *(undefined2 *)(param_2 + 0x1b8);
  uVar49 = 3;
  if ((*(uint *)(param_2 + 0xe0) & 1) != 0) {
    uVar49 = 1;
  }
  uVar50 = 2;
  if (*(char *)(param_2 + 0x180) == '\0') {
    uVar50 = uVar49;
  }
  *(undefined4 *)((long)param_1 + 0x484) = uVar50;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 0x51,param_2 + 0x1c0);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 0x54,param_2 + 0x1d8);
  if ((DAT_0a455f7f & 1) == 0) {
    _DAT_0a455f54 = CONCAT44((int)DAT_084d8358,(int)DAT_084cd9d8);
    uRam000000000a455f5c = CONCAT44((int)DAT_084d8360,(int)DAT_084a2ea0);
    _DAT_0a455f64 = CONCAT44((int)DAT_08480b40,(int)DAT_08492e68);
    uRam000000000a455f6c = CONCAT44((int)DAT_08492248,(int)ram0x084804f0);
    DAT_0a455f74 = CONCAT44((int)DAT_089ffb50,(int)DAT_08658460);
    DAT_0a455f7c = 0x7965;
    DAT_0a455f7e = 0;
    DAT_0a455f7f = 1;
  }
  sVar11 = _strlen(&DAT_0a455f54);
  if (0x7ffffffffffffff7 < sVar11) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_190);
  }
  if (sVar11 < 0x17) {
    local_180 = CONCAT17((char)sVar11,(undefined7)local_180);
    pppppppuVar12 = &local_190;
    if (sVar11 != 0) goto LAB_0454d2f4;
  }
  else {
    uVar10 = 0x19;
    if ((sVar11 | 7) != 0x17) {
      uVar10 = (sVar11 | 7) + 1;
    }
    pppppppuVar12 = (undefined8 *******)__Znwm(uVar10);
    local_180 = uVar10 | 0x8000000000000000;
    local_190 = pppppppuVar12;
    plStack_188 = (long *)sVar11;
LAB_0454d2f4:
    _memcpy(pppppppuVar12,&DAT_0a455f54,sVar11);
  }
  *(undefined1 *)((long)pppppppuVar12 + sVar11) = 0;
  iVar5 = FUN_0471bb14(&local_190,0);
  if ((long)local_180 < 0) {
    __ZdlPvm(local_190,local_180 & 0x7fffffffffffffff);
  }
  if (iVar5 != 0) {
    iVar5 = thunk_FUN_05e1d97c(2);
    if (iVar5 != 0) {
      FUN_0488143c(&local_1e0);
      pppppppuVar12 = local_1e0;
      if (-1 < cStack_1c9) {
        pppppppuVar12 = &local_1e0;
      }
      if ((DAT_0a455f21 & 1) == 0) {
        uRam000000000a455f18 = _UNK_089ffce8;
        _DAT_0a455f10 = _DAT_089ffce0;
        DAT_0a455f20 = 0;
        DAT_0a455f21 = 1;
      }
      if ((DAT_0a455f44 & 1) == 0) {
        uRam000000000a455f38 = _UNK_089ffcf8;
        _DAT_0a455f30 = _DAT_089ffcf0;
        DAT_0a455f40 = (undefined4)DAT_084b03a8;
        DAT_0a455f44 = 1;
      }
      FUN_05e1d050(&local_190,2,pppppppuVar12,&DAT_0a455f10,&DAT_0a455f30,0x5d,0,0);
      if ((DAT_0a455f9d & 1) == 0) {
        _DAT_0a455f80 = CONCAT44((int)DAT_08486a50,(int)DAT_084df440);
        uRam000000000a455f88 = CONCAT44((int)DAT_0878b1d0,(int)DAT_089ffb58);
        DAT_0a455f90 = CONCAT44((int)DAT_08543ad8,(int)DAT_08487d10);
        DAT_0a455f98 = (undefined4)DAT_08487d68;
        DAT_0a455f9c = 0;
        DAT_0a455f9d = 1;
      }
      local_98 = 0;
      uStack_a0 = 0;
      local_88 = 0;
      uStack_90 = 0;
      local_b8 = 0;
      uStack_c0 = 0;
      local_a8 = 0;
      uStack_b0 = 0;
      local_d8 = 0;
      uStack_e0 = 0;
      local_c8 = 0;
      uStack_d0 = 0;
      plStack_f8 = (long *)0x0;
      local_100 = (undefined8 *******)0x0;
      local_e8 = 0;
      uStack_f0 = 0;
      FUN_05e1d31c(&local_190,&DAT_0a455f80,&local_100);
      thunk_FUN_05e1d0bc(&local_190);
      if (cStack_1c9 < '\0') {
        __ZdlPvm(local_1e0,CONCAT17(cStack_1c9,local_1d0) & 0x7fffffffffffffff);
      }
    }
    FUN_045436ec(&local_190,param_1 + 0x57,2);
    puVar7 = (undefined8 *)__Znwm(0xb8);
    puVar7[1] = 0;
    puVar7[2] = 0;
    *puVar7 = &PTR_FUN_09e878d0;
    lVar8 = thunk_FUN_03b07dcc(puVar7 + 3,&local_190);
    param_1[0x73] = lVar8;
    plVar17 = (long *)param_1[0x74];
    param_1[0x74] = (long)puVar7;
    if (plVar17 != (long *)0x0) {
      LOAcquire();
      lVar8 = plVar17[1];
      plVar17[1] = lVar8 + -1;
      LORelease();
      if (lVar8 == 0) {
        (**(code **)(*plVar17 + 0x10))(plVar17);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar17);
      }
    }
    FUN_0002b440(&local_190);
  }
  uVar10 = *(ulong *)(param_2 + 0x1a8);
  if (-1 < (char)*(byte *)(param_2 + 0x1b7)) {
    uVar10 = (ulong)*(byte *)(param_2 + 0x1b7);
  }
  if (uVar10 != 0) {
    FUN_04669774();
    FUN_0466ad74(&local_100);
    pppppppuVar12 = local_100;
    if ((DAT_0a455f44 & 1) == 0) {
      uRam000000000a455f38 = _UNK_089ffcf8;
      _DAT_0a455f30 = _DAT_089ffcf0;
      DAT_0a455f40 = (undefined4)DAT_084b03a8;
      DAT_0a455f44 = 1;
    }
    if ((DAT_0a455fff & 1) == 0) {
      uVar10 = 0;
      do {
        uVar49 = *(undefined4 *)((long)&DAT_08a00242 + uVar10);
        uVar2 = CONCAT12((char)((uint)uVar49 >> 8),(short)uVar49) & 0xff00ff;
        uVar50 = *(undefined4 *)((long)&DAT_08a0022e + uVar10 % 0x14);
        *(uint *)((long)&DAT_0a455f9e + uVar10) =
             CONCAT13((char)((uint)uVar49 >> 0x18) + 0x8aU ^ (byte)((uint)uVar50 >> 0x18),
                      CONCAT12((char)((uint)uVar49 >> 0x10) + 0x8aU ^ (byte)((uint)uVar50 >> 0x10),
                               CONCAT11((char)(uVar2 >> 0x10) + 0x8aU ^ (byte)((uint)uVar50 >> 8),
                                        (char)uVar2 + 0x8aU ^ (byte)uVar50)));
        uVar10 = uVar10 + 4;
      } while (uVar10 != 0x60);
      DAT_0a455ffe = 0;
      DAT_0a455fff = 1;
    }
    FUN_0003bb6c(&local_190,&DAT_0a455f30,&DAT_0a455f9e,99);
    FUN_04556dc0(auStack_420,param_2);
    local_1e8 = (long *)0x0;
    local_230 = param_1;
    plVar17 = (long *)__Znwm(0x200);
    *plVar17 = (long)&PTR_FUN_09e87920;
    FUN_04556dc0(plVar17 + 1,auStack_420);
    plVar17[0x3f] = (long)local_230;
    local_1e8 = plVar17;
    FUN_0453bbe0(auStack_228,pppppppuVar12,&local_190,alStack_200,1);
    if (local_220 != (long *)0x0) {
      LOAcquire();
      lVar8 = local_220[1];
      local_220[1] = lVar8 + -1;
      LORelease();
      if (lVar8 == 0) {
        (**(code **)(*local_220 + 0x10))(local_220);
        __ZNSt3__119__shared_weak_count14__release_weakEv(local_220);
      }
    }
    if (local_1e8 == alStack_200) {
      pcVar13 = *(code **)(*local_1e8 + 0x20);
LAB_0454d73c:
      (*pcVar13)();
    }
    else if (local_1e8 != (long *)0x0) {
      pcVar13 = *(code **)(*local_1e8 + 0x28);
      goto LAB_0454d73c;
    }
    FUN_02feb8bc(auStack_420);
    plVar17 = plStack_f8;
    if (plStack_f8 != (long *)0x0) {
      LOAcquire();
      lVar8 = plStack_f8[1];
      plStack_f8[1] = lVar8 + -1;
      LORelease();
      if (lVar8 == 0) {
        (**(code **)(*plStack_f8 + 0x10))(plStack_f8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar17);
      }
    }
  }
  lVar8 = FUN_047471b0();
  param_1[0x91] = lVar8;
  local_430 = &SUB_aaaaaaaaaaaaaaaa;
  local_428 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  (**(code **)(*param_1 + 0x28))(&local_430,param_1);
  puVar14 = local_430;
  if (local_430 == (undefined1 *)0x0) goto LAB_0454db20;
  if ((DAT_0a456015 & 1) == 0) {
    _DAT_0a456000 = CONCAT44((int)DAT_084e3210,(int)DAT_085b4630);
    uRam000000000a456008 = CONCAT44((int)DAT_089ffb60,(int)ram0x084f7f78);
    DAT_0a456010 = (undefined4)DAT_08495970;
    DAT_0a456014 = 0;
    DAT_0a456015 = 1;
  }
  sVar11 = _strlen(&DAT_0a456000);
  if (0x7ffffffffffffff7 < sVar11) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_190);
  }
  if (sVar11 < 0x17) {
    local_180 = CONCAT17((char)sVar11,(undefined7)local_180);
    pppppppuVar12 = &local_190;
    if (sVar11 != 0) goto LAB_0454d85c;
  }
  else {
    uVar10 = 0x19;
    if ((sVar11 | 7) != 0x17) {
      uVar10 = (sVar11 | 7) + 1;
    }
    pppppppuVar12 = (undefined8 *******)__Znwm(uVar10);
    local_180 = uVar10 | 0x8000000000000000;
    local_190 = pppppppuVar12;
    plStack_188 = (long *)sVar11;
LAB_0454d85c:
    _memcpy(pppppppuVar12,&DAT_0a456000,sVar11);
  }
  *(undefined1 *)((long)pppppppuVar12 + sVar11) = 0;
  lVar8 = FUN_04536938(puVar14,&local_190,0);
  param_1[0x92] = lVar8;
  if ((long)local_180 < 0) {
    __ZdlPvm(local_190,local_180 & 0x7fffffffffffffff);
  }
  iVar5 = thunk_FUN_05e1d97c(2);
  if (iVar5 != 0) {
    FUN_0488143c(local_218);
    pppppppuVar12 = local_218[0];
    if (-1 < cStack_201) {
      pppppppuVar12 = local_218;
    }
    if ((DAT_0a455f21 & 1) == 0) {
      uRam000000000a455f18 = _UNK_089ffce8;
      _DAT_0a455f10 = _DAT_089ffce0;
      DAT_0a455f20 = 0;
      DAT_0a455f21 = 1;
    }
    if ((DAT_0a455f44 & 1) == 0) {
      uRam000000000a455f38 = _UNK_089ffcf8;
      _DAT_0a455f30 = _DAT_089ffcf0;
      DAT_0a455f40 = (undefined4)DAT_084b03a8;
      DAT_0a455f44 = 1;
    }
    FUN_05e1d050(&local_190,2,pppppppuVar12,&DAT_0a455f10,&DAT_0a455f30,0x6d,0,0);
    uVar10 = param_1[0x92];
    local_1e0 = (undefined8 *******)&local_1d8;
    if ((DAT_0a4564b0 & 1) == 0) {
      uVar16 = 0;
      do {
        uVar49 = *(undefined4 *)((long)&DAT_08a00aab + uVar16);
        uVar2 = CONCAT12((char)((uint)uVar49 >> 8),(short)uVar49) & 0xff00ff;
        uVar50 = *(undefined4 *)((long)&DAT_08a00a97 + uVar16 % 0x14);
        *(uint *)((long)&DAT_0a456468 + uVar16) =
             CONCAT13((char)((uint)uVar49 >> 0x18) + 0x8aU ^ (byte)((uint)uVar50 >> 0x18),
                      CONCAT12((char)((uint)uVar49 >> 0x10) + 0x8aU ^ (byte)((uint)uVar50 >> 0x10),
                               CONCAT11((char)(uVar2 >> 0x10) + 0x8aU ^ (byte)((uint)uVar50 >> 8),
                                        (char)uVar2 + 0x8aU ^ (byte)uVar50)));
        uVar16 = uVar16 + 4;
      } while (uVar16 != 0x48);
      DAT_0a4564b0 = 1;
    }
    lVar8 = 0;
    do {
      lVar4 = lVar8;
      *(undefined1 *)((long)&local_1d8 + lVar4) = *(undefined1 *)(uVar10 % 10 + 0xa45648b);
      bVar3 = 9 < uVar10;
      uVar10 = uVar10 / 10;
      lVar8 = lVar4 + 1;
    } while (bVar3);
    *(undefined1 *)((long)&local_1d8 + lVar4 + 1) = 0;
    if (8 < lVar4 + 8U) {
      puVar14 = (undefined1 *)((long)&local_1d8 + lVar4);
      puVar15 = (undefined1 *)((long)&local_1d8 + 1);
      do {
        uVar1 = *puVar14;
        *puVar14 = puVar15[-1];
        puVar15[-1] = uVar1;
        bVar3 = puVar15 < puVar14 + -1;
        puVar14 = puVar14 + -1;
        puVar15 = puVar15 + 1;
      } while (bVar3);
    }
    if ((DAT_0a456030 & 1) == 0) {
      _DAT_0a456018 = CONCAT44((int)DAT_0853b3e8,(int)DAT_0848be60);
      uRam000000000a456020 = CONCAT44((int)DAT_08815a30,(int)DAT_08492288);
      DAT_0a456028 = CONCAT44((int)ram0x084c9468,(int)DAT_084aeac0);
      DAT_0a456030 = 1;
    }
    uStack_f0 = 0;
    plStack_f8 = (long *)0x0;
    local_100 = &local_1e0;
    uStack_e0 = 0;
    local_e8 = 0;
    uStack_d0 = 0;
    local_d8 = 0;
    uStack_c0 = 0;
    local_c8 = 0;
    uStack_b0 = 0;
    local_b8 = 0;
    uStack_a0 = 0;
    local_a8 = 0;
    uStack_90 = 0;
    local_98 = 0;
    local_88 = 0;
    FUN_05e1d31c(&local_190,&DAT_0a456018,&local_100);
    thunk_FUN_05e1d0bc(&local_190);
    if (cStack_201 < '\0') {
      __ZdlPvm(local_218[0],CONCAT17(cStack_201,local_208) & 0x7fffffffffffffff);
    }
  }
LAB_0454db20:
  plVar17 = local_428;
  if (local_428 != (long *)0x0) {
    LOAcquire();
    lVar8 = local_428[1];
    local_428[1] = lVar8 + -1;
    LORelease();
    if (lVar8 == 0) {
      (**(code **)(*local_428 + 0x10))(local_428);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar17);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_78) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return param_1;
}


