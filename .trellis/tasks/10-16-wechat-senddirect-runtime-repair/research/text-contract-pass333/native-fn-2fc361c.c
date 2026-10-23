// Ghidra inferred pseudocode; requested=0x2fc361c
// entry=02fc361c end=02fc4a83

/* WARNING: Removing unreachable block (ram,0x02fc372c) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_02fc361c(ulong *param_1,long param_2,long param_3)

{
  undefined1 *puVar1;
  long **pplVar2;
  uint3 uVar3;
  ulong uVar4;
  ulong uVar5;
  int iVar6;
  ulong uVar7;
  long lVar8;
  long *plVar9;
  char *pcVar10;
  undefined8 *puVar11;
  undefined8 *puVar12;
  long *plVar13;
  code *pcVar14;
  undefined8 uVar15;
  long *plVar16;
  undefined4 uVar17;
  undefined4 uVar18;
  long *local_3e0;
  undefined1 *puStack_3d8;
  undefined1 *local_3d0;
  undefined1 *puStack_3c8;
  undefined1 *local_3c0;
  undefined1 *local_3b8;
  undefined1 *puStack_3b0;
  undefined1 *local_3a8;
  undefined1 auStack_3a0 [112];
  undefined1 auStack_330 [32];
  long local_310;
  long *local_308;
  long *local_300;
  undefined1 *local_2f8;
  undefined1 *local_2f0;
  undefined1 *puStack_2e8;
  undefined1 *local_2e0;
  undefined1 *local_2d0;
  undefined1 *puStack_2c8;
  undefined1 *local_2c0;
  undefined8 local_2b8;
  undefined8 uStack_2b0;
  undefined7 local_2a8;
  char cStack_2a1;
  undefined8 local_2a0;
  undefined8 uStack_298;
  ulong local_290;
  undefined8 local_288;
  undefined8 uStack_280;
  undefined8 local_278;
  undefined8 local_270;
  undefined1 *local_260;
  long *local_258;
  undefined1 *local_250;
  long *local_248;
  undefined8 local_240;
  long *plStack_238;
  undefined8 uStack_230;
  undefined8 uStack_228;
  long *local_220;
  long *local_218;
  undefined1 *puStack_210;
  undefined1 *local_208;
  undefined1 auStack_200 [112];
  undefined1 *local_190;
  long *local_188;
  undefined1 *local_180;
  long *local_178;
  undefined8 *local_170;
  long *plStack_168;
  undefined1 *local_160;
  undefined1 *local_158;
  long *plStack_150;
  long *plStack_148;
  undefined1 *local_140;
  undefined1 *puStack_138;
  undefined1 *local_130;
  undefined8 uStack_128;
  undefined8 uStack_120;
  undefined8 uStack_118;
  undefined8 local_110;
  undefined8 uStack_108;
  undefined8 uStack_100;
  undefined8 uStack_f8;
  undefined8 local_b8;
  long alStack_a8 [3];
  long *local_90;
  undefined **local_88;
  undefined1 *puStack_80;
  long *local_78;
  undefined ***local_70;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  puStack_2c8 = &SUB_aaaaaaaaaaaaaaaa;
  local_2c0 = &SUB_aaaaaaaaaaaaaaaa;
  local_2d0 = &SUB_aaaaaaaaaaaaaaaa;
  if (*(char *)(param_3 + 0x1f) < '\0') {
    FUN_00018d20(&local_2d0,*(undefined8 *)(param_3 + 8),*(undefined8 *)(param_3 + 0x10));
  }
  else {
    puStack_2c8 = *(undefined1 **)(param_3 + 0x10);
    local_2d0 = *(undefined1 **)(param_3 + 8);
    local_2c0 = *(undefined1 **)(param_3 + 0x18);
  }
  puStack_2e8 = &SUB_aaaaaaaaaaaaaaaa;
  local_2e0 = &SUB_aaaaaaaaaaaaaaaa;
  local_2f0 = &SUB_aaaaaaaaaaaaaaaa;
  if (*(char *)(param_3 + 0x3f) < '\0') {
    FUN_00018d20(&local_2f0,*(undefined8 *)(param_3 + 0x28),*(undefined8 *)(param_3 + 0x30));
  }
  else {
    puStack_2e8 = *(undefined1 **)(param_3 + 0x30);
    local_2f0 = *(undefined1 **)(param_3 + 0x28);
    local_2e0 = *(undefined1 **)(param_3 + 0x38);
  }
  puVar1 = puStack_2c8;
  if (-1 < (long)local_2c0) {
    puVar1 = (undefined1 *)((ulong)local_2c0 >> 0x38);
  }
  if (puVar1 != (undefined1 *)0x0) {
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (param_2 + 0x168,&local_2d0);
  }
  local_240 = (undefined8 *)0x0;
  plStack_238 = (undefined8 *)0x0;
  uStack_230 = (undefined1 *)0x0;
  uVar7 = FUN_04a7a3e0(param_2 + 0x168,&local_240);
  if (local_240 != (undefined8 *)0x0) {
    for (; plStack_238 != local_240; plStack_238 = plStack_238 + -3) {
    }
    plStack_238 = local_240;
    __ZdlPvm(local_240,(long)uStack_230 - (long)local_240);
  }
  if ((uVar7 & 1) == 0) {
    iVar6 = thunk_FUN_05e1d97c(3);
    if (iVar6 != 0) {
      FUN_0488143c(&local_3e0);
      pplVar2 = (long **)local_3e0;
      if (-1 < (long)local_3d0) {
        pplVar2 = &local_3e0;
      }
      if ((DAT_0a3d2361 & 1) == 0) {
        uRam000000000a3d2358._0_1_ = s_login_manager_ccauto_login_close_0889c040[8];
        uRam000000000a3d2358._1_1_ = s_login_manager_ccauto_login_close_0889c040[9];
        uRam000000000a3d2358._2_1_ = s_login_manager_ccauto_login_close_0889c040[10];
        uRam000000000a3d2358._3_1_ = s_login_manager_ccauto_login_close_0889c040[0xb];
        uRam000000000a3d2358._4_1_ = s_login_manager_ccauto_login_close_0889c040[0xc];
        uRam000000000a3d2358._5_1_ = s_login_manager_ccauto_login_close_0889c040[0xd];
        uRam000000000a3d2358._6_1_ = s_login_manager_ccauto_login_close_0889c040[0xe];
        uRam000000000a3d2358._7_1_ = s_login_manager_ccauto_login_close_0889c040[0xf];
        DAT_0a3d2350 = s_login_manager_ccauto_login_close_0889c040[0];
        DAT_0a3d2350_1._0_1_ = s_login_manager_ccauto_login_close_0889c040[1];
        DAT_0a3d2350_1._1_1_ = s_login_manager_ccauto_login_close_0889c040[2];
        DAT_0a3d2350_1._2_1_ = s_login_manager_ccauto_login_close_0889c040[3];
        DAT_0a3d2350_1._3_1_ = s_login_manager_ccauto_login_close_0889c040[4];
        DAT_0a3d2350_1._4_1_ = s_login_manager_ccauto_login_close_0889c040[5];
        DAT_0a3d2350_1._5_1_ = s_login_manager_ccauto_login_close_0889c040[6];
        DAT_0a3d2350_1._6_1_ = s_login_manager_ccauto_login_close_0889c040[7];
        DAT_0a3d2360 = 0;
        DAT_0a3d2361 = 1;
      }
      if ((DAT_0a3d243e & 1) == 0) {
        DAT_0a3d2430._0_1_ = s_CriticalSeri_0848ba50[0];
        DAT_0a3d2430._1_1_ = s_CriticalSeri_0848ba50[1];
        DAT_0a3d2430._2_1_ = s_CriticalSeri_0848ba50[2];
        DAT_0a3d2430._3_1_ = s_CriticalSeri_0848ba50[3];
        DAT_0a3d2430._4_1_ = s_CriticalSeri_0848ba50[4];
        DAT_0a3d2430._5_1_ = s_CriticalSeri_0848ba50[5];
        DAT_0a3d2430._6_1_ = s_CriticalSeri_0848ba50[6];
        DAT_0a3d2430._7_1_ = s_CriticalSeri_0848ba50[7];
        DAT_0a3d2438 = (undefined4)DAT_085aff28;
        DAT_0a3d243c = 0x6e;
        DAT_0a3d243e = 1;
      }
      FUN_05e1d050(&local_240,3,pplVar2,&DAT_0a3d2350,&DAT_0a3d2430,0xd5,0,0);
      if ((DAT_0a3d247d & 1) == 0) {
        uVar7 = 0;
        do {
          uVar17 = *(undefined4 *)((long)&DAT_0889d2f9 + uVar7);
          uVar3 = CONCAT12((char)((uint)uVar17 >> 8),(short)uVar17) & 0xff00ff;
          uVar18 = *(undefined4 *)((long)&DAT_0889d2e5 + uVar7 % 0x14);
          *(uint *)((long)&DAT_0a3d243f + uVar7) =
               CONCAT13((char)((uint)uVar17 >> 0x18) + 0x8aU ^ (byte)((uint)uVar18 >> 0x18),
                        CONCAT12((char)((uint)uVar17 >> 0x10) + 0x8aU ^ (byte)((uint)uVar18 >> 0x10)
                                 ,CONCAT11((char)(uVar3 >> 0x10) + 0x8aU ^ (byte)((uint)uVar18 >> 8)
                                           ,(char)uVar3 + 0x8aU ^ (byte)uVar18)));
          uVar7 = uVar7 + 4;
        } while (uVar7 != 0x3c);
        DAT_0a3d247b = 0x2e;
        DAT_0a3d247d = 1;
      }
      uStack_108 = 0;
      local_110 = 0;
      uStack_f8 = 0;
      uStack_100 = 0;
      uStack_128 = 0;
      local_130 = (undefined1 *)0x0;
      uStack_118 = 0;
      uStack_120 = 0;
      plStack_148 = (long *)0x0;
      plStack_150 = (long *)0x0;
      puStack_138 = (undefined1 *)0x0;
      local_140 = (undefined1 *)0x0;
      plStack_168 = (long *)0x0;
      local_170 = (undefined8 *)0x0;
      local_158 = (undefined1 *)0x0;
      local_160 = (undefined1 *)0x0;
      FUN_05e1d31c(&local_240,&DAT_0a3d243f,&local_170);
      thunk_FUN_05e1d0bc(&local_240);
      if ((long)local_3d0 < 0) {
        __ZdlPvm(local_3e0,(ulong)local_3d0 & 0x7fffffffffffffff);
      }
    }
    local_170 = DAT_0889c240;
    local_160 = (undefined1 *)0x0;
    plStack_168 = (long *)0x0;
    plStack_150 = (long *)0x0;
    local_158 = (undefined1 *)0x0;
    plStack_148 = (long *)0x0;
    plVar13 = (long *)__Znwm(0x270);
    plVar13[2] = 0;
    plVar13[1] = 0;
    *plVar13 = (long)&PTR_FUN_09de0f80;
    _bzero(plVar13 + 3,0x228);
    *(undefined4 *)(plVar13 + 3) = 1;
    plVar13[0x40] = 0;
    plVar13[0x42] = 0;
    plVar13[0x41] = 0;
    *(undefined1 *)(plVar13 + 0x43) = 0;
    plVar13[0x11] = 0;
    plVar13[0x10] = 0;
    plVar13[0x13] = 0;
    plVar13[0x12] = 0;
    plVar13[0x15] = 0;
    plVar13[0x14] = 0;
    plVar13[0x17] = 0;
    plVar13[0x16] = 0;
    plVar13[0x19] = 0;
    plVar13[0x18] = 0;
    plVar13[0x1b] = 0;
    plVar13[0x1a] = 0;
    plVar13[0x1d] = 0;
    plVar13[0x1c] = 0;
    plVar13[0x1f] = 0;
    plVar13[0x1e] = 0;
    plVar13[0x21] = 0;
    plVar13[0x20] = 0;
    plVar13[0x23] = 0;
    plVar13[0x22] = 0;
    plVar13[0x25] = 0;
    plVar13[0x24] = 0;
    plVar13[0x27] = 0;
    plVar13[0x26] = 0;
    plVar13[0x29] = 0;
    plVar13[0x28] = 0;
    plVar13[0x2b] = 0;
    plVar13[0x2a] = 0;
    plVar13[0x2d] = 0;
    plVar13[0x2c] = 0;
    plVar13[0x2f] = 0;
    plVar13[0x2e] = 0;
    plVar13[0x31] = 0;
    plVar13[0x30] = 0;
    plVar13[0x33] = 0;
    plVar13[0x32] = 0;
    plVar13[0x35] = 0;
    plVar13[0x34] = 0;
    plVar13[0x37] = 0;
    plVar13[0x36] = 0;
    plVar13[0x39] = 0;
    plVar13[0x38] = 0;
    plVar13[0x3b] = 0;
    plVar13[0x3a] = 0;
    plVar13[0x3d] = 0;
    plVar13[0x3c] = 0;
    *(undefined8 *)((long)plVar13 + 0x1f1) = 0;
    *(undefined8 *)((long)plVar13 + 0x1e9) = 0;
    *(undefined2 *)(plVar13 + 0x47) = 0;
    plVar13[0x46] = 0;
    plVar13[0x45] = 0;
    plVar13[0x44] = 0;
    plVar13[0x49] = 0;
    plVar13[0x48] = 0;
    plVar13[0x4b] = 0;
    plVar13[0x4a] = 0;
    plVar13[0x4d] = 0;
    plVar13[0x4c] = 0;
    plStack_150 = plVar13 + 3;
    plStack_148 = plVar13;
    pcVar10 = (char *)FUN_04e04488();
    puVar11 = (undefined8 *)_strlen(pcVar10);
    if ((undefined8 *)0x7ffffffffffffff7 < puVar11) {
                    /* WARNING: Subroutine does not return */
      FUN_00018d9c(&local_240);
    }
    if ((undefined8 *)((long)&MACH_HEADER.sizeofcmds + 2) < puVar11) {
      uVar7 = 0x19;
      if (((ulong)puVar11 | 7) != 0x17) {
        uVar7 = ((ulong)puVar11 | 7) + 1;
      }
      puVar12 = (undefined8 *)__Znwm(uVar7);
      uStack_230 = (undefined1 *)(uVar7 | 0x8000000000000000);
      local_240 = puVar12;
      plStack_238 = puVar11;
LAB_02fc3e6c:
      _memmove(puVar12,pcVar10,(size_t)puVar11);
    }
    else {
      uStack_230 = (undefined1 *)CONCAT17((char)puVar11,(undefined7)uStack_230);
      puVar12 = &local_240;
      if (puVar11 != (undefined8 *)0x0) goto LAB_02fc3e6c;
    }
    *(undefined1 *)((long)puVar12 + (long)puVar11) = 0;
    uStack_228 = (undefined1 *)((ulong)uStack_228._4_4_ << 0x20);
    local_218 = (long *)0x0;
    puStack_210 = (undefined1 *)0x0;
    local_220 = (long *)0x0;
    FUN_0002b2c0(&local_208);
    FUN_02fc4f04(plStack_150 + 2,&local_240);
    FUN_0002b440(&local_208);
    if ((long)puStack_210 < 0) {
      __ZdlPvm(local_220,(ulong)puStack_210 & 0x7fffffffffffffff);
    }
    if ((long)uStack_230 < 0) {
      __ZdlPvm(local_240,(ulong)uStack_230 & 0x7fffffffffffffff);
    }
    local_240 = (long *)((ulong)local_240 & 0xffffff0000000000);
    plStack_238 = (long *)((ulong)plStack_238 & 0xffffffffffffff00);
    local_208 = (undefined1 *)((ulong)local_208 & 0xffffffffffffff00);
    *param_1 = (ulong)local_170;
    if ((long)local_158 < 0) {
      FUN_00018d20(param_1 + 1,plStack_168,local_160);
    }
    else {
      param_1[2] = (ulong)local_160;
      param_1[1] = (ulong)plStack_168;
      param_1[3] = (ulong)local_158;
    }
    param_1[4] = (ulong)plStack_150;
    param_1[5] = (ulong)plStack_148;
    if (plStack_148 != (long *)0x0) {
      plStack_148[1] = plStack_148[1] + 1;
    }
    *(undefined1 *)(param_1 + 7) = 0;
    *(undefined4 *)(param_1 + 6) = (undefined4)local_240;
    *(undefined1 *)((long)param_1 + 0x34) = local_240._4_1_;
    *(undefined1 *)(param_1 + 0xd) = 0;
    if ((char)local_208 == '\x01') {
      *(undefined4 *)(param_1 + 7) = plStack_238._0_4_;
      FUN_02fea310(param_1 + 8,&uStack_230);
      *(undefined1 *)(param_1 + 0xd) = 1;
      uVar7 = (ulong)uStack_230;
      plVar13 = local_220;
      if (((ulong)local_208 & 1) != 0) {
joined_r0x02fc3fa8:
        while (plVar13 != (long *)0x0) {
          plVar9 = (long *)*plVar13;
          uStack_230 = (undefined1 *)uVar7;
          __ZdlPvm(plVar13,0x18);
          uVar7 = (ulong)uStack_230;
          plVar13 = plVar9;
        }
        uStack_230 = (undefined1 *)0x0;
        if (uVar7 != 0) {
          __ZdlPvm(uVar7,(long)uStack_228 << 3);
        }
      }
    }
    else {
      uVar7 = (ulong)uStack_230;
      plVar13 = local_220;
      if ((char)local_208 != '\0') goto joined_r0x02fc3fa8;
    }
    plVar9 = plStack_148;
    plVar13 = plStack_168;
    puVar1 = local_158;
    if (plStack_148 != (long *)0x0) {
      LOAcquire();
      lVar8 = plStack_148[1];
      plStack_148[1] = lVar8 + -1;
      LORelease();
      if (lVar8 == 0) {
        (**(code **)(*plStack_148 + 0x10))(plStack_148);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar9);
        plVar13 = plStack_168;
        puVar1 = local_158;
      }
    }
  }
  else {
    FUN_02fc5058(param_2,1);
    lVar8 = FUN_04669774();
    if ((*(byte *)(lVar8 + 0xc0) & 1) == 0) {
      lVar8 = FUN_04669774();
      if (2 < *(int *)(lVar8 + 0x2b0) - 2U) {
        iVar6 = thunk_FUN_05e1d97c(2);
        if (iVar6 != 0) {
          FUN_0488143c(&local_3e0);
          pplVar2 = (long **)local_3e0;
          if (-1 < (long)local_3d0) {
            pplVar2 = &local_3e0;
          }
          if ((DAT_0a3d2361 & 1) == 0) {
            uRam000000000a3d2358._0_1_ = s_login_manager_ccauto_login_close_0889c040[8];
            uRam000000000a3d2358._1_1_ = s_login_manager_ccauto_login_close_0889c040[9];
            uRam000000000a3d2358._2_1_ = s_login_manager_ccauto_login_close_0889c040[10];
            uRam000000000a3d2358._3_1_ = s_login_manager_ccauto_login_close_0889c040[0xb];
            uRam000000000a3d2358._4_1_ = s_login_manager_ccauto_login_close_0889c040[0xc];
            uRam000000000a3d2358._5_1_ = s_login_manager_ccauto_login_close_0889c040[0xd];
            uRam000000000a3d2358._6_1_ = s_login_manager_ccauto_login_close_0889c040[0xe];
            uRam000000000a3d2358._7_1_ = s_login_manager_ccauto_login_close_0889c040[0xf];
            DAT_0a3d2350 = s_login_manager_ccauto_login_close_0889c040[0];
            DAT_0a3d2350_1._0_1_ = s_login_manager_ccauto_login_close_0889c040[1];
            DAT_0a3d2350_1._1_1_ = s_login_manager_ccauto_login_close_0889c040[2];
            DAT_0a3d2350_1._2_1_ = s_login_manager_ccauto_login_close_0889c040[3];
            DAT_0a3d2350_1._3_1_ = s_login_manager_ccauto_login_close_0889c040[4];
            DAT_0a3d2350_1._4_1_ = s_login_manager_ccauto_login_close_0889c040[5];
            DAT_0a3d2350_1._5_1_ = s_login_manager_ccauto_login_close_0889c040[6];
            DAT_0a3d2350_1._6_1_ = s_login_manager_ccauto_login_close_0889c040[7];
            DAT_0a3d2360 = 0;
            DAT_0a3d2361 = 1;
          }
          if ((DAT_0a3d243e & 1) == 0) {
            DAT_0a3d2430._0_1_ = s_CriticalSeri_0848ba50[0];
            DAT_0a3d2430._1_1_ = s_CriticalSeri_0848ba50[1];
            DAT_0a3d2430._2_1_ = s_CriticalSeri_0848ba50[2];
            DAT_0a3d2430._3_1_ = s_CriticalSeri_0848ba50[3];
            DAT_0a3d2430._4_1_ = s_CriticalSeri_0848ba50[4];
            DAT_0a3d2430._5_1_ = s_CriticalSeri_0848ba50[5];
            DAT_0a3d2430._6_1_ = s_CriticalSeri_0848ba50[6];
            DAT_0a3d2430._7_1_ = s_CriticalSeri_0848ba50[7];
            DAT_0a3d2438 = (undefined4)DAT_085aff28;
            DAT_0a3d243c = 0x6e;
            DAT_0a3d243e = 1;
          }
          FUN_05e1d050(&local_240,2,pplVar2,&DAT_0a3d2350,&DAT_0a3d2430,0xf0,0,0);
          if ((DAT_0a3d24e4 & 1) == 0) {
            _DAT_0a3d24c4 = CONCAT44((int)DAT_084d8630,(int)DAT_0889c248);
            uRam000000000a3d24cc = CONCAT44((int)DAT_084c7768,(int)DAT_0889c250);
            _DAT_0a3d24d4 = CONCAT44((int)DAT_08801070,(int)DAT_0889c258);
            uRam000000000a3d24dc = CONCAT44((int)DAT_0889c260,(int)DAT_086e7950);
            DAT_0a3d24e4 = 1;
          }
          uStack_108 = 0;
          local_110 = 0;
          uStack_f8 = 0;
          uStack_100 = 0;
          uStack_128 = 0;
          local_130 = (undefined1 *)0x0;
          uStack_118 = 0;
          uStack_120 = 0;
          plStack_148 = (long *)0x0;
          plStack_150 = (long *)0x0;
          puStack_138 = (undefined1 *)0x0;
          local_140 = (undefined1 *)0x0;
          plStack_168 = (long *)0x0;
          local_170 = (undefined8 *)0x0;
          local_158 = (undefined1 *)0x0;
          local_160 = (undefined1 *)0x0;
          FUN_05e1d31c(&local_240,&DAT_0a3d24c4,&local_170);
          thunk_FUN_05e1d0bc(&local_240);
          if ((long)local_3d0 < 0) {
            __ZdlPvm(local_3e0,(ulong)local_3d0 & 0x7fffffffffffffff);
          }
        }
        if ((*(byte *)(param_2 + 0x120) & 1) == 0) {
          local_300 = (long *)&SUB_aaaaaaaaaaaaaaaa;
          local_2f8 = &SUB_aaaaaaaaaaaaaaaa;
          FUN_02fc5ae4(&local_300,param_2);
          FUN_04669774();
          FUN_0466ad74(&local_310);
          if ((DAT_0a3d243e & 1) == 0) {
            DAT_0a3d2430._0_1_ = s_CriticalSeri_0848ba50[0];
            DAT_0a3d2430._1_1_ = s_CriticalSeri_0848ba50[1];
            DAT_0a3d2430._2_1_ = s_CriticalSeri_0848ba50[2];
            DAT_0a3d2430._3_1_ = s_CriticalSeri_0848ba50[3];
            DAT_0a3d2430._4_1_ = s_CriticalSeri_0848ba50[4];
            DAT_0a3d2430._5_1_ = s_CriticalSeri_0848ba50[5];
            DAT_0a3d2430._6_1_ = s_CriticalSeri_0848ba50[6];
            DAT_0a3d2430._7_1_ = s_CriticalSeri_0848ba50[7];
            DAT_0a3d2438 = (undefined4)DAT_085aff28;
            DAT_0a3d243c = 0x6e;
            DAT_0a3d243e = 1;
          }
          if ((DAT_0a3d2546 & 1) == 0) {
            uVar7 = 0;
            do {
              uVar17 = *(undefined4 *)((long)&DAT_0889d3e6 + uVar7);
              uVar3 = CONCAT12((char)((uint)uVar17 >> 8),(short)uVar17) & 0xff00ff;
              uVar18 = *(undefined4 *)((long)&DAT_0889d3d2 + uVar7 % 0x14);
              *(uint *)((long)&DAT_0a3d24e5 + uVar7) =
                   CONCAT13((char)((uint)uVar17 >> 0x18) + 0x8aU ^ (byte)((uint)uVar18 >> 0x18),
                            CONCAT12((char)((uint)uVar17 >> 0x10) + 0x8aU ^
                                     (byte)((uint)uVar18 >> 0x10),
                                     CONCAT11((char)(uVar3 >> 0x10) + 0x8aU ^
                                              (byte)((uint)uVar18 >> 8),
                                              (char)uVar3 + 0x8aU ^ (byte)uVar18)));
              uVar7 = uVar7 + 4;
            } while (uVar7 != 0x60);
            DAT_0a3d2545 = 0;
            DAT_0a3d2546 = 1;
          }
          FUN_0003bb6c(auStack_330,&DAT_0a3d2430,&DAT_0a3d24e5,0xf3);
          local_3e0 = local_300;
          puStack_3d8 = local_2f8;
          if (local_2f8 != (undefined1 *)0x0) {
            *(long *)(local_2f8 + 0x10) = *(long *)(local_2f8 + 0x10) + 1;
          }
          if ((long)local_2c0 < 0) {
            FUN_00018d20(&local_3d0,local_2d0,puStack_2c8);
          }
          else {
            puStack_3c8 = puStack_2c8;
            local_3d0 = local_2d0;
            local_3c0 = local_2c0;
          }
          if ((long)local_2e0 < 0) {
            FUN_00018d20(&local_3b8,local_2f0,puStack_2e8);
          }
          else {
            puStack_3b0 = puStack_2e8;
            local_3b8 = local_2f0;
            local_3a8 = local_2e0;
          }
          FUN_02fec014(auStack_3a0,param_3);
          uVar15 = *(undefined8 *)(local_310 + 8);
          FUN_0453d700(&local_2b8,auStack_330);
          if (cStack_2a1 < '\0') {
            FUN_00018d20(&local_2a0,local_2b8,uStack_2b0);
          }
          else {
            uStack_298 = uStack_2b0;
            local_2a0 = local_2b8;
            local_290 = CONCAT17(cStack_2a1,local_2a8);
          }
          local_278 = 0;
          uStack_280 = 0;
          local_288 = 0;
          local_270 = 0x80000000ffffffff;
          local_170 = &local_2a0;
          local_160 = puStack_3d8;
          plStack_168 = local_3e0;
          local_3e0 = (long *)0x0;
          puStack_3d8 = (undefined1 *)0x0;
          plStack_150 = (long *)puStack_3c8;
          local_158 = local_3d0;
          plStack_148 = (long *)local_3c0;
          local_3d0 = (undefined1 *)0x0;
          puStack_3c8 = (undefined1 *)0x0;
          local_3c0 = (undefined1 *)0x0;
          puStack_138 = puStack_3b0;
          local_140 = local_3b8;
          local_130 = local_3a8;
          puStack_3b0 = (undefined1 *)0x0;
          local_3a8 = (undefined1 *)0x0;
          local_3b8 = (undefined1 *)0x0;
          FUN_02fec014(&uStack_128,auStack_3a0);
          local_250 = &SUB_aaaaaaaaaaaaaaaa;
          local_248 = (long *)&SUB_aaaaaaaaaaaaaaaa;
          local_b8 = uVar15;
          FUN_021efaf0(&local_250,&local_240);
          uVar15 = local_b8;
          plStack_238 = (long *)local_160;
          local_240 = plStack_168;
          puVar11 = local_170;
          local_188 = local_248;
          local_190 = local_250;
          local_260 = local_250;
          local_258 = local_248;
          if (local_248 != (long *)0x0) {
            local_248[1] = local_248[1] + 1;
          }
          local_178 = (long *)&SUB_aaaaaaaaaaaaaaaa;
          local_180 = &SUB_aaaaaaaaaaaaaaaa;
          plStack_168 = (long *)0x0;
          local_160 = (undefined1 *)0x0;
          uStack_228 = (undefined1 *)plStack_150;
          uStack_230 = local_158;
          local_158 = (undefined1 *)0x0;
          plStack_150 = (long *)0x0;
          local_220 = plStack_148;
          local_208 = local_130;
          puStack_210 = puStack_138;
          local_218 = (long *)local_140;
          plStack_148 = (long *)0x0;
          local_140 = (undefined1 *)0x0;
          puStack_138 = (undefined1 *)0x0;
          local_130 = (undefined1 *)0x0;
          FUN_02fec014(auStack_200,&uStack_128);
          if (local_188 != (long *)0x0) {
            local_188[1] = local_188[1] + 1;
          }
          local_90 = (long *)0x0;
          plVar13 = (long *)__Znwm(200);
          *plVar13 = (long)&PTR_FUN_09de0b00;
          plVar13[2] = (long)plStack_238;
          plVar13[1] = (long)local_240;
          local_240 = (long *)0x0;
          plStack_238 = (long *)0x0;
          plVar13[4] = (long)uStack_228;
          plVar13[3] = (long)uStack_230;
          plVar13[5] = (long)local_220;
          uStack_230 = (undefined1 *)0x0;
          uStack_228 = (undefined1 *)0x0;
          plVar13[7] = (long)puStack_210;
          plVar13[6] = (long)local_218;
          plVar13[8] = (long)local_208;
          local_220 = (long *)0x0;
          local_218 = (long *)0x0;
          puStack_210 = (undefined1 *)0x0;
          local_208 = (undefined1 *)0x0;
          FUN_02fec014(plVar13 + 9,auStack_200);
          plVar13[0x17] = (long)local_190;
          plVar13[0x18] = (long)local_188;
          if (local_188 != (long *)0x0) {
            local_188[1] = local_188[1] + 1;
          }
          local_90 = plVar13;
          FUN_06684b8c(&local_180,uVar15,puVar11,alStack_a8);
          if (local_90 == alStack_a8) {
            pcVar14 = *(code **)(*local_90 + 0x20);
LAB_02fc45c4:
            (*pcVar14)();
          }
          else if (local_90 != (long *)0x0) {
            pcVar14 = *(code **)(*local_90 + 0x28);
            goto LAB_02fc45c4;
          }
          plVar13 = local_188;
          if (local_188 != (long *)0x0) {
            LOAcquire();
            lVar8 = local_188[1];
            local_188[1] = lVar8 + -1;
            LORelease();
            if (lVar8 == 0) {
              (**(code **)(*local_188 + 0x10))(local_188);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
            }
          }
          FUN_02fc5bc4(&local_240);
          plVar13 = local_178;
          if (local_178 != (long *)0x0) {
            plVar9 = local_178 + 2;
            *plVar9 = *plVar9 + 1;
            *plVar9 = *plVar9 + 1;
          }
          local_88 = &PTR_FUN_09de0c00;
          puStack_80 = local_180;
          local_78 = local_178;
          local_70 = &local_88;
          FUN_06668c44(local_260,&local_88);
          if (local_70 == &local_88) {
            pcVar14 = (code *)(*local_70)[4];
LAB_02fc4660:
            (*pcVar14)();
          }
          else if (local_70 != (undefined ***)0x0) {
            pcVar14 = (code *)(*local_70)[5];
            goto LAB_02fc4660;
          }
          if (plVar13 != (long *)0x0) {
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
          }
          plVar13 = local_178;
          if (local_178 != (long *)0x0) {
            LOAcquire();
            lVar8 = local_178[1];
            local_178[1] = lVar8 + -1;
            LORelease();
            if (lVar8 == 0) {
              (**(code **)(*local_178 + 0x10))(local_178);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
            }
          }
          plVar13 = local_258;
          if (local_258 != (long *)0x0) {
            LOAcquire();
            lVar8 = local_258[1];
            local_258[1] = lVar8 + -1;
            LORelease();
            if (lVar8 == 0) {
              (**(code **)(*local_258 + 0x10))(local_258);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
            }
          }
          plVar13 = local_248;
          puVar1 = local_250;
          if ((local_248 != (long *)0x0) &&
             (local_248[1] = local_248[1] + 1, local_248 != (long *)0x0)) {
            LOAcquire();
            lVar8 = local_248[1];
            local_248[1] = lVar8 + -1;
            LORelease();
            if (lVar8 == 0) {
              (**(code **)(*local_248 + 0x10))(local_248);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
            }
          }
          FUN_02fc5bc4(&plStack_168);
          if ((long)local_290 < 0) {
            __ZdlPvm(local_2a0,local_290 & 0x7fffffffffffffff);
          }
          if (cStack_2a1 < '\0') {
            __ZdlPvm(local_2b8,CONCAT17(cStack_2a1,local_2a8) & 0x7fffffffffffffff);
          }
          if (*(char *)(param_2 + 0x120) == '\x01') {
            if (plVar13 != (long *)0x0) {
              plVar13[1] = plVar13[1] + 1;
            }
            plVar9 = *(long **)(param_2 + 0x118);
            *(undefined1 **)(param_2 + 0x110) = puVar1;
            *(long **)(param_2 + 0x118) = plVar13;
            if (plVar9 != (long *)0x0) {
              LOAcquire();
              lVar8 = plVar9[1];
              plVar9[1] = lVar8 + -1;
              LORelease();
              if (lVar8 == 0) {
                (**(code **)(*plVar9 + 0x10))(plVar9);
                __ZNSt3__119__shared_weak_count14__release_weakEv(plVar9);
              }
            }
          }
          else {
            *(undefined1 **)(param_2 + 0x110) = puVar1;
            *(long **)(param_2 + 0x118) = plVar13;
            if (plVar13 != (long *)0x0) {
              plVar13[1] = plVar13[1] + 1;
            }
            *(undefined1 *)(param_2 + 0x120) = 1;
          }
          if (plVar13 != (long *)0x0) {
            LOAcquire();
            lVar8 = plVar13[1];
            plVar13[1] = lVar8 + -1;
            LORelease();
            if (lVar8 == 0) {
              (**(code **)(*plVar13 + 0x10))(plVar13);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
            }
          }
          FUN_02fc5bc4(&local_3e0);
          if (local_308 != (long *)0x0) {
            LOAcquire();
            lVar8 = local_308[1];
            local_308[1] = lVar8 + -1;
            LORelease();
            if (lVar8 == 0) {
              (**(code **)(*local_308 + 0x10))(local_308);
              __ZNSt3__119__shared_weak_count14__release_weakEv(local_308);
            }
          }
          if (local_2f8 != (undefined1 *)0x0) {
            __ZNSt3__119__shared_weak_count14__release_weakEv();
          }
        }
        uVar5 = _UNK_0889ca80;
        uVar4 = _DAT_0889ca78;
        uVar7 = _DAT_0889ca68;
        param_1[9] = _UNK_0889ca70;
        param_1[8] = uVar7;
        param_1[0xb] = uVar5;
        param_1[10] = uVar4;
        uVar7 = _DAT_0889ca88;
        param_1[0xd] = _UNK_0889ca90;
        param_1[0xc] = uVar7;
        uVar5 = _UNK_0889ca40;
        uVar4 = _DAT_0889ca38;
        uVar7 = _DAT_0889ca28;
        param_1[1] = _UNK_0889ca30;
        *param_1 = uVar7;
        param_1[3] = uVar5;
        param_1[2] = uVar4;
        uVar5 = _UNK_0889ca60;
        uVar4 = _DAT_0889ca58;
        uVar7 = _DAT_0889ca48;
        param_1[5] = _UNK_0889ca50;
        param_1[4] = uVar7;
        param_1[7] = uVar5;
        param_1[6] = uVar4;
        local_240 = *(long **)(param_2 + 0x110);
        plStack_238 = *(long **)(param_2 + 0x118);
        lVar8 = 0;
        if (plStack_238 != (long *)0x0) {
          lVar8 = plStack_238[1];
          plStack_238[1] = lVar8 + 1;
        }
        uStack_230 = (undefined1 *)0x0;
        FUN_066856fc(lVar8,&local_240);
        uVar15 = FUN_02fec170(&local_240);
        plVar13 = plStack_238;
        if (plStack_238 != (long *)0x0) {
          LOAcquire();
          lVar8 = plStack_238[1];
          plStack_238[1] = lVar8 + -1;
          LORelease();
          if (lVar8 == 0) {
            (**(code **)(*plStack_238 + 0x10))(plStack_238);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
          }
        }
        FUN_02fec20c(param_1,uVar15);
        iVar6 = thunk_FUN_05e1d97c(2);
        if (iVar6 != 0) {
          FUN_0488143c(&local_3e0);
          pplVar2 = (long **)local_3e0;
          if (-1 < (long)local_3d0) {
            pplVar2 = &local_3e0;
          }
          if ((DAT_0a3d2361 & 1) == 0) {
            uRam000000000a3d2358._0_1_ = s_login_manager_ccauto_login_close_0889c040[8];
            uRam000000000a3d2358._1_1_ = s_login_manager_ccauto_login_close_0889c040[9];
            uRam000000000a3d2358._2_1_ = s_login_manager_ccauto_login_close_0889c040[10];
            uRam000000000a3d2358._3_1_ = s_login_manager_ccauto_login_close_0889c040[0xb];
            uRam000000000a3d2358._4_1_ = s_login_manager_ccauto_login_close_0889c040[0xc];
            uRam000000000a3d2358._5_1_ = s_login_manager_ccauto_login_close_0889c040[0xd];
            uRam000000000a3d2358._6_1_ = s_login_manager_ccauto_login_close_0889c040[0xe];
            uRam000000000a3d2358._7_1_ = s_login_manager_ccauto_login_close_0889c040[0xf];
            DAT_0a3d2350 = s_login_manager_ccauto_login_close_0889c040[0];
            DAT_0a3d2350_1._0_1_ = s_login_manager_ccauto_login_close_0889c040[1];
            DAT_0a3d2350_1._1_1_ = s_login_manager_ccauto_login_close_0889c040[2];
            DAT_0a3d2350_1._2_1_ = s_login_manager_ccauto_login_close_0889c040[3];
            DAT_0a3d2350_1._3_1_ = s_login_manager_ccauto_login_close_0889c040[4];
            DAT_0a3d2350_1._4_1_ = s_login_manager_ccauto_login_close_0889c040[5];
            DAT_0a3d2350_1._5_1_ = s_login_manager_ccauto_login_close_0889c040[6];
            DAT_0a3d2350_1._6_1_ = s_login_manager_ccauto_login_close_0889c040[7];
            DAT_0a3d2360 = 0;
            DAT_0a3d2361 = 1;
          }
          if ((DAT_0a3d243e & 1) == 0) {
            DAT_0a3d2430._0_1_ = s_CriticalSeri_0848ba50[0];
            DAT_0a3d2430._1_1_ = s_CriticalSeri_0848ba50[1];
            DAT_0a3d2430._2_1_ = s_CriticalSeri_0848ba50[2];
            DAT_0a3d2430._3_1_ = s_CriticalSeri_0848ba50[3];
            DAT_0a3d2430._4_1_ = s_CriticalSeri_0848ba50[4];
            DAT_0a3d2430._5_1_ = s_CriticalSeri_0848ba50[5];
            DAT_0a3d2430._6_1_ = s_CriticalSeri_0848ba50[6];
            DAT_0a3d2430._7_1_ = s_CriticalSeri_0848ba50[7];
            DAT_0a3d2438 = (undefined4)DAT_085aff28;
            DAT_0a3d243c = 0x6e;
            DAT_0a3d243e = 1;
          }
          FUN_05e1d050(&local_240,2,pplVar2,&DAT_0a3d2350,&DAT_0a3d2430,0x13a,0,0);
          if ((DAT_0a3d2565 & 1) == 0) {
            _DAT_0a3d2548 = CONCAT44((int)DAT_084d8630,(int)DAT_0889c248);
            uRam000000000a3d2550 = CONCAT44((int)DAT_08801070,(int)DAT_0889c268);
            DAT_0a3d2558 = CONCAT44((int)DAT_086db4d0,(int)DAT_086e7950);
            DAT_0a3d2560 = (undefined4)DAT_0889c270;
            DAT_0a3d2564 = 0;
            DAT_0a3d2565 = 1;
          }
          uStack_108 = 0;
          local_110 = 0;
          uStack_f8 = 0;
          uStack_100 = 0;
          uStack_128 = 0;
          local_130 = (undefined1 *)0x0;
          uStack_118 = 0;
          uStack_120 = 0;
          plStack_148 = (long *)0x0;
          plStack_150 = (long *)0x0;
          puStack_138 = (undefined1 *)0x0;
          local_140 = (undefined1 *)0x0;
          plStack_168 = (long *)0x0;
          local_170 = (undefined8 *)0x0;
          local_158 = (undefined1 *)0x0;
          local_160 = (undefined1 *)0x0;
          FUN_05e1d31c(&local_240,&DAT_0a3d2548,&local_170);
          thunk_FUN_05e1d0bc(&local_240);
          if ((long)local_3d0 < 0) {
            __ZdlPvm(local_3e0,(ulong)local_3d0 & 0x7fffffffffffffff);
          }
        }
        if (*(char *)(param_2 + 0x120) == '\x01') {
          plVar13 = *(long **)(param_2 + 0x118);
          if (plVar13 != (long *)0x0) {
            LOAcquire();
            lVar8 = plVar13[1];
            plVar13[1] = lVar8 + -1;
            LORelease();
            if (lVar8 == 0) {
              (**(code **)(*plVar13 + 0x10))(plVar13);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar13);
            }
          }
          *(undefined1 *)(param_2 + 0x120) = 0;
        }
        goto LAB_02fc402c;
      }
      iVar6 = thunk_FUN_05e1d97c(4);
      if (iVar6 != 0) {
        FUN_0488143c(&local_3e0);
        pplVar2 = (long **)local_3e0;
        if (-1 < (long)local_3d0) {
          pplVar2 = &local_3e0;
        }
        if ((DAT_0a3d2361 & 1) == 0) {
          uRam000000000a3d2358._0_1_ = s_login_manager_ccauto_login_close_0889c040[8];
          uRam000000000a3d2358._1_1_ = s_login_manager_ccauto_login_close_0889c040[9];
          uRam000000000a3d2358._2_1_ = s_login_manager_ccauto_login_close_0889c040[10];
          uRam000000000a3d2358._3_1_ = s_login_manager_ccauto_login_close_0889c040[0xb];
          uRam000000000a3d2358._4_1_ = s_login_manager_ccauto_login_close_0889c040[0xc];
          uRam000000000a3d2358._5_1_ = s_login_manager_ccauto_login_close_0889c040[0xd];
          uRam000000000a3d2358._6_1_ = s_login_manager_ccauto_login_close_0889c040[0xe];
          uRam000000000a3d2358._7_1_ = s_login_manager_ccauto_login_close_0889c040[0xf];
          DAT_0a3d2350 = s_login_manager_ccauto_login_close_0889c040[0];
          DAT_0a3d2350_1._0_1_ = s_login_manager_ccauto_login_close_0889c040[1];
          DAT_0a3d2350_1._1_1_ = s_login_manager_ccauto_login_close_0889c040[2];
          DAT_0a3d2350_1._2_1_ = s_login_manager_ccauto_login_close_0889c040[3];
          DAT_0a3d2350_1._3_1_ = s_login_manager_ccauto_login_close_0889c040[4];
          DAT_0a3d2350_1._4_1_ = s_login_manager_ccauto_login_close_0889c040[5];
          DAT_0a3d2350_1._5_1_ = s_login_manager_ccauto_login_close_0889c040[6];
          DAT_0a3d2350_1._6_1_ = s_login_manager_ccauto_login_close_0889c040[7];
          DAT_0a3d2360 = 0;
          DAT_0a3d2361 = 1;
        }
        if ((DAT_0a3d243e & 1) == 0) {
          DAT_0a3d2430._0_1_ = s_CriticalSeri_0848ba50[0];
          DAT_0a3d2430._1_1_ = s_CriticalSeri_0848ba50[1];
          DAT_0a3d2430._2_1_ = s_CriticalSeri_0848ba50[2];
          DAT_0a3d2430._3_1_ = s_CriticalSeri_0848ba50[3];
          DAT_0a3d2430._4_1_ = s_CriticalSeri_0848ba50[4];
          DAT_0a3d2430._5_1_ = s_CriticalSeri_0848ba50[5];
          DAT_0a3d2430._6_1_ = s_CriticalSeri_0848ba50[6];
          DAT_0a3d2430._7_1_ = s_CriticalSeri_0848ba50[7];
          DAT_0a3d2438 = (undefined4)DAT_085aff28;
          DAT_0a3d243c = 0x6e;
          DAT_0a3d243e = 1;
        }
        FUN_05e1d050(&local_240,4,pplVar2,&DAT_0a3d2350,&DAT_0a3d2430,0xea,0,0);
        if ((DAT_0a3d24c3 & 1) == 0) {
          _DAT_0a3d24a8 = CONCAT44((int)DAT_084d8630,(int)DAT_0889c248);
          uRam000000000a3d24b0 = CONCAT44((int)DAT_0889c280,(int)DAT_0889c278);
          DAT_0a3d24b8 = CONCAT44((int)DAT_084d8298,(int)DAT_084ca3c8);
          DAT_0a3d24c0 = 0x6e69;
          DAT_0a3d24c2 = 0;
          DAT_0a3d24c3 = 1;
        }
        uStack_108 = 0;
        local_110 = 0;
        uStack_f8 = 0;
        uStack_100 = 0;
        uStack_128 = 0;
        local_130 = (undefined1 *)0x0;
        uStack_118 = 0;
        uStack_120 = 0;
        plStack_148 = (long *)0x0;
        plStack_150 = (long *)0x0;
        puStack_138 = (undefined1 *)0x0;
        local_140 = (undefined1 *)0x0;
        plStack_168 = (long *)0x0;
        local_170 = (undefined8 *)0x0;
        local_158 = (undefined1 *)0x0;
        local_160 = (undefined1 *)0x0;
        FUN_05e1d31c(&local_240,&DAT_0a3d24a8,&local_170);
        thunk_FUN_05e1d0bc(&local_240);
        if ((long)local_3d0 < 0) {
          __ZdlPvm(local_3e0,(ulong)local_3d0 & 0x7fffffffffffffff);
        }
      }
      local_240 = (long *)DAT_0889c288;
      uStack_230 = (undefined1 *)0x0;
      plStack_238 = (long *)0x0;
      local_220 = (long *)0x0;
      uStack_228 = (undefined1 *)0x0;
      local_218 = (long *)0x0;
      plVar9 = (long *)__Znwm(0x270);
    }
    else {
      iVar6 = thunk_FUN_05e1d97c(3);
      if (iVar6 != 0) {
        FUN_0488143c(&local_3e0);
        pplVar2 = (long **)local_3e0;
        if (-1 < (long)local_3d0) {
          pplVar2 = &local_3e0;
        }
        if ((DAT_0a3d2361 & 1) == 0) {
          uRam000000000a3d2358._0_1_ = s_login_manager_ccauto_login_close_0889c040[8];
          uRam000000000a3d2358._1_1_ = s_login_manager_ccauto_login_close_0889c040[9];
          uRam000000000a3d2358._2_1_ = s_login_manager_ccauto_login_close_0889c040[10];
          uRam000000000a3d2358._3_1_ = s_login_manager_ccauto_login_close_0889c040[0xb];
          uRam000000000a3d2358._4_1_ = s_login_manager_ccauto_login_close_0889c040[0xc];
          uRam000000000a3d2358._5_1_ = s_login_manager_ccauto_login_close_0889c040[0xd];
          uRam000000000a3d2358._6_1_ = s_login_manager_ccauto_login_close_0889c040[0xe];
          uRam000000000a3d2358._7_1_ = s_login_manager_ccauto_login_close_0889c040[0xf];
          DAT_0a3d2350 = s_login_manager_ccauto_login_close_0889c040[0];
          DAT_0a3d2350_1._0_1_ = s_login_manager_ccauto_login_close_0889c040[1];
          DAT_0a3d2350_1._1_1_ = s_login_manager_ccauto_login_close_0889c040[2];
          DAT_0a3d2350_1._2_1_ = s_login_manager_ccauto_login_close_0889c040[3];
          DAT_0a3d2350_1._3_1_ = s_login_manager_ccauto_login_close_0889c040[4];
          DAT_0a3d2350_1._4_1_ = s_login_manager_ccauto_login_close_0889c040[5];
          DAT_0a3d2350_1._5_1_ = s_login_manager_ccauto_login_close_0889c040[6];
          DAT_0a3d2350_1._6_1_ = s_login_manager_ccauto_login_close_0889c040[7];
          DAT_0a3d2360 = 0;
          DAT_0a3d2361 = 1;
        }
        if ((DAT_0a3d243e & 1) == 0) {
          DAT_0a3d2430._0_1_ = s_CriticalSeri_0848ba50[0];
          DAT_0a3d2430._1_1_ = s_CriticalSeri_0848ba50[1];
          DAT_0a3d2430._2_1_ = s_CriticalSeri_0848ba50[2];
          DAT_0a3d2430._3_1_ = s_CriticalSeri_0848ba50[3];
          DAT_0a3d2430._4_1_ = s_CriticalSeri_0848ba50[4];
          DAT_0a3d2430._5_1_ = s_CriticalSeri_0848ba50[5];
          DAT_0a3d2430._6_1_ = s_CriticalSeri_0848ba50[6];
          DAT_0a3d2430._7_1_ = s_CriticalSeri_0848ba50[7];
          DAT_0a3d2438 = (undefined4)DAT_085aff28;
          DAT_0a3d243c = 0x6e;
          DAT_0a3d243e = 1;
        }
        FUN_05e1d050(&local_240,3,pplVar2,&DAT_0a3d2350,&DAT_0a3d2430,0xe0,0,0);
        if ((DAT_0a3d24a4 & 1) == 0) {
          _DAT_0a3d2480 = CONCAT44((int)DAT_084d8630,(int)DAT_0889c248);
          uRam000000000a3d2488 = CONCAT44((int)DAT_08782818,(int)DAT_0889c290);
          _DAT_0a3d2490 = CONCAT44((int)DAT_0889c298,(int)DAT_084a24c8);
          uRam000000000a3d2498 = CONCAT44((int)DAT_0889c2a8,(int)DAT_0889c2a0);
          DAT_0a3d24a0 = (undefined4)DAT_084a2f38;
          DAT_0a3d24a4 = 1;
        }
        uStack_108 = 0;
        local_110 = 0;
        uStack_f8 = 0;
        uStack_100 = 0;
        uStack_128 = 0;
        local_130 = (undefined1 *)0x0;
        uStack_118 = 0;
        uStack_120 = 0;
        plStack_148 = (long *)0x0;
        plStack_150 = (long *)0x0;
        puStack_138 = (undefined1 *)0x0;
        local_140 = (undefined1 *)0x0;
        plStack_168 = (long *)0x0;
        local_170 = (undefined8 *)0x0;
        local_158 = (undefined1 *)0x0;
        local_160 = (undefined1 *)0x0;
        FUN_05e1d31c(&local_240,&DAT_0a3d2480,&local_170);
        thunk_FUN_05e1d0bc(&local_240);
        if ((long)local_3d0 < 0) {
          __ZdlPvm(local_3e0,(ulong)local_3d0 & 0x7fffffffffffffff);
        }
      }
      local_240 = (long *)DAT_0889c2b0;
      uStack_230 = (undefined1 *)0x0;
      plStack_238 = (long *)0x0;
      local_220 = (long *)0x0;
      uStack_228 = (undefined1 *)0x0;
      local_218 = (long *)0x0;
      plVar9 = (long *)__Znwm(0x270);
    }
    plVar16 = plVar9 + 1;
    plVar9[2] = 0;
    *plVar16 = 0;
    *plVar9 = (long)&PTR_FUN_09de0f80;
    plVar13 = plVar9 + 3;
    _bzero(plVar13,0x228);
    *(undefined4 *)(plVar9 + 3) = 1;
    plVar9[0x40] = 0;
    plVar9[0x42] = 0;
    plVar9[0x41] = 0;
    *(undefined1 *)(plVar9 + 0x43) = 0;
    plVar9[0x11] = 0;
    plVar9[0x10] = 0;
    plVar9[0x13] = 0;
    plVar9[0x12] = 0;
    plVar9[0x15] = 0;
    plVar9[0x14] = 0;
    plVar9[0x17] = 0;
    plVar9[0x16] = 0;
    plVar9[0x19] = 0;
    plVar9[0x18] = 0;
    plVar9[0x1b] = 0;
    plVar9[0x1a] = 0;
    plVar9[0x1d] = 0;
    plVar9[0x1c] = 0;
    plVar9[0x1f] = 0;
    plVar9[0x1e] = 0;
    plVar9[0x21] = 0;
    plVar9[0x20] = 0;
    plVar9[0x23] = 0;
    plVar9[0x22] = 0;
    plVar9[0x25] = 0;
    plVar9[0x24] = 0;
    plVar9[0x27] = 0;
    plVar9[0x26] = 0;
    plVar9[0x29] = 0;
    plVar9[0x28] = 0;
    plVar9[0x2b] = 0;
    plVar9[0x2a] = 0;
    plVar9[0x2d] = 0;
    plVar9[0x2c] = 0;
    plVar9[0x2f] = 0;
    plVar9[0x2e] = 0;
    plVar9[0x31] = 0;
    plVar9[0x30] = 0;
    plVar9[0x33] = 0;
    plVar9[0x32] = 0;
    plVar9[0x35] = 0;
    plVar9[0x34] = 0;
    plVar9[0x37] = 0;
    plVar9[0x36] = 0;
    plVar9[0x39] = 0;
    plVar9[0x38] = 0;
    plVar9[0x3b] = 0;
    plVar9[0x3a] = 0;
    plVar9[0x3d] = 0;
    plVar9[0x3c] = 0;
    *(undefined8 *)((long)plVar9 + 0x1f1) = 0;
    *(undefined8 *)((long)plVar9 + 0x1e9) = 0;
    *(undefined2 *)(plVar9 + 0x47) = 0;
    plVar9[0x46] = 0;
    plVar9[0x45] = 0;
    plVar9[0x44] = 0;
    plVar9[0x49] = 0;
    plVar9[0x48] = 0;
    plVar9[0x4b] = 0;
    plVar9[0x4a] = 0;
    plVar9[0x4d] = 0;
    plVar9[0x4c] = 0;
    *param_1 = (ulong)local_240;
    param_1[1] = 0;
    param_1[2] = 0;
    param_1[3] = 0;
    param_1[4] = (ulong)plVar13;
    param_1[5] = (ulong)plVar9;
    local_220 = plVar13;
    local_218 = plVar9;
    plVar13 = plStack_238;
    puVar1 = uStack_228;
    if (plVar9 == (long *)0x0) {
      *(undefined1 *)((long)param_1 + 0x34) = 0;
      *(undefined4 *)(param_1 + 6) = 0;
      *(undefined1 *)(param_1 + 7) = 0;
      *(undefined1 *)(param_1 + 0xd) = 0;
    }
    else {
      *plVar16 = *plVar16 + 1;
      *(undefined1 *)((long)param_1 + 0x34) = 0;
      *(undefined4 *)(param_1 + 6) = 0;
      *(undefined1 *)(param_1 + 7) = 0;
      *(undefined1 *)(param_1 + 0xd) = 0;
      LOAcquire();
      lVar8 = *plVar16;
      *plVar16 = lVar8 + -1;
      LORelease();
      if (lVar8 == 0) {
        (**(code **)(*plVar9 + 0x10))(plVar9);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar9);
        plVar13 = plStack_238;
        puVar1 = uStack_228;
      }
    }
  }
  if ((long)puVar1 < 0) {
    __ZdlPvm(plVar13,(ulong)puVar1 & 0x7fffffffffffffff);
  }
LAB_02fc402c:
  if ((long)local_2e0 < 0) {
    __ZdlPvm(local_2f0,(ulong)local_2e0 & 0x7fffffffffffffff);
  }
  if ((long)local_2c0 < 0) {
    __ZdlPvm(local_2d0,(ulong)local_2c0 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


