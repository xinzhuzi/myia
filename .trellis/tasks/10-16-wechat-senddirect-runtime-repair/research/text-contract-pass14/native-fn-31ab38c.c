// Ghidra inferred pseudocode; requested=0x31ab38c
// entry=031ab38c end=031ac0d7

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_031ab38c(undefined8 param_1,long param_2)

{
  int iVar1;
  ulong uVar2;
  char *pcVar3;
  undefined1 *puVar4;
  undefined8 ****ppppuVar5;
  long lVar6;
  undefined8 uVar7;
  uint uVar8;
  undefined1 *local_2a8;
  undefined1 *local_2a0;
  undefined1 *local_298;
  undefined8 ***local_290 [2];
  undefined7 local_280;
  char cStack_279;
  undefined1 *local_278;
  undefined8 ***local_270;
  undefined1 *local_268;
  undefined8 local_260;
  undefined1 *local_258;
  undefined1 *local_250;
  undefined1 *local_248;
  undefined8 local_1c8;
  ulong local_1c0;
  ulong local_1b8;
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
  undefined8 local_e0;
  undefined8 uStack_d8;
  undefined8 uStack_d0;
  undefined8 uStack_c8;
  undefined8 local_c0;
  undefined8 uStack_b8;
  undefined8 uStack_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 uStack_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 uStack_70;
  undefined8 uStack_68;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar6 = *(long *)(param_2 + 0x20);
  if (lVar6 == 0) {
    lVar6 = *(long *)(DAT_0a521850 + 0x20);
  }
  uVar7 = *(undefined8 *)(lVar6 + 8);
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
  FUN_0572111c(&local_1b0);
  local_1c8 = 0;
  local_1c0 = 0;
  local_1b8 = 0;
  uVar2 = FUN_04bd7eb0(uVar7,&local_1b0);
  if ((uVar2 & 1) == 0) {
    iVar1 = thunk_FUN_05e1d97c(3);
    if (iVar1 != 0) {
      FUN_0488143c(&local_270);
      ppppuVar5 = (undefined8 ****)local_270;
      if (-1 < (long)local_260) {
        ppppuVar5 = &local_270;
      }
      if ((DAT_0a3dd363 & 1) == 0) {
        uVar2 = 0;
        do {
          (&DAT_0a3dd350)[uVar2] = (&DAT_088bce97)[uVar2] + 0x8a ^ (&DAT_088bce87)[uVar2 & 0xf];
          uVar2 = uVar2 + 1;
        } while (uVar2 != 0x13);
        DAT_0a3dd363 = 1;
      }
      if ((DAT_0a3dec24 & 1) == 0) {
        uRam000000000a3dec18._0_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x78];
        uRam000000000a3dec18._1_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x79];
        uRam000000000a3dec18._2_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7a];
        uRam000000000a3dec18._3_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7b];
        uRam000000000a3dec18._4_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7c];
        uRam000000000a3dec18._5_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7d];
        uRam000000000a3dec18._6_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7e];
        uRam000000000a3dec18._7_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7f];
        DAT_0a3dec10 = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x70];
        DAT_0a3dec10_1._0_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x71];
        DAT_0a3dec10_1._1_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x72];
        DAT_0a3dec10_1._2_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x73];
        DAT_0a3dec10_1._3_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x74];
        DAT_0a3dec10_1._4_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x75];
        DAT_0a3dec10_1._5_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x76];
        DAT_0a3dec10_1._6_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x77];
        DAT_0a3dec20 = (undefined4)ram0x087913e0;
        DAT_0a3dec24 = 1;
      }
      FUN_05e1d050(&local_258,3,ppppuVar5,&DAT_0a3dd350,&DAT_0a3dec10,0xa13,0,0);
      if ((DAT_0a3dea20 & 1) == 0) {
        uRam000000000a3dea18._0_1_ = s_IAppletManagerV3applet_service_c_08788e40[0x38];
        uRam000000000a3dea18._1_1_ = s_IAppletManagerV3applet_service_c_08788e40[0x39];
        uRam000000000a3dea18._2_1_ = s_IAppletManagerV3applet_service_c_08788e40[0x3a];
        uRam000000000a3dea18._3_1_ = s_IAppletManagerV3applet_service_c_08788e40[0x3b];
        uRam000000000a3dea18._4_1_ = s_IAppletManagerV3applet_service_c_08788e40[0x3c];
        uRam000000000a3dea18._5_1_ = s_IAppletManagerV3applet_service_c_08788e40[0x3d];
        uRam000000000a3dea18._6_1_ = s_IAppletManagerV3applet_service_c_08788e40[0x3e];
        uRam000000000a3dea18._7_1_ = s_IAppletManagerV3applet_service_c_08788e40[0x3f];
        DAT_0a3dea10 = s_IAppletManagerV3applet_service_c_08788e40[0x30];
        DAT_0a3dea10_1._0_1_ = s_IAppletManagerV3applet_service_c_08788e40[0x31];
        DAT_0a3dea10_1._1_1_ = s_IAppletManagerV3applet_service_c_08788e40[0x32];
        DAT_0a3dea10_1._2_1_ = s_IAppletManagerV3applet_service_c_08788e40[0x33];
        DAT_0a3dea10_1._3_1_ = s_IAppletManagerV3applet_service_c_08788e40[0x34];
        DAT_0a3dea10_1._4_1_ = s_IAppletManagerV3applet_service_c_08788e40[0x35];
        DAT_0a3dea10_1._5_1_ = s_IAppletManagerV3applet_service_c_08788e40[0x36];
        DAT_0a3dea10_1._6_1_ = s_IAppletManagerV3applet_service_c_08788e40[0x37];
        DAT_0a3dea20 = 1;
      }
      uStack_78 = 0;
      local_80 = 0;
      uStack_68 = 0;
      uStack_70 = 0;
      uStack_98 = 0;
      local_a0 = 0;
      uStack_88 = 0;
      uStack_90 = 0;
      uStack_b8 = 0;
      local_c0 = 0;
      uStack_a8 = 0;
      uStack_b0 = 0;
      uStack_d8 = 0;
      local_e0 = 0;
      uStack_c8 = 0;
      uStack_d0 = 0;
      FUN_05e1d31c(&local_258,&DAT_0a3dea10,&local_e0);
