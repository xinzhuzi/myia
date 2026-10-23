// Ghidra inferred pseudocode; requested=0x2920b74
// entry=0291fb70 end=02921897

/* WARNING: Removing unreachable block (ram,0x0292039c) */
/* WARNING: Removing unreachable block (ram,0x02921068) */
/* WARNING: Removing unreachable block (ram,0x029214e8) */
/* WARNING: Removing unreachable block (ram,0x02920494) */
/* WARNING: Removing unreachable block (ram,0x029204f0) */
/* WARNING: Removing unreachable block (ram,0x02920994) */
/* WARNING: Removing unreachable block (ram,0x029216bc) */
/* WARNING: Removing unreachable block (ram,0x02921158) */
/* WARNING: Removing unreachable block (ram,0x029203f8) */
/* WARNING: Removing unreachable block (ram,0x02921754) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0291fb70(undefined8 param_1,long *******param_2,long *******param_3,undefined8 *param_4)

{
  undefined4 uVar1;
  undefined1 uVar2;
  char cVar3;
  uint3 uVar4;
  bool bVar5;
  long *****ppppplVar6;
  long ******pppppplVar7;
  long lVar8;
  int iVar9;
  uint uVar10;
  long *******ppppppplVar11;
  long *******ppppppplVar12;
  undefined1 *puVar13;
  undefined8 *******pppppppuVar14;
  long *plVar15;
  undefined8 *puVar16;
  undefined8 uVar17;
  code *pcVar18;
  undefined1 *puVar19;
  ulong uVar20;
  long lVar21;
  ulong uVar22;
  undefined1 *puVar23;
  undefined4 uVar24;
  undefined4 uVar25;
  long *******local_380;
  long *plStack_378;
  long ******local_370;
  long ******pppppplStack_368;
  long ******local_360;
  long *******local_358;
  long ******pppppplStack_350;
  long *******local_348;
  long *******ppppppplStack_340;
  long ******local_338;
  undefined4 local_330;
  undefined8 *******local_328;
  undefined1 *puStack_320;
  undefined1 auStack_318 [16];
  undefined8 local_308;
  undefined8 local_300;
  undefined8 *******local_2f8;
  undefined1 *puStack_2f0;
  undefined7 local_2e8;
  char cStack_2e1;
  long *******local_2e0;
  long ******local_2d8;
  undefined8 local_2d0;
  undefined8 local_2c8;
  undefined8 local_2c0;
  undefined8 local_2b8;
  undefined8 local_2b0;
  undefined8 local_2a8;
  undefined8 *******local_2a0;
  undefined1 *local_298;
  undefined8 local_290;
  undefined8 *******local_288;
  ulong local_280;
  ulong local_278;
  long *******local_270;
  long ******pppppplStack_268;
  undefined1 *local_260;
  undefined1 *local_258;
  undefined1 *local_250;
  long *******ppppppplStack_248;
  long *******ppppppplStack_240;
  long ******local_238;
  undefined1 *local_230;
  undefined1 *local_1e0;
  long *local_1d8;
  long alStack_1d0 [3];
  long *local_1b8;
  undefined **local_1b0;
  long *******ppppppplStack_1a8;
  long *local_1a0;
  undefined ***local_198;
  long *******local_190;
  undefined8 uStack_188;
  undefined1 *local_180;
  undefined1 *local_178;
  long *******local_140;
  long *local_138;
  undefined8 local_130;
  long *******local_f0;
  long *******ppppppplStack_e8;
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
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_1e0 = &SUB_aaaaaaaaaaaaaaaa;
  local_1d8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0466aca8(&local_140);
  FUN_01205740(&local_f0,local_140);
  FUN_0230000c(&local_270,local_f0);
  FUN_02ab6388(&local_1e0,local_270,param_2);
  pppppplVar7 = pppppplStack_268;
  if (pppppplStack_268 != (long ******)0x0) {
    LOAcquire();
    ppppplVar6 = pppppplStack_268[1];
    pppppplStack_268[1] = (long *****)((long)ppppplVar6 + -1);
    LORelease();
    if (ppppplVar6 == (long *****)0x0) {
      (*(code *)(*pppppplStack_268)[2])(pppppplStack_268);
      __ZNSt3__119__shared_weak_count14__release_weakEv(pppppplVar7);
    }
  }
  ppppppplVar11 = ppppppplStack_e8;
  plVar15 = local_138;
  if (ppppppplStack_e8 != (long *******)0x0) {
    LOAcquire();
    pppppplVar7 = ppppppplStack_e8[1];
    ppppppplStack_e8[1] = (long ******)((long)pppppplVar7 + -1);
    LORelease();
    if (pppppplVar7 == (long ******)0x0) {
      (*(code *)(*ppppppplStack_e8)[2])(ppppppplStack_e8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar11);
      plVar15 = local_138;
    }
  }
  local_138 = plVar15;
  if (plVar15 != (long *)0x0) {
    LOAcquire();
    lVar8 = *(long *)((long)plVar15 + 8U);
    *(long *)((long)plVar15 + 8U) = lVar8 + -1;
    LORelease();
    if (lVar8 == 0) {
      (**(code **)(*plVar15 + 0x10))(plVar15);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar15);
    }
  }
  if (local_1e0 != (undefined1 *)0x0) {
    local_288 = (undefined8 *******)0x0;
    local_280 = 0;
    local_278 = 0;
    if (*(char *)(param_2 + 8) == '\x01') {
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (&local_288,param_2 + 4);
LAB_0292052c:
      iVar9 = thunk_FUN_05e1d97c(2);
      if (iVar9 != 0) {
        FUN_0488143c(&local_2a0);
        pppppppuVar14 = local_2a0;
        if (-1 < (long)local_290) {
          pppppppuVar14 = &local_2a0;
        }
        if ((DAT_0a3a556a & 1) == 0) {
          _DAT_0a3a5544 = CONCAT44((int)DAT_084a66c8,(int)DAT_08486a48);
          uRam000000000a3a554c = CONCAT44((int)DAT_084a66a8,(int)DAT_084a8ea0);
          _DAT_0a3a5554 = CONCAT44((int)DAT_08617fc8,(int)DAT_084a66b0);
          uRam000000000a3a555c = CONCAT44((int)DAT_084967c0,(int)DAT_08489770);
          DAT_0a3a5564 = (undefined4)DAT_084ccd80;
          DAT_0a3a5568 = 99;
          DAT_0a3a556a = 1;
        }
        if ((DAT_0a3a58cb & 1) == 0) {
          DAT_0a3a58c0._0_1_ = s_end_timeDoBusineParameter___08809538[8];
          DAT_0a3a58c0._1_1_ = s_end_timeDoBusineParameter___08809538[9];
          DAT_0a3a58c0._2_1_ = s_end_timeDoBusineParameter___08809538[10];
          DAT_0a3a58c0._3_1_ = s_end_timeDoBusineParameter___08809538[0xb];
          DAT_0a3a58c0._4_1_ = s_end_timeDoBusineParameter___08809538[0xc];
          DAT_0a3a58c0._5_1_ = s_end_timeDoBusineParameter___08809538[0xd];
          DAT_0a3a58c0._6_1_ = s_end_timeDoBusineParameter___08809538[0xe];
          DAT_0a3a58c0._7_1_ = s_end_timeDoBusineParameter___08809538[0xf];
          DAT_0a3a58c8 = 0x7373;
          DAT_0a3a58ca = 0;
          DAT_0a3a58cb = 1;
        }
        FUN_05e1d050(&local_270,2,pppppppuVar14,&DAT_0a3a5544,&DAT_0a3a58c0,299,0,0);
        local_140 = (long *******)*param_3;
        if (-1 < *(char *)((long)param_3 + 0x17)) {
          local_140 = param_3;
        }
        local_138 = (long *)((ulong)local_138 & 0xffffffffffffff00);
        uVar20 = local_280;
        if (-1 < (long)local_278) {
          uVar20 = local_278 >> 0x38;
        }
        local_190 = (long *******)&uStack_188;
        if ((DAT_0a3a617a & 1) == 0) {
          uVar22 = 0;
          do {
            (&DAT_0a3a6132)[uVar22] = (&DAT_08826e85)[uVar22] + 0x69 ^ (&DAT_08826e75)[uVar22 & 0xf]
            ;
            uVar22 = uVar22 + 1;
          } while (uVar22 != 0x48);
          DAT_0a3a617a = 1;
        }
        lVar8 = 0;
        do {
          lVar21 = lVar8;
          *(undefined1 *)((long)&uStack_188 + lVar21) = *(undefined1 *)(uVar20 % 10 + 0xa3a6155);
          bVar5 = 9 < uVar20;
          uVar20 = uVar20 / 10;
          lVar8 = lVar21 + 1;
        } while (bVar5);
        *(undefined1 *)((long)&uStack_188 + lVar21 + 1) = 0;
        if (8 < lVar21 + 8U) {
          puVar19 = (undefined1 *)((long)&uStack_188 + lVar21);
          puVar13 = (undefined1 *)((long)&uStack_188 + 1);
          do {
            uVar2 = *puVar19;
            *puVar19 = puVar13[-1];
            puVar13[-1] = uVar2;
            bVar5 = puVar13 < puVar19 + -1;
            puVar19 = puVar19 + -1;
            puVar13 = puVar13 + 1;
          } while (bVar5);
        }
        if ((DAT_0a3a59ae & 1) == 0) {
          _DAT_0a3a5984 = CONCAT44((int)ram0x085cdbd8,(int)DAT_0848e640);
          uRam000000000a3a598c = CONCAT44((int)DAT_08824ba8,(int)DAT_08824ba0);
          _DAT_0a3a5994 = CONCAT44((int)DAT_08824bb0,(int)DAT_084a2f50);
          uRam000000000a3a599c = CONCAT44((int)DAT_084caf68,(int)DAT_0859b170);
          DAT_0a3a59a4 = CONCAT44((int)DAT_08711ec0,(int)DAT_08480658);
          DAT_0a3a59ac = 0x5f;
          DAT_0a3a59ae = 1;
        }
        local_f0 = (long *******)&local_140;
        ppppppplStack_e8 = (long *******)&local_190;
        uStack_d8 = 0;
        local_e0 = (long ******)0x0;
        uStack_c8 = 0;
        uStack_d0 = 0;
        uStack_b8 = 0;
        local_c0 = 0;
        uStack_a8 = 0;
        uStack_b0 = 0;
        uStack_98 = 0;
        local_a0 = 0;
        uStack_88 = 0;
        uStack_90 = 0;
        uStack_78 = 0;
        local_80 = 0;
        FUN_05e1d31c(&local_270,&DAT_0a3a5984,&local_f0);
        thunk_FUN_05e1d0bc(&local_270);
        if ((long)local_290 < 0) {
          __ZdlPvm(local_2a0,(ulong)local_290 & 0x7fffffffffffffff);
        }
      }
      local_298 = &SUB_aaaaaaaaaaaaaaaa;
      local_290 = &SUB_aaaaaaaaaaaaaaaa;
      local_2a0 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
      if ((DAT_0a3a59b9 & 1) == 0) {
        DAT_0a3a59b0._0_1_ = s_text_tittitle_v2categoryAddF_08527508[0x10];
        DAT_0a3a59b0._1_1_ = s_text_tittitle_v2categoryAddF_08527508[0x11];
        DAT_0a3a59b0._2_1_ = s_text_tittitle_v2categoryAddF_08527508[0x12];
        DAT_0a3a59b0._3_1_ = s_text_tittitle_v2categoryAddF_08527508[0x13];
        DAT_0a3a59b0._4_1_ = s_text_tittitle_v2categoryAddF_08527508[0x14];
        DAT_0a3a59b0._5_1_ = s_text_tittitle_v2categoryAddF_08527508[0x15];
        DAT_0a3a59b0._6_1_ = s_text_tittitle_v2categoryAddF_08527508[0x16];
        DAT_0a3a59b0._7_1_ = s_text_tittitle_v2categoryAddF_08527508[0x17];
        DAT_0a3a59b8 = 0;
        DAT_0a3a59b9 = 1;
      }
      ppppppplVar11 = (long *******)_strlen((char *)&DAT_0a3a59b0);
      if ((long *******)0x7ffffffffffffff7 < ppppppplVar11) {
                    /* WARNING: Subroutine does not return */
        FUN_00018d9c(&local_f0);
      }
      if ((long *******)((long)&MACH_HEADER.sizeofcmds + 2) < ppppppplVar11) {
        uVar20 = 0x19;
        if (((ulong)ppppppplVar11 | 7) != 0x17) {
          uVar20 = ((ulong)ppppppplVar11 | 7) + 1;
        }
        ppppppplVar12 = (long *******)__Znwm(uVar20);
        local_e0 = (long ******)(uVar20 | 0x8000000000000000);
        local_f0 = ppppppplVar12;
        ppppppplStack_e8 = ppppppplVar11;
LAB_029208d4:
        _memcpy(ppppppplVar12,&DAT_0a3a59b0,(size_t)ppppppplVar11);
      }
      else {
        local_e0 = (long ******)CONCAT17((char)ppppppplVar11,(undefined7)local_e0);
        ppppppplVar12 = (long *******)&local_f0;
        if (ppppppplVar11 != (long *******)0x0) goto LAB_029208d4;
      }
      *(undefined1 *)((long)ppppppplVar12 + (long)ppppppplVar11) = 0;
      FUN_02922400(&local_270,&local_288,&local_f0);
      FUN_02921fc8(&local_2a0,&local_270);
      if ((long)local_260 < 0) {
        __ZdlPvm(local_270,(ulong)local_260 & 0x7fffffffffffffff);
      }
      if ((DAT_0a3a59ce & 1) == 0) {
        DAT_0a3a59c0._0_1_ = s_brand_aco_ac_0858c8e0[0];
        DAT_0a3a59c0._1_1_ = s_brand_aco_ac_0858c8e0[1];
        DAT_0a3a59c0._2_1_ = s_brand_aco_ac_0858c8e0[2];
        DAT_0a3a59c0._3_1_ = s_brand_aco_ac_0858c8e0[3];
        DAT_0a3a59c0._4_1_ = s_brand_aco_ac_0858c8e0[4];
        DAT_0a3a59c0._5_1_ = s_brand_aco_ac_0858c8e0[5];
        DAT_0a3a59c0._6_1_ = s_brand_aco_ac_0858c8e0[6];
        DAT_0a3a59c0._7_1_ = s_brand_aco_ac_0858c8e0[7];
        DAT_0a3a59c8 = (undefined4)DAT_08483208;
        DAT_0a3a59cc = 0x74;
        DAT_0a3a59ce = 1;
      }
      puVar13 = (undefined1 *)_strlen((char *)&DAT_0a3a59c0);
      puVar19 = local_290;
      puVar23 = (undefined1 *)(long)local_290._7_1_;
      if ((long)puVar23 < 0) {
        if (puVar13 == local_298) {
          pppppppuVar14 = local_2a0;
          if (puVar13 == (undefined1 *)0xffffffffffffffff) {
                    /* WARNING: Subroutine does not return */
            FUN_0020edd0(&local_2a0);
          }
          goto LAB_029209c0;
        }
LAB_029209d0:
        if ((DAT_0a3a59d9 & 1) == 0) {
          DAT_0a3a59d0._0_1_ = s_emoticon_a956af0a_0852a358[0];
          DAT_0a3a59d0._1_1_ = s_emoticon_a956af0a_0852a358[1];
          DAT_0a3a59d0._2_1_ = s_emoticon_a956af0a_0852a358[2];
          DAT_0a3a59d0._3_1_ = s_emoticon_a956af0a_0852a358[3];
          DAT_0a3a59d0._4_1_ = s_emoticon_a956af0a_0852a358[4];
          DAT_0a3a59d0._5_1_ = s_emoticon_a956af0a_0852a358[5];
          DAT_0a3a59d0._6_1_ = s_emoticon_a956af0a_0852a358[6];
          DAT_0a3a59d0._7_1_ = s_emoticon_a956af0a_0852a358[7];
          DAT_0a3a59d8 = 0;
          DAT_0a3a59d9 = 1;
        }
        puVar13 = (undefined1 *)_strlen((char *)&DAT_0a3a59d0);
        if ((long)puVar19 < 0) {
          if (puVar13 == local_298) {
            pppppppuVar14 = local_2a0;
            if (puVar13 == (undefined1 *)0xffffffffffffffff) {
                    /* WARNING: Subroutine does not return */
              FUN_0020edd0(&local_2a0);
            }
            goto LAB_02920a38;
          }
        }
        else if (puVar13 == puVar23) {
          pppppppuVar14 = &local_2a0;
LAB_02920a38:
          uVar10 = _memcmp(pppppppuVar14,&DAT_0a3a59d0,(size_t)puVar13);
          puVar13 = (undefined1 *)(ulong)uVar10;
          if (uVar10 == 0) {
            local_2b0 = *param_4;
            *param_4 = 0;
            FUN_0292385c(0,param_2,&local_288,param_3,&local_2b0);
            FUN_00033d2c(&local_2b0);
            goto LAB_029217a4;
          }
        }
        iVar9 = *(int *)(param_2 + 3);
        if (iVar9 == 3) {
          local_2c0 = *param_4;
          *param_4 = 0;
          FUN_0292674c(puVar13,param_2,&local_288,param_3,&local_2c0);
          FUN_00033d2c(&local_2c0);
        }
        else if (iVar9 == 0x31) {
          pppppplStack_268 = (long ******)&SUB_aaaaaaaaaaaaaaaa;
          local_260 = &SUB_aaaaaaaaaaaaaaaa;
          local_270 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
          if ((DAT_0a3a59e1 & 1) == 0) {
            DAT_0a3a59dc = (undefined4)DAT_08489788;
            DAT_0a3a59e0 = 0;
            DAT_0a3a59e1 = 1;
          }
          plVar15 = (long *)_strlen((char *)&DAT_0a3a59dc);
          if ((long *)0x7ffffffffffffff7 < plVar15) {
                    /* WARNING: Subroutine does not return */
            FUN_00018d9c(&local_140);
          }
          if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar15) {
            uVar20 = 0x19;
            if (((ulong)plVar15 | 7) != 0x17) {
              uVar20 = ((ulong)plVar15 | 7) + 1;
            }
            ppppppplVar11 = (long *******)__Znwm(uVar20);
            local_130 = uVar20 | 0x8000000000000000;
            local_140 = ppppppplVar11;
            local_138 = plVar15;
LAB_0292102c:
            _memcpy(ppppppplVar11,&DAT_0a3a59dc,(size_t)plVar15);
          }
          else {
            local_130 = CONCAT17((char)plVar15,(undefined7)local_130);
            ppppppplVar11 = (long *******)&local_140;
            if (plVar15 != (long *)0x0) goto LAB_0292102c;
          }
          *(undefined1 *)((long)ppppppplVar11 + (long)plVar15) = 0;
          FUN_02922400(&local_f0,&local_288,&local_140);
          FUN_02921fc8(&local_270,&local_f0);
          if ((long)local_130 < 0) {
            __ZdlPvm(local_140,local_130 & 0x7fffffffffffffff);
          }
          pppppplVar7 = pppppplStack_268;
          if (-1 < (long)local_260) {
            pppppplVar7 = (long ******)((ulong)local_260 >> 0x38);
          }
          if (pppppplVar7 == (long ******)0x0) {
LAB_029210c0:
            if ((DAT_0a3a59fa & 1) == 0) {
              _DAT_0a3a59e4 = CONCAT44((int)ram0x0858c8e8,(int)DAT_08529aa8);
              uRam000000000a3a59ec = CONCAT44((int)DAT_0858c8f0,(int)DAT_08483208);
              DAT_0a3a59f4 = (undefined4)DAT_0857fdf0;
              DAT_0a3a59f8 = 0x65;
              DAT_0a3a59fa = 1;
            }
            uVar17 = FUN_00b0fd90(&local_2a0,&DAT_0a3a59e4);
LAB_02921130:
            local_2d0 = *param_4;
            *param_4 = 0;
            puVar16 = &local_2d0;
            FUN_02928b44(uVar17,param_2,&local_288,param_3,&local_2d0);
          }
          else {
            uVar17 = FUN_04b56844(&local_270,0);
            if ((int)uVar17 != 6) {
              if ((int)uVar17 == 0) goto LAB_029210c0;
              goto LAB_02921130;
            }
            local_2c8 = *param_4;
            *param_4 = 0;
            puVar16 = &local_2c8;
            FUN_0292799c(uVar17,param_2,&local_288,param_3,&local_2c8);
          }
          FUN_00033d2c(puVar16);
          if ((long)local_260 < 0) {
            __ZdlPvm(local_270,(ulong)local_260 & 0x7fffffffffffffff);
          }
        }
        else {
          if (iVar9 == 0x2f) {
            local_2b8 = *param_4;
            *param_4 = 0;
            FUN_029255e8(puVar13,param_2,&local_288,param_3,&local_2b8);
            FUN_00033d2c(&local_2b8);
            goto LAB_029217a4;
          }
          if (iVar9 == 1) {
            local_270 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
            pppppplStack_268 = (long ******)&SUB_aaaaaaaaaaaaaaaa;
            FUN_0077bdd0(&local_270,&local_f0);
            *(undefined4 *)((long)local_270 + 0xe4) = 1;
            __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                      (local_270 + 0xb9,&local_288);
            __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                      (local_270 + 0x12,param_2);
            pppppplVar7 = pppppplStack_268;
            ppppppplVar11 = local_270;
            local_2e0 = local_270;
            local_2d8 = pppppplStack_268;
            if (local_270 == (long *******)0x0) goto LAB_02920ccc;
            local_2f8 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
            puStack_2f0 = &SUB_aaaaaaaaaaaaaaaa;
            FUN_0466aca8(&local_f0);
            FUN_01205740(&local_270,local_f0);
            FUN_0268f370(&local_2f8,local_270);
            FUN_00129f68(&local_270);
            FUN_00129f68(&local_f0);
            if (local_2f8 == (undefined8 *******)0x0) {
              iVar9 = thunk_FUN_05e1d97c(4);
              if (iVar9 != 0) {
                FUN_0488143c(&local_190);
                ppppppplVar11 = local_190;
                if (-1 < (long)local_180) {
                  ppppppplVar11 = (long *******)&local_190;
                }
                if ((DAT_0a3a556a & 1) == 0) {
                  _DAT_0a3a5544 = CONCAT44((int)DAT_084a66c8,(int)DAT_08486a48);
                  uRam000000000a3a554c = CONCAT44((int)DAT_084a66a8,(int)DAT_084a8ea0);
                  _DAT_0a3a5554 = CONCAT44((int)DAT_08617fc8,(int)DAT_084a66b0);
                  uRam000000000a3a555c = CONCAT44((int)DAT_084967c0,(int)DAT_08489770);
                  DAT_0a3a5564 = (undefined4)DAT_084ccd80;
                  DAT_0a3a5568 = 99;
                  DAT_0a3a556a = 1;
                }
                if ((DAT_0a3a58cb & 1) == 0) {
                  DAT_0a3a58c0._0_1_ = s_end_timeDoBusineParameter___08809538[8];
                  DAT_0a3a58c0._1_1_ = s_end_timeDoBusineParameter___08809538[9];
                  DAT_0a3a58c0._2_1_ = s_end_timeDoBusineParameter___08809538[10];
                  DAT_0a3a58c0._3_1_ = s_end_timeDoBusineParameter___08809538[0xb];
                  DAT_0a3a58c0._4_1_ = s_end_timeDoBusineParameter___08809538[0xc];
                  DAT_0a3a58c0._5_1_ = s_end_timeDoBusineParameter___08809538[0xd];
                  DAT_0a3a58c0._6_1_ = s_end_timeDoBusineParameter___08809538[0xe];
                  DAT_0a3a58c0._7_1_ = s_end_timeDoBusineParameter___08809538[0xf];
                  DAT_0a3a58c8 = 0x7373;
                  DAT_0a3a58ca = 0;
                  DAT_0a3a58cb = 1;
                }
                FUN_05e1d050(&local_270,4,ppppppplVar11,&DAT_0a3a5544,&DAT_0a3a58c0,0x167,0,0);
                local_140 = (long *******)*param_3;
                if (-1 < *(char *)((long)param_3 + 0x17)) {
                  local_140 = param_3;
                }
                local_138 = (long *)((ulong)local_138 & 0xffffffffffffff00);
                if ((DAT_0a3a5a68 & 1) == 0) {
                  _DAT_0a3a5a40 = CONCAT44((int)ram0x085cdbd8,(int)DAT_0848e640);
                  uRam000000000a3a5a48 = CONCAT44((int)DAT_084caf50,(int)DAT_087682b8);
                  _DAT_0a3a5a50 = CONCAT44((int)DAT_084ef428,(int)DAT_08482350);
                  uRam000000000a3a5a58 = CONCAT44((int)DAT_084a66b0,(int)DAT_08820c28);
                  DAT_0a3a5a60 = CONCAT44((int)ram0x0873a920,(int)DAT_084d82d8);
                  DAT_0a3a5a68 = 1;
                }
                local_e0 = (long ******)0x0;
                ppppppplStack_e8 = (long *******)0x0;
                local_f0 = (long *******)&local_140;
                uStack_d0 = 0;
                uStack_d8 = 0;
                local_c0 = 0;
                uStack_c8 = 0;
                uStack_b0 = 0;
                uStack_b8 = 0;
                local_a0 = 0;
                uStack_a8 = 0;
                uStack_90 = 0;
                uStack_98 = 0;
                local_80 = 0;
                uStack_88 = 0;
                uStack_78 = 0;
                FUN_05e1d31c(&local_270,&DAT_0a3a5a40,&local_f0);
                thunk_FUN_05e1d0bc(&local_270);
                if ((long)local_180 < 0) {
                  __ZdlPvm(local_190,(ulong)local_180 & 0x7fffffffffffffff);
                }
              }
              if ((DAT_0a3a5a9f & 1) == 0) {
                _DAT_0a3a5a6c = CONCAT44((int)DAT_084a66a8,(int)DAT_084a8ea0);
                uRam000000000a3a5a74 = CONCAT44((int)DAT_0849fe70,(int)DAT_084a66b0);
                _DAT_0a3a5a7c = CONCAT44((int)DAT_08820c28,(int)DAT_085805c0);
                uRam000000000a3a5a84 = CONCAT44((int)DAT_084d82d8,(int)DAT_084a66b0);
                _DAT_0a3a5a8c = CONCAT44((int)DAT_0877c0f8,(int)DAT_084d82e0);
                uRam000000000a3a5a94 = CONCAT44((int)DAT_08711e88,(int)DAT_08824bb8);
                DAT_0a3a5a9c = 0x656c;
                DAT_0a3a5a9e = 0;
                DAT_0a3a5a9f = 1;
              }
              FUN_00255b9c(&local_f0,&DAT_0a3a5a6c);
              FUN_02921ee8(&local_270);
              FUN_02921e94(param_4,&local_270);
              if (((char)local_230 == '\x01') && ((long)local_238 < 0)) {
                __ZdlPvm(ppppppplStack_248,(ulong)local_238 & 0x7fffffffffffffff);
              }
            }
            else {
              local_138 = (long *)__Znwm(0x28);
              local_138[1] = 0;
              local_138[2] = 0;
              local_138[4] = 0;
              *local_138 = (long)&PTR_FUN_09db38a8;
              local_140 = (long *******)(local_138 + 3);
              *local_140 = (long ******)0x0;
              FUN_00033c7c(local_138 + 4,param_4);
              FUN_0466aca8(&local_190);
              FUN_01205740(&local_f0,local_190);
              FUN_026870f0(&local_270,local_f0);
              if (local_138 != (long *)0x0) {
                local_138[1] = local_138[1] + 1;
              }
              local_1b0 = &PTR_FUN_09db38f8;
              ppppppplStack_1a8 = local_140;
              local_308 = 0;
              local_300 = 0;
              local_1a0 = local_138;
              local_198 = &local_1b0;
              FUN_028562e4(local_270,&local_1b0);
              if (local_198 == &local_1b0) {
                pcVar18 = (code *)(*local_198)[4];
LAB_02921504:
                (*pcVar18)();
              }
              else if (local_198 != (undefined ***)0x0) {
                pcVar18 = (code *)(*local_198)[5];
                goto LAB_02921504;
              }
              FUN_00129f68(&local_308);
              FUN_00129f68(&local_270);
              FUN_00129f68(&local_f0);
              FUN_00129f68(&local_190);
              ppppppplStack_e8 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
              local_e0 = (long ******)&SUB_aaaaaaaaaaaaaaaa;
              local_f0 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
              if (*(char *)((long)param_2 + 0x17) < '\0') {
                FUN_00018d20(&local_f0,*param_2,param_2[1]);
              }
              else {
                ppppppplStack_e8 = (long *******)param_2[1];
                local_f0 = (long *******)*param_2;
                local_e0 = param_2[2];
              }
              uVar1 = *(undefined4 *)(param_2 + 3);
              FUN_04669774();
              FUN_0466ad74(&local_190);
              ppppppplVar12 = local_190;
              if ((DAT_0a3a58cb & 1) == 0) {
                DAT_0a3a58c0._0_1_ = s_end_timeDoBusineParameter___08809538[8];
                DAT_0a3a58c0._1_1_ = s_end_timeDoBusineParameter___08809538[9];
                DAT_0a3a58c0._2_1_ = s_end_timeDoBusineParameter___08809538[10];
                DAT_0a3a58c0._3_1_ = s_end_timeDoBusineParameter___08809538[0xb];
                DAT_0a3a58c0._4_1_ = s_end_timeDoBusineParameter___08809538[0xc];
                DAT_0a3a58c0._5_1_ = s_end_timeDoBusineParameter___08809538[0xd];
                DAT_0a3a58c0._6_1_ = s_end_timeDoBusineParameter___08809538[0xe];
                DAT_0a3a58c0._7_1_ = s_end_timeDoBusineParameter___08809538[0xf];
                DAT_0a3a58c8 = 0x7373;
                DAT_0a3a58ca = 0;
                DAT_0a3a58cb = 1;
              }
              if ((DAT_0a3a5b2d & 1) == 0) {
                uVar20 = 0;
                do {
                  uVar24 = *(undefined4 *)((long)&DAT_0882629d + uVar20);
                  uVar4 = CONCAT12((char)((uint)uVar24 >> 8),(short)uVar24) & 0xff00ff;
                  uVar25 = *(undefined4 *)((long)&DAT_08826289 + uVar20 % 0x14);
                  *(uint *)((long)&DAT_0a3a5aa0 + uVar20) =
                       CONCAT13((char)((uint)uVar24 >> 0x18) + 0x8aU ^ (byte)((uint)uVar25 >> 0x18),
                                CONCAT12((char)((uint)uVar24 >> 0x10) + 0x8aU ^
                                         (byte)((uint)uVar25 >> 0x10),
                                         CONCAT11((char)(uVar4 >> 0x10) + 0x8aU ^
                                                  (byte)((uint)uVar25 >> 8),
                                                  (char)uVar4 + 0x8aU ^ (byte)uVar25)));
                  uVar20 = uVar20 + 4;
                } while (uVar20 != 0x8c);
                DAT_0a3a5b2c = 0;
                DAT_0a3a5b2d = 1;
              }
              FUN_0003bb6c(&local_270,&DAT_0a3a58c0,&DAT_0a3a5aa0,0x183);
              local_380 = local_140;
              plStack_378 = local_138;
              if (local_138 != (long *)0x0) {
                local_138[1] = local_138[1] + 1;
              }
              if (*(char *)((long)param_3 + 0x17) < '\0') {
                FUN_00018d20(&local_370,*param_3,param_3[1]);
              }
              else {
                pppppplStack_368 = param_3[1];
                local_370 = *param_3;
                local_360 = param_3[2];
              }
              local_358 = ppppppplVar11;
              pppppplStack_350 = pppppplVar7;
              if (pppppplVar7 != (long ******)0x0) {
                pppppplVar7[1] = (long *****)((long)pppppplVar7[1] + 1);
              }
              ppppppplStack_340 = ppppppplStack_e8;
              local_348 = local_f0;
              local_338 = local_e0;
              local_328 = local_2f8;
              puStack_320 = puStack_2f0;
              lVar8 = 0;
              if (puStack_2f0 != (undefined1 *)0x0) {
                lVar8 = *(long *)(puStack_2f0 + 8);
                *(long *)(puStack_2f0 + 8) = lVar8 + 1;
              }
              local_330 = uVar1;
              FUN_0292d868(lVar8,alStack_1d0,&local_380);
              FUN_0453cce8(auStack_318,ppppppplVar12,&local_270,alStack_1d0,1);
              FUN_0218c0a0(auStack_318);
              if (local_1b8 == alStack_1d0) {
                pcVar18 = *(code **)(*local_1b8 + 0x20);
LAB_02921738:
                (*pcVar18)();
              }
              else if (local_1b8 != (long *)0x0) {
                pcVar18 = *(code **)(*local_1b8 + 0x28);
                goto LAB_02921738;
              }
              FUN_0292d940(&local_380);
              FUN_00129f68(&local_190);
              FUN_00129f68(&local_140);
            }
            FUN_00129f68(&local_2f8);
            pppppplVar7 = local_2d8;
          }
          else {
            local_2e0 = (long *******)0x0;
            local_2d8 = (long ******)0x0;
LAB_02920ccc:
            iVar9 = thunk_FUN_05e1d97c(4);
            if (iVar9 != 0) {
              FUN_0488143c(&local_2f8);
              pppppppuVar14 = local_2f8;
              if (-1 < cStack_2e1) {
                pppppppuVar14 = &local_2f8;
              }
              if ((DAT_0a3a556a & 1) == 0) {
                _DAT_0a3a5544 = CONCAT44((int)DAT_084a66c8,(int)DAT_08486a48);
                uRam000000000a3a554c = CONCAT44((int)DAT_084a66a8,(int)DAT_084a8ea0);
                _DAT_0a3a5554 = CONCAT44((int)DAT_08617fc8,(int)DAT_084a66b0);
                uRam000000000a3a555c = CONCAT44((int)DAT_084967c0,(int)DAT_08489770);
                DAT_0a3a5564 = (undefined4)DAT_084ccd80;
                DAT_0a3a5568 = 99;
                DAT_0a3a556a = 1;
              }
              if ((DAT_0a3a58cb & 1) == 0) {
                DAT_0a3a58c0._0_1_ = s_end_timeDoBusineParameter___08809538[8];
                DAT_0a3a58c0._1_1_ = s_end_timeDoBusineParameter___08809538[9];
                DAT_0a3a58c0._2_1_ = s_end_timeDoBusineParameter___08809538[10];
                DAT_0a3a58c0._3_1_ = s_end_timeDoBusineParameter___08809538[0xb];
                DAT_0a3a58c0._4_1_ = s_end_timeDoBusineParameter___08809538[0xc];
                DAT_0a3a58c0._5_1_ = s_end_timeDoBusineParameter___08809538[0xd];
                DAT_0a3a58c0._6_1_ = s_end_timeDoBusineParameter___08809538[0xe];
                DAT_0a3a58c0._7_1_ = s_end_timeDoBusineParameter___08809538[0xf];
                DAT_0a3a58c8 = 0x7373;
                DAT_0a3a58ca = 0;
                DAT_0a3a58cb = 1;
              }
              FUN_05e1d050(&local_270,4,pppppppuVar14,&DAT_0a3a5544,&DAT_0a3a58c0,0x15f,0,0);
              local_140 = (long *******)*param_3;
              if (-1 < *(char *)((long)param_3 + 0x17)) {
                local_140 = param_3;
              }
              local_138 = (long *)((ulong)local_138 & 0xffffffffffffff00);
              local_f0 = (long *******)CONCAT44(local_f0._4_4_,*(undefined4 *)(param_2 + 3));
              local_190 = (long *******)0x0;
              FUN_003eccb4(&local_f0,&uStack_188,10,1);
              if ((DAT_0a3a5a23 & 1) == 0) {
                _DAT_0a3a59fc = CONCAT44((int)ram0x085cdbd8,(int)DAT_0848e640);
                uRam000000000a3a5a04 = CONCAT44((int)DAT_087c0f20,(int)DAT_08771268);
                _DAT_0a3a5a0c = CONCAT44((int)DAT_0853b498,(int)DAT_084a4ea0);
                uRam000000000a3a5a14 = CONCAT44((int)DAT_08536f80,(int)DAT_0848f630);
                DAT_0a3a5a1c = (undefined4)DAT_085b0640;
                DAT_0a3a5a20 = 0x5f25;
                DAT_0a3a5a22 = 0;
                DAT_0a3a5a23 = 1;
              }
              local_f0 = (long *******)&local_140;
              uStack_d8 = 0;
              local_e0 = (long ******)0x0;
              uStack_c8 = 0;
              uStack_d0 = 0;
              uStack_b8 = 0;
              local_c0 = 0;
              uStack_a8 = 0;
              uStack_b0 = 0;
              uStack_98 = 0;
              local_a0 = 0;
              uStack_88 = 0;
              uStack_90 = 0;
              uStack_78 = 0;
              local_80 = 0;
              local_190 = (long *******)&uStack_188;
              ppppppplStack_e8 = (long *******)&local_190;
              FUN_05e1d31c(&local_270,&DAT_0a3a59fc,&local_f0);
              thunk_FUN_05e1d0bc(&local_270);
              if (cStack_2e1 < '\0') {
                __ZdlPvm(local_2f8,CONCAT17(cStack_2e1,local_2e8) & 0x7fffffffffffffff);
              }
            }
            __ZNSt3__19to_stringEi(&local_140,*(undefined4 *)(param_2 + 3));
            if ((DAT_0a3a5a3f & 1) == 0) {
              _DAT_0a3a5a24 = CONCAT44((int)DAT_08482f58,(int)DAT_08824bc0);
              uRam000000000a3a5a2c = CONCAT44((int)DAT_08486a48,(int)DAT_08480958);
              DAT_0a3a5a34 = CONCAT44((int)DAT_08489788,(int)DAT_08486a50);
              DAT_0a3a5a3c = 0x203a;
              DAT_0a3a5a3e = 0;
              DAT_0a3a5a3f = 1;
            }
            puVar16 = (undefined8 *)
                      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6insertEmPKc
                                (&local_140,0,&DAT_0a3a5a24);
            ppppppplStack_e8 = (long *******)puVar16[1];
            local_f0 = (long *******)*puVar16;
            local_e0 = (long ******)puVar16[2];
            puVar16[1] = 0;
            puVar16[2] = 0;
            *puVar16 = 0;
            FUN_02921ee8(&local_270,&local_f0);
            FUN_02921e94(param_4,&local_270);
            if (((char)local_230 == '\x01') && ((long)local_238 < 0)) {
              __ZdlPvm(ppppppplStack_248,(ulong)local_238 & 0x7fffffffffffffff);
            }
            pppppplVar7 = local_2d8;
            if ((long)local_130 < 0) {
              __ZdlPvm(local_140,local_130 & 0x7fffffffffffffff);
              pppppplVar7 = local_2d8;
            }
          }
          local_2d8 = pppppplVar7;
          if (pppppplVar7 != (long ******)0x0) {
            LOAcquire();
            ppppplVar6 = pppppplVar7[1];
            pppppplVar7[1] = (long *****)((long)ppppplVar6 + -1);
            LORelease();
            if (ppppplVar6 == (long *****)0x0) {
              (*(code *)(*pppppplVar7)[2])(pppppplVar7);
              __ZNSt3__119__shared_weak_count14__release_weakEv(pppppplVar7);
            }
          }
        }
      }
      else {
        if (puVar13 != puVar23) goto LAB_029209d0;
        pppppppuVar14 = &local_2a0;
LAB_029209c0:
        iVar9 = _memcmp(pppppppuVar14,&DAT_0a3a59c0,(size_t)puVar13);
        if (iVar9 != 0) goto LAB_029209d0;
        local_2a8 = *param_4;
        *param_4 = 0;
        FUN_0292285c(0,param_2,&local_288,param_3,&local_2a8);
        FUN_00033d2c(&local_2a8);
      }
