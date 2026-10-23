// Ghidra inferred pseudocode; requested=0x4671338
// entry=04671338 end=046717f3

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_04671338(void)

{
  undefined8 ***pppuVar1;
  long *plVar2;
  long lVar3;
  int iVar4;
  undefined8 **local_178 [2];
  undefined7 local_168;
  char cStack_161;
  undefined8 local_160;
  long *local_158;
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
  iVar4 = thunk_FUN_05e1d97c(2);
  if (iVar4 != 0) {
    FUN_0488143c(local_178);
    pppuVar1 = (undefined8 ***)local_178[0];
    if (-1 < cStack_161) {
      pppuVar1 = local_178;
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
    if ((DAT_0a45e3a5 & 1) == 0) {
      DAT_0a45e398._0_1_ = s_DeinitKernel_08a134c0[0];
      DAT_0a45e398._1_1_ = s_DeinitKernel_08a134c0[1];
      DAT_0a45e398._2_1_ = s_DeinitKernel_08a134c0[2];
      DAT_0a45e398._3_1_ = s_DeinitKernel_08a134c0[3];
      DAT_0a45e398._4_1_ = s_DeinitKernel_08a134c0[4];
      DAT_0a45e398._5_1_ = s_DeinitKernel_08a134c0[5];
      DAT_0a45e398._6_1_ = s_DeinitKernel_08a134c0[6];
      DAT_0a45e398._7_1_ = s_DeinitKernel_08a134c0[7];
      DAT_0a45e3a0 = (undefined4)ram0x08a134c8;
      DAT_0a45e3a4 = 0;
      DAT_0a45e3a5 = 1;
    }
    FUN_05e1d050(&local_160,2,pppuVar1,&DAT_0a45df80,&DAT_0a45e398,0x37b,0,0);
    if ((DAT_0a45e3c3 & 1) == 0) {
      uRam000000000a45e3b8._0_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x48];
      uRam000000000a45e3b8._1_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x49];
      uRam000000000a45e3b8._2_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x4a];
      uRam000000000a45e3b8._3_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x4b];
      uRam000000000a45e3b8._4_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x4c];
      uRam000000000a45e3b8._5_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x4d];
      uRam000000000a45e3b8._6_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x4e];
      uRam000000000a45e3b8._7_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x4f];
      DAT_0a45e3b0 = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x40];
      DAT_0a45e3b0_1._0_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x41];
      DAT_0a45e3b0_1._1_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x42];
      DAT_0a45e3b0_1._2_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x43];
      DAT_0a45e3b0_1._3_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x44];
      DAT_0a45e3b0_1._4_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x45];
      DAT_0a45e3b0_1._5_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x46];
      DAT_0a45e3b0_1._6_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x47];
      DAT_0a45e3c0 = 0x6574;
      DAT_0a45e3c2 = 0;
      DAT_0a45e3c3 = 1;
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
    FUN_05e1d31c(&local_160,&DAT_0a45e3b0,&local_d0);
    thunk_FUN_05e1d0bc(&local_160);
    if (cStack_161 < '\0') {
      __ZdlPvm(local_178[0],CONCAT17(cStack_161,local_168) & 0x7fffffffffffffff);
    }
  }
  FUN_046698d0(DAT_0a45df38);
  iVar4 = thunk_FUN_05e1d97c(2);
  if (iVar4 != 0) {
    FUN_0488143c(local_178);
    pppuVar1 = (undefined8 ***)local_178[0];
    if (-1 < cStack_161) {
      pppuVar1 = local_178;
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
    if ((DAT_0a45e3a5 & 1) == 0) {
      DAT_0a45e398._0_1_ = s_DeinitKernel_08a134c0[0];
      DAT_0a45e398._1_1_ = s_DeinitKernel_08a134c0[1];
      DAT_0a45e398._2_1_ = s_DeinitKernel_08a134c0[2];
      DAT_0a45e398._3_1_ = s_DeinitKernel_08a134c0[3];
      DAT_0a45e398._4_1_ = s_DeinitKernel_08a134c0[4];
      DAT_0a45e398._5_1_ = s_DeinitKernel_08a134c0[5];
      DAT_0a45e398._6_1_ = s_DeinitKernel_08a134c0[6];
      DAT_0a45e398._7_1_ = s_DeinitKernel_08a134c0[7];
      DAT_0a45e3a0 = (undefined4)ram0x08a134c8;
      DAT_0a45e3a4 = 0;
      DAT_0a45e3a5 = 1;
    }
    FUN_05e1d050(&local_160,2,pppuVar1,&DAT_0a45df80,&DAT_0a45e398,0x380,0,0);
    if ((DAT_0a45e3df & 1) == 0) {
      _DAT_0a45e3c4 = CONCAT44((int)DAT_0884a6b0,(int)DAT_08a134d0);
      uRam000000000a45e3cc = CONCAT44((int)DAT_08502a20,(int)DAT_0884a6b8);
      DAT_0a45e3d4 = CONCAT44((int)DAT_087da070,(int)DAT_084d66f8);
      DAT_0a45e3dc = 0x7469;
      DAT_0a45e3de = 0;
      DAT_0a45e3df = 1;
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
    FUN_05e1d31c(&local_160,&DAT_0a45e3c4,&local_d0);
    thunk_FUN_05e1d0bc(&local_160);
    if (cStack_161 < '\0') {
      __ZdlPvm(local_178[0],CONCAT17(cStack_161,local_168) & 0x7fffffffffffffff);
    }
  }
  FUN_049038d0(&local_160);
  FUN_04903374(local_160);
  plVar2 = local_158;
  if (local_158 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_158[1];
    local_158[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_158 + 0x10))(local_158);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  FUN_04af4c50(&local_160);
  FUN_04af4f04(local_160);
  if (local_158 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_158[1];
    local_158[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_158 + 0x10))(local_158);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_158);
    }
  }
  iVar4 = thunk_FUN_05e1d97c(2);
  if (iVar4 != 0) {
    FUN_0488143c(local_178);
    pppuVar1 = (undefined8 ***)local_178[0];
    if (-1 < cStack_161) {
      pppuVar1 = local_178;
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
    if ((DAT_0a45e3a5 & 1) == 0) {
      DAT_0a45e398._0_1_ = s_DeinitKernel_08a134c0[0];
      DAT_0a45e398._1_1_ = s_DeinitKernel_08a134c0[1];
      DAT_0a45e398._2_1_ = s_DeinitKernel_08a134c0[2];
      DAT_0a45e398._3_1_ = s_DeinitKernel_08a134c0[3];
      DAT_0a45e398._4_1_ = s_DeinitKernel_08a134c0[4];
      DAT_0a45e398._5_1_ = s_DeinitKernel_08a134c0[5];
      DAT_0a45e398._6_1_ = s_DeinitKernel_08a134c0[6];
      DAT_0a45e398._7_1_ = s_DeinitKernel_08a134c0[7];
      DAT_0a45e3a0 = (undefined4)ram0x08a134c8;
      DAT_0a45e3a4 = 0;
      DAT_0a45e3a5 = 1;
    }
    FUN_05e1d050(&local_160,2,pppuVar1,&DAT_0a45df80,&DAT_0a45e398,0x388,0,0);
    if ((DAT_0a45e3ed & 1) == 0) {
      DAT_0a45e3e0._0_1_ = s_Threads_Unit_08a134d8[0];
      DAT_0a45e3e0._1_1_ = s_Threads_Unit_08a134d8[1];
      DAT_0a45e3e0._2_1_ = s_Threads_Unit_08a134d8[2];
      DAT_0a45e3e0._3_1_ = s_Threads_Unit_08a134d8[3];
      DAT_0a45e3e0._4_1_ = s_Threads_Unit_08a134d8[4];
      DAT_0a45e3e0._5_1_ = s_Threads_Unit_08a134d8[5];
      DAT_0a45e3e0._6_1_ = s_Threads_Unit_08a134d8[6];
      DAT_0a45e3e0._7_1_ = s_Threads_Unit_08a134d8[7];
      DAT_0a45e3e8 = (undefined4)ram0x08a134e0;
      DAT_0a45e3ec = 0;
      DAT_0a45e3ed = 1;
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
    FUN_05e1d31c(&local_160,&DAT_0a45e3e0,&local_d0);
    thunk_FUN_05e1d0bc(&local_160);
    if (cStack_161 < '\0') {
      __ZdlPvm(local_178[0],CONCAT17(cStack_161,local_168) & 0x7fffffffffffffff);
    }
  }
  FUN_04b6ee38();
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


