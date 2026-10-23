// Ghidra inferred pseudocode; requested=0x66846b8
// entry=066846b8 end=06684abf

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_066846b8(undefined8 *param_1,long param_2,long param_3,long *param_4,long *param_5)

{
  undefined4 uVar1;
  long *plVar2;
  ulong uVar3;
  int iVar4;
  int iVar5;
  long **pplVar6;
  code *pcVar7;
  long lVar8;
  undefined4 uVar9;
  long local_1e0 [26];
  undefined8 local_110;
  undefined8 uStack_108;
  ulong local_100;
  long lStack_f8;
  long local_f0;
  long local_e8;
  undefined8 local_e0;
  long alStack_d0 [3];
  long *local_b8;
  long alStack_b0 [3];
  long *local_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined4 local_80;
  undefined4 uStack_7c;
  undefined8 local_78;
  undefined4 local_70;
  undefined4 uStack_6c;
  undefined8 uStack_68;
  undefined1 *local_60;
  undefined8 local_58;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  lStack_f8 = 0;
  local_100 = 0;
  local_e8 = 0;
  local_f0 = 0;
  uStack_108 = 0;
  local_110 = 0;
  local_e0 = 0x80000000ffffffff;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(&local_110);
  lStack_f8 = *(long *)(param_3 + 0x18);
  if (lStack_f8 == 0) {
    lStack_f8 = *(long *)(param_2 + 0x120);
  }
  local_f0 = *(long *)(param_3 + 0x20);
  if (local_f0 == 0) {
    local_f0 = *(long *)(param_2 + 0x128);
  }
  local_e8 = *(long *)(param_3 + 0x28);
  if (local_e8 == 0) {
    local_e8 = *(long *)(param_2 + 0x130);
  }
  iVar4 = *(int *)(param_3 + 0x30);
  if (iVar4 == -1) {
    iVar4 = *(int *)(param_2 + 0x138);
  }
  iVar5 = *(int *)(param_3 + 0x34);
  if (iVar5 == -0x80000000) {
    iVar5 = *(int *)(param_2 + 0x13c);
  }
  local_e0 = CONCAT44(iVar5,iVar4);
  pplVar6 = (long **)(param_4 + 3);
  plVar2 = *pplVar6;
  *param_1 = &SUB_aaaaaaaaaaaaaaaa;
  param_1[1] = &SUB_aaaaaaaaaaaaaaaa;
  if (plVar2 == (long *)0x0) {
    pplVar6 = &local_98;
LAB_0668479c:
    *pplVar6 = (long *)0x0;
  }
  else {
    local_98 = plVar2;
    if (plVar2 != param_4) goto LAB_0668479c;
    local_98 = alStack_b0;
    (**(code **)(*plVar2 + 0x18))(plVar2,alStack_b0);
  }
  plVar2 = (long *)param_5[3];
  local_b8 = (long *)0x0;
  if (plVar2 != (long *)0x0) {
    if (plVar2 == param_5) {
      local_b8 = alStack_d0;
      (**(code **)(*plVar2 + 0x18))(plVar2,alStack_d0);
    }
    else {
      local_b8 = (long *)(**(code **)(*plVar2 + 0x10))();
    }
  }
  FUN_0667ddf8(param_1,&local_110,alStack_b0,alStack_d0);
  if (local_b8 == alStack_d0) {
    pcVar7 = *(code **)(*local_b8 + 0x20);
LAB_06684834:
    (*pcVar7)();
  }
  else if (local_b8 != (long *)0x0) {
    pcVar7 = *(code **)(*local_b8 + 0x28);
    goto LAB_06684834;
  }
  if (local_98 == alStack_b0) {
    pcVar7 = *(code **)(*local_98 + 0x20);
LAB_06684860:
    (*pcVar7)();
  }
  else if (local_98 != (long *)0x0) {
    pcVar7 = *(code **)(*local_98 + 0x28);
    goto LAB_06684860;
  }
  if (((*(byte *)(param_2 + 0x140) >> 1 & 1) == 0) && ((local_e0._4_1_ >> 1 & 1) == 0)) {
    FUN_06682d18(param_2 + 8,param_1);
  }
  else {
    uVar3 = FUN_0668dad0(1);
    if ((uVar3 & 1) != 0) {
      if ((DAT_0a51886d & 1) == 0) {
        DAT_0a518868 = (undefined4)ram0x08782918;
        DAT_0a51886c = 0;
        DAT_0a51886d = 1;
      }
      if ((DAT_0a51887a & 1) == 0) {
        DAT_0a518870._0_1_ = s_co_launcco_scope_b15db7bc_09686440[0];
        DAT_0a518870._1_1_ = s_co_launcco_scope_b15db7bc_09686440[1];
        DAT_0a518870._2_1_ = s_co_launcco_scope_b15db7bc_09686440[2];
        DAT_0a518870._3_1_ = s_co_launcco_scope_b15db7bc_09686440[3];
        DAT_0a518870._4_1_ = s_co_launcco_scope_b15db7bc_09686440[4];
        DAT_0a518870._5_1_ = s_co_launcco_scope_b15db7bc_09686440[5];
        DAT_0a518870._6_1_ = s_co_launcco_scope_b15db7bc_09686440[6];
        DAT_0a518870._7_1_ = s_co_launcco_scope_b15db7bc_09686440[7];
        DAT_0a518878 = 0x68;
        DAT_0a51887a = 1;
      }
      if ((DAT_0a51888d & 1) == 0) {
        DAT_0a518880._0_1_ = s_co_launcco_scope_b15db7bc_09686440[8];
        DAT_0a518880._1_1_ = s_co_launcco_scope_b15db7bc_09686440[9];
        DAT_0a518880._2_1_ = s_co_launcco_scope_b15db7bc_09686440[10];
        DAT_0a518880._3_1_ = s_co_launcco_scope_b15db7bc_09686440[0xb];
        DAT_0a518880._4_1_ = s_co_launcco_scope_b15db7bc_09686440[0xc];
        DAT_0a518880._5_1_ = s_co_launcco_scope_b15db7bc_09686440[0xd];
        DAT_0a518880._6_1_ = s_co_launcco_scope_b15db7bc_09686440[0xe];
        DAT_0a518880._7_1_ = s_co_launcco_scope_b15db7bc_09686440[0xf];
        DAT_0a518888 = (undefined4)ram0x08b32c40;
        DAT_0a51888c = 0;
        DAT_0a51888d = 1;
      }
      FUN_0668db5c(local_1e0,&DAT_0a518868,&DAT_0a518870,&DAT_0a518880,0x5500002800);
      if ((DAT_0a518911 & 1) == 0) {
        uVar3 = 0;
        do {
          uVar9 = *(undefined4 *)((long)&DAT_09686517 + uVar3);
          uVar1 = *(undefined4 *)((long)&DAT_09686503 + uVar3 % 0x14);
          *(uint *)((long)&DAT_0a51888e + uVar3) =
               CONCAT13((byte)((uint)uVar1 >> 0x18) ^ (byte)((uint)uVar9 >> 0x18),
                        CONCAT12((byte)((uint)uVar1 >> 0x10) ^ (byte)((uint)uVar9 >> 0x10),
                                 CONCAT11((byte)((uint)uVar1 >> 8) ^ (byte)((uint)uVar9 >> 8),
                                          (byte)uVar1 ^ (byte)uVar9)));
          uVar3 = uVar3 + 4;
        } while (uVar3 != 0x80);
        DAT_0a51890e = 0x7825;
        DAT_0a518910 = 0;
        DAT_0a518911 = 1;
      }
      plVar2 = (long *)(local_1e0[0] + 0x68);
      if (*(char *)(local_1e0[0] + 0x7f) < '\0') {
        plVar2 = (long *)*plVar2;
      }
      uStack_88 = 0xaaaaaaaa00000007;
      local_90 = 0xaaaaaaaa00000002;
      local_78 = 0xaaaaaaaa00000007;
      _local_80 = CONCAT44(0xaaaaaaaa,*(undefined4 *)(param_2 + 0x140));
      uStack_68 = 0xaaaaaaaa00000007;
      _local_70 = CONCAT44(0xaaaaaaaa,local_e0._4_4_);
      local_58 = 0xaaaaaaaa00000006;
      local_60 = &DAT_aaaaaaaa00000000;
      FUN_0668e1e4(local_1e0[0] + 0x38,&DAT_0a51888e,plVar2,&local_90,3);
      FUN_0668dbac();
      thunk_FUN_0668e878(local_1e0);
    }
  }
  uVar3 = FUN_06682d08(param_2 + 8);
  if ((uVar3 & 1) == 0) {
    if ((local_e0 & 0x100000000) != 0) goto LAB_06684a74;
    lVar8 = 0x10;
  }
  else {
    lVar8 = 0x18;
  }
  (**(code **)(*(long *)*param_1 + lVar8))();
LAB_06684a74:
  if ((long)local_100 < 0) {
    __ZdlPvm(local_110,local_100 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


