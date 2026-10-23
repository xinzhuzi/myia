// Ghidra inferred pseudocode; requested=0x83e394
// entry=0083e394 end=0083e98b

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0083e394(long param_1,char *param_2)

{
  undefined8 ***pppuVar1;
  long *plVar2;
  int iVar3;
  long lVar4;
  undefined8 uVar5;
  ulong uVar6;
  long lVar7;
  char local_648 [8];
  undefined1 auStack_640 [536];
  undefined8 local_428;
  long *local_420;
  undefined8 local_418;
  char local_410 [8];
  undefined1 auStack_408 [536];
  undefined8 local_1f0;
  long *local_1e8;
  undefined8 **local_1e0 [2];
  undefined7 local_1d0;
  char cStack_1c9;
  undefined8 **local_1c8 [2];
  undefined7 local_1b8;
  char cStack_1b1;
  undefined8 **local_1b0;
  ulong uStack_1a8;
  undefined8 **local_120;
  ulong uStack_118;
  undefined7 local_110;
  char cStack_109;
  undefined8 **local_d0;
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
  _bzero(local_648,0x230);
  if (*param_2 != '\x01') {
    lVar7 = *(long *)(param_1 + 8);
    if ((*(long **)(lVar7 + 0x198) == (long *)0x0) ||
       (iVar3 = (**(code **)(**(long **)(lVar7 + 0x198) + 0x200))(), iVar3 != 0)) {
      uVar5 = FUN_00a82fdc(*(undefined8 *)(lVar7 + 0x1a8));
      FUN_008372c8(lVar7,0,local_648,uVar5);
    }
    goto LAB_0083e890;
  }
  FUN_003c56c4(auStack_640,param_2 + 8);
  local_428 = *(undefined8 *)(param_2 + 0x220);
  local_420 = *(long **)(param_2 + 0x228);
  if (local_420 != (long *)0x0) {
    local_420[1] = local_420[1] + 1;
  }
  local_648[0] = '\x01';
  lVar7 = *(long *)(param_1 + 8);
  iVar3 = thunk_FUN_05e1d97c(2);
  if (iVar3 != 0) {
    FUN_0488143c(local_1c8);
    pppuVar1 = (undefined8 ***)local_1c8[0];
    if (-1 < cStack_1b1) {
      pppuVar1 = local_1c8;
    }
    if ((DAT_0a2a4b74 & 1) == 0) {
      uRam000000000a2a4b68._0_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[8];
      uRam000000000a2a4b68._1_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[9];
      uRam000000000a2a4b68._2_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[10];
      uRam000000000a2a4b68._3_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[0xb];
      uRam000000000a2a4b68._4_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[0xc];
      uRam000000000a2a4b68._5_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[0xd];
      uRam000000000a2a4b68._6_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[0xe];
      uRam000000000a2a4b68._7_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[0xf];
      DAT_0a2a4b60 = s_chat_detail_viewWxGame_is_friend_08543b50[0];
      DAT_0a2a4b60_1._0_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[1];
      DAT_0a2a4b60_1._1_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[2];
      DAT_0a2a4b60_1._2_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[3];
      DAT_0a2a4b60_1._3_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[4];
      DAT_0a2a4b60_1._4_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[5];
      DAT_0a2a4b60_1._5_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[6];
      DAT_0a2a4b60_1._6_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[7];
      DAT_0a2a4b70 = (undefined4)DAT_084c8608;
      DAT_0a2a4b74 = 1;
    }
    if ((DAT_0a2a5033 & 1) == 0) {
      DAT_0a2a5028._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
      DAT_0a2a5028._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
      DAT_0a2a5028._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
      DAT_0a2a5028._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
      DAT_0a2a5028._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
      DAT_0a2a5028._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
      DAT_0a2a5028._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
      DAT_0a2a5028._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
      DAT_0a2a5030 = 0x2928;
      DAT_0a2a5032 = 0;
      DAT_0a2a5033 = 1;
    }
    FUN_05e1d050(&local_1b0,2,pppuVar1,&DAT_0a2a4b60,&DAT_0a2a5028,0x113,0,0);
    FUN_0001accc(auStack_640);
    FUN_04980e70(local_1e0);
    local_120 = local_1e0[0];
    if (-1 < cStack_1c9) {
      local_120 = local_1e0;
    }
    uStack_118 = uStack_118 & 0xffffffffffffff00;
    if ((DAT_0a2a5113 & 1) == 0) {
      uVar6 = 0;
      do {
        (&DAT_0a2a50fc)[uVar6] = (&DAT_08544d93)[uVar6] + 0x69 ^ (&DAT_08544d83)[uVar6 & 0xf];
        uVar6 = uVar6 + 1;
      } while (uVar6 != 0x17);
      DAT_0a2a5113 = 1;
    }
    uStack_c0 = 0;
    uStack_c8 = 0;
    local_d0 = &local_120;
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
    FUN_05e1d31c(&local_1b0,&DAT_0a2a50fc,&local_d0);
    if (cStack_1c9 < '\0') {
      __ZdlPvm(local_1e0[0],CONCAT17(cStack_1c9,local_1d0) & 0x7fffffffffffffff);
    }
    thunk_FUN_05e1d0bc(&local_1b0);
    if (cStack_1b1 < '\0') {
      __ZdlPvm(local_1c8[0],CONCAT17(cStack_1b1,local_1b8) & 0x7fffffffffffffff);
    }
  }
  FUN_0001accc(auStack_640);
  uVar6 = FUN_04bb3ffc();
  if ((uVar6 & 1) == 0) {
    FUN_0001accc(auStack_640);
    iVar3 = FUN_04bb4f0c();
    if (iVar3 == 0) {
LAB_0083e870:
      uVar5 = 1;
      goto LAB_0083e874;
    }
    lVar4 = FUN_00836288(lVar7,3);
    if (lVar4 == 0) {
      uVar5 = thunk_FUN_05e1d97c(4);
      if ((int)uVar5 != 0) {
        FUN_0488143c(&local_120);
        pppuVar1 = (undefined8 ***)local_120;
        if (-1 < cStack_109) {
          pppuVar1 = &local_120;
        }
        if ((DAT_0a2a4b74 & 1) == 0) {
          uRam000000000a2a4b68._0_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[8];
          uRam000000000a2a4b68._1_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[9];
          uRam000000000a2a4b68._2_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[10];
          uRam000000000a2a4b68._3_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[0xb];
          uRam000000000a2a4b68._4_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[0xc];
          uRam000000000a2a4b68._5_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[0xd];
          uRam000000000a2a4b68._6_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[0xe];
          uRam000000000a2a4b68._7_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[0xf];
          DAT_0a2a4b60 = s_chat_detail_viewWxGame_is_friend_08543b50[0];
          DAT_0a2a4b60_1._0_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[1];
          DAT_0a2a4b60_1._1_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[2];
          DAT_0a2a4b60_1._2_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[3];
          DAT_0a2a4b60_1._3_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[4];
          DAT_0a2a4b60_1._4_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[5];
          DAT_0a2a4b60_1._5_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[6];
          DAT_0a2a4b60_1._6_1_ = s_chat_detail_viewWxGame_is_friend_08543b50[7];
          DAT_0a2a4b70 = (undefined4)DAT_084c8608;
          DAT_0a2a4b74 = 1;
        }
        if ((DAT_0a2a5033 & 1) == 0) {
          DAT_0a2a5028._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
          DAT_0a2a5028._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
          DAT_0a2a5028._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
          DAT_0a2a5028._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
          DAT_0a2a5028._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
          DAT_0a2a5028._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
          DAT_0a2a5028._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
          DAT_0a2a5028._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
          DAT_0a2a5030 = 0x2928;
          DAT_0a2a5032 = 0;
          DAT_0a2a5033 = 1;
        }
        FUN_05e1d050(&local_1b0,4,pppuVar1,&DAT_0a2a4b60,&DAT_0a2a5028,0x124,0,0);
        if ((DAT_0a2a512b & 1) == 0) {
          uVar6 = 0;
          do {
            (&DAT_0a2a5114)[uVar6] = (&DAT_08544dba)[uVar6] + 0x69 ^ (&DAT_08544daa)[uVar6 & 0xf];
            uVar6 = uVar6 + 1;
          } while (uVar6 != 0x17);
          DAT_0a2a512b = 1;
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
        local_d0 = (undefined8 ***)0x0;
        local_b8 = 0;
        uStack_c0 = 0;
        FUN_05e1d31c(&local_1b0,&DAT_0a2a5114,&local_d0);
        uVar5 = thunk_FUN_05e1d0bc(&local_1b0);
        if (cStack_109 < '\0') {
          uVar5 = __ZdlPvm(local_120,CONCAT17(cStack_109,local_110) & 0x7fffffffffffffff);
        }
      }
      FUN_0083b468(uVar5,0);
      goto LAB_0083e870;
    }
    iVar3 = FUN_008f8a20(lVar4);
    if (iVar3 == 0) {
      local_d0 = (undefined8 **)FUN_0083b2ac;
      uStack_c8 = 0;
      local_1c8[0] = (undefined8 **)FUN_00040430(lVar7 + 0x1d0);
      FUN_000404d8(&local_1b0,local_1c8,*(undefined8 *)(lVar7 + 0x1d8));
      FUN_000403ac(local_1c8);
      uStack_118 = uStack_1a8;
      local_120 = local_1b0;
      uVar5 = __Znwm(0x270);
      FUN_0083ee94(uVar5,FUN_0083eb08,&local_d0,&local_120,local_648);
      local_418 = uVar5;
      FUN_008f8a28(lVar4,&local_418);
      FUN_00033d2c(&local_418);
      FUN_000403ac(&local_120);
    }
    else {
      _bzero(local_410,0x230);
      if (local_648[0] == '\x01') {
        FUN_003c56c4(auStack_408,auStack_640);
        local_1f0 = local_428;
        local_1e8 = local_420;
        if (local_420 != (long *)0x0) {
          local_420[1] = local_420[1] + 1;
        }
        local_410[0] = '\x01';
      }
      FUN_0083b2ac(lVar7,local_410,0);
      plVar2 = local_1e8;
      if (local_410[0] == '\x01') {
        if (local_1e8 != (long *)0x0) {
          LOAcquire();
          lVar4 = local_1e8[1];
          local_1e8[1] = lVar4 + -1;
          LORelease();
          if (lVar4 == 0) {
            (**(code **)(*local_1e8 + 0x10))(local_1e8);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
          }
        }
        FUN_001ef570(auStack_408);
        local_410[0] = '\0';
      }
    }
  }
  else {
    uVar5 = 2;
LAB_0083e874:
    FUN_008372c8(lVar7,uVar5,local_648,0);
  }
  FUN_008392d0(lVar7,lVar7);
LAB_0083e890:
  plVar2 = local_420;
  if (local_648[0] == '\x01') {
    if (local_420 != (long *)0x0) {
      LOAcquire();
      lVar7 = local_420[1];
      local_420[1] = lVar7 + -1;
      LORelease();
      if (lVar7 == 0) {
        (**(code **)(*local_420 + 0x10))(local_420);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
      }
    }
    FUN_001ef570(auStack_640);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


