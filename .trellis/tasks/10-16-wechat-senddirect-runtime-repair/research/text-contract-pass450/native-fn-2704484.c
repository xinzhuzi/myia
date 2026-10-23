// Ghidra inferred pseudocode; requested=0x2704484
// entry=02704484 end=02704533

undefined8 * FUN_02704484(undefined8 *param_1,long param_2)

{
  long lVar1;
  long *plVar2;
  undefined8 uVar3;
  
  uVar3 = *(undefined8 *)(param_2 + 8);
  lVar1 = *(long *)(param_2 + 0x10);
  *param_1 = &PTR____cxa_pure_virtual_09da6188;
  param_1[1] = uVar3;
  param_1[2] = lVar1;
  if (lVar1 != 0) {
    *(long *)(lVar1 + 8) = *(long *)(lVar1 + 8) + 1;
  }
  *param_1 = &PTR_FUN_09da6148;
  param_1[3] = *(undefined8 *)(param_2 + 0x18);
  plVar2 = *(long **)(param_2 + 0x38);
  uVar3 = 0;
  if (plVar2 != (long *)0x0) {
    if (plVar2 == (long *)(param_2 + 0x20)) {
      param_1[7] = param_1 + 4;
      (**(code **)(**(long **)(param_2 + 0x38) + 0x18))(*(long **)(param_2 + 0x38),param_1 + 4);
      goto LAB_02704518;
    }
    uVar3 = (**(code **)(*plVar2 + 0x10))();
  }
  param_1[7] = uVar3;
LAB_02704518:
  FUN_0562e24c(param_1);
  return param_1;
}


