// Ghidra inferred pseudocode; requested=0x2857ca4
// entry=02857ca4 end=028582df

/* WARNING: Removing unreachable block (ram,0x02858134) */
/* WARNING: Removing unreachable block (ram,0x0285817c) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_02857ca4(long param_1,undefined8 param_2,long param_3)

{
  undefined8 ***pppuVar1;
  long *plVar2;
  long *plVar3;
  int iVar4;
  long lVar5;
  long lVar6;
  long *plVar7;
  int *piVar8;
  undefined8 uVar9;
  long local_240;
  undefined8 **local_238 [2];
  undefined7 local_228;
  char cStack_221;
  int *local_220;
  undefined8 *puStack_218;
  undefined8 *local_210;
  undefined8 *local_208;
  undefined1 *local_200;
  undefined8 *puStack_1f8;
  undefined8 *local_1f0;
  undefined1 *puStack_1e8;
  undefined8 local_188;
  undefined8 local_180;
  long local_178;
  undefined1 local_170;
  long local_128;
  undefined1 local_120;
  long *local_d8;
  long *plStack_d0;
  undefined8 local_c8;
  undefined8 uStack_c0;
  undefined8 uStack_b8;
  undefined8 uStack_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 uStack_98;
  undefined8 uStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  undefined8 uStack_78;
  undefined8 uStack_70;
  undefined8 local_68;
  undefined8 uStack_60;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  plVar2 = *(long **)(param_3 + 0x10);
  plVar3 = *(long **)(param_3 + 0x18);
  lVar5 = thunk_FUN_000a571c();
  local_220 = (int *)0x8000000000000000;
  if (!SCARRY8(lVar5,-0x295e9648864000)) {
    local_220 = (int *)(lVar5 + -0x295e9648864000);
  }
  local_180 = FUN_000a4ee8(&local_220);
  local_188 = thunk_FUN_000a5900();
  lVar5 = FUN_02877d34(param_1 + 0x20,plVar3);
  if (lVar5 == 0) {
    iVar4 = thunk_FUN_05e1d97c(3);
    if (iVar4 != 0) {
      FUN_0488143c(local_238);
      pppuVar1 = (undefined8 ***)local_238[0];
      if (-1 < cStack_221) {
        pppuVar1 = local_238;
      }
      if ((DAT_0a39e011 & 1) == 0) {
        _DAT_0a39dff8 = CONCAT44((int)DAT_08482f20,(int)DAT_08572368);
        uRam000000000a39e000 = CONCAT44((int)DAT_0849fe78,(int)DAT_08760488);
        DAT_0a39e008 = CONCAT44((int)DAT_0851e180,(int)DAT_0849b068);
        DAT_0a39e010 = 0;
        DAT_0a39e011 = 1;
      }
      if ((DAT_0a39e279 & 1) == 0) {
        DAT_0a39e270._0_1_ = s_app_routDispatch_App_08656678[8];
        DAT_0a39e270._1_1_ = s_app_routDispatch_App_08656678[9];
        DAT_0a39e270._2_1_ = s_app_routDispatch_App_08656678[10];
        DAT_0a39e270._3_1_ = s_app_routDispatch_App_08656678[0xb];
        DAT_0a39e270._4_1_ = s_app_routDispatch_App_08656678[0xc];
        DAT_0a39e270._5_1_ = s_app_routDispatch_App_08656678[0xd];
        DAT_0a39e270._6_1_ = s_app_routDispatch_App_08656678[0xe];
        DAT_0a39e270._7_1_ = s_app_routDispatch_App_08656678[0xf];
        DAT_0a39e278 = 0;
        DAT_0a39e279 = 1;
      }
      FUN_05e1d050(&local_220,3,pppuVar1,&DAT_0a39dff8,&DAT_0a39e270,0x12d,0,0);
      local_128 = *plVar2;
      if (-1 < *(char *)((long)plVar2 + 0x17)) {
        local_128 = (long)plVar2;
      }
      local_120 = 0;
      local_178 = *plVar3;
      if (-1 < *(char *)((long)plVar3 + 0x17)) {
        local_178 = (long)plVar3;
      }
      local_170 = 0;
      if ((DAT_0a39e299 & 1) == 0) {
        _DAT_0a39e27c = CONCAT44((int)ram0x085cdbd8,(int)DAT_0848e640);
        uRam000000000a39e284 = CONCAT44((int)DAT_08503668,(int)DAT_085d75e0);
        DAT_0a39e28c = CONCAT44((int)DAT_08483b10,(int)DAT_088051b0);
        DAT_0a39e294 = (undefined4)DAT_08483b18;
        DAT_0a39e298 = 0;
        DAT_0a39e299 = 1;
      }
      local_d8 = &local_128;
      plStack_d0 = &local_178;
      uStack_c0 = 0;
      local_c8 = 0;
      uStack_b0 = 0;
      uStack_b8 = 0;
      uStack_a0 = 0;
      local_a8 = 0;
      uStack_90 = 0;
      uStack_98 = 0;
      uStack_80 = 0;
      local_88 = 0;
      uStack_70 = 0;
      uStack_78 = 0;
      uStack_60 = 0;
      local_68 = 0;
      FUN_05e1d31c(&local_220,&DAT_0a39e27c,&local_d8);
      thunk_FUN_05e1d0bc(&local_220);
      if (cStack_221 < '\0') {
        __ZdlPvm(local_238[0],CONCAT17(cStack_221,local_228) & 0x7fffffffffffffff);
      }
    }
    puStack_1f8 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
    local_200 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_1e8 = &SUB_aaaaaaaaaaaaaaaa;
    local_1f0 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
    puStack_218 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
    local_220 = (int *)&SUB_aaaaaaaaaaaaaaaa;
    local_208 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
    local_210 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
    FUN_0559f2d8(&local_220);
    if ((DAT_0a39e2b1 & 1) == 0) {
      _DAT_0a39e29c = CONCAT44((int)DAT_08482f20,(int)DAT_08572368);
      uRam000000000a39e2a4 = CONCAT44((int)DAT_088051b8,(int)DAT_08760488);
      DAT_0a39e2ac = (undefined4)DAT_088051c0;
      DAT_0a39e2b0 = 0;
      DAT_0a39e2b1 = 1;
    }
    puStack_1e8 = (undefined1 *)((ulong)puStack_1e8 | 0x100000000);
    if (puStack_218 == DAT_0a523c10) {
      puStack_218 = (undefined8 *)__Znwm(0x18);
      *puStack_218 = 0;
      puStack_218[1] = 0;
      puStack_218[2] = 0;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
              (puStack_218,&DAT_0a39e29c);
    puStack_1e8 = (undefined1 *)((ulong)puStack_1e8 | 0x200000000);
    if (local_210 == &DAT_0a524ad0) {
      local_210 = (undefined8 *)__Znwm(0x18);
      *local_210 = 0;
      local_210[1] = 0;
      local_210[2] = 0;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(local_210,plVar2);
    puStack_1e8 = (undefined1 *)((ulong)puStack_1e8 | 0x400000000);
    if (local_208 == &DAT_0a524ad0) {
      local_208 = (undefined8 *)__Znwm(0x18);
      *local_208 = 0;
      local_208[1] = 0;
      local_208[2] = 0;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(local_208,plVar3);
    if ((*(byte *)(param_3 + 0x38) >> 4 & 1) != 0) {
      uVar9 = *(undefined8 *)(param_3 + 0x28);
      puStack_1e8 = (undefined1 *)((ulong)puStack_1e8 | 0x1000000000);
      if (puStack_1f8 == &DAT_0a524ad0) {
        puStack_1f8 = (undefined8 *)__Znwm(0x18);
        *puStack_1f8 = 0;
        puStack_1f8[1] = 0;
        puStack_1f8[2] = 0;
      }
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puStack_1f8,uVar9);
    }
    if ((DAT_0a39e2c9 & 1) == 0) {
      _DAT_0a39e2b4 = CONCAT44((int)DAT_08482f20,(int)DAT_087e2fa8);
      uRam000000000a39e2bc = CONCAT44((int)ram0x08543a60,(int)DAT_08487d20);
      DAT_0a39e2c4 = (undefined4)DAT_08514018;
      DAT_0a39e2c8 = 0;
      DAT_0a39e2c9 = 1;
    }
    __ZNSt3__1plIcNS_11char_traitsIcEENS_9allocatorIcEEEENS_12basic_stringIT_T0_T1_EEPKS6_RKS9_
              (&local_d8,&DAT_0a39e2b4,plVar3);
    puStack_1e8 = (undefined1 *)((ulong)puStack_1e8 | 0x2000000000);
    if (local_1f0 == &DAT_0a524ad0) {
      local_1f0 = (undefined8 *)__Znwm(0x18);
      *local_1f0 = 0;
      local_1f0[1] = 0;
      local_1f0[2] = 0;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(local_1f0,&local_d8);
    local_d8 = (long *)0x0;
    plStack_d0 = (long *)0x0;
    local_c8 = 0;
    FUN_028583b8(plVar3,plVar2,local_180,0,0,local_1f0,local_188,0,0,&local_d8);
    FUN_02857158(param_1,param_2,&local_220);
    FUN_055bf9ec(&local_220);
  }
  else {
    local_128 = param_1;
    if ((*(byte *)(param_3 + 0x38) >> 4 & 1) == 0) {
      local_220 = (int *)0x0;
      puStack_218 = (undefined8 *)0x0;
      local_210 = (undefined8 *)0x0;
    }
    else {
      plVar7 = *(long **)(param_3 + 0x28);
      if (*(char *)((long)plVar7 + 0x17) < '\0') {
        FUN_00018d20(&local_220,*plVar7,plVar7[1]);
      }
      else {
        puStack_218 = (undefined8 *)plVar7[1];
        local_220 = (int *)*plVar7;
        local_210 = (undefined8 *)plVar7[2];
      }
    }
    uVar9 = *(undefined8 *)(param_3 + 0x20);
    lVar6 = __Znwm(0xe8);
    FUN_00033c40(lVar6,FUN_02878320,FUN_028794e8);
    FUN_02879700(lVar6 + 0x28,&local_128,param_2,plVar2,plVar3,&local_220,&local_180,&local_188,
                 uVar9,lVar5 + 0x68);
    if ((long)local_210 < 0) {
      __ZdlPvm(local_220,(ulong)local_210 & 0x7fffffffffffffff);
    }
    uVar9 = *(undefined8 *)(param_3 + 0x20);
    local_d8 = (long *)0x0;
    piVar8 = *(int **)(lVar5 + 0x40);
    local_220 = piVar8;
    local_240 = lVar6;
    if (piVar8 == (int *)0x0) {
      lVar5 = 0;
    }
    else {
      FUN_0002769c(piVar8);
      lVar5 = *(long *)(lVar5 + 0x40);
    }
    (**(code **)(lVar5 + 8))(lVar5,uVar9,plVar2,&local_240);
    if (piVar8 != (int *)0x0) {
      LOAcquire();
      iVar4 = *piVar8;
      *piVar8 = iVar4 + -1;
      LORelease();
      if (iVar4 == 1) {
        FUN_00033c38(piVar8);
      }
    }
    FUN_00033d2c(&local_240);
    FUN_00033d2c(&local_d8);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_58) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


