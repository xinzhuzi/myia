// Ghidra inferred pseudocode; requested=0x30efce4
// entry=030efce4 end=030f1927

/* WARNING: Removing unreachable block (ram,0x030f172c) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_030efce4(long *param_1,long param_2)

{
  long *plVar1;
  long ****pppplVar2;
  long *****ppppplVar3;
  long *****ppppplVar4;
  undefined1 uVar5;
  bool bVar6;
  long ****pppplVar7;
  undefined1 *puVar8;
  long ****pppplVar9;
  long ***ppplVar10;
  int iVar11;
  uint uVar12;
  int iVar13;
  undefined4 uVar14;
  undefined8 *puVar15;
  long *plVar16;
  undefined8 uVar17;
  ulong uVar18;
  char cVar19;
  ulong uVar20;
  long lVar21;
  undefined1 *puVar22;
  ulong uVar23;
  undefined1 *puVar24;
  long *plVar25;
  long lVar26;
  undefined8 *puVar27;
  long *plVar28;
  long *plVar29;
  long *local_400;
  long *plStack_3f8;
  undefined1 *local_3f0;
  undefined1 *puStack_3e8;
  undefined1 *puStack_3e0;
  undefined1 *puStack_3d8;
  undefined1 *local_3d0;
  undefined1 *puStack_3c8;
  undefined1 *puStack_3c0;
  undefined1 *puStack_3b8;
  undefined1 *local_3b0;
  undefined1 *puStack_3a8;
  undefined1 *puStack_3a0;
  undefined1 *puStack_398;
  undefined1 *local_390;
  undefined1 *puStack_388;
  undefined1 *puStack_380;
  undefined1 *puStack_378;
  undefined1 *local_370;
  undefined1 *puStack_368;
  undefined1 *puStack_360;
  undefined1 *puStack_358;
  undefined1 *local_350;
  undefined1 *puStack_348;
  undefined1 *puStack_340;
  undefined1 *puStack_338;
  undefined1 *local_330;
  undefined1 *puStack_328;
  undefined1 *puStack_320;
  undefined1 *puStack_318;
  undefined1 *local_310;
  long *local_308;
  long *local_300;
  long ****local_2f8 [2];
  undefined7 local_2e8;
  char cStack_2e1;
  undefined4 *local_2e0;
  undefined1 local_2d8;
  long *local_290;
  undefined1 local_288;
  long ****local_240;
  undefined8 local_238;
  undefined7 local_230;
  char cStack_229;
  undefined8 *local_1f0;
  undefined8 local_1e8;
  long ****local_1a0;
  undefined8 local_198;
  undefined7 local_190;
  byte bStack_189;
  long ****local_150;
  undefined1 uStack_148;
  undefined7 uStack_147;
  undefined7 local_140;
  byte bStack_139;
  long ****local_100;
  long ****pppplStack_f8;
  undefined8 local_f0;
  long ****local_e8;
  long **pplStack_e0;
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
  long local_78;
  
  local_78 = *(long *)PTR____stack_chk_guard_09b36c98;
  plVar29 = *(long **)(param_2 + 8);
  if (plVar29 == (long *)0x0) {
    iVar11 = thunk_FUN_05e1d97c(4);
    if (iVar11 != 0) {
      FUN_0488143c(&local_150);
      ppppplVar3 = (long *****)local_150;
      if (-1 < (char)bStack_139) {
        ppppplVar3 = &local_150;
      }
      if ((DAT_0a3d9838 & 1) == 0) {
        uVar18 = 0;
        do {
          (&DAT_0a3d9820)[uVar18] = (&DAT_088b055e)[uVar18] + 0x8a ^ (&DAT_088b054e)[uVar18 & 0xf];
          uVar18 = uVar18 + 1;
        } while (uVar18 != 0x18);
        DAT_0a3d9838 = 1;
      }
      if ((DAT_0a3d9857 & 1) == 0) {
        _DAT_0a3d983c = CONCAT44((int)DAT_085095c0,(int)DAT_084d5770);
        uRam000000000a3d9844 = CONCAT44((int)DAT_08538c30,(int)DAT_084a66b0);
        DAT_0a3d984c = CONCAT44((int)DAT_084b0730,(int)DAT_08546648);
        DAT_0a3d9854 = 0x6563;
        DAT_0a3d9856 = 0;
        DAT_0a3d9857 = 1;
      }
      FUN_05e1d050(&local_400,4,ppppplVar3,&DAT_0a3d9820,&DAT_0a3d983c,0x56,0,0);
      if ((DAT_0a3d989a & 1) == 0) {
        uVar18 = 0;
        do {
          (&DAT_0a3d9858)[uVar18] = (&DAT_088b05b5)[uVar18] + 0x8a ^ (&DAT_088b05a5)[uVar18 & 0xf];
          uVar18 = uVar18 + 1;
        } while (uVar18 != 0x42);
        DAT_0a3d989a = 1;
      }
      local_98 = 0;
      uStack_a0 = 0;
      local_88 = 0;
      uStack_90 = 0;
      local_b8 = 0;
      uStack_c0 = 0;
      local_a8 = 0;
      uStack_b0 = 0;
      local_d8 = (undefined4 **)0x0;
      pplStack_e0 = (long **)0x0;
      local_c8 = 0;
      uStack_d0 = 0;
      pppplStack_f8 = (long ****)0x0;
      local_100 = (long ****)0x0;
      local_e8 = (long ****)0x0;
      local_f0 = (undefined8 **)0x0;
      FUN_05e1d31c(&local_400,&DAT_0a3d9858,&local_100);
      thunk_FUN_05e1d0bc(&local_400);
      if ((char)bStack_139 < '\0') {
        __ZdlPvm(local_150,CONCAT17(bStack_139,local_140) & 0x7fffffffffffffff);
      }
    }
    puVar15 = (undefined8 *)__Znwm(0x290);
    puVar15[1] = 0;
    puVar15[2] = 0;
    *puVar15 = &PTR_FUN_09c92390;
    puVar27 = puVar15 + 3;
    _bzero(puVar27,0x278);
    FUN_00ac6038(puVar27);
    *param_1 = (long)puVar27;
    param_1[1] = (long)puVar15;
    goto LAB_030f18bc;
  }
  *param_1 = (long)&SUB_aaaaaaaaaaaaaaaa;
  param_1[1] = (long)&SUB_aaaaaaaaaaaaaaaa;
  local_300 = *(long **)(param_2 + 0x10);
  if (local_300 != (long *)0x0) {
    local_300[1] = local_300[1] + 1;
  }
  *param_1 = (long)&SUB_aaaaaaaaaaaaaaaa;
  param_1[1] = (long)&SUB_aaaaaaaaaaaaaaaa;
  local_308 = plVar29;
  puVar15 = (undefined8 *)__Znwm(0x290);
  puVar15[1] = 0;
  puVar15[2] = 0;
  *puVar15 = &PTR_FUN_09c92390;
  puVar27 = puVar15 + 3;
  _bzero(puVar27,0x278);
  FUN_00ac6038(puVar27);
  *param_1 = (long)puVar27;
  param_1[1] = (long)puVar15;
  plVar16 = (long *)FUN_04669774();
  uVar17 = (**(code **)(*plVar16 + 0x28))();
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar15 + 6,uVar17);
  ppppplVar3 = (long *****)(plVar29 + 0x12);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar15 + 9,ppppplVar3);
  FUN_04cbbc88(&local_400,puVar27);
  FUN_04cbb728(puVar27,&local_400);
  if ((long)local_3f0 < 0) {
    __ZdlPvm(local_400,(ulong)local_3f0 & 0x7fffffffffffffff);
  }
  plVar16 = (long *)FUN_04669774();
  uVar18 = (**(code **)(*plVar16 + 0x50))();
  iVar11 = thunk_FUN_05e1d97c(2);
  plVar16 = plVar29;
  if (iVar11 != 0) {
    FUN_0488143c(&local_240);
    ppppplVar4 = (long *****)local_240;
    if (-1 < cStack_229) {
      ppppplVar4 = &local_240;
    }
    if ((DAT_0a3d9838 & 1) == 0) {
      uVar20 = 0;
      do {
        (&DAT_0a3d9820)[uVar20] = (&DAT_088b055e)[uVar20] + 0x8a ^ (&DAT_088b054e)[uVar20 & 0xf];
        uVar20 = uVar20 + 1;
      } while (uVar20 != 0x18);
      DAT_0a3d9838 = 1;
    }
    if ((DAT_0a3d9a82 & 1) == 0) {
      uVar20 = 0;
      do {
        (&DAT_0a3d9a6c)[uVar20] = (&DAT_088b0905)[uVar20] + 0x8a ^ (&DAT_088b08f5)[uVar20 & 0xf];
        uVar20 = uVar20 + 1;
      } while (uVar20 != 0x16);
      DAT_0a3d9a82 = 1;
    }
    FUN_05e1d050(&local_400,2,ppppplVar4,&DAT_0a3d9820,&DAT_0a3d9a6c,0x1d,0,0);
    local_150 = (long ****)plVar29[0x12];
    if (-1 < *(char *)((long)plVar29 + 0xa7)) {
      local_150 = (long ****)ppppplVar3;
    }
    uStack_148 = 0;
    local_1a0 = (long ****)0x0;
    local_1a0 = (long ****)&local_198;
    if ((DAT_0a3d9bbd & 1) == 0) {
      uVar20 = 0;
      do {
        (&DAT_0a3d9b75)[uVar20] = (&DAT_088b0a63)[uVar20] + 0x8a ^ (&DAT_088b0a53)[uVar20 & 0xf];
        uVar20 = uVar20 + 1;
      } while (uVar20 != 0x48);
      DAT_0a3d9bbd = 1;
    }
    lVar26 = 0;
    uVar20 = uVar18;
    do {
      lVar21 = lVar26;
      uVar12 = (uint)uVar20;
      *(undefined1 *)((long)&local_198 + lVar21) =
           (&DAT_0a3d9b75)[uVar12 + (int)((uVar20 & 0xffffffff) / 10) * -10 + 0x23];
      lVar26 = lVar21 + 1;
      uVar20 = (uVar20 & 0xffffffff) / 10;
    } while (9 < uVar12);
    *(undefined1 *)((long)&local_198 + lVar21 + 1) = 0;
    if (8 < lVar21 + 8U) {
      puVar22 = (undefined1 *)((long)&local_198 + lVar21);
      puVar8 = (undefined1 *)((long)&local_198 + 1);
      do {
        uVar5 = *puVar22;
        *puVar22 = puVar8[-1];
        puVar8[-1] = uVar5;
        bVar6 = puVar8 < puVar22 + -1;
        puVar22 = puVar22 + -1;
        puVar8 = puVar8 + 1;
      } while (bVar6);
    }
    uVar20 = FUN_039401ec(ppppplVar3);
    local_1f0 = (undefined8 *)0x0;
    local_1f0 = &local_1e8;
    if ((DAT_0a3d9bbd & 1) == 0) {
      uVar23 = 0;
      do {
        (&DAT_0a3d9b75)[uVar23] = (&DAT_088b0a63)[uVar23] + 0x8a ^ (&DAT_088b0a53)[uVar23 & 0xf];
        uVar23 = uVar23 + 1;
      } while (uVar23 != 0x48);
      DAT_0a3d9bbd = 1;
    }
    lVar26 = 0;
    do {
      lVar21 = lVar26;
      uVar12 = (uint)uVar20;
      *(undefined1 *)((long)&local_1e8 + lVar21) =
           (&DAT_0a3d9b75)[uVar12 + (int)((uVar20 & 0xffffffff) / 10) * -10 + 0x23];
      uVar20 = (uVar20 & 0xffffffff) / 10;
      lVar26 = lVar21 + 1;
    } while (9 < uVar12);
    *(undefined1 *)((long)&local_1e8 + lVar21 + 1) = 0;
    if (8 < lVar21 + 8U) {
      puVar22 = (undefined1 *)((long)&local_1e8 + lVar21);
      puVar8 = (undefined1 *)((long)&local_1e8 + 1);
      do {
        uVar5 = *puVar22;
        *puVar22 = puVar8[-1];
        puVar8[-1] = uVar5;
        bVar6 = puVar8 < puVar22 + -1;
        puVar22 = puVar22 + -1;
        puVar8 = puVar8 + 1;
      } while (bVar6);
    }
    if ((DAT_0a3d9acb & 1) == 0) {
      uVar20 = 0;
      do {
        (&DAT_0a3d9a83)[uVar20] = (&DAT_088b092b)[uVar20] + 0x8a ^ (&DAT_088b091b)[uVar20 & 0xf];
        uVar20 = uVar20 + 1;
      } while (uVar20 != 0x48);
      DAT_0a3d9acb = 1;
    }
    local_100 = (long ****)&local_150;
    pppplStack_f8 = (long ****)&local_1a0;
    local_f0 = &local_1f0;
    pplStack_e0 = (long **)0x0;
    local_e8 = (long ****)0x0;
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
    local_88 = 0;
    FUN_05e1d31c(&local_400,&DAT_0a3d9a83,&local_100);
    thunk_FUN_05e1d0bc(&local_400);
    plVar16 = local_308;
    if (cStack_229 < '\0') {
      __ZdlPvm(local_240,CONCAT17(cStack_229,local_230) & 0x7fffffffffffffff);
      plVar16 = local_308;
    }
  }
  *(int *)((long)puVar15 + 300) = (int)uVar18;
  puVar15[0x23] = (uVar18 & 0xffffffff) * 1000;
  if ((char)plVar16[0x1b] == '\x01') {
    *(uint *)((long)puVar15 + 0x21c) = *(uint *)((long)puVar15 + 0x21c) | 0x1000;
    lVar26 = puVar15[0x41];
    if (lVar26 == 0) {
      lVar26 = __Znwm(0x18);
      FUN_04ea6b70();
      puVar15[0x41] = lVar26;
    }
    *(uint *)(lVar26 + 0x10) = *(uint *)(lVar26 + 0x10) | 1;
    *(undefined1 *)(lVar26 + 8) = 1;
    *(uint *)((long)puVar15 + 0x21c) = *(uint *)((long)puVar15 + 0x21c) | 0x1000;
    if (lVar26 == 0) {
      lVar26 = __Znwm(0x18);
      FUN_04ea6b70();
      puVar15[0x41] = lVar26;
    }
    *(uint *)(lVar26 + 0x10) = *(uint *)(lVar26 + 0x10) | 2;
    *(undefined1 *)(lVar26 + 9) = 0;
    if ((*(byte *)(plVar16 + 0x1b) & 1) == 0) {
                    /* WARNING: Subroutine does not return */
      FUN_004d04d4();
    }
    FUN_0466aca8(&local_150);
    FUN_01205740(&local_100,local_150);
    FUN_0268f370(&local_400,local_100);
    plVar28 = plVar16 + 0x17;
    uVar12 = FUN_03204674(local_400,ppppplVar3,plVar28,*(undefined4 *)((long)puVar15 + 300));
    plVar25 = plStack_3f8;
    if (plStack_3f8 != (long *)0x0) {
      LOAcquire();
      lVar26 = plStack_3f8[1];
      plStack_3f8[1] = lVar26 + -1;
      LORelease();
      if (lVar26 == 0) {
        (**(code **)(*plStack_3f8 + 0x10))(plStack_3f8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar25);
      }
    }
    pppplVar9 = pppplStack_f8;
    if ((long *****)pppplStack_f8 != (long *****)0x0) {
      LOAcquire();
      pppplVar7 = (long ****)pppplStack_f8[1];
      pppplStack_f8[1] = (long ***)((long)pppplVar7 + -1);
      LORelease();
      if (pppplVar7 == (long ****)0x0) {
        (*(code *)(*pppplVar9)[2])(pppplVar9);
        __ZNSt3__119__shared_weak_count14__release_weakEv(pppplVar9);
      }
    }
    plVar25 = (long *)CONCAT71(uStack_147,uStack_148);
    if (plVar25 != (long *)0x0) {
      LOAcquire();
      lVar26 = plVar25[1];
      plVar25[1] = lVar26 + -1;
      LORelease();
      if (lVar26 == 0) {
        (**(code **)(*plVar25 + 0x10))(plVar25);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar25);
      }
    }
    plVar25 = local_308;
    if (uVar12 != 0) {
      lVar26 = *param_1;
      *(uint *)(lVar26 + 0x114) = uVar12;
      *(ulong *)(lVar26 + 0x100) = (ulong)uVar12 * 1000;
    }
    iVar11 = (**(code **)(*local_308 + 0x20))(local_308);
    if (iVar11 == 3) {
      if (plVar25 == (long *)0x0) {
        lVar26 = 0;
      }
      else {
        lVar26 = ___dynamic_cast(plVar25,&PTR_DAT_09c37aa0,&PTR_DAT_09de95b8,0);
        plVar25 = local_300;
        if ((lVar26 != 0) && (local_300 != (long *)0x0)) {
          plVar1 = local_300 + 1;
          *plVar1 = *plVar1 + 1;
          uVar20 = *(ulong *)(lVar26 + 0x188);
          LOAcquire();
          lVar26 = *plVar1;
          *plVar1 = lVar26 + -1;
          LORelease();
          if (lVar26 == 0) {
            (**(code **)(*local_300 + 0x10))(local_300);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar25);
          }
          goto LAB_030f0970;
        }
      }
      uVar20 = *(ulong *)(lVar26 + 0x188);
    }
    else {
      uVar20 = 0;
    }
