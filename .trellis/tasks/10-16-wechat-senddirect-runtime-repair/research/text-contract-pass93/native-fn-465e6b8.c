// Ghidra inferred pseudocode; requested=0x465e6b8
// entry=0465e660 end=0465e773

void FUN_0465e660(long param_1,undefined8 param_2)

{
  uint uVar1;
  long lVar2;
  
  uVar1 = *(uint *)(param_1 + 0x34);
  if ((uVar1 & 1) != 0) {
    FUN_05ab4db4(1,*(undefined4 *)(param_1 + 0x10),param_2);
    uVar1 = *(uint *)(param_1 + 0x34);
  }
  if ((uVar1 >> 1 & 1) != 0) {
    lVar2 = *(long *)(param_1 + 8);
    if (lVar2 == 0) {
      lVar2 = *(long *)(DAT_0a51ea48 + 8);
    }
    FUN_05ab50f0(2,lVar2,param_2);
    uVar1 = *(uint *)(param_1 + 0x34);
  }
  if ((uVar1 >> 2 & 1) != 0) {
    FUN_05ab4e34(3,*(undefined4 *)(param_1 + 0x14),param_2);
    uVar1 = *(uint *)(param_1 + 0x34);
  }
  if ((uVar1 >> 3 & 1) != 0) {
    FUN_05ab4e34(4,*(undefined4 *)(param_1 + 0x18),param_2);
    uVar1 = *(uint *)(param_1 + 0x34);
  }
  if ((uVar1 >> 4 & 1) != 0) {
    FUN_05ab4e34(5,*(undefined4 *)(param_1 + 0x1c),param_2);
    uVar1 = *(uint *)(param_1 + 0x34);
  }
  if ((uVar1 >> 5 & 1) != 0) {
    FUN_05ab4e34(6,*(undefined4 *)(param_1 + 0x20),param_2);
    uVar1 = *(uint *)(param_1 + 0x34);
  }
  if ((uVar1 >> 6 & 1) != 0) {
    FUN_05ab4e34(7,*(undefined4 *)(param_1 + 0x24),param_2);
    uVar1 = *(uint *)(param_1 + 0x34);
  }
  if ((uVar1 >> 7 & 1) == 0) {
    return;
  }
  FUN_05ab4e00(8,*(undefined8 *)(param_1 + 0x28),param_2);
  return;
}


