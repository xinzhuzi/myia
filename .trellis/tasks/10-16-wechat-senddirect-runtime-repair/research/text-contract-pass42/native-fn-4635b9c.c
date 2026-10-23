// Ghidra inferred pseudocode; requested=0x4635b9c
// entry=04635b9c end=046363df

undefined8
FUN_04635b9c(long param_1,ulong param_2,undefined8 param_3,undefined8 param_4,int param_5,
            int param_6,undefined8 param_7,undefined8 param_8)

{
  long *plVar1;
  undefined8 ******ppppppuVar2;
  undefined1 uVar3;
  bool bVar4;
  int iVar5;
  long *plVar6;
  long lVar7;
  undefined8 uVar8;
  undefined8 uVar9;
  ulong uVar10;
  long *plVar11;
  undefined8 *puVar12;
  long *plVar13;
  undefined1 *puVar14;
  undefined1 *puVar15;
  long lVar16;
  undefined1 *puVar17;
  long *plVar18;
  uint uVar19;
  long *plVar20;
  undefined8 *****local_218 [2];
  undefined7 local_208;
  char cStack_201;
  undefined8 *****local_200;
  undefined1 *puStack_1f8;
  undefined8 *local_1f0;
  undefined8 *puStack_1e8;
  undefined1 *puStack_1e0;
  undefined8 uStack_1d8;
  long *local_1d0;
  undefined1 *puStack_1c8;
  undefined1 *local_1c0;
  undefined1 *local_138;
  undefined1 local_130 [72];
  undefined1 **local_e8;
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
  undefined8 uStack_78;
  undefined8 local_70;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  __ZNSt3__15mutex4lockEv(param_1 + 0x80);
  plVar13 = (long *)(param_1 + 0x70);
  plVar6 = (long *)*plVar13;
  plVar18 = plVar13;
  plVar11 = plVar6;
  plVar20 = plVar13;
  if (plVar6 != (long *)0x0) {
    do {
      uVar19 = (uint)param_2;
      if (*(uint *)(plVar11 + 4) >= uVar19) {
        plVar18 = plVar11;
      }
      plVar1 = plVar11 + (*(uint *)(plVar11 + 4) < uVar19);
      plVar11 = (long *)*plVar1;
    } while ((long *)*plVar1 != (long *)0x0);
    if ((plVar18 != plVar13) && (*(uint *)(plVar18 + 4) <= uVar19)) {
      plVar20 = plVar18;
    }
  }
  if (plVar13 == plVar20) {
    iVar5 = thunk_FUN_05e1d97c(4);
    if (iVar5 != 0) {
      FUN_0488143c(&local_200);
      ppppppuVar2 = (undefined8 ******)local_200;
      if (-1 < (long)local_1f0) {
        ppppppuVar2 = &local_200;
      }
      if ((DAT_0a45cea6 & 1) == 0) {
        uVar10 = 0;
        do {
          (&DAT_0a45ce91)[uVar10] = (&DAT_08a10f2b)[uVar10] + 0x8a ^ (&DAT_08a10f1b)[uVar10 & 0xf];
          uVar10 = uVar10 + 1;
        } while (uVar10 != 0x15);
        DAT_0a45cea6 = 1;
      }
      if ((DAT_0a45d2f2 & 1) == 0) {
        DAT_0a45d2e8._0_1_ = s_OnTaskEn101_91_33_17_08a10bd8[0];
        DAT_0a45d2e8._1_1_ = s_OnTaskEn101_91_33_17_08a10bd8[1];
        DAT_0a45d2e8._2_1_ = s_OnTaskEn101_91_33_17_08a10bd8[2];
        DAT_0a45d2e8._3_1_ = s_OnTaskEn101_91_33_17_08a10bd8[3];
        DAT_0a45d2e8._4_1_ = s_OnTaskEn101_91_33_17_08a10bd8[4];
        DAT_0a45d2e8._5_1_ = s_OnTaskEn101_91_33_17_08a10bd8[5];
        DAT_0a45d2e8._6_1_ = s_OnTaskEn101_91_33_17_08a10bd8[6];
        DAT_0a45d2e8._7_1_ = s_OnTaskEn101_91_33_17_08a10bd8[7];
        DAT_0a45d2f0 = 100;
        DAT_0a45d2f2 = 1;
      }
      FUN_05e1d050(&local_1d0,4,ppppppuVar2,&DAT_0a45ce91,&DAT_0a45d2e8,0x2af,0,0);
      local_138 = local_130;
      if ((DAT_0a45d389 & 1) == 0) {
        uVar10 = 0;
        do {
          (&DAT_0a45d341)[uVar10] = (&DAT_08a116aa)[uVar10] + 0x8a ^ (&DAT_08a1169a)[uVar10 & 0xf];
          uVar10 = uVar10 + 1;
        } while (uVar10 != 0x48);
        DAT_0a45d389 = 1;
      }
      lVar7 = 0;
      do {
        lVar16 = lVar7;
        uVar19 = (uint)param_2;
        local_130[lVar16] =
             (&DAT_0a45d341)[uVar19 + (int)((param_2 & 0xffffffff) / 10) * -10 + 0x23];
        lVar7 = lVar16 + 1;
        param_2 = (param_2 & 0xffffffff) / 10;
      } while (9 < uVar19);
      local_130[lVar16 + 1] = 0;
      if (8 < lVar16 + 8U) {
        puVar17 = local_130;
        puVar14 = local_130 + lVar16;
        do {
          puVar17 = puVar17 + 1;
          uVar3 = *puVar14;
          puVar15 = puVar14 + -1;
          *puVar14 = puVar17[-1];
          puVar17[-1] = uVar3;
          puVar14 = puVar15;
        } while (puVar17 < puVar15);
      }
      if ((DAT_0a45d311 & 1) == 0) {
        uVar10 = 0;
        do {
          (&DAT_0a45d2f3)[uVar10] = (&DAT_08a11625)[uVar10] + 0x8a ^ (&DAT_08a11615)[uVar10 & 0xf];
          uVar10 = uVar10 + 1;
        } while (uVar10 != 0x1e);
        DAT_0a45d311 = 1;
      }
      uStack_d8 = 0;
      local_e0 = 0;
      local_e8 = &local_138;
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
      local_70 = 0;
      FUN_05e1d31c(&local_1d0,&DAT_0a45d2f3,&local_e8);
      thunk_FUN_05e1d0bc(&local_1d0);
      if ((long)local_1f0 < 0) {
        __ZdlPvm(local_200,(ulong)local_1f0 & 0x7fffffffffffffff);
      }
    }
    __ZNSt3__15mutex6unlockEv(param_1 + 0x80);
  }
  else {
    plVar18 = plVar20;
    plVar11 = (long *)plVar20[1];
    if ((long *)plVar20[1] == (long *)0x0) {
      do {
        plVar13 = (long *)plVar18[2];
        bVar4 = (long *)*plVar13 != plVar18;
        plVar18 = plVar13;
      } while (bVar4);
    }
    else {
      do {
        plVar13 = plVar11;
        plVar11 = (long *)*plVar13;
      } while ((long *)*plVar13 != (long *)0x0);
    }
    plVar18 = (long *)plVar20[5];
    if (*(long **)(param_1 + 0x68) == plVar20) {
      *(long **)(param_1 + 0x68) = plVar13;
    }
    *(long *)(param_1 + 0x78) = *(long *)(param_1 + 0x78) + -1;
    FUN_00024618(plVar6,plVar20);
    __ZdlPvm(plVar20,0x30);
    __ZNSt3__15mutex6unlockEv(param_1 + 0x80);
    lVar7 = FUN_056300b4(param_8,0);
    if ((lVar7 != 0) && (lVar7 = FUN_009ce4a8(param_8), lVar7 != 0)) {
      puStack_1e8 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
      local_1f0 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
      uStack_1d8 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_1e0 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_1f8 = &SUB_aaaaaaaaaaaaaaaa;
      local_200 = (undefined8 *****)&SUB_aaaaaaaaaaaaaaaa;
      FUN_05563138(&local_200);
      uVar8 = FUN_056300b4(param_8,0);
      uVar9 = FUN_009ce4a8(param_8);
      iVar5 = FUN_05ab3ab8(&local_200,uVar8,uVar9);
      if (iVar5 == 0) {
        if ((param_6 == 0 && param_5 == 0) && (iVar5 = thunk_FUN_05e1d97c(4), iVar5 != 0)) {
          FUN_0488143c(local_218);
          ppppppuVar2 = (undefined8 ******)local_218[0];
          if (-1 < cStack_201) {
            ppppppuVar2 = local_218;
          }
          if ((DAT_0a45cea6 & 1) == 0) {
            uVar10 = 0;
            do {
              (&DAT_0a45ce91)[uVar10] =
                   (&DAT_08a10f2b)[uVar10] + 0x8a ^ (&DAT_08a10f1b)[uVar10 & 0xf];
              uVar10 = uVar10 + 1;
            } while (uVar10 != 0x15);
            DAT_0a45cea6 = 1;
          }
          if ((DAT_0a45d2f2 & 1) == 0) {
            DAT_0a45d2e8._0_1_ = s_OnTaskEn101_91_33_17_08a10bd8[0];
            DAT_0a45d2e8._1_1_ = s_OnTaskEn101_91_33_17_08a10bd8[1];
            DAT_0a45d2e8._2_1_ = s_OnTaskEn101_91_33_17_08a10bd8[2];
            DAT_0a45d2e8._3_1_ = s_OnTaskEn101_91_33_17_08a10bd8[3];
            DAT_0a45d2e8._4_1_ = s_OnTaskEn101_91_33_17_08a10bd8[4];
            DAT_0a45d2e8._5_1_ = s_OnTaskEn101_91_33_17_08a10bd8[5];
            DAT_0a45d2e8._6_1_ = s_OnTaskEn101_91_33_17_08a10bd8[6];
            DAT_0a45d2e8._7_1_ = s_OnTaskEn101_91_33_17_08a10bd8[7];
            DAT_0a45d2f0 = 100;
            DAT_0a45d2f2 = 1;
          }
          FUN_05e1d050(&local_1d0,4,ppppppuVar2,&DAT_0a45ce91,&DAT_0a45d2e8,0x2d9,0,0);
          local_138 = local_130;
          if ((DAT_0a45d389 & 1) == 0) {
            uVar10 = 0;
            do {
              (&DAT_0a45d341)[uVar10] =
                   (&DAT_08a116aa)[uVar10] + 0x8a ^ (&DAT_08a1169a)[uVar10 & 0xf];
              uVar10 = uVar10 + 1;
            } while (uVar10 != 0x48);
            DAT_0a45d389 = 1;
          }
          lVar7 = 0;
          do {
            lVar16 = lVar7;
            uVar19 = (uint)param_2;
            local_130[lVar16] =
                 (&DAT_0a45d341)[uVar19 + (int)((param_2 & 0xffffffff) / 10) * -10 + 0x23];
            lVar7 = lVar16 + 1;
            param_2 = (param_2 & 0xffffffff) / 10;
          } while (9 < uVar19);
          local_130[lVar16 + 1] = 0;
          if (8 < lVar16 + 8U) {
            puVar17 = local_130;
            puVar14 = local_130 + lVar16;
            do {
              puVar17 = puVar17 + 1;
              uVar3 = *puVar14;
              puVar15 = puVar14 + -1;
              *puVar14 = puVar17[-1];
              puVar17[-1] = uVar3;
              puVar14 = puVar15;
            } while (puVar17 < puVar15);
          }
          if ((DAT_0a45d340 & 1) == 0) {
            uVar10 = 0;
            do {
              (&DAT_0a45d312)[uVar10] =
                   (&DAT_08a11653)[uVar10] + 0x8a ^ (&DAT_08a11643)[uVar10 & 0xf];
              uVar10 = uVar10 + 1;
            } while (uVar10 != 0x2e);
            DAT_0a45d340 = 1;
          }
          uStack_d8 = 0;
          local_e0 = 0;
          local_e8 = &local_138;
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
          local_70 = 0;
          FUN_05e1d31c(&local_1d0,&DAT_0a45d312,&local_e8);
          thunk_FUN_05e1d0bc(&local_1d0);
          if (cStack_201 < '\0') {
            __ZdlPvm(local_218[0],CONCAT17(cStack_201,local_208) & 0x7fffffffffffffff);
          }
        }
      }
      else if (param_6 == 0 && param_5 == 0) {
        if ((uStack_1d8._4_4_ >> 2 & 1) != 0) {
          lVar7 = (long)*(char *)((long)puStack_1e8 + 0x17);
          if (lVar7 < 0) {
            lVar7 = puStack_1e8[1];
          }
          if (lVar7 != 0) {
            puStack_1c8 = &SUB_aaaaaaaaaaaaaaaa;
            local_1c0 = &SUB_aaaaaaaaaaaaaaaa;
            local_1d0 = (long *)&SUB_aaaaaaaaaaaaaaaa;
            if (*(char *)((long)puStack_1e8 + 0x17) < '\0') {
              FUN_00018d20(&local_1d0,*puStack_1e8,puStack_1e8[1]);
            }
            else {
              puStack_1c8 = (undefined1 *)puStack_1e8[1];
              local_1d0 = (long *)*puStack_1e8;
              local_1c0 = (undefined1 *)puStack_1e8[2];
            }
            if ((*(int *)((long)plVar18 + 0xc) == 0x2fb) || (*(int *)((long)plVar18 + 0xc) == 0xfc))
            {
              uVar8 = FUN_04669774();
              FUN_0466c494(uVar8,&local_1d0);
              if (*(long *)(param_1 + 0x60) != 0) {
                FUN_05cc1cf4(*(long *)(param_1 + 0x60),&local_1d0);
              }
            }
            else {
              uVar8 = FUN_04669774();
              iVar5 = FUN_04671ac0(uVar8,*(undefined4 *)((long)plVar18 + 0xc));
              if (iVar5 != 0) {
                uVar8 = FUN_04669774();
                FUN_04671e00(uVar8,*(undefined4 *)((long)plVar18 + 0xc),&local_1d0);
              }
            }
            if ((long)local_1c0 < 0) {
              __ZdlPvm(local_1d0,(ulong)local_1c0 & 0x7fffffffffffffff);
            }
          }
        }
        if ((uStack_1d8._4_4_ >> 1 & 1) != 0) {
          lVar7 = (long)*(char *)((long)local_1f0 + 0x17);
          if (lVar7 < 0) {
            lVar7 = local_1f0[1];
          }
          if (lVar7 != 0) {
            local_1d0 = (long *)&SUB_aaaaaaaaaaaaaaaa;
            FUN_04659d5c(&local_1d0);
            lVar7 = (long)*(char *)((long)local_1f0 + 0x17);
            puVar12 = local_1f0;
            if (lVar7 < 0) {
              puVar12 = (undefined8 *)*local_1f0;
              lVar7 = local_1f0[1];
            }
            FUN_04659f18(&local_1d0,puVar12,lVar7);
            (**(code **)(*plVar18 + 0x18))(plVar18,&local_1d0);
            FUN_04659ddc(&local_1d0);
          }
        }
      }
      FUN_05565bac(&local_200);
    }
    if (param_6 == -0xd) {
      uVar8 = FUN_04669774();
      uVar10 = FUN_04671ac0(uVar8,*(undefined4 *)((long)plVar18 + 0xc));
      if ((uVar10 & 1) == 0) {
        if (*(long **)(param_1 + 0x28) != (long *)0x0) {
          (**(code **)(**(long **)(param_1 + 0x28) + 0x18))();
        }
        param_6 = -0xd;
      }
      else {
        param_6 = -0xe;
      }
    }
    local_e8 = (undefined1 **)CONCAT44(local_e8._4_4_,param_5);
    local_138 = (undefined1 *)CONCAT44(local_138._4_4_,param_6);
    plVar11 = (long *)plVar18[0xd];
    local_1d0 = plVar18;
    if (plVar11 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
      FUN_0021eccc();
    }
    iVar5 = (**(code **)(*plVar11 + 0x30))(plVar11,&local_1d0,&local_e8,&local_138);
    if (iVar5 != 0 && plVar18 != (long *)0x0) {
      (**(code **)(*plVar18 + 8))(plVar18);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_68) {
    return 0;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


