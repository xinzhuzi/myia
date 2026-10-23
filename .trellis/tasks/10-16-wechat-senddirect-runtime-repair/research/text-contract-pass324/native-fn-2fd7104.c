// Ghidra inferred pseudocode; requested=0x2fd7104
// entry=02fd7104 end=02fd8e17

/* WARNING: Removing unreachable block (ram,0x02fd8160) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_02fd7104(undefined8 *param_1,code *param_2,int *param_3,undefined8 *****param_4,
                 ulong param_5,undefined8 param_6,undefined8 param_7,int param_8)

{
  uint uVar1;
  uint uVar2;
  long *******ppppppplVar3;
  undefined8 *****pppppuVar4;
  undefined1 uVar5;
  char cVar6;
  uint3 uVar7;
  bool bVar8;
  long ******pppppplVar9;
  int iVar10;
  undefined8 uVar11;
  undefined8 *puVar12;
  undefined8 uVar13;
  size_t sVar14;
  char *pcVar15;
  long *plVar16;
  undefined8 *******pppppppuVar17;
  long *plVar18;
  undefined8 *puVar19;
  long lVar20;
  code *pcVar21;
  undefined1 *puVar22;
  long lVar23;
  long lVar24;
  ulong uVar25;
  undefined1 *puVar26;
  ulong uVar27;
  uint uVar28;
  int iVar29;
  undefined8 ****ppppuVar30;
  undefined8 uVar31;
  undefined4 uVar32;
  undefined4 uVar33;
  code *local_380;
  code *pcStack_378;
  code *local_370;
  undefined1 *local_368;
  code *pcStack_360;
  undefined1 *puStack_358;
  undefined1 *puStack_350;
  undefined1 *local_348;
  undefined1 *local_340;
  undefined1 *puStack_338;
  undefined1 *local_330;
  undefined1 *puStack_328;
  undefined1 *local_320;
  undefined1 *puStack_318;
  undefined1 *local_310;
  undefined1 *local_308;
  undefined1 *local_300;
  undefined1 *puStack_2f8;
  undefined1 *local_2f0;
  undefined1 *puStack_2e8;
  undefined1 *local_2e0;
  undefined1 *puStack_2d8;
  undefined1 *puStack_2d0;
  undefined1 *puStack_2c8;
  undefined1 *local_2c0;
  undefined8 *******local_2b0;
  undefined8 uStack_2a8;
  ulong local_2a0;
  undefined8 *******local_298;
  undefined8 uStack_290;
  ulong local_288;
  undefined8 *******local_280;
  ulong local_278;
  ulong local_270;
  undefined8 *******local_230;
  long *plStack_228;
  undefined8 local_220;
  undefined8 uStack_218;
  undefined1 *puStack_210;
  undefined1 *local_208;
  undefined1 *puStack_200;
  undefined1 *local_1f8;
  undefined1 *puStack_1f0;
  undefined1 *local_1e8;
  undefined1 *puStack_1e0;
  undefined1 *local_1d8;
  undefined8 uStack_1d0;
  undefined8 local_1c8;
  undefined8 uStack_1c0;
  undefined8 local_1b8;
  long *******local_1a0;
  undefined8 local_198;
  ulong local_190;
  undefined1 uStack_151;
  undefined8 local_150;
  undefined8 local_148;
  ulong local_140;
  undefined1 uStack_101;
  undefined8 local_100;
  undefined8 uStack_f8;
  undefined8 *******local_f0;
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
  
  local_78 = *(long *)PTR____stack_chk_guard_09b36c98;
  uVar11 = FUN_04669774();
  plVar18 = param_1 + 4;
  param_1[5] = 0;
  *plVar18 = 0;
  param_1[1] = 0;
  *param_1 = 0;
  param_1[3] = 0;
  param_1[2] = 0;
  puVar12 = (undefined8 *)__Znwm(0x270);
  puVar12[2] = 0;
  puVar12[1] = 0;
  *puVar12 = &PTR_FUN_09de0f80;
  _bzero(puVar12 + 3,0x228);
  *(undefined4 *)(puVar12 + 3) = 1;
  puVar12[0x40] = 0;
  puVar12[0x42] = 0;
  puVar12[0x41] = 0;
  *(undefined1 *)(puVar12 + 0x43) = 0;
  puVar12[0x11] = 0;
  puVar12[0x10] = 0;
  puVar12[0x13] = 0;
  puVar12[0x12] = 0;
  puVar12[0x15] = 0;
  puVar12[0x14] = 0;
  puVar12[0x17] = 0;
  puVar12[0x16] = 0;
  puVar12[0x19] = 0;
  puVar12[0x18] = 0;
  puVar12[0x1b] = 0;
  puVar12[0x1a] = 0;
  puVar12[0x1d] = 0;
  puVar12[0x1c] = 0;
  puVar12[0x1f] = 0;
  puVar12[0x1e] = 0;
  puVar12[0x21] = 0;
  puVar12[0x20] = 0;
  puVar12[0x23] = 0;
  puVar12[0x22] = 0;
  puVar12[0x25] = 0;
  puVar12[0x24] = 0;
  puVar12[0x27] = 0;
  puVar12[0x26] = 0;
  puVar12[0x29] = 0;
  puVar12[0x28] = 0;
  puVar12[0x2b] = 0;
  puVar12[0x2a] = 0;
  puVar12[0x2d] = 0;
  puVar12[0x2c] = 0;
  puVar12[0x2f] = 0;
  puVar12[0x2e] = 0;
  puVar12[0x31] = 0;
  puVar12[0x30] = 0;
  puVar12[0x33] = 0;
  puVar12[0x32] = 0;
  puVar12[0x35] = 0;
  puVar12[0x34] = 0;
  puVar12[0x37] = 0;
  puVar12[0x36] = 0;
  puVar12[0x39] = 0;
  puVar12[0x38] = 0;
  puVar12[0x3b] = 0;
  puVar12[0x3a] = 0;
  puVar12[0x3d] = 0;
  puVar12[0x3c] = 0;
  *(undefined8 *)((long)puVar12 + 0x1f1) = 0;
  *(undefined8 *)((long)puVar12 + 0x1e9) = 0;
  *(undefined2 *)(puVar12 + 0x47) = 0;
  puVar12[0x46] = 0;
  puVar12[0x45] = 0;
  puVar12[0x44] = 0;
  puVar12[0x49] = 0;
  puVar12[0x48] = 0;
  puVar12[0x4b] = 0;
  puVar12[0x4a] = 0;
  puVar12[0x4d] = 0;
  puVar12[0x4c] = 0;
  param_1[4] = puVar12 + 3;
  param_1[5] = puVar12;
  iVar10 = *param_3;
  iVar29 = param_3[1];
  *(int *)(puVar12 + 4) = iVar29;
  if (iVar10 != 0 || iVar29 != 0) {
    iVar10 = thunk_FUN_05e1d97c(4);
    if (iVar10 != 0) {
      FUN_0488143c(&local_280);
      pppppppuVar17 = local_280;
      if (-1 < (long)local_270) {
        pppppppuVar17 = &local_280;
      }
      if ((DAT_0a3d2361 & 1) == 0) {
        uRam000000000a3d2358._0_1_ = s_login_manager_ccauto_login_close_0889c040[8];
        uRam000000000a3d2358._1_1_ = s_login_manager_ccauto_login_close_0889c040[9];
        uRam000000000a3d2358._2_1_ = s_login_manager_ccauto_login_close_0889c040[10];
        uRam000000000a3d2358._3_1_ = s_login_manager_ccauto_login_close_0889c040[0xb];
        uRam000000000a3d2358._4_1_ = s_login_manager_ccauto_login_close_0889c040[0xc];
        uRam000000000a3d2358._5_1_ = s_login_manager_ccauto_login_close_0889c040[0xd];
        uRam000000000a3d2358._6_1_ = s_login_manager_ccauto_login_close_0889c040[0xe];
        uRam000000000a3d2358._7_1_ = s_login_manager_ccauto_login_close_0889c040[0xf];
        DAT_0a3d2350 = s_login_manager_ccauto_login_close_0889c040[0];
        DAT_0a3d2350_1._0_1_ = s_login_manager_ccauto_login_close_0889c040[1];
        DAT_0a3d2350_1._1_1_ = s_login_manager_ccauto_login_close_0889c040[2];
        DAT_0a3d2350_1._2_1_ = s_login_manager_ccauto_login_close_0889c040[3];
        DAT_0a3d2350_1._3_1_ = s_login_manager_ccauto_login_close_0889c040[4];
        DAT_0a3d2350_1._4_1_ = s_login_manager_ccauto_login_close_0889c040[5];
        DAT_0a3d2350_1._5_1_ = s_login_manager_ccauto_login_close_0889c040[6];
        DAT_0a3d2350_1._6_1_ = s_login_manager_ccauto_login_close_0889c040[7];
        DAT_0a3d2360 = 0;
        DAT_0a3d2361 = 1;
      }
      if ((DAT_0a3d2c37 & 1) == 0) {
        DAT_0a3d2c28._0_1_ = s_HandleAu_tim_0889c498[0];
        DAT_0a3d2c28._1_1_ = s_HandleAu_tim_0889c498[1];
        DAT_0a3d2c28._2_1_ = s_HandleAu_tim_0889c498[2];
        DAT_0a3d2c28._3_1_ = s_HandleAu_tim_0889c498[3];
        DAT_0a3d2c28._4_1_ = s_HandleAu_tim_0889c498[4];
        DAT_0a3d2c28._5_1_ = s_HandleAu_tim_0889c498[5];
        DAT_0a3d2c28._6_1_ = s_HandleAu_tim_0889c498[6];
        DAT_0a3d2c28._7_1_ = s_HandleAu_tim_0889c498[7];
        DAT_0a3d2c30 = (undefined4)DAT_087e31d8;
        DAT_0a3d2c34 = 0x7073;
        DAT_0a3d2c36 = 0;
        DAT_0a3d2c37 = 1;
      }
      FUN_05e1d050(&local_380,4,pppppppuVar17,&DAT_0a3d2350,&DAT_0a3d2c28,0x3d6,0,0);
      iVar10 = *param_3;
      local_100 = (undefined8 ******)0x0;
      if ((DAT_0a3d37f2 & 1) == 0) {
        uVar27 = 0;
        do {
          uVar32 = *(undefined4 *)((long)&DAT_0889efbe + uVar27);
          uVar7 = CONCAT12((char)((uint)uVar32 >> 8),(short)uVar32) & 0xff00ff;
          uVar33 = *(undefined4 *)((long)&DAT_0889efaa + uVar27 % 0x14);
          *(uint *)((long)&DAT_0a3d37aa + uVar27) =
               CONCAT13((char)((uint)uVar32 >> 0x18) + 0x69U ^ (byte)((uint)uVar33 >> 0x18),
                        CONCAT12((char)((uint)uVar32 >> 0x10) + 0x69U ^ (byte)((uint)uVar33 >> 0x10)
                                 ,CONCAT11((char)(uVar7 >> 0x10) + 0x69U ^ (byte)((uint)uVar33 >> 8)
                                           ,(char)uVar7 + 0x69U ^ (byte)uVar33)));
          uVar27 = uVar27 + 4;
        } while (uVar27 != 0x48);
        DAT_0a3d37f2 = 1;
      }
      lVar20 = 8;
      iVar29 = iVar10;
      do {
        lVar23 = lVar20;
        *(undefined1 *)((long)&local_100 + lVar23) =
             *(undefined1 *)((long)&DAT_0a3d37aa + (long)(iVar29 % 10 + 0x23));
        lVar20 = lVar23 + 1;
        uVar1 = iVar29 + 9;
        iVar29 = iVar29 / 10;
      } while (0x12 < uVar1);
      if (iVar10 < 0) {
        *(undefined1 *)((long)&local_100 + lVar23 + 1) = 0x2d;
        lVar20 = lVar23 + 2;
      }
      *(undefined1 *)((long)&local_100 + lVar20) = 0;
      if (9 < lVar20) {
        puVar22 = &uStack_101 + lVar20;
        puVar26 = (undefined1 *)((long)&uStack_f8 + 1);
        do {
          uVar5 = *puVar22;
          *puVar22 = puVar26[-1];
          puVar26[-1] = uVar5;
          bVar8 = puVar26 < puVar22 + -1;
          puVar22 = puVar22 + -1;
          puVar26 = puVar26 + 1;
        } while (bVar8);
      }
      local_100 = (undefined8 ******)&uStack_f8;
      iVar10 = param_3[1];
      local_150 = (undefined8 *****)0x0;
      lVar20 = 8;
      iVar29 = iVar10;
      do {
        lVar23 = lVar20;
        *(undefined1 *)((long)&local_150 + lVar23) =
             *(undefined1 *)((long)&DAT_0a3d37aa + (long)(iVar29 % 10 + 0x23));
        lVar20 = lVar23 + 1;
        uVar1 = iVar29 + 9;
        iVar29 = iVar29 / 10;
      } while (0x12 < uVar1);
      if (iVar10 < 0) {
        *(undefined1 *)((long)&local_150 + lVar23 + 1) = 0x2d;
        lVar20 = lVar23 + 2;
      }
      *(undefined1 *)((long)&local_150 + lVar20) = 0;
      if (9 < lVar20) {
        puVar22 = &uStack_151 + lVar20;
        puVar26 = (undefined1 *)((long)&local_148 + 1);
        do {
          uVar5 = *puVar22;
          *puVar22 = puVar26[-1];
          puVar26[-1] = uVar5;
          bVar8 = puVar26 < puVar22 + -1;
          puVar22 = puVar22 + -1;
          puVar26 = puVar26 + 1;
        } while (bVar8);
      }
      local_1a0 = *(long ********)(param_3 + 2);
      if (-1 < *(char *)((long)param_3 + 0x1f)) {
        local_1a0 = (long *******)(param_3 + 2);
      }
      local_198 = (long ******)((ulong)local_198 & 0xffffffffffffff00);
      if ((DAT_0a3d2c6c & 1) == 0) {
        _DAT_0a3d2c38 = CONCAT44((int)DAT_0889c450,(int)DAT_0889c448);
        uRam000000000a3d2c40 = CONCAT44((int)DAT_0852d448,(int)DAT_0852a9d8);
        _DAT_0a3d2c48 = CONCAT44((int)DAT_0856bb18,(int)DAT_088472b0);
        uRam000000000a3d2c50 = CONCAT44((int)DAT_08502a00,(int)DAT_084f1788);
        _DAT_0a3d2c58 = CONCAT44((int)DAT_084f1788,(int)ram0x087ce8e8);
        uRam000000000a3d2c60 = CONCAT44((int)DAT_0855b940,(int)DAT_084d77a0);
        DAT_0a3d2c68 = (undefined4)DAT_084fbc10;
        DAT_0a3d2c6c = 1;
      }
      local_230 = (undefined8 *******)&local_100;
      plStack_228 = &local_150;
      local_220 = (long *******)&local_1a0;
      puStack_210 = (undefined1 *)0x0;
      uStack_218 = (undefined1 *)0x0;
      puStack_200 = (undefined1 *)0x0;
      local_208 = (undefined1 *)0x0;
      puStack_1f0 = (undefined1 *)0x0;
      local_1f8 = (undefined1 *)0x0;
      puStack_1e0 = (undefined1 *)0x0;
      local_1e8 = (undefined1 *)0x0;
      uStack_1d0 = 0;
      local_1d8 = (undefined1 *)0x0;
      uStack_1c0 = 0;
      local_1c8 = 0;
      local_1b8 = 0;
      local_150 = (undefined8 *****)&local_148;
      FUN_05e1d31c(&local_380,&DAT_0a3d2c38,&local_230);
      thunk_FUN_05e1d0bc(&local_380);
      if ((long)local_270 < 0) {
        __ZdlPvm(local_280,local_270 & 0x7fffffffffffffff);
      }
    }
    lVar20 = *plVar18;
    *(undefined1 *)(lVar20 + 4) = 0;
    *(int *)(lVar20 + 8) = param_3[1];
    local_380 = (code *)&DAT_aaaaaaaa00000000;
    local_370 = (code *)0x0;
    pcStack_378 = (code *)0x0;
    pcStack_360 = (code *)0x0;
    local_368 = (undefined1 *)0x0;
    puStack_350 = (undefined1 *)0x0;
    puStack_358 = (undefined1 *)0x0;
    local_348 = &DAT_aaaaaaaa00000000;
    puStack_338 = (undefined1 *)0x0;
    local_340 = (undefined1 *)0x0;
    puStack_328 = (undefined1 *)0x0;
    local_330 = (undefined1 *)0x0;
    puStack_318 = (undefined1 *)0x0;
    local_320 = (undefined1 *)0x0;
    local_308 = (undefined1 *)0x0;
    local_310 = (undefined1 *)0x0;
    puStack_2f8 = (undefined1 *)0x0;
    local_300 = (undefined1 *)0x0;
    local_2f0 = &DAT_aaaaaaaa00000000;
    iVar10 = FUN_0471789c(&local_380,param_3 + 2);
    if (iVar10 != 0) {
      if ((long)local_368 < 0) {
        FUN_00018d20(&local_230,pcStack_378,local_370);
      }
      else {
        puVar12 = (undefined8 *)((ulong)&local_380 | 8);
        plStack_228 = (long *)puVar12[1];
        local_230 = (undefined8 *******)*puVar12;
        local_220 = (long *******)puVar12[2];
      }
      uStack_218 = (undefined1 *)((ulong)uStack_218 & 0xffffffff00000000);
      local_208 = (undefined1 *)0x0;
      puStack_200 = (undefined1 *)0x0;
      puStack_210 = (undefined1 *)0x0;
      FUN_0002b2c0(&local_1f8);
      FUN_02fc4f04(*plVar18 + 0x10,&local_230);
      FUN_0002b440(&local_1f8);
      if ((long)puStack_200 < 0) {
        __ZdlPvm(puStack_210,(ulong)puStack_200 & 0x7fffffffffffffff);
      }
      if ((long)local_220 < 0) {
        __ZdlPvm(local_230,(ulong)local_220 & 0x7fffffffffffffff);
      }
    }
    if (param_3[1] == -0x7da) {
      iVar10 = thunk_FUN_05e1d97c(4);
      if (iVar10 != 0) {
        FUN_0488143c(&local_298);
        pppppppuVar17 = local_298;
        if (-1 < (long)local_288) {
          pppppppuVar17 = &local_298;
        }
        if ((DAT_0a3d2361 & 1) == 0) {
          uRam000000000a3d2358._0_1_ = s_login_manager_ccauto_login_close_0889c040[8];
          uRam000000000a3d2358._1_1_ = s_login_manager_ccauto_login_close_0889c040[9];
          uRam000000000a3d2358._2_1_ = s_login_manager_ccauto_login_close_0889c040[10];
          uRam000000000a3d2358._3_1_ = s_login_manager_ccauto_login_close_0889c040[0xb];
          uRam000000000a3d2358._4_1_ = s_login_manager_ccauto_login_close_0889c040[0xc];
          uRam000000000a3d2358._5_1_ = s_login_manager_ccauto_login_close_0889c040[0xd];
          uRam000000000a3d2358._6_1_ = s_login_manager_ccauto_login_close_0889c040[0xe];
          uRam000000000a3d2358._7_1_ = s_login_manager_ccauto_login_close_0889c040[0xf];
          DAT_0a3d2350 = s_login_manager_ccauto_login_close_0889c040[0];
          DAT_0a3d2350_1._0_1_ = s_login_manager_ccauto_login_close_0889c040[1];
          DAT_0a3d2350_1._1_1_ = s_login_manager_ccauto_login_close_0889c040[2];
          DAT_0a3d2350_1._2_1_ = s_login_manager_ccauto_login_close_0889c040[3];
          DAT_0a3d2350_1._3_1_ = s_login_manager_ccauto_login_close_0889c040[4];
          DAT_0a3d2350_1._4_1_ = s_login_manager_ccauto_login_close_0889c040[5];
          DAT_0a3d2350_1._5_1_ = s_login_manager_ccauto_login_close_0889c040[6];
          DAT_0a3d2350_1._6_1_ = s_login_manager_ccauto_login_close_0889c040[7];
          DAT_0a3d2360 = 0;
          DAT_0a3d2361 = 1;
        }
        if ((DAT_0a3d2c37 & 1) == 0) {
          DAT_0a3d2c28._0_1_ = s_HandleAu_tim_0889c498[0];
          DAT_0a3d2c28._1_1_ = s_HandleAu_tim_0889c498[1];
          DAT_0a3d2c28._2_1_ = s_HandleAu_tim_0889c498[2];
          DAT_0a3d2c28._3_1_ = s_HandleAu_tim_0889c498[3];
          DAT_0a3d2c28._4_1_ = s_HandleAu_tim_0889c498[4];
          DAT_0a3d2c28._5_1_ = s_HandleAu_tim_0889c498[5];
          DAT_0a3d2c28._6_1_ = s_HandleAu_tim_0889c498[6];
          DAT_0a3d2c28._7_1_ = s_HandleAu_tim_0889c498[7];
          DAT_0a3d2c30 = (undefined4)DAT_087e31d8;
          DAT_0a3d2c34 = 0x7073;
          DAT_0a3d2c36 = 0;
          DAT_0a3d2c37 = 1;
        }
        FUN_05e1d050(&local_230,4,pppppppuVar17,&DAT_0a3d2350,&DAT_0a3d2c28,0x3e4,0,0);
        local_150 = (undefined8 *****)*param_4;
        if (-1 < *(char *)((long)param_4 + 0x17)) {
          local_150 = param_4;
        }
        local_148 = local_148 & 0xffffffffffffff00;
        local_1a0 = (long *******)&local_198;
        if ((DAT_0a3d37f2 & 1) == 0) {
          uVar27 = 0;
          do {
            uVar32 = *(undefined4 *)((long)&DAT_0889efbe + uVar27);
            uVar7 = CONCAT12((char)((uint)uVar32 >> 8),(short)uVar32) & 0xff00ff;
            uVar33 = *(undefined4 *)((long)&DAT_0889efaa + uVar27 % 0x14);
            *(uint *)((long)&DAT_0a3d37aa + uVar27) =
                 CONCAT13((char)((uint)uVar32 >> 0x18) + 0x69U ^ (byte)((uint)uVar33 >> 0x18),
                          CONCAT12((char)((uint)uVar32 >> 0x10) + 0x69U ^
                                   (byte)((uint)uVar33 >> 0x10),
                                   CONCAT11((char)(uVar7 >> 0x10) + 0x69U ^
                                            (byte)((uint)uVar33 >> 8),
                                            (char)uVar7 + 0x69U ^ (byte)uVar33)));
            uVar27 = uVar27 + 4;
          } while (uVar27 != 0x48);
          DAT_0a3d37f2 = 1;
        }
        lVar20 = 0;
        do {
          lVar23 = lVar20;
          *(undefined1 *)((long)&local_198 + lVar23) = *(undefined1 *)(param_5 % 10 + 0xa3d37cd);
          bVar8 = 9 < param_5;
          lVar20 = lVar23 + 1;
          param_5 = param_5 / 10;
        } while (bVar8);
        *(undefined1 *)((long)&local_198 + lVar23 + 1) = 0;
        if (8 < lVar23 + 8U) {
          puVar22 = (undefined1 *)((long)&local_198 + lVar23);
          puVar26 = (undefined1 *)((long)&local_198 + 1);
          do {
            uVar5 = *puVar22;
            *puVar22 = puVar26[-1];
            puVar26[-1] = uVar5;
            bVar8 = puVar26 < puVar22 + -1;
            puVar22 = puVar22 + -1;
            puVar26 = puVar26 + 1;
          } while (bVar8);
        }
        lVar20 = *plVar18;
        if (*(char *)(lVar20 + 0x60) == '\x01') {
          if (*(char *)(lVar20 + 0x27) < '\0') {
            FUN_00018d20(&local_2b0,*(undefined8 *)(lVar20 + 0x10),*(undefined8 *)(lVar20 + 0x18));
          }
          else {
            uStack_2a8 = *(undefined8 *)(lVar20 + 0x18);
            local_2b0 = *(undefined8 ********)(lVar20 + 0x10);
            local_2a0 = *(ulong *)(lVar20 + 0x20);
          }
        }
        else {
          local_2b0 = (undefined8 *******)0x0;
          uStack_2a8 = 0;
          local_2a0 = 0;
        }
        local_280 = local_2b0;
        if (-1 < (long)local_2a0) {
          local_280 = &local_2b0;
        }
        local_278 = local_278 & 0xffffffffffffff00;
        if ((DAT_0a3d2cb2 & 1) == 0) {
          uVar27 = 0;
          do {
            uVar32 = *(undefined4 *)((long)&DAT_0889de87 + uVar27);
            uVar7 = CONCAT12((char)((uint)uVar32 >> 8),(short)uVar32) & 0xff00ff;
            uVar33 = *(undefined4 *)((long)&DAT_0889de73 + uVar27 % 0x14);
            *(uint *)((long)&DAT_0a3d2c6d + uVar27) =
                 CONCAT13((char)((uint)uVar32 >> 0x18) + 0x8aU ^ (byte)((uint)uVar33 >> 0x18),
                          CONCAT12((char)((uint)uVar32 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar33 >> 0x10),
                                   CONCAT11((char)(uVar7 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar33 >> 8),
                                            (char)uVar7 + 0x8aU ^ (byte)uVar33)));
            uVar27 = uVar27 + 4;
          } while (uVar27 != 0x44);
          DAT_0a3d2cb1 = 0;
          DAT_0a3d2cb2 = 1;
        }
        local_100 = (undefined8 ******)&local_150;
        uStack_f8 = (long *******)&local_1a0;
        local_f0 = &local_280;
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
        FUN_05e1d31c(&local_230,&DAT_0a3d2c6d,&local_100);
        if ((long)local_2a0 < 0) {
          __ZdlPvm(local_2b0,local_2a0 & 0x7fffffffffffffff);
        }
        thunk_FUN_05e1d0bc(&local_230);
        if ((long)local_288 < 0) {
          __ZdlPvm(local_298,local_288 & 0x7fffffffffffffff);
        }
      }
      pcVar15 = (char *)FUN_04e043c8();
      plVar16 = (long *)_strlen(pcVar15);
      if ((long *)0x7ffffffffffffff7 < plVar16) {
                    /* WARNING: Subroutine does not return */
        FUN_00018d9c(&local_230);
      }
      if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar16) {
        uVar27 = 0x19;
        if (((ulong)plVar16 | 7) != 0x17) {
          uVar27 = ((ulong)plVar16 | 7) + 1;
        }
        pppppppuVar17 = (undefined8 *******)__Znwm(uVar27);
        local_220 = (long *******)(uVar27 | 0x8000000000000000);
        local_230 = pppppppuVar17;
        plStack_228 = plVar16;
LAB_02fd8c10:
        _memmove(pppppppuVar17,pcVar15,(size_t)plVar16);
      }
      else {
        local_220 = (long *******)CONCAT17((char)plVar16,(undefined7)local_220);
        pppppppuVar17 = &local_230;
        if (plVar16 != (long *)0x0) goto LAB_02fd8c10;
      }
      *(undefined1 *)((long)pppppppuVar17 + (long)plVar16) = 0;
      uStack_218 = (undefined1 *)((ulong)uStack_218._4_4_ << 0x20);
      local_208 = (undefined1 *)0x0;
      puStack_200 = (undefined1 *)0x0;
      puStack_210 = (undefined1 *)0x0;
      FUN_0002b2c0(&local_1f8);
      FUN_02fc4f04(*plVar18 + 0x10,&local_230);
      FUN_0002b440(&local_1f8);
      if ((long)puStack_200 < 0) {
        __ZdlPvm(puStack_210,(ulong)puStack_200 & 0x7fffffffffffffff);
      }
      if ((long)local_220 < 0) {
        __ZdlPvm(local_230,(ulong)local_220 & 0x7fffffffffffffff);
      }
      iVar10 = FUN_03b032cc(1);
      if (iVar10 != 0) {
        local_1e8 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_1f0 = &SUB_aaaaaaaaaaaaaaaa;
        local_1d8 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_1e0 = &SUB_aaaaaaaaaaaaaaaa;
        local_208 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_210 = &SUB_aaaaaaaaaaaaaaaa;
        local_1f8 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_200 = &SUB_aaaaaaaaaaaaaaaa;
        plStack_228 = (long *)&SUB_aaaaaaaaaaaaaaaa;
        uStack_218 = &SUB_aaaaaaaaaaaaaaaa;
        local_220 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
        local_230 = (undefined8 *******)&DAT_aaaaaaaa00000000;
        plVar18 = (long *)((ulong)&local_230 | 8);
        if (*(char *)((long)param_4 + 0x17) < '\0') {
          FUN_00018d20(plVar18,*param_4,param_4[1]);
        }
        else {
          ppppuVar30 = *param_4;
          plVar18[1] = (long)param_4[1];
          *plVar18 = (long)ppppuVar30;
          plVar18[2] = (long)param_4[2];
        }
        puStack_1f0 = (undefined1 *)0x0;
        local_1e8 = (undefined1 *)0x0;
        local_1d8 = (undefined1 *)((ulong)local_1d8 & 0xffffffffffff0000);
        puStack_1e0 = (undefined1 *)0x0;
        puStack_200 = (undefined1 *)DAT_0889c4b8;
        local_1f8 = (undefined1 *)CONCAT71(local_1f8._1_7_,1);
        puStack_210 = (undefined1 *)CONCAT44(puStack_210._4_4_,1);
        local_208 = (undefined1 *)0x0;
        FUN_03b03320(&local_230);
        if ((long)uStack_218 < 0) {
          __ZdlPvm(plStack_228,(ulong)uStack_218 & 0x7fffffffffffffff);
        }
      }
      FUN_02fd9174(param_2,param_4);
    }
    if ((long)puStack_2f8 < 0) {
      __ZdlPvm(local_308,(ulong)puStack_2f8 & 0x7fffffffffffffff);
    }
    if ((long)local_310 < 0) {
      __ZdlPvm(local_320,(ulong)local_310 & 0x7fffffffffffffff);
    }
    if ((long)local_330 < 0) {
      __ZdlPvm(local_340,(ulong)local_330 & 0x7fffffffffffffff);
    }
    if ((long)puStack_350 < 0) {
      __ZdlPvm(pcStack_360,(ulong)puStack_350 & 0x7fffffffffffffff);
    }
    if ((long)local_368 < 0) {
      __ZdlPvm(pcStack_378,(ulong)local_368 & 0x7fffffffffffffff);
    }
    goto LAB_02fd8d58;
  }
  *(undefined1 *)((long)puVar12 + 0x1c) = 1;
  FUN_04669774();
  FUN_0466ad94();
  lVar20 = FUN_01f4e748(uVar11);
  FUN_04669774();
  FUN_0466ad74(&local_100);
  pcStack_378 = FUN_03000a6c;
  local_370 = FUN_02fd98dc;
  local_368 = (undefined1 *)0x0;
  pcStack_360 = FUN_03000a84;
  local_230 = (undefined8 *******)0x0;
  plStack_228 = (long *)0x0;
  local_380 = param_2;
  FUN_06686420(lVar20 + 0xf8,&local_380,0,0,local_100[1],&local_230);
  plVar16 = plStack_228;
  if (plStack_228 != (long *)0x0) {
    LOAcquire();
    lVar20 = plStack_228[1];
    plStack_228[1] = lVar20 + -1;
    LORelease();
    if (lVar20 == 0) {
      (**(code **)(*plStack_228 + 0x10))(plStack_228);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar16);
    }
  }
  ppppppplVar3 = uStack_f8;
  if (uStack_f8 != (long *******)0x0) {
    LOAcquire();
    pppppplVar9 = uStack_f8[1];
    uStack_f8[1] = (long ******)((long)pppppplVar9 + -1);
    LORelease();
    if (pppppplVar9 == (long ******)0x0) {
      (*(code *)(*uStack_f8)[2])(uStack_f8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar3);
    }
  }
  lVar20 = *(long *)(*(long *)(param_3 + 8) + 0x10);
  if (lVar20 == 0) {
    lVar20 = *(long *)(DAT_0a520ca0 + 0x10);
  }
  uVar1 = *(uint *)(lVar20 + 0x94);
  uVar27 = (ulong)uVar1;
  iVar10 = thunk_FUN_05e1d97c(2);
  if (iVar10 != 0) {
    FUN_0488143c(&local_1a0);
    ppppppplVar3 = local_1a0;
    if (-1 < (long)local_190) {
      ppppppplVar3 = (long *******)&local_1a0;
    }
    if ((DAT_0a3d2361 & 1) == 0) {
      uRam000000000a3d2358._0_1_ = s_login_manager_ccauto_login_close_0889c040[8];
      uRam000000000a3d2358._1_1_ = s_login_manager_ccauto_login_close_0889c040[9];
      uRam000000000a3d2358._2_1_ = s_login_manager_ccauto_login_close_0889c040[10];
      uRam000000000a3d2358._3_1_ = s_login_manager_ccauto_login_close_0889c040[0xb];
      uRam000000000a3d2358._4_1_ = s_login_manager_ccauto_login_close_0889c040[0xc];
      uRam000000000a3d2358._5_1_ = s_login_manager_ccauto_login_close_0889c040[0xd];
      uRam000000000a3d2358._6_1_ = s_login_manager_ccauto_login_close_0889c040[0xe];
      uRam000000000a3d2358._7_1_ = s_login_manager_ccauto_login_close_0889c040[0xf];
      DAT_0a3d2350 = s_login_manager_ccauto_login_close_0889c040[0];
      DAT_0a3d2350_1._0_1_ = s_login_manager_ccauto_login_close_0889c040[1];
      DAT_0a3d2350_1._1_1_ = s_login_manager_ccauto_login_close_0889c040[2];
      DAT_0a3d2350_1._2_1_ = s_login_manager_ccauto_login_close_0889c040[3];
      DAT_0a3d2350_1._3_1_ = s_login_manager_ccauto_login_close_0889c040[4];
      DAT_0a3d2350_1._4_1_ = s_login_manager_ccauto_login_close_0889c040[5];
      DAT_0a3d2350_1._5_1_ = s_login_manager_ccauto_login_close_0889c040[6];
      DAT_0a3d2350_1._6_1_ = s_login_manager_ccauto_login_close_0889c040[7];
      DAT_0a3d2360 = 0;
      DAT_0a3d2361 = 1;
    }
    if ((DAT_0a3d2c37 & 1) == 0) {
      DAT_0a3d2c28._0_1_ = s_HandleAu_tim_0889c498[0];
      DAT_0a3d2c28._1_1_ = s_HandleAu_tim_0889c498[1];
      DAT_0a3d2c28._2_1_ = s_HandleAu_tim_0889c498[2];
      DAT_0a3d2c28._3_1_ = s_HandleAu_tim_0889c498[3];
      DAT_0a3d2c28._4_1_ = s_HandleAu_tim_0889c498[4];
      DAT_0a3d2c28._5_1_ = s_HandleAu_tim_0889c498[5];
      DAT_0a3d2c28._6_1_ = s_HandleAu_tim_0889c498[6];
      DAT_0a3d2c28._7_1_ = s_HandleAu_tim_0889c498[7];
      DAT_0a3d2c30 = (undefined4)DAT_087e31d8;
      DAT_0a3d2c34 = 0x7073;
      DAT_0a3d2c36 = 0;
      DAT_0a3d2c37 = 1;
    }
    FUN_05e1d050(&local_380,2,ppppppplVar3,&DAT_0a3d2350,&DAT_0a3d2c28,0x3fd,0,0);
    local_100 = (undefined8 ******)0x0;
    local_100 = (undefined8 ******)&uStack_f8;
    if ((DAT_0a3d37f2 & 1) == 0) {
      uVar25 = 0;
      do {
        uVar32 = *(undefined4 *)((long)&DAT_0889efbe + uVar25);
        uVar7 = CONCAT12((char)((uint)uVar32 >> 8),(short)uVar32) & 0xff00ff;
        uVar33 = *(undefined4 *)((long)&DAT_0889efaa + uVar25 % 0x14);
        *(uint *)((long)&DAT_0a3d37aa + uVar25) =
             CONCAT13((char)((uint)uVar32 >> 0x18) + 0x69U ^ (byte)((uint)uVar33 >> 0x18),
                      CONCAT12((char)((uint)uVar32 >> 0x10) + 0x69U ^ (byte)((uint)uVar33 >> 0x10),
                               CONCAT11((char)(uVar7 >> 0x10) + 0x69U ^ (byte)((uint)uVar33 >> 8),
                                        (char)uVar7 + 0x69U ^ (byte)uVar33)));
        uVar25 = uVar25 + 4;
      } while (uVar25 != 0x48);
      DAT_0a3d37f2 = 1;
    }
    lVar20 = 0;
    uVar25 = uVar27;
    do {
      lVar23 = lVar20;
      uVar28 = (uint)uVar25;
      *(undefined1 *)((long)&uStack_f8 + lVar23) =
           *(undefined1 *)((long)&DAT_0a3d37aa + (ulong)(uVar28 + (int)(uVar25 / 10) * -10 + 0x23));
      lVar20 = lVar23 + 1;
      uVar25 = uVar25 / 10;
    } while (9 < uVar28);
    *(undefined1 *)((long)&uStack_f8 + lVar23 + 1) = 0;
    if (8 < lVar23 + 8U) {
      puVar22 = (undefined1 *)((long)&uStack_f8 + lVar23);
      puVar26 = (undefined1 *)((long)&uStack_f8 + 1);
      do {
        uVar5 = *puVar22;
        *puVar22 = puVar26[-1];
        puVar26[-1] = uVar5;
        bVar8 = puVar26 < puVar22 + -1;
        puVar22 = puVar22 + -1;
        puVar26 = puVar26 + 1;
      } while (bVar8);
    }
    local_150 = (undefined8 *****)*param_4;
    if (-1 < *(char *)((long)param_4 + 0x17)) {
      local_150 = param_4;
    }
    local_148 = local_148 & 0xffffffffffffff00;
    if ((DAT_0a3d2ce3 & 1) == 0) {
      _DAT_0a3d2cb4 = CONCAT44((int)DAT_086eb438,(int)ram0x0889c4a0);
      uRam000000000a3d2cbc = CONCAT44((int)DAT_0889c4a8,(int)DAT_08801070);
      _DAT_0a3d2cc4 = CONCAT44((int)DAT_086872a8,(int)DAT_0855bd90);
      uRam000000000a3d2ccc = CONCAT44((int)ram0x08628300,(int)DAT_0889c4b0);
      DAT_0a3d2cd4 = CONCAT44((int)DAT_0862c958,(int)DAT_08502a30);
      DAT_0a3d2cdc = (undefined4)DAT_0883db60;
      DAT_0a3d2ce0 = 0x5f25;
      DAT_0a3d2ce2 = 0;
      DAT_0a3d2ce3 = 1;
    }
    local_230 = (undefined8 *******)&local_100;
    plStack_228 = &local_150;
    uStack_218 = (undefined1 *)0x0;
    local_220 = (long *******)0x0;
    local_208 = (undefined1 *)0x0;
    puStack_210 = (undefined1 *)0x0;
    local_1f8 = (undefined1 *)0x0;
    puStack_200 = (undefined1 *)0x0;
    local_1e8 = (undefined1 *)0x0;
    puStack_1f0 = (undefined1 *)0x0;
    local_1d8 = (undefined1 *)0x0;
    puStack_1e0 = (undefined1 *)0x0;
    local_1c8 = 0;
    uStack_1d0 = 0;
    local_1b8 = 0;
    uStack_1c0 = 0;
    FUN_05e1d31c(&local_380,&DAT_0a3d2cb4,&local_230);
    thunk_FUN_05e1d0bc(&local_380);
    if ((long)local_190 < 0) {
      __ZdlPvm(local_1a0,local_190 & 0x7fffffffffffffff);
    }
  }
  if (uVar1 != 0) {
    FUN_04670f4c(uVar11);
    FUN_04670f44(uVar11,uVar27);
    FUN_04670f5c(uVar11,uVar27);
  }
  uVar1 = *(uint *)(*(long *)(param_3 + 8) + 0x30);
  uVar13 = thunk_FUN_05e1d97c(2);
  if ((int)uVar13 != 0) {
    FUN_0488143c(&local_150);
    pppppuVar4 = local_150;
    if (-1 < (long)local_140) {
      pppppuVar4 = (undefined8 *****)&local_150;
    }
    if ((DAT_0a3d2361 & 1) == 0) {
      uRam000000000a3d2358._0_1_ = s_login_manager_ccauto_login_close_0889c040[8];
      uRam000000000a3d2358._1_1_ = s_login_manager_ccauto_login_close_0889c040[9];
      uRam000000000a3d2358._2_1_ = s_login_manager_ccauto_login_close_0889c040[10];
      uRam000000000a3d2358._3_1_ = s_login_manager_ccauto_login_close_0889c040[0xb];
      uRam000000000a3d2358._4_1_ = s_login_manager_ccauto_login_close_0889c040[0xc];
      uRam000000000a3d2358._5_1_ = s_login_manager_ccauto_login_close_0889c040[0xd];
      uRam000000000a3d2358._6_1_ = s_login_manager_ccauto_login_close_0889c040[0xe];
      uRam000000000a3d2358._7_1_ = s_login_manager_ccauto_login_close_0889c040[0xf];
      DAT_0a3d2350 = s_login_manager_ccauto_login_close_0889c040[0];
      DAT_0a3d2350_1._0_1_ = s_login_manager_ccauto_login_close_0889c040[1];
      DAT_0a3d2350_1._1_1_ = s_login_manager_ccauto_login_close_0889c040[2];
      DAT_0a3d2350_1._2_1_ = s_login_manager_ccauto_login_close_0889c040[3];
      DAT_0a3d2350_1._3_1_ = s_login_manager_ccauto_login_close_0889c040[4];
      DAT_0a3d2350_1._4_1_ = s_login_manager_ccauto_login_close_0889c040[5];
      DAT_0a3d2350_1._5_1_ = s_login_manager_ccauto_login_close_0889c040[6];
      DAT_0a3d2350_1._6_1_ = s_login_manager_ccauto_login_close_0889c040[7];
      DAT_0a3d2360 = 0;
      DAT_0a3d2361 = 1;
    }
    if ((DAT_0a3d2c37 & 1) == 0) {
      DAT_0a3d2c28._0_1_ = s_HandleAu_tim_0889c498[0];
      DAT_0a3d2c28._1_1_ = s_HandleAu_tim_0889c498[1];
      DAT_0a3d2c28._2_1_ = s_HandleAu_tim_0889c498[2];
      DAT_0a3d2c28._3_1_ = s_HandleAu_tim_0889c498[3];
      DAT_0a3d2c28._4_1_ = s_HandleAu_tim_0889c498[4];
      DAT_0a3d2c28._5_1_ = s_HandleAu_tim_0889c498[5];
      DAT_0a3d2c28._6_1_ = s_HandleAu_tim_0889c498[6];
      DAT_0a3d2c28._7_1_ = s_HandleAu_tim_0889c498[7];
      DAT_0a3d2c30 = (undefined4)DAT_087e31d8;
      DAT_0a3d2c34 = 0x7073;
      DAT_0a3d2c36 = 0;
      DAT_0a3d2c37 = 1;
    }
    FUN_05e1d050(&local_380,2,pppppuVar4,&DAT_0a3d2350,&DAT_0a3d2c28,0x406,0,0);
    local_100 = (undefined8 ******)0x0;
    if ((DAT_0a3d37f2 & 1) == 0) {
      uVar27 = 0;
      do {
        uVar32 = *(undefined4 *)((long)&DAT_0889efbe + uVar27);
        uVar7 = CONCAT12((char)((uint)uVar32 >> 8),(short)uVar32) & 0xff00ff;
        uVar33 = *(undefined4 *)((long)&DAT_0889efaa + uVar27 % 0x14);
        *(uint *)((long)&DAT_0a3d37aa + uVar27) =
             CONCAT13((char)((uint)uVar32 >> 0x18) + 0x69U ^ (byte)((uint)uVar33 >> 0x18),
                      CONCAT12((char)((uint)uVar32 >> 0x10) + 0x69U ^ (byte)((uint)uVar33 >> 0x10),
                               CONCAT11((char)(uVar7 >> 0x10) + 0x69U ^ (byte)((uint)uVar33 >> 8),
                                        (char)uVar7 + 0x69U ^ (byte)uVar33)));
        uVar27 = uVar27 + 4;
      } while (uVar27 != 0x48);
      DAT_0a3d37f2 = 1;
    }
    lVar20 = 8;
    uVar28 = uVar1;
    do {
      lVar23 = lVar20;
      *(undefined1 *)((long)&local_100 + lVar23) =
           *(undefined1 *)((long)&DAT_0a3d37aa + (long)((int)uVar28 % 10 + 0x23));
      lVar20 = lVar23 + 1;
      uVar2 = uVar28 + 9;
      uVar28 = (int)uVar28 / 10;
    } while (0x12 < uVar2);
    if ((int)uVar1 < 0) {
      *(undefined1 *)((long)&local_100 + lVar23 + 1) = 0x2d;
      lVar20 = lVar23 + 2;
    }
    *(undefined1 *)((long)&local_100 + lVar20) = 0;
    if (9 < lVar20) {
      puVar22 = &uStack_101 + lVar20;
      puVar26 = (undefined1 *)((long)&uStack_f8 + 1);
      do {
        uVar5 = *puVar22;
        *puVar22 = puVar26[-1];
        puVar26[-1] = uVar5;
        bVar8 = puVar26 < puVar22 + -1;
        puVar22 = puVar22 + -1;
        puVar26 = puVar26 + 1;
      } while (bVar8);
    }
    if ((DAT_0a3d2d04 & 1) == 0) {
      uRam000000000a3d2cf8._0_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x48];
      uRam000000000a3d2cf8._1_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x49];
      uRam000000000a3d2cf8._2_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x4a];
      uRam000000000a3d2cf8._3_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x4b];
      uRam000000000a3d2cf8._4_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x4c];
      uRam000000000a3d2cf8._5_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x4d];
      uRam000000000a3d2cf8._6_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x4e];
      uRam000000000a3d2cf8._7_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x4f];
      DAT_0a3d2cf0 = s_CheckLoginQRCodePCAccountName____0889c0b0[0x40];
      DAT_0a3d2cf0_1._0_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x41];
      DAT_0a3d2cf0_1._1_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x42];
      DAT_0a3d2cf0_1._2_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x43];
      DAT_0a3d2cf0_1._3_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x44];
      DAT_0a3d2cf0_1._4_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x45];
      DAT_0a3d2cf0_1._5_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x46];
      DAT_0a3d2cf0_1._6_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x47];
      DAT_0a3d2d00 = (undefined4)ram0x084c9468;
      DAT_0a3d2d04 = 1;
    }
    local_220 = (long *******)0x0;
    plStack_228 = (long *)0x0;
    local_230 = (undefined8 *******)&local_100;
    puStack_210 = (undefined1 *)0x0;
    uStack_218 = (undefined1 *)0x0;
    puStack_200 = (undefined1 *)0x0;
    local_208 = (undefined1 *)0x0;
    puStack_1f0 = (undefined1 *)0x0;
    local_1f8 = (undefined1 *)0x0;
    puStack_1e0 = (undefined1 *)0x0;
    local_1e8 = (undefined1 *)0x0;
    uStack_1d0 = 0;
    local_1d8 = (undefined1 *)0x0;
    uStack_1c0 = 0;
    local_1c8 = 0;
    local_1b8 = 0;
    local_100 = (undefined8 ******)&uStack_f8;
    FUN_05e1d31c(&local_380,&DAT_0a3d2cf0,&local_230);
    uVar13 = thunk_FUN_05e1d0bc(&local_380);
    if ((long)local_140 < 0) {
      uVar13 = __ZdlPvm(local_150,local_140 & 0x7fffffffffffffff);
    }
  }
  if ((uVar1 >> 1 & 1) != 0) {
    lVar20 = *(long *)(param_3 + 8);
    lVar23 = *(long *)(lVar20 + 0x10);
    if (lVar23 == 0) {
      lVar23 = *(long *)(DAT_0a520ca0 + 0x10);
    }
    lVar24 = *plVar18;
    *(undefined8 *)(lVar24 + 0x68) = *(undefined8 *)(lVar23 + 8);
    lVar20 = *(long *)(lVar20 + 0x18);
    if (lVar20 == 0) {
      lVar20 = *(long *)(DAT_0a520ca0 + 0x18);
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (lVar24 + 0x70,*(undefined8 *)(lVar20 + 8));
    lVar20 = *(long *)(*(long *)(param_3 + 8) + 0x18);
    if (lVar20 == 0) {
      lVar20 = *(long *)(DAT_0a520ca0 + 0x18);
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (*plVar18 + 0x100,*(undefined8 *)(lVar20 + 0x30));
    lVar23 = *plVar18;
    lVar20 = *(long *)(*(long *)(param_3 + 8) + 0x18);
    if (lVar20 == 0) {
      lVar20 = *(long *)(DAT_0a520ca0 + 0x18);
    }
    puVar19 = *(undefined8 **)(lVar20 + 0x30);
    puVar12 = *(undefined8 **)(lVar23 + 0x210);
    if (puVar12 < *(undefined8 **)(lVar23 + 0x218)) {
      if (*(char *)((long)puVar19 + 0x17) < '\0') {
        FUN_00018d20(puVar12,*puVar19,puVar19[1]);
      }
      else {
        uVar31 = puVar19[1];
        uVar13 = *puVar19;
        puVar12[2] = puVar19[2];
        puVar12[1] = uVar31;
        *puVar12 = uVar13;
      }
      puVar12 = puVar12 + 3;
      *(undefined8 **)(lVar23 + 0x210) = puVar12;
    }
    else {
      puVar12 = (undefined8 *)FUN_0002df44(lVar23 + 0x208);
    }
    *(undefined8 **)(lVar23 + 0x210) = puVar12;
    pcStack_378 = (code *)&SUB_aaaaaaaaaaaaaaaa;
    local_370 = (code *)&SUB_aaaaaaaaaaaaaaaa;
    local_380 = (code *)&SUB_aaaaaaaaaaaaaaaa;
    lVar20 = *(long *)(*(long *)(param_3 + 8) + 0x18);
    if (lVar20 == 0) {
      lVar20 = *(long *)(DAT_0a520ca0 + 0x18);
    }
    puVar19 = *(undefined8 **)(lVar20 + 0x70);
    cVar6 = *(char *)((long)puVar19 + 0x17);
    puVar12 = (undefined8 *)*puVar19;
    if (-1 < (long)cVar6) {
      puVar12 = puVar19;
    }
    lVar20 = puVar19[1];
    if (-1 < cVar6) {
      lVar20 = (long)cVar6;
    }
    if ((DAT_0a3d2d07 & 1) == 0) {
      DAT_0a3d2d05 = 0x2c;
      DAT_0a3d2d07 = 1;
    }
    sVar14 = _strlen((char *)&DAT_0a3d2d05);
    FUN_00063f9c(&local_380,puVar12,lVar20,&DAT_0a3d2d05,sVar14,1,1);
    uVar13 = FUN_03000aac(*plVar18 + 0x208,*(undefined8 *)(*plVar18 + 0x210),local_380,pcStack_378,
                          ((long)pcStack_378 - (long)local_380 >> 3) * -0x5555555555555555);
    if (local_380 != (code *)0x0) {
      for (; pcStack_378 != local_380; pcStack_378 = pcStack_378 + -0x18) {
      }
      pcStack_378 = local_380;
      uVar13 = __ZdlPvm(local_380,(long)local_370 - (long)local_380);
    }
  }
  if ((uVar1 & 1) != 0) {
    local_148 = 0;
    local_150 = (undefined8 *****)0x0;
    local_140 = 0;
    local_1a0 = (long *******)0x0;
    local_198 = (long ******)0x0;
    local_190 = 0;
    local_280 = (undefined8 *******)0x0;
    local_278 = 0;
    local_270 = 0;
    local_298 = (undefined8 *******)0x0;
    uStack_290 = 0;
    local_288 = 0;
    FUN_02fd4080(param_3,param_7,&local_150,&local_1a0,&local_280,&local_298);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (*plVar18 + 0x88,&local_150);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (*plVar18 + 0xa0,&local_1a0);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (*plVar18 + 0xb8,&local_280);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (*plVar18 + 0xd0,&local_298);
    if (*(long *)(*(long *)(param_3 + 8) + 0x10) == 0) {
      lVar20 = *(long *)(*(long *)(DAT_0a520ca0 + 0x10) + 0x60);
    }
    else {
      lVar20 = *(long *)(*(long *)(*(long *)(param_3 + 8) + 0x10) + 0x60);
    }
    if (lVar20 == 0) {
      lVar20 = *(long *)(DAT_0a520c80 + 0x60);
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (*plVar18 + 0xe8,*(undefined8 *)(lVar20 + 8));
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (*plVar18 + 0x148,*plVar18 + 0x70);
    lVar20 = *(long *)(*(long *)(param_3 + 8) + 0x18);
    if (lVar20 == 0) {
      lVar20 = *(long *)(DAT_0a520ca0 + 0x18);
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (*plVar18 + 0x168,*(undefined8 *)(lVar20 + 0x10));
    if (*(long *)(*(long *)(param_3 + 8) + 0x10) == 0) {
      lVar20 = *(long *)(*(long *)(DAT_0a520ca0 + 0x10) + 0x20);
    }
    else {
      lVar20 = *(long *)(*(long *)(*(long *)(param_3 + 8) + 0x10) + 0x20);
    }
    if (lVar20 == 0) {
      lVar20 = *(long *)(DAT_0a520c80 + 0x20);
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (*plVar18 + 0x180,*(undefined8 *)(lVar20 + 8));
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (*plVar18 + 0x198,param_2 + 0x1b0);
    FUN_0474f5bc(&local_380);
    lVar20 = *plVar18;
    if (*(char *)(lVar20 + 0x1c7) < '\0') {
      __ZdlPvm(*(undefined8 *)(lVar20 + 0x1b0),*(ulong *)(lVar20 + 0x1c0) & 0x7fffffffffffffff);
    }
    *(code **)(lVar20 + 0x1b8) = pcStack_378;
    *(code **)(lVar20 + 0x1b0) = local_380;
    *(code **)(lVar20 + 0x1c0) = local_370;
    lVar20 = *plVar18;
    *(undefined4 *)(lVar20 + 0x160) = *(undefined4 *)(param_2 + 0x1d8);
    *(int *)(lVar20 + 0x164) = (int)*(undefined8 *)(param_2 + 0x1d0);
    FUN_0466d4c8(&local_380,uVar11);
    uVar13 = __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                       (*plVar18 + 0x1c8,&local_380);
    if ((long)local_370 < 0) {
      uVar13 = __ZdlPvm(local_380,(ulong)local_370 & 0x7fffffffffffffff);
    }
    lVar20 = *plVar18;
    *(undefined1 *)(lVar20 + 0x1e0) = 0;
    *(code *)(lVar20 + 0x200) = param_2[0x1de];
    *(undefined2 *)(lVar20 + 0x220) = *(undefined2 *)(param_2 + 0x1dc);
    param_2[0x1de] = (code)0x0;
    if (param_8 != 0) {
      local_2c0 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_2d8 = &SUB_aaaaaaaaaaaaaaaa;
      local_2e0 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_2c8 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_2d0 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_2f8 = &SUB_aaaaaaaaaaaaaaaa;
      local_300 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_2e8 = &SUB_aaaaaaaaaaaaaaaa;
      local_2f0 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_318 = &SUB_aaaaaaaaaaaaaaaa;
      local_320 = &SUB_aaaaaaaaaaaaaaaa;
      local_308 = &SUB_aaaaaaaaaaaaaaaa;
      local_310 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_338 = &SUB_aaaaaaaaaaaaaaaa;
      local_340 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_328 = &SUB_aaaaaaaaaaaaaaaa;
      local_330 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_358 = &SUB_aaaaaaaaaaaaaaaa;
      pcStack_360 = (code *)&SUB_aaaaaaaaaaaaaaaa;
      local_348 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_350 = &SUB_aaaaaaaaaaaaaaaa;
      pcStack_378 = (code *)&SUB_aaaaaaaaaaaaaaaa;
      local_380 = (code *)&SUB_aaaaaaaaaaaaaaaa;
      local_368 = &SUB_aaaaaaaaaaaaaaaa;
      local_370 = (code *)&SUB_aaaaaaaaaaaaaaaa;
      uVar13 = FUN_04669774();
      FUN_0466ae88(&local_380,uVar13,0);
      if ((char)local_2c0 == '\x01') {
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (*plVar18 + 0x148,&local_380);
        if ((char)local_2c0 != '\x01') {
LAB_02fd8e14:
                    /* WARNING: Subroutine does not return */
          FUN_004d04d4();
        }
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (*plVar18 + 0x168,&pcStack_360);
        if (((char)local_2c0 != '\x01') ||
           (uVar13 = __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                               (*plVar18 + 0x198,&local_330), ((ulong)local_2c0 & 1) == 0))
        goto LAB_02fd8e14;
        *(undefined1 **)(*plVar18 + 0x160) = local_368;
      }
      else {
        uVar13 = thunk_FUN_05e1d97c(4);
        if ((int)uVar13 != 0) {
          FUN_0488143c(&local_2b0);
          pppppppuVar17 = local_2b0;
          if (-1 < (long)local_2a0) {
            pppppppuVar17 = &local_2b0;
          }
          if ((DAT_0a3d2361 & 1) == 0) {
            uRam000000000a3d2358._0_1_ = s_login_manager_ccauto_login_close_0889c040[8];
            uRam000000000a3d2358._1_1_ = s_login_manager_ccauto_login_close_0889c040[9];
            uRam000000000a3d2358._2_1_ = s_login_manager_ccauto_login_close_0889c040[10];
            uRam000000000a3d2358._3_1_ = s_login_manager_ccauto_login_close_0889c040[0xb];
            uRam000000000a3d2358._4_1_ = s_login_manager_ccauto_login_close_0889c040[0xc];
            uRam000000000a3d2358._5_1_ = s_login_manager_ccauto_login_close_0889c040[0xd];
            uRam000000000a3d2358._6_1_ = s_login_manager_ccauto_login_close_0889c040[0xe];
            uRam000000000a3d2358._7_1_ = s_login_manager_ccauto_login_close_0889c040[0xf];
            DAT_0a3d2350 = s_login_manager_ccauto_login_close_0889c040[0];
            DAT_0a3d2350_1._0_1_ = s_login_manager_ccauto_login_close_0889c040[1];
            DAT_0a3d2350_1._1_1_ = s_login_manager_ccauto_login_close_0889c040[2];
            DAT_0a3d2350_1._2_1_ = s_login_manager_ccauto_login_close_0889c040[3];
            DAT_0a3d2350_1._3_1_ = s_login_manager_ccauto_login_close_0889c040[4];
            DAT_0a3d2350_1._4_1_ = s_login_manager_ccauto_login_close_0889c040[5];
            DAT_0a3d2350_1._5_1_ = s_login_manager_ccauto_login_close_0889c040[6];
            DAT_0a3d2350_1._6_1_ = s_login_manager_ccauto_login_close_0889c040[7];
            DAT_0a3d2360 = 0;
            DAT_0a3d2361 = 1;
          }
          if ((DAT_0a3d2c37 & 1) == 0) {
            DAT_0a3d2c28._0_1_ = s_HandleAu_tim_0889c498[0];
            DAT_0a3d2c28._1_1_ = s_HandleAu_tim_0889c498[1];
            DAT_0a3d2c28._2_1_ = s_HandleAu_tim_0889c498[2];
            DAT_0a3d2c28._3_1_ = s_HandleAu_tim_0889c498[3];
            DAT_0a3d2c28._4_1_ = s_HandleAu_tim_0889c498[4];
            DAT_0a3d2c28._5_1_ = s_HandleAu_tim_0889c498[5];
            DAT_0a3d2c28._6_1_ = s_HandleAu_tim_0889c498[6];
            DAT_0a3d2c28._7_1_ = s_HandleAu_tim_0889c498[7];
            DAT_0a3d2c30 = (undefined4)DAT_087e31d8;
            DAT_0a3d2c34 = 0x7073;
            DAT_0a3d2c36 = 0;
            DAT_0a3d2c37 = 1;
          }
          FUN_05e1d050(&local_230,4,pppppppuVar17,&DAT_0a3d2350,&DAT_0a3d2c28,0x43a,0,0);
          if ((DAT_0a3d2d22 & 1) == 0) {
            uRam000000000a3d2d18._0_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x58];
            uRam000000000a3d2d18._1_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x59];
            uRam000000000a3d2d18._2_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x5a];
            uRam000000000a3d2d18._3_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x5b];
            uRam000000000a3d2d18._4_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x5c];
            uRam000000000a3d2d18._5_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x5d];
            uRam000000000a3d2d18._6_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x5e];
            uRam000000000a3d2d18._7_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x5f];
            DAT_0a3d2d10 = s_CheckLoginQRCodePCAccountName____0889c0b0[0x50];
            DAT_0a3d2d10_1._0_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x51];
            DAT_0a3d2d10_1._1_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x52];
            DAT_0a3d2d10_1._2_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x53];
            DAT_0a3d2d10_1._3_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x54];
            DAT_0a3d2d10_1._4_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x55];
            DAT_0a3d2d10_1._5_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x56];
            DAT_0a3d2d10_1._6_1_ = s_CheckLoginQRCodePCAccountName____0889c0b0[0x57];
            DAT_0a3d2d20 = 0x6f;
            DAT_0a3d2d22 = 1;
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
          uStack_f8 = (long *******)0x0;
          local_100 = (undefined8 ******)0x0;
          local_e8 = 0;
          local_f0 = (undefined8 *******)0x0;
          FUN_05e1d31c(&local_230,&DAT_0a3d2d10,&local_100);
          uVar13 = thunk_FUN_05e1d0bc(&local_230);
          if ((long)local_2a0 < 0) {
            uVar13 = __ZdlPvm(local_2b0,local_2a0 & 0x7fffffffffffffff);
          }
        }
      }
      if ((char)local_2c0 == '\x01') {
        uVar13 = FUN_002b5e18(&local_380);
      }
    }
    if ((long)local_288 < 0) {
      uVar13 = __ZdlPvm(local_298,local_288 & 0x7fffffffffffffff);
    }
    if ((long)local_270 < 0) {
      uVar13 = __ZdlPvm(local_280,local_270 & 0x7fffffffffffffff);
    }
    if ((long)local_190 < 0) {
      uVar13 = __ZdlPvm(local_1a0,local_190 & 0x7fffffffffffffff);
    }
    if ((long)local_140 < 0) {
      uVar13 = __ZdlPvm(local_150,local_140 & 0x7fffffffffffffff);
    }
  }
  if ((uVar1 >> 2 & 1) != 0) {
    lVar20 = *(long *)(*(long *)(param_3 + 8) + 0x20);
    if (lVar20 == 0) {
      lVar23 = *(long *)(*(long *)(DAT_0a520ca0 + 0x20) + 0x18);
      if (lVar23 != 0) goto LAB_02fd85c4;
LAB_02fd8708:
      lVar23 = *(long *)(DAT_0a520c78 + 0x18);
      if (lVar20 != 0) goto LAB_02fd85cc;
LAB_02fd8720:
      lVar24 = *(long *)(*(long *)(DAT_0a520ca0 + 0x20) + 0x10);
      if (lVar24 != 0) goto LAB_02fd85d4;
LAB_02fd8738:
      lVar24 = *(long *)(DAT_0a520c78 + 0x10);
      if (lVar20 != 0) goto LAB_02fd85d8;
LAB_02fd874c:
      lVar20 = *(long *)(*(long *)(DAT_0a520ca0 + 0x20) + 8);
    }
    else {
      lVar23 = *(long *)(lVar20 + 0x18);
      if (lVar23 == 0) goto LAB_02fd8708;
LAB_02fd85c4:
      if (lVar20 == 0) goto LAB_02fd8720;
LAB_02fd85cc:
      lVar24 = *(long *)(lVar20 + 0x10);
      if (lVar24 == 0) goto LAB_02fd8738;
LAB_02fd85d4:
      if (lVar20 == 0) goto LAB_02fd874c;
LAB_02fd85d8:
      lVar20 = *(long *)(lVar20 + 8);
    }
    if (lVar20 == 0) {
      lVar20 = *(long *)(DAT_0a520c78 + 8);
    }
    FUN_02fd60f4(uVar13,uVar11,0,lVar23,lVar24,lVar20);
  }
  if ((uVar1 & 1) == 0) {
LAB_02fd86c8:
    lVar20 = *(long *)(param_3 + 8);
  }
  else {
    pcStack_378 = (code *)0x0;
    local_370 = (code *)0x0;
    local_380 = (code *)0x0;
    lVar20 = *(long *)(*(long *)(param_3 + 8) + 0x10);
    if (lVar20 == 0) {
      lVar23 = *(long *)(*(long *)(DAT_0a520ca0 + 0x10) + 0x40);
    }
    else {
      lVar23 = *(long *)(lVar20 + 0x40);
    }
    if (lVar23 == 0) {
      lVar23 = *(long *)(DAT_0a520c80 + 0x40);
    }
    plVar16 = *(long **)(lVar23 + 8);
    if (*(char *)((long)plVar16 + 0x17) < '\0') {
      plVar16 = (long *)*plVar16;
      if (lVar20 != 0) goto LAB_02fd8620;
LAB_02fd87ac:
      lVar20 = *(long *)(*(long *)(DAT_0a520ca0 + 0x10) + 0x40);
    }
    else {
      if (lVar20 == 0) goto LAB_02fd87ac;
LAB_02fd8620:
      lVar20 = *(long *)(lVar20 + 0x40);
    }
    if (lVar20 == 0) {
      lVar20 = *(long *)(DAT_0a520c80 + 0x40);
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKcm
              (&local_380,plVar16,*(undefined4 *)(lVar20 + 0x10));
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (*plVar18 + 0x118,&local_380);
    plStack_228 = (long *)0x0;
    local_220 = (long *******)0x0;
    local_230 = (undefined8 *******)0x0;
    lVar20 = *(long *)(*(long *)(param_3 + 8) + 0x10);
    if (lVar20 == 0) {
      lVar23 = *(long *)(*(long *)(DAT_0a520ca0 + 0x10) + 0x48);
    }
    else {
      lVar23 = *(long *)(lVar20 + 0x48);
    }
    if (lVar23 == 0) {
      lVar23 = *(long *)(DAT_0a520c80 + 0x48);
    }
    plVar16 = *(long **)(lVar23 + 8);
    if (*(char *)((long)plVar16 + 0x17) < '\0') {
      plVar16 = (long *)*plVar16;
      if (lVar20 != 0) goto LAB_02fd8674;
LAB_02fd880c:
      lVar20 = *(long *)(*(long *)(DAT_0a520ca0 + 0x10) + 0x48);
    }
    else {
      if (lVar20 == 0) goto LAB_02fd880c;
LAB_02fd8674:
      lVar20 = *(long *)(lVar20 + 0x48);
    }
    if (lVar20 == 0) {
      lVar20 = *(long *)(DAT_0a520c80 + 0x48);
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKcm
              (&local_230,plVar16,*(undefined4 *)(lVar20 + 0x10));
    lVar20 = *(long *)(*(long *)(param_3 + 8) + 0x18);
    if (lVar20 == 0) {
      lVar20 = *(long *)(DAT_0a520ca0 + 0x18);
    }
    FUN_02fd9adc(param_2,*(undefined8 *)(lVar20 + 8),&local_230,1);
    if ((long)local_220 < 0) {
      __ZdlPvm(local_230,(ulong)local_220 & 0x7fffffffffffffff);
    }
    if (-1 < (long)local_370) goto LAB_02fd86c8;
    __ZdlPvm(local_380,(ulong)local_370 & 0x7fffffffffffffff);
    lVar20 = *(long *)(param_3 + 8);
  }
  if (((uVar1 >> 3 & 1) != 0) && ((*(byte *)(lVar20 + 0x38) >> 5 & 1) != 0)) {
    if (*(long *)(lVar20 + 0x28) == 0) {
      iVar10 = *(int *)(*(long *)(DAT_0a520ca0 + 0x28) + 0x10);
    }
    else {
      iVar10 = *(int *)(*(long *)(lVar20 + 0x28) + 0x10);
    }
    if (0 < iVar10) {
      FUN_05ab4028(&local_380);
      lVar20 = *plVar18;
      if (*(char *)(lVar20 + 0x147) < '\0') {
        __ZdlPvm(*(undefined8 *)(lVar20 + 0x130),*(ulong *)(lVar20 + 0x140) & 0x7fffffffffffffff);
      }
      *(code **)(lVar20 + 0x138) = pcStack_378;
      *(code **)(lVar20 + 0x130) = local_380;
      *(code **)(lVar20 + 0x140) = local_370;
      lVar20 = *(long *)(param_3 + 8);
    }
  }
  lVar20 = *(long *)(lVar20 + 0x10);
  if (lVar20 == 0) {
    lVar20 = *(long *)(DAT_0a520ca0 + 0x10);
  }
  *(undefined4 *)(param_2 + 0x284) = *(undefined4 *)(lVar20 + 0x80);
  pcStack_378 = (code *)&SUB_aaaaaaaaaaaaaaaa;
  local_370 = (code *)&SUB_aaaaaaaaaaaaaaaa;
  local_380 = (code *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_050c72a4(&local_380);
  if (*(long *)(*(long *)(param_3 + 8) + 0x10) == 0) {
    lVar20 = *(long *)(*(long *)(DAT_0a520ca0 + 0x10) + 0xb0);
  }
  else {
    lVar20 = *(long *)(*(long *)(*(long *)(param_3 + 8) + 0x10) + 0xb0);
  }
  if (lVar20 == 0) {
    lVar20 = *(long *)(DAT_0a520c80 + 0xb0);
  }
  iVar10 = FUN_05ab38ec(&local_380,*(undefined8 *)(lVar20 + 8));
  if (iVar10 != 0) {
    pcVar21 = pcStack_378;
    if (pcStack_378 == (code *)0x0) {
      pcVar21 = *(code **)(DAT_0a520cd0 + 8);
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (*plVar18 + 0x240,*(undefined8 *)(pcVar21 + 8));
  }
  lVar20 = *(long *)(*(long *)(param_3 + 8) + 0x20);
  if (lVar20 == 0) {
    lVar23 = *(long *)(*(long *)(DAT_0a520ca0 + 0x20) + 0x28);
  }
  else {
    lVar23 = *(long *)(lVar20 + 0x28);
  }
  if (lVar23 == 0) {
    lVar23 = *(long *)(DAT_0a520c78 + 0x28);
  }
  plVar16 = *(long **)(lVar23 + 8);
  if (*(char *)((long)plVar16 + 0x17) < '\0') {
    plVar16 = (long *)*plVar16;
  }
  if (lVar20 == 0) {
    lVar20 = *(long *)(DAT_0a520ca0 + 0x20);
  }
  lVar20 = *(long *)(lVar20 + 0x28);
  if (lVar20 == 0) {
    lVar20 = *(long *)(DAT_0a520c78 + 0x28);
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKcm
            (*plVar18 + 0x228,plVar16,*(undefined4 *)(lVar20 + 0x10));
  plVar18 = *(long **)(param_2 + 0x278);
  if (plVar18 != (long *)0x0) {
    *(undefined8 *)(param_2 + 0x278) = 0;
    (**(code **)(*plVar18 + 8))();
  }
  *(undefined2 *)(param_2 + 0x280) = 0;
  FUN_050e5a70(&local_380);
LAB_02fd8d58:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_78) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


