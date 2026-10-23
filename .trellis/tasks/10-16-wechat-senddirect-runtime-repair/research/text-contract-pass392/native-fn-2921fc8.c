// Ghidra inferred pseudocode; requested=0x2921fc8
// entry=02921fc8 end=029223ab

void FUN_02921fc8(undefined8 *param_1,undefined8 *param_2)

{
  undefined1 *puVar1;
  undefined1 *puVar2;
  ulong uVar3;
  byte bVar4;
  ulong uVar5;
  uint uVar6;
  int iVar7;
  undefined1 *puVar8;
  undefined8 *****pppppuVar9;
  undefined8 *puVar10;
  undefined8 *puVar11;
  undefined1 *puVar12;
  undefined1 *puVar13;
  undefined1 *puVar14;
  undefined8 uVar15;
  undefined8 ****local_90;
  undefined1 *local_88;
  undefined8 local_80;
  undefined8 ****local_78;
  undefined1 *local_70;
  undefined8 local_68;
  
  local_70 = &SUB_aaaaaaaaaaaaaaaa;
  local_68 = &SUB_aaaaaaaaaaaaaaaa;
  local_78 = (undefined8 ****)&SUB_aaaaaaaaaaaaaaaa;
  if ((DAT_0a3a6192 & 1) == 0) {
    DAT_0a3a6188 = DAT_0858c920;
    DAT_0a3a6190 = 0x5b;
    DAT_0a3a6192 = 1;
  }
  puVar8 = (undefined1 *)_strlen((char *)&DAT_0a3a6188);
  if ((undefined1 *)0x7ffffffffffffff7 < puVar8) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_78);
  }
  if (puVar8 < (undefined1 *)0x17) {
    local_68 = (undefined1 *)CONCAT17((char)puVar8,(undefined7)local_68);
    pppppuVar9 = &local_78;
    if (puVar8 != (undefined1 *)0x0) goto LAB_0292208c;
  }
  else {
    uVar5 = 0x19;
    if (((ulong)puVar8 | 7) != 0x17) {
      uVar5 = ((ulong)puVar8 | 7) + 1;
    }
    pppppuVar9 = (undefined8 *****)__Znwm(uVar5);
    local_68 = (undefined1 *)(uVar5 | 0x8000000000000000);
    local_78 = pppppuVar9;
    local_70 = puVar8;
LAB_0292208c:
    _memcpy(pppppuVar9,&DAT_0a3a6188,(size_t)puVar8);
  }
  *(undefined1 *)((long)pppppuVar9 + (long)puVar8) = 0;
  local_88 = &SUB_aaaaaaaaaaaaaaaa;
  local_80 = &SUB_aaaaaaaaaaaaaaaa;
  local_90 = (undefined8 ****)&SUB_aaaaaaaaaaaaaaaa;
  if ((DAT_0a3a6198 & 1) == 0) {
    DAT_0a3a6194 = (undefined4)DAT_0858c928;
    DAT_0a3a6198 = 1;
  }
  puVar8 = (undefined1 *)_strlen((char *)&DAT_0a3a6194);
  if ((undefined1 *)0x7ffffffffffffff7 < puVar8) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_90);
  }
  if (puVar8 < (undefined1 *)0x17) {
    local_80 = (undefined1 *)CONCAT17((char)puVar8,(undefined7)local_80);
    pppppuVar9 = &local_90;
    if (puVar8 != (undefined1 *)0x0) goto LAB_0292212c;
  }
  else {
    uVar5 = 0x19;
    if (((ulong)puVar8 | 7) != 0x17) {
      uVar5 = ((ulong)puVar8 | 7) + 1;
    }
    pppppuVar9 = (undefined8 *****)__Znwm(uVar5);
    local_80 = (undefined1 *)(uVar5 | 0x8000000000000000);
    local_90 = pppppuVar9;
    local_88 = puVar8;
LAB_0292212c:
    _memcpy(pppppuVar9,&DAT_0a3a6194,(size_t)puVar8);
  }
  *(undefined1 *)((long)pppppuVar9 + (long)puVar8) = 0;
  bVar4 = *(byte *)((long)param_2 + 0x17);
  puVar14 = (undefined1 *)(ulong)bVar4;
  puVar12 = (undefined1 *)param_2[1];
  puVar8 = puVar12;
  if (-1 < (char)bVar4) {
    puVar8 = puVar14;
  }
  puVar1 = local_70;
  if (-1 < (long)local_68) {
    puVar1 = (undefined1 *)((ulong)local_68 >> 0x38);
  }
  uVar6 = (uint)(char)local_80._7_1_;
  puVar2 = local_88;
  if (-1 < (int)uVar6) {
    puVar2 = (undefined1 *)(ulong)local_80._7_1_;
  }
  uVar5 = (long)puVar8 - (long)(puVar2 + (long)puVar1);
  if (puVar8 < puVar2 + (long)puVar1) {
LAB_02922190:
    if ((char)bVar4 < '\0') {
      FUN_00018d20(param_1,*param_2,puVar12);
    }
    else {
      uVar15 = *param_2;
      param_1[1] = param_2[1];
      *param_1 = uVar15;
      param_1[2] = param_2[2];
    }
    if ((uVar6 >> 7 & 1) == 0) goto joined_r0x029221e4;
  }
  else {
    puVar11 = param_2;
    if ((char)bVar4 < '\0') {
      if (puVar1 == (undefined1 *)0xffffffffffffffff) goto LAB_02922398;
      puVar13 = puVar12;
      if (puVar1 <= puVar12) {
        puVar13 = puVar1;
      }
      puVar10 = (undefined8 *)*param_2;
    }
    else {
      if (puVar1 == (undefined1 *)0xffffffffffffffff) goto LAB_02922398;
      puVar10 = param_2;
      puVar13 = puVar14;
      if (puVar1 <= puVar14) {
        puVar13 = puVar1;
      }
    }
    pppppuVar9 = (undefined8 *****)local_78;
    if (-1 < (long)local_68) {
      pppppuVar9 = &local_78;
    }
    iVar7 = _memcmp(puVar10,pppppuVar9,(size_t)puVar13);
    if ((iVar7 != 0) || (puVar13 != puVar1)) goto LAB_02922190;
    puVar8 = puVar8 + -(long)puVar2;
    if ((char)bVar4 < '\0') {
      if ((puVar2 == (undefined1 *)0xffffffffffffffff) || (puVar12 < puVar8)) goto LAB_02922398;
      puVar13 = puVar12 + -(long)puVar8;
      if (puVar2 <= puVar12 + -(long)puVar8) {
        puVar13 = puVar2;
      }
      puVar11 = (undefined8 *)*param_2;
    }
    else {
      if ((puVar14 < puVar8) || (puVar2 == (undefined1 *)0xffffffffffffffff)) goto LAB_02922398;
      puVar13 = puVar14 + -(long)puVar8;
      if (puVar2 <= puVar14 + -(long)puVar8) {
        puVar13 = puVar2;
      }
    }
    pppppuVar9 = (undefined8 *****)local_90;
    if (-1 < (int)uVar6) {
      pppppuVar9 = &local_90;
    }
    iVar7 = _memcmp((undefined1 *)((long)puVar11 + (long)puVar8),pppppuVar9,(size_t)puVar13);
    if ((iVar7 != 0) || (puVar13 != puVar2)) goto LAB_02922190;
    puVar11 = param_1;
    if ((char)bVar4 < '\0') {
      if (puVar12 < puVar1) goto LAB_02922398;
      param_2 = (undefined8 *)*param_2;
    }
    else {
      puVar12 = puVar14;
      if (puVar14 < puVar1) {
LAB_02922398:
                    /* WARNING: Subroutine does not return */
        FUN_0020edd0(puVar11);
      }
    }
    uVar3 = (long)puVar12 - (long)puVar1;
    if (uVar5 <= (ulong)((long)puVar12 - (long)puVar1)) {
      uVar3 = uVar5;
    }
    if (0x7ffffffffffffff7 < uVar3) {
                    /* WARNING: Subroutine does not return */
      FUN_00018d9c(param_1);
    }
    if (uVar3 < 0x17) {
      *(char *)((long)param_1 + 0x17) = (char)uVar3;
      if (uVar3 != 0) goto LAB_02922320;
    }
    else {
      uVar5 = 0x19;
      if ((uVar3 | 7) != 0x17) {
        uVar5 = (uVar3 | 7) + 1;
      }
      puVar11 = (undefined8 *)__Znwm(uVar5);
      param_1[1] = uVar3;
      param_1[2] = uVar5 | 0x8000000000000000;
      *param_1 = puVar11;
LAB_02922320:
      _memmove(puVar11,(undefined1 *)((long)param_2 + (long)puVar1),uVar3);
      param_1 = puVar11;
    }
    *(undefined1 *)((long)param_1 + uVar3) = 0;
    if (-1 < (long)local_80) goto joined_r0x029221e4;
  }
  __ZdlPvm(local_90,(ulong)local_80 & 0x7fffffffffffffff);
joined_r0x029221e4:
  if ((long)local_68 < 0) {
    __ZdlPvm(local_78,(ulong)local_68 & 0x7fffffffffffffff);
    return;
  }
  return;
}


