// Ghidra inferred pseudocode; requested=0x2eb5688
// entry=02eb5688 end=02eb5de3

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_02eb5688(long *param_1,undefined8 param_2,long *param_3)

{
  undefined8 *******pppppppuVar1;
  int iVar2;
  undefined8 *puVar3;
  long lVar4;
  ulong uVar5;
  long lVar6;
  long lVar7;
  long *plVar8;
  long local_1f8;
  long *local_1f0;
  long *local_1e8;
  long *local_1e0;
  undefined1 auStack_1d8 [8];
  undefined8 local_1d0;
  undefined7 local_1c0;
  char cStack_1b9;
  long *local_1b0;
  long *local_1a8;
  long *local_1a0;
  undefined1 *local_198;
  long *local_190;
  long *local_188;
  long *local_180;
  undefined8 *******local_178;
  long *local_170;
  undefined7 local_168;
  char cStack_161;
  long *local_160;
  long *local_158;
  long local_d0;
  long *plStack_c8;
  undefined8 uStack_c0;
  undefined8 uStack_b8;
  undefined8 local_b0;
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
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  if (*param_3 == 0) {
    iVar2 = thunk_FUN_05e1d97c(4);
    if (iVar2 != 0) {
      FUN_0488143c(&local_178);
      pppppppuVar1 = local_178;
      if (-1 < cStack_161) {
        pppppppuVar1 = &local_178;
      }
      if ((DAT_0a3c9f34 & 1) == 0) {
        uVar5 = 0;
        do {
          (&DAT_0a3c9f1b)[uVar5] = (&DAT_08886d88)[uVar5] + 0x8a ^ (&DAT_08886d78)[uVar5 & 0xf];
          uVar5 = uVar5 + 1;
        } while (uVar5 != 0x19);
        DAT_0a3c9f34 = 1;
      }
      if ((DAT_0a3ca1ab & 1) == 0) {
        uVar5 = 0;
        do {
          (&DAT_0a3ca18f)[uVar5] = (&DAT_08887106)[uVar5 & 0xf] ^ (&DAT_08887116)[uVar5];
          uVar5 = uVar5 + 1;
        } while (uVar5 != 0x1c);
        DAT_0a3ca1ab = 1;
      }
      FUN_05e1d050(&local_160,4,pppppppuVar1,&DAT_0a3c9f1b,&DAT_0a3ca18f,0x14f,0,0);
      if ((DAT_0a3ca1c2 & 1) == 0) {
        uRam000000000a3ca1b8._0_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0x68];
        uRam000000000a3ca1b8._1_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0x69];
        uRam000000000a3ca1b8._2_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0x6a];
        uRam000000000a3ca1b8._3_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0x6b];
        uRam000000000a3ca1b8._4_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0x6c];
        uRam000000000a3ca1b8._5_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0x6d];
        uRam000000000a3ca1b8._6_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0x6e];
        uRam000000000a3ca1b8._7_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0x6f];
        DAT_0a3ca1b0 = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0x60];
        DAT_0a3ca1b0_1._0_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0x61];
        DAT_0a3ca1b0_1._1_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0x62];
        DAT_0a3ca1b0_1._2_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[99];
        DAT_0a3ca1b0_1._3_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[100];
        DAT_0a3ca1b0_1._4_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0x65];
        DAT_0a3ca1b0_1._5_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0x66];
        DAT_0a3ca1b0_1._6_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0x67];
        DAT_0a3ca1c0 = 0x6c;
        DAT_0a3ca1c2 = 1;
      }
      uStack_68 = 0;
      local_70 = 0;
      uStack_58 = 0;
      uStack_60 = 0;
      uStack_88 = 0;
      local_90 = 0;
      uStack_78 = 0;
      uStack_80 = 0;
      uStack_a8 = 0;
      local_b0 = 0;
      uStack_98 = 0;
      uStack_a0 = 0;
      plStack_c8 = (long *)0x0;
      local_d0 = 0;
      uStack_b8 = 0;
      uStack_c0 = 0;
      FUN_05e1d31c(&local_160,&DAT_0a3ca1b0,&local_d0);
      thunk_FUN_05e1d0bc(&local_160);
      if (cStack_161 < '\0') {
        __ZdlPvm(local_178,CONCAT17(cStack_161,local_168) & 0x7fffffffffffffff);
      }
    }
    *param_1 = 0;
    param_1[1] = 0;
    goto LAB_02eb5d80;
  }
  local_188 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_180 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_023ca588(&local_188,&local_160);
  *(undefined8 *)((long)local_188 + 0xe4) = DAT_08798418;
  lVar7 = *param_3;
  puVar3 = (undefined8 *)__Znwm(0x1e8);
  puVar3[1] = 0;
  puVar3[2] = 0;
  *puVar3 = &PTR_FUN_09c92020;
  lVar7 = FUN_00f516bc(puVar3 + 3,lVar7);
  local_188[0xc6] = lVar7;
  plVar8 = (long *)local_188[199];
  local_188[199] = (long)puVar3;
  if (plVar8 != (long *)0x0) {
    LOAcquire();
    lVar7 = plVar8[1];
    plVar8[1] = lVar7 + -1;
    LORelease();
    if (lVar7 == 0) {
      (**(code **)(*plVar8 + 0x10))(plVar8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    }
  }
  local_198 = &SUB_aaaaaaaaaaaaaaaa;
  local_190 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0466aca8(&local_178);
  FUN_01205740(&local_d0,local_178);
  FUN_0268f370(&local_160,local_d0);
  local_1a8 = local_188;
  local_1a0 = local_180;
  if (local_180 != (long *)0x0) {
    local_180[1] = local_180[1] + 1;
  }
  FUN_0319a638(&local_198,local_160,&local_1a8);
  plVar8 = local_1a0;
  if (local_1a0 != (long *)0x0) {
    LOAcquire();
    lVar7 = local_1a0[1];
    local_1a0[1] = lVar7 + -1;
    LORelease();
    if (lVar7 == 0) {
      (**(code **)(*local_1a0 + 0x10))(local_1a0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    }
  }
  plVar8 = local_158;
  if (local_158 != (long *)0x0) {
    LOAcquire();
    lVar7 = local_158[1];
    local_158[1] = lVar7 + -1;
    LORelease();
    if (lVar7 == 0) {
      (**(code **)(*local_158 + 0x10))(local_158);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    }
  }
  plVar8 = plStack_c8;
  if (plStack_c8 == (long *)0x0) {
LAB_02eb5814:
    if (local_170 == (long *)0x0) goto LAB_02eb582c;
LAB_02eb581c:
    LOAcquire();
    lVar7 = local_170[1];
    local_170[1] = lVar7 + -1;
    LORelease();
    if (lVar7 != 0) goto LAB_02eb582c;
    (**(code **)(*local_170 + 0x10))(local_170);
    __ZNSt3__119__shared_weak_count14__release_weakEv(local_170);
    if (local_198 != (undefined1 *)0x0) goto LAB_02eb5834;
LAB_02eb5bb0:
    iVar2 = thunk_FUN_05e1d97c(4);
    if (iVar2 != 0) {
      FUN_0488143c(&local_178);
      pppppppuVar1 = local_178;
      if (-1 < cStack_161) {
        pppppppuVar1 = &local_178;
      }
      if ((DAT_0a3c9f34 & 1) == 0) {
        uVar5 = 0;
        do {
          (&DAT_0a3c9f1b)[uVar5] = (&DAT_08886d88)[uVar5] + 0x8a ^ (&DAT_08886d78)[uVar5 & 0xf];
          uVar5 = uVar5 + 1;
        } while (uVar5 != 0x19);
        DAT_0a3c9f34 = 1;
      }
      if ((DAT_0a3ca1ab & 1) == 0) {
        uVar5 = 0;
        do {
          (&DAT_0a3ca18f)[uVar5] = (&DAT_08887106)[uVar5 & 0xf] ^ (&DAT_08887116)[uVar5];
          uVar5 = uVar5 + 1;
        } while (uVar5 != 0x1c);
        DAT_0a3ca1ab = 1;
      }
      FUN_05e1d050(&local_160,4,pppppppuVar1,&DAT_0a3c9f1b,&DAT_0a3ca18f,0x162,0,0);
      if ((DAT_0a3ca1e2 & 1) == 0) {
        uRam000000000a3ca1d8 = _UNK_088868d8;
        _DAT_0a3ca1d0 = _DAT_088868d0;
        DAT_0a3ca1e0 = 100;
        DAT_0a3ca1e2 = 1;
      }
      uStack_68 = 0;
      local_70 = 0;
      uStack_58 = 0;
      uStack_60 = 0;
      uStack_88 = 0;
      local_90 = 0;
      uStack_78 = 0;
      uStack_80 = 0;
      uStack_a8 = 0;
      local_b0 = 0;
      uStack_98 = 0;
      uStack_a0 = 0;
      plStack_c8 = (long *)0x0;
      local_d0 = 0;
      uStack_b8 = 0;
      uStack_c0 = 0;
      FUN_05e1d31c(&local_160,&DAT_0a3ca1d0,&local_d0);
      thunk_FUN_05e1d0bc(&local_160);
      if (cStack_161 < '\0') {
        __ZdlPvm(local_178,CONCAT17(cStack_161,local_168) & 0x7fffffffffffffff);
      }
    }
    *param_1 = 0;
    param_1[1] = 0;
  }
  else {
    LOAcquire();
    lVar7 = plStack_c8[1];
    plStack_c8[1] = lVar7 + -1;
    LORelease();
    if (lVar7 != 0) goto LAB_02eb5814;
    (**(code **)(*plStack_c8 + 0x10))(plStack_c8);
    __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    if (local_170 != (long *)0x0) goto LAB_02eb581c;
LAB_02eb582c:
    if (local_198 == (undefined1 *)0x0) goto LAB_02eb5bb0;
LAB_02eb5834:
    plVar8 = (long *)__Znwm(0xf8);
    FUN_02ebf038(plVar8,&local_188);
    local_1e8 = plVar8 + 3;
    if (plVar8 != (long *)0x0) {
      plVar8[1] = plVar8[1] + 1;
    }
    local_1e0 = plVar8;
    local_160 = local_1e8;
    local_158 = plVar8;
    FUN_030d2154(auStack_1d8,local_198,&local_1e8);
    if (local_1b0 != (long *)0x0) {
      LOAcquire();
      lVar7 = local_1b0[1];
      local_1b0[1] = lVar7 + -1;
      LORelease();
      if (lVar7 == 0) {
        (**(code **)(*local_1b0 + 0x10))(local_1b0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(local_1b0);
      }
    }
    if (cStack_1b9 < '\0') {
      __ZdlPvm(local_1d0,CONCAT17(cStack_1b9,local_1c0) & 0x7fffffffffffffff);
    }
    plVar8 = local_1e0;
    if (local_1e0 != (long *)0x0) {
      LOAcquire();
      lVar7 = local_1e0[1];
      local_1e0[1] = lVar7 + -1;
      LORelease();
      if (lVar7 == 0) {
        (**(code **)(*local_1e0 + 0x10))(local_1e0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
      }
    }
    lVar6 = local_160[3];
    *param_1 = lVar6;
    lVar4 = local_160[4];
    param_1[1] = lVar4;
    lVar7 = 0;
    if (lVar4 != 0) {
      lVar7 = *(long *)(lVar4 + 8);
      *(long *)(lVar4 + 8) = lVar7 + 1;
    }
    if ((*(long *)(lVar6 + 0x220) == 0) ||
       (local_d0 = ___dynamic_cast(lVar7,*(long *)(lVar6 + 0x220),&PTR_DAT_09eb1040,
                                   &PTR_DAT_09eb0cc0,0), local_d0 == 0)) {
      local_d0 = 0;
      plStack_c8 = (long *)0x0;
      local_1f0 = (long *)0x0;
    }
    else {
      plStack_c8 = *(long **)(lVar6 + 0x228);
      if (plStack_c8 == (long *)0x0) {
        local_1f0 = (long *)0x0;
      }
      else {
        plVar8 = plStack_c8 + 1;
        *plVar8 = *plVar8 + 1;
        *plVar8 = *plVar8 + 1;
        local_1f0 = plStack_c8;
      }
    }
    local_1f8 = local_d0;
    (**(code **)(*local_188 + 0x40))(local_188,&local_1f8);
    plVar8 = local_1f0;
    if (local_1f0 != (long *)0x0) {
      LOAcquire();
      lVar7 = local_1f0[1];
      local_1f0[1] = lVar7 + -1;
      LORelease();
      if (lVar7 == 0) {
        (**(code **)(*local_1f0 + 0x10))(local_1f0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
      }
    }
    plVar8 = plStack_c8;
    if (plStack_c8 != (long *)0x0) {
      LOAcquire();
      lVar7 = plStack_c8[1];
      plStack_c8[1] = lVar7 + -1;
      LORelease();
      if (lVar7 == 0) {
        (**(code **)(*plStack_c8 + 0x10))(plStack_c8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
      }
    }
    plVar8 = local_158;
    if (local_158 != (long *)0x0) {
      LOAcquire();
      lVar7 = local_158[1];
      local_158[1] = lVar7 + -1;
      LORelease();
      if (lVar7 == 0) {
        (**(code **)(*local_158 + 0x10))(local_158);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
      }
    }
  }
  plVar8 = local_190;
  if (local_190 != (long *)0x0) {
    LOAcquire();
    lVar7 = local_190[1];
    local_190[1] = lVar7 + -1;
    LORelease();
    if (lVar7 == 0) {
      (**(code **)(*local_190 + 0x10))(local_190);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    }
  }
  plVar8 = local_180;
  if (local_180 != (long *)0x0) {
    LOAcquire();
    lVar7 = local_180[1];
    local_180[1] = lVar7 + -1;
    LORelease();
    if (lVar7 == 0) {
      (**(code **)(*local_180 + 0x10))(local_180);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    }
  }
LAB_02eb5d80:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


