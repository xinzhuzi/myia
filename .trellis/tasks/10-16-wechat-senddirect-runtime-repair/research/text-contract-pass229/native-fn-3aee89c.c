// Ghidra inferred pseudocode; requested=0x3aee89c
// entry=03aee89c end=03aef2ff

/* WARNING: Removing unreachable block (ram,0x03aef298) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_03aee89c(long *param_1,long param_2,long param_3)

{
  undefined8 *******pppppppuVar1;
  long *******ppppppplVar2;
  undefined1 uVar3;
  uint3 uVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  undefined8 uVar8;
  long *plVar9;
  bool bVar10;
  undefined1 *puVar11;
  int iVar12;
  ulong uVar13;
  undefined8 uVar14;
  code *pcVar15;
  undefined1 *puVar16;
  undefined1 *puVar17;
  long lVar18;
  ulong uVar19;
  long *plVar20;
  undefined4 uVar21;
  undefined4 uVar22;
  undefined4 uVar23;
  undefined4 uVar24;
  undefined4 uVar25;
  undefined4 uVar26;
  long ******pppppplVar27;
  long lVar28;
  undefined4 uVar29;
  undefined4 uVar30;
  undefined4 uVar31;
  undefined4 uVar32;
  undefined4 uVar33;
  undefined4 uVar34;
  undefined8 *******local_2f0 [2];
  undefined7 local_2e0;
  char cStack_2d9;
  long *local_2d8;
  long *local_2d0;
  long *local_2c8;
  undefined4 *local_2c0;
  undefined1 local_2b8;
  undefined1 *local_270;
  undefined1 local_268 [72];
  undefined8 *******local_220;
  undefined8 local_218;
  undefined7 local_210;
  char cStack_209;
  long *******local_1d0;
  undefined8 local_1c8;
  undefined7 local_1c0;
  char cStack_1b9;
  long local_180 [3];
  long *local_168;
  long *******local_f0;
  undefined8 *******pppppppuStack_e8;
  undefined1 **ppuStack_e0;
  undefined4 **local_d8;
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
  undefined8 uStack_80;
  undefined8 local_78;
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_09b36c98;
  if (*(long *)(param_2 + 0x18) == 0) {
    uVar14 = 1;
    goto LAB_03aef2c0;
  }
  uVar13 = (**(code **)(*param_1 + 0x10))();
  if ((uVar13 & 1) == 0) {
    iVar12 = thunk_FUN_05e1d97c(4);
    if (iVar12 != 0) {
      FUN_0488143c(&local_1d0);
      ppppppplVar2 = local_1d0;
      if (-1 < cStack_1b9) {
        ppppppplVar2 = (long *******)&local_1d0;
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
      if ((DAT_0a41c1f8 & 1) == 0) {
        _DAT_0a41c1dc = CONCAT44((int)DAT_08839968,(int)DAT_0870c398);
        uRam000000000a41c1e4 = CONCAT44((int)DAT_0883d870,(int)DAT_088cf620);
        DAT_0a41c1ec = CONCAT44((int)DAT_08964678,(int)DAT_08674c40);
        DAT_0a41c1f4 = (undefined4)ram0x084e7748;
        DAT_0a41c1f8 = 1;
      }
      FUN_05e1d050(local_180,4,ppppppplVar2,&DAT_0a41be70,&DAT_0a41c1dc,0x13d,0,0);
      if ((DAT_0a41c1bd & 1) == 0) {
        _DAT_0a41c198 = CONCAT44((int)DAT_08839950,(int)ram0x08489fc8);
        uRam000000000a41c1a0 = CONCAT44((int)DAT_088546b0,(int)DAT_084abe58);
        _DAT_0a41c1a8 = CONCAT44((int)DAT_08567f28,(int)DAT_08554238);
        uRam000000000a41c1b0 = CONCAT44((int)DAT_08545158,(int)DAT_084d4a68);
        DAT_0a41c1b8 = (undefined4)ram0x08480938;
        DAT_0a41c1bc = 0;
        DAT_0a41c1bd = 1;
      }
      local_88 = 0;
      uStack_90 = 0;
      local_78 = 0;
      uStack_80 = 0;
      local_a8 = 0;
      uStack_b0 = 0;
      local_98 = 0;
      uStack_a0 = 0;
      local_c8 = 0;
      uStack_d0 = 0;
      local_b8 = 0;
      uStack_c0 = 0;
      pppppppuStack_e8 = (undefined8 *******)0x0;
      local_f0 = (long *******)0x0;
      local_d8 = (undefined4 **)0x0;
      ppuStack_e0 = (undefined1 **)0x0;
      FUN_05e1d31c(local_180,&DAT_0a41c198,&local_f0);
      thunk_FUN_05e1d0bc(local_180);
      if (cStack_1b9 < '\0') {
        __ZdlPvm(local_1d0,CONCAT17(cStack_1b9,local_1c0) & 0x7fffffffffffffff);
      }
    }
    uVar14 = 0;
    goto LAB_03aef2c0;
  }
  local_2d8 = (long *)0x0;
  local_2d0 = (long *)0x0;
  local_2c8 = (long *)0x0;
  FUN_0039488c(&local_2d8,*(undefined8 *)(param_2 + 0x18));
  uVar7 = s_base_storage_cc_08964550._8_8_;
  uVar5 = s_base_storage_cc_08964550._0_8_;
  uVar14 = ram0x084e7748;
  plVar20 = *(long **)(param_2 + 0x10);
  if (plVar20 != (long *)0x0) {
    uVar21 = (undefined4)DAT_084d1008;
    uVar29 = (undefined4)DAT_085a9068;
    uVar33 = (undefined4)DAT_084d00a0;
    uVar22 = (undefined4)DAT_08850810;
    uVar23 = (undefined4)DAT_084c9870;
    uVar30 = (undefined4)DAT_084ca398;
    uVar24 = (undefined4)DAT_08839968;
    uVar31 = (undefined4)DAT_0870c398;
    uVar34 = (undefined4)DAT_088cf620;
    uVar25 = (undefined4)DAT_0883d870;
    uVar26 = (undefined4)DAT_08964678;
    uVar32 = (undefined4)DAT_08674c40;
    do {
      while( true ) {
        ppppppplVar2 = (long *******)(plVar20 + 2);
        iVar12 = FUN_04bb2ea4(ppppppplVar2);
        plVar9 = local_2d0;
        if (iVar12 == 0) break;
        iVar12 = thunk_FUN_05e1d97c(3);
        if (iVar12 != 0) {
          FUN_0488143c(&local_220);
          uVar8 = s_base_storage_cc_08964550._8_8_;
          uVar6 = s_base_storage_cc_08964550._0_8_;
          pppppppuVar1 = local_220;
          if (-1 < cStack_209) {
            pppppppuVar1 = &local_220;
          }
          if ((DAT_0a41be80 & 1) == 0) {
            s_base_storage_cc_08964550[8] = (char)uVar7;
            s_base_storage_cc_08964550[9] = SUB81(uVar7,1);
            s_base_storage_cc_08964550[10] = SUB81(uVar7,2);
            s_base_storage_cc_08964550[0xb] = SUB81(uVar7,3);
            s_base_storage_cc_08964550[0xc] = SUB81(uVar7,4);
            s_base_storage_cc_08964550[0xd] = SUB81(uVar7,5);
            s_base_storage_cc_08964550[0xe] = SUB81(uVar7,6);
            s_base_storage_cc_08964550[0xf] = SUB81(uVar7,7);
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
          if ((DAT_0a41c1f8 & 1) == 0) {
            DAT_0a41c1f4 = (undefined4)uVar14;
            DAT_0a41c1f8 = 1;
            _DAT_0a41c1dc = CONCAT44(uVar24,uVar31);
            uRam000000000a41c1e4 = CONCAT44(uVar25,uVar34);
            DAT_0a41c1ec = CONCAT44(uVar26,uVar32);
          }
          s_base_storage_cc_08964550._0_8_ = uVar6;
          s_base_storage_cc_08964550._8_8_ = uVar8;
          FUN_05e1d050(local_180,3,pppppppuVar1,&DAT_0a41be70,&DAT_0a41c1dc,0x145,0,0);
          local_1d0 = (long *******)plVar20[2];
          if (-1 < *(char *)((long)plVar20 + 0x27)) {
            local_1d0 = ppppppplVar2;
          }
          local_1c8._0_1_ = 0;
          if ((DAT_0a41c1db & 1) == 0) {
            DAT_0a41c1d8 = 0x5f25;
            DAT_0a41c1da = 0;
            DAT_0a41c1db = 1;
            _DAT_0a41c1c0 = CONCAT44(uVar21,uVar29);
            uRam000000000a41c1c8 = CONCAT44(uVar22,uVar33);
            DAT_0a41c1d0 = CONCAT44(uVar23,uVar30);
          }
          local_f0 = (long *******)&local_1d0;
          ppuStack_e0 = (undefined1 **)0x0;
          pppppppuStack_e8 = (undefined8 *******)0x0;
          uStack_d0 = 0;
          local_d8 = (undefined4 **)0x0;
          uStack_c0 = 0;
          local_c8 = 0;
          uStack_b0 = 0;
          local_b8 = 0;
          uStack_a0 = 0;
          local_a8 = 0;
          uStack_90 = 0;
          local_98 = 0;
          uStack_80 = 0;
          local_88 = 0;
          local_78 = 0;
          FUN_05e1d31c(local_180,&DAT_0a41c1c0,&local_f0);
          thunk_FUN_05e1d0bc(local_180);
          if (cStack_209 < '\0') {
            __ZdlPvm(local_220,CONCAT17(cStack_209,local_210) & 0x7fffffffffffffff);
          }
        }
        local_180[0]._0_4_ = 0;
        FUN_03af667c(param_3,ppppppplVar2,ppppppplVar2,local_180);
        plVar20 = (long *)*plVar20;
        if (plVar20 == (long *)0x0) goto LAB_03aeeb8c;
      }
      if (local_2d0 < local_2c8) {
        if (*(char *)((long)plVar20 + 0x27) < '\0') {
          FUN_00018d20(local_2d0,plVar20[2],plVar20[3]);
        }
        else {
          lVar28 = plVar20[3];
          pppppplVar27 = *ppppppplVar2;
          local_2d0[2] = plVar20[4];
          local_2d0[1] = lVar28;
          *local_2d0 = (long)pppppplVar27;
        }
        local_2d0 = plVar9 + 3;
      }
      else {
        local_2d0 = (long *)FUN_0002df44(&local_2d8,ppppppplVar2);
      }
      plVar20 = (long *)*plVar20;
    } while (plVar20 != (long *)0x0);
  }
LAB_03aeeb8c:
  local_168 = (long *)__Znwm(0x20);
  *local_168 = (long)&PTR_FUN_09e22a98;
  local_168[1] = (long)&local_2d8;
  local_168[2] = (long)param_1;
  local_168[3] = param_3;
  uVar14 = FUN_03aeddb4(param_1,local_180);
  if (local_168 == local_180) {
    pcVar15 = *(code **)(*local_168 + 0x20);
LAB_03aeeda8:
    (*pcVar15)();
  }
  else if (local_168 != (long *)0x0) {
    pcVar15 = *(code **)(*local_168 + 0x28);
    goto LAB_03aeeda8;
  }
  iVar12 = thunk_FUN_05e1d97c(2);
  if (iVar12 != 0) {
    FUN_0488143c(local_2f0);
    pppppppuVar1 = local_2f0[0];
    if (-1 < cStack_2d9) {
      pppppppuVar1 = local_2f0;
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
    if ((DAT_0a41c1f8 & 1) == 0) {
      _DAT_0a41c1dc = CONCAT44((int)DAT_08839968,(int)DAT_0870c398);
      uRam000000000a41c1e4 = CONCAT44((int)DAT_0883d870,(int)DAT_088cf620);
      DAT_0a41c1ec = CONCAT44((int)DAT_08964678,(int)DAT_08674c40);
      DAT_0a41c1f4 = (undefined4)ram0x084e7748;
      DAT_0a41c1f8 = 1;
    }
    FUN_05e1d050(local_180,2,pppppppuVar1,&DAT_0a41be70,&DAT_0a41c1dc,0x195,0,0);
    uVar13 = *(ulong *)(param_3 + 0x18);
    local_1d0 = (long *******)0x0;
    if ((DAT_0a41c597 & 1) == 0) {
      uVar19 = 0;
      do {
        uVar33 = *(undefined4 *)((long)&DAT_08965616 + uVar19);
        uVar4 = CONCAT12((char)((uint)uVar33 >> 8),(short)uVar33) & 0xff00ff;
        uVar34 = *(undefined4 *)((long)&DAT_08965602 + uVar19 % 0x14);
        *(uint *)((long)&DAT_0a41c54f + uVar19) =
             CONCAT13((char)((uint)uVar33 >> 0x18) + 0x8aU ^ (byte)((uint)uVar34 >> 0x18),
                      CONCAT12((char)((uint)uVar33 >> 0x10) + 0x8aU ^ (byte)((uint)uVar34 >> 0x10),
                               CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^ (byte)((uint)uVar34 >> 8),
                                        (char)uVar4 + 0x8aU ^ (byte)uVar34)));
        uVar19 = uVar19 + 4;
      } while (uVar19 != 0x48);
      DAT_0a41c597 = 1;
    }
    lVar28 = 0;
    do {
      lVar18 = lVar28;
      *(undefined1 *)((long)&local_1c8 + lVar18) = (&DAT_0a41c572)[uVar13 % 10];
      bVar10 = 9 < uVar13;
      uVar13 = uVar13 / 10;
      lVar28 = lVar18 + 1;
    } while (bVar10);
    *(undefined1 *)((long)&local_1c8 + lVar18 + 1) = 0;
    if (8 < lVar18 + 8U) {
      puVar17 = (undefined1 *)((long)&local_1c8 + lVar18);
      puVar11 = (undefined1 *)((long)&local_1c8 + 1);
      do {
        uVar3 = *puVar17;
        *puVar17 = puVar11[-1];
        puVar11[-1] = uVar3;
        bVar10 = puVar11 < puVar17 + -1;
        puVar17 = puVar17 + -1;
        puVar11 = puVar11 + 1;
      } while (bVar10);
    }
    local_1d0 = (long *******)&local_1c8;
    local_220 = (undefined8 *******)0x0;
    lVar28 = 0;
    uVar13 = *(ulong *)(param_2 + 0x18);
    do {
      lVar18 = lVar28;
      *(undefined1 *)((long)&local_218 + lVar18) = (&DAT_0a41c572)[uVar13 % 10];
      bVar10 = 9 < uVar13;
      lVar28 = lVar18 + 1;
      uVar13 = uVar13 / 10;
    } while (bVar10);
    *(undefined1 *)((long)&local_218 + lVar18 + 1) = 0;
    if (8 < lVar18 + 8U) {
      puVar17 = (undefined1 *)((long)&local_218 + lVar18);
      puVar11 = (undefined1 *)((long)&local_218 + 1);
      do {
        uVar3 = *puVar17;
        *puVar17 = puVar11[-1];
        puVar11[-1] = uVar3;
        bVar10 = puVar11 < puVar17 + -1;
        puVar17 = puVar17 + -1;
        puVar11 = puVar11 + 1;
      } while (bVar10);
    }
    local_220 = (undefined8 *******)&local_218;
    local_270 = local_268;
    lVar28 = 0;
    uVar13 = ((long)local_2d0 - (long)local_2d8 >> 3) * -0x5555555555555555;
    do {
      lVar18 = lVar28;
      local_268[lVar18] = (&DAT_0a41c572)[uVar13 % 10];
      bVar10 = 9 < uVar13;
      lVar28 = lVar18 + 1;
      uVar13 = uVar13 / 10;
    } while (bVar10);
    local_268[lVar18 + 1] = 0;
    if (8 < lVar18 + 8U) {
      puVar17 = local_268;
      puVar11 = local_268 + lVar18;
      do {
        puVar17 = puVar17 + 1;
        uVar3 = *puVar11;
        puVar16 = puVar11 + -1;
        *puVar11 = puVar17[-1];
        puVar17[-1] = uVar3;
        puVar11 = puVar16;
      } while (puVar17 < puVar16);
    }
    if ((int)uVar14 == 0) {
      local_2c0 = &DAT_0a41c548;
      if ((DAT_0a41c54e & 1) == 0) {
        DAT_0a41c548 = (undefined4)DAT_0847fe48;
        puVar11 = &DAT_0a41c54c;
        puVar17 = &DAT_0a41c54d;
        puVar16 = &DAT_0a41c54e;
        goto LAB_03aef13c;
      }
    }
    else {
      local_2c0 = (undefined4 *)&DAT_0a41c541;
      if ((DAT_0a41c546 & 1) == 0) {
        DAT_0a41c541 = 0x7274;
        DAT_0a41c543 = 0x75;
        puVar17 = &DAT_0a41c545;
        puVar11 = &DAT_0a41c544;
        puVar16 = &DAT_0a41c546;
LAB_03aef13c:
        *puVar11 = 0x65;
        *puVar17 = 0;
        *puVar16 = 1;
      }
    }
    local_2b8 = 0;
    if ((DAT_0a41c22f & 1) == 0) {
      _DAT_0a41c1fc = CONCAT44((int)ram0x08489fc8,(int)DAT_0848be60);
      uRam000000000a41c204 = CONCAT44((int)DAT_08531b60,(int)DAT_08839950);
      _DAT_0a41c20c = CONCAT44((int)DAT_084f5f40,(int)DAT_084cf930);
      uRam000000000a41c214 = CONCAT44((int)DAT_08771a40,(int)DAT_084f5f48);
      _DAT_0a41c21c = CONCAT44((int)DAT_08504b78,(int)DAT_086026d8);
      uRam000000000a41c224 = CONCAT44((int)DAT_086b5ed0,(int)DAT_0875d370);
      DAT_0a41c22c = 0x5f25;
      DAT_0a41c22e = 0;
      DAT_0a41c22f = 1;
    }
    local_f0 = (long *******)&local_1d0;
    pppppppuStack_e8 = &local_220;
    ppuStack_e0 = &local_270;
    local_d8 = &local_2c0;
    local_c8 = 0;
    uStack_d0 = 0;
    local_b8 = 0;
    uStack_c0 = 0;
    local_a8 = 0;
    uStack_b0 = 0;
    local_98 = 0;
    uStack_a0 = 0;
    local_88 = 0;
    uStack_90 = 0;
    local_78 = 0;
    uStack_80 = 0;
    FUN_05e1d31c(local_180,&DAT_0a41c1fc,&local_f0);
    thunk_FUN_05e1d0bc(local_180);
    if (cStack_2d9 < '\0') {
      __ZdlPvm(local_2f0[0],CONCAT17(cStack_2d9,local_2e0) & 0x7fffffffffffffff);
    }
  }
  if (local_2d8 != (long *)0x0) {
    for (; local_2d0 != local_2d8; local_2d0 = local_2d0 + -3) {
    }
    local_2d0 = local_2d8;
    __ZdlPvm(local_2d8,(long)local_2c8 - (long)local_2d8);
  }
LAB_03aef2c0:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_70) {
    return uVar14;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


