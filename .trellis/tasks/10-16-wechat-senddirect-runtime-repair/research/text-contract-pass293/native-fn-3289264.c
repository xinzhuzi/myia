// Ghidra inferred pseudocode; requested=0x3289264
// entry=03289264 end=032892e7

undefined4 FUN_03289264(long param_1)

{
  int iVar1;
  ulong uVar2;
  undefined4 uVar3;
  
  uVar2 = *(ulong *)(param_1 + 8);
  if (-1 < (char)*(byte *)(param_1 + 0x17)) {
    uVar2 = (ulong)*(byte *)(param_1 + 0x17);
  }
  if (uVar2 == 0) {
    return 0;
  }
  uVar2 = FUN_04bb4dc0();
  if (((((uVar2 & 1) == 0) && (uVar2 = FUN_04bb5cd8(param_1), (uVar2 & 1) == 0)) &&
      (uVar2 = FUN_04bb368c(param_1), (uVar2 & 1) == 0)) &&
     (uVar2 = FUN_04bb6588(param_1), (uVar2 & 1) == 0)) {
    iVar1 = FUN_04bb4a4c(param_1);
    uVar3 = 1;
    if (iVar1 != 0) {
      uVar3 = 2;
    }
  }
  else {
    uVar3 = 2;
  }
  return uVar3;
}


