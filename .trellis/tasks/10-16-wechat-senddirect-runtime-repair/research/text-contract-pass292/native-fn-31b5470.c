// Ghidra inferred pseudocode; requested=0x31b5470
// entry=031b5470 end=031b5563

void FUN_031b5470(undefined8 param_1,undefined8 param_2,long *param_3)

{
  undefined8 *puVar1;
  undefined8 uVar2;
  undefined8 *puVar3;
  undefined8 *local_58;
  undefined8 *local_50;
  long local_48;
  
  FUN_03196d64();
  FUN_03191958(param_1,param_2,param_3);
  local_58 = (undefined8 *)0x0;
  local_50 = (undefined8 *)0x0;
  local_48 = 0;
  uVar2 = FUN_03214ae4(&local_58,*param_3,param_3[1],
                       (param_3[1] - *param_3 >> 3) * -0x6474a8819ec8e951);
  FUN_031b5578(uVar2,&local_58);
  puVar1 = local_58;
  puVar3 = local_50;
  if (local_58 != (undefined8 *)0x0) {
    while (puVar3 != puVar1) {
      puVar3 = puVar3 + -0x4f;
      (**(code **)*puVar3)(puVar3);
    }
    local_50 = puVar1;
    __ZdlPvm(local_58,local_48 - (long)local_58);
  }
  uVar2 = FUN_031955b4(param_1,param_2,param_3);
  FUN_03198a18(uVar2,param_2,param_3);
  return;
}


