// Ghidra inferred pseudocode; requested=0x56f3be0
// entry=056f3be0 end=056f3d97

void FUN_056f3be0(char *param_1,long *param_2,undefined8 param_3)

{
  uint uVar1;
  undefined8 uVar2;
  ulong uVar3;
  long lVar4;
  long *plVar5;
  long lVar6;
  long lVar7;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined1 *local_90;
  undefined1 *puStack_88;
  undefined1 *local_80;
  undefined1 *puStack_78;
  undefined1 *puStack_70;
  undefined1 *puStack_68;
  undefined1 *local_60;
  undefined1 *puStack_58;
  undefined1 *puStack_50;
  undefined1 *puStack_48;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  param_1[8] = '\0';
  param_1[9] = '\0';
  param_1[10] = '\0';
  param_1[0xb] = '\0';
  param_1[0xc] = '\0';
  param_1[0xd] = '\0';
  param_1[0xe] = '\0';
  param_1[0xf] = '\0';
  param_1[0] = '\0';
  param_1[1] = '\0';
  param_1[2] = '\0';
  param_1[3] = '\0';
  param_1[4] = '\0';
  param_1[5] = '\0';
  param_1[6] = '\0';
  param_1[7] = '\0';
  param_1[0x18] = '\0';
  param_1[0x19] = '\0';
  param_1[0x1a] = '\0';
  param_1[0x1b] = '\0';
  param_1[0x1c] = '\0';
  param_1[0x1d] = '\0';
  param_1[0x1e] = '\0';
  param_1[0x1f] = '\0';
  param_1[0x10] = '\0';
  param_1[0x11] = '\0';
  param_1[0x12] = '\0';
  param_1[0x13] = '\0';
  param_1[0x14] = '\0';
  param_1[0x15] = '\0';
  param_1[0x16] = '\0';
  param_1[0x17] = '\0';
  FUN_00069f7c(param_1);
  param_1[8] = '\0';
  puStack_58 = &SUB_aaaaaaaaaaaaaaaa;
  local_60 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_48 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_50 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_78 = &SUB_aaaaaaaaaaaaaaaa;
  local_80 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_68 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_70 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_88 = &SUB_aaaaaaaaaaaaaaaa;
  local_90 = &SUB_aaaaaaaaaaaaaaaa;
  (**(code **)(*param_2 + 0x10))(&local_90,param_2,0);
  if (puStack_78 != (undefined1 *)0x0) {
    uVar2 = FUN_0564668c(&local_90);
    uVar3 = FUN_05646028(uVar2,param_3);
    if ((uVar3 & 1) == 0) {
      FUN_0564668c(&local_90);
      uVar2 = FUN_0109d770();
      FUN_056f2390(param_2,uVar2);
    }
    else {
      FUN_0564668c(&local_90);
      uVar1 = FUN_05646030();
      if (uVar1 != 0) {
        FUN_0564668c(&local_90);
        uVar3 = FUN_05646050();
        if ((uVar3 & 1) == 0) {
          FUN_0564668c(&local_90);
          FUN_056460a8(&local_b0);
          if (*param_1 == '\x01') {
            lVar7 = *(long *)(param_1 + 8);
            if (lVar7 != 0) {
              lVar4 = *(long *)(param_1 + 0x10);
              lVar6 = lVar7;
              if (lVar4 != lVar7) {
                do {
                  lVar4 = FUN_056caefc(lVar4 + -0x68);
                } while (lVar4 != lVar7);
                lVar6 = *(long *)(param_1 + 8);
              }
              *(long *)(param_1 + 0x10) = lVar7;
              __ZdlPvm(lVar6,*(long *)(param_1 + 0x18) - lVar6);
            }
            *(undefined8 *)(param_1 + 0x10) = uStack_a8;
            *(undefined8 *)(param_1 + 8) = local_b0;
            *(undefined8 *)(param_1 + 0x18) = local_a0;
          }
          else {
            *(undefined8 *)(param_1 + 0x10) = uStack_a8;
            *(undefined8 *)(param_1 + 8) = local_b0;
            *(undefined8 *)(param_1 + 0x18) = local_a0;
            *param_1 = '\x01';
          }
        }
      }
      plVar5 = (long *)FUN_0564668c(&local_90);
      (**(code **)(*plVar5 + 0x80))();
      if ((uVar1 & 1) == 0) {
        FUN_0564668c(&local_90);
        uVar2 = FUN_0109d770();
        FUN_056f2390(param_2,uVar2);
      }
    }
  }
  thunk_FUN_05646544(&local_90);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


