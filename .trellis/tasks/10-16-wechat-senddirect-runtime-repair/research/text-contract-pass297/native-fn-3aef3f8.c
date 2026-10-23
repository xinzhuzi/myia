// Ghidra inferred pseudocode; requested=0x3aef3f8
// entry=03aef3f8 end=03af0ae7

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_03aef3f8(long *param_1,long param_2,long param_3)

{
  undefined1 uVar1;
  uint3 uVar2;
  long *******ppppppplVar3;
  undefined8 uVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  undefined4 *puVar8;
  code *pcVar9;
  bool bVar10;
  undefined4 uVar11;
  undefined4 uVar12;
  int iVar13;
  ulong uVar14;
  undefined ********ppppppppuVar15;
  long ******pppppplVar16;
  undefined8 uVar17;
  char *pcVar18;
  size_t sVar19;
  undefined8 *******pppppppuVar20;
  undefined1 *puVar21;
  long lVar22;
  uint uVar23;
  undefined *******pppppppuVar24;
  undefined ******ppppppuVar25;
  undefined8 ******ppppppuVar26;
  undefined1 *puVar27;
  long lVar28;
  long *****ppppplVar29;
  long *plVar30;
  undefined *******pppppppuVar31;
  undefined ******ppppppuVar32;
  undefined *****pppppuVar33;
  undefined8 ******ppppppuVar34;
  ulong uVar35;
  undefined4 *puVar36;
  undefined ********ppppppppuVar37;
  long *plVar38;
  long *******ppppppplVar39;
  long lVar40;
  undefined8 *******pppppppuVar41;
  long *plVar42;
  undefined4 uVar43;
  undefined4 uVar44;
  undefined4 uVar45;
  undefined4 uVar46;
  undefined4 uVar47;
  undefined4 uVar48;
  undefined4 uVar49;
  undefined4 uVar50;
  undefined4 uVar51;
  undefined4 uVar52;
  undefined **local_7d8;
  undefined8 *******local_7d0;
  undefined8 *******local_7c8;
  long local_7c0;
  undefined1 auStack_7b8 [24];
  undefined **local_7a0;
  long local_798;
  long *plStack_790;
  long local_788;
  undefined8 *******local_780;
  undefined1 *puStack_778;
  undefined1 *local_770;
  undefined1 *local_768;
  undefined1 *local_760;
  long *plStack_758;
  long *local_750;
  undefined1 *puStack_748;
  undefined **local_738;
  long *******local_730;
  long *******local_728;
  long local_720;
  undefined4 *local_718;
  undefined4 *local_710;
  long local_708;
  undefined ********local_700;
  undefined8 local_6f8;
  undefined7 local_6f0;
  char cStack_6e9;
  long local_6e8;
  undefined ********local_5a0;
  undefined8 local_598;
  undefined *******local_590;
  long local_588;
  undefined1 auStack_4e8 [56];
  undefined ********local_4b0;
  undefined ********ppppppppuStack_4a8;
  undefined ********local_4a0;
  long lStack_498;
  undefined8 uStack_490;
  undefined8 uStack_488;
  undefined8 uStack_480;
  undefined8 uStack_478;
  undefined8 uStack_470;
  undefined8 uStack_468;
  undefined8 local_460;
  undefined8 uStack_458;
  undefined8 local_450;
  undefined8 uStack_448;
  undefined8 local_440;
  undefined8 uStack_438;
  undefined **local_400;
  undefined **local_3f8;
  undefined **local_3f0;
  undefined **local_3e8;
  undefined **local_3e0;
  undefined **local_3d8;
  undefined **local_3d0;
  undefined **local_3c8;
  undefined8 *******local_350;
  size_t sStack_348;
  undefined8 local_340;
  undefined8 uStack_338;
  undefined8 local_330;
  undefined8 uStack_328;
  undefined8 local_320;
  undefined8 uStack_318;
  undefined8 local_310;
  undefined8 uStack_308;
  undefined8 local_300;
  undefined8 uStack_2f8;
  undefined8 local_2f0;
  undefined8 uStack_2e8;
  undefined8 local_2e0;
  undefined8 uStack_2d8;
  undefined1 auStack_290 [160];
  undefined1 *local_1f0;
  undefined1 *puStack_1e8;
  undefined1 *local_1e0;
  undefined1 *puStack_1d8;
  undefined1 *local_1d0;
  undefined1 *puStack_1c8;
  undefined1 *local_1c0;
  undefined1 *puStack_1b8;
  undefined1 *local_1b0;
  undefined1 *puStack_1a8;
  undefined1 *local_1a0;
  undefined1 *puStack_198;
  undefined1 *local_190;
  undefined1 *puStack_188;
  undefined1 *local_180;
  undefined1 *puStack_178;
  undefined1 *local_170;
  undefined1 *puStack_168;
  undefined1 *local_160;
  undefined1 *puStack_158;
  undefined1 *local_150;
  undefined1 *puStack_148;
  undefined1 *local_140;
  undefined1 *puStack_138;
  undefined1 *local_130;
  undefined1 *puStack_128;
  undefined1 *local_120;
  undefined1 *puStack_118;
  undefined1 *local_110;
  undefined1 *puStack_108;
  undefined1 *local_100;
  undefined1 *puStack_f8;
  undefined1 *local_f0;
  undefined1 *puStack_e8;
  undefined1 *local_e0;
  undefined1 *puStack_d8;
  undefined1 *local_d0;
  undefined1 *puStack_c8;
  undefined1 *local_c0;
  undefined1 *puStack_b8;
  undefined1 *local_b0;
  undefined1 *puStack_a8;
  undefined1 *local_a0;
  undefined1 *puStack_98;
  long local_88;
  
  local_88 = *(long *)PTR____stack_chk_guard_09b36c98;
  if (*(long *)(param_2 + 0x18) != 0) {
    uVar14 = (**(code **)(*param_1 + 0x10))();
    if ((uVar14 & 1) == 0) {
      uVar17 = thunk_FUN_05e1d97c(4);
      if ((int)uVar17 != 0) {
        FUN_0488143c(&local_4b0);
        ppppppppuVar15 = local_4b0;
        if (-1 < (long)local_4a0) {
          ppppppppuVar15 = (undefined ********)&local_4b0;
        }
        if ((DAT_0a41be80 & 1) == 0) {
          uRam000000000a41be78._0_1_ = s_base_storage_cc_08964550[8];
          uRam000000000a41be78._1_1_ = s_base_storage_cc_08964550[9];
          uRam000000000a41be78._2_1_ = s_base_storage_cc_08964550[10];
          uRam000000000a41be78._3_1_ = s_base_storage_cc_08964550[0xb];
          uRam000000000a41be78._4_1_ = s_base_storage_cc_08964550[0xc];
          uRam000000000a41be78._5_1_ = s_base_storage_cc_08964550[0xd];
          uRam000000000a41be78._6_1_ = s_base_storage_cc_08964550[0xe];
          uRam000000000a41be78._7_1_ = s_base_storage_cc_08964550[0xf];
          DAT_0a41be70 = s_base_storage_cc_08964550[0];
          DAT_0a41be70_1._0_1_ = s_base_storage_cc_08964550[1];
          DAT_0a41be70_1._1_1_ = s_base_storage_cc_08964550[2];
          DAT_0a41be70_1._2_1_ = s_base_storage_cc_08964550[3];
          DAT_0a41be70_1._3_1_ = s_base_storage_cc_08964550[4];
          DAT_0a41be70_1._4_1_ = s_base_storage_cc_08964550[5];
          DAT_0a41be70_1._5_1_ = s_base_storage_cc_08964550[6];
          DAT_0a41be70_1._6_1_ = s_base_storage_cc_08964550[7];
          DAT_0a41be80 = 1;
        }
        if ((DAT_0a41c249 & 1) == 0) {
          uVar14 = 0;
          do {
            (&DAT_0a41c233)[uVar14] = (&DAT_08964ff2)[uVar14 & 0xf] ^ (&DAT_08965002)[uVar14];
            uVar14 = uVar14 + 1;
          } while (uVar14 != 0x16);
          DAT_0a41c249 = 1;
        }
        FUN_05e1d050(&local_1f0,4,ppppppppuVar15,&DAT_0a41be70,&DAT_0a41c233,0x1b7,0,0);
        if ((DAT_0a41c1bd & 1) == 0) {
          _DAT_0a41c198 = CONCAT44((int)DAT_08839950,(int)ram0x08489fc8);
          uRam000000000a41c1a0 = CONCAT44((int)DAT_088546b0,(int)DAT_084abe58);
          _DAT_0a41c1a8 = CONCAT44((int)DAT_08567f28,(int)DAT_08554238);
          uRam000000000a41c1b0 = CONCAT44((int)DAT_08545158,(int)DAT_084d4a68);
          DAT_0a41c1b8 = (undefined4)ram0x08480938;
          DAT_0a41c1bc = 0;
          DAT_0a41c1bd = 1;
        }
        uStack_2d8 = 0;
        local_2e0 = 0;
        uStack_2e8 = 0;
        local_2f0 = 0;
        uStack_2f8 = 0;
        local_300 = 0;
        uStack_308 = 0;
        local_310 = 0;
        uStack_318 = 0;
        local_320 = 0;
        uStack_328 = 0;
        local_330 = 0;
        uStack_338 = 0;
        local_340 = 0;
        sStack_348 = 0;
        local_350 = (undefined8 *******)0x0;
        FUN_05e1d31c(&local_1f0,&DAT_0a41c198,&local_350);
        thunk_FUN_05e1d0bc(&local_1f0);
        if ((long)local_4a0 < 0) {
          __ZdlPvm(local_4b0,(ulong)local_4a0 & 0x7fffffffffffffff);
        }
        uVar17 = 0;
      }
      goto LAB_03af0a84;
    }
    plVar38 = *(long **)(param_2 + 0x10);
    local_710 = (undefined4 *)0x0;
    local_708 = 0;
    local_718 = (undefined4 *)0x0;
    if (plVar38 != (long *)0x0) {
      lVar40 = 0;
      uVar14 = 0xffffffffffffffff;
      plVar30 = plVar38;
      do {
        plVar30 = (long *)*plVar30;
        uVar14 = uVar14 + 1;
        lVar40 = lVar40 + 4;
      } while (plVar30 != (long *)0x0);
      if (0x3ffffffffffffffe < uVar14) {
        FUN_00801dbc(&local_718);
                    /* WARNING: Does not return */
        pcVar9 = (code *)SoftwareBreakpoint(1,0x3af0ae8);
        (*pcVar9)();
      }
      local_718 = (undefined4 *)__Znwm(lVar40);
      local_708 = (long)local_718 + lVar40;
      puVar36 = local_718;
      do {
        local_710 = puVar36 + 1;
        *puVar36 = (int)plVar38[2];
        plVar38 = (long *)*plVar38;
        puVar36 = local_710;
      } while (plVar38 != (long *)0x0);
    }
    puVar8 = local_710;
    puVar36 = local_718;
    puStack_98 = &SUB_aaaaaaaaaaaaaaaa;
    local_a0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_a8 = &SUB_aaaaaaaaaaaaaaaa;
    local_b0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_b8 = &SUB_aaaaaaaaaaaaaaaa;
    local_c0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_c8 = &SUB_aaaaaaaaaaaaaaaa;
    local_d0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_d8 = &SUB_aaaaaaaaaaaaaaaa;
    local_e0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_e8 = &SUB_aaaaaaaaaaaaaaaa;
    local_f0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_f8 = &SUB_aaaaaaaaaaaaaaaa;
    local_100 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_108 = &SUB_aaaaaaaaaaaaaaaa;
    local_110 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_118 = &SUB_aaaaaaaaaaaaaaaa;
    local_120 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_128 = &SUB_aaaaaaaaaaaaaaaa;
    local_130 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_138 = &SUB_aaaaaaaaaaaaaaaa;
    local_140 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_148 = &SUB_aaaaaaaaaaaaaaaa;
    local_150 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_158 = &SUB_aaaaaaaaaaaaaaaa;
    local_160 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_168 = &SUB_aaaaaaaaaaaaaaaa;
    local_170 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_178 = &SUB_aaaaaaaaaaaaaaaa;
    local_180 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_188 = &SUB_aaaaaaaaaaaaaaaa;
    local_190 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_198 = &SUB_aaaaaaaaaaaaaaaa;
    local_1a0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_1a8 = &SUB_aaaaaaaaaaaaaaaa;
    local_1b0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_1b8 = &SUB_aaaaaaaaaaaaaaaa;
    local_1c0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_1c8 = &SUB_aaaaaaaaaaaaaaaa;
    local_1d0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_1d8 = &SUB_aaaaaaaaaaaaaaaa;
    local_1e0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_1e8 = &SUB_aaaaaaaaaaaaaaaa;
    local_1f0 = &SUB_aaaaaaaaaaaaaaaa;
    FUN_056cc60c(&local_350);
    lStack_498 = 0;
    local_4b0 = (undefined ********)&PTR_FUN_09da5fe0;
    ppppppppuStack_4a8 = (undefined ********)&ppppppppuStack_4a8;
    local_4a0 = (undefined ********)&ppppppppuStack_4a8;
    for (; puVar36 != puVar8; puVar36 = puVar36 + 1) {
      ppppppppuVar15 = (undefined ********)__Znwm(0x170);
      *ppppppppuVar15 = (undefined *******)0x0;
      ppppppppuVar15[1] = (undefined *******)0x0;
      FUN_026fc2c4(ppppppppuVar15 + 2,puVar36);
      *ppppppppuVar15 = (undefined *******)ppppppppuStack_4a8;
      ppppppppuVar15[1] = (undefined *******)&ppppppppuStack_4a8;
      ppppppppuStack_4a8[1] = (undefined *******)ppppppppuVar15;
      lStack_498 = lStack_498 + 1;
      ppppppppuStack_4a8 = ppppppppuVar15;
    }
    local_4b0 = (undefined ********)&PTR_FUN_09da5f48;
    FUN_056ca4ec(&local_1f0,auStack_290,&local_4b0);
    if (lStack_498 != 0) {
      pppppppuVar24 = ppppppppuStack_4a8[1];
      pppppppuVar31 = *local_4a0;
      pppppppuVar31[1] = (undefined ******)pppppppuVar24;
      *pppppppuVar24 = (undefined ******)pppppppuVar31;
      lStack_498 = 0;
      ppppppppuVar15 = local_4a0;
      while ((undefined *********)ppppppppuVar15 != &ppppppppuStack_4a8) {
        ppppppppuVar37 = (undefined ********)ppppppppuVar15[1];
        FUN_056cd5a8(ppppppppuVar15 + 2);
        __ZdlPvm(ppppppppuVar15,0x170);
        ppppppppuVar15 = ppppppppuVar37;
      }
    }
    FUN_056cc220(&local_350);
    local_720 = 0;
    local_738 = &PTR_FUN_09da5f48;
    local_730 = (long *******)&local_730;
    local_728 = (long *******)&local_730;
    FUN_056cc60c(&local_4b0);
    FUN_056cdd7c(&local_350,&local_4b0);
    pppppplVar16 = (long ******)__Znwm(0x170);
    *pppppplVar16 = (long *****)0x0;
    pppppplVar16[1] = (long *****)0x0;
    FUN_02dc2a4c(&local_720,pppppplVar16 + 2,&local_350);
    *pppppplVar16 = (long *****)local_730;
    pppppplVar16[1] = (long *****)&local_730;
    local_730[1] = pppppplVar16;
    local_720 = local_720 + 1;
    local_730 = (long *******)pppppplVar16;
    FUN_056cd5a8(&local_350);
    FUN_056cc220(&local_4b0);
    local_400 = &PTR____cxa_pure_virtual_09da57d8;
    FUN_056cbbe8(&local_4b0,&PTR_PTR_09f24220);
    local_4b0 = (undefined ********)&PTR_FUN_09f23fe8;
    local_400 = &PTR_FUN_09f24040;
    local_3f8 = &PTR_FUN_09f24080;
    local_3f0 = &PTR_FUN_09f240c0;
    local_3e8 = &PTR_FUN_09f24100;
    local_3e0 = &PTR_FUN_09f24140;
    local_3d8 = &PTR_FUN_09f24180;
    local_3d0 = &PTR_FUN_09f241c0;
    local_3c8 = &PTR_FUN_09f24200;
    uVar17 = FUN_04dd65e4();
    FUN_056fa6fc(&local_4b0,uVar17,0);
    FUN_02c98798(&local_350,&local_4b0);
    pppppplVar16 = (long ******)__Znwm(0x170);
    *pppppplVar16 = (long *****)0x0;
    pppppplVar16[1] = (long *****)0x0;
    FUN_02dc2a4c(&local_720,pppppplVar16 + 2,&local_350);
    *pppppplVar16 = (long *****)local_730;
    pppppplVar16[1] = (long *****)&local_730;
    local_730[1] = pppppplVar16;
    local_720 = local_720 + 1;
    local_730 = (long *******)pppppplVar16;
    FUN_056cd5a8(&local_350);
    FUN_056fa308(&local_4b0);
    puStack_748 = &SUB_aaaaaaaaaaaaaaaa;
    local_750 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    plStack_758 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    local_760 = &SUB_aaaaaaaaaaaaaaaa;
    lVar40 = param_1[1];
    FUN_02dbb528(&local_700,&local_738);
    local_700 = (undefined ********)&PTR_FUN_09da6740;
    if ((DAT_0a41c128 & 1) == 0) {
      DAT_0a41c120._0_1_ = s_empty_svName2Id_088c9b78[8];
      DAT_0a41c120._1_1_ = s_empty_svName2Id_088c9b78[9];
      DAT_0a41c120._2_1_ = s_empty_svName2Id_088c9b78[10];
      DAT_0a41c120._3_1_ = s_empty_svName2Id_088c9b78[0xb];
      DAT_0a41c120._4_1_ = s_empty_svName2Id_088c9b78[0xc];
      DAT_0a41c120._5_1_ = s_empty_svName2Id_088c9b78[0xd];
      DAT_0a41c120._6_1_ = s_empty_svName2Id_088c9b78[0xe];
      DAT_0a41c120._7_1_ = s_empty_svName2Id_088c9b78[0xf];
      DAT_0a41c128 = 1;
    }
    FUN_0562fcc8(&local_780,&DAT_0a41c120);
    local_588 = 0;
    local_5a0 = (undefined ********)&PTR_FUN_09da5e40;
    local_598 = (undefined *******)&local_598;
    local_590 = (undefined *******)&local_598;
    FUN_056cd3ec(&local_350);
    FUN_056cd3ec(&local_4b0);
    FUN_056f3dc4(&local_760,lVar40,&local_700,&local_780,&local_1f0,&local_5a0,&local_350,&local_4b0
                );
    FUN_056cd5a8(&local_4b0);
    FUN_056cd5a8(&local_350);
    if (local_588 != 0) {
      ppppppuVar25 = local_598[1];
      ppppppuVar32 = *local_590;
      ppppppuVar32[1] = (undefined *****)ppppppuVar25;
      *ppppppuVar25 = (undefined *****)ppppppuVar32;
      local_588 = 0;
      pppppppuVar24 = local_590;
      while (pppppppuVar24 != (undefined *******)&local_598) {
        pppppppuVar31 = (undefined *******)pppppppuVar24[1];
        FUN_056cf45c(pppppppuVar24 + 2);
        __ZdlPvm(pppppppuVar24,0x160);
        pppppppuVar24 = pppppppuVar31;
      }
    }
    FUN_0562fd84(&local_780);
    if (local_6e8 != 0) {
      ppppppuVar25 = local_6f8[1];
      pppppuVar33 = *(undefined ******)CONCAT17(cStack_6e9,local_6f0);
      pppppuVar33[1] = (undefined ****)ppppppuVar25;
      *ppppppuVar25 = pppppuVar33;
      local_6e8 = 0;
      plVar38 = (long *)CONCAT17(cStack_6e9,local_6f0);
      while (plVar38 != &local_6f8) {
        plVar30 = (long *)plVar38[1];
        (**(code **)plVar38[2])();
        __ZdlPvm(plVar38,0x158);
        plVar38 = plVar30;
      }
    }
    plVar30 = local_750;
    plVar38 = plStack_758;
    if ((char)local_760 == '\x01') {
      for (; plVar38 != plVar30; plVar38 = plVar38 + 3) {
        uVar11 = FUN_056cb608(*plVar38);
        local_700 = (undefined ********)CONCAT44(local_700._4_4_,uVar11);
        FUN_056cb228(&local_4b0,*plVar38 + 0x68);
        pcVar18 = (char *)FUN_0008a8b8(&local_4b0);
        sVar19 = _strlen(pcVar18);
        if (0x7ffffffffffffff7 < sVar19) {
                    /* WARNING: Subroutine does not return */
          FUN_00018d9c(&local_350);
        }
        if (sVar19 < 0x17) {
          local_340 = CONCAT17((char)sVar19,(undefined7)local_340);
          pppppppuVar20 = &local_350;
          if (sVar19 != 0) goto LAB_03aefb44;
        }
        else {
          uVar14 = 0x19;
          if ((sVar19 | 7) != 0x17) {
            uVar14 = (sVar19 | 7) + 1;
          }
          pppppppuVar20 = (undefined8 *******)__Znwm(uVar14);
          local_340 = uVar14 | 0x8000000000000000;
          local_350 = pppppppuVar20;
          sStack_348 = sVar19;
LAB_03aefb44:
          _memmove(pppppppuVar20,pcVar18,sVar19);
        }
        *(undefined1 *)((long)pppppppuVar20 + sVar19) = 0;
        FUN_032a2ab4(param_3,&local_700,&local_700,&local_350);
        if ((long)local_340 < 0) {
          __ZdlPvm(local_350,local_340 & 0x7fffffffffffffff);
        }
        FUN_0562fd84(&local_4b0);
      }
      iVar13 = thunk_FUN_05e1d97c(2);
      if (iVar13 != 0) {
        FUN_0488143c(&local_780);
        pppppppuVar20 = local_780;
        if (-1 < (long)local_770) {
          pppppppuVar20 = &local_780;
        }
        if ((DAT_0a41be80 & 1) == 0) {
          uRam000000000a41be78._0_1_ = s_base_storage_cc_08964550[8];
          uRam000000000a41be78._1_1_ = s_base_storage_cc_08964550[9];
          uRam000000000a41be78._2_1_ = s_base_storage_cc_08964550[10];
          uRam000000000a41be78._3_1_ = s_base_storage_cc_08964550[0xb];
          uRam000000000a41be78._4_1_ = s_base_storage_cc_08964550[0xc];
          uRam000000000a41be78._5_1_ = s_base_storage_cc_08964550[0xd];
          uRam000000000a41be78._6_1_ = s_base_storage_cc_08964550[0xe];
          uRam000000000a41be78._7_1_ = s_base_storage_cc_08964550[0xf];
          DAT_0a41be70 = s_base_storage_cc_08964550[0];
          DAT_0a41be70_1._0_1_ = s_base_storage_cc_08964550[1];
          DAT_0a41be70_1._1_1_ = s_base_storage_cc_08964550[2];
          DAT_0a41be70_1._2_1_ = s_base_storage_cc_08964550[3];
          DAT_0a41be70_1._3_1_ = s_base_storage_cc_08964550[4];
          DAT_0a41be70_1._4_1_ = s_base_storage_cc_08964550[5];
          DAT_0a41be70_1._5_1_ = s_base_storage_cc_08964550[6];
          DAT_0a41be70_1._6_1_ = s_base_storage_cc_08964550[7];
          DAT_0a41be80 = 1;
        }
        if ((DAT_0a41c249 & 1) == 0) {
          uVar14 = 0;
          do {
            (&DAT_0a41c233)[uVar14] = (&DAT_08964ff2)[uVar14 & 0xf] ^ (&DAT_08965002)[uVar14];
            uVar14 = uVar14 + 1;
          } while (uVar14 != 0x16);
          DAT_0a41c249 = 1;
        }
        FUN_05e1d050(&local_350,2,pppppppuVar20,&DAT_0a41be70,&DAT_0a41c233,0x1c9,0,0);
        local_700 = (undefined ********)0x0;
        if ((DAT_0a41c597 & 1) == 0) {
          uVar14 = 0;
          do {
            uVar11 = *(undefined4 *)((long)&DAT_08965616 + uVar14);
            uVar2 = CONCAT12((char)((uint)uVar11 >> 8),(short)uVar11) & 0xff00ff;
            uVar52 = *(undefined4 *)((long)&DAT_08965602 + uVar14 % 0x14);
            *(uint *)((long)&DAT_0a41c54f + uVar14) =
                 CONCAT13((char)((uint)uVar11 >> 0x18) + 0x8aU ^ (byte)((uint)uVar52 >> 0x18),
                          CONCAT12((char)((uint)uVar11 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar52 >> 0x10),
                                   CONCAT11((char)(uVar2 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar52 >> 8),
                                            (char)uVar2 + 0x8aU ^ (byte)uVar52)));
            uVar14 = uVar14 + 4;
          } while (uVar14 != 0x48);
          DAT_0a41c597 = 1;
        }
        uVar14 = ((long)local_750 - (long)plStack_758 >> 3) * -0x5555555555555555;
        lVar40 = 0;
        do {
          lVar28 = lVar40;
          *(undefined1 *)((long)&local_6f8 + lVar28) = (&DAT_0a41c572)[uVar14 % 10];
          bVar10 = 9 < uVar14;
          uVar14 = uVar14 / 10;
          lVar40 = lVar28 + 1;
        } while (bVar10);
        *(undefined1 *)((long)&local_6f8 + lVar28 + 1) = 0;
        if (8 < lVar28 + 8U) {
          puVar27 = (undefined1 *)((long)&local_6f8 + lVar28);
          puVar21 = (undefined1 *)((long)&local_6f8 + 1);
          do {
            uVar1 = *puVar27;
            *puVar27 = puVar21[-1];
            puVar21[-1] = uVar1;
            bVar10 = puVar21 < puVar27 + -1;
            puVar27 = puVar27 + -1;
            puVar21 = puVar21 + 1;
          } while (bVar10);
        }
        local_700 = (undefined ********)&local_6f8;
        local_5a0 = (undefined ********)0x0;
        local_5a0 = (undefined ********)&local_598;
        lVar40 = 0;
        uVar14 = *(ulong *)(param_2 + 0x18);
        do {
          lVar28 = lVar40;
          *(undefined1 *)((long)&local_598 + lVar28) = (&DAT_0a41c572)[uVar14 % 10];
          bVar10 = 9 < uVar14;
          lVar40 = lVar28 + 1;
          uVar14 = uVar14 / 10;
        } while (bVar10);
        *(undefined1 *)((long)&local_598 + lVar28 + 1) = 0;
        if (8 < lVar28 + 8U) {
          puVar27 = (undefined1 *)((long)&local_598 + lVar28);
          puVar21 = (undefined1 *)((long)&local_598 + 1);
          do {
            uVar1 = *puVar27;
            *puVar27 = puVar21[-1];
            puVar21[-1] = uVar1;
            bVar10 = puVar21 < puVar27 + -1;
            puVar27 = puVar27 + -1;
            puVar21 = puVar21 + 1;
          } while (bVar10);
        }
        if ((DAT_0a41c26b & 1) == 0) {
          _DAT_0a41c24c = CONCAT44((int)DAT_088df260,(int)DAT_0848be60);
          uRam000000000a41c254 = CONCAT44((int)DAT_08895b80,(int)DAT_0847fdf8);
          DAT_0a41c25c = CONCAT44((int)ram0x08850000,(int)DAT_08610dd0);
          DAT_0a41c264 = (undefined4)DAT_088544c0;
          DAT_0a41c268 = 0x5f25;
          DAT_0a41c26a = 0;
          DAT_0a41c26b = 1;
        }
        local_4b0 = (undefined ********)&local_700;
        ppppppppuStack_4a8 = (undefined ********)&local_5a0;
        lStack_498 = 0;
        local_4a0 = (undefined ********)0x0;
        uStack_488 = 0;
        uStack_490 = 0;
        uStack_478 = 0;
        uStack_480 = 0;
        uStack_468 = 0;
        uStack_470 = 0;
        uStack_458 = 0;
        local_460 = 0;
        uStack_448 = 0;
        local_450 = 0;
        uStack_438 = 0;
        local_440 = 0;
        FUN_05e1d31c(&local_350,&DAT_0a41c24c,&local_4b0);
LAB_03af0968:
        thunk_FUN_05e1d0bc(&local_350);
        if ((long)local_770 < 0) {
          __ZdlPvm(local_780,(ulong)local_770 & 0x7fffffffffffffff);
        }
      }
    }
    else {
      iVar13 = thunk_FUN_05e1d97c(4);
      if (iVar13 != 0) {
        FUN_0488143c(&local_700);
        ppppppppuVar15 = local_700;
        if (-1 < cStack_6e9) {
          ppppppppuVar15 = (undefined ********)&local_700;
        }
        if ((DAT_0a41be80 & 1) == 0) {
          uRam000000000a41be78._0_1_ = s_base_storage_cc_08964550[8];
          uRam000000000a41be78._1_1_ = s_base_storage_cc_08964550[9];
          uRam000000000a41be78._2_1_ = s_base_storage_cc_08964550[10];
          uRam000000000a41be78._3_1_ = s_base_storage_cc_08964550[0xb];
          uRam000000000a41be78._4_1_ = s_base_storage_cc_08964550[0xc];
          uRam000000000a41be78._5_1_ = s_base_storage_cc_08964550[0xd];
          uRam000000000a41be78._6_1_ = s_base_storage_cc_08964550[0xe];
          uRam000000000a41be78._7_1_ = s_base_storage_cc_08964550[0xf];
          DAT_0a41be70 = s_base_storage_cc_08964550[0];
          DAT_0a41be70_1._0_1_ = s_base_storage_cc_08964550[1];
          DAT_0a41be70_1._1_1_ = s_base_storage_cc_08964550[2];
          DAT_0a41be70_1._2_1_ = s_base_storage_cc_08964550[3];
          DAT_0a41be70_1._3_1_ = s_base_storage_cc_08964550[4];
          DAT_0a41be70_1._4_1_ = s_base_storage_cc_08964550[5];
          DAT_0a41be70_1._5_1_ = s_base_storage_cc_08964550[6];
          DAT_0a41be70_1._6_1_ = s_base_storage_cc_08964550[7];
          DAT_0a41be80 = 1;
        }
        if ((DAT_0a41c249 & 1) == 0) {
          uVar14 = 0;
          do {
            (&DAT_0a41c233)[uVar14] = (&DAT_08964ff2)[uVar14 & 0xf] ^ (&DAT_08965002)[uVar14];
            uVar14 = uVar14 + 1;
          } while (uVar14 != 0x16);
          DAT_0a41c249 = 1;
        }
        FUN_05e1d050(&local_350,4,ppppppppuVar15,&DAT_0a41be70,&DAT_0a41c233,0x1d1,0,0);
        if ((DAT_0a41c28d & 1) == 0) {
          _DAT_0a41c26c = CONCAT44((int)DAT_088df260,(int)DAT_0848be60);
          uRam000000000a41c274 = CONCAT44((int)DAT_08895b80,(int)DAT_0847fdf8);
          _DAT_0a41c27c = CONCAT44((int)DAT_084d77b8,(int)DAT_084caf60);
          uRam000000000a41c284 = CONCAT44((int)DAT_0849b838,(int)DAT_08563690);
          DAT_0a41c28c = 0;
          DAT_0a41c28d = 1;
        }
        uStack_448 = 0;
        local_450 = 0;
        uStack_438 = 0;
        local_440 = 0;
        uStack_468 = 0;
        uStack_470 = 0;
        uStack_458 = 0;
        local_460 = 0;
        uStack_488 = 0;
        uStack_490 = 0;
        uStack_478 = 0;
        uStack_480 = 0;
        ppppppppuStack_4a8 = (undefined ********)0x0;
        local_4b0 = (undefined ********)0x0;
        lStack_498 = 0;
        local_4a0 = (undefined ********)0x0;
        FUN_05e1d31c(&local_350,&DAT_0a41c26c,&local_4b0);
        thunk_FUN_05e1d0bc(&local_350);
        if (cStack_6e9 < '\0') {
          __ZdlPvm(local_700,CONCAT17(cStack_6e9,local_6f0) & 0x7fffffffffffffff);
        }
      }
      uVar6 = s_base_storage_cc_08964550._8_8_;
      uVar5 = s_base_storage_cc_08964550._0_8_;
      uVar17 = s_empty_svName2Id_088c9b78._8_8_;
      plVar38 = *(long **)(param_2 + 0x10);
      if (plVar38 != (long *)0x0) {
        uVar43 = (undefined4)DAT_088df260;
        uVar48 = (undefined4)DAT_0848be60;
        uVar11 = (undefined4)DAT_0847fdf8;
        uVar44 = (undefined4)DAT_08895b80;
        uVar45 = (undefined4)DAT_084d77b8;
        uVar49 = (undefined4)DAT_084caf60;
        uVar52 = (undefined4)DAT_08563690;
        uVar46 = (undefined4)DAT_0849b838;
        uVar47 = (undefined4)DAT_084d1ec0;
        uVar50 = (undefined4)DAT_084d4ad0;
        do {
          puStack_778 = &SUB_aaaaaaaaaaaaaaaa;
          local_780 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
          local_768 = &SUB_aaaaaaaaaaaaaaaa;
          local_770 = &SUB_aaaaaaaaaaaaaaaa;
          lVar40 = param_1[1];
          FUN_02dbb528(&local_7a0,&local_738);
          uVar4 = s_empty_svName2Id_088c9b78._8_8_;
          local_7a0 = &PTR_FUN_09da6740;
          if ((DAT_0a41c128 & 1) == 0) {
            s_empty_svName2Id_088c9b78[8] = (char)uVar17;
            s_empty_svName2Id_088c9b78[9] = SUB81(uVar17,1);
            s_empty_svName2Id_088c9b78[10] = SUB81(uVar17,2);
            s_empty_svName2Id_088c9b78[0xb] = SUB81(uVar17,3);
            s_empty_svName2Id_088c9b78[0xc] = SUB81(uVar17,4);
            s_empty_svName2Id_088c9b78[0xd] = SUB81(uVar17,5);
            s_empty_svName2Id_088c9b78[0xe] = SUB81(uVar17,6);
            s_empty_svName2Id_088c9b78[0xf] = SUB81(uVar17,7);
            DAT_0a41c120._0_1_ = s_empty_svName2Id_088c9b78[8];
            DAT_0a41c120._1_1_ = s_empty_svName2Id_088c9b78[9];
            DAT_0a41c120._2_1_ = s_empty_svName2Id_088c9b78[10];
            DAT_0a41c120._3_1_ = s_empty_svName2Id_088c9b78[0xb];
            DAT_0a41c120._4_1_ = s_empty_svName2Id_088c9b78[0xc];
            DAT_0a41c120._5_1_ = s_empty_svName2Id_088c9b78[0xd];
            DAT_0a41c120._6_1_ = s_empty_svName2Id_088c9b78[0xe];
            DAT_0a41c120._7_1_ = s_empty_svName2Id_088c9b78[0xf];
            DAT_0a41c128 = 1;
          }
          s_empty_svName2Id_088c9b78._8_8_ = uVar4;
          FUN_0562fcc8(auStack_7b8,&DAT_0a41c120);
          FUN_056cc60c(&local_5a0);
          FUN_026fc2c4(&local_4b0,plVar38 + 2);
          FUN_056c9dac(&local_350,auStack_4e8,&local_4b0);
          local_7d0 = &local_7d0;
          local_7c0 = 0;
          local_7d8 = &PTR_FUN_09da5e40;
          local_7c8 = &local_7d0;
          FUN_056cd3ec(&local_700);
          FUN_056f3a00(&local_780,lVar40,&local_7a0,auStack_7b8,&local_350,&local_7d8,&local_700);
          FUN_056cd5a8(&local_700);
          if (local_7c0 != 0) {
            ppppppuVar26 = local_7d0[1];
            ppppppuVar34 = *local_7c8;
            ppppppuVar34[1] = ppppppuVar26;
            *ppppppuVar26 = ppppppuVar34;
            local_7c0 = 0;
            pppppppuVar20 = local_7c8;
            while ((undefined8 ********)pppppppuVar20 != &local_7d0) {
              pppppppuVar41 = (undefined8 *******)pppppppuVar20[1];
              FUN_056cf45c(pppppppuVar20 + 2);
              __ZdlPvm(pppppppuVar20,0x160);
              pppppppuVar20 = pppppppuVar41;
            }
          }
          FUN_056cd5a8(&local_350);
          FUN_056cd5a8(&local_4b0);
          FUN_056cc220(&local_5a0);
          FUN_0562fd84(auStack_7b8);
          if (local_788 != 0) {
            plVar30 = *(long **)(local_798 + 8);
            lVar40 = *plStack_790;
            *(long **)(lVar40 + 8) = plVar30;
            *plVar30 = lVar40;
            local_788 = 0;
            plVar30 = plStack_790;
            while (plVar30 != &local_798) {
              plVar42 = (long *)plVar30[1];
              (**(code **)plVar30[2])();
              __ZdlPvm(plVar30,0x158);
              plVar30 = plVar42;
            }
          }
          if ((char)local_780 == '\x01') {
            uVar12 = FUN_056cb608(puStack_778);
            local_700 = (undefined ********)CONCAT44(local_700._4_4_,uVar12);
            FUN_056cb228(&local_4b0,puStack_778 + 0x68);
            pcVar18 = (char *)FUN_0008a8b8(&local_4b0);
            sVar19 = _strlen(pcVar18);
            if (0x7ffffffffffffff7 < sVar19) {
                    /* WARNING: Subroutine does not return */
              FUN_00018d9c(&local_350);
            }
            if (sVar19 < 0x17) {
              local_340 = CONCAT17((char)sVar19,(undefined7)local_340);
              pppppppuVar20 = &local_350;
              if (sVar19 != 0) goto LAB_03af0270;
            }
            else {
              uVar14 = 0x19;
              if ((sVar19 | 7) != 0x17) {
                uVar14 = (sVar19 | 7) + 1;
              }
              pppppppuVar20 = (undefined8 *******)__Znwm(uVar14);
              local_340 = uVar14 | 0x8000000000000000;
              local_350 = pppppppuVar20;
              sStack_348 = sVar19;
LAB_03af0270:
              _memmove(pppppppuVar20,pcVar18,sVar19);
            }
            *(undefined1 *)((long)pppppppuVar20 + sVar19) = 0;
            FUN_032a2ab4(param_3,&local_700,&local_700,&local_350);
            if ((long)local_340 < 0) {
              __ZdlPvm(local_350,local_340 & 0x7fffffffffffffff);
            }
            FUN_0562fd84(&local_4b0);
          }
          else {
            iVar13 = thunk_FUN_05e1d97c(4);
            if (iVar13 != 0) {
              FUN_0488143c(&local_5a0);
              uVar7 = s_base_storage_cc_08964550._8_8_;
              uVar4 = s_base_storage_cc_08964550._0_8_;
              ppppppppuVar15 = local_5a0;
              if (-1 < (long)local_590) {
                ppppppppuVar15 = (undefined ********)&local_5a0;
              }
              if ((DAT_0a41be80 & 1) == 0) {
                s_base_storage_cc_08964550[8] = (char)uVar6;
                s_base_storage_cc_08964550[9] = SUB81(uVar6,1);
                s_base_storage_cc_08964550[10] = SUB81(uVar6,2);
                s_base_storage_cc_08964550[0xb] = SUB81(uVar6,3);
                s_base_storage_cc_08964550[0xc] = SUB81(uVar6,4);
                s_base_storage_cc_08964550[0xd] = SUB81(uVar6,5);
                s_base_storage_cc_08964550[0xe] = SUB81(uVar6,6);
                s_base_storage_cc_08964550[0xf] = SUB81(uVar6,7);
                uRam000000000a41be78._0_1_ = s_base_storage_cc_08964550[8];
                uRam000000000a41be78._1_1_ = s_base_storage_cc_08964550[9];
                uRam000000000a41be78._2_1_ = s_base_storage_cc_08964550[10];
                uRam000000000a41be78._3_1_ = s_base_storage_cc_08964550[0xb];
                uRam000000000a41be78._4_1_ = s_base_storage_cc_08964550[0xc];
                uRam000000000a41be78._5_1_ = s_base_storage_cc_08964550[0xd];
                uRam000000000a41be78._6_1_ = s_base_storage_cc_08964550[0xe];
                uRam000000000a41be78._7_1_ = s_base_storage_cc_08964550[0xf];
                s_base_storage_cc_08964550[0] = (char)uVar5;
                s_base_storage_cc_08964550[1] = SUB81(uVar5,1);
                s_base_storage_cc_08964550[2] = SUB81(uVar5,2);
                s_base_storage_cc_08964550[3] = SUB81(uVar5,3);
                s_base_storage_cc_08964550[4] = SUB81(uVar5,4);
                s_base_storage_cc_08964550[5] = SUB81(uVar5,5);
                s_base_storage_cc_08964550[6] = SUB81(uVar5,6);
                s_base_storage_cc_08964550[7] = SUB81(uVar5,7);
                DAT_0a41be70 = s_base_storage_cc_08964550[0];
                DAT_0a41be70_1._0_1_ = s_base_storage_cc_08964550[1];
                DAT_0a41be70_1._1_1_ = s_base_storage_cc_08964550[2];
                DAT_0a41be70_1._2_1_ = s_base_storage_cc_08964550[3];
                DAT_0a41be70_1._3_1_ = s_base_storage_cc_08964550[4];
                DAT_0a41be70_1._4_1_ = s_base_storage_cc_08964550[5];
                DAT_0a41be70_1._5_1_ = s_base_storage_cc_08964550[6];
                DAT_0a41be70_1._6_1_ = s_base_storage_cc_08964550[7];
                DAT_0a41be80 = 1;
              }
              s_base_storage_cc_08964550._0_8_ = uVar4;
              s_base_storage_cc_08964550._8_8_ = uVar7;
              if ((DAT_0a41c249 & 1) == 0) {
                uVar14 = 0;
                do {
                  (&DAT_0a41c233)[uVar14] = (&DAT_08964ff2)[uVar14 & 0xf] ^ (&DAT_08965002)[uVar14];
                  uVar14 = uVar14 + 1;
                } while (uVar14 != 0x16);
                DAT_0a41c249 = 1;
              }
              FUN_05e1d050(&local_350,4,ppppppppuVar15,&DAT_0a41be70,&DAT_0a41c233,0x1dd,0,0);
              uVar23 = *(uint *)(plVar38 + 2);
              local_700 = (undefined ********)0x0;
              if ((DAT_0a41c597 & 1) == 0) {
                uVar14 = 0;
                do {
                  uVar12 = *(undefined4 *)((long)&DAT_08965616 + uVar14);
                  uVar2 = CONCAT12((char)((uint)uVar12 >> 8),(short)uVar12) & 0xff00ff;
                  uVar51 = *(undefined4 *)((long)&DAT_08965602 + uVar14 % 0x14);
                  *(uint *)((long)&DAT_0a41c54f + uVar14) =
                       CONCAT13((char)((uint)uVar12 >> 0x18) + 0x8aU ^ (byte)((uint)uVar51 >> 0x18),
                                CONCAT12((char)((uint)uVar12 >> 0x10) + 0x8aU ^
                                         (byte)((uint)uVar51 >> 0x10),
                                         CONCAT11((char)(uVar2 >> 0x10) + 0x8aU ^
                                                  (byte)((uint)uVar51 >> 8),
                                                  (char)uVar2 + 0x8aU ^ (byte)uVar51)));
                  uVar14 = uVar14 + 4;
                } while (uVar14 != 0x48);
                DAT_0a41c597 = 1;
              }
              uVar14 = (ulong)uVar23;
              lVar40 = 0;
              do {
                lVar28 = lVar40;
                uVar23 = (uint)uVar14;
                *(undefined1 *)((long)&local_6f8 + lVar28) =
                     *(undefined1 *)
                      ((long)&DAT_0a41c54f + (ulong)(uVar23 + (int)(uVar14 / 10) * -10 + 0x23));
                uVar14 = uVar14 / 10;
                lVar40 = lVar28 + 1;
              } while (9 < uVar23);
              *(undefined1 *)((long)&local_6f8 + lVar28 + 1) = 0;
              if (8 < lVar28 + 8U) {
                puVar27 = (undefined1 *)((long)&local_6f8 + lVar28);
                puVar21 = (undefined1 *)((long)&local_6f8 + 1);
                do {
                  uVar1 = *puVar27;
                  *puVar27 = puVar21[-1];
                  puVar21[-1] = uVar1;
                  bVar10 = puVar21 < puVar27 + -1;
                  puVar27 = puVar27 + -1;
                  puVar21 = puVar21 + 1;
                } while (bVar10);
              }
              if ((DAT_0a41c2b8 & 1) == 0) {
                DAT_0a41c2b8 = 1;
                _DAT_0a41c290 = CONCAT44(uVar43,uVar48);
                uRam000000000a41c298 = CONCAT44(uVar44,uVar11);
                _DAT_0a41c2a0 = CONCAT44(uVar45,uVar49);
                uRam000000000a41c2a8 = CONCAT44(uVar46,uVar52);
                DAT_0a41c2b0 = CONCAT44(uVar47,uVar50);
              }
              local_4a0 = (undefined ********)0x0;
              ppppppppuStack_4a8 = (undefined ********)0x0;
              uStack_490 = 0;
              lStack_498 = 0;
              uStack_480 = 0;
              uStack_488 = 0;
              uStack_470 = 0;
              uStack_478 = 0;
              local_460 = 0;
              uStack_468 = 0;
              local_450 = 0;
              uStack_458 = 0;
              local_440 = 0;
              uStack_448 = 0;
              uStack_438 = 0;
              local_700 = (undefined ********)&local_6f8;
              local_4b0 = (undefined ********)&local_700;
              FUN_05e1d31c(&local_350,&DAT_0a41c290,&local_4b0);
              thunk_FUN_05e1d0bc(&local_350);
              if ((long)local_590 < 0) {
                __ZdlPvm(local_5a0,(ulong)local_590 & 0x7fffffffffffffff);
              }
            }
          }
          puVar27 = puStack_778;
          if (((char)local_780 == '\x01') && (puVar21 = local_770, puStack_778 != (undefined1 *)0x0)
             ) {
            for (; puVar21 != puVar27; puVar21 = (undefined1 *)FUN_056caefc(puVar21 + -0x68)) {
            }
            local_770 = puVar27;
            __ZdlPvm(puStack_778,(long)local_768 - (long)puStack_778);
          }
          plVar38 = (long *)*plVar38;
        } while (plVar38 != (long *)0x0);
      }
      iVar13 = thunk_FUN_05e1d97c(2);
      if (iVar13 != 0) {
        FUN_0488143c(&local_780);
        pppppppuVar20 = local_780;
        if (-1 < (long)local_770) {
          pppppppuVar20 = &local_780;
        }
        if ((DAT_0a41be80 & 1) == 0) {
          uRam000000000a41be78._0_1_ = s_base_storage_cc_08964550[8];
          uRam000000000a41be78._1_1_ = s_base_storage_cc_08964550[9];
          uRam000000000a41be78._2_1_ = s_base_storage_cc_08964550[10];
          uRam000000000a41be78._3_1_ = s_base_storage_cc_08964550[0xb];
          uRam000000000a41be78._4_1_ = s_base_storage_cc_08964550[0xc];
          uRam000000000a41be78._5_1_ = s_base_storage_cc_08964550[0xd];
          uRam000000000a41be78._6_1_ = s_base_storage_cc_08964550[0xe];
          uRam000000000a41be78._7_1_ = s_base_storage_cc_08964550[0xf];
          DAT_0a41be70 = s_base_storage_cc_08964550[0];
          DAT_0a41be70_1._0_1_ = s_base_storage_cc_08964550[1];
          DAT_0a41be70_1._1_1_ = s_base_storage_cc_08964550[2];
          DAT_0a41be70_1._2_1_ = s_base_storage_cc_08964550[3];
          DAT_0a41be70_1._3_1_ = s_base_storage_cc_08964550[4];
          DAT_0a41be70_1._4_1_ = s_base_storage_cc_08964550[5];
          DAT_0a41be70_1._5_1_ = s_base_storage_cc_08964550[6];
          DAT_0a41be70_1._6_1_ = s_base_storage_cc_08964550[7];
          DAT_0a41be80 = 1;
        }
        if ((DAT_0a41c249 & 1) == 0) {
          uVar14 = 0;
          do {
            (&DAT_0a41c233)[uVar14] = (&DAT_08964ff2)[uVar14 & 0xf] ^ (&DAT_08965002)[uVar14];
            uVar14 = uVar14 + 1;
          } while (uVar14 != 0x16);
          DAT_0a41c249 = 1;
        }
        FUN_05e1d050(&local_350,2,pppppppuVar20,&DAT_0a41be70,&DAT_0a41c233,0x1e1,0,0);
        uVar14 = *(ulong *)(param_3 + 0x18);
        local_700 = (undefined ********)0x0;
        if ((DAT_0a41c597 & 1) == 0) {
          uVar35 = 0;
          do {
            uVar11 = *(undefined4 *)((long)&DAT_08965616 + uVar35);
            uVar2 = CONCAT12((char)((uint)uVar11 >> 8),(short)uVar11) & 0xff00ff;
            uVar52 = *(undefined4 *)((long)&DAT_08965602 + uVar35 % 0x14);
            *(uint *)((long)&DAT_0a41c54f + uVar35) =
                 CONCAT13((char)((uint)uVar11 >> 0x18) + 0x8aU ^ (byte)((uint)uVar52 >> 0x18),
                          CONCAT12((char)((uint)uVar11 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar52 >> 0x10),
                                   CONCAT11((char)(uVar2 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar52 >> 8),
                                            (char)uVar2 + 0x8aU ^ (byte)uVar52)));
            uVar35 = uVar35 + 4;
          } while (uVar35 != 0x48);
          DAT_0a41c597 = 1;
        }
        lVar40 = 0;
        do {
          lVar28 = lVar40;
          *(undefined1 *)((long)&local_6f8 + lVar28) = (&DAT_0a41c572)[uVar14 % 10];
          bVar10 = 9 < uVar14;
          uVar14 = uVar14 / 10;
          lVar40 = lVar28 + 1;
        } while (bVar10);
        *(undefined1 *)((long)&local_6f8 + lVar28 + 1) = 0;
        if (8 < lVar28 + 8U) {
          puVar27 = (undefined1 *)((long)&local_6f8 + lVar28);
          puVar21 = (undefined1 *)((long)&local_6f8 + 1);
          do {
            uVar1 = *puVar27;
            *puVar27 = puVar21[-1];
            puVar21[-1] = uVar1;
            bVar10 = puVar21 < puVar27 + -1;
            puVar27 = puVar27 + -1;
            puVar21 = puVar21 + 1;
          } while (bVar10);
        }
        local_700 = (undefined ********)&local_6f8;
        local_5a0 = (undefined ********)0x0;
        local_5a0 = (undefined ********)&local_598;
        lVar40 = 0;
        uVar14 = *(ulong *)(param_2 + 0x18);
        do {
          lVar28 = lVar40;
          *(undefined1 *)((long)&local_598 + lVar28) = (&DAT_0a41c572)[uVar14 % 10];
          bVar10 = 9 < uVar14;
          lVar40 = lVar28 + 1;
          uVar14 = uVar14 / 10;
        } while (bVar10);
        *(undefined1 *)((long)&local_598 + lVar28 + 1) = 0;
        if (8 < lVar28 + 8U) {
          puVar27 = (undefined1 *)((long)&local_598 + lVar28);
          puVar21 = (undefined1 *)((long)&local_598 + 1);
          do {
            uVar1 = *puVar27;
            *puVar27 = puVar21[-1];
            puVar21[-1] = uVar1;
            bVar10 = puVar21 < puVar27 + -1;
            puVar27 = puVar27 + -1;
            puVar21 = puVar21 + 1;
          } while (bVar10);
        }
        if ((DAT_0a41c2e5 & 1) == 0) {
          _DAT_0a41c2bc = CONCAT44((int)DAT_088df260,(int)DAT_0848be60);
          uRam000000000a41c2c4 = CONCAT44((int)DAT_08531b60,(int)DAT_0847fdf8);
          _DAT_0a41c2cc = CONCAT44((int)DAT_084d86b0,(int)DAT_0855a590);
          uRam000000000a41c2d4 = CONCAT44((int)DAT_0855a678,(int)ram0x08489fc8);
          DAT_0a41c2dc = CONCAT44((int)DAT_084d57c0,(int)DAT_084937e0);
          DAT_0a41c2e4 = 0;
          DAT_0a41c2e5 = 1;
        }
        local_4b0 = (undefined ********)&local_700;
        ppppppppuStack_4a8 = (undefined ********)&local_5a0;
        lStack_498 = 0;
        local_4a0 = (undefined ********)0x0;
        uStack_488 = 0;
        uStack_490 = 0;
        uStack_478 = 0;
        uStack_480 = 0;
        uStack_468 = 0;
        uStack_470 = 0;
        uStack_458 = 0;
        local_460 = 0;
        uStack_448 = 0;
        local_450 = 0;
        uStack_438 = 0;
        local_440 = 0;
        FUN_05e1d31c(&local_350,&DAT_0a41c2bc,&local_4b0);
        goto LAB_03af0968;
      }
    }
    plVar38 = plStack_758;
    if (((char)local_760 == '\x01') && (plVar30 = local_750, plStack_758 != (long *)0x0)) {
      while (plVar42 = plVar30, plVar42 != plVar38) {
        plVar30 = plVar42 + -3;
        lVar40 = *plVar30;
        if (lVar40 != 0) {
          lVar22 = plVar42[-2];
          lVar28 = lVar40;
          if (lVar22 != lVar40) {
            do {
              lVar22 = FUN_056caefc(lVar22 + -0x68);
            } while (lVar22 != lVar40);
            lVar28 = *plVar30;
          }
          plVar42[-2] = lVar40;
          __ZdlPvm(lVar28,plVar42[-1] - lVar28);
        }
      }
      local_750 = plVar38;
      __ZdlPvm(plStack_758,(long)puStack_748 - (long)plStack_758);
    }
    if (local_720 != 0) {
      ppppplVar29 = (long *****)local_730[1];
      pppppplVar16 = *local_728;
      pppppplVar16[1] = ppppplVar29;
      *ppppplVar29 = (long ****)pppppplVar16;
      local_720 = 0;
      ppppppplVar3 = local_728;
      while ((long ********)ppppppplVar3 != &local_730) {
        ppppppplVar39 = (long *******)ppppppplVar3[1];
        FUN_056cd5a8(ppppppplVar3 + 2);
        __ZdlPvm(ppppppplVar3,0x170);
        ppppppplVar3 = ppppppplVar39;
      }
    }
    FUN_056cd5a8(&local_1f0);
    if (local_718 != (undefined4 *)0x0) {
      __ZdlPvm(local_718,local_708 - (long)local_718);
    }
  }
  uVar17 = 1;
LAB_03af0a84:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_88) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail(uVar17);
}


