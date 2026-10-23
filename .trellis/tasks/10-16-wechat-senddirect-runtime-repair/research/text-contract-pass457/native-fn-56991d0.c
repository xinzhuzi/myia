// Ghidra inferred pseudocode; requested=0x56991d0
// entry=056991d0 end=05699263

undefined8 * FUN_056991d0(undefined8 *param_1,long param_2)

{
  long lVar1;
  long lVar2;
  
  lVar1 = FUN_0569fbe8();
  FUN_0562a6b0(lVar1 + 0x180,param_2 + 0x180);
  param_1[0x30] = &PTR_FUN_09f1cce0;
  *(undefined1 *)(param_1 + 0x33) = *(undefined1 *)(param_2 + 0x198);
  param_1[0x34] = *(undefined8 *)(param_2 + 0x1a0);
  lVar1 = *(long *)(param_2 + 0x1a8);
  param_1[0x35] = lVar1;
  lVar2 = *(long *)(param_2 + 0x1b0);
  param_1[0x36] = lVar2;
  if (lVar2 == 0) {
    param_1[0x34] = param_1 + 0x35;
  }
  else {
    *(undefined8 **)(lVar1 + 0x10) = param_1 + 0x35;
    *(undefined8 **)(param_2 + 0x1a0) = (undefined8 *)(param_2 + 0x1a8);
    *(undefined8 *)(param_2 + 0x1a8) = 0;
    *(undefined8 *)(param_2 + 0x1b0) = 0;
  }
  *param_1 = &PTR_FUN_09f1cbc0;
  param_1[0x30] = &PTR_FUN_09f1cc48;
  return param_1;
}


