// Ghidra inferred pseudocode; requested=0x667a274
// entry=0667a274 end=0667a6d7

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 *
FUN_0667a274(undefined8 *param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
            long param_5)

{
  undefined8 *puVar1;
  long lVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  int iVar5;
  undefined8 ***pppuVar6;
  ulong uVar7;
  undefined8 uVar8;
  undefined8 **local_198;
  ulong uStack_190;
  undefined7 local_188;
  byte bStack_181;
  undefined8 local_c8;
  undefined1 *local_c0;
  undefined8 *puStack_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined4 uStack_98;
  undefined4 uStack_94;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined1 *local_80;
  undefined8 uStack_78;
  undefined1 *local_70;
  undefined4 uStack_68;
  undefined4 uStack_64;
  undefined8 local_60;
  undefined1 *puStack_58;
  undefined8 local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  *param_1 = 0;
  param_1[1] = 0;
  puVar1 = param_1 + 0x75;
  param_1[0x4e] = 0;
  param_1[0x4d] = 0;
  param_1[0x50] = 0;
  param_1[0x4f] = 0;
  *(undefined4 *)(param_1 + 0x51) = 0;
  param_1[0x73] = 0;
  param_1[0x72] = 0;
  param_1[0x75] = 0;
  param_1[0x74] = 0;
  param_1[0x77] = 0;
  param_1[0x76] = 0;
  *(undefined8 *)((long)param_1 + 0x3c4) = 0;
  *(undefined8 *)((long)param_1 + 0x3bc) = 0;
  *(undefined4 *)((long)param_1 + 0x3cc) = 0x32;
  param_1[0x7a] = 0;
  param_1[0x7c] = 0;
  param_1[0x7b] = 0;
  param_1[0x4a] = param_2;
  param_1[0x4c] = param_3;
  param_1[0x4b] = param_4;
  LOAcquire();
  LORelease();
  lVar2 = DAT_0a5265c8 + 1;
  DAT_0a5265c8 = DAT_0a5265c8 + 1;
  param_1[0x74] = lVar2;
  uVar7 = *(ulong *)(param_5 + 8);
  if (-1 < (char)*(byte *)(param_5 + 0x17)) {
    uVar7 = (ulong)*(byte *)(param_5 + 0x17);
  }
  if (uVar7 == 0) {
    if ((DAT_0a5180b3 & 1) == 0) {
      DAT_0a5180a8._0_1_ = s_coroutinCoAsync_087e2ce0[0];
      DAT_0a5180a8._1_1_ = s_coroutinCoAsync_087e2ce0[1];
      DAT_0a5180a8._2_1_ = s_coroutinCoAsync_087e2ce0[2];
      DAT_0a5180a8._3_1_ = s_coroutinCoAsync_087e2ce0[3];
      DAT_0a5180a8._4_1_ = s_coroutinCoAsync_087e2ce0[4];
      DAT_0a5180a8._5_1_ = s_coroutinCoAsync_087e2ce0[5];
      DAT_0a5180a8._6_1_ = s_coroutinCoAsync_087e2ce0[6];
      DAT_0a5180a8._7_1_ = s_coroutinCoAsync_087e2ce0[7];
      DAT_0a5180b0 = 0x5f65;
      DAT_0a5180b2 = 0;
      DAT_0a5180b3 = 1;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
              (puVar1,&DAT_0a5180a8);
    __ZNSt3__19to_stringEy(&local_198,param_1[0x74]);
    pppuVar6 = (undefined8 ***)local_198;
    if (-1 < (char)bStack_181) {
      uStack_190 = (ulong)bStack_181;
      pppuVar6 = &local_198;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
              (puVar1,pppuVar6,uStack_190);
    if ((char)bStack_181 < '\0') {
      __ZdlPvm(local_198,CONCAT17(bStack_181,local_188) & 0x7fffffffffffffff);
    }
  }
  else {
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar1,param_5);
  }
  if (-1 < *(int *)(param_5 + 0x30)) {
    *(int *)((long)param_1 + 0x3cc) = *(int *)(param_5 + 0x30);
  }
  _bzero(param_1 + 2,0x240);
  uVar8 = *(undefined8 *)(param_5 + 0x18);
  param_1[0x4e] = *(undefined8 *)(param_5 + 0x20);
  param_1[0x4d] = uVar8;
  param_1[0x50] = *(undefined8 *)(param_5 + 0x28);
  param_1[0x6f] = 0;
  param_1[0x6e] = 0;
  param_1[0x71] = 0;
  param_1[0x70] = 0;
  param_1[0x6b] = 0;
  param_1[0x6a] = 0;
  param_1[0x6d] = 0;
  param_1[0x6c] = 0;
  param_1[0x67] = 0;
  param_1[0x66] = 0;
  param_1[0x69] = 0;
  param_1[0x68] = 0;
  param_1[99] = 0;
  param_1[0x62] = 0;
  param_1[0x65] = 0;
  param_1[100] = 0;
  param_1[0x5f] = 0;
  param_1[0x5e] = 0;
  param_1[0x61] = 0;
  param_1[0x60] = 0;
  param_1[0x5b] = 0;
  param_1[0x5a] = 0;
  param_1[0x5d] = 0;
  param_1[0x5c] = 0;
  param_1[0x57] = 0;
  param_1[0x56] = 0;
  param_1[0x59] = 0;
  param_1[0x58] = 0;
  param_1[0x53] = 0;
  param_1[0x52] = 0;
  param_1[0x55] = 0;
  param_1[0x54] = 0;
  param_1[0x7d] = 0;
  *(undefined1 *)(param_1 + 0x7e) = 1;
  if (((DAT_0a517ac0 & 1) == 0) && (iVar5 = ___cxa_guard_acquire(&DAT_0a517ac0), iVar5 != 0)) {
    FUN_06676a4c(&DAT_0a5179d0);
    ___cxa_guard_release(&DAT_0a517ac0);
  }
  FUN_0667a760(&DAT_0a517a48,param_1[0x74],puVar1,0);
  iVar5 = FUN_0668dad0(1);
  if (iVar5 != 0) {
    if ((DAT_0a517add & 1) == 0) {
      DAT_0a517ad8 = (undefined4)ram0x08782918;
      DAT_0a517adc = 0;
      DAT_0a517add = 1;
    }
    if ((DAT_0a5180c2 & 1) == 0) {
      DAT_0a5180b8._0_1_ = s_coroutinCoAsync_087e2ce0[0];
      DAT_0a5180b8._1_1_ = s_coroutinCoAsync_087e2ce0[1];
      DAT_0a5180b8._2_1_ = s_coroutinCoAsync_087e2ce0[2];
      DAT_0a5180b8._3_1_ = s_coroutinCoAsync_087e2ce0[3];
      DAT_0a5180b8._4_1_ = s_coroutinCoAsync_087e2ce0[4];
      DAT_0a5180b8._5_1_ = s_coroutinCoAsync_087e2ce0[5];
      DAT_0a5180b8._6_1_ = s_coroutinCoAsync_087e2ce0[6];
      DAT_0a5180b8._7_1_ = s_coroutinCoAsync_087e2ce0[7];
      DAT_0a5180c0 = 0x65;
      DAT_0a5180c2 = 1;
    }
    if ((DAT_0a517aec & 1) == 0) {
      DAT_0a517ae0._0_1_ = s_co_core_resume_ie__i_09684bb0[0];
      DAT_0a517ae0._1_1_ = s_co_core_resume_ie__i_09684bb0[1];
      DAT_0a517ae0._2_1_ = s_co_core_resume_ie__i_09684bb0[2];
      DAT_0a517ae0._3_1_ = s_co_core_resume_ie__i_09684bb0[3];
      DAT_0a517ae0._4_1_ = s_co_core_resume_ie__i_09684bb0[4];
      DAT_0a517ae0._5_1_ = s_co_core_resume_ie__i_09684bb0[5];
      DAT_0a517ae0._6_1_ = s_co_core_resume_ie__i_09684bb0[6];
      DAT_0a517ae0._7_1_ = s_co_core_resume_ie__i_09684bb0[7];
      DAT_0a517ae8 = (undefined4)DAT_085722b0;
      DAT_0a517aec = 1;
    }
    FUN_0668db5c(&local_198,&DAT_0a517ad8,&DAT_0a5180b8,&DAT_0a517ae0,0x12900002800);
    if ((DAT_0a518122 & 1) == 0) {
      uVar7 = 0;
      do {
        uVar3 = *(undefined4 *)((long)&DAT_0968597a + uVar7);
        uVar4 = *(undefined4 *)((long)&DAT_09685966 + uVar7 % 0x14);
        *(uint *)((long)&DAT_0a5180c3 + uVar7) =
             CONCAT13((char)((uint)uVar3 >> 0x18) + 0x8aU ^ (byte)((uint)uVar4 >> 0x18),
                      CONCAT12((char)((uint)uVar3 >> 0x10) + 0x8aU ^ (byte)((uint)uVar4 >> 0x10),
                               CONCAT11((char)((uint)uVar3 >> 8) + 0x8aU ^ (byte)((uint)uVar4 >> 8),
                                        (char)uVar3 + 0x8aU ^ (byte)uVar4)));
        uVar7 = uVar7 + 4;
      } while (uVar7 != 0x5c);
      DAT_0a51811f = 0x7825;
      DAT_0a518121 = 0;
      DAT_0a518122 = 1;
    }
    pppuVar6 = (undefined8 ***)(local_198 + 0xd);
    if (*(char *)((long)local_198 + 0x7f) < '\0') {
      pppuVar6 = (undefined8 ***)*pppuVar6;
    }
    local_c8 = param_1[0x74];
    local_c0 = &DAT_aaaaaaaa0000000b;
    local_b0 = 0xaaaaaaaa00000010;
    puStack_b8 = (undefined8 *)param_1[0x75];
    if (-1 < *(char *)((long)param_1 + 0x3bf)) {
      puStack_b8 = puVar1;
    }
    uStack_a8 = param_1[0x50];
    local_90 = 0xaaaaaaaa00000006;
    local_a0 = 0xaaaaaaaa00000009;
    _uStack_98 = CONCAT44(0xaaaaaaaa,*(undefined4 *)((long)param_1 + 0x3cc));
    uStack_88 = param_1[0x4d];
    local_80 = &DAT_aaaaaaaa0000000f;
    uStack_78 = param_1[0x4e];
    local_70 = &DAT_aaaaaaaa0000000f;
    _uStack_68 = CONCAT44(0xaaaaaaaa,*(undefined4 *)(param_5 + 0x34));
    local_50 = 0xaaaaaaaa00000006;
    local_60 = 0xaaaaaaaa00000007;
    puStack_58 = &DAT_aaaaaaaa00000000;
    FUN_0668e1e4(local_198 + 7,&DAT_0a5180c3,pppuVar6,&local_c8,7);
    FUN_0668dbac();
    thunk_FUN_0668e878(&local_198);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return param_1;
}


