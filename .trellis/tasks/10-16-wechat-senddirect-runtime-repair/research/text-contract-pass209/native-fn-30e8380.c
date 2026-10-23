// Ghidra inferred pseudocode; requested=0x30e8380
// entry=030e8380 end=030e8433

void FUN_030e8380(undefined8 *param_1,long param_2,undefined8 param_3,undefined8 *param_4,
                 undefined8 *param_5)

{
  undefined8 *puVar1;
  undefined8 uVar2;
  
  param_1[2] = &SUB_aaaaaaaaaaaaaaaa;
  puVar1 = (undefined8 *)__Znwm(0x40);
  *param_1 = puVar1;
  param_1[1] = param_2 + 0x10;
  *(undefined1 *)(param_1 + 2) = 0;
  *puVar1 = 0;
  puVar1[1] = param_3;
  if (*(char *)((long)param_4 + 0x17) < '\0') {
    FUN_00018d20(puVar1 + 2,*param_4,param_4[1]);
  }
  else {
    uVar2 = *param_4;
    puVar1[3] = param_4[1];
    puVar1[2] = uVar2;
    puVar1[4] = param_4[2];
  }
  if (*(char *)((long)param_5 + 0x17) < '\0') {
    FUN_00018d20(puVar1 + 5,*param_5,param_5[1]);
  }
  else {
    uVar2 = *param_5;
    puVar1[6] = param_5[1];
    puVar1[5] = uVar2;
    puVar1[7] = param_5[2];
  }
  *(undefined1 *)(param_1 + 2) = 1;
  return;
}


