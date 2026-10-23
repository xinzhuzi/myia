// Ghidra inferred pseudocode; requested=0x5654344
// entry=05654344 end=0565494f

void FUN_05654344(long param_1,undefined8 param_2,int param_3)

{
  int iVar1;
  int iVar2;
  long lVar3;
  undefined8 uVar4;
  long *plVar5;
  undefined8 uVar6;
  ulong uVar7;
  ulong uVar8;
  undefined8 uVar9;
  long lVar10;
  undefined8 local_138;
  int local_12c;
  undefined8 local_128;
  undefined1 auStack_120 [96];
  int *local_c0;
  ulong uStack_b8;
  undefined8 local_b0;
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
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_12c = param_3;
  local_c0 = &local_12c;
  lVar3 = FUN_05656d80(param_1 + 0x68,&local_12c,&DAT_08b7a8b8,&local_c0,&local_128);
  lVar10 = *(long *)(lVar3 + 0x18);
  local_c0 = &local_12c;
  lVar3 = FUN_05656d80(param_1 + 0x68,&local_12c,&DAT_08b7a8b8,&local_c0,&local_128);
  if (*(long *)(lVar3 + 0x18) == 0) {
    FUN_05698f30(param_1);
    iVar2 = FUN_056a1608();
    if (local_12c <= iVar2) {
      FUN_0569910c(param_1,param_2);
    }
    if (((*(char *)(param_1 + 0x28) == '\'') && (*(long *)(param_1 + 0xa0) != 0)) &&
       (iVar2 = FUN_056a1608(*(long *)(param_1 + 0x98) + 0x10), local_12c <= iVar2)) {
      plVar5 = (long *)(*(long *)(param_1 + 0x98) + 0x10);
      (**(code **)(*plVar5 + 0x58))(plVar5,param_2);
    }
  }
  else if (local_12c == *(int *)(lVar10 + 0x18)) {
    uVar4 = FUN_05698f44(param_1);
    FUN_0562fcc8(&local_c0,"");
    FUN_005e41b0(*(undefined8 *)(lVar10 + 0x88));
    FUN_0008a8b8();
    if ((DAT_0a4d6a5b & 1) == 0) {
      uVar8 = 0;
      do {
        (&DAT_0a4d6a31)[uVar8] = (&DAT_08b2de76)[uVar8 & 0xf] ^ (&DAT_08b2de86)[uVar8];
        uVar8 = uVar8 + 1;
      } while (uVar8 != 0x2a);
      DAT_0a4d6a5b = 1;
    }
    FUN_05630c8c(&local_128,&DAT_0a4d6a31);
    thunk_FUN_05695d78(uVar4,0x15,&local_c0,&local_128);
    FUN_0562fd84(&local_128);
    FUN_0562fd84(&local_c0);
    *(undefined1 *)(param_1 + 0x2a) = 1;
  }
  else {
    if (*(int *)(lVar10 + 0x18) < 1) {
      iVar2 = FUN_0565da80(*(undefined8 *)(lVar10 + 0x88));
      local_60 = 0;
      uStack_78 = 0;
      local_80 = 0;
      uStack_68 = 0;
      uStack_70 = 0;
      uStack_98 = 0;
      local_a0 = 0;
      uStack_88 = 0;
      uStack_90 = 0;
      uStack_a8 = 0;
      local_b0 = 0;
      uStack_b8 = 0;
      local_c0 = (int *)0x0;
      FUN_00069f7c(&local_c0);
      uStack_b8 = uStack_b8 & 0xffffffffffffff00;
      iVar1 = FUN_0565a3c8(*(undefined8 *)(param_1 + 0x20));
      if (iVar1 == 0) {
        if ((char)local_c0 == '\x01') {
          FUN_0563265c((ulong)&local_c0 | 8,param_2);
        }
        else {
          FUN_056323cc((ulong)&local_c0 | 8,param_2);
          local_c0 = (int *)CONCAT71(local_c0._1_7_,1);
        }
      }
      else {
        uVar4 = FUN_0565b9a8();
        if (iVar2 == 1) {
          uVar9 = FUN_0565da88(*(undefined8 *)(lVar10 + 0x88));
        }
        else {
          uVar9 = 0;
        }
        uVar6 = FUN_05698f44(param_1);
        FUN_0565ba38(&local_128,uVar4,param_2,uVar9,uVar6);
        if ((char)local_c0 == (char)local_128) {
          if ((char)local_c0 != '\0') {
            FUN_05632750((ulong)&local_c0 | 8,auStack_120);
          }
        }
        else if ((char)local_c0 == '\0') {
          FUN_05632480((ulong)&local_c0 | 8,auStack_120);
          local_c0 = (int *)CONCAT71(local_c0._1_7_,1);
        }
        else {
          FUN_0563255c((ulong)&local_c0 | 8);
          uStack_b8 = uStack_b8 & 0xffffffffffffff00;
          local_c0 = (int *)((ulong)local_c0 & 0xffffffffffffff00);
        }
        if ((char)local_128 == '\x01') {
          FUN_0563255c(auStack_120);
        }
      }
      if (((ulong)local_c0 & 1) == 0) {
        *(undefined1 *)(param_1 + 0x2a) = 1;
      }
      else {
        uVar8 = FUN_009ce4a8((ulong)&local_c0 | 8);
        uVar7 = FUN_009ce4a8(param_2);
        if (uVar8 < uVar7) {
          FUN_0569910c(param_1,(ulong)&local_c0 | 8,*(undefined4 *)(lVar10 + 0x10));
          local_128 = 3;
          if (iVar2 != 1) {
            local_128 = 5;
          }
          FUN_0569900c(param_1,&local_128,*(undefined4 *)(lVar10 + 0x14));
        }
        else {
          FUN_0569910c(param_1,param_2,local_12c);
          iVar2 = FUN_0565a3c8(*(undefined8 *)(param_1 + 0x20));
          if (iVar2 == 0) {
            FUN_05699148(param_1,*(undefined4 *)(lVar10 + 0x14));
          }
          else {
            local_128 = 1;
            FUN_0569900c(param_1,&local_128,*(undefined4 *)(lVar10 + 0x14));
          }
        }
      }
    }
    else {
      uVar8 = FUN_056cb740(lVar10 + 0x20);
      if ((uVar8 & 1) != 0) {
        local_c0 = (int *)CONCAT71(local_c0._1_7_,4);
        FUN_056c91c0(&local_128,param_2);
        FUN_05626f58(&uStack_b8,&local_128);
        FUN_0563255c(&local_128);
        FUN_056cb048(lVar10 + 0x20,&local_c0);
        FUN_056caefc(&local_c0);
        goto LAB_056548d0;
      }
      local_60 = 0;
      uStack_78 = 0;
      local_80 = 0;
      uStack_68 = 0;
      uStack_70 = 0;
      uStack_98 = 0;
      local_a0 = 0;
      uStack_88 = 0;
      uStack_90 = 0;
      uStack_a8 = 0;
      local_b0 = 0;
      uStack_b8 = 0;
      local_c0 = (int *)0x0;
      FUN_00069f7c(&local_c0);
      uStack_b8 = uStack_b8 & 0xffffffffffffff00;
      iVar2 = FUN_0565a3c8(*(undefined8 *)(param_1 + 0x20));
      if (iVar2 == 0) {
        if ((char)local_c0 == '\x01') {
          FUN_0563265c((ulong)&local_c0 | 8,param_2);
        }
        else {
          FUN_056323cc((ulong)&local_c0 | 8,param_2);
          local_c0 = (int *)CONCAT71(local_c0._1_7_,1);
        }
      }
      else {
        uVar4 = FUN_0565b9a8();
        uVar9 = *(undefined8 *)(lVar10 + 0x88);
        local_138 = FUN_056cb608(lVar10 + 0x20);
        uVar9 = FUN_0565da90(uVar9,&local_138);
        uVar6 = FUN_05698f44(param_1);
        FUN_0565ba38(&local_128,uVar4,param_2,uVar9,uVar6);
        if ((char)local_c0 == (char)local_128) {
          if ((char)local_c0 != '\0') {
            FUN_05632750((ulong)&local_c0 | 8,auStack_120);
          }
        }
        else if ((char)local_c0 == '\0') {
          FUN_05632480((ulong)&local_c0 | 8,auStack_120);
          local_c0 = (int *)CONCAT71(local_c0._1_7_,1);
        }
        else {
          FUN_0563255c((ulong)&local_c0 | 8);
          uStack_b8 = uStack_b8 & 0xffffffffffffff00;
          local_c0 = (int *)((ulong)local_c0 & 0xffffffffffffff00);
        }
        if ((char)local_128 == '\x01') {
          FUN_0563255c(auStack_120);
        }
      }
      if (((ulong)local_c0 & 1) == 0) {
        *(undefined1 *)(param_1 + 0x2a) = 1;
      }
      else {
        uVar8 = FUN_009ce4a8((ulong)&local_c0 | 8);
        uVar7 = FUN_009ce4a8(param_2);
        if (uVar8 < uVar7) {
          FUN_0569910c(param_1,(ulong)&local_c0 | 8,*(undefined4 *)(lVar10 + 0x10));
          local_128 = 3;
          FUN_0569900c(param_1,&local_128,*(undefined4 *)(lVar10 + 0x14));
        }
        else {
          FUN_0569910c(param_1,param_2,local_12c);
          iVar2 = FUN_0565a3c8(*(undefined8 *)(param_1 + 0x20));
          if (iVar2 == 0) {
            FUN_05699148(param_1,*(undefined4 *)(lVar10 + 0x14));
          }
          else {
            local_128 = 1;
            FUN_0569900c(param_1,&local_128,*(undefined4 *)(lVar10 + 0x14));
          }
        }
      }
    }
    if ((char)local_c0 == '\x01') {
      FUN_0563255c((ulong)&local_c0 | 8);
    }
  }
LAB_056548d0:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


