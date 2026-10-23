// Ghidra inferred pseudocode; requested=0x465dacc
// entry=0465dacc end=0465db7b

int FUN_0465dacc(long param_1)

{
  int iVar1;
  int iVar2;
  undefined8 uVar3;
  long lVar4;
  
  if ((*(byte *)(param_1 + 0x28) & 1) == 0) {
    iVar1 = 0;
  }
  else if (*(uint *)(param_1 + 0x20) < 0x80) {
    iVar1 = 2;
  }
  else {
    iVar1 = FUN_0571a3d8();
    iVar1 = iVar1 + 1;
  }
  iVar1 = *(int *)(param_1 + 0x10) + iVar1;
  if (0 < *(int *)(param_1 + 0x10)) {
    lVar4 = 0;
    do {
      uVar3 = FUN_0465d11c(*(undefined8 *)(*(long *)(param_1 + 8) + lVar4 * 8));
      if ((uint)uVar3 < 0x80) {
        iVar2 = 1;
      }
      else {
        iVar2 = FUN_0571a3d8(uVar3);
      }
      iVar1 = (uint)uVar3 + iVar1 + iVar2;
      lVar4 = lVar4 + 1;
    } while (lVar4 < *(int *)(param_1 + 0x10));
  }
  *(int *)(param_1 + 0x24) = iVar1;
  return iVar1;
}


