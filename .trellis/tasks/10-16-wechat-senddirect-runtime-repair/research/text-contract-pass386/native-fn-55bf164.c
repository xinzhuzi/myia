// Ghidra inferred pseudocode; requested=0x55bf164
// entry=055bf164 end=055bf22f

void FUN_055bf164(long param_1,undefined8 param_2)

{
  uint uVar1;
  
  uVar1 = *(uint *)(param_1 + 0x38);
  if ((uVar1 & 1) != 0) {
    FUN_05ab4f58(1,*(undefined8 *)(param_1 + 8),param_2);
    uVar1 = *(uint *)(param_1 + 0x38);
  }
  if ((uVar1 >> 1 & 1) != 0) {
    FUN_05ab4f58(2,*(undefined8 *)(param_1 + 0x10),param_2);
    uVar1 = *(uint *)(param_1 + 0x38);
  }
  if ((uVar1 >> 2 & 1) != 0) {
    FUN_05ab4f58(3,*(undefined8 *)(param_1 + 0x18),param_2);
    uVar1 = *(uint *)(param_1 + 0x38);
  }
  if ((uVar1 >> 3 & 1) != 0) {
    FUN_05ab4f58(4,*(undefined8 *)(param_1 + 0x20),param_2);
    uVar1 = *(uint *)(param_1 + 0x38);
  }
  if ((uVar1 >> 4 & 1) != 0) {
    FUN_05ab5024(5,*(undefined8 *)(param_1 + 0x28),param_2);
    uVar1 = *(uint *)(param_1 + 0x38);
  }
  if ((uVar1 >> 5 & 1) == 0) {
    return;
  }
  FUN_05ab4e34(6,*(undefined4 *)(param_1 + 0x30),param_2);
  return;
}


