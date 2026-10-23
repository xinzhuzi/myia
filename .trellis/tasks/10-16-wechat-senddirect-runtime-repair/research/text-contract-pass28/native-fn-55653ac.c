// Ghidra inferred pseudocode; requested=0x55653ac
// entry=055653ac end=0556555b

void FUN_055653ac(long param_1,undefined8 param_2)

{
  uint uVar1;
  long lVar2;
  
  uVar1 = *(uint *)(param_1 + 0x44);
  if ((uVar1 & 1) != 0) {
    FUN_05ab4e00(1,*(undefined8 *)(param_1 + 8),param_2);
    uVar1 = *(uint *)(param_1 + 0x44);
  }
  if ((uVar1 >> 1 & 1) != 0) {
    FUN_05ab5024(2,*(undefined8 *)(param_1 + 0x10),param_2);
    uVar1 = *(uint *)(param_1 + 0x44);
  }
  if ((uVar1 >> 2 & 1) != 0) {
    FUN_05ab4db4(3,*(undefined4 *)(param_1 + 0x18),param_2);
    uVar1 = *(uint *)(param_1 + 0x44);
  }
  if ((uVar1 >> 3 & 1) != 0) {
    FUN_05ab4e34(4,*(undefined1 *)(param_1 + 0x28),param_2);
    uVar1 = *(uint *)(param_1 + 0x44);
  }
  if ((uVar1 >> 4 & 1) != 0) {
    FUN_05ab4e34(5,*(undefined1 *)(param_1 + 0x29),param_2);
    uVar1 = *(uint *)(param_1 + 0x44);
  }
  if ((uVar1 >> 5 & 1) != 0) {
    FUN_05ab4e34(6,*(undefined4 *)(param_1 + 0x1c),param_2);
    uVar1 = *(uint *)(param_1 + 0x44);
  }
  if ((uVar1 >> 6 & 1) != 0) {
    FUN_05ab5024(7,*(undefined8 *)(param_1 + 0x20),param_2);
    uVar1 = *(uint *)(param_1 + 0x44);
  }
  if ((uVar1 >> 7 & 1) != 0) {
    FUN_05ab4e34(8,*(undefined1 *)(param_1 + 0x2a),param_2);
    uVar1 = *(uint *)(param_1 + 0x44);
  }
  if ((uVar1 >> 8 & 1) != 0) {
    FUN_05ab4e34(9,*(undefined1 *)(param_1 + 0x2b),param_2);
    uVar1 = *(uint *)(param_1 + 0x44);
  }
  if ((uVar1 >> 9 & 1) != 0) {
    lVar2 = *(long *)(param_1 + 0x30);
    if (lVar2 == 0) {
      lVar2 = *(long *)(DAT_0a5237c0 + 0x30);
    }
    FUN_05ab50f0(10,lVar2,param_2);
    uVar1 = *(uint *)(param_1 + 0x44);
  }
  if ((uVar1 >> 10 & 1) != 0) {
    lVar2 = *(long *)(param_1 + 0x38);
    if (lVar2 == 0) {
      lVar2 = *(long *)(DAT_0a5237c0 + 0x38);
    }
    FUN_05ab50f0(0xb,lVar2,param_2);
    uVar1 = *(uint *)(param_1 + 0x44);
  }
  if ((uVar1 >> 0xb & 1) != 0) {
    FUN_05ab4e34(0xc,*(undefined1 *)(param_1 + 0x2c),param_2);
    uVar1 = *(uint *)(param_1 + 0x44);
  }
  if ((uVar1 >> 0xc & 1) != 0) {
    FUN_05ab4e34(0xd,*(undefined1 *)(param_1 + 0x2d),param_2);
    return;
  }
  return;
}


