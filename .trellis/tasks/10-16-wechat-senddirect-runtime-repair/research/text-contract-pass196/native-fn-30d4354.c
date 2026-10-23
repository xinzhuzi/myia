// Ghidra inferred pseudocode; requested=0x30d4354
// entry=030d4354 end=030d54cb

/* WARNING: Removing unreachable block (ram,0x030d508c) */
/* WARNING: Removing unreachable block (ram,0x030d4684) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_030d4354(undefined8 *param_1,long *param_2,long *param_3)

{
  uint3 uVar1;
  undefined8 *******pppppppuVar2;
  long lVar3;
  int iVar4;
  undefined8 *******pppppppuVar5;
  undefined8 *puVar6;
  ulong uVar7;
  long *plVar8;
  long lVar9;
  undefined8 uVar10;
  undefined4 uVar11;
  undefined4 uVar12;
  undefined8 local_790;
  long *plStack_788;
  long local_780;
  long *local_778;
  undefined8 local_770;
  long *local_768;
  undefined8 local_760;
  long *local_758;
  undefined8 local_750;
  long *local_748;
  undefined8 local_740;
  long *local_738;
  undefined1 *local_730;
  undefined8 local_728 [2];
  undefined7 local_718;
  char cStack_711;
  undefined1 *local_710;
  long *local_708;
  undefined1 auStack_6d8 [760];
  long local_3e0;
  long *local_3d8;
  long local_3d0;
  long *local_3c8;
  long local_3c0;
  long *local_3b8;
  long local_3b0;
  long *local_3a8;
  undefined8 *******local_3a0;
  long *local_398;
  undefined7 local_390;
  char cStack_389;
  undefined8 *******local_388;
  undefined1 *local_380;
  undefined7 local_378;
  char cStack_371;
  long *local_370;
  long *local_368;
  undefined8 local_360;
  undefined1 *puStack_358;
  undefined1 *local_350;
  undefined1 *puStack_348;
  undefined1 *local_340;
  long *plStack_338;
  undefined8 *******local_330;
  undefined8 uStack_328;
  undefined8 uStack_320;
  undefined8 uStack_318;
  undefined8 uStack_310;
  undefined8 local_308;
  undefined8 uStack_300;
  undefined8 local_2f8;
  undefined8 uStack_2f0;
  undefined8 local_2e8;
  undefined8 uStack_2e0;
  undefined8 local_2d8;
  undefined8 uStack_2d0;
  undefined8 local_2c8;
  undefined8 uStack_2c0;
  undefined8 local_2b8;
  undefined8 *******local_b8;
  undefined8 *******local_b0;
  undefined8 *******local_a8;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  plStack_338 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_340 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_348 = &SUB_aaaaaaaaaaaaaaaa;
  local_350 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_358 = &SUB_aaaaaaaaaaaaaaaa;
  local_360 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0304f1cc(&local_360,0,0);
  local_370 = *(long **)(*param_3 + 8);
  if (local_370 == (long *)0x0) {
    local_368 = (long *)0x0;
    local_370 = (long *)0x0;
    iVar4 = thunk_FUN_05e1d97c(4);
    if (iVar4 != 0) {
      FUN_0488143c(&local_b8);
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
      if ((DAT_0a3d8e39 & 1) == 0) {
        _DAT_0a3d8e24 = CONCAT44((int)DAT_087e2df0,(int)ram0x087e2de8);
        uRam000000000a3d8e2c = CONCAT44((int)DAT_0867c9b8,(int)DAT_0854dcf8);
        DAT_0a3d8e34 = (undefined4)DAT_084a66b0;
        DAT_0a3d8e38 = 0;
        DAT_0a3d8e39 = 1;
      }
      FUN_05e1d050(&local_730,4,&local_b8,&DAT_0a3d8cf0,&DAT_0a3d8e24,0x92,0,0);
      if ((DAT_0a3d8e23 & 1) == 0) {
        _DAT_0a3d8e0c = CONCAT44((int)DAT_084abe90,(int)DAT_084a8ea0);
        uRam000000000a3d8e14 = CONCAT44((int)DAT_08486ac8,(int)DAT_0856e3c0);
        DAT_0a3d8e1c = (undefined4)DAT_0854c0c0;
        DAT_0a3d8e20 = 0x7274;
        DAT_0a3d8e22 = 0;
        DAT_0a3d8e23 = 1;
      }
      local_2b8 = 0;
      uStack_2c0 = 0;
      local_2c8 = 0;
      uStack_2d0 = 0;
      local_2d8 = 0;
      uStack_2e0 = 0;
      local_2e8 = 0;
      uStack_2f0 = 0;
      local_2f8 = 0;
      uStack_300 = 0;
      local_308 = 0;
      uStack_310 = 0;
      uStack_318 = 0;
      uStack_320 = 0;
      uStack_328 = 0;
      local_330 = (undefined8 *******)0x0;
      FUN_05e1d31c(&local_730,&DAT_0a3d8e0c,&local_330);
      thunk_FUN_05e1d0bc(&local_730);
    }
    FUN_030f6650(param_1,1,1,4,400);
    goto LAB_030d540c;
  }
  local_368 = *(long **)(*param_3 + 0x10);
  if (local_368 != (long *)0x0) {
    local_368[1] = local_368[1] + 1;
  }
  iVar4 = (**(code **)(*local_370 + 0x20))();
  if (iVar4 < 3) {
    if (iVar4 == 1) {
      if ((char)local_370[0x1b] != '\x01') {
        local_3c0 = *param_3;
        local_3b8 = (long *)param_3[1];
        if (local_3b8 != (long *)0x0) {
          local_3b8[1] = local_3b8[1] + 1;
        }
        (**(code **)(*param_2 + 0x80))(&local_730,param_2,&local_3c0);
        local_360 = local_730;
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  ((ulong)&local_360 | 8,local_728);
        plVar8 = plStack_338;
        if (local_708 != (long *)0x0) {
          local_708[1] = local_708[1] + 1;
        }
        local_340 = local_710;
        plStack_338 = local_708;
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
        if (local_708 != (long *)0x0) {
          LOAcquire();
          lVar3 = local_708[1];
          local_708[1] = lVar3 + -1;
          LORelease();
          if (lVar3 == 0) {
            (**(code **)(*local_708 + 0x10))(local_708);
            __ZNSt3__119__shared_weak_count14__release_weakEv(local_708);
          }
        }
        plVar8 = local_3b8;
        if (cStack_711 < '\0') {
          __ZdlPvm(local_728[0],CONCAT17(cStack_711,local_718) & 0x7fffffffffffffff);
          plVar8 = local_3b8;
        }
        goto joined_r0x030d4ef0;
      }
      iVar4 = thunk_FUN_05e1d97c(2);
      if (iVar4 != 0) {
        FUN_0488143c(&local_388);
        pppppppuVar5 = local_388;
        if (-1 < cStack_371) {
          pppppppuVar5 = &local_388;
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
        if ((DAT_0a3d8e39 & 1) == 0) {
          _DAT_0a3d8e24 = CONCAT44((int)DAT_087e2df0,(int)ram0x087e2de8);
          uRam000000000a3d8e2c = CONCAT44((int)DAT_0867c9b8,(int)DAT_0854dcf8);
          DAT_0a3d8e34 = (undefined4)DAT_084a66b0;
          DAT_0a3d8e38 = 0;
          DAT_0a3d8e39 = 1;
        }
        FUN_05e1d050(&local_730,2,pppppppuVar5,&DAT_0a3d8cf0,&DAT_0a3d8e24,0x9a,0,0);
        FUN_030f1f08(&local_3a0,*param_3);
        local_b8 = local_3a0;
        if (-1 < cStack_389) {
          local_b8 = &local_3a0;
        }
        local_b0 = (undefined8 *******)((ulong)local_b0 & 0xffffffffffffff00);
        if ((DAT_0a3d8e67 & 1) == 0) {
          _DAT_0a3d8e3c = CONCAT44((int)DAT_084ec280,(int)DAT_08486a48);
          uRam000000000a3d8e44 = CONCAT44((int)DAT_0884db28,(int)DAT_084ec258);
          _DAT_0a3d8e4c = CONCAT44((int)DAT_084916e8,(int)DAT_088ae238);
          uRam000000000a3d8e54 = CONCAT44((int)DAT_088ae240,(int)DAT_08487d40);
          DAT_0a3d8e5c = CONCAT44((int)DAT_08485ea0,(int)DAT_088ae248);
          DAT_0a3d8e64 = 0x2970;
          DAT_0a3d8e66 = 0;
          DAT_0a3d8e67 = 1;
        }
        uStack_320 = 0;
        uStack_328 = 0;
        local_330 = &local_b8;
        uStack_310 = 0;
        uStack_318 = 0;
        uStack_300 = 0;
        local_308 = 0;
        uStack_2f0 = 0;
        local_2f8 = 0;
        uStack_2e0 = 0;
        local_2e8 = 0;
        uStack_2d0 = 0;
        local_2d8 = 0;
        uStack_2c0 = 0;
        local_2c8 = 0;
        local_2b8 = 0;
        FUN_05e1d31c(&local_730,&DAT_0a3d8e3c,&local_330);
        if (cStack_389 < '\0') {
          __ZdlPvm(local_3a0,CONCAT17(cStack_389,local_390) & 0x7fffffffffffffff);
        }
        thunk_FUN_05e1d0bc(&local_730);
        if (cStack_371 < '\0') {
          __ZdlPvm(local_388,CONCAT17(cStack_371,local_378) & 0x7fffffffffffffff);
        }
      }
      local_3b0 = *param_3;
      local_3a8 = (long *)param_3[1];
      if (local_3a8 != (long *)0x0) {
        local_3a8[1] = local_3a8[1] + 1;
      }
      (**(code **)(*param_2 + 0x88))(&local_730,param_2,&local_3b0);
      local_360 = local_730;
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                ((ulong)&local_360 | 8,local_728);
      plVar8 = plStack_338;
      if (local_708 != (long *)0x0) {
        local_708[1] = local_708[1] + 1;
      }
      local_340 = local_710;
      plStack_338 = local_708;
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
      if (local_708 != (long *)0x0) {
        LOAcquire();
        lVar3 = local_708[1];
        local_708[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*local_708 + 0x10))(local_708);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_708);
        }
      }
      plVar8 = local_3a8;
      if (cStack_711 < '\0') {
        __ZdlPvm(local_728[0],CONCAT17(cStack_711,local_718) & 0x7fffffffffffffff);
        plVar8 = local_3a8;
      }
joined_r0x030d47a4:
      if (plVar8 == (long *)0x0) goto LAB_030d50cc;
LAB_030d50a4:
      LOAcquire();
      lVar3 = plVar8[1];
      plVar8[1] = lVar3 + -1;
      LORelease();
      if (lVar3 == 0) {
        (**(code **)(*plVar8 + 0x10))(plVar8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
      }
    }
    else if (iVar4 == 2) {
      local_3d0 = *param_3;
      local_3c8 = (long *)param_3[1];
      if (local_3c8 != (long *)0x0) {
        local_3c8[1] = local_3c8[1] + 1;
      }
      (**(code **)(*param_2 + 0xa0))(&local_730,param_2,&local_3d0);
      local_360 = local_730;
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                ((ulong)&local_360 | 8,local_728);
      plVar8 = plStack_338;
      if (local_708 != (long *)0x0) {
        local_708[1] = local_708[1] + 1;
      }
      local_340 = local_710;
      plStack_338 = local_708;
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
      if (local_708 != (long *)0x0) {
        LOAcquire();
        lVar3 = local_708[1];
        local_708[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*local_708 + 0x10))(local_708);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_708);
        }
      }
      plVar8 = local_3c8;
      if (cStack_711 < '\0') {
        __ZdlPvm(local_728[0],CONCAT17(cStack_711,local_718) & 0x7fffffffffffffff);
        plVar8 = local_3c8;
      }
joined_r0x030d4ef0:
      if (plVar8 != (long *)0x0) goto LAB_030d50a4;
    }
  }
  else if (iVar4 == 3) {
    local_3e0 = *param_3;
    local_3d8 = (long *)param_3[1];
    if (local_3d8 != (long *)0x0) {
      local_3d8[1] = local_3d8[1] + 1;
    }
    (**(code **)(*param_2 + 0xa0))(&local_730,param_2,&local_3e0);
    local_360 = local_730;
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              ((ulong)&local_360 | 8,local_728);
    plVar8 = plStack_338;
    if (local_708 != (long *)0x0) {
      local_708[1] = local_708[1] + 1;
    }
    local_340 = local_710;
    plStack_338 = local_708;
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
    if (local_708 != (long *)0x0) {
      LOAcquire();
      lVar3 = local_708[1];
      local_708[1] = lVar3 + -1;
      LORelease();
      if (lVar3 == 0) {
        (**(code **)(*local_708 + 0x10))(local_708);
        __ZNSt3__119__shared_weak_count14__release_weakEv(local_708);
      }
    }
    if (cStack_711 < '\0') {
      __ZdlPvm(local_728[0],CONCAT17(cStack_711,local_718) & 0x7fffffffffffffff);
    }
    plVar8 = local_3d8;
    if (local_3d8 != (long *)0x0) {
      LOAcquire();
      lVar3 = local_3d8[1];
      local_3d8[1] = lVar3 + -1;
      LORelease();
      if (lVar3 == 0) {
        (**(code **)(*local_3d8 + 0x10))(local_3d8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
      }
    }
    if ((uint)local_360 != 0 || local_360._4_4_ != 0) {
      lVar9 = *param_3;
      lVar3 = *(long *)(lVar9 + 8);
      if ((lVar3 == 0) ||
         (pppppppuVar5 = (undefined8 *******)
                         ___dynamic_cast(lVar3,&PTR_DAT_09c37aa0,&PTR_DAT_09c3edd0,0),
         pppppppuVar5 == (undefined8 *******)0x0)) {
        local_398 = (long *)0x0;
        local_3a0 = (undefined8 *******)0x0;
        iVar4 = thunk_FUN_05e1d97c(4);
        plVar8 = local_398;
        if (iVar4 != 0) {
          FUN_0488143c(&local_b8);
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
          if ((DAT_0a3d8e39 & 1) == 0) {
            _DAT_0a3d8e24 = CONCAT44((int)DAT_087e2df0,(int)ram0x087e2de8);
            uRam000000000a3d8e2c = CONCAT44((int)DAT_0867c9b8,(int)DAT_0854dcf8);
            DAT_0a3d8e34 = (undefined4)DAT_084a66b0;
            DAT_0a3d8e38 = 0;
            DAT_0a3d8e39 = 1;
          }
          FUN_05e1d050(&local_730,4,&local_b8,&DAT_0a3d8cf0,&DAT_0a3d8e24,0xaf,0,0);
          if ((DAT_0a3d8e7f & 1) == 0) {
            _DAT_0a3d8e68 = CONCAT44((int)DAT_084958d8,(int)ram0x0857f178);
            uRam000000000a3d8e70 = CONCAT44((int)DAT_08648e60,(int)DAT_08523398);
            DAT_0a3d8e78 = (undefined4)DAT_0854c0c0;
            DAT_0a3d8e7c = 0x7274;
            DAT_0a3d8e7e = 0;
            DAT_0a3d8e7f = 1;
          }
          local_2b8 = 0;
          uStack_2c0 = 0;
          local_2c8 = 0;
          uStack_2d0 = 0;
          local_2d8 = 0;
          uStack_2e0 = 0;
          local_2e8 = 0;
          uStack_2f0 = 0;
          local_2f8 = 0;
          uStack_300 = 0;
          local_308 = 0;
          uStack_310 = 0;
          uStack_318 = 0;
          uStack_320 = 0;
          uStack_328 = 0;
          local_330 = (undefined8 *******)0x0;
          FUN_05e1d31c(&local_730,&DAT_0a3d8e68,&local_330);
          thunk_FUN_05e1d0bc(&local_730);
          plVar8 = local_398;
        }
      }
      else {
        local_398 = *(long **)(lVar9 + 0x10);
        if (local_398 != (long *)0x0) {
          local_398[1] = local_398[1] + 1;
        }
        local_3a0 = pppppppuVar5;
        _memcpy(&local_730,&DAT_088ae860,0x350);
        FUN_00395584(&local_730,pppppppuVar5 + 0x1d);
        FUN_0466aca8(&local_760);
        FUN_01205740(&local_750,local_760);
        FUN_0268f370(&local_740,local_750);
        FUN_039ee5e4(&local_770,&local_730);
        FUN_00f57630(&local_330,local_770);
        local_b8 = (undefined8 *******)0x0;
        local_b0 = (undefined8 *******)0x0;
        local_a8 = (undefined8 *******)0x0;
        local_388 = &local_b8;
        local_380 = &DAT_aaaaaaaaaaaaaa00;
        local_b8 = (undefined8 *******)__Znwm(0x278);
        pppppppuVar5 = local_b8 + 0x4f;
        local_b0 = local_b8;
        local_a8 = pppppppuVar5;
        FUN_00f57630(local_b8,&local_330);
        local_b0 = pppppppuVar5;
        FUN_031ae0f0(local_740,auStack_6d8,&local_b8);
        pppppppuVar2 = local_b8;
        pppppppuVar5 = local_b0;
        if (local_b8 != (undefined8 *******)0x0) {
          while (pppppppuVar5 != pppppppuVar2) {
            pppppppuVar5 = pppppppuVar5 + -0x4f;
            (*(code *)**pppppppuVar5)(pppppppuVar5);
          }
          local_b0 = pppppppuVar2;
          __ZdlPvm(local_b8,(long)local_a8 - (long)local_b8);
        }
        FUN_00ac6290(&local_330);
        if (local_768 != (long *)0x0) {
          LOAcquire();
          lVar3 = local_768[1];
          local_768[1] = lVar3 + -1;
          LORelease();
          if (lVar3 == 0) {
            (**(code **)(*local_768 + 0x10))(local_768);
            __ZNSt3__119__shared_weak_count14__release_weakEv(local_768);
          }
        }
        if (local_738 != (long *)0x0) {
          LOAcquire();
          lVar3 = local_738[1];
          local_738[1] = lVar3 + -1;
          LORelease();
          if (lVar3 == 0) {
            (**(code **)(*local_738 + 0x10))(local_738);
            __ZNSt3__119__shared_weak_count14__release_weakEv(local_738);
          }
        }
        if (local_748 != (long *)0x0) {
          LOAcquire();
          lVar3 = local_748[1];
          local_748[1] = lVar3 + -1;
          LORelease();
          if (lVar3 == 0) {
            (**(code **)(*local_748 + 0x10))(local_748);
            __ZNSt3__119__shared_weak_count14__release_weakEv(local_748);
          }
        }
        if (local_758 != (long *)0x0) {
          LOAcquire();
          lVar3 = local_758[1];
          local_758[1] = lVar3 + -1;
          LORelease();
          if (lVar3 == 0) {
            (**(code **)(*local_758 + 0x10))(local_758);
            __ZNSt3__119__shared_weak_count14__release_weakEv(local_758);
          }
        }
        FUN_00396780(&local_730);
        plVar8 = local_398;
      }
      goto joined_r0x030d4ef0;
    }
  }
  else if (iVar4 == 4) {
    local_780 = *param_3;
    local_778 = (long *)param_3[1];
    if (local_778 != (long *)0x0) {
      local_778[1] = local_778[1] + 1;
    }
    (**(code **)(*param_2 + 0x80))(&local_730,param_2,&local_780);
    local_360 = local_730;
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              ((ulong)&local_360 | 8,local_728);
    plVar8 = plStack_338;
    if (local_708 != (long *)0x0) {
      local_708[1] = local_708[1] + 1;
    }
    local_340 = local_710;
    plStack_338 = local_708;
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
    if (local_708 != (long *)0x0) {
      LOAcquire();
      lVar3 = local_708[1];
      local_708[1] = lVar3 + -1;
      LORelease();
      if (lVar3 == 0) {
        (**(code **)(*local_708 + 0x10))(local_708);
        __ZNSt3__119__shared_weak_count14__release_weakEv(local_708);
      }
    }
    plVar8 = local_778;
    if (cStack_711 < '\0') {
      __ZdlPvm(local_728[0],CONCAT17(cStack_711,local_718) & 0x7fffffffffffffff);
      plVar8 = local_778;
    }
    goto joined_r0x030d47a4;
  }
LAB_030d50cc:
  uVar10 = *(undefined8 *)(*param_3 + 0x18);
  local_738 = *(long **)(*param_3 + 0x20);
  lVar3 = 0;
  if (local_738 != (long *)0x0) {
    lVar3 = local_738[1];
    local_738[1] = lVar3 + 1;
  }
  local_740 = uVar10;
  FUN_04cbf874(lVar3,uVar10);
  iVar4 = (**(code **)(*local_370 + 0x20))();
  if (iVar4 == 4) {
    iVar4 = thunk_FUN_05e1d97c(2);
    if (iVar4 != 0) {
      FUN_0488143c(&local_388);
      pppppppuVar5 = local_388;
      if (-1 < cStack_371) {
        pppppppuVar5 = &local_388;
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
      if ((DAT_0a3d8e39 & 1) == 0) {
        _DAT_0a3d8e24 = CONCAT44((int)DAT_087e2df0,(int)ram0x087e2de8);
        uRam000000000a3d8e2c = CONCAT44((int)DAT_0867c9b8,(int)DAT_0854dcf8);
        DAT_0a3d8e34 = (undefined4)DAT_084a66b0;
        DAT_0a3d8e38 = 0;
        DAT_0a3d8e39 = 1;
      }
      FUN_05e1d050(&local_730,2,pppppppuVar5,&DAT_0a3d8cf0,&DAT_0a3d8e24,0xc0,0,0);
      uVar10 = local_740;
      FUN_04cbe440(&local_3a0,local_740);
      local_b8 = local_3a0;
      if (-1 < cStack_389) {
        local_b8 = &local_3a0;
      }
      local_b0 = (undefined8 *******)((ulong)local_b0 & 0xffffffffffffff00);
      if ((DAT_0a3d8eb8 & 1) == 0) {
        uVar7 = 0;
        do {
          uVar11 = *(undefined4 *)((long)&DAT_088af2ba + uVar7);
          uVar1 = CONCAT12((char)((uint)uVar11 >> 8),(short)uVar11) & 0xff00ff;
          uVar12 = *(undefined4 *)((long)&DAT_088af2a6 + uVar7 % 0x14);
          *(uint *)((long)&DAT_0a3d8e80 + uVar7) =
               CONCAT13((char)((uint)uVar11 >> 0x18) + 0x8aU ^ (byte)((uint)uVar12 >> 0x18),
                        CONCAT12((char)((uint)uVar11 >> 0x10) + 0x8aU ^ (byte)((uint)uVar12 >> 0x10)
                                 ,CONCAT11((char)(uVar1 >> 0x10) + 0x8aU ^ (byte)((uint)uVar12 >> 8)
                                           ,(char)uVar1 + 0x8aU ^ (byte)uVar12)));
          uVar7 = uVar7 + 4;
        } while (uVar7 != 0x38);
        DAT_0a3d8eb8 = 1;
      }
      uStack_320 = 0;
      uStack_328 = 0;
      local_330 = &local_b8;
      uStack_310 = 0;
      uStack_318 = 0;
      uStack_300 = 0;
      local_308 = 0;
      uStack_2f0 = 0;
      local_2f8 = 0;
      uStack_2e0 = 0;
      local_2e8 = 0;
      uStack_2d0 = 0;
      local_2d8 = 0;
      uStack_2c0 = 0;
      local_2c8 = 0;
      local_2b8 = 0;
      FUN_05e1d31c(&local_730,&DAT_0a3d8e80,&local_330);
      if (cStack_389 < '\0') {
        __ZdlPvm(local_3a0,CONCAT17(cStack_389,local_390) & 0x7fffffffffffffff);
      }
      thunk_FUN_05e1d0bc(&local_730);
      if (cStack_371 < '\0') {
        __ZdlPvm(local_388,CONCAT17(cStack_371,local_378) & 0x7fffffffffffffff);
      }
    }
    FUN_030d05d0(param_2,0x800000000,uVar10);
  }
  else {
    FUN_030cfe58(param_2,uVar10);
  }
  plVar8 = local_738;
  uVar7 = (ulong)((uint)local_360 | local_360._4_4_);
  if (((uint)local_360 | local_360._4_4_) != 0) {
    plStack_788 = local_738;
    if (local_738 != (long *)0x0) {
      uVar7 = local_738[1];
      local_738[1] = uVar7 + 1;
    }
    local_790 = uVar10;
    FUN_030d5738(uVar7,param_2,&local_790);
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
  *param_1 = local_360;
  if ((long)puStack_348 < 0) {
    FUN_00018d20(param_1 + 1,puStack_358,local_350);
  }
  else {
    puVar6 = (undefined8 *)((ulong)&local_360 | 8);
    uVar10 = *puVar6;
    param_1[2] = puVar6[1];
    param_1[1] = uVar10;
    param_1[3] = puVar6[2];
  }
  plVar8 = local_738;
  param_1[4] = local_340;
  param_1[5] = plStack_338;
  if (plStack_338 != (long *)0x0) {
    plStack_338[1] = plStack_338[1] + 1;
  }
  if (local_738 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_738[1];
    local_738[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_738 + 0x10))(local_738);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    }
  }
LAB_030d540c:
  plVar8 = local_368;
  if (local_368 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_368[1];
    local_368[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_368 + 0x10))(local_368);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    }
  }
  plVar8 = plStack_338;
  if (plStack_338 != (long *)0x0) {
    LOAcquire();
    lVar3 = plStack_338[1];
    plStack_338[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*plStack_338 + 0x10))(plStack_338);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    }
  }
  if ((long)puStack_348 < 0) {
    __ZdlPvm(puStack_358,(ulong)puStack_348 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_68) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


