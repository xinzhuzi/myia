// Ghidra inferred pseudocode; requested=0x30c31bc
// entry=030c31bc end=030c3223

void FUN_030c31bc(long param_1)

{
  undefined8 uVar1;
  undefined8 *puVar2;
  long lVar3;
  
  puVar2 = (undefined8 *)__Znwm(0x30);
  uVar1 = *(undefined8 *)(param_1 + 8);
  lVar3 = *(long *)(param_1 + 0x10);
  *puVar2 = &PTR_FUN_09de82c0;
  puVar2[1] = uVar1;
  puVar2[2] = lVar3;
  if (lVar3 != 0) {
    *(long *)(lVar3 + 8) = *(long *)(lVar3 + 8) + 1;
  }
  uVar1 = *(undefined8 *)(param_1 + 0x20);
  puVar2[3] = *(undefined8 *)(param_1 + 0x18);
  puVar2[4] = uVar1;
  lVar3 = *(long *)(param_1 + 0x28);
  puVar2[5] = lVar3;
  if (lVar3 != 0) {
    *(long *)(lVar3 + 8) = *(long *)(lVar3 + 8) + 1;
  }
  return;
}


