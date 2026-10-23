// Ghidra inferred pseudocode; requested=0x32cf5e8
// entry=032cf5e8 end=032d0b57

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_032cf5e8(undefined8 *param_1,undefined8 param_2,long param_3,long *******param_4,
                 undefined1 param_5,int param_6)

{
  long *******ppppppplVar1;
  undefined8 *******pppppppuVar2;
  undefined1 uVar3;
  char cVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  long *******ppppppplVar7;
  bool bVar8;
  long ******pppppplVar9;
  undefined1 *puVar10;
  long ******pppppplVar11;
  int iVar12;
  undefined8 uVar13;
  ulong uVar14;
  long *******ppppppplVar15;
  char *pcVar16;
  undefined1 *puVar17;
  ulong uVar18;
  long lVar19;
  long lVar20;
  undefined1 *puVar21;
  int iVar22;
  uint uVar23;
  undefined1 auStack_5c8 [632];
  long ******local_350;
  long ******pppppplStack_348;
  long ******local_340;
  undefined1 local_338;
  long *******local_330;
  long *******local_328;
  long ******local_320;
  long ******local_318;
  long ******pppppplStack_310;
  long ******local_308;
  long *******local_300;
  long *******local_2f8;
  long *******local_2f0;
  long *******local_2e8;
  undefined7 local_2e0;
  char cStack_2d9;
  long *******local_2d8 [2];
  undefined7 local_2c8;
  char cStack_2c1;
  long *******local_2c0;
  long *******local_2b8;
  undefined8 local_2b0;
  undefined8 *******local_230;
  undefined1 local_228;
  undefined7 local_220;
  char cStack_219;
  undefined1 uStack_1e1;
  undefined8 local_1e0;
  undefined8 local_1d8;
  undefined7 local_1d0;
  char cStack_1c9;
  long *******local_190;
  undefined8 local_188;
  undefined7 local_180;
  char cStack_179;
  undefined1 uStack_141;
  undefined8 local_140;
  undefined8 local_138;
  long *******local_f0;
  long *******local_e8;
  undefined8 *puStack_e0;
  undefined8 *******pppppppuStack_d8;
  undefined8 local_d0;
  undefined8 uStack_c8;
  undefined8 uStack_c0;
  undefined8 uStack_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 uStack_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 uStack_80;
  undefined8 local_78;
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_09b36c98;
  pppppplVar9 = param_4[1];
  if (-1 < (char)*(byte *)((long)param_4 + 0x17)) {
    pppppplVar9 = (long ******)(ulong)*(byte *)((long)param_4 + 0x17);
  }
  if (pppppplVar9 == (long ******)0x0) {
    iVar12 = thunk_FUN_05e1d97c(4);
    if (iVar12 != 0) {
      FUN_0488143c(&local_190);
      ppppppplVar1 = local_190;
      if (-1 < cStack_179) {
        ppppppplVar1 = (long *******)&local_190;
      }
      if ((DAT_0a3e7408 & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3e73f0)[uVar14] = (&DAT_088d08e0)[uVar14] + 0x8a ^ (&DAT_088d08d0)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x18);
        DAT_0a3e7408 = 1;
      }
      if ((DAT_0a3e7681 & 1) == 0) {
        uRam000000000a3e7678._0_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x18];
        uRam000000000a3e7678._1_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x19];
        uRam000000000a3e7678._2_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1a];
        uRam000000000a3e7678._3_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1b];
        uRam000000000a3e7678._4_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1c];
        uRam000000000a3e7678._5_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1d];
        uRam000000000a3e7678._6_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1e];
        uRam000000000a3e7678._7_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1f];
        DAT_0a3e7670 = s___filter_duplicaCoAddMessageToDB_088cf290[0x10];
        DAT_0a3e7670_1._0_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x11];
        DAT_0a3e7670_1._1_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x12];
        DAT_0a3e7670_1._2_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x13];
        DAT_0a3e7670_1._3_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x14];
        DAT_0a3e7670_1._4_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x15];
        DAT_0a3e7670_1._5_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x16];
        DAT_0a3e7670_1._6_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x17];
        DAT_0a3e7680 = 0;
        DAT_0a3e7681 = 1;
      }
      FUN_05e1d050(&local_2c0,4,ppppppplVar1,&DAT_0a3e73f0,&DAT_0a3e7670,0x194,0,0);
      FUN_04cbe440(&local_1e0,param_3);
      local_140 = local_1e0;
      if (-1 < cStack_1c9) {
        local_140 = (long *******)&local_1e0;
      }
      local_138 = (long *******)((ulong)local_138 & 0xffffffffffffff00);
      if ((DAT_0a3e7697 & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3e7682)[uVar14] = (&DAT_088d0c6b)[uVar14] + 0x8a ^ (&DAT_088d0c5b)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x15);
        DAT_0a3e7697 = 1;
      }
      puStack_e0 = (undefined8 *)0x0;
      local_e8 = (long *******)0x0;
      local_f0 = (long *******)&local_140;
      local_d0 = 0;
      pppppppuStack_d8 = (undefined8 *******)0x0;
      uStack_c0 = 0;
      uStack_c8 = 0;
      local_b0 = 0;
      uStack_b8 = 0;
      uStack_a0 = 0;
      uStack_a8 = 0;
      local_90 = 0;
      uStack_98 = 0;
      uStack_80 = 0;
      uStack_88 = 0;
      local_78 = 0;
      FUN_05e1d31c(&local_2c0,&DAT_0a3e7682,&local_f0);
      if (cStack_1c9 < '\0') {
        __ZdlPvm(local_1e0,CONCAT17(cStack_1c9,local_1d0) & 0x7fffffffffffffff);
      }
      thunk_FUN_05e1d0bc(&local_2c0);
      if (cStack_179 < '\0') {
        __ZdlPvm(local_190,CONCAT17(cStack_179,local_180) & 0x7fffffffffffffff);
      }
    }
    local_2b8 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
    local_2c0 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
    FUN_021efaf0(&local_2c0,&local_f0);
    local_f0 = local_2c0;
    local_e8 = local_2b8;
    pppppplVar9 = (long ******)0x0;
    if (local_2b8 != (long *******)0x0) {
      pppppplVar9 = local_2b8[1];
      local_2b8[1] = (long ******)((long)pppppplVar9 + 1);
    }
    FUN_0335bddc(pppppplVar9,&local_f0,param_3);
    ppppppplVar1 = local_e8;
    if (local_e8 != (long *******)0x0) {
      LOAcquire();
      pppppplVar9 = local_e8[1];
      local_e8[1] = (long ******)((long)pppppplVar9 + -1);
      LORelease();
      if (pppppplVar9 == (long ******)0x0) {
        (*(code *)(*local_e8)[2])(local_e8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar1);
      }
    }
    *param_1 = local_2c0;
    param_1[1] = local_2b8;
    if (local_2b8 == (long *******)0x0) goto LAB_032d0af8;
    local_2b8[1] = (long ******)((long)local_2b8[1] + 1);
    ppppppplVar1 = local_2b8;
  }
  else {
    uVar23 = *(uint *)(param_3 + 0x114);
    FUN_0466aca8(&local_140);
    FUN_01205740(&local_f0,local_140);
    FUN_02603584(&local_2c0,local_f0);
    ppppppplVar1 = local_2c0;
    uVar13 = FUN_03289264(param_4);
    uVar14 = FUN_03bda490(ppppppplVar1,uVar13,(ulong)uVar23);
    ppppppplVar1 = local_2b8;
    if (local_2b8 != (long *******)0x0) {
      LOAcquire();
      pppppplVar9 = local_2b8[1];
      local_2b8[1] = (long ******)((long)pppppplVar9 + -1);
      LORelease();
      if (pppppplVar9 == (long ******)0x0) {
        (*(code *)(*local_2b8)[2])(local_2b8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar1);
      }
    }
    ppppppplVar1 = local_e8;
    if (local_e8 != (long *******)0x0) {
      LOAcquire();
      pppppplVar9 = local_e8[1];
      local_e8[1] = (long ******)((long)pppppplVar9 + -1);
      LORelease();
      if (pppppplVar9 == (long ******)0x0) {
        (*(code *)(*local_e8)[2])(local_e8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar1);
      }
    }
    ppppppplVar1 = local_138;
    if (local_138 != (long *******)0x0) {
      LOAcquire();
      pppppplVar9 = local_138[1];
      local_138[1] = (long ******)((long)pppppplVar9 + -1);
      LORelease();
      if (pppppplVar9 == (long ******)0x0) {
        (*(code *)(*local_138)[2])(local_138);
        __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar1);
      }
    }
    iVar12 = thunk_FUN_05e1d97c(2);
    iVar22 = (int)uVar14;
    if (iVar12 != 0) {
      FUN_0488143c(local_2d8);
      ppppppplVar1 = local_2d8[0];
      if (-1 < cStack_2c1) {
        ppppppplVar1 = (long *******)local_2d8;
      }
      if ((DAT_0a3e7408 & 1) == 0) {
        uVar18 = 0;
        do {
          (&DAT_0a3e73f0)[uVar18] = (&DAT_088d08e0)[uVar18] + 0x8a ^ (&DAT_088d08d0)[uVar18 & 0xf];
          uVar18 = uVar18 + 1;
        } while (uVar18 != 0x18);
        DAT_0a3e7408 = 1;
      }
      if ((DAT_0a3e7681 & 1) == 0) {
        uRam000000000a3e7678._0_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x18];
        uRam000000000a3e7678._1_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x19];
        uRam000000000a3e7678._2_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1a];
        uRam000000000a3e7678._3_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1b];
        uRam000000000a3e7678._4_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1c];
        uRam000000000a3e7678._5_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1d];
        uRam000000000a3e7678._6_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1e];
        uRam000000000a3e7678._7_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1f];
        DAT_0a3e7670 = s___filter_duplicaCoAddMessageToDB_088cf290[0x10];
        DAT_0a3e7670_1._0_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x11];
        DAT_0a3e7670_1._1_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x12];
        DAT_0a3e7670_1._2_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x13];
        DAT_0a3e7670_1._3_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x14];
        DAT_0a3e7670_1._4_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x15];
        DAT_0a3e7670_1._5_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x16];
        DAT_0a3e7670_1._6_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x17];
        DAT_0a3e7680 = 0;
        DAT_0a3e7681 = 1;
      }
      FUN_05e1d050(&local_2c0,2,ppppppplVar1,&DAT_0a3e73f0,&DAT_0a3e7670,0x19f,0,0);
      FUN_04cbde70(&local_2f0,param_3);
      local_140 = local_2f0;
      if (-1 < cStack_2d9) {
        local_140 = (long *******)&local_2f0;
      }
      local_138 = (long *******)((ulong)local_138 & 0xffffffffffffff00);
      local_190 = (long *******)0x0;
      if ((DAT_0a3ea7a2 & 1) == 0) {
        uVar18 = 0;
        do {
          uVar5 = *(undefined4 *)((long)&DAT_088d5f33 + uVar18);
          uVar6 = *(undefined4 *)((long)&DAT_088d5f1f + uVar18 % 0x14);
          *(uint *)((long)&DAT_0a3ea75a + uVar18) =
               CONCAT13((char)((uint)uVar5 >> 0x18) + 0x69U ^ (byte)((uint)uVar6 >> 0x18),
                        CONCAT12((char)((uint)uVar5 >> 0x10) + 0x69U ^ (byte)((uint)uVar6 >> 0x10),
                                 CONCAT11((char)((uint)uVar5 >> 8) + 0x69U ^
                                          (byte)((uint)uVar6 >> 8),(char)uVar5 + 0x69U ^ (byte)uVar6
                                         )));
          uVar18 = uVar18 + 4;
        } while (uVar18 != 0x48);
        DAT_0a3ea7a2 = 1;
      }
      lVar20 = 0;
      uVar18 = (ulong)uVar23;
      do {
        lVar19 = lVar20;
        uVar23 = (uint)uVar18;
        *(undefined1 *)((long)&local_188 + lVar19) =
             *(undefined1 *)
              ((long)&DAT_0a3ea75a + (ulong)(uVar23 + (int)(uVar18 / 10) * -10 + 0x23));
        lVar20 = lVar19 + 1;
        uVar18 = uVar18 / 10;
      } while (9 < uVar23);
      *(undefined1 *)((long)&local_188 + lVar19 + 1) = 0;
      if (8 < lVar19 + 8U) {
        puVar17 = (undefined1 *)((long)&local_188 + lVar19);
        puVar10 = (undefined1 *)((long)&local_188 + 1);
        do {
          uVar3 = *puVar17;
          *puVar17 = puVar10[-1];
          puVar10[-1] = uVar3;
          bVar8 = puVar10 < puVar17 + -1;
          puVar17 = puVar17 + -1;
          puVar10 = puVar10 + 1;
        } while (bVar8);
      }
      local_190 = (long *******)&local_188;
      local_1e0 = (long *******)0x0;
      lVar20 = 8;
      uVar18 = uVar14;
      do {
        lVar19 = lVar20;
        iVar12 = (int)uVar18;
        uVar18 = (ulong)(uint)(iVar12 / 10);
        *(undefined1 *)((long)&local_1e0 + lVar19) =
             *(undefined1 *)((long)&DAT_0a3ea75a + (long)(iVar12 % 10 + 0x23));
        lVar20 = lVar19 + 1;
      } while (0x12 < iVar12 + 9U);
      if (iVar22 < 0) {
        *(undefined1 *)((long)&local_1e0 + lVar19 + 1) = 0x2d;
        lVar20 = lVar19 + 2;
      }
      *(undefined1 *)((long)&local_1e0 + lVar20) = 0;
      if (9 < lVar20) {
        puVar17 = &uStack_1e1 + lVar20;
        puVar10 = (undefined1 *)((long)&local_1d8 + 1);
        do {
          uVar3 = *puVar17;
          *puVar17 = puVar10[-1];
          puVar10[-1] = uVar3;
          bVar8 = puVar10 < puVar17 + -1;
          puVar17 = puVar17 + -1;
          puVar10 = puVar10 + 1;
        } while (bVar8);
      }
      if (param_6 == 0) {
        local_230 = (undefined8 *******)&DAT_0a3eae8c;
        if ((DAT_0a3eae92 & 1) == 0) {
          DAT_0a3eae8c = (undefined4)DAT_0847fe48;
          puVar10 = &DAT_0a3eae90;
          puVar17 = &DAT_0a3eae91;
          puVar21 = &DAT_0a3eae92;
          goto LAB_032cfc80;
        }
      }
      else {
        local_230 = (undefined8 *******)&DAT_0a3eae84;
        if ((DAT_0a3eae89 & 1) == 0) {
          DAT_0a3eae84._0_2_ = 0x7274;
          DAT_0a3eae84._2_1_ = 0x75;
          puVar17 = &DAT_0a3eae88;
          puVar10 = (undefined1 *)((long)&DAT_0a3eae84 + 3);
          puVar21 = &DAT_0a3eae89;
LAB_032cfc80:
          *puVar10 = 0x65;
          *puVar17 = 0;
          *puVar21 = 1;
        }
      }
      local_228 = 0;
      if ((DAT_0a3e76e0 & 1) == 0) {
        uVar18 = 0;
        do {
          (&DAT_0a3e7698)[uVar18] = (&DAT_088d0c90)[uVar18] + 0x8a ^ (&DAT_088d0c80)[uVar18 & 0xf];
          uVar18 = uVar18 + 1;
        } while (uVar18 != 0x48);
        DAT_0a3e76e0 = 1;
      }
      local_f0 = (long *******)&local_140;
      local_e8 = (long *******)&local_190;
      puStack_e0 = &local_1e0;
      pppppppuStack_d8 = &local_230;
      uStack_c8 = 0;
      local_d0 = 0;
      uStack_b8 = 0;
      uStack_c0 = 0;
      uStack_a8 = 0;
      local_b0 = 0;
      uStack_98 = 0;
      uStack_a0 = 0;
      uStack_88 = 0;
      local_90 = 0;
      local_78 = 0;
      uStack_80 = 0;
      local_1e0 = (long *******)&local_1d8;
      FUN_05e1d31c(&local_2c0,&DAT_0a3e7698,&local_f0);
      if (cStack_2d9 < '\0') {
        __ZdlPvm(local_2f0,CONCAT17(cStack_2d9,local_2e0) & 0x7fffffffffffffff);
      }
      thunk_FUN_05e1d0bc(&local_2c0);
      if (cStack_2c1 < '\0') {
        __ZdlPvm(local_2d8[0],CONCAT17(cStack_2c1,local_2c8) & 0x7fffffffffffffff);
      }
    }
    local_2e8 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
    local_2f0 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
    FUN_0466aca8(&local_140);
    FUN_01205740(&local_f0,local_140);
    FUN_02603584(&local_2c0,local_f0);
    ppppppplVar1 = local_2c0;
    uVar13 = FUN_03289264(param_4);
    FUN_03bda4e8(&local_2f0,ppppppplVar1,uVar13,uVar14);
    ppppppplVar1 = local_2b8;
    if (local_2b8 != (long *******)0x0) {
      LOAcquire();
      pppppplVar9 = local_2b8[1];
      local_2b8[1] = (long ******)((long)pppppplVar9 + -1);
      LORelease();
      if (pppppplVar9 == (long ******)0x0) {
        (*(code *)(*local_2b8)[2])(local_2b8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar1);
      }
    }
    ppppppplVar1 = local_e8;
    if (local_e8 != (long *******)0x0) {
      LOAcquire();
      pppppplVar9 = local_e8[1];
      local_e8[1] = (long ******)((long)pppppplVar9 + -1);
      LORelease();
      if (pppppplVar9 == (long ******)0x0) {
        (*(code *)(*ppppppplVar1)[2])(ppppppplVar1);
        __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar1);
      }
    }
    ppppppplVar1 = local_138;
    if (local_138 == (long *******)0x0) {
LAB_032cfe28:
      if (local_2f0 != (long *******)0x0) goto LAB_032cfe30;
LAB_032cfe88:
      iVar12 = thunk_FUN_05e1d97c(4);
      if (iVar12 != 0) {
        FUN_0488143c(&local_190);
        ppppppplVar1 = local_190;
        if (-1 < cStack_179) {
          ppppppplVar1 = (long *******)&local_190;
        }
        if ((DAT_0a3e7408 & 1) == 0) {
          uVar18 = 0;
          do {
            (&DAT_0a3e73f0)[uVar18] = (&DAT_088d08e0)[uVar18] + 0x8a ^ (&DAT_088d08d0)[uVar18 & 0xf]
            ;
            uVar18 = uVar18 + 1;
          } while (uVar18 != 0x18);
          DAT_0a3e7408 = 1;
        }
        if ((DAT_0a3e7681 & 1) == 0) {
          uRam000000000a3e7678._0_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x18];
          uRam000000000a3e7678._1_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x19];
          uRam000000000a3e7678._2_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1a];
          uRam000000000a3e7678._3_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1b];
          uRam000000000a3e7678._4_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1c];
          uRam000000000a3e7678._5_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1d];
          uRam000000000a3e7678._6_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1e];
          uRam000000000a3e7678._7_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1f];
          DAT_0a3e7670 = s___filter_duplicaCoAddMessageToDB_088cf290[0x10];
          DAT_0a3e7670_1._0_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x11];
          DAT_0a3e7670_1._1_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x12];
          DAT_0a3e7670_1._2_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x13];
          DAT_0a3e7670_1._3_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x14];
          DAT_0a3e7670_1._4_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x15];
          DAT_0a3e7670_1._5_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x16];
          DAT_0a3e7670_1._6_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x17];
          DAT_0a3e7680 = 0;
          DAT_0a3e7681 = 1;
        }
        FUN_05e1d050(&local_2c0,4,ppppppplVar1,&DAT_0a3e73f0,&DAT_0a3e7670,0x1a4,0,0);
        local_140 = (long *******)0x0;
        if ((DAT_0a3ea7a2 & 1) == 0) {
          uVar18 = 0;
          do {
            uVar5 = *(undefined4 *)((long)&DAT_088d5f33 + uVar18);
            uVar6 = *(undefined4 *)((long)&DAT_088d5f1f + uVar18 % 0x14);
            *(uint *)((long)&DAT_0a3ea75a + uVar18) =
                 CONCAT13((char)((uint)uVar5 >> 0x18) + 0x69U ^ (byte)((uint)uVar6 >> 0x18),
                          CONCAT12((char)((uint)uVar5 >> 0x10) + 0x69U ^ (byte)((uint)uVar6 >> 0x10)
                                   ,CONCAT11((char)((uint)uVar5 >> 8) + 0x69U ^
                                             (byte)((uint)uVar6 >> 8),
                                             (char)uVar5 + 0x69U ^ (byte)uVar6)));
            uVar18 = uVar18 + 4;
          } while (uVar18 != 0x48);
          DAT_0a3ea7a2 = 1;
        }
        lVar20 = 8;
        do {
          lVar19 = lVar20;
          iVar12 = (int)uVar14;
          uVar14 = (ulong)(uint)(iVar12 / 10);
          *(undefined1 *)((long)&local_140 + lVar19) =
               *(undefined1 *)((long)&DAT_0a3ea75a + (long)(iVar12 % 10 + 0x23));
          lVar20 = lVar19 + 1;
        } while (0x12 < iVar12 + 9U);
        if (iVar22 < 0) {
          *(undefined1 *)((long)&local_140 + lVar19 + 1) = 0x2d;
          lVar20 = lVar19 + 2;
        }
        *(undefined1 *)((long)&local_140 + lVar20) = 0;
        if (9 < lVar20) {
          puVar17 = &uStack_141 + lVar20;
          puVar10 = (undefined1 *)((long)&local_138 + 1);
          do {
            uVar3 = *puVar17;
            *puVar17 = puVar10[-1];
            puVar10[-1] = uVar3;
            bVar8 = puVar10 < puVar17 + -1;
            puVar17 = puVar17 + -1;
            puVar10 = puVar10 + 1;
          } while (bVar8);
        }
        if ((DAT_0a3e7704 & 1) == 0) {
          uVar14 = 0;
          do {
            (&DAT_0a3e76e1)[uVar14] = (&DAT_088d0ce8)[uVar14] + 0x8a ^ (&DAT_088d0cd8)[uVar14 & 0xf]
            ;
            uVar14 = uVar14 + 1;
          } while (uVar14 != 0x23);
          DAT_0a3e7704 = 1;
        }
        puStack_e0 = (undefined8 *)0x0;
        local_e8 = (long *******)0x0;
        local_f0 = (long *******)&local_140;
        local_d0 = 0;
        pppppppuStack_d8 = (undefined8 *******)0x0;
        uStack_c0 = 0;
        uStack_c8 = 0;
        local_b0 = 0;
        uStack_b8 = 0;
        uStack_a0 = 0;
        uStack_a8 = 0;
        local_90 = 0;
        uStack_98 = 0;
        uStack_80 = 0;
        uStack_88 = 0;
        local_78 = 0;
        local_140 = (long *******)&local_138;
        FUN_05e1d31c(&local_2c0,&DAT_0a3e76e1,&local_f0);
        thunk_FUN_05e1d0bc(&local_2c0);
        if (cStack_179 < '\0') {
          __ZdlPvm(local_190,CONCAT17(cStack_179,local_180) & 0x7fffffffffffffff);
        }
      }
      local_2b8 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
      local_2c0 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
      FUN_021efaf0(&local_2c0,&local_f0);
      local_f0 = local_2c0;
      local_e8 = local_2b8;
      pppppplVar9 = (long ******)0x0;
      if (local_2b8 != (long *******)0x0) {
        pppppplVar9 = local_2b8[1];
        local_2b8[1] = (long ******)((long)pppppplVar9 + 1);
      }
      FUN_0335bddc(pppppplVar9,&local_f0,param_3);
