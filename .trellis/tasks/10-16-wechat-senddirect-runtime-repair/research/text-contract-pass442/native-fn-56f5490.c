// Ghidra inferred pseudocode; requested=0x56f5490
// entry=056f5490 end=056f54e7

undefined8 * FUN_056f5490(undefined8 *param_1,long param_2)

{
  long lVar1;
  long lVar2;
  
  *param_1 = &PTR____cxa_pure_virtual_09f23978;
  lVar1 = *(long *)(param_2 + 0x10);
  param_1[1] = *(undefined8 *)(param_2 + 8);
  param_1[2] = lVar1;
  lVar2 = 0;
  if (lVar1 != 0) {
    lVar2 = *(long *)(lVar1 + 8);
    *(long *)(lVar1 + 8) = lVar2 + 1;
  }
  FUN_05632dcc(lVar2,param_1 + 4);
  return param_1;
}


