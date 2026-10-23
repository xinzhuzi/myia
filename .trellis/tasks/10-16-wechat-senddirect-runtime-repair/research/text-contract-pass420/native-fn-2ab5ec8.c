// Ghidra inferred pseudocode; requested=0x2ab5ec8
// entry=02ab5ec8 end=02ab6323

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_02ab5ec8(undefined8 param_1,long param_2)

{
  ulong uVar1;
  undefined1 **ppuVar2;
  long *plVar3;
  long lVar4;
  int iVar5;
  long lVar6;
  undefined8 *puVar7;
  undefined8 *puVar8;
  undefined1 *local_210 [2];
  undefined7 local_200;
  char cStack_1f9;
  undefined4 local_1f8;
  undefined4 uStack_1f4;
  long *local_1f0;
  undefined7 local_1e8;
  char cStack_1e1;
  undefined8 *local_168;
  undefined1 local_160;
  long local_118;
  undefined1 local_110;
  long *local_c8;
  undefined8 **ppuStack_c0;
  undefined8 local_b8;
  undefined8 uStack_b0;
  undefined8 uStack_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined8 uStack_88;
  undefined8 uStack_80;
  undefined8 local_78;
  undefined8 uStack_70;
  undefined8 uStack_68;
  undefined8 uStack_60;
  undefined8 local_58;
  undefined8 uStack_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  iVar5 = FUN_04bb5f30(param_2 + 8);
  if (iVar5 != 0) {
    FUN_0466aca8(&local_1f8);
    lVar6 = (**(code **)(*(long *)CONCAT44(uStack_1f4,local_1f8) + 8))();
    if (local_1f0 != (long *)0x0) {
      LOAcquire();
      lVar4 = local_1f0[1];
      local_1f0[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*local_1f0 + 0x10))(local_1f0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(local_1f0);
      }
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (param_2 + 0x20,lVar6 + 0x20);
    FUN_04b5570c(&local_1f8,lVar6 + 0x38);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (param_2 + 0xa8,&local_1f8);
    if (cStack_1e1 < '\0') {
      __ZdlPvm(CONCAT44(uStack_1f4,local_1f8),CONCAT17(cStack_1e1,local_1e8) & 0x7fffffffffffffff);
    }
    uVar1 = *(ulong *)(lVar6 + 0xc0);
    plVar3 = (long *)*(long *)(lVar6 + 0xb8);
    if (-1 < (char)*(byte *)(lVar6 + 0xcf)) {
      uVar1 = (ulong)*(byte *)(lVar6 + 0xcf);
      plVar3 = (long *)(lVar6 + 0xb8);
    }
    *(uint *)(param_2 + 0x29c) = *(uint *)(param_2 + 0x29c) | 0x10;
    puVar7 = *(undefined8 **)(param_2 + 0x1a0);
    if (puVar7 == &DAT_0a524ad0) {
      puVar7 = (undefined8 *)__Znwm(0x18);
      puVar7[1] = 0;
      puVar7[2] = 0;
      *puVar7 = 0;
      *(undefined8 **)(param_2 + 0x1a0) = puVar7;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKcm
              (puVar7,plVar3,uVar1);
    uVar1 = *(ulong *)(lVar6 + 0xa8);
    plVar3 = (long *)*(long *)(lVar6 + 0xa0);
    if (-1 < (char)*(byte *)(lVar6 + 0xb7)) {
      uVar1 = (ulong)*(byte *)(lVar6 + 0xb7);
      plVar3 = (long *)(lVar6 + 0xa0);
    }
    *(uint *)(param_2 + 0x29c) = *(uint *)(param_2 + 0x29c) | 0x20;
    puVar7 = *(undefined8 **)(param_2 + 0x1a8);
    if (puVar7 == &DAT_0a524ad0) {
      puVar7 = (undefined8 *)__Znwm(0x18);
      puVar7[1] = 0;
      puVar7[2] = 0;
      *puVar7 = 0;
      *(undefined8 **)(param_2 + 0x1a8) = puVar7;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKcm
              (puVar7,plVar3,uVar1);
    uVar1 = *(ulong *)(lVar6 + 0x90);
    plVar3 = (long *)*(long *)(lVar6 + 0x88);
    if (-1 < (char)*(byte *)(lVar6 + 0x9f)) {
      uVar1 = (ulong)*(byte *)(lVar6 + 0x9f);
      plVar3 = (long *)(lVar6 + 0x88);
    }
    *(uint *)(param_2 + 0x29c) = *(uint *)(param_2 + 0x29c) | 0x40;
    puVar7 = *(undefined8 **)(param_2 + 0x1b0);
    if (puVar7 == &DAT_0a524ad0) {
      puVar7 = (undefined8 *)__Znwm(0x18);
      puVar7[1] = 0;
      puVar7[2] = 0;
      *puVar7 = 0;
      *(undefined8 **)(param_2 + 0x1b0) = puVar7;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKcm
              (puVar7,plVar3,uVar1);
    local_1f8 = *(undefined4 *)(lVar6 + 0x6c);
    FUN_04c24758(param_2,&local_1f8);
    uVar1 = *(ulong *)(lVar6 + 0x78);
    puVar7 = *(undefined8 **)(lVar6 + 0x70);
    if (-1 < (char)*(byte *)(lVar6 + 0x87)) {
      uVar1 = (ulong)*(byte *)(lVar6 + 0x87);
      puVar7 = (undefined8 *)(lVar6 + 0x70);
    }
    *(uint *)(param_2 + 0x29c) = *(uint *)(param_2 + 0x29c) | 8;
    puVar8 = *(undefined8 **)(param_2 + 0x198);
    if (puVar8 == &DAT_0a524ad0) {
      puVar8 = (undefined8 *)__Znwm(0x18);
      puVar8[1] = 0;
      puVar8[2] = 0;
      *puVar8 = 0;
      *(undefined8 **)(param_2 + 0x198) = puVar8;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKcm
              (puVar8,puVar7,uVar1);
    *(uint *)(param_2 + 0x54) = *(uint *)(param_2 + 0x54) | 1;
    iVar5 = thunk_FUN_05e1d97c(2);
    if (iVar5 != 0) {
      FUN_0488143c(local_210);
      ppuVar2 = (undefined1 **)local_210[0];
      if (-1 < cStack_1f9) {
        ppuVar2 = local_210;
      }
      if ((DAT_0a3af0c3 & 1) == 0) {
        uRam000000000a3af0b8._0_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[8];
        uRam000000000a3af0b8._1_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[9];
        uRam000000000a3af0b8._2_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[10];
        uRam000000000a3af0b8._3_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[0xb];
        uRam000000000a3af0b8._4_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[0xc];
        uRam000000000a3af0b8._5_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[0xd];
        uRam000000000a3af0b8._6_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[0xe];
        uRam000000000a3af0b8._7_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[0xf];
        DAT_0a3af0b0 = s_contact_manager_CoLoadFriendCont_0883d3c0[0];
        DAT_0a3af0b0_1._0_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[1];
        DAT_0a3af0b0_1._1_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[2];
        DAT_0a3af0b0_1._2_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[3];
        DAT_0a3af0b0_1._3_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[4];
        DAT_0a3af0b0_1._4_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[5];
        DAT_0a3af0b0_1._5_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[6];
        DAT_0a3af0b0_1._6_1_ = s_contact_manager_CoLoadFriendCont_0883d3c0[7];
        DAT_0a3af0c0 = 0x6363;
        DAT_0a3af0c2 = 0;
        DAT_0a3af0c3 = 1;
      }
      if ((DAT_0a3b0142 & 1) == 0) {
        _DAT_0a3b0124 = CONCAT44((int)DAT_086384c8,(int)ram0x0883d7d8);
        uRam000000000a3b012c = CONCAT44((int)DAT_084d8880,(int)DAT_08480b48);
        DAT_0a3b0134 = CONCAT44((int)DAT_0883d7e0,(int)DAT_085a90b0);
        DAT_0a3b013c = (undefined4)DAT_084a9b38;
        DAT_0a3b0140 = 0x74;
        DAT_0a3b0142 = 1;
      }
      FUN_05e1d050(&local_1f8,2,ppuVar2,&DAT_0a3af0b0,&DAT_0a3b0124,0xa0e,0,0);
      local_118 = *(long *)(param_2 + 0xd8);
      if (-1 < *(char *)(param_2 + 0xef)) {
        local_118 = param_2 + 0xd8;
      }
      local_110 = 0;
      local_168 = *(undefined8 **)(param_2 + 0xc0);
      if (-1 < *(char *)(param_2 + 0xd7)) {
        local_168 = (undefined8 *)(param_2 + 0xc0);
      }
      local_160 = 0;
      if ((DAT_0a3b0159 & 1) == 0) {
        _DAT_0a3b0144 = CONCAT44((int)DAT_0883d7f0,(int)DAT_0883d7e8);
        uRam000000000a3b014c = CONCAT44((int)DAT_084d8a70,(int)DAT_0883d7f8);
        DAT_0a3b0154 = (undefined4)DAT_0883d800;
        DAT_0a3b0158 = 0;
        DAT_0a3b0159 = 1;
      }
      local_c8 = &local_118;
      ppuStack_c0 = &local_168;
      uStack_b0 = 0;
      local_b8 = 0;
      uStack_a0 = 0;
      uStack_a8 = 0;
      uStack_90 = 0;
      local_98 = 0;
      uStack_80 = 0;
      uStack_88 = 0;
      uStack_70 = 0;
      local_78 = 0;
      uStack_60 = 0;
      uStack_68 = 0;
      uStack_50 = 0;
      local_58 = 0;
      FUN_05e1d31c(&local_1f8,&DAT_0a3b0144,&local_c8);
      thunk_FUN_05e1d0bc(&local_1f8);
      if (cStack_1f9 < '\0') {
        __ZdlPvm(local_210[0],CONCAT17(cStack_1f9,local_200) & 0x7fffffffffffffff);
      }
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


