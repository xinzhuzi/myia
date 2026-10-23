// Ghidra inferred pseudocode; requested=0x465b6d8
// entry=0465b6d8 end=0465b79b

void FUN_0465b6d8(long param_1)

{
  byte bVar1;
  int iVar2;
  int iVar3;
  long lVar4;
  undefined8 uVar5;
  
  bVar1 = *(byte *)(param_1 + 0x18);
  if (bVar1 == 0) {
    iVar2 = 0;
    goto LAB_0465b788;
  }
  if ((bVar1 & 1) == 0) {
    iVar2 = 0;
joined_r0x0465b720:
    if ((bVar1 >> 1 & 1) == 0) goto LAB_0465b788;
  }
  else {
    if ((int)*(uint *)(param_1 + 0x10) < 0) {
      iVar2 = 0xb;
      goto joined_r0x0465b720;
    }
    if (*(uint *)(param_1 + 0x10) < 0x80) {
      iVar2 = 2;
      goto joined_r0x0465b720;
    }
    iVar2 = FUN_0571a3d8();
    iVar2 = iVar2 + 1;
    if ((*(uint *)(param_1 + 0x18) >> 1 & 1) == 0) goto LAB_0465b788;
  }
  lVar4 = *(long *)(param_1 + 8);
  if (lVar4 == 0) {
    lVar4 = *(long *)(DAT_0a51ea28 + 8);
  }
  uVar5 = FUN_04f37cb0(lVar4);
  if ((uint)uVar5 < 0x80) {
    iVar3 = 1;
  }
  else {
    iVar3 = FUN_0571a3d8(uVar5);
  }
  iVar2 = iVar2 + (uint)uVar5 + iVar3 + 1;
LAB_0465b788:
  *(int *)(param_1 + 0x14) = iVar2;
  return;
}


