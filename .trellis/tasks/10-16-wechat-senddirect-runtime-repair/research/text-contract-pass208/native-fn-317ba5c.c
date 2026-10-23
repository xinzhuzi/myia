// Ghidra inferred pseudocode; requested=0x317ba5c
// entry=0317ba5c end=0317c2e3

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0317ba5c(long param_1)

{
  undefined8 *****pppppuVar1;
  long *plVar2;
  long *plVar3;
  long lVar4;
  int iVar5;
  long lVar6;
  ulong uVar7;
  long *plVar8;
  long local_1c8;
  long *local_1c0;
  long local_1b8;
  long *local_1b0;
  undefined8 ****local_1a8;
  long *local_1a0;
  undefined7 local_198;
  char cStack_191;
  long local_190;
  code *pcStack_188;
  code *local_180;
  undefined8 uStack_178;
  code *local_170;
  undefined8 local_100;
  long lStack_f8;
  undefined8 local_f0;
  long local_e8;
  undefined8 local_e0;
  undefined8 uStack_d8;
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
  long local_78;
  
  local_78 = *(long *)PTR____stack_chk_guard_09b36c98;
  iVar5 = thunk_FUN_05e1d97c(2);
  if (iVar5 != 0) {
    FUN_0488143c(&local_1a8);
    pppppuVar1 = (undefined8 *****)local_1a8;
    if (-1 < cStack_191) {
      pppppuVar1 = &local_1a8;
    }
    if ((DAT_0a3dd363 & 1) == 0) {
      uVar7 = 0;
      do {
        (&DAT_0a3dd350)[uVar7] = (&DAT_088bce97)[uVar7] + 0x8a ^ (&DAT_088bce87)[uVar7 & 0xf];
        uVar7 = uVar7 + 1;
      } while (uVar7 != 0x13);
      DAT_0a3dd363 = 1;
    }
    if ((DAT_0a3de2fd & 1) == 0) {
      DAT_0a3de2f0._0_1_ = s_InitHandlers_088ba990[0];
      DAT_0a3de2f0._1_1_ = s_InitHandlers_088ba990[1];
      DAT_0a3de2f0._2_1_ = s_InitHandlers_088ba990[2];
      DAT_0a3de2f0._3_1_ = s_InitHandlers_088ba990[3];
      DAT_0a3de2f0._4_1_ = s_InitHandlers_088ba990[4];
      DAT_0a3de2f0._5_1_ = s_InitHandlers_088ba990[5];
      DAT_0a3de2f0._6_1_ = s_InitHandlers_088ba990[6];
      DAT_0a3de2f0._7_1_ = s_InitHandlers_088ba990[7];
      DAT_0a3de2f8 = (undefined4)ram0x088ba998;
      DAT_0a3de2fc = 0;
      DAT_0a3de2fd = 1;
    }
    FUN_05e1d050(&local_190,2,pppppuVar1,&DAT_0a3dd350,&DAT_0a3de2f0,0x62a,0,0);
    if ((DAT_0a3de2fd & 1) == 0) {
      DAT_0a3de2f0._0_1_ = s_InitHandlers_088ba990[0];
      DAT_0a3de2f0._1_1_ = s_InitHandlers_088ba990[1];
      DAT_0a3de2f0._2_1_ = s_InitHandlers_088ba990[2];
      DAT_0a3de2f0._3_1_ = s_InitHandlers_088ba990[3];
      DAT_0a3de2f0._4_1_ = s_InitHandlers_088ba990[4];
      DAT_0a3de2f0._5_1_ = s_InitHandlers_088ba990[5];
      DAT_0a3de2f0._6_1_ = s_InitHandlers_088ba990[6];
      DAT_0a3de2f0._7_1_ = s_InitHandlers_088ba990[7];
      DAT_0a3de2f8 = (undefined4)ram0x088ba998;
      DAT_0a3de2fc = 0;
      DAT_0a3de2fd = 1;
    }
    uStack_98 = 0;
    local_a0 = 0;
    uStack_88 = 0;
    uStack_90 = 0;
    uStack_b8 = 0;
    local_c0 = 0;
    uStack_a8 = 0;
    uStack_b0 = 0;
    uStack_d8 = 0;
    local_e0 = 0;
    uStack_c8 = 0;
    uStack_d0 = 0;
    lStack_f8 = 0;
    local_100 = 0;
    local_e8 = 0;
    local_f0 = 0;
    FUN_05e1d31c(&local_190,&DAT_0a3de2f0,&local_100);
    thunk_FUN_05e1d0bc(&local_190);
    if (cStack_191 < '\0') {
      __ZdlPvm(local_1a8,CONCAT17(cStack_191,local_198) & 0x7fffffffffffffff);
    }
  }
  local_100 = *(undefined8 *)(param_1 + 0xb78);
  lStack_f8 = *(long *)(param_1 + 0xb80);
  if (lStack_f8 != 0) {
    *(long *)(lStack_f8 + 0x10) = *(long *)(lStack_f8 + 0x10) + 1;
  }
  lVar6 = *(long *)(param_1 + 0xb20);
  local_f0 = *(undefined8 *)(lVar6 + 0x148);
  local_e8 = *(long *)(lVar6 + 0x150);
  lVar4 = 0;
  if (local_e8 != 0) {
    lVar4 = *(long *)(local_e8 + 0x10);
    *(long *)(local_e8 + 0x10) = lVar4 + 1;
    lVar6 = *(long *)(param_1 + 0xb20);
  }
  FUN_030e3fb0(lVar4,lVar6,lVar6 + 0x28,&local_100);
  for (plVar8 = *(long **)(*(long *)(param_1 + 0xb20) + 0x10); plVar8 != (long *)0x0;
      plVar8 = (long *)*plVar8) {
    lVar4 = plVar8[5];
    FUN_04669774();
    FUN_0466ad74(&local_1b8);
    pcStack_188 = FUN_03213a30;
    local_180 = FUN_0317d1cc;
    uStack_178 = 0;
    local_170 = FUN_03213a4c;
    local_1a8 = (undefined8 ****)0x0;
    local_1a0 = (long *)0x0;
    local_190 = param_1;
    FUN_06686420(lVar4 + 0x18,&local_190,0,0,*(undefined8 *)(local_1b8 + 0x10),&local_1a8);
    plVar3 = local_1a0;
    plVar2 = local_1b0;
    if (local_1a0 != (long *)0x0) {
      LOAcquire();
      lVar4 = local_1a0[1];
      local_1a0[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*local_1a0 + 0x10))(local_1a0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
        plVar2 = local_1b0;
      }
    }
    local_1b0 = plVar2;
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
    lVar4 = plVar8[5];
    FUN_04669774();
    FUN_0466ad74(&local_1b8);
    pcStack_188 = FUN_03213a74;
    local_180 = FUN_0317d4ac;
    uStack_178 = 0;
    local_170 = FUN_03213a94;
    local_1a8 = (undefined8 ****)0x0;
    local_1a0 = (long *)0x0;
    local_190 = param_1;
    FUN_06686420(lVar4 + 0x90,&local_190,0,0,*(undefined8 *)(local_1b8 + 0x10),&local_1a8);
    plVar3 = local_1a0;
    plVar2 = local_1b0;
    if (local_1a0 != (long *)0x0) {
      LOAcquire();
      lVar4 = local_1a0[1];
      local_1a0[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*local_1a0 + 0x10))(local_1a0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
        plVar2 = local_1b0;
      }
    }
    local_1b0 = plVar2;
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
    lVar4 = plVar8[5];
    FUN_04669774();
    FUN_0466ad74(&local_1b8);
    pcStack_188 = FUN_03213a30;
    local_180 = FUN_0317d4b4;
    uStack_178 = 0;
    local_170 = FUN_03213a4c;
    local_1a8 = (undefined8 ****)0x0;
    local_1a0 = (long *)0x0;
    local_190 = param_1;
    FUN_06686420(lVar4 + 0x108,&local_190,0,0,*(undefined8 *)(local_1b8 + 0x10),&local_1a8);
    plVar3 = local_1a0;
    plVar2 = local_1b0;
    if (local_1a0 != (long *)0x0) {
      LOAcquire();
      lVar4 = local_1a0[1];
      local_1a0[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*local_1a0 + 0x10))(local_1a0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
        plVar2 = local_1b0;
      }
    }
    local_1b0 = plVar2;
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
    lVar4 = plVar8[5];
    FUN_04669774();
    FUN_0466ad74(&local_1b8);
    pcStack_188 = FUN_03213abc;
    local_180 = FUN_0317d4bc;
    uStack_178 = 0;
    local_170 = FUN_03213adc;
    local_1a8 = (undefined8 ****)0x0;
    local_1a0 = (long *)0x0;
    local_190 = param_1;
    FUN_06686420(lVar4 + 0x180,&local_190,0,0,*(undefined8 *)(local_1b8 + 0x10),&local_1a8);
    plVar3 = local_1a0;
    plVar2 = local_1b0;
    if (local_1a0 != (long *)0x0) {
      LOAcquire();
      lVar4 = local_1a0[1];
      local_1a0[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*local_1a0 + 0x10))(local_1a0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
        plVar2 = local_1b0;
      }
    }
    local_1b0 = plVar2;
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
    lVar4 = plVar8[5];
    FUN_04669774();
    FUN_0466ad74(&local_1b8);
    pcStack_188 = FUN_03213b04;
    local_180 = FUN_0317d644;
    uStack_178 = 0;
    local_170 = FUN_03213b24;
    local_1a8 = (undefined8 ****)0x0;
    local_1a0 = (long *)0x0;
    local_190 = param_1;
    FUN_06686420(lVar4 + 0x1f8,&local_190,0,0,*(undefined8 *)(local_1b8 + 0x10),&local_1a8);
    plVar3 = local_1a0;
    plVar2 = local_1b0;
    if (local_1a0 != (long *)0x0) {
      LOAcquire();
      lVar4 = local_1a0[1];
      local_1a0[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*local_1a0 + 0x10))(local_1a0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
        plVar2 = local_1b0;
      }
    }
    local_1b0 = plVar2;
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
    lVar4 = plVar8[5];
    FUN_04669774();
    FUN_0466ad74(&local_1b8);
    pcStack_188 = FUN_03213b4c;
    local_180 = FUN_0317dba0;
    uStack_178 = 0;
    local_170 = FUN_03213b68;
    local_1a8 = (undefined8 ****)0x0;
    local_1a0 = (long *)0x0;
    local_190 = param_1;
    FUN_06686420(lVar4 + 0x270,&local_190,0,0,*(undefined8 *)(local_1b8 + 0x10),&local_1a8);
    plVar3 = local_1a0;
    plVar2 = local_1b0;
    if (local_1a0 != (long *)0x0) {
      LOAcquire();
      lVar4 = local_1a0[1];
      local_1a0[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*local_1a0 + 0x10))(local_1a0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
        plVar2 = local_1b0;
      }
    }
    local_1b0 = plVar2;
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
    lVar4 = plVar8[5];
    FUN_04669774();
    FUN_0466ad74(&local_1b8);
    pcStack_188 = FUN_03213b90;
    local_180 = FUN_0317dec4;
    uStack_178 = 0;
    local_170 = FUN_03213bac;
    local_1a8 = (undefined8 *****)0x0;
    local_1a0 = (long *)0x0;
    local_190 = param_1;
    FUN_06686420(lVar4 + 0x2e8,&local_190,0,0,*(undefined8 *)(local_1b8 + 0x10),&local_1a8);
    plVar3 = local_1a0;
    plVar2 = local_1b0;
    if (local_1a0 != (long *)0x0) {
      LOAcquire();
      lVar4 = local_1a0[1];
      local_1a0[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*local_1a0 + 0x10))(local_1a0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
        plVar2 = local_1b0;
      }
    }
    local_1b0 = plVar2;
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
    if ((plVar8[5] != 0) &&
       (lVar4 = ___dynamic_cast(plVar8[5],&PTR_DAT_09de8868,&PTR_DAT_09dea1c8,0), lVar4 != 0)) {
      local_1b0 = (long *)plVar8[6];
      lVar6 = 0;
      if (local_1b0 != (long *)0x0) {
        lVar6 = local_1b0[1];
        local_1b0[1] = lVar6 + 1;
      }
      local_1b8 = lVar4;
      FUN_04669774(lVar6);
      FUN_0466ad74(&local_1c8);
      pcStack_188 = FUN_03213bd4;
      local_180 = FUN_0317decc;
      uStack_178 = 0;
      local_170 = FUN_03213bf4;
      local_1a8 = (undefined8 *****)0x0;
      local_1a0 = (long *)0x0;
      local_190 = param_1;
      FUN_06686420(lVar4 + 0x380,&local_190,0,0,*(undefined8 *)(local_1c8 + 0x10),&local_1a8);
      plVar3 = local_1a0;
      plVar2 = local_1c0;
      if (local_1a0 != (long *)0x0) {
        LOAcquire();
        lVar4 = local_1a0[1];
        local_1a0[1] = lVar4 + -1;
        LORelease();
        if (lVar4 == 0) {
          (**(code **)(*local_1a0 + 0x10))(local_1a0);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
          plVar2 = local_1c0;
        }
      }
      local_1c0 = plVar2;
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
    }
  }
  if (local_e8 != 0) {
    __ZNSt3__119__shared_weak_count14__release_weakEv();
  }
  if (lStack_f8 != 0) {
    __ZNSt3__119__shared_weak_count14__release_weakEv();
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_78) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


