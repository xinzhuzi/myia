// Ghidra inferred pseudocode; requested=0x322274c
// entry=0322274c end=03222bab

/* WARNING: Removing unreachable block (ram,0x03222b5c) */
/* WARNING: Removing unreachable block (ram,0x03222a68) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0322274c(long param_1)

{
  undefined8 *******pppppppuVar1;
  long *plVar2;
  long *plVar3;
  long lVar4;
  undefined1 *puVar5;
  int iVar6;
  ulong uVar7;
  undefined8 *puVar8;
  undefined8 uVar9;
  undefined1 *local_1d0;
  long *plStack_1c8;
  undefined7 local_1c0;
  char cStack_1b9;
  undefined8 *******local_1b8;
  long *local_1b0;
  undefined7 local_1a8;
  char cStack_1a1;
  undefined1 **local_1a0;
  undefined1 *puStack_198;
  undefined1 *local_190;
  undefined1 *puStack_188;
  undefined1 *local_180;
  long *local_178;
  undefined1 *local_108;
  long *local_100;
  undefined1 **local_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined1 *puStack_98;
  long *local_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 local_60;
  undefined8 uStack_58;
  undefined8 local_50;
  undefined8 uStack_48;
  undefined8 local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  uVar9 = *(undefined8 *)(param_1 + 0x18);
  iVar6 = thunk_FUN_05e1d97c(2);
  if (iVar6 != 0) {
    FUN_0488143c(&local_1b8);
    pppppppuVar1 = local_1b8;
    if (-1 < cStack_1a1) {
      pppppppuVar1 = &local_1b8;
    }
    if ((DAT_0a3dd363 & 1) == 0) {
      uVar7 = 0;
      do {
        (&DAT_0a3dd350)[uVar7] = (&DAT_088bce97)[uVar7] + 0x8a ^ (&DAT_088bce87)[uVar7 & 0xf];
        uVar7 = uVar7 + 1;
      } while (uVar7 != 0x13);
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
    FUN_05e1d050(&local_1a0,2,pppppppuVar1,&DAT_0a3dd350,0xa3e2ed8,0x1053,0,0);
    FUN_030f1f08(&local_1d0,*(undefined8 *)(param_1 + 8));
    local_108 = local_1d0;
    if (-1 < cStack_1b9) {
      local_108 = (undefined1 *)&local_1d0;
    }
    local_100 = (long *)((ulong)local_100 & 0xffffffffffffff00);
    if ((DAT_0a3e33a3 & 1) == 0) {
      _DAT_0a3e3388 = CONCAT44((int)DAT_084ec280,(int)DAT_08486a48);
      uRam000000000a3e3390 = CONCAT44((int)DAT_08486578,(int)DAT_084e3ff8);
      DAT_0a3e3398 = CONCAT44((int)DAT_088bb3c8,(int)DAT_0853ae18);
      DAT_0a3e33a0 = 0x626f;
      DAT_0a3e33a2 = 0;
      DAT_0a3e33a3 = 1;
    }
    uStack_a8 = 0;
    local_b0 = 0;
    local_b8 = &local_108;
    puStack_98 = (undefined1 *)0x0;
    local_a0 = 0;
    uStack_88 = 0;
    local_90 = (long *)0x0;
    uStack_78 = 0;
    local_80 = 0;
    uStack_68 = 0;
    local_70 = 0;
    uStack_58 = 0;
    local_60 = 0;
    uStack_48 = 0;
    local_50 = 0;
    local_40 = 0;
    FUN_05e1d31c(&local_1a0,&DAT_0a3e3388,&local_b8);
    if (cStack_1b9 < '\0') {
      __ZdlPvm(local_1d0,CONCAT17(cStack_1b9,local_1c0) & 0x7fffffffffffffff);
    }
    thunk_FUN_05e1d0bc(&local_1a0);
    if (cStack_1a1 < '\0') {
      __ZdlPvm(local_1b8,CONCAT17(cStack_1a1,local_1a8) & 0x7fffffffffffffff);
    }
  }
  FUN_03182084(uVar9,param_1 + 0x20);
  puStack_188 = &SUB_aaaaaaaaaaaaaaaa;
  local_190 = &SUB_aaaaaaaaaaaaaaaa;
  local_178 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_180 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_198 = &SUB_aaaaaaaaaaaaaaaa;
  local_1a0 = (undefined1 **)&SUB_aaaaaaaaaaaaaaaa;
  local_108 = *(undefined1 **)(param_1 + 8);
  plVar2 = *(long **)(param_1 + 0x10);
  if (plVar2 != (long *)0x0) {
    plVar2[1] = plVar2[1] + 1;
  }
  local_100 = plVar2;
  FUN_031d15fc(&local_1a0,uVar9,&local_108);
  if (plVar2 != (long *)0x0) {
    LOAcquire();
    lVar4 = plVar2[1];
    plVar2[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*plVar2 + 0x10))(plVar2);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  local_1b8 = *(undefined8 ********)(param_1 + 8);
  local_1b0 = *(long **)(param_1 + 0x10);
  if (local_1b0 != (long *)0x0) {
    local_1b0[1] = local_1b0[1] + 1;
  }
  local_b8 = local_1a0;
  if ((long)puStack_188 < 0) {
    FUN_00018d20(&local_b0,puStack_198,local_190);
  }
  else {
    puVar8 = (undefined8 *)((ulong)&local_1a0 | 8);
    uStack_a8 = puVar8[1];
    local_b0 = *puVar8;
    local_a0 = puVar8[2];
  }
  puStack_98 = local_180;
  local_90 = local_178;
  lVar4 = 0;
  if (local_178 != (long *)0x0) {
    lVar4 = local_178[1];
    local_178[1] = lVar4 + 1;
  }
  FUN_0488b574(lVar4,&local_1b8,&local_b8);
  plVar2 = local_90;
  if (local_90 != (long *)0x0) {
    LOAcquire();
    lVar4 = local_90[1];
    local_90[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*local_90 + 0x10))(local_90);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  plVar2 = local_1b0;
  if (local_1b0 != (long *)0x0) {
    LOAcquire();
    lVar4 = local_1b0[1];
    local_1b0[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*local_1b0 + 0x10))(local_1b0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  local_1d0 = *(undefined1 **)(param_1 + 8);
  plVar2 = *(long **)(param_1 + 0x10);
  puVar5 = local_1d0;
  if (plVar2 != (long *)0x0) {
    puVar5 = (undefined1 *)plVar2[1];
    plVar2[1] = (long)(puVar5 + 1);
  }
  plStack_1c8 = plVar2;
  FUN_031cba64(puVar5,uVar9,&local_1d0);
  plVar3 = local_178;
  if (plVar2 != (long *)0x0) {
    LOAcquire();
    lVar4 = plVar2[1];
    plVar2[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*plVar2 + 0x10))(plVar2);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
      plVar3 = local_178;
    }
  }
  local_178 = plVar3;
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
  if ((long)puStack_188 < 0) {
    __ZdlPvm(puStack_198,(ulong)puStack_188 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


