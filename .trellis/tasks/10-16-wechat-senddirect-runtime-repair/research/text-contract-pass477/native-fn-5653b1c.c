// Ghidra inferred pseudocode; requested=0x5653b1c
// entry=05653b1c end=0565413b

void FUN_05653b1c(long param_1,undefined8 param_2,int param_3)

{
  int iVar1;
  int iVar2;
  long lVar3;
  undefined8 uVar4;
  long *plVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  ulong uVar8;
  ulong uVar9;
  undefined8 local_1a8;
  int local_19c;
  undefined8 local_198;
  undefined1 auStack_190 [96];
  int *local_130;
  ulong uStack_128;
  undefined8 local_120;
  undefined8 uStack_118;
  undefined8 local_110;
  undefined8 uStack_108;
  undefined8 uStack_100;
  undefined8 uStack_f8;
  undefined8 local_f0;
  undefined8 uStack_e8;
  undefined8 uStack_e0;
  undefined8 uStack_d8;
  undefined8 local_d0;
  undefined1 *local_c0;
  undefined1 *puStack_b8;
  undefined1 *puStack_b0;
  undefined1 *puStack_a8;
  undefined1 *local_a0;
  undefined1 *puStack_98;
  undefined1 *puStack_90;
  undefined1 *puStack_88;
  undefined1 *local_80;
  undefined1 *puStack_78;
  undefined1 *puStack_70;
  undefined1 *puStack_68;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_130 = &local_19c;
  local_19c = param_3;
  lVar3 = FUN_05656d80(param_1 + 0x68,&local_19c,&DAT_08b7a8b8,&local_130,&local_198);
  lVar3 = *(long *)(lVar3 + 0x18);
  if (lVar3 == 0) {
    FUN_05698f30(param_1);
    iVar2 = FUN_056a1608();
    if (local_19c <= iVar2) {
      FUN_05699084(param_1,param_2);
    }
    if (((*(char *)(param_1 + 0x28) == '\'') && (*(long *)(param_1 + 0xa0) != 0)) &&
       (iVar2 = FUN_056a1608(*(long *)(param_1 + 0x98) + 0x10), local_19c <= iVar2)) {
      plVar5 = (long *)(*(long *)(param_1 + 0x98) + 0x10);
      (**(code **)(*plVar5 + 0x48))(plVar5,param_2);
    }
    goto LAB_056540c0;
  }
  if (local_19c == *(int *)(lVar3 + 0x18)) {
    uVar4 = FUN_05698f44(param_1);
    FUN_0562fcc8(&local_130,"");
    FUN_005e41b0(*(undefined8 *)(lVar3 + 0x88));
    FUN_0008a8b8();
    if ((DAT_0a4d6a30 & 1) == 0) {
      uVar9 = 0;
      do {
        (&DAT_0a4d6a06)[uVar9] = (&DAT_08b2de3c)[uVar9 & 0xf] ^ (&DAT_08b2de4c)[uVar9];
        uVar9 = uVar9 + 1;
      } while (uVar9 != 0x2a);
      DAT_0a4d6a30 = 1;
    }
    FUN_05630c8c(&local_198,&DAT_0a4d6a06);
    thunk_FUN_05695d78(uVar4,0x15,&local_130,&local_198);
    FUN_0562fd84(&local_198);
    FUN_0562fd84(&local_130);
    *(undefined1 *)(param_1 + 0x2a) = 1;
    goto LAB_056540c0;
  }
  puStack_78 = &SUB_aaaaaaaaaaaaaaaa;
  local_80 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_68 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_70 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_98 = &SUB_aaaaaaaaaaaaaaaa;
  local_a0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_88 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_90 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_b8 = &SUB_aaaaaaaaaaaaaaaa;
  local_c0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_a8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_b0 = &SUB_aaaaaaaaaaaaaaaa;
  uVar4 = FUN_0008a8b8(param_2);
  uVar6 = FUN_009abfd4(param_2);
  FUN_05632308(&local_c0,uVar4,uVar6);
  if (*(int *)(lVar3 + 0x18) < 1) {
    iVar2 = FUN_0565da80(*(undefined8 *)(lVar3 + 0x88));
    local_d0 = 0;
    uStack_e8 = 0;
    local_f0 = 0;
    uStack_d8 = 0;
    uStack_e0 = 0;
    uStack_108 = 0;
    local_110 = 0;
    uStack_f8 = 0;
    uStack_100 = 0;
    uStack_118 = 0;
    local_120 = 0;
    uStack_128 = 0;
    local_130 = (int *)0x0;
    FUN_00069f7c(&local_130);
    uStack_128 = uStack_128 & 0xffffffffffffff00;
    iVar1 = FUN_0565a3c8(*(undefined8 *)(param_1 + 0x20));
    if (iVar1 == 0) {
      if ((char)local_130 == '\x01') {
        FUN_0563265c((ulong)&local_130 | 8,&local_c0);
      }
      else {
        FUN_056323cc((ulong)&local_130 | 8,&local_c0);
        local_130 = (int *)CONCAT71(local_130._1_7_,1);
      }
    }
    else {
      uVar4 = FUN_0565b9a8();
      if (iVar2 == 1) {
        uVar6 = FUN_0565da88(*(undefined8 *)(lVar3 + 0x88));
      }
      else {
        uVar6 = 0;
      }
      uVar7 = FUN_05698f44(param_1);
      FUN_0565ba38(&local_198,uVar4,&local_c0,uVar6,uVar7);
      if ((char)local_130 == (char)local_198) {
        if ((char)local_130 != '\0') {
          FUN_05632750((ulong)&local_130 | 8,auStack_190);
        }
      }
      else if ((char)local_130 == '\0') {
        FUN_05632480((ulong)&local_130 | 8,auStack_190);
        local_130 = (int *)CONCAT71(local_130._1_7_,1);
      }
      else {
        FUN_0563255c((ulong)&local_130 | 8);
        uStack_128 = uStack_128 & 0xffffffffffffff00;
        local_130 = (int *)((ulong)local_130 & 0xffffffffffffff00);
      }
      if ((char)local_198 == '\x01') {
        FUN_0563255c(auStack_190);
      }
    }
    if (((ulong)local_130 & 1) == 0) {
      *(undefined1 *)(param_1 + 0x2a) = 1;
    }
    else {
      uVar9 = FUN_009ce4a8((ulong)&local_130 | 8);
      uVar8 = FUN_009abfd4(param_2);
      if (uVar9 < uVar8) {
        FUN_0569910c(param_1,(ulong)&local_130 | 8,*(undefined4 *)(lVar3 + 0x10));
        local_198 = 2;
        if (iVar2 != 1) {
          local_198 = 4;
        }
        FUN_0569900c(param_1,&local_198,*(undefined4 *)(lVar3 + 0x14));
      }
      else {
        FUN_05699084(param_1,param_2,local_19c);
        iVar2 = FUN_0565a3c8(*(undefined8 *)(param_1 + 0x20));
        if (iVar2 == 0) {
          FUN_05699148(param_1,*(undefined4 *)(lVar3 + 0x14));
        }
        else {
          local_198 = 0;
          FUN_0569900c(param_1,&local_198,*(undefined4 *)(lVar3 + 0x14));
        }
      }
    }
joined_r0x05653fcc:
    if ((char)local_130 == '\x01') {
      FUN_0563255c((ulong)&local_130 | 8);
    }
  }
  else {
    uVar9 = FUN_056cb740(lVar3 + 0x20);
    if ((uVar9 & 1) == 0) {
      local_d0 = 0;
      uStack_e8 = 0;
      local_f0 = 0;
      uStack_d8 = 0;
      uStack_e0 = 0;
      uStack_108 = 0;
      local_110 = 0;
      uStack_f8 = 0;
      uStack_100 = 0;
      uStack_118 = 0;
      local_120 = 0;
      uStack_128 = 0;
      local_130 = (int *)0x0;
      FUN_00069f7c(&local_130);
      uStack_128 = uStack_128 & 0xffffffffffffff00;
      iVar2 = FUN_0565a3c8(*(undefined8 *)(param_1 + 0x20));
      if (iVar2 == 0) {
        if ((char)local_130 == '\x01') {
          FUN_0563265c((ulong)&local_130 | 8,&local_c0);
        }
        else {
          FUN_056323cc((ulong)&local_130 | 8,&local_c0);
          local_130 = (int *)CONCAT71(local_130._1_7_,1);
        }
      }
      else {
        uVar4 = FUN_0565b9a8();
        uVar6 = *(undefined8 *)(lVar3 + 0x88);
        local_1a8 = FUN_056cb608(lVar3 + 0x20);
        uVar6 = FUN_0565da90(uVar6,&local_1a8);
        uVar7 = FUN_05698f44(param_1);
        FUN_0565ba38(&local_198,uVar4,&local_c0,uVar6,uVar7);
        if ((char)local_130 == (char)local_198) {
          if ((char)local_130 != '\0') {
            FUN_05632750((ulong)&local_130 | 8,auStack_190);
          }
        }
        else if ((char)local_130 == '\0') {
          FUN_05632480((ulong)&local_130 | 8,auStack_190);
          local_130 = (int *)CONCAT71(local_130._1_7_,1);
        }
        else {
          FUN_0563255c((ulong)&local_130 | 8);
          uStack_128 = uStack_128 & 0xffffffffffffff00;
          local_130 = (int *)((ulong)local_130 & 0xffffffffffffff00);
        }
        if ((char)local_198 == '\x01') {
          FUN_0563255c(auStack_190);
        }
      }
      if (((ulong)local_130 & 1) == 0) {
        *(undefined1 *)(param_1 + 0x2a) = 1;
      }
      else {
        uVar9 = FUN_009ce4a8((ulong)&local_130 | 8);
        uVar8 = FUN_009abfd4(param_2);
        if (uVar9 < uVar8) {
          FUN_0569910c(param_1,(ulong)&local_130 | 8,*(undefined4 *)(lVar3 + 0x10));
          local_198 = 2;
          FUN_0569900c(param_1,&local_198,*(undefined4 *)(lVar3 + 0x14));
        }
        else {
          FUN_05699084(param_1,param_2,local_19c);
          iVar2 = FUN_0565a3c8(*(undefined8 *)(param_1 + 0x20));
          if (iVar2 == 0) {
            FUN_05699148(param_1,*(undefined4 *)(lVar3 + 0x14));
          }
          else {
            local_198 = 0;
            FUN_0569900c(param_1,&local_198,*(undefined4 *)(lVar3 + 0x14));
          }
        }
      }
      goto joined_r0x05653fcc;
    }
    local_130 = (int *)CONCAT71(local_130._1_7_,3);
    FUN_056c9128(&local_198,param_2);
    FUN_056309f0(&uStack_128,&local_198);
    FUN_0562fd84(&local_198);
    FUN_056cb048(lVar3 + 0x20,&local_130);
    FUN_056caefc(&local_130);
  }
  FUN_0563255c(&local_c0);
LAB_056540c0:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


