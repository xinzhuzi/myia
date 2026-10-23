// Ghidra inferred pseudocode; requested=0x5ce61ec
// entry=05ce61ec end=05ce6277

undefined8 FUN_05ce61ec(long param_1)

{
  long *plVar1;
  undefined8 uVar2;
  uint uVar3;
  
  uVar3 = *(uint *)(param_1 + 0x44);
  if (((uVar3 ^ 0xffffffff) & 0xf) != 0) {
    return 0;
  }
  if ((uVar3 >> 9 & 1) != 0) {
    plVar1 = *(long **)(param_1 + 0x30);
    if (plVar1 == (long *)0x0) {
      plVar1 = *(long **)(DAT_0a5250d8 + 0x30);
    }
    uVar2 = (**(code **)(*plVar1 + 0x28))();
    if ((int)uVar2 == 0) {
      return uVar2;
    }
    uVar3 = *(uint *)(param_1 + 0x44);
  }
  if ((uVar3 >> 10 & 1) != 0) {
    plVar1 = *(long **)(param_1 + 0x38);
    if (plVar1 == (long *)0x0) {
      plVar1 = *(long **)(DAT_0a5250d8 + 0x38);
    }
    uVar2 = (**(code **)(*plVar1 + 0x28))();
    if ((int)uVar2 == 0) {
      return uVar2;
    }
  }
  return 1;
}


