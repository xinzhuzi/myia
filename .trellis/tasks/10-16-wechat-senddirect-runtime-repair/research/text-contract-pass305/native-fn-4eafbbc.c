// Ghidra inferred pseudocode; requested=0x4eafbbc
// entry=04eafbbc end=04eafe17

void FUN_04eafbbc(long param_1,undefined8 param_2)

{
  uint uVar1;
  long lVar2;
  
  uVar1 = *(uint *)(param_1 + 0x74);
  if ((uVar1 & 1) != 0) {
    FUN_05ab4e34(1,*(undefined4 *)(param_1 + 8),param_2);
    uVar1 = *(uint *)(param_1 + 0x74);
  }
  if ((uVar1 >> 1 & 1) != 0) {
    FUN_05ab4e34(2,*(undefined4 *)(param_1 + 0xc),param_2);
    uVar1 = *(uint *)(param_1 + 0x74);
  }
  if ((uVar1 >> 2 & 1) != 0) {
    lVar2 = *(long *)(param_1 + 0x10);
    if (lVar2 == 0) {
      lVar2 = *(long *)(DAT_0a51f728 + 0x10);
    }
    FUN_05ab50f0(3,lVar2,param_2);
    uVar1 = *(uint *)(param_1 + 0x74);
  }
  if ((uVar1 >> 3 & 1) != 0) {
    lVar2 = *(long *)(param_1 + 0x18);
    if (lVar2 == 0) {
      lVar2 = *(long *)(DAT_0a51f728 + 0x18);
    }
    FUN_05ab50f0(4,lVar2,param_2);
    uVar1 = *(uint *)(param_1 + 0x74);
  }
  if ((uVar1 >> 4 & 1) != 0) {
    lVar2 = *(long *)(param_1 + 0x20);
    if (lVar2 == 0) {
      lVar2 = *(long *)(DAT_0a51f728 + 0x20);
    }
    FUN_05ab50f0(5,lVar2,param_2);
    uVar1 = *(uint *)(param_1 + 0x74);
  }
  if ((uVar1 >> 5 & 1) != 0) {
    lVar2 = *(long *)(param_1 + 0x28);
    if (lVar2 == 0) {
      lVar2 = *(long *)(DAT_0a51f728 + 0x28);
    }
    FUN_05ab50f0(6,lVar2,param_2);
    uVar1 = *(uint *)(param_1 + 0x74);
  }
  if ((uVar1 >> 6 & 1) != 0) {
    lVar2 = *(long *)(param_1 + 0x30);
    if (lVar2 == 0) {
      lVar2 = *(long *)(DAT_0a51f728 + 0x30);
    }
    FUN_05ab50f0(7,lVar2,param_2);
    uVar1 = *(uint *)(param_1 + 0x74);
  }
  if ((uVar1 >> 7 & 1) != 0) {
    lVar2 = *(long *)(param_1 + 0x38);
    if (lVar2 == 0) {
      lVar2 = *(long *)(DAT_0a51f728 + 0x38);
    }
    FUN_05ab50f0(8,lVar2,param_2);
    uVar1 = *(uint *)(param_1 + 0x74);
  }
  if ((uVar1 >> 8 & 1) != 0) {
    lVar2 = *(long *)(param_1 + 0x40);
    if (lVar2 == 0) {
      lVar2 = *(long *)(DAT_0a51f728 + 0x40);
    }
    FUN_05ab50f0(9,lVar2,param_2);
    uVar1 = *(uint *)(param_1 + 0x74);
  }
  if ((uVar1 >> 9 & 1) != 0) {
    lVar2 = *(long *)(param_1 + 0x48);
    if (lVar2 == 0) {
      lVar2 = *(long *)(DAT_0a51f728 + 0x48);
    }
    FUN_05ab50f0(10,lVar2,param_2);
    uVar1 = *(uint *)(param_1 + 0x74);
  }
  if ((uVar1 >> 10 & 1) != 0) {
    FUN_05ab4e00(0xb,*(undefined8 *)(param_1 + 0x50),param_2);
    uVar1 = *(uint *)(param_1 + 0x74);
  }
  if ((uVar1 >> 0xb & 1) != 0) {
    lVar2 = *(long *)(param_1 + 0x58);
    if (lVar2 == 0) {
      lVar2 = *(long *)(DAT_0a51f728 + 0x58);
    }
    FUN_05ab50f0(0xc,lVar2,param_2);
    uVar1 = *(uint *)(param_1 + 0x74);
  }
  if ((uVar1 >> 0xc & 1) != 0) {
    lVar2 = *(long *)(param_1 + 0x60);
    if (lVar2 == 0) {
      lVar2 = *(long *)(DAT_0a51f728 + 0x60);
    }
    FUN_05ab50f0(0xd,lVar2,param_2);
    uVar1 = *(uint *)(param_1 + 0x74);
  }
  if ((uVar1 >> 0xd & 1) == 0) {
    return;
  }
  lVar2 = *(long *)(param_1 + 0x68);
  if (lVar2 == 0) {
    lVar2 = *(long *)(DAT_0a51f728 + 0x68);
  }
  FUN_05ab50f0(0xe,lVar2,param_2);
  return;
}