LAB_030f0970:
    lVar26 = *param_1;
    if (uVar20 < (ulong)*(uint *)(lVar26 + 0x114) * 1000) {
      FUN_0466aca8(&local_150);
      FUN_01205740(&local_100,local_150);
      FUN_02891054(&local_400,local_100);
      uVar20 = FUN_03968f68(local_400,ppppplVar3,plVar28,*(undefined4 *)(lVar26 + 0x114),1);
      plVar25 = plStack_3f8;
      if (plStack_3f8 != (long *)0x0) {
        LOAcquire();
        lVar26 = plStack_3f8[1];
        plStack_3f8[1] = lVar26 + -1;
        LORelease();
        if (lVar26 == 0) {
          (**(code **)(*plStack_3f8 + 0x10))(plStack_3f8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar25);
        }
      }
      pppplVar9 = pppplStack_f8;
      if ((long *****)pppplStack_f8 != (long *****)0x0) {
        LOAcquire();
        pppplVar7 = (long ****)pppplStack_f8[1];
        pppplStack_f8[1] = (long ***)((long)pppplVar7 + -1);
        LORelease();
        if (pppplVar7 == (long ****)0x0) {
          (*(code *)(*pppplVar9)[2])(pppplVar9);
          __ZNSt3__119__shared_weak_count14__release_weakEv(pppplVar9);
        }
      }
      plVar25 = (long *)CONCAT71(uStack_147,uStack_148);
      if (plVar25 != (long *)0x0) {
        LOAcquire();
        lVar26 = plVar25[1];
        plVar25[1] = lVar26 + -1;
        LORelease();
        if (lVar26 == 0) {
          (**(code **)(*plVar25 + 0x10))(plVar25);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar25);
        }
      }
    }
    iVar13 = thunk_FUN_05e1d97c(2);
    if (iVar13 != 0) {
      FUN_0488143c(local_2f8);
      ppppplVar4 = (long *****)local_2f8[0];
      if (-1 < cStack_2e1) {
        ppppplVar4 = local_2f8;
      }
      if ((DAT_0a3d9838 & 1) == 0) {
        uVar23 = 0;
        do {
          (&DAT_0a3d9820)[uVar23] = (&DAT_088b055e)[uVar23] + 0x8a ^ (&DAT_088b054e)[uVar23 & 0xf];
          uVar23 = uVar23 + 1;
        } while (uVar23 != 0x18);
        DAT_0a3d9838 = 1;
      }
      if ((DAT_0a3d9a82 & 1) == 0) {
        uVar23 = 0;
        do {
          (&DAT_0a3d9a6c)[uVar23] = (&DAT_088b0905)[uVar23] + 0x8a ^ (&DAT_088b08f5)[uVar23 & 0xf];
          uVar23 = uVar23 + 1;
        } while (uVar23 != 0x16);
        DAT_0a3d9a82 = 1;
      }
      FUN_05e1d050(&local_400,2,ppppplVar4,&DAT_0a3d9820,&DAT_0a3d9a6c,0x37,0,0);
      local_150 = (long ****)plVar29[0x12];
      if (-1 < *(char *)((long)plVar29 + 0xa7)) {
        local_150 = (long ****)ppppplVar3;
      }
      uStack_148 = 0;
      uVar12 = *(uint *)(*param_1 + 0x114);
      local_1a0 = (long ****)0x0;
      if ((DAT_0a3d9bbd & 1) == 0) {
        uVar23 = 0;
        do {
          (&DAT_0a3d9b75)[uVar23] = (&DAT_088b0a63)[uVar23] + 0x8a ^ (&DAT_088b0a53)[uVar23 & 0xf];
          uVar23 = uVar23 + 1;
        } while (uVar23 != 0x48);
        DAT_0a3d9bbd = 1;
      }
      uVar23 = (ulong)uVar12;
      lVar26 = 0;
      do {
        lVar21 = lVar26;
        uVar12 = (uint)uVar23;
        *(undefined1 *)((long)&local_198 + lVar21) =
             (&DAT_0a3d9b75)[uVar12 + (int)(uVar23 / 10) * -10 + 0x23];
        uVar23 = uVar23 / 10;
        lVar26 = lVar21 + 1;
      } while (9 < uVar12);
      *(undefined1 *)((long)&local_198 + lVar21 + 1) = 0;
      if (8 < lVar21 + 8U) {
        puVar22 = (undefined1 *)((long)&local_198 + lVar21);
        puVar8 = (undefined1 *)((long)&local_198 + 1);
        do {
          uVar5 = *puVar22;
          *puVar22 = puVar8[-1];
          puVar8[-1] = uVar5;
          bVar6 = puVar8 < puVar22 + -1;
          puVar22 = puVar22 + -1;
          puVar8 = puVar8 + 1;
        } while (bVar6);
      }
      local_1a0 = (long ****)&local_198;
      local_1f0 = (undefined8 *)0x0;
      lVar26 = 0;
      do {
        lVar21 = lVar26;
        uVar12 = (uint)uVar18;
        *(undefined1 *)((long)&local_1e8 + lVar21) =
             (&DAT_0a3d9b75)[uVar12 + (int)((uVar18 & 0xffffffff) / 10) * -10 + 0x23];
        lVar26 = lVar21 + 1;
        uVar18 = (uVar18 & 0xffffffff) / 10;
      } while (9 < uVar12);
      *(undefined1 *)((long)&local_1e8 + lVar21 + 1) = 0;
      if (8 < lVar21 + 8U) {
        puVar22 = (undefined1 *)((long)&local_1e8 + lVar21);
        puVar8 = (undefined1 *)((long)&local_1e8 + 1);
        do {
          uVar5 = *puVar22;
          *puVar22 = puVar8[-1];
          puVar8[-1] = uVar5;
          bVar6 = puVar8 < puVar22 + -1;
          puVar22 = puVar22 + -1;
          puVar8 = puVar8 + 1;
        } while (bVar6);
      }
      local_1f0 = &local_1e8;
      lVar26 = 0;
      uVar18 = uVar20;
      do {
        lVar21 = lVar26;
        *(undefined1 *)((long)&local_238 + lVar21) = *(undefined1 *)(uVar18 % 10 + 0xa3d9b98);
        bVar6 = 9 < uVar18;
        lVar26 = lVar21 + 1;
        uVar18 = uVar18 / 10;
      } while (bVar6);
      local_240 = (long ****)&local_238;
      *(undefined1 *)((long)&local_238 + lVar21 + 1) = 0;
      if (8 < lVar21 + 8U) {
        puVar22 = (undefined1 *)((long)&local_238 + lVar21);
        puVar8 = (undefined1 *)((long)&local_238 + 1);
        do {
          uVar5 = *puVar22;
          *puVar22 = puVar8[-1];
          puVar8[-1] = uVar5;
          bVar6 = puVar8 < puVar22 + -1;
          puVar22 = puVar22 + -1;
          puVar8 = puVar8 + 1;
        } while (bVar6);
      }
      local_290 = (long *)plVar16[0x17];
      if (-1 < *(char *)((long)plVar16 + 0xcf)) {
        local_290 = plVar28;
      }
      local_288 = 0;
      if (iVar11 == 3) {
        local_2e0 = (undefined4 *)&DAT_0a3d9bbe;
        if ((DAT_0a3d9bc3 & 1) == 0) {
          DAT_0a3d9bbe = 0x7274;
          DAT_0a3d9bc0 = 0x75;
          puVar22 = &DAT_0a3d9bc2;
          puVar8 = &DAT_0a3d9bc1;
          puVar24 = &DAT_0a3d9bc3;
LAB_030f0df8:
          *puVar8 = 0x65;
          *puVar22 = 0;
          *puVar24 = 1;
        }
      }
      else {
        local_2e0 = &DAT_0a3d9bc4;
        if ((DAT_0a3d9bca & 1) == 0) {
          DAT_0a3d9bc4 = (undefined4)DAT_0847fe48;
          puVar8 = &DAT_0a3d9bc8;
          puVar22 = &DAT_0a3d9bc9;
          puVar24 = &DAT_0a3d9bca;
          goto LAB_030f0df8;
        }
      }
      local_2d8 = 0;
      if ((DAT_0a3d9b39 & 1) == 0) {
        uVar18 = 0;
        do {
          (&DAT_0a3d9acc)[uVar18] = (&DAT_088b0983)[uVar18] + 0x8a ^ (&DAT_088b0973)[uVar18 & 0xf];
          uVar18 = uVar18 + 1;
        } while (uVar18 != 0x6d);
        DAT_0a3d9b39 = 1;
      }
      local_100 = (long ****)&local_150;
      pppplStack_f8 = (long ****)&local_1a0;
      local_f0 = &local_1f0;
      local_e8 = (long ****)&local_240;
      pplStack_e0 = &local_290;
      local_d8 = &local_2e0;
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
      FUN_05e1d31c(&local_400,&DAT_0a3d9acc,&local_100);
      thunk_FUN_05e1d0bc(&local_400);
      if (cStack_2e1 < '\0') {
        uVar18 = CONCAT17(cStack_2e1,local_2e8);
LAB_030f0ec8:
        __ZdlPvm(local_2f8[0],uVar18 & 0x7fffffffffffffff);
      }
    }
  }
  else {
    FUN_0466aca8(&local_150);
    FUN_01205740(&local_100,local_150);
    FUN_02891054(&local_400,local_100);
    uVar20 = FUN_03967ec8(local_400,ppppplVar3,*(undefined4 *)((long)puVar15 + 300),1);
    plVar16 = plStack_3f8;
    if (plStack_3f8 != (long *)0x0) {
      LOAcquire();
      lVar26 = plStack_3f8[1];
      plStack_3f8[1] = lVar26 + -1;
      LORelease();
      if (lVar26 == 0) {
        (**(code **)(*plStack_3f8 + 0x10))(plStack_3f8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar16);
      }
    }
    pppplVar9 = pppplStack_f8;
    if ((long *****)pppplStack_f8 != (long *****)0x0) {
      LOAcquire();
      pppplVar7 = (long ****)pppplStack_f8[1];
      pppplStack_f8[1] = (long ***)((long)pppplVar7 + -1);
      LORelease();
      if (pppplVar7 == (long ****)0x0) {
        (*(code *)(*pppplVar9)[2])(pppplVar9);
        __ZNSt3__119__shared_weak_count14__release_weakEv(pppplVar9);
      }
    }
    plVar16 = (long *)CONCAT71(uStack_147,uStack_148);
    if (plVar16 != (long *)0x0) {
      LOAcquire();
      lVar26 = plVar16[1];
      plVar16[1] = lVar26 + -1;
      LORelease();
      if (lVar26 == 0) {
        (**(code **)(*plVar16 + 0x10))(plVar16);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar16);
      }
    }
    iVar11 = thunk_FUN_05e1d97c(2);
    if (iVar11 != 0) {
      FUN_0488143c(&local_240);
      ppppplVar4 = (long *****)local_240;
      if (-1 < cStack_229) {
        ppppplVar4 = &local_240;
      }
      if ((DAT_0a3d9838 & 1) == 0) {
        uVar18 = 0;
        do {
          (&DAT_0a3d9820)[uVar18] = (&DAT_088b055e)[uVar18] + 0x8a ^ (&DAT_088b054e)[uVar18 & 0xf];
          uVar18 = uVar18 + 1;
        } while (uVar18 != 0x18);
        DAT_0a3d9838 = 1;
      }
      if ((DAT_0a3d9a82 & 1) == 0) {
        uVar18 = 0;
        do {
          (&DAT_0a3d9a6c)[uVar18] = (&DAT_088b0905)[uVar18] + 0x8a ^ (&DAT_088b08f5)[uVar18 & 0xf];
          uVar18 = uVar18 + 1;
        } while (uVar18 != 0x16);
        DAT_0a3d9a82 = 1;
      }
      FUN_05e1d050(&local_400,2,ppppplVar4,&DAT_0a3d9820,&DAT_0a3d9a6c,0x3a,0,0);
      local_150 = (long ****)plVar29[0x12];
      if (-1 < *(char *)((long)plVar29 + 0xa7)) {
        local_150 = (long ****)ppppplVar3;
      }
      uStack_148 = 0;
      uVar12 = *(uint *)(*param_1 + 0x114);
      local_1a0 = (long ****)0x0;
      if ((DAT_0a3d9bbd & 1) == 0) {
        uVar18 = 0;
        do {
          (&DAT_0a3d9b75)[uVar18] = (&DAT_088b0a63)[uVar18] + 0x8a ^ (&DAT_088b0a53)[uVar18 & 0xf];
          uVar18 = uVar18 + 1;
        } while (uVar18 != 0x48);
        DAT_0a3d9bbd = 1;
      }
      uVar18 = (ulong)uVar12;
      lVar26 = 0;
      do {
        lVar21 = lVar26;
        uVar12 = (uint)uVar18;
        *(undefined1 *)((long)&local_198 + lVar21) =
             (&DAT_0a3d9b75)[uVar12 + (int)(uVar18 / 10) * -10 + 0x23];
        uVar18 = uVar18 / 10;
        lVar26 = lVar21 + 1;
      } while (9 < uVar12);
      *(undefined1 *)((long)&local_198 + lVar21 + 1) = 0;
      if (8 < lVar21 + 8U) {
        puVar22 = (undefined1 *)((long)&local_198 + lVar21);
        puVar8 = (undefined1 *)((long)&local_198 + 1);
        do {
          uVar5 = *puVar22;
          *puVar22 = puVar8[-1];
          puVar8[-1] = uVar5;
          bVar6 = puVar8 < puVar22 + -1;
          puVar22 = puVar22 + -1;
          puVar8 = puVar8 + 1;
        } while (bVar6);
      }
      local_1a0 = (long ****)&local_198;
      local_1f0 = (undefined8 *)0x0;
      lVar26 = 0;
      uVar18 = uVar20;
      do {
        lVar21 = lVar26;
        *(undefined1 *)((long)&local_1e8 + lVar21) = *(undefined1 *)(uVar18 % 10 + 0xa3d9b98);
        bVar6 = 9 < uVar18;
        lVar26 = lVar21 + 1;
        uVar18 = uVar18 / 10;
      } while (bVar6);
      local_1f0 = &local_1e8;
      *(undefined1 *)((long)&local_1e8 + lVar21 + 1) = 0;
      if (8 < lVar21 + 8U) {
        puVar22 = (undefined1 *)((long)&local_1e8 + lVar21);
        puVar8 = (undefined1 *)((long)&local_1e8 + 1);
        do {
          uVar5 = *puVar22;
          *puVar22 = puVar8[-1];
          puVar8[-1] = uVar5;
          bVar6 = puVar8 < puVar22 + -1;
          puVar22 = puVar22 + -1;
          puVar8 = puVar8 + 1;
        } while (bVar6);
      }
      if ((DAT_0a3d9b74 & 1) == 0) {
        uVar18 = 0;
        do {
          (&DAT_0a3d9b3a)[uVar18] = (&DAT_088b0a00)[uVar18] + 0x8a ^ (&DAT_088b09f0)[uVar18 & 0xf];
          uVar18 = uVar18 + 1;
        } while (uVar18 != 0x3a);
        DAT_0a3d9b74 = 1;
      }
      local_100 = (long ****)&local_150;
      pppplStack_f8 = (long ****)&local_1a0;
      local_f0 = &local_1f0;
      pplStack_e0 = (long **)0x0;
      local_e8 = (long ****)0x0;
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
      local_88 = 0;
      FUN_05e1d31c(&local_400,&DAT_0a3d9b3a,&local_100);
      thunk_FUN_05e1d0bc(&local_400);
      if (cStack_229 < '\0') {
        uVar18 = CONCAT17(cStack_229,local_230);
        local_2f8[0] = local_240;
        goto LAB_030f0ec8;
      }
    }
  }
  plVar29 = local_300;
  lVar26 = *param_1;
  *(ulong *)(lVar26 + 0x100) = uVar20;
  *(undefined4 *)(lVar26 + 0x128) = 1;
  if (local_300 != (long *)0x0) {
    LOAcquire();
    lVar26 = local_300[1];
    local_300[1] = lVar26 + -1;
    LORelease();
    if (lVar26 == 0) {
      (**(code **)(*local_300 + 0x10))(local_300);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar29);
    }
  }
  lVar26 = *param_1;
  uVar17 = (**(code **)(**(long **)(param_2 + 8) + 0x10))();
  FUN_04cbbd20(lVar26,uVar17);
  lVar26 = *param_1;
  uVar17 = (**(code **)(**(long **)(param_2 + 8) + 0x18))();
  FUN_04cbcfd4(lVar26,uVar17);
  lVar26 = *param_1;
  uVar14 = 1;
  if (*(char *)(param_2 + 0xb0) == '\0') {
    uVar14 = 2;
  }
  *(undefined4 *)(lVar26 + 0x118) = uVar14;
  puVar27 = *(undefined8 **)(lVar26 + 0x230);
  local_1e8 = *(long **)(lVar26 + 0x238);
  if (local_1e8 != (long *)0x0) {
    local_1e8[1] = local_1e8[1] + 1;
  }
  local_1f0 = puVar27;
  if (puVar27 != (undefined8 *)0x0) {
    lVar26 = *(long *)(param_2 + 8);
    if (*(char *)(lVar26 + 0x47) < '\0') {
      if (*(long *)(lVar26 + 0x38) != 0) goto LAB_030f0f9c;
LAB_030f10a4:
      cVar19 = *(char *)(lVar26 + 0x77);
      if (cVar19 < '\0') goto LAB_030f1084;
LAB_030f10ac:
      if (cVar19 == '\0') goto LAB_030f108c;
LAB_030f10b0:
      plStack_3f8 = (long *)__Znwm(0x30);
      plStack_3f8[1] = 0;
      plStack_3f8[2] = 0;
      *plStack_3f8 = (long)&PTR_FUN_09de9680;
      plStack_3f8[4] = 0;
      plStack_3f8[5] = 0;
      local_400 = plStack_3f8 + 3;
      *local_400 = 0;
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (local_400,lVar26 + 0x60);
      plVar29 = plStack_3f8;
      if (plStack_3f8 != (long *)0x0) {
        plVar16 = plStack_3f8 + 1;
        *plVar16 = *plVar16 + 1;
        *plVar16 = *plVar16 + 1;
      }
      plVar16 = (long *)local_1f0[0x10];
      local_1f0[0xf] = local_400;
      local_1f0[0x10] = plStack_3f8;
      if (plVar16 != (long *)0x0) {
        LOAcquire();
        lVar26 = plVar16[1];
        plVar16[1] = lVar26 + -1;
        LORelease();
        if (lVar26 == 0) {
          (**(code **)(*plVar16 + 0x10))(plVar16);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar16);
        }
      }
      if (plVar29 != (long *)0x0) {
        LOAcquire();
        lVar26 = plVar29[1];
        plVar29[1] = lVar26 + -1;
        LORelease();
        if (lVar26 == 0) {
          (**(code **)(*plVar29 + 0x10))(plVar29);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar29);
        }
      }
      plVar29 = plStack_3f8;
      if (plStack_3f8 != (long *)0x0) {
        LOAcquire();
        lVar26 = plStack_3f8[1];
        plStack_3f8[1] = lVar26 + -1;
        LORelease();
        if (lVar26 == 0) {
          (**(code **)(*plStack_3f8 + 0x10))(plStack_3f8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar29);
        }
      }
      lVar26 = *(long *)(param_2 + 8);
      cVar19 = *(char *)(lVar26 + 0x2f);
      if (-1 < cVar19) goto LAB_030f1094;
