// Ghidra inferred pseudocode; requested=0x465d11c
// entry=0465d11c end=0465d307

/* WARNING: Type propagation algorithm not settling */

int FUN_0465d11c(long param_1)

{
  uint uVar1;
  int iVar2;
  int iVar3;
  undefined8 uVar4;
  uint uVar5;
  uint uVar6;
  uint uVar7;
  byte bVar8;
  long lVar9;
  
  bVar8 = *(byte *)(param_1 + 0x34);
  uVar5 = (uint)bVar8;
  if (bVar8 == 0) {
    iVar2 = 0;
    goto LAB_0465d2f0;
  }
  if ((bVar8 & 1) == 0) {
    iVar2 = 0;
    if ((bVar8 >> 1 & 1) != 0) {
LAB_0465d194:
      lVar9 = *(long *)(param_1 + 0x10);
      bVar8 = *(byte *)(lVar9 + 0x17);
      uVar6 = (uint)bVar8;
      uVar7 = (uint)*(undefined8 *)(lVar9 + 8);
      uVar1 = uVar7;
      if (-1 < (char)bVar8) {
        uVar1 = uVar6;
      }
      if (uVar1 < 0x80) {
        iVar3 = 1;
      }
      else {
        iVar3 = FUN_0571a3d8();
        bVar8 = *(byte *)(lVar9 + 0x17);
        uVar6 = (uint)bVar8;
        uVar7 = (uint)*(undefined8 *)(lVar9 + 8);
        uVar5 = *(uint *)(param_1 + 0x34);
      }
      if (-1 < (char)bVar8) {
        uVar7 = uVar6;
      }
      iVar2 = iVar2 + iVar3 + uVar7 + 1;
    }
  }
  else {
    lVar9 = *(long *)(param_1 + 8);
    if (lVar9 == 0) {
      lVar9 = *(long *)(DAT_0a51ea38 + 8);
    }
    uVar4 = FUN_04f37cb0(lVar9);
    if ((uint)uVar4 < 0x80) {
      iVar2 = 1;
    }
    else {
      iVar2 = FUN_0571a3d8(uVar4);
    }
    iVar2 = (uint)uVar4 + iVar2 + 1;
    uVar5 = *(uint *)(param_1 + 0x34);
    if ((uVar5 >> 1 & 1) != 0) goto LAB_0465d194;
  }
  if ((uVar5 >> 2 & 1) != 0) {
    if (*(uint *)(param_1 + 0x18) < 0x80) {
      iVar3 = 2;
    }
    else {
      iVar3 = FUN_0571a3d8();
      iVar3 = iVar3 + 1;
      uVar5 = *(uint *)(param_1 + 0x34);
    }
    iVar2 = iVar3 + iVar2;
  }
  if ((uVar5 >> 3 & 1) != 0) {
    if (*(uint *)(param_1 + 0x1c) < 0x80) {
      iVar3 = 2;
    }
    else {
      iVar3 = FUN_0571a3d8();
      iVar3 = iVar3 + 1;
      uVar5 = *(uint *)(param_1 + 0x34);
    }
    iVar2 = iVar3 + iVar2;
  }
  if ((uVar5 >> 4 & 1) != 0) {
    if (*(uint *)(param_1 + 0x28) < 0x80) {
      iVar3 = 2;
    }
    else {
      iVar3 = FUN_0571a3d8();
      iVar3 = iVar3 + 1;
      uVar5 = *(uint *)(param_1 + 0x34);
    }
    iVar2 = iVar3 + iVar2;
  }
  if ((uVar5 >> 5 & 1) != 0) {
    lVar9 = *(long *)(param_1 + 0x20);
    bVar8 = *(byte *)(lVar9 + 0x17);
    uVar6 = (uint)bVar8;
    uVar7 = (uint)*(undefined8 *)(lVar9 + 8);
    uVar1 = uVar7;
    if (-1 < (char)bVar8) {
      uVar1 = uVar6;
    }
    if (uVar1 < 0x80) {
      iVar3 = 1;
    }
    else {
      iVar3 = FUN_0571a3d8();
      bVar8 = *(byte *)(lVar9 + 0x17);
      uVar6 = (uint)bVar8;
      uVar7 = (uint)*(undefined8 *)(lVar9 + 8);
      uVar5 = *(uint *)(param_1 + 0x34);
    }
    if (-1 < (char)bVar8) {
      uVar7 = uVar6;
    }
    iVar2 = iVar2 + iVar3 + uVar7 + 1;
  }
  if ((uVar5 >> 6 & 1) != 0) {
    if (*(uint *)(param_1 + 0x2c) < 0x80) {
      iVar3 = 2;
    }
    else {
      iVar3 = FUN_0571a3d8();
      iVar3 = iVar3 + 1;
    }
    iVar2 = iVar3 + iVar2;
  }
LAB_0465d2f0:
  *(int *)(param_1 + 0x30) = iVar2;
  return iVar2;
}


