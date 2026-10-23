// Ghidra inferred pseudocode; requested=0x55bf230
// entry=055bf230 end=055bf45f

/* WARNING: Type propagation algorithm not settling */

int FUN_055bf230(long param_1)

{
  uint uVar1;
  int iVar2;
  int iVar3;
  uint uVar4;
  uint uVar5;
  uint uVar6;
  byte bVar7;
  long lVar8;
  
  bVar7 = *(byte *)(param_1 + 0x38);
  uVar4 = (uint)bVar7;
  if (bVar7 == 0) {
    iVar2 = 0;
    goto LAB_055bf448;
  }
  if ((bVar7 & 1) == 0) {
    iVar2 = 0;
    if ((bVar7 >> 1 & 1) != 0) {
LAB_055bf2b8:
      lVar8 = *(long *)(param_1 + 0x10);
      bVar7 = *(byte *)(lVar8 + 0x17);
      uVar5 = (uint)bVar7;
      uVar6 = (uint)*(undefined8 *)(lVar8 + 8);
      uVar1 = uVar6;
      if (-1 < (char)bVar7) {
        uVar1 = uVar5;
      }
      if (uVar1 < 0x80) {
        iVar3 = 1;
      }
      else {
        iVar3 = FUN_0571a3d8();
        bVar7 = *(byte *)(lVar8 + 0x17);
        uVar5 = (uint)bVar7;
        uVar6 = (uint)*(undefined8 *)(lVar8 + 8);
        uVar4 = *(uint *)(param_1 + 0x38);
      }
      if (-1 < (char)bVar7) {
        uVar6 = uVar5;
      }
      iVar2 = iVar2 + iVar3 + uVar6 + 1;
    }
  }
  else {
    lVar8 = *(long *)(param_1 + 8);
    bVar7 = *(byte *)(lVar8 + 0x17);
    uVar5 = (uint)bVar7;
    uVar6 = (uint)*(undefined8 *)(lVar8 + 8);
    uVar1 = uVar6;
    if (-1 < (char)bVar7) {
      uVar1 = uVar5;
    }
    if (uVar1 < 0x80) {
      iVar2 = 2;
    }
    else {
      iVar2 = FUN_0571a3d8();
      bVar7 = *(byte *)(lVar8 + 0x17);
      uVar5 = (uint)bVar7;
      uVar6 = (uint)*(undefined8 *)(lVar8 + 8);
      iVar2 = iVar2 + 1;
      uVar4 = *(uint *)(param_1 + 0x38);
    }
    if (-1 < (char)bVar7) {
      uVar6 = uVar5;
    }
    iVar2 = iVar2 + uVar6;
    if ((uVar4 >> 1 & 1) != 0) goto LAB_055bf2b8;
  }
  if ((uVar4 >> 2 & 1) != 0) {
    lVar8 = *(long *)(param_1 + 0x18);
    bVar7 = *(byte *)(lVar8 + 0x17);
    uVar5 = (uint)bVar7;
    uVar6 = (uint)*(undefined8 *)(lVar8 + 8);
    uVar1 = uVar6;
    if (-1 < (char)bVar7) {
      uVar1 = uVar5;
    }
    if (uVar1 < 0x80) {
      iVar3 = 1;
    }
    else {
      iVar3 = FUN_0571a3d8();
      bVar7 = *(byte *)(lVar8 + 0x17);
      uVar5 = (uint)bVar7;
      uVar6 = (uint)*(undefined8 *)(lVar8 + 8);
      uVar4 = *(uint *)(param_1 + 0x38);
    }
    if (-1 < (char)bVar7) {
      uVar6 = uVar5;
    }
    iVar2 = iVar2 + iVar3 + uVar6 + 1;
  }
  if ((uVar4 >> 3 & 1) != 0) {
    lVar8 = *(long *)(param_1 + 0x20);
    bVar7 = *(byte *)(lVar8 + 0x17);
    uVar5 = (uint)bVar7;
    uVar6 = (uint)*(undefined8 *)(lVar8 + 8);
    uVar1 = uVar6;
    if (-1 < (char)bVar7) {
      uVar1 = uVar5;
    }
    if (uVar1 < 0x80) {
      iVar3 = 1;
    }
    else {
      iVar3 = FUN_0571a3d8();
      bVar7 = *(byte *)(lVar8 + 0x17);
      uVar5 = (uint)bVar7;
      uVar6 = (uint)*(undefined8 *)(lVar8 + 8);
      uVar4 = *(uint *)(param_1 + 0x38);
    }
    if (-1 < (char)bVar7) {
      uVar6 = uVar5;
    }
    iVar2 = iVar2 + iVar3 + uVar6 + 1;
  }
  if ((uVar4 >> 4 & 1) != 0) {
    lVar8 = *(long *)(param_1 + 0x28);
    bVar7 = *(byte *)(lVar8 + 0x17);
    uVar5 = (uint)bVar7;
    uVar6 = (uint)*(undefined8 *)(lVar8 + 8);
    uVar1 = uVar6;
    if (-1 < (char)bVar7) {
      uVar1 = uVar5;
    }
    if (uVar1 < 0x80) {
      iVar3 = 1;
    }
    else {
      iVar3 = FUN_0571a3d8();
      bVar7 = *(byte *)(lVar8 + 0x17);
      uVar5 = (uint)bVar7;
      uVar6 = (uint)*(undefined8 *)(lVar8 + 8);
      uVar4 = *(uint *)(param_1 + 0x38);
    }
    if (-1 < (char)bVar7) {
      uVar6 = uVar5;
    }
    iVar2 = iVar2 + iVar3 + uVar6 + 1;
  }
  if ((uVar4 >> 5 & 1) != 0) {
    if (*(uint *)(param_1 + 0x30) < 0x80) {
      iVar3 = 2;
    }
    else {
      iVar3 = FUN_0571a3d8();
      iVar3 = iVar3 + 1;
    }
    iVar2 = iVar3 + iVar2;
  }
LAB_055bf448:
  *(int *)(param_1 + 0x34) = iVar2;
  return iVar2;
}