LAB_030f119c:
      if (*(long *)(lVar26 + 0x20) != 0) goto LAB_030f11a4;
    }
    else {
      if (*(char *)(lVar26 + 0x47) == '\0') goto LAB_030f10a4;
LAB_030f0f9c:
      plVar29 = (long *)__Znwm(0x30);
      plVar28 = plVar29 + 1;
      *plVar28 = 0;
      plVar29[2] = 0;
      *plVar29 = (long)&PTR_FUN_09de9630;
      plVar16 = plVar29 + 3;
      *plVar16 = 0;
      plVar29[4] = 0;
      plVar29[5] = 0;
      local_400 = plVar16;
      plStack_3f8 = plVar29;
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (plVar16,lVar26 + 0x30);
      if (plVar29 != (long *)0x0) {
        *plVar28 = *plVar28 + 1;
        *plVar28 = *plVar28 + 1;
      }
      plVar25 = (long *)puVar27[0x12];
      puVar27[0x11] = plVar16;
      puVar27[0x12] = plVar29;
      if (plVar25 != (long *)0x0) {
        LOAcquire();
        lVar26 = plVar25[1];
        plVar25[1] = lVar26 + -1;
        LORelease();
        if (lVar26 == 0) {
          (**(code **)(*plVar25 + 0x10))(plVar25);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar25);
        }
      }
      if (plVar29 != (long *)0x0) {
        LOAcquire();
        lVar26 = *plVar28;
        *plVar28 = lVar26 + -1;
        LORelease();
        if (lVar26 == 0) {
          (**(code **)(*plVar29 + 0x10))(plVar29);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar29);
        }
      }
      plVar29 = plStack_3f8;
      if (plStack_3f8 != (long *)0x0) {
        LOAcquire();
        lVar26 = plStack_3f8[1];
        plStack_3f8[1] = lVar26 + -1;
        LORelease();
        if (lVar26 == 0) {
          (**(code **)(*plStack_3f8 + 0x10))(plStack_3f8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar29);
        }
      }
      lVar26 = *(long *)(param_2 + 8);
      cVar19 = *(char *)(lVar26 + 0x77);
      if (-1 < cVar19) goto LAB_030f10ac;
