// Ghidra inferred pseudocode; requested=0x2686020
// entry=02686020 end=0268646f

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_02686020(undefined8 param_1,long *param_2,long *param_3)

{
  bool bVar1;
  long *plVar2;
  undefined8 ******ppppppuVar3;
  undefined1 uVar4;
  undefined4 uVar5;
  uint3 uVar6;
  uint uVar7;
  undefined1 **ppuVar8;
  long lVar9;
  undefined1 *puVar10;
  int iVar11;
  undefined1 *puVar12;
  undefined1 *puVar13;
  ulong uVar14;
  long lVar15;
  ulong uVar16;
  undefined4 uVar17;
  undefined8 *****local_248 [2];
  undefined7 local_238;
  char cStack_231;
  undefined8 local_230;
  long *local_228;
  undefined1 *local_1a0;
  undefined1 *puStack_198;
  undefined1 *puStack_190;
  undefined1 *puStack_188;
  undefined1 *local_180;
  undefined1 *puStack_178;
  undefined1 *puStack_170;
  undefined1 *puStack_168;
  undefined1 *local_158;
  undefined1 local_150 [72];
  long local_108;
  undefined1 local_100;
  undefined7 uStack_ff;
  long *local_b8;
  undefined1 **local_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  undefined8 local_78;
  undefined8 uStack_70;
  undefined8 local_68;
  undefined8 uStack_60;
  undefined8 local_58;
  undefined8 uStack_50;
  undefined8 local_48;
  undefined8 uStack_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  puStack_178 = &SUB_aaaaaaaaaaaaaaaa;
  local_180 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_168 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_170 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_198 = &SUB_aaaaaaaaaaaaaaaa;
  local_1a0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_188 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_190 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0559f2a0(&local_1a0);
  plVar2 = (long *)*param_3;
  uVar7 = *(uint *)(param_3 + 1);
  if (-1 < (char)*(byte *)((long)param_3 + 0x17)) {
    plVar2 = param_3;
    uVar7 = (uint)*(byte *)((long)param_3 + 0x17);
  }
  iVar11 = FUN_05ab3ab8(&local_1a0,plVar2,uVar7);
  if (iVar11 == 0) {
    iVar11 = thunk_FUN_05e1d97c(4);
    if (iVar11 != 0) {
      FUN_0488143c(local_248);
      ppppppuVar3 = (undefined8 ******)local_248[0];
      if (-1 < cStack_231) {
        ppppppuVar3 = local_248;
      }
      if ((DAT_0a391bc3 & 1) == 0) {
        uRam000000000a391bb8._0_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x18];
        uRam000000000a391bb8._1_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x19];
        uRam000000000a391bb8._2_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1a];
        uRam000000000a391bb8._3_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1b];
        uRam000000000a391bb8._4_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1c];
        uRam000000000a391bb8._5_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1d];
        uRam000000000a391bb8._6_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1e];
        uRam000000000a391bb8._7_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x1f];
        DAT_0a391bb0 = s_ai_assisasst_talchatbot_manager__087e3420[0x10];
        DAT_0a391bb0_1._0_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x11];
        DAT_0a391bb0_1._1_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x12];
        DAT_0a391bb0_1._2_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x13];
        DAT_0a391bb0_1._3_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x14];
        DAT_0a391bb0_1._4_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x15];
        DAT_0a391bb0_1._5_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x16];
        DAT_0a391bb0_1._6_1_ = s_ai_assisasst_talchatbot_manager__087e3420[0x17];
        DAT_0a391bc0 = 0x6363;
        DAT_0a391bc2 = 0;
        DAT_0a391bc3 = 1;
      }
      if ((DAT_0a392ce5 & 1) == 0) {
        _DAT_0a392cd0 = CONCAT44((int)DAT_08500d68,(int)DAT_08502978);
        uRam000000000a392cd8 = CONCAT44((int)DAT_08482f20,(int)DAT_087e2fa8);
        DAT_0a392ce0 = (undefined4)DAT_08484c30;
        DAT_0a392ce4 = 0;
        DAT_0a392ce5 = 1;
      }
      FUN_05e1d050(&local_230,4,ppppppuVar3,&DAT_0a391bb0,&DAT_0a392cd0,0x88e,0,0);
      local_108 = *param_2;
      if (-1 < *(char *)((long)param_2 + 0x17)) {
        local_108 = (long)param_2;
      }
      local_100 = 0;
      uVar14 = param_3[1];
      if (-1 < (char)*(byte *)((long)param_3 + 0x17)) {
        uVar14 = (ulong)*(byte *)((long)param_3 + 0x17);
      }
      local_158 = local_150;
      if ((DAT_0a394c3a & 1) == 0) {
        uVar16 = 0;
        do {
          uVar17 = *(undefined4 *)((long)&DAT_087e9335 + uVar16);
          uVar6 = CONCAT12((char)((uint)uVar17 >> 8),(short)uVar17) & 0xff00ff;
          uVar5 = *(undefined4 *)((long)&DAT_087e9321 + uVar16 % 0x14);
          *(uint *)((long)&DAT_0a394bf2 + uVar16) =
               CONCAT13((char)((uint)uVar17 >> 0x18) + 0x69U ^ (byte)((uint)uVar5 >> 0x18),
                        CONCAT12((char)((uint)uVar17 >> 0x10) + 0x69U ^ (byte)((uint)uVar5 >> 0x10),
                                 CONCAT11((char)(uVar6 >> 0x10) + 0x69U ^ (byte)((uint)uVar5 >> 8),
                                          (char)uVar6 + 0x69U ^ (byte)uVar5)));
          uVar16 = uVar16 + 4;
        } while (uVar16 != 0x48);
        DAT_0a394c3a = 1;
      }
      lVar9 = 0;
      do {
        lVar15 = lVar9;
        local_150[lVar15] = (&DAT_0a394c15)[uVar14 % 10];
        bVar1 = 9 < uVar14;
        uVar14 = uVar14 / 10;
        lVar9 = lVar15 + 1;
      } while (bVar1);
      local_150[lVar15 + 1] = 0;
      if (8 < lVar15 + 8U) {
        puVar10 = local_150;
        puVar12 = local_150 + lVar15;
        do {
          puVar10 = puVar10 + 1;
          uVar4 = *puVar12;
          puVar13 = puVar12 + -1;
          *puVar12 = puVar10[-1];
          puVar10[-1] = uVar4;
          puVar12 = puVar13;
        } while (puVar10 < puVar13);
      }
      if ((DAT_0a392d2f & 1) == 0) {
        uVar14 = 0;
        do {
          uVar17 = *(undefined4 *)((long)&DAT_087e67a6 + uVar14);
          uVar6 = CONCAT12((char)((uint)uVar17 >> 8),(short)uVar17) & 0xff00ff;
          uVar5 = *(undefined4 *)((long)&DAT_087e6792 + uVar14 % 0x14);
          *(uint *)((long)&DAT_0a392ce6 + uVar14) =
               CONCAT13((char)((uint)uVar17 >> 0x18) + 0x8aU ^ (byte)((uint)uVar5 >> 0x18),
                        CONCAT12((char)((uint)uVar17 >> 0x10) + 0x8aU ^ (byte)((uint)uVar5 >> 0x10),
                                 CONCAT11((char)(uVar6 >> 0x10) + 0x8aU ^ (byte)((uint)uVar5 >> 8),
                                          (char)uVar6 + 0x8aU ^ (byte)uVar5)));
          uVar14 = uVar14 + 4;
        } while (uVar14 != 0x48);
        DAT_0a392d2e = 0;
        DAT_0a392d2f = 1;
      }
      local_b8 = &local_108;
      local_b0 = &local_158;
      uStack_a0 = 0;
      local_a8 = 0;
      uStack_90 = 0;
      local_98 = 0;
      uStack_80 = 0;
      local_88 = 0;
      uStack_70 = 0;
      local_78 = 0;
      uStack_60 = 0;
      local_68 = 0;
      uStack_50 = 0;
      local_58 = 0;
      uStack_40 = 0;
      local_48 = 0;
      FUN_05e1d31c(&local_230,&DAT_0a392ce6,&local_b8);
      thunk_FUN_05e1d0bc(&local_230);
      if (cStack_231 < '\0') {
        __ZdlPvm(local_248[0],CONCAT17(cStack_231,local_238) & 0x7fffffffffffffff);
      }
    }
  }
  else {
    FUN_0466aca8(&local_108);
    FUN_01205740(&local_b8,local_108);
    FUN_026870f0(&local_230,local_b8);
    FUN_02857ca4(local_230,param_2,&local_1a0);
    if (local_228 != (long *)0x0) {
      LOAcquire();
      lVar9 = local_228[1];
      local_228[1] = lVar9 + -1;
      LORelease();
      if (lVar9 == 0) {
        (**(code **)(*local_228 + 0x10))(local_228);
        __ZNSt3__119__shared_weak_count14__release_weakEv(local_228);
      }
    }
    ppuVar8 = local_b0;
    if (local_b0 != (undefined1 **)0x0) {
      LOAcquire();
      puVar10 = local_b0[1];
      local_b0[1] = puVar10 + -1;
      LORelease();
      if (puVar10 == (undefined1 *)0x0) {
        (**(code **)(*local_b0 + 0x10))(local_b0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(ppuVar8);
      }
    }
    plVar2 = (long *)CONCAT71(uStack_ff,local_100);
    if (plVar2 != (long *)0x0) {
      LOAcquire();
      lVar9 = plVar2[1];
      plVar2[1] = lVar9 + -1;
      LORelease();
      if (lVar9 == 0) {
        (**(code **)(*plVar2 + 0x10))(plVar2);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
      }
    }
  }
  FUN_055bebd4(&local_1a0);
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_38) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


