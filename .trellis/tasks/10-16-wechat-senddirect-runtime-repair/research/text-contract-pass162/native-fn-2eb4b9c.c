// Ghidra inferred pseudocode; requested=0x2eb4b9c
// entry=02eb4b9c end=02eb54c3

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_02eb4b9c(long *param_1,undefined8 param_2,long *param_3)

{
  long *plVar1;
  undefined8 *******pppppppuVar2;
  int iVar3;
  undefined8 *puVar4;
  long *plVar5;
  long lVar6;
  long lVar7;
  ulong uVar8;
  long lVar9;
  undefined4 uVar10;
  long local_278;
  long *local_270;
  long *local_268;
  long *local_260;
  undefined1 auStack_258 [8];
  undefined8 local_250;
  undefined7 local_240;
  char cStack_239;
  long *local_230;
  undefined8 *******local_228;
  long *local_220;
  undefined7 local_218;
  char cStack_211;
  long *local_210;
  long *local_208;
  undefined1 *local_200;
  long *local_1f8;
  long *local_1f0;
  long *local_1e8;
  undefined1 *local_1e0;
  undefined1 *puStack_1d8;
  undefined1 *local_1d0;
  undefined1 *local_1c0;
  undefined1 *puStack_1b8;
  undefined1 *local_1b0;
  undefined1 *local_1a0;
  undefined1 *puStack_198;
  undefined1 *local_190;
  undefined8 *******local_180;
  undefined1 *puStack_178;
  undefined1 *local_170;
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
  puVar4 = (undefined8 *)*param_3;
  if (puVar4 == (undefined8 *)0x0) {
    iVar3 = thunk_FUN_05e1d97c(4);
    if (iVar3 != 0) {
      FUN_0488143c(&local_180);
      pppppppuVar2 = local_180;
      if (-1 < (long)local_170) {
        pppppppuVar2 = &local_180;
      }
      if ((DAT_0a3c9f34 & 1) == 0) {
        uVar8 = 0;
        do {
          (&DAT_0a3c9f1b)[uVar8] = (&DAT_08886d88)[uVar8] + 0x8a ^ (&DAT_08886d78)[uVar8 & 0xf];
          uVar8 = uVar8 + 1;
        } while (uVar8 != 0x19);
        DAT_0a3c9f34 = 1;
      }
      if ((DAT_0a3ca1fc & 1) == 0) {
        _DAT_0a3ca1e4 = CONCAT44((int)DAT_086c0318,(int)DAT_084d5770);
        uRam000000000a3ca1ec = CONCAT44((int)DAT_084a8110,(int)ram0x08886930);
        DAT_0a3ca1f4 = CONCAT44((int)DAT_08728740,(int)ram0x085d6680);
        DAT_0a3ca1fc = 1;
      }
      FUN_05e1d050(&local_160,4,pppppppuVar2,&DAT_0a3c9f1b,&DAT_0a3ca1e4,0x171,0,0);
      if ((DAT_0a3ca210 & 1) == 0) {
        uRam000000000a3ca208._0_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0xa8];
        uRam000000000a3ca208._1_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0xa9];
        uRam000000000a3ca208._2_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0xaa];
        uRam000000000a3ca208._3_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0xab];
        uRam000000000a3ca208._4_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0xac];
        uRam000000000a3ca208._5_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0xad];
        uRam000000000a3ca208._6_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0xae];
        uRam000000000a3ca208._7_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0xaf];
        DAT_0a3ca200 = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0xa0];
        DAT_0a3ca200_1._0_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0xa1];
        DAT_0a3ca200_1._1_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0xa2];
        DAT_0a3ca200_1._2_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0xa3];
        DAT_0a3ca200_1._3_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0xa4];
        DAT_0a3ca200_1._4_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0xa5];
        DAT_0a3ca200_1._5_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0xa6];
        DAT_0a3ca200_1._6_1_ = s_LaunchMapByLiteALaunchTabInterna_087d26c0[0xa7];
        DAT_0a3ca210 = 1;
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
      FUN_05e1d31c(&local_160,&DAT_0a3ca200,&local_d0);
      thunk_FUN_05e1d0bc(&local_160);
      if ((long)local_170 < 0) {
        __ZdlPvm(local_180,(ulong)local_170 & 0x7fffffffffffffff);
      }
    }
    *param_1 = 0;
    param_1[1] = 0;
    goto LAB_02eb53cc;
  }
  puStack_178 = &SUB_aaaaaaaaaaaaaaaa;
  local_170 = &SUB_aaaaaaaaaaaaaaaa;
  local_180 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
  lVar6 = puVar4[0x19];
  if (lVar6 == 0) {
    local_170 = &SUB_aaaaaaaaaaaaaa;
    local_180 = (undefined8 *******)&DAT_aaaaaaaaaaaaaa00;
  }
  else if (*(char *)(lVar6 + 0x47) < '\0') {
    FUN_00018d20(&local_180,*(undefined8 *)(lVar6 + 0x30),*(undefined8 *)(lVar6 + 0x38));
    puVar4 = (undefined8 *)*param_3;
  }
  else {
    puStack_178 = *(undefined1 **)(lVar6 + 0x38);
    local_180 = *(undefined8 ********)(lVar6 + 0x30);
    local_170 = *(undefined1 **)(lVar6 + 0x40);
  }
  puStack_198 = &SUB_aaaaaaaaaaaaaaaa;
  local_190 = &SUB_aaaaaaaaaaaaaaaa;
  local_1a0 = &SUB_aaaaaaaaaaaaaaaa;
  if (*(char *)((long)puVar4 + 0x17) < '\0') {
    FUN_00018d20(&local_1a0,*puVar4,puVar4[1]);
    puVar4 = (undefined8 *)*param_3;
  }
  else {
    puStack_198 = (undefined1 *)puVar4[1];
    local_1a0 = (undefined1 *)*puVar4;
    local_190 = (undefined1 *)puVar4[2];
  }
  puStack_1b8 = &SUB_aaaaaaaaaaaaaaaa;
  local_1b0 = &SUB_aaaaaaaaaaaaaaaa;
  local_1c0 = &SUB_aaaaaaaaaaaaaaaa;
  puVar4 = (undefined8 *)FUN_04de24dc(puVar4);
  if (*(char *)((long)puVar4 + 0x17) < '\0') {
    FUN_00018d20(&local_1c0,*puVar4,puVar4[1]);
  }
  else {
    puStack_1b8 = (undefined1 *)puVar4[1];
    local_1c0 = (undefined1 *)*puVar4;
    local_1b0 = (undefined1 *)puVar4[2];
  }
  lVar6 = *(long *)(*param_3 + 200);
  plVar5 = *(long **)(*param_3 + 0xd0);
  if (plVar5 == (long *)0x0) {
    uVar10 = (undefined4)*(undefined8 *)(lVar6 + 0xd0);
  }
  else {
    plVar1 = plVar5 + 1;
    *plVar1 = *plVar1 + 1;
    uVar10 = (undefined4)*(undefined8 *)(lVar6 + 0xd0);
    LOAcquire();
    lVar6 = *plVar1;
    *plVar1 = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*plVar5 + 0x10))(plVar5);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
    }
  }
  puStack_1d8 = &SUB_aaaaaaaaaaaaaaaa;
  local_1d0 = &SUB_aaaaaaaaaaaaaaaa;
  local_1e0 = &SUB_aaaaaaaaaaaaaaaa;
  lVar6 = *param_3;
  if (*(char *)(lVar6 + 0x77) < '\0') {
    FUN_00018d20(&local_1e0,*(undefined8 *)(lVar6 + 0x60),*(undefined8 *)(lVar6 + 0x68));
  }
  else {
    puStack_1d8 = *(undefined1 **)(lVar6 + 0x68);
    local_1e0 = *(undefined1 **)(lVar6 + 0x60);
    local_1d0 = *(undefined1 **)(lVar6 + 0x70);
  }
  local_1f0 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_1e8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0230e018(&local_1f0,&local_160);
  *(undefined8 *)((long)local_1f0 + 0xe4) = ram0x08791410;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (local_1f0 + 0xc9,&local_1a0);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (local_1f0 + 0xc6,&local_1c0);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (local_1f0 + 0xbf,&local_180);
  *(undefined4 *)((long)local_1f0 + 0x67c) = uVar10;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (local_1f0 + 0xb9,&local_1c0);
  local_200 = &SUB_aaaaaaaaaaaaaaaa;
  local_1f8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0466aca8(&local_228);
  FUN_01205740(&local_d0,local_228);
  FUN_0268f370(&local_160,local_d0);
  local_210 = local_1f0;
  local_208 = local_1e8;
  if (local_1e8 != (long *)0x0) {
    local_1e8[1] = local_1e8[1] + 1;
  }
  FUN_0319a638(&local_200,local_160,&local_210);
  plVar5 = local_208;
  if (local_208 != (long *)0x0) {
    LOAcquire();
    lVar6 = local_208[1];
    local_208[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*local_208 + 0x10))(local_208);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
    }
  }
  plVar5 = local_158;
  if (local_158 != (long *)0x0) {
    LOAcquire();
    lVar6 = local_158[1];
    local_158[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*local_158 + 0x10))(local_158);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
    }
  }
  plVar5 = plStack_c8;
  if (plStack_c8 == (long *)0x0) {
LAB_02eb4fbc:
    if (local_220 == (long *)0x0) goto LAB_02eb4fd4;
LAB_02eb4fc4:
    LOAcquire();
    lVar6 = local_220[1];
    local_220[1] = lVar6 + -1;
    LORelease();
    if (lVar6 != 0) goto LAB_02eb4fd4;
    (**(code **)(*local_220 + 0x10))(local_220);
    __ZNSt3__119__shared_weak_count14__release_weakEv(local_220);
    if (local_200 != (undefined1 *)0x0) goto LAB_02eb4fdc;
LAB_02eb51f8:
    iVar3 = thunk_FUN_05e1d97c(4);
    if (iVar3 != 0) {
      FUN_0488143c(&local_228);
      pppppppuVar2 = local_228;
      if (-1 < cStack_211) {
        pppppppuVar2 = &local_228;
      }
      if ((DAT_0a3c9f34 & 1) == 0) {
        uVar8 = 0;
        do {
          (&DAT_0a3c9f1b)[uVar8] = (&DAT_08886d88)[uVar8] + 0x8a ^ (&DAT_08886d78)[uVar8 & 0xf];
          uVar8 = uVar8 + 1;
        } while (uVar8 != 0x19);
        DAT_0a3c9f34 = 1;
      }
      if ((DAT_0a3ca1fc & 1) == 0) {
        _DAT_0a3ca1e4 = CONCAT44((int)DAT_086c0318,(int)DAT_084d5770);
        uRam000000000a3ca1ec = CONCAT44((int)DAT_084a8110,(int)ram0x08886930);
        DAT_0a3ca1f4 = CONCAT44((int)DAT_08728740,(int)ram0x085d6680);
        DAT_0a3ca1fc = 1;
      }
      FUN_05e1d050(&local_160,4,pppppppuVar2,&DAT_0a3c9f1b,&DAT_0a3ca1e4,0x187,0,0);
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
      if (cStack_211 < '\0') {
        __ZdlPvm(local_228,CONCAT17(cStack_211,local_218) & 0x7fffffffffffffff);
      }
    }
    *param_1 = 0;
    param_1[1] = 0;
  }
  else {
    LOAcquire();
    lVar6 = plStack_c8[1];
    plStack_c8[1] = lVar6 + -1;
    LORelease();
    if (lVar6 != 0) goto LAB_02eb4fbc;
    (**(code **)(*plStack_c8 + 0x10))(plStack_c8);
    __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
    if (local_220 != (long *)0x0) goto LAB_02eb4fc4;
LAB_02eb4fd4:
    if (local_200 == (undefined1 *)0x0) goto LAB_02eb51f8;
LAB_02eb4fdc:
    plVar5 = (long *)__Znwm(0xf8);
    FUN_02ebf12c(plVar5,&local_1f0);
    local_268 = plVar5 + 3;
    if (plVar5 != (long *)0x0) {
      plVar5[1] = plVar5[1] + 1;
    }
    local_260 = plVar5;
    local_160 = local_268;
    local_158 = plVar5;
    FUN_030d2154(auStack_258,local_200,&local_268);
    if (local_230 != (long *)0x0) {
      LOAcquire();
      lVar6 = local_230[1];
      local_230[1] = lVar6 + -1;
      LORelease();
      if (lVar6 == 0) {
        (**(code **)(*local_230 + 0x10))(local_230);
        __ZNSt3__119__shared_weak_count14__release_weakEv(local_230);
      }
    }
    if (cStack_239 < '\0') {
      __ZdlPvm(local_250,CONCAT17(cStack_239,local_240) & 0x7fffffffffffffff);
    }
    plVar5 = local_260;
    if (local_260 != (long *)0x0) {
      LOAcquire();
      lVar6 = local_260[1];
      local_260[1] = lVar6 + -1;
      LORelease();
      if (lVar6 == 0) {
        (**(code **)(*local_260 + 0x10))(local_260);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
      }
    }
    lVar9 = local_160[3];
    *param_1 = lVar9;
    lVar7 = local_160[4];
    param_1[1] = lVar7;
    lVar6 = 0;
    if (lVar7 != 0) {
      lVar6 = *(long *)(lVar7 + 8);
      *(long *)(lVar7 + 8) = lVar6 + 1;
    }
    if ((*(long *)(lVar9 + 0x220) == 0) ||
       (local_d0 = ___dynamic_cast(lVar6,*(long *)(lVar9 + 0x220),&PTR_DAT_09eb1040,
                                   &PTR_DAT_09eb0cc0,0), local_d0 == 0)) {
      local_d0 = 0;
      plStack_c8 = (long *)0x0;
    }
    else {
      plStack_c8 = *(long **)(lVar9 + 0x228);
      if (plStack_c8 != (long *)0x0) {
        plStack_c8[1] = plStack_c8[1] + 1;
      }
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (local_d0 + 0x398,&local_1e0);
    local_278 = local_d0;
    local_270 = plStack_c8;
    if (plStack_c8 != (long *)0x0) {
      plStack_c8[1] = plStack_c8[1] + 1;
    }
    (**(code **)(*local_1f0 + 0x40))(local_1f0,&local_278);
    plVar5 = local_270;
    if (local_270 != (long *)0x0) {
      LOAcquire();
      lVar6 = local_270[1];
      local_270[1] = lVar6 + -1;
      LORelease();
      if (lVar6 == 0) {
        (**(code **)(*local_270 + 0x10))(local_270);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
      }
    }
    plVar5 = plStack_c8;
    if (plStack_c8 != (long *)0x0) {
      LOAcquire();
      lVar6 = plStack_c8[1];
      plStack_c8[1] = lVar6 + -1;
      LORelease();
      if (lVar6 == 0) {
        (**(code **)(*plStack_c8 + 0x10))(plStack_c8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
      }
    }
    plVar5 = local_158;
    if (local_158 != (long *)0x0) {
      LOAcquire();
      lVar6 = local_158[1];
      local_158[1] = lVar6 + -1;
      LORelease();
      if (lVar6 == 0) {
        (**(code **)(*local_158 + 0x10))(local_158);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
      }
    }
  }
  plVar1 = local_1f8;
  plVar5 = local_1e8;
  if (local_1f8 != (long *)0x0) {
    LOAcquire();
    lVar6 = local_1f8[1];
    local_1f8[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*local_1f8 + 0x10))(local_1f8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
      plVar5 = local_1e8;
    }
  }
  local_1e8 = plVar5;
  if (plVar5 != (long *)0x0) {
    LOAcquire();
    lVar6 = *(long *)((long)plVar5 + 8U);
    *(long *)((long)plVar5 + 8U) = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*plVar5 + 0x10))(plVar5);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
    }
  }
  if ((long)local_1d0 < 0) {
    __ZdlPvm(local_1e0,(ulong)local_1d0 & 0x7fffffffffffffff);
  }
  if ((long)local_1b0 < 0) {
    __ZdlPvm(local_1c0,(ulong)local_1b0 & 0x7fffffffffffffff);
  }
  if ((long)local_190 < 0) {
    __ZdlPvm(local_1a0,(ulong)local_190 & 0x7fffffffffffffff);
  }
  if ((long)local_170 < 0) {
    __ZdlPvm(local_180,(ulong)local_170 & 0x7fffffffffffffff);
  }
LAB_02eb53cc:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


