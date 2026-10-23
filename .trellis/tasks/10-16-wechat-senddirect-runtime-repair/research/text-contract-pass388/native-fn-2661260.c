// Ghidra inferred pseudocode; requested=0x2661260
// entry=02661260 end=02661ee3

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_02661260(long param_1)

{
  uint uVar1;
  undefined8 ****ppppuVar2;
  undefined1 uVar3;
  uint3 uVar4;
  long *plVar5;
  bool bVar6;
  long lVar7;
  int iVar8;
  ulong uVar9;
  undefined1 *puVar10;
  undefined1 *puVar11;
  long lVar12;
  ulong uVar13;
  int iVar14;
  undefined4 uVar15;
  undefined4 uVar16;
  undefined8 ***local_1e8 [2];
  undefined7 local_1d8;
  char cStack_1d1;
  undefined8 local_1d0;
  long *local_1c8;
  undefined8 ***local_140;
  undefined1 *puStack_138;
  undefined1 *local_130;
  undefined1 *puStack_128;
  undefined1 *puStack_120;
  undefined1 *puStack_118;
  undefined1 uStack_109;
  undefined8 local_108;
  undefined8 local_100;
  undefined8 *local_b8;
  long *local_b0;
  undefined8 uStack_a8;
  undefined8 uStack_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 uStack_80;
  undefined8 uStack_78;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 uStack_60;
  undefined8 uStack_58;
  undefined8 local_50;
  undefined8 uStack_48;
  undefined8 local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar7 = param_1 + 8;
  iVar8 = *(int *)(param_1 + 0x20);
  if (iVar8 < 4) {
    if (iVar8 == 1) {
      FUN_0466aca8(&local_108);
      FUN_01205740(&local_b8,local_108);
      FUN_02662244(&local_1d0,local_b8);
      FUN_0265f400(local_1d0,*(undefined4 *)(param_1 + 0x24));
      plVar5 = local_1c8;
      if (local_1c8 != (long *)0x0) {
        LOAcquire();
        lVar7 = local_1c8[1];
        local_1c8[1] = lVar7 + -1;
        LORelease();
        if (lVar7 == 0) {
          (**(code **)(*local_1c8 + 0x10))(local_1c8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
        }
      }
      plVar5 = local_b0;
      if (local_b0 != (long *)0x0) {
        LOAcquire();
        lVar7 = local_b0[1];
        local_b0[1] = lVar7 + -1;
        LORelease();
        if (lVar7 == 0) {
          (**(code **)(*local_b0 + 0x10))(local_b0);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
        }
      }
      plVar5 = local_100;
      if (local_100 != (long *)0x0) {
        LOAcquire();
        lVar7 = local_100[1];
        local_100[1] = lVar7 + -1;
        LORelease();
        if (lVar7 == 0) {
          (**(code **)(*local_100 + 0x10))(local_100);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
        }
      }
      FUN_0466aca8(&local_108);
      FUN_01205740(&local_b8,local_108);
      FUN_026620bc(&local_1d0,local_b8);
      FUN_02687278(local_1d0,*(undefined4 *)(param_1 + 0x24));
LAB_02661808:
      if (local_1c8 != (long *)0x0) {
        LOAcquire();
        lVar7 = local_1c8[1];
        local_1c8[1] = lVar7 + -1;
        LORelease();
        if (lVar7 == 0) {
          (**(code **)(*local_1c8 + 0x10))(local_1c8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_1c8);
        }
      }
      plVar5 = local_b0;
      if (local_b0 != (long *)0x0) {
        LOAcquire();
        lVar7 = local_b0[1];
        local_b0[1] = lVar7 + -1;
        LORelease();
        if (lVar7 == 0) {
          (**(code **)(*local_b0 + 0x10))(local_b0);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
        }
      }
      if (local_100 != (long *)0x0) {
        LOAcquire();
        lVar7 = local_100[1];
        local_100[1] = lVar7 + -1;
        LORelease();
        if (lVar7 == 0) {
          (**(code **)(*local_100 + 0x10))(local_100);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_100);
        }
      }
      goto LAB_02661eb4;
    }
    if (iVar8 == 2) {
      puStack_128 = &SUB_aaaaaaaaaaaaaaaa;
      local_130 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_118 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_120 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_138 = &SUB_aaaaaaaaaaaaaaaa;
      local_140 = (undefined8 ***)&SUB_aaaaaaaaaaaaaaaa;
      FUN_05607970(&local_140);
      lVar12 = *(long *)(param_1 + 8);
      uVar1 = *(uint *)(param_1 + 0x10);
      if (-1 < (char)*(byte *)(param_1 + 0x1f)) {
        lVar12 = lVar7;
        uVar1 = (uint)*(byte *)(param_1 + 0x1f);
      }
      uVar9 = FUN_05ab3ab8(&local_140,lVar12,uVar1);
      if ((uVar9 & 1) == 0) {
        iVar8 = thunk_FUN_05e1d97c(4);
        if (iVar8 != 0) {
          FUN_0488143c(local_1e8);
          ppppuVar2 = (undefined8 ****)local_1e8[0];
          if (-1 < cStack_1d1) {
            ppppuVar2 = local_1e8;
          }
          if ((DAT_0a3919ba & 1) == 0) {
            _DAT_0a3919a0 = CONCAT44((int)DAT_087e26e0,(int)DAT_087e26d8);
            uRam000000000a3919a8 = CONCAT44((int)DAT_087e26e8,(int)DAT_08545168);
            DAT_0a3919b0 = CONCAT44((int)DAT_08596728,(int)DAT_084f17a8);
            DAT_0a3919b8 = 99;
            DAT_0a3919ba = 1;
          }
          if ((DAT_0a3919cb & 1) == 0) {
            DAT_0a3919c0._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
            DAT_0a3919c0._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
            DAT_0a3919c0._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
            DAT_0a3919c0._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
            DAT_0a3919c0._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
            DAT_0a3919c0._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
            DAT_0a3919c0._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
            DAT_0a3919c0._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
            DAT_0a3919c8 = 0x2928;
            DAT_0a3919ca = 0;
            DAT_0a3919cb = 1;
          }
          FUN_05e1d050(&local_1d0,4,ppppuVar2,&DAT_0a3919a0,&DAT_0a3919c0,0x1a,0,0);
          uVar9 = *(ulong *)(param_1 + 0x10);
          if (-1 < (char)*(byte *)(param_1 + 0x1f)) {
            uVar9 = (ulong)*(byte *)(param_1 + 0x1f);
          }
          local_108 = (undefined8 *)0x0;
          local_108 = &local_100;
          if ((DAT_0a391a9b & 1) == 0) {
            uVar13 = 0;
            do {
              uVar15 = *(undefined4 *)((long)&DAT_087e2b88 + uVar13);
              uVar4 = CONCAT12((char)((uint)uVar15 >> 8),(short)uVar15) & 0xff00ff;
              uVar16 = *(undefined4 *)((long)&DAT_087e2b74 + uVar13 % 0x14);
              *(uint *)((long)&DAT_0a391a53 + uVar13) =
                   CONCAT13((char)((uint)uVar15 >> 0x18) + 0x8aU ^ (byte)((uint)uVar16 >> 0x18),
                            CONCAT12((char)((uint)uVar15 >> 0x10) + 0x8aU ^
                                     (byte)((uint)uVar16 >> 0x10),
                                     CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^
                                              (byte)((uint)uVar16 >> 8),
                                              (char)uVar4 + 0x8aU ^ (byte)uVar16)));
              uVar13 = uVar13 + 4;
            } while (uVar13 != 0x48);
            DAT_0a391a9b = 1;
          }
          lVar7 = 0;
          do {
            lVar12 = lVar7;
            *(undefined1 *)((long)&local_100 + lVar12) = *(undefined1 *)(uVar9 % 10 + 0xa391a76);
            bVar6 = 9 < uVar9;
            uVar9 = uVar9 / 10;
            lVar7 = lVar12 + 1;
          } while (bVar6);
          *(undefined1 *)((long)&local_100 + lVar12 + 1) = 0;
          if (8 < lVar12 + 8U) {
            puVar10 = (undefined1 *)((long)&local_100 + lVar12);
            puVar11 = (undefined1 *)((long)&local_100 + 1);
            do {
              uVar3 = *puVar10;
              *puVar10 = puVar11[-1];
              puVar11[-1] = uVar3;
              bVar6 = puVar11 < puVar10 + -1;
              puVar10 = puVar10 + -1;
              puVar11 = puVar11 + 1;
            } while (bVar6);
          }
          if ((DAT_0a3919f7 & 1) == 0) {
            _DAT_0a3919cc = CONCAT44((int)DAT_087e26f8,(int)DAT_087e26f0);
            uRam000000000a3919d4 = CONCAT44((int)DAT_085d7590,(int)DAT_085232e0);
            _DAT_0a3919dc = CONCAT44((int)ram0x08789fe0,(int)DAT_087e1b30);
            uRam000000000a3919e4 = CONCAT44((int)DAT_084caf60,(int)DAT_087e2700);
            DAT_0a3919ec = CONCAT44((int)DAT_087e2708,(int)DAT_084caf68);
            DAT_0a3919f4 = 0x5f25;
            DAT_0a3919f6 = 0;
            DAT_0a3919f7 = 1;
          }
          local_b8 = &local_108;
          uStack_a8 = 0;
          local_b0 = (long *)0x0;
          uStack_98 = 0;
          uStack_a0 = 0;
          uStack_88 = 0;
          local_90 = 0;
          uStack_78 = 0;
          uStack_80 = 0;
          uStack_68 = 0;
          local_70 = 0;
          uStack_58 = 0;
          uStack_60 = 0;
          uStack_48 = 0;
          local_50 = 0;
          local_40 = 0;
          FUN_05e1d31c(&local_1d0,&DAT_0a3919cc,&local_b8);
          thunk_FUN_05e1d0bc(&local_1d0);
          if (cStack_1d1 < '\0') {
            __ZdlPvm(local_1e8[0],CONCAT17(cStack_1d1,local_1d8) & 0x7fffffffffffffff);
          }
        }
      }
      else {
        FUN_0466aca8(&local_108);
        FUN_01205740(&local_b8,local_108);
        FUN_026620bc(&local_1d0,local_b8);
        FUN_02684bf0(local_1d0,&local_140);
        if (local_1c8 != (long *)0x0) {
          LOAcquire();
          lVar7 = local_1c8[1];
          local_1c8[1] = lVar7 + -1;
          LORelease();
          if (lVar7 == 0) {
            (**(code **)(*local_1c8 + 0x10))(local_1c8);
            __ZNSt3__119__shared_weak_count14__release_weakEv(local_1c8);
          }
        }
        plVar5 = local_b0;
        if (local_b0 != (long *)0x0) {
          LOAcquire();
          lVar7 = local_b0[1];
          local_b0[1] = lVar7 + -1;
          LORelease();
          if (lVar7 == 0) {
            (**(code **)(*local_b0 + 0x10))(local_b0);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
          }
        }
        if (local_100 != (long *)0x0) {
          LOAcquire();
          lVar7 = local_100[1];
          local_100[1] = lVar7 + -1;
          LORelease();
          if (lVar7 == 0) {
            (**(code **)(*local_100 + 0x10))(local_100);
            __ZNSt3__119__shared_weak_count14__release_weakEv(local_100);
          }
        }
      }
      FUN_0560d07c(&local_140);
      goto LAB_02661eb4;
    }
  }
  else {
    if (iVar8 == 4) {
      FUN_0466aca8(&local_108);
      FUN_01205740(&local_b8,local_108);
      FUN_02662244(&local_1d0,local_b8);
      FUN_0265f6f4(local_1d0,lVar7);
      goto LAB_02661808;
    }
    if (iVar8 == 5) {
      puStack_138 = &SUB_aaaaaaaaaaaaaaaa;
      local_140 = (undefined8 ***)&SUB_aaaaaaaaaaaaaaaa;
      puStack_128 = &SUB_aaaaaaaaaaaaaaaa;
      local_130 = &SUB_aaaaaaaaaaaaaaaa;
      FUN_05607928(&local_140);
      lVar12 = *(long *)(param_1 + 8);
      uVar1 = *(uint *)(param_1 + 0x10);
      if (-1 < (char)*(byte *)(param_1 + 0x1f)) {
        lVar12 = lVar7;
        uVar1 = (uint)*(byte *)(param_1 + 0x1f);
      }
      uVar9 = FUN_05ab3ab8(&local_140,lVar12,uVar1);
      if ((uVar9 & 1) == 0) {
        iVar8 = thunk_FUN_05e1d97c(4);
        if (iVar8 != 0) {
          FUN_0488143c(local_1e8);
          ppppuVar2 = (undefined8 ****)local_1e8[0];
          if (-1 < cStack_1d1) {
            ppppuVar2 = local_1e8;
          }
          if ((DAT_0a3919ba & 1) == 0) {
            _DAT_0a3919a0 = CONCAT44((int)DAT_087e26e0,(int)DAT_087e26d8);
            uRam000000000a3919a8 = CONCAT44((int)DAT_087e26e8,(int)DAT_08545168);
            DAT_0a3919b0 = CONCAT44((int)DAT_08596728,(int)DAT_084f17a8);
            DAT_0a3919b8 = 99;
            DAT_0a3919ba = 1;
          }
          if ((DAT_0a3919cb & 1) == 0) {
            DAT_0a3919c0._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
            DAT_0a3919c0._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
            DAT_0a3919c0._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
            DAT_0a3919c0._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
            DAT_0a3919c0._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
            DAT_0a3919c0._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
            DAT_0a3919c0._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
            DAT_0a3919c0._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
            DAT_0a3919c8 = 0x2928;
            DAT_0a3919ca = 0;
            DAT_0a3919cb = 1;
          }
          FUN_05e1d050(&local_1d0,4,ppppuVar2,&DAT_0a3919a0,&DAT_0a3919c0,0x30,0,0);
          uVar9 = *(ulong *)(param_1 + 0x10);
          if (-1 < (char)*(byte *)(param_1 + 0x1f)) {
            uVar9 = (ulong)*(byte *)(param_1 + 0x1f);
          }
          local_108 = (undefined8 *)0x0;
          local_108 = &local_100;
          if ((DAT_0a391a9b & 1) == 0) {
            uVar13 = 0;
            do {
              uVar15 = *(undefined4 *)((long)&DAT_087e2b88 + uVar13);
              uVar4 = CONCAT12((char)((uint)uVar15 >> 8),(short)uVar15) & 0xff00ff;
              uVar16 = *(undefined4 *)((long)&DAT_087e2b74 + uVar13 % 0x14);
              *(uint *)((long)&DAT_0a391a53 + uVar13) =
                   CONCAT13((char)((uint)uVar15 >> 0x18) + 0x8aU ^ (byte)((uint)uVar16 >> 0x18),
                            CONCAT12((char)((uint)uVar15 >> 0x10) + 0x8aU ^
                                     (byte)((uint)uVar16 >> 0x10),
                                     CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^
                                              (byte)((uint)uVar16 >> 8),
                                              (char)uVar4 + 0x8aU ^ (byte)uVar16)));
              uVar13 = uVar13 + 4;
            } while (uVar13 != 0x48);
            DAT_0a391a9b = 1;
          }
          lVar7 = 0;
          do {
            lVar12 = lVar7;
            *(undefined1 *)((long)&local_100 + lVar12) = *(undefined1 *)(uVar9 % 10 + 0xa391a76);
            bVar6 = 9 < uVar9;
            uVar9 = uVar9 / 10;
            lVar7 = lVar12 + 1;
          } while (bVar6);
          *(undefined1 *)((long)&local_100 + lVar12 + 1) = 0;
          if (8 < lVar12 + 8U) {
            puVar10 = (undefined1 *)((long)&local_100 + lVar12);
            puVar11 = (undefined1 *)((long)&local_100 + 1);
            do {
              uVar3 = *puVar10;
              *puVar10 = puVar11[-1];
              puVar11[-1] = uVar3;
              bVar6 = puVar11 < puVar10 + -1;
              puVar10 = puVar10 + -1;
              puVar11 = puVar11 + 1;
            } while (bVar6);
          }
          if ((DAT_0a391a2d & 1) == 0) {
            _DAT_0a3919f8 = CONCAT44((int)DAT_087e26f8,(int)DAT_087e26f0);
            uRam000000000a391a00 = CONCAT44((int)DAT_085d7590,(int)DAT_085232e0);
            _DAT_0a391a08 = CONCAT44((int)ram0x08789fe0,(int)DAT_087e1b30);
            uRam000000000a391a10 = CONCAT44((int)DAT_084a4ea0,(int)DAT_08660af8);
            _DAT_0a391a18 = CONCAT44((int)DAT_084d4b20,(int)DAT_08498b68);
            uRam000000000a391a20 = CONCAT44((int)DAT_08480638,(int)ram0x08480938);
            DAT_0a391a28 = (undefined4)DAT_086e5d00;
            DAT_0a391a2c = 0;
            DAT_0a391a2d = 1;
          }
          local_b8 = &local_108;
          uStack_a8 = 0;
          local_b0 = (long *)0x0;
          uStack_98 = 0;
          uStack_a0 = 0;
          uStack_88 = 0;
          local_90 = 0;
          uStack_78 = 0;
          uStack_80 = 0;
          uStack_68 = 0;
          local_70 = 0;
          uStack_58 = 0;
          uStack_60 = 0;
          uStack_48 = 0;
          local_50 = 0;
          local_40 = 0;
          FUN_05e1d31c(&local_1d0,&DAT_0a3919f8,&local_b8);
          thunk_FUN_05e1d0bc(&local_1d0);
          if (cStack_1d1 < '\0') {
            __ZdlPvm(local_1e8[0],CONCAT17(cStack_1d1,local_1d8) & 0x7fffffffffffffff);
          }
        }
      }
      else {
        FUN_04af3aa8((ulong)local_130 & 0xffffffff,puStack_138,1);
      }
      FUN_0560b724(&local_140);
      goto LAB_02661eb4;
    }
  }
  iVar8 = thunk_FUN_05e1d97c(3);
  if (iVar8 != 0) {
    FUN_0488143c(&local_140);
    ppppuVar2 = (undefined8 ****)local_140;
    if (-1 < (long)local_130) {
      ppppuVar2 = &local_140;
    }
    if ((DAT_0a3919ba & 1) == 0) {
      _DAT_0a3919a0 = CONCAT44((int)DAT_087e26e0,(int)DAT_087e26d8);
      uRam000000000a3919a8 = CONCAT44((int)DAT_087e26e8,(int)DAT_08545168);
      DAT_0a3919b0 = CONCAT44((int)DAT_08596728,(int)DAT_084f17a8);
      DAT_0a3919b8 = 99;
      DAT_0a3919ba = 1;
    }
    if ((DAT_0a3919cb & 1) == 0) {
      DAT_0a3919c0._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
      DAT_0a3919c0._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
      DAT_0a3919c0._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
      DAT_0a3919c0._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
      DAT_0a3919c0._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
      DAT_0a3919c0._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
      DAT_0a3919c0._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
      DAT_0a3919c0._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
      DAT_0a3919c8 = 0x2928;
      DAT_0a3919ca = 0;
      DAT_0a3919cb = 1;
    }
    FUN_05e1d050(&local_1d0,3,ppppuVar2,&DAT_0a3919a0,&DAT_0a3919c0,0x38,0,0);
    iVar8 = *(int *)(param_1 + 0x20);
    local_108 = (undefined8 *)0x0;
    if ((DAT_0a391a9b & 1) == 0) {
      uVar9 = 0;
      do {
        uVar15 = *(undefined4 *)((long)&DAT_087e2b88 + uVar9);
        uVar4 = CONCAT12((char)((uint)uVar15 >> 8),(short)uVar15) & 0xff00ff;
        uVar16 = *(undefined4 *)((long)&DAT_087e2b74 + uVar9 % 0x14);
        *(uint *)((long)&DAT_0a391a53 + uVar9) =
             CONCAT13((char)((uint)uVar15 >> 0x18) + 0x8aU ^ (byte)((uint)uVar16 >> 0x18),
                      CONCAT12((char)((uint)uVar15 >> 0x10) + 0x8aU ^ (byte)((uint)uVar16 >> 0x10),
                               CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^ (byte)((uint)uVar16 >> 8),
                                        (char)uVar4 + 0x8aU ^ (byte)uVar16)));
        uVar9 = uVar9 + 4;
      } while (uVar9 != 0x48);
      DAT_0a391a9b = 1;
    }
    lVar7 = 8;
    iVar14 = iVar8;
    do {
      lVar12 = lVar7;
      *(undefined1 *)((long)&local_108 + lVar12) =
           *(undefined1 *)((long)&DAT_0a391a53 + (long)(iVar14 % 10 + 0x23));
      lVar7 = lVar12 + 1;
      uVar1 = iVar14 + 9;
      iVar14 = iVar14 / 10;
    } while (0x12 < uVar1);
    if (iVar8 < 0) {
      *(undefined1 *)((long)&local_108 + lVar12 + 1) = 0x2d;
      lVar7 = lVar12 + 2;
    }
    *(undefined1 *)((long)&local_108 + lVar7) = 0;
    if (9 < lVar7) {
      puVar10 = &uStack_109 + lVar7;
      puVar11 = (undefined1 *)((long)&local_100 + 1);
      do {
        uVar3 = *puVar10;
        *puVar10 = puVar11[-1];
        puVar11[-1] = uVar3;
        bVar6 = puVar11 < puVar10 + -1;
        puVar10 = puVar10 + -1;
        puVar11 = puVar11 + 1;
      } while (bVar6);
    }
    if ((DAT_0a391a52 & 1) == 0) {
      _DAT_0a391a30 = CONCAT44((int)DAT_087e26f8,(int)DAT_087e26f0);
      uRam000000000a391a38 = CONCAT44((int)DAT_08480588,(int)DAT_0856e290);
      _DAT_0a391a40 = CONCAT44((int)DAT_084abf30,(int)DAT_08486af0);
      uRam000000000a391a48 = CONCAT44((int)DAT_08542cd8,(int)DAT_085b4648);
      DAT_0a391a50 = 0x5f;
      DAT_0a391a52 = 1;
    }
    local_b8 = &local_108;
    uStack_a8 = 0;
    local_b0 = (long *)0x0;
    uStack_98 = 0;
    uStack_a0 = 0;
    uStack_88 = 0;
    local_90 = 0;
    uStack_78 = 0;
    uStack_80 = 0;
    uStack_68 = 0;
    local_70 = 0;
    uStack_58 = 0;
    uStack_60 = 0;
    uStack_48 = 0;
    local_50 = 0;
    local_40 = 0;
    local_108 = &local_100;
    FUN_05e1d31c(&local_1d0,&DAT_0a391a30,&local_b8);
    thunk_FUN_05e1d0bc(&local_1d0);
    if ((long)local_130 < 0) {
      __ZdlPvm(local_140,(ulong)local_130 & 0x7fffffffffffffff);
    }
  }
LAB_02661eb4:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_38) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