LAB_030f1084:
      if (*(long *)(lVar26 + 0x68) != 0) goto LAB_030f10b0;
LAB_030f108c:
      cVar19 = *(char *)(lVar26 + 0x2f);
      if (cVar19 < '\0') goto LAB_030f119c;
LAB_030f1094:
      if (cVar19 != '\0') {
LAB_030f11a4:
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (local_1f0 + 0x1a,lVar26 + 0x18);
      }
    }
    uVar17 = FUN_04cbd624(*param_1);
    iVar11 = FUN_04bb4a4c();
    if (iVar11 != 0) {
      local_238 = (long ****)__Znwm(0xa8);
      local_238[1] = (long ***)0x0;
      local_238[2] = (long ***)0x0;
      *local_238 = (long ***)&PTR_FUN_09de96d0;
      local_238[0x10] = (long ***)0x0;
      local_238[0xf] = (long ***)0x0;
      local_238[0xe] = (long ***)0x0;
      local_238[0xd] = (long ***)0x0;
      local_238[0xc] = (long ***)0x0;
      local_238[0xb] = (long ***)0x0;
      local_238[10] = (long ***)0x0;
      local_238[9] = (long ***)0x0;
      local_238[8] = (long ***)0x0;
      local_238[7] = (long ***)0x0;
      local_238[6] = (long ***)0x0;
      local_238[5] = (long ***)0x0;
      local_238[0x11] = (long ***)0x0;
      local_238[0x12] = (long ***)0x0;
      local_240 = local_238 + 3;
      local_238[4] = (long ***)0x0;
      *local_240 = (long ***)0x0;
      *(undefined4 *)local_240 = 1;
      local_238[0x13] = (long ***)0x0;
      local_238[0x14] = (long ***)0x0;
      *(undefined8 *)((long)local_238 + 0x85) = 0;
      *(undefined8 *)((long)local_238 + 0x7d) = 0;
      local_238[0xd] = (long ***)0x0;
      local_238[0xc] = (long ***)0x0;
      local_238[0xf] = (long ***)0x0;
      local_238[0xe] = (long ***)0x0;
      local_238[9] = (long ***)0x0;
      local_238[8] = (long ***)0x0;
      local_238[0xb] = (long ***)0x0;
      local_238[10] = (long ***)0x0;
      local_238[7] = (long ***)0x0;
      local_238[6] = (long ***)0x0;
      local_238[5] = (long ***)0x0;
      local_238[4] = (long ***)0x0;
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(local_238 + 4,uVar17)
      ;
      iVar11 = FUN_04bb4c9c(uVar17);
      if (iVar11 == 0) {
        local_400 = (long *)&SUB_aaaaaaaaaaaaaaaa;
        plStack_3f8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
        FUN_0466aca8(&local_1a0);
        FUN_01205740(&local_150,local_1a0);
        FUN_023f9000(&local_100,local_150);
        FUN_027de17c(&local_400,local_100,uVar17);
        pppplVar9 = pppplStack_f8;
        if ((long *****)pppplStack_f8 != (long *****)0x0) {
          LOAcquire();
          pppplVar7 = (long ****)pppplStack_f8[1];
          pppplStack_f8[1] = (long ***)((long)pppplVar7 + -1);
          LORelease();
          if (pppplVar7 == (long ****)0x0) {
            (*(code *)(*pppplVar9)[2])(pppplVar9);
            __ZNSt3__119__shared_weak_count14__release_weakEv(pppplVar9);
          }
        }
        plVar29 = (long *)CONCAT71(uStack_147,uStack_148);
        if (plVar29 != (long *)0x0) {
          LOAcquire();
          lVar26 = plVar29[1];
          plVar29[1] = lVar26 + -1;
          LORelease();
          if (lVar26 == 0) {
            (**(code **)(*plVar29 + 0x10))(plVar29);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar29);
          }
        }
        ppppplVar3 = local_198;
        if (local_198 != (long *****)0x0) {
          LOAcquire();
          pppplVar9 = local_198[1];
          local_198[1] = (long ****)((long)pppplVar9 + -1);
          LORelease();
          if (pppplVar9 == (long ****)0x0) {
            (*(code *)(*local_198)[2])(local_198);
            __ZNSt3__119__shared_weak_count14__release_weakEv(ppppplVar3);
          }
        }
        local_240[4] = (long ***)local_400[10];
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (local_240 + 0xf,local_400 + 7);
      }
      else {
        local_400 = (long *)&SUB_aaaaaaaaaaaaaaaa;
        plStack_3f8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
        FUN_0466aca8(&local_1a0);
        FUN_01205740(&local_150,local_1a0);
        FUN_023f9000(&local_100,local_150);
        FUN_027dfc08(&local_400,local_100,uVar17);
        pppplVar9 = pppplStack_f8;
        if ((long *****)pppplStack_f8 != (long *****)0x0) {
          LOAcquire();
          pppplVar7 = (long ****)pppplStack_f8[1];
          pppplStack_f8[1] = (long ***)((long)pppplVar7 + -1);
          LORelease();
          if (pppplVar7 == (long ****)0x0) {
            (*(code *)(*pppplVar9)[2])(pppplVar9);
            __ZNSt3__119__shared_weak_count14__release_weakEv(pppplVar9);
          }
        }
        plVar29 = (long *)CONCAT71(uStack_147,uStack_148);
        if (plVar29 != (long *)0x0) {
          LOAcquire();
          lVar26 = plVar29[1];
          plVar29[1] = lVar26 + -1;
          LORelease();
          if (lVar26 == 0) {
            (**(code **)(*plVar29 + 0x10))(plVar29);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar29);
          }
        }
        ppppplVar3 = local_198;
        if (local_198 != (long *****)0x0) {
          LOAcquire();
          pppplVar9 = local_198[1];
          local_198[1] = (long ****)((long)pppplVar9 + -1);
          LORelease();
          if (pppplVar9 == (long ****)0x0) {
            (*(code *)(*local_198)[2])(local_198);
            __ZNSt3__119__shared_weak_count14__release_weakEv(ppppplVar3);
          }
        }
        local_240[4] = (long ***)local_400[8];
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (local_240 + 0xf,local_400 + 4);
      }
      plVar29 = plStack_3f8;
      if (plStack_3f8 != (long *)0x0) {
        LOAcquire();
        lVar26 = plStack_3f8[1];
        plStack_3f8[1] = lVar26 + -1;
        LORelease();
        if (lVar26 == 0) {
          (**(code **)(*plStack_3f8 + 0x10))(plStack_3f8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar29);
        }
      }
      local_310 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_328 = &SUB_aaaaaaaaaaaaaaaa;
      local_330 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_318 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_320 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_348 = &SUB_aaaaaaaaaaaaaaaa;
      local_350 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_338 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_340 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_368 = &SUB_aaaaaaaaaaaaaaaa;
      local_370 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_358 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_360 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_388 = &SUB_aaaaaaaaaaaaaaaa;
      local_390 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_378 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_380 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_3a8 = &SUB_aaaaaaaaaaaaaaaa;
      local_3b0 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_398 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_3a0 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_3c8 = &SUB_aaaaaaaaaaaaaaaa;
      local_3d0 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_3b8 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_3c0 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_3e8 = &SUB_aaaaaaaaaaaaaaaa;
      local_3f0 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_3d8 = &SUB_aaaaaaaaaaaaaaaa;
      puStack_3e0 = &SUB_aaaaaaaaaaaaaaaa;
      plStack_3f8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
      local_400 = (long *)&SUB_aaaaaaaaaaaaaaaa;
      FUN_0466aca8(&local_1a0);
      FUN_01205740(&local_150,local_1a0);
      FUN_023f9000(&local_100,local_150);
      FUN_027e8598(&local_400,local_100,local_240 + 0xf);
      pppplVar9 = pppplStack_f8;
      if ((long *****)pppplStack_f8 != (long *****)0x0) {
        LOAcquire();
        pppplVar7 = (long ****)pppplStack_f8[1];
        pppplStack_f8[1] = (long ***)((long)pppplVar7 + -1);
        LORelease();
        if (pppplVar7 == (long ****)0x0) {
          (*(code *)(*pppplVar9)[2])(pppplVar9);
          __ZNSt3__119__shared_weak_count14__release_weakEv(pppplVar9);
        }
      }
      plVar29 = (long *)CONCAT71(uStack_147,uStack_148);
      if (plVar29 != (long *)0x0) {
        LOAcquire();
        lVar26 = plVar29[1];
        plVar29[1] = lVar26 + -1;
        LORelease();
        if (lVar26 == 0) {
          (**(code **)(*plVar29 + 0x10))(plVar29);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar29);
        }
      }
      ppppplVar3 = local_198;
      if (local_198 != (long *****)0x0) {
        LOAcquire();
        pppplVar9 = local_198[1];
        local_198[1] = (long ****)((long)pppplVar9 + -1);
        LORelease();
        if (pppplVar9 == (long ****)0x0) {
          (*(code *)(*local_198)[2])(local_198);
          __ZNSt3__119__shared_weak_count14__release_weakEv(ppppplVar3);
        }
      }
      pppplVar9 = local_240;
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (local_240 + 5,(ulong)&local_400 | 8);
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (pppplVar9 + 8,&puStack_3e0);
      uVar12 = _time(0);
      _srand(uVar12);
      pppplStack_f8 = (long ****)&SUB_aaaaaaaaaaaaaaaa;
      local_f0 = (undefined8 **)&SUB_aaaaaaaaaaaaaaaa;
      local_100 = (long ****)&SUB_aaaaaaaaaaaaaaaa;
      lVar26 = *param_1;
      if (*(char *)(lVar26 + 0x147) < '\0') {
        FUN_00018d20(&local_100,*(undefined8 *)(lVar26 + 0x130),*(undefined8 *)(lVar26 + 0x138));
      }
      else {
        pppplStack_f8 = *(long *****)(lVar26 + 0x138);
        local_100 = *(long *****)(lVar26 + 0x130);
        local_f0 = *(undefined8 ***)(lVar26 + 0x140);
      }
      pppplVar7 = local_240;
      pppplVar9 = (long ****)local_240[6];
      ppppplVar3 = (long *****)local_240[5];
      if (-1 < (char)*(byte *)((long)local_240 + 0x3f)) {
        pppplVar9 = (long ****)(ulong)*(byte *)((long)local_240 + 0x3f);
        ppppplVar3 = (long *****)(local_240 + 5);
      }
      uVar17 = __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
                         (&local_100,ppppplVar3,pppplVar9);
      FUN_0474715c();
      __ZNSt3__19to_stringEy(&local_150);
      uVar18 = CONCAT71(uStack_147,uStack_148);
      ppppplVar3 = (long *****)local_150;
      if (-1 < (char)bStack_139) {
        uVar18 = (ulong)bStack_139;
        ppppplVar3 = &local_150;
      }
      uVar17 = __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
                         (uVar17,ppppplVar3,uVar18);
      iVar11 = _rand();
      __ZNSt3__19to_stringEi(&local_1a0,iVar11);
      ppppplVar3 = (long *****)local_1a0;
      if (-1 < (char)bStack_189) {
        local_198 = (long *****)(ulong)bStack_189;
        ppppplVar3 = &local_1a0;
      }
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
                (uVar17,ppppplVar3,local_198);
      if ((char)bStack_189 < '\0') {
        __ZdlPvm(local_1a0,CONCAT17(bStack_189,local_190) & 0x7fffffffffffffff);
      }
      if ((char)bStack_139 < '\0') {
        __ZdlPvm(local_150,CONCAT17(bStack_139,local_140) & 0x7fffffffffffffff);
      }
      local_1a0 = local_100;
      if (-1 < (long)local_f0._7_1_) {
        local_1a0 = (long ****)&local_100;
      }
      local_198 = (long *****)pppplStack_f8;
      if (-1 < (long)local_f0) {
        local_198 = (long *****)(long)local_f0._7_1_;
      }
      FUN_00034078(&local_150,&local_1a0);
      if (*(char *)((long)pppplVar7 + 0x6f) < '\0') {
        __ZdlPvm(pppplVar7[0xb],(ulong)pppplVar7[0xd] & 0x7fffffffffffffff);
      }
      pppplVar9 = local_238;
      pppplVar7[0xc] = (long ***)CONCAT71(uStack_147,uStack_148);
      pppplVar7[0xb] = (long ***)local_150;
      pppplVar7[0xd] = (long ***)CONCAT17(bStack_139,local_140);
      if (local_238 != (long ****)0x0) {
        pppplVar2 = local_238 + 1;
        *pppplVar2 = (long ***)((long)*pppplVar2 + 1);
        *pppplVar2 = (long ***)((long)*pppplVar2 + 1);
      }
      plVar29 = (long *)local_1f0[0x14];
      local_1f0[0x13] = pppplVar7;
      local_1f0[0x14] = local_238;
      if (plVar29 != (long *)0x0) {
        LOAcquire();
        lVar26 = plVar29[1];
        plVar29[1] = lVar26 + -1;
        LORelease();
        if (lVar26 == 0) {
          (**(code **)(*plVar29 + 0x10))(plVar29);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar29);
        }
      }
      if (pppplVar9 != (long ****)0x0) {
        LOAcquire();
        ppplVar10 = pppplVar9[1];
        pppplVar9[1] = (long ***)((long)ppplVar10 + -1);
        LORelease();
        if (ppplVar10 == (long ***)0x0) {
          (*(code *)(*pppplVar9)[2])(pppplVar9);
          __ZNSt3__119__shared_weak_count14__release_weakEv(pppplVar9);
        }
      }
      FUN_04cbb728(*param_1,local_240 + 5);
      FUN_027f4cbc(&local_400);
      pppplVar9 = local_238;
      if (local_238 != (long ****)0x0) {
        LOAcquire();
        ppplVar10 = local_238[1];
        local_238[1] = (long ***)((long)ppplVar10 + -1);
        LORelease();
        if (ppplVar10 == (long ***)0x0) {
          (*(code *)(*local_238)[2])(local_238);
          __ZNSt3__119__shared_weak_count14__release_weakEv(pppplVar9);
        }
      }
    }
  }
  iVar11 = (**(code **)(**(long **)(param_2 + 8) + 0x20))();
  if (iVar11 == 2) {
    if ((*(long *)(param_2 + 8) == 0) ||
       (local_400 = (long *)___dynamic_cast(*(long *)(param_2 + 8),&PTR_DAT_09c37aa0,
                                            &PTR_DAT_09c3edd0,0), local_400 == (long *)0x0)) {
      local_400 = (long *)0x0;
      plStack_3f8 = (long *)0x0;
    }
    else {
      plStack_3f8 = *(long **)(param_2 + 0x10);
      lVar26 = 0;
      if (plStack_3f8 != (long *)0x0) {
        lVar26 = plStack_3f8[1];
        plStack_3f8[1] = lVar26 + 1;
      }
      iVar11 = FUN_04d396d4(lVar26,local_400 + 0x1d);
      if (iVar11 == 9) {
        lVar26 = *param_1;
        uVar14 = FUN_04d396d4(local_400 + 0x1d);
        *(undefined4 *)(lVar26 + 0x128) = uVar14;
      }
    }
LAB_030f1848:
    plVar29 = plStack_3f8;
    if (plStack_3f8 != (long *)0x0) {
      LOAcquire();
      lVar26 = plStack_3f8[1];
      plStack_3f8[1] = lVar26 + -1;
      LORelease();
      if (lVar26 == 0) {
        (**(code **)(*plStack_3f8 + 0x10))(plStack_3f8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar29);
      }
    }
  }
  else if ((*(long *)(param_2 + 8) != 0) &&
          (plVar29 = (long *)___dynamic_cast(*(long *)(param_2 + 8),&PTR_DAT_09c37aa0,
                                             &PTR_DAT_09eb2580,0), plVar29 != (long *)0x0)) {
    plStack_3f8 = *(long **)(param_2 + 0x10);
    if (plStack_3f8 != (long *)0x0) {
      plStack_3f8[1] = plStack_3f8[1] + 1;
    }
    local_400 = plVar29;
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (*param_1 + 0x260,plVar29 + 0xb0);
    goto LAB_030f1848;
  }
  plVar29 = local_1e8;
  if (*(int *)(*param_1 + 0x128) == 0) {
    *(undefined4 *)(*param_1 + 0x128) = 1;
  }
  if (local_1e8 != (long *)0x0) {
    LOAcquire();
    lVar26 = local_1e8[1];
    local_1e8[1] = lVar26 + -1;
    LORelease();
    if (lVar26 == 0) {
      (**(code **)(*local_1e8 + 0x10))(local_1e8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar29);
    }
  }
LAB_030f18bc:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_78) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


