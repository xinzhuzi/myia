// Ghidra inferred pseudocode; requested=0x3092230
// entry=03092230 end=03093afb

/* WARNING: Removing unreachable block (ram,0x03092fe8) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_03092230(undefined8 *param_1,undefined8 param_2,long *param_3)

{
  undefined8 *******pppppppuVar1;
  long lVar2;
  long *plVar3;
  long lVar4;
  undefined1 *puVar5;
  int iVar6;
  uint uVar7;
  undefined1 *puVar8;
  undefined8 ******ppppppuVar9;
  long *plVar10;
  undefined8 uVar11;
  long lVar12;
  undefined8 *puVar13;
  ulong uVar14;
  ulong uVar15;
  undefined1 *puVar16;
  long local_510;
  long *plStack_508;
  undefined8 *******local_500 [2];
  undefined7 local_4f0;
  char cStack_4e9;
  long local_4e8;
  long lStack_4e0;
  long local_4d8;
  long *plStack_4d0;
  undefined8 *******local_4c8 [2];
  undefined7 local_4b8;
  char cStack_4b1;
  undefined8 local_4b0;
  undefined1 *puStack_4a8;
  undefined1 *local_4a0;
  undefined1 *puStack_498;
  undefined1 *local_490;
  long *local_488;
  long local_478;
  long *plStack_470;
  long local_468;
  long lStack_460;
  long local_458;
  long *plStack_450;
  long local_448;
  long *local_440;
  undefined1 *local_438;
  undefined1 *local_430;
  undefined1 *local_428;
  undefined1 *local_420;
  undefined1 *puStack_418;
  undefined1 *local_410;
  long *local_400;
  long *local_3f8;
  undefined8 local_3f0;
  undefined1 *puStack_3e8;
  undefined1 *local_3e0;
  undefined1 *puStack_3d8;
  undefined1 *local_3d0;
  long *local_3c8;
  undefined8 local_3c0;
  undefined8 local_3b8;
  ulong local_3b0;
  ulong local_3a8;
  undefined1 local_3a0;
  undefined4 local_39c;
  long local_330;
  long *local_328;
  long local_320;
  long *local_318;
  undefined8 *******local_310;
  undefined1 local_308;
  undefined7 local_300;
  char cStack_2f9;
  undefined8 *******local_2c0;
  undefined8 ******ppppppuStack_2b8;
  undefined7 local_2b0;
  char cStack_2a9;
  undefined8 local_270;
  undefined8 *****pppppuStack_268;
  undefined1 *local_260;
  undefined1 *puStack_258;
  undefined8 *local_250;
  long *local_248;
  undefined8 *******local_220;
  undefined8 ******ppppppuStack_218;
  undefined1 *local_210;
  undefined1 *puStack_208;
  undefined8 *local_200;
  undefined8 uStack_1f8;
  undefined1 *puStack_1f0;
  undefined1 *puStack_1e8;
  undefined8 local_1e0;
  undefined1 *puStack_1d8;
  undefined1 *puStack_1d0;
  undefined8 uStack_1c8;
  undefined8 *******local_1c0;
  undefined8 *puStack_1b8;
  undefined8 *local_1b0;
  undefined8 *puStack_1a8;
  undefined8 local_1a0;
  undefined8 *local_198;
  undefined8 *local_190;
  undefined8 uStack_188;
  undefined1 *puStack_180;
  undefined1 *puStack_178;
  undefined8 *local_170;
  undefined8 *puStack_168;
  undefined8 *local_160;
  undefined1 *puStack_158;
  undefined8 local_150;
  undefined8 *******local_140;
  undefined1 local_138;
  undefined7 local_130;
  char cStack_129;
  undefined8 *******local_f0;
  undefined8 *******pppppppuStack_e8;
  undefined8 *******local_e0;
  undefined8 *******pppppppuStack_d8;
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
  undefined8 uStack_78;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  FUN_030f3214(*param_3,10);
  lVar12 = *param_3;
  lVar4 = *(long *)(lVar12 + 0x18);
  local_318 = *(long **)(lVar12 + 0x20);
  if (local_318 != (long *)0x0) {
    local_318[1] = local_318[1] + 1;
    lVar12 = *param_3;
  }
  lVar2 = *(long *)(lVar12 + 0x28);
  local_328 = *(long **)(lVar12 + 0x30);
  lVar12 = 0;
  if (local_328 != (long *)0x0) {
    lVar12 = local_328[1];
    local_328[1] = lVar12 + 1;
  }
  local_330 = lVar2;
  local_320 = lVar4;
  if (lVar4 == 0 || lVar2 == 0) {
    iVar6 = thunk_FUN_05e1d97c(4);
    if (iVar6 != 0) {
      FUN_0488143c(&local_1c0);
      pppppppuVar1 = local_1c0;
      if (-1 < (long)local_1b0) {
        pppppppuVar1 = &local_1c0;
      }
      if ((DAT_0a3d6ca3 & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3d6c8b)[uVar14] = (&DAT_088a98e8)[uVar14] + 0x8a ^ (&DAT_088a98d8)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x18);
        DAT_0a3d6ca3 = 1;
      }
      if ((DAT_0a3d70b0 & 1) == 0) {
        uRam000000000a3d70a8._0_1_ = s_CoSendAppMsgCgi_088a8fb0[8];
        uRam000000000a3d70a8._1_1_ = s_CoSendAppMsgCgi_088a8fb0[9];
        uRam000000000a3d70a8._2_1_ = s_CoSendAppMsgCgi_088a8fb0[10];
        uRam000000000a3d70a8._3_1_ = s_CoSendAppMsgCgi_088a8fb0[0xb];
        uRam000000000a3d70a8._4_1_ = s_CoSendAppMsgCgi_088a8fb0[0xc];
        uRam000000000a3d70a8._5_1_ = s_CoSendAppMsgCgi_088a8fb0[0xd];
        uRam000000000a3d70a8._6_1_ = s_CoSendAppMsgCgi_088a8fb0[0xe];
        uRam000000000a3d70a8._7_1_ = s_CoSendAppMsgCgi_088a8fb0[0xf];
        DAT_0a3d70a0 = s_CoSendAppMsgCgi_088a8fb0[0];
        DAT_0a3d70a0_1._0_1_ = s_CoSendAppMsgCgi_088a8fb0[1];
        DAT_0a3d70a0_1._1_1_ = s_CoSendAppMsgCgi_088a8fb0[2];
        DAT_0a3d70a0_1._2_1_ = s_CoSendAppMsgCgi_088a8fb0[3];
        DAT_0a3d70a0_1._3_1_ = s_CoSendAppMsgCgi_088a8fb0[4];
        DAT_0a3d70a0_1._4_1_ = s_CoSendAppMsgCgi_088a8fb0[5];
        DAT_0a3d70a0_1._5_1_ = s_CoSendAppMsgCgi_088a8fb0[6];
        DAT_0a3d70a0_1._6_1_ = s_CoSendAppMsgCgi_088a8fb0[7];
        DAT_0a3d70b0 = 1;
      }
      FUN_05e1d050(&local_3c0,4,pppppppuVar1,&DAT_0a3d6c8b,&DAT_0a3d70a0,0x1a9,0,0);
      if ((DAT_0a3d6ff2 & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3d6fc6)[uVar14] = (&DAT_088a9d73)[uVar14] + 0x8a ^ (&DAT_088a9d63)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x2c);
        DAT_0a3d6ff2 = 1;
      }
      uStack_88 = 0;
      local_90 = 0;
      uStack_78 = 0;
      local_80 = 0;
      uStack_a8 = 0;
      local_b0 = 0;
      uStack_98 = 0;
      local_a0 = 0;
      uStack_c8 = 0;
      local_d0 = 0;
      uStack_b8 = 0;
      local_c0 = 0;
      pppppppuStack_e8 = (undefined8 *******)0x0;
      local_f0 = (undefined8 *******)0x0;
      pppppppuStack_d8 = (undefined8 *******)0x0;
      local_e0 = (undefined8 *******)0x0;
      FUN_05e1d31c(&local_3c0,&DAT_0a3d6fc6,&local_f0);
      thunk_FUN_05e1d0bc(&local_3c0);
      if ((long)local_1b0 < 0) {
        __ZdlPvm(local_1c0,(ulong)local_1b0 & 0x7fffffffffffffff);
      }
    }
    FUN_030f6650(param_1,1,1,4,400);
    goto LAB_030937c8;
  }
  puStack_3d8 = &SUB_aaaaaaaaaaaaaaaa;
  local_3e0 = &SUB_aaaaaaaaaaaaaaaa;
  local_3c8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_3d0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_3e8 = &SUB_aaaaaaaaaaaaaaaa;
  local_3f0 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0304f1cc(lVar12,&local_3f0,0,0);
  if (*(char *)(lVar2 + 0x80) == '\x01') {
    iVar6 = thunk_FUN_05e1d97c(2);
    if (iVar6 != 0) {
      FUN_0488143c(&local_220);
      pppppppuVar1 = local_220;
      if (-1 < (long)local_210) {
        pppppppuVar1 = &local_220;
      }
      if ((DAT_0a3d6ca3 & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3d6c8b)[uVar14] = (&DAT_088a98e8)[uVar14] + 0x8a ^ (&DAT_088a98d8)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x18);
        DAT_0a3d6ca3 = 1;
      }
      if ((DAT_0a3d70b0 & 1) == 0) {
        uRam000000000a3d70a8._0_1_ = s_CoSendAppMsgCgi_088a8fb0[8];
        uRam000000000a3d70a8._1_1_ = s_CoSendAppMsgCgi_088a8fb0[9];
        uRam000000000a3d70a8._2_1_ = s_CoSendAppMsgCgi_088a8fb0[10];
        uRam000000000a3d70a8._3_1_ = s_CoSendAppMsgCgi_088a8fb0[0xb];
        uRam000000000a3d70a8._4_1_ = s_CoSendAppMsgCgi_088a8fb0[0xc];
        uRam000000000a3d70a8._5_1_ = s_CoSendAppMsgCgi_088a8fb0[0xd];
        uRam000000000a3d70a8._6_1_ = s_CoSendAppMsgCgi_088a8fb0[0xe];
        uRam000000000a3d70a8._7_1_ = s_CoSendAppMsgCgi_088a8fb0[0xf];
        DAT_0a3d70a0 = s_CoSendAppMsgCgi_088a8fb0[0];
        DAT_0a3d70a0_1._0_1_ = s_CoSendAppMsgCgi_088a8fb0[1];
        DAT_0a3d70a0_1._1_1_ = s_CoSendAppMsgCgi_088a8fb0[2];
        DAT_0a3d70a0_1._2_1_ = s_CoSendAppMsgCgi_088a8fb0[3];
        DAT_0a3d70a0_1._3_1_ = s_CoSendAppMsgCgi_088a8fb0[4];
        DAT_0a3d70a0_1._4_1_ = s_CoSendAppMsgCgi_088a8fb0[5];
        DAT_0a3d70a0_1._5_1_ = s_CoSendAppMsgCgi_088a8fb0[6];
        DAT_0a3d70a0_1._6_1_ = s_CoSendAppMsgCgi_088a8fb0[7];
        DAT_0a3d70b0 = 1;
      }
      FUN_05e1d050(&local_3c0,2,pppppppuVar1,&DAT_0a3d6c8b,&DAT_0a3d70a0,0x1b0,0,0);
      FUN_04cbe440(&local_140,local_320);
      local_1c0 = local_140;
      if (-1 < cStack_129) {
        local_1c0 = &local_140;
      }
      puStack_1b8 = (undefined8 *)((ulong)puStack_1b8 & 0xffffffffffffff00);
      if ((DAT_0a3d70dc & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3d70b1)[uVar14] = (&DAT_088a9ed3)[uVar14] + 0x8a ^ (&DAT_088a9ec3)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x2b);
        DAT_0a3d70dc = 1;
      }
      local_e0 = (undefined8 *******)0x0;
      pppppppuStack_e8 = (undefined8 *******)0x0;
      local_f0 = &local_1c0;
      local_d0 = 0;
      pppppppuStack_d8 = (undefined8 *******)0x0;
      local_c0 = 0;
      uStack_c8 = 0;
      local_b0 = 0;
      uStack_b8 = 0;
      local_a0 = 0;
      uStack_a8 = 0;
      local_90 = 0;
      uStack_98 = 0;
      local_80 = 0;
      uStack_88 = 0;
      uStack_78 = 0;
      FUN_05e1d31c(&local_3c0,&DAT_0a3d70b1,&local_f0);
      if (cStack_129 < '\0') {
        __ZdlPvm(local_140,CONCAT17(cStack_129,local_130) & 0x7fffffffffffffff);
      }
      thunk_FUN_05e1d0bc(&local_3c0);
      if ((long)local_210 < 0) {
        __ZdlPvm(local_220,(ulong)local_210 & 0x7fffffffffffffff);
      }
    }
    *param_1 = local_3f0;
    if ((long)puStack_3d8 < 0) {
      FUN_00018d20(param_1 + 1,puStack_3e8,local_3e0);
    }
    else {
      puVar13 = (undefined8 *)((ulong)&local_3f0 | 8);
      uVar11 = *puVar13;
      param_1[2] = puVar13[1];
      param_1[1] = uVar11;
      param_1[3] = puVar13[2];
    }
    param_1[4] = local_3d0;
    param_1[5] = local_3c8;
    if (local_3c8 != (long *)0x0) {
      local_3c8[1] = local_3c8[1] + 1;
    }
  }
  else {
    *(undefined1 *)(lVar2 + 0x80) = 1;
    if ((*(long *)(lVar4 + 0x220) == 0) ||
       (local_400 = (long *)___dynamic_cast(*(long *)(lVar4 + 0x220),&PTR_DAT_09eb1040,
                                            &PTR_DAT_09eb0cc0,0), local_400 == (long *)0x0)) {
      local_400 = (long *)0x0;
      local_3f8 = (long *)0x0;
      iVar6 = thunk_FUN_05e1d97c(4);
      if (iVar6 != 0) {
        FUN_0488143c(&local_1c0);
        pppppppuVar1 = local_1c0;
        if (-1 < (long)local_1b0) {
          pppppppuVar1 = &local_1c0;
        }
        if ((DAT_0a3d6ca3 & 1) == 0) {
          uVar14 = 0;
          do {
            (&DAT_0a3d6c8b)[uVar14] = (&DAT_088a98e8)[uVar14] + 0x8a ^ (&DAT_088a98d8)[uVar14 & 0xf]
            ;
            uVar14 = uVar14 + 1;
          } while (uVar14 != 0x18);
          DAT_0a3d6ca3 = 1;
        }
        if ((DAT_0a3d70b0 & 1) == 0) {
          uRam000000000a3d70a8._0_1_ = s_CoSendAppMsgCgi_088a8fb0[8];
          uRam000000000a3d70a8._1_1_ = s_CoSendAppMsgCgi_088a8fb0[9];
          uRam000000000a3d70a8._2_1_ = s_CoSendAppMsgCgi_088a8fb0[10];
          uRam000000000a3d70a8._3_1_ = s_CoSendAppMsgCgi_088a8fb0[0xb];
          uRam000000000a3d70a8._4_1_ = s_CoSendAppMsgCgi_088a8fb0[0xc];
          uRam000000000a3d70a8._5_1_ = s_CoSendAppMsgCgi_088a8fb0[0xd];
          uRam000000000a3d70a8._6_1_ = s_CoSendAppMsgCgi_088a8fb0[0xe];
          uRam000000000a3d70a8._7_1_ = s_CoSendAppMsgCgi_088a8fb0[0xf];
          DAT_0a3d70a0 = s_CoSendAppMsgCgi_088a8fb0[0];
          DAT_0a3d70a0_1._0_1_ = s_CoSendAppMsgCgi_088a8fb0[1];
          DAT_0a3d70a0_1._1_1_ = s_CoSendAppMsgCgi_088a8fb0[2];
          DAT_0a3d70a0_1._2_1_ = s_CoSendAppMsgCgi_088a8fb0[3];
          DAT_0a3d70a0_1._3_1_ = s_CoSendAppMsgCgi_088a8fb0[4];
          DAT_0a3d70a0_1._4_1_ = s_CoSendAppMsgCgi_088a8fb0[5];
          DAT_0a3d70a0_1._5_1_ = s_CoSendAppMsgCgi_088a8fb0[6];
          DAT_0a3d70a0_1._6_1_ = s_CoSendAppMsgCgi_088a8fb0[7];
          DAT_0a3d70b0 = 1;
        }
        FUN_05e1d050(&local_3c0,4,pppppppuVar1,&DAT_0a3d6c8b,&DAT_0a3d70a0,0x1b6,0,0);
        if ((DAT_0a3d6d11 & 1) == 0) {
          uVar14 = 0;
          do {
            (&DAT_0a3d6cfc)[uVar14] = (&DAT_088a998a)[uVar14] + 0x8a ^ (&DAT_088a997a)[uVar14 & 0xf]
            ;
            uVar14 = uVar14 + 1;
          } while (uVar14 != 0x15);
          DAT_0a3d6d11 = 1;
        }
        uStack_88 = 0;
        local_90 = 0;
        uStack_78 = 0;
        local_80 = 0;
        uStack_a8 = 0;
        local_b0 = 0;
        uStack_98 = 0;
        local_a0 = 0;
        uStack_c8 = 0;
        local_d0 = 0;
        uStack_b8 = 0;
        local_c0 = 0;
        pppppppuStack_e8 = (undefined8 *******)0x0;
        local_f0 = (undefined8 *******)0x0;
        pppppppuStack_d8 = (undefined8 *******)0x0;
        local_e0 = (undefined8 *******)0x0;
        FUN_05e1d31c(&local_3c0,&DAT_0a3d6cfc,&local_f0);
        thunk_FUN_05e1d0bc(&local_3c0);
        if ((long)local_1b0 < 0) {
          __ZdlPvm(local_1c0,(ulong)local_1b0 & 0x7fffffffffffffff);
        }
      }
      FUN_030f6650(param_1,1,1,4,400);
      plVar10 = local_3f8;
    }
    else {
      local_3f8 = *(long **)(lVar4 + 0x228);
      if (local_3f8 != (long *)0x0) {
        local_3f8[1] = local_3f8[1] + 1;
      }
      (**(code **)(*local_400 + 0x10))(local_400,lVar4);
      plVar3 = local_400;
      puStack_418 = &SUB_aaaaaaaaaaaaaaaa;
      local_410 = &SUB_aaaaaaaaaaaaaaaa;
      local_420 = &SUB_aaaaaaaaaaaaaaaa;
      plVar10 = local_400 + 0x52;
      if (*(char *)((long)local_400 + 0x2a7) < '\0') {
        FUN_00018d20(&local_420,local_400[0x52],local_400[0x53]);
      }
      else {
        puStack_418 = (undefined1 *)local_400[0x53];
        local_420 = (undefined1 *)*plVar10;
        local_410 = (undefined1 *)local_400[0x54];
      }
      puVar8 = puStack_418;
      if (-1 < (long)local_410) {
        puVar8 = (undefined1 *)((ulong)local_410 >> 0x38);
      }
      if (puVar8 == (undefined1 *)0x0) {
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (&local_420,plVar3 + 0x87);
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(plVar10,&local_420)
        ;
      }
      local_430 = &SUB_aaaaaaaaaaaaaaaa;
      local_428 = &SUB_aaaaaaaaaaaaaaaa;
      local_438 = &SUB_aaaaaaaaaaaaaaaa;
      FUN_030f1d74(&local_438,*param_3);
      iVar6 = FUN_04bb6cd4(&local_438);
      if (iVar6 == 0) {
        local_150 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_168 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
        local_170 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
        puStack_158 = &SUB_aaaaaaaaaaaaaaaa;
        local_160 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
        uStack_188 = &SUB_aaaaaaaaaaaaaaaa;
        local_190 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
        puStack_178 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_180 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_1a8 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
        local_1b0 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
        local_198 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
        local_1a0 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_1b8 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
        local_1c0 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
        FUN_050ef4b0(&local_1c0);
        lVar4 = local_320;
        local_150 = (undefined1 *)((ulong)local_150 | 1);
        if (puStack_1b8 == &DAT_0a524ad0) {
          puStack_1b8 = (undefined8 *)__Znwm(0x18);
          *puStack_1b8 = 0;
          puStack_1b8[1] = 0;
          puStack_1b8[2] = 0;
        }
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (puStack_1b8,lVar4 + 0x18);
        local_150 = (undefined1 *)((ulong)local_150 | 2);
        if (local_1b0 == &DAT_0a524ad0) {
          local_1b0 = (undefined8 *)__Znwm(0x18);
          *local_1b0 = 0;
          local_1b0[1] = 0;
          local_1b0[2] = 0;
        }
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (local_1b0,plVar3 + 0x8c);
        local_1a0 = (undefined1 *)CONCAT44(local_1a0._4_4_,(int)plVar3[0x35]);
        local_150 = (undefined1 *)((ulong)local_150 | 0xc);
        if (puStack_1a8 == &DAT_0a524ad0) {
          puStack_1a8 = (undefined8 *)__Znwm(0x18);
          *puStack_1a8 = 0;
          puStack_1a8[1] = 0;
          puStack_1a8[2] = 0;
        }
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (puStack_1a8,&local_438);
        local_150 = (undefined1 *)((ulong)local_150 | 0x10);
        local_1a0 = (undefined1 *)CONCAT44(*(undefined4 *)(lVar4 + 0x10),(undefined4)local_1a0);
        FUN_04ccd684(&local_3c0,plVar3,lVar4);
        local_150 = (undefined1 *)((ulong)local_150 | 0x20);
        if (local_198 == &DAT_0a524ad0) {
          local_198 = (undefined8 *)__Znwm(0x18);
          *local_198 = 0;
          local_198[1] = 0;
          local_198[2] = 0;
        }
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (local_198,&local_3c0);
        if ((long)local_3b0 < 0) {
          __ZdlPvm(local_3c0,local_3b0 & 0x7fffffffffffffff);
        }
        local_150 = (undefined1 *)((ulong)local_150 | 0x40);
        uStack_188 = (undefined1 *)CONCAT44(uStack_188._4_4_,*(undefined4 *)(lVar4 + 0x114));
        FUN_030f2168(&local_3c0,*param_3);
        local_150 = (undefined1 *)((ulong)local_150 | 0x80);
        if (local_190 == &DAT_0a524ad0) {
          local_190 = (undefined8 *)__Znwm(0x18);
          *local_190 = 0;
          local_190[1] = 0;
          local_190[2] = 0;
        }
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (local_190,&local_3c0);
        if ((long)local_3b0 < 0) {
          __ZdlPvm(local_3c0,local_3b0 & 0x7fffffffffffffff);
        }
        uVar7 = (uint)local_150 | 0x200;
        local_150 = (undefined1 *)((ulong)local_150 | 0x200);
        uStack_188 = (undefined1 *)CONCAT44(1,(undefined4)uStack_188);
        lVar12 = (long)*(char *)(lVar4 + 0x177);
        if (lVar12 < 0) {
          lVar12 = *(long *)(lVar4 + 0x168);
        }
        if (lVar12 != 0) {
          FUN_03094c34(&local_1c0,lVar4 + 0x160);
          uVar7 = (uint)local_150;
        }
        local_150 = (undefined1 *)(CONCAT44(local_150._4_4_,uVar7) | 0x2000);
        if (puStack_168 == &DAT_0a524ad0) {
          puStack_168 = (undefined8 *)__Znwm(0x18);
          *puStack_168 = 0;
          puStack_168[1] = 0;
          puStack_168[2] = 0;
        }
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (puStack_168,&local_420);
        local_150 = (undefined1 *)((ulong)local_150 | 0x1000);
        if (local_170 == &DAT_0a524ad0) {
          local_170 = (undefined8 *)__Znwm(0x18);
          *local_170 = 0;
          local_170[1] = 0;
          local_170[2] = 0;
        }
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (local_170,&local_420);
        local_150 = (undefined1 *)((ulong)local_150 | 0x4000);
        if (local_160 == &DAT_0a524ad0) {
          local_160 = (undefined8 *)__Znwm(0x18);
          *local_160 = 0;
          local_160[1] = 0;
          local_160[2] = 0;
        }
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc(local_160,"");
        puStack_1d8 = &SUB_aaaaaaaaaaaaaaaa;
        local_1e0 = &SUB_aaaaaaaaaaaaaaaa;
        uStack_1c8 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_1d0 = &SUB_aaaaaaaaaaaaaaaa;
        uStack_1f8 = &SUB_aaaaaaaaaaaaaaaa;
        local_200 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
        puStack_1e8 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_1f0 = &SUB_aaaaaaaaaaaaaaaa;
        ppppppuStack_218 = (undefined8 ******)&SUB_aaaaaaaaaaaaaaaa;
        local_220 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
        puStack_208 = &SUB_aaaaaaaaaaaaaaaa;
        local_210 = &SUB_aaaaaaaaaaaaaaaa;
        FUN_050ef4f4(&local_220);
        puStack_1d8 = (undefined1 *)CONCAT44(puStack_1d8._4_4_,2);
        uStack_1c8 = (undefined1 *)((ulong)uStack_1c8 | 0x40200000000);
        if (local_210 == (undefined1 *)0x0) {
          puVar8 = (undefined1 *)__Znwm(0x78);
          FUN_050ef4b0();
          local_210 = puVar8;
        }
        FUN_0510761c(local_210,&local_1c0);
        uVar7 = uStack_1c8._4_4_;
        if (0x1900000 < (ulong)plVar3[0x5e]) {
          uVar7 = uStack_1c8._4_4_ | 0x20;
          uStack_1f8 = (undefined1 *)CONCAT44(7,(undefined4)uStack_1f8);
        }
        uStack_1c8 = (undefined1 *)(CONCAT44(uVar7,(undefined4)uStack_1c8) | 0x1000000000);
        if (local_200 == &DAT_0a524ad0) {
          local_200 = (undefined8 *)__Znwm(0x18);
          *local_200 = 0;
          local_200[1] = 0;
          local_200[2] = 0;
        }
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (local_200,plVar3 + 0x3f);
        local_1e0 = (undefined1 *)CONCAT44((int)plVar3[0x2b],(uint)*(byte *)(local_330 + 8));
        uStack_1c8 = (undefined1 *)((ulong)uStack_1c8 | 0x30100000000);
        if (ppppppuStack_218 == (undefined8 ******)0x0) {
          ppppppuVar9 = (undefined8 ******)__Znwm(0x38);
          FUN_0465a1bc();
          ppppppuStack_218 = ppppppuVar9;
        }
        *(uint *)((long)ppppppuStack_218 + 0x34) = *(uint *)((long)ppppppuStack_218 + 0x34) | 0x20;
        *(undefined4 *)((long)ppppppuStack_218 + 0x2c) = 0;
        puStack_498 = &SUB_aaaaaaaaaaaaaaaa;
        local_4a0 = &SUB_aaaaaaaaaaaaaaaa;
        local_488 = (long *)&SUB_aaaaaaaaaaaaaaaa;
        local_490 = &SUB_aaaaaaaaaaaaaaaa;
        puStack_4a8 = &SUB_aaaaaaaaaaaaaaaa;
        local_4b0 = &SUB_aaaaaaaaaaaaaaaa;
        plVar10 = (long *)FUN_04669774();
        uVar11 = (**(code **)(*plVar10 + 0x18))();
        local_e0 = (undefined8 *******)((ulong)local_e0 & 0xffffffffffffff);
        local_f0 = (undefined8 *******)((ulong)local_f0 & 0xffffffffffffff00);
        local_3c0 = DAT_0875d510;
        local_39c = 0;
        local_3b0 = 0;
        local_3a8 = 0;
        local_3b8 = 0;
        local_3a0 = 0;
        FUN_03058298(&local_4b0,uVar11,&local_220,&local_f0,&local_3c0);
        if ((long)local_3a8 < 0) {
          __ZdlPvm(local_3b8,local_3a8 & 0x7fffffffffffffff);
        }
        local_3f0 = local_4b0;
        puVar13 = (undefined8 *)((ulong)&local_3f0 | 8);
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (puVar13,(ulong)&local_4b0 | 8);
        puVar8 = local_490;
        if ((int)local_4b0 == 0 && local_4b0._4_4_ == 0) {
          iVar6 = thunk_FUN_05e1d97c(2);
          if (iVar6 != 0) {
            FUN_0488143c(&local_310);
            pppppppuVar1 = local_310;
            if (-1 < cStack_2f9) {
              pppppppuVar1 = &local_310;
            }
            if ((DAT_0a3d6ca3 & 1) == 0) {
              uVar14 = 0;
              do {
                (&DAT_0a3d6c8b)[uVar14] =
                     (&DAT_088a98e8)[uVar14] + 0x8a ^ (&DAT_088a98d8)[uVar14 & 0xf];
                uVar14 = uVar14 + 1;
              } while (uVar14 != 0x18);
              DAT_0a3d6ca3 = 1;
            }
            if ((DAT_0a3d70b0 & 1) == 0) {
              uRam000000000a3d70a8._0_1_ = s_CoSendAppMsgCgi_088a8fb0[8];
              uRam000000000a3d70a8._1_1_ = s_CoSendAppMsgCgi_088a8fb0[9];
              uRam000000000a3d70a8._2_1_ = s_CoSendAppMsgCgi_088a8fb0[10];
              uRam000000000a3d70a8._3_1_ = s_CoSendAppMsgCgi_088a8fb0[0xb];
              uRam000000000a3d70a8._4_1_ = s_CoSendAppMsgCgi_088a8fb0[0xc];
              uRam000000000a3d70a8._5_1_ = s_CoSendAppMsgCgi_088a8fb0[0xd];
              uRam000000000a3d70a8._6_1_ = s_CoSendAppMsgCgi_088a8fb0[0xe];
              uRam000000000a3d70a8._7_1_ = s_CoSendAppMsgCgi_088a8fb0[0xf];
              DAT_0a3d70a0 = s_CoSendAppMsgCgi_088a8fb0[0];
              DAT_0a3d70a0_1._0_1_ = s_CoSendAppMsgCgi_088a8fb0[1];
              DAT_0a3d70a0_1._1_1_ = s_CoSendAppMsgCgi_088a8fb0[2];
              DAT_0a3d70a0_1._2_1_ = s_CoSendAppMsgCgi_088a8fb0[3];
              DAT_0a3d70a0_1._3_1_ = s_CoSendAppMsgCgi_088a8fb0[4];
              DAT_0a3d70a0_1._4_1_ = s_CoSendAppMsgCgi_088a8fb0[5];
              DAT_0a3d70a0_1._5_1_ = s_CoSendAppMsgCgi_088a8fb0[6];
              DAT_0a3d70a0_1._6_1_ = s_CoSendAppMsgCgi_088a8fb0[7];
              DAT_0a3d70b0 = 1;
            }
            FUN_05e1d050(&local_3c0,2,pppppppuVar1,&DAT_0a3d6c8b,&DAT_0a3d70a0,0x1fc,0,0);
            lVar4 = local_320;
            FUN_04cbe440(local_4c8,local_320);
            local_140 = local_4c8[0];
            if (-1 < cStack_4b1) {
              local_140 = local_4c8;
            }
            local_138 = 0;
            FUN_0026d4e8(&local_270,*(undefined8 *)(lVar4 + 0xf8),10);
            FUN_0026d4e8(&local_2c0,*(undefined8 *)(puVar8 + 0x38),10);
            if ((DAT_0a3d717d & 1) == 0) {
              uVar14 = 0;
              do {
                (&DAT_0a3d7142)[uVar14] =
                     (&DAT_088a9f91)[uVar14] + 0x8a ^ (&DAT_088a9f81)[uVar14 & 0xf];
                uVar14 = uVar14 + 1;
              } while (uVar14 != 0x3b);
              DAT_0a3d717d = 1;
            }
            local_f0 = &local_140;
            pppppppuStack_e8 = (undefined8 *******)&local_270;
            local_e0 = &local_2c0;
            local_d0 = 0;
            pppppppuStack_d8 = (undefined8 *******)0x0;
            local_c0 = 0;
            uStack_c8 = 0;
            local_b0 = 0;
            uStack_b8 = 0;
            local_a0 = 0;
            uStack_a8 = 0;
            local_90 = 0;
            uStack_98 = 0;
            local_80 = 0;
            uStack_88 = 0;
            uStack_78 = 0;
            FUN_05e1d31c(&local_3c0,&DAT_0a3d7142,&local_f0);
            if (cStack_4b1 < '\0') {
              __ZdlPvm(local_4c8[0],CONCAT17(cStack_4b1,local_4b8) & 0x7fffffffffffffff);
            }
            thunk_FUN_05e1d0bc(&local_3c0);
            if (cStack_2f9 < '\0') {
              __ZdlPvm(local_310,CONCAT17(cStack_2f9,local_300) & 0x7fffffffffffffff);
            }
          }
          FUN_0466aca8(&local_140);
          FUN_01205740(&local_f0,local_140);
          FUN_0268f370(&local_3c0,local_f0);
          FUN_031a5b7c(local_3c0,*(undefined8 *)(lVar4 + 0xf8),*(undefined8 *)(puVar8 + 0x38));
          FUN_00129f68(&local_3c0);
          FUN_00129f68(&local_f0);
          FUN_00129f68(&local_140);
          *(undefined8 *)(lVar4 + 0xf8) = *(undefined8 *)(puVar8 + 0x38);
          __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                    (lVar4 + 0x160,*(undefined8 *)(puVar8 + 0x50));
          local_4d8 = local_320;
          plStack_4d0 = local_318;
          lVar4 = 0;
          if (local_318 != (long *)0x0) {
            lVar4 = local_318[1];
            local_318[1] = lVar4 + 1;
          }
          FUN_0309486c(lVar4,param_2,&local_4d8,1);
          FUN_00129f68(&local_4d8);
        }
        else {
          local_4e8 = *param_3;
          lStack_4e0 = param_3[1];
          lVar12 = 0;
          if (lStack_4e0 != 0) {
            lVar12 = *(long *)(lStack_4e0 + 8);
            *(long *)(lStack_4e0 + 8) = lVar12 + 1;
          }
          uVar7 = FUN_030dc518(lVar12,param_2,&local_4e8,local_3f0._4_4_);
          FUN_00129f68(&local_4e8);
          iVar6 = thunk_FUN_05e1d97c(4);
          if (iVar6 != 0) {
            FUN_0488143c(local_4c8);
            pppppppuVar1 = local_4c8[0];
            if (-1 < cStack_4b1) {
              pppppppuVar1 = local_4c8;
            }
            if ((DAT_0a3d6ca3 & 1) == 0) {
              uVar14 = 0;
              do {
                (&DAT_0a3d6c8b)[uVar14] =
                     (&DAT_088a98e8)[uVar14] + 0x8a ^ (&DAT_088a98d8)[uVar14 & 0xf];
                uVar14 = uVar14 + 1;
              } while (uVar14 != 0x18);
              DAT_0a3d6ca3 = 1;
            }
            if ((DAT_0a3d70b0 & 1) == 0) {
              uRam000000000a3d70a8._0_1_ = s_CoSendAppMsgCgi_088a8fb0[8];
              uRam000000000a3d70a8._1_1_ = s_CoSendAppMsgCgi_088a8fb0[9];
              uRam000000000a3d70a8._2_1_ = s_CoSendAppMsgCgi_088a8fb0[10];
              uRam000000000a3d70a8._3_1_ = s_CoSendAppMsgCgi_088a8fb0[0xb];
              uRam000000000a3d70a8._4_1_ = s_CoSendAppMsgCgi_088a8fb0[0xc];
              uRam000000000a3d70a8._5_1_ = s_CoSendAppMsgCgi_088a8fb0[0xd];
              uRam000000000a3d70a8._6_1_ = s_CoSendAppMsgCgi_088a8fb0[0xe];
              uRam000000000a3d70a8._7_1_ = s_CoSendAppMsgCgi_088a8fb0[0xf];
              DAT_0a3d70a0 = s_CoSendAppMsgCgi_088a8fb0[0];
              DAT_0a3d70a0_1._0_1_ = s_CoSendAppMsgCgi_088a8fb0[1];
              DAT_0a3d70a0_1._1_1_ = s_CoSendAppMsgCgi_088a8fb0[2];
              DAT_0a3d70a0_1._2_1_ = s_CoSendAppMsgCgi_088a8fb0[3];
              DAT_0a3d70a0_1._3_1_ = s_CoSendAppMsgCgi_088a8fb0[4];
              DAT_0a3d70a0_1._4_1_ = s_CoSendAppMsgCgi_088a8fb0[5];
              DAT_0a3d70a0_1._5_1_ = s_CoSendAppMsgCgi_088a8fb0[6];
              DAT_0a3d70a0_1._6_1_ = s_CoSendAppMsgCgi_088a8fb0[7];
              DAT_0a3d70b0 = 1;
            }
            FUN_05e1d050(&local_3c0,4,pppppppuVar1,&DAT_0a3d6c8b,&DAT_0a3d70a0,0x205,0,0);
            lVar4 = local_320;
            FUN_04cbe440(local_500,local_320);
            local_140 = local_500[0];
            if (-1 < cStack_4e9) {
              local_140 = local_500;
            }
            local_138 = 0;
            local_f0._0_4_ = (undefined4)local_3f0;
            local_270 = (undefined8 ******)0x0;
            FUN_003eccb4(&local_f0,&pppppuStack_268,10,1);
            local_f0 = (undefined8 *******)CONCAT44(local_f0._4_4_,local_3f0._4_4_);
            local_2c0 = (undefined8 *******)0x0;
            local_270 = &pppppuStack_268;
            FUN_003eccb4(&local_f0,&ppppppuStack_2b8,10,1);
            if (uVar7 == 0) {
              local_310 = (undefined8 *******)&DAT_0a3d7784;
              if ((DAT_0a3d778a & 1) == 0) {
                DAT_0a3d7784 = (undefined4)DAT_0847fe48;
                puVar5 = &DAT_0a3d7788;
                puVar8 = &DAT_0a3d7789;
                puVar16 = &DAT_0a3d778a;
                goto LAB_030938d0;
              }
            }
            else {
              local_310 = (undefined8 *******)&DAT_0a3d777c;
              if ((DAT_0a3d7781 & 1) == 0) {
                DAT_0a3d777c = 0x7274;
                DAT_0a3d777e = 0x75;
                puVar8 = &DAT_0a3d7780;
                puVar5 = &DAT_0a3d777f;
                puVar16 = &DAT_0a3d7781;
LAB_030938d0:
                *puVar5 = 0x65;
                *puVar8 = 0;
                *puVar16 = 1;
              }
            }
            local_308 = 0;
            if ((DAT_0a3d71d7 & 1) == 0) {
              uVar14 = 0;
              do {
                (&DAT_0a3d717e)[uVar14] =
                     (&DAT_088a9fdc)[uVar14] + 0x8a ^ (&DAT_088a9fcc)[uVar14 & 0xf];
                uVar14 = uVar14 + 1;
              } while (uVar14 != 0x59);
              DAT_0a3d71d7 = 1;
            }
            local_f0 = &local_140;
            pppppppuStack_e8 = (undefined8 *******)&local_270;
            local_e0 = &local_2c0;
            pppppppuStack_d8 = &local_310;
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
            uStack_78 = 0;
            local_80 = 0;
            local_2c0 = &ppppppuStack_2b8;
            FUN_05e1d31c(&local_3c0,&DAT_0a3d717e,&local_f0);
            if (cStack_4e9 < '\0') {
              __ZdlPvm(local_500[0],CONCAT17(cStack_4e9,local_4f0) & 0x7fffffffffffffff);
            }
            thunk_FUN_05e1d0bc(&local_3c0);
            if (cStack_4b1 < '\0') {
              __ZdlPvm(local_4c8[0],CONCAT17(cStack_4b1,local_4b8) & 0x7fffffffffffffff);
            }
          }
          if ((uVar7 & 1) == 0) {
            plStack_508 = local_318;
            lVar12 = 0;
            if (local_318 != (long *)0x0) {
              lVar12 = local_318[1];
              local_318[1] = lVar12 + 1;
            }
            local_510 = lVar4;
            FUN_0309486c(lVar12,param_2,&local_510,0);
            FUN_00129f68(&local_510);
          }
          FUN_030f6650(&local_3c0,3,0xc,(ulong)local_3f0 & 0xffffffff,local_3f0._4_4_);
          FUN_0308d48c(&local_3f0,&local_3c0);
          FUN_00257824(&local_3c0);
        }
        *(undefined1 *)(local_330 + 0x80) = 0;
        *param_1 = local_3f0;
        if ((long)puStack_3d8 < 0) {
          FUN_00018d20(param_1 + 1,puStack_3e8,local_3e0);
        }
        else {
          uVar11 = *puVar13;
          param_1[2] = puVar13[1];
          param_1[1] = uVar11;
          param_1[3] = puVar13[2];
        }
        plVar10 = local_488;
        param_1[4] = local_3d0;
        param_1[5] = local_3c8;
        if (local_3c8 != (long *)0x0) {
          local_3c8[1] = local_3c8[1] + 1;
        }
        if (local_488 != (long *)0x0) {
          LOAcquire();
          lVar4 = local_488[1];
          local_488[1] = lVar4 + -1;
          LORelease();
          if (lVar4 == 0) {
            (**(code **)(*local_488 + 0x10))(local_488);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
          }
        }
        if ((long)puStack_498 < 0) {
          __ZdlPvm(puStack_4a8,(ulong)puStack_498 & 0x7fffffffffffffff);
        }
        FUN_05107e00(&local_220);
        FUN_05106484(&local_1c0);
      }
      else {
        puStack_258 = &SUB_aaaaaaaaaaaaaaaa;
        local_260 = &SUB_aaaaaaaaaaaaaaaa;
        local_248 = (long *)&SUB_aaaaaaaaaaaaaaaa;
        local_250 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
        pppppuStack_268 = (undefined8 *****)&SUB_aaaaaaaaaaaaaaaa;
        local_270 = (undefined8 ******)&SUB_aaaaaaaaaaaaaaaa;
        local_448 = *param_3;
        local_440 = (long *)param_3[1];
        if (local_440 != (long *)0x0) {
          local_440[1] = local_440[1] + 1;
        }
        FUN_0284a574(&local_270,0x18,&local_448);
        plVar10 = local_440;
        if (local_440 != (long *)0x0) {
          LOAcquire();
          lVar4 = local_440[1];
          local_440[1] = lVar4 + -1;
          LORelease();
          if (lVar4 == 0) {
            (**(code **)(*local_440 + 0x10))(local_440);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
          }
        }
        lVar4 = local_320;
        if ((int)local_270 == 0 && local_270._4_4_ == 0) {
          *(undefined4 *)(local_320 + 0x118) = 2;
          FUN_0466aca8(&local_1c0);
          FUN_01205740(&local_f0,local_1c0);
          FUN_0268f370(&local_3c0,local_f0);
          FUN_031a5b7c(local_3c0,*(undefined8 *)(lVar4 + 0xf8),*local_250);
          FUN_00129f68(&local_3c0);
          FUN_00129f68(&local_f0);
          FUN_00129f68(&local_1c0);
          *(undefined8 *)(lVar4 + 0xf8) = *local_250;
          local_458 = lVar4;
          plStack_450 = local_318;
          lVar4 = 0;
          if (local_318 != (long *)0x0) {
            lVar4 = local_318[1];
            local_318[1] = lVar4 + 1;
          }
          FUN_0309486c(lVar4,param_2,&local_458,1);
          FUN_00129f68(&local_458);
          iVar6 = thunk_FUN_05e1d97c(2);
          if (iVar6 != 0) {
            FUN_0488143c(&local_2c0);
            pppppppuVar1 = local_2c0;
            if (-1 < cStack_2a9) {
              pppppppuVar1 = &local_2c0;
            }
            if ((DAT_0a3d6ca3 & 1) == 0) {
              uVar14 = 0;
              do {
                (&DAT_0a3d6c8b)[uVar14] =
                     (&DAT_088a98e8)[uVar14] + 0x8a ^ (&DAT_088a98d8)[uVar14 & 0xf];
                uVar14 = uVar14 + 1;
              } while (uVar14 != 0x18);
              DAT_0a3d6ca3 = 1;
            }
            if ((DAT_0a3d70b0 & 1) == 0) {
              uRam000000000a3d70a8._0_1_ = s_CoSendAppMsgCgi_088a8fb0[8];
              uRam000000000a3d70a8._1_1_ = s_CoSendAppMsgCgi_088a8fb0[9];
              uRam000000000a3d70a8._2_1_ = s_CoSendAppMsgCgi_088a8fb0[10];
              uRam000000000a3d70a8._3_1_ = s_CoSendAppMsgCgi_088a8fb0[0xb];
              uRam000000000a3d70a8._4_1_ = s_CoSendAppMsgCgi_088a8fb0[0xc];
              uRam000000000a3d70a8._5_1_ = s_CoSendAppMsgCgi_088a8fb0[0xd];
              uRam000000000a3d70a8._6_1_ = s_CoSendAppMsgCgi_088a8fb0[0xe];
              uRam000000000a3d70a8._7_1_ = s_CoSendAppMsgCgi_088a8fb0[0xf];
              DAT_0a3d70a0 = s_CoSendAppMsgCgi_088a8fb0[0];
              DAT_0a3d70a0_1._0_1_ = s_CoSendAppMsgCgi_088a8fb0[1];
              DAT_0a3d70a0_1._1_1_ = s_CoSendAppMsgCgi_088a8fb0[2];
              DAT_0a3d70a0_1._2_1_ = s_CoSendAppMsgCgi_088a8fb0[3];
              DAT_0a3d70a0_1._3_1_ = s_CoSendAppMsgCgi_088a8fb0[4];
              DAT_0a3d70a0_1._4_1_ = s_CoSendAppMsgCgi_088a8fb0[5];
              DAT_0a3d70a0_1._5_1_ = s_CoSendAppMsgCgi_088a8fb0[6];
              DAT_0a3d70a0_1._6_1_ = s_CoSendAppMsgCgi_088a8fb0[7];
              DAT_0a3d70b0 = 1;
            }
            FUN_05e1d050(&local_3c0,2,pppppppuVar1,&DAT_0a3d6c8b,&DAT_0a3d70a0,0x1ca,0,0);
            lVar4 = local_320;
            FUN_04cbe440(&local_310,local_320);
            local_1c0 = local_310;
            if (-1 < cStack_2f9) {
              local_1c0 = &local_310;
            }
            puStack_1b8 = (undefined8 *)((ulong)puStack_1b8 & 0xffffffffffffff00);
            local_f0 = (undefined8 *******)*local_250;
            local_220 = (undefined8 *******)0x0;
            FUN_00eb46c8(&local_f0,&ppppppuStack_218,10,1);
            local_220 = &ppppppuStack_218;
            FUN_0027f8b0(&local_140,*(undefined4 *)(lVar4 + 0x114),10);
            if ((DAT_0a3d7117 & 1) == 0) {
              uVar14 = 0;
              do {
                (&DAT_0a3d70dd)[uVar14] =
                     (&DAT_088a9f0e)[uVar14] + 0x8a ^ (&DAT_088a9efe)[uVar14 & 0xf];
                uVar14 = uVar14 + 1;
              } while (uVar14 != 0x3a);
              DAT_0a3d7117 = 1;
            }
            local_f0 = &local_1c0;
            pppppppuStack_e8 = &local_220;
            local_e0 = &local_140;
            local_d0 = 0;
            pppppppuStack_d8 = (undefined8 *******)0x0;
            local_c0 = 0;
            uStack_c8 = 0;
            local_b0 = 0;
            uStack_b8 = 0;
            local_a0 = 0;
            uStack_a8 = 0;
            local_90 = 0;
            uStack_98 = 0;
            local_80 = 0;
            uStack_88 = 0;
            uStack_78 = 0;
            FUN_05e1d31c(&local_3c0,&DAT_0a3d70dd,&local_f0);
            if (cStack_2f9 < '\0') {
              __ZdlPvm(local_310,CONCAT17(cStack_2f9,local_300) & 0x7fffffffffffffff);
            }
            thunk_FUN_05e1d0bc(&local_3c0);
            if (cStack_2a9 < '\0') {
              __ZdlPvm(local_2c0,CONCAT17(cStack_2a9,local_2b0) & 0x7fffffffffffffff);
            }
          }
        }
        else {
          local_468 = *param_3;
          lStack_460 = param_3[1];
          lVar4 = 0;
          if (lStack_460 != 0) {
            lVar4 = *(long *)(lStack_460 + 8);
            *(long *)(lStack_460 + 8) = lVar4 + 1;
          }
          uVar14 = FUN_030dc518(lVar4,param_2,&local_468,local_3f0._4_4_);
          FUN_00129f68(&local_468);
          iVar6 = thunk_FUN_05e1d97c(4);
          if (iVar6 != 0) {
            FUN_0488143c(&local_140);
            pppppppuVar1 = local_140;
            if (-1 < cStack_129) {
              pppppppuVar1 = &local_140;
            }
            if ((DAT_0a3d6ca3 & 1) == 0) {
              uVar15 = 0;
              do {
                (&DAT_0a3d6c8b)[uVar15] =
                     (&DAT_088a98e8)[uVar15] + 0x8a ^ (&DAT_088a98d8)[uVar15 & 0xf];
                uVar15 = uVar15 + 1;
              } while (uVar15 != 0x18);
              DAT_0a3d6ca3 = 1;
            }
            if ((DAT_0a3d70b0 & 1) == 0) {
              uRam000000000a3d70a8._0_1_ = s_CoSendAppMsgCgi_088a8fb0[8];
              uRam000000000a3d70a8._1_1_ = s_CoSendAppMsgCgi_088a8fb0[9];
              uRam000000000a3d70a8._2_1_ = s_CoSendAppMsgCgi_088a8fb0[10];
              uRam000000000a3d70a8._3_1_ = s_CoSendAppMsgCgi_088a8fb0[0xb];
              uRam000000000a3d70a8._4_1_ = s_CoSendAppMsgCgi_088a8fb0[0xc];
              uRam000000000a3d70a8._5_1_ = s_CoSendAppMsgCgi_088a8fb0[0xd];
              uRam000000000a3d70a8._6_1_ = s_CoSendAppMsgCgi_088a8fb0[0xe];
              uRam000000000a3d70a8._7_1_ = s_CoSendAppMsgCgi_088a8fb0[0xf];
              DAT_0a3d70a0 = s_CoSendAppMsgCgi_088a8fb0[0];
              DAT_0a3d70a0_1._0_1_ = s_CoSendAppMsgCgi_088a8fb0[1];
              DAT_0a3d70a0_1._1_1_ = s_CoSendAppMsgCgi_088a8fb0[2];
              DAT_0a3d70a0_1._2_1_ = s_CoSendAppMsgCgi_088a8fb0[3];
              DAT_0a3d70a0_1._3_1_ = s_CoSendAppMsgCgi_088a8fb0[4];
              DAT_0a3d70a0_1._4_1_ = s_CoSendAppMsgCgi_088a8fb0[5];
              DAT_0a3d70a0_1._5_1_ = s_CoSendAppMsgCgi_088a8fb0[6];
              DAT_0a3d70a0_1._6_1_ = s_CoSendAppMsgCgi_088a8fb0[7];
              DAT_0a3d70b0 = 1;
            }
            FUN_05e1d050(&local_3c0,4,pppppppuVar1,&DAT_0a3d6c8b,&DAT_0a3d70a0,0x1cd,0,0);
            FUN_04cbe440(&local_2c0,local_320);
            local_1c0 = local_2c0;
            if (-1 < cStack_2a9) {
              local_1c0 = &local_2c0;
            }
            puStack_1b8 = (undefined8 *)((ulong)puStack_1b8 & 0xffffffffffffff00);
            local_f0 = (undefined8 *******)CONCAT44(local_f0._4_4_,local_270._4_4_);
            local_220 = (undefined8 *******)0x0;
            FUN_003eccb4(&local_f0,&ppppppuStack_218,10,1);
            if ((DAT_0a3d7141 & 1) == 0) {
              uVar15 = 0;
              do {
                (&DAT_0a3d7118)[uVar15] =
                     (&DAT_088a9f58)[uVar15] + 0x8a ^ (&DAT_088a9f48)[uVar15 & 0xf];
                uVar15 = uVar15 + 1;
              } while (uVar15 != 0x29);
              DAT_0a3d7141 = 1;
            }
            local_f0 = &local_1c0;
            pppppppuStack_d8 = (undefined8 *******)0x0;
            local_e0 = (undefined8 *******)0x0;
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
            uStack_78 = 0;
            local_80 = 0;
            local_220 = &ppppppuStack_218;
            pppppppuStack_e8 = &local_220;
            FUN_05e1d31c(&local_3c0,&DAT_0a3d7118,&local_f0);
            if (cStack_2a9 < '\0') {
              __ZdlPvm(local_2c0,CONCAT17(cStack_2a9,local_2b0) & 0x7fffffffffffffff);
            }
            thunk_FUN_05e1d0bc(&local_3c0);
            if (cStack_129 < '\0') {
              __ZdlPvm(local_140,CONCAT17(cStack_129,local_130) & 0x7fffffffffffffff);
            }
          }
          if ((uVar14 & 1) == 0) {
            local_478 = local_320;
            plStack_470 = local_318;
            lVar4 = 0;
            if (local_318 != (long *)0x0) {
              lVar4 = local_318[1];
              local_318[1] = lVar4 + 1;
            }
            FUN_0309486c(lVar4,param_2,&local_478,0);
            FUN_00129f68(&local_478);
          }
          FUN_030f6650(&local_3c0,3,0xc,(ulong)local_3f0 & 0xffffffff,local_3f0._4_4_);
          FUN_0308d48c(&local_3f0,&local_3c0);
          FUN_00257824(&local_3c0);
        }
        *(undefined1 *)(local_330 + 0x80) = 0;
        *param_1 = local_3f0;
        if ((long)puStack_3d8 < 0) {
          FUN_00018d20(param_1 + 1,puStack_3e8,local_3e0);
        }
        else {
          puVar13 = (undefined8 *)((ulong)&local_3f0 | 8);
          uVar11 = *puVar13;
          param_1[2] = puVar13[1];
          param_1[1] = uVar11;
          param_1[3] = puVar13[2];
        }
        plVar10 = local_248;
        param_1[4] = local_3d0;
        param_1[5] = local_3c8;
        if (local_3c8 != (long *)0x0) {
          local_3c8[1] = local_3c8[1] + 1;
        }
        if (local_248 != (long *)0x0) {
          LOAcquire();
          lVar4 = local_248[1];
          local_248[1] = lVar4 + -1;
          LORelease();
          if (lVar4 == 0) {
            (**(code **)(*local_248 + 0x10))(local_248);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
          }
        }
        if ((long)puStack_258 < 0) {
          __ZdlPvm(pppppuStack_268,(ulong)puStack_258 & 0x7fffffffffffffff);
        }
      }
      if ((long)local_428 < 0) {
        __ZdlPvm(local_438,(ulong)local_428 & 0x7fffffffffffffff);
      }
      plVar10 = local_3f8;
      if ((long)local_410 < 0) {
        __ZdlPvm(local_420,(ulong)local_410 & 0x7fffffffffffffff);
        plVar10 = local_3f8;
      }
    }
    local_3f8 = plVar10;
    if (plVar10 != (long *)0x0) {
      LOAcquire();
      lVar4 = plVar10[1];
      plVar10[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*plVar10 + 0x10))(plVar10);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
      }
    }
  }
  plVar10 = local_3c8;
  if (local_3c8 != (long *)0x0) {
    LOAcquire();
    lVar4 = local_3c8[1];
    local_3c8[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*local_3c8 + 0x10))(local_3c8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
    }
  }
  if ((long)puStack_3d8 < 0) {
    __ZdlPvm(puStack_3e8,(ulong)puStack_3d8 & 0x7fffffffffffffff);
  }
LAB_030937c8:
  plVar10 = local_328;
  if (local_328 != (long *)0x0) {
    LOAcquire();
    lVar4 = local_328[1];
    local_328[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*local_328 + 0x10))(local_328);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
    }
  }
  plVar10 = local_318;
  if (local_318 != (long *)0x0) {
    LOAcquire();
    lVar4 = local_318[1];
    local_318[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*local_318 + 0x10))(local_318);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar10);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