LAB_031ab714:
      thunk_FUN_05e1d0bc(&local_258);
      if ((long)local_260 < 0) {
        __ZdlPvm(local_270,(ulong)local_260 & 0x7fffffffffffffff);
      }
    }
  }
  else {
    local_278 = &SUB_aaaaaaaaaaaaaaaa;
    if ((DAT_0a3dea2b & 1) == 0) {
      DAT_0a3dea24 = (undefined4)DAT_08788f20;
      DAT_0a3dea28 = 0x6773;
      DAT_0a3dea2a = 0;
      DAT_0a3dea2b = 1;
    }
    local_278 = (undefined1 *)FUN_0571ce74(&local_1b0,&DAT_0a3dea24);
    iVar1 = FUN_04af2fcc(&local_278);
    if (iVar1 == 0) {
      local_268 = &SUB_aaaaaaaaaaaaaaaa;
      local_260 = &SUB_aaaaaaaaaaaaaaaa;
      local_270 = (undefined8 ***)&SUB_aaaaaaaaaaaaaaaa;
      if ((DAT_0a3dec2d & 1) == 0) {
        DAT_0a3dec28 = (undefined4)DAT_08489788;
        DAT_0a3dec2c = 0;
        DAT_0a3dec2d = 1;
      }
      local_258 = (undefined1 *)FUN_0571cee8(&local_278,&DAT_0a3dec28);
      pcVar3 = (char *)FUN_0571c188(&local_258,"");
      puVar4 = (undefined1 *)_strlen(pcVar3);
      if ((undefined1 *)0x7ffffffffffffff7 < puVar4) {
                    /* WARNING: Subroutine does not return */
        FUN_00018d9c(&local_270);
      }
      if (puVar4 < (undefined1 *)0x17) {
        local_260 = (undefined1 *)CONCAT17((char)puVar4,(undefined7)local_260);
        ppppuVar5 = &local_270;
        if (puVar4 != (undefined1 *)0x0) goto LAB_031ab7ec;
      }
      else {
        uVar2 = 0x19;
        if (((ulong)puVar4 | 7) != 0x17) {
          uVar2 = ((ulong)puVar4 | 7) + 1;
        }
        ppppuVar5 = (undefined8 ****)__Znwm(uVar2);
        local_260 = (undefined1 *)(uVar2 | 0x8000000000000000);
        local_270 = ppppuVar5;
        local_268 = puVar4;
LAB_031ab7ec:
        _memmove(ppppuVar5,pcVar3,(size_t)puVar4);
      }
      *(undefined1 *)((long)ppppuVar5 + (long)puVar4) = 0;
      if ((DAT_0a3dec3e & 1) == 0) {
        DAT_0a3dec30._0_1_ = s_SendMsgFtouserna_tou_088bac38[0];
        DAT_0a3dec30._1_1_ = s_SendMsgFtouserna_tou_088bac38[1];
        DAT_0a3dec30._2_1_ = s_SendMsgFtouserna_tou_088bac38[2];
        DAT_0a3dec30._3_1_ = s_SendMsgFtouserna_tou_088bac38[3];
        DAT_0a3dec30._4_1_ = s_SendMsgFtouserna_tou_088bac38[4];
        DAT_0a3dec30._5_1_ = s_SendMsgFtouserna_tou_088bac38[5];
        DAT_0a3dec30._6_1_ = s_SendMsgFtouserna_tou_088bac38[6];
        DAT_0a3dec30._7_1_ = s_SendMsgFtouserna_tou_088bac38[7];
        DAT_0a3dec38 = (undefined4)DAT_084caf50;
        DAT_0a3dec3c = 100;
        DAT_0a3dec3e = 1;
      }
      puVar4 = (undefined1 *)_strlen((char *)&DAT_0a3dec30);
      if ((long)local_260._7_1_ < 0) {
        if (puVar4 == local_268) {
          ppppuVar5 = (undefined8 ****)local_270;
          if (puVar4 == (undefined1 *)0xffffffffffffffff) {
                    /* WARNING: Subroutine does not return */
            FUN_0020edd0(&local_270);
          }
          goto LAB_031ab87c;
        }
LAB_031ab88c:
        iVar1 = thunk_FUN_05e1d97c(3);
        if (iVar1 != 0) {
          FUN_0488143c(local_290);
          ppppuVar5 = (undefined8 ****)local_290[0];
          if (-1 < cStack_279) {
            ppppuVar5 = local_290;
          }
          if ((DAT_0a3dd363 & 1) == 0) {
            uVar2 = 0;
            do {
              (&DAT_0a3dd350)[uVar2] = (&DAT_088bce97)[uVar2] + 0x8a ^ (&DAT_088bce87)[uVar2 & 0xf];
              uVar2 = uVar2 + 1;
            } while (uVar2 != 0x13);
            DAT_0a3dd363 = 1;
          }
          if ((DAT_0a3dec24 & 1) == 0) {
            uRam000000000a3dec18._0_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x78];
            uRam000000000a3dec18._1_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x79];
            uRam000000000a3dec18._2_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7a];
            uRam000000000a3dec18._3_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7b];
            uRam000000000a3dec18._4_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7c];
            uRam000000000a3dec18._5_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7d];
            uRam000000000a3dec18._6_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7e];
            uRam000000000a3dec18._7_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7f];
            DAT_0a3dec10 = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x70];
            DAT_0a3dec10_1._0_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x71];
            DAT_0a3dec10_1._1_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x72];
            DAT_0a3dec10_1._2_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x73];
            DAT_0a3dec10_1._3_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x74];
            DAT_0a3dec10_1._4_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x75];
            DAT_0a3dec10_1._5_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x76];
            DAT_0a3dec10_1._6_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x77];
            DAT_0a3dec20 = (undefined4)ram0x087913e0;
            DAT_0a3dec24 = 1;
          }
          FUN_05e1d050(&local_258,3,ppppuVar5,&DAT_0a3dd350,&DAT_0a3dec10,0xa1d,0,0);
          if ((DAT_0a3dec4b & 1) == 0) {
            DAT_0a3dec40._0_1_ = s_top_diviGetReuseerror_tyItemAtIn_084efa30[0x10];
            DAT_0a3dec40._1_1_ = s_top_diviGetReuseerror_tyItemAtIn_084efa30[0x11];
            DAT_0a3dec40._2_1_ = s_top_diviGetReuseerror_tyItemAtIn_084efa30[0x12];
            DAT_0a3dec40._3_1_ = s_top_diviGetReuseerror_tyItemAtIn_084efa30[0x13];
            DAT_0a3dec40._4_1_ = s_top_diviGetReuseerror_tyItemAtIn_084efa30[0x14];
            DAT_0a3dec40._5_1_ = s_top_diviGetReuseerror_tyItemAtIn_084efa30[0x15];
            DAT_0a3dec40._6_1_ = s_top_diviGetReuseerror_tyItemAtIn_084efa30[0x16];
            DAT_0a3dec40._7_1_ = s_top_diviGetReuseerror_tyItemAtIn_084efa30[0x17];
            DAT_0a3dec48 = 0x6570;
            DAT_0a3dec4a = 0;
            DAT_0a3dec4b = 1;
          }
          uStack_78 = 0;
          local_80 = 0;
          uStack_68 = 0;
          uStack_70 = 0;
          uStack_98 = 0;
          local_a0 = 0;
          uStack_88 = 0;
          uStack_90 = 0;
          uStack_b8 = 0;
          local_c0 = 0;
          uStack_a8 = 0;
          uStack_b0 = 0;
          uStack_d8 = 0;
          local_e0 = 0;
          uStack_c8 = 0;
          uStack_d0 = 0;
          FUN_05e1d31c(&local_258,&DAT_0a3dec40,&local_e0);
