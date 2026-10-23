// Ghidra inferred pseudocode; requested=0x292285c
// entry=0292285c end=029235ab

/* WARNING: Removing unreachable block (ram,0x029233dc) */
/* WARNING: Removing unreachable block (ram,0x02923514) */
/* WARNING: Removing unreachable block (ram,0x02923534) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0292285c(undefined8 param_1,undefined8 *param_2,undefined8 param_3,long *param_4,
                 undefined8 param_5)

{
  undefined4 uVar1;
  uint3 uVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  undefined1 *puVar5;
  undefined1 *puVar6;
  long lVar7;
  int iVar8;
  long *plVar9;
  char *pcVar10;
  long *plVar11;
  undefined8 *******pppppppuVar12;
  ulong uVar13;
  uint uVar14;
  code *pcVar15;
  long *plVar16;
  undefined4 uVar17;
  long local_2c0;
  long lStack_2b8;
  ulong local_2b0;
  undefined1 *local_2a8;
  long *plStack_2a0;
  undefined8 ******local_298;
  undefined1 *puStack_290;
  undefined1 *local_288;
  undefined8 *******local_280;
  long *local_278;
  undefined8 local_270;
  undefined1 auStack_260 [8];
  long *local_258;
  undefined8 local_250;
  undefined8 uStack_248;
  undefined1 local_240;
  undefined7 uStack_23f;
  undefined7 local_230;
  char cStack_229;
  undefined1 local_228;
  undefined7 uStack_227;
  undefined7 local_218;
  char cStack_211;
  undefined1 local_210;
  undefined7 uStack_20f;
  undefined7 local_200;
  char cStack_1f9;
  long *local_1f8;
  long *local_1f0;
  undefined8 local_1e8;
  undefined1 *local_1e0;
  long *local_1d8;
  undefined8 *******local_1d0;
  long *plStack_1c8;
  undefined8 local_1c0;
  undefined8 *******local_1b8;
  long *local_1b0;
  long *local_1a8;
  undefined1 *local_1a0;
  long *local_198;
  long alStack_190 [3];
  long *local_178;
  undefined **local_170;
  long *plStack_168;
  long *local_160;
  undefined ***local_158;
  undefined8 *******local_150;
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
  undefined1 *local_e0;
  undefined1 *puStack_d8;
  undefined1 *puStack_d0;
  undefined1 *puStack_c8;
  undefined1 *local_c0;
  undefined1 *puStack_b8;
  undefined1 *puStack_b0;
  undefined1 *puStack_a8;
  undefined1 *local_a0;
  undefined1 *puStack_98;
  undefined1 *puStack_90;
  undefined1 *puStack_88;
  long local_80;
  
  local_80 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_1a0 = &SUB_aaaaaaaaaaaaaaaa;
  local_198 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_00d6bd24(&local_1a0,&local_150);
  *(undefined4 *)(local_1a0 + 0xe4) = 0x2a;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(local_1a0 + 0x90,param_2)
  ;
  plVar9 = (long *)__Znwm(0x2e0);
  plVar16 = plVar9 + 1;
  *plVar16 = 0;
  plVar9[2] = 0;
  *plVar9 = (long)&PTR_FUN_09c83160;
  plVar11 = plVar9 + 3;
  _bzero(plVar11,0x2c8);
  if (plVar9 != (long *)0x0) {
    *plVar16 = *plVar16 + 1;
  }
  *(long **)(local_1a0 + 0x5c8) = plVar11;
  plVar16 = *(long **)(local_1a0 + 0x5d0);
  *(long **)(local_1a0 + 0x5d0) = plVar9;
  local_1b0 = plVar11;
  local_1a8 = plVar9;
  if (plVar16 != (long *)0x0) {
    LOAcquire();
    lVar7 = plVar16[1];
    plVar16[1] = lVar7 + -1;
    LORelease();
    if (lVar7 == 0) {
      (**(code **)(*plVar16 + 0x10))(plVar16);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar16);
    }
  }
  puStack_98 = &SUB_aaaaaaaaaaaaaaaa;
  local_a0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_88 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_90 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_b8 = &SUB_aaaaaaaaaaaaaaaa;
  local_c0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_a8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_b0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_d8 = &SUB_aaaaaaaaaaaaaaaa;
  local_e0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_c8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_d0 = &SUB_aaaaaaaaaaaaaaaa;
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
  puStack_148 = &SUB_aaaaaaaaaaaaaaaa;
  local_150 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0572111c(&local_150);
  iVar8 = FUN_04bd7eb0(param_3,&local_150);
  if (iVar8 != 0) {
    local_1b8 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
    if (local_150 != (undefined8 *******)0x0) {
      local_1d0 = (undefined8 *******)FUN_0571c170(&local_150);
      uVar3 = s_real_xmltotallenfileext_0858c958._0_8_;
joined_r0x029229a4:
      do {
        if ((local_1d0 == (undefined8 *******)0x0) || (local_1d0 == local_150)) goto LAB_02922b88;
        pcVar10 = (char *)FUN_0571c2d4(&local_1d0);
        plVar11 = (long *)_strlen(pcVar10);
        if ((long *)0x7ffffffffffffff7 < plVar11) {
                    /* WARNING: Subroutine does not return */
          FUN_00018d9c(&local_280);
        }
        if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar11) {
          uVar13 = 0x19;
          if (((ulong)plVar11 | 7) != 0x17) {
            uVar13 = ((ulong)plVar11 | 7) + 1;
          }
          pppppppuVar12 = (undefined8 *******)__Znwm(uVar13);
          local_270 = (undefined1 *)(uVar13 | 0x8000000000000000);
          local_280 = pppppppuVar12;
          local_278 = plVar11;
LAB_02922a28:
          _memmove(pppppppuVar12,pcVar10,(size_t)plVar11);
        }
        else {
          local_270 = (undefined1 *)CONCAT17((char)plVar11,(undefined7)local_270);
          pppppppuVar12 = &local_280;
          if (plVar11 != (long *)0x0) goto LAB_02922a28;
        }
        uVar4 = s_real_xmltotallenfileext_0858c958._0_8_;
        *(undefined1 *)((long)pppppppuVar12 + (long)plVar11) = 0;
        if ((DAT_0a3a6379 & 1) == 0) {
          s_real_xmltotallenfileext_0858c958[0] = (char)uVar3;
          s_real_xmltotallenfileext_0858c958[1] = SUB81(uVar3,1);
          s_real_xmltotallenfileext_0858c958[2] = SUB81(uVar3,2);
          s_real_xmltotallenfileext_0858c958[3] = SUB81(uVar3,3);
          s_real_xmltotallenfileext_0858c958[4] = SUB81(uVar3,4);
          s_real_xmltotallenfileext_0858c958[5] = SUB81(uVar3,5);
          s_real_xmltotallenfileext_0858c958[6] = SUB81(uVar3,6);
          s_real_xmltotallenfileext_0858c958[7] = SUB81(uVar3,7);
          DAT_0a3a6370._0_1_ = s_real_xmltotallenfileext_0858c958[0];
          DAT_0a3a6370._1_1_ = s_real_xmltotallenfileext_0858c958[1];
          DAT_0a3a6370._2_1_ = s_real_xmltotallenfileext_0858c958[2];
          DAT_0a3a6370._3_1_ = s_real_xmltotallenfileext_0858c958[3];
          DAT_0a3a6370._4_1_ = s_real_xmltotallenfileext_0858c958[4];
          DAT_0a3a6370._5_1_ = s_real_xmltotallenfileext_0858c958[5];
          DAT_0a3a6370._6_1_ = s_real_xmltotallenfileext_0858c958[6];
          DAT_0a3a6370._7_1_ = s_real_xmltotallenfileext_0858c958[7];
          DAT_0a3a6378 = 0;
          DAT_0a3a6379 = 1;
        }
        s_real_xmltotallenfileext_0858c958._0_8_ = uVar4;
        plVar11 = (long *)_strlen((char *)&DAT_0a3a6370);
        pppppppuVar12 = local_280;
        if ((long)local_270._7_1_ < 0) {
          if (plVar11 == local_278) {
            if (plVar11 == (long *)0xffffffffffffffff) {
                    /* WARNING: Subroutine does not return */
              FUN_0020edd0(&local_280);
            }
            iVar8 = _memcmp(local_280,&DAT_0a3a6370,(size_t)plVar11);
            __ZdlPvm(pppppppuVar12,(ulong)local_270 & 0x7fffffffffffffff);
            goto joined_r0x02922abc;
          }
          __ZdlPvm(local_280,(ulong)local_270 & 0x7fffffffffffffff);
        }
        else if (plVar11 == (long *)(long)local_270._7_1_) {
          iVar8 = _memcmp(&local_280,&DAT_0a3a6370,(size_t)plVar11);
joined_r0x02922abc:
          pppppppuVar12 = local_1d0;
          if (iVar8 == 0) goto LAB_02922b9c;
        }
        local_280 = (undefined8 *******)FUN_0571c170(&local_1d0);
        lVar7 = FUN_0571cdcc(&local_280);
        if (lVar7 == 0) {
          local_280 = (undefined8 *******)FUN_0571cf98(&local_1d0);
          lVar7 = FUN_0571cdcc(&local_280);
          if (lVar7 == 0) {
            local_280 = (undefined8 *******)FUN_0571cf98(&local_1d0);
            iVar8 = FUN_04af2fcc(&local_280);
            if (iVar8 != 0) {
              do {
                if (local_1d0 == local_150) goto joined_r0x029229a4;
                local_1d0 = (undefined8 *******)FUN_0571cfb0(&local_1d0);
                local_280 = (undefined8 *******)FUN_0571cf98(&local_1d0);
                uVar13 = FUN_04af2fcc(&local_280);
              } while ((uVar13 & 1) != 0);
            }
            if (local_1d0 != local_150) {
              local_1d0 = (undefined8 *******)FUN_0571cf98(&local_1d0);
            }
          }
          else {
            local_1d0 = (undefined8 *******)FUN_0571cf98(&local_1d0);
          }
        }
        else {
          local_1d0 = (undefined8 *******)FUN_0571c170(&local_1d0);
        }
      } while( true );
    }
    FUN_00033b60(&local_280);
    pppppppuVar12 = local_280;
    goto LAB_02922b9c;
  }
