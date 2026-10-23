// Ghidra inferred pseudocode; requested=0x5cc4468
// entry=05cc4468 end=05cc7393

/* WARNING: Type propagation algorithm not settling */

undefined8 FUN_05cc4468(void)

{
  ulong uVar1;
  undefined4 uVar2;
  undefined1 uVar3;
  undefined1 auVar4 [4];
  undefined8 *******pppppppuVar5;
  bool bVar6;
  bool bVar7;
  int iVar8;
  int iVar9;
  undefined8 uVar10;
  undefined8 uVar11;
  ulong uVar12;
  long *plVar13;
  long *******ppppppplVar14;
  undefined8 *puVar15;
  undefined8 in_x4;
  undefined4 *in_x6;
  uint uVar16;
  long lVar17;
  undefined1 *puVar18;
  undefined1 *puVar19;
  ulong uVar20;
  undefined4 uVar21;
  undefined8 *puVar22;
  long lVar23;
  undefined1 auVar24 [12];
  long *******in_stack_00000000;
  undefined2 in_stack_00000008;
  long in_stack_00000010;
  undefined8 local_1108 [2];
  char local_10f1;
  long *******local_10f0 [2];
  char local_10d9;
  undefined8 local_10d8 [2];
  char local_10c1;
  undefined8 local_10c0;
  undefined8 local_10b8;
  undefined8 uStack_10b0;
  long local_10a8;
  undefined8 local_10a0;
  undefined8 uStack_1098;
  undefined8 local_1090;
  undefined8 local_1088;
  undefined8 uStack_1080;
  long local_1078;
  undefined8 local_1070;
  undefined8 uStack_1068;
  undefined8 local_1060;
  undefined8 local_1058;
  undefined8 uStack_1050;
  long local_1048;
  undefined8 local_1040;
  undefined8 uStack_1038;
  undefined8 local_1030;
  undefined8 local_1028;
  undefined8 uStack_1020;
  long local_1018;
  undefined8 local_1010;
  undefined8 uStack_1008;
  undefined8 local_1000 [2];
  char local_fe9;
  undefined8 local_fe8;
  undefined8 local_fe0;
  undefined8 uStack_fd8;
  long local_fd0;
  undefined8 local_fc8;
  undefined8 uStack_fc0;
  long *******local_fb8 [2];
  char local_fa1;
  long *******local_fa0 [2];
  char local_f89;
  long *******local_f88 [2];
  char local_f71;
  long *******local_f70;
  ulong local_f68;
  undefined8 uStack_f60;
  long *******local_f58 [2];
  char local_f41;
  undefined8 local_f40 [2];
  char local_f29;
  undefined8 *******local_f28;
  ulong uStack_f20;
  ulong local_f18;
  undefined8 local_f10;
  undefined8 local_f08;
  undefined8 uStack_f00;
  long local_ef8;
  undefined8 local_ef0;
  undefined8 uStack_ee8;
  undefined1 auStack_ee0 [8];
  undefined8 local_ed8;
  undefined8 *local_ed0;
  undefined1 local_ec8;
  byte local_ec4;
  undefined8 *local_ec0;
  undefined1 local_eb8;
  char local_eb6;
  char local_eb5;
  char local_eb4;
  char local_eb3;
  long local_eb0;
  long local_ea8;
  uint local_e9c;
  undefined4 local_e98;
  undefined4 uStack_e94;
  undefined8 local_e90;
  undefined8 uStack_e88;
  long local_e80;
  undefined8 local_e78;
  undefined4 uStack_e70;
  undefined4 uStack_e6c;
  undefined1 local_e64 [4];
  undefined8 local_e60;
  undefined8 local_e58;
  char local_e49;
  undefined8 local_e10;
  undefined8 local_e08;
  undefined8 *local_e00;
  undefined8 *local_df8;
  undefined8 *local_df0;
  undefined8 *local_de8;
  undefined8 *local_de0;
  undefined8 *local_dd8;
  undefined8 *local_dd0;
  undefined8 *local_dc8;
  undefined8 local_dc0;
  undefined8 uStack_db8;
  undefined8 uStack_db0;
  undefined8 uStack_da8;
  undefined8 local_da0;
  undefined8 uStack_d98;
  undefined8 *local_d80;
  long *******local_d78;
  undefined8 *local_d70;
  undefined8 *puStack_d68;
  undefined8 *puStack_d60;
  undefined8 *local_d58;
  undefined8 *puStack_d50;
  undefined8 *local_d48;
  undefined8 *puStack_d40;
  undefined8 *local_d38;
  undefined8 *puStack_d30;
  undefined8 local_d28;
  undefined8 uStack_d20;
  undefined8 local_d18;
  undefined8 uStack_d10;
  undefined8 local_d08;
  undefined8 local_980;
  undefined8 local_978;
  char local_969;
  undefined8 local_930;
  undefined8 local_928;
  char local_919;
  undefined8 local_8e0;
  undefined8 local_8d8;
  char local_8c9;
  undefined8 local_890;
  undefined8 local_888;
  char local_879;
  undefined8 local_840;
  undefined8 local_838;
  char local_829;
  uint *local_7f0 [128];
  undefined8 local_3f0;
  undefined8 local_3e8;
  undefined8 local_3a0;
  undefined8 local_398;
  undefined8 local_350;
  undefined8 local_348;
  undefined8 local_300;
  undefined8 uStack_2f8;
  long local_2f0;
  long *******local_2a8;
  ulong local_2a0;
  long local_298;
  int local_290;
  undefined8 local_288;
  ulong uStack_280;
  ulong local_278;
  undefined8 uStack_270;
  undefined8 local_268;
  undefined8 uStack_260;
  undefined8 local_258;
  undefined8 uStack_250;
  undefined8 local_248;
  undefined8 *local_240;
  undefined8 local_238;
  undefined8 local_230;
  undefined8 local_228;
  undefined8 uStack_220;
  undefined8 local_218;
  undefined8 uStack_210;
  undefined8 local_208;
  undefined8 uStack_200;
  undefined8 local_1f8;
  undefined8 local_1f0;
  undefined2 local_1e8;
  uint local_1e4;
  undefined4 local_1e0;
  undefined8 local_1d8;
  undefined8 local_1d0;
  undefined8 *******local_1c8;
  ulong local_1c0;
  undefined2 local_1b8;
  undefined2 local_1b6;
  byte local_1ac;
  undefined1 local_1ab;
  undefined2 local_1aa;
  undefined2 local_1a8;
  undefined4 local_1a4;
  long local_1a0;
  undefined1 local_198;
  undefined1 auStack_190 [40];
  undefined8 local_168;
  ulong local_160;
  ulong local_158;
  undefined8 local_148;
  undefined8 local_140;
  undefined8 local_138;
  undefined8 uStack_130;
  long local_128;
  undefined8 uStack_120;
  undefined8 local_118;
  long lStack_110;
  ulong local_108;
  undefined1 local_100;
  byte local_ff;
  undefined8 local_f8;
  undefined8 local_f0;
  undefined8 *local_e8;
  undefined8 *puStack_e0;
  undefined8 *local_d8;
  undefined8 *puStack_d0;
  undefined8 *local_c8;
  undefined8 *puStack_c0;
  undefined8 *local_b8;
  undefined8 *puStack_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  long local_78;
  
  auVar24 = (*(code *)PTR____chkstk_darwin_09b36ba8)();
  local_e64 = auVar24._8_4_;
  puVar15 = auVar24._0_8_;
  local_78 = *(long *)PTR____stack_chk_guard_09b36c98;
  uStack_e88 = 0;
  local_e90 = 0;
  local_e80 = 0;
  local_e98 = 1;
  uStack_e94 = (undefined4)*(undefined8 *)(in_stack_00000010 + 0x60);
  ppppppplVar14 = (long *******)(in_stack_00000010 + 0x18);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(&local_e90,ppppppplVar14)
  ;
  local_e78 = CONCAT44(1,(undefined4)local_e78);
  FUN_05ce425c(auStack_ee0);
  uVar10 = FUN_056300b4(in_stack_00000010 + 0x1c8,0);
  uVar11 = FUN_009ce4a8(in_stack_00000010 + 0x1c8);
  uVar12 = FUN_05ab3ab8(auStack_ee0,uVar10,uVar11);
  if ((uVar12 & 1) == 0) {
    iVar8 = thunk_FUN_05e1d97c(4);
    if (iVar8 != 0) {
      FUN_05e1d050(local_7f0,4,"mars::account","account_core.cc","MMReq2Buf",0x14a,0,0);
      local_1f0 = (undefined2 *)0x0;
      uVar12 = (ulong)(uint)local_e64;
      uVar1 = 8;
      do {
        uVar20 = uVar1;
        uVar16 = (uint)uVar12;
        *(char *)((long)&local_1f0 + uVar20) =
             "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
             [uVar16 + (int)(uVar12 / 10) * -10 + 0x23];
        uVar12 = uVar12 / 10;
        uVar1 = uVar20 + 1;
      } while (9 < uVar16);
      local_d80 = &local_1f0;
      *(undefined1 *)((long)local_d80 + uVar20 + 1) = 0;
      local_1f0 = &local_1e8;
      if (8 < uVar20) {
        puVar18 = (undefined1 *)((long)&local_1f0 + uVar20);
        puVar19 = (undefined1 *)((long)&local_1e8 + 1);
        do {
          uVar3 = *puVar18;
          *puVar18 = puVar19[-1];
          puVar19[-1] = uVar3;
          bVar6 = puVar19 < puVar18 + -1;
          puVar18 = puVar18 + -1;
          puVar19 = puVar19 + 1;
        } while (bVar6);
      }
      local_2a8 = *(long ********)(in_stack_00000010 + 0x18);
      if (-1 < *(char *)(in_stack_00000010 + 0x2f)) {
        local_2a8 = ppppppplVar14;
      }
      local_2a0 = local_2a0 & 0xffffffffffffff00;
      local_e10 = (long *******)*in_stack_00000000;
      if (-1 < *(char *)((long)in_stack_00000000 + 0x17)) {
        local_e10 = in_stack_00000000;
      }
      local_e08 = (long ******)((ulong)local_e08 & 0xffffffffffffff00);
      local_d78 = (long *******)&local_2a8;
      local_d70 = &local_e10;
      puStack_d60 = (undefined8 *)0x0;
      puStack_d68 = (undefined8 *)0x0;
      puStack_d50 = (undefined8 *)0x0;
      local_d58 = (undefined8 *)0x0;
      puStack_d40 = (undefined8 *)0x0;
      local_d48 = (undefined8 *)0x0;
      puStack_d30 = (undefined8 *)0x0;
      local_d38 = (undefined8 *)0x0;
      uStack_d20 = 0;
      local_d28 = 0;
      uStack_d10 = 0;
      local_d18 = 0;
      local_d08 = 0;
      FUN_05e1d31c(local_7f0,"mmpack taskid:%_, cgi:%_, host:%_ parse reqbuf fail. ",&local_d80);
      thunk_FUN_05e1d0bc(local_7f0);
    }
    uStack_e70 = 0x12;
    uVar10 = FUN_0597d418(*puVar15);
    auVar4 = local_e64;
    local_f10 = CONCAT44(uStack_e94,local_e98);
    if (local_e80 < 0) {
      FUN_00018d20(&local_f08,local_e90,uStack_e88);
    }
    else {
      uStack_f00 = uStack_e88;
      local_f08 = local_e90;
      local_ef8 = local_e80;
    }
    uStack_ee8 = CONCAT44(uStack_e6c,uStack_e70);
    local_ef0 = local_e78;
    FUN_05cc1d54(uVar10,auVar4,&local_f10);
    if (local_ef8 < 0) {
      __ZdlPv(local_f08);
    }
  }
  else {
    if ((*(char *)(in_stack_00000010 + 0x1c0) != '\x01') ||
       (((*(byte *)(in_stack_00000010 + 0x30) & 1) == 0 && (local_eb3 != '\x01')))) {
      local_1c0 = 0;
      local_1c8 = (undefined8 *******)0x0;
      FUN_05ded178(auStack_190,0x80);
      local_160 = 0;
      local_168 = 0;
      local_158 = 0;
      uStack_130 = 0;
      local_138 = 0;
      uStack_120 = 0;
      local_128 = 0;
      lStack_110 = 0;
      local_118 = 0;
      local_1d8 = local_ed8;
      local_1d0 = local_ed8;
      local_1b8 = (undefined2)*(undefined8 *)(in_stack_00000010 + 0x60);
      local_1e0 = *(undefined4 *)((long)puVar15 + 0x34);
      local_1b6 = *(undefined2 *)(puVar15 + 6);
      local_1a0 = (long)(puVar15 + 3);
      if (*(char *)((long)puVar15 + 0x2f) < '\0') {
        local_1a0 = *(long *)local_1a0;
      }
      iVar8 = FUN_05cc91f8();
      if (iVar8 != 0) {
        local_1a8 = in_stack_00000008;
      }
      local_198 = 0;
      local_1f0 = (undefined2 *)CONCAT62(local_1f0._2_6_,1);
      local_140 = 0;
      local_148 = 0;
      local_f28 = (undefined8 *******)0x0;
      uStack_f20 = 0;
      local_f18 = 0;
      __ZNSt3__119__shared_mutex_base11lock_sharedEv(puVar15 + 0x34);
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (&local_f28,puVar15 + 0x14);
      __ZNSt3__119__shared_mutex_base13unlock_sharedEv(puVar15 + 0x34);
      local_2a0 = 0;
      local_2a8 = (long *******)0x0;
      local_298 = 0;
      local_240 = &local_238;
      local_230 = 0;
      local_238 = 0;
      uStack_280 = 0;
      local_288 = 0;
      uStack_270 = 0;
      local_278 = 0;
      uStack_260 = 0;
      local_268 = 0;
      uStack_250 = 0;
      local_258 = 0;
      local_248 = 0;
      uStack_220 = 0;
      local_228 = 0;
      uStack_210 = 0;
      local_218 = 0;
      uStack_200 = 0;
      local_208 = 0;
      local_1f8 = 0;
      if (local_eb6 == '\x01') {
        iVar8 = thunk_FUN_05e1d97c(2);
        if (iVar8 != 0) {
          FUN_05e1d050(local_7f0,2,"mars::account","account_core.cc","MMReq2Buf",0x180,0,0);
          local_e10 = (long *******)0x0;
          uVar12 = (ulong)(uint)local_e64;
          uVar1 = 8;
          do {
            uVar20 = uVar1;
            uVar16 = (uint)uVar12;
            *(char *)((long)&local_e10 + uVar20) =
                 "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                 [uVar16 + (int)(uVar12 / 10) * -10 + 0x23];
            uVar12 = uVar12 / 10;
            uVar1 = uVar20 + 1;
          } while (9 < uVar16);
          *(undefined1 *)((long)&local_e10 + uVar20 + 1) = 0;
          local_e10 = (long *******)&local_e08;
          if (8 < uVar20) {
            puVar18 = (undefined1 *)((long)&local_e10 + uVar20);
            puVar19 = (undefined1 *)((long)&local_e08 + 1);
            do {
              uVar3 = *puVar18;
              *puVar18 = puVar19[-1];
              puVar19[-1] = uVar3;
              bVar6 = puVar19 < puVar18 + -1;
              puVar18 = puVar18 + -1;
              puVar19 = puVar19 + 1;
            } while (bVar6);
          }
          lVar17 = local_eb0;
          if (local_eb0 == 0) {
            lVar17 = *(long *)(DAT_0a5250d8 + 0x30);
          }
          local_d80._0_4_ = *(undefined4 *)(lVar17 + 8);
          local_f8 = (long *******)0x0;
          FUN_003eccb4(&local_d80,&local_f0,10,1);
          lVar17 = local_eb0;
          if (local_eb0 == 0) {
            lVar17 = *(long *)(DAT_0a5250d8 + 0x30);
          }
          local_d80 = (undefined8 *)CONCAT44(local_d80._4_4_,*(undefined4 *)(lVar17 + 0xc));
          local_300 = (long *******)0x0;
          local_f8 = (long *******)&local_f0;
          FUN_003eccb4(&local_d80,&uStack_2f8,10,1);
          lVar17 = local_eb0;
          if (local_eb0 == 0) {
            lVar17 = *(long *)(DAT_0a5250d8 + 0x30);
          }
          local_300 = (long *******)&uStack_2f8;
          FUN_05e17fdc(&local_890,*(undefined8 *)(lVar17 + 0x10));
          FUN_05cc9218(&local_840,&local_890);
          local_350 = local_840;
          if (-1 < local_829) {
            local_350 = (long *******)&local_840;
          }
          local_348._0_1_ = 0;
          lVar17 = local_eb0;
          if (local_eb0 == 0) {
            lVar17 = *(long *)(DAT_0a5250d8 + 0x30);
          }
          FUN_05e17fdc(&local_930,*(undefined8 *)(lVar17 + 0x18));
          FUN_05cc9218(&local_8e0,&local_930);
          local_3a0 = local_8e0;
          if (-1 < local_8c9) {
            local_3a0 = (long *******)&local_8e0;
          }
          local_398._0_1_ = 0;
          lVar17 = local_eb0;
          if (local_eb0 == 0) {
            lVar17 = *(long *)(DAT_0a5250d8 + 0x30);
          }
          bVar6 = (*(byte *)(lVar17 + 0x2c) >> 4 & 1) != 0;
          if (bVar6) {
            FUN_05e17fdc(local_f40,*(undefined8 *)(lVar17 + 0x20));
            FUN_05cc9218(&local_980,local_f40);
          }
          else {
            FUN_05941fe8(&local_980,"empty");
          }
          local_3f0 = local_980;
          if (-1 < local_969) {
            local_3f0 = (long *******)&local_980;
          }
          local_3e8._0_1_ = 0;
          local_d80 = &local_e10;
          local_d78 = (long *******)&local_f8;
          local_d70 = &local_300;
          puStack_d68 = &local_350;
          puStack_d60 = &local_3a0;
          local_d58 = &local_3f0;
          local_d48 = (undefined8 *)0x0;
          puStack_d50 = (undefined8 *)0x0;
          local_d38 = (undefined8 *)0x0;
          puStack_d40 = (undefined8 *)0x0;
          local_d28 = 0;
          puStack_d30 = (undefined8 *)0x0;
          local_d18 = 0;
          uStack_d20 = 0;
          local_d08 = 0;
          uStack_d10 = 0;
          FUN_05e1d31c(local_7f0,
                       "mmpack taskid:%_ certVersion:%_, Nid:%_ EcdhKey:%_ EcdasKey:%_ AuthKey:%_",
                       &local_d80);
          if (local_969 < '\0') {
            __ZdlPv(local_980);
          }
          if ((bVar6) && (local_f29 < '\0')) {
            __ZdlPv(local_f40[0]);
          }
          if (local_8c9 < '\0') {
            __ZdlPv(local_8e0);
          }
          if (local_919 < '\0') {
            __ZdlPv(local_930);
          }
          if (local_829 < '\0') {
            __ZdlPv(local_840);
          }
          if (local_879 < '\0') {
            __ZdlPv(local_890);
          }
          thunk_FUN_05e1d0bc(local_7f0);
        }
        lVar23 = local_eb0;
        lVar17 = DAT_0a5250d8;
        local_e78 = DAT_08b9b138;
        if (local_eb0 == 0) {
          uVar21 = *(undefined4 *)(*(long *)(DAT_0a5250d8 + 0x30) + 8);
          _bzero(local_7f0,0x400);
          lVar17 = *(long *)(lVar17 + 0x30);
        }
        else {
          uVar21 = *(undefined4 *)(local_eb0 + 8);
          _bzero(local_7f0,0x400);
          lVar17 = lVar23;
        }
        plVar13 = *(long **)(lVar17 + 0x10);
        if (*(char *)((long)plVar13 + 0x17) < '\0') {
          plVar13 = (long *)*plVar13;
        }
        if (lVar23 == 0) {
          lVar23 = *(long *)(DAT_0a5250d8 + 0x30);
        }
        lVar17 = (long)*(char *)(*(long *)(lVar23 + 0x10) + 0x17);
        if (lVar17 < 0) {
          lVar17 = *(long *)(*(long *)(lVar23 + 0x10) + 8);
        }
        iVar8 = FUN_05dee3f8(plVar13,local_7f0,lVar17);
        if (0 < iVar8) {
          _bzero(&local_d80,0x400);
          lVar17 = local_eb0;
          if (local_eb0 == 0) {
            lVar17 = *(long *)(DAT_0a5250d8 + 0x30);
          }
          plVar13 = *(long **)(lVar17 + 0x18);
          if (*(char *)((long)plVar13 + 0x17) < '\0') {
            plVar13 = (long *)*plVar13;
          }
          lVar17 = local_eb0;
          if (local_eb0 == 0) {
            lVar17 = *(long *)(DAT_0a5250d8 + 0x30);
          }
          lVar23 = (long)*(char *)(*(long *)(lVar17 + 0x18) + 0x17);
          if (lVar23 < 0) {
            lVar23 = *(long *)(*(long *)(lVar17 + 0x18) + 8);
          }
          iVar9 = FUN_05dee3f8(plVar13,&local_d80,lVar23);
          if (iVar9 < 1) {
            iVar8 = thunk_FUN_05e1d97c(4);
            if (iVar8 != 0) {
              FUN_05e1d050(&local_e10,4,"mars::account","account_core.cc","MMReq2Buf",0x1b4,0,0);
              local_300 = (long *******)0x0;
              uVar12 = (ulong)(uint)local_e64;
              uVar1 = 8;
              do {
                uVar20 = uVar1;
                uVar16 = (uint)uVar12;
                *(char *)((long)&local_300 + uVar20) =
                     "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                     [uVar16 + (int)(uVar12 / 10) * -10 + 0x23];
                uVar12 = uVar12 / 10;
                uVar1 = uVar20 + 1;
              } while (9 < uVar16);
              *(undefined1 *)((long)&local_300 + uVar20 + 1) = 0;
              local_300 = (long *******)&uStack_2f8;
              if (8 < uVar20) {
                puVar18 = (undefined1 *)((long)&local_300 + uVar20);
                puVar19 = (undefined1 *)((long)&uStack_2f8 + 1);
                do {
                  uVar3 = *puVar18;
                  *puVar18 = puVar19[-1];
                  puVar19[-1] = uVar3;
                  bVar6 = puVar19 < puVar18 + -1;
                  puVar18 = puVar18 + -1;
                  puVar19 = puVar19 + 1;
                } while (bVar6);
              }
              local_350 = *(long ********)(in_stack_00000010 + 0x18);
              if (-1 < *(char *)(in_stack_00000010 + 0x2f)) {
                local_350 = ppppppplVar14;
              }
              local_348._0_1_ = 0;
              local_3a0 = (long *******)*in_stack_00000000;
              if (-1 < *(char *)((long)in_stack_00000000 + 0x17)) {
                local_3a0 = in_stack_00000000;
              }
              local_398._0_1_ = 0;
              lVar17 = local_eb0;
              if (local_eb0 == 0) {
                lVar17 = *(long *)(DAT_0a5250d8 + 0x30);
              }
              local_f8 = (long *******)CONCAT44(local_f8._4_4_,*(undefined4 *)(lVar17 + 0xc));
              local_3f0 = (long *******)0x0;
              FUN_003eccb4(&local_f8,&local_3e8,10,1);
              lVar17 = local_eb0;
              if (local_eb0 == 0) {
                lVar17 = *(long *)(DAT_0a5250d8 + 0x30);
              }
              local_3f0 = (long *******)&local_3e8;
              FUN_05e17fdc(&local_f70,*(undefined8 *)(lVar17 + 0x10));
              FUN_05cc9218(local_f58,&local_f70);
              local_840 = local_f58[0];
              if (-1 < local_f41) {
                local_840 = (long *******)local_f58;
              }
              local_838._0_1_ = 0;
              lVar17 = local_eb0;
              if (local_eb0 == 0) {
                lVar17 = *(long *)(DAT_0a5250d8 + 0x30);
              }
              uVar12 = (ulong)*(char *)(*(long *)(lVar17 + 0x10) + 0x17);
              if ((long)uVar12 < 0) {
                uVar12 = *(ulong *)(*(long *)(lVar17 + 0x10) + 8);
              }
              local_890 = (long *******)0x0;
              uVar1 = 8;
              do {
                uVar20 = uVar1;
                *(char *)((long)&local_890 + uVar20) =
                     "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                     [uVar12 % 10 + 0x23];
                bVar6 = 9 < uVar12;
                uVar12 = uVar12 / 10;
                uVar1 = uVar20 + 1;
              } while (bVar6);
              *(undefined1 *)((long)&local_890 + uVar20 + 1) = 0;
              local_890 = (long *******)&local_888;
              if (8 < uVar20) {
                puVar18 = (undefined1 *)((long)&local_890 + uVar20);
                puVar19 = (undefined1 *)((long)&local_888 + 1);
                do {
                  uVar3 = *puVar18;
                  *puVar18 = puVar19[-1];
                  puVar19[-1] = uVar3;
                  bVar6 = puVar19 < puVar18 + -1;
                  puVar18 = puVar18 + -1;
                  puVar19 = puVar19 + 1;
                } while (bVar6);
              }
              lVar17 = local_eb0;
              if (local_eb0 == 0) {
                lVar17 = *(long *)(DAT_0a5250d8 + 0x30);
              }
              FUN_05e17fdc(local_fa0,*(undefined8 *)(lVar17 + 0x18));
              FUN_05cc9218(local_f88,local_fa0);
              local_8e0 = local_f88[0];
              if (-1 < local_f71) {
                local_8e0 = (long *******)local_f88;
              }
              local_8d8._0_1_ = 0;
              lVar17 = local_eb0;
              if (local_eb0 == 0) {
                lVar17 = *(long *)(DAT_0a5250d8 + 0x30);
              }
              uVar12 = (ulong)*(char *)(*(long *)(lVar17 + 0x18) + 0x17);
              if ((long)uVar12 < 0) {
                uVar12 = *(ulong *)(*(long *)(lVar17 + 0x18) + 8);
              }
              local_930 = (long *******)0x0;
              uVar1 = 8;
              do {
                uVar20 = uVar1;
                *(char *)((long)&local_930 + uVar20) =
                     "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                     [uVar12 % 10 + 0x23];
                bVar6 = 9 < uVar12;
                uVar12 = uVar12 / 10;
                uVar1 = uVar20 + 1;
              } while (bVar6);
              *(undefined1 *)((long)&local_930 + uVar20 + 1) = 0;
              local_930 = (long *******)&local_928;
              if (8 < uVar20) {
                puVar18 = (undefined1 *)((long)&local_930 + uVar20);
                puVar19 = (undefined1 *)((long)&local_928 + 1);
                do {
                  uVar3 = *puVar18;
                  *puVar18 = puVar19[-1];
                  puVar19[-1] = uVar3;
                  bVar6 = puVar19 < puVar18 + -1;
                  puVar18 = puVar18 + -1;
                  puVar19 = puVar19 + 1;
                } while (bVar6);
              }
              lVar17 = local_eb0;
              if (local_eb0 == 0) {
                lVar17 = *(long *)(DAT_0a5250d8 + 0x30);
              }
              bVar6 = (*(byte *)(lVar17 + 0x2c) >> 4 & 1) != 0;
              if (bVar6) {
                FUN_05e17fdc(local_1000,*(undefined8 *)(lVar17 + 0x20));
                FUN_05cc9218(local_fb8,local_1000);
              }
              else {
                FUN_05941fe8(local_fb8,"empty");
              }
              local_980 = local_fb8[0];
              if (-1 < local_fa1) {
                local_980 = (long *******)local_fb8;
              }
              local_978._0_1_ = 0;
              if (local_eb0 == 0) {
                local_eb0 = *(long *)(DAT_0a5250d8 + 0x30);
              }
              if ((*(byte *)(local_eb0 + 0x2c) >> 4 & 1) == 0) {
                uVar12 = 0;
              }
              else {
                uVar12 = (ulong)*(char *)(*(long *)(local_eb0 + 0x20) + 0x17);
                if ((long)uVar12 < 0) {
                  uVar12 = *(ulong *)(*(long *)(local_eb0 + 0x20) + 8);
                }
              }
              local_e60 = (long *******)0x0;
              uVar1 = 8;
              do {
                uVar20 = uVar1;
                *(char *)((long)&local_e60 + uVar20) =
                     "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                     [uVar12 % 10 + 0x23];
                bVar7 = 9 < uVar12;
                uVar12 = uVar12 / 10;
                uVar1 = uVar20 + 1;
              } while (bVar7);
              *(undefined1 *)((long)&local_e60 + uVar20 + 1) = 0;
              local_e60 = (long *******)&local_e58;
              if (8 < uVar20) {
                puVar18 = (undefined1 *)((long)&local_e60 + uVar20);
                puVar19 = (undefined1 *)((long)&local_e58 + 1);
                do {
                  uVar3 = *puVar18;
                  *puVar18 = puVar19[-1];
                  puVar19[-1] = uVar3;
                  bVar7 = puVar19 < puVar18 + -1;
                  puVar18 = puVar18 + -1;
                  puVar19 = puVar19 + 1;
                } while (bVar7);
              }
              local_f8 = (long *******)&local_300;
              local_f0 = (long ******)&local_350;
              local_e8 = &local_3a0;
              puStack_e0 = &local_3f0;
              local_d8 = &local_840;
              puStack_d0 = &local_890;
              local_c8 = &local_8e0;
              puStack_c0 = &local_930;
              local_b8 = &local_980;
              uStack_a0 = 0;
              local_a8 = 0;
              uStack_90 = 0;
              local_98 = 0;
              uStack_80 = 0;
              local_88 = 0;
              puStack_b0 = &local_e60;
              FUN_05e1d31c(&local_e10,
                           "mmpack taskid:%_, cgi:%_, host:%_ decodeBase64 failed for ecdsa_public_key. ecdh info nid:%_, ecdh_key:%_, len:%_, ecdsa_key:%_, len:%_ auth_key:%_, len:%_"
                           ,&local_f8);
              if (local_fa1 < '\0') {
                __ZdlPv(local_fb8[0]);
              }
              if ((bVar6) && (local_fe9 < '\0')) {
                __ZdlPv(local_1000[0]);
              }
              if (local_f71 < '\0') {
                __ZdlPv(local_f88[0]);
              }
              if (local_f89 < '\0') {
                __ZdlPv(local_fa0[0]);
              }
              if (local_f41 < '\0') {
                __ZdlPv(local_f58[0]);
              }
              if ((long)uStack_f60 < 0) {
                __ZdlPv(local_f70);
              }
              thunk_FUN_05e1d0bc(&local_e10);
            }
            uStack_e70 = 3;
            uVar10 = FUN_0597d418(*puVar15);
            auVar4 = local_e64;
            local_1030 = CONCAT44(uStack_e94,local_e98);
            if (local_e80 < 0) {
              FUN_00018d20(&local_1028,local_e90,uStack_e88);
            }
            else {
              uStack_1020 = uStack_e88;
              local_1028 = local_e90;
              local_1018 = local_e80;
            }
            uStack_1008 = CONCAT44(uStack_e6c,uStack_e70);
            local_1010 = local_e78;
            FUN_05cc1d54(uVar10,auVar4,&local_1030);
            if (local_1018 < 0) {
              __ZdlPv(local_1028);
            }
          }
          else {
            uVar10 = __Znwm(0x78);
            lVar17 = local_eb0;
            if (local_eb0 == 0) {
              lVar17 = *(long *)(DAT_0a5250d8 + 0x30);
            }
            uVar2 = *(undefined4 *)(lVar17 + 0xc);
            FUN_0597f37c(&local_e10,local_7f0,iVar8);
            FUN_0597f37c(&local_f8,&local_d80,iVar9);
            if (local_eb0 == 0) {
              local_eb0 = *(long *)(DAT_0a5250d8 + 0x30);
            }
            if ((*(byte *)(local_eb0 + 0x2c) >> 4 & 1) == 0) {
              uStack_2f8 = (long ******)0x0;
              local_300 = (long *******)0x0;
              local_2f0 = 0;
            }
            else {
              plVar13 = *(long **)(local_eb0 + 0x20);
              if (*(char *)((long)plVar13 + 0x17) < '\0') {
                FUN_00018d20(&local_300,*plVar13,plVar13[1]);
              }
              else {
                uStack_2f8 = (long ******)plVar13[1];
                local_300 = (long *******)*plVar13;
                local_2f0 = plVar13[2];
              }
            }
            thunk_FUN_05a83c6c(uVar10,uVar2,&local_e10,&local_f8,&local_300);
            if (local_2f0 < 0) {
              __ZdlPv(local_300);
            }
            if ((long)local_e8 < 0) {
              __ZdlPv(local_f8);
            }
            if ((long)local_e00 < 0) {
              __ZdlPv(local_e10);
            }
            __ZNSt3__15mutex4lockEv(puVar15 + 0x4f);
            local_e10 = (long *******)local_e64;
            lVar17 = FUN_05cc9138(puVar15 + 0x49,local_e64,&DAT_08b7a8b8,&local_e10,&local_f8);
            *(undefined8 *)(lVar17 + 0x28) = uVar10;
            iVar8 = thunk_FUN_05e1d97c(2);
            if (iVar8 != 0) {
              FUN_05e1d050(&local_e10,2,"mars::account","account_core.cc","MMReq2Buf",0x1c4,0,0);
              local_300 = (long *******)0x0;
              uVar12 = (ulong)(uint)local_e64;
              uVar1 = 8;
              do {
                uVar20 = uVar1;
                uVar16 = (uint)uVar12;
                *(char *)((long)&local_300 + uVar20) =
                     "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                     [uVar16 + (int)(uVar12 / 10) * -10 + 0x23];
                uVar12 = uVar12 / 10;
                uVar1 = uVar20 + 1;
              } while (9 < uVar16);
              *(undefined1 *)((long)&local_300 + uVar20 + 1) = 0;
              local_300 = (long *******)&uStack_2f8;
              if (8 < uVar20) {
                puVar18 = (undefined1 *)((long)&local_300 + uVar20);
                puVar19 = (undefined1 *)((long)&uStack_2f8 + 1);
                do {
                  uVar3 = *puVar18;
                  *puVar18 = puVar19[-1];
                  puVar19[-1] = uVar3;
                  bVar6 = puVar19 < puVar18 + -1;
                  puVar18 = puVar18 + -1;
                  puVar19 = puVar19 + 1;
                } while (bVar6);
              }
              local_350 = (long *******)*in_stack_00000000;
              if (-1 < *(char *)((long)in_stack_00000000 + 0x17)) {
                local_350 = in_stack_00000000;
              }
              local_348._0_1_ = 0;
              local_f0 = (long ******)&local_350;
              puStack_e0 = (undefined8 *)0x0;
              local_e8 = (undefined8 *)0x0;
              puStack_d0 = (undefined8 *)0x0;
              local_d8 = (undefined8 *)0x0;
              puStack_c0 = (undefined8 *)0x0;
              local_c8 = (undefined8 *)0x0;
              puStack_b0 = (undefined8 *)0x0;
              local_b8 = (undefined8 *)0x0;
              uStack_a0 = 0;
              local_a8 = 0;
              uStack_90 = 0;
              local_98 = 0;
              uStack_80 = 0;
              local_88 = 0;
              local_f8 = (long *******)&local_300;
              FUN_05e1d31c(&local_e10,"mmpack taskid:%_, host:%_ add ecdh client",&local_f8);
              thunk_FUN_05e1d0bc(&local_e10);
            }
            __ZNSt3__15mutex6unlockEv(puVar15 + 0x4f);
            local_1e8 = 0xc;
            local_1f0 = (undefined2 *)CONCAT62(local_1f0._2_6_,2);
            local_148 = uVar10;
          }
          uVar3 = local_ec8;
          if (0 < iVar9) goto LAB_05cc6504;
          goto LAB_05cc6d34;
        }
        iVar8 = thunk_FUN_05e1d97c(4);
        if (iVar8 != 0) {
          FUN_05e1d050(&local_d80,4,"mars::account","account_core.cc","MMReq2Buf",0x19b,0,0);
          local_f8 = (long *******)0x0;
          uVar12 = (ulong)(uint)local_e64;
          uVar1 = 8;
          do {
            uVar20 = uVar1;
            uVar16 = (uint)uVar12;
            *(char *)((long)&local_f8 + uVar20) =
                 "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                 [uVar16 + (int)(uVar12 / 10) * -10 + 0x23];
            uVar12 = uVar12 / 10;
            uVar1 = uVar20 + 1;
          } while (9 < uVar16);
          *(undefined1 *)((long)&local_f8 + uVar20 + 1) = 0;
          local_f8 = (long *******)&local_f0;
          if (8 < uVar20) {
            puVar18 = (undefined1 *)((long)&local_f8 + uVar20);
            puVar19 = (undefined1 *)((long)&local_f0 + 1);
            do {
              uVar3 = *puVar18;
              *puVar18 = puVar19[-1];
              puVar19[-1] = uVar3;
              bVar6 = puVar19 < puVar18 + -1;
              puVar18 = puVar18 + -1;
              puVar19 = puVar19 + 1;
            } while (bVar6);
          }
          local_300 = *(long ********)(in_stack_00000010 + 0x18);
          if (-1 < *(char *)(in_stack_00000010 + 0x2f)) {
            local_300 = ppppppplVar14;
          }
          uStack_2f8 = (long ******)((ulong)uStack_2f8 & 0xffffffffffffff00);
          local_350 = (long *******)*in_stack_00000000;
          if (-1 < *(char *)((long)in_stack_00000000 + 0x17)) {
            local_350 = in_stack_00000000;
          }
          local_348._0_1_ = 0;
          lVar17 = local_eb0;
          if (local_eb0 == 0) {
            lVar17 = *(long *)(DAT_0a5250d8 + 0x30);
          }
          local_e10 = (long *******)CONCAT44(local_e10._4_4_,*(undefined4 *)(lVar17 + 0xc));
          local_3a0 = (long *******)0x0;
          FUN_003eccb4(&local_e10,&local_398,10,1);
          lVar17 = local_eb0;
          if (local_eb0 == 0) {
            lVar17 = *(long *)(DAT_0a5250d8 + 0x30);
          }
          local_3a0 = (long *******)&local_398;
          FUN_05e17fdc(local_f58,*(undefined8 *)(lVar17 + 0x10));
          FUN_05cc9218(&local_e60,local_f58);
          local_3f0 = local_e60;
          if (-1 < local_e49) {
            local_3f0 = (long *******)&local_e60;
          }
          local_3e8._0_1_ = 0;
          lVar17 = local_eb0;
          if (local_eb0 == 0) {
            lVar17 = *(long *)(DAT_0a5250d8 + 0x30);
          }
          uVar12 = (ulong)*(char *)(*(long *)(lVar17 + 0x10) + 0x17);
          if ((long)uVar12 < 0) {
            uVar12 = *(ulong *)(*(long *)(lVar17 + 0x10) + 8);
          }
          local_840 = (long *******)0x0;
          uVar1 = 8;
          do {
            uVar20 = uVar1;
            *(char *)((long)&local_840 + uVar20) =
                 "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                 [uVar12 % 10 + 0x23];
            bVar6 = 9 < uVar12;
            uVar12 = uVar12 / 10;
            uVar1 = uVar20 + 1;
          } while (bVar6);
          *(undefined1 *)((long)&local_840 + uVar20 + 1) = 0;
          local_840 = (long *******)&local_838;
          if (8 < uVar20) {
            puVar18 = (undefined1 *)((long)&local_840 + uVar20);
            puVar19 = (undefined1 *)((long)&local_838 + 1);
            do {
              uVar3 = *puVar18;
              *puVar18 = puVar19[-1];
              puVar19[-1] = uVar3;
              bVar6 = puVar19 < puVar18 + -1;
              puVar18 = puVar18 + -1;
              puVar19 = puVar19 + 1;
            } while (bVar6);
          }
          lVar17 = local_eb0;
          if (local_eb0 == 0) {
            lVar17 = *(long *)(DAT_0a5250d8 + 0x30);
          }
          FUN_05e17fdc(local_f88,*(undefined8 *)(lVar17 + 0x18));
          FUN_05cc9218(&local_f70,local_f88);
          local_890 = local_f70;
          if (-1 < (long)uStack_f60) {
            local_890 = (long *******)&local_f70;
          }
          local_888._0_1_ = 0;
          lVar17 = local_eb0;
          if (local_eb0 == 0) {
            lVar17 = *(long *)(DAT_0a5250d8 + 0x30);
          }
          uVar12 = (ulong)*(char *)(*(long *)(lVar17 + 0x18) + 0x17);
          if ((long)uVar12 < 0) {
            uVar12 = *(ulong *)(*(long *)(lVar17 + 0x18) + 8);
          }
          local_8e0 = (long *******)0x0;
          uVar1 = 8;
          do {
            uVar20 = uVar1;
            *(char *)((long)&local_8e0 + uVar20) =
                 "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                 [uVar12 % 10 + 0x23];
            bVar6 = 9 < uVar12;
            uVar12 = uVar12 / 10;
            uVar1 = uVar20 + 1;
          } while (bVar6);
          *(undefined1 *)((long)&local_8e0 + uVar20 + 1) = 0;
          local_8e0 = (long *******)&local_8d8;
          if (8 < uVar20) {
            puVar18 = (undefined1 *)((long)&local_8e0 + uVar20);
            puVar19 = (undefined1 *)((long)&local_8d8 + 1);
            do {
              uVar3 = *puVar18;
              *puVar18 = puVar19[-1];
              puVar19[-1] = uVar3;
              bVar6 = puVar19 < puVar18 + -1;
              puVar18 = puVar18 + -1;
              puVar19 = puVar19 + 1;
            } while (bVar6);
          }
          lVar17 = local_eb0;
          if (local_eb0 == 0) {
            lVar17 = *(long *)(DAT_0a5250d8 + 0x30);
          }
          bVar6 = (*(byte *)(lVar17 + 0x2c) >> 4 & 1) != 0;
          if (bVar6) {
            FUN_05e17fdc(local_fb8,*(undefined8 *)(lVar17 + 0x20));
            FUN_05cc9218(local_fa0,local_fb8);
          }
          else {
            FUN_05941fe8(local_fa0,"empty");
          }
          local_930 = local_fa0[0];
          if (-1 < local_f89) {
            local_930 = (long *******)local_fa0;
          }
          local_928._0_1_ = 0;
          if (local_eb0 == 0) {
            local_eb0 = *(long *)(DAT_0a5250d8 + 0x30);
          }
          if ((*(byte *)(local_eb0 + 0x2c) >> 4 & 1) == 0) {
            uVar12 = 0;
          }
          else {
            uVar12 = (ulong)*(char *)(*(long *)(local_eb0 + 0x20) + 0x17);
            if ((long)uVar12 < 0) {
              uVar12 = *(ulong *)(*(long *)(local_eb0 + 0x20) + 8);
            }
          }
          local_980 = (long *******)0x0;
          uVar1 = 8;
          do {
            uVar20 = uVar1;
            *(char *)((long)&local_980 + uVar20) =
                 "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                 [uVar12 % 10 + 0x23];
            bVar7 = 9 < uVar12;
            uVar12 = uVar12 / 10;
            uVar1 = uVar20 + 1;
          } while (bVar7);
          local_dc8 = &local_980;
          *(undefined1 *)((long)local_dc8 + uVar20 + 1) = 0;
          local_980 = (long *******)&local_978;
          if (8 < uVar20) {
            puVar18 = (undefined1 *)((long)&local_980 + uVar20);
            puVar19 = (undefined1 *)((long)&local_978 + 1);
            do {
              uVar3 = *puVar18;
              *puVar18 = puVar19[-1];
              puVar19[-1] = uVar3;
              bVar7 = puVar19 < puVar18 + -1;
              puVar18 = puVar18 + -1;
              puVar19 = puVar19 + 1;
            } while (bVar7);
          }
          local_e10 = (long *******)&local_f8;
          local_e08 = (long ******)&local_300;
          local_e00 = &local_350;
          local_df8 = &local_3a0;
          local_df0 = &local_3f0;
          local_de8 = &local_840;
          local_de0 = &local_890;
          local_dd8 = &local_8e0;
          local_dd0 = &local_930;
          uStack_db8 = 0;
          local_dc0 = 0;
          uStack_da8 = 0;
          uStack_db0 = 0;
          uStack_d98 = 0;
          local_da0 = 0;
          FUN_05e1d31c(&local_d80,
                       "mmpack taskid:%_, cgi:%_, host:%_ decodeBase64 failed for ecdh_public_key. ecdh info nid:%_, ecdh_key:%_, len:%_, ecdsa_key:%_, len:%_ auth_key:%_, len:%_"
                       ,&local_e10);
          if (local_f89 < '\0') {
            __ZdlPv(local_fa0[0]);
          }
          if ((bVar6) && (local_fa1 < '\0')) {
            __ZdlPv(local_fb8[0]);
          }
          if ((long)uStack_f60 < 0) {
            __ZdlPv(local_f70);
          }
          if (local_f71 < '\0') {
            __ZdlPv(local_f88[0]);
          }
          if (local_e49 < '\0') {
            __ZdlPv(local_e60);
          }
          if (local_f41 < '\0') {
            __ZdlPv(local_f58[0]);
          }
          thunk_FUN_05e1d0bc(&local_d80);
        }
        uStack_e70 = 2;
        uVar10 = FUN_0597d418(*puVar15);
        auVar4 = local_e64;
        local_fe8 = CONCAT44(uStack_e94,local_e98);
        if (local_e80 < 0) {
          FUN_00018d20(&local_fe0,local_e90,uStack_e88);
        }
        else {
          uStack_fd8 = uStack_e88;
          local_fe0 = local_e90;
          local_fd0 = local_e80;
        }
        uStack_fc0 = CONCAT44(uStack_e6c,uStack_e70);
        local_fc8 = local_e78;
        FUN_05cc1d54(uVar10,auVar4,&local_fe8);
        if (local_fd0 < 0) {
          __ZdlPv(local_fe0);
        }
        uVar10 = 0;
      }
      else {
        if (local_eb5 == '\x01') {
          local_e78 = DAT_08b9b130;
          uVar10 = __Znwm(0x60);
          lVar17 = local_ea8;
          if (local_ea8 == 0) {
            lVar17 = *(long *)(DAT_0a5250d8 + 0x38);
          }
          thunk_FUN_05a79a8c(uVar10,*(undefined4 *)(lVar17 + 0x18),*(undefined8 *)(lVar17 + 8),
                             *(undefined8 *)(lVar17 + 0x10));
          __ZNSt3__15mutex4lockEv(puVar15 + 0x4f);
          local_7f0[0] = (uint *)local_e64;
          lVar17 = FUN_05cc9138(puVar15 + 0x4c,local_e64,&DAT_08b7a8b8,local_7f0,&local_d80);
          *(undefined8 *)(lVar17 + 0x28) = uVar10;
          iVar8 = thunk_FUN_05e1d97c(2);
          if (iVar8 != 0) {
            FUN_05e1d050(local_7f0,2,"mars::account","account_core.cc","MMReq2Buf",0x1d7,0,0);
            local_e10 = (long *******)0x0;
            uVar12 = (ulong)(uint)local_e64;
            uVar1 = 8;
            do {
              uVar20 = uVar1;
              uVar16 = (uint)uVar12;
              *(char *)((long)&local_e10 + uVar20) =
                   "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                   [uVar16 + (int)(uVar12 / 10) * -10 + 0x23];
              uVar12 = uVar12 / 10;
              uVar1 = uVar20 + 1;
            } while (9 < uVar16);
            *(undefined1 *)((long)&local_e10 + uVar20 + 1) = 0;
            local_e10 = (long *******)&local_e08;
            if (8 < uVar20) {
              puVar18 = (undefined1 *)((long)&local_e10 + uVar20);
              puVar19 = (undefined1 *)((long)&local_e08 + 1);
              do {
                uVar3 = *puVar18;
                *puVar18 = puVar19[-1];
                puVar19[-1] = uVar3;
                bVar6 = puVar19 < puVar18 + -1;
                puVar18 = puVar18 + -1;
                puVar19 = puVar19 + 1;
              } while (bVar6);
            }
            local_f8 = (long *******)*in_stack_00000000;
            if (-1 < *(char *)((long)in_stack_00000000 + 0x17)) {
              local_f8 = in_stack_00000000;
            }
            local_f0 = (long ******)((ulong)local_f0 & 0xffffffffffffff00);
            local_d78 = (long *******)&local_f8;
            puStack_d68 = (undefined8 *)0x0;
            local_d70 = (undefined8 *)0x0;
            local_d58 = (undefined8 *)0x0;
            puStack_d60 = (undefined8 *)0x0;
            local_d48 = (undefined8 *)0x0;
            puStack_d50 = (undefined8 *)0x0;
            local_d38 = (undefined8 *)0x0;
            puStack_d40 = (undefined8 *)0x0;
            local_d28 = 0;
            puStack_d30 = (undefined8 *)0x0;
            local_d18 = 0;
            uStack_d20 = 0;
            local_d08 = 0;
            uStack_d10 = 0;
            local_d80 = &local_e10;
            FUN_05e1d31c(local_7f0,"mmpack taskid:%_, host:%_ add axecdh client",&local_d80);
            thunk_FUN_05e1d0bc(local_7f0);
          }
          __ZNSt3__15mutex6unlockEv(puVar15 + 0x4f);
          local_1e8 = 0xb;
          local_1f0 = (undefined2 *)CONCAT62(local_1f0._2_6_,2);
          local_140 = uVar10;
          iVar8 = thunk_FUN_05e1d97c(1);
          if (iVar8 != 0) {
            FUN_05e1d050(local_7f0,1,"mars::account","account_core.cc","MMReq2Buf",0x1e5,0,0);
            local_e10 = (long *******)0x0;
            uVar12 = (ulong)(uint)local_e64;
            uVar1 = 8;
            do {
              uVar20 = uVar1;
              uVar16 = (uint)uVar12;
              *(char *)((long)&local_e10 + uVar20) =
                   "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                   [uVar16 + (int)(uVar12 / 10) * -10 + 0x23];
              uVar12 = uVar12 / 10;
              uVar1 = uVar20 + 1;
            } while (9 < uVar16);
            *(undefined1 *)((long)&local_e10 + uVar20 + 1) = 0;
            local_e10 = (long *******)&local_e08;
            if (8 < uVar20) {
              puVar18 = (undefined1 *)((long)&local_e10 + uVar20);
              puVar19 = (undefined1 *)((long)&local_e08 + 1);
              do {
                uVar3 = *puVar18;
                *puVar18 = puVar19[-1];
                puVar19[-1] = uVar3;
                bVar6 = puVar19 < puVar18 + -1;
                puVar18 = puVar18 + -1;
                puVar19 = puVar19 + 1;
              } while (bVar6);
            }
            local_f8 = (long *******)*in_stack_00000000;
            if (-1 < *(char *)((long)in_stack_00000000 + 0x17)) {
              local_f8 = in_stack_00000000;
            }
            local_f0 = (long ******)((ulong)local_f0 & 0xffffffffffffff00);
            lVar17 = local_ea8;
            if (local_ea8 == 0) {
              lVar17 = *(long *)(DAT_0a5250d8 + 0x38);
            }
            local_d80 = (undefined8 *)CONCAT44(local_d80._4_4_,*(undefined4 *)(lVar17 + 0x18));
            local_300 = (long *******)0x0;
            FUN_003eccb4(&local_d80,&uStack_2f8,10,1);
            lVar17 = local_ea8;
            if (local_ea8 == 0) {
              lVar17 = *(long *)(DAT_0a5250d8 + 0x38);
            }
            local_300 = (long *******)&uStack_2f8;
            FUN_05e17fdc(&local_8e0,*(undefined8 *)(lVar17 + 8));
            FUN_05cc9218(&local_890,&local_8e0);
            local_350 = local_890;
            if (-1 < local_879) {
              local_350 = (long *******)&local_890;
            }
            local_348._0_1_ = 0;
            lVar17 = local_ea8;
            if (local_ea8 == 0) {
              lVar17 = *(long *)(DAT_0a5250d8 + 0x38);
            }
            uVar12 = (ulong)*(char *)(*(long *)(lVar17 + 8) + 0x17);
            if ((long)uVar12 < 0) {
              uVar12 = *(ulong *)(*(long *)(lVar17 + 8) + 8);
            }
            local_3a0 = (long *******)0x0;
            uVar1 = 8;
            do {
              uVar20 = uVar1;
              *(char *)((long)&local_3a0 + uVar20) =
                   "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                   [uVar12 % 10 + 0x23];
              bVar6 = 9 < uVar12;
              uVar12 = uVar12 / 10;
              uVar1 = uVar20 + 1;
            } while (bVar6);
            *(undefined1 *)((long)&local_3a0 + uVar20 + 1) = 0;
            local_3a0 = (long *******)&local_398;
            if (8 < uVar20) {
              puVar18 = (undefined1 *)((long)&local_3a0 + uVar20);
              puVar19 = (undefined1 *)((long)&local_398 + 1);
              do {
                uVar3 = *puVar18;
                *puVar18 = puVar19[-1];
                puVar19[-1] = uVar3;
                bVar6 = puVar19 < puVar18 + -1;
                puVar18 = puVar18 + -1;
                puVar19 = puVar19 + 1;
              } while (bVar6);
            }
            lVar17 = local_ea8;
            if (local_ea8 == 0) {
              lVar17 = *(long *)(DAT_0a5250d8 + 0x38);
            }
            FUN_05e17fdc(&local_980,*(undefined8 *)(lVar17 + 0x10));
            FUN_05cc9218(&local_930,&local_980);
            local_3f0 = local_930;
            if (-1 < local_919) {
              local_3f0 = (long *******)&local_930;
            }
            local_3e8._0_1_ = 0;
            if (local_ea8 == 0) {
              local_ea8 = *(long *)(DAT_0a5250d8 + 0x38);
            }
            uVar12 = (ulong)*(char *)(*(long *)(local_ea8 + 0x10) + 0x17);
            if ((long)uVar12 < 0) {
              uVar12 = *(ulong *)(*(long *)(local_ea8 + 0x10) + 8);
            }
            local_840 = (long *******)0x0;
            uVar1 = 8;
            do {
              uVar20 = uVar1;
              *(char *)((long)&local_840 + uVar20) =
                   "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                   [uVar12 % 10 + 0x23];
              bVar6 = 9 < uVar12;
              uVar12 = uVar12 / 10;
              uVar1 = uVar20 + 1;
            } while (bVar6);
            puStack_d50 = &local_840;
            *(undefined1 *)((long)puStack_d50 + uVar20 + 1) = 0;
            local_840 = (long *******)&local_838;
            if (8 < uVar20) {
              puVar18 = (undefined1 *)((long)&local_840 + uVar20);
              puVar19 = (undefined1 *)((long)&local_838 + 1);
              do {
                uVar3 = *puVar18;
                *puVar18 = puVar19[-1];
                puVar19[-1] = uVar3;
                bVar6 = puVar19 < puVar18 + -1;
                puVar18 = puVar18 + -1;
                puVar19 = puVar19 + 1;
              } while (bVar6);
            }
            local_d80 = &local_e10;
            local_d78 = (long *******)&local_f8;
            local_d70 = &local_300;
            puStack_d68 = &local_350;
            puStack_d60 = &local_3a0;
            local_d58 = &local_3f0;
            puStack_d40 = (undefined8 *)0x0;
            local_d48 = (undefined8 *)0x0;
            puStack_d30 = (undefined8 *)0x0;
            local_d38 = (undefined8 *)0x0;
            uStack_d20 = 0;
            local_d28 = 0;
            uStack_d10 = 0;
            local_d18 = 0;
            local_d08 = 0;
            FUN_05e1d31c(local_7f0,
                         "mmpack taskid:%_, host:%_ axecdh info business_type:%_, random_key:%_, len:%_, ticket:%_, len:%_"
                         ,&local_d80);
            if (local_919 < '\0') {
              __ZdlPv(local_930);
            }
            if (local_969 < '\0') {
              __ZdlPv(local_980);
            }
            if (local_879 < '\0') {
              __ZdlPv(local_890);
            }
            if (local_8c9 < '\0') {
              __ZdlPv(local_8e0);
            }
            thunk_FUN_05e1d0bc(local_7f0);
          }
LAB_05cc60d0:
          uVar21 = 0;
          uVar3 = 0;
LAB_05cc6504:
          local_1ab = uVar3;
          local_100 = local_eb8;
          local_ff = (byte)(local_e9c >> 4) & 1;
          local_1c0 = uStack_f20;
          local_1c8 = local_f28;
          if (-1 < (long)local_f18) {
            local_1c0 = local_f18 >> 0x38;
            local_1c8 = &local_f28;
          }
          local_1e4 = (uint)local_1c0;
          local_1ac = local_ec4 & (byte)((int)(local_e9c << 0x1a) >> 0x1f);
          local_1a4 = uVar21;
          FUN_0597d418(*puVar15);
          local_1aa = FUN_05cc2730();
          plVar13 = puVar15 + 0x11;
          if (*(char *)((long)puVar15 + 0x9f) < '\0') {
            if (puVar15[0x12] != 0) {
              plVar13 = (long *)*plVar13;
              goto LAB_05cc6588;
            }
          }
          else if (*(char *)((long)puVar15 + 0x9f) != '\0') {
LAB_05cc6588:
            FUN_05ded508(auStack_190,plVar13);
          }
          __ZNSt3__119__shared_mutex_base11lock_sharedEv(puVar15 + 0x34);
          __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                    (&local_138,puVar15 + 0x2a);
          __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                    (&uStack_120,puVar15 + 0x2d);
          local_108 = puVar15[0x30];
          __ZNSt3__119__shared_mutex_base13unlock_sharedEv(puVar15 + 0x34);
          lVar17 = (long)*(char *)((long)local_ed0 + 0x17);
          if (lVar17 < 0) {
            lVar17 = local_ed0[1];
            if (lVar17 != 0) {
              puVar22 = (undefined8 *)*local_ed0;
              goto LAB_05cc65e4;
            }
          }
          else {
            puVar22 = local_ed0;
            if (*(char *)((long)local_ed0 + 0x17) != '\0') {
LAB_05cc65e4:
              iVar8 = thunk_FUN_05e1d97c(1);
              if (iVar8 != 0) {
                FUN_05e1d050(local_7f0,1,"mars::account","account_core.cc","MMReq2Buf",0x23c,0,0);
                local_e10 = (long *******)0x0;
                uVar12 = (ulong)(uint)local_e64;
                uVar1 = 8;
                do {
                  uVar20 = uVar1;
                  uVar16 = (uint)uVar12;
                  *(char *)((long)&local_e10 + uVar20) =
                       "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                       [uVar16 + (int)(uVar12 / 10) * -10 + 0x23];
                  uVar12 = uVar12 / 10;
                  uVar1 = uVar20 + 1;
                } while (9 < uVar16);
                *(undefined1 *)((long)&local_e10 + uVar20 + 1) = 0;
                if (8 < uVar20) {
                  puVar18 = (undefined1 *)((long)&local_e10 + uVar20);
                  puVar19 = (undefined1 *)((long)&local_e08 + 1);
                  do {
                    uVar3 = *puVar18;
                    *puVar18 = puVar19[-1];
                    puVar19[-1] = uVar3;
                    bVar6 = puVar19 < puVar18 + -1;
                    puVar18 = puVar18 + -1;
                    puVar19 = puVar19 + 1;
                  } while (bVar6);
                }
                local_e10 = (long *******)&local_e08;
                local_f8 = *(long ********)(in_stack_00000010 + 0x18);
                if (-1 < *(char *)(in_stack_00000010 + 0x2f)) {
                  local_f8 = ppppppplVar14;
                }
                local_f0 = (long ******)((ulong)local_f0 & 0xffffffffffffff00);
                local_300 = (long *******)*in_stack_00000000;
                if (-1 < *(char *)((long)in_stack_00000000 + 0x17)) {
                  local_300 = in_stack_00000000;
                }
                uStack_2f8 = (long ******)((ulong)uStack_2f8 & 0xffffffffffffff00);
                uVar12 = (ulong)*(char *)((long)local_ed0 + 0x17);
                if ((long)uVar12 < 0) {
                  uVar12 = local_ed0[1];
                }
                local_350 = (long *******)0x0;
                uVar1 = 8;
                do {
                  uVar20 = uVar1;
                  *(char *)((long)&local_350 + uVar20) =
                       "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                       [uVar12 % 10 + 0x23];
                  bVar6 = 9 < uVar12;
                  uVar12 = uVar12 / 10;
                  uVar1 = uVar20 + 1;
                } while (bVar6);
                puStack_d68 = &local_350;
                *(undefined1 *)((long)puStack_d68 + uVar20 + 1) = 0;
                local_350 = (long *******)&local_348;
                if (8 < uVar20) {
                  puVar18 = (undefined1 *)((long)&local_350 + uVar20);
                  puVar19 = (undefined1 *)((long)&local_348 + 1);
                  do {
                    uVar3 = *puVar18;
                    *puVar18 = puVar19[-1];
                    puVar19[-1] = uVar3;
                    bVar6 = puVar19 < puVar18 + -1;
                    puVar18 = puVar18 + -1;
                    puVar19 = puVar19 + 1;
                  } while (bVar6);
                }
                local_d80 = &local_e10;
                local_d78 = (long *******)&local_f8;
                local_d70 = &local_300;
                local_d58 = (undefined8 *)0x0;
                puStack_d60 = (undefined8 *)0x0;
                local_d48 = (undefined8 *)0x0;
                puStack_d50 = (undefined8 *)0x0;
                local_d38 = (undefined8 *)0x0;
                puStack_d40 = (undefined8 *)0x0;
                local_d28 = 0;
                puStack_d30 = (undefined8 *)0x0;
                local_d18 = 0;
                uStack_d20 = 0;
                local_d08 = 0;
                uStack_d10 = 0;
                FUN_05e1d31c(local_7f0,"mmpack taskid:%_, cgi:%_, host:%_, reqbuf len:%_",&local_d80
                            );
                thunk_FUN_05e1d0bc(local_7f0);
              }
              if (local_eb4 == '\x01') {
                uVar12 = FUN_05cd12a0(puVar15[1],local_e64,in_x4,puVar22,lVar17);
              }
              else {
                uVar12 = FUN_05ccc2f8(puVar15[1],local_e64,in_x4,puVar22,lVar17,&local_1f0,
                                      &local_e98);
              }
              if ((uVar12 & 1) == 0) {
                iVar8 = thunk_FUN_05e1d97c(4);
                if (iVar8 != 0) {
                  FUN_05e1d050(local_7f0,4,"mars::account","account_core.cc","MMReq2Buf",0x251,0,0);
                  local_e10 = (long *******)0x0;
                  uVar12 = (ulong)(uint)local_e64;
                  uVar1 = 8;
                  do {
                    uVar20 = uVar1;
                    uVar16 = (uint)uVar12;
                    *(char *)((long)&local_e10 + uVar20) =
                         "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                         [uVar16 + (int)(uVar12 / 10) * -10 + 0x23];
                    uVar12 = uVar12 / 10;
                    uVar1 = uVar20 + 1;
                  } while (9 < uVar16);
                  *(undefined1 *)((long)&local_e10 + uVar20 + 1) = 0;
                  local_e10 = (long *******)&local_e08;
                  if (8 < uVar20) {
                    puVar18 = (undefined1 *)((long)&local_e10 + uVar20);
                    puVar19 = (undefined1 *)((long)&local_e08 + 1);
                    do {
                      uVar3 = *puVar18;
                      *puVar18 = puVar19[-1];
                      puVar19[-1] = uVar3;
                      bVar6 = puVar19 < puVar18 + -1;
                      puVar18 = puVar18 + -1;
                      puVar19 = puVar19 + 1;
                    } while (bVar6);
                  }
                  local_f8 = *(long ********)(in_stack_00000010 + 0x18);
                  if (-1 < *(char *)(in_stack_00000010 + 0x2f)) {
                    local_f8 = ppppppplVar14;
                  }
                  local_f0 = (long ******)((ulong)local_f0 & 0xffffffffffffff00);
                  local_300 = (long *******)*in_stack_00000000;
                  if (-1 < *(char *)((long)in_stack_00000000 + 0x17)) {
                    local_300 = in_stack_00000000;
                  }
                  uStack_2f8 = (long ******)((ulong)uStack_2f8 & 0xffffffffffffff00);
                  local_d80 = (undefined8 *)CONCAT44(local_d80._4_4_,uStack_e70);
                  local_350 = (long *******)0x0;
                  FUN_003eccb4(&local_d80,&local_348,10,1);
                  local_d78 = (long *******)&local_f8;
                  local_d70 = &local_300;
                  local_d58 = (undefined8 *)0x0;
                  puStack_d60 = (undefined8 *)0x0;
                  local_d48 = (undefined8 *)0x0;
                  puStack_d50 = (undefined8 *)0x0;
                  local_d38 = (undefined8 *)0x0;
                  puStack_d40 = (undefined8 *)0x0;
                  local_d28 = 0;
                  puStack_d30 = (undefined8 *)0x0;
                  local_d18 = 0;
                  uStack_d20 = 0;
                  local_d08 = 0;
                  uStack_d10 = 0;
                  local_d80 = &local_e10;
                  puStack_d68 = &local_350;
                  local_350 = (long *******)&local_348;
                  FUN_05e1d31c(local_7f0,
                               "mmpack taskid:%_, cgi:%_, host:%_, err_code:%_ pack failed.",
                               &local_d80);
                  thunk_FUN_05e1d0bc(local_7f0);
                }
                *in_x6 = 0xfffffffe;
                uStack_e70 = 7;
                uVar10 = FUN_0597d418(*puVar15);
                auVar4 = local_e64;
                local_10c0 = CONCAT44(uStack_e94,local_e98);
                if (local_e80 < 0) {
                  FUN_00018d20(&local_10b8,local_e90,uStack_e88);
                }
                else {
                  uStack_10b0 = uStack_e88;
                  local_10b8 = local_e90;
                  local_10a8 = local_e80;
                }
                uStack_1098 = CONCAT44(uStack_e6c,uStack_e70);
                local_10a0 = local_e78;
                FUN_05cc1d54(uVar10,auVar4,&local_10c0);
                uVar10 = local_10b8;
                lVar17 = local_10a8;
                goto joined_r0x05cc7380;
              }
              iVar8 = thunk_FUN_05e1d97c(2);
              if (iVar8 != 0) {
                FUN_05e1d050(local_7f0,2,"mars::account","account_core.cc","MMReq2Buf",0x265,0,0);
                local_e10 = (long *******)0x0;
                uVar12 = (ulong)(uint)local_e64;
                uVar1 = 8;
                do {
                  uVar20 = uVar1;
                  uVar16 = (uint)uVar12;
                  *(char *)((long)&local_e10 + uVar20) =
                       "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                       [uVar16 + (int)(uVar12 / 10) * -10 + 0x23];
                  uVar12 = uVar12 / 10;
                  uVar1 = uVar20 + 1;
                } while (9 < uVar16);
                *(undefined1 *)((long)&local_e10 + uVar20 + 1) = 0;
                local_e10 = (long *******)&local_e08;
                if (8 < uVar20) {
                  puVar18 = (undefined1 *)((long)&local_e10 + uVar20);
                  puVar19 = (undefined1 *)((long)&local_e08 + 1);
                  do {
                    uVar3 = *puVar18;
                    *puVar18 = puVar19[-1];
                    puVar19[-1] = uVar3;
                    bVar6 = puVar19 < puVar18 + -1;
                    puVar18 = puVar18 + -1;
                    puVar19 = puVar19 + 1;
                  } while (bVar6);
                }
                uVar12 = local_1c0;
                pppppppuVar5 = local_1c8;
                local_f8 = (long *******)"true";
                if (local_eb6 == '\0') {
                  local_f8 = (long *******)"false";
                }
                local_f0 = (long ******)((ulong)local_f0 & 0xffffffffffffff00);
                local_300 = (long *******)"true";
                if (local_eb5 == '\0') {
                  local_300 = (long *******)"false";
                }
                uStack_2f8 = (long ******)((ulong)uStack_2f8 & 0xffffffffffffff00);
                local_350 = local_2a8;
                if (-1 < local_298) {
                  local_350 = (long *******)&local_2a8;
                }
                local_348._0_1_ = 0;
                if (0x7ffffffffffffff7 < local_1c0) {
                    /* WARNING: Subroutine does not return */
                  FUN_00023b4c();
                }
                if (local_1c0 < 0x17) {
                  uStack_f60 = CONCAT17((char)local_1c0,(undefined7)uStack_f60);
                  ppppppplVar14 = (long *******)&local_f70;
                  if (local_1c0 != 0) goto LAB_05cc6d64;
                }
                else {
                  uVar1 = 0x19;
                  if ((local_1c0 | 7) != 0x17) {
                    uVar1 = (local_1c0 | 7) + 1;
                  }
                  ppppppplVar14 = (long *******)__Znwm(uVar1);
                  uStack_f60 = uVar1 | 0x8000000000000000;
                  local_f68 = uVar12;
                  local_f70 = ppppppplVar14;
LAB_05cc6d64:
                  _memmove(ppppppplVar14,pppppppuVar5,uVar12);
                }
                *(undefined1 *)((long)ppppppplVar14 + uVar12) = 0;
                FUN_05e17fdc(local_f58,&local_f70);
                FUN_05cc9218(&local_e60,local_f58);
                local_3a0 = local_e60;
                if (-1 < local_e49) {
                  local_3a0 = (long *******)&local_e60;
                }
                local_398._0_1_ = 0;
                local_3f0 = (long *******)0x0;
                uVar12 = (ulong)local_1e4;
                uVar1 = 8;
                do {
                  uVar20 = uVar1;
                  uVar16 = (uint)uVar12;
                  *(char *)((long)&local_3f0 + uVar20) =
                       "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                       [uVar16 + (int)(uVar12 / 10) * -10 + 0x23];
                  uVar12 = uVar12 / 10;
                  uVar1 = uVar20 + 1;
                } while (9 < uVar16);
                *(undefined1 *)((long)&local_3f0 + uVar20 + 1) = 0;
                local_3f0 = (long *******)&local_3e8;
                if (8 < uVar20) {
                  puVar18 = (undefined1 *)((long)&local_3f0 + uVar20);
                  puVar19 = (undefined1 *)((long)&local_3e8 + 1);
                  do {
                    uVar3 = *puVar18;
                    *puVar18 = puVar19[-1];
                    puVar19[-1] = uVar3;
                    bVar6 = puVar19 < puVar18 + -1;
                    puVar18 = puVar18 + -1;
                    puVar19 = puVar19 + 1;
                  } while (bVar6);
                }
                FUN_05e17fdc(local_fa0,&local_168);
                FUN_05cc9218(local_f88,local_fa0);
                local_840 = local_f88[0];
                if (-1 < local_f71) {
                  local_840 = (long *******)local_f88;
                }
                uVar12 = local_160;
                if (-1 < (long)local_158) {
                  uVar12 = local_158 >> 0x38;
                }
                local_838._0_1_ = 0;
                local_890 = (long *******)0x0;
                uVar1 = 8;
                do {
                  uVar20 = uVar1;
                  *(char *)((long)&local_890 + uVar20) =
                       "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                       [uVar12 % 10 + 0x23];
                  bVar6 = 9 < uVar12;
                  uVar12 = uVar12 / 10;
                  uVar1 = uVar20 + 1;
                } while (bVar6);
                *(undefined1 *)((long)&local_890 + uVar20 + 1) = 0;
                local_890 = (long *******)&local_888;
                if (8 < uVar20) {
                  puVar18 = (undefined1 *)((long)&local_890 + uVar20);
                  puVar19 = (undefined1 *)((long)&local_888 + 1);
                  do {
                    uVar3 = *puVar18;
                    *puVar18 = puVar19[-1];
                    puVar19[-1] = uVar3;
                    bVar6 = puVar19 < puVar18 + -1;
                    puVar18 = puVar18 + -1;
                    puVar19 = puVar19 + 1;
                  } while (bVar6);
                }
                FUN_05e17fdc(local_10d8,&local_138);
                FUN_05cc9218(local_fb8,local_10d8);
                local_8e0 = local_fb8[0];
                if (-1 < local_fa1) {
                  local_8e0 = (long *******)local_fb8;
                }
                local_8d8._0_1_ = 0;
                FUN_05e17fdc(local_1108,&uStack_120);
                FUN_05cc9218(local_10f0,local_1108);
                local_930 = local_10f0[0];
                if (-1 < local_10d9) {
                  local_930 = (long *******)local_10f0;
                }
                local_928._0_1_ = 0;
                local_980 = (long *******)0x0;
                uVar12 = local_108;
                uVar1 = 8;
                do {
                  uVar20 = uVar1;
                  *(char *)((long)&local_980 + uVar20) =
                       "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                       [uVar12 % 10 + 0x23];
                  bVar6 = 9 < uVar12;
                  uVar12 = uVar12 / 10;
                  uVar1 = uVar20 + 1;
                } while (bVar6);
                puStack_d30 = &local_980;
                *(undefined1 *)((long)puStack_d30 + uVar20 + 1) = 0;
                local_980 = (long *******)&local_978;
                if (8 < uVar20) {
                  puVar18 = (undefined1 *)((long)&local_980 + uVar20);
                  puVar19 = (undefined1 *)((long)&local_978 + 1);
                  do {
                    uVar3 = *puVar18;
                    *puVar18 = puVar19[-1];
                    puVar19[-1] = uVar3;
                    bVar6 = puVar19 < puVar18 + -1;
                    puVar18 = puVar18 + -1;
                    puVar19 = puVar19 + 1;
                  } while (bVar6);
                }
                local_d80 = &local_e10;
                local_d78 = (long *******)&local_f8;
                local_d70 = &local_300;
                puStack_d68 = &local_350;
                puStack_d60 = &local_3a0;
                local_d58 = &local_3f0;
                puStack_d50 = &local_840;
                local_d48 = &local_890;
                puStack_d40 = &local_8e0;
                local_d38 = &local_930;
                uStack_d20 = 0;
                local_d28 = 0;
                uStack_d10 = 0;
                local_d18 = 0;
                local_d08 = 0;
                FUN_05e1d31c(local_7f0,
                             "mmpack taskid:%_, use_ecdh:%_, use_axecdh:%_, identify:%_, server_id:%_, len:%_, session_key:%_, len:%_, connection_id:%_, request_id:%_, router_fake_id:%_"
                             ,&local_d80);
                if (local_10d9 < '\0') {
                  __ZdlPv(local_10f0[0]);
                }
                if (local_10f1 < '\0') {
                  __ZdlPv(local_1108[0]);
                }
                if (local_fa1 < '\0') {
                  __ZdlPv(local_fb8[0]);
                }
                if (local_10c1 < '\0') {
                  __ZdlPv(local_10d8[0]);
                }
                if (local_f71 < '\0') {
                  __ZdlPv(local_f88[0]);
                }
                if (local_f89 < '\0') {
                  __ZdlPv(local_fa0[0]);
                }
                if (local_e49 < '\0') {
                  __ZdlPv(local_e60);
                }
                if (local_f41 < '\0') {
                  __ZdlPv(local_f58[0]);
                }
                if ((long)uStack_f60 < 0) {
                  __ZdlPv(local_f70);
                }
                thunk_FUN_05e1d0bc(local_7f0);
              }
              uVar10 = 1;
              goto LAB_05cc7110;
            }
          }
          iVar8 = thunk_FUN_05e1d97c(4);
          if (iVar8 != 0) {
            FUN_05e1d050(local_7f0,4,"mars::account","account_core.cc","MMReq2Buf",0x23e,0,0);
            local_e10 = (long *******)0x0;
            uVar12 = (ulong)(uint)local_e64;
            uVar1 = 8;
            do {
              uVar20 = uVar1;
              uVar16 = (uint)uVar12;
              *(char *)((long)&local_e10 + uVar20) =
                   "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                   [uVar16 + (int)(uVar12 / 10) * -10 + 0x23];
              uVar12 = uVar12 / 10;
              uVar1 = uVar20 + 1;
            } while (9 < uVar16);
            *(undefined1 *)((long)&local_e10 + uVar20 + 1) = 0;
            local_e10 = (long *******)&local_e08;
            if (8 < uVar20) {
              puVar18 = (undefined1 *)((long)&local_e10 + uVar20);
              puVar19 = (undefined1 *)((long)&local_e08 + 1);
              do {
                uVar3 = *puVar18;
                *puVar18 = puVar19[-1];
                puVar19[-1] = uVar3;
                bVar6 = puVar19 < puVar18 + -1;
                puVar18 = puVar18 + -1;
                puVar19 = puVar19 + 1;
              } while (bVar6);
            }
            local_f8 = *(long ********)(in_stack_00000010 + 0x18);
            if (-1 < *(char *)(in_stack_00000010 + 0x2f)) {
              local_f8 = ppppppplVar14;
            }
            local_f0 = (long ******)((ulong)local_f0 & 0xffffffffffffff00);
            local_300 = (long *******)*in_stack_00000000;
            if (-1 < *(char *)((long)in_stack_00000000 + 0x17)) {
              local_300 = in_stack_00000000;
            }
            uStack_2f8 = (long ******)((ulong)uStack_2f8 & 0xffffffffffffff00);
            local_d78 = (long *******)&local_f8;
            local_d70 = &local_300;
            puStack_d60 = (undefined8 *)0x0;
            puStack_d68 = (undefined8 *)0x0;
            puStack_d50 = (undefined8 *)0x0;
            local_d58 = (undefined8 *)0x0;
            puStack_d40 = (undefined8 *)0x0;
            local_d48 = (undefined8 *)0x0;
            puStack_d30 = (undefined8 *)0x0;
            local_d38 = (undefined8 *)0x0;
            uStack_d20 = 0;
            local_d28 = 0;
            uStack_d10 = 0;
            local_d18 = 0;
            local_d08 = 0;
            local_d80 = &local_e10;
            FUN_05e1d31c(local_7f0,"mmpack taskid:%_, cgi:%_, host:%_ request buffer is empty",
                         &local_d80);
            thunk_FUN_05e1d0bc(local_7f0);
          }
          *in_x6 = 0xffffffff;
          uStack_e70 = 4;
          uVar10 = FUN_0597d418(*puVar15);
          auVar4 = local_e64;
          local_1090 = CONCAT44(uStack_e94,local_e98);
          if (local_e80 < 0) {
            FUN_00018d20(&local_1088,local_e90,uStack_e88);
          }
          else {
            uStack_1080 = uStack_e88;
            local_1088 = local_e90;
            local_1078 = local_e80;
          }
          uStack_1068 = CONCAT44(uStack_e6c,uStack_e70);
          local_1070 = local_e78;
          FUN_05cc1d54(uVar10,auVar4,&local_1090);
          uVar10 = local_1088;
          lVar17 = local_1078;
        }
        else {
          if (*(long *)(in_stack_00000010 + 0x60) == 1000) {
            local_e78 = CONCAT44(local_e78._4_4_,5);
            __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
                      (&local_2a8,"CreateQRCodeOffline");
            local_290 = 5;
            __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                      (&local_258,&local_f28);
            __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                      (&local_288,local_ec0);
            __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                      (&uStack_270,local_ec0);
LAB_05cc5e14:
            __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                      (&local_f28,&local_258);
            __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                      (&local_168,&local_288);
            local_1e8 = (undefined2)local_290;
            local_198 = 1;
            if (((byte)local_e9c >> 6 & 1) != 0) {
              if (*(char *)((long)local_ec0 + 0x17) < '\0') {
                if (local_ec0[1] != 0) {
                  local_ec0 = (undefined8 *)*local_ec0;
                  goto LAB_05cc60c8;
                }
              }
              else if (*(char *)((long)local_ec0 + 0x17) != '\0') {
LAB_05cc60c8:
                FUN_05ded508(auStack_190,local_ec0);
              }
            }
            goto LAB_05cc60d0;
          }
          if (*(long *)(in_stack_00000010 + 0x60) == 0x307) {
            local_e78 = DAT_084874b8;
            local_1f0 = (undefined2 *)CONCAT62(local_1f0._2_6_,2);
            __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
                      (&local_2a8,"GetDisasterInfo");
            local_290 = 0;
            __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                      (&local_258,&local_f28);
            __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
                      (&local_288,"");
            __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
                      (&uStack_270,"");
            goto LAB_05cc5e14;
          }
          local_e78 = CONCAT44(local_e78._4_4_,local_290);
          FUN_05cc3e8c(local_7f0,puVar15,local_e64,in_stack_00000000);
          FUN_05cc7394(&local_2a8,local_7f0);
          FUN_05cc8bfc(local_7f0);
          uVar12 = uStack_280;
          if (-1 < (long)local_278) {
            uVar12 = local_278 >> 0x38;
          }
          if (uVar12 != 0) {
            if (local_290 == 0xd) {
              local_1f0 = (undefined2 *)CONCAT62(local_1f0._2_6_,2);
            }
            goto LAB_05cc5e14;
          }
          iVar8 = thunk_FUN_05e1d97c(4);
          if (iVar8 != 0) {
            FUN_05e1d050(local_7f0,4,"mars::account","account_core.cc","MMReq2Buf",0x201,0,0);
            local_e10 = (long *******)0x0;
            uVar12 = (ulong)(uint)local_e64;
            uVar1 = 8;
            do {
              uVar20 = uVar1;
              uVar16 = (uint)uVar12;
              *(char *)((long)&local_e10 + uVar20) =
                   "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                   [uVar16 + (int)(uVar12 / 10) * -10 + 0x23];
              uVar12 = uVar12 / 10;
              uVar1 = uVar20 + 1;
            } while (9 < uVar16);
            *(undefined1 *)((long)&local_e10 + uVar20 + 1) = 0;
            local_e10 = (long *******)&local_e08;
            if (8 < uVar20) {
              puVar18 = (undefined1 *)((long)&local_e10 + uVar20);
              puVar19 = (undefined1 *)((long)&local_e08 + 1);
              do {
                uVar3 = *puVar18;
                *puVar18 = puVar19[-1];
                puVar19[-1] = uVar3;
                bVar6 = puVar19 < puVar18 + -1;
                puVar18 = puVar18 + -1;
                puVar19 = puVar19 + 1;
              } while (bVar6);
            }
            local_f8 = *(long ********)(in_stack_00000010 + 0x18);
            if (-1 < *(char *)(in_stack_00000010 + 0x2f)) {
              local_f8 = ppppppplVar14;
            }
            local_f0 = (long ******)((ulong)local_f0 & 0xffffffffffffff00);
            local_300 = (long *******)*in_stack_00000000;
            if (-1 < *(char *)((long)in_stack_00000000 + 0x17)) {
              local_300 = in_stack_00000000;
            }
            uStack_2f8 = (long ******)((ulong)uStack_2f8 & 0xffffffffffffff00);
            local_d78 = (long *******)&local_f8;
            local_d70 = &local_300;
            puStack_d60 = (undefined8 *)0x0;
            puStack_d68 = (undefined8 *)0x0;
            puStack_d50 = (undefined8 *)0x0;
            local_d58 = (undefined8 *)0x0;
            puStack_d40 = (undefined8 *)0x0;
            local_d48 = (undefined8 *)0x0;
            puStack_d30 = (undefined8 *)0x0;
            local_d38 = (undefined8 *)0x0;
            uStack_d20 = 0;
            local_d28 = 0;
            uStack_d10 = 0;
            local_d18 = 0;
            local_d08 = 0;
            local_d80 = &local_e10;
            FUN_05e1d31c(local_7f0,"mmpack taskid:%_, cgi:%_, host:%_ client session key is empty",
                         &local_d80);
            thunk_FUN_05e1d0bc(local_7f0);
          }
          uStack_e70 = 9;
          uVar10 = FUN_0597d418(*puVar15);
          auVar4 = local_e64;
          local_1060 = CONCAT44(uStack_e94,local_e98);
          if (local_e80 < 0) {
            FUN_00018d20(&local_1058,local_e90,uStack_e88);
          }
          else {
            uStack_1050 = uStack_e88;
            local_1058 = local_e90;
            local_1048 = local_e80;
          }
          uStack_1038 = CONCAT44(uStack_e6c,uStack_e70);
          local_1040 = local_e78;
          FUN_05cc1d54(uVar10,auVar4,&local_1060);
          uVar10 = local_1058;
          lVar17 = local_1048;
        }
joined_r0x05cc7380:
        if (lVar17 < 0) {
          __ZdlPv(uVar10);
        }
LAB_05cc6d34:
        uVar10 = 0;
      }
LAB_05cc7110:
      FUN_05cc8bfc(&local_2a8);
      if ((long)local_f18 < 0) {
        __ZdlPv(local_f28);
      }
      if (lStack_110 < 0) {
        __ZdlPv(uStack_120);
      }
      if (local_128 < 0) {
        __ZdlPv(local_138);
      }
      if ((long)local_158 < 0) {
        __ZdlPv(local_168);
      }
      FUN_05ded188(auStack_190);
      goto LAB_05cc7160;
    }
    if (*(char *)((long)local_ed0 + 0x17) < '\0') {
      if (local_ed0[1] != 0) {
        puVar15 = (undefined8 *)*local_ed0;
        goto LAB_05cc5098;
      }
    }
    else {
      puVar15 = local_ed0;
      if (*(char *)((long)local_ed0 + 0x17) != '\0') {
LAB_05cc5098:
        FUN_05ded508(in_x4,puVar15);
        iVar8 = thunk_FUN_05e1d97c(2);
        if (iVar8 != 0) {
          FUN_05e1d050(local_7f0,2,"mars::account","account_core.cc","MMReq2Buf",0x15b,0,0);
          local_1f0 = (undefined2 *)0x0;
          uVar12 = (ulong)(uint)local_e64;
          uVar1 = 8;
          do {
            uVar20 = uVar1;
            uVar16 = (uint)uVar12;
            *(char *)((long)&local_1f0 + uVar20) =
                 "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                 [uVar16 + (int)(uVar12 / 10) * -10 + 0x23];
            uVar12 = uVar12 / 10;
            uVar1 = uVar20 + 1;
          } while (9 < uVar16);
          *(undefined1 *)((long)&local_1f0 + uVar20 + 1) = 0;
          if (8 < uVar20) {
            puVar18 = (undefined1 *)((long)&local_1f0 + uVar20);
            puVar19 = (undefined1 *)((long)&local_1e8 + 1);
            do {
              uVar3 = *puVar18;
              *puVar18 = puVar19[-1];
              puVar19[-1] = uVar3;
              bVar6 = puVar19 < puVar18 + -1;
              puVar18 = puVar18 + -1;
              puVar19 = puVar19 + 1;
            } while (bVar6);
          }
          local_1f0 = &local_1e8;
          local_2a8 = *(long ********)(in_stack_00000010 + 0x18);
          if (-1 < *(char *)(in_stack_00000010 + 0x2f)) {
            local_2a8 = ppppppplVar14;
          }
          local_2a0 = local_2a0 & 0xffffffffffffff00;
          local_e10 = (long *******)*in_stack_00000000;
          if (-1 < *(char *)((long)in_stack_00000000 + 0x17)) {
            local_e10 = in_stack_00000000;
          }
          local_e08 = (long ******)((ulong)local_e08 & 0xffffffffffffff00);
          uVar12 = (ulong)*(char *)((long)local_ed0 + 0x17);
          if ((long)uVar12 < 0) {
            uVar12 = local_ed0[1];
          }
          local_f8 = (long *******)0x0;
          uVar1 = 8;
          do {
            uVar20 = uVar1;
            *(char *)((long)&local_f8 + uVar20) =
                 "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                 [uVar12 % 10 + 0x23];
            bVar6 = 9 < uVar12;
            uVar12 = uVar12 / 10;
            uVar1 = uVar20 + 1;
          } while (bVar6);
          puStack_d68 = &local_f8;
          *(undefined1 *)((long)puStack_d68 + uVar20 + 1) = 0;
          local_f8 = (long *******)&local_f0;
          if (8 < uVar20) {
            puVar18 = (undefined1 *)((long)&local_f8 + uVar20);
            puVar19 = (undefined1 *)((long)&local_f0 + 1);
            do {
              uVar3 = *puVar18;
              *puVar18 = puVar19[-1];
              puVar19[-1] = uVar3;
              bVar6 = puVar19 < puVar18 + -1;
              puVar18 = puVar18 + -1;
              puVar19 = puVar19 + 1;
            } while (bVar6);
          }
          local_d80 = &local_1f0;
          local_d78 = (long *******)&local_2a8;
          local_d70 = &local_e10;
          local_d58 = (undefined8 *)0x0;
          puStack_d60 = (undefined8 *)0x0;
          local_d48 = (undefined8 *)0x0;
          puStack_d50 = (undefined8 *)0x0;
          local_d38 = (undefined8 *)0x0;
          puStack_d40 = (undefined8 *)0x0;
          local_d28 = 0;
          puStack_d30 = (undefined8 *)0x0;
          local_d18 = 0;
          uStack_d20 = 0;
          local_d08 = 0;
          uStack_d10 = 0;
          FUN_05e1d31c(local_7f0,
                       "mmpack taskid:%_, cgi:%_, host:%_ send_only skip mmpkg, reqbuf len:%_",
                       &local_d80);
          thunk_FUN_05e1d0bc(local_7f0);
        }
        uVar10 = 1;
        goto LAB_05cc7160;
      }
    }
    iVar8 = thunk_FUN_05e1d97c(4);
    if (iVar8 != 0) {
      FUN_05e1d050(local_7f0,4,"mars::account","account_core.cc","MMReq2Buf",0x153,0,0);
      local_1f0 = (undefined2 *)0x0;
      uVar12 = (ulong)(uint)local_e64;
      uVar1 = 8;
      do {
        uVar20 = uVar1;
        uVar16 = (uint)uVar12;
        *(char *)((long)&local_1f0 + uVar20) =
             "ZYXWVUTSRQPONMLKJIHGFEDCBA9876543210123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
             [uVar16 + (int)(uVar12 / 10) * -10 + 0x23];
        uVar12 = uVar12 / 10;
        uVar1 = uVar20 + 1;
      } while (9 < uVar16);
      local_d80 = &local_1f0;
      *(undefined1 *)((long)local_d80 + uVar20 + 1) = 0;
      local_1f0 = &local_1e8;
      if (8 < uVar20) {
        puVar18 = (undefined1 *)((long)&local_1f0 + uVar20);
        puVar19 = (undefined1 *)((long)&local_1e8 + 1);
        do {
          uVar3 = *puVar18;
          *puVar18 = puVar19[-1];
          puVar19[-1] = uVar3;
          bVar6 = puVar19 < puVar18 + -1;
          puVar18 = puVar18 + -1;
          puVar19 = puVar19 + 1;
        } while (bVar6);
      }
      local_2a8 = *(long ********)(in_stack_00000010 + 0x18);
      if (-1 < *(char *)(in_stack_00000010 + 0x2f)) {
        local_2a8 = ppppppplVar14;
      }
      local_2a0 = local_2a0 & 0xffffffffffffff00;
      local_e10 = (long *******)*in_stack_00000000;
      if (-1 < *(char *)((long)in_stack_00000000 + 0x17)) {
        local_e10 = in_stack_00000000;
      }
      local_e08 = (long ******)((ulong)local_e08 & 0xffffffffffffff00);
      local_d78 = (long *******)&local_2a8;
      local_d70 = &local_e10;
      puStack_d60 = (undefined8 *)0x0;
      puStack_d68 = (undefined8 *)0x0;
      puStack_d50 = (undefined8 *)0x0;
      local_d58 = (undefined8 *)0x0;
      puStack_d40 = (undefined8 *)0x0;
      local_d48 = (undefined8 *)0x0;
      puStack_d30 = (undefined8 *)0x0;
      local_d38 = (undefined8 *)0x0;
      uStack_d20 = 0;
      local_d28 = 0;
      uStack_d10 = 0;
      local_d18 = 0;
      local_d08 = 0;
      FUN_05e1d31c(local_7f0,"mmpack taskid:%_, cgi:%_, host:%_ reqbuf is empty for send_only.",
                   &local_d80);
      thunk_FUN_05e1d0bc(local_7f0);
    }
  }
  uVar10 = 0;
LAB_05cc7160:
  FUN_05ce54cc(auStack_ee0);
  if (local_e80 < 0) {
    __ZdlPv(local_e90);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_78) {
    return uVar10;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


