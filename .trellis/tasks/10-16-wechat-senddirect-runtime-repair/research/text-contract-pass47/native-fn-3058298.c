// Ghidra inferred pseudocode; requested=0x3058298
// entry=03058298 end=03058a17

/* WARNING: Removing unreachable block (ram,0x030584e4) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_03058298(int *param_1,undefined8 param_2,undefined8 param_3,undefined8 *param_4,
                 int *param_5)

{
  undefined8 *******pppppppuVar1;
  undefined1 uVar2;
  char cVar3;
  uint uVar4;
  bool bVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  undefined8 uVar8;
  undefined8 uVar9;
  undefined8 uVar10;
  int iVar11;
  long lVar12;
  undefined1 *puVar13;
  undefined1 *puVar14;
  undefined1 *puVar15;
  ulong uVar16;
  long lVar17;
  int iVar18;
  bool bVar19;
  long *plVar20;
  int local_32c;
  undefined8 *******local_328 [2];
  undefined7 local_318;
  char cStack_311;
  undefined1 *local_310;
  undefined1 *puStack_308;
  undefined1 *local_300;
  undefined8 *******pppppppuStack_2f8;
  undefined1 *puStack_2f0;
  undefined1 *local_2e8;
  undefined1 *local_2e0;
  undefined1 auStack_2d0 [96];
  undefined8 local_270;
  undefined8 uStack_268;
  ulong local_260;
  undefined8 local_258;
  undefined8 local_250;
  undefined8 uStack_248;
  ulong local_240;
  undefined8 local_238;
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
  
  uVar10 = _UNK_0878b328;
  uVar9 = _DAT_0878b320;
  uVar8 = s_mm_cgi_hest__0875d530._0_8_;
  local_88 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_32c = *param_5;
  do {
    puStack_218 = &SUB_aaaaaaaaaaaaaaaa;
    local_220 = &SUB_aaaaaaaaaaaaaaaa;
    local_208 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    puStack_210 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_228 = &SUB_aaaaaaaaaaaaaaaa;
    local_230 = &SUB_aaaaaaaaaaaaaaaa;
    FUN_0305c3cc(&local_230,0,0);
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
    if ((DAT_0a3d59b1 & 1) == 0) {
      uRam000000000a3d59a8 = uVar10;
      _DAT_0a3d59a0 = uVar9;
      DAT_0a3d59b0 = 0;
      DAT_0a3d59b1 = 1;
    }
    if ((DAT_0a3d59c1 & 1) == 0) {
      DAT_0a3d59b8 = uVar8;
      DAT_0a3d59c0 = 0;
      DAT_0a3d59c1 = 1;
    }
    FUN_0305bb18(&local_108,&DAT_0a3d59a0,&DAT_0a3d59b8,0x13e,0,param_5[1],&local_230);
    FUN_05107c20(auStack_2d0,param_3);
    if (*(char *)((long)param_4 + 0x17) < '\0') {
      FUN_00018d20(&local_270,*param_4,param_4[1]);
    }
    else {
      uStack_268 = param_4[1];
      local_270 = *param_4;
      local_260 = param_4[2];
    }
    local_258 = *(undefined8 *)param_5;
    if (*(char *)((long)param_5 + 0x1f) < '\0') {
      FUN_00018d20(&local_250,*(undefined8 *)(param_5 + 2),*(undefined8 *)(param_5 + 4));
    }
    else {
      uStack_248 = *(undefined8 *)(param_5 + 4);
      local_250 = *(undefined8 *)(param_5 + 2);
      local_240 = *(ulong *)(param_5 + 6);
    }
    local_238 = *(undefined8 *)(param_5 + 8);
    FUN_0305bc40(param_1,&local_108,auStack_2d0);
    if ((long)local_240 < 0) {
      __ZdlPvm(local_250,local_240 & 0x7fffffffffffffff);
    }
    if ((long)local_260 < 0) {
      __ZdlPvm(local_270,local_260 & 0x7fffffffffffffff);
    }
    FUN_05107e00(auStack_2d0);
    if (local_c0 != (long *)0x0) {
      (**(code **)(*local_c0 + 8))();
      local_c0 = (long *)0x0;
    }
    local_2e0 = &SUB_aaaaaaaaaaaaaaaa;
    pppppppuStack_2f8 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
    local_300 = &SUB_aaaaaaaaaaaaaaaa;
    local_2e8 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_2f0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_308 = &SUB_aaaaaaaaaaaaaaaa;
    local_310 = &SUB_aaaaaaaaaaaaaaaa;
    FUN_0305c2b8(&local_310);
    uVar16 = *(ulong *)(param_5 + 4);
    if (-1 < (char)*(byte *)((long)param_5 + 0x1f)) {
      uVar16 = (ulong)*(byte *)((long)param_5 + 0x1f);
    }
    if (uVar16 != 0) {
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (&pppppppuStack_2f8,param_5 + 2);
    }
    iVar11 = *param_5;
    uVar4 = iVar11 - local_32c;
    if (*param_1 == 0 && param_1[1] == 0) {
      iVar18 = 0;
LAB_030588a0:
      if (iVar11 != local_32c) {
        lVar12 = *(long *)(*(long *)(param_1 + 8) + 8);
        if (lVar12 == 0) {
          lVar12 = *(long *)(DAT_0a520db8 + 8);
        }
        FUN_0461bb2c(&pppppppuStack_2f8,iVar18,param_1[1],*(undefined4 *)(lVar12 + 0x10),uVar4);
      }
      bVar5 = false;
      bVar19 = true;
    }
    else {
      lVar12 = *(long *)(*(long *)(param_1 + 8) + 8);
      if (lVar12 == 0) {
        lVar12 = *(long *)(DAT_0a520db8 + 8);
      }
      FUN_0461bb2c(&pppppppuStack_2f8,*param_1,param_1[1],*(undefined4 *)(lVar12 + 0x10),uVar4);
      iVar18 = *param_1;
      if ((iVar18 != -0x6e && iVar18 != 0) || (local_32c == 0)) goto LAB_030588a0;
      FUN_066859ec(1000 << (ulong)(uVar4 & 0x1f));
      iVar11 = thunk_FUN_05e1d97c(2);
      local_32c = local_32c + -1;
      if (iVar11 != 0) {
        FUN_0488143c(local_328);
        pppppppuVar1 = local_328[0];
        if (-1 < cStack_311) {
          pppppppuVar1 = local_328;
        }
        if ((DAT_0a3d59c1 & 1) == 0) {
          DAT_0a3d59b8 = uVar8;
          DAT_0a3d59c0 = 0;
          DAT_0a3d59c1 = 1;
        }
        if ((DAT_0a3d59b1 & 1) == 0) {
          uRam000000000a3d59a8 = uVar10;
          _DAT_0a3d59a0 = uVar9;
          DAT_0a3d59b0 = 0;
          DAT_0a3d59b1 = 1;
        }
        FUN_05e1d050(auStack_2d0,2,pppppppuVar1,&DAT_0a3d59b8,&DAT_0a3d59a0,0x150,0,0);
        local_158 = pppppppuStack_2f8;
        if (-1 < (long)local_2e8) {
          local_158 = &pppppppuStack_2f8;
        }
        local_150 = 0;
        iVar11 = *param_1;
        if ((DAT_0a3d596f & 1) == 0) {
          uVar16 = 0;
          do {
            (&DAT_0a3d5927)[uVar16] = (&DAT_088a5ebf)[uVar16] + 0x8a ^ (&DAT_088a5eaf)[uVar16 & 0xf]
            ;
            uVar16 = uVar16 + 1;
          } while (uVar16 != 0x48);
          DAT_0a3d596f = 1;
        }
        lVar12 = 8;
        iVar18 = iVar11;
        do {
          lVar17 = lVar12;
          *(undefined1 *)((long)&local_1a8 + lVar17) = (&DAT_0a3d5927)[iVar18 % 10 + 0x23];
          lVar12 = lVar17 + 1;
          uVar4 = iVar18 + 9;
          iVar18 = iVar18 / 10;
        } while (0x12 < uVar4);
        if (iVar11 < 0) {
          *(undefined1 *)((long)&local_1a8 + lVar12) = 0x2d;
          lVar12 = lVar17 + 2;
        }
        *(undefined1 *)((long)&local_1a8 + lVar12) = 0;
        if (9 < lVar12) {
          puVar14 = &uStack_1a9 + lVar12;
          puVar15 = local_1a0;
          do {
            puVar15 = puVar15 + 1;
            uVar2 = *puVar14;
            puVar13 = puVar14 + -1;
            *puVar14 = puVar15[-1];
            puVar15[-1] = uVar2;
            puVar14 = puVar13;
          } while (puVar15 < puVar13);
        }
        iVar11 = param_1[1];
        lVar12 = 8;
        iVar18 = iVar11;
        local_1a8 = local_1a0;
        do {
          lVar17 = lVar12;
          *(undefined1 *)((long)&local_1f8 + lVar17) = (&DAT_0a3d5927)[iVar18 % 10 + 0x23];
          lVar12 = lVar17 + 1;
          uVar4 = iVar18 + 9;
          iVar18 = iVar18 / 10;
        } while (0x12 < uVar4);
        if (iVar11 < 0) {
          *(undefined1 *)((long)&local_1f8 + lVar12) = 0x2d;
          lVar12 = lVar17 + 2;
        }
        *(undefined1 *)((long)&local_1f8 + lVar12) = 0;
        if (9 < lVar12) {
          puVar14 = &uStack_1f9 + lVar12;
          puVar15 = local_1f0;
          do {
            puVar15 = puVar15 + 1;
            uVar2 = *puVar14;
            puVar13 = puVar14 + -1;
            *puVar14 = puVar15[-1];
            puVar15[-1] = uVar2;
            puVar14 = puVar13;
          } while (puVar15 < puVar13);
        }
        if ((DAT_0a3d59dc & 1) == 0) {
          uVar16 = 0;
          do {
            (&DAT_0a3d59c2)[uVar16] = (&DAT_088a6172)[uVar16] + 0x8a ^ (&DAT_088a6162)[uVar16 & 0xf]
            ;
            uVar16 = uVar16 + 1;
          } while (uVar16 != 0x1a);
          DAT_0a3d59dc = 1;
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
        FUN_05e1d31c(auStack_2d0,&DAT_0a3d59c2,&local_108);
        thunk_FUN_05e1d0bc(auStack_2d0);
        if (cStack_311 < '\0') {
          __ZdlPvm(local_328[0],CONCAT17(cStack_311,local_318) & 0x7fffffffffffffff);
        }
      }
      bVar19 = false;
      bVar5 = true;
    }
    if ((long)local_2e8 < 0) {
      __ZdlPvm(pppppppuStack_2f8,(ulong)local_2e8 & 0x7fffffffffffffff);
    }
    plVar20 = local_208;
    if (!bVar19) {
      plVar20 = *(long **)(param_1 + 10);
      if (plVar20 == (long *)0x0) {
LAB_03058918:
        cVar3 = *(char *)((long)param_1 + 0x1f);
      }
      else {
        LOAcquire();
        lVar12 = plVar20[1];
        plVar20[1] = lVar12 + -1;
        LORelease();
        if (lVar12 != 0) goto LAB_03058918;
        (**(code **)(*plVar20 + 0x10))(plVar20);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar20);
        cVar3 = *(char *)((long)param_1 + 0x1f);
      }
      plVar20 = local_208;
      if (cVar3 < '\0') {
        __ZdlPvm(*(undefined8 *)(param_1 + 2),*(ulong *)(param_1 + 6) & 0x7fffffffffffffff);
        plVar20 = local_208;
      }
    }
    local_208 = plVar20;
    if (plVar20 != (long *)0x0) {
      LOAcquire();
      lVar12 = plVar20[1];
      plVar20[1] = lVar12 + -1;
      LORelease();
      if (lVar12 == 0) {
        (**(code **)(*plVar20 + 0x10))(plVar20);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar20);
      }
    }
    uVar6 = s_mm_cgi_hest__0875d530._0_8_;
    uVar7 = DAT_0a3d59b8;
    if ((long)puStack_218 < 0) {
      __ZdlPvm(puStack_228,(ulong)puStack_218 & 0x7fffffffffffffff);
      uVar6 = s_mm_cgi_hest__0875d530._0_8_;
      uVar7 = DAT_0a3d59b8;
    }
    s_mm_cgi_hest__0875d530._0_8_ = uVar6;
    DAT_0a3d59b8 = uVar7;
    if (!bVar5) {
      s_mm_cgi_hest__0875d530[0] = (char)uVar6;
      s_mm_cgi_hest__0875d530[1] = SUB81(uVar6,1);
      s_mm_cgi_hest__0875d530[2] = SUB81(uVar6,2);
      s_mm_cgi_hest__0875d530[3] = SUB81(uVar6,3);
      s_mm_cgi_hest__0875d530[4] = SUB81(uVar6,4);
      s_mm_cgi_hest__0875d530[5] = SUB81(uVar6,5);
      s_mm_cgi_hest__0875d530[6] = SUB81(uVar6,6);
      s_mm_cgi_hest__0875d530[7] = SUB81(uVar6,7);
      DAT_0a3d59b8._0_1_ = (char)uVar7;
      DAT_0a3d59b8._1_1_ = SUB81(uVar7,1);
      DAT_0a3d59b8._2_1_ = SUB81(uVar7,2);
      DAT_0a3d59b8._3_1_ = SUB81(uVar7,3);
      DAT_0a3d59b8._4_1_ = SUB81(uVar7,4);
      DAT_0a3d59b8._5_1_ = SUB81(uVar7,5);
      DAT_0a3d59b8._6_1_ = SUB81(uVar7,6);
      DAT_0a3d59b8._7_1_ = SUB81(uVar7,7);
      if (*(long *)PTR____stack_chk_guard_09b36c98 != local_88) {
        s_mm_cgi_hest__0875d530._0_8_ = uVar6;
        DAT_0a3d59b8 = uVar7;
                    /* WARNING: Subroutine does not return */
        ___stack_chk_fail();
      }
      return;
    }
  } while( true );
}


