// Ghidra inferred pseudocode; requested=0x5632cf8
// entry=05632cf8 end=05632d87

long FUN_05632cf8(long param_1,undefined8 *param_2,long *param_3)

{
  undefined8 *puVar1;
  long *plVar2;
  undefined8 uVar3;
  
  puVar1 = (undefined8 *)FUN_0562e0a8();
  *puVar1 = &PTR_FUN_09da5788;
  uVar3 = *param_2;
  puVar1[4] = param_2[1];
  puVar1[3] = uVar3;
  plVar2 = (long *)param_3[3];
  uVar3 = 0;
  if (plVar2 != (long *)0x0) {
    if (plVar2 == param_3) {
      *(undefined8 **)(param_1 + 0x40) = puVar1 + 5;
      (**(code **)(*(long *)param_3[3] + 0x18))((long *)param_3[3],puVar1 + 5);
      goto LAB_05632d6c;
    }
    uVar3 = (**(code **)(*plVar2 + 0x10))();
  }
  *(undefined8 *)(param_1 + 0x40) = uVar3;
LAB_05632d6c:
  FUN_0562e24c(param_1);
  return param_1;
}


