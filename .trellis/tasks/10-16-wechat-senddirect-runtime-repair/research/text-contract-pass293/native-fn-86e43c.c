// Ghidra inferred pseudocode; requested=0x86e43c
// entry=0086e43c end=0086e4df

undefined8 * FUN_0086e43c(undefined8 *param_1,undefined8 *param_2)

{
  undefined8 uVar1;
  undefined8 uVar2;
  
  *(undefined1 *)param_1 = 0;
  *(undefined1 *)(param_1 + 8) = 0;
  if (*(char *)(param_2 + 8) == '\x01') {
    if (*(char *)((long)param_2 + 0x17) < '\0') {
      FUN_00018d20(param_1,*param_2,param_2[1]);
    }
    else {
      uVar2 = param_2[1];
      uVar1 = *param_2;
      param_1[2] = param_2[2];
      param_1[1] = uVar2;
      *param_1 = uVar1;
    }
    uVar1 = param_2[3];
    param_1[4] = param_2[4];
    param_1[3] = uVar1;
    if (*(char *)((long)param_2 + 0x3f) < '\0') {
      FUN_00018d20(param_1 + 5,param_2[5],param_2[6]);
    }
    else {
      uVar2 = param_2[6];
      uVar1 = param_2[5];
      param_1[7] = param_2[7];
      param_1[6] = uVar2;
      param_1[5] = uVar1;
    }
    *(undefined1 *)(param_1 + 8) = 1;
  }
  return param_1;
}


