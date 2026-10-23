// Ghidra inferred pseudocode; requested=0x30bcd9c
// entry=030bcd9c end=030bd51f

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_030bcd9c(undefined8 param_1,undefined8 param_2,long *param_3)

{
  undefined8 ***pppuVar1;
  long *plVar2;
  long lVar3;
  long lVar4;
  int iVar5;
  ulong uVar6;
  long *plVar7;
  long lVar8;
  long local_1d8;
  long *local_1d0;
  long local_1c8;
  long *local_1c0;
  long local_1b8;
  long *local_1b0;
  undefined8 **local_1a8 [2];
  undefined7 local_198;
  char cStack_191;
  long local_190;
  long *local_188;
  long local_100;
  long *local_f8;
  long local_f0;
  long *local_e8;
  long *local_e0;
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
  lVar8 = *param_3;
  lVar4 = *(long *)(lVar8 + 0x18);
  local_e8 = *(long **)(lVar8 + 0x20);
  lVar3 = 0;
  if (local_e8 != (long *)0x0) {
    lVar3 = local_e8[1];
    local_e8[1] = lVar3 + 1;
    lVar8 = *param_3;
  }
  local_f0 = lVar4;
  if ((*(long *)(lVar8 + 8) == 0) ||
     (lVar3 = ___dynamic_cast(lVar3,*(long *)(lVar8 + 8),&PTR_DAT_09c37aa0,&PTR_DAT_09d03c08,0),
     lVar3 == 0)) {
    local_100 = 0;
    local_f8 = (long *)0x0;
  }
  else {
    local_f8 = *(long **)(lVar8 + 0x10);
    if (local_f8 != (long *)0x0) {
      local_f8[1] = local_f8[1] + 1;
    }
    local_100 = lVar3;
    if (lVar4 != 0) {
      if ((*(long *)(lVar4 + 0x220) == 0) ||
         (local_1b8 = ___dynamic_cast(*(long *)(lVar4 + 0x220),&PTR_DAT_09eb1040,&PTR_DAT_09eb2498,0
                                     ), local_1b8 == 0)) {
        local_1b8 = 0;
        local_1b0 = (long *)0x0;
        iVar5 = thunk_FUN_05e1d97c(4);
        if (iVar5 != 0) {
          FUN_0488143c(local_1a8);
          pppuVar1 = (undefined8 ***)local_1a8[0];
          if (-1 < cStack_191) {
            pppuVar1 = local_1a8;
          }
          if ((DAT_0a3d86c9 & 1) == 0) {
            uVar6 = 0;
            do {
              (&DAT_0a3d86ad)[uVar6] = (&DAT_088ad3fc)[uVar6] + 0x8a ^ (&DAT_088ad3ec)[uVar6 & 0xf];
              uVar6 = uVar6 + 1;
            } while (uVar6 != 0x1c);
            DAT_0a3d86c9 = 1;
          }
          if ((DAT_0a3d86e8 & 1) == 0) {
            _DAT_0a3d86cc = CONCAT44((int)DAT_087e2df0,(int)ram0x087e2de8);
            uRam000000000a3d86d4 = CONCAT44((int)DAT_08546648,(int)ram0x084f0820);
            DAT_0a3d86dc = CONCAT44((int)DAT_0850ad18,(int)DAT_084b0670);
            DAT_0a3d86e4 = (undefined4)DAT_088a3be8;
            DAT_0a3d86e8 = 1;
          }
          FUN_05e1d050(&local_190,4,pppuVar1,&DAT_0a3d86ad,&DAT_0a3d86cc,0x1e,0,0);
          if ((DAT_0a3d8702 & 1) == 0) {
            uVar6 = 0;
            do {
              (&DAT_0a3d86e9)[uVar6] = (&DAT_088ad458)[uVar6] + 0x8a ^ (&DAT_088ad448)[uVar6 & 0xf];
              uVar6 = uVar6 + 1;
            } while (uVar6 != 0x19);
            DAT_0a3d8702 = 1;
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
          local_e0 = (long *)0x0;
          uStack_c8 = 0;
          uStack_d0 = 0;
          FUN_05e1d31c(&local_190,&DAT_0a3d86e9,&local_e0);
          thunk_FUN_05e1d0bc(&local_190);
          if (cStack_191 < '\0') {
            __ZdlPvm(local_1a8[0],CONCAT17(cStack_191,local_198) & 0x7fffffffffffffff);
          }
        }
        FUN_030f6650(param_1,1,1,4,400);
      }
      else {
        local_1b0 = *(long **)(lVar4 + 0x228);
        if (local_1b0 == (long *)0x0) {
          local_1c0 = (long *)0x0;
          lVar4 = local_1b8;
        }
        else {
          plVar2 = local_1b0 + 1;
          *plVar2 = *plVar2 + 1;
          lVar4 = *plVar2;
          *plVar2 = lVar4 + 1;
          local_1c0 = local_1b0;
        }
        local_1c8 = local_1b8;
        FUN_04cff4c0(lVar4,lVar3,&local_1c8);
        plVar2 = local_1c0;
        if (local_1c0 != (long *)0x0) {
          LOAcquire();
          lVar4 = local_1c0[1];
          local_1c0[1] = lVar4 + -1;
          LORelease();
          if (lVar4 == 0) {
            (**(code **)(*local_1c0 + 0x10))(local_1c0);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
          }
        }
        lVar4 = local_f0;
        FUN_04cbf744(local_f0);
        local_190 = *(long *)(lVar4 + 0x230);
        local_188 = *(long **)(lVar4 + 0x238);
        if (local_188 != (long *)0x0) {
          local_188[1] = local_188[1] + 1;
        }
        if (local_190 != 0) {
          local_e0 = *(long **)(local_190 + 0x48);
          plVar2 = *(long **)(local_190 + 0x50);
          if (plVar2 != (long *)0x0) {
            plVar2[1] = plVar2[1] + 1;
          }
          plStack_d8 = plVar2;
          if (local_e0 == (long *)0x0) {
            plStack_d8 = (long *)__Znwm(0x20);
            plStack_d8[1] = 0;
            plStack_d8[2] = 0;
            *plStack_d8 = (long)&PTR_FUN_09de65c8;
            local_e0 = plStack_d8 + 3;
            *local_e0 = 0;
            if (plVar2 != (long *)0x0) {
              LOAcquire();
              lVar4 = plVar2[1];
              plVar2[1] = lVar4 + -1;
              LORelease();
              if (lVar4 == 0) {
                (**(code **)(*plVar2 + 0x10))(plVar2);
                __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
              }
            }
            *(int *)local_e0 = 1;
          }
          else if ((int)*local_e0 == 0) {
            *(int *)local_e0 = 1;
          }
          plVar2 = plStack_d8;
          if (plStack_d8 != (long *)0x0) {
            plVar7 = plStack_d8 + 1;
            *plVar7 = *plVar7 + 1;
            *plVar7 = *plVar7 + 1;
          }
          plVar7 = *(long **)(local_190 + 0x50);
          *(long **)(local_190 + 0x48) = local_e0;
          *(long **)(local_190 + 0x50) = plStack_d8;
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
          if (plVar2 != (long *)0x0) {
            LOAcquire();
            lVar4 = plVar2[1];
            plVar2[1] = lVar4 + -1;
            LORelease();
            if (lVar4 == 0) {
              (**(code **)(*plVar2 + 0x10))(plVar2);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
            }
          }
          plVar2 = plStack_d8;
          if (plStack_d8 != (long *)0x0) {
            LOAcquire();
            lVar4 = plStack_d8[1];
            plStack_d8[1] = lVar4 + -1;
            LORelease();
            if (lVar4 == 0) {
              (**(code **)(*plStack_d8 + 0x10))(plStack_d8);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
            }
          }
        }
        local_1d8 = *param_3;
        local_1d0 = (long *)param_3[1];
        if (local_1d0 != (long *)0x0) {
          local_1d0[1] = local_1d0[1] + 1;
        }
        FUN_030db798(param_1,param_2,&local_1d8);
        plVar2 = local_1d0;
        if (local_1d0 != (long *)0x0) {
          LOAcquire();
          lVar4 = local_1d0[1];
          local_1d0[1] = lVar4 + -1;
          LORelease();
          if (lVar4 == 0) {
            (**(code **)(*local_1d0 + 0x10))(local_1d0);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
          }
        }
        plVar2 = local_188;
        if (local_188 != (long *)0x0) {
          LOAcquire();
          lVar4 = local_188[1];
          local_188[1] = lVar4 + -1;
          LORelease();
          if (lVar4 == 0) {
            (**(code **)(*local_188 + 0x10))(local_188);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
          }
        }
      }
      plVar2 = local_1b0;
      if (local_1b0 != (long *)0x0) {
        LOAcquire();
        lVar4 = local_1b0[1];
        local_1b0[1] = lVar4 + -1;
        LORelease();
        if (lVar4 == 0) {
          (**(code **)(*local_1b0 + 0x10))(local_1b0);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
        }
      }
      goto LAB_030bd05c;
    }
  }
  iVar5 = thunk_FUN_05e1d97c(4);
  if (iVar5 != 0) {
    FUN_0488143c(local_1a8);
    pppuVar1 = (undefined8 ***)local_1a8[0];
    if (-1 < cStack_191) {
      pppuVar1 = local_1a8;
    }
    if ((DAT_0a3d86c9 & 1) == 0) {
      uVar6 = 0;
      do {
        (&DAT_0a3d86ad)[uVar6] = (&DAT_088ad3fc)[uVar6] + 0x8a ^ (&DAT_088ad3ec)[uVar6 & 0xf];
        uVar6 = uVar6 + 1;
      } while (uVar6 != 0x1c);
      DAT_0a3d86c9 = 1;
    }
    if ((DAT_0a3d86e8 & 1) == 0) {
      _DAT_0a3d86cc = CONCAT44((int)DAT_087e2df0,(int)ram0x087e2de8);
      uRam000000000a3d86d4 = CONCAT44((int)DAT_08546648,(int)ram0x084f0820);
      DAT_0a3d86dc = CONCAT44((int)DAT_0850ad18,(int)DAT_084b0670);
      DAT_0a3d86e4 = (undefined4)DAT_088a3be8;
      DAT_0a3d86e8 = 1;
    }
    FUN_05e1d050(&local_190,4,pppuVar1,&DAT_0a3d86ad,&DAT_0a3d86cc,0x18,0,0);
    if ((DAT_0a3d8702 & 1) == 0) {
      uVar6 = 0;
      do {
        (&DAT_0a3d86e9)[uVar6] = (&DAT_088ad458)[uVar6] + 0x8a ^ (&DAT_088ad448)[uVar6 & 0xf];
        uVar6 = uVar6 + 1;
      } while (uVar6 != 0x19);
      DAT_0a3d8702 = 1;
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
    local_e0 = (long *)0x0;
    uStack_c8 = 0;
    uStack_d0 = 0;
    FUN_05e1d31c(&local_190,&DAT_0a3d86e9,&local_e0);
    thunk_FUN_05e1d0bc(&local_190);
    if (cStack_191 < '\0') {
      __ZdlPvm(local_1a8[0],CONCAT17(cStack_191,local_198) & 0x7fffffffffffffff);
    }
  }
  FUN_030f6650(param_1,1,1,4,400);
LAB_030bd05c:
  plVar2 = local_f8;
  if (local_f8 != (long *)0x0) {
    LOAcquire();
    lVar4 = local_f8[1];
    local_f8[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*local_f8 + 0x10))(local_f8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  plVar2 = local_e8;
  if (local_e8 != (long *)0x0) {
    LOAcquire();
    lVar4 = local_e8[1];
    local_e8[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*local_e8 + 0x10))(local_e8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


