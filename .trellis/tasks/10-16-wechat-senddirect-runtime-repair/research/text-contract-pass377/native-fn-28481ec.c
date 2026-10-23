// Ghidra inferred pseudocode; requested=0x28481ec
// entry=028481ec end=028489b7

/* WARNING: Removing unreachable block (ram,0x02848468) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_028481ec(int *param_1,undefined8 param_2,undefined8 param_3,undefined8 *param_4,
                 int *param_5)

{
  undefined8 *******pppppppuVar1;
  undefined1 uVar2;
  char cVar3;
  uint uVar4;
  undefined4 uVar5;
  uint3 uVar6;
  bool bVar7;
  undefined8 uVar8;
  undefined8 uVar9;
  undefined8 uVar10;
  undefined8 uVar11;
  undefined8 uVar12;
  undefined8 uVar13;
  int iVar14;
  long lVar15;
  undefined1 *puVar16;
  undefined1 *puVar17;
  undefined1 *puVar18;
  ulong uVar19;
  long lVar20;
  int iVar21;
  bool bVar22;
  long *plVar23;
  undefined4 uVar24;
  undefined4 uVar25;
  undefined4 uVar26;
  undefined4 uVar27;
  undefined4 uVar28;
  int local_31c;
  undefined8 *******local_318 [2];
  undefined7 local_308;
  char cStack_301;
  undefined1 auStack_300 [40];
  undefined8 local_2d8;
  undefined8 uStack_2d0;
  ulong local_2c8;
  undefined8 local_2c0;
  undefined8 local_2b8;
  undefined8 uStack_2b0;
  ulong local_2a8;
  undefined8 local_2a0;
  undefined1 *local_270;
  undefined1 *puStack_268;
  undefined1 *local_260;
  undefined8 *******pppppppuStack_258;
  undefined1 *puStack_250;
  undefined1 *local_248;
  undefined1 *local_240;
  undefined8 local_230;
  undefined1 *puStack_228;
  undefined1 *local_220;
  undefined1 *puStack_218;
  undefined1 *puStack_210;
  long *local_208;
  undefined1 uStack_1f9;
  undefined8 local_1f8;
  undefined1 local_1f0 [71];
  undefined1 uStack_1a9;
  undefined8 local_1a8;
  undefined1 local_1a0 [72];
  undefined8 *******local_158;
  undefined1 local_150;
  undefined8 *******local_108;
  undefined8 *local_100;
  undefined8 *local_f8;
  undefined8 local_f0;
  undefined8 uStack_e8;
  undefined8 local_e0;
  undefined8 uStack_d8;
  undefined8 local_d0;
  undefined8 uStack_c8;
  long *local_c0;
  undefined8 uStack_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  long local_88;
  
  uVar13 = _UNK_0878b328;
  uVar12 = _DAT_0878b320;
  uVar11 = s_mm_cgi_hest__0875d530._0_8_;
  uVar10 = DAT_084cfd10;
  local_88 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_31c = *param_5;
  uVar24 = (undefined4)DAT_085233b0;
  uVar28 = (undefined4)DAT_084e1078;
  uVar5 = (undefined4)ram0x0878b178;
  uVar26 = (undefined4)DAT_0878b180;
  do {
    puStack_218 = &SUB_aaaaaaaaaaaaaaaa;
    local_220 = &SUB_aaaaaaaaaaaaaaaa;
    local_208 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    puStack_210 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_228 = &SUB_aaaaaaaaaaaaaaaa;
    local_230 = &SUB_aaaaaaaaaaaaaaaa;
    FUN_0284c5f4(&local_230,0,0);
    local_230 = (undefined1 *)CONCAT44(local_230._4_4_,0xffffff92);
    if (local_230._4_4_ == 0) {
      local_230 = (undefined1 *)0xfffffbaaffffff92;
    }
    *(undefined1 **)(param_1 + 6) = &SUB_aaaaaaaaaaaaaaaa;
    *(undefined1 **)(param_1 + 4) = &SUB_aaaaaaaaaaaaaaaa;
    *(undefined1 **)(param_1 + 10) = &SUB_aaaaaaaaaaaaaaaa;
    *(undefined1 **)(param_1 + 8) = &SUB_aaaaaaaaaaaaaaaa;
    *(undefined1 **)(param_1 + 2) = &SUB_aaaaaaaaaaaaaaaa;
    *(undefined1 **)param_1 = &SUB_aaaaaaaaaaaaaaaa;
    if ((DAT_0a39df71 & 1) == 0) {
      uRam000000000a39df68 = uVar13;
      _DAT_0a39df60 = uVar12;
      DAT_0a39df70 = 0;
      DAT_0a39df71 = 1;
    }
    if ((DAT_0a39df81 & 1) == 0) {
      DAT_0a39df78 = uVar11;
      DAT_0a39df80 = 0;
      DAT_0a39df81 = 1;
    }
    FUN_0284bd1c(&local_108,&DAT_0a39df60,&DAT_0a39df78,0x13e,0,param_5[1],&local_230);
    FUN_0513bbf4(auStack_300,param_3);
    if (*(char *)((long)param_4 + 0x17) < '\0') {
      FUN_00018d20(&local_2d8,*param_4,param_4[1]);
    }
    else {
      uStack_2d0 = param_4[1];
      local_2d8 = *param_4;
      local_2c8 = param_4[2];
    }
    local_2c0 = *(undefined8 *)param_5;
    if (*(char *)((long)param_5 + 0x1f) < '\0') {
      FUN_00018d20(&local_2b8,*(undefined8 *)(param_5 + 2),*(undefined8 *)(param_5 + 4));
    }
    else {
      uStack_2b0 = *(undefined8 *)(param_5 + 4);
      local_2b8 = *(undefined8 *)(param_5 + 2);
      local_2a8 = *(ulong *)(param_5 + 6);
    }
    local_2a0 = *(undefined8 *)(param_5 + 8);
    FUN_0284be44(param_1,&local_108,auStack_300);
    if ((long)local_2a8 < 0) {
      __ZdlPvm(local_2b8,local_2a8 & 0x7fffffffffffffff);
    }
    if ((long)local_2c8 < 0) {
      __ZdlPvm(local_2d8,local_2c8 & 0x7fffffffffffffff);
    }
    FUN_0513bc40(auStack_300);
    if (local_c0 != (long *)0x0) {
      (**(code **)(*local_c0 + 8))();
      local_c0 = (long *)0x0;
    }
    local_240 = &SUB_aaaaaaaaaaaaaaaa;
    pppppppuStack_258 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
    local_260 = &SUB_aaaaaaaaaaaaaaaa;
    local_248 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_250 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_268 = &SUB_aaaaaaaaaaaaaaaa;
    local_270 = &SUB_aaaaaaaaaaaaaaaa;
    FUN_0284c4bc(&local_270);
    uVar19 = *(ulong *)(param_5 + 4);
    if (-1 < (char)*(byte *)((long)param_5 + 0x1f)) {
      uVar19 = (ulong)*(byte *)((long)param_5 + 0x1f);
    }
    if (uVar19 != 0) {
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (&pppppppuStack_258,param_5 + 2);
    }
    iVar14 = *param_5;
    uVar4 = iVar14 - local_31c;
    if (*param_1 == 0 && param_1[1] == 0) {
      iVar21 = 0;
LAB_02848840:
      if (iVar14 != local_31c) {
        lVar15 = *(long *)(*(long *)(param_1 + 8) + 8);
        if (lVar15 == 0) {
          lVar15 = *(long *)(DAT_0a520f60 + 8);
        }
        FUN_0461bb2c(&pppppppuStack_258,iVar21,param_1[1],*(undefined4 *)(lVar15 + 0x10),uVar4);
      }
      bVar7 = false;
      bVar22 = true;
    }
    else {
      lVar15 = *(long *)(*(long *)(param_1 + 8) + 8);
      if (lVar15 == 0) {
        lVar15 = *(long *)(DAT_0a520f60 + 8);
      }
      FUN_0461bb2c(&pppppppuStack_258,*param_1,param_1[1],*(undefined4 *)(lVar15 + 0x10),uVar4);
      iVar21 = *param_1;
      if ((iVar21 != -0x6e && iVar21 != 0) || (local_31c == 0)) goto LAB_02848840;
      FUN_066859ec(1000 << (ulong)(uVar4 & 0x1f));
      iVar14 = thunk_FUN_05e1d97c(2);
      local_31c = local_31c + -1;
      if (iVar14 != 0) {
        FUN_0488143c(local_318);
        pppppppuVar1 = local_318[0];
        if (-1 < cStack_301) {
          pppppppuVar1 = local_318;
        }
        if ((DAT_0a39df81 & 1) == 0) {
          DAT_0a39df78 = uVar11;
          DAT_0a39df80 = 0;
          DAT_0a39df81 = 1;
        }
        if ((DAT_0a39df71 & 1) == 0) {
          uRam000000000a39df68 = uVar13;
          _DAT_0a39df60 = uVar12;
          DAT_0a39df70 = 0;
          DAT_0a39df71 = 1;
        }
        FUN_05e1d050(auStack_300,2,pppppppuVar1,&DAT_0a39df78,&DAT_0a39df60,0x150,0,0);
        local_158 = pppppppuStack_258;
        if (-1 < (long)local_248) {
          local_158 = &pppppppuStack_258;
        }
        local_150 = 0;
        iVar14 = *param_1;
        if ((DAT_0a39df51 & 1) == 0) {
          uVar19 = 0;
          do {
            uVar25 = *(undefined4 *)((long)&DAT_08804e86 + uVar19);
            uVar6 = CONCAT12((char)((uint)uVar25 >> 8),(short)uVar25) & 0xff00ff;
            uVar27 = *(undefined4 *)((long)&DAT_08804e72 + uVar19 % 0x14);
            *(uint *)((long)&DAT_0a39df09 + uVar19) =
                 CONCAT13((char)((uint)uVar25 >> 0x18) + 0x8aU ^ (byte)((uint)uVar27 >> 0x18),
                          CONCAT12((char)((uint)uVar25 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar27 >> 0x10),
                                   CONCAT11((char)(uVar6 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar27 >> 8),
                                            (char)uVar6 + 0x8aU ^ (byte)uVar27)));
            uVar19 = uVar19 + 4;
          } while (uVar19 != 0x48);
          DAT_0a39df51 = 1;
        }
        lVar15 = 8;
        iVar21 = iVar14;
        do {
          lVar20 = lVar15;
          *(undefined1 *)((long)&local_1a8 + lVar20) =
               *(undefined1 *)((long)&DAT_0a39df09 + (long)(iVar21 % 10 + 0x23));
          lVar15 = lVar20 + 1;
          uVar4 = iVar21 + 9;
          iVar21 = iVar21 / 10;
        } while (0x12 < uVar4);
        if (iVar14 < 0) {
          *(undefined1 *)((long)&local_1a8 + lVar15) = 0x2d;
          lVar15 = lVar20 + 2;
        }
        *(undefined1 *)((long)&local_1a8 + lVar15) = 0;
        if (9 < lVar15) {
          puVar17 = &uStack_1a9 + lVar15;
          puVar18 = local_1a0;
          do {
            puVar18 = puVar18 + 1;
            uVar2 = *puVar17;
            puVar16 = puVar17 + -1;
            *puVar17 = puVar18[-1];
            puVar18[-1] = uVar2;
            puVar17 = puVar16;
          } while (puVar18 < puVar16);
        }
        iVar14 = param_1[1];
        lVar15 = 8;
        iVar21 = iVar14;
        local_1a8 = local_1a0;
        do {
          lVar20 = lVar15;
          *(undefined1 *)((long)&local_1f8 + lVar20) =
               *(undefined1 *)((long)&DAT_0a39df09 + (long)(iVar21 % 10 + 0x23));
          lVar15 = lVar20 + 1;
          uVar4 = iVar21 + 9;
          iVar21 = iVar21 / 10;
        } while (0x12 < uVar4);
        if (iVar14 < 0) {
          *(undefined1 *)((long)&local_1f8 + lVar15) = 0x2d;
          lVar15 = lVar20 + 2;
        }
        *(undefined1 *)((long)&local_1f8 + lVar15) = 0;
        if (9 < lVar15) {
          puVar17 = &uStack_1f9 + lVar15;
          puVar18 = local_1f0;
          do {
            puVar18 = puVar18 + 1;
            uVar2 = *puVar17;
            puVar16 = puVar17 + -1;
            *puVar17 = puVar18[-1];
            puVar18[-1] = uVar2;
            puVar17 = puVar16;
          } while (puVar18 < puVar16);
        }
        if ((DAT_0a39df9e & 1) == 0) {
          DAT_0a39df94 = CONCAT44((int)uVar10,(int)uVar10);
          DAT_0a39df9c = 0x5f;
          DAT_0a39df9e = 1;
          _DAT_0a39df84 = CONCAT44(uVar24,uVar28);
          uRam000000000a39df8c = CONCAT44(uVar26,uVar5);
        }
        local_108 = &local_158;
        uStack_e8 = 0;
        local_f0 = 0;
        uStack_d8 = 0;
        local_e0 = 0;
        uStack_c8 = 0;
        local_d0 = 0;
        uStack_b8 = 0;
        local_c0 = (long *)0x0;
        uStack_a8 = 0;
        local_b0 = 0;
        uStack_98 = 0;
        local_a0 = 0;
        local_90 = 0;
        local_1f8 = local_1f0;
        local_100 = &local_1a8;
        local_f8 = &local_1f8;
        FUN_05e1d31c(auStack_300,&DAT_0a39df84,&local_108);
        thunk_FUN_05e1d0bc(auStack_300);
        if (cStack_301 < '\0') {
          __ZdlPvm(local_318[0],CONCAT17(cStack_301,local_308) & 0x7fffffffffffffff);
        }
      }
      bVar22 = false;
      bVar7 = true;
    }
    if ((long)local_248 < 0) {
      __ZdlPvm(pppppppuStack_258,(ulong)local_248 & 0x7fffffffffffffff);
    }
    plVar23 = local_208;
    if (!bVar22) {
      plVar23 = *(long **)(param_1 + 10);
      if (plVar23 == (long *)0x0) {
LAB_028488b8:
        cVar3 = *(char *)((long)param_1 + 0x1f);
      }
      else {
        LOAcquire();
        lVar15 = plVar23[1];
        plVar23[1] = lVar15 + -1;
        LORelease();
        if (lVar15 != 0) goto LAB_028488b8;
        (**(code **)(*plVar23 + 0x10))(plVar23);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar23);
        cVar3 = *(char *)((long)param_1 + 0x1f);
      }
      plVar23 = local_208;
      if (cVar3 < '\0') {
        __ZdlPvm(*(undefined8 *)(param_1 + 2),*(ulong *)(param_1 + 6) & 0x7fffffffffffffff);
        plVar23 = local_208;
      }
    }
    local_208 = plVar23;
    if (plVar23 != (long *)0x0) {
      LOAcquire();
      lVar15 = plVar23[1];
      plVar23[1] = lVar15 + -1;
      LORelease();
      if (lVar15 == 0) {
        (**(code **)(*plVar23 + 0x10))(plVar23);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar23);
      }
    }
    uVar8 = s_mm_cgi_hest__0875d530._0_8_;
    uVar9 = DAT_0a39df78;
    if ((long)puStack_218 < 0) {
      __ZdlPvm(puStack_228,(ulong)puStack_218 & 0x7fffffffffffffff);
      uVar8 = s_mm_cgi_hest__0875d530._0_8_;
      uVar9 = DAT_0a39df78;
    }
    s_mm_cgi_hest__0875d530._0_8_ = uVar8;
    DAT_0a39df78 = uVar9;
    if (!bVar7) {
      s_mm_cgi_hest__0875d530[0] = (char)uVar8;
      s_mm_cgi_hest__0875d530[1] = SUB81(uVar8,1);
      s_mm_cgi_hest__0875d530[2] = SUB81(uVar8,2);
      s_mm_cgi_hest__0875d530[3] = SUB81(uVar8,3);
      s_mm_cgi_hest__0875d530[4] = SUB81(uVar8,4);
      s_mm_cgi_hest__0875d530[5] = SUB81(uVar8,5);
      s_mm_cgi_hest__0875d530[6] = SUB81(uVar8,6);
      s_mm_cgi_hest__0875d530[7] = SUB81(uVar8,7);
      DAT_0a39df78._0_1_ = (char)uVar9;
      DAT_0a39df78._1_1_ = SUB81(uVar9,1);
      DAT_0a39df78._2_1_ = SUB81(uVar9,2);
      DAT_0a39df78._3_1_ = SUB81(uVar9,3);
      DAT_0a39df78._4_1_ = SUB81(uVar9,4);
      DAT_0a39df78._5_1_ = SUB81(uVar9,5);
      DAT_0a39df78._6_1_ = SUB81(uVar9,6);
      DAT_0a39df78._7_1_ = SUB81(uVar9,7);
      if (*(long *)PTR____stack_chk_guard_09b36c98 != local_88) {
        s_mm_cgi_hest__0875d530._0_8_ = uVar8;
        DAT_0a39df78 = uVar9;
                    /* WARNING: Subroutine does not return */
        ___stack_chk_fail();
      }
      return;
    }
  } while( true );
}


