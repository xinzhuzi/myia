// Ghidra inferred pseudocode; requested=0x30d28a4
// entry=030d28a4 end=030d30f3

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_030d28a4(undefined8 *param_1,long *param_2,long *param_3)

{
  undefined8 *******pppppppuVar1;
  long lVar2;
  int iVar3;
  undefined8 uVar4;
  long *plVar5;
  long local_288;
  long *local_280;
  long local_278;
  long *local_270;
  long local_268;
  long *local_260;
  undefined1 auStack_258 [8];
  undefined8 local_250;
  undefined7 local_240;
  char cStack_239;
  long *local_230;
  long local_228;
  long *local_220;
  long local_218;
  long *local_210;
  undefined1 auStack_208 [8];
  undefined8 local_200;
  undefined7 local_1f0;
  char cStack_1e9;
  long *local_1e0;
  long local_1d8;
  long *local_1d0;
  long local_1c8;
  long *local_1c0;
  undefined1 auStack_1b8 [8];
  undefined8 local_1b0;
  undefined7 local_1a0;
  char cStack_199;
  long *local_190;
  undefined8 *******local_188 [2];
  undefined7 local_178;
  char cStack_171;
  undefined8 local_170;
  undefined8 local_168 [2];
  undefined7 local_158;
  char cStack_151;
  undefined8 local_150;
  long *local_148;
  long *local_e0;
  long *local_d8;
  undefined8 local_d0;
  undefined8 uStack_c8;
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
  plVar5 = *(long **)(*param_3 + 8);
  if (plVar5 == (long *)0x0) {
    local_e0 = (long *)0x0;
    local_d8 = (long *)0x0;
    iVar3 = thunk_FUN_05e1d97c(4);
    if (iVar3 != 0) {
      FUN_0488143c(local_188);
      pppppppuVar1 = local_188[0];
      if (-1 < cStack_171) {
        pppppppuVar1 = local_188;
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
      if ((DAT_0a3d8e08 & 1) == 0) {
        _DAT_0a3d8df0 = CONCAT44((int)DAT_087e2df0,(int)ram0x087e2de8);
        uRam000000000a3d8df8 = CONCAT44((int)DAT_084b0670,(int)ram0x084f0820);
        DAT_0a3d8e00 = CONCAT44((int)DAT_088a3be8,(int)DAT_0850ad18);
        DAT_0a3d8e08 = 1;
      }
      FUN_05e1d050(&local_170,4,pppppppuVar1,&DAT_0a3d8cf0,&DAT_0a3d8df0,0x6d,0,0);
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
      uStack_c8 = 0;
      local_d0 = 0;
      uStack_b8 = 0;
      uStack_c0 = 0;
      FUN_05e1d31c(&local_170,&DAT_0a3d8e0c,&local_d0);
      thunk_FUN_05e1d0bc(&local_170);
      if (cStack_171 < '\0') {
        __ZdlPvm(local_188[0],CONCAT17(cStack_171,local_178) & 0x7fffffffffffffff);
      }
    }
    FUN_030f6650(param_1,1,1,4,400);
  }
  else {
    local_d8 = *(long **)(*param_3 + 0x10);
    lVar2 = 0;
    if (local_d8 != (long *)0x0) {
      lVar2 = local_d8[1];
      local_d8[1] = lVar2 + 1;
    }
    param_1[3] = &SUB_aaaaaaaaaaaaaaaa;
    param_1[2] = &SUB_aaaaaaaaaaaaaaaa;
    param_1[5] = &SUB_aaaaaaaaaaaaaaaa;
    param_1[4] = &SUB_aaaaaaaaaaaaaaaa;
    param_1[1] = &SUB_aaaaaaaaaaaaaaaa;
    *param_1 = &SUB_aaaaaaaaaaaaaaaa;
    local_e0 = plVar5;
    FUN_0304f1cc(lVar2,param_1,0,0);
    uVar4 = (**(code **)(*plVar5 + 0x20))(plVar5);
    iVar3 = (int)uVar4;
    if (iVar3 < 3) {
      if (iVar3 == 1) {
        local_1c8 = *param_3;
        local_1c0 = (long *)param_3[1];
        if (local_1c0 != (long *)0x0) {
          local_1c0[1] = local_1c0[1] + 1;
        }
        FUN_030d31f0(auStack_1b8,uVar4,&local_1c8);
        if (local_190 != (long *)0x0) {
          LOAcquire();
          lVar2 = local_190[1];
          local_190[1] = lVar2 + -1;
          LORelease();
          if (lVar2 == 0) {
            (**(code **)(*local_190 + 0x10))(local_190);
            __ZNSt3__119__shared_weak_count14__release_weakEv(local_190);
          }
        }
        if (cStack_199 < '\0') {
          __ZdlPvm(local_1b0,CONCAT17(cStack_199,local_1a0) & 0x7fffffffffffffff);
        }
        plVar5 = local_1c0;
        if (local_1c0 != (long *)0x0) {
          LOAcquire();
          lVar2 = local_1c0[1];
          local_1c0[1] = lVar2 + -1;
          LORelease();
          if (lVar2 == 0) {
            (**(code **)(*local_1c0 + 0x10))(local_1c0);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
          }
        }
        local_1d8 = *param_3;
        local_1d0 = (long *)param_3[1];
        if (local_1d0 != (long *)0x0) {
          local_1d0[1] = local_1d0[1] + 1;
        }
        (**(code **)(*param_2 + 0x78))(&local_170,param_2,&local_1d8);
        *param_1 = local_170;
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (param_1 + 1,local_168);
        if (local_148 != (long *)0x0) {
          local_148[1] = local_148[1] + 1;
        }
        plVar5 = (long *)param_1[5];
        param_1[4] = local_150;
        param_1[5] = local_148;
        if (plVar5 != (long *)0x0) {
          LOAcquire();
          lVar2 = plVar5[1];
          plVar5[1] = lVar2 + -1;
          LORelease();
          if (lVar2 == 0) {
            (**(code **)(*plVar5 + 0x10))(plVar5);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
          }
        }
        if (local_148 != (long *)0x0) {
          LOAcquire();
          lVar2 = local_148[1];
          local_148[1] = lVar2 + -1;
          LORelease();
          if (lVar2 == 0) {
            (**(code **)(*local_148 + 0x10))(local_148);
            __ZNSt3__119__shared_weak_count14__release_weakEv(local_148);
          }
        }
        plVar5 = local_1d0;
        if (cStack_151 < '\0') {
          __ZdlPvm(local_168[0],CONCAT17(cStack_151,local_158) & 0x7fffffffffffffff);
          plVar5 = local_1d0;
        }
      }
      else {
        if (iVar3 != 2) goto LAB_030d3090;
        local_218 = *param_3;
        local_210 = (long *)param_3[1];
        if (local_210 != (long *)0x0) {
          local_210[1] = local_210[1] + 1;
        }
        FUN_030d39d8(auStack_208,uVar4,&local_218);
        if (local_1e0 != (long *)0x0) {
          LOAcquire();
          lVar2 = local_1e0[1];
          local_1e0[1] = lVar2 + -1;
          LORelease();
          if (lVar2 == 0) {
            (**(code **)(*local_1e0 + 0x10))(local_1e0);
            __ZNSt3__119__shared_weak_count14__release_weakEv(local_1e0);
          }
        }
        if (cStack_1e9 < '\0') {
          __ZdlPvm(local_200,CONCAT17(cStack_1e9,local_1f0) & 0x7fffffffffffffff);
        }
        plVar5 = local_210;
        if (local_210 != (long *)0x0) {
          LOAcquire();
          lVar2 = local_210[1];
          local_210[1] = lVar2 + -1;
          LORelease();
          if (lVar2 == 0) {
            (**(code **)(*local_210 + 0x10))(local_210);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
          }
        }
        local_228 = *param_3;
        local_220 = (long *)param_3[1];
        if (local_220 != (long *)0x0) {
          local_220[1] = local_220[1] + 1;
        }
        (**(code **)(*param_2 + 0x98))(&local_170,param_2,&local_228);
        *param_1 = local_170;
        __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                  (param_1 + 1,local_168);
        if (local_148 != (long *)0x0) {
          local_148[1] = local_148[1] + 1;
        }
        plVar5 = (long *)param_1[5];
        param_1[4] = local_150;
        param_1[5] = local_148;
        if (plVar5 != (long *)0x0) {
          LOAcquire();
          lVar2 = plVar5[1];
          plVar5[1] = lVar2 + -1;
          LORelease();
          if (lVar2 == 0) {
            (**(code **)(*plVar5 + 0x10))(plVar5);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
          }
        }
        if (local_148 != (long *)0x0) {
          LOAcquire();
          lVar2 = local_148[1];
          local_148[1] = lVar2 + -1;
          LORelease();
          if (lVar2 == 0) {
            (**(code **)(*local_148 + 0x10))(local_148);
            __ZNSt3__119__shared_weak_count14__release_weakEv(local_148);
          }
        }
        plVar5 = local_220;
        if (cStack_151 < '\0') {
          __ZdlPvm(local_168[0],CONCAT17(cStack_151,local_158) & 0x7fffffffffffffff);
          plVar5 = local_220;
        }
      }
    }
    else if (iVar3 == 3) {
      local_268 = *param_3;
      local_260 = (long *)param_3[1];
      if (local_260 != (long *)0x0) {
        local_260[1] = local_260[1] + 1;
      }
      FUN_030d39d8(auStack_258,uVar4,&local_268);
      if (local_230 != (long *)0x0) {
        LOAcquire();
        lVar2 = local_230[1];
        local_230[1] = lVar2 + -1;
        LORelease();
        if (lVar2 == 0) {
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
        lVar2 = local_260[1];
        local_260[1] = lVar2 + -1;
        LORelease();
        if (lVar2 == 0) {
          (**(code **)(*local_260 + 0x10))(local_260);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
        }
      }
      local_278 = *param_3;
      local_270 = (long *)param_3[1];
      if (local_270 != (long *)0x0) {
        local_270[1] = local_270[1] + 1;
      }
      (**(code **)(*param_2 + 0xb0))(&local_170,param_2,&local_278);
      *param_1 = local_170;
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (param_1 + 1,local_168);
      if (local_148 != (long *)0x0) {
        local_148[1] = local_148[1] + 1;
      }
      plVar5 = (long *)param_1[5];
      param_1[4] = local_150;
      param_1[5] = local_148;
      if (plVar5 != (long *)0x0) {
        LOAcquire();
        lVar2 = plVar5[1];
        plVar5[1] = lVar2 + -1;
        LORelease();
        if (lVar2 == 0) {
          (**(code **)(*plVar5 + 0x10))(plVar5);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
        }
      }
      if (local_148 != (long *)0x0) {
        LOAcquire();
        lVar2 = local_148[1];
        local_148[1] = lVar2 + -1;
        LORelease();
        if (lVar2 == 0) {
          (**(code **)(*local_148 + 0x10))(local_148);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_148);
        }
      }
      plVar5 = local_270;
      if (cStack_151 < '\0') {
        __ZdlPvm(local_168[0],CONCAT17(cStack_151,local_158) & 0x7fffffffffffffff);
        plVar5 = local_270;
      }
    }
    else {
      if (iVar3 != 4) goto LAB_030d3090;
      local_288 = *param_3;
      local_280 = (long *)param_3[1];
      if (local_280 != (long *)0x0) {
        local_280[1] = local_280[1] + 1;
      }
      (**(code **)(*param_2 + 0xb8))(&local_170,param_2,&local_288);
      *param_1 = local_170;
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (param_1 + 1,local_168);
      if (local_148 != (long *)0x0) {
        local_148[1] = local_148[1] + 1;
      }
      plVar5 = (long *)param_1[5];
      param_1[4] = local_150;
      param_1[5] = local_148;
      if (plVar5 != (long *)0x0) {
        LOAcquire();
        lVar2 = plVar5[1];
        plVar5[1] = lVar2 + -1;
        LORelease();
        if (lVar2 == 0) {
          (**(code **)(*plVar5 + 0x10))(plVar5);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
        }
      }
      if (local_148 != (long *)0x0) {
        LOAcquire();
        lVar2 = local_148[1];
        local_148[1] = lVar2 + -1;
        LORelease();
        if (lVar2 == 0) {
          (**(code **)(*local_148 + 0x10))(local_148);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_148);
        }
      }
      plVar5 = local_280;
      if (cStack_151 < '\0') {
        __ZdlPvm(local_168[0],CONCAT17(cStack_151,local_158) & 0x7fffffffffffffff);
        plVar5 = local_280;
      }
    }
    if (plVar5 != (long *)0x0) {
      LOAcquire();
      lVar2 = plVar5[1];
      plVar5[1] = lVar2 + -1;
      LORelease();
      if (lVar2 == 0) {
        (**(code **)(*plVar5 + 0x10))(plVar5);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
      }
    }
  }
LAB_030d3090:
  plVar5 = local_d8;
  if (local_d8 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_d8[1];
    local_d8[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_d8 + 0x10))(local_d8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


