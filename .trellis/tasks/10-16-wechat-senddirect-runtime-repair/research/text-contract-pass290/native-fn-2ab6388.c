// Ghidra inferred pseudocode; requested=0x2ab6388
// entry=02ab6388 end=02ab6f33

/* WARNING: Removing unreachable block (ram,0x02ab6c20) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_02ab6388(undefined8 *param_1,long param_2,long *param_3)

{
  ulong uVar1;
  long *******ppppppplVar2;
  long *plVar3;
  long lVar4;
  long lVar5;
  int iVar6;
  long *plVar7;
  undefined8 uVar8;
  undefined8 *puVar9;
  long lVar10;
  long *******local_548;
  long *local_540;
  undefined7 local_538;
  char cStack_531;
  long **local_530;
  long *local_528;
  long **local_520;
  long *local_518;
  undefined8 local_510;
  undefined1 auStack_478 [824];
  undefined1 *local_140;
  long *plStack_138;
  undefined **local_130;
  long *local_128;
  undefined1 local_120;
  undefined7 uStack_11f;
  long **local_d8;
  long *local_d0;
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
  undefined8 local_60;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  uVar1 = param_3[1];
  if (-1 < (char)*(byte *)((long)param_3 + 0x17)) {
    uVar1 = (ulong)*(byte *)((long)param_3 + 0x17);
  }
  if (uVar1 == 0) {
    *param_1 = 0;
    param_1[1] = 0;
    goto LAB_02ab6ef8;
  }
  iVar6 = FUN_04bb4a4c(param_3);
  if (iVar6 == 0) {
    iVar6 = FUN_04bb3c60(param_3);
    if (iVar6 != 0) {
      FUN_0466aca8(&local_128);
      FUN_01205740(&local_d8,local_128);
      FUN_0230b2a8(&local_520,local_d8);
      FUN_03d64828(param_1,local_520,param_3);
      goto LAB_02ab645c;
    }
    plStack_138 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    local_140 = &SUB_aaaaaaaaaaaaaaaa;
    plVar7 = (long *)FUN_04669774();
    (**(code **)(*plVar7 + 0x68))(&local_548);
    (*(code *)(*local_548)[7])(&local_128);
    local_530 = (long **)&PTR_FUN_09c567e0;
    local_520 = (long **)&SUB_aaaaaaaaaaaaaaaa;
    local_518 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    FUN_044e6b1c(&local_520,local_128,&local_530);
    plVar7 = local_518;
    local_d8 = local_520;
    local_d0 = local_518;
    if ((local_518 != (long *)0x0) && (local_518[1] = local_518[1] + 1, local_518 != (long *)0x0)) {
      LOAcquire();
      lVar4 = local_518[1];
      local_518[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*local_518 + 0x10))(local_518);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
      }
    }
    FUN_044fb300(&local_140,local_d8,param_3);
    plVar7 = local_d0;
    if (local_d0 != (long *)0x0) {
      LOAcquire();
      lVar4 = local_d0[1];
      local_d0[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*local_d0 + 0x10))(local_d0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
      }
    }
    plVar7 = (long *)CONCAT71(uStack_11f,local_120);
    if (plVar7 != (long *)0x0) {
      LOAcquire();
      lVar4 = plVar7[1];
      plVar7[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*plVar7 + 0x10))(plVar7);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
      }
    }
    plVar7 = local_540;
    if (local_540 != (long *)0x0) {
      LOAcquire();
      lVar4 = local_540[1];
      local_540[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*local_540 + 0x10))(local_540);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
      }
    }
    if (local_140 == (undefined1 *)0x0) {
      local_530 = (long **)&SUB_aaaaaaaaaaaaaaaa;
      local_528 = (long *)&SUB_aaaaaaaaaaaaaaaa;
      FUN_02b4b150(&local_530,*(undefined8 *)(param_2 + 0x188),param_3);
      local_520 = local_530;
      local_518 = local_528;
      lVar4 = 0;
      if (local_528 != (long *)0x0) {
        lVar4 = local_528[1];
        local_528[1] = lVar4 + 1;
      }
      local_510 = 0;
      FUN_066856fc(lVar4,&local_520);
      lVar10 = FUN_02ae2294(&local_520);
      plVar7 = local_518;
      lVar4 = lVar10;
      if (local_518 != (long *)0x0) {
        LOAcquire();
        lVar5 = local_518[1];
        local_518[1] = lVar5 + -1;
        LORelease();
        if (lVar5 == 0) {
          (**(code **)(*local_518 + 0x10))(local_518);
          lVar4 = __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
        }
      }
      if (*(char *)(lVar10 + 0x3e0) == '\x01') {
        FUN_02ab8e14(lVar4,lVar10);
        plVar7 = (long *)FUN_04669774();
        (**(code **)(*plVar7 + 0x68))(&local_548);
        (*(code *)(*local_548)[7])(&local_128);
        local_130 = &PTR_FUN_09c567e0;
        local_520 = (long **)&SUB_aaaaaaaaaaaaaaaa;
        local_518 = (long *)&SUB_aaaaaaaaaaaaaaaa;
        FUN_044e6b1c(&local_520,local_128,&local_130);
        plVar7 = local_518;
        local_d8 = local_520;
        local_d0 = local_518;
        if ((local_518 != (long *)0x0) &&
           (local_518[1] = local_518[1] + 1, local_518 != (long *)0x0)) {
          LOAcquire();
          lVar4 = local_518[1];
          local_518[1] = lVar4 + -1;
          LORelease();
          if (lVar4 == 0) {
            (**(code **)(*local_518 + 0x10))(local_518);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
          }
        }
        if ((*(byte *)(lVar10 + 0x3e0) & 1) == 0) {
                    /* WARNING: Subroutine does not return */
          FUN_004d04d4();
        }
        FUN_044f8f50(local_d8,lVar10);
        plVar7 = local_d0;
        if (local_d0 != (long *)0x0) {
          LOAcquire();
          lVar4 = local_d0[1];
          local_d0[1] = lVar4 + -1;
          LORelease();
          if (lVar4 == 0) {
            (**(code **)(*local_d0 + 0x10))(local_d0);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
          }
        }
        plVar7 = (long *)CONCAT71(uStack_11f,local_120);
        if (plVar7 != (long *)0x0) {
          LOAcquire();
          lVar4 = plVar7[1];
          plVar7[1] = lVar4 + -1;
          LORelease();
          if (lVar4 == 0) {
            (**(code **)(*plVar7 + 0x10))(plVar7);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
          }
        }
        plVar7 = local_540;
        if (local_540 != (long *)0x0) {
          LOAcquire();
          lVar4 = local_540[1];
          local_540[1] = lVar4 + -1;
          LORelease();
          if (lVar4 == 0) {
            (**(code **)(*local_540 + 0x10))(local_540);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
          }
        }
        plVar7 = (long *)FUN_04669774();
        (**(code **)(*plVar7 + 0x68))(&local_548);
        (*(code *)(*local_548)[7])(&local_128);
        local_130 = &PTR_FUN_09c567e0;
        local_520 = (long **)&SUB_aaaaaaaaaaaaaaaa;
        local_518 = (long *)&SUB_aaaaaaaaaaaaaaaa;
        FUN_044e6b1c(&local_520,local_128,&local_130);
        plVar7 = local_518;
        local_d8 = local_520;
        local_d0 = local_518;
        if ((local_518 != (long *)0x0) &&
           (local_518[1] = local_518[1] + 1, local_518 != (long *)0x0)) {
          LOAcquire();
          lVar4 = local_518[1];
          local_518[1] = lVar4 + -1;
          LORelease();
          if (lVar4 == 0) {
            (**(code **)(*local_518 + 0x10))(local_518);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
          }
        }
        FUN_044fb300(param_1,local_d8,param_3);
        plVar7 = local_d0;
        if (local_d0 != (long *)0x0) {
          LOAcquire();
          lVar4 = local_d0[1];
          local_d0[1] = lVar4 + -1;
          LORelease();
          if (lVar4 == 0) {
            (**(code **)(*local_d0 + 0x10))(local_d0);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
          }
        }
        plVar7 = (long *)CONCAT71(uStack_11f,local_120);
        if (plVar7 != (long *)0x0) {
          LOAcquire();
          lVar4 = plVar7[1];
          plVar7[1] = lVar4 + -1;
          LORelease();
          if (lVar4 == 0) {
            (**(code **)(*plVar7 + 0x10))(plVar7);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
          }
        }
        if (local_540 != (long *)0x0) {
          LOAcquire();
          lVar4 = local_540[1];
          local_540[1] = lVar4 + -1;
          LORelease();
          if (lVar4 == 0) {
            (**(code **)(*local_540 + 0x10))(local_540);
            __ZNSt3__119__shared_weak_count14__release_weakEv(local_540);
          }
        }
      }
      else {
        iVar6 = FUN_04bb5f30(param_3);
        if (iVar6 == 0) {
          iVar6 = FUN_04bb62cc(param_3);
          if (iVar6 == 0) {
            iVar6 = thunk_FUN_05e1d97c(2);
            if (iVar6 != 0) {
              FUN_0488143c(&local_548);
              ppppppplVar2 = local_548;
              if (-1 < cStack_531) {
                ppppppplVar2 = (long *******)&local_548;
              }
              if ((DAT_0a3af0c3 & 1) == 0) {
                uRam000000000a3af0b8._0_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[8];
                uRam000000000a3af0b8._1_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[9];
                uRam000000000a3af0b8._2_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[10];
                uRam000000000a3af0b8._3_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[0xb];
                uRam000000000a3af0b8._4_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[0xc];
                uRam000000000a3af0b8._5_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[0xd];
                uRam000000000a3af0b8._6_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[0xe];
                uRam000000000a3af0b8._7_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[0xf];
                DAT_0a3af0b0 = s_contact_manager_CoLoadFriendCont_0883d3c0[0];
                DAT_0a3af0b0_1._0_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[1];
                DAT_0a3af0b0_1._1_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[2];
                DAT_0a3af0b0_1._2_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[3];
                DAT_0a3af0b0_1._3_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[4];
                DAT_0a3af0b0_1._4_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[5];
                DAT_0a3af0b0_1._5_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[6];
                DAT_0a3af0b0_1._6_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[7];
                DAT_0a3af0c0 = 0x6363;
                DAT_0a3af0c2 = 0;
                DAT_0a3af0c3 = 1;
              }
              if ((DAT_0a3af35b & 1) == 0) {
                DAT_0a3af350._0_1_ = s_GetContact_e_0883d808[0];
                DAT_0a3af350._1_1_ = s_GetContact_e_0883d808[1];
                DAT_0a3af350._2_1_ = s_GetContact_e_0883d808[2];
                DAT_0a3af350._3_1_ = s_GetContact_e_0883d808[3];
                DAT_0a3af350._4_1_ = s_GetContact_e_0883d808[4];
                DAT_0a3af350._5_1_ = s_GetContact_e_0883d808[5];
                DAT_0a3af350._6_1_ = s_GetContact_e_0883d808[6];
                DAT_0a3af350._7_1_ = s_GetContact_e_0883d808[7];
                DAT_0a3af358 = 0x7463;
                DAT_0a3af35a = 0;
                DAT_0a3af35b = 1;
              }
              FUN_05e1d050(&local_520,2,ppppppplVar2,&DAT_0a3af0b0,&DAT_0a3af350,0x286,0,0);
              local_128 = (long *)*param_3;
              if (-1 < *(char *)((long)param_3 + 0x17)) {
                local_128 = param_3;
              }
              local_120 = 0;
              if ((DAT_0a3af392 & 1) == 0) {
                _DAT_0a3af378 = CONCAT44((int)DAT_0849b088,(int)DAT_085029a8);
                uRam000000000a3af380 = CONCAT44((int)DAT_0883d818,(int)ram0x0883d810);
                DAT_0a3af388 = CONCAT44((int)DAT_08598098,(int)ram0x08489fc8);
                DAT_0a3af390 = 0x5f;
                DAT_0a3af392 = 1;
              }
              local_d8 = &local_128;
              uStack_c8 = 0;
              local_d0 = (long *)0x0;
              uStack_b8 = 0;
              uStack_c0 = 0;
              uStack_a8 = 0;
              local_b0 = 0;
              uStack_98 = 0;
              uStack_a0 = 0;
              uStack_88 = 0;
              local_90 = 0;
              uStack_78 = 0;
              uStack_80 = 0;
              uStack_68 = 0;
              local_70 = 0;
              local_60 = 0;
              FUN_05e1d31c(&local_520,&DAT_0a3af378,&local_d8);
              thunk_FUN_05e1d0bc(&local_520);
              if (cStack_531 < '\0') {
                __ZdlPvm(local_548,CONCAT17(cStack_531,local_538) & 0x7fffffffffffffff);
              }
            }
            *param_1 = 0;
            param_1[1] = 0;
            goto LAB_02ab6e98;
          }
          _memset(&local_520,0xaa,0x3e0);
          FUN_025ddd08(&local_520);
          __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                    (&local_518,param_3);
          uVar8 = FUN_04e266e4();
          FUN_00255b9c(&local_d8,uVar8);
          __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                    (auStack_478,&local_d8);
          plVar7 = (long *)FUN_04669774();
          (**(code **)(*plVar7 + 0x68))(&local_548);
          (*(code *)(*local_548)[7])(&local_128);
          FUN_02444ec0(&local_d8,local_128);
          FUN_044f8f50(local_d8,&local_520);
          FUN_00129f68(&local_d8);
          FUN_00129f68(&local_128);
          FUN_00129f68(&local_548);
          plVar7 = (long *)FUN_04669774();
          (**(code **)(*plVar7 + 0x68))(&local_548);
          (*(code *)(*local_548)[7])(&local_128);
          FUN_02444ec0(&local_d8,local_128);
          FUN_044fb300(param_1,local_d8,param_3);
          FUN_00129f68(&local_d8);
          FUN_00129f68(&local_128);
          FUN_00129f68(&local_548);
        }
        else {
          iVar6 = thunk_FUN_05e1d97c(2);
          if (iVar6 != 0) {
            FUN_0488143c(&local_548);
            ppppppplVar2 = local_548;
            if (-1 < cStack_531) {
              ppppppplVar2 = (long *******)&local_548;
            }
            if ((DAT_0a3af0c3 & 1) == 0) {
              uRam000000000a3af0b8._0_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[8];
              uRam000000000a3af0b8._1_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[9];
              uRam000000000a3af0b8._2_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[10];
              uRam000000000a3af0b8._3_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[0xb];
              uRam000000000a3af0b8._4_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[0xc];
              uRam000000000a3af0b8._5_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[0xd];
              uRam000000000a3af0b8._6_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[0xe];
              uRam000000000a3af0b8._7_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[0xf];
              DAT_0a3af0b0 = s_contact_manager_CoLoadFriendCont_0883d3c0[0];
              DAT_0a3af0b0_1._0_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[1];
              DAT_0a3af0b0_1._1_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[2];
              DAT_0a3af0b0_1._2_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[3];
              DAT_0a3af0b0_1._3_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[4];
              DAT_0a3af0b0_1._4_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[5];
              DAT_0a3af0b0_1._5_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[6];
              DAT_0a3af0b0_1._6_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[7];
              DAT_0a3af0c0 = 0x6363;
              DAT_0a3af0c2 = 0;
              DAT_0a3af0c3 = 1;
            }
            if ((DAT_0a3af35b & 1) == 0) {
              DAT_0a3af350._0_1_ = s_GetContact_e_0883d808[0];
              DAT_0a3af350._1_1_ = s_GetContact_e_0883d808[1];
              DAT_0a3af350._2_1_ = s_GetContact_e_0883d808[2];
              DAT_0a3af350._3_1_ = s_GetContact_e_0883d808[3];
              DAT_0a3af350._4_1_ = s_GetContact_e_0883d808[4];
              DAT_0a3af350._5_1_ = s_GetContact_e_0883d808[5];
              DAT_0a3af350._6_1_ = s_GetContact_e_0883d808[6];
              DAT_0a3af350._7_1_ = s_GetContact_e_0883d808[7];
              DAT_0a3af358 = 0x7463;
              DAT_0a3af35a = 0;
              DAT_0a3af35b = 1;
            }
            FUN_05e1d050(&local_520,2,ppppppplVar2,&DAT_0a3af0b0,&DAT_0a3af350,0x278,0,0);
            local_128 = (long *)*param_3;
            if (-1 < *(char *)((long)param_3 + 0x17)) {
              local_128 = param_3;
            }
            local_120 = 0;
            if ((DAT_0a3af376 & 1) == 0) {
              _DAT_0a3af35c = CONCAT44((int)DAT_08489720,(int)DAT_085b0898);
              uRam000000000a3af364 = CONCAT44((int)DAT_0883d820,(int)DAT_0853ae18);
              DAT_0a3af36c = CONCAT44((int)DAT_0883d828,(int)DAT_0849b088);
              DAT_0a3af374 = 0x5f;
              DAT_0a3af376 = 1;
            }
            local_d8 = &local_128;
            uStack_c8 = 0;
            local_d0 = (long *)0x0;
            uStack_b8 = 0;
            uStack_c0 = 0;
            uStack_a8 = 0;
            local_b0 = 0;
            uStack_98 = 0;
            uStack_a0 = 0;
            uStack_88 = 0;
            local_90 = 0;
            uStack_78 = 0;
            uStack_80 = 0;
            uStack_68 = 0;
            local_70 = 0;
            local_60 = 0;
            FUN_05e1d31c(&local_520,&DAT_0a3af35c,&local_d8);
            thunk_FUN_05e1d0bc(&local_520);
            if (cStack_531 < '\0') {
              __ZdlPvm(local_548,CONCAT17(cStack_531,local_538) & 0x7fffffffffffffff);
            }
          }
          _memset(&local_520,0xaa,0x3e0);
          FUN_025ddd08(&local_520);
          uVar8 = __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                            (&local_518,param_3);
          FUN_02ab5ec8(uVar8,&local_520);
          FUN_02ab8f80(param_1,&local_520);
        }
        FUN_02331b88(&local_520);
      }
