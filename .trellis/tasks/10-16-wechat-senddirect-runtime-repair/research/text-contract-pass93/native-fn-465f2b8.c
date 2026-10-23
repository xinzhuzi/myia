// Ghidra inferred pseudocode; requested=0x465f2b8
// entry=0465f2b8 end=0465f353

void FUN_0465f2b8(long param_1,undefined8 param_2)

{
  long lVar1;
  uint uVar2;
  
  uVar2 = *(uint *)(param_1 + 0x30);
  if ((uVar2 & 1) != 0) {
    lVar1 = *(long *)(param_1 + 8);
    if (lVar1 == 0) {
      lVar1 = *(long *)(DAT_0a51ea50 + 8);
    }
    FUN_05ab50f0(1,lVar1,param_2);
    uVar2 = *(uint *)(param_1 + 0x30);
  }
  if ((uVar2 >> 1 & 1) != 0) {
    FUN_05ab4e34(2,*(undefined4 *)(param_1 + 0x28),param_2);
  }
  if (0 < *(int *)(param_1 + 0x18)) {
    lVar1 = 0;
    do {
      FUN_05ab50f0(3,*(undefined8 *)(*(long *)(param_1 + 0x10) + lVar1 * 8),param_2);
      lVar1 = lVar1 + 1;
    } while (lVar1 < *(int *)(param_1 + 0x18));
  }
  return;
}


