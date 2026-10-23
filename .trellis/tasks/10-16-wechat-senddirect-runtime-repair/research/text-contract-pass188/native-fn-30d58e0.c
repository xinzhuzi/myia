// Ghidra inferred pseudocode; requested=0x30d58e0
// entry=030d58e0 end=030d6503

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_030d58e0(undefined8 *param_1,long *param_2,long *param_3)

{
  undefined1 *puVar1;
  undefined8 *******pppppppuVar2;
  long lVar3;
  int iVar4;
  ulong uVar5;
  undefined8 *puVar6;
  undefined8 *******pppppppuVar7;
  long *plVar8;
  long lVar9;
  undefined8 uVar10;
  undefined1 *local_728;
  long *plStack_720;
  long local_718;
  long *local_710;
  undefined8 local_708;
  long *local_700;
  undefined8 local_6f8;
  long *local_6f0;
  undefined8 local_6e8;
  long *local_6e0;
  undefined8 local_6d8;
  long *local_6d0;
  undefined1 *local_6c8;
  long *local_6c0 [2];
  undefined7 local_6b0;
  char cStack_6a9;
  undefined1 *local_6a8;
  long *local_6a0;
  undefined1 auStack_670 [760];
  long local_378;
  long *local_370;
  long local_368;
  long *local_360;
  long local_358;
  long *local_350;
  long local_348;
  long *local_340;
  undefined8 *******local_338;
  undefined8 *******local_330;
  undefined8 *******local_328;
  long *local_320;
  long *local_318;
  undefined8 local_310;
  undefined1 *puStack_308;
  undefined1 *local_300;
  undefined1 *puStack_2f8;
  undefined1 *local_2f0;
  long *local_2e8;
  undefined8 *******local_2e0;
  undefined1 *local_2d8;
  undefined8 local_2d0;
  undefined8 uStack_2c8;
  undefined8 uStack_2c0;
  undefined8 uStack_2b8;
  undefined8 local_2b0;
  undefined8 uStack_2a8;
  undefined8 uStack_2a0;
  undefined8 uStack_298;
  undefined8 local_290;
  undefined8 uStack_288;
  undefined8 uStack_280;
  undefined8 uStack_278;
  undefined8 local_270;
  undefined8 uStack_268;
  undefined8 uStack_260;
  undefined8 uStack_258;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  puStack_2f8 = &SUB_aaaaaaaaaaaaaaaa;
  local_300 = &SUB_aaaaaaaaaaaaaaaa;
  local_2e8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_2f0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_308 = &SUB_aaaaaaaaaaaaaaaa;
  local_310 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0304f1cc(&local_310,0,0);
  local_320 = *(long **)(*param_3 + 8);
  if (local_320 == (long *)0x0) {
    local_318 = (long *)0x0;
    local_320 = (long *)0x0;
    iVar4 = thunk_FUN_05e1d97c(4);
    if (iVar4 != 0) {
      FUN_0488143c(&local_338);
      pppppppuVar7 = local_338;
      if (-1 < (long)local_328) {
        pppppppuVar7 = &local_338;
      }
      if ((DAT_0a3d8d03 & 1) == 0) {
        uRam000000000a3d8cf8._0_1_ = s_message_handler_get_aeskey_faile_088ae330[8];
        uRam000000000a3d8cf8._1_1_ = s_message_handler_get_aeskey_faile_088ae330[9];
        uRam000000000a3d8cf8._2_1_ = s_message_handler_get_aeskey_faile_088ae330[10];
        uRam000000000a3d8cf8._3_1_ = s_message_handler_get_aeskey_faile_088ae330[0xb];
        uRam000000000a3d8cf8._4_1_ = s_message_handler_get_aeskey_faile_088ae330[0xc];
        uRam000000000a3d8cf8._5_1_ = s_message_handler_get_aeskey_faile_088ae330[0xd];
        uRam000000000a3d8cf8._6_1_ = s_message_handler_get_aeskey_faile_088ae330[0xe];
        uRam000000000a3d8cf8._7_1_ = s_message_handler_get_aeskey_faile_088ae330[0xf];
        DAT_0a3d8cf0 = s_message_handler_get_aeskey_faile_088ae330[0];
        DAT_0a3d8cf0_1._0_1_ = s_message_handler_get_aeskey_faile_088ae330[1];
        DAT_0a3d8cf0_1._1_1_ = s_message_handler_get_aeskey_faile_088ae330[2];
        DAT_0a3d8cf0_1._2_1_ = s_message_handler_get_aeskey_faile_088ae330[3];
        DAT_0a3d8cf0_1._3_1_ = s_message_handler_get_aeskey_faile_088ae330[4];
        DAT_0a3d8cf0_1._4_1_ = s_message_handler_get_aeskey_faile_088ae330[5];
        DAT_0a3d8cf0_1._5_1_ = s_message_handler_get_aeskey_faile_088ae330[6];
        DAT_0a3d8cf0_1._6_1_ = s_message_handler_get_aeskey_faile_088ae330[7];
        DAT_0a3d8d00 = 0x6363;
        DAT_0a3d8d02 = 0;
        DAT_0a3d8d03 = 1;
      }
      if ((DAT_0a3d8ed6 & 1) == 0) {
        _DAT_0a3d8ebc = CONCAT44((int)DAT_087e2df0,(int)ram0x087e2de8);
        uRam000000000a3d8ec4 = CONCAT44((int)DAT_084a66b0,(int)DAT_08508320);
        DAT_0a3d8ecc = CONCAT44((int)DAT_086c55e0,(int)DAT_086eb4a8);
        DAT_0a3d8ed4 = 0x77;
        DAT_0a3d8ed6 = 1;
      }
      FUN_05e1d050(&local_6c8,4,pppppppuVar7,&DAT_0a3d8cf0,&DAT_0a3d8ebc,0xd4,0,0);
      if ((DAT_0a3d8e23 & 1) == 0) {
        _DAT_0a3d8e0c = CONCAT44((int)DAT_084abe90,(int)DAT_084a8ea0);
        uRam000000000a3d8e14 = CONCAT44((int)DAT_08486ac8,(int)DAT_0856e3c0);
        DAT_0a3d8e1c = (undefined4)DAT_0854c0c0;
        DAT_0a3d8e20 = 0x7274;
        DAT_0a3d8e22 = 0;
        DAT_0a3d8e23 = 1;
      }
      uStack_268 = 0;
      local_270 = 0;
      uStack_258 = 0;
      uStack_260 = 0;
      uStack_288 = 0;
      local_290 = 0;
      uStack_278 = 0;
      uStack_280 = 0;
      uStack_2a8 = 0;
      local_2b0 = 0;
      uStack_298 = 0;
      uStack_2a0 = 0;
      uStack_2c8 = 0;
      local_2d0 = 0;
      uStack_2b8 = 0;
      uStack_2c0 = 0;
      FUN_05e1d31c(&local_6c8,&DAT_0a3d8e0c,&local_2d0);
      thunk_FUN_05e1d0bc(&local_6c8);
      if ((long)local_328 < 0) {
        __ZdlPvm(local_338,(ulong)local_328 & 0x7fffffffffffffff);
      }
    }
    FUN_030f6650(param_1,1,1,4,400);
    goto LAB_030d6448;
  }
  local_318 = *(long **)(*param_3 + 0x10);
  if (local_318 != (long *)0x0) {
    local_318[1] = local_318[1] + 1;
  }
  iVar4 = (**(code **)(*local_320 + 0x20))();
  if (iVar4 < 3) {
    if (iVar4 == 1) {
      local_348 = *param_3;
      local_340 = (long *)param_3[1];
      if (local_340 != (long *)0x0) {
        local_340[1] = local_340[1] + 1;
      }
      (**(code **)(*param_2 + 0x90))(&local_6c8,param_2,&local_348);
      local_310 = local_6c8;
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                ((ulong)&local_310 | 8,local_6c0);
      plVar8 = local_2e8;
      if (local_6a0 != (long *)0x0) {
        local_6a0[1] = local_6a0[1] + 1;
      }
      local_2f0 = local_6a8;
      local_2e8 = local_6a0;
      if (plVar8 != (long *)0x0) {
        LOAcquire();
        lVar3 = plVar8[1];
        plVar8[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*plVar8 + 0x10))(plVar8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
        }
      }
      if (local_6a0 != (long *)0x0) {
        LOAcquire();
        lVar3 = local_6a0[1];
        local_6a0[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*local_6a0 + 0x10))(local_6a0);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_6a0);
        }
      }
      plVar8 = local_340;
      if (cStack_6a9 < '\0') {
        __ZdlPvm(local_6c0[0],CONCAT17(cStack_6a9,local_6b0) & 0x7fffffffffffffff);
        plVar8 = local_340;
      }
