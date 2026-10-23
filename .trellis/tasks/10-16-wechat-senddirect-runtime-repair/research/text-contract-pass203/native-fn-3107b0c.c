// Ghidra inferred pseudocode; requested=0x3107b0c
// entry=03107b0c end=0310973f

/* WARNING: Removing unreachable block (ram,0x03108b10) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_03107b0c(long *param_1,undefined8 param_2,long *param_3)

{
  undefined1 uVar1;
  uint3 uVar2;
  long *plVar3;
  bool bVar4;
  long lVar5;
  int iVar6;
  long lVar7;
  undefined8 *puVar8;
  undefined8 uVar9;
  undefined8 *******pppppppuVar10;
  char cVar11;
  undefined1 *puVar12;
  undefined1 *puVar13;
  undefined1 *puVar14;
  uint uVar15;
  ulong uVar16;
  long lVar17;
  ulong uVar18;
  int iVar19;
  long lVar20;
  long *plVar21;
  long lVar22;
  undefined4 uVar23;
  undefined4 uVar24;
  long local_3b0;
  long *local_3a8;
  undefined8 *******local_3a0 [2];
  undefined7 local_390;
  char cStack_389;
  undefined8 *******local_388 [2];
  undefined7 local_378;
  char cStack_371;
  undefined8 local_370;
  undefined1 *puStack_368;
  undefined1 *local_360;
  undefined1 *puStack_358;
  undefined1 *local_350;
  long *local_348;
  undefined8 *******local_340;
  undefined1 *puStack_338;
  undefined8 local_330;
  undefined1 *puStack_328;
  undefined1 *local_320;
  undefined1 *local_318;
  long local_308;
  long *local_300;
  long local_2f8;
  undefined8 local_2f0;
  ulong local_2e8;
  ulong local_2e0;
  uint local_2d8;
  undefined4 uStack_2d4;
  long *local_2d0;
  long local_268;
  long *local_260;
  undefined1 *local_258;
  undefined1 *local_250;
  undefined1 *local_248;
  long local_240;
  long *local_238;
  undefined8 local_230;
  undefined8 uStack_228;
  undefined1 *local_220;
  undefined1 *puStack_218;
  long *local_210;
  long *local_208;
  undefined1 uStack_1d9;
  undefined8 local_1d8;
  undefined8 local_1d0;
  undefined7 local_1c8;
  char cStack_1c1;
  undefined1 uStack_189;
  undefined8 local_188;
  undefined1 local_180 [72];
  undefined8 *******local_138;
  undefined1 local_130;
  undefined8 *******local_e8;
  undefined8 *puStack_e0;
  undefined8 *local_d8;
  undefined8 *puStack_d0;
  undefined8 uStack_c8;
  undefined8 uStack_c0;
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
  lVar7 = *param_3;
  lVar5 = *(long *)(lVar7 + 0x18);
  local_238 = *(long **)(lVar7 + 0x20);
  if (local_238 != (long *)0x0) {
    local_238[1] = local_238[1] + 1;
    lVar7 = *param_3;
  }
  local_250 = &SUB_aaaaaaaaaaaaaaaa;
  local_248 = &SUB_aaaaaaaaaaaaaaaa;
  local_258 = &SUB_aaaaaaaaaaaaaaaa;
  local_240 = lVar5;
  FUN_030f1d74(&local_258,lVar7);
  param_1[3] = (long)&SUB_aaaaaaaaaaaaaaaa;
  param_1[2] = (long)&SUB_aaaaaaaaaaaaaaaa;
  param_1[5] = (long)&SUB_aaaaaaaaaaaaaaaa;
  param_1[4] = (long)&SUB_aaaaaaaaaaaaaaaa;
  param_1[1] = (long)&SUB_aaaaaaaaaaaaaaaa;
  *param_1 = (long)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0304f1cc(param_1,0,0);
  iVar6 = FUN_04bb6cd4(&local_258);
  if (iVar6 != 0) {
    puStack_218 = &SUB_aaaaaaaaaaaaaaaa;
    local_220 = &SUB_aaaaaaaaaaaaaaaa;
    local_208 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    local_210 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    uStack_228 = (undefined8 ******)&SUB_aaaaaaaaaaaaaaaa;
    local_230 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
    local_268 = *param_3;
    local_260 = (long *)param_3[1];
    if (local_260 != (long *)0x0) {
      local_260[1] = local_260[1] + 1;
    }
    FUN_02849004(&local_230,0x18,&local_268);
    plVar21 = local_260;
    if (local_260 != (long *)0x0) {
      LOAcquire();
      lVar5 = local_260[1];
      local_260[1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*local_260 + 0x10))(local_260);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar21);
      }
    }
    lVar5 = local_240;
    if ((int)local_230 == 0 && local_230._4_4_ == 0) {
      *(undefined4 *)(local_240 + 0x118) = 2;
      *(long *)(local_240 + 0xf8) = *local_210;
      iVar6 = thunk_FUN_05e1d97c(2);
      local_308 = lVar5;
      if (iVar6 != 0) {
        FUN_0488143c(&local_340);
        pppppppuVar10 = local_340;
        if (-1 < (long)local_330) {
          pppppppuVar10 = &local_340;
        }
        if ((DAT_0a3da318 & 1) == 0) {
          _DAT_0a3da300 = CONCAT44((int)DAT_084a66a8,(int)DAT_0849a618);
          uRam000000000a3da308 = CONCAT44((int)DAT_0875a898,(int)DAT_084a66b0);
          DAT_0a3da310 = CONCAT44((int)DAT_084c8608,(int)DAT_084d88d0);
          DAT_0a3da318 = 1;
        }
        if ((DAT_0a3da494 & 1) == 0) {
          _DAT_0a3da478 = CONCAT44((int)DAT_088a7260,(int)DAT_087e2f50);
          uRam000000000a3da480 = CONCAT44((int)DAT_08485e90,(int)DAT_084a8110);
          DAT_0a3da488 = CONCAT44((int)DAT_0863e0f0,(int)DAT_088a7268);
          DAT_0a3da490 = (undefined4)DAT_0847fdb8;
          DAT_0a3da494 = 1;
        }
        FUN_05e1d050(&local_2f8,2,pppppppuVar10,&DAT_0a3da300,&DAT_0a3da478,0x8e,0,0);
        lVar5 = local_240;
        FUN_04cbe440(&local_370,local_240);
        local_138 = local_370;
        if (-1 < (long)local_360) {
          local_138 = (undefined8 *******)&local_370;
        }
        local_130 = 0;
        lVar7 = *local_210;
        local_188 = (undefined1 *)0x0;
        if ((DAT_0a3da6d9 & 1) == 0) {
          uVar16 = 0;
          do {
            uVar23 = *(undefined4 *)((long)&DAT_088b337c + uVar16);
            uVar2 = CONCAT12((char)((uint)uVar23 >> 8),(short)uVar23) & 0xff00ff;
            uVar24 = *(undefined4 *)((long)&DAT_088b3368 + uVar16 % 0x14);
            *(uint *)((long)&DAT_0a3da691 + uVar16) =
                 CONCAT13((char)((uint)uVar23 >> 0x18) + 0x8aU ^ (byte)((uint)uVar24 >> 0x18),
                          CONCAT12((char)((uint)uVar23 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar24 >> 0x10),
                                   CONCAT11((char)(uVar2 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar24 >> 8),
                                            (char)uVar2 + 0x8aU ^ (byte)uVar24)));
            uVar16 = uVar16 + 4;
          } while (uVar16 != 0x48);
          DAT_0a3da6d9 = 1;
        }
        lVar22 = 8;
        lVar20 = lVar7;
        do {
          lVar17 = lVar22;
          local_180[lVar17 + -8] = *(undefined1 *)(lVar20 % 10 + 0xa3da6b4);
          lVar22 = lVar17 + 1;
          uVar16 = lVar20 + 9;
          lVar20 = lVar20 / 10;
        } while (0x12 < uVar16);
        if (lVar7 < 0) {
          local_180[lVar17 + -7] = 0x2d;
          lVar22 = lVar17 + 2;
        }
        local_180[lVar22 + -8] = 0;
        if (9 < lVar22) {
          puVar12 = local_180;
          puVar13 = &uStack_189 + lVar22;
          do {
            puVar12 = puVar12 + 1;
            uVar1 = *puVar13;
            puVar14 = puVar13 + -1;
            *puVar13 = puVar12[-1];
            puVar12[-1] = uVar1;
            puVar13 = puVar14;
          } while (puVar12 < puVar14);
        }
        local_188 = local_180;
        local_1d8 = (undefined8 *******)0x0;
        local_1d8 = (undefined8 *******)&local_1d0;
        lVar7 = 0;
        uVar16 = (ulong)*(uint *)(lVar5 + 0x114);
        do {
          lVar22 = lVar7;
          uVar15 = (uint)uVar16;
          *(undefined1 *)((long)&local_1d0 + lVar22) =
               *(undefined1 *)
                ((long)&DAT_0a3da691 + (ulong)(uVar15 + (int)(uVar16 / 10) * -10 + 0x23));
          lVar7 = lVar22 + 1;
          uVar16 = uVar16 / 10;
        } while (9 < uVar15);
        *(undefined1 *)((long)&local_1d0 + lVar22 + 1) = 0;
        if (8 < lVar22 + 8U) {
          puVar12 = (undefined1 *)((long)&local_1d0 + lVar22);
          puVar13 = (undefined1 *)((long)&local_1d0 + 1);
          do {
            uVar1 = *puVar12;
            *puVar12 = puVar13[-1];
            puVar13[-1] = uVar1;
            bVar4 = puVar13 < puVar12 + -1;
            puVar12 = puVar12 + -1;
            puVar13 = puVar13 + 1;
          } while (bVar4);
        }
        if ((DAT_0a3da4cf & 1) == 0) {
          uVar16 = 0;
          do {
            uVar23 = *(undefined4 *)((long)&DAT_088b2ffe + uVar16);
            uVar2 = CONCAT12((char)((uint)uVar23 >> 8),(short)uVar23) & 0xff00ff;
            uVar24 = *(undefined4 *)((long)&DAT_088b2fea + uVar16 % 0x14);
            *(uint *)((long)&DAT_0a3da495 + uVar16) =
                 CONCAT13((char)((uint)uVar23 >> 0x18) + 0x8aU ^ (byte)((uint)uVar24 >> 0x18),
                          CONCAT12((char)((uint)uVar23 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar24 >> 0x10),
                                   CONCAT11((char)(uVar2 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar24 >> 8),
                                            (char)uVar2 + 0x8aU ^ (byte)uVar24)));
            uVar16 = uVar16 + 4;
          } while (uVar16 != 0x38);
          DAT_0a3da4cd = 0x5f;
          DAT_0a3da4cf = 1;
        }
        local_e8 = &local_138;
        puStack_e0 = &local_188;
        local_d8 = &local_1d8;
        uStack_c8 = 0;
        puStack_d0 = (undefined8 *)0x0;
        uStack_b8 = 0;
        uStack_c0 = 0;
        uStack_a8 = 0;
        local_b0 = 0;
        uStack_98 = 0;
        local_a0 = 0;
        uStack_88 = 0;
        local_90 = 0;
        uStack_78 = 0;
        local_80 = 0;
        local_70 = 0;
        FUN_05e1d31c(&local_2f8,&DAT_0a3da495,&local_e8);
LAB_0310852c:
        if ((long)local_360 < 0) {
          __ZdlPvm(local_370,(ulong)local_360 & 0x7fffffffffffffff);
        }
        thunk_FUN_05e1d0bc(&local_2f8);
        local_308 = lVar5;
        if ((long)local_330 < 0) {
          __ZdlPvm(local_340,(ulong)local_330 & 0x7fffffffffffffff);
        }
      }
    }
    else {
      *(undefined4 *)(local_240 + 0x118) = 5;
      FUN_030f6650(&local_2f8,3,0xc,(int)*param_1,*(undefined4 *)((long)param_1 + 4));
      *param_1 = local_2f8;
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (param_1 + 1,&local_2f0);
      if (local_2d0 != (long *)0x0) {
        local_2d0[1] = local_2d0[1] + 1;
      }
      plVar21 = (long *)param_1[5];
      param_1[4] = CONCAT44(uStack_2d4,local_2d8);
      param_1[5] = (long)local_2d0;
      if (plVar21 != (long *)0x0) {
        LOAcquire();
        lVar5 = plVar21[1];
        plVar21[1] = lVar5 + -1;
        LORelease();
        if (lVar5 == 0) {
          (**(code **)(*plVar21 + 0x10))(plVar21);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar21);
        }
      }
      if (local_2d0 != (long *)0x0) {
        LOAcquire();
        lVar5 = local_2d0[1];
        local_2d0[1] = lVar5 + -1;
        LORelease();
        if (lVar5 == 0) {
          (**(code **)(*local_2d0 + 0x10))(local_2d0);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_2d0);
        }
      }
      if ((long)local_2e0 < 0) {
        __ZdlPvm(local_2f0,local_2e0 & 0x7fffffffffffffff);
      }
      iVar6 = thunk_FUN_05e1d97c(4);
      local_308 = local_240;
      if (iVar6 != 0) {
        FUN_0488143c(&local_340);
        pppppppuVar10 = local_340;
        if (-1 < (long)local_330) {
          pppppppuVar10 = &local_340;
        }
        if ((DAT_0a3da318 & 1) == 0) {
          _DAT_0a3da300 = CONCAT44((int)DAT_084a66a8,(int)DAT_0849a618);
          uRam000000000a3da308 = CONCAT44((int)DAT_0875a898,(int)DAT_084a66b0);
          DAT_0a3da310 = CONCAT44((int)DAT_084c8608,(int)DAT_084d88d0);
          DAT_0a3da318 = 1;
        }
        if ((DAT_0a3da494 & 1) == 0) {
          _DAT_0a3da478 = CONCAT44((int)DAT_088a7260,(int)DAT_087e2f50);
          uRam000000000a3da480 = CONCAT44((int)DAT_08485e90,(int)DAT_084a8110);
          DAT_0a3da488 = CONCAT44((int)DAT_0863e0f0,(int)DAT_088a7268);
          DAT_0a3da490 = (undefined4)DAT_0847fdb8;
          DAT_0a3da494 = 1;
        }
        FUN_05e1d050(&local_2f8,4,pppppppuVar10,&DAT_0a3da300,&DAT_0a3da478,0x92,0,0);
        lVar5 = local_240;
        FUN_04cbe440(&local_370,local_240);
        local_138 = local_370;
        if (-1 < (long)local_360) {
          local_138 = (undefined8 *******)&local_370;
        }
        local_130 = 0;
        local_188 = (undefined1 *)0x0;
        if ((DAT_0a3da6d9 & 1) == 0) {
          uVar16 = 0;
          do {
            uVar23 = *(undefined4 *)((long)&DAT_088b337c + uVar16);
            uVar2 = CONCAT12((char)((uint)uVar23 >> 8),(short)uVar23) & 0xff00ff;
            uVar24 = *(undefined4 *)((long)&DAT_088b3368 + uVar16 % 0x14);
            *(uint *)((long)&DAT_0a3da691 + uVar16) =
                 CONCAT13((char)((uint)uVar23 >> 0x18) + 0x8aU ^ (byte)((uint)uVar24 >> 0x18),
                          CONCAT12((char)((uint)uVar23 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar24 >> 0x10),
                                   CONCAT11((char)(uVar2 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar24 >> 8),
                                            (char)uVar2 + 0x8aU ^ (byte)uVar24)));
            uVar16 = uVar16 + 4;
          } while (uVar16 != 0x48);
          DAT_0a3da6d9 = 1;
        }
        lVar7 = 8;
        iVar6 = (int)local_230;
        do {
          lVar22 = lVar7;
          local_180[lVar22 + -8] = *(undefined1 *)((long)&DAT_0a3da691 + (long)(iVar6 % 10 + 0x23));
          lVar7 = lVar22 + 1;
          uVar15 = iVar6 + 9;
          iVar6 = iVar6 / 10;
        } while (0x12 < uVar15);
        if ((int)local_230 < 0) {
          local_180[lVar22 + -7] = 0x2d;
          lVar7 = lVar22 + 2;
        }
        local_180[lVar7 + -8] = 0;
        if (9 < lVar7) {
          puVar12 = local_180;
          puVar13 = &uStack_189 + lVar7;
          do {
            puVar12 = puVar12 + 1;
            uVar1 = *puVar13;
            puVar14 = puVar13 + -1;
            *puVar13 = puVar12[-1];
            puVar12[-1] = uVar1;
            puVar13 = puVar14;
          } while (puVar12 < puVar14);
        }
        local_188 = local_180;
        local_1d8 = (undefined8 *******)0x0;
        lVar7 = 8;
        iVar6 = local_230._4_4_;
        do {
          lVar22 = lVar7;
          *(undefined1 *)((long)&local_1d8 + lVar22) =
               *(undefined1 *)((long)&DAT_0a3da691 + (long)(iVar6 % 10 + 0x23));
          lVar7 = lVar22 + 1;
          uVar15 = iVar6 + 9;
          iVar6 = iVar6 / 10;
        } while (0x12 < uVar15);
        if ((long)local_230 < 0) {
          *(undefined1 *)((long)&local_1d8 + lVar22 + 1) = 0x2d;
          lVar7 = lVar22 + 2;
        }
        *(undefined1 *)((long)&local_1d8 + lVar7) = 0;
        if (9 < lVar7) {
          puVar12 = &uStack_1d9 + lVar7;
          puVar13 = (undefined1 *)((long)&local_1d0 + 1);
          do {
            uVar1 = *puVar12;
            *puVar12 = puVar13[-1];
            puVar13[-1] = uVar1;
            bVar4 = puVar13 < puVar12 + -1;
            puVar12 = puVar12 + -1;
            puVar13 = puVar13 + 1;
          } while (bVar4);
        }
        if ((DAT_0a3da500 & 1) == 0) {
          _DAT_0a3da4d0 = CONCAT44((int)DAT_08507730,(int)DAT_0849a618);
          uRam000000000a3da4d8 = CONCAT44((int)DAT_084fdd78,(int)DAT_084a66b0);
          _DAT_0a3da4e0 = CONCAT44((int)DAT_084f5b30,(int)ram0x08487528);
          uRam000000000a3da4e8 = CONCAT44((int)DAT_084ce700,(int)ram0x08480938);
          _DAT_0a3da4f0 = CONCAT44((int)DAT_08486068,(int)DAT_084e3fc8);
          uRam000000000a3da4f8 = CONCAT44((int)DAT_084ca300,(int)ram0x084e4a40);
          DAT_0a3da500 = 1;
        }
        local_e8 = &local_138;
        puStack_e0 = &local_188;
        local_d8 = &local_1d8;
        uStack_c8 = 0;
        puStack_d0 = (undefined8 *)0x0;
        uStack_b8 = 0;
        uStack_c0 = 0;
        uStack_a8 = 0;
        local_b0 = 0;
        uStack_98 = 0;
        local_a0 = 0;
        uStack_88 = 0;
        local_90 = 0;
        uStack_78 = 0;
        local_80 = 0;
        local_70 = 0;
        local_1d8 = (undefined8 *******)&local_1d0;
        FUN_05e1d31c(&local_2f8,&DAT_0a3da4d0,&local_e8);
        goto LAB_0310852c;
      }
    }
    local_300 = local_238;
    lVar5 = 0;
    if (local_238 != (long *)0x0) {
      lVar5 = local_238[1];
      local_238[1] = lVar5 + 1;
    }
    FUN_030daf78(lVar5,param_2,&local_308,1,1);
    plVar3 = local_300;
    plVar21 = local_208;
    if (local_300 != (long *)0x0) {
      LOAcquire();
      lVar5 = local_300[1];
      local_300[1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*local_300 + 0x10))(local_300);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
        plVar21 = local_208;
      }
    }
    local_208 = plVar21;
    if (plVar21 != (long *)0x0) {
      LOAcquire();
      lVar5 = plVar21[1];
      plVar21[1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*plVar21 + 0x10))(plVar21);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar21);
      }
    }
    if ((long)puStack_218 < 0) {
      __ZdlPvm(uStack_228,(ulong)puStack_218 & 0x7fffffffffffffff);
    }
    goto joined_r0x03108bf8;
  }
  puStack_328 = &SUB_aaaaaaaaaaaaaaaa;
  local_330 = &SUB_aaaaaaaaaaaaaaaa;
  local_318 = &SUB_aaaaaaaaaaaaaaaa;
  local_320 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_338 = &SUB_aaaaaaaaaaaaaaaa;
  local_340 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0465bdac(&local_340);
  local_318 = (undefined1 *)((ulong)local_318 | 1);
  local_320 = (undefined1 *)CONCAT44(local_320._4_4_,1);
  lVar7 = (long)(int)local_330;
  if ((int)local_330 < local_330._4_4_) {
    local_330 = (undefined1 *)CONCAT44(local_330._4_4_,(int)local_330 + 1);
    lVar7 = *(long *)(puStack_338 + lVar7 * 8);
  }
  else {
    if (local_330._4_4_ == (int)puStack_328) {
      FUN_05ab4038((ulong)&local_340 | 8,local_330._4_4_ + 1);
    }
    local_330._4_4_ = local_330._4_4_ + 1;
    lVar7 = __Znwm(0x38);
    FUN_0465bd88();
    lVar22 = (long)(int)local_330;
    local_330 = (undefined1 *)CONCAT44(local_330._4_4_,(int)local_330 + 1);
    *(long *)(puStack_338 + lVar22 * 8) = lVar7;
  }
  *(uint *)(lVar7 + 0x34) = *(uint *)(lVar7 + 0x34) | 2;
  puVar8 = *(undefined8 **)(lVar7 + 0x10);
  if (puVar8 == &DAT_0a524ad0) {
    puVar8 = (undefined8 *)__Znwm(0x18);
    *puVar8 = 0;
    puVar8[1] = 0;
    puVar8[2] = 0;
    *(undefined8 **)(lVar7 + 0x10) = puVar8;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar8,lVar5 + 0x130);
  *(uint *)(lVar7 + 0x34) = *(uint *)(lVar7 + 0x34) | 1;
  lVar22 = *(long *)(lVar7 + 8);
  if (lVar22 == 0) {
    lVar22 = __Znwm(0x18);
    FUN_04f33c00();
    *(long *)(lVar7 + 8) = lVar22;
  }
  *(uint *)(lVar22 + 0x14) = *(uint *)(lVar22 + 0x14) | 1;
  puVar8 = *(undefined8 **)(lVar22 + 8);
  if (puVar8 == &DAT_0a524ad0) {
    puVar8 = (undefined8 *)__Znwm(0x18);
    *puVar8 = 0;
    puVar8[1] = 0;
    puVar8[2] = 0;
    *(undefined8 **)(lVar22 + 8) = puVar8;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar8,&local_258);
  uVar23 = *(undefined4 *)(lVar5 + 0xc);
  uVar15 = *(uint *)(lVar7 + 0x34);
  *(uint *)(lVar7 + 0x34) = uVar15 | 4;
  *(undefined4 *)(lVar7 + 0x18) = uVar23;
  uVar23 = *(undefined4 *)(lVar5 + 0x114);
  *(uint *)(lVar7 + 0x34) = uVar15 | 0xc;
  *(undefined4 *)(lVar7 + 0x1c) = uVar23;
  FUN_030f2168(&local_2f8,*param_3);
  uVar23 = FUN_00033fcc(&local_2f8);
  *(uint *)(lVar7 + 0x34) = *(uint *)(lVar7 + 0x34) | 0x10;
  *(undefined4 *)(lVar7 + 0x28) = uVar23;
  if ((long)local_2e8 < 0) {
    __ZdlPvm(local_2f8,local_2e8 & 0x7fffffffffffffff);
    cVar11 = *(char *)(lVar5 + 0x177);
    if (cVar11 < '\0') goto LAB_031086c0;
LAB_031086a0:
    if (cVar11 != '\0') {
LAB_031086c8:
      *(uint *)(lVar7 + 0x34) = *(uint *)(lVar7 + 0x34) | 0x20;
      puVar8 = *(undefined8 **)(lVar7 + 0x20);
      if (puVar8 == &DAT_0a524ad0) {
        puVar8 = (undefined8 *)__Znwm(0x18);
        *puVar8 = 0;
        puVar8[1] = 0;
        puVar8[2] = 0;
        *(undefined8 **)(lVar7 + 0x20) = puVar8;
      }
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar8,lVar5 + 0x160)
      ;
    }
  }
  else {
    cVar11 = *(char *)(lVar5 + 0x177);
    if (-1 < cVar11) goto LAB_031086a0;
LAB_031086c0:
    if (*(long *)(lVar5 + 0x168) != 0) goto LAB_031086c8;
  }
  puStack_358 = &SUB_aaaaaaaaaaaaaaaa;
  local_360 = &SUB_aaaaaaaaaaaaaaaa;
  local_348 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_350 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_368 = &SUB_aaaaaaaaaaaaaaaa;
  local_370 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
  plVar21 = (long *)FUN_04669774();
  uVar9 = (**(code **)(*plVar21 + 0x18))();
  local_d8 = (undefined8 *)((ulong)local_d8 & 0xffffffffffffff);
  local_e8 = (undefined8 *******)((ulong)local_e8 & 0xffffffffffffff00);
  local_2f8 = DAT_087fa3f0;
  uStack_2d4 = 0;
  local_2e8 = 0;
  local_2e0 = 0;
  local_2f0 = 0;
  local_2d8 = local_2d8 & 0xffffff00;
  FUN_030bee20(&local_370,uVar9,&local_340,&local_e8,&local_2f8);
  if ((long)local_2e0 < 0) {
    __ZdlPvm(local_2f0,local_2e0 & 0x7fffffffffffffff);
  }
  if (((int)local_370 == 0 && local_370._4_4_ == 0) && (*(int *)(local_350 + 0x28) != 0)) {
    lVar7 = **(long **)(local_350 + 0x10);
    if (*(int *)(lVar7 + 0x10) == 0) {
      *(undefined4 *)(lVar5 + 0x118) = 2;
      *(undefined8 *)(lVar5 + 0xf8) = *(undefined8 *)(lVar7 + 0x28);
      iVar6 = thunk_FUN_05e1d97c(2);
      if (iVar6 != 0) {
        FUN_0488143c(local_388);
        pppppppuVar10 = local_388[0];
        if (-1 < cStack_371) {
          pppppppuVar10 = local_388;
        }
        if ((DAT_0a3da318 & 1) == 0) {
          _DAT_0a3da300 = CONCAT44((int)DAT_084a66a8,(int)DAT_0849a618);
          uRam000000000a3da308 = CONCAT44((int)DAT_0875a898,(int)DAT_084a66b0);
          DAT_0a3da310 = CONCAT44((int)DAT_084c8608,(int)DAT_084d88d0);
          DAT_0a3da318 = 1;
        }
        if ((DAT_0a3da494 & 1) == 0) {
          _DAT_0a3da478 = CONCAT44((int)DAT_088a7260,(int)DAT_087e2f50);
          uRam000000000a3da480 = CONCAT44((int)DAT_08485e90,(int)DAT_084a8110);
          DAT_0a3da488 = CONCAT44((int)DAT_0863e0f0,(int)DAT_088a7268);
          DAT_0a3da490 = (undefined4)DAT_0847fdb8;
          DAT_0a3da494 = 1;
        }
        FUN_05e1d050(&local_2f8,2,pppppppuVar10,&DAT_0a3da300,&DAT_0a3da478,0xb1,0,0);
        lVar5 = local_240;
        FUN_04cbe440(local_3a0,local_240);
        local_138 = local_3a0[0];
        if (-1 < cStack_389) {
          local_138 = local_3a0;
        }
        local_130 = 0;
        uVar16 = *(ulong *)(lVar5 + 0xf8);
        local_188 = (undefined1 *)0x0;
        if ((DAT_0a3da6d9 & 1) == 0) {
          uVar18 = 0;
          do {
            uVar23 = *(undefined4 *)((long)&DAT_088b337c + uVar18);
            uVar2 = CONCAT12((char)((uint)uVar23 >> 8),(short)uVar23) & 0xff00ff;
            uVar24 = *(undefined4 *)((long)&DAT_088b3368 + uVar18 % 0x14);
            *(uint *)((long)&DAT_0a3da691 + uVar18) =
                 CONCAT13((char)((uint)uVar23 >> 0x18) + 0x8aU ^ (byte)((uint)uVar24 >> 0x18),
                          CONCAT12((char)((uint)uVar23 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar24 >> 0x10),
                                   CONCAT11((char)(uVar2 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar24 >> 8),
                                            (char)uVar2 + 0x8aU ^ (byte)uVar24)));
            uVar18 = uVar18 + 4;
          } while (uVar18 != 0x48);
          DAT_0a3da6d9 = 1;
        }
        lVar22 = 0;
        do {
          lVar20 = lVar22;
          local_180[lVar20] = *(undefined1 *)(uVar16 % 10 + 0xa3da6b4);
          bVar4 = 9 < uVar16;
          uVar16 = uVar16 / 10;
          lVar22 = lVar20 + 1;
        } while (bVar4);
        local_180[lVar20 + 1] = 0;
        if (8 < lVar20 + 8U) {
          puVar12 = local_180;
          puVar13 = local_180 + lVar20;
          do {
            puVar12 = puVar12 + 1;
            uVar1 = *puVar13;
            puVar14 = puVar13 + -1;
            *puVar13 = puVar12[-1];
            puVar12[-1] = uVar1;
            puVar13 = puVar14;
          } while (puVar12 < puVar14);
        }
        local_188 = local_180;
        local_1d8 = (undefined8 *******)0x0;
        lVar22 = 0;
        uVar16 = (ulong)*(uint *)(lVar7 + 0x1c);
        do {
          lVar20 = lVar22;
          uVar15 = (uint)uVar16;
          *(undefined1 *)((long)&local_1d0 + lVar20) =
               *(undefined1 *)
                ((long)&DAT_0a3da691 + (ulong)(uVar15 + (int)(uVar16 / 10) * -10 + 0x23));
          lVar22 = lVar20 + 1;
          uVar16 = uVar16 / 10;
        } while (9 < uVar15);
        *(undefined1 *)((long)&local_1d0 + lVar20 + 1) = 0;
        if (8 < lVar20 + 8U) {
          puVar12 = (undefined1 *)((long)&local_1d0 + lVar20);
          puVar13 = (undefined1 *)((long)&local_1d0 + 1);
          do {
            uVar1 = *puVar12;
            *puVar12 = puVar13[-1];
            puVar13[-1] = uVar1;
            bVar4 = puVar13 < puVar12 + -1;
            puVar12 = puVar12 + -1;
            puVar13 = puVar13 + 1;
          } while (bVar4);
        }
        local_1d8 = (undefined8 *******)&local_1d0;
        local_230 = (undefined8 *******)&uStack_228;
        lVar22 = 0;
        uVar16 = (ulong)*(uint *)(lVar7 + 0x20);
        do {
          lVar7 = lVar22;
          uVar15 = (uint)uVar16;
          *(undefined1 *)((long)&uStack_228 + lVar7) =
               *(undefined1 *)
                ((long)&DAT_0a3da691 + (ulong)(uVar15 + (int)(uVar16 / 10) * -10 + 0x23));
          lVar22 = lVar7 + 1;
          uVar16 = uVar16 / 10;
        } while (9 < uVar15);
        *(undefined1 *)((long)&uStack_228 + lVar7 + 1) = 0;
        if (8 < lVar7 + 8U) {
          puVar12 = (undefined1 *)((long)&uStack_228 + lVar7);
          puVar13 = (undefined1 *)((long)&uStack_228 + 1);
          do {
            uVar1 = *puVar12;
            *puVar12 = puVar13[-1];
            puVar13[-1] = uVar1;
            bVar4 = puVar13 < puVar12 + -1;
            puVar12 = puVar12 + -1;
            puVar13 = puVar13 + 1;
          } while (bVar4);
        }
        if ((DAT_0a3da549 & 1) == 0) {
          uVar16 = 0;
          do {
            uVar23 = *(undefined4 *)((long)&DAT_088b3090 + uVar16);
            uVar2 = CONCAT12((char)((uint)uVar23 >> 8),(short)uVar23) & 0xff00ff;
            uVar24 = *(undefined4 *)((long)&DAT_088b307c + uVar16 % 0x14);
            *(uint *)((long)&DAT_0a3da501 + uVar16) =
                 CONCAT13((char)((uint)uVar23 >> 0x18) + 0x8aU ^ (byte)((uint)uVar24 >> 0x18),
                          CONCAT12((char)((uint)uVar23 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar24 >> 0x10),
                                   CONCAT11((char)(uVar2 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar24 >> 8),
                                            (char)uVar2 + 0x8aU ^ (byte)uVar24)));
            uVar16 = uVar16 + 4;
          } while (uVar16 != 0x48);
          DAT_0a3da549 = 1;
        }
        local_e8 = &local_138;
        puStack_e0 = &local_188;
        local_d8 = &local_1d8;
        puStack_d0 = &local_230;
        uStack_c0 = 0;
        uStack_c8 = 0;
        local_b0 = 0;
        uStack_b8 = 0;
        local_a0 = 0;
        uStack_a8 = 0;
        local_90 = 0;
        uStack_98 = 0;
        local_80 = 0;
        uStack_88 = 0;
        local_70 = 0;
        uStack_78 = 0;
        FUN_05e1d31c(&local_2f8,&DAT_0a3da501,&local_e8);
        if (cStack_389 < '\0') {
          __ZdlPvm(local_3a0[0],CONCAT17(cStack_389,local_390) & 0x7fffffffffffffff);
        }
        thunk_FUN_05e1d0bc(&local_2f8);
        if (cStack_371 < '\0') {
          uVar16 = CONCAT17(cStack_371,local_378);
          pppppppuVar10 = local_388[0];
          goto LAB_03109064;
        }
      }
    }
    else {
      iVar6 = thunk_FUN_05e1d97c(4);
      if (iVar6 != 0) {
        FUN_0488143c(&local_1d8);
        pppppppuVar10 = local_1d8;
        if (-1 < cStack_1c1) {
          pppppppuVar10 = (undefined8 *******)&local_1d8;
        }
        if ((DAT_0a3da318 & 1) == 0) {
          _DAT_0a3da300 = CONCAT44((int)DAT_084a66a8,(int)DAT_0849a618);
          uRam000000000a3da308 = CONCAT44((int)DAT_0875a898,(int)DAT_084a66b0);
          DAT_0a3da310 = CONCAT44((int)DAT_084c8608,(int)DAT_084d88d0);
          DAT_0a3da318 = 1;
        }
        if ((DAT_0a3da494 & 1) == 0) {
          _DAT_0a3da478 = CONCAT44((int)DAT_088a7260,(int)DAT_087e2f50);
          uRam000000000a3da480 = CONCAT44((int)DAT_08485e90,(int)DAT_084a8110);
          DAT_0a3da488 = CONCAT44((int)DAT_0863e0f0,(int)DAT_088a7268);
          DAT_0a3da490 = (undefined4)DAT_0847fdb8;
          DAT_0a3da494 = 1;
        }
        FUN_05e1d050(&local_2f8,4,pppppppuVar10,&DAT_0a3da300,&DAT_0a3da478,0xb3,0,0);
        lVar5 = local_240;
        FUN_04cbe440(&local_230,local_240);
        local_138 = local_230;
        if (-1 < (long)local_220) {
          local_138 = (undefined8 *******)&local_230;
        }
        local_130 = 0;
        iVar6 = *(int *)(lVar7 + 0x10);
        local_188 = (undefined1 *)0x0;
        if ((DAT_0a3da6d9 & 1) == 0) {
          uVar16 = 0;
          do {
            uVar23 = *(undefined4 *)((long)&DAT_088b337c + uVar16);
            uVar2 = CONCAT12((char)((uint)uVar23 >> 8),(short)uVar23) & 0xff00ff;
            uVar24 = *(undefined4 *)((long)&DAT_088b3368 + uVar16 % 0x14);
            *(uint *)((long)&DAT_0a3da691 + uVar16) =
                 CONCAT13((char)((uint)uVar23 >> 0x18) + 0x8aU ^ (byte)((uint)uVar24 >> 0x18),
                          CONCAT12((char)((uint)uVar23 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar24 >> 0x10),
                                   CONCAT11((char)(uVar2 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar24 >> 8),
                                            (char)uVar2 + 0x8aU ^ (byte)uVar24)));
            uVar16 = uVar16 + 4;
          } while (uVar16 != 0x48);
          DAT_0a3da6d9 = 1;
        }
        lVar7 = 8;
        iVar19 = iVar6;
        do {
          lVar22 = lVar7;
          local_180[lVar22 + -8] = *(undefined1 *)((long)&DAT_0a3da691 + (long)(iVar19 % 10 + 0x23))
          ;
          lVar7 = lVar22 + 1;
          uVar15 = iVar19 + 9;
          iVar19 = iVar19 / 10;
        } while (0x12 < uVar15);
        if (iVar6 < 0) {
          local_180[lVar22 + -7] = 0x2d;
          lVar7 = lVar22 + 2;
        }
        local_180[lVar7 + -8] = 0;
        if (9 < lVar7) {
          puVar12 = local_180;
          puVar13 = &uStack_189 + lVar7;
          do {
            puVar12 = puVar12 + 1;
            uVar1 = *puVar13;
            puVar14 = puVar13 + -1;
            *puVar13 = puVar12[-1];
            puVar12[-1] = uVar1;
            puVar13 = puVar14;
          } while (puVar12 < puVar14);
        }
        if ((DAT_0a3da575 & 1) == 0) {
          _DAT_0a3da54c = CONCAT44((int)DAT_08507730,(int)DAT_0849a618);
          uRam000000000a3da554 = CONCAT44((int)DAT_084fdd78,(int)DAT_084a66b0);
          _DAT_0a3da55c = CONCAT44((int)DAT_084f5b30,(int)ram0x08487528);
          uRam000000000a3da564 = CONCAT44((int)DAT_084d1018,(int)ram0x08480938);
          DAT_0a3da56c = CONCAT44((int)DAT_084e4b10,(int)DAT_086db3d0);
          DAT_0a3da574 = 0;
          DAT_0a3da575 = 1;
        }
        local_e8 = &local_138;
        puStack_e0 = &local_188;
        puStack_d0 = (undefined8 *)0x0;
        local_d8 = (undefined8 *)0x0;
        uStack_c0 = 0;
        uStack_c8 = 0;
        local_b0 = 0;
        uStack_b8 = 0;
        local_a0 = 0;
        uStack_a8 = 0;
        local_90 = 0;
        uStack_98 = 0;
        local_80 = 0;
        uStack_88 = 0;
        local_70 = 0;
        uStack_78 = 0;
        local_188 = local_180;
        FUN_05e1d31c(&local_2f8,&DAT_0a3da54c,&local_e8);
        if ((long)local_220 < 0) {
          __ZdlPvm(local_230,(ulong)local_220 & 0x7fffffffffffffff);
        }
        thunk_FUN_05e1d0bc(&local_2f8);
        if (cStack_1c1 < '\0') {
          uVar16 = CONCAT17(cStack_1c1,local_1c8);
          pppppppuVar10 = local_1d8;
LAB_03109064:
          __ZdlPvm(pppppppuVar10,uVar16 & 0x7fffffffffffffff);
        }
      }
    }
  }
  *param_1 = (long)local_370;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 1,(ulong)&local_370 | 8);
  local_3b0 = lVar5;
  if (*(int *)(lVar5 + 0x118) != 2) {
    *(undefined4 *)(lVar5 + 0x118) = 5;
    iVar6 = thunk_FUN_05e1d97c(4);
    if (iVar6 != 0) {
      FUN_0488143c(local_388);
      pppppppuVar10 = local_388[0];
      if (-1 < cStack_371) {
        pppppppuVar10 = local_388;
      }
      if ((DAT_0a3da318 & 1) == 0) {
        _DAT_0a3da300 = CONCAT44((int)DAT_084a66a8,(int)DAT_0849a618);
        uRam000000000a3da308 = CONCAT44((int)DAT_0875a898,(int)DAT_084a66b0);
        DAT_0a3da310 = CONCAT44((int)DAT_084c8608,(int)DAT_084d88d0);
        DAT_0a3da318 = 1;
      }
      if ((DAT_0a3da494 & 1) == 0) {
        _DAT_0a3da478 = CONCAT44((int)DAT_088a7260,(int)DAT_087e2f50);
        uRam000000000a3da480 = CONCAT44((int)DAT_08485e90,(int)DAT_084a8110);
        DAT_0a3da488 = CONCAT44((int)DAT_0863e0f0,(int)DAT_088a7268);
        DAT_0a3da490 = (undefined4)DAT_0847fdb8;
        DAT_0a3da494 = 1;
      }
      FUN_05e1d050(&local_2f8,4,pppppppuVar10,&DAT_0a3da300,&DAT_0a3da478,0xbe,0,0);
      FUN_04cbe440(local_3a0,local_240);
      local_138 = local_3a0[0];
      if (-1 < cStack_389) {
        local_138 = local_3a0;
      }
      local_130 = 0;
      local_188 = (undefined1 *)0x0;
      if ((DAT_0a3da6d9 & 1) == 0) {
        uVar16 = 0;
        do {
          uVar23 = *(undefined4 *)((long)&DAT_088b337c + uVar16);
          uVar2 = CONCAT12((char)((uint)uVar23 >> 8),(short)uVar23) & 0xff00ff;
          uVar24 = *(undefined4 *)((long)&DAT_088b3368 + uVar16 % 0x14);
          *(uint *)((long)&DAT_0a3da691 + uVar16) =
               CONCAT13((char)((uint)uVar23 >> 0x18) + 0x8aU ^ (byte)((uint)uVar24 >> 0x18),
                        CONCAT12((char)((uint)uVar23 >> 0x10) + 0x8aU ^ (byte)((uint)uVar24 >> 0x10)
                                 ,CONCAT11((char)(uVar2 >> 0x10) + 0x8aU ^ (byte)((uint)uVar24 >> 8)
                                           ,(char)uVar2 + 0x8aU ^ (byte)uVar24)));
          uVar16 = uVar16 + 4;
        } while (uVar16 != 0x48);
        DAT_0a3da6d9 = 1;
      }
      lVar5 = 8;
      iVar6 = (int)local_370;
      do {
        lVar7 = lVar5;
        local_180[lVar7 + -8] = *(undefined1 *)((long)&DAT_0a3da691 + (long)(iVar6 % 10 + 0x23));
        lVar5 = lVar7 + 1;
        uVar15 = iVar6 + 9;
        iVar6 = iVar6 / 10;
      } while (0x12 < uVar15);
      if ((int)local_370 < 0) {
        local_180[lVar7 + -7] = 0x2d;
        lVar5 = lVar7 + 2;
      }
      local_180[lVar5 + -8] = 0;
      if (9 < lVar5) {
        puVar12 = local_180;
        puVar13 = &uStack_189 + lVar5;
        do {
          puVar12 = puVar12 + 1;
          uVar1 = *puVar13;
          puVar14 = puVar13 + -1;
          *puVar13 = puVar12[-1];
          puVar12[-1] = uVar1;
          puVar13 = puVar14;
        } while (puVar12 < puVar14);
      }
      local_188 = local_180;
      local_1d8 = (undefined8 *******)0x0;
      lVar5 = 8;
      iVar6 = local_370._4_4_;
      do {
        lVar7 = lVar5;
        *(undefined1 *)((long)&local_1d8 + lVar7) =
             *(undefined1 *)((long)&DAT_0a3da691 + (long)(iVar6 % 10 + 0x23));
        lVar5 = lVar7 + 1;
        uVar15 = iVar6 + 9;
        iVar6 = iVar6 / 10;
      } while (0x12 < uVar15);
      if ((long)local_370 < 0) {
        *(undefined1 *)((long)&local_1d8 + lVar7 + 1) = 0x2d;
        lVar5 = lVar7 + 2;
      }
      *(undefined1 *)((long)&local_1d8 + lVar5) = 0;
      if (9 < lVar5) {
        puVar12 = &uStack_1d9 + lVar5;
        puVar13 = (undefined1 *)((long)&local_1d0 + 1);
        do {
          uVar1 = *puVar12;
          *puVar12 = puVar13[-1];
          puVar13[-1] = uVar1;
          bVar4 = puVar13 < puVar12 + -1;
          puVar12 = puVar12 + -1;
          puVar13 = puVar13 + 1;
        } while (bVar4);
      }
      local_1d8 = (undefined8 *******)&local_1d0;
      local_230 = (undefined8 *******)&uStack_228;
      lVar5 = 0;
      uVar16 = (ulong)*(uint *)(local_350 + 0x28);
      do {
        lVar7 = lVar5;
        uVar15 = (uint)uVar16;
        *(undefined1 *)((long)&uStack_228 + lVar7) =
             *(undefined1 *)
              ((long)&DAT_0a3da691 + (ulong)(uVar15 + (int)(uVar16 / 10) * -10 + 0x23));
        lVar5 = lVar7 + 1;
        uVar16 = uVar16 / 10;
      } while (9 < uVar15);
      *(undefined1 *)((long)&uStack_228 + lVar7 + 1) = 0;
      if (8 < lVar7 + 8U) {
        puVar12 = (undefined1 *)((long)&uStack_228 + lVar7);
        puVar13 = (undefined1 *)((long)&uStack_228 + 1);
        do {
          uVar1 = *puVar12;
          *puVar12 = puVar13[-1];
          puVar13[-1] = uVar1;
          bVar4 = puVar13 < puVar12 + -1;
          puVar12 = puVar12 + -1;
          puVar13 = puVar13 + 1;
        } while (bVar4);
      }
      if ((DAT_0a3da5bf & 1) == 0) {
        uVar16 = 0;
        do {
          uVar23 = *(undefined4 *)((long)&DAT_088b3129 + uVar16);
          uVar2 = CONCAT12((char)((uint)uVar23 >> 8),(short)uVar23) & 0xff00ff;
          uVar24 = *(undefined4 *)((long)&DAT_088b3115 + uVar16 % 0x14);
          *(uint *)((long)&DAT_0a3da576 + uVar16) =
               CONCAT13((char)((uint)uVar23 >> 0x18) + 0x8aU ^ (byte)((uint)uVar24 >> 0x18),
                        CONCAT12((char)((uint)uVar23 >> 0x10) + 0x8aU ^ (byte)((uint)uVar24 >> 0x10)
                                 ,CONCAT11((char)(uVar2 >> 0x10) + 0x8aU ^ (byte)((uint)uVar24 >> 8)
                                           ,(char)uVar2 + 0x8aU ^ (byte)uVar24)));
          uVar16 = uVar16 + 4;
        } while (uVar16 != 0x48);
        DAT_0a3da5be = 0;
        DAT_0a3da5bf = 1;
      }
      local_e8 = &local_138;
      puStack_e0 = &local_188;
      local_d8 = &local_1d8;
      puStack_d0 = &local_230;
      uStack_c0 = 0;
      uStack_c8 = 0;
      local_b0 = 0;
      uStack_b8 = 0;
      local_a0 = 0;
      uStack_a8 = 0;
      local_90 = 0;
      uStack_98 = 0;
      local_80 = 0;
      uStack_88 = 0;
      local_70 = 0;
      uStack_78 = 0;
      FUN_05e1d31c(&local_2f8,&DAT_0a3da576,&local_e8);
      if (cStack_389 < '\0') {
        __ZdlPvm(local_3a0[0],CONCAT17(cStack_389,local_390) & 0x7fffffffffffffff);
      }
      thunk_FUN_05e1d0bc(&local_2f8);
      if (cStack_371 < '\0') {
        __ZdlPvm(local_388[0],CONCAT17(cStack_371,local_378) & 0x7fffffffffffffff);
      }
    }
    FUN_030f6650(&local_2f8,3,0xc,(int)*param_1,*(undefined4 *)((long)param_1 + 4));
    *param_1 = local_2f8;
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_1 + 1,&local_2f0)
    ;
    if (local_2d0 != (long *)0x0) {
      local_2d0[1] = local_2d0[1] + 1;
    }
    plVar21 = (long *)param_1[5];
    param_1[4] = CONCAT44(uStack_2d4,local_2d8);
    param_1[5] = (long)local_2d0;
    if (plVar21 != (long *)0x0) {
      LOAcquire();
      lVar5 = plVar21[1];
      plVar21[1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*plVar21 + 0x10))(plVar21);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar21);
      }
    }
    if (local_2d0 != (long *)0x0) {
      LOAcquire();
      lVar5 = local_2d0[1];
      local_2d0[1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*local_2d0 + 0x10))(local_2d0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(local_2d0);
      }
    }
    local_3b0 = local_240;
    if ((long)local_2e0 < 0) {
      __ZdlPvm(local_2f0,local_2e0 & 0x7fffffffffffffff);
      local_3b0 = local_240;
    }
  }
  local_3a8 = local_238;
  lVar5 = 0;
  if (local_238 != (long *)0x0) {
    lVar5 = local_238[1];
    local_238[1] = lVar5 + 1;
  }
  FUN_030daf78(lVar5,param_2,&local_3b0,1,1);
  plVar3 = local_3a8;
  plVar21 = local_348;
  if (local_3a8 != (long *)0x0) {
    LOAcquire();
    lVar5 = local_3a8[1];
    local_3a8[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*local_3a8 + 0x10))(local_3a8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
      plVar21 = local_348;
    }
  }
  local_348 = plVar21;
  if (plVar21 != (long *)0x0) {
    LOAcquire();
    lVar5 = *(long *)((long)plVar21 + 8U);
    *(long *)((long)plVar21 + 8U) = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*plVar21 + 0x10))(plVar21);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar21);
    }
  }
  if ((long)puStack_358 < 0) {
    __ZdlPvm(puStack_368,(ulong)puStack_358 & 0x7fffffffffffffff);
  }
  FUN_0465d634(&local_340);
joined_r0x03108bf8:
  plVar21 = local_238;
  if ((long)local_248 < 0) {
    __ZdlPvm(local_258,(ulong)local_248 & 0x7fffffffffffffff);
    plVar21 = local_238;
  }
  local_238 = plVar21;
  if (plVar21 != (long *)0x0) {
    LOAcquire();
    lVar5 = plVar21[1];
    plVar21[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*plVar21 + 0x10))(plVar21);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar21);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


