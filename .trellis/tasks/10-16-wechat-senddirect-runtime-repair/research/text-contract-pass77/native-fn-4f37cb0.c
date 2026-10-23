// Ghidra inferred pseudocode; requested=0x4f37cb0
// entry=04f37cb0 end=04f37d3b

int FUN_04f37cb0(long param_1)

{
  uint uVar1;
  int iVar2;
  uint uVar3;
  uint uVar4;
  byte bVar5;
  long lVar6;
  
  if ((*(byte *)(param_1 + 0x14) & 1) == 0) {
    iVar2 = 0;
  }
  else {
    lVar6 = *(long *)(param_1 + 8);
    bVar5 = *(byte *)(lVar6 + 0x17);
    uVar3 = (uint)bVar5;
    uVar4 = (uint)*(undefined8 *)(lVar6 + 8);
    uVar1 = uVar4;
    if (-1 < (char)bVar5) {
      uVar1 = uVar3;
    }
    if (uVar1 < 0x80) {
      iVar2 = 2;
    }
    else {
      iVar2 = FUN_0571a3d8(uVar1);
      bVar5 = *(byte *)(lVar6 + 0x17);
      uVar3 = (uint)bVar5;
      uVar4 = (uint)*(undefined8 *)(lVar6 + 8);
      iVar2 = iVar2 + 1;
    }
    if (-1 < (char)bVar5) {
      uVar4 = uVar3;
    }
    iVar2 = iVar2 + uVar4;
  }
  *(int *)(param_1 + 0x10) = iVar2;
  return iVar2;
}


