// Ghidra inferred pseudocode; requested=0x326a144
// entry=0326a144 end=0326ab73

/* WARNING: Removing unreachable block (ram,0x0326ab44) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_0326a144(long param_1,long param_2,long param_3,undefined1 param_4)

{
  undefined8 *******pppppppuVar1;
  int iVar2;
  undefined8 uVar3;
  long *plVar4;
  undefined8 *puVar5;
  code *pcVar6;
  ulong uVar7;
  long lVar8;
  long lVar9;
  undefined8 local_2a0;
  undefined8 uStack_298;
  ulong local_290;
  undefined8 *******local_280 [2];
  undefined7 local_270;
  char cStack_269;
  undefined8 *******local_268;
  ulong uStack_260;
  undefined7 local_258;
  byte bStack_251;
  undefined8 *******local_250;
  long lStack_248;
  long *local_240;
  undefined8 uStack_238;
  undefined8 local_230;
  undefined8 *******local_220;
  undefined1 *puStack_218;
  undefined1 *local_210;
  undefined1 *puStack_208;
  undefined1 *local_200;
  undefined1 *puStack_1f8;
  undefined1 *local_1f0;
  undefined1 *local_1e8;
  undefined1 local_1d1;
  undefined8 *******local_1d0;
  undefined1 local_1c8;
  undefined7 local_1c0;
  char cStack_1b9;
  long local_180;
  long lStack_178;
  ulong local_170;
  long *local_168;
  undefined8 local_160;
  undefined8 *******local_f0;
  long lStack_e8;
  long local_e0;
  undefined8 local_d8;
  undefined8 uStack_d0;
  undefined8 local_c8;
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
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  uVar7 = *(ulong *)(param_3 + 8);
  if (-1 < (char)*(byte *)(param_3 + 0x17)) {
    uVar7 = (ulong)*(byte *)(param_3 + 0x17);
  }
  local_1d1 = param_4;
  if (uVar7 == 0) {
    iVar2 = thunk_FUN_05e1d97c(4);
    if (iVar2 != 0) {
      FUN_0488143c(&local_220);
      pppppppuVar1 = local_220;
      if (-1 < (long)local_210) {
        pppppppuVar1 = &local_220;
      }
      if ((DAT_0a3e46b7 & 1) == 0) {
        uVar7 = 0;
        do {
          (&DAT_0a3e46a4)[uVar7] = (&DAT_088ca7e4)[uVar7] + 0x8a ^ (&DAT_088ca7d4)[uVar7 & 0xf];
          uVar7 = uVar7 + 1;
        } while (uVar7 != 0x13);
        DAT_0a3e46b7 = 1;
      }
      if ((DAT_0a3e4f7b & 1) == 0) {
        DAT_0a3e4f70._0_1_ = s_AddMessa__final_geMa_088c9aa0[0];
        DAT_0a3e4f70._1_1_ = s_AddMessa__final_geMa_088c9aa0[1];
        DAT_0a3e4f70._2_1_ = s_AddMessa__final_geMa_088c9aa0[2];
        DAT_0a3e4f70._3_1_ = s_AddMessa__final_geMa_088c9aa0[3];
        DAT_0a3e4f70._4_1_ = s_AddMessa__final_geMa_088c9aa0[4];
        DAT_0a3e4f70._5_1_ = s_AddMessa__final_geMa_088c9aa0[5];
        DAT_0a3e4f70._6_1_ = s_AddMessa__final_geMa_088c9aa0[6];
        DAT_0a3e4f70._7_1_ = s_AddMessa__final_geMa_088c9aa0[7];
        DAT_0a3e4f78 = 0x6567;
        DAT_0a3e4f7a = 0;
        DAT_0a3e4f7b = 1;
      }
      FUN_05e1d050(&local_180,4,pppppppuVar1,&DAT_0a3e46a4,&DAT_0a3e4f70,0x368,0,0);
      FUN_04cbe440(&local_250,param_2);
      local_1d0 = local_250;
      if (-1 < (long)local_240) {
        local_1d0 = &local_250;
      }
      local_1c8 = 0;
      if ((DAT_0a3e4fa8 & 1) == 0) {
        uVar7 = 0;
        do {
          (&DAT_0a3e4f7c)[uVar7] = (&DAT_088cb9af)[uVar7] + 0x8a ^ (&DAT_088cb99f)[uVar7 & 0xf];
          uVar7 = uVar7 + 1;
        } while (uVar7 != 0x2c);
        DAT_0a3e4fa8 = 1;
      }
      local_e0 = 0;
      lStack_e8 = 0;
      local_f0 = &local_1d0;
      uStack_d0 = 0;
      local_d8 = 0;
      uStack_c0 = 0;
      local_c8 = 0;
      uStack_b0 = 0;
      local_b8 = 0;
      uStack_a0 = 0;
      local_a8 = 0;
      uStack_90 = 0;
      local_98 = 0;
      uStack_80 = 0;
      local_88 = 0;
      local_78 = 0;
      FUN_05e1d31c(&local_180,&DAT_0a3e4f7c,&local_f0);
      if ((long)local_240 < 0) {
        __ZdlPvm(local_250,(ulong)local_240 & 0x7fffffffffffffff);
      }
      thunk_FUN_05e1d0bc(&local_180);
      if ((long)local_210 < 0) {
        __ZdlPvm(local_220,(ulong)local_210 & 0x7fffffffffffffff);
      }
    }
    uVar3 = 0;
    goto LAB_0326a934;
  }
  puStack_1f8 = &SUB_aaaaaaaaaaaaaaaa;
  local_200 = &SUB_aaaaaaaaaaaaaaaa;
  local_1e8 = &SUB_aaaaaaaaaaaaaaaa;
  local_1f0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_218 = &SUB_aaaaaaaaaaaaaaaa;
  local_220 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
  puStack_208 = &SUB_aaaaaaaaaaaaaaaa;
  local_210 = &SUB_aaaaaaaaaaaaaaaa;
  if ((DAT_0a3e4f7b & 1) == 0) {
    DAT_0a3e4f70 = s_AddMessa__final_geMa_088c9aa0._0_8_;
    DAT_0a3e4f78 = 0x6567;
    DAT_0a3e4f7a = 0;
    DAT_0a3e4f7b = 1;
  }
  if ((DAT_0a3e500e & 1) == 0) {
    uVar7 = 0;
    do {
      (&DAT_0a3e4fa9)[uVar7] = (&DAT_088cb9eb)[uVar7] + 0x8a ^ (&DAT_088cb9db)[uVar7 & 0xf];
      uVar7 = uVar7 + 1;
    } while (uVar7 != 0x65);
    DAT_0a3e500e = 1;
  }
  FUN_0003bb6c(&local_180,&DAT_0a3e4f70,&DAT_0a3e4fa9,0x36c);
  local_220 = (undefined8 *******)CONCAT44(local_220._4_4_,2);
  local_210 = (undefined1 *)0x0;
  local_200 = (undefined1 *)lStack_178;
  puStack_208 = (undefined1 *)local_180;
  local_1f0 = (undefined1 *)0x0;
  local_1e8 = (undefined1 *)0x0;
  puStack_1f8 = (undefined1 *)0x0;
  puStack_218 = (undefined1 *)FUN_0474715c();
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
            (&puStack_1f8,&DAT_0a3e4f70);
  lStack_248 = 0;
  local_250 = (undefined8 *******)0x0;
  uStack_238 = 0;
  local_240 = (long *)0x0;
  local_230 = 0xaaaaaaaa3f800000;
  lStack_178 = 0;
  local_180 = 0;
  local_168 = (long *)0x0;
  local_170 = 0;
  local_160 = 0xaaaaaaaa3f800000;
  FUN_003e8854(&local_180,param_2 + 0x18,param_2 + 0x18);
  FUN_003e8854(&local_180,param_2 + 0x30,param_2 + 0x30);
  FUN_003e8854(&local_180,param_2 + 0x48,param_2 + 0x48);
  uVar7 = FUN_03aee89c(param_1,&local_180,&local_250);
  lVar8 = local_180;
  plVar4 = (long *)local_170;
  while (plVar4 != (long *)0x0) {
    lVar9 = *plVar4;
    local_180 = lVar8;
    if (*(char *)((long)plVar4 + 0x27) < '\0') {
      __ZdlPvm(plVar4[2],plVar4[4] & 0x7fffffffffffffff);
    }
    __ZdlPvm(plVar4,0x28);
    lVar8 = local_180;
    plVar4 = (long *)lVar9;
  }
  local_180 = 0;
  if (lVar8 != 0) {
    __ZdlPvm(lVar8,lStack_178 << 3);
  }
  if ((uVar7 & 1) == 0) {
    iVar2 = thunk_FUN_05e1d97c(4);
    if (iVar2 != 0) {
      FUN_0488143c(&local_268);
      pppppppuVar1 = local_268;
      if (-1 < (char)bStack_251) {
        pppppppuVar1 = &local_268;
      }
      if ((DAT_0a3e46b7 & 1) == 0) {
        uVar7 = 0;
        do {
          (&DAT_0a3e46a4)[uVar7] = (&DAT_088ca7e4)[uVar7] + 0x8a ^ (&DAT_088ca7d4)[uVar7 & 0xf];
          uVar7 = uVar7 + 1;
        } while (uVar7 != 0x13);
        DAT_0a3e46b7 = 1;
      }
      if ((DAT_0a3e4f7b & 1) == 0) {
        DAT_0a3e4f70._0_1_ = s_AddMessa__final_geMa_088c9aa0[0];
        DAT_0a3e4f70._1_1_ = s_AddMessa__final_geMa_088c9aa0[1];
        DAT_0a3e4f70._2_1_ = s_AddMessa__final_geMa_088c9aa0[2];
        DAT_0a3e4f70._3_1_ = s_AddMessa__final_geMa_088c9aa0[3];
        DAT_0a3e4f70._4_1_ = s_AddMessa__final_geMa_088c9aa0[4];
        DAT_0a3e4f70._5_1_ = s_AddMessa__final_geMa_088c9aa0[5];
        DAT_0a3e4f70._6_1_ = s_AddMessa__final_geMa_088c9aa0[6];
        DAT_0a3e4f70._7_1_ = s_AddMessa__final_geMa_088c9aa0[7];
        DAT_0a3e4f78 = 0x6567;
        DAT_0a3e4f7a = 0;
        DAT_0a3e4f7b = 1;
      }
      FUN_05e1d050(&local_180,4,pppppppuVar1,&DAT_0a3e46a4,&DAT_0a3e4f70,0x378,0,0);
      FUN_04cbe440(local_280,param_2);
      local_1d0 = local_280[0];
      if (-1 < cStack_269) {
        local_1d0 = local_280;
      }
      local_1c8 = 0;
      if ((DAT_0a3e5031 & 1) == 0) {
        uVar7 = 0;
        do {
          (&DAT_0a3e500f)[uVar7] = (&DAT_088cba60)[uVar7] + 0x8a ^ (&DAT_088cba50)[uVar7 & 0xf];
          uVar7 = uVar7 + 1;
        } while (uVar7 != 0x22);
        DAT_0a3e5031 = 1;
      }
      local_e0 = 0;
      lStack_e8 = 0;
      local_f0 = &local_1d0;
      uStack_d0 = 0;
      local_d8 = 0;
      uStack_c0 = 0;
      local_c8 = 0;
      uStack_b0 = 0;
      local_b8 = 0;
      uStack_a0 = 0;
      local_a8 = 0;
      uStack_90 = 0;
      local_98 = 0;
      uStack_80 = 0;
      local_88 = 0;
      local_78 = 0;
      FUN_05e1d31c(&local_180,&DAT_0a3e500f,&local_f0);
LAB_0326a8c0:
      if (cStack_269 < '\0') {
        __ZdlPvm(local_280[0],CONCAT17(cStack_269,local_270) & 0x7fffffffffffffff);
      }
      thunk_FUN_05e1d0bc(&local_180);
      if ((char)bStack_251 < '\0') {
        __ZdlPvm(local_268,CONCAT17(bStack_251,local_258) & 0x7fffffffffffffff);
      }
    }
LAB_0326a8f8:
    uVar3 = 0;
    pppppppuVar1 = local_250;
    plVar4 = local_240;
  }
  else {
    uVar7 = FUN_0326ad6c(param_1,param_3);
    if ((uVar7 & 1) == 0) {
      iVar2 = thunk_FUN_05e1d97c(4);
      if (iVar2 != 0) {
        FUN_0488143c(&local_268);
        pppppppuVar1 = local_268;
        if (-1 < (char)bStack_251) {
          pppppppuVar1 = &local_268;
        }
        if ((DAT_0a3e46b7 & 1) == 0) {
          uVar7 = 0;
          do {
            (&DAT_0a3e46a4)[uVar7] = (&DAT_088ca7e4)[uVar7] + 0x8a ^ (&DAT_088ca7d4)[uVar7 & 0xf];
            uVar7 = uVar7 + 1;
          } while (uVar7 != 0x13);
          DAT_0a3e46b7 = 1;
        }
        if ((DAT_0a3e4f7b & 1) == 0) {
          DAT_0a3e4f70._0_1_ = s_AddMessa__final_geMa_088c9aa0[0];
          DAT_0a3e4f70._1_1_ = s_AddMessa__final_geMa_088c9aa0[1];
          DAT_0a3e4f70._2_1_ = s_AddMessa__final_geMa_088c9aa0[2];
          DAT_0a3e4f70._3_1_ = s_AddMessa__final_geMa_088c9aa0[3];
          DAT_0a3e4f70._4_1_ = s_AddMessa__final_geMa_088c9aa0[4];
          DAT_0a3e4f70._5_1_ = s_AddMessa__final_geMa_088c9aa0[5];
          DAT_0a3e4f70._6_1_ = s_AddMessa__final_geMa_088c9aa0[6];
          DAT_0a3e4f70._7_1_ = s_AddMessa__final_geMa_088c9aa0[7];
          DAT_0a3e4f78 = 0x6567;
          DAT_0a3e4f7a = 0;
          DAT_0a3e4f7b = 1;
        }
        FUN_05e1d050(&local_180,4,pppppppuVar1,&DAT_0a3e46a4,&DAT_0a3e4f70,0x37e,0,0);
        FUN_04cbe440(local_280,param_2);
        local_1d0 = local_280[0];
        if (-1 < cStack_269) {
          local_1d0 = local_280;
        }
        local_1c8 = 0;
        if ((DAT_0a3e5059 & 1) == 0) {
          uVar7 = 0;
          do {
            (&DAT_0a3e5032)[uVar7] = (&DAT_088cba92)[uVar7] + 0x8a ^ (&DAT_088cba82)[uVar7 & 0xf];
            uVar7 = uVar7 + 1;
          } while (uVar7 != 0x27);
          DAT_0a3e5059 = 1;
        }
        local_e0 = 0;
        lStack_e8 = 0;
        local_f0 = &local_1d0;
        uStack_d0 = 0;
        local_d8 = 0;
        uStack_c0 = 0;
        local_c8 = 0;
        uStack_b0 = 0;
        local_b8 = 0;
        uStack_a0 = 0;
        local_a8 = 0;
        uStack_90 = 0;
        local_98 = 0;
        uStack_80 = 0;
        local_88 = 0;
        local_78 = 0;
        FUN_05e1d31c(&local_180,&DAT_0a3e5032,&local_f0);
        goto LAB_0326a8c0;
      }
      goto LAB_0326a8f8;
    }
    FUN_03269bec(uVar7,param_2);
    local_168 = (long *)__Znwm(0x30);
    *local_168 = (long)&PTR_FUN_09df1b90;
    local_168[1] = param_2;
    local_168[2] = (long)&local_250;
    local_168[3] = (long)&local_1d1;
    local_168[4] = param_3;
    local_168[5] = param_1;
    uVar3 = FUN_03aeddb4(param_1,&local_180);
    if (local_168 == &local_180) {
      pcVar6 = *(code **)(*local_168 + 0x20);
LAB_0326a9b4:
      (*pcVar6)();
    }
    else if (local_168 != (long *)0x0) {
      pcVar6 = *(code **)(*local_168 + 0x28);
      goto LAB_0326a9b4;
    }
    FUN_04cbe440(&local_1d0,param_2);
    if ((DAT_0a3e5071 & 1) == 0) {
      uRam000000000a3e5068 = _UNK_088c99d8;
      _DAT_0a3e5060 = _DAT_088c99d0;
      DAT_0a3e5070 = 0;
      DAT_0a3e5071 = 1;
    }
    plVar4 = (long *)__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6insertEmPKc
                               (&local_1d0,0,&DAT_0a3e5060);
    lStack_e8 = plVar4[1];
    local_f0 = (undefined8 *******)*plVar4;
    local_e0 = plVar4[2];
    plVar4[1] = 0;
    plVar4[2] = 0;
    *plVar4 = 0;
    if ((DAT_0a3e507b & 1) == 0) {
      DAT_0a3e5074 = (undefined4)DAT_084e3fc0;
      DAT_0a3e5078 = 0x3a74;
      DAT_0a3e507a = 0;
      DAT_0a3e507b = 1;
    }
    plVar4 = (long *)__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKc
                               (&local_f0,&DAT_0a3e5074);
    lStack_178 = plVar4[1];
    local_180 = *plVar4;
    local_170 = plVar4[2];
    plVar4[1] = 0;
    plVar4[2] = 0;
    *plVar4 = 0;
    __ZNSt3__19to_stringEi(&local_268,uVar3);
    pppppppuVar1 = local_268;
    if (-1 < (char)bStack_251) {
      uStack_260 = (ulong)bStack_251;
      pppppppuVar1 = &local_268;
    }
    puVar5 = (undefined8 *)
             __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
                       (&local_180,pppppppuVar1,uStack_260);
    uStack_298 = puVar5[1];
    local_2a0 = *puVar5;
    local_290 = puVar5[2];
    puVar5[1] = 0;
    puVar5[2] = 0;
    *puVar5 = 0;
    FUN_02ac5bf8(&local_220,&local_2a0,0x32);
    if ((long)local_290 < 0) {
      __ZdlPvm(local_2a0,local_290 & 0x7fffffffffffffff);
    }
    if ((char)bStack_251 < '\0') {
      __ZdlPvm(local_268,CONCAT17(bStack_251,local_258) & 0x7fffffffffffffff);
    }
    if ((long)local_170 < 0) {
      __ZdlPvm(local_180,local_170 & 0x7fffffffffffffff);
    }
    pppppppuVar1 = local_250;
    plVar4 = local_240;
    if (cStack_1b9 < '\0') {
      __ZdlPvm(local_1d0,CONCAT17(cStack_1b9,local_1c0) & 0x7fffffffffffffff);
      pppppppuVar1 = local_250;
      plVar4 = local_240;
    }
  }
  while (plVar4 != (long *)0x0) {
    lVar8 = *plVar4;
    local_250 = pppppppuVar1;
    if (*(char *)((long)plVar4 + 0x27) < '\0') {
      __ZdlPvm(plVar4[2],plVar4[4] & 0x7fffffffffffffff);
    }
    __ZdlPvm(plVar4,0x30);
    pppppppuVar1 = local_250;
    plVar4 = (long *)lVar8;
  }
  local_250 = (undefined8 *******)0x0;
  if (pppppppuVar1 != (undefined8 *******)0x0) {
    __ZdlPvm(pppppppuVar1,lStack_248 << 3);
  }
  if ((long)local_1e8 < 0) {
    __ZdlPvm(puStack_1f8,(ulong)local_1e8 & 0x7fffffffffffffff);
  }
LAB_0326a934:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_68) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return uVar3;
}


