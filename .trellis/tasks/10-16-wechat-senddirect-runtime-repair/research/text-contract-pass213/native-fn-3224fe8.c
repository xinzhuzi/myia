// Ghidra inferred pseudocode; requested=0x3224fe8
// entry=03224fe8 end=032255af

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_03224fe8(int *param_1,undefined8 *param_2,undefined8 *param_3)

{
  undefined8 *******pppppppuVar1;
  long lVar2;
  int iVar3;
  undefined8 uVar4;
  ulong uVar5;
  long *plVar6;
  undefined8 local_1f8;
  long *local_1f0;
  undefined8 *******local_1e8 [2];
  undefined7 local_1d8;
  char cStack_1d1;
  undefined8 *******local_1d0 [2];
  undefined7 local_1c0;
  char cStack_1b9;
  undefined8 local_1b8;
  undefined8 local_1b0 [2];
  undefined7 local_1a0;
  char cStack_199;
  undefined8 local_198;
  long *local_190;
  undefined8 local_128;
  long *local_120;
  undefined8 *******local_118;
  undefined1 local_110;
  undefined8 *******local_c8;
  undefined8 local_c0;
  undefined8 uStack_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 local_60;
  undefined8 uStack_58;
  undefined8 local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  *(undefined1 **)(param_1 + 6) = &SUB_aaaaaaaaaaaaaaaa;
  *(undefined1 **)(param_1 + 4) = &SUB_aaaaaaaaaaaaaaaa;
  *(undefined1 **)(param_1 + 10) = &SUB_aaaaaaaaaaaaaaaa;
  *(undefined1 **)(param_1 + 8) = &SUB_aaaaaaaaaaaaaaaa;
  *(undefined1 **)(param_1 + 2) = &SUB_aaaaaaaaaaaaaaaa;
  *(undefined1 **)param_1 = &SUB_aaaaaaaaaaaaaaaa;
  uVar4 = *param_3;
  local_128 = *param_2;
  local_120 = (long *)param_2[1];
  if (local_120 != (long *)0x0) {
    local_120[1] = local_120[1] + 1;
  }
  FUN_030d66c0(param_1,uVar4,&local_128);
  plVar6 = local_120;
  if (local_120 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_120[1];
    local_120[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_120 + 0x10))(local_120);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  if (*param_1 == 0 && param_1[1] == 0) {
    FUN_030f3214(*param_2,10);
    uVar4 = *param_3;
    local_1f8 = *param_2;
    local_1f0 = (long *)param_2[1];
    if (local_1f0 != (long *)0x0) {
      local_1f0[1] = local_1f0[1] + 1;
    }
    FUN_030d692c(&local_1b8,uVar4,&local_1f8);
    *(undefined8 *)param_1 = local_1b8;
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_1 + 2,local_1b0);
    if (local_190 != (long *)0x0) {
      local_190[1] = local_190[1] + 1;
    }
    plVar6 = *(long **)(param_1 + 10);
    *(undefined8 *)(param_1 + 8) = local_198;
    *(long **)(param_1 + 10) = local_190;
    if (plVar6 != (long *)0x0) {
      LOAcquire();
      lVar2 = plVar6[1];
      plVar6[1] = lVar2 + -1;
      LORelease();
      if (lVar2 == 0) {
        (**(code **)(*plVar6 + 0x10))(plVar6);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
      }
    }
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
      __ZdlPvm(local_1b0[0],CONCAT17(cStack_199,local_1a0) & 0x7fffffffffffffff);
    }
    plVar6 = local_1f0;
    if (local_1f0 != (long *)0x0) {
      LOAcquire();
      lVar2 = local_1f0[1];
      local_1f0[1] = lVar2 + -1;
      LORelease();
      if (lVar2 == 0) {
        (**(code **)(*local_1f0 + 0x10))(local_1f0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
      }
    }
    if ((*param_1 == 0 && param_1[1] == 0) || (iVar3 = thunk_FUN_05e1d97c(4), iVar3 == 0))
    goto LAB_03225534;
    FUN_0488143c(local_1d0);
    pppppppuVar1 = local_1d0[0];
    if (-1 < cStack_1b9) {
      pppppppuVar1 = local_1d0;
    }
    if ((DAT_0a3dd363 & 1) == 0) {
      uVar5 = 0;
      do {
        (&DAT_0a3dd350)[uVar5] = (&DAT_088bce97)[uVar5] + 0x8a ^ (&DAT_088bce87)[uVar5 & 0xf];
        uVar5 = uVar5 + 1;
      } while (uVar5 != 0x13);
      DAT_0a3dd363 = 1;
    }
    if ((DAT_0a3e2ee3 & 1) == 0) {
      DAT_0a3e2ed4._4_1_ = s_StartScaoperatorh_op_084cadf8[8];
      DAT_0a3e2ed4._5_1_ = s_StartScaoperatorh_op_084cadf8[9];
      DAT_0a3e2ed4._6_1_ = s_StartScaoperatorh_op_084cadf8[10];
      DAT_0a3e2ed4._7_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
      DAT_0a3e2ed4_5._3_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
      DAT_0a3e2ed4_5._4_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
      DAT_0a3e2ed4_5._5_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
      DAT_0a3e2ed4_5._6_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
      DAT_0a3e2ee0 = 0x2928;
      DAT_0a3e2ee2 = 0;
      DAT_0a3e2ee3 = 1;
    }
    FUN_05e1d050(&local_1b8,4,pppppppuVar1,&DAT_0a3dd350,0xa3e2ed8,0x1113,0,0);
    FUN_030f1f08(local_1e8,*param_2);
    local_118 = local_1e8[0];
    if (-1 < cStack_1d1) {
      local_118 = local_1e8;
    }
    local_110 = 0;
    if ((DAT_0a3e0609 & 1) == 0) {
      _DAT_0a3e05e8 = CONCAT44((int)DAT_084ec280,(int)DAT_08486a48);
      uRam000000000a3e05f0 = CONCAT44((int)DAT_087e2f50,(int)DAT_084e3ff8);
      _DAT_0a3e05f8 = CONCAT44((int)DAT_084a8110,(int)DAT_088a7260);
      uRam000000000a3e0600 = CONCAT44((int)ram0x08480938,(int)DAT_08545158);
      DAT_0a3e0608 = 0;
      DAT_0a3e0609 = 1;
    }
    uStack_b8 = 0;
    local_c0 = 0;
    local_c8 = &local_118;
    uStack_a8 = 0;
    local_b0 = 0;
    uStack_98 = 0;
    local_a0 = 0;
    uStack_88 = 0;
    local_90 = 0;
    uStack_78 = 0;
    local_80 = 0;
    uStack_68 = 0;
    local_70 = 0;
    uStack_58 = 0;
    local_60 = 0;
    local_50 = 0;
    FUN_05e1d31c(&local_1b8,&DAT_0a3e05e8,&local_c8);
  }
  else {
    iVar3 = thunk_FUN_05e1d97c(4);
    if (iVar3 == 0) goto LAB_03225534;
    FUN_0488143c(local_1d0);
    pppppppuVar1 = local_1d0[0];
    if (-1 < cStack_1b9) {
      pppppppuVar1 = local_1d0;
    }
    if ((DAT_0a3dd363 & 1) == 0) {
      uVar5 = 0;
      do {
        (&DAT_0a3dd350)[uVar5] = (&DAT_088bce97)[uVar5] + 0x8a ^ (&DAT_088bce87)[uVar5 & 0xf];
        uVar5 = uVar5 + 1;
      } while (uVar5 != 0x13);
      DAT_0a3dd363 = 1;
    }
    if ((DAT_0a3e2ee3 & 1) == 0) {
      DAT_0a3e2ed4._4_1_ = s_StartScaoperatorh_op_084cadf8[8];
      DAT_0a3e2ed4._5_1_ = s_StartScaoperatorh_op_084cadf8[9];
      DAT_0a3e2ed4._6_1_ = s_StartScaoperatorh_op_084cadf8[10];
      DAT_0a3e2ed4._7_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
      DAT_0a3e2ed4_5._3_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
      DAT_0a3e2ed4_5._4_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
      DAT_0a3e2ed4_5._5_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
      DAT_0a3e2ed4_5._6_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
      DAT_0a3e2ee0 = 0x2928;
      DAT_0a3e2ee2 = 0;
      DAT_0a3e2ee3 = 1;
    }
    FUN_05e1d050(&local_1b8,4,pppppppuVar1,&DAT_0a3dd350,0xa3e2ed8,"",0,0);
    FUN_030f1f08(local_1e8,*param_2);
    local_118 = local_1e8[0];
    if (-1 < cStack_1d1) {
      local_118 = local_1e8;
    }
    local_110 = 0;
    if ((DAT_0a3e3470 & 1) == 0) {
      _DAT_0a3e344c = CONCAT44((int)DAT_084ec280,(int)DAT_08486a48);
      uRam000000000a3e3454 = CONCAT44((int)DAT_087e2e00,(int)DAT_084e3ff8);
      _DAT_0a3e345c = CONCAT44((int)DAT_085256f0,(int)ram0x0847fd88);
      uRam000000000a3e3464 = CONCAT44((int)DAT_0847fde0,(int)ram0x08491928);
      DAT_0a3e346c = (undefined4)DAT_0847fde8;
      DAT_0a3e3470 = 1;
    }
    uStack_b8 = 0;
    local_c0 = 0;
    local_c8 = &local_118;
    uStack_a8 = 0;
    local_b0 = 0;
    uStack_98 = 0;
    local_a0 = 0;
    uStack_88 = 0;
    local_90 = 0;
    uStack_78 = 0;
    local_80 = 0;
    uStack_68 = 0;
    local_70 = 0;
    uStack_58 = 0;
    local_60 = 0;
    local_50 = 0;
    FUN_05e1d31c(&local_1b8,&DAT_0a3e344c,&local_c8);
  }
  if (cStack_1d1 < '\0') {
    __ZdlPvm(local_1e8[0],CONCAT17(cStack_1d1,local_1d8) & 0x7fffffffffffffff);
  }
  thunk_FUN_05e1d0bc(&local_1b8);
  if (cStack_1b9 < '\0') {
    __ZdlPvm(local_1d0[0],CONCAT17(cStack_1b9,local_1c0) & 0x7fffffffffffffff);
  }
LAB_03225534:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


