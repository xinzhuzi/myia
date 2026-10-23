// Ghidra inferred pseudocode; requested=0x6666628
// entry=06666628 end=066666fb

void FUN_06666628(long param_1)

{
  int iVar1;
  undefined8 *puVar2;
  undefined8 *puVar3;
  pthread_t p_Var4;
  
  puVar2 = (undefined8 *)__Znwm(0x48);
  *puVar2 = &PTR_FUN_09fb1840;
  puVar2[1] = 0;
  puVar3 = (undefined8 *)__Znwm(0x20);
  *puVar3 = &PTR_FUN_09fb1ac8;
  puVar3[3] = puVar3;
  puVar2[2] = puVar3;
  puVar2[3] = puVar3;
  puVar2[4] = FUN_025bf788;
  puVar2[5] = FUN_025bf3d8;
  puVar2[6] = 0;
  puVar2[7] = FUN_025bf7a0;
  FUN_06661db0(param_1,1,puVar2,0xffffffff,0);
  p_Var4 = _pthread_self();
  *(pthread_t *)(param_1 + 0x28) = p_Var4;
  FUN_06662554(param_1);
  iVar1 = (**(code **)(**(long **)(param_1 + 0x10) + 0x10))(*(long **)(param_1 + 0x10),1,0);
  FUN_06662554(0);
  *(undefined8 *)(param_1 + 0x28) = 0;
  if (iVar1 != 0) {
    __ZNSt3__17promiseIvE9set_valueEv(param_1 + 0x38);
    return;
  }
  return;
}


