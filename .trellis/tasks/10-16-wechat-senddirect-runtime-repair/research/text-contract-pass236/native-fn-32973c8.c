// Ghidra inferred pseudocode; requested=0x32973c8
// entry=032973c8 end=03297873

bool FUN_032973c8(long param_1)

{
  byte bVar1;
  bool bVar2;
  int iVar3;
  long lVar4;
  undefined8 uVar5;
  ulong uVar6;
  long lVar7;
  long *plVar8;
  ulong *puVar9;
  undefined *puVar10;
  ulong uVar11;
  long lVar12;
  long *plVar13;
  ulong *puVar14;
  ulong uVar15;
  undefined1 auStack_b0 [8];
  long local_a8;
  long *plStack_a0;
  long local_98;
  undefined **local_90;
  long local_88;
  long *plStack_80;
  long local_78;
  undefined **local_70;
  ulong local_68;
  ulong *local_60;
  long local_58;
  
  if ((*(long *)(param_1 + 0xb0) == 0) && (lVar4 = FUN_04cbaf6c(), param_1 + 0x98 != lVar4)) {
    FUN_027052a4(param_1 + 0xa0,*(undefined8 *)(lVar4 + 0x10),lVar4 + 8);
  }
  lVar4 = FUN_056c28b8(param_1 + 0x58);
  if (*(long *)(lVar4 + 0x90) == 0) {
    FUN_0270583c(&local_70,param_1 + 0x98);
    local_70 = &PTR_FUN_09da63b0;
    uVar5 = FUN_056d63ac(param_1 + 0x58,&local_70);
    FUN_056cb938(auStack_b0,*(undefined8 *)(param_1 + 0xb0));
    FUN_02705c78(&local_90,auStack_b0);
    local_90 = &PTR_FUN_09da5f48;
    FUN_056d6590(uVar5,&local_90);
    if (local_78 != 0) {
      plVar8 = *(long **)(local_88 + 8);
      lVar4 = *plStack_80;
      *(long **)(lVar4 + 8) = plVar8;
      *plVar8 = lVar4;
      local_78 = 0;
      plVar8 = plStack_80;
      while (plVar8 != &local_88) {
        plVar13 = (long *)plVar8[1];
        FUN_056cd5a8(plVar8 + 2);
        __ZdlPvm(plVar8,0x170);
        plVar8 = plVar13;
      }
    }
    if (local_98 != 0) {
      plVar8 = *(long **)(local_a8 + 8);
      lVar4 = *plStack_a0;
      *(long **)(lVar4 + 8) = plVar8;
      *plVar8 = lVar4;
      local_98 = 0;
      plVar8 = plStack_a0;
      while (plVar8 != &local_a8) {
        plVar13 = (long *)plVar8[1];
        FUN_056cb8d0(plVar8 + 2);
        __ZdlPvm(plVar8,0x60);
        plVar8 = plVar13;
      }
    }
    if (local_58 != 0) {
      puVar9 = *(ulong **)(local_68 + 8);
      uVar11 = *local_60;
      *(ulong **)(uVar11 + 8) = puVar9;
      *puVar9 = uVar11;
      local_58 = 0;
      puVar9 = local_60;
      while (puVar9 != &local_68) {
        puVar14 = (ulong *)puVar9[1];
        (**(code **)puVar9[2])();
        __ZdlPvm(puVar9,0x100);
        puVar9 = puVar14;
      }
    }
  }
  local_70 = (undefined **)0x0;
  local_68 = 0;
  local_60 = (ulong *)0x0;
  lVar4 = FUN_056c28b8(param_1 + 0x58);
  if (*(char *)(lVar4 + 0x28) < '\0') {
    for (lVar4 = *(long *)(param_1 + 0xa8); lVar4 != param_1 + 0xa0; lVar4 = *(long *)(lVar4 + 8)) {
      FUN_056c25d4(lVar4 + 0x10);
      uVar5 = FUN_056d9700();
      lVar12 = FUN_056c25d4(lVar4 + 0x10);
      lVar12 = FUN_056c3988(uVar5,lVar12 + 0x48);
      if (lVar12 == 0) {
        if ((DAT_0a3e6404 & 1) == 0) {
          uVar11 = 0;
          do {
            (&DAT_0a3e63e4)[uVar11] = (&DAT_088cdb0d)[uVar11] + 0x69 ^ (&DAT_088cdafd)[uVar11 & 0xf]
            ;
            uVar11 = uVar11 + 1;
          } while (uVar11 != 0x20);
          DAT_0a3e6404 = 1;
        }
        FUN_0562fcc8(&local_90,&DAT_0a3e63e4);
        FUN_056f55e4(param_1,&local_90);
        FUN_0562fd84(&local_90);
        bVar2 = false;
        goto LAB_03297830;
      }
      FUN_056c25d4();
      iVar3 = FUN_056daa0c();
      if (local_68 == (long)local_60 * 0x40) {
        if ((long)(local_68 + 1) < 0) {
                    /* WARNING: Subroutine does not return */
          FUN_007626e4(&local_70);
        }
        uVar15 = (long)local_60 * 0x80;
        uVar11 = (local_68 & 0x3fffffffffffffc0) + 0x40;
        if (uVar15 < uVar11 || uVar15 - uVar11 == 0) {
          uVar15 = uVar11;
        }
        uVar11 = 0x7fffffffffffffff;
        if (local_68 < 0x3fffffffffffffff) {
          uVar11 = uVar15;
        }
        FUN_007625d4(&local_70,uVar11);
      }
      uVar15 = local_68 >> 6;
      uVar11 = 1L << (local_68 & 0x3f);
      if (iVar3 == 0) {
        puVar10 = (undefined *)((ulong)local_70[uVar15] & (uVar11 ^ 0xffffffffffffffff));
      }
      else {
        puVar10 = (undefined *)((ulong)local_70[uVar15] | uVar11);
      }
      local_70[uVar15] = puVar10;
      local_68 = local_68 + 1;
    }
  }
  iVar3 = FUN_056f4d14(*(undefined8 *)(param_1 + 8),param_1 + 0x58);
  if (iVar3 == 0) {
    bVar2 = false;
    goto LAB_03297830;
  }
  bVar1 = *(byte *)(param_1 + 0xb8);
  uVar11 = (ulong)bVar1;
  bVar2 = true;
  if (bVar1 < 3) {
    if (bVar1 == 1) goto LAB_0329778c;
    if (bVar1 == 2) {
      uVar11 = ((*(long **)(param_1 + 0xc0))[1] - **(long **)(param_1 + 0xc0) >> 3) *
               -0x6474a8819ec8e951;
      goto joined_r0x032976e8;
    }
  }
  else {
    if (bVar1 == 3) {
      uVar11 = (*(long **)(param_1 + 0xc0))[1] - **(long **)(param_1 + 0xc0) >> 3;
    }
    else {
      if (bVar1 != 4) goto LAB_03297828;
      uVar11 = (*(long **)(param_1 + 0xc0))[1] - **(long **)(param_1 + 0xc0) >> 4;
    }
joined_r0x032976e8:
    if (uVar11 != 0) {
LAB_0329778c:
      lVar12 = 0;
      lVar4 = 0;
      bVar2 = false;
      uVar15 = 0;
      do {
        bVar1 = *(byte *)(param_1 + 0xb8);
        if (bVar1 < 3) {
          if (bVar1 == 1) {
            lVar7 = *(long *)(param_1 + 0xc0);
          }
          else {
            if (bVar1 != 2) {
LAB_03297870:
                    /* WARNING: Subroutine does not return */
              _abort();
            }
            lVar7 = **(long **)(param_1 + 0xc0) + lVar12;
          }
        }
        else if (bVar1 == 3) {
          lVar7 = *(long *)(**(long **)(param_1 + 0xc0) + uVar15 * 8);
        }
        else {
          if (bVar1 != 4) goto LAB_03297870;
          lVar7 = *(long *)(**(long **)(param_1 + 0xc0) + lVar4);
        }
        uVar6 = FUN_032979e0(param_1,lVar7,&local_70);
        if ((uVar6 & 1) == 0) break;
        uVar15 = uVar15 + 1;
        bVar2 = uVar11 <= uVar15;
        lVar4 = lVar4 + 0x10;
        lVar12 = lVar12 + 0x278;
      } while (uVar11 != uVar15);
    }
  }
LAB_03297828:
  FUN_056f4d80(*(undefined8 *)(param_1 + 8));
LAB_03297830:
  if (local_70 != (undefined **)0x0) {
    __ZdlPvm(local_70,(long)local_60 << 3);
  }
  return bVar2;
}


