// Ghidra inferred pseudocode; requested=0x32243a8
// entry=032243a8 end=03224e1b

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_032243a8(long param_1)

{
  long *plVar1;
  undefined8 *******pppppppuVar2;
  long *plVar3;
  undefined8 uVar4;
  long lVar5;
  undefined1 *puVar6;
  int iVar7;
  ulong uVar8;
  undefined1 *puVar9;
  undefined1 *puVar10;
  undefined8 uVar11;
  undefined8 *******local_2d0 [2];
  undefined7 local_2c0;
  char cStack_2b9;
  undefined8 local_2b8;
  long *local_2b0;
  undefined8 local_2a8;
  long *local_2a0;
  undefined8 *******local_298 [2];
  undefined7 local_288;
  char cStack_281;
  undefined8 local_280;
  long *local_278;
  undefined8 local_270;
  long *plStack_268;
  undefined8 local_260;
  long *local_258;
  undefined8 local_250;
  undefined1 *puStack_248;
  undefined1 *local_240;
  undefined1 *puStack_238;
  undefined1 *local_230;
  long *local_228;
  long local_218;
  long *local_210;
  undefined8 ******local_208;
  undefined8 local_200 [2];
  undefined7 local_1f0;
  char cStack_1e9;
  undefined1 *local_1e8;
  long *local_1e0;
  undefined8 *******local_178;
  undefined1 local_170;
  undefined7 local_168;
  char cStack_161;
  undefined8 *******local_128;
  undefined1 local_120;
  undefined8 *******local_d8;
  undefined8 *******local_d0;
  undefined8 uStack_c8;
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
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  uVar11 = *(undefined8 *)(param_1 + 0x28);
  iVar7 = thunk_FUN_05e1d97c(2);
  if (iVar7 != 0) {
    FUN_0488143c(&local_178);
    pppppppuVar2 = local_178;
    if (-1 < cStack_161) {
      pppppppuVar2 = &local_178;
    }
    if ((DAT_0a3dd363 & 1) == 0) {
      uVar8 = 0;
      do {
        (&DAT_0a3dd350)[uVar8] = (&DAT_088bce97)[uVar8] + 0x8a ^ (&DAT_088bce87)[uVar8 & 0xf];
        uVar8 = uVar8 + 1;
      } while (uVar8 != 0x13);
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
    FUN_05e1d050(&local_208,2,pppppppuVar2,&DAT_0a3dd350,0xa3e2ed8,"oreText",0,0);
    FUN_030f1f08(&local_250,*(undefined8 *)(param_1 + 8));
    local_128 = local_250;
    if (-1 < (long)local_240) {
      local_128 = (undefined8 *******)&local_250;
    }
    local_120 = 0;
    if ((DAT_0a3e33f5 & 1) == 0) {
      _DAT_0a3e33d0 = CONCAT44((int)DAT_084ec280,(int)DAT_08486a48);
      uRam000000000a3e33d8 = CONCAT44((int)DAT_08486578,(int)DAT_084e3ff8);
      _DAT_0a3e33e0 = CONCAT44((int)DAT_0877c100,(int)DAT_0853ae18);
      uRam000000000a3e33e8 = CONCAT44((int)DAT_08480a88,(int)DAT_0848c0c8);
      DAT_0a3e33f0 = (undefined4)DAT_088bb3e0;
      DAT_0a3e33f4 = 0;
      DAT_0a3e33f5 = 1;
    }
    uStack_c8 = 0;
    local_d0 = (undefined8 *******)0x0;
    local_d8 = &local_128;
    uStack_b8 = 0;
    local_c0 = 0;
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
    local_60 = 0;
    FUN_05e1d31c(&local_208,&DAT_0a3e33d0,&local_d8);
    if ((long)local_240 < 0) {
      __ZdlPvm(local_250,(ulong)local_240 & 0x7fffffffffffffff);
    }
    thunk_FUN_05e1d0bc(&local_208);
    if (cStack_161 < '\0') {
      __ZdlPvm(local_178,CONCAT17(cStack_161,local_168) & 0x7fffffffffffffff);
    }
  }
  local_218 = *(long *)(*(long *)(param_1 + 8) + 0x18);
  local_210 = *(long **)(*(long *)(param_1 + 8) + 0x20);
  lVar5 = 0;
  if (local_210 != (long *)0x0) {
    lVar5 = local_210[1];
    local_210[1] = lVar5 + 1;
  }
  if ((local_218 != 0) && (uVar8 = FUN_04a28ef8(lVar5), (uVar8 & 1) == 0)) {
    FUN_030f3214(*(undefined8 *)(param_1 + 8),9);
  }
  puStack_238 = &SUB_aaaaaaaaaaaaaaaa;
  local_240 = &SUB_aaaaaaaaaaaaaaaa;
  local_228 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_230 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_248 = &SUB_aaaaaaaaaaaaaaaa;
  local_250 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
  local_260 = *(undefined8 *)(param_1 + 8);
  local_258 = *(long **)(param_1 + 0x10);
  if (local_258 != (long *)0x0) {
    local_258[1] = local_258[1] + 1;
  }
  local_270 = *(undefined8 *)(param_1 + 0x18);
  plVar3 = *(long **)(param_1 + 0x20);
  if (plVar3 != (long *)0x0) {
    plVar3[1] = plVar3[1] + 1;
  }
  plStack_268 = plVar3;
  FUN_03224fe8(&local_250,&local_260,&local_270);
  if (plVar3 != (long *)0x0) {
    LOAcquire();
    lVar5 = plVar3[1];
    plVar3[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*plVar3 + 0x10))(plVar3);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  plVar3 = local_258;
  if (local_258 != (long *)0x0) {
    LOAcquire();
    lVar5 = local_258[1];
    local_258[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*local_258 + 0x10))(local_258);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  if ((int)local_250 != 0 || local_250._4_4_ != 0) {
    local_278 = *(long **)(param_1 + 0x10);
    uVar4 = *(undefined8 *)(param_1 + 0x18);
    local_280 = *(undefined8 *)(param_1 + 8);
    lVar5 = 0;
    if (local_278 != (long *)0x0) {
      lVar5 = local_278[1];
      local_278[1] = lVar5 + 1;
    }
    iVar7 = FUN_030dc518(lVar5,uVar4,&local_280);
    plVar3 = local_278;
    if (local_278 != (long *)0x0) {
      LOAcquire();
      lVar5 = local_278[1];
      local_278[1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*local_278 + 0x10))(local_278);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
      }
    }
    if (iVar7 != 0) {
      puVar9 = *(undefined1 **)(*(long *)(param_1 + 8) + 0x28);
      plVar3 = *(long **)(*(long *)(param_1 + 8) + 0x30);
      if (plVar3 == (long *)0x0) {
        *puVar9 = 0;
      }
      else {
        plVar1 = plVar3 + 1;
        *plVar1 = *plVar1 + 1;
        *puVar9 = 0;
        LOAcquire();
        lVar5 = *plVar1;
        *plVar1 = lVar5 + -1;
        LORelease();
        if (lVar5 == 0) {
          (**(code **)(*plVar3 + 0x10))(plVar3);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
        }
      }
      iVar7 = thunk_FUN_05e1d97c(2);
      if (iVar7 != 0) {
        FUN_0488143c(&local_178);
        pppppppuVar2 = local_178;
        if (-1 < cStack_161) {
          pppppppuVar2 = &local_178;
        }
        if ((DAT_0a3dd363 & 1) == 0) {
          uVar8 = 0;
          do {
            (&DAT_0a3dd350)[uVar8] = (&DAT_088bce97)[uVar8] + 0x8a ^ (&DAT_088bce87)[uVar8 & 0xf];
            uVar8 = uVar8 + 1;
          } while (uVar8 != 0x13);
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
        FUN_05e1d050(&local_208,2,pppppppuVar2,&DAT_0a3dd350,0xa3e2ed8,0x111c,0,0);
        FUN_030f1f08(local_298,*(undefined8 *)(param_1 + 8));
        local_128 = local_298[0];
        if (-1 < cStack_281) {
          local_128 = local_298;
        }
        local_120 = 0;
        if ((DAT_0a3e3429 & 1) == 0) {
          _DAT_0a3e33f8 = CONCAT44((int)DAT_084ec280,(int)DAT_08486a48);
          uRam000000000a3e3400 = CONCAT44((int)DAT_084a8ea0,(int)DAT_084e3ff8);
          _DAT_0a3e3408 = CONCAT44((int)DAT_0847fde0,(int)DAT_08804950);
          uRam000000000a3e3410 = CONCAT44((int)DAT_086026d0,(int)DAT_08486af0);
          _DAT_0a3e3418 = CONCAT44((int)DAT_084d57f0,(int)DAT_084a5d18);
          uRam000000000a3e3420 = CONCAT44((int)DAT_084b0210,(int)DAT_088bb3e8);
          DAT_0a3e3428 = 0;
          DAT_0a3e3429 = 1;
        }
        uStack_c8 = 0;
        local_d0 = (undefined8 *******)0x0;
        local_d8 = &local_128;
        uStack_b8 = 0;
        local_c0 = 0;
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
        local_60 = 0;
        FUN_05e1d31c(&local_208,&DAT_0a3e33f8,&local_d8);
        if (cStack_281 < '\0') {
          __ZdlPvm(local_298[0],CONCAT17(cStack_281,local_288) & 0x7fffffffffffffff);
        }
        thunk_FUN_05e1d0bc(&local_208);
        if (cStack_161 < '\0') {
          __ZdlPvm(local_178,CONCAT17(cStack_161,local_168) & 0x7fffffffffffffff);
        }
      }
      local_2a8 = *(undefined8 *)(param_1 + 8);
      local_2a0 = *(long **)(param_1 + 0x10);
      if (local_2a0 != (long *)0x0) {
        local_2a0[1] = local_2a0[1] + 1;
      }
      local_2b8 = *(undefined8 *)(param_1 + 0x18);
      local_2b0 = *(long **)(param_1 + 0x20);
      if (local_2b0 != (long *)0x0) {
        local_2b0[1] = local_2b0[1] + 1;
      }
      FUN_03224fe8(&local_208,&local_2a8,&local_2b8);
      local_250 = (undefined8 *******)local_208;
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                ((ulong)&local_250 | 8,local_200);
      plVar3 = local_228;
      if (local_1e0 != (long *)0x0) {
        local_1e0[1] = local_1e0[1] + 1;
      }
      local_230 = local_1e8;
      local_228 = local_1e0;
      if (plVar3 != (long *)0x0) {
        LOAcquire();
        lVar5 = plVar3[1];
        plVar3[1] = lVar5 + -1;
        LORelease();
        if (lVar5 == 0) {
          (**(code **)(*plVar3 + 0x10))(plVar3);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
        }
      }
      if (local_1e0 != (long *)0x0) {
        LOAcquire();
        lVar5 = local_1e0[1];
        local_1e0[1] = lVar5 + -1;
        LORelease();
        if (lVar5 == 0) {
          (**(code **)(*local_1e0 + 0x10))(local_1e0);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_1e0);
        }
      }
      if (cStack_1e9 < '\0') {
        __ZdlPvm(local_200[0],CONCAT17(cStack_1e9,local_1f0) & 0x7fffffffffffffff);
      }
      plVar3 = local_2b0;
      if (local_2b0 != (long *)0x0) {
        LOAcquire();
        lVar5 = local_2b0[1];
        local_2b0[1] = lVar5 + -1;
        LORelease();
        if (lVar5 == 0) {
          (**(code **)(*local_2b0 + 0x10))(local_2b0);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
        }
      }
      plVar3 = local_2a0;
      if (local_2a0 != (long *)0x0) {
        LOAcquire();
        lVar5 = local_2a0[1];
        local_2a0[1] = lVar5 + -1;
        LORelease();
        if (lVar5 == 0) {
          (**(code **)(*local_2a0 + 0x10))(local_2a0);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
        }
      }
    }
  }
  iVar7 = thunk_FUN_05e1d97c(2);
  if (iVar7 == 0) goto LAB_03224d44;
  FUN_0488143c(local_298);
  pppppppuVar2 = local_298[0];
  if (-1 < cStack_281) {
    pppppppuVar2 = local_298;
  }
  if ((DAT_0a3dd363 & 1) == 0) {
    uVar8 = 0;
    do {
      (&DAT_0a3dd350)[uVar8] = (&DAT_088bce97)[uVar8] + 0x8a ^ (&DAT_088bce87)[uVar8 & 0xf];
      uVar8 = uVar8 + 1;
    } while (uVar8 != 0x13);
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
  FUN_05e1d050(&local_208,2,pppppppuVar2,&DAT_0a3dd350,0xa3e2ed8,0x1121,0,0);
  FUN_030f1f08(local_2d0,*(undefined8 *)(param_1 + 8));
  local_128 = local_2d0[0];
  if (-1 < cStack_2b9) {
    local_128 = local_2d0;
  }
  local_120 = 0;
  if ((int)local_250 == 0 && local_250._4_4_ == 0) {
    local_178 = (undefined8 *******)&DAT_0a3e2ec4;
    if ((DAT_0a3e2ec9 & 1) == 0) {
      DAT_0a3e2ec4 = 0x7274;
      DAT_0a3e2ec6 = 0x75;
      puVar9 = &DAT_0a3e2ec8;
      puVar6 = &DAT_0a3e2ec7;
      puVar10 = &DAT_0a3e2ec9;
LAB_03224c4c:
      *puVar6 = 0x65;
      *puVar9 = 0;
      *puVar10 = 1;
    }
  }
  else {
    local_178 = (undefined8 *******)&DAT_0a3e2ecc;
    if ((DAT_0a3e2ed2 & 1) == 0) {
      DAT_0a3e2ecc = (undefined4)DAT_0847fe48;
      puVar6 = &DAT_0a3e2ed0;
      puVar9 = &DAT_0a3e2ed1;
      puVar10 = &DAT_0a3e2ed2;
      goto LAB_03224c4c;
    }
  }
  local_170 = 0;
  if ((DAT_0a3e3448 & 1) == 0) {
    _DAT_0a3e342c = CONCAT44((int)DAT_084ec280,(int)DAT_08486a48);
    uRam000000000a3e3434 = CONCAT44((int)DAT_084a8ea0,(int)DAT_084e3ff8);
    DAT_0a3e343c = CONCAT44((int)DAT_08489290,(int)DAT_0860f288);
    DAT_0a3e3444 = (undefined4)DAT_084d1ec0;
    DAT_0a3e3448 = 1;
  }
  local_d8 = &local_128;
  local_d0 = &local_178;
  local_c0 = 0;
  uStack_c8 = 0;
  local_b0 = 0;
  uStack_b8 = 0;
  local_a0 = 0;
  uStack_a8 = 0;
  local_90 = 0;
  uStack_98 = 0;
  local_80 = 0;
  uStack_88 = 0;
  local_70 = 0;
  uStack_78 = 0;
  local_60 = 0;
  uStack_68 = 0;
  FUN_05e1d31c(&local_208,&DAT_0a3e342c,&local_d8);
  if (cStack_2b9 < '\0') {
    __ZdlPvm(local_2d0[0],CONCAT17(cStack_2b9,local_2c0) & 0x7fffffffffffffff);
  }
  thunk_FUN_05e1d0bc(&local_208);
  if (cStack_281 < '\0') {
    __ZdlPvm(local_298[0],CONCAT17(cStack_281,local_288) & 0x7fffffffffffffff);
  }
LAB_03224d44:
  FUN_03127208(*(long *)(param_1 + 8) + 0xa0,&local_250);
  FUN_031cbd88(uVar11,param_1 + 0x30);
  plVar3 = local_228;
  if (local_228 != (long *)0x0) {
    LOAcquire();
    lVar5 = local_228[1];
    local_228[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*local_228 + 0x10))(local_228);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  if ((long)puStack_238 < 0) {
    __ZdlPvm(puStack_248,(ulong)puStack_238 & 0x7fffffffffffffff);
  }
  plVar3 = local_210;
  if (local_210 != (long *)0x0) {
    LOAcquire();
    lVar5 = local_210[1];
    local_210[1] = lVar5 + -1;
    LORelease();
    if (lVar5 == 0) {
      (**(code **)(*local_210 + 0x10))(local_210);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_58) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


