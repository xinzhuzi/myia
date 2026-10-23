// Ghidra inferred pseudocode; requested=0x2eb4418
// entry=02eb4418 end=02eb4a8b

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_02eb4418(long *param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
                 undefined8 param_5)

{
  undefined8 *******pppppppuVar1;
  long lVar2;
  int iVar3;
  long *plVar4;
  long lVar5;
  ulong uVar6;
  long lVar7;
  long *local_200;
  long *local_1f8;
  long *local_1f0;
  undefined1 auStack_1e8 [8];
  undefined8 local_1e0;
  undefined7 local_1d0;
  char cStack_1c9;
  long *local_1c0;
  undefined8 *******local_1b8;
  long *local_1b0;
  undefined7 local_1a8;
  char cStack_1a1;
  undefined8 local_1a0;
  long *local_198;
  long *local_110;
  long *local_108;
  undefined1 *local_100;
  long *local_f8;
  long *local_f0;
  long *local_e8;
  undefined8 local_e0;
  long *plStack_d8;
  undefined8 uStack_d0;
  undefined8 uStack_c8;
  undefined8 local_c0;
  undefined8 uStack_b8;
  undefined8 uStack_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 uStack_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 uStack_70;
  undefined8 uStack_68;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_f0 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_e8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0077bdd0(&local_f0,&local_1a0);
  *(undefined8 *)((long)local_f0 + 0xe4) = DAT_087b64c8;
  local_100 = &SUB_aaaaaaaaaaaaaaaa;
  local_f8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0466aca8(&local_1b8);
  FUN_01205740(&local_e0,local_1b8);
  FUN_0268f370(&local_1a0,local_e0);
  local_110 = local_f0;
  local_108 = local_e8;
  if (local_e8 != (long *)0x0) {
    local_e8[1] = local_e8[1] + 1;
  }
  FUN_0319a638(&local_100,local_1a0,&local_110);
  plVar4 = local_108;
  if (local_108 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_108[1];
    local_108[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_108 + 0x10))(local_108);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if (local_198 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_198[1];
    local_198[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_198 + 0x10))(local_198);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_198);
    }
  }
  plVar4 = plStack_d8;
  if (plStack_d8 != (long *)0x0) {
    LOAcquire();
    lVar2 = plStack_d8[1];
    plStack_d8[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*plStack_d8 + 0x10))(plStack_d8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if (local_1b0 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_1b0[1];
    local_1b0[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_1b0 + 0x10))(local_1b0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_1b0);
    }
  }
  if (local_100 == (undefined1 *)0x0) {
    iVar3 = thunk_FUN_05e1d97c(4);
    if (iVar3 != 0) {
      FUN_0488143c(&local_1b8);
      pppppppuVar1 = local_1b8;
      if (-1 < cStack_1a1) {
        pppppppuVar1 = &local_1b8;
      }
      if ((DAT_0a3c9f34 & 1) == 0) {
        uVar6 = 0;
        do {
          (&DAT_0a3c9f1b)[uVar6] = (&DAT_08886d88)[uVar6] + 0x8a ^ (&DAT_08886d78)[uVar6 & 0xf];
          uVar6 = uVar6 + 1;
        } while (uVar6 != 0x19);
        DAT_0a3c9f34 = 1;
      }
      if ((DAT_0a3ca235 & 1) == 0) {
        uRam000000000a3ca228 = _UNK_088868b8;
        _DAT_0a3ca220 = _DAT_088868b0;
        DAT_0a3ca230 = (undefined4)DAT_086cacd0;
        DAT_0a3ca234 = 0;
        DAT_0a3ca235 = 1;
      }
      FUN_05e1d050(&local_1a0,4,pppppppuVar1,&DAT_0a3c9f1b,&DAT_0a3ca220,0x1a2,0,0);
      if ((DAT_0a3ca1e2 & 1) == 0) {
        uRam000000000a3ca1d8 = _UNK_088868d8;
        _DAT_0a3ca1d0 = _DAT_088868d0;
        DAT_0a3ca1e0 = 100;
        DAT_0a3ca1e2 = 1;
      }
      uStack_78 = 0;
      local_80 = 0;
      uStack_68 = 0;
      uStack_70 = 0;
      uStack_98 = 0;
      local_a0 = 0;
      uStack_88 = 0;
      uStack_90 = 0;
      uStack_b8 = 0;
      local_c0 = 0;
      uStack_a8 = 0;
      uStack_b0 = 0;
      plStack_d8 = (long *)0x0;
      local_e0 = 0;
      uStack_c8 = 0;
      uStack_d0 = 0;
      FUN_05e1d31c(&local_1a0,&DAT_0a3ca1d0,&local_e0);
      thunk_FUN_05e1d0bc(&local_1a0);
      if (cStack_1a1 < '\0') {
        __ZdlPvm(local_1b8,CONCAT17(cStack_1a1,local_1a8) & 0x7fffffffffffffff);
      }
    }
    *param_1 = 0;
    param_1[1] = 0;
  }
  else {
    plVar4 = (long *)__Znwm(0xf8);
    FUN_02ebf1d8(plVar4,&local_f0);
    local_1f8 = plVar4 + 3;
    if (plVar4 != (long *)0x0) {
      plVar4[1] = plVar4[1] + 1;
    }
    local_1f0 = plVar4;
    local_110 = local_1f8;
    local_108 = plVar4;
    FUN_030d2154(auStack_1e8,local_100,&local_1f8);
    if (local_1c0 != (long *)0x0) {
      LOAcquire();
      lVar2 = local_1c0[1];
      local_1c0[1] = lVar2 + -1;
      LORelease();
      if (lVar2 == 0) {
        (**(code **)(*local_1c0 + 0x10))(local_1c0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(local_1c0);
      }
    }
    if (cStack_1c9 < '\0') {
      __ZdlPvm(local_1e0,CONCAT17(cStack_1c9,local_1d0) & 0x7fffffffffffffff);
    }
    plVar4 = local_1f0;
    if (local_1f0 != (long *)0x0) {
      LOAcquire();
      lVar2 = local_1f0[1];
      local_1f0[1] = lVar2 + -1;
      LORelease();
      if (lVar2 == 0) {
        (**(code **)(*local_1f0 + 0x10))(local_1f0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
      }
    }
    lVar7 = local_110[3];
    *param_1 = lVar7;
    lVar5 = local_110[4];
    param_1[1] = lVar5;
    lVar2 = 0;
    if (lVar5 != 0) {
      lVar2 = *(long *)(lVar5 + 8);
      *(long *)(lVar5 + 8) = lVar2 + 1;
    }
    if ((*(long *)(lVar7 + 0x220) == 0) ||
       (lVar2 = ___dynamic_cast(lVar2,*(long *)(lVar7 + 0x220),&PTR_DAT_09eb1040,&PTR_DAT_09eb0cc0,0
                               ), lVar2 == 0)) {
      local_200 = (long *)0x0;
      iVar3 = thunk_FUN_05e1d97c(4);
      if (iVar3 != 0) {
        FUN_0488143c(&local_1b8);
        pppppppuVar1 = local_1b8;
        if (-1 < cStack_1a1) {
          pppppppuVar1 = &local_1b8;
        }
        if ((DAT_0a3c9f34 & 1) == 0) {
          uVar6 = 0;
          do {
            (&DAT_0a3c9f1b)[uVar6] = (&DAT_08886d88)[uVar6] + 0x8a ^ (&DAT_08886d78)[uVar6 & 0xf];
            uVar6 = uVar6 + 1;
          } while (uVar6 != 0x19);
          DAT_0a3c9f34 = 1;
        }
        if ((DAT_0a3ca235 & 1) == 0) {
          uRam000000000a3ca228 = _UNK_088868b8;
          _DAT_0a3ca220 = _DAT_088868b0;
          DAT_0a3ca230 = (undefined4)DAT_086cacd0;
          DAT_0a3ca234 = 0;
          DAT_0a3ca235 = 1;
        }
        FUN_05e1d050(&local_1a0,4,pppppppuVar1,&DAT_0a3c9f1b,&DAT_0a3ca220,0x1aa,0,0);
        if ((DAT_0a3ca252 & 1) == 0) {
          uRam000000000a3ca248 = _UNK_088868c8;
          _DAT_0a3ca240 = _DAT_088868c0;
          DAT_0a3ca250 = 100;
          DAT_0a3ca252 = 1;
        }
        uStack_78 = 0;
        local_80 = 0;
        uStack_68 = 0;
        uStack_70 = 0;
        uStack_98 = 0;
        local_a0 = 0;
        uStack_88 = 0;
        uStack_90 = 0;
        uStack_b8 = 0;
        local_c0 = 0;
        uStack_a8 = 0;
        uStack_b0 = 0;
        plStack_d8 = (long *)0x0;
        local_e0 = 0;
        uStack_c8 = 0;
        uStack_d0 = 0;
        FUN_05e1d31c(&local_1a0,&DAT_0a3ca240,&local_e0);
        thunk_FUN_05e1d0bc(&local_1a0);
        if (cStack_1a1 < '\0') {
          __ZdlPvm(local_1b8,CONCAT17(cStack_1a1,local_1a8) & 0x7fffffffffffffff);
        }
      }
    }
    else {
      local_200 = *(long **)(lVar7 + 0x228);
      lVar5 = 0;
      if (local_200 != (long *)0x0) {
        lVar5 = local_200[1];
        local_200[1] = lVar5 + 1;
      }
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (lVar5,lVar2 + 0x1e0,param_5);
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (lVar2 + 0x290,param_3);
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (lVar2 + 0x398,param_4);
    }
    if (local_200 != (long *)0x0) {
      LOAcquire();
      lVar2 = local_200[1];
      local_200[1] = lVar2 + -1;
      LORelease();
      if (lVar2 == 0) {
        (**(code **)(*local_200 + 0x10))(local_200);
        __ZNSt3__119__shared_weak_count14__release_weakEv(local_200);
      }
    }
    plVar4 = local_108;
    if (local_108 != (long *)0x0) {
      LOAcquire();
      lVar2 = local_108[1];
      local_108[1] = lVar2 + -1;
      LORelease();
      if (lVar2 == 0) {
        (**(code **)(*local_108 + 0x10))(local_108);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
      }
    }
  }
  plVar4 = local_f8;
  if (local_f8 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_f8[1];
    local_f8[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_f8 + 0x10))(local_f8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  plVar4 = local_e8;
  if (local_e8 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_e8[1];
    local_e8[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_e8 + 0x10))(local_e8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_58) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


