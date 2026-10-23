// Ghidra inferred pseudocode; requested=0x31099b8
// entry=031099b8 end=03109faf

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

bool FUN_031099b8(undefined8 param_1,long *param_2)

{
  undefined8 ***pppuVar1;
  long *plVar2;
  bool bVar3;
  long lVar4;
  int iVar5;
  long lVar6;
  long lVar7;
  long *local_190;
  undefined8 **local_188 [2];
  undefined7 local_178;
  char cStack_171;
  undefined1 auStack_170 [144];
  long local_e0;
  long *local_d8;
  long local_d0;
  long *local_c8;
  undefined8 local_c0;
  undefined8 uStack_b8;
  undefined8 uStack_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 uStack_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 uStack_70;
  undefined8 uStack_68;
  undefined8 local_60;
  undefined8 uStack_58;
  undefined8 uStack_50;
  undefined8 uStack_48;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar7 = *param_2;
  lVar6 = *(long *)(lVar7 + 0x18);
  local_c8 = *(long **)(lVar7 + 0x20);
  lVar4 = 0;
  if (local_c8 != (long *)0x0) {
    lVar4 = local_c8[1];
    local_c8[1] = lVar4 + 1;
    lVar7 = *param_2;
  }
  local_d0 = lVar6;
  if ((*(long *)(lVar7 + 8) == 0) ||
     (local_e0 = ___dynamic_cast(lVar4,*(long *)(lVar7 + 8),&PTR_DAT_09c37aa0,&PTR_DAT_09eb2580,0),
     local_e0 == 0)) {
    local_e0 = 0;
    local_d8 = (long *)0x0;
    if (lVar6 == 0) goto LAB_03109bec;
    iVar5 = thunk_FUN_05e1d97c(4);
    if (iVar5 != 0) {
      FUN_0488143c(local_188);
      pppuVar1 = (undefined8 ***)local_188[0];
      if (-1 < cStack_171) {
        pppuVar1 = local_188;
      }
      if ((DAT_0a3da318 & 1) == 0) {
        _DAT_0a3da300 = CONCAT44((int)DAT_084a66a8,(int)DAT_0849a618);
        uRam000000000a3da308 = CONCAT44((int)DAT_0875a898,(int)DAT_084a66b0);
        DAT_0a3da310 = CONCAT44((int)DAT_084c8608,(int)DAT_084d88d0);
        DAT_0a3da318 = 1;
      }
      if ((DAT_0a3da5d1 & 1) == 0) {
        uRam000000000a3da5c8 = _UNK_088a7388;
        _DAT_0a3da5c0 = _DAT_088a7380;
        DAT_0a3da5d0 = 0;
        DAT_0a3da5d1 = 1;
      }
      FUN_05e1d050(auStack_170,4,pppuVar1,&DAT_0a3da300,&DAT_0a3da5c0,0xce,0,0);
      if ((DAT_0a3da609 & 1) == 0) {
        _DAT_0a3da5f4 = CONCAT44((int)DAT_08499930,(int)DAT_084a8ea0);
        uRam000000000a3da5fc = CONCAT44((int)DAT_08483050,(int)DAT_08532030);
        DAT_0a3da604 = (undefined4)DAT_08483058;
        DAT_0a3da608 = 0;
        DAT_0a3da609 = 1;
      }
      uStack_58 = 0;
      local_60 = 0;
      uStack_48 = 0;
      uStack_50 = 0;
      uStack_78 = 0;
      local_80 = 0;
      uStack_68 = 0;
      uStack_70 = 0;
      uStack_98 = 0;
      local_a0 = 0;
      uStack_88 = 0;
      uStack_90 = 0;
      uStack_b8 = 0;
      local_c0 = 0;
      uStack_a8 = 0;
      uStack_b0 = 0;
      FUN_05e1d31c(auStack_170,&DAT_0a3da5f4,&local_c0);
      goto LAB_03109d28;
    }
  }
  else {
    local_190 = *(long **)(lVar7 + 0x10);
    if (local_190 != (long *)0x0) {
      local_190[1] = local_190[1] + 1;
    }
    local_d8 = local_190;
    if (lVar6 != 0) {
      lVar6 = ___dynamic_cast(local_e0,&PTR_DAT_09eb2580,&PTR_DAT_09eb2598,0);
      bVar3 = lVar6 != 0;
      if (lVar6 == 0) {
        local_190 = (long *)0x0;
        iVar5 = thunk_FUN_05e1d97c(4);
        if (iVar5 != 0) {
          FUN_0488143c(local_188);
          pppuVar1 = (undefined8 ***)local_188[0];
          if (-1 < cStack_171) {
            pppuVar1 = local_188;
          }
          if ((DAT_0a3da318 & 1) == 0) {
            _DAT_0a3da300 = CONCAT44((int)DAT_084a66a8,(int)DAT_0849a618);
            uRam000000000a3da308 = CONCAT44((int)DAT_0875a898,(int)DAT_084a66b0);
            DAT_0a3da310 = CONCAT44((int)DAT_084c8608,(int)DAT_084d88d0);
            DAT_0a3da318 = 1;
          }
          if ((DAT_0a3da5d1 & 1) == 0) {
            uRam000000000a3da5c8 = _UNK_088a7388;
            _DAT_0a3da5c0 = _DAT_088a7380;
            DAT_0a3da5d0 = 0;
            DAT_0a3da5d1 = 1;
          }
          FUN_05e1d050(auStack_170,4,pppuVar1,&DAT_0a3da300,&DAT_0a3da5c0,0xd4,0,0);
          if ((DAT_0a3da627 & 1) == 0) {
            _DAT_0a3da60c = CONCAT44((int)DAT_08557bc8,(int)DAT_0849a618);
            uRam000000000a3da614 = CONCAT44((int)DAT_0856e3c0,(int)DAT_085e8930);
            DAT_0a3da61c = CONCAT44((int)DAT_0854c0c0,(int)DAT_08486ac8);
            DAT_0a3da624 = 0x7274;
            DAT_0a3da626 = 0;
            DAT_0a3da627 = 1;
          }
          uStack_58 = 0;
          local_60 = 0;
          uStack_48 = 0;
          uStack_50 = 0;
          uStack_78 = 0;
          local_80 = 0;
          uStack_68 = 0;
          uStack_70 = 0;
          uStack_98 = 0;
          local_a0 = 0;
          uStack_88 = 0;
          uStack_90 = 0;
          uStack_b8 = 0;
          local_c0 = 0;
          uStack_a8 = 0;
          uStack_b0 = 0;
          FUN_05e1d31c(auStack_170,&DAT_0a3da60c,&local_c0);
          thunk_FUN_05e1d0bc(auStack_170);
          if (cStack_171 < '\0') {
            __ZdlPvm(local_188[0],CONCAT17(cStack_171,local_178) & 0x7fffffffffffffff);
          }
        }
      }
      else {
        if (local_190 == (long *)0x0) goto LAB_03109d4c;
        local_190[1] = local_190[1] + 1;
      }
      if (local_190 != (long *)0x0) {
        LOAcquire();
        lVar6 = local_190[1];
        local_190[1] = lVar6 + -1;
        LORelease();
        if (lVar6 == 0) {
          (**(code **)(*local_190 + 0x10))(local_190);
          __ZNSt3__119__shared_weak_count14__release_weakEv(local_190);
        }
      }
      goto LAB_03109d4c;
    }
LAB_03109bec:
    iVar5 = thunk_FUN_05e1d97c(4);
    if (iVar5 != 0) {
      FUN_0488143c(local_188);
      pppuVar1 = (undefined8 ***)local_188[0];
      if (-1 < cStack_171) {
        pppuVar1 = local_188;
      }
      if ((DAT_0a3da318 & 1) == 0) {
        _DAT_0a3da300 = CONCAT44((int)DAT_084a66a8,(int)DAT_0849a618);
        uRam000000000a3da308 = CONCAT44((int)DAT_0875a898,(int)DAT_084a66b0);
        DAT_0a3da310 = CONCAT44((int)DAT_084c8608,(int)DAT_084d88d0);
        DAT_0a3da318 = 1;
      }
      if ((DAT_0a3da5d1 & 1) == 0) {
        uRam000000000a3da5c8 = _UNK_088a7388;
        _DAT_0a3da5c0 = _DAT_088a7380;
        DAT_0a3da5d0 = 0;
        DAT_0a3da5d1 = 1;
      }
      FUN_05e1d050(auStack_170,4,pppuVar1,&DAT_0a3da300,&DAT_0a3da5c0,0xc9,0,0);
      if ((DAT_0a3da5f3 & 1) == 0) {
        uRam000000000a3da5e8._0_1_ = s_message_is_nullpOpenFromDataItem_08538d30[8];
        uRam000000000a3da5e8._1_1_ = s_message_is_nullpOpenFromDataItem_08538d30[9];
        uRam000000000a3da5e8._2_1_ = s_message_is_nullpOpenFromDataItem_08538d30[10];
        uRam000000000a3da5e8._3_1_ = s_message_is_nullpOpenFromDataItem_08538d30[0xb];
        uRam000000000a3da5e8._4_1_ = s_message_is_nullpOpenFromDataItem_08538d30[0xc];
        uRam000000000a3da5e8._5_1_ = s_message_is_nullpOpenFromDataItem_08538d30[0xd];
        uRam000000000a3da5e8._6_1_ = s_message_is_nullpOpenFromDataItem_08538d30[0xe];
        uRam000000000a3da5e8._7_1_ = s_message_is_nullpOpenFromDataItem_08538d30[0xf];
        DAT_0a3da5e0 = s_message_is_nullpOpenFromDataItem_08538d30[0];
        DAT_0a3da5e0_1._0_1_ = s_message_is_nullpOpenFromDataItem_08538d30[1];
        DAT_0a3da5e0_1._1_1_ = s_message_is_nullpOpenFromDataItem_08538d30[2];
        DAT_0a3da5e0_1._2_1_ = s_message_is_nullpOpenFromDataItem_08538d30[3];
        DAT_0a3da5e0_1._3_1_ = s_message_is_nullpOpenFromDataItem_08538d30[4];
        DAT_0a3da5e0_1._4_1_ = s_message_is_nullpOpenFromDataItem_08538d30[5];
        DAT_0a3da5e0_1._5_1_ = s_message_is_nullpOpenFromDataItem_08538d30[6];
        DAT_0a3da5e0_1._6_1_ = s_message_is_nullpOpenFromDataItem_08538d30[7];
        DAT_0a3da5f0 = 0x7274;
        DAT_0a3da5f2 = 0;
        DAT_0a3da5f3 = 1;
      }
      uStack_58 = 0;
      local_60 = 0;
      uStack_48 = 0;
      uStack_50 = 0;
      uStack_78 = 0;
      local_80 = 0;
      uStack_68 = 0;
      uStack_70 = 0;
      uStack_98 = 0;
      local_a0 = 0;
      uStack_88 = 0;
      uStack_90 = 0;
      uStack_b8 = 0;
      local_c0 = 0;
      uStack_a8 = 0;
      uStack_b0 = 0;
      FUN_05e1d31c(auStack_170,&DAT_0a3da5e0,&local_c0);
LAB_03109d28:
      thunk_FUN_05e1d0bc(auStack_170);
      if (cStack_171 < '\0') {
        __ZdlPvm(local_188[0],CONCAT17(cStack_171,local_178) & 0x7fffffffffffffff);
      }
    }
  }
  bVar3 = false;
LAB_03109d4c:
  plVar2 = local_d8;
  if (local_d8 != (long *)0x0) {
    LOAcquire();
    lVar6 = local_d8[1];
    local_d8[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*local_d8 + 0x10))(local_d8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  plVar2 = local_c8;
  if (local_c8 != (long *)0x0) {
    LOAcquire();
    lVar6 = local_c8[1];
    local_c8[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*local_c8 + 0x10))(local_c8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return bVar3;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


