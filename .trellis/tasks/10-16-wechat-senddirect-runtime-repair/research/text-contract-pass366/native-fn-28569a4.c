// Ghidra inferred pseudocode; requested=0x28569a4
// entry=028569a4 end=028570ab

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_028569a4(long param_1,undefined8 ******param_2,ulong ******param_3,undefined8 *param_4,
                 undefined8 *param_5,int param_6,undefined8 *param_7)

{
  uint uVar1;
  ulong ******ppppppuVar2;
  undefined8 ******ppppppuVar3;
  void *pvVar4;
  undefined1 uVar5;
  char cVar6;
  size_t sVar7;
  undefined4 uVar8;
  uint3 uVar9;
  int iVar10;
  long lVar11;
  long lVar12;
  ulong uVar13;
  undefined1 *puVar14;
  undefined1 *puVar15;
  undefined1 *puVar16;
  undefined4 uVar17;
  undefined8 *****local_298 [2];
  undefined7 local_288;
  char cStack_281;
  ulong ****local_280;
  ulong ****ppppuStack_278;
  ulong ****local_270;
  undefined8 local_268;
  void *local_260;
  void *pvStack_258;
  long local_250;
  int local_248;
  undefined8 local_240;
  undefined8 uStack_238;
  undefined8 local_230;
  undefined8 local_228;
  undefined8 uStack_220;
  undefined8 local_218;
  undefined1 uStack_1e9;
  undefined8 local_1e8;
  undefined1 local_1e0 [72];
  ulong *****local_198;
  undefined1 local_190;
  undefined7 local_188;
  char cStack_181;
  undefined8 *****local_148;
  undefined1 local_140;
  undefined8 *****local_f8;
  ulong *****local_f0;
  undefined8 *puStack_e8;
  undefined8 local_e0;
  undefined8 uStack_d8;
  undefined8 local_d0;
  undefined8 uStack_c8;
  undefined8 local_c0;
  undefined8 uStack_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 local_80;
  long local_78;
  
  local_78 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar11 = FUN_02877d34(param_1 + 0x20);
  if ((lVar11 != 0) && (iVar10 = thunk_FUN_05e1d97c(3), iVar10 != 0)) {
    FUN_0488143c(&local_198);
    ppppppuVar2 = (ulong ******)local_198;
    if (-1 < cStack_181) {
      ppppppuVar2 = &local_198;
    }
    if ((DAT_0a39e011 & 1) == 0) {
      _DAT_0a39dff8 = CONCAT44((int)DAT_08482f20,(int)DAT_08572368);
      uRam000000000a39e000 = CONCAT44((int)DAT_0849fe78,(int)DAT_08760488);
      DAT_0a39e008 = CONCAT44((int)DAT_0851e180,(int)DAT_0849b068);
      DAT_0a39e010 = 0;
      DAT_0a39e011 = 1;
    }
    if ((DAT_0a39e0f1 & 1) == 0) {
      DAT_0a39e0e8._0_1_ = s_window_manager_cclose_WindowID___084e3f50[0x20];
      DAT_0a39e0e8._1_1_ = s_window_manager_cclose_WindowID___084e3f50[0x21];
      DAT_0a39e0e8._2_1_ = s_window_manager_cclose_WindowID___084e3f50[0x22];
      DAT_0a39e0e8._3_1_ = s_window_manager_cclose_WindowID___084e3f50[0x23];
      DAT_0a39e0e8._4_1_ = s_window_manager_cclose_WindowID___084e3f50[0x24];
      DAT_0a39e0e8._5_1_ = s_window_manager_cclose_WindowID___084e3f50[0x25];
      DAT_0a39e0e8._6_1_ = s_window_manager_cclose_WindowID___084e3f50[0x26];
      DAT_0a39e0e8._7_1_ = s_window_manager_cclose_WindowID___084e3f50[0x27];
      DAT_0a39e0f0 = 0;
      DAT_0a39e0f1 = 1;
    }
    FUN_05e1d050(&local_280,3,ppppppuVar2,&DAT_0a39dff8,&DAT_0a39e0e8,0x107,0,0);
    local_148 = *param_2;
    if (-1 < *(char *)((long)param_2 + 0x17)) {
      local_148 = param_2;
    }
    local_140 = 0;
    if ((DAT_0a39e130 & 1) == 0) {
      uVar13 = 0;
      do {
        uVar17 = *(undefined4 *)((long)&DAT_08805a72 + uVar13);
        uVar9 = CONCAT12((char)((uint)uVar17 >> 8),(short)uVar17) & 0xff00ff;
        uVar8 = *(undefined4 *)((long)&DAT_08805a5e + uVar13 % 0x14);
        *(uint *)((long)&DAT_0a39e0f2 + uVar13) =
             CONCAT13((char)((uint)uVar17 >> 0x18) + 0x8aU ^ (byte)((uint)uVar8 >> 0x18),
                      CONCAT12((char)((uint)uVar17 >> 0x10) + 0x8aU ^ (byte)((uint)uVar8 >> 0x10),
                               CONCAT11((char)(uVar9 >> 0x10) + 0x8aU ^ (byte)((uint)uVar8 >> 8),
                                        (char)uVar9 + 0x8aU ^ (byte)uVar8)));
        uVar13 = uVar13 + 4;
      } while (uVar13 != 0x3c);
      DAT_0a39e12e = 0x5f;
      DAT_0a39e130 = 1;
    }
    puStack_e8 = (undefined8 *)0x0;
    local_f0 = (ulong *****)0x0;
    local_f8 = &local_148;
    uStack_d8 = 0;
    local_e0 = 0;
    uStack_c8 = 0;
    local_d0 = 0;
    uStack_b8 = 0;
    local_c0 = 0;
    uStack_a8 = 0;
    local_b0 = 0;
    uStack_98 = 0;
    local_a0 = 0;
    uStack_88 = 0;
    local_90 = 0;
    local_80 = 0;
    FUN_05e1d31c(&local_280,&DAT_0a39e0f2,&local_f8);
    thunk_FUN_05e1d0bc(&local_280);
    if (cStack_181 < '\0') {
      __ZdlPvm(local_198,CONCAT17(cStack_181,local_188) & 0x7fffffffffffffff);
      cVar6 = *(char *)((long)param_3 + 0x17);
      goto joined_r0x02856c04;
    }
  }
  cVar6 = *(char *)((long)param_3 + 0x17);
joined_r0x02856c04:
  if (cVar6 < '\0') {
    FUN_00018d20(&local_280,*param_3,param_3[1]);
  }
  else {
    ppppuStack_278 = (ulong ****)param_3[1];
    local_280 = (ulong ****)*param_3;
    local_270 = (ulong ****)param_3[2];
  }
  local_268 = *param_5;
  *param_5 = 0;
  local_260 = (void *)0x0;
  pvStack_258 = (void *)0x0;
  local_250 = 0;
  pvVar4 = (void *)*param_4;
  sVar7 = param_4[1] - (long)pvVar4;
  if (sVar7 != 0) {
    if ((long)sVar7 < 0) {
                    /* WARNING: Subroutine does not return */
      FUN_003980cc(&local_260);
    }
    local_260 = (void *)__Znwm(sVar7);
    lVar11 = (long)local_260 + sVar7;
    pvStack_258 = local_260;
    local_250 = lVar11;
    _memcpy(local_260,pvVar4,sVar7);
    pvStack_258 = (void *)lVar11;
  }
  uStack_238 = param_7[1];
  local_240 = *param_7;
  local_230 = param_7[2];
  *param_7 = 0;
  param_7[1] = 0;
  uStack_220 = param_7[4];
  local_228 = param_7[3];
  local_218 = param_7[5];
  param_7[2] = 0;
  param_7[3] = 0;
  param_7[4] = 0;
  param_7[5] = 0;
  local_248 = param_6;
  local_f8 = param_2;
  lVar11 = FUN_02877ec4(param_1 + 0x20,param_2,&DAT_08b7a8b8,&local_f8,&local_148);
  if (*(char *)(lVar11 + 0x3f) < '\0') {
    __ZdlPvm(*(undefined8 *)(lVar11 + 0x28),*(ulong *)(lVar11 + 0x38) & 0x7fffffffffffffff);
  }
  *(ulong *****)(lVar11 + 0x30) = ppppuStack_278;
  *(ulong *****)(lVar11 + 0x28) = local_280;
  *(ulong *****)(lVar11 + 0x38) = local_270;
  local_270 = (ulong ****)((ulong)local_270 & 0xffffffffffffff);
  local_280 = (ulong ****)((ulong)local_280 & 0xffffffffffffff00);
  FUN_00033c7c(lVar11 + 0x40,&local_268);
  lVar12 = *(long *)(lVar11 + 0x48);
  if (lVar12 != 0) {
    *(long *)(lVar11 + 0x50) = lVar12;
    __ZdlPvm(lVar12,*(long *)(lVar11 + 0x58) - lVar12);
    *(long *)(lVar11 + 0x48) = 0;
    *(undefined8 *)(lVar11 + 0x50) = 0;
    *(undefined8 *)(lVar11 + 0x58) = 0;
  }
  *(void **)(lVar11 + 0x50) = pvStack_258;
  *(void **)(lVar11 + 0x48) = local_260;
  *(long *)(lVar11 + 0x58) = local_250;
  pvStack_258 = (void *)0x0;
  local_250 = 0;
  local_260 = (void *)0x0;
  *(int *)(lVar11 + 0x60) = local_248;
  FUN_028777e0(lVar11 + 0x68,&local_240);
  FUN_02877908(&local_280);
  iVar10 = thunk_FUN_05e1d97c(2);
  if (iVar10 != 0) {
    FUN_0488143c(local_298);
    ppppppuVar3 = (undefined8 ******)local_298[0];
    if (-1 < cStack_281) {
      ppppppuVar3 = local_298;
    }
    if ((DAT_0a39e011 & 1) == 0) {
      _DAT_0a39dff8 = CONCAT44((int)DAT_08482f20,(int)DAT_08572368);
      uRam000000000a39e000 = CONCAT44((int)DAT_0849fe78,(int)DAT_08760488);
      DAT_0a39e008 = CONCAT44((int)DAT_0851e180,(int)DAT_0849b068);
      DAT_0a39e010 = 0;
      DAT_0a39e011 = 1;
    }
    if ((DAT_0a39e0f1 & 1) == 0) {
      DAT_0a39e0e8._0_1_ = s_window_manager_cclose_WindowID___084e3f50[0x20];
      DAT_0a39e0e8._1_1_ = s_window_manager_cclose_WindowID___084e3f50[0x21];
      DAT_0a39e0e8._2_1_ = s_window_manager_cclose_WindowID___084e3f50[0x22];
      DAT_0a39e0e8._3_1_ = s_window_manager_cclose_WindowID___084e3f50[0x23];
      DAT_0a39e0e8._4_1_ = s_window_manager_cclose_WindowID___084e3f50[0x24];
      DAT_0a39e0e8._5_1_ = s_window_manager_cclose_WindowID___084e3f50[0x25];
      DAT_0a39e0e8._6_1_ = s_window_manager_cclose_WindowID___084e3f50[0x26];
      DAT_0a39e0e8._7_1_ = s_window_manager_cclose_WindowID___084e3f50[0x27];
      DAT_0a39e0f0 = 0;
      DAT_0a39e0f1 = 1;
    }
    FUN_05e1d050(&local_280,2,ppppppuVar3,&DAT_0a39dff8,&DAT_0a39e0e8,0x10a,0,0);
    local_148 = *param_2;
    if (-1 < *(char *)((long)param_2 + 0x17)) {
      local_148 = param_2;
    }
    local_140 = 0;
    local_198 = *param_3;
    if (-1 < *(char *)((long)param_3 + 0x17)) {
      local_198 = (ulong *****)param_3;
    }
    local_190 = 0;
    local_1e8 = (undefined1 *)0x0;
    if ((DAT_0a39ece8 & 1) == 0) {
      uVar13 = 0;
      do {
        uVar17 = *(undefined4 *)((long)&DAT_08808a13 + uVar13);
        uVar9 = CONCAT12((char)((uint)uVar17 >> 8),(short)uVar17) & 0xff00ff;
        uVar8 = *(undefined4 *)((long)&DAT_088089ff + uVar13 % 0x14);
        *(uint *)((long)&DAT_0a39eca0 + uVar13) =
             CONCAT13((char)((uint)uVar17 >> 0x18) + 0x69U ^ (byte)((uint)uVar8 >> 0x18),
                      CONCAT12((char)((uint)uVar17 >> 0x10) + 0x69U ^ (byte)((uint)uVar8 >> 0x10),
                               CONCAT11((char)(uVar9 >> 0x10) + 0x69U ^ (byte)((uint)uVar8 >> 8),
                                        (char)uVar9 + 0x69U ^ (byte)uVar8)));
        uVar13 = uVar13 + 4;
      } while (uVar13 != 0x48);
      DAT_0a39ece8 = 1;
    }
    lVar11 = 8;
    iVar10 = param_6;
    do {
      lVar12 = lVar11;
      local_1e0[lVar12 + -8] = *(undefined1 *)((long)&DAT_0a39eca0 + (long)(iVar10 % 10 + 0x23));
      lVar11 = lVar12 + 1;
      uVar1 = iVar10 + 9;
      iVar10 = iVar10 / 10;
    } while (0x12 < uVar1);
    if (param_6 < 0) {
      local_1e0[lVar12 + -7] = 0x2d;
      lVar11 = lVar12 + 2;
    }
    local_1e0[lVar11 + -8] = 0;
    if (9 < lVar11) {
      puVar16 = local_1e0;
      puVar14 = &uStack_1e9 + lVar11;
      do {
        puVar16 = puVar16 + 1;
        uVar5 = *puVar14;
        puVar15 = puVar14 + -1;
        *puVar14 = puVar16[-1];
        puVar16[-1] = uVar5;
        puVar14 = puVar15;
      } while (puVar16 < puVar15);
    }
    if ((DAT_0a39e16f & 1) == 0) {
      uVar13 = 0;
      do {
        uVar17 = *(undefined4 *)((long)&DAT_08805ac4 + uVar13);
        uVar9 = CONCAT12((char)((uint)uVar17 >> 8),(short)uVar17) & 0xff00ff;
        uVar8 = *(undefined4 *)((long)&DAT_08805ab0 + uVar13 % 0x14);
        *(uint *)((long)&DAT_0a39e131 + uVar13) =
             CONCAT13((char)((uint)uVar17 >> 0x18) + 0x8aU ^ (byte)((uint)uVar8 >> 0x18),
                      CONCAT12((char)((uint)uVar17 >> 0x10) + 0x8aU ^ (byte)((uint)uVar8 >> 0x10),
                               CONCAT11((char)(uVar9 >> 0x10) + 0x8aU ^ (byte)((uint)uVar8 >> 8),
                                        (char)uVar9 + 0x8aU ^ (byte)uVar8)));
        uVar13 = uVar13 + 4;
      } while (uVar13 != 0x3c);
      DAT_0a39e16d = 0x29;
      DAT_0a39e16f = 1;
    }
    local_f8 = &local_148;
    local_f0 = (ulong *****)&local_198;
    puStack_e8 = &local_1e8;
    uStack_d8 = 0;
    local_e0 = 0;
    uStack_c8 = 0;
    local_d0 = 0;
    uStack_b8 = 0;
    local_c0 = 0;
    uStack_a8 = 0;
    local_b0 = 0;
    uStack_98 = 0;
    local_a0 = 0;
    uStack_88 = 0;
    local_90 = 0;
    local_80 = 0;
    local_1e8 = local_1e0;
    FUN_05e1d31c(&local_280,&DAT_0a39e131,&local_f8);
    thunk_FUN_05e1d0bc(&local_280);
    if (cStack_281 < '\0') {
      __ZdlPvm(local_298[0],CONCAT17(cStack_281,local_288) & 0x7fffffffffffffff);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_78) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