joined_r0x030d5d28:
      if (plVar8 != (long *)0x0) goto LAB_030d6304;
    }
    else if (iVar4 == 2) {
      local_358 = *param_3;
      local_350 = (long *)param_3[1];
      if (local_350 != (long *)0x0) {
        local_350[1] = local_350[1] + 1;
      }
      (**(code **)(*param_2 + 0xa8))(&local_6c8,param_2,&local_358);
      local_310 = local_6c8;
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                ((ulong)&local_310 | 8,local_6c0);
      plVar8 = local_2e8;
      if (local_6a0 != (long *)0x0) {
        local_6a0[1] = local_6a0[1] + 1;
      }
      local_2f0 = local_6a8;
      local_2e8 = local_6a0;
      if (plVar8 != (long *)0x0) {
        LOAcquire();
        lVar3 = plVar8[1];
        plVar8[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*plVar8 + 0x10))(plVar8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
        }
      }
      if (local_6a0 != (long *)0x0) {
        LOAcquire();
        lVar3 = local_6a0[1];
        local_6a0[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*local_6a0 + 0x10))(local_6a0);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_6a0);
        }
      }
      plVar8 = local_350;
      if (cStack_6a9 < '\0') {
        __ZdlPvm(local_6c0[0],CONCAT17(cStack_6a9,local_6b0) & 0x7fffffffffffffff);
        plVar8 = local_350;
      }
      goto joined_r0x030d6300;
    }
  }
  else {
    if (iVar4 != 3) {
      if (iVar4 != 4) goto LAB_030d632c;
      local_718 = *param_3;
      local_710 = (long *)param_3[1];
      if (local_710 != (long *)0x0) {
        local_710[1] = local_710[1] + 1;
      }
      (**(code **)(*param_2 + 0x90))(&local_6c8,param_2,&local_718);
      local_310 = local_6c8;
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                ((ulong)&local_310 | 8,local_6c0);
      plVar8 = local_2e8;
      if (local_6a0 != (long *)0x0) {
        local_6a0[1] = local_6a0[1] + 1;
      }
      local_2f0 = local_6a8;
      local_2e8 = local_6a0;
      if (plVar8 != (long *)0x0) {
        LOAcquire();
        lVar3 = plVar8[1];
        plVar8[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*plVar8 + 0x10))(plVar8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
        }
      }
      if (local_6a0 != (long *)0x0) {
        LOAcquire();
        lVar3 = local_6a0[1];
        local_6a0[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*local_6a0 + 0x10))(local_6a0);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_6a0);
        }
      }
      plVar8 = local_710;
      if (cStack_6a9 < '\0') {
        __ZdlPvm(local_6c0[0],CONCAT17(cStack_6a9,local_6b0) & 0x7fffffffffffffff);
        plVar8 = local_710;
      }
      goto joined_r0x030d5d28;
    }
    local_368 = *param_3;
    local_360 = (long *)param_3[1];
    if (local_360 != (long *)0x0) {
      local_360[1] = local_360[1] + 1;
    }
    (**(code **)(*param_2 + 0xa8))(&local_6c8,param_2,&local_368);
    local_310 = local_6c8;
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              ((ulong)&local_310 | 8,local_6c0);
    plVar8 = local_2e8;
    if (local_6a0 != (long *)0x0) {
      local_6a0[1] = local_6a0[1] + 1;
    }
    local_2f0 = local_6a8;
    local_2e8 = local_6a0;
    if (plVar8 != (long *)0x0) {
      LOAcquire();
      lVar3 = plVar8[1];
      plVar8[1] = lVar3 + -1;
      LORelease();
      if (lVar3 == 0) {
        (**(code **)(*plVar8 + 0x10))(plVar8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
      }
    }
    if (local_6a0 != (long *)0x0) {
      LOAcquire();
      lVar3 = local_6a0[1];
      local_6a0[1] = lVar3 + -1;
      LORelease();
      if (lVar3 == 0) {
        (**(code **)(*local_6a0 + 0x10))(local_6a0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(local_6a0);
      }
    }
    if (cStack_6a9 < '\0') {
      __ZdlPvm(local_6c0[0],CONCAT17(cStack_6a9,local_6b0) & 0x7fffffffffffffff);
    }
    plVar8 = local_360;
    if (local_360 != (long *)0x0) {
      LOAcquire();
      lVar3 = local_360[1];
      local_360[1] = lVar3 + -1;
      LORelease();
      if (lVar3 == 0) {
        (**(code **)(*local_360 + 0x10))(local_360);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
      }
    }
    lVar9 = *param_3;
    lVar3 = *(long *)(lVar9 + 8);
    if ((lVar3 == 0) ||
       (lVar3 = ___dynamic_cast(lVar3,&PTR_DAT_09c37aa0,&PTR_DAT_09c3edd0,0), lVar3 == 0)) {
      local_370 = (long *)0x0;
      local_378 = 0;
      iVar4 = thunk_FUN_05e1d97c(4);
      plVar8 = local_370;
      if (iVar4 != 0) {
        FUN_0488143c(&local_338);
        pppppppuVar7 = local_338;
        if (-1 < (long)local_328) {
          pppppppuVar7 = &local_338;
        }
        if ((DAT_0a3d8d03 & 1) == 0) {
          uRam000000000a3d8cf8._0_1_ = s_message_handler_get_aeskey_faile_088ae330[8];
          uRam000000000a3d8cf8._1_1_ = s_message_handler_get_aeskey_faile_088ae330[9];
          uRam000000000a3d8cf8._2_1_ = s_message_handler_get_aeskey_faile_088ae330[10];
          uRam000000000a3d8cf8._3_1_ = s_message_handler_get_aeskey_faile_088ae330[0xb];
          uRam000000000a3d8cf8._4_1_ = s_message_handler_get_aeskey_faile_088ae330[0xc];
          uRam000000000a3d8cf8._5_1_ = s_message_handler_get_aeskey_faile_088ae330[0xd];
          uRam000000000a3d8cf8._6_1_ = s_message_handler_get_aeskey_faile_088ae330[0xe];
          uRam000000000a3d8cf8._7_1_ = s_message_handler_get_aeskey_faile_088ae330[0xf];
          DAT_0a3d8cf0 = s_message_handler_get_aeskey_faile_088ae330[0];
          DAT_0a3d8cf0_1._0_1_ = s_message_handler_get_aeskey_faile_088ae330[1];
          DAT_0a3d8cf0_1._1_1_ = s_message_handler_get_aeskey_faile_088ae330[2];
          DAT_0a3d8cf0_1._2_1_ = s_message_handler_get_aeskey_faile_088ae330[3];
          DAT_0a3d8cf0_1._3_1_ = s_message_handler_get_aeskey_faile_088ae330[4];
          DAT_0a3d8cf0_1._4_1_ = s_message_handler_get_aeskey_faile_088ae330[5];
          DAT_0a3d8cf0_1._5_1_ = s_message_handler_get_aeskey_faile_088ae330[6];
          DAT_0a3d8cf0_1._6_1_ = s_message_handler_get_aeskey_faile_088ae330[7];
          DAT_0a3d8d00 = 0x6363;
          DAT_0a3d8d02 = 0;
          DAT_0a3d8d03 = 1;
        }
        if ((DAT_0a3d8ed6 & 1) == 0) {
          _DAT_0a3d8ebc = CONCAT44((int)DAT_087e2df0,(int)ram0x087e2de8);
          uRam000000000a3d8ec4 = CONCAT44((int)DAT_084a66b0,(int)DAT_08508320);
          DAT_0a3d8ecc = CONCAT44((int)DAT_086c55e0,(int)DAT_086eb4a8);
          DAT_0a3d8ed4 = 0x77;
          DAT_0a3d8ed6 = 1;
        }
        FUN_05e1d050(&local_6c8,4,pppppppuVar7,&DAT_0a3d8cf0,&DAT_0a3d8ebc,0xe9,0,0);
        if ((DAT_0a3d8e7f & 1) == 0) {
          _DAT_0a3d8e68 = CONCAT44((int)DAT_084958d8,(int)ram0x0857f178);
          uRam000000000a3d8e70 = CONCAT44((int)DAT_08648e60,(int)DAT_08523398);
          DAT_0a3d8e78 = (undefined4)DAT_0854c0c0;
          DAT_0a3d8e7c = 0x7274;
          DAT_0a3d8e7e = 0;
          DAT_0a3d8e7f = 1;
        }
        uStack_268 = 0;
        local_270 = 0;
        uStack_258 = 0;
        uStack_260 = 0;
        uStack_288 = 0;
        local_290 = 0;
        uStack_278 = 0;
        uStack_280 = 0;
        uStack_2a8 = 0;
        local_2b0 = 0;
        uStack_298 = 0;
        uStack_2a0 = 0;
        uStack_2c8 = 0;
        local_2d0 = 0;
        uStack_2b8 = 0;
        uStack_2c0 = 0;
        FUN_05e1d31c(&local_6c8,&DAT_0a3d8e68,&local_2d0);
        thunk_FUN_05e1d0bc(&local_6c8);
        plVar8 = local_370;
        if ((long)local_328 < 0) {
          __ZdlPvm(local_338,(ulong)local_328 & 0x7fffffffffffffff);
          plVar8 = local_370;
        }
      }
    }
    else {
      local_370 = *(long **)(lVar9 + 0x10);
      if (local_370 != (long *)0x0) {
        local_370[1] = local_370[1] + 1;
      }
      local_378 = lVar3;
      _memcpy(&local_6c8,&DAT_088ae860,0x350);
      FUN_00395584(&local_6c8,lVar3 + 0xe8);
      FUN_0466aca8(&local_6f8);
      FUN_01205740(&local_6e8,local_6f8);
      FUN_0268f370(&local_6d8,local_6e8);
      FUN_039ee5e4(&local_708,&local_6c8);
      FUN_00f57630(&local_2d0,local_708);
      local_330 = (undefined8 *******)0x0;
      local_338 = (undefined8 *******)0x0;
      local_328 = (undefined8 *******)0x0;
      local_2e0 = &local_338;
      local_2d8 = &DAT_aaaaaaaaaaaaaa00;
      local_338 = (undefined8 *******)__Znwm(0x278);
      pppppppuVar7 = local_338 + 0x4f;
      local_330 = local_338;
      local_328 = pppppppuVar7;
      FUN_00f57630(local_338,&local_2d0);
      local_330 = pppppppuVar7;
      FUN_031ae0f0(local_6d8,auStack_670,&local_338);
      pppppppuVar2 = local_338;
      pppppppuVar7 = local_330;
      if (local_338 != (undefined8 *******)0x0) {
        while (pppppppuVar7 != pppppppuVar2) {
          pppppppuVar7 = pppppppuVar7 + -0x4f;
          (*(code *)**pppppppuVar7)(pppppppuVar7);
        }
        local_330 = pppppppuVar2;
        __ZdlPvm(local_338,(long)local_328 - (long)local_338);
      }
      FUN_00ac6290(&local_2d0);
      if (local_700 != (long *)0x0) {
        LOAcquire();
        lVar3 = local_700[1];
        local_700[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*local_700 + 0x10))(local_700);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_700);
        }
      }
      if (local_6d0 != (long *)0x0) {
        LOAcquire();
        lVar3 = local_6d0[1];
        local_6d0[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*local_6d0 + 0x10))(local_6d0);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_6d0);
        }
      }
      if (local_6e0 != (long *)0x0) {
        LOAcquire();
        lVar3 = local_6e0[1];
        local_6e0[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*local_6e0 + 0x10))(local_6e0);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_6e0);
        }
      }
      if (local_6f0 != (long *)0x0) {
        LOAcquire();
        lVar3 = local_6f0[1];
        local_6f0[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*local_6f0 + 0x10))(local_6f0);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_6f0);
        }
      }
      FUN_00396780(&local_6c8);
      plVar8 = local_370;
    }
