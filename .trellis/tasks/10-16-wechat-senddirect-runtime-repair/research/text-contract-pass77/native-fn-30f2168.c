// Ghidra inferred pseudocode; requested=0x30f2168
// entry=030f2168 end=030f2737

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_030f2168(long *param_1,long param_2)

{
  long *plVar1;
  undefined8 *****pppppuVar2;
  int iVar3;
  undefined8 uVar4;
  size_t sVar5;
  ulong uVar6;
  long lVar7;
  undefined8 ****local_350 [2];
  undefined7 local_340;
  char cStack_339;
  undefined8 ****local_338 [2];
  undefined7 local_328;
  char cStack_321;
  undefined8 ****local_320;
  ulong uStack_318;
  undefined7 local_310;
  byte bStack_309;
  undefined **local_290 [4];
  undefined1 *puStack_270;
  undefined1 *puStack_268;
  undefined1 *local_260;
  undefined1 *puStack_258;
  undefined1 *puStack_250;
  undefined1 *puStack_248;
  undefined1 *local_240;
  undefined1 *puStack_238;
  undefined1 *puStack_230;
  undefined1 *local_228;
  undefined1 *local_220;
  undefined1 *puStack_218;
  undefined1 *puStack_210;
  undefined1 *puStack_208;
  undefined1 *local_200;
  undefined1 *puStack_1f8;
  undefined1 *puStack_1f0;
  undefined1 *puStack_1e8;
  undefined1 *local_1e0;
  undefined1 *puStack_1d8;
  undefined1 *puStack_1d0;
  undefined1 *puStack_1c8;
  undefined1 *local_1c0;
  undefined1 *puStack_1b8;
  undefined1 *puStack_1b0;
  undefined1 *puStack_1a8;
  undefined1 *local_1a0;
  undefined1 *puStack_198;
  undefined1 *puStack_190;
  undefined1 *puStack_188;
  undefined1 *local_180;
  long *local_170;
  undefined1 local_168;
  undefined8 ****local_120;
  undefined1 local_118;
  undefined7 local_110;
  char cStack_109;
  undefined8 ****local_d0;
  long **pplStack_c8;
  undefined8 local_c0;
  undefined8 uStack_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 local_60;
  undefined8 uStack_58;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  plVar1 = (long *)(param_2 + 0xb8);
  if (*(char *)(param_2 + 0xcf) < '\0') {
    if (*(long *)(param_2 + 0xc0) != 0) {
      if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
        FUN_00018d20(param_1,*plVar1);
        return;
      }
      goto LAB_030f2734;
    }
LAB_030f21fc:
    local_180 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_198 = &SUB_aaaaaaaaaaaaaaaa;
    local_1a0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_188 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_190 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_1b8 = &SUB_aaaaaaaaaaaaaaaa;
    local_1c0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_1a8 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_1b0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_1d8 = &SUB_aaaaaaaaaaaaaaaa;
    local_1e0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_1c8 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_1d0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_1f8 = &SUB_aaaaaaaaaaaaaaaa;
    local_200 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_1e8 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_1f0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_218 = &SUB_aaaaaaaaaaaaaaaa;
    local_220 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_208 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_210 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_238 = &SUB_aaaaaaaaaaaaaaaa;
    local_240 = &SUB_aaaaaaaaaaaaaaaa;
    local_228 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_230 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_258 = &SUB_aaaaaaaaaaaaaaaa;
    local_260 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_248 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_250 = &SUB_aaaaaaaaaaaaaaaa;
    local_290[3] = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
    local_290[2] = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
    puStack_268 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_270 = &SUB_aaaaaaaaaaaaaaaa;
    local_290[1] = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
    local_290[0] = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
    FUN_003b064c(local_290);
    if (*(long *)(param_2 + 0x18) == 0) {
      iVar3 = thunk_FUN_05e1d97c(4);
      if (iVar3 != 0) {
        FUN_0488143c(&local_120);
        pppppuVar2 = (undefined8 *****)local_120;
        if (-1 < cStack_109) {
          pppppuVar2 = &local_120;
        }
        if ((DAT_0a3d9838 & 1) == 0) {
          uVar6 = 0;
          do {
            (&DAT_0a3d9820)[uVar6] = (&DAT_088b055e)[uVar6] + 0x8a ^ (&DAT_088b054e)[uVar6 & 0xf];
            uVar6 = uVar6 + 1;
          } while (uVar6 != 0x18);
          DAT_0a3d9838 = 1;
        }
        if ((DAT_0a3d98d0 & 1) == 0) {
          uRam000000000a3d98c8._0_1_ = s_GetSendClientId_088b02e0[8];
          uRam000000000a3d98c8._1_1_ = s_GetSendClientId_088b02e0[9];
          uRam000000000a3d98c8._2_1_ = s_GetSendClientId_088b02e0[10];
          uRam000000000a3d98c8._3_1_ = s_GetSendClientId_088b02e0[0xb];
          uRam000000000a3d98c8._4_1_ = s_GetSendClientId_088b02e0[0xc];
          uRam000000000a3d98c8._5_1_ = s_GetSendClientId_088b02e0[0xd];
          uRam000000000a3d98c8._6_1_ = s_GetSendClientId_088b02e0[0xe];
          uRam000000000a3d98c8._7_1_ = s_GetSendClientId_088b02e0[0xf];
          DAT_0a3d98c0 = s_GetSendClientId_088b02e0[0];
          DAT_0a3d98c0_1._0_1_ = s_GetSendClientId_088b02e0[1];
          DAT_0a3d98c0_1._1_1_ = s_GetSendClientId_088b02e0[2];
          DAT_0a3d98c0_1._2_1_ = s_GetSendClientId_088b02e0[3];
          DAT_0a3d98c0_1._3_1_ = s_GetSendClientId_088b02e0[4];
          DAT_0a3d98c0_1._4_1_ = s_GetSendClientId_088b02e0[5];
          DAT_0a3d98c0_1._5_1_ = s_GetSendClientId_088b02e0[6];
          DAT_0a3d98c0_1._6_1_ = s_GetSendClientId_088b02e0[7];
          DAT_0a3d98d0 = 1;
        }
        FUN_05e1d050(&local_320,4,pppppuVar2,&DAT_0a3d9820,&DAT_0a3d98c0,0xd1,0,0);
        if ((DAT_0a3d98f8 & 1) == 0) {
          uVar6 = 0;
          do {
            (&DAT_0a3d98d1)[uVar6] = (&DAT_088b065a)[uVar6] + 0x8a ^ (&DAT_088b064a)[uVar6 & 0xf];
            uVar6 = uVar6 + 1;
          } while (uVar6 != 0x27);
          DAT_0a3d98f8 = 1;
        }
        uStack_68 = 0;
        local_70 = 0;
        uStack_58 = 0;
        local_60 = 0;
        uStack_88 = 0;
        local_90 = 0;
        uStack_78 = 0;
        local_80 = 0;
        uStack_a8 = 0;
        local_b0 = 0;
        uStack_98 = 0;
        local_a0 = 0;
        pplStack_c8 = (long **)0x0;
        local_d0 = (undefined8 *****)0x0;
        uStack_b8 = 0;
        local_c0 = 0;
        FUN_05e1d31c(&local_320,&DAT_0a3d98d1,&local_d0);
        thunk_FUN_05e1d0bc(&local_320);
        if (cStack_109 < '\0') {
          __ZdlPvm(local_120,CONCAT17(cStack_109,local_110) & 0x7fffffffffffffff);
        }
      }
      DAT_0a05a2b8 = DAT_0a05a2b8 + 1;
      __ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEElsEy(local_290 + 2);
    }
    else {
      FUN_04cbe440(&local_320);
      uVar6 = uStack_318;
      pppppuVar2 = (undefined8 *****)local_320;
      if (-1 < (char)bStack_309) {
        uVar6 = (ulong)bStack_309;
        pppppuVar2 = &local_320;
      }
      uVar4 = FUN_003b1afc(local_290 + 2,pppppuVar2,uVar6);
      if ((DAT_0a3d98ba & 1) == 0) {
        DAT_0a3d98b0._0_1_ = s_sending__xwechatSetSendS_088b02f0[8];
        DAT_0a3d98b0._1_1_ = s_sending__xwechatSetSendS_088b02f0[9];
        DAT_0a3d98b0._2_1_ = s_sending__xwechatSetSendS_088b02f0[10];
        DAT_0a3d98b0._3_1_ = s_sending__xwechatSetSendS_088b02f0[0xb];
        DAT_0a3d98b0._4_1_ = s_sending__xwechatSetSendS_088b02f0[0xc];
        DAT_0a3d98b0._5_1_ = s_sending__xwechatSetSendS_088b02f0[0xd];
        DAT_0a3d98b0._6_1_ = s_sending__xwechatSetSendS_088b02f0[0xe];
        DAT_0a3d98b0._7_1_ = s_sending__xwechatSetSendS_088b02f0[0xf];
        DAT_0a3d98b8 = 0x5f;
        DAT_0a3d98ba = 1;
      }
      sVar5 = _strlen((char *)&DAT_0a3d98b0);
      FUN_003b1afc(uVar4,&DAT_0a3d98b0,sVar5);
      DAT_0a05a2b8 = DAT_0a05a2b8 + 1;
      __ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEElsEy();
      if ((char)bStack_309 < '\0') {
        __ZdlPvm(local_320,CONCAT17(bStack_309,local_310) & 0x7fffffffffffffff);
      }
    }
    FUN_05f96e3c(&local_320,local_290 + 3);
    if (*(char *)(param_2 + 0xcf) < '\0') {
      __ZdlPvm(*(undefined8 *)(param_2 + 0xb8),*(ulong *)(param_2 + 200) & 0x7fffffffffffffff);
    }
    *(ulong *)(param_2 + 0xc0) = uStack_318;
    *plVar1 = (long)local_320;
    *(ulong *)(param_2 + 200) = CONCAT17(bStack_309,local_310);
    iVar3 = thunk_FUN_05e1d97c(2);
    if (iVar3 == 0) {
LAB_030f2660:
      if (-1 < *(char *)(param_2 + 0xcf)) goto LAB_030f2668;
LAB_030f2694:
      FUN_00018d20(param_1,*(undefined8 *)(param_2 + 0xb8),*(undefined8 *)(param_2 + 0xc0));
    }
    else {
      FUN_0488143c(local_338);
      pppppuVar2 = (undefined8 *****)local_338[0];
      if (-1 < cStack_321) {
        pppppuVar2 = local_338;
      }
      if ((DAT_0a3d9838 & 1) == 0) {
        uVar6 = 0;
        do {
          (&DAT_0a3d9820)[uVar6] = (&DAT_088b055e)[uVar6] + 0x8a ^ (&DAT_088b054e)[uVar6 & 0xf];
          uVar6 = uVar6 + 1;
        } while (uVar6 != 0x18);
        DAT_0a3d9838 = 1;
      }
      if ((DAT_0a3d98d0 & 1) == 0) {
        uRam000000000a3d98c8._0_1_ = s_GetSendClientId_088b02e0[8];
        uRam000000000a3d98c8._1_1_ = s_GetSendClientId_088b02e0[9];
        uRam000000000a3d98c8._2_1_ = s_GetSendClientId_088b02e0[10];
        uRam000000000a3d98c8._3_1_ = s_GetSendClientId_088b02e0[0xb];
        uRam000000000a3d98c8._4_1_ = s_GetSendClientId_088b02e0[0xc];
        uRam000000000a3d98c8._5_1_ = s_GetSendClientId_088b02e0[0xd];
        uRam000000000a3d98c8._6_1_ = s_GetSendClientId_088b02e0[0xe];
        uRam000000000a3d98c8._7_1_ = s_GetSendClientId_088b02e0[0xf];
        DAT_0a3d98c0 = s_GetSendClientId_088b02e0[0];
        DAT_0a3d98c0_1._0_1_ = s_GetSendClientId_088b02e0[1];
        DAT_0a3d98c0_1._1_1_ = s_GetSendClientId_088b02e0[2];
        DAT_0a3d98c0_1._2_1_ = s_GetSendClientId_088b02e0[3];
        DAT_0a3d98c0_1._3_1_ = s_GetSendClientId_088b02e0[4];
        DAT_0a3d98c0_1._4_1_ = s_GetSendClientId_088b02e0[5];
        DAT_0a3d98c0_1._5_1_ = s_GetSendClientId_088b02e0[6];
        DAT_0a3d98c0_1._6_1_ = s_GetSendClientId_088b02e0[7];
        DAT_0a3d98d0 = 1;
      }
      FUN_05e1d050(&local_320,2,pppppuVar2,&DAT_0a3d9820,&DAT_0a3d98c0,0xd6,0,0);
      FUN_04cbe440(local_350,*(undefined8 *)(param_2 + 0x18));
      local_120 = local_350[0];
      if (-1 < cStack_339) {
        local_120 = local_350;
      }
      local_118 = 0;
      local_170 = *(long **)(param_2 + 0xb8);
      if (-1 < *(char *)(param_2 + 0xcf)) {
        local_170 = plVar1;
      }
      local_168 = 0;
      if ((DAT_0a3d9918 & 1) == 0) {
        uVar6 = 0;
        do {
          (&DAT_0a3d98f9)[uVar6] = (&DAT_088b0691)[uVar6] + 0x8a ^ (&DAT_088b0681)[uVar6 & 0xf];
          uVar6 = uVar6 + 1;
        } while (uVar6 != 0x1f);
        DAT_0a3d9918 = 1;
      }
      local_d0 = &local_120;
      pplStack_c8 = &local_170;
      uStack_b8 = 0;
      local_c0 = 0;
      uStack_a8 = 0;
      local_b0 = 0;
      uStack_98 = 0;
      local_a0 = 0;
      uStack_88 = 0;
      local_90 = 0;
      uStack_78 = 0;
      local_80 = 0;
      uStack_68 = 0;
      local_70 = 0;
      uStack_58 = 0;
      local_60 = 0;
      FUN_05e1d31c(&local_320,&DAT_0a3d98f9,&local_d0);
      if (cStack_339 < '\0') {
        __ZdlPvm(local_350[0],CONCAT17(cStack_339,local_340) & 0x7fffffffffffffff);
      }
      thunk_FUN_05e1d0bc(&local_320);
      if (-1 < cStack_321) goto LAB_030f2660;
      __ZdlPvm(local_338[0],CONCAT17(cStack_321,local_328) & 0x7fffffffffffffff);
      if (*(char *)(param_2 + 0xcf) < '\0') goto LAB_030f2694;
LAB_030f2668:
      lVar7 = *plVar1;
      param_1[1] = *(long *)(param_2 + 0xc0);
      *param_1 = lVar7;
      param_1[2] = *(long *)(param_2 + 200);
    }
    local_290[0] = (undefined **)PTR_PTR_09f2b418;
    *(undefined **)((long)local_290 + *(long *)(PTR_PTR_09f2b418 + -0x18)) = PTR_PTR_09f2b458;
    local_290[2] = (undefined **)PTR_PTR_09f2b460;
    local_290[3] = &PTR_FUN_09f2b5a8;
    if ((long)local_228 < 0) {
      __ZdlPvm(puStack_238,(ulong)local_228 & 0x7fffffffffffffff);
    }
    __ZNSt3__115basic_streambufIcNS_11char_traitsIcEEED2Ev(local_290 + 3);
    __ZNSt3__114basic_iostreamIcNS_11char_traitsIcEEED2Ev(local_290,&PTR_PTR_09f2b420);
    __ZNSt3__19basic_iosIcNS_11char_traitsIcEEED2Ev(&puStack_210);
  }
  else {
    if (*(char *)(param_2 + 0xcf) == '\0') goto LAB_030f21fc;
    lVar7 = *plVar1;
    param_1[1] = *(long *)(param_2 + 0xc0);
    *param_1 = lVar7;
    param_1[2] = *(long *)(param_2 + 200);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
LAB_030f2734:
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