LAB_031ab9c0:
          thunk_FUN_05e1d0bc(&local_258);
          if (cStack_279 < '\0') {
            __ZdlPvm(local_290[0],CONCAT17(cStack_279,local_280) & 0x7fffffffffffffff);
          }
        }
LAB_031ab9e0:
        uVar7 = 0;
        uVar8 = 2;
      }
      else {
        if (puVar4 != (undefined1 *)(long)local_260._7_1_) goto LAB_031ab88c;
        ppppuVar5 = &local_270;
LAB_031ab87c:
        iVar1 = _memcmp(ppppuVar5,&DAT_0a3dec30,(size_t)puVar4);
        if (iVar1 != 0) goto LAB_031ab88c;
        local_298 = &SUB_aaaaaaaaaaaaaaaa;
        local_298 = (undefined1 *)FUN_0571ce74(&local_278,&DAT_0a3dec30);
        iVar1 = FUN_04af2fcc(&local_298);
        if (iVar1 == 0) {
          local_2a0 = &SUB_aaaaaaaaaaaaaaaa;
          if ((DAT_0a3dec83 & 1) == 0) {
            DAT_0a3dec78._0_1_ = s_SendMsgFtouserna_tou_088bac38[8];
            DAT_0a3dec78._1_1_ = s_SendMsgFtouserna_tou_088bac38[9];
            DAT_0a3dec78._2_1_ = s_SendMsgFtouserna_tou_088bac38[10];
            DAT_0a3dec78._3_1_ = s_SendMsgFtouserna_tou_088bac38[0xb];
            DAT_0a3dec78._4_1_ = s_SendMsgFtouserna_tou_088bac38[0xc];
            DAT_0a3dec78._5_1_ = s_SendMsgFtouserna_tou_088bac38[0xd];
            DAT_0a3dec78._6_1_ = s_SendMsgFtouserna_tou_088bac38[0xe];
            DAT_0a3dec78._7_1_ = s_SendMsgFtouserna_tou_088bac38[0xf];
            DAT_0a3dec80 = 0x656d;
            DAT_0a3dec82 = 0;
            DAT_0a3dec83 = 1;
          }
          local_2a0 = (undefined1 *)FUN_0571ce74(&local_298,&DAT_0a3dec78);
          iVar1 = FUN_04af2fcc(&local_2a0);
          if (iVar1 == 0) {
            local_258 = (undefined1 *)FUN_0008a8b8(&local_2a0);
            uVar7 = FUN_0571ffc0(&local_258,"");
            __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
                      (&local_1c8,uVar7);
            local_2a8 = &SUB_aaaaaaaaaaaaaaaa;
            if ((DAT_0a3dea79 & 1) == 0) {
              DAT_0a3dea70._0_1_ = s_newmsgidsec_msg_bubble_tpreview__088babb8[0];
              DAT_0a3dea70._1_1_ = s_newmsgidsec_msg_bubble_tpreview__088babb8[1];
              DAT_0a3dea70._2_1_ = s_newmsgidsec_msg_bubble_tpreview__088babb8[2];
              DAT_0a3dea70._3_1_ = s_newmsgidsec_msg_bubble_tpreview__088babb8[3];
              DAT_0a3dea70._4_1_ = s_newmsgidsec_msg_bubble_tpreview__088babb8[4];
              DAT_0a3dea70._5_1_ = s_newmsgidsec_msg_bubble_tpreview__088babb8[5];
              DAT_0a3dea70._6_1_ = s_newmsgidsec_msg_bubble_tpreview__088babb8[6];
              DAT_0a3dea70._7_1_ = s_newmsgidsec_msg_bubble_tpreview__088babb8[7];
              DAT_0a3dea78 = 0;
              DAT_0a3dea79 = 1;
            }
            local_2a8 = (undefined1 *)FUN_0571ce74(&local_298,&DAT_0a3dea70);
            iVar1 = FUN_04af2fcc(&local_2a8);
            if (iVar1 != 0) {
              iVar1 = thunk_FUN_05e1d97c(3);
              if (iVar1 != 0) {
                FUN_0488143c(local_290);
                ppppuVar5 = (undefined8 ****)local_290[0];
                if (-1 < cStack_279) {
                  ppppuVar5 = local_290;
                }
                if ((DAT_0a3dd363 & 1) == 0) {
                  uVar2 = 0;
                  do {
                    (&DAT_0a3dd350)[uVar2] =
                         (&DAT_088bce97)[uVar2] + 0x8a ^ (&DAT_088bce87)[uVar2 & 0xf];
                    uVar2 = uVar2 + 1;
                  } while (uVar2 != 0x13);
                  DAT_0a3dd363 = 1;
                }
                if ((DAT_0a3dec24 & 1) == 0) {
                  uRam000000000a3dec18._0_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x78];
                  uRam000000000a3dec18._1_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x79];
                  uRam000000000a3dec18._2_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7a];
                  uRam000000000a3dec18._3_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7b];
                  uRam000000000a3dec18._4_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7c];
                  uRam000000000a3dec18._5_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7d];
                  uRam000000000a3dec18._6_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7e];
                  uRam000000000a3dec18._7_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7f];
                  DAT_0a3dec10 = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x70];
                  DAT_0a3dec10_1._0_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x71];
                  DAT_0a3dec10_1._1_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x72];
                  DAT_0a3dec10_1._2_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x73];
                  DAT_0a3dec10_1._3_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x74];
                  DAT_0a3dec10_1._4_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x75];
                  DAT_0a3dec10_1._5_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x76];
                  DAT_0a3dec10_1._6_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x77];
                  DAT_0a3dec20 = (undefined4)ram0x087913e0;
                  DAT_0a3dec24 = 1;
                }
                FUN_05e1d050(&local_258,3,ppppuVar5,&DAT_0a3dd350,&DAT_0a3dec10,0xa2f,0,0);
                if ((DAT_0a3decc7 & 1) == 0) {
                  _DAT_0a3deca8 = CONCAT44((int)DAT_085d7578,(int)DAT_084f9040);
                  uRam000000000a3decb0 = CONCAT44((int)DAT_084a5d18,(int)DAT_085315f0);
                  DAT_0a3decb8 = CONCAT44((int)DAT_0852c728,(int)DAT_084e4b20);
                  DAT_0a3decc0 = (undefined4)DAT_087408e8;
                  DAT_0a3decc4 = 0x6c6c;
                  DAT_0a3decc6 = 0;
                  DAT_0a3decc7 = 1;
                }
                uStack_78 = 0;
                local_80 = 0;
                uStack_68 = 0;
                uStack_70 = 0;
                uStack_98 = 0;
                local_a0 = 0;
                uStack_88 = 0;
                uStack_90 = 0;
                uStack_b8 = 0;
                local_c0 = 0;
                uStack_a8 = 0;
                uStack_b0 = 0;
                uStack_d8 = 0;
                local_e0 = 0;
                uStack_c8 = 0;
                uStack_d0 = 0;
                FUN_05e1d31c(&local_258,&DAT_0a3deca8,&local_e0);
                goto LAB_031ab9c0;
              }
              goto LAB_031ab9e0;
            }
            local_250 = &SUB_aaaaaaaaaaaaaaaa;
            local_248 = &SUB_aaaaaaaaaaaaaaaa;
            local_258 = &SUB_aaaaaaaaaaaaaaaa;
            local_e0 = FUN_0008a8b8(&local_2a8);
            uVar7 = FUN_0571ffc0(&local_e0,"");
            FUN_00255b9c(&local_258,uVar7);
            lVar6 = FUN_04b56844(&local_258,0);
            uVar7 = 0;
            uVar2 = local_1c0;
            if (-1 < (long)local_1b8) {
              uVar2 = local_1b8 >> 0x38;
            }
            uVar8 = 2;
            if ((lVar6 != 0) && (uVar2 != 0)) {
              uVar7 = FUN_031ac1dc(param_1,&local_1c8,lVar6,5);
              uVar8 = 0;
            }
            if ((long)local_248 < 0) {
              __ZdlPvm(local_258,(ulong)local_248 & 0x7fffffffffffffff);
            }
            goto LAB_031ab9e8;
          }
          iVar1 = thunk_FUN_05e1d97c(3);
          if (iVar1 != 0) {
            FUN_0488143c(local_290);
            ppppuVar5 = (undefined8 ****)local_290[0];
            if (-1 < cStack_279) {
              ppppuVar5 = local_290;
            }
            if ((DAT_0a3dd363 & 1) == 0) {
              uVar2 = 0;
              do {
                (&DAT_0a3dd350)[uVar2] =
                     (&DAT_088bce97)[uVar2] + 0x8a ^ (&DAT_088bce87)[uVar2 & 0xf];
                uVar2 = uVar2 + 1;
              } while (uVar2 != 0x13);
              DAT_0a3dd363 = 1;
            }
            if ((DAT_0a3dec24 & 1) == 0) {
              uRam000000000a3dec18._0_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x78];
              uRam000000000a3dec18._1_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x79];
              uRam000000000a3dec18._2_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7a];
              uRam000000000a3dec18._3_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7b];
              uRam000000000a3dec18._4_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7c];
              uRam000000000a3dec18._5_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7d];
              uRam000000000a3dec18._6_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7e];
              uRam000000000a3dec18._7_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7f];
              DAT_0a3dec10 = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x70];
              DAT_0a3dec10_1._0_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x71];
              DAT_0a3dec10_1._1_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x72];
              DAT_0a3dec10_1._2_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x73];
              DAT_0a3dec10_1._3_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x74];
              DAT_0a3dec10_1._4_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x75];
              DAT_0a3dec10_1._5_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x76];
              DAT_0a3dec10_1._6_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x77];
              DAT_0a3dec20 = (undefined4)ram0x087913e0;
              DAT_0a3dec24 = 1;
            }
            FUN_05e1d050(&local_258,3,ppppuVar5,&DAT_0a3dd350,&DAT_0a3dec10,0xa28,0,0);
            if ((DAT_0a3deca5 & 1) == 0) {
              _DAT_0a3dec84 = CONCAT44((int)DAT_085d7578,(int)DAT_084f9040);
              uRam000000000a3dec8c = CONCAT44((int)DAT_084a5d18,(int)DAT_085315f0);
              _DAT_0a3dec94 = CONCAT44((int)DAT_084ca398,(int)ram0x088bac48);
              uRam000000000a3dec9c = CONCAT44((int)DAT_08486088,(int)DAT_0847fdf8);
              DAT_0a3deca4 = 0;
              DAT_0a3deca5 = 1;
            }
            uStack_78 = 0;
            local_80 = 0;
            uStack_68 = 0;
            uStack_70 = 0;
            uStack_98 = 0;
            local_a0 = 0;
            uStack_88 = 0;
            uStack_90 = 0;
            uStack_b8 = 0;
            local_c0 = 0;
            uStack_a8 = 0;
            uStack_b0 = 0;
            uStack_d8 = 0;
            local_e0 = 0;
            uStack_c8 = 0;
            uStack_d0 = 0;
            FUN_05e1d31c(&local_258,&DAT_0a3dec84,&local_e0);
            goto LAB_031ab9c0;
          }
          goto LAB_031ab9e0;
        }
        iVar1 = thunk_FUN_05e1d97c(3);
        if (iVar1 != 0) {
          FUN_0488143c(local_290);
          ppppuVar5 = (undefined8 ****)local_290[0];
          if (-1 < cStack_279) {
            ppppuVar5 = local_290;
          }
          if ((DAT_0a3dd363 & 1) == 0) {
            uVar2 = 0;
            do {
              (&DAT_0a3dd350)[uVar2] = (&DAT_088bce97)[uVar2] + 0x8a ^ (&DAT_088bce87)[uVar2 & 0xf];
              uVar2 = uVar2 + 1;
            } while (uVar2 != 0x13);
            DAT_0a3dd363 = 1;
          }
          if ((DAT_0a3dec24 & 1) == 0) {
            uRam000000000a3dec18._0_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x78];
            uRam000000000a3dec18._1_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x79];
            uRam000000000a3dec18._2_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7a];
            uRam000000000a3dec18._3_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7b];
            uRam000000000a3dec18._4_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7c];
            uRam000000000a3dec18._5_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7d];
            uRam000000000a3dec18._6_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7e];
            uRam000000000a3dec18._7_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7f];
            DAT_0a3dec10 = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x70];
            DAT_0a3dec10_1._0_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x71];
            DAT_0a3dec10_1._1_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x72];
            DAT_0a3dec10_1._2_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x73];
            DAT_0a3dec10_1._3_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x74];
            DAT_0a3dec10_1._4_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x75];
            DAT_0a3dec10_1._5_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x76];
            DAT_0a3dec10_1._6_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x77];
            DAT_0a3dec20 = (undefined4)ram0x087913e0;
            DAT_0a3dec24 = 1;
          }
          FUN_05e1d050(&local_258,3,ppppuVar5,&DAT_0a3dd350,&DAT_0a3dec10,0xa23,0,0);
          if ((DAT_0a3dec70 & 1) == 0) {
            _DAT_0a3dec4c = CONCAT44((int)DAT_085d7578,(int)DAT_084f9040);
            uRam000000000a3dec54 = CONCAT44((int)DAT_084a5d18,(int)DAT_085315f0);
            _DAT_0a3dec5c = CONCAT44((int)ram0x0858c8d0,(int)ram0x087e2e38);
            uRam000000000a3dec64 = CONCAT44((int)DAT_0873a968,(int)DAT_0848afe0);
            DAT_0a3dec6c = (undefined4)DAT_084ca380;
            DAT_0a3dec70 = 1;
          }
          uStack_78 = 0;
          local_80 = 0;
          uStack_68 = 0;
          uStack_70 = 0;
          uStack_98 = 0;
          local_a0 = 0;
          uStack_88 = 0;
          uStack_90 = 0;
          uStack_b8 = 0;
          local_c0 = 0;
          uStack_a8 = 0;
          uStack_b0 = 0;
          uStack_d8 = 0;
          local_e0 = 0;
          uStack_c8 = 0;
          uStack_d0 = 0;
          FUN_05e1d31c(&local_258,&DAT_0a3dec4c,&local_e0);
          thunk_FUN_05e1d0bc(&local_258);
          if (cStack_279 < '\0') {
            __ZdlPvm(local_290[0],CONCAT17(cStack_279,local_280) & 0x7fffffffffffffff);
          }
        }
        uVar7 = 0;
        uVar8 = 1;
      }
