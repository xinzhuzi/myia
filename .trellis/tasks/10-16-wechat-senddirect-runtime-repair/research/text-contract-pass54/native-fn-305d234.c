// Ghidra inferred pseudocode; requested=0x305d234
// entry=0305d234 end=0305d2e7

long FUN_0305d234(long param_1,undefined8 *param_2)

{
  undefined8 *puVar1;
  undefined8 uVar2;
  
  *(undefined8 *)(param_1 + 0x18) = 0;
  puVar1 = (undefined8 *)__Znwm(0x58);
  *puVar1 = &PTR_FUN_09de57f0;
  uVar2 = *param_2;
  puVar1[2] = param_2[1];
  puVar1[1] = uVar2;
  if (*(char *)((long)param_2 + 0x27) < '\0') {
    FUN_00018d20(puVar1 + 3,param_2[2],param_2[3]);
  }
  else {
    uVar2 = param_2[2];
    puVar1[4] = param_2[3];
    puVar1[3] = uVar2;
    puVar1[5] = param_2[4];
  }
  puVar1[6] = param_2[5];
  if (*(char *)((long)param_2 + 0x47) < '\0') {
    FUN_00018d20(puVar1 + 7,param_2[6],param_2[7]);
  }
  else {
    uVar2 = param_2[6];
    puVar1[8] = param_2[7];
    puVar1[7] = uVar2;
    puVar1[9] = param_2[8];
  }
  puVar1[10] = param_2[9];
  *(undefined8 **)(param_1 + 0x18) = puVar1;
  return param_1;
}