LAB_02922f84:
  plVar11 = (long *)__Znwm(0x28);
  plVar9 = plVar11 + 1;
  *plVar9 = 0;
  plVar11[2] = 0;
  plVar16 = plVar11 + 3;
  *plVar16 = 0;
  *plVar11 = (long)&PTR_FUN_09db4418;
  plVar11[4] = 0;
  local_1f8 = plVar16;
  local_1f0 = plVar11;
  FUN_00033c7c(plVar11 + 4,param_5);
  FUN_0466aca8(&local_1e0);
  FUN_01205740(&local_1d0,local_1e0);
  FUN_026870f0(&local_280,local_1d0);
  if (plVar11 != (long *)0x0) {
    *plVar9 = *plVar9 + 1;
  }
  local_170 = &PTR_FUN_09db4468;
  local_250 = 0;
  uStack_248 = 0;
  plStack_168 = plVar16;
  local_160 = plVar11;
  local_158 = &local_170;
  FUN_028562e4(local_280,&local_170);
  if (local_158 == &local_170) {
    pcVar15 = (code *)(*local_158)[4];
LAB_02923034:
    (*pcVar15)();
  }
  else if (local_158 != (undefined ***)0x0) {
    pcVar15 = (code *)(*local_158)[5];
    goto LAB_02923034;
  }
  plVar11 = local_278;
  if (local_278 != (long *)0x0) {
    LOAcquire();
    lVar7 = local_278[1];
    local_278[1] = lVar7 + -1;
    LORelease();
    if (lVar7 == 0) {
      (**(code **)(*local_278 + 0x10))(local_278);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar11);
    }
  }
  plVar11 = plStack_1c8;
  if (plStack_1c8 != (long *)0x0) {
    LOAcquire();
    lVar7 = plStack_1c8[1];
    plStack_1c8[1] = lVar7 + -1;
    LORelease();
    if (lVar7 == 0) {
      (**(code **)(*plStack_1c8 + 0x10))(plStack_1c8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar11);
    }
  }
  plVar11 = local_1d8;
  if (local_1d8 != (long *)0x0) {
    LOAcquire();
    lVar7 = local_1d8[1];
    local_1d8[1] = lVar7 + -1;
    LORelease();
    if (lVar7 == 0) {
      (**(code **)(*local_1d8 + 0x10))(local_1d8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar11);
    }
  }
  plStack_1c8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_1c0 = &SUB_aaaaaaaaaaaaaaaa;
  local_1d0 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
  if (*(char *)((long)param_2 + 0x17) < '\0') {
    FUN_00018d20(&local_1d0,*param_2,param_2[1]);
  }
  else {
    plStack_1c8 = (long *)param_2[1];
    local_1d0 = (undefined8 *******)*param_2;
    local_1c0 = (undefined1 *)param_2[2];
  }
  FUN_04669774();
  FUN_0466ad74(&local_1e0);
  puVar6 = local_1e0;
  if ((DAT_0a3a5f37 & 1) == 0) {
    _DAT_0a3a5f20 = CONCAT44((int)ram0x0854dd68,(int)DAT_08824be0);
    uRam000000000a3a5f28 = CONCAT44((int)DAT_08824bf0,(int)DAT_08824be8);
    DAT_0a3a5f30 = (undefined4)DAT_084e4730;
    DAT_0a3a5f34 = 0x6472;
    DAT_0a3a5f36 = 0;
    DAT_0a3a5f37 = 1;
  }
  if ((DAT_0a3a5b2d & 1) == 0) {
    uVar13 = 0;
    do {
      uVar17 = *(undefined4 *)((long)&DAT_0882629d + uVar13);
      uVar2 = CONCAT12((char)((uint)uVar17 >> 8),(short)uVar17) & 0xff00ff;
      uVar1 = *(undefined4 *)((long)&DAT_08826289 + uVar13 % 0x14);
      *(uint *)((long)&DAT_0a3a5aa0 + uVar13) =
           CONCAT13((char)((uint)uVar17 >> 0x18) + 0x8aU ^ (byte)((uint)uVar1 >> 0x18),
                    CONCAT12((char)((uint)uVar17 >> 0x10) + 0x8aU ^ (byte)((uint)uVar1 >> 0x10),
                             CONCAT11((char)(uVar2 >> 0x10) + 0x8aU ^ (byte)((uint)uVar1 >> 8),
                                      (char)uVar2 + 0x8aU ^ (byte)uVar1)));
      uVar13 = uVar13 + 4;
    } while (uVar13 != 0x8c);
    DAT_0a3a5b2c = 0;
    DAT_0a3a5b2d = 1;
  }
  FUN_0003bb6c(&local_280,&DAT_0a3a5f20,&DAT_0a3a5aa0,0x3a5);
  plVar9 = local_1f0;
  plVar11 = local_1f8;
  if (local_1f0 != (long *)0x0) {
    local_1f0[1] = local_1f0[1] + 1;
  }
  if (*(char *)((long)param_4 + 0x17) < '\0') {
    FUN_00018d20(&local_2c0,*param_4,param_4[1]);
  }
  else {
    lStack_2b8 = param_4[1];
    local_2c0 = *param_4;
    local_2b0 = param_4[2];
  }
  local_2a8 = local_1a0;
  plStack_2a0 = local_198;
  if (local_198 != (long *)0x0) {
    local_198[1] = local_198[1] + 1;
  }
  if ((long)local_1c0 < 0) {
    FUN_00018d20(&local_298,local_1d0,plStack_1c8);
  }
  else {
    puStack_290 = (undefined1 *)plStack_1c8;
    local_298 = local_1d0;
    local_288 = local_1c0;
  }
  local_178 = (long *)0x0;
  plVar16 = (long *)__Znwm(0x58);
  *plVar16 = (long)&PTR_FUN_09db44e8;
  plVar16[2] = (long)plVar9;
  plVar16[1] = (long)plVar11;
  if ((long)local_2b0 < 0) {
    FUN_00018d20(plVar16 + 3,local_2c0,lStack_2b8);
  }
  else {
    plVar16[4] = lStack_2b8;
    plVar16[3] = local_2c0;
    plVar16[5] = local_2b0;
  }
  plVar11 = plStack_2a0;
  puVar5 = local_2a8;
  local_2a8 = (undefined1 *)0x0;
  plStack_2a0 = (long *)0x0;
  plVar16[7] = (long)plVar11;
  plVar16[6] = (long)puVar5;
  plVar16[9] = (long)puStack_290;
  plVar16[8] = (long)local_298;
  plVar16[10] = (long)local_288;
  local_298 = (undefined8 ******)0x0;
  puStack_290 = (undefined1 *)0x0;
  local_288 = (undefined1 *)0x0;
  local_178 = plVar16;
  FUN_0453cce8(auStack_260,puVar6,&local_280,alStack_190,1);
  if (local_258 != (long *)0x0) {
    LOAcquire();
    lVar7 = local_258[1];
    local_258[1] = lVar7 + -1;
    LORelease();
    if (lVar7 == 0) {
      (**(code **)(*local_258 + 0x10))(local_258);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_258);
    }
  }
  if (local_178 == alStack_190) {
    pcVar15 = *(code **)(*local_178 + 0x20);
  }
  else {
    if (local_178 == (long *)0x0) goto LAB_02923380;
    pcVar15 = *(code **)(*local_178 + 0x28);
  }
  (*pcVar15)();
