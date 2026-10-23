// Ghidra inferred pseudocode; requested=0x453df64
// entry=0453df64 end=0453e44f

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0453df64(undefined8 *param_1,long ****param_2)

{
  undefined8 ****ppppuVar1;
  long ***ppplVar2;
  bool bVar3;
  int iVar4;
  undefined8 uVar5;
  long ****pppplVar6;
  long lVar7;
  long ***ppplVar8;
  long ***ppplVar9;
  long ***ppplVar10;
  void **ppvVar11;
  byte bVar12;
  undefined8 ***local_1c8 [2];
  undefined7 local_1b8;
  char cStack_1b1;
  void *local_1b0;
  long **pplStack_1a8;
  undefined8 local_1a0;
  long ***local_120;
  undefined1 local_118;
  undefined7 local_110;
  char cStack_109;
  long ***local_d0;
  undefined8 uStack_c8;
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
  undefined8 uStack_60;
  undefined8 local_58;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  iVar4 = thunk_FUN_05e1d97c(2);
  if (iVar4 != 0) {
    FUN_0488143c(local_1c8);
    ppppuVar1 = (undefined8 ****)local_1c8[0];
    if (-1 < cStack_1b1) {
      ppppuVar1 = local_1c8;
    }
    if ((DAT_0a455765 & 1) == 0) {
      DAT_0a455758._0_1_ = s_coroutinCoAsync_087e2ce0[0];
      DAT_0a455758._1_1_ = s_coroutinCoAsync_087e2ce0[1];
      DAT_0a455758._2_1_ = s_coroutinCoAsync_087e2ce0[2];
      DAT_0a455758._3_1_ = s_coroutinCoAsync_087e2ce0[3];
      DAT_0a455758._4_1_ = s_coroutinCoAsync_087e2ce0[4];
      DAT_0a455758._5_1_ = s_coroutinCoAsync_087e2ce0[5];
      DAT_0a455758._6_1_ = s_coroutinCoAsync_087e2ce0[6];
      DAT_0a455758._7_1_ = s_coroutinCoAsync_087e2ce0[7];
      DAT_0a455760 = (undefined4)DAT_084c8598;
      DAT_0a455764 = 0;
      DAT_0a455765 = 1;
    }
    if ((DAT_0a4557ef & 1) == 0) {
      DAT_0a4557e0._0_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x18];
      DAT_0a4557e0._1_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x19];
      DAT_0a4557e0._2_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x1a];
      DAT_0a4557e0._3_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x1b];
      DAT_0a4557e0._4_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x1c];
      DAT_0a4557e0._5_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x1d];
      DAT_0a4557e0._6_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x1e];
      DAT_0a4557e0._7_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x1f];
      DAT_0a4557e8 = (undefined4)DAT_0889c588;
      DAT_0a4557ec = 0x7265;
      DAT_0a4557ee = 0;
      DAT_0a4557ef = 1;
    }
    FUN_05e1d050(&local_1b0,2,ppppuVar1,&DAT_0a455758,&DAT_0a4557e0,0x119,0,0);
    local_120 = *param_2;
    if (-1 < *(char *)((long)param_2 + 0x17)) {
      local_120 = (long ***)param_2;
    }
    local_118 = 0;
    if ((DAT_0a45580f & 1) == 0) {
      _DAT_0a4557f0 = CONCAT44((int)DAT_087ec760,(int)DAT_087ec758);
      uRam000000000a4557f8 = CONCAT44((int)DAT_084e32c0,(int)DAT_0855bcb8);
      DAT_0a455800 = CONCAT44((int)DAT_085d97c0,(int)DAT_08484450);
      DAT_0a455808 = (undefined4)DAT_084d4a88;
      DAT_0a45580c = 0x5f25;
      DAT_0a45580e = 0;
      DAT_0a45580f = 1;
    }
    uStack_c0 = 0;
    uStack_c8 = 0;
    local_d0 = (long ***)&local_120;
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
    uStack_60 = 0;
    local_68 = 0;
    local_58 = 0;
    FUN_05e1d31c(&local_1b0,&DAT_0a4557f0,&local_d0);
    thunk_FUN_05e1d0bc(&local_1b0);
    if (cStack_1b1 < '\0') {
      __ZdlPvm(local_1c8[0],CONCAT17(cStack_1b1,local_1b8) & 0x7fffffffffffffff);
    }
  }
  bVar12 = *(byte *)((long)param_2 + 0x17);
  ppplVar9 = (long ***)(ulong)bVar12;
  ppplVar10 = param_2[1];
  ppplVar2 = ppplVar10;
  if (-1 < (char)bVar12) {
    ppplVar2 = ppplVar9;
  }
  lVar7 = param_1[2];
  if (ppplVar2 == (long ***)0x0) {
    if (lVar7 != 0) {
      FUN_0668272c(lVar7 + 8);
      FUN_066823c4(param_1[2] + 8);
      if ((long *)param_1[2] != (long *)0x0) {
        (**(code **)(*(long *)param_1[2] + 8))();
      }
      param_1[2] = 0;
    }
    goto LAB_0453e284;
  }
  if (lVar7 != 0) {
    if (*(char *)(lVar7 + 0xf7) < '\0') {
      FUN_00018d20(&local_1b0,*(undefined8 *)(lVar7 + 0xe0),*(undefined8 *)(lVar7 + 0xe8));
      bVar12 = *(byte *)((long)param_2 + 0x17);
      ppplVar9 = (long ***)(ulong)bVar12;
      ppplVar10 = param_2[1];
    }
    else {
      pplStack_1a8 = (long **)*(long ****)(lVar7 + 0xe8);
      local_1b0 = *(void **)(lVar7 + 0xe0);
      local_1a0 = *(ulong *)(lVar7 + 0xf0);
    }
    ppplVar8 = (long ***)(ulong)local_1a0._7_1_;
    ppplVar2 = (long ***)pplStack_1a8;
    if (-1 < (long)local_1a0) {
      ppplVar2 = ppplVar8;
    }
    if (-1 < (char)bVar12) {
      ppplVar10 = ppplVar9;
    }
    if (ppplVar2 == ppplVar10) {
      pppplVar6 = (long ****)*param_2;
      if (-1 < (char)bVar12) {
        pppplVar6 = param_2;
      }
      if ((long)local_1a0 < 0) {
        iVar4 = _memcmp(local_1b0,pppplVar6,(size_t)pplStack_1a8);
        bVar3 = iVar4 == 0;
        goto LAB_0453e2c4;
      }
      if (local_1a0._7_1_ != 0) {
        ppvVar11 = &local_1b0;
        do {
          ppplVar8 = (long ***)((long)ppplVar8 + -1);
          bVar3 = *(char *)ppvVar11 == *(char *)pppplVar6;
          if (!bVar3) break;
          pppplVar6 = (long ****)((long)pppplVar6 + 1);
          ppvVar11 = (void **)((long)ppvVar11 + 1);
        } while (ppplVar8 != (long ***)0x0);
        goto LAB_0453e248;
      }
LAB_0453e2d8:
      iVar4 = thunk_FUN_05e1d97c(4);
      if (iVar4 != 0) {
        FUN_0488143c(&local_120);
        pppplVar6 = (long ****)local_120;
        if (-1 < cStack_109) {
          pppplVar6 = &local_120;
        }
        if ((DAT_0a455765 & 1) == 0) {
          DAT_0a455758._0_1_ = s_coroutinCoAsync_087e2ce0[0];
          DAT_0a455758._1_1_ = s_coroutinCoAsync_087e2ce0[1];
          DAT_0a455758._2_1_ = s_coroutinCoAsync_087e2ce0[2];
          DAT_0a455758._3_1_ = s_coroutinCoAsync_087e2ce0[3];
          DAT_0a455758._4_1_ = s_coroutinCoAsync_087e2ce0[4];
          DAT_0a455758._5_1_ = s_coroutinCoAsync_087e2ce0[5];
          DAT_0a455758._6_1_ = s_coroutinCoAsync_087e2ce0[6];
          DAT_0a455758._7_1_ = s_coroutinCoAsync_087e2ce0[7];
          DAT_0a455760 = (undefined4)DAT_084c8598;
          DAT_0a455764 = 0;
          DAT_0a455765 = 1;
        }
        if ((DAT_0a4557ef & 1) == 0) {
          DAT_0a4557e0._0_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x18];
          DAT_0a4557e0._1_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x19];
          DAT_0a4557e0._2_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x1a];
          DAT_0a4557e0._3_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x1b];
          DAT_0a4557e0._4_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x1c];
          DAT_0a4557e0._5_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x1d];
          DAT_0a4557e0._6_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x1e];
          DAT_0a4557e0._7_1_ = s_dummy_jocoLaunchfrom_unkSetCurre_089feb88[0x1f];
          DAT_0a4557e8 = (undefined4)DAT_0889c588;
          DAT_0a4557ec = 0x7265;
          DAT_0a4557ee = 0;
          DAT_0a4557ef = 1;
        }
        FUN_05e1d050(&local_1b0,4,pppplVar6,&DAT_0a455758,&DAT_0a4557e0,0x11d,0,0);
        if ((DAT_0a455826 & 1) == 0) {
          _DAT_0a455810 = CONCAT44((int)DAT_08480a78,(int)DAT_087f8a10);
          uRam000000000a455818 = CONCAT44((int)DAT_084f5f40,(int)DAT_084998c0);
          DAT_0a455820 = (undefined4)DAT_084f5f48;
          DAT_0a455824 = 0x65;
          DAT_0a455826 = 1;
        }
        local_68 = 0;
        uStack_70 = 0;
        local_58 = 0;
        uStack_60 = 0;
        local_88 = 0;
        uStack_90 = 0;
        local_78 = 0;
        uStack_80 = 0;
        local_a8 = 0;
        uStack_b0 = 0;
        local_98 = 0;
        uStack_a0 = 0;
        uStack_c8 = 0;
        local_d0 = (long ***)0x0;
        local_b8 = 0;
        uStack_c0 = 0;
        FUN_05e1d31c(&local_1b0,&DAT_0a455810,&local_d0);
        thunk_FUN_05e1d0bc(&local_1b0);
        if (cStack_109 < '\0') {
          __ZdlPvm(local_120,CONCAT17(cStack_109,local_110) & 0x7fffffffffffffff);
        }
      }
      goto LAB_0453e284;
    }
    bVar3 = false;
LAB_0453e248:
    if ((long)local_1a0 < 0) {
LAB_0453e2c4:
      __ZdlPvm(local_1b0,local_1a0 & 0x7fffffffffffffff);
      if (bVar3) goto LAB_0453e2d8;
    }
    else if (bVar3) goto LAB_0453e2d8;
  }
  uVar5 = __Znwm(0x148);
  FUN_066845d0(uVar5,param_2);
  param_1[2] = uVar5;
  FUN_0668467c(uVar5,param_1[1]);
  uVar5 = *param_1;
  lVar7 = FUN_02e0a888(param_1[2]);
  *(undefined8 *)(lVar7 + 0x18) = uVar5;
LAB_0453e284:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


