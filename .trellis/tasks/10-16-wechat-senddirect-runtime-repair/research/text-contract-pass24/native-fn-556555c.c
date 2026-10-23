// Ghidra inferred pseudocode; requested=0x556555c
// entry=0556555c end=055657ab

void FUN_0556555c(long param_1)

{
  uint uVar1;
  int iVar2;
  int iVar3;
  undefined8 uVar4;
  ulong uVar5;
  uint uVar6;
  uint uVar7;
  byte bVar8;
  long lVar9;
  
  uVar1 = *(uint *)(param_1 + 0x44);
  uVar5 = (ulong)uVar1;
  if ((uVar1 & 0xff) == 0) {
    iVar2 = 0;
    if ((uVar1 & 0xff00) == 0) goto LAB_05565798;
  }
  else {
    if ((uVar1 & 1) == 0) {
      iVar2 = 0;
    }
    else {
      iVar2 = FUN_05ab36b8(*(undefined8 *)(param_1 + 8));
      iVar2 = iVar2 + 1;
      uVar1 = *(uint *)(param_1 + 0x44);
      uVar5 = (ulong)uVar1;
    }
    if ((uVar1 >> 1 & 1) != 0) {
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
        uVar5 = (ulong)*(uint *)(param_1 + 0x44);
      }
      if (-1 < (char)bVar8) {
        uVar7 = uVar6;
      }
      iVar2 = iVar2 + iVar3 + uVar7 + 1;
    }
    if (((uint)uVar5 >> 2 & 1) != 0) {
      if ((int)*(uint *)(param_1 + 0x18) < 0) {
        iVar3 = 0xb;
      }
      else if (*(uint *)(param_1 + 0x18) < 0x80) {
        iVar3 = 2;
      }
      else {
        iVar3 = FUN_0571a3d8();
        iVar3 = iVar3 + 1;
        uVar5 = (ulong)*(uint *)(param_1 + 0x44);
      }
      iVar2 = iVar3 + iVar2;
    }
    iVar2 = ((uint)(uVar5 >> 2) & 2) + iVar2 + ((uint)(uVar5 >> 3) & 2);
    if (((uint)uVar5 >> 5 & 1) != 0) {
      if (*(uint *)(param_1 + 0x1c) < 0x80) {
        iVar3 = 2;
      }
      else {
        iVar3 = FUN_0571a3d8();
        iVar3 = iVar3 + 1;
        uVar5 = (ulong)*(uint *)(param_1 + 0x44);
      }
      iVar2 = iVar3 + iVar2;
    }
    if (((uint)uVar5 >> 6 & 1) != 0) {
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
        uVar5 = (ulong)*(uint *)(param_1 + 0x44);
      }
      if (-1 < (char)bVar8) {
        uVar7 = uVar6;
      }
      iVar2 = iVar2 + iVar3 + uVar7 + 1;
    }
    iVar2 = ((uint)(uVar5 >> 6) & 2) + iVar2;
    if ((uVar5 & 0xff00) == 0) goto LAB_05565798;
  }
  iVar2 = ((uint)(uVar5 >> 7) & 2) + iVar2;
  if (((uint)uVar5 >> 9 & 1) != 0) {
    lVar9 = *(long *)(param_1 + 0x30);
    if (lVar9 == 0) {
      lVar9 = *(long *)(DAT_0a5237c0 + 0x30);
    }
    uVar4 = FUN_05563918(lVar9);
    if ((uint)uVar4 < 0x80) {
      iVar3 = 1;
    }
    else {
      iVar3 = FUN_0571a3d8(uVar4);
    }
    iVar2 = iVar2 + (uint)uVar4 + iVar3 + 1;
    uVar5 = (ulong)*(uint *)(param_1 + 0x44);
  }
  if (((uint)uVar5 >> 10 & 1) != 0) {
    lVar9 = *(long *)(param_1 + 0x38);
    if (lVar9 == 0) {
      lVar9 = *(long *)(DAT_0a5237c0 + 0x38);
    }
    uVar4 = FUN_055641cc(lVar9);
    if ((uint)uVar4 < 0x80) {
      iVar3 = 1;
    }
    else {
      iVar3 = FUN_0571a3d8(uVar4);
    }
    iVar2 = iVar2 + (uint)uVar4 + iVar3 + 1;
    uVar5 = (ulong)*(uint *)(param_1 + 0x44);
  }
  iVar2 = ((uint)(uVar5 >> 10) & 2) + ((uint)(uVar5 >> 0xb) & 2) + iVar2;
LAB_05565798:
  *(int *)(param_1 + 0x40) = iVar2;
  return;
}


