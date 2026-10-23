// Ghidra inferred pseudocode; requested=0x3263cd4
// entry=03263cd4 end=03263f93

/* WARNING: Removing unreachable block (ram,0x03263f40) */

void FUN_03263cd4(undefined8 param_1,undefined8 param_2,long *param_3)

{
  long lVar1;
  undefined4 uVar2;
  byte bVar3;
  undefined8 *puVar4;
  bool bVar5;
  ulong uVar6;
  long lVar7;
  undefined8 *puVar8;
  ulong *puVar9;
  undefined8 *puVar10;
  long lVar11;
  undefined8 *puVar12;
  undefined8 uVar13;
  undefined8 uVar14;
  undefined8 *local_b0;
  undefined8 *puStack_a8;
  undefined8 *local_a0;
  undefined1 *local_98;
  undefined8 *local_88;
  undefined8 local_80;
  long local_78;
  undefined1 uStack_69;
  undefined8 **local_68;
  
  local_80 = 0;
  local_78 = 0;
  lVar11 = *param_3;
  lVar1 = param_3[1];
  local_88 = &local_80;
  if (lVar11 != lVar1) {
    do {
      uVar6 = FUN_048a1fac(*(undefined4 *)(lVar11 + 0xc));
      if ((uVar6 & 1) != 0) {
        lVar7 = FUN_04cc2258(lVar11);
        bVar3 = *(byte *)(lVar7 + 0x1f);
        uVar6 = *(ulong *)(lVar7 + 0x10);
        if (-1 < (char)bVar3) {
          uVar6 = (ulong)bVar3;
        }
        if (uVar6 != 0) {
          uVar6 = *(ulong *)(lVar11 + 0x100);
          puStack_a8 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
          local_b0 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
          local_98 = &SUB_aaaaaaaaaaaaaaaa;
          local_a0 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
          uVar2 = *(undefined4 *)(lVar11 + 0x114);
          if ((char)bVar3 < '\0') {
            FUN_00018d20(&local_b0,*(undefined8 *)(lVar7 + 8));
          }
          else {
            puStack_a8 = *(undefined8 **)(lVar7 + 0x10);
            local_b0 = *(undefined8 **)(lVar7 + 8);
            local_a0 = *(undefined8 **)(lVar7 + 0x18);
          }
          local_98 = (undefined1 *)CONCAT44(local_98._4_4_,uVar2);
          puVar8 = (undefined8 *)FUN_03291c18(&local_88,&local_b0);
          uVar6 = (uVar6 / 1000) * 1000;
          if (&local_80 == puVar8) {
            local_68 = &local_b0;
            lVar7 = FUN_03291dc0(&local_88,&local_b0,&DAT_08b7a8b8,&local_68,&uStack_69);
            puVar9 = (ulong *)(lVar7 + 0x40);
LAB_03263e08:
            *puVar9 = uVar6;
          }
          else {
            puVar9 = puVar8 + 8;
            if (uVar6 < *puVar9) goto LAB_03263e08;
          }
          if ((long)local_a0 < 0) {
            __ZdlPvm(local_b0,(ulong)local_a0 & 0x7fffffffffffffff);
          }
        }
      }
      lVar11 = lVar11 + 0x278;
    } while (lVar11 != lVar1);
    if (local_78 != 0) {
      local_b0 = (undefined8 *)0x0;
      puStack_a8 = (undefined8 *)0x0;
      local_a0 = (undefined8 *)0x0;
      FUN_03263ff4(&local_b0);
      puVar8 = puStack_a8;
      puVar10 = local_88;
      while (puStack_a8 = puVar8, puVar10 != &local_80) {
        if (puVar8 < local_a0) {
          if (*(char *)((long)puVar10 + 0x37) < '\0') {
            FUN_00018d20(puVar8,puVar10[4],puVar10[5]);
          }
          else {
            uVar14 = puVar10[5];
            uVar13 = puVar10[4];
            puVar8[2] = puVar10[6];
            puVar8[1] = uVar14;
            *puVar8 = uVar13;
          }
          *(undefined4 *)(puVar8 + 3) = *(undefined4 *)(puVar10 + 7);
          puVar8[4] = puVar10[8];
          puVar8 = puVar8 + 5;
        }
        else {
          puVar8 = (undefined8 *)FUN_0329208c(&local_b0,puVar10 + 4,puVar10 + 7,puVar10 + 8);
        }
        puVar4 = (undefined8 *)puVar10[1];
        puVar12 = puVar10;
        if ((undefined8 *)puVar10[1] == (undefined8 *)0x0) {
          do {
            puVar10 = (undefined8 *)puVar12[2];
            bVar5 = (undefined8 *)*puVar10 != puVar12;
            puVar12 = puVar10;
          } while (bVar5);
        }
        else {
          do {
            puVar10 = puVar4;
            puVar4 = (undefined8 *)*puVar10;
          } while ((undefined8 *)*puVar10 != (undefined8 *)0x0);
        }
      }
      FUN_03262d74(param_1,param_2,&local_b0);
      if (local_b0 != (undefined8 *)0x0) {
        for (; puStack_a8 != local_b0; puStack_a8 = puStack_a8 + -5) {
        }
        puStack_a8 = local_b0;
        __ZdlPvm(local_b0,(long)local_a0 - (long)local_b0);
      }
    }
  }
  FUN_03291bbc(&local_88,local_80);
  return;
}


