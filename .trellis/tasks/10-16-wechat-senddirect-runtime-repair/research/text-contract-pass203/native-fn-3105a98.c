// Ghidra inferred pseudocode; requested=0x3105a98
// entry=03105a98 end=031064e3

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_03105a98(undefined8 param_1,long *param_2,long *param_3)

{
  undefined8 *******pppppppuVar1;
  long *plVar2;
  long lVar3;
  int iVar4;
  ulong uVar5;
  long lVar6;
  long *plVar7;
  long local_1e8;
  long *local_1e0;
  long local_1d8;
  long *local_1d0;
  long local_1c8;
  long *local_1c0;
  long local_1b8;
  long *local_1b0;
  undefined8 *******local_1a8 [2];
  undefined7 local_198;
  char cStack_191;
  long *local_190;
  long *local_188;
  long local_100;
  long *local_f8;
  long local_f0;
  long *local_e8;
  long local_e0;
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
  lVar6 = *param_3;
  local_e0 = *(long *)(lVar6 + 0x18);
  local_d8 = *(long **)(lVar6 + 0x20);
  lVar3 = 0;
  if (local_d8 != (long *)0x0) {
    lVar3 = local_d8[1];
    local_d8[1] = lVar3 + 1;
    lVar6 = *param_3;
  }
  if ((*(long *)(lVar6 + 8) == 0) ||
     (local_f0 = ___dynamic_cast(lVar3,*(long *)(lVar6 + 8),&PTR_DAT_09c37aa0,&PTR_DAT_09eb2580,0),
     local_f0 == 0)) {
    local_f0 = 0;
    local_e8 = (long *)0x0;
  }
  else {
    local_e8 = *(long **)(lVar6 + 0x10);
    if (local_e8 != (long *)0x0) {
      local_e8[1] = local_e8[1] + 1;
      lVar6 = *param_3;
    }
  }
  local_f8 = (long *)param_3[1];
  if (local_f8 != (long *)0x0) {
    local_f8[1] = local_f8[1] + 1;
  }
  local_100 = lVar6;
  uVar5 = (**(code **)(*param_2 + 0xe0))(param_2,&local_100);
  plVar2 = local_f8;
  if (local_f8 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_f8[1];
    local_f8[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_f8 + 0x10))(local_f8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  if ((uVar5 & 1) == 0) {
    iVar4 = thunk_FUN_05e1d97c(4);
    if (iVar4 != 0) {
      FUN_0488143c(local_1a8);
      pppppppuVar1 = local_1a8[0];
      if (-1 < cStack_191) {
        pppppppuVar1 = local_1a8;
      }
      if ((DAT_0a3da318 & 1) == 0) {
        _DAT_0a3da300 = CONCAT44((int)DAT_084a66a8,(int)DAT_0849a618);
        uRam000000000a3da308 = CONCAT44((int)DAT_0875a898,(int)DAT_084a66b0);
        DAT_0a3da310 = CONCAT44((int)DAT_084c8608,(int)DAT_084d88d0);
        DAT_0a3da318 = 1;
      }
      if ((DAT_0a3da338 & 1) == 0) {
        _DAT_0a3da31c = CONCAT44((int)DAT_087e2df0,(int)ram0x087e2de8);
        uRam000000000a3da324 = CONCAT44((int)DAT_08546648,(int)ram0x084f0820);
        DAT_0a3da32c = CONCAT44((int)DAT_0850ad18,(int)DAT_084b0670);
        DAT_0a3da334 = (undefined4)DAT_088a3be8;
        DAT_0a3da338 = 1;
      }
      FUN_05e1d050(&local_190,4,pppppppuVar1,&DAT_0a3da300,&DAT_0a3da31c,0x1f,0,0);
      if ((DAT_0a3da355 & 1) == 0) {
        _DAT_0a3da33c = CONCAT44((int)DAT_084b0670,(int)DAT_08546648);
        uRam000000000a3da344 = CONCAT44((int)DAT_084b0210,(int)DAT_0851e6c0);
        DAT_0a3da34c = CONCAT44((int)DAT_084d1000,(int)DAT_0847fde0);
        DAT_0a3da354 = 0;
        DAT_0a3da355 = 1;
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
      FUN_05e1d31c(&local_190,&DAT_0a3da33c,&local_d0);
      thunk_FUN_05e1d0bc(&local_190);
      if (cStack_191 < '\0') {
        __ZdlPvm(local_1a8[0],CONCAT17(cStack_191,local_198) & 0x7fffffffffffffff);
      }
    }
    FUN_030f6650(param_1,1,1,4,400);
  }
  else {
    if ((local_f0 == 0) ||
       (local_1b8 = ___dynamic_cast(local_f0,&PTR_DAT_09eb2580,&PTR_DAT_09eb2598,0), local_1b8 == 0)
       ) {
      local_1b8 = 0;
      local_1b0 = (long *)0x0;
      iVar4 = thunk_FUN_05e1d97c(4);
      if (iVar4 != 0) {
        FUN_0488143c(local_1a8);
        pppppppuVar1 = local_1a8[0];
        if (-1 < cStack_191) {
          pppppppuVar1 = local_1a8;
        }
        if ((DAT_0a3da318 & 1) == 0) {
          _DAT_0a3da300 = CONCAT44((int)DAT_084a66a8,(int)DAT_0849a618);
          uRam000000000a3da308 = CONCAT44((int)DAT_0875a898,(int)DAT_084a66b0);
          DAT_0a3da310 = CONCAT44((int)DAT_084c8608,(int)DAT_084d88d0);
          DAT_0a3da318 = 1;
        }
        if ((DAT_0a3da338 & 1) == 0) {
          _DAT_0a3da31c = CONCAT44((int)DAT_087e2df0,(int)ram0x087e2de8);
          uRam000000000a3da324 = CONCAT44((int)DAT_08546648,(int)ram0x084f0820);
          DAT_0a3da32c = CONCAT44((int)DAT_0850ad18,(int)DAT_084b0670);
          DAT_0a3da334 = (undefined4)DAT_088a3be8;
          DAT_0a3da338 = 1;
        }
        FUN_05e1d050(&local_190,4,pppppppuVar1,&DAT_0a3da300,&DAT_0a3da31c,0x25,0,0);
        if ((DAT_0a3da374 & 1) == 0) {
          _DAT_0a3da358 = CONCAT44((int)DAT_08557bc8,(int)DAT_0849a618);
          uRam000000000a3da360 = CONCAT44((int)ram0x08491928,(int)DAT_085e8930);
          DAT_0a3da368 = CONCAT44((int)DAT_08486088,(int)DAT_084cadd8);
          DAT_0a3da370 = (undefined4)DAT_084eadc8;
          DAT_0a3da374 = 1;
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
        FUN_05e1d31c(&local_190,&DAT_0a3da358,&local_d0);
        thunk_FUN_05e1d0bc(&local_190);
        if (cStack_191 < '\0') {
          __ZdlPvm(local_1a8[0],CONCAT17(cStack_191,local_198) & 0x7fffffffffffffff);
        }
      }
      local_1c8 = *param_3;
      local_1c0 = (long *)param_3[1];
      if (local_1c0 != (long *)0x0) {
        local_1c0[1] = local_1c0[1] + 1;
      }
      FUN_030db798(param_1,param_2,&local_1c8);
      plVar2 = local_1c0;
    }
    else {
      local_1b0 = local_e8;
      if (local_e8 != (long *)0x0) {
        local_e8[1] = local_e8[1] + 1;
      }
      local_1d8 = *(long *)(local_e0 + 0x230);
      local_1d0 = *(long **)(local_e0 + 0x238);
      if (local_1d0 != (long *)0x0) {
        local_1d0[1] = local_1d0[1] + 1;
      }
      if (local_1d8 == 0) {
        lVar3 = (long)*(char *)(local_1b8 + 0x5f7);
        if (lVar3 < 0) {
          lVar3 = *(long *)(local_1b8 + 0x5e8);
        }
        if ((lVar3 != 0) && (iVar4 = thunk_FUN_05e1d97c(2), iVar4 != 0)) {
          FUN_0488143c(local_1a8);
          pppppppuVar1 = local_1a8[0];
          if (-1 < cStack_191) {
            pppppppuVar1 = local_1a8;
          }
          if ((DAT_0a3da318 & 1) == 0) {
            _DAT_0a3da300 = CONCAT44((int)DAT_084a66a8,(int)DAT_0849a618);
            uRam000000000a3da308 = CONCAT44((int)DAT_0875a898,(int)DAT_084a66b0);
            DAT_0a3da310 = CONCAT44((int)DAT_084c8608,(int)DAT_084d88d0);
            DAT_0a3da318 = 1;
          }
          if ((DAT_0a3da338 & 1) == 0) {
            _DAT_0a3da31c = CONCAT44((int)DAT_087e2df0,(int)ram0x087e2de8);
            uRam000000000a3da324 = CONCAT44((int)DAT_08546648,(int)ram0x084f0820);
            DAT_0a3da32c = CONCAT44((int)DAT_0850ad18,(int)DAT_084b0670);
            DAT_0a3da334 = (undefined4)DAT_088a3be8;
            DAT_0a3da338 = 1;
          }
          FUN_05e1d050(&local_190,2,pppppppuVar1,&DAT_0a3da300,&DAT_0a3da31c,0x39,0,0);
          if ((DAT_0a3da3a2 & 1) == 0) {
            _DAT_0a3da378 = CONCAT44((int)DAT_08548d20,(int)DAT_08523398);
            uRam000000000a3da380 = CONCAT44((int)ram0x084f1748,(int)DAT_084cd458);
            _DAT_0a3da388 = CONCAT44((int)DAT_08531ed8,(int)DAT_088a3c40);
            uRam000000000a3da390 = CONCAT44((int)DAT_0852d038,(int)DAT_0853e438);
            DAT_0a3da398 = CONCAT44((int)DAT_084cd478,(int)DAT_084d86b0);
            DAT_0a3da3a0 = 0x74;
            DAT_0a3da3a2 = 1;
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
          FUN_05e1d31c(&local_190,&DAT_0a3da378,&local_d0);
          thunk_FUN_05e1d0bc(&local_190);
          if (cStack_191 < '\0') {
            __ZdlPvm(local_1a8[0],CONCAT17(cStack_191,local_198) & 0x7fffffffffffffff);
          }
        }
      }
      else {
        local_190 = *(long **)(local_1d8 + 0x48);
        plVar2 = *(long **)(local_1d8 + 0x50);
        if (plVar2 != (long *)0x0) {
          plVar2[1] = plVar2[1] + 1;
        }
        local_188 = plVar2;
        if (local_190 == (long *)0x0) {
          local_188 = (long *)__Znwm(0x20);
          local_188[1] = 0;
          local_188[2] = 0;
          *local_188 = (long)&PTR_FUN_09de65c8;
          local_190 = local_188 + 3;
          *local_190 = 0;
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
          *(int *)local_190 = 1;
        }
        else if ((int)*local_190 == 0) {
          *(int *)local_190 = 1;
        }
        plVar2 = local_188;
        if (local_188 != (long *)0x0) {
          plVar7 = local_188 + 1;
          *plVar7 = *plVar7 + 1;
          *plVar7 = *plVar7 + 1;
        }
        plVar7 = *(long **)(local_1d8 + 0x50);
        *(long **)(local_1d8 + 0x48) = local_190;
        *(long **)(local_1d8 + 0x50) = local_188;
        if (plVar7 != (long *)0x0) {
          LOAcquire();
          lVar3 = plVar7[1];
          plVar7[1] = lVar3 + -1;
          LORelease();
          if (lVar3 == 0) {
            (**(code **)(*plVar7 + 0x10))(plVar7);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
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
        lVar3 = (long)*(char *)(local_1b8 + 0x5f7);
        if (lVar3 < 0) {
          lVar3 = *(long *)(local_1b8 + 0x5e8);
        }
        if (lVar3 != 0) {
          __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                    (local_1d8 + 0x18,local_1b8 + 0x5e0);
        }
        plVar2 = local_188;
        if (local_188 != (long *)0x0) {
          LOAcquire();
          lVar3 = local_188[1];
          local_188[1] = lVar3 + -1;
          LORelease();
          if (lVar3 == 0) {
            (**(code **)(*local_188 + 0x10))(local_188);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
          }
        }
      }
      *(undefined1 *)(local_e0 + 600) = 0;
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (local_e0 + 0x130,local_1b8 + 0x5c8);
      local_1e8 = *param_3;
      local_1e0 = (long *)param_3[1];
      if (local_1e0 != (long *)0x0) {
        local_1e0[1] = local_1e0[1] + 1;
      }
      FUN_030db798(param_1,param_2,&local_1e8);
      plVar7 = local_1e0;
      plVar2 = local_1d0;
      if (local_1e0 != (long *)0x0) {
        LOAcquire();
        lVar3 = local_1e0[1];
        local_1e0[1] = lVar3 + -1;
        LORelease();
        if (lVar3 == 0) {
          (**(code **)(*local_1e0 + 0x10))(local_1e0);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
          plVar2 = local_1d0;
        }
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
    plVar2 = local_1b0;
    if (local_1b0 != (long *)0x0) {
      LOAcquire();
      lVar3 = local_1b0[1];
      local_1b0[1] = lVar3 + -1;
      LORelease();
      if (lVar3 == 0) {
        (**(code **)(*local_1b0 + 0x10))(local_1b0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
      }
    }
  }
  plVar2 = local_e8;
  if (local_e8 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_e8[1];
    local_e8[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_e8 + 0x10))(local_e8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  plVar2 = local_d8;
  if (local_d8 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_d8[1];
    local_d8[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_d8 + 0x10))(local_d8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


