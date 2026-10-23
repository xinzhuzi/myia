// Ghidra inferred pseudocode; requested=0x5632bb4
// entry=05632bb4 end=05632caf

undefined8 * FUN_05632bb4(undefined8 *param_1,long param_2)

{
  long lVar1;
  long *plVar2;
  undefined8 uVar3;
  code *pcVar4;
  undefined8 local_38;
  
  uVar3 = *(undefined8 *)(param_2 + 8);
  lVar1 = *(long *)(param_2 + 0x10);
  *param_1 = &PTR____cxa_pure_virtual_09da6188;
  param_1[1] = uVar3;
  param_1[2] = lVar1;
  if (lVar1 != 0) {
    *(long *)(lVar1 + 8) = *(long *)(lVar1 + 8) + 1;
  }
  *param_1 = &PTR_FUN_09da5788;
  uVar3 = *(undefined8 *)(param_2 + 0x18);
  param_1[4] = *(undefined8 *)(param_2 + 0x20);
  param_1[3] = uVar3;
  plVar2 = *(long **)(param_2 + 0x40);
  uVar3 = 0;
  if (plVar2 != (long *)0x0) {
    if (plVar2 == (long *)(param_2 + 0x28)) {
      param_1[8] = param_1 + 5;
      (**(code **)(**(long **)(param_2 + 0x40) + 0x18))(*(long **)(param_2 + 0x40),param_1 + 5);
      goto LAB_05632c50;
    }
    uVar3 = (**(code **)(*plVar2 + 0x10))();
  }
  param_1[8] = uVar3;
LAB_05632c50:
  FUN_0562e24c(param_1);
  local_38 = 0;
  FUN_0562e288(param_2,&local_38);
  *(undefined8 *)(param_2 + 0x18) = 0;
  *(undefined8 *)(param_2 + 0x20) = 0;
  plVar2 = *(long **)(param_2 + 0x40);
  *(undefined8 *)(param_2 + 0x40) = 0;
  if (plVar2 == (long *)(param_2 + 0x28)) {
    pcVar4 = *(code **)(*plVar2 + 0x20);
  }
  else {
    if (plVar2 == (long *)0x0) {
      return param_1;
    }
    pcVar4 = *(code **)(*plVar2 + 0x28);
  }
  (*pcVar4)();
  return param_1;
}


