// Ghidra inferred pseudocode; requested=0x270583c
// entry=0270583c end=027058cf

undefined8 * FUN_0270583c(undefined8 *param_1,long param_2)

{
  undefined8 *puVar1;
  long *plVar2;
  long lVar3;
  long lVar4;
  
  puVar1 = param_1 + 1;
  param_1[2] = puVar1;
  param_1[3] = 0;
  *param_1 = &PTR_FUN_09da6448;
  param_1[1] = puVar1;
  for (lVar4 = *(long *)(param_2 + 0x10); lVar4 != param_2 + 8; lVar4 = *(long *)(lVar4 + 8)) {
    plVar2 = (long *)__Znwm(0x100);
    *plVar2 = 0;
    plVar2[1] = 0;
    FUN_02705b00(plVar2 + 2,lVar4 + 0x10);
    lVar3 = param_1[1];
    *plVar2 = lVar3;
    plVar2[1] = (long)puVar1;
    *(long **)(lVar3 + 8) = plVar2;
    param_1[1] = plVar2;
    param_1[3] = param_1[3] + 1;
  }
  return param_1;
}