LAB_02923380:
  plVar11 = plStack_2a0;
  if ((long)local_288 < 0) {
    __ZdlPvm(local_298,(ulong)local_288 & 0x7fffffffffffffff);
    plVar11 = plStack_2a0;
  }
  plStack_2a0 = plVar11;
  if (plVar11 != (long *)0x0) {
    LOAcquire();
    lVar7 = plVar11[1];
    plVar11[1] = lVar7 + -1;
    LORelease();
    if (lVar7 == 0) {
      (**(code **)(*plVar11 + 0x10))(plVar11);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar11);
    }
  }
  if ((long)local_2b0 < 0) {
    __ZdlPvm(local_2c0,local_2b0 & 0x7fffffffffffffff);
  }
  plVar11 = local_1d8;
  if (local_1d8 != (long *)0x0) {
    LOAcquire();
    lVar7 = local_1d8[1];
    local_1d8[1] = lVar7 + -1;
    LORelease();
    if (lVar7 == 0) {
      (**(code **)(*local_1d8 + 0x10))(local_1d8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar11);
    }
  }
  if ((long)local_1c0 < 0) {
    __ZdlPvm(local_1d0,(ulong)local_1c0 & 0x7fffffffffffffff);
  }
  plVar11 = local_1f0;
  if (local_1f0 != (long *)0x0) {
    LOAcquire();
    lVar7 = local_1f0[1];
    local_1f0[1] = lVar7 + -1;
    LORelease();
    if (lVar7 == 0) {
      (**(code **)(*local_1f0 + 0x10))(local_1f0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar11);
    }
  }
  FUN_0572116c(&local_150);
  plVar11 = local_1a8;
  if (local_1a8 != (long *)0x0) {
    LOAcquire();
    lVar7 = local_1a8[1];
    local_1a8[1] = lVar7 + -1;
    LORelease();
    if (lVar7 == 0) {
      (**(code **)(*local_1a8 + 0x10))(local_1a8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar11);
    }
  }
  plVar11 = local_198;
  if (local_198 != (long *)0x0) {
    LOAcquire();
    lVar7 = local_198[1];
    local_198[1] = lVar7 + -1;
    LORelease();
    if (lVar7 == 0) {
      (**(code **)(*local_198 + 0x10))(local_198);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar11);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_80) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