LAB_032d0798:
      ppppppplVar1 = local_e8;
      if (local_e8 != (long *******)0x0) {
        LOAcquire();
        pppppplVar9 = local_e8[1];
        local_e8[1] = (long ******)((long)pppppplVar9 + -1);
        LORelease();
        if (pppppplVar9 == (long ******)0x0) {
          (*(code *)(*local_e8)[2])(local_e8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar1);
        }
      }
      ppppppplVar7 = local_2b8;
      *param_1 = local_2c0;
      param_1[1] = local_2b8;
      ppppppplVar1 = local_2e8;
      if ((local_2b8 != (long *******)0x0) &&
         (local_2b8[1] = (long ******)((long)local_2b8[1] + 1), local_2b8 != (long *******)0x0)) {
        LOAcquire();
        pppppplVar9 = local_2b8[1];
        local_2b8[1] = (long ******)((long)pppppplVar9 + -1);
        LORelease();
        if (pppppplVar9 == (long ******)0x0) {
          (*(code *)(*local_2b8)[2])(local_2b8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar7);
          ppppppplVar1 = local_2e8;
        }
      }
    }
    else {
      LOAcquire();
      pppppplVar9 = local_138[1];
      local_138[1] = (long ******)((long)pppppplVar9 + -1);
      LORelease();
      if (pppppplVar9 != (long ******)0x0) goto LAB_032cfe28;
      (*(code *)(*local_138)[2])(local_138);
      __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar1);
      if (local_2f0 == (long *******)0x0) goto LAB_032cfe88;
