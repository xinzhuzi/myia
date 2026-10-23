// Ghidra inferred pseudocode; requested=0x2879700
// entry=02879700 end=028798a3

ulong * FUN_02879700(ulong *param_1,ulong *param_2,ulong *param_3,ulong *param_4,ulong *param_5,
                    ulong *param_6,ulong *param_7,ulong *param_8,ulong *param_9,long *param_10)

{
  ulong uVar1;
  ulong uVar2;
  
  uVar1 = *param_2;
  if ((uVar1 & 0xfffffffc00000000) == DAT_09ffaec8) {
    FUN_0003f84c(uVar1);
  }
  *param_1 = uVar1;
  if (*(char *)((long)param_3 + 0x17) < '\0') {
    FUN_00018d20(param_1 + 1,*param_3,param_3[1]);
  }
  else {
    uVar2 = param_3[1];
    uVar1 = *param_3;
    param_1[3] = param_3[2];
    param_1[2] = uVar2;
    param_1[1] = uVar1;
  }
  if (*(char *)((long)param_4 + 0x17) < '\0') {
    FUN_00018d20(param_1 + 4,*param_4,param_4[1]);
  }
  else {
    uVar2 = param_4[1];
    uVar1 = *param_4;
    param_1[6] = param_4[2];
    param_1[5] = uVar2;
    param_1[4] = uVar1;
  }
  if (*(char *)((long)param_5 + 0x17) < '\0') {
    FUN_00018d20(param_1 + 7,*param_5,param_5[1]);
  }
  else {
    uVar2 = param_5[1];
    uVar1 = *param_5;
    param_1[9] = param_5[2];
    param_1[8] = uVar2;
    param_1[7] = uVar1;
  }
  if (*(char *)((long)param_6 + 0x17) < '\0') {
    FUN_00018d20(param_1 + 10,*param_6,param_6[1]);
  }
  else {
    uVar2 = param_6[1];
    uVar1 = *param_6;
    param_1[0xc] = param_6[2];
    param_1[0xb] = uVar2;
    param_1[10] = uVar1;
  }
  param_1[0xd] = *param_7;
  param_1[0xe] = *param_8;
  if (*(char *)((long)param_9 + 0x17) < '\0') {
    FUN_00018d20(param_1 + 0xf,*param_9,param_9[1]);
  }
  else {
    uVar2 = param_9[1];
    uVar1 = *param_9;
    param_1[0x11] = param_9[2];
    param_1[0x10] = uVar2;
    param_1[0xf] = uVar1;
  }
  param_1[0x12] = 0;
  param_1[0x13] = 0;
  param_1[0x14] = 0;
  FUN_001eadb4(param_1 + 0x12,*param_10,param_10[1],
               (param_10[1] - *param_10 >> 3) * -0x5555555555555555);
  param_1[0x15] = 0;
  param_1[0x16] = 0;
  param_1[0x17] = 0;
  FUN_001eadb4();
  return param_1;
}


