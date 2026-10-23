// Ghidra inferred pseudocode; requested=0x30db798
// entry=030db798 end=030dc0d3

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_030db798(undefined8 *param_1,long param_2,long *param_3)

{
  undefined8 *******pppppppuVar1;
  long *plVar2;
  long lVar3;
  int iVar4;
  long *plVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  undefined8 *puVar8;
  undefined8 *******local_428 [2];
  undefined7 local_418;
  char cStack_411;
  undefined8 *******local_410 [2];
  undefined7 local_400;
  char cStack_3f9;
  undefined1 auStack_3f8 [632];
  long local_180;
  long *local_178;
  undefined1 *local_170;
  long *local_168;
  undefined1 *local_160;
  undefined1 *puStack_158;
  undefined1 *local_150;
  undefined1 *puStack_148;
  undefined1 *local_140;
  long *local_138;
  undefined8 *******local_130;
  undefined1 local_128;
  undefined7 local_120;
  char cStack_119;
  undefined8 *******local_e0;
  long *plStack_d8;
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
  undefined8 uStack_80;
  undefined8 local_78;
  undefined8 uStack_70;
  undefined8 local_68;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  puStack_148 = &SUB_aaaaaaaaaaaaaaaa;
  local_150 = &SUB_aaaaaaaaaaaaaaaa;
  local_138 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_140 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_158 = &SUB_aaaaaaaaaaaaaaaa;
  local_160 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0304f1cc(&local_160,0,0);
  local_170 = &SUB_aaaaaaaaaaaaaaaa;
  if ((*(long *)(param_2 + 0x368) != 0) &&
     (local_168 = (long *)__ZNSt3__119__shared_weak_count4lockEv(), local_168 != (long *)0x0)) {
    local_170 = *(undefined1 **)(param_2 + 0x360);
    if (local_170 != (undefined1 *)0x0) {
      local_180 = *(long *)(*param_3 + 0x18);
      local_178 = *(long **)(*param_3 + 0x20);
      lVar3 = 0;
      if (local_178 != (long *)0x0) {
        lVar3 = local_178[1];
        local_178[1] = lVar3 + 1;
      }
      if (local_180 == 0) {
        iVar4 = thunk_FUN_05e1d97c(lVar3,4);
        if (iVar4 != 0) {
          FUN_0488143c(&local_130);
          pppppppuVar1 = local_130;
          if (-1 < cStack_119) {
            pppppppuVar1 = &local_130;
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
          if ((DAT_0a3d93f1 & 1) == 0) {
            _DAT_0a3d93dc = CONCAT44((int)DAT_087e3028,(int)DAT_087ef190);
            uRam000000000a3d93e4 = CONCAT44((int)DAT_084a66b0,(int)DAT_085095c0);
            DAT_0a3d93ec = (undefined4)DAT_08833a40;
            DAT_0a3d93f0 = 0;
            DAT_0a3d93f1 = 1;
          }
          FUN_05e1d050(auStack_3f8,4,pppppppuVar1,&DAT_0a3d8cf0,&DAT_0a3d93dc,0x290,0,0);
          if ((DAT_0a3d9417 & 1) == 0) {
            _DAT_0a3d93f4 = CONCAT44((int)DAT_08486a50,(int)DAT_08486a48);
            uRam000000000a3d93fc = CONCAT44((int)DAT_0854c0c0,(int)DAT_08486ac8);
            _DAT_0a3d9404 = CONCAT44((int)DAT_08531ed8,(int)DAT_088ae318);
            uRam000000000a3d940c = CONCAT44((int)DAT_084c7cb8,(int)DAT_0853ae20);
            DAT_0a3d9414 = 0x6264;
            DAT_0a3d9416 = 0;
            DAT_0a3d9417 = 1;
          }
          local_78 = 0;
          uStack_80 = 0;
          local_68 = 0;
          uStack_70 = 0;
          local_98 = 0;
          uStack_a0 = 0;
          local_88 = 0;
          uStack_90 = 0;
          local_b8 = 0;
          uStack_c0 = 0;
          local_a8 = 0;
          uStack_b0 = 0;
          plStack_d8 = (long *)0x0;
          local_e0 = (undefined8 *******)0x0;
          local_c8 = 0;
          uStack_d0 = 0;
          FUN_05e1d31c(auStack_3f8,&DAT_0a3d93f4,&local_e0);
          thunk_FUN_05e1d0bc(auStack_3f8);
          if (cStack_119 < '\0') {
            __ZdlPvm(local_130,CONCAT17(cStack_119,local_120) & 0x7fffffffffffffff);
          }
        }
        uVar7 = 400;
        uVar6 = 4;
      }
      else {
        FUN_032cf5ac(&local_e0,local_170);
        FUN_030dc1e0(auStack_3f8,&local_130,&local_e0);
        plVar5 = (long *)__Znwm(0x290);
        plVar5[1] = 0;
        plVar5[2] = 0;
        *plVar5 = (long)&PTR_FUN_09c92390;
        local_180 = FUN_02a0cf30(plVar5 + 3,auStack_3f8);
        plVar2 = local_178;
        if (local_178 != (long *)0x0) {
          LOAcquire();
          lVar3 = local_178[1];
          local_178[1] = lVar3 + -1;
          LORelease();
          if (lVar3 == 0) {
            lVar3 = *local_178;
            local_178 = plVar5;
            (**(code **)(lVar3 + 0x10))(plVar2);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
            plVar5 = local_178;
          }
        }
        local_178 = plVar5;
        FUN_00ac6290(auStack_3f8);
        plVar2 = plStack_d8;
        if (plStack_d8 != (long *)0x0) {
          LOAcquire();
          lVar3 = plStack_d8[1];
          plStack_d8[1] = lVar3 + -1;
          LORelease();
          if (lVar3 == 0) {
            (**(code **)(*plStack_d8 + 0x10))(plStack_d8);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
          }
        }
        plVar2 = local_178;
        if (*(int *)(local_180 + 0xf4) != 0) {
          lVar3 = *param_3;
          if (local_178 != (long *)0x0) {
            plVar5 = local_178 + 1;
            *plVar5 = *plVar5 + 1;
            *plVar5 = *plVar5 + 1;
          }
          plVar5 = *(long **)(lVar3 + 0x20);
          *(long *)(lVar3 + 0x18) = local_180;
          *(long **)(lVar3 + 0x20) = local_178;
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
          if (plVar2 != (long *)0x0) {
            LOAcquire();
            lVar3 = plVar2[1];
            plVar2[1] = lVar3 + -1;
            LORelease();
            if (lVar3 == 0) {
              (**(code **)(*plVar2 + 0x10))(plVar2);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
            }
          }
          iVar4 = thunk_FUN_05e1d97c(2);
          if (iVar4 != 0) {
            FUN_0488143c(local_410);
            pppppppuVar1 = local_410[0];
            if (-1 < cStack_3f9) {
              pppppppuVar1 = local_410;
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
            if ((DAT_0a3d93f1 & 1) == 0) {
              _DAT_0a3d93dc = CONCAT44((int)DAT_087e3028,(int)DAT_087ef190);
              uRam000000000a3d93e4 = CONCAT44((int)DAT_084a66b0,(int)DAT_085095c0);
              DAT_0a3d93ec = (undefined4)DAT_08833a40;
              DAT_0a3d93f0 = 0;
              DAT_0a3d93f1 = 1;
            }
            FUN_05e1d050(auStack_3f8,2,pppppppuVar1,&DAT_0a3d8cf0,&DAT_0a3d93dc,0x29a,0,0);
            FUN_04cbe440(local_428,local_180);
            local_130 = local_428[0];
            if (-1 < cStack_411) {
              local_130 = local_428;
            }
            local_128 = 0;
            if ((DAT_0a3d9456 & 1) == 0) {
              _DAT_0a3d9438 = CONCAT44((int)DAT_08486a48,(int)DAT_0855b808);
              uRam000000000a3d9440 = CONCAT44((int)DAT_084e3ff8,(int)DAT_084ec280);
              DAT_0a3d9448 = CONCAT44((int)DAT_088ae308,(int)DAT_088769a8);
              DAT_0a3d9450 = (undefined4)DAT_084c77e8;
              DAT_0a3d9454 = 0x73;
              DAT_0a3d9456 = 1;
            }
            uStack_d0 = 0;
            plStack_d8 = (long *)0x0;
            local_e0 = &local_130;
            uStack_c0 = 0;
            local_c8 = 0;
            uStack_b0 = 0;
            local_b8 = 0;
            uStack_a0 = 0;
            local_a8 = 0;
            uStack_90 = 0;
            local_98 = 0;
            uStack_80 = 0;
            local_88 = 0;
            uStack_70 = 0;
            local_78 = 0;
            local_68 = 0;
            FUN_05e1d31c(auStack_3f8,&DAT_0a3d9438,&local_e0);
            if (cStack_411 < '\0') {
              __ZdlPvm(local_428[0],CONCAT17(cStack_411,local_418) & 0x7fffffffffffffff);
            }
            thunk_FUN_05e1d0bc(auStack_3f8);
            if (cStack_3f9 < '\0') {
              __ZdlPvm(local_410[0],CONCAT17(cStack_3f9,local_400) & 0x7fffffffffffffff);
            }
          }
          plVar2 = local_178;
          if (local_178 != (long *)0x0) {
            LOAcquire();
            lVar3 = local_178[1];
            local_178[1] = lVar3 + -1;
            LORelease();
            if (lVar3 == 0) {
              (**(code **)(*local_178 + 0x10))(local_178);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
            }
          }
          if (local_168 == (long *)0x0) goto LAB_030dbbd0;
          goto LAB_030dbba8;
        }
        iVar4 = thunk_FUN_05e1d97c(4);
        if (iVar4 != 0) {
          FUN_0488143c(local_410);
          pppppppuVar1 = local_410[0];
          if (-1 < cStack_3f9) {
            pppppppuVar1 = local_410;
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
          if ((DAT_0a3d93f1 & 1) == 0) {
            _DAT_0a3d93dc = CONCAT44((int)DAT_087e3028,(int)DAT_087ef190);
            uRam000000000a3d93e4 = CONCAT44((int)DAT_084a66b0,(int)DAT_085095c0);
            DAT_0a3d93ec = (undefined4)DAT_08833a40;
            DAT_0a3d93f0 = 0;
            DAT_0a3d93f1 = 1;
          }
          FUN_05e1d050(auStack_3f8,4,pppppppuVar1,&DAT_0a3d8cf0,&DAT_0a3d93dc,0x296,0,0);
          FUN_04cbe440(local_428,local_180);
          local_130 = local_428[0];
          if (-1 < cStack_411) {
            local_130 = local_428;
          }
          local_128 = 0;
          if ((DAT_0a3d9434 & 1) == 0) {
            _DAT_0a3d9418 = CONCAT44((int)DAT_084ec280,(int)DAT_08486a48);
            uRam000000000a3d9420 = CONCAT44((int)DAT_088ae310,(int)DAT_0874c1f8);
            DAT_0a3d9428 = CONCAT44((int)DAT_0847fde0,(int)DAT_088ae300);
            DAT_0a3d9430 = (undefined4)DAT_0847fde8;
            DAT_0a3d9434 = 1;
          }
          uStack_d0 = 0;
          plStack_d8 = (long *)0x0;
          local_e0 = &local_130;
          uStack_c0 = 0;
          local_c8 = 0;
          uStack_b0 = 0;
          local_b8 = 0;
          uStack_a0 = 0;
          local_a8 = 0;
          uStack_90 = 0;
          local_98 = 0;
          uStack_80 = 0;
          local_88 = 0;
          uStack_70 = 0;
          local_78 = 0;
          local_68 = 0;
          FUN_05e1d31c(auStack_3f8,&DAT_0a3d9418,&local_e0);
          if (cStack_411 < '\0') {
            __ZdlPvm(local_428[0],CONCAT17(cStack_411,local_418) & 0x7fffffffffffffff);
          }
          thunk_FUN_05e1d0bc(auStack_3f8);
          if (cStack_3f9 < '\0') {
            __ZdlPvm(local_410[0],CONCAT17(cStack_3f9,local_400) & 0x7fffffffffffffff);
          }
        }
        uVar7 = 200;
        uVar6 = 2;
      }
      FUN_030f6650(param_1,1,2,uVar6,uVar7);
      plVar2 = local_178;
      if (local_178 != (long *)0x0) {
        LOAcquire();
        lVar3 = local_178[1];
        local_178[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*local_178 + 0x10))(local_178);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
        }
      }
      plVar2 = local_168;
      if (local_168 != (long *)0x0) {
        LOAcquire();
        lVar3 = local_168[1];
        local_168[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*local_168 + 0x10))(local_168);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
        }
      }
      goto LAB_030dbc24;
    }
LAB_030dbba8:
    plVar2 = local_168;
    LOAcquire();
    lVar3 = local_168[1];
    local_168[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_168 + 0x10))();
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
LAB_030dbbd0:
  *param_1 = local_160;
  if ((long)puStack_148 < 0) {
    FUN_00018d20(param_1 + 1,puStack_158,local_150);
  }
  else {
    puVar8 = (undefined8 *)((ulong)&local_160 | 8);
    uVar6 = *puVar8;
    param_1[2] = puVar8[1];
    param_1[1] = uVar6;
    param_1[3] = puVar8[2];
  }
  param_1[4] = local_140;
  param_1[5] = local_138;
  if (local_138 != (long *)0x0) {
    local_138[1] = local_138[1] + 1;
  }
LAB_030dbc24:
  plVar2 = local_138;
  if (local_138 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_138[1];
    local_138[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_138 + 0x10))(local_138);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  if ((long)puStack_148 < 0) {
    __ZdlPvm(puStack_158,(ulong)puStack_148 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_58) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