LAB_029217a4:
      if ((long)local_290 < 0) {
        __ZdlPvm(local_2a0,(ulong)local_290 & 0x7fffffffffffffff);
      }
    }
    else {
      uStack_188 = (long ******)&SUB_aaaaaaaaaaaaaaaa;
      local_190 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
      local_178 = &SUB_aaaaaaaaaaaaaaaa;
      local_180 = &SUB_aaaaaaaaaaaaaaaa;
      local_270 = (long *******)0x0;
      pppppplStack_268 = (long ******)0x0;
      local_260 = (undefined1 *)0x0;
      cVar3 = *(char *)((long)param_2 + 0x37);
      ppppppplVar11 = (long *******)param_2[4];
      if (-1 < (long)cVar3) {
        ppppppplVar11 = param_2 + 4;
      }
      pppppplVar7 = param_2[5];
      if (-1 < cVar3) {
        pppppplVar7 = (long ******)(long)cVar3;
      }
      uVar20 = FUN_000206bc(ppppppplVar11,pppppplVar7,&local_270);
      if ((uVar20 & 1) == 0) {
        local_190 = (long *******)((ulong)local_190 & 0xffffffffffffff00);
        local_178 = (undefined1 *)((ulong)local_178._1_7_ << 8);
        if (((long)local_260 < 0) &&
           (__ZdlPvm(local_270,(ulong)local_260 & 0x7fffffffffffffff), ((ulong)local_178 & 1) != 0))
        goto LAB_0291fcc8;
        iVar9 = thunk_FUN_05e1d97c(4);
        if (iVar9 != 0) {
          FUN_0488143c(&local_2a0);
          pppppppuVar14 = local_2a0;
          if (-1 < (long)local_290) {
            pppppppuVar14 = &local_2a0;
          }
          if ((DAT_0a3a556a & 1) == 0) {
            _DAT_0a3a5544 = CONCAT44((int)DAT_084a66c8,(int)DAT_08486a48);
            uRam000000000a3a554c = CONCAT44((int)DAT_084a66a8,(int)DAT_084a8ea0);
            _DAT_0a3a5554 = CONCAT44((int)DAT_08617fc8,(int)DAT_084a66b0);
            uRam000000000a3a555c = CONCAT44((int)DAT_084967c0,(int)DAT_08489770);
            DAT_0a3a5564 = (undefined4)DAT_084ccd80;
            DAT_0a3a5568 = 99;
            DAT_0a3a556a = 1;
          }
          if ((DAT_0a3a58cb & 1) == 0) {
            DAT_0a3a58c0._0_1_ = s_end_timeDoBusineParameter___08809538[8];
            DAT_0a3a58c0._1_1_ = s_end_timeDoBusineParameter___08809538[9];
            DAT_0a3a58c0._2_1_ = s_end_timeDoBusineParameter___08809538[10];
            DAT_0a3a58c0._3_1_ = s_end_timeDoBusineParameter___08809538[0xb];
            DAT_0a3a58c0._4_1_ = s_end_timeDoBusineParameter___08809538[0xc];
            DAT_0a3a58c0._5_1_ = s_end_timeDoBusineParameter___08809538[0xd];
            DAT_0a3a58c0._6_1_ = s_end_timeDoBusineParameter___08809538[0xe];
            DAT_0a3a58c0._7_1_ = s_end_timeDoBusineParameter___08809538[0xf];
            DAT_0a3a58c8 = 0x7373;
            DAT_0a3a58ca = 0;
            DAT_0a3a58cb = 1;
          }
          FUN_05e1d050(&local_270,4,pppppppuVar14,&DAT_0a3a5544,&DAT_0a3a58c0,0x125,0,0);
          local_140 = (long *******)*param_3;
          if (-1 < *(char *)((long)param_3 + 0x17)) {
            local_140 = param_3;
          }
          local_138 = (long *)((ulong)local_138 & 0xffffffffffffff00);
          if ((DAT_0a3a594b & 1) == 0) {
            _DAT_0a3a5914 = CONCAT44((int)ram0x085cdbd8,(int)DAT_0848e640);
            uRam000000000a3a591c = CONCAT44((int)DAT_084f9010,(int)DAT_08824b88);
            _DAT_0a3a5924 = CONCAT44((int)DAT_084ec448,(int)DAT_08824b90);
            uRam000000000a3a592c = CONCAT44((int)DAT_08486af0,(int)DAT_0847fde0);
            _DAT_0a3a5934 = CONCAT44((int)DAT_08486a60,(int)DAT_084d4aa0);
            uRam000000000a3a593c = CONCAT44((int)DAT_08788ee0,(int)DAT_084937f8);
            DAT_0a3a5944 = (undefined4)DAT_08480908;
            DAT_0a3a5948 = 0x3436;
            DAT_0a3a594a = 0;
            DAT_0a3a594b = 1;
          }
          local_e0 = (long ******)0x0;
          ppppppplStack_e8 = (long *******)0x0;
          local_f0 = (long *******)&local_140;
          uStack_d0 = 0;
          uStack_d8 = 0;
          local_c0 = 0;
          uStack_c8 = 0;
          uStack_b0 = 0;
          uStack_b8 = 0;
          local_a0 = 0;
          uStack_a8 = 0;
          uStack_90 = 0;
          uStack_98 = 0;
          local_80 = 0;
          uStack_88 = 0;
          uStack_78 = 0;
          FUN_05e1d31c(&local_270,&DAT_0a3a5914,&local_f0);
          thunk_FUN_05e1d0bc(&local_270);
          if ((long)local_290 < 0) {
            __ZdlPvm(local_2a0,(ulong)local_290 & 0x7fffffffffffffff);
          }
        }
        if ((DAT_0a3a5980 & 1) == 0) {
          _DAT_0a3a594c = CONCAT44((int)DAT_084f9058,(int)ram0x084b0668);
          uRam000000000a3a5954 = CONCAT44((int)DAT_08545158,(int)DAT_0859b170);
          _DAT_0a3a595c = CONCAT44((int)DAT_085b01e0,(int)ram0x08480938);
          uRam000000000a3a5964 = CONCAT44((int)DAT_08824b98,(int)DAT_084a24d8);
          _DAT_0a3a596c = CONCAT44((int)DAT_085d7570,(int)DAT_084a9ae8);
          uRam000000000a3a5974 = CONCAT44((int)DAT_084cade0,(int)DAT_084cadd8);
          DAT_0a3a597c = (undefined4)DAT_084cade8;
          DAT_0a3a5980 = 1;
        }
        ppppppplVar11 = (long *******)_strlen(&DAT_0a3a594c);
        if ((long *******)0x7ffffffffffffff7 < ppppppplVar11) {
                    /* WARNING: Subroutine does not return */
          FUN_00018d9c(&local_f0);
        }
        if ((long *******)((long)&MACH_HEADER.sizeofcmds + 2) < ppppppplVar11) {
          uVar20 = 0x19;
          if (((ulong)ppppppplVar11 | 7) != 0x17) {
            uVar20 = ((ulong)ppppppplVar11 | 7) + 1;
          }
          ppppppplVar12 = (long *******)__Znwm(uVar20);
          local_e0 = (long ******)(uVar20 | 0x8000000000000000);
          local_f0 = ppppppplVar12;
          ppppppplStack_e8 = ppppppplVar11;
LAB_0292042c:
          _memcpy(ppppppplVar12,&DAT_0a3a594c,(size_t)ppppppplVar11);
        }
        else {
          local_e0 = (long ******)CONCAT17((char)ppppppplVar11,(undefined7)local_e0);
          ppppppplVar12 = (long *******)&local_f0;
          if (ppppppplVar11 != (long *******)0x0) goto LAB_0292042c;
        }
        *(undefined1 *)((long)ppppppplVar12 + (long)ppppppplVar11) = 0;
        pppppplStack_268 = (long ******)&DAT_aaaaaaaaaaaaaa00;
        local_260 = &DAT_aaaaaaaaaaaaaa00;
        local_258 = &DAT_aaaaaaaaaaaaaa00;
        local_250 = &DAT_aaaaaaaaaaaaaa00;
        local_270 = (long *******)&DAT_aaaaaaaaaaaaaa00;
        ppppppplStack_240 = ppppppplStack_e8;
        ppppppplStack_248 = local_f0;
        local_238 = local_e0;
        local_230 = &DAT_aaaaaaaaaaaaaa01;
        local_140 = (long *******)*param_4;
        *param_4 = 0;
        (*(code *)local_140[1])(local_140,&local_270);
        FUN_00033d2c(&local_140);
        if (((char)local_230 == '\x01') && ((long)local_238 < 0)) {
          __ZdlPvm(ppppppplStack_248,(ulong)local_238 & 0x7fffffffffffffff);
        }
        bVar5 = false;
      }
      else {
        uStack_188 = pppppplStack_268;
        local_190 = local_270;
        local_180 = local_260;
        local_178 = (undefined1 *)CONCAT71(local_178._1_7_,1);
LAB_0291fcc8:
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (&local_288,&local_190);
        bVar5 = true;
      }
      if (((char)local_178 == '\x01') && ((long)local_180 < 0)) {
        __ZdlPvm(local_190,(ulong)local_180 & 0x7fffffffffffffff);
      }
      if (bVar5) goto LAB_0292052c;
    }
    plVar15 = local_1d8;
    if ((long)local_278 < 0) {
      __ZdlPvm(local_288,local_278 & 0x7fffffffffffffff);
      plVar15 = local_1d8;
    }
    goto joined_r0x029217ec;
  }
  iVar9 = thunk_FUN_05e1d97c(3);
  if (iVar9 != 0) {
    FUN_0488143c(&local_288);
    pppppppuVar14 = local_288;
    if (-1 < (long)local_278) {
      pppppppuVar14 = &local_288;
    }
    if ((DAT_0a3a556a & 1) == 0) {
      _DAT_0a3a5544 = CONCAT44((int)DAT_084a66c8,(int)DAT_08486a48);
      uRam000000000a3a554c = CONCAT44((int)DAT_084a66a8,(int)DAT_084a8ea0);
      _DAT_0a3a5554 = CONCAT44((int)DAT_08617fc8,(int)DAT_084a66b0);
      uRam000000000a3a555c = CONCAT44((int)DAT_084967c0,(int)DAT_08489770);
      DAT_0a3a5564 = (undefined4)DAT_084ccd80;
      DAT_0a3a5568 = 99;
      DAT_0a3a556a = 1;
    }
    if ((DAT_0a3a58cb & 1) == 0) {
      DAT_0a3a58c0._0_1_ = s_end_timeDoBusineParameter___08809538[8];
      DAT_0a3a58c0._1_1_ = s_end_timeDoBusineParameter___08809538[9];
      DAT_0a3a58c0._2_1_ = s_end_timeDoBusineParameter___08809538[10];
      DAT_0a3a58c0._3_1_ = s_end_timeDoBusineParameter___08809538[0xb];
      DAT_0a3a58c0._4_1_ = s_end_timeDoBusineParameter___08809538[0xc];
      DAT_0a3a58c0._5_1_ = s_end_timeDoBusineParameter___08809538[0xd];
      DAT_0a3a58c0._6_1_ = s_end_timeDoBusineParameter___08809538[0xe];
      DAT_0a3a58c0._7_1_ = s_end_timeDoBusineParameter___08809538[0xf];
      DAT_0a3a58c8 = 0x7373;
      DAT_0a3a58ca = 0;
      DAT_0a3a58cb = 1;
    }
    FUN_05e1d050(&local_270,3,pppppppuVar14,&DAT_0a3a5544,&DAT_0a3a58c0,0x119,0,0);
    local_140 = (long *******)*param_3;
    if (-1 < *(char *)((long)param_3 + 0x17)) {
      local_140 = param_3;
    }
    local_138 = (long *)((ulong)local_138 & 0xffffffffffffff00);
    local_190 = (long *******)*param_2;
    if (-1 < *(char *)((long)param_2 + 0x17)) {
      local_190 = param_2;
    }
    uStack_188 = (long ******)((ulong)uStack_188 & 0xffffffffffffff00);
    if ((DAT_0a3a58f5 & 1) == 0) {
      _DAT_0a3a58cc = CONCAT44((int)ram0x085cdbd8,(int)DAT_0848e640);
      uRam000000000a3a58d4 = CONCAT44((int)DAT_0849b088,(int)DAT_087716c0);
      _DAT_0a3a58dc = CONCAT44((int)DAT_084d57b8,(int)DAT_084ec408);
      uRam000000000a3a58e4 = CONCAT44((int)DAT_086732b8,(int)DAT_0849b8f8);
      DAT_0a3a58ec = CONCAT44((int)DAT_08592980,(int)DAT_084a2f90);
      DAT_0a3a58f4 = 0;
      DAT_0a3a58f5 = 1;
    }
    local_f0 = (long *******)&local_140;
    ppppppplStack_e8 = (long *******)&local_190;
    uStack_d8 = 0;
    local_e0 = (long ******)0x0;
    uStack_c8 = 0;
    uStack_d0 = 0;
    uStack_b8 = 0;
    local_c0 = 0;
    uStack_a8 = 0;
    uStack_b0 = 0;
    uStack_98 = 0;
    local_a0 = 0;
    uStack_88 = 0;
    uStack_90 = 0;
    uStack_78 = 0;
    local_80 = 0;
    FUN_05e1d31c(&local_270,&DAT_0a3a58cc,&local_f0);
    thunk_FUN_05e1d0bc(&local_270);
    if ((long)local_278 < 0) {
      __ZdlPvm(local_288,local_278 & 0x7fffffffffffffff);
    }
  }
  if ((DAT_0a3a5912 & 1) == 0) {
    uRam000000000a3a5908 = _UNK_08824cc8;
    _DAT_0a3a5900 = _DAT_08824cc0;
    DAT_0a3a5910 = 100;
    DAT_0a3a5912 = 1;
  }
  ppppppplVar11 = (long *******)_strlen(&DAT_0a3a5900);
  if ((long *******)0x7ffffffffffffff7 < ppppppplVar11) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_f0);
  }
  if ((long *******)((long)&MACH_HEADER.sizeofcmds + 2) < ppppppplVar11) {
    uVar20 = 0x19;
    if (((ulong)ppppppplVar11 | 7) != 0x17) {
      uVar20 = ((ulong)ppppppplVar11 | 7) + 1;
    }
    ppppppplVar12 = (long *******)__Znwm(uVar20);
    local_e0 = (long ******)(uVar20 | 0x8000000000000000);
    local_f0 = ppppppplVar12;
    ppppppplStack_e8 = ppppppplVar11;
LAB_0291ffd8:
    _memcpy(ppppppplVar12,&DAT_0a3a5900,(size_t)ppppppplVar11);
  }
  else {
    local_e0 = (long ******)CONCAT17((char)ppppppplVar11,(undefined7)local_e0);
    ppppppplVar12 = (long *******)&local_f0;
    if (ppppppplVar11 != (long *******)0x0) goto LAB_0291ffd8;
  }
  *(undefined1 *)((long)ppppppplVar12 + (long)ppppppplVar11) = 0;
  pppppplStack_268 = (long ******)&DAT_aaaaaaaaaaaaaa00;
  local_260 = &DAT_aaaaaaaaaaaaaa00;
  local_258 = &DAT_aaaaaaaaaaaaaa00;
  local_250 = &DAT_aaaaaaaaaaaaaa00;
  local_270 = (long *******)&DAT_aaaaaaaaaaaaaa00;
  ppppppplStack_240 = ppppppplStack_e8;
  ppppppplStack_248 = local_f0;
  local_238 = local_e0;
  local_230 = &DAT_aaaaaaaaaaaaaa01;
  local_140 = (long *******)*param_4;
  *param_4 = 0;
  (*(code *)local_140[1])(local_140,&local_270);
  FUN_00033d2c(&local_140);
  plVar15 = local_1d8;
  if (((char)local_230 == '\x01') && ((long)local_238 < 0)) {
    __ZdlPvm(ppppppplStack_248,(ulong)local_238 & 0x7fffffffffffffff);
    plVar15 = local_1d8;
  }
joined_r0x029217ec:
  local_1d8 = plVar15;
  if (plVar15 != (long *)0x0) {
    LOAcquire();
    lVar8 = plVar15[1];
    plVar15[1] = lVar8 + -1;
    LORelease();
    if (lVar8 == 0) {
      (**(code **)(*plVar15 + 0x10))(plVar15);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar15);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_68) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


