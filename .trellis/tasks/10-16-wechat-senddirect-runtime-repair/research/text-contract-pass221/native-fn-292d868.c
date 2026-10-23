// Ghidra inferred pseudocode; requested=0x292d868
// entry=0292d868 end=0292d91b

long FUN_0292d868(long param_1,undefined8 *param_2)

{
  undefined8 *puVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  undefined8 uVar5;
  
  *(undefined8 *)(param_1 + 0x18) = 0;
  puVar1 = (undefined8 *)__Znwm(0x70);
  *puVar1 = &PTR_FUN_09db3978;
  uVar2 = *param_2;
  puVar1[2] = param_2[1];
  puVar1[1] = uVar2;
  *param_2 = 0;
  param_2[1] = 0;
  if (*(char *)((long)param_2 + 0x27) < '\0') {
    FUN_00018d20(puVar1 + 3,param_2[2],param_2[3]);
  }
  else {
    uVar2 = param_2[2];
    puVar1[4] = param_2[3];
    puVar1[3] = uVar2;
    puVar1[5] = param_2[4];
  }
  uVar3 = param_2[6];
  uVar2 = param_2[5];
  uVar5 = param_2[8];
  uVar4 = param_2[7];
  param_2[5] = 0;
  param_2[6] = 0;
  puVar1[7] = uVar3;
  puVar1[6] = uVar2;
  puVar1[9] = uVar5;
  puVar1[8] = uVar4;
  puVar1[10] = param_2[9];
  param_2[7] = 0;
  param_2[8] = 0;
  param_2[9] = 0;
  *(undefined4 *)(puVar1 + 0xb) = *(undefined4 *)(param_2 + 10);
  uVar2 = param_2[0xb];
  puVar1[0xd] = param_2[0xc];
  puVar1[0xc] = uVar2;
  param_2[0xb] = 0;
  param_2[0xc] = 0;
  *(undefined8 **)(param_1 + 0x18) = puVar1;
  return param_1;
}


