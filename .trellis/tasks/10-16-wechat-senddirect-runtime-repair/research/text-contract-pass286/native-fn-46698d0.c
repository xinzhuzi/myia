// Ghidra inferred pseudocode; requested=0x46698d0
// entry=046698d0 end=0466a26b

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_046698d0(long param_1)

{
  undefined8 *******pppppppuVar1;
  long *plVar2;
  long lVar3;
  int iVar4;
  long lVar5;
  long *plVar6;
  undefined8 *******local_198 [2];
  undefined7 local_188;
  char cStack_181;
  long *local_180;
  long *plStack_178;
  undefined8 local_f0;
  undefined8 uStack_e8;
  undefined8 uStack_e0;
  undefined8 uStack_d8;
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
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  iVar4 = thunk_FUN_05e1d97c(2);
  if (iVar4 != 0) {
    FUN_0488143c(local_198);
    pppppppuVar1 = local_198[0];
    if (-1 < cStack_181) {
      pppppppuVar1 = local_198;
    }
    if ((DAT_0a45df8a & 1) == 0) {
      DAT_0a45df80._0_1_ = s_input_ackernel_cpadV_08a133a0[8];
      DAT_0a45df80._1_1_ = s_input_ackernel_cpadV_08a133a0[9];
      DAT_0a45df80._2_1_ = s_input_ackernel_cpadV_08a133a0[10];
      DAT_0a45df80._3_1_ = s_input_ackernel_cpadV_08a133a0[0xb];
      DAT_0a45df80._4_1_ = s_input_ackernel_cpadV_08a133a0[0xc];
      DAT_0a45df80._5_1_ = s_input_ackernel_cpadV_08a133a0[0xd];
      DAT_0a45df80._6_1_ = s_input_ackernel_cpadV_08a133a0[0xe];
      DAT_0a45df80._7_1_ = s_input_ackernel_cpadV_08a133a0[0xf];
      DAT_0a45df88 = 99;
      DAT_0a45df8a = 1;
    }
    if ((DAT_0a45dfea & 1) == 0) {
      DAT_0a45dfe0._0_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x10];
      DAT_0a45dfe0._1_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x11];
      DAT_0a45dfe0._2_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x12];
      DAT_0a45dfe0._3_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x13];
      DAT_0a45dfe0._4_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x14];
      DAT_0a45dfe0._5_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x15];
      DAT_0a45dfe0._6_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x16];
      DAT_0a45dfe0._7_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x17];
      DAT_0a45dfe8 = 0x65;
      DAT_0a45dfea = 1;
    }
    FUN_05e1d050(&local_180,2,pppppppuVar1,&DAT_0a45df80,&DAT_0a45dfe0,0xe3,0,0);
    if ((DAT_0a45dffd & 1) == 0) {
      DAT_0a45dff0._0_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x18];
      DAT_0a45dff0._1_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x19];
      DAT_0a45dff0._2_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x1a];
      DAT_0a45dff0._3_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x1b];
      DAT_0a45dff0._4_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x1c];
      DAT_0a45dff0._5_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x1d];
      DAT_0a45dff0._6_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x1e];
      DAT_0a45dff0._7_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x1f];
      DAT_0a45dff8 = (undefined4)DAT_084d82e8;
      DAT_0a45dffc = 0;
      DAT_0a45dffd = 1;
    }
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
    uStack_e8 = 0;
    local_f0 = 0;
    uStack_d8 = 0;
    uStack_e0 = 0;
    FUN_05e1d31c(&local_180,&DAT_0a45dff0,&local_f0);
    thunk_FUN_05e1d0bc(&local_180);
    if (cStack_181 < '\0') {
      __ZdlPvm(local_198[0],CONCAT17(cStack_181,local_188) & 0x7fffffffffffffff);
    }
  }
  FUN_022166d0();
  iVar4 = thunk_FUN_05e1d97c(2);
  if (iVar4 != 0) {
    FUN_0488143c(local_198);
    pppppppuVar1 = local_198[0];
    if (-1 < cStack_181) {
      pppppppuVar1 = local_198;
    }
    if ((DAT_0a45df8a & 1) == 0) {
      DAT_0a45df80._0_1_ = s_input_ackernel_cpadV_08a133a0[8];
      DAT_0a45df80._1_1_ = s_input_ackernel_cpadV_08a133a0[9];
      DAT_0a45df80._2_1_ = s_input_ackernel_cpadV_08a133a0[10];
      DAT_0a45df80._3_1_ = s_input_ackernel_cpadV_08a133a0[0xb];
      DAT_0a45df80._4_1_ = s_input_ackernel_cpadV_08a133a0[0xc];
      DAT_0a45df80._5_1_ = s_input_ackernel_cpadV_08a133a0[0xd];
      DAT_0a45df80._6_1_ = s_input_ackernel_cpadV_08a133a0[0xe];
      DAT_0a45df80._7_1_ = s_input_ackernel_cpadV_08a133a0[0xf];
      DAT_0a45df88 = 99;
      DAT_0a45df8a = 1;
    }
    if ((DAT_0a45dfea & 1) == 0) {
      DAT_0a45dfe0._0_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x10];
      DAT_0a45dfe0._1_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x11];
      DAT_0a45dfe0._2_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x12];
      DAT_0a45dfe0._3_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x13];
      DAT_0a45dfe0._4_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x14];
      DAT_0a45dfe0._5_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x15];
      DAT_0a45dfe0._6_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x16];
      DAT_0a45dfe0._7_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x17];
      DAT_0a45dfe8 = 0x65;
      DAT_0a45dfea = 1;
    }
    FUN_05e1d050(&local_180,2,pppppppuVar1,&DAT_0a45df80,&DAT_0a45dfe0,0xe9,0,0);
    if ((DAT_0a45e01b & 1) == 0) {
      _DAT_0a45e000 = CONCAT44((int)DAT_08647248,(int)ram0x08a13408);
      uRam000000000a45e008 = CONCAT44((int)DAT_0848d498,(int)DAT_08558ee8);
      DAT_0a45e010 = CONCAT44((int)DAT_08a13410,(int)ram0x085635e0);
      DAT_0a45e018 = 0x6574;
      DAT_0a45e01a = 0;
      DAT_0a45e01b = 1;
    }
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
    uStack_e8 = 0;
    local_f0 = 0;
    uStack_d8 = 0;
    uStack_e0 = 0;
    FUN_05e1d31c(&local_180,&DAT_0a45e000,&local_f0);
    thunk_FUN_05e1d0bc(&local_180);
    if (cStack_181 < '\0') {
      __ZdlPvm(local_198[0],CONCAT17(cStack_181,local_188) & 0x7fffffffffffffff);
    }
  }
  lVar5 = FUN_0001accc(*(undefined8 *)(param_1 + 0x78));
  for (plVar6 = *(long **)(lVar5 + 0x10); plVar6 != (long *)0x0; plVar6 = (long *)*plVar6) {
    local_180 = (long *)plVar6[5];
    plVar2 = (long *)plVar6[6];
    if (plVar2 != (long *)0x0) {
      plVar2[1] = plVar2[1] + 1;
    }
    *(undefined4 *)((long)local_180 + 0x1c) = 2;
    plStack_178 = plVar2;
    (**(code **)(*local_180 + 0x30))();
    if (plVar2 != (long *)0x0) {
      LOAcquire();
      lVar5 = plVar2[1];
      plVar2[1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*plVar2 + 0x10))(plVar2);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
      }
    }
  }
  iVar4 = thunk_FUN_05e1d97c(2);
  if (iVar4 != 0) {
    FUN_0488143c(local_198);
    pppppppuVar1 = local_198[0];
    if (-1 < cStack_181) {
      pppppppuVar1 = local_198;
    }
    if ((DAT_0a45df8a & 1) == 0) {
      DAT_0a45df80._0_1_ = s_input_ackernel_cpadV_08a133a0[8];
      DAT_0a45df80._1_1_ = s_input_ackernel_cpadV_08a133a0[9];
      DAT_0a45df80._2_1_ = s_input_ackernel_cpadV_08a133a0[10];
      DAT_0a45df80._3_1_ = s_input_ackernel_cpadV_08a133a0[0xb];
      DAT_0a45df80._4_1_ = s_input_ackernel_cpadV_08a133a0[0xc];
      DAT_0a45df80._5_1_ = s_input_ackernel_cpadV_08a133a0[0xd];
      DAT_0a45df80._6_1_ = s_input_ackernel_cpadV_08a133a0[0xe];
      DAT_0a45df80._7_1_ = s_input_ackernel_cpadV_08a133a0[0xf];
      DAT_0a45df88 = 99;
      DAT_0a45df8a = 1;
    }
    if ((DAT_0a45dfea & 1) == 0) {
      DAT_0a45dfe0._0_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x10];
      DAT_0a45dfe0._1_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x11];
      DAT_0a45dfe0._2_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x12];
      DAT_0a45dfe0._3_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x13];
      DAT_0a45dfe0._4_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x14];
      DAT_0a45dfe0._5_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x15];
      DAT_0a45dfe0._6_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x16];
      DAT_0a45dfe0._7_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x17];
      DAT_0a45dfe8 = 0x65;
      DAT_0a45dfea = 1;
    }
    FUN_05e1d050(&local_180,2,pppppppuVar1,&DAT_0a45df80,&DAT_0a45dfe0,0xf2,0,0);
    if ((DAT_0a45e033 & 1) == 0) {
      uRam000000000a45e028._0_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[8];
      uRam000000000a45e028._1_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[9];
      uRam000000000a45e028._2_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[10];
      uRam000000000a45e028._3_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0xb];
      uRam000000000a45e028._4_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0xc];
      uRam000000000a45e028._5_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0xd];
      uRam000000000a45e028._6_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0xe];
      uRam000000000a45e028._7_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0xf];
      DAT_0a45e020 = s_3_coroutine_uninSetWordingsProdu_08a135a0[0];
      DAT_0a45e020_1._0_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[1];
      DAT_0a45e020_1._1_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[2];
      DAT_0a45e020_1._2_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[3];
      DAT_0a45e020_1._3_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[4];
      DAT_0a45e020_1._4_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[5];
      DAT_0a45e020_1._5_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[6];
      DAT_0a45e020_1._6_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[7];
      DAT_0a45e030 = 0x7469;
      DAT_0a45e032 = 0;
      DAT_0a45e033 = 1;
    }
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
    uStack_e8 = 0;
    local_f0 = 0;
    uStack_d8 = 0;
    uStack_e0 = 0;
    FUN_05e1d31c(&local_180,&DAT_0a45e020,&local_f0);
    thunk_FUN_05e1d0bc(&local_180);
    if (cStack_181 < '\0') {
      __ZdlPvm(local_198[0],CONCAT17(cStack_181,local_188) & 0x7fffffffffffffff);
    }
  }
  FUN_0453e904(*(undefined8 *)(param_1 + 0x290));
  iVar4 = thunk_FUN_05e1d97c(2);
  if (iVar4 != 0) {
    FUN_0488143c(local_198);
    pppppppuVar1 = local_198[0];
    if (-1 < cStack_181) {
      pppppppuVar1 = local_198;
    }
    if ((DAT_0a45df8a & 1) == 0) {
      DAT_0a45df80._0_1_ = s_input_ackernel_cpadV_08a133a0[8];
      DAT_0a45df80._1_1_ = s_input_ackernel_cpadV_08a133a0[9];
      DAT_0a45df80._2_1_ = s_input_ackernel_cpadV_08a133a0[10];
      DAT_0a45df80._3_1_ = s_input_ackernel_cpadV_08a133a0[0xb];
      DAT_0a45df80._4_1_ = s_input_ackernel_cpadV_08a133a0[0xc];
      DAT_0a45df80._5_1_ = s_input_ackernel_cpadV_08a133a0[0xd];
      DAT_0a45df80._6_1_ = s_input_ackernel_cpadV_08a133a0[0xe];
      DAT_0a45df80._7_1_ = s_input_ackernel_cpadV_08a133a0[0xf];
      DAT_0a45df88 = 99;
      DAT_0a45df8a = 1;
    }
    if ((DAT_0a45dfea & 1) == 0) {
      DAT_0a45dfe0._0_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x10];
      DAT_0a45dfe0._1_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x11];
      DAT_0a45dfe0._2_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x12];
      DAT_0a45dfe0._3_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x13];
      DAT_0a45dfe0._4_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x14];
      DAT_0a45dfe0._5_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x15];
      DAT_0a45dfe0._6_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x16];
      DAT_0a45dfe0._7_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x17];
      DAT_0a45dfe8 = 0x65;
      DAT_0a45dfea = 1;
    }
    FUN_05e1d050(&local_180,2,pppppppuVar1,&DAT_0a45df80,&DAT_0a45dfe0,0xf7,0,0);
    if ((DAT_0a45e046 & 1) == 0) {
      DAT_0a45e038._0_1_ = s_4_mars_u5_vi_08a13418[0];
      DAT_0a45e038._1_1_ = s_4_mars_u5_vi_08a13418[1];
      DAT_0a45e038._2_1_ = s_4_mars_u5_vi_08a13418[2];
      DAT_0a45e038._3_1_ = s_4_mars_u5_vi_08a13418[3];
      DAT_0a45e038._4_1_ = s_4_mars_u5_vi_08a13418[4];
      DAT_0a45e038._5_1_ = s_4_mars_u5_vi_08a13418[5];
      DAT_0a45e038._6_1_ = s_4_mars_u5_vi_08a13418[6];
      DAT_0a45e038._7_1_ = s_4_mars_u5_vi_08a13418[7];
      DAT_0a45e040 = (undefined4)DAT_084e3338;
      DAT_0a45e044 = 0x74;
      DAT_0a45e046 = 1;
    }
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
    uStack_e8 = 0;
    local_f0 = 0;
    uStack_d8 = 0;
    uStack_e0 = 0;
    FUN_05e1d31c(&local_180,&DAT_0a45e038,&local_f0);
    thunk_FUN_05e1d0bc(&local_180);
    if (cStack_181 < '\0') {
      __ZdlPvm(local_198[0],CONCAT17(cStack_181,local_188) & 0x7fffffffffffffff);
    }
  }
  (**(code **)**(undefined8 **)(param_1 + 0x250))();
  (**(code **)**(undefined8 **)(param_1 + 0x260))();
  iVar4 = thunk_FUN_05e1d97c(2);
  if (iVar4 != 0) {
    FUN_0488143c(local_198);
    pppppppuVar1 = local_198[0];
    if (-1 < cStack_181) {
      pppppppuVar1 = local_198;
    }
    if ((DAT_0a45df8a & 1) == 0) {
      DAT_0a45df80._0_1_ = s_input_ackernel_cpadV_08a133a0[8];
      DAT_0a45df80._1_1_ = s_input_ackernel_cpadV_08a133a0[9];
      DAT_0a45df80._2_1_ = s_input_ackernel_cpadV_08a133a0[10];
      DAT_0a45df80._3_1_ = s_input_ackernel_cpadV_08a133a0[0xb];
      DAT_0a45df80._4_1_ = s_input_ackernel_cpadV_08a133a0[0xc];
      DAT_0a45df80._5_1_ = s_input_ackernel_cpadV_08a133a0[0xd];
      DAT_0a45df80._6_1_ = s_input_ackernel_cpadV_08a133a0[0xe];
      DAT_0a45df80._7_1_ = s_input_ackernel_cpadV_08a133a0[0xf];
      DAT_0a45df88 = 99;
      DAT_0a45df8a = 1;
    }
    if ((DAT_0a45dfea & 1) == 0) {
      DAT_0a45dfe0._0_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x10];
      DAT_0a45dfe0._1_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x11];
      DAT_0a45dfe0._2_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x12];
      DAT_0a45dfe0._3_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x13];
      DAT_0a45dfe0._4_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x14];
      DAT_0a45dfe0._5_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x15];
      DAT_0a45dfe0._6_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x16];
      DAT_0a45dfe0._7_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x17];
      DAT_0a45dfe8 = 0x65;
      DAT_0a45dfea = 1;
    }
    FUN_05e1d050(&local_180,2,pppppppuVar1,&DAT_0a45df80,&DAT_0a45dfe0,0xfd,0,0);
    if ((DAT_0a45e05d & 1) == 0) {
      _DAT_0a45e048 = CONCAT44((int)DAT_0863b300,(int)ram0x08a13420);
      uRam000000000a45e050 = CONCAT44((int)DAT_0882c038,(int)DAT_084a5870);
      DAT_0a45e058 = (undefined4)DAT_084d82e8;
      DAT_0a45e05c = 0;
      DAT_0a45e05d = 1;
    }
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
    uStack_e8 = 0;
    local_f0 = 0;
    uStack_d8 = 0;
    uStack_e0 = 0;
    FUN_05e1d31c(&local_180,&DAT_0a45e048,&local_f0);
    thunk_FUN_05e1d0bc(&local_180);
    if (cStack_181 < '\0') {
      __ZdlPvm(local_198[0],CONCAT17(cStack_181,local_188) & 0x7fffffffffffffff);
    }
  }
  if (((DAT_0a05a718 & 1) == 0) && (iVar4 = ___cxa_guard_acquire(&DAT_0a05a718), iVar4 != 0)) {
    FUN_046774f0(&DAT_0a05a660);
    ___cxa_atexit(thunk_FUN_04677558,&DAT_0a05a660,0);
    ___cxa_guard_release(&DAT_0a05a718);
  }
  FUN_048cc1b0(&DAT_0a05a660);
  lVar5 = *(long *)(param_1 + 0x68);
  plVar6 = *(long **)(param_1 + 0x70);
  if (plVar6 != (long *)0x0) {
    plVar2 = plVar6 + 1;
    *plVar2 = *plVar2 + 1;
    LOAcquire();
    lVar3 = *plVar2;
    *plVar2 = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*plVar6 + 0x10))(plVar6);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  if (lVar5 != 0) {
    iVar4 = thunk_FUN_05e1d97c(4);
    if (iVar4 != 0) {
      FUN_0488143c(local_198);
      pppppppuVar1 = local_198[0];
      if (-1 < cStack_181) {
        pppppppuVar1 = local_198;
      }
      if ((DAT_0a45df8a & 1) == 0) {
        DAT_0a45df80._0_1_ = s_input_ackernel_cpadV_08a133a0[8];
        DAT_0a45df80._1_1_ = s_input_ackernel_cpadV_08a133a0[9];
        DAT_0a45df80._2_1_ = s_input_ackernel_cpadV_08a133a0[10];
        DAT_0a45df80._3_1_ = s_input_ackernel_cpadV_08a133a0[0xb];
        DAT_0a45df80._4_1_ = s_input_ackernel_cpadV_08a133a0[0xc];
        DAT_0a45df80._5_1_ = s_input_ackernel_cpadV_08a133a0[0xd];
        DAT_0a45df80._6_1_ = s_input_ackernel_cpadV_08a133a0[0xe];
        DAT_0a45df80._7_1_ = s_input_ackernel_cpadV_08a133a0[0xf];
        DAT_0a45df88 = 99;
        DAT_0a45df8a = 1;
      }
      if ((DAT_0a45dfea & 1) == 0) {
        DAT_0a45dfe0._0_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x10];
        DAT_0a45dfe0._1_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x11];
        DAT_0a45dfe0._2_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x12];
        DAT_0a45dfe0._3_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x13];
        DAT_0a45dfe0._4_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x14];
        DAT_0a45dfe0._5_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x15];
        DAT_0a45dfe0._6_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x16];
        DAT_0a45dfe0._7_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0x17];
        DAT_0a45dfe8 = 0x65;
        DAT_0a45dfea = 1;
      }
      FUN_05e1d050(&local_180,4,pppppppuVar1,&DAT_0a45df80,&DAT_0a45dfe0,0x104,0,0);
      if ((DAT_0a45e07f & 1) == 0) {
        _DAT_0a45e060 = CONCAT44((int)DAT_084e49c0,(int)DAT_084a24c8);
        uRam000000000a45e068 = CONCAT44((int)DAT_08685840,(int)DAT_08492618);
        DAT_0a45e070 = CONCAT44((int)DAT_08487d20,(int)DAT_084d8a50);
        DAT_0a45e078 = (undefined4)DAT_084e4988;
        DAT_0a45e07c = 0x7473;
        DAT_0a45e07e = 0;
        DAT_0a45e07f = 1;
      }
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
      uStack_e8 = 0;
      local_f0 = 0;
      uStack_d8 = 0;
      uStack_e0 = 0;
      FUN_05e1d31c(&local_180,&DAT_0a45e060,&local_f0);
      thunk_FUN_05e1d0bc(&local_180);
      if (cStack_181 < '\0') {
        __ZdlPvm(local_198[0],CONCAT17(cStack_181,local_188) & 0x7fffffffffffffff);
      }
    }
    plVar6 = (long *)_GetWaveLink(&DAT_013526a3);
    if (plVar6 != (long *)0x0) {
      (**(code **)(*plVar6 + 8))();
    }
    plVar6 = (long *)_GetContextNoPB();
    (**(code **)(*plVar6 + 0x18))();
    _DestroyContextNoPB();
    plVar6 = (long *)_GetLogManagerNoPB();
    (**(code **)(*plVar6 + 0x38))();
    _DestroyLogManagerNoPB();
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_68) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


