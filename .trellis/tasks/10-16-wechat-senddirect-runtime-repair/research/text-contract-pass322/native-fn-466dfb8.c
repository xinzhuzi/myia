// Ghidra inferred pseudocode; requested=0x466dfb8
// entry=0466dfb8 end=0466eb6b

/* WARNING: Removing unreachable block (ram,0x0466e6a0) */
/* WARNING: Removing unreachable block (ram,0x0466e6b8) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0466dfb8(undefined8 *param_1,undefined8 param_2,undefined8 *param_3)

{
  undefined8 *******pppppppuVar1;
  uint3 uVar2;
  long *plVar3;
  long lVar4;
  undefined1 *puVar5;
  int iVar6;
  int iVar7;
  undefined8 uVar8;
  ulong uVar9;
  undefined1 *puVar10;
  undefined1 *puVar11;
  long *plVar12;
  undefined4 uVar13;
  undefined4 uVar14;
  undefined8 *******local_2b0 [2];
  undefined7 local_2a0;
  char cStack_299;
  undefined8 *******local_298 [2];
  undefined7 local_288;
  char cStack_281;
  undefined1 *local_280;
  undefined1 *local_278;
  undefined1 *puStack_270;
  undefined1 *local_268;
  undefined1 *local_260;
  undefined1 *puStack_258;
  long local_250;
  undefined8 local_248;
  long *local_240;
  ulong uStack_238;
  long local_230;
  long lStack_228;
  undefined8 local_220;
  undefined8 uStack_218;
  undefined8 local_210;
  undefined8 uStack_208;
  undefined8 local_200;
  undefined8 uStack_1f8;
  undefined8 local_1f0;
  undefined8 uStack_1e8;
  undefined8 local_1e0;
  ulong uStack_1d8;
  undefined8 local_1d0;
  undefined8 uStack_1c8;
  ulong local_1c0;
  undefined8 uStack_1b8;
  undefined4 local_1b0;
  undefined4 uStack_1ac;
  undefined4 uStack_1a8;
  int iStack_1a4;
  undefined4 local_1a0;
  undefined4 uStack_19c;
  undefined8 local_198;
  undefined4 *local_190;
  undefined1 local_188;
  undefined8 *******local_140;
  undefined1 local_138;
  undefined7 local_130;
  char cStack_129;
  undefined8 local_f0;
  undefined8 uStack_e8;
  undefined1 *local_e0;
  undefined1 *puStack_d8;
  undefined1 *local_d0;
  undefined1 *puStack_c8;
  undefined1 *local_c0;
  undefined1 *puStack_b8;
  undefined1 *local_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  iVar6 = thunk_FUN_05e1d97c(2);
  if (iVar6 != 0) {
    FUN_0488143c(&local_140);
    pppppppuVar1 = local_140;
    if (-1 < cStack_129) {
      pppppppuVar1 = &local_140;
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
    if ((DAT_0a45e268 & 1) == 0) {
      DAT_0a45e260[0] = s_CoLogin_08a13480[0];
      DAT_0a45e260[1] = s_CoLogin_08a13480[1];
      DAT_0a45e260[2] = s_CoLogin_08a13480[2];
      DAT_0a45e260[3] = s_CoLogin_08a13480[3];
      DAT_0a45e260[4] = s_CoLogin_08a13480[4];
      DAT_0a45e260[5] = s_CoLogin_08a13480[5];
      DAT_0a45e260[6] = s_CoLogin_08a13480[6];
      DAT_0a45e260[7] = s_CoLogin_08a13480[7];
      DAT_0a45e268 = 1;
    }
    FUN_05e1d050(&local_248,2,pppppppuVar1,&DAT_0a45df80,DAT_0a45e260,0x222,0,0);
    if ((DAT_0a45e286 & 1) == 0) {
      _DAT_0a45e26c = CONCAT44((int)DAT_084d8630,(int)DAT_0889c248);
      uRam000000000a45e274 = CONCAT44((int)DAT_087447c8,(int)DAT_08a13488);
      DAT_0a45e27c = CONCAT44((int)DAT_085a4cd8,(int)DAT_08484450);
      DAT_0a45e284 = 0x72;
      DAT_0a45e286 = 1;
    }
    uStack_88 = 0;
    local_90 = 0;
    uStack_78 = 0;
    local_80 = 0;
    uStack_a8 = 0;
    local_b0 = (undefined1 *)0x0;
    uStack_98 = 0;
    local_a0 = 0;
    puStack_c8 = (undefined1 *)0x0;
    local_d0 = (undefined1 *)0x0;
    puStack_b8 = (undefined1 *)0x0;
    local_c0 = (undefined1 *)0x0;
    uStack_e8._0_4_ = 0;
    uStack_e8._4_4_ = 0;
    local_f0._0_4_ = 0;
    local_f0._4_4_ = 0;
    puStack_d8 = (undefined1 *)0x0;
    local_e0 = (undefined1 *)0x0;
    FUN_05e1d31c(&local_248,&DAT_0a45e26c,&local_f0);
    thunk_FUN_05e1d0bc(&local_248);
    if (cStack_129 < '\0') {
      __ZdlPvm(local_140,CONCAT17(cStack_129,local_130) & 0x7fffffffffffffff);
    }
  }
  FUN_04668f94(param_2,2);
  local_248 = DAT_0a45df38[0x52];
  plVar12 = (long *)DAT_0a45df38[0x53];
  plVar3 = DAT_0a45df38;
  if (plVar12 != (long *)0x0) {
    plVar3 = (long *)plVar12[1];
    plVar12[1] = (long)plVar3 + 1;
  }
  local_240 = plVar12;
  FUN_0453df64(plVar3,local_248,param_3);
  if (plVar12 != (long *)0x0) {
    LOAcquire();
    lVar4 = plVar12[1];
    plVar12[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*plVar12 + 0x10))(plVar12);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar12);
    }
  }
  iVar6 = thunk_FUN_05e1d97c(2);
  if (iVar6 != 0) {
    FUN_0488143c(&local_140);
    pppppppuVar1 = local_140;
    if (-1 < cStack_129) {
      pppppppuVar1 = &local_140;
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
    if ((DAT_0a45e268 & 1) == 0) {
      DAT_0a45e260[0] = s_CoLogin_08a13480[0];
      DAT_0a45e260[1] = s_CoLogin_08a13480[1];
      DAT_0a45e260[2] = s_CoLogin_08a13480[2];
      DAT_0a45e260[3] = s_CoLogin_08a13480[3];
      DAT_0a45e260[4] = s_CoLogin_08a13480[4];
      DAT_0a45e260[5] = s_CoLogin_08a13480[5];
      DAT_0a45e260[6] = s_CoLogin_08a13480[6];
      DAT_0a45e260[7] = s_CoLogin_08a13480[7];
      DAT_0a45e268 = 1;
    }
    FUN_05e1d050(&local_248,2,pppppppuVar1,&DAT_0a45df80,DAT_0a45e260,0x228,0,0);
    if ((DAT_0a45e2a4 & 1) == 0) {
      _DAT_0a45e288 = CONCAT44((int)DAT_084d8630,(int)DAT_0889c248);
      uRam000000000a45e290 = CONCAT44((int)DAT_08a13498,(int)DAT_08a13490);
      DAT_0a45e298 = CONCAT44((int)DAT_08480a78,(int)DAT_084de6a8);
      DAT_0a45e2a0 = (undefined4)ram0x08480568;
      DAT_0a45e2a4 = 1;
    }
    uStack_88 = 0;
    local_90 = 0;
    uStack_78 = 0;
    local_80 = 0;
    uStack_a8 = 0;
    local_b0 = (undefined1 *)0x0;
    uStack_98 = 0;
    local_a0 = 0;
    puStack_c8 = (undefined1 *)0x0;
    local_d0 = (undefined1 *)0x0;
    puStack_b8 = (undefined1 *)0x0;
    local_c0 = (undefined1 *)0x0;
    uStack_e8._0_4_ = 0;
    uStack_e8._4_4_ = 0;
    local_f0._0_4_ = 0;
    local_f0._4_4_ = 0;
    puStack_d8 = (undefined1 *)0x0;
    local_e0 = (undefined1 *)0x0;
    FUN_05e1d31c(&local_248,&DAT_0a45e288,&local_f0);
    thunk_FUN_05e1d0bc(&local_248);
    if (cStack_129 < '\0') {
      __ZdlPvm(local_140,CONCAT17(cStack_129,local_130) & 0x7fffffffffffffff);
    }
  }
  plVar3 = (long *)(**(code **)(*DAT_0a45df38 + 0x18))();
  (**(code **)(*plVar3 + 0x70))(plVar3,param_3[3]);
  iVar6 = thunk_FUN_05e1d97c(2);
  if (iVar6 != 0) {
    FUN_0488143c(&local_140);
    pppppppuVar1 = local_140;
    if (-1 < cStack_129) {
      pppppppuVar1 = &local_140;
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
    if ((DAT_0a45e268 & 1) == 0) {
      DAT_0a45e260[0] = s_CoLogin_08a13480[0];
      DAT_0a45e260[1] = s_CoLogin_08a13480[1];
      DAT_0a45e260[2] = s_CoLogin_08a13480[2];
      DAT_0a45e260[3] = s_CoLogin_08a13480[3];
      DAT_0a45e260[4] = s_CoLogin_08a13480[4];
      DAT_0a45e260[5] = s_CoLogin_08a13480[5];
      DAT_0a45e260[6] = s_CoLogin_08a13480[6];
      DAT_0a45e260[7] = s_CoLogin_08a13480[7];
      DAT_0a45e268 = 1;
    }
    FUN_05e1d050(&local_248,2,pppppppuVar1,&DAT_0a45df80,DAT_0a45e260,0x22d,0,0);
    if ((DAT_0a45e2c0 & 1) == 0) {
      _DAT_0a45e2a8 = CONCAT44((int)DAT_084d8630,(int)DAT_0889c248);
      uRam000000000a45e2b0 = CONCAT44((int)DAT_0889c280,(int)DAT_0889c278);
      DAT_0a45e2b8 = CONCAT44((int)DAT_08497400,(int)DAT_08a134a0);
      DAT_0a45e2c0 = 1;
    }
    uStack_88 = 0;
    local_90 = 0;
    uStack_78 = 0;
    local_80 = 0;
    uStack_a8 = 0;
    local_b0 = (undefined1 *)0x0;
    uStack_98 = 0;
    local_a0 = 0;
    puStack_c8 = (undefined1 *)0x0;
    local_d0 = (undefined1 *)0x0;
    puStack_b8 = (undefined1 *)0x0;
    local_c0 = (undefined1 *)0x0;
    uStack_e8._0_4_ = 0;
    uStack_e8._4_4_ = 0;
    local_f0._0_4_ = 0;
    local_f0._4_4_ = 0;
    puStack_d8 = (undefined1 *)0x0;
    local_e0 = (undefined1 *)0x0;
    FUN_05e1d31c(&local_248,&DAT_0a45e2a8,&local_f0);
    thunk_FUN_05e1d0bc(&local_248);
    if (cStack_129 < '\0') {
      __ZdlPvm(local_140,CONCAT17(cStack_129,local_130) & 0x7fffffffffffffff);
    }
  }
  FUN_0466eccc(param_2,param_3);
  thunk_FUN_05cf09f0(param_3[3]);
  FUN_04906044(param_3[3]);
  FUN_04906280(param_3[3]);
  FUN_04906cec(param_3[3]);
  local_240 = (long *)&DAT_aaaaaaaa00000000;
  uStack_19c = 0xaaaaaaaa;
  local_198 = 0;
  local_230 = 0;
  uStack_238 = 0;
  local_220 = 0;
  lStack_228 = 0;
  local_210 = 0;
  uStack_218 = 0;
  local_200 = 0;
  uStack_208 = 0;
  local_1f0 = 0;
  uStack_1f8 = 0;
  local_1e0 = 0;
  uStack_1e8 = 0;
  local_1d0 = 0;
  uStack_1d8 = 0;
  local_1c0 = 0;
  uStack_1c8 = 0;
  local_1b0 = 0;
  uStack_1b8 = 0;
  iStack_1a4 = 0;
  local_1a0 = 0;
  uStack_1ac = 0;
  uStack_1a8 = 0;
  local_248 = 0x32;
  local_b0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_c8 = &SUB_aaaaaaaaaaaaaaaa;
  local_d0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_b8 = &SUB_aaaaaaaaaaaaaaaa;
  local_c0 = &SUB_aaaaaaaaaaaaaaaa;
  uStack_e8._0_4_ = -0x55555556;
  uStack_e8._4_4_ = 0xaaaaaaaa;
  local_f0._0_4_ = 0xaaaaaaaa;
  local_f0._4_4_ = -0x55555556;
  puStack_d8 = &SUB_aaaaaaaaaaaaaaaa;
  local_e0 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_04749384(&local_f0);
  local_248 = CONCAT44(1,(undefined4)local_248);
  uVar8 = param_3[3];
  uStack_238 = (ulong)(byte)local_f0;
  local_198 = uVar8;
  if ((byte)local_f0 == 1) {
    local_230 = (long)local_f0._4_4_;
    lStack_228 = (long)(int)uStack_e8;
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(&uStack_1e8,&local_e0);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(&local_1d0,&puStack_c8)
    ;
    uVar8 = param_3[3];
  }
  local_220 = uVar8;
  FUN_04af307c(&local_248,0);
  if (iStack_1a4 < 0) {
    __ZdlPvm(uStack_1b8,CONCAT44(iStack_1a4,uStack_1a8) & 0x7fffffffffffffff);
  }
  if ((long)local_1c0 < 0) {
    __ZdlPvm(local_1d0,local_1c0 & 0x7fffffffffffffff);
  }
  if ((long)uStack_1d8 < 0) {
    __ZdlPvm(uStack_1e8,uStack_1d8 & 0x7fffffffffffffff);
  }
  if ((DAT_0a45e268 & 1) == 0) {
    DAT_0a45e268 = 1;
    DAT_0a45e260 = s_CoLogin_08a13480;
  }
  if ((DAT_0a45e308 & 1) == 0) {
    uVar9 = 0;
    do {
      uVar13 = *(undefined4 *)((long)&DAT_08a143c1 + uVar9);
      uVar2 = CONCAT12((char)((uint)uVar13 >> 8),(short)uVar13) & 0xff00ff;
      uVar14 = *(undefined4 *)((long)&DAT_08a143ad + uVar9 % 0x14);
      *(uint *)((long)&DAT_0a45e2c1 + uVar9) =
           CONCAT13((char)((uint)uVar13 >> 0x18) + 0x8aU ^ (byte)((uint)uVar14 >> 0x18),
                    CONCAT12((char)((uint)uVar13 >> 0x10) + 0x8aU ^ (byte)((uint)uVar14 >> 0x10),
                             CONCAT11((char)(uVar2 >> 0x10) + 0x8aU ^ (byte)((uint)uVar14 >> 8),
                                      (char)uVar2 + 0x8aU ^ (byte)uVar14)));
      uVar9 = uVar9 + 4;
    } while (uVar9 != 0x44);
    DAT_0a45e305 = 0x6363;
    DAT_0a45e307 = 0;
    DAT_0a45e308 = 1;
  }
  FUN_0003bb6c(&local_248,DAT_0a45e260,&DAT_0a45e2c1,0x252);
  lVar4 = __Znwm(0x48);
  FUN_00033c40(lVar4,FUN_0467a4cc,FUN_0467a4dc);
  *(undefined8 *)(lVar4 + 0x28) = param_3[3];
  if (*(char *)((long)param_3 + 0x17) < '\0') {
    FUN_00018d20(lVar4 + 0x30,*param_3,param_3[1]);
  }
  else {
    uVar8 = *param_3;
    *(undefined8 *)(lVar4 + 0x38) = param_3[1];
    *(undefined8 *)(lVar4 + 0x30) = uVar8;
    *(undefined8 *)(lVar4 + 0x40) = param_3[2];
  }
  local_250 = lVar4;
  FUN_04b7141c(&local_248,&local_250,0,0);
  FUN_00033d2c(&local_250);
  param_1[3] = &SUB_aaaaaaaaaaaaaaaa;
  param_1[2] = &SUB_aaaaaaaaaaaaaaaa;
  param_1[5] = &SUB_aaaaaaaaaaaaaaaa;
  param_1[4] = &SUB_aaaaaaaaaaaaaaaa;
  param_1[1] = &SUB_aaaaaaaaaaaaaaaa;
  *param_1 = &SUB_aaaaaaaaaaaaaaaa;
  *(undefined4 *)(param_1 + 6) = 0xffffffff;
  *(undefined1 **)((long)param_1 + 0x34) = &SUB_aaaaaaaaaaaaaaaa;
  *(undefined4 *)((long)param_1 + 0x3c) = 0xaaaaaaaa;
  FUN_0466ee94(&local_248,param_2,param_3);
  FUN_0466f170(param_1,&local_f0,&local_248);
  plVar3 = local_240;
  if (local_240 != (long *)0x0) {
    LOAcquire();
    lVar4 = local_240[1];
    local_240[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*local_240 + 0x10))(local_240);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  plVar3 = (long *)(**(code **)(*DAT_0a45df38 + 0x18))();
  if (plVar3 != (long *)0x0) {
    (**(code **)(*plVar3 + 0xe0))();
  }
  FUN_0466a420();
  local_260 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_258 = &SUB_aaaaaaaaaaaaaaaa;
  local_268 = &SUB_aaaaaaaaaaaaaaaa;
  (**(code **)(*DAT_0a45df38 + 0x68))(&local_248);
  plVar3 = local_240;
  local_f0._0_4_ = (undefined4)local_248;
  local_f0._4_4_ = (int)((ulong)local_248 >> 0x20);
  uStack_e8._0_4_ = (int)local_240;
  uStack_e8._4_4_ = (undefined4)((ulong)local_240 >> 0x20);
  if ((local_240 != (long *)0x0) && (local_240[1] = local_240[1] + 1, local_240 != (long *)0x0)) {
    LOAcquire();
    lVar4 = local_240[1];
    local_240[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*local_240 + 0x10))(local_240);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  local_248 = CONCAT44(local_248._4_4_,2);
  FUN_045513b4(&local_268,CONCAT44(local_f0._4_4_,(undefined4)local_f0),&local_248);
  plVar3 = (long *)CONCAT44(uStack_e8._4_4_,(int)uStack_e8);
  if (plVar3 != (long *)0x0) {
    LOAcquire();
    lVar4 = plVar3[1];
    plVar3[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*plVar3 + 0x10))(plVar3);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  local_278 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_270 = &SUB_aaaaaaaaaaaaaaaa;
  local_280 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0002c368(&local_248,&local_268,"contact",7);
  FUN_0002c368(&local_280,&local_248,"contact.db",10);
  FUN_0002b440(&local_248);
  iVar6 = thunk_FUN_000311e8(&local_280);
  iVar7 = thunk_FUN_05e1d97c(2);
  if (iVar7 == 0) goto LAB_0466eb1c;
  FUN_0488143c(local_298);
  pppppppuVar1 = local_298[0];
  if (-1 < cStack_281) {
    pppppppuVar1 = local_298;
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
  if ((DAT_0a45e268 & 1) == 0) {
    DAT_0a45e260[0] = s_CoLogin_08a13480[0];
    DAT_0a45e260[1] = s_CoLogin_08a13480[1];
    DAT_0a45e260[2] = s_CoLogin_08a13480[2];
    DAT_0a45e260[3] = s_CoLogin_08a13480[3];
    DAT_0a45e260[4] = s_CoLogin_08a13480[4];
    DAT_0a45e260[5] = s_CoLogin_08a13480[5];
    DAT_0a45e260[6] = s_CoLogin_08a13480[6];
    DAT_0a45e260[7] = s_CoLogin_08a13480[7];
    DAT_0a45e268 = 1;
  }
  FUN_05e1d050(&local_248,2,pppppppuVar1,&DAT_0a45df80,DAT_0a45e260,0x26a,0,0);
  FUN_04980e70(local_2b0,param_3);
  local_140 = local_2b0[0];
  if (-1 < cStack_299) {
    local_140 = local_2b0;
  }
  local_138 = 0;
  if (iVar6 == 0) {
    local_190 = &DAT_0a45e664;
    if ((DAT_0a45e66a & 1) == 0) {
      DAT_0a45e664 = (undefined4)DAT_0847fe48;
      puVar5 = &DAT_0a45e668;
      puVar10 = &DAT_0a45e669;
      puVar11 = &DAT_0a45e66a;
      goto LAB_0466ea0c;
    }
  }
  else {
    local_190 = (undefined4 *)&DAT_0a45e65b;
    if ((DAT_0a45e660 & 1) == 0) {
      DAT_0a45e65b = 0x7274;
      DAT_0a45e65d = 0x75;
      puVar10 = &DAT_0a45e65f;
      puVar5 = &DAT_0a45e65e;
      puVar11 = &DAT_0a45e660;
LAB_0466ea0c:
      *puVar5 = 0x65;
      *puVar10 = 0;
      *puVar11 = 1;
    }
  }
  local_188 = 0;
  if ((DAT_0a45e331 & 1) == 0) {
    _DAT_0a45e30c = CONCAT44((int)DAT_084d8298,(int)DAT_084d86b0);
    uRam000000000a45e314 = CONCAT44((int)DAT_08623e50,(int)DAT_0855bba8);
    _DAT_0a45e31c = CONCAT44((int)DAT_0849b088,(int)DAT_088546d0);
    uRam000000000a45e324 = CONCAT44((int)DAT_084e4910,(int)ram0x0883d810);
    DAT_0a45e32c = (undefined4)DAT_085f3170;
    DAT_0a45e330 = 0;
    DAT_0a45e331 = 1;
  }
  local_f0 = &local_140;
  uStack_e8 = &local_190;
  puStack_d8 = (undefined1 *)0x0;
  local_e0 = (undefined1 *)0x0;
  puStack_c8 = (undefined1 *)0x0;
  local_d0 = (undefined1 *)0x0;
  puStack_b8 = (undefined1 *)0x0;
  local_c0 = (undefined1 *)0x0;
  uStack_a8 = 0;
  local_b0 = (undefined1 *)0x0;
  uStack_98 = 0;
  local_a0 = 0;
  uStack_88 = 0;
  local_90 = 0;
  uStack_78 = 0;
  local_80 = 0;
  FUN_05e1d31c(&local_248,&DAT_0a45e30c,&local_f0);
  if (cStack_299 < '\0') {
    __ZdlPvm(local_2b0[0],CONCAT17(cStack_299,local_2a0) & 0x7fffffffffffffff);
  }
  thunk_FUN_05e1d0bc(&local_248);
  if (cStack_281 < '\0') {
    __ZdlPvm(local_298[0],CONCAT17(cStack_281,local_288) & 0x7fffffffffffffff);
  }
LAB_0466eb1c:
  *(char *)((long)param_1 + 4) = (char)iVar6;
  FUN_0002b440(&local_280);
  FUN_0002b440(&local_268);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


