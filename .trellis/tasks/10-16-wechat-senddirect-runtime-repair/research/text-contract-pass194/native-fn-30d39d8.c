// Ghidra inferred pseudocode; requested=0x30d39d8
// entry=030d39d8 end=030d424f

/* WARNING: Removing unreachable block (ram,0x030d3cf8) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_030d39d8(undefined8 *param_1,undefined8 param_2,long *param_3)

{
  undefined8 *puVar1;
  long lVar2;
  long lVar3;
  int iVar4;
  long *plVar5;
  long *plVar6;
  long ****pppplVar7;
  long *plVar8;
  long lVar9;
  undefined8 local_530;
  undefined8 uStack_528;
  ulong local_520;
  long ***local_518;
  long *local_510;
  undefined7 local_508;
  char cStack_501;
  long *local_500;
  long *local_4f8;
  undefined1 auStack_4f0 [144];
  long local_460;
  long local_2c8;
  long *local_2c0;
  long local_1a0;
  long *local_198;
  long local_190;
  long *local_188;
  long local_180;
  long *local_178;
  long local_170;
  long *local_168;
  long local_160;
  long *plStack_158;
  undefined8 uStack_150;
  undefined8 uStack_148;
  undefined8 local_140;
  undefined8 uStack_138;
  undefined8 uStack_130;
  undefined8 uStack_128;
  undefined8 local_120;
  undefined8 uStack_118;
  undefined8 local_110;
  undefined8 uStack_108;
  undefined8 local_100;
  undefined8 uStack_f8;
  undefined8 local_f0;
  undefined8 uStack_e8;
  undefined8 *local_d0;
  long *plStack_c8;
  undefined8 local_c0;
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
  lVar9 = *param_3;
  lVar3 = *(long *)(lVar9 + 0x18);
  local_168 = *(long **)(lVar9 + 0x20);
  lVar2 = 0;
  if (local_168 != (long *)0x0) {
    lVar2 = local_168[1];
    local_168[1] = lVar2 + 1;
    lVar9 = *param_3;
  }
  local_170 = lVar3;
  if ((*(long *)(lVar9 + 8) == 0) ||
     (local_180 = ___dynamic_cast(lVar2,*(long *)(lVar9 + 8),&PTR_DAT_09c37aa0,&PTR_DAT_09c3edd0,0),
     local_180 == 0)) {
    local_178 = (long *)0x0;
    local_180 = 0;
  }
  else {
    local_178 = *(long **)(lVar9 + 0x10);
    if (local_178 != (long *)0x0) {
      local_178[1] = local_178[1] + 1;
      lVar9 = *param_3;
    }
  }
  lVar2 = local_180;
  local_190 = *(long *)(lVar9 + 0x28);
  local_188 = *(long **)(lVar9 + 0x30);
  if (local_188 != (long *)0x0) {
    local_188[1] = local_188[1] + 1;
  }
  *(undefined4 *)(local_190 + 0x84) = 3;
  if (local_180 == 0) {
    iVar4 = thunk_FUN_05e1d97c(4);
    if (iVar4 != 0) {
      FUN_0488143c(&local_d0);
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
      if ((DAT_0a3d8ef6 & 1) == 0) {
        _DAT_0a3d8ed8 = CONCAT44((int)DAT_087e2df0,(int)ram0x087e2de8);
        uRam000000000a3d8ee0 = CONCAT44((int)DAT_084a66b0,(int)DAT_08508320);
        DAT_0a3d8ee8 = CONCAT44((int)DAT_0860c3a0,(int)DAT_08503670);
        DAT_0a3d8ef0 = (undefined4)ram0x084e31f0;
        DAT_0a3d8ef4 = 0x65;
        DAT_0a3d8ef6 = 1;
      }
      FUN_05e1d050(auStack_4f0,4,&local_d0,&DAT_0a3d8cf0,&DAT_0a3d8ed8,0x108,0,0);
      if ((DAT_0a3d8f12 & 1) == 0) {
        _DAT_0a3d8ef8 = CONCAT44((int)DAT_084958d8,(int)ram0x0857f178);
        uRam000000000a3d8f00 = CONCAT44((int)DAT_08548d20,(int)DAT_08523398);
        DAT_0a3d8f08 = CONCAT44((int)ram0x084f1748,(int)DAT_084cd458);
        DAT_0a3d8f10 = 0x72;
        DAT_0a3d8f12 = 1;
      }
      uStack_e8 = 0;
      local_f0 = 0;
      uStack_f8 = 0;
      local_100 = 0;
      uStack_108 = 0;
      local_110 = 0;
      uStack_118 = 0;
      local_120 = 0;
      uStack_138 = 0;
      local_140 = 0;
      uStack_128 = 0;
      uStack_130 = 0;
      plStack_158 = (long *)0x0;
      local_160 = 0;
      uStack_148 = 0;
      uStack_150 = 0;
      FUN_05e1d31c(auStack_4f0,&DAT_0a3d8ef8,&local_160);
      thunk_FUN_05e1d0bc(auStack_4f0);
    }
    FUN_030f6650(param_1,1,1,4,400);
  }
  else {
    param_1[3] = &SUB_aaaaaaaaaaaaaaaa;
    param_1[2] = &SUB_aaaaaaaaaaaaaaaa;
    param_1[5] = &SUB_aaaaaaaaaaaaaaaa;
    param_1[4] = &SUB_aaaaaaaaaaaaaaaa;
    param_1[1] = &SUB_aaaaaaaaaaaaaaaa;
    *param_1 = &SUB_aaaaaaaaaaaaaaaa;
    FUN_0304f1cc(param_1,0,0);
    local_1a0 = *(long *)(lVar3 + 0x230);
    local_198 = *(long **)(lVar3 + 0x238);
    if (local_198 != (long *)0x0) {
      local_198[1] = local_198[1] + 1;
    }
    if (local_1a0 != 0) {
      _memcpy(auStack_4f0,&DAT_088ae860,0x350);
      FUN_00395584(auStack_4f0,lVar2 + 0xe8);
      plVar5 = (long *)__Znwm(0x20);
      plVar5[1] = 0;
      plVar5[2] = 0;
      *plVar5 = (long)&PTR_FUN_09de65c8;
      plVar8 = plVar5 + 3;
      *plVar8 = 0;
      iVar4 = *(int *)(local_180 + 0x7c);
      local_500 = plVar8;
      local_4f8 = plVar5;
      if (iVar4 == 0) {
        if (local_460 == 0) {
          iVar4 = thunk_FUN_05e1d97c(4);
          if (iVar4 != 0) {
            FUN_0488143c(&local_518);
            pppplVar7 = (long ****)local_518;
            if (-1 < cStack_501) {
              pppplVar7 = &local_518;
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
            if ((DAT_0a3d8ef6 & 1) == 0) {
              _DAT_0a3d8ed8 = CONCAT44((int)DAT_087e2df0,(int)ram0x087e2de8);
              uRam000000000a3d8ee0 = CONCAT44((int)DAT_084a66b0,(int)DAT_08508320);
              DAT_0a3d8ee8 = CONCAT44((int)DAT_0860c3a0,(int)DAT_08503670);
              DAT_0a3d8ef0 = (undefined4)ram0x084e31f0;
              DAT_0a3d8ef4 = 0x65;
              DAT_0a3d8ef6 = 1;
            }
            FUN_05e1d050(&local_160,4,pppplVar7,&DAT_0a3d8cf0,&DAT_0a3d8ed8,0x11b,0,0);
            if ((DAT_0a3d8f34 & 1) == 0) {
              _DAT_0a3d8f14 = CONCAT44((int)DAT_084874d0,(int)DAT_08507720);
              uRam000000000a3d8f1c = CONCAT44((int)DAT_088ae230,(int)DAT_084a8100);
              _DAT_0a3d8f24 = CONCAT44((int)DAT_084b0268,(int)DAT_08547c20);
              uRam000000000a3d8f2c = CONCAT44((int)DAT_084811b0,(int)DAT_0878afd0);
              DAT_0a3d8f34 = 1;
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
            local_d0 = (undefined8 *)0x0;
            uStack_b8 = 0;
            local_c0 = 0;
            FUN_05e1d31c(&local_160,&DAT_0a3d8f14,&local_d0);
            thunk_FUN_05e1d0bc(&local_160);
            plVar5 = local_4f8;
            plVar8 = local_500;
            if (cStack_501 < '\0') {
              __ZdlPvm(local_518,CONCAT17(cStack_501,local_508) & 0x7fffffffffffffff);
              plVar5 = local_4f8;
              plVar8 = local_500;
            }
          }
          iVar4 = 1;
        }
        else {
          iVar4 = 2;
        }
      }
      *(int *)plVar8 = iVar4;
      if (plVar5 != (long *)0x0) {
        plVar6 = plVar5 + 1;
        *plVar6 = *plVar6 + 1;
        *plVar6 = *plVar6 + 1;
      }
      plVar6 = *(long **)(local_1a0 + 0x50);
      *(long **)(local_1a0 + 0x48) = plVar8;
      *(long **)(local_1a0 + 0x50) = plVar5;
      if (plVar6 != (long *)0x0) {
        LOAcquire();
        lVar3 = plVar6[1];
        plVar6[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*plVar6 + 0x10))(plVar6);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
        }
      }
      if (plVar5 != (long *)0x0) {
        LOAcquire();
        lVar3 = plVar5[1];
        plVar5[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*plVar5 + 0x10))(plVar5);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
        }
      }
      local_160 = local_2c8;
      plStack_158 = local_2c0;
      if (local_2c0 != (long *)0x0) {
        local_2c0[1] = local_2c0[1] + 1;
      }
      if (local_2c8 != 0) {
        puVar1 = *(undefined8 **)(local_2c8 + 0x58);
        plStack_c8 = *(long **)(local_2c8 + 0x60);
        if (plStack_c8 != (long *)0x0) {
          local_2c8 = plStack_c8[1];
          plStack_c8[1] = local_2c8 + 1;
        }
        local_d0 = puVar1;
        if (puVar1 != (undefined8 *)0x0) {
          plVar5 = (long *)__Znwm(local_2c8,0x30);
          plVar8 = plVar5 + 1;
          *plVar8 = 0;
          plVar5[2] = 0;
          pppplVar7 = (long ****)(plVar5 + 3);
          *pppplVar7 = (long ***)0x0;
          *plVar5 = (long)&PTR_FUN_09de8b20;
          plVar5[4] = 0;
          plVar5[5] = 0;
          local_518 = (long ***)pppplVar7;
          local_510 = plVar5;
          if (*(char *)((long)puVar1 + 0x17) < '\0') {
            FUN_00018d20(&local_530,*puVar1,puVar1[1]);
          }
          else {
            uStack_528 = puVar1[1];
            local_530 = *puVar1;
            local_520 = puVar1[2];
          }
          __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                    (pppplVar7,&local_530);
          if ((long)local_520 < 0) {
            __ZdlPvm(local_530,local_520 & 0x7fffffffffffffff);
          }
          if (plVar5 != (long *)0x0) {
            *plVar8 = *plVar8 + 1;
            *plVar8 = *plVar8 + 1;
          }
          plVar6 = *(long **)(local_1a0 + 0x60);
          *(long *****)(local_1a0 + 0x58) = pppplVar7;
          *(long **)(local_1a0 + 0x60) = plVar5;
          if (plVar6 != (long *)0x0) {
            LOAcquire();
            lVar3 = plVar6[1];
            plVar6[1] = lVar3 + -1;
            LORelease();
            if (lVar3 == 0) {
              (**(code **)(*plVar6 + 0x10))(plVar6);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
            }
          }
          if (plVar5 != (long *)0x0) {
            LOAcquire();
            lVar3 = *plVar8;
            *plVar8 = lVar3 + -1;
            LORelease();
            if (lVar3 == 0) {
              (**(code **)(*plVar5 + 0x10))(plVar5);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
            }
          }
          plVar5 = local_510;
          if (local_510 != (long *)0x0) {
            LOAcquire();
            lVar3 = local_510[1];
            local_510[1] = lVar3 + -1;
            LORelease();
            if (lVar3 == 0) {
              (**(code **)(*local_510 + 0x10))(local_510);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
            }
          }
        }
        plVar5 = plStack_c8;
        if (plStack_c8 != (long *)0x0) {
          LOAcquire();
          lVar3 = plStack_c8[1];
          plStack_c8[1] = lVar3 + -1;
          LORelease();
          if (lVar3 == 0) {
            (**(code **)(*plStack_c8 + 0x10))(plStack_c8);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
          }
        }
      }
      plVar5 = plStack_158;
      if (plStack_158 != (long *)0x0) {
        LOAcquire();
        lVar3 = plStack_158[1];
        plStack_158[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*plStack_158 + 0x10))(plStack_158);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
        }
      }
      plVar5 = local_4f8;
      if (local_4f8 != (long *)0x0) {
        LOAcquire();
        lVar3 = local_4f8[1];
        local_4f8[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*local_4f8 + 0x10))(local_4f8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
        }
      }
      FUN_00396780(auStack_4f0);
    }
    plVar5 = local_198;
    if (local_198 != (long *)0x0) {
      LOAcquire();
      lVar3 = local_198[1];
      local_198[1] = lVar3 + -1;
      LORelease();
      if (lVar3 == 0) {
        (**(code **)(*local_198 + 0x10))(local_198);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
      }
    }
  }
  plVar5 = local_188;
  if (local_188 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_188[1];
    local_188[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_188 + 0x10))(local_188);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
    }
  }
  plVar5 = local_178;
  if (local_178 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_178[1];
    local_178[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_178 + 0x10))(local_178);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
    }
  }
  plVar5 = local_168;
  if (local_168 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_168[1];
    local_168[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_168 + 0x10))(local_168);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


