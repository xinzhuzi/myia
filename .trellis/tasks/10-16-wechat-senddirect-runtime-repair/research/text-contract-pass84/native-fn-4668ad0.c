// Ghidra inferred pseudocode; requested=0x4668ad0
// entry=04668ad0 end=04668df3

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_04668ad0(long param_1)

{
  undefined8 *puVar1;
  undefined8 ****ppppuVar2;
  int iVar3;
  undefined8 *puVar4;
  long lVar5;
  long *plVar6;
  undefined8 ***local_1e8 [2];
  undefined7 local_1d8;
  char cStack_1d1;
  undefined1 auStack_1d0 [144];
  undefined1 *local_140;
  undefined1 *puStack_138;
  undefined1 *local_130;
  undefined1 *puStack_128;
  undefined1 *local_120;
  undefined1 *puStack_118;
  undefined1 *local_110;
  undefined1 *puStack_108;
  undefined1 *local_100;
  undefined1 *puStack_f8;
  undefined1 *local_f0;
  undefined1 *puStack_e8;
  undefined1 *puStack_e0;
  undefined1 *local_d8;
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
  puStack_e8 = &SUB_aaaaaaaaaaaaaaaa;
  local_f0 = &SUB_aaaaaaaaaaaaaaaa;
  local_d8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_e0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_108 = &SUB_aaaaaaaaaaaaaaaa;
  local_110 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_f8 = &SUB_aaaaaaaaaaaaaaaa;
  local_100 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_128 = &SUB_aaaaaaaaaaaaaaaa;
  local_130 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_118 = &SUB_aaaaaaaaaaaaaaaa;
  local_120 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_138 = &SUB_aaaaaaaaaaaaaaaa;
  local_140 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_011b97f8(&local_140);
  FUN_04d4dc14(&local_140);
  FUN_0466935c(param_1,&local_140);
  puVar4 = (undefined8 *)__Znwm(0x110);
  puVar4[1] = 0;
  puVar4[2] = 0;
  *puVar4 = &PTR_FUN_09e92c98;
  lVar5 = thunk_FUN_0462e4d4(puVar4 + 3);
  puVar1 = (undefined8 *)0x0;
  if (lVar5 != 0) {
    puVar1 = puVar4 + 5;
  }
  *(undefined8 **)(param_1 + 0x250) = puVar1;
  plVar6 = *(long **)(param_1 + 600);
  *(undefined8 **)(param_1 + 600) = puVar4;
  if (plVar6 != (long *)0x0) {
    LOAcquire();
    lVar5 = plVar6[1];
    plVar6[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*plVar6 + 0x10))(plVar6);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  puVar4 = (undefined8 *)__Znwm(0x308);
  puVar4[1] = 0;
  puVar4[2] = 0;
  *puVar4 = &PTR_FUN_09e92ce8;
  puVar1 = puVar4 + 3;
  _bzero(puVar1,0x2f0);
  FUN_0467a210(puVar1);
  *(undefined8 **)(param_1 + 0x260) = puVar1;
  plVar6 = *(long **)(param_1 + 0x268);
  *(undefined8 **)(param_1 + 0x268) = puVar4;
  if (plVar6 != (long *)0x0) {
    LOAcquire();
    lVar5 = plVar6[1];
    plVar6[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*plVar6 + 0x10))(plVar6);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  (**(code **)(**(long **)(param_1 + 0x250) + 8))
            (*(long **)(param_1 + 0x250),*(undefined8 *)(param_1 + 0x260));
  iVar3 = thunk_FUN_05e1d97c(2);
  if (iVar3 != 0) {
    FUN_0488143c(local_1e8);
    ppppuVar2 = (undefined8 ****)local_1e8[0];
    if (-1 < cStack_1d1) {
      ppppuVar2 = local_1e8;
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
    if ((DAT_0a45e10c & 1) == 0) {
      DAT_0a45e100._0_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0];
      DAT_0a45e100._1_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[1];
      DAT_0a45e100._2_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[2];
      DAT_0a45e100._3_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[3];
      DAT_0a45e100._4_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[4];
      DAT_0a45e100._5_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[5];
      DAT_0a45e100._6_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[6];
      DAT_0a45e100._7_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[7];
      DAT_0a45e108 = (undefined4)ram0x08578410;
      DAT_0a45e10c = 1;
    }
    FUN_05e1d050(auStack_1d0,2,ppppuVar2,&DAT_0a45df80,&DAT_0a45e100,0x143,0,0);
    if ((DAT_0a45e10c & 1) == 0) {
      DAT_0a45e100._0_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[0];
      DAT_0a45e100._1_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[1];
      DAT_0a45e100._2_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[2];
      DAT_0a45e100._3_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[3];
      DAT_0a45e100._4_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[4];
      DAT_0a45e100._5_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[5];
      DAT_0a45e100._6_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[6];
      DAT_0a45e100._7_1_ = s_InitNetCSetKerneTerminat1_wcs_un_08a133e8[7];
      DAT_0a45e108 = (undefined4)ram0x08578410;
      DAT_0a45e10c = 1;
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
    FUN_05e1d31c(auStack_1d0,&DAT_0a45e100,&local_d0);
    thunk_FUN_05e1d0bc(auStack_1d0);
    if (cStack_1d1 < '\0') {
      __ZdlPvm(local_1e8[0],CONCAT17(cStack_1d1,local_1d8) & 0x7fffffffffffffff);
    }
  }
  if ((long)local_d8 < 0) {
    __ZdlPvm(puStack_e8,(ulong)local_d8 & 0x7fffffffffffffff);
  }
  if ((long)local_f0 < 0) {
    __ZdlPvm(local_100,(ulong)local_f0 & 0x7fffffffffffffff);
  }
  if ((long)local_110 < 0) {
    __ZdlPvm(local_120,(ulong)local_110 & 0x7fffffffffffffff);
  }
  if ((long)puStack_128 < 0) {
    __ZdlPvm(puStack_138,(ulong)puStack_128 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


