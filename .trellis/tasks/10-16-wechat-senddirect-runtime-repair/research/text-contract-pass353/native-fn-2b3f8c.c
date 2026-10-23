// Ghidra inferred pseudocode; requested=0x2b3f8c
// entry=002b3f8c end=002b4033

undefined8 * FUN_002b3f8c(undefined8 *param_1,undefined8 *param_2)

{
  char cVar1;
  undefined8 uVar2;
  undefined8 uVar3;
  
  if (*(char *)((long)param_2 + 0x17) < '\0') {
    FUN_00018d20(param_1,*param_2,param_2[1]);
    cVar1 = *(char *)((long)param_2 + 0x2f);
  }
  else {
    uVar3 = param_2[1];
    uVar2 = *param_2;
    param_1[2] = param_2[2];
    param_1[1] = uVar3;
    *param_1 = uVar2;
    cVar1 = *(char *)((long)param_2 + 0x2f);
  }
  if (cVar1 < '\0') {
    FUN_00018d20(param_1 + 3,param_2[3],param_2[4]);
  }
  else {
    uVar3 = param_2[4];
    uVar2 = param_2[3];
    param_1[5] = param_2[5];
    param_1[4] = uVar3;
    param_1[3] = uVar2;
  }
  if (*(char *)((long)param_2 + 0x47) < '\0') {
    FUN_00018d20(param_1 + 6,param_2[6],param_2[7]);
  }
  else {
    uVar3 = param_2[7];
    uVar2 = param_2[6];
    param_1[8] = param_2[8];
    param_1[7] = uVar3;
    param_1[6] = uVar2;
  }
  param_1[9] = param_2[9];
  return param_1;
}


