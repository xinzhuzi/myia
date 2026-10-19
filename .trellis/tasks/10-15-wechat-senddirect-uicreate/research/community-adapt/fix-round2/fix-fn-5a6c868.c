// requested=0x5a6c868
// entry=05a6c868 end=05a6c9bb

int FUN_05a6c868(long param_1)

{
  uint uVar1;
  int iVar2;
  int iVar3;
  uint uVar4;
  uint uVar5;
  uint uVar6;
  byte bVar7;
  long lVar8;
  
  bVar7 = *(byte *)(param_1 + 0x24);
  uVar4 = (uint)bVar7;
  if (bVar7 == 0) {
    iVar2 = 0;
    goto LAB_05a6c9a4;
  }
  if ((bVar7 & 1) == 0) {
    iVar2 = 0;
    if ((bVar7 >> 1 & 1) != 0) {
LAB_05a6c8f0:
      if (*(uint *)(param_1 + 0x18) < 0x80) {
        iVar3 = 2;
      }
      else {
        iVar3 = FUN_0571a3d8();
        iVar3 = iVar3 + 1;
        uVar4 = *(uint *)(param_1 + 0x24);
      }
      iVar2 = iVar3 + iVar2;
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
      uVar4 = *(uint *)(param_1 + 0x24);
    }
    if (-1 < (char)bVar7) {
      uVar6 = uVar5;
    }
    iVar2 = iVar2 + uVar6;
    if ((uVar4 >> 1 & 1) != 0) goto LAB_05a6c8f0;
  }
  if ((uVar4 >> 2 & 1) != 0) {
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
      uVar4 = *(uint *)(param_1 + 0x24);
    }
    if (-1 < (char)bVar7) {
      uVar6 = uVar5;
    }
    iVar2 = iVar2 + iVar3 + uVar6 + 1;
  }
  if ((uVar4 >> 3 & 1) != 0) {
    if ((int)*(uint *)(param_1 + 0x1c) < 0) {
      iVar3 = 0xb;
    }
    else if (*(uint *)(param_1 + 0x1c) < 0x80) {
      iVar3 = 2;
    }
    else {
      iVar3 = FUN_0571a3d8();
      iVar3 = iVar3 + 1;
    }
    iVar2 = iVar3 + iVar2;
  }
LAB_05a6c9a4:
  *(int *)(param_1 + 0x20) = iVar2;
  return iVar2;
}