LAB_02922b88:
  FUN_00033b60(&local_280);
  pppppppuVar12 = local_280;
LAB_02922b9c:
  local_280 = pppppppuVar12;
  local_1b8 = local_280;
  uVar13 = FUN_04af2fcc(&local_1b8);
  plVar11 = local_1b0;
  if ((uVar13 & 1) == 0) {
    if ((DAT_0a3a5c0e & 1) == 0) {
      DAT_0a3a5c08 = (undefined4)DAT_08495920;
      DAT_0a3a5c0c = 0x65;
      DAT_0a3a5c0e = 1;
    }
    FUN_0571ce74(&local_1b8,&DAT_0a3a5c08);
    FUN_04bd7f04(&local_280);
    FUN_012a58d8(plVar11,&local_280);
    if ((long)local_270 < 0) {
      __ZdlPvm(local_280,(ulong)local_270 & 0x7fffffffffffffff);
    }
    local_278 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    local_270 = &SUB_aaaaaaaaaaaaaaaa;
    local_280 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
    if ((DAT_0a3a5e50 & 1) == 0) {
      DAT_0a3a5e48[0] = s_iconUrl_0858ec10[0];
      DAT_0a3a5e48[1] = s_iconUrl_0858ec10[1];
      DAT_0a3a5e48[2] = s_iconUrl_0858ec10[2];
      DAT_0a3a5e48[3] = s_iconUrl_0858ec10[3];
      DAT_0a3a5e48[4] = s_iconUrl_0858ec10[4];
      DAT_0a3a5e48[5] = s_iconUrl_0858ec10[5];
      DAT_0a3a5e48[6] = s_iconUrl_0858ec10[6];
      DAT_0a3a5e48[7] = s_iconUrl_0858ec10[7];
      DAT_0a3a5e50 = 1;
    }
    FUN_0571ce74(&local_1b8,DAT_0a3a5e48);
    FUN_04bd7f04(&local_280);
    plVar9 = local_278;
    if (-1 < (long)local_270) {
      plVar9 = (long *)((ulong)local_270 >> 0x38);
    }
    if (plVar9 != (long *)0x0) {
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(plVar11,&local_280);
      FUN_04d1b3b8(plVar11,&local_280);
    }
    if ((DAT_0a3a5e71 & 1) == 0) {
      DAT_0a3a5e68._0_1_ = s_objectIdobjectNofeedTypebizUsern_08798420[0x38];
      DAT_0a3a5e68._1_1_ = s_objectIdobjectNofeedTypebizUsern_08798420[0x39];
      DAT_0a3a5e68._2_1_ = s_objectIdobjectNofeedTypebizUsern_08798420[0x3a];
      DAT_0a3a5e68._3_1_ = s_objectIdobjectNofeedTypebizUsern_08798420[0x3b];
      DAT_0a3a5e68._4_1_ = s_objectIdobjectNofeedTypebizUsern_08798420[0x3c];
      DAT_0a3a5e68._5_1_ = s_objectIdobjectNofeedTypebizUsern_08798420[0x3d];
      DAT_0a3a5e68._6_1_ = s_objectIdobjectNofeedTypebizUsern_08798420[0x3e];
      DAT_0a3a5e68._7_1_ = s_objectIdobjectNofeedTypebizUsern_08798420[0x3f];
      DAT_0a3a5e70 = 0;
      DAT_0a3a5e71 = 1;
    }
    FUN_0571ce74(&local_1b8,&DAT_0a3a5e68);
    FUN_04bd7f04(&local_1d0);
    FUN_04d1b3b0(plVar11,&local_1d0);
    if ((long)local_1c0 < 0) {
      __ZdlPvm(local_1d0,(ulong)local_1c0 & 0x7fffffffffffffff);
    }
    plStack_1c8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    local_1c0 = &SUB_aaaaaaaaaaaaaaaa;
    local_1d0 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
    if ((DAT_0a3a5e83 & 1) == 0) {
      DAT_0a3a5e78._0_1_ = s_jsapiParencryptUchxm_0858e678[0];
      DAT_0a3a5e78._1_1_ = s_jsapiParencryptUchxm_0858e678[1];
      DAT_0a3a5e78._2_1_ = s_jsapiParencryptUchxm_0858e678[2];
      DAT_0a3a5e78._3_1_ = s_jsapiParencryptUchxm_0858e678[3];
      DAT_0a3a5e78._4_1_ = s_jsapiParencryptUchxm_0858e678[4];
      DAT_0a3a5e78._5_1_ = s_jsapiParencryptUchxm_0858e678[5];
      DAT_0a3a5e78._6_1_ = s_jsapiParencryptUchxm_0858e678[6];
      DAT_0a3a5e78._7_1_ = s_jsapiParencryptUchxm_0858e678[7];
      DAT_0a3a5e80 = 0x6d61;
      DAT_0a3a5e82 = 0;
      DAT_0a3a5e83 = 1;
    }
    FUN_0571ce74(&local_1b8,&DAT_0a3a5e78);
    FUN_04bd7f04(&local_1d0);
    uVar14 = (uint)(char)local_1c0._7_1_;
    plVar9 = plStack_1c8;
    if (-1 < (int)uVar14) {
      plVar9 = (long *)(ulong)local_1c0._7_1_;
    }
    if (plVar9 != (long *)0x0) {
      local_1e0 = &SUB_aaaaaaaaaaaaaaaa;
      local_1d8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
      FUN_04878be8(&local_1e0,&local_1d0);
      if ((char)local_1e0 == '\t') {
        uVar13 = 9;
      }
      else {
        cStack_1f9 = '\0';
        local_210 = 0;
        if ((DAT_0a3a5ef9 & 1) == 0) {
          DAT_0a3a5ef0._0_1_ = s_userNamepagePathOpenProfbiz_menu_08542d48[0];
          DAT_0a3a5ef0._1_1_ = s_userNamepagePathOpenProfbiz_menu_08542d48[1];
          DAT_0a3a5ef0._2_1_ = s_userNamepagePathOpenProfbiz_menu_08542d48[2];
          DAT_0a3a5ef0._3_1_ = s_userNamepagePathOpenProfbiz_menu_08542d48[3];
          DAT_0a3a5ef0._4_1_ = s_userNamepagePathOpenProfbiz_menu_08542d48[4];
          DAT_0a3a5ef0._5_1_ = s_userNamepagePathOpenProfbiz_menu_08542d48[5];
          DAT_0a3a5ef0._6_1_ = s_userNamepagePathOpenProfbiz_menu_08542d48[6];
          DAT_0a3a5ef0._7_1_ = s_userNamepagePathOpenProfbiz_menu_08542d48[7];
          DAT_0a3a5ef8 = 0;
          DAT_0a3a5ef9 = 1;
        }
        FUN_0487929c(&local_1f8,&local_1e0,&DAT_0a3a5ef0,&local_210);
        FUN_017b5a0c(plVar11,&local_1f8);
        if ((long)local_1e8 < 0) {
          __ZdlPvm(local_1f8,(ulong)local_1e8 & 0x7fffffffffffffff);
        }
        if (cStack_1f9 < '\0') {
          __ZdlPvm(CONCAT71(uStack_20f,local_210),
                   CONCAT17(cStack_1f9,local_200) & 0x7fffffffffffffff);
        }
        cStack_211 = '\0';
        local_228 = 0;
        if ((DAT_0a3a5f0a & 1) == 0) {
          DAT_0a3a5f00._0_1_ = s_aliasNamheadHDImgUrl_08824bc8[0];
          DAT_0a3a5f00._1_1_ = s_aliasNamheadHDImgUrl_08824bc8[1];
          DAT_0a3a5f00._2_1_ = s_aliasNamheadHDImgUrl_08824bc8[2];
          DAT_0a3a5f00._3_1_ = s_aliasNamheadHDImgUrl_08824bc8[3];
          DAT_0a3a5f00._4_1_ = s_aliasNamheadHDImgUrl_08824bc8[4];
          DAT_0a3a5f00._5_1_ = s_aliasNamheadHDImgUrl_08824bc8[5];
          DAT_0a3a5f00._6_1_ = s_aliasNamheadHDImgUrl_08824bc8[6];
          DAT_0a3a5f00._7_1_ = s_aliasNamheadHDImgUrl_08824bc8[7];
          DAT_0a3a5f08 = 0x65;
          DAT_0a3a5f0a = 1;
        }
        FUN_0487929c(&local_1f8,&local_1e0,&DAT_0a3a5f00,&local_228);
        FUN_017b5a24(plVar11,&local_1f8);
        if ((long)local_1e8 < 0) {
          __ZdlPvm(local_1f8,(ulong)local_1e8 & 0x7fffffffffffffff);
        }
        if (cStack_211 < '\0') {
          __ZdlPvm(CONCAT71(uStack_227,local_228),
                   CONCAT17(cStack_211,local_218) & 0x7fffffffffffffff);
        }
        local_1f0 = (long *)&SUB_aaaaaaaaaaaaaaaa;
        local_1e8 = &SUB_aaaaaaaaaaaaaaaa;
        local_1f8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
        cStack_229 = '\0';
        local_240 = 0;
        if ((DAT_0a3a5f1d & 1) == 0) {
          DAT_0a3a5f10._0_1_ = s_aliasNamheadHDImgUrl_08824bc8[8];
          DAT_0a3a5f10._1_1_ = s_aliasNamheadHDImgUrl_08824bc8[9];
          DAT_0a3a5f10._2_1_ = s_aliasNamheadHDImgUrl_08824bc8[10];
          DAT_0a3a5f10._3_1_ = s_aliasNamheadHDImgUrl_08824bc8[0xb];
          DAT_0a3a5f10._4_1_ = s_aliasNamheadHDImgUrl_08824bc8[0xc];
          DAT_0a3a5f10._5_1_ = s_aliasNamheadHDImgUrl_08824bc8[0xd];
          DAT_0a3a5f10._6_1_ = s_aliasNamheadHDImgUrl_08824bc8[0xe];
          DAT_0a3a5f10._7_1_ = s_aliasNamheadHDImgUrl_08824bc8[0xf];
          DAT_0a3a5f18 = (undefined4)ram0x08824bd8;
          DAT_0a3a5f1c = 0;
          DAT_0a3a5f1d = 1;
        }
        FUN_0487929c(&local_1f8,&local_1e0,&DAT_0a3a5f10,&local_240);
        if (cStack_229 < '\0') {
          __ZdlPvm(CONCAT71(uStack_23f,local_240),
                   CONCAT17(cStack_229,local_230) & 0x7fffffffffffffff);
        }
        uVar14 = (uint)(char)local_1e8._7_1_;
        plVar9 = local_1f0;
        if (-1 < (int)uVar14) {
          plVar9 = (long *)(ulong)local_1e8._7_1_;
        }
        if (plVar9 != (long *)0x0) {
          FUN_013a5688(plVar11,&local_1f8);
          uVar14 = (uint)local_1e8._7_1_;
        }
        if ((uVar14 >> 7 & 1) != 0) {
          __ZdlPvm(local_1f8,(ulong)local_1e8 & 0x7fffffffffffffff);
        }
        uVar13 = (ulong)local_1e0 & 0xff;
      }
      FUN_001fa1c8(&local_1d8,uVar13);
      uVar14 = (uint)local_1c0._7_1_;
    }
    if ((uVar14 >> 7 & 1) != 0) {
      __ZdlPvm(local_1d0,(ulong)local_1c0 & 0x7fffffffffffffff);
    }
    if ((long)local_270 < 0) {
      __ZdlPvm(local_280,(ulong)local_270 & 0x7fffffffffffffff);
    }
  }
  goto LAB_02922f84;
}


