// Ghidra inferred pseudocode; requested=0x30d31f0
// entry=030d31f0 end=030d38ff

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_030d31f0(undefined8 *param_1,undefined8 param_2,long *param_3)

{
  long ****pppplVar1;
  long lVar2;
  long lVar3;
  int iVar4;
  long *plVar5;
  long *plVar6;
  long *plVar7;
  long lVar8;
  long *plVar9;
  long *local_200;
  long *local_1f8;
  undefined8 local_1f0;
  long *local_1e8;
  long *local_1e0;
  long *local_1d8;
  undefined1 *local_1d0;
  long *local_1c8;
  undefined8 local_1c0;
  undefined8 uStack_1b8;
  ulong local_1b0;
  long ***local_1a0;
  long *local_198;
  undefined7 local_190;
  char cStack_189;
  long *local_188;
  long *local_180;
  long local_f8;
  long *local_f0;
  long local_e8;
  long *local_e0;
  undefined **local_d8;
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
  lVar8 = *param_3;
  lVar3 = *(long *)(lVar8 + 0x18);
  local_e0 = *(long **)(lVar8 + 0x20);
  lVar2 = 0;
  if (local_e0 != (long *)0x0) {
    lVar2 = local_e0[1];
    local_e0[1] = lVar2 + 1;
    lVar8 = *param_3;
  }
  local_e8 = lVar3;
  if ((*(long *)(lVar8 + 8) == 0) ||
     (lVar2 = ___dynamic_cast(lVar2,*(long *)(lVar8 + 8),&PTR_DAT_09c37aa0,&PTR_DAT_09eb2580,0),
     lVar2 == 0)) {
    local_f8 = 0;
    local_f0 = (long *)0x0;
    iVar4 = thunk_FUN_05e1d97c(4);
    if (iVar4 != 0) {
      FUN_0488143c(&local_1a0);
      pppplVar1 = (long ****)local_1a0;
      if (-1 < cStack_189) {
        pppplVar1 = &local_1a0;
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
      if ((DAT_0a3d8f53 & 1) == 0) {
        _DAT_0a3d8f38 = CONCAT44((int)DAT_087e2df0,(int)ram0x087e2de8);
        uRam000000000a3d8f40 = CONCAT44((int)DAT_084a66b0,(int)DAT_08508320);
        DAT_0a3d8f48 = CONCAT44((int)DAT_084b0730,(int)DAT_08546648);
        DAT_0a3d8f50 = 0x6563;
        DAT_0a3d8f52 = 0;
        DAT_0a3d8f53 = 1;
      }
      FUN_05e1d050(&local_188,4,pppplVar1,&DAT_0a3d8cf0,&DAT_0a3d8f38,0x134,0,0);
      if ((DAT_0a3d8e23 & 1) == 0) {
        _DAT_0a3d8e0c = CONCAT44((int)DAT_084abe90,(int)DAT_084a8ea0);
        uRam000000000a3d8e14 = CONCAT44((int)DAT_08486ac8,(int)DAT_0856e3c0);
        DAT_0a3d8e1c = (undefined4)DAT_0854c0c0;
        DAT_0a3d8e20 = 0x7274;
        DAT_0a3d8e22 = 0;
        DAT_0a3d8e23 = 1;
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
      FUN_05e1d31c(&local_188,&DAT_0a3d8e0c,&local_d0);
      thunk_FUN_05e1d0bc(&local_188);
      if (cStack_189 < '\0') {
        __ZdlPvm(local_1a0,CONCAT17(cStack_189,local_190) & 0x7fffffffffffffff);
      }
    }
    FUN_030f6650(param_1,1,1,4,400);
    goto LAB_030d386c;
  }
  local_f0 = *(long **)(lVar8 + 0x10);
  lVar8 = 0;
  if (local_f0 != (long *)0x0) {
    lVar8 = local_f0[1];
    local_f0[1] = lVar8 + 1;
  }
  param_1[3] = &SUB_aaaaaaaaaaaaaaaa;
  param_1[2] = &SUB_aaaaaaaaaaaaaaaa;
  param_1[5] = &SUB_aaaaaaaaaaaaaaaa;
  param_1[4] = &SUB_aaaaaaaaaaaaaaaa;
  param_1[1] = &SUB_aaaaaaaaaaaaaaaa;
  *param_1 = &SUB_aaaaaaaaaaaaaaaa;
  local_f8 = lVar2;
  FUN_0304f1cc(lVar8,param_1,0,0);
  lVar8 = *(long *)(lVar3 + 0x230);
  plStack_c8 = *(long **)(lVar3 + 0x238);
  if (plStack_c8 != (long *)0x0) {
    plStack_c8[1] = plStack_c8[1] + 1;
  }
  local_d0 = lVar8;
  if (lVar8 != 0) {
    plVar5 = (long *)__Znwm(0x20);
    plVar7 = plVar5 + 1;
    *plVar7 = 0;
    plVar5[2] = 0;
    *plVar5 = (long)&PTR_FUN_09de65c8;
    local_1a0 = (long ***)(plVar5 + 3);
    *local_1a0 = (long **)0x0;
    iVar4 = 2;
    if (*(int *)(lVar2 + 0x7c) != 0) {
      iVar4 = *(int *)(lVar2 + 0x7c);
    }
    *(int *)local_1a0 = iVar4;
    if (plVar5 != (long *)0x0) {
      *plVar7 = *plVar7 + 1;
      *plVar7 = *plVar7 + 1;
    }
    plVar6 = *(long **)(lVar8 + 0x50);
    *(long ****)(lVar8 + 0x48) = local_1a0;
    *(long **)(lVar8 + 0x50) = plVar5;
    local_198 = plVar5;
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
      lVar3 = *plVar7;
      *plVar7 = lVar3 + -1;
      LORelease();
      if (lVar3 == 0) {
        (**(code **)(*plVar5 + 0x10))();
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
      }
    }
    lVar3 = local_f8;
    if (*(char *)(local_f8 + 399) < '\0') {
      if (*(long *)(local_f8 + 0x180) != 0) goto LAB_030d3548;
    }
    else if (*(char *)(local_f8 + 399) != '\0') {
LAB_030d3548:
      plVar5 = (long *)__Znwm(0x30);
      plVar6 = plVar5 + 1;
      *plVar6 = 0;
      plVar5[2] = 0;
      plVar7 = plVar5 + 3;
      *plVar7 = 0;
      *plVar5 = (long)&PTR_FUN_09de8b20;
      plVar5[4] = 0;
      plVar5[5] = 0;
      local_188 = plVar7;
      local_180 = plVar5;
      if (*(char *)(lVar3 + 399) < '\0') {
        FUN_00018d20(&local_1c0,*(undefined8 *)(lVar3 + 0x178),*(undefined8 *)(lVar3 + 0x180));
      }
      else {
        uStack_1b8 = *(undefined8 *)(lVar3 + 0x180);
        local_1c0 = *(undefined8 *)(lVar3 + 0x178);
        local_1b0 = *(ulong *)(lVar3 + 0x188);
      }
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(plVar7,&local_1c0);
      if ((long)local_1b0 < 0) {
        __ZdlPvm(local_1c0,local_1b0 & 0x7fffffffffffffff);
      }
      if (plVar5 != (long *)0x0) {
        *plVar6 = *plVar6 + 1;
        *plVar6 = *plVar6 + 1;
      }
      plVar9 = *(long **)(local_d0 + 0x60);
      *(long **)(local_d0 + 0x58) = plVar7;
      *(long **)(local_d0 + 0x60) = plVar5;
      if (plVar9 != (long *)0x0) {
        LOAcquire();
        lVar3 = plVar9[1];
        plVar9[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*plVar9 + 0x10))(plVar9);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar9);
        }
      }
      if (plVar5 != (long *)0x0) {
        LOAcquire();
        lVar3 = *plVar6;
        *plVar6 = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*plVar5 + 0x10))(plVar5);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
        }
      }
      plVar5 = local_180;
      if (local_180 != (long *)0x0) {
        LOAcquire();
        lVar3 = local_180[1];
        local_180[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*local_180 + 0x10))(local_180);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
        }
      }
    }
    iVar4 = FUN_04bb368c(local_e8 + 0x30);
    if (iVar4 != 0) {
      local_1d0 = &SUB_aaaaaaaaaaaaaaaa;
      local_1c8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
      plVar5 = (long *)FUN_04669774();
      (**(code **)(*plVar5 + 0x68))(&local_200);
      (**(code **)(*local_200 + 0x38))(&local_1f0);
      local_d8 = &PTR_FUN_09c567e0;
      local_188 = (long *)&SUB_aaaaaaaaaaaaaaaa;
      local_180 = (long *)&SUB_aaaaaaaaaaaaaaaa;
      FUN_044e6b1c(&local_188,local_1f0,&local_d8);
      plVar5 = local_180;
      local_1e0 = local_188;
      local_1d8 = local_180;
      if ((local_180 != (long *)0x0) && (local_180[1] = local_180[1] + 1, local_180 != (long *)0x0))
      {
        LOAcquire();
        lVar3 = local_180[1];
        local_180[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*local_180 + 0x10))(local_180);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
        }
      }
      FUN_044fb300(&local_1d0,local_1e0,local_e8 + 0x30);
      plVar5 = local_1d8;
      if (local_1d8 != (long *)0x0) {
        LOAcquire();
        lVar3 = local_1d8[1];
        local_1d8[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*local_1d8 + 0x10))(local_1d8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
        }
      }
      if (local_1e8 != (long *)0x0) {
        LOAcquire();
        lVar3 = local_1e8[1];
        local_1e8[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*local_1e8 + 0x10))(local_1e8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_1e8);
        }
      }
      if (local_1f8 != (long *)0x0) {
        LOAcquire();
        lVar3 = local_1f8[1];
        local_1f8[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*local_1f8 + 0x10))(local_1f8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_1f8);
        }
      }
      plVar5 = local_1c8;
      if ((local_1d0 == (undefined1 *)0x0) || ((local_1d0[0x54] & 1) == 0)) {
        *(uint *)(local_d0 + 0xc0) = *(uint *)(local_d0 + 0xc0) | 1;
      }
      if (local_1c8 != (long *)0x0) {
        LOAcquire();
        lVar3 = local_1c8[1];
        local_1c8[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*local_1c8 + 0x10))(local_1c8);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
        }
      }
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
LAB_030d386c:
  plVar5 = local_f0;
  if (local_f0 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_f0[1];
    local_f0[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_f0 + 0x10))(local_f0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
    }
  }
  plVar5 = local_e0;
  if (local_e0 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_e0[1];
    local_e0[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_e0 + 0x10))(local_e0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