LAB_031ab9e8:
      if ((long)local_260 < 0) {
        __ZdlPvm(local_270,(ulong)local_260 & 0x7fffffffffffffff);
      }
      if ((uVar8 | 2) == 2) goto joined_r0x031aba10;
    }
    else {
      iVar1 = thunk_FUN_05e1d97c(3);
      if (iVar1 != 0) {
        FUN_0488143c(&local_270);
        ppppuVar5 = (undefined8 ****)local_270;
        if (-1 < (long)local_260) {
          ppppuVar5 = &local_270;
        }
        if ((DAT_0a3dd363 & 1) == 0) {
          uVar2 = 0;
          do {
            (&DAT_0a3dd350)[uVar2] = (&DAT_088bce97)[uVar2] + 0x8a ^ (&DAT_088bce87)[uVar2 & 0xf];
            uVar2 = uVar2 + 1;
          } while (uVar2 != 0x13);
          DAT_0a3dd363 = 1;
        }
        if ((DAT_0a3dec24 & 1) == 0) {
          uRam000000000a3dec18._0_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x78];
          uRam000000000a3dec18._1_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x79];
          uRam000000000a3dec18._2_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7a];
          uRam000000000a3dec18._3_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7b];
          uRam000000000a3dec18._4_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7c];
          uRam000000000a3dec18._5_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7d];
          uRam000000000a3dec18._6_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7e];
          uRam000000000a3dec18._7_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x7f];
          DAT_0a3dec10 = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x70];
          DAT_0a3dec10_1._0_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x71];
          DAT_0a3dec10_1._1_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x72];
          DAT_0a3dec10_1._2_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x73];
          DAT_0a3dec10_1._3_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x74];
          DAT_0a3dec10_1._4_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x75];
          DAT_0a3dec10_1._5_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x76];
          DAT_0a3dec10_1._6_1_ = s_ReceiveAddMsgLisIsNeedFilterMess_088bb4c0[0x77];
          DAT_0a3dec20 = (undefined4)ram0x087913e0;
          DAT_0a3dec24 = 1;
        }
        FUN_05e1d050(&local_258,3,ppppuVar5,&DAT_0a3dd350,&DAT_0a3dec10,0xa18,0,0);
        if ((DAT_0a3dea49 & 1) == 0) {
          _DAT_0a3dea2c = CONCAT44((int)DAT_085d7578,(int)DAT_084f9040);
          uRam000000000a3dea34 = CONCAT44((int)DAT_084a5d18,(int)DAT_085315f0);
          DAT_0a3dea3c = CONCAT44((int)DAT_08673270,(int)DAT_08709590);
          DAT_0a3dea44 = (undefined4)DAT_08486088;
          DAT_0a3dea48 = 0;
          DAT_0a3dea49 = 1;
        }
        uStack_78 = 0;
        local_80 = 0;
        uStack_68 = 0;
        uStack_70 = 0;
        uStack_98 = 0;
        local_a0 = 0;
        uStack_88 = 0;
        uStack_90 = 0;
        uStack_b8 = 0;
        local_c0 = 0;
        uStack_a8 = 0;
        uStack_b0 = 0;
        uStack_d8 = 0;
        local_e0 = 0;
        uStack_c8 = 0;
        uStack_d0 = 0;
        FUN_05e1d31c(&local_258,&DAT_0a3dea2c,&local_e0);
        goto LAB_031ab714;
      }
    }
  }
  uVar7 = 0;
joined_r0x031aba10:
  if ((long)local_1b8 < 0) {
    __ZdlPvm(local_1c8,local_1b8 & 0x7fffffffffffffff);
  }
  FUN_0572116c(&local_1b0);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_58) {
    return uVar7;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


