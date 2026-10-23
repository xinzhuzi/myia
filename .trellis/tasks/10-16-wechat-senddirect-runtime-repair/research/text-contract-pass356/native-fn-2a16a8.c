// Ghidra inferred pseudocode; requested=0x2a16a8
// entry=002a16a8 end=002a23c7

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_002a16a8(undefined8 param_1,long *param_2)

{
  long lVar1;
  undefined8 *****pppppuVar2;
  undefined8 *puVar3;
  ulong uVar4;
  uint uVar5;
  undefined8 ******ppppppuVar6;
  int *piVar7;
  int iVar8;
  undefined8 uVar9;
  undefined8 *******pppppppuVar10;
  undefined8 uVar11;
  ulong uVar12;
  long lVar13;
  long lVar14;
  ulong uVar15;
  undefined8 ******local_1a0;
  ulong uStack_198;
  ulong local_190;
  undefined8 *******local_188;
  ulong uStack_180;
  ulong local_178;
  undefined8 *******local_170;
  ulong uStack_168;
  ulong local_160;
  undefined8 local_158;
  undefined8 ******local_150;
  undefined8 ******ppppppuStack_148;
  ulong uStack_140;
  undefined8 *******local_138;
  undefined8 *******pppppppuStack_130;
  ulong local_128;
  undefined8 *******pppppppuStack_120;
  ulong local_118;
  ulong uStack_110;
  undefined8 local_108;
  int *local_f8;
  undefined8 local_f0;
  undefined7 local_e0;
  char cStack_d9;
  undefined8 local_d8;
  undefined7 local_c8;
  char cStack_c1;
  undefined8 *****local_b0;
  undefined4 local_a8;
  int *local_a0;
  undefined8 *******local_98;
  ulong uStack_90;
  undefined8 local_88;
  undefined8 local_80;
  undefined4 local_78;
  
  iVar8 = (int)param_1;
  if (3 < iVar8) {
    if (iVar8 < 6) {
      if (iVar8 == 4) {
        uVar9 = __Znwm(0x28);
        FUN_002b3248(uVar9,0);
        return uVar9;
      }
      if (iVar8 == 5) {
        uVar9 = __Znwm(0x28);
        thunk_FUN_002b648c(uVar9,0);
        return uVar9;
      }
      goto LAB_002a1e3c;
    }
    if (iVar8 != 6) {
      if (iVar8 == 10) {
        uVar9 = __Znwm(0x18);
        FUN_002b6850(uVar9,0);
        return uVar9;
      }
      goto LAB_002a1e3c;
    }
    local_118 = 0;
    pppppppuStack_120 = (undefined8 *******)0x0;
    local_108 = 0;
    uStack_110 = 0;
    local_138 = (undefined8 *******)0x0;
    uStack_140 = 0;
    local_128 = 0;
    pppppppuStack_130 = (undefined8 *******)0x0;
    ppppppuStack_148 = (undefined8 ******)0x0;
    local_150 = (undefined8 ******)0x0;
    local_a8 = 0x80000000;
    local_b0 = (undefined8 *****)0x0;
    lVar14 = *(long *)(*param_2 + 0x10);
    if (lVar14 == 0) {
LAB_002a1de4:
      lVar13 = 0;
    }
    else {
      lVar13 = 0;
      do {
        iVar8 = FUN_06ef30ec(lVar14 + 0x18,&DAT_0a51cd68);
        lVar1 = 0x10;
        if (iVar8 == 0) {
          lVar1 = 8;
          lVar13 = lVar14;
        }
        lVar14 = *(long *)(lVar14 + lVar1);
      } while (lVar14 != 0);
      if ((lVar13 == 0) || (iVar8 = FUN_06ef30ec(&DAT_0a51cd68,lVar13 + 0x18), iVar8 != 0))
      goto LAB_002a1de4;
    }
    pppppuVar2 = &local_b0;
    if (lVar13 != 0) {
      pppppuVar2 = (undefined8 *****)(lVar13 + 0x20);
    }
    FUN_06fe1020(&local_80,pppppuVar2);
    FUN_06fe2ce0(&local_a0);
    piVar7 = local_a0;
    uVar5 = local_a0[1];
    uVar12 = (ulong)(int)uVar5;
    uVar15 = *(ulong *)(local_a0 + 4);
    if (uVar5 != 0 && uVar15 < 0x18) {
      FUN_070d5cd0();
LAB_002a23b0:
                    /* WARNING: Subroutine does not return */
      FUN_00018d9c(&local_98);
    }
    if ((int)uVar5 < 0) goto LAB_002a23b0;
    if (uVar5 < 0x17) {
      local_88 = CONCAT17((char)uVar5,(undefined7)local_88);
      pppppppuVar10 = &local_98;
      if (uVar5 != 0) goto LAB_002a1e88;
    }
    else {
      uVar4 = 0x19;
      if ((uVar12 | 7) != 0x17) {
        uVar4 = (uVar12 | 7) + 1;
      }
      pppppppuVar10 = (undefined8 *******)__Znwm(uVar4);
      local_88 = uVar4 | 0x8000000000000000;
      local_98 = pppppppuVar10;
      uStack_90 = uVar12;
LAB_002a1e88:
      _memmove(pppppppuVar10,(void *)(uVar15 + (long)piVar7),uVar12);
    }
    *(undefined1 *)((long)pppppppuVar10 + uVar12) = 0;
    if ((long)local_128 < 0) {
      __ZdlPvm(local_138,local_128 & 0x7fffffffffffffff);
    }
    pppppppuStack_130 = (undefined8 *******)uStack_90;
    local_138 = local_98;
    local_128 = local_88;
    local_88 = local_88 & 0xffffffffffffff;
    local_98 = (undefined8 *******)((ulong)local_98 & 0xffffffffffffff00);
    if (*local_a0 != -1) {
      if (*local_a0 != 0) {
        LOAcquire();
        iVar8 = *local_a0;
        *local_a0 = iVar8 + -1;
        LORelease();
        if (iVar8 != 1) goto LAB_002a1f04;
      }
      FUN_06ea14cc(local_a0,1,8);
    }
LAB_002a1f04:
    FUN_06fe0f68(&local_80);
    FUN_06fe0f68(&local_b0);
    local_a8 = 0x80000000;
    local_b0 = (undefined8 *****)0x0;
    lVar14 = *(long *)(*param_2 + 0x10);
    if (lVar14 == 0) {
LAB_002a1f7c:
      lVar13 = 0;
    }
    else {
      lVar13 = 0;
      do {
        iVar8 = FUN_06ef30ec(lVar14 + 0x18,&DAT_0a51cd70);
        lVar1 = 0x10;
        if (iVar8 == 0) {
          lVar1 = 8;
          lVar13 = lVar14;
        }
        lVar14 = *(long *)(lVar14 + lVar1);
      } while (lVar14 != 0);
      if ((lVar13 == 0) || (iVar8 = FUN_06ef30ec(&DAT_0a51cd70,lVar13 + 0x18), iVar8 != 0))
      goto LAB_002a1f7c;
    }
    pppppuVar2 = &local_b0;
    if (lVar13 != 0) {
      pppppuVar2 = (undefined8 *****)(lVar13 + 0x20);
    }
    FUN_06fe1020(&local_80,pppppuVar2);
    FUN_06fe2ce0(&local_a0);
    piVar7 = local_a0;
    uVar5 = local_a0[1];
    uVar12 = (ulong)(int)uVar5;
    uVar15 = *(ulong *)(local_a0 + 4);
    if ((uVar5 != 0) && (uVar15 < 0x18)) {
      FUN_070d5cd0();
LAB_002a23c0:
                    /* WARNING: Subroutine does not return */
      FUN_00018d9c(&local_98);
    }
    if ((int)uVar5 < 0) goto LAB_002a23c0;
    if (uVar5 < 0x17) {
      local_88 = CONCAT17((char)uVar5,(undefined7)local_88);
      pppppppuVar10 = &local_98;
      if (uVar5 != 0) goto LAB_002a1ff8;
    }
    else {
      uVar4 = 0x19;
      if ((uVar12 | 7) != 0x17) {
        uVar4 = (uVar12 | 7) + 1;
      }
      pppppppuVar10 = (undefined8 *******)__Znwm(uVar4);
      local_88 = uVar4 | 0x8000000000000000;
      local_98 = pppppppuVar10;
      uStack_90 = uVar12;
LAB_002a1ff8:
      _memmove(pppppppuVar10,(void *)(uVar15 + (long)piVar7),uVar12);
    }
    *(undefined1 *)((long)pppppppuVar10 + uVar12) = 0;
    if ((long)uStack_110 < 0) {
      __ZdlPvm(pppppppuStack_120,uStack_110 & 0x7fffffffffffffff);
    }
    local_118 = uStack_90;
    pppppppuStack_120 = local_98;
    uStack_110 = local_88;
    local_88 = local_88 & 0xffffffffffffff;
    local_98 = (undefined8 *******)((ulong)local_98 & 0xffffffffffffff00);
    if (*local_a0 != -1) {
      if (*local_a0 != 0) {
        LOAcquire();
        iVar8 = *local_a0;
        *local_a0 = iVar8 + -1;
        LORelease();
        if (iVar8 != 1) goto LAB_002a2074;
      }
      FUN_06ea14cc(local_a0,1,8);
    }
LAB_002a2074:
    FUN_06fe0f68(&local_80);
    FUN_06fe0f68(&local_b0);
    local_a8 = 0x80000000;
    local_b0 = (undefined8 *****)0x0;
    lVar14 = *(long *)(*param_2 + 0x10);
    if (lVar14 == 0) {
LAB_002a20ec:
      lVar13 = 0;
    }
    else {
      lVar13 = 0;
      do {
        iVar8 = FUN_06ef30ec(lVar14 + 0x18,&DAT_0a51cd78);
        lVar1 = 0x10;
        if (iVar8 == 0) {
          lVar1 = 8;
          lVar13 = lVar14;
        }
        lVar14 = *(long *)(lVar14 + lVar1);
      } while (lVar14 != 0);
      if ((lVar13 == 0) || (iVar8 = FUN_06ef30ec(&DAT_0a51cd78,lVar13 + 0x18), iVar8 != 0))
      goto LAB_002a20ec;
    }
    pppppuVar2 = &local_b0;
    if (lVar13 != 0) {
      pppppuVar2 = (undefined8 *****)(lVar13 + 0x20);
    }
    FUN_06fe1020(&local_80,pppppuVar2);
    FUN_06fe2590(&local_a0);
    FUN_0020ba10(&local_98,&local_a0);
    if ((long)uStack_140 < 0) {
      __ZdlPvm(local_150,uStack_140 & 0x7fffffffffffffff);
    }
    ppppppuStack_148 = (undefined8 ******)uStack_90;
    local_150 = local_98;
    uStack_140 = local_88;
    local_88 = local_88 & 0xffffffffffffff;
    local_98 = (undefined8 *******)((ulong)local_98 & 0xffffffffffffff00);
    if (*local_a0 != -1) {
      if (*local_a0 != 0) {
        LOAcquire();
        iVar8 = *local_a0;
        *local_a0 = iVar8 + -1;
        LORelease();
        if (iVar8 != 1) goto LAB_002a217c;
      }
      FUN_06ea14cc(local_a0,2,8);
    }
LAB_002a217c:
    FUN_06fe0f68(&local_80);
    FUN_06fe0f68(&local_b0);
    local_78 = 0x80000000;
    local_80 = 0;
    lVar14 = *(long *)(*param_2 + 0x10);
    if (lVar14 != 0) {
      lVar13 = 0;
      do {
        iVar8 = FUN_06ef30ec(lVar14 + 0x18,&DAT_0a51cd80);
        lVar1 = 0x10;
        if (iVar8 == 0) {
          lVar1 = 8;
          lVar13 = lVar14;
        }
        lVar14 = *(long *)(lVar14 + lVar1);
      } while (lVar14 != 0);
      if ((lVar13 != 0) && (iVar8 = FUN_06ef30ec(&DAT_0a51cd80,lVar13 + 0x18), iVar8 == 0))
      goto LAB_002a21f8;
    }
    lVar13 = 0;
LAB_002a21f8:
    puVar3 = &local_80;
    if (lVar13 != 0) {
      puVar3 = (undefined8 *)(lVar13 + 0x20);
    }
    uVar9 = FUN_06fe1020(&local_98,puVar3);
    uVar9 = FUN_06fe3db4(uVar9,0);
    local_108 = uVar9;
    FUN_06fe0f68(&local_98);
    FUN_06fe0f68(&local_80);
    uVar11 = __Znwm(0x70);
    if ((long)uStack_140 < 0) {
      FUN_00018d20(&local_1a0,local_150,ppppppuStack_148);
    }
    else {
      uStack_198 = (ulong)ppppppuStack_148;
      local_1a0 = local_150;
      local_190 = uStack_140;
    }
    if ((long)local_128 < 0) {
      FUN_00018d20(&local_188,local_138,pppppppuStack_130);
    }
    else {
      uStack_180 = (ulong)pppppppuStack_130;
      local_188 = local_138;
      local_178 = local_128;
    }
    if ((long)uStack_110 < 0) {
      FUN_00018d20(&local_170,pppppppuStack_120,local_118);
    }
    else {
      uStack_168 = local_118;
      local_170 = pppppppuStack_120;
      local_160 = uStack_110;
    }
    local_158 = uVar9;
    thunk_FUN_002b355c(uVar11,0,&local_1a0);
    if ((long)local_160 < 0) {
      __ZdlPvm(local_170,local_160 & 0x7fffffffffffffff);
    }
    if ((long)local_178 < 0) {
      __ZdlPvm(local_188,local_178 & 0x7fffffffffffffff);
    }
    if ((long)local_190 < 0) {
      __ZdlPvm(local_1a0,local_190 & 0x7fffffffffffffff);
    }
    if ((long)uStack_110 < 0) {
      __ZdlPvm(pppppppuStack_120,uStack_110 & 0x7fffffffffffffff);
    }
    if ((long)local_128 < 0) {
      __ZdlPvm(local_138,local_128 & 0x7fffffffffffffff);
    }
    if (-1 < (long)uStack_140) {
      return uVar11;
    }
    __ZdlPvm(local_150,uStack_140 & 0x7fffffffffffffff);
    return uVar11;
  }
  if (1 < iVar8) {
    if (iVar8 == 2) {
      uVar9 = __Znwm(0x48);
      thunk_FUN_002a3820(uVar9,0);
      return uVar9;
    }
    if (iVar8 == 3) {
      uVar9 = __Znwm(0x20);
      FUN_002b2e88(uVar9,0);
      return uVar9;
    }
LAB_002a1e3c:
    uVar9 = FUN_002a2da4(param_1,param_2);
    return uVar9;
  }
  if (iVar8 == 0) {
    return 0;
  }
  if (iVar8 != 1) goto LAB_002a1e3c;
  local_150 = (undefined8 ******)&DAT_0a2320b0;
  uStack_110 = _UNK_0848c0f8;
  local_118 = _DAT_0848c0f0;
  uStack_140 = 0;
  ppppppuStack_148 = (undefined8 ******)0x0;
  pppppppuStack_130 = (undefined8 *******)0x0;
  local_138 = (undefined8 *******)0x0;
  pppppppuStack_120 = (undefined8 *******)0x0;
  local_128 = 0;
  local_78 = 0x80000000;
  local_80 = 0;
  lVar14 = *(long *)(*param_2 + 0x10);
  if (lVar14 == 0) {
LAB_002a1778:
    lVar13 = 0;
  }
  else {
    lVar13 = 0;
    do {
      iVar8 = FUN_06ef30ec(lVar14 + 0x18,&DAT_0a51cd30);
      lVar1 = 0x10;
      if (iVar8 == 0) {
        lVar1 = 8;
        lVar13 = lVar14;
      }
      lVar14 = *(long *)(lVar14 + lVar1);
    } while (lVar14 != 0);
    if ((lVar13 == 0) || (iVar8 = FUN_06ef30ec(&DAT_0a51cd30,lVar13 + 0x18), iVar8 != 0))
    goto LAB_002a1778;
  }
  puVar3 = &local_80;
  if (lVar13 != 0) {
    puVar3 = (undefined8 *)(lVar13 + 0x20);
  }
  FUN_06fe1020(&local_98,puVar3);
  FUN_06fe2590(&local_b0);
  ppppppuVar6 = local_150;
  local_150 = (undefined8 ******)local_b0;
  local_b0 = ppppppuVar6;
  if (*(int *)ppppppuVar6 != -1) {
    if (*(int *)ppppppuVar6 != 0) {
      LOAcquire();
      iVar8 = *(int *)ppppppuVar6;
      *(int *)ppppppuVar6 = iVar8 + -1;
      LORelease();
      if (iVar8 != 1) goto LAB_002a17dc;
    }
    FUN_06ea14cc(ppppppuVar6,2,8);
  }
LAB_002a17dc:
  FUN_06fe0f68(&local_98);
  FUN_06fe0f68(&local_80);
  local_a8 = 0x80000000;
  local_b0 = (undefined8 *****)0x0;
  lVar14 = *(long *)(*param_2 + 0x10);
  if (lVar14 == 0) {
LAB_002a1850:
    lVar13 = 0;
  }
  else {
    lVar13 = 0;
    do {
      iVar8 = FUN_06ef30ec(lVar14 + 0x18,&DAT_0a51cd48);
      lVar1 = 0x10;
      if (iVar8 == 0) {
        lVar1 = 8;
        lVar13 = lVar14;
      }
      lVar14 = *(long *)(lVar14 + lVar1);
    } while (lVar14 != 0);
    if ((lVar13 == 0) || (iVar8 = FUN_06ef30ec(&DAT_0a51cd48,lVar13 + 0x18), iVar8 != 0))
    goto LAB_002a1850;
  }
  pppppuVar2 = &local_b0;
  if (lVar13 != 0) {
    pppppuVar2 = (undefined8 *****)(lVar13 + 0x20);
  }
  FUN_06fe1020(&local_80,pppppuVar2);
  FUN_06fe2590(&local_a0);
  FUN_0020ba10(&local_98,&local_a0);
  if ((long)pppppppuStack_120 < 0) {
    __ZdlPvm(pppppppuStack_130,(ulong)pppppppuStack_120 & 0x7fffffffffffffff);
  }
  local_128 = uStack_90;
  pppppppuStack_130 = local_98;
  pppppppuStack_120 = (undefined8 *******)local_88;
  local_88 = local_88 & 0xffffffffffffff;
  local_98 = (undefined8 *******)((ulong)local_98 & 0xffffffffffffff00);
  if (*local_a0 != -1) {
    if (*local_a0 != 0) {
      LOAcquire();
      iVar8 = *local_a0;
      *local_a0 = iVar8 + -1;
      LORelease();
      if (iVar8 != 1) goto LAB_002a18e8;
    }
    FUN_06ea14cc(local_a0,2,8);
  }
LAB_002a18e8:
  FUN_06fe0f68(&local_80);
  FUN_06fe0f68(&local_b0);
  local_a8 = 0x80000000;
  local_b0 = (undefined8 *****)0x0;
  lVar14 = *(long *)(*param_2 + 0x10);
  if (lVar14 == 0) {
LAB_002a1960:
    lVar13 = 0;
  }
  else {
    lVar13 = 0;
    do {
      iVar8 = FUN_06ef30ec(lVar14 + 0x18,&DAT_0a51cd50);
      lVar1 = 0x10;
      if (iVar8 == 0) {
        lVar1 = 8;
        lVar13 = lVar14;
      }
      lVar14 = *(long *)(lVar14 + lVar1);
    } while (lVar14 != 0);
    if ((lVar13 == 0) || (iVar8 = FUN_06ef30ec(&DAT_0a51cd50,lVar13 + 0x18), iVar8 != 0))
    goto LAB_002a1960;
  }
  pppppuVar2 = &local_b0;
  if (lVar13 != 0) {
    pppppuVar2 = (undefined8 *****)(lVar13 + 0x20);
  }
  FUN_06fe1020(&local_80,pppppuVar2);
  FUN_06fe2590(&local_a0);
  FUN_0020ba10(&local_98,&local_a0);
  if ((long)local_138 < 0) {
    __ZdlPvm(ppppppuStack_148,(ulong)local_138 & 0x7fffffffffffffff);
  }
  uStack_140 = uStack_90;
  ppppppuStack_148 = local_98;
  local_138 = (undefined8 *******)local_88;
  local_88 = local_88 & 0xffffffffffffff;
  local_98 = (undefined8 *******)((ulong)local_98 & 0xffffffffffffff00);
  if (*local_a0 != -1) {
    if (*local_a0 != 0) {
      LOAcquire();
      iVar8 = *local_a0;
      *local_a0 = iVar8 + -1;
      LORelease();
      if (iVar8 != 1) goto LAB_002a19f4;
    }
    FUN_06ea14cc(local_a0,2,8);
  }
LAB_002a19f4:
  FUN_06fe0f68(&local_80);
  FUN_06fe0f68(&local_b0);
  local_78 = 0x80000000;
  local_80 = 0;
  lVar14 = *(long *)(*param_2 + 0x10);
  if (lVar14 == 0) {
LAB_002a1a6c:
    lVar13 = 0;
  }
  else {
    lVar13 = 0;
    do {
      iVar8 = FUN_06ef30ec(lVar14 + 0x18,&DAT_0a51cd58);
      lVar1 = 0x10;
      if (iVar8 == 0) {
        lVar1 = 8;
        lVar13 = lVar14;
      }
      lVar14 = *(long *)(lVar14 + lVar1);
    } while (lVar14 != 0);
    if ((lVar13 == 0) || (iVar8 = FUN_06ef30ec(&DAT_0a51cd58,lVar13 + 0x18), iVar8 != 0))
    goto LAB_002a1a6c;
  }
  puVar3 = &local_80;
  if (lVar13 != 0) {
    puVar3 = (undefined8 *)(lVar13 + 0x20);
  }
  FUN_06fe1020(&local_98,puVar3);
  FUN_06fe2590(&local_b0);
  local_118 = FUN_06efb4dc(&local_b0,0,10);
  if (*(int *)local_b0 != -1) {
    if (*(int *)local_b0 != 0) {
      LOAcquire();
      iVar8 = *(int *)local_b0;
      *(int *)local_b0 = iVar8 + -1;
      LORelease();
      if (iVar8 != 1) goto LAB_002a1ad4;
    }
    FUN_06ea14cc(local_b0,2,8);
  }
LAB_002a1ad4:
  FUN_06fe0f68(&local_98);
  FUN_06fe0f68(&local_80);
  local_78 = 0x80000000;
  local_80 = 0;
  lVar14 = *(long *)(*param_2 + 0x10);
  if (lVar14 == 0) {
LAB_002a1b4c:
    lVar13 = 0;
  }
  else {
    lVar13 = 0;
    do {
      iVar8 = FUN_06ef30ec(lVar14 + 0x18,&DAT_0a51cd60);
      lVar1 = 0x10;
      if (iVar8 == 0) {
        lVar1 = 8;
        lVar13 = lVar14;
      }
      lVar14 = *(long *)(lVar14 + lVar1);
    } while (lVar14 != 0);
    if ((lVar13 == 0) || (iVar8 = FUN_06ef30ec(&DAT_0a51cd60,lVar13 + 0x18), iVar8 != 0))
    goto LAB_002a1b4c;
  }
  puVar3 = &local_80;
  if (lVar13 != 0) {
    puVar3 = (undefined8 *)(lVar13 + 0x20);
  }
  FUN_06fe1020(&local_98,puVar3);
  FUN_06fe2590(&local_b0);
  uStack_110 = FUN_06efb52c(&local_b0,0,10);
  if (*(int *)local_b0 != -1) {
    if (*(int *)local_b0 != 0) {
      LOAcquire();
      iVar8 = *(int *)local_b0;
      *(int *)local_b0 = iVar8 + -1;
      LORelease();
      if (iVar8 != 1) goto LAB_002a1bb4;
    }
    FUN_06ea14cc(local_b0,2,8);
  }
LAB_002a1bb4:
  FUN_06fe0f68(&local_98);
  FUN_06fe0f68(&local_80);
  uVar9 = __Znwm(0x70);
  FUN_002a265c(&local_f8,&local_150);
  thunk_FUN_002b2454(uVar9,0,&local_f8);
  if (cStack_c1 < '\0') {
    __ZdlPvm(local_d8,CONCAT17(cStack_c1,local_c8) & 0x7fffffffffffffff);
  }
  if (cStack_d9 < '\0') {
    __ZdlPvm(local_f0,CONCAT17(cStack_d9,local_e0) & 0x7fffffffffffffff);
  }
  if (*local_f8 != -1) {
    if (*local_f8 != 0) {
      LOAcquire();
      iVar8 = *local_f8;
      *local_f8 = iVar8 + -1;
      LORelease();
      if (iVar8 != 1) goto LAB_002a1c50;
    }
    FUN_06ea14cc(local_f8,2,8);
  }
LAB_002a1c50:
  if ((long)pppppppuStack_120 < 0) {
    __ZdlPvm(pppppppuStack_130,(ulong)pppppppuStack_120 & 0x7fffffffffffffff);
  }
  if ((long)local_138 < 0) {
    __ZdlPvm(ppppppuStack_148,(ulong)local_138 & 0x7fffffffffffffff);
  }
  if (*(int *)local_150 != -1) {
    if (*(int *)local_150 != 0) {
      LOAcquire();
      iVar8 = *(int *)local_150;
      *(int *)local_150 = iVar8 + -1;
      LORelease();
      if (iVar8 != 1) {
        return uVar9;
      }
    }
    FUN_06ea14cc(local_150,2,8);
  }
  return uVar9;
}


