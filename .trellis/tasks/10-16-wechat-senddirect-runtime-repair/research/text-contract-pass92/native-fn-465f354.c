// Ghidra inferred pseudocode; requested=0x465f354
// entry=0465f354 end=0465f45b

int FUN_0465f354(long param_1)

{
  byte bVar1;
  int iVar2;
  int iVar3;
  undefined8 uVar4;
  long lVar5;
  
  bVar1 = *(byte *)(param_1 + 0x30);
  if (bVar1 == 0) {
    iVar2 = 0;
  }
  else {
    if ((bVar1 & 1) == 0) {
      iVar2 = 0;
      if ((bVar1 >> 1 & 1) == 0) goto LAB_0465f3ec;
    }
    else {
      lVar5 = *(long *)(param_1 + 8);
      if (lVar5 == 0) {
        lVar5 = *(long *)(DAT_0a51ea50 + 8);
      }
      uVar4 = FUN_0465b6d8(lVar5);
      if ((uint)uVar4 < 0x80) {
        iVar2 = 1;
      }
      else {
        iVar2 = FUN_0571a3d8(uVar4);
      }
      iVar2 = (uint)uVar4 + iVar2 + 1;
      if ((*(uint *)(param_1 + 0x30) >> 1 & 1) == 0) goto LAB_0465f3ec;
    }
    if (*(uint *)(param_1 + 0x28) < 0x80) {
      iVar3 = 2;
    }
    else {
      iVar3 = FUN_0571a3d8();
      iVar3 = iVar3 + 1;
    }
    iVar2 = iVar3 + iVar2;
  }
LAB_0465f3ec:
  iVar2 = *(int *)(param_1 + 0x18) + iVar2;
  if (0 < *(int *)(param_1 + 0x18)) {
    lVar5 = 0;
    do {
      uVar4 = FUN_0465e774(*(undefined8 *)(*(long *)(param_1 + 0x10) + lVar5 * 8));
      if ((uint)uVar4 < 0x80) {
        iVar3 = 1;
      }
      else {
        iVar3 = FUN_0571a3d8(uVar4);
      }
      iVar2 = (uint)uVar4 + iVar2 + iVar3;
      lVar5 = lVar5 + 1;
    } while (lVar5 < *(int *)(param_1 + 0x18));
  }
  *(int *)(param_1 + 0x2c) = iVar2;
  return iVar2;
}