LAB_02ab6e98:
      plVar3 = local_528;
      plVar7 = plStack_138;
      if (local_528 != (long *)0x0) {
        LOAcquire();
        lVar4 = local_528[1];
        local_528[1] = lVar4 + -1;
        LORelease();
        if (lVar4 == 0) {
          (**(code **)(*local_528 + 0x10))(local_528);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
          plVar7 = plStack_138;
        }
      }
    }
    else {
      iVar6 = FUN_04bb4dc0(local_140 + 8);
      if (iVar6 == 0) {
        iVar6 = FUN_04bb5048(local_140 + 8);
        if (iVar6 == 0) {
          iVar6 = FUN_04bb55b8(local_140 + 8);
          if (iVar6 == 0) {
            param_1[1] = plStack_138;
            *param_1 = local_140;
            plStack_138 = (long *)0x0;
            local_140 = (undefined1 *)0x0;
            plVar7 = plStack_138;
            goto joined_r0x02ab6ecc;
          }
          _memset(&local_520,0xaa,0x3e0);
          uVar8 = FUN_0233200c(&local_520,local_140);
          FUN_02ab9104(uVar8,&local_520);
          FUN_02ab8f80(param_1,&local_520);
        }
        else {
          _memset(&local_520,0xaa,0x3e0);
          uVar8 = FUN_0233200c(&local_520,local_140);
          FUN_02ab8ff4(uVar8,&local_520);
          FUN_02ab8f80(param_1,&local_520);
        }
      }
      else {
        _memset(&local_520,0xaa,0x3e0);
        uVar8 = FUN_0233200c(&local_520,local_140);
        FUN_02ab8e14(uVar8,&local_520);
        puVar9 = (undefined8 *)__Znwm(0x3f8);
        puVar9[1] = 0;
        puVar9[2] = 0;
        *puVar9 = &PTR_FUN_09dafb50;
        uVar8 = FUN_0233200c(puVar9 + 3,&local_520);
        *param_1 = uVar8;
        param_1[1] = puVar9;
      }
      FUN_02331b88(&local_520);
      plVar7 = plStack_138;
    }
  }
  else {
    FUN_0466aca8(&local_128);
    FUN_01205740(&local_d8,local_128);
    FUN_023f9000(&local_520,local_d8);
    FUN_027eecc4(param_1,local_520,param_3);
LAB_02ab645c:
    plVar7 = local_518;
    if (local_518 != (long *)0x0) {
      LOAcquire();
      lVar4 = local_518[1];
      local_518[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*local_518 + 0x10))(local_518);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
      }
    }
    plVar7 = local_d0;
    if (local_d0 != (long *)0x0) {
      LOAcquire();
      lVar4 = local_d0[1];
      local_d0[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*local_d0 + 0x10))(local_d0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
      }
    }
    plVar7 = (long *)CONCAT71(uStack_11f,local_120);
  }
joined_r0x02ab6ecc:
  if (plVar7 != (long *)0x0) {
    LOAcquire();
    lVar4 = plVar7[1];
    plVar7[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*plVar7 + 0x10))(plVar7);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
    }
  }
LAB_02ab6ef8:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


