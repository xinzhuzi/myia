// Ghidra inferred pseudocode; requested=0x5627708
// entry=05627708 end=0562774f

void FUN_05627708(long param_1)

{
  undefined8 uVar1;
  long lVar2;
  undefined8 *puVar3;
  
  puVar3 = (undefined8 *)__Znwm(0x18);
  uVar1 = *(undefined8 *)(param_1 + 8);
  lVar2 = *(long *)(param_1 + 0x10);
  *puVar3 = &PTR_FUN_09f17180;
  puVar3[1] = uVar1;
  puVar3[2] = lVar2;
  if (lVar2 != 0) {
    *(long *)(lVar2 + 8) = *(long *)(lVar2 + 8) + 1;
  }
  return;
}