joined_r0x030d6300:
    if (plVar8 == (long *)0x0) goto LAB_030d632c;
LAB_030d6304:
    LOAcquire();
    lVar3 = plVar8[1];
    plVar8[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*plVar8 + 0x10))(plVar8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    }
  }
LAB_030d632c:
  lVar3 = *param_3;
  puVar1 = *(undefined1 **)(lVar3 + 0x18);
  plVar8 = *(long **)(lVar3 + 0x20);
  if (plVar8 != (long *)0x0) {
    lVar3 = plVar8[1];
    plVar8[1] = lVar3 + 1;
  }
  local_6c8 = puVar1;
  local_6c0[0] = plVar8;
  FUN_04cbf874(lVar3,puVar1);
  uVar5 = (ulong)((uint)local_310 | local_310._4_4_);
  if (((uint)local_310 | local_310._4_4_) == 0) {
    FUN_030d05d0(param_2,0x800000000,puVar1);
  }
  else {
    if (plVar8 != (long *)0x0) {
      uVar5 = plVar8[1];
      plVar8[1] = uVar5 + 1;
    }
    local_728 = puVar1;
    plStack_720 = plVar8;
    FUN_030d5738(uVar5,param_2,&local_728);
    if (plVar8 != (long *)0x0) {
      LOAcquire();
      lVar3 = plVar8[1];
      plVar8[1] = lVar3 + -1;
      LORelease();
      if (lVar3 == 0) {
        (**(code **)(*plVar8 + 0x10))(plVar8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
      }
    }
  }
  *param_1 = local_310;
  if ((long)puStack_2f8 < 0) {
    FUN_00018d20(param_1 + 1,puStack_308,local_300);
  }
  else {
    puVar6 = (undefined8 *)((ulong)&local_310 | 8);
    uVar10 = *puVar6;
    param_1[2] = puVar6[1];
    param_1[1] = uVar10;
    param_1[3] = puVar6[2];
  }
  plVar8 = local_6c0[0];
  param_1[4] = local_2f0;
  param_1[5] = local_2e8;
  if (local_2e8 != (long *)0x0) {
    local_2e8[1] = local_2e8[1] + 1;
  }
  if (local_6c0[0] != (long *)0x0) {
    LOAcquire();
    lVar3 = local_6c0[0][1];
    local_6c0[0][1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_6c0[0] + 0x10))(local_6c0[0]);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    }
  }
LAB_030d6448:
  plVar8 = local_318;
  if (local_318 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_318[1];
    local_318[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_318 + 0x10))(local_318);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    }
  }
  plVar8 = local_2e8;
  if (local_2e8 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_2e8[1];
    local_2e8[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_2e8 + 0x10))(local_2e8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    }
  }
  if ((long)puStack_2f8 < 0) {
    __ZdlPvm(puStack_308,(ulong)puStack_2f8 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_58) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