LAB_032cfe30:
      pppppplVar9 = *(long *******)(param_3 + 0xf8);
      if ((pppppplVar9 != (long ******)0x0) && (param_6 != 0)) {
        local_320 = pppppplVar9;
        if (*(char *)((long)param_4 + 0x17) < '\0') {
          FUN_00018d20(&local_318,*param_4,param_4[1]);
        }
        else {
          pppppplStack_310 = param_4[1];
          local_318 = *param_4;
          local_308 = param_4[2];
        }
        local_2f8 = local_2e8;
        if (local_2e8 != (long *******)0x0) {
          local_2e8[1] = (long ******)((long)local_2e8[1] + 1);
        }
        local_f0 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
        local_e8 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
        local_300 = local_2f0;
        FUN_021efaf0(&local_f0,&local_2c0);
        ppppppplVar7 = local_e8;
        ppppppplVar1 = local_f0;
        local_140 = local_f0;
        local_138 = local_e8;
        if (local_e8 != (long *******)0x0) {
          local_e8[1] = (long ******)((long)local_e8[1] + 1);
        }
        if ((DAT_0a3ead0b & 1) == 0) {
          DAT_0a3ead00._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
          DAT_0a3ead00._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
          DAT_0a3ead00._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
          DAT_0a3ead00._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
          DAT_0a3ead00._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
          DAT_0a3ead00._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
          DAT_0a3ead00._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
          DAT_0a3ead00._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
          DAT_0a3ead08 = 0x2928;
          DAT_0a3ead0a = 0;
          DAT_0a3ead0b = 1;
        }
        if ((DAT_0a3e7559 & 1) == 0) {
          uVar14 = 0;
          do {
            (&DAT_0a3e74ef)[uVar14] = (&DAT_088d0a59)[uVar14] + 0x8a ^ (&DAT_088d0a49)[uVar14 & 0xf]
            ;
            uVar14 = uVar14 + 1;
          } while (uVar14 != 0x6a);
          DAT_0a3e7559 = 1;
        }
        FUN_0003bb6c(&local_2c0,&DAT_0a3ead00,&DAT_0a3e74ef,0x1af);
        ppppppplVar15 = (long *******)__Znwm(0x68);
        FUN_00033c40(ppppppplVar15,FUN_0335bfac,FUN_0335c0f0);
        ppppppplVar15[5] = local_320;
        if ((long)local_308 < 0) {
          FUN_00018d20(ppppppplVar15 + 6,local_318,pppppplStack_310);
        }
        else {
          ppppppplVar15[7] = pppppplStack_310;
          ppppppplVar15[6] = local_318;
          ppppppplVar15[8] = local_308;
        }
        ppppppplVar15[9] = (long ******)local_300;
        ppppppplVar15[10] = (long ******)local_2f8;
        pppppplVar11 = (long ******)0x0;
        if (local_2f8 != (long *******)0x0) {
          pppppplVar11 = local_2f8[1];
          local_2f8[1] = (long ******)((long)pppppplVar11 + 1);
        }
        ppppppplVar15[0xb] = (long ******)ppppppplVar1;
        ppppppplVar15[0xc] = (long ******)ppppppplVar7;
        if (ppppppplVar7 != (long *******)0x0) {
          pppppplVar11 = ppppppplVar7[1];
          ppppppplVar7[1] = (long ******)((long)pppppplVar11 + 1);
        }
        local_1e0 = ppppppplVar15;
        FUN_03c17870(pppppplVar11,&local_2c0,&local_1e0);
        FUN_00033d2c(&local_1e0);
        if (ppppppplVar7 != (long *******)0x0) {
          LOAcquire();
          pppppplVar11 = ppppppplVar7[1];
          ppppppplVar7[1] = (long ******)((long)pppppplVar11 + -1);
          LORelease();
          if (pppppplVar11 == (long ******)0x0) {
            (*(code *)(*ppppppplVar7)[2])(ppppppplVar7);
            __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar7);
          }
        }
        ppppppplVar1 = local_e8;
        local_190 = local_f0;
        local_188 = local_e8;
        if ((local_e8 != (long *******)0x0) &&
           (local_e8[1] = (long ******)((long)local_e8[1] + 1), local_e8 != (long *******)0x0)) {
          LOAcquire();
          pppppplVar11 = local_e8[1];
          local_e8[1] = (long ******)((long)pppppplVar11 + -1);
          LORelease();
          if (pppppplVar11 == (long ******)0x0) {
            (*(code *)(*local_e8)[2])(local_e8);
            __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar1);
          }
        }
        local_2c0 = local_190;
        local_2b8 = local_188;
        pppppplVar11 = (long ******)0x0;
        if (local_188 != (long *******)0x0) {
          pppppplVar11 = local_188[1];
          local_188[1] = (long ******)((long)pppppplVar11 + 1);
        }
        local_2b0 = 0;
        FUN_066856fc(pppppplVar11,&local_2c0);
        pcVar16 = (char *)FUN_022d9f40(&local_2c0);
        ppppppplVar1 = local_2b8;
        cVar4 = *pcVar16;
        if (local_2b8 != (long *******)0x0) {
          LOAcquire();
          pppppplVar11 = local_2b8[1];
          local_2b8[1] = (long ******)((long)pppppplVar11 + -1);
          LORelease();
          if (pppppplVar11 == (long ******)0x0) {
            (*(code *)(*local_2b8)[2])(local_2b8);
            __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar1);
          }
        }
        ppppppplVar1 = local_188;
        if (local_188 != (long *******)0x0) {
          LOAcquire();
          pppppplVar11 = local_188[1];
          local_188[1] = (long ******)((long)pppppplVar11 + -1);
          LORelease();
          if (pppppplVar11 == (long ******)0x0) {
            (*(code *)(*local_188)[2])(local_188);
            __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar1);
          }
        }
        ppppppplVar1 = local_2f8;
        if (local_2f8 != (long *******)0x0) {
          LOAcquire();
          pppppplVar11 = local_2f8[1];
          local_2f8[1] = (long ******)((long)pppppplVar11 + -1);
          LORelease();
          if (pppppplVar11 == (long ******)0x0) {
            (*(code *)(*local_2f8)[2])(local_2f8);
            __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar1);
          }
        }
        if ((long)local_308 < 0) {
          __ZdlPvm(local_318,(ulong)local_308 & 0x7fffffffffffffff);
        }
        if (cVar4 != '\0') {
          iVar12 = thunk_FUN_05e1d97c(3);
          if (iVar12 != 0) {
            FUN_0488143c(&local_230);
            pppppppuVar2 = local_230;
            if (-1 < cStack_219) {
              pppppppuVar2 = &local_230;
            }
            if ((DAT_0a3e7408 & 1) == 0) {
              uVar14 = 0;
              do {
                (&DAT_0a3e73f0)[uVar14] =
                     (&DAT_088d08e0)[uVar14] + 0x8a ^ (&DAT_088d08d0)[uVar14 & 0xf];
                uVar14 = uVar14 + 1;
              } while (uVar14 != 0x18);
              DAT_0a3e7408 = 1;
            }
            if ((DAT_0a3e7681 & 1) == 0) {
              uRam000000000a3e7678._0_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x18];
              uRam000000000a3e7678._1_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x19];
              uRam000000000a3e7678._2_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1a];
              uRam000000000a3e7678._3_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1b];
              uRam000000000a3e7678._4_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1c];
              uRam000000000a3e7678._5_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1d];
              uRam000000000a3e7678._6_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1e];
              uRam000000000a3e7678._7_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x1f];
              DAT_0a3e7670 = s___filter_duplicaCoAddMessageToDB_088cf290[0x10];
              DAT_0a3e7670_1._0_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x11];
              DAT_0a3e7670_1._1_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x12];
              DAT_0a3e7670_1._2_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x13];
              DAT_0a3e7670_1._3_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x14];
              DAT_0a3e7670_1._4_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x15];
              DAT_0a3e7670_1._5_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x16];
              DAT_0a3e7670_1._6_1_ = s___filter_duplicaCoAddMessageToDB_088cf290[0x17];
              DAT_0a3e7680 = 0;
              DAT_0a3e7681 = 1;
            }
            FUN_05e1d050(&local_2c0,3,pppppppuVar2,&DAT_0a3e73f0,&DAT_0a3e7670,0x1b8,0,0);
            local_140 = (long *******)0x0;
            local_140 = (long *******)&local_138;
            if ((DAT_0a3ea7a2 & 1) == 0) {
              uVar14 = 0;
              do {
                uVar5 = *(undefined4 *)((long)&DAT_088d5f33 + uVar14);
                uVar6 = *(undefined4 *)((long)&DAT_088d5f1f + uVar14 % 0x14);
                *(uint *)((long)&DAT_0a3ea75a + uVar14) =
                     CONCAT13((char)((uint)uVar5 >> 0x18) + 0x69U ^ (byte)((uint)uVar6 >> 0x18),
                              CONCAT12((char)((uint)uVar5 >> 0x10) + 0x69U ^
                                       (byte)((uint)uVar6 >> 0x10),
                                       CONCAT11((char)((uint)uVar5 >> 8) + 0x69U ^
                                                (byte)((uint)uVar6 >> 8),
                                                (char)uVar5 + 0x69U ^ (byte)uVar6)));
                uVar14 = uVar14 + 4;
              } while (uVar14 != 0x48);
              DAT_0a3ea7a2 = 1;
            }
            lVar20 = 0;
            do {
              lVar19 = lVar20;
              *(undefined1 *)((long)&local_138 + lVar19) = (&DAT_0a3ea77d)[(ulong)pppppplVar9 % 10];
              bVar8 = (long ******)0x9 < pppppplVar9;
              lVar20 = lVar19 + 1;
              pppppplVar9 = (long ******)((ulong)pppppplVar9 / 10);
            } while (bVar8);
            *(undefined1 *)((long)&local_138 + lVar19 + 1) = 0;
            if (8 < lVar19 + 8U) {
              puVar17 = (undefined1 *)((long)&local_138 + lVar19);
              puVar10 = (undefined1 *)((long)&local_138 + 1);
              do {
                uVar3 = *puVar17;
                *puVar17 = puVar10[-1];
                puVar10[-1] = uVar3;
                bVar8 = puVar10 < puVar17 + -1;
                puVar17 = puVar17 + -1;
                puVar10 = puVar10 + 1;
              } while (bVar8);
            }
            local_190 = (long *******)*param_4;
            if (-1 < *(char *)((long)param_4 + 0x17)) {
              local_190 = param_4;
            }
            local_188 = (long *******)((ulong)local_188 & 0xffffffffffffff00);
            FUN_04cbe440(local_2d8,param_3);
            local_1e0 = local_2d8[0];
            if (-1 < cStack_2c1) {
              local_1e0 = (long *******)local_2d8;
            }
            local_1d8._0_1_ = 0;
            if ((DAT_0a3e7736 & 1) == 0) {
              uVar14 = 0;
              do {
                (&DAT_0a3e7705)[uVar14] =
                     (&DAT_088d0d1b)[uVar14] + 0x8a ^ (&DAT_088d0d0b)[uVar14 & 0xf];
                uVar14 = uVar14 + 1;
              } while (uVar14 != 0x31);
              DAT_0a3e7736 = 1;
            }
            local_f0 = (long *******)&local_140;
            local_e8 = (long *******)&local_190;
            puStack_e0 = &local_1e0;
            local_d0 = 0;
            pppppppuStack_d8 = (undefined8 *******)0x0;
            uStack_c0 = 0;
            uStack_c8 = 0;
            local_b0 = 0;
            uStack_b8 = 0;
            uStack_a0 = 0;
            uStack_a8 = 0;
            local_90 = 0;
            uStack_98 = 0;
            uStack_80 = 0;
            uStack_88 = 0;
            local_78 = 0;
            FUN_05e1d31c(&local_2c0,&DAT_0a3e7705,&local_f0);
            if (cStack_2c1 < '\0') {
              __ZdlPvm(local_2d8[0],CONCAT17(cStack_2c1,local_2c8) & 0x7fffffffffffffff);
            }
            thunk_FUN_05e1d0bc(&local_2c0);
            if (cStack_219 < '\0') {
              __ZdlPvm(local_230,CONCAT17(cStack_219,local_220) & 0x7fffffffffffffff);
            }
          }
          local_2b8 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
          local_2c0 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
          FUN_021efaf0(&local_2c0,&local_f0);
          local_f0 = local_2c0;
          local_e8 = local_2b8;
          pppppplVar9 = (long ******)0x0;
          if (local_2b8 != (long *******)0x0) {
            pppppplVar9 = local_2b8[1];
            local_2b8[1] = (long ******)((long)pppppplVar9 + 1);
          }
          FUN_0335bddc(pppppplVar9,&local_f0,param_3);
          goto LAB_032d0798;
        }
      }
      FUN_00f57630(auStack_5c8,param_3);
      if (*(char *)((long)param_4 + 0x17) < '\0') {
        FUN_00018d20(&local_350,*param_4,param_4[1]);
      }
      else {
        pppppplStack_348 = param_4[1];
        local_350 = *param_4;
        local_340 = param_4[2];
      }
      local_330 = local_2f0;
      local_328 = local_2e8;
      if (local_2e8 != (long *******)0x0) {
        local_2e8[1] = (long ******)((long)local_2e8[1] + 1);
      }
      local_f0 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
      local_e8 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
      local_338 = param_5;
      FUN_021efaf0(&local_f0,&local_2c0);
      ppppppplVar7 = local_e8;
      ppppppplVar1 = local_f0;
      local_140 = local_f0;
      local_138 = local_e8;
      if (local_e8 != (long *******)0x0) {
        local_e8[1] = (long ******)((long)local_e8[1] + 1);
      }
      if ((DAT_0a3ead0b & 1) == 0) {
        DAT_0a3ead00._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
        DAT_0a3ead00._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
        DAT_0a3ead00._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
        DAT_0a3ead00._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
        DAT_0a3ead00._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
        DAT_0a3ead00._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
        DAT_0a3ead00._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
        DAT_0a3ead00._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
        DAT_0a3ead08 = 0x2928;
        DAT_0a3ead0a = 0;
        DAT_0a3ead0b = 1;
      }
      if ((DAT_0a3e7559 & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3e74ef)[uVar14] = (&DAT_088d0a59)[uVar14] + 0x8a ^ (&DAT_088d0a49)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x6a);
        DAT_0a3e7559 = 1;
      }
      FUN_0003bb6c(&local_2c0,&DAT_0a3ead00,&DAT_0a3e74ef,0x1c2);
      ppppppplVar15 = (long *******)__Znwm(0x2e0);
      FUN_00033c40(ppppppplVar15,FUN_0335c1b4,FUN_0335c4ec);
      FUN_00f57630(ppppppplVar15 + 5,auStack_5c8);
      if ((long)local_340 < 0) {
        FUN_00018d20(ppppppplVar15 + 0x54,local_350,pppppplStack_348);
      }
      else {
        ppppppplVar15[0x55] = pppppplStack_348;
        ppppppplVar15[0x54] = local_350;
        ppppppplVar15[0x56] = local_340;
      }
      *(undefined1 *)(ppppppplVar15 + 0x57) = local_338;
      ppppppplVar15[0x58] = (long ******)local_330;
      ppppppplVar15[0x59] = (long ******)local_328;
      if (local_328 != (long *******)0x0) {
        local_328[1] = (long ******)((long)local_328[1] + 1);
      }
      ppppppplVar15[0x5a] = (long ******)ppppppplVar1;
      ppppppplVar15[0x5b] = (long ******)ppppppplVar7;
      if (ppppppplVar7 != (long *******)0x0) {
        ppppppplVar7[1] = (long ******)((long)ppppppplVar7[1] + 1);
      }
      local_190 = ppppppplVar15;
      uVar13 = (*(code *)local_330[0xb][2])();
      FUN_03c17954(&local_2c0,&local_190,uVar13);
      FUN_00033d2c(&local_190);
      if (ppppppplVar7 != (long *******)0x0) {
        LOAcquire();
        pppppplVar9 = ppppppplVar7[1];
        ppppppplVar7[1] = (long ******)((long)pppppplVar9 + -1);
        LORelease();
        if (pppppplVar9 == (long ******)0x0) {
          (*(code *)(*ppppppplVar7)[2])(ppppppplVar7);
          __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar7);
        }
      }
      ppppppplVar1 = local_e8;
      *param_1 = local_f0;
      param_1[1] = local_e8;
      if ((local_e8 != (long *******)0x0) &&
         (local_e8[1] = (long ******)((long)local_e8[1] + 1), local_e8 != (long *******)0x0)) {
        LOAcquire();
        pppppplVar9 = local_e8[1];
        local_e8[1] = (long ******)((long)pppppplVar9 + -1);
        LORelease();
        if (pppppplVar9 == (long ******)0x0) {
          (*(code *)(*local_e8)[2])(local_e8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar1);
        }
      }
      ppppppplVar1 = local_328;
      if (local_328 != (long *******)0x0) {
        LOAcquire();
        pppppplVar9 = local_328[1];
        local_328[1] = (long ******)((long)pppppplVar9 + -1);
        LORelease();
        if (pppppplVar9 == (long ******)0x0) {
          (*(code *)(*local_328)[2])(local_328);
          __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar1);
        }
      }
      if ((long)local_340 < 0) {
        __ZdlPvm(local_350,(ulong)local_340 & 0x7fffffffffffffff);
      }
      FUN_00ac6290(auStack_5c8);
      ppppppplVar1 = local_2e8;
    }
  }
  if (ppppppplVar1 != (long *******)0x0) {
    LOAcquire();
    pppppplVar9 = ppppppplVar1[1];
    ppppppplVar1[1] = (long ******)((long)pppppplVar9 + -1);
    LORelease();
    if (pppppplVar9 == (long ******)0x0) {
      (*(code *)(*ppppppplVar1)[2])(ppppppplVar1);
      __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar1);
    }
  }
LAB_032d0af8:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_70) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


