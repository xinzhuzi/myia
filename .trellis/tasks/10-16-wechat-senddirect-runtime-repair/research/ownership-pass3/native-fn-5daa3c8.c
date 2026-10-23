// Ghidra inferred pseudocode; requested=0x5daa3c8
// entry=05daa3c8 end=05daa6fb

undefined8 * FUN_05daa3c8(undefined8 *param_1,undefined8 *param_2)

{
  undefined8 uVar1;
  undefined8 uVar2;
  
  *param_1 = *param_2;
  param_1[1] = param_2[1];
  param_1[2] = param_2[2];
  if (*(char *)((long)param_2 + 0x2f) < '\0') {
    FUN_00018d20(param_1 + 3,param_2[3],param_2[4]);
  }
  else {
    uVar2 = param_2[4];
    uVar1 = param_2[3];
    param_1[5] = param_2[5];
    param_1[4] = uVar2;
    param_1[3] = uVar1;
  }
  *(undefined4 *)(param_1 + 6) = *(undefined4 *)(param_2 + 6);
  *(undefined1 *)((long)param_1 + 0x34) = *(undefined1 *)((long)param_2 + 0x34);
  uVar1 = param_2[7];
  param_1[8] = param_2[8];
  param_1[7] = uVar1;
  *(undefined4 *)(param_1 + 9) = *(undefined4 *)(param_2 + 9);
  *(undefined1 *)((long)param_1 + 0x4c) = *(undefined1 *)((long)param_2 + 0x4c);
  *(undefined4 *)(param_1 + 10) = *(undefined4 *)(param_2 + 10);
  uVar1 = param_2[0xc];
  param_1[0xb] = param_2[0xb];
  param_1[0xc] = uVar1;
  if (*(char *)((long)param_2 + 0x7f) < '\0') {
    FUN_00018d20(param_1 + 0xd,param_2[0xd],param_2[0xe]);
  }
  else {
    uVar2 = param_2[0xe];
    uVar1 = param_2[0xd];
    param_1[0xf] = param_2[0xf];
    param_1[0xe] = uVar2;
    param_1[0xd] = uVar1;
  }
  if (*(char *)((long)param_2 + 0x97) < '\0') {
    FUN_00018d20(param_1 + 0x10,param_2[0x10],param_2[0x11]);
  }
  else {
    uVar2 = param_2[0x11];
    uVar1 = param_2[0x10];
    param_1[0x12] = param_2[0x12];
    param_1[0x11] = uVar2;
    param_1[0x10] = uVar1;
  }
  if (*(char *)((long)param_2 + 0xaf) < '\0') {
    FUN_00018d20(param_1 + 0x13,param_2[0x13],param_2[0x14]);
  }
  else {
    uVar2 = param_2[0x14];
    uVar1 = param_2[0x13];
    param_1[0x15] = param_2[0x15];
    param_1[0x14] = uVar2;
    param_1[0x13] = uVar1;
  }
  *(undefined4 *)(param_1 + 0x16) = *(undefined4 *)(param_2 + 0x16);
  param_1[0x19] = 0;
  param_1[0x18] = 0;
  param_1[0x17] = param_1 + 0x18;
  FUN_059de6ac(param_1 + 0x17,param_2[0x17],param_2 + 0x18);
  param_1[0x1b] = 0;
  param_1[0x1c] = 0;
  param_1[0x1a] = 0;
  FUN_0596bc10();
  param_1[0x1d] = 0;
  param_1[0x1e] = 0;
  param_1[0x1f] = 0;
  FUN_0596bc10(param_1 + 0x1d,param_2[0x1d],param_2[0x1e],
               ((long)(param_2[0x1e] - param_2[0x1d]) >> 3) * -0x5555555555555555);
  param_1[0x20] = 0;
  param_1[0x21] = 0;
  param_1[0x22] = 0;
  FUN_0596bc10(param_1 + 0x20,param_2[0x20],param_2[0x21],
               ((long)(param_2[0x21] - param_2[0x20]) >> 3) * -0x5555555555555555);
  param_1[0x23] = 0;
  param_1[0x24] = 0;
  param_1[0x25] = 0;
  FUN_0596bc10(param_1 + 0x23,param_2[0x23],param_2[0x24],
               ((long)(param_2[0x24] - param_2[0x23]) >> 3) * -0x5555555555555555);
  param_1[0x26] = 0;
  param_1[0x27] = 0;
  param_1[0x28] = 0;
  FUN_0596bc10(param_1 + 0x26,param_2[0x26],param_2[0x27],
               ((long)(param_2[0x27] - param_2[0x26]) >> 3) * -0x5555555555555555);
  *(undefined4 *)(param_1 + 0x29) = *(undefined4 *)(param_2 + 0x29);
  if (*(char *)((long)param_2 + 0x167) < '\0') {
    FUN_00018d20(param_1 + 0x2a,param_2[0x2a],param_2[0x2b]);
  }
  else {
    uVar2 = param_2[0x2b];
    uVar1 = param_2[0x2a];
    param_1[0x2c] = param_2[0x2c];
    param_1[0x2b] = uVar2;
    param_1[0x2a] = uVar1;
  }
  if (*(char *)((long)param_2 + 0x17f) < '\0') {
    FUN_00018d20(param_1 + 0x2d,param_2[0x2d],param_2[0x2e]);
  }
  else {
    uVar2 = param_2[0x2e];
    uVar1 = param_2[0x2d];
    param_1[0x2f] = param_2[0x2f];
    param_1[0x2e] = uVar2;
    param_1[0x2d] = uVar1;
  }
  *(undefined4 *)(param_1 + 0x30) = *(undefined4 *)(param_2 + 0x30);
  *(undefined4 *)((long)param_1 + 0x184) = *(undefined4 *)((long)param_2 + 0x184);
  *(undefined1 *)(param_1 + 0x31) = *(undefined1 *)(param_2 + 0x31);
  *(undefined4 *)((long)param_1 + 0x18c) = *(undefined4 *)((long)param_2 + 0x18c);
  param_1[0x33] = 0;
  param_1[0x34] = 0;
  param_1[0x32] = param_1 + 0x33;
  FUN_059de6ac(param_1 + 0x32,param_2[0x32],param_2 + 0x33);
  if (*(char *)((long)param_2 + 0x1bf) < '\0') {
    FUN_00018d20(param_1 + 0x35,param_2[0x35],param_2[0x36]);
  }
  else {
    uVar2 = param_2[0x36];
    uVar1 = param_2[0x35];
    param_1[0x37] = param_2[0x37];
    param_1[0x36] = uVar2;
    param_1[0x35] = uVar1;
  }
  *(undefined1 *)(param_1 + 0x38) = *(undefined1 *)(param_2 + 0x38);
  FUN_05ded178(param_1 + 0x39,0x80);
  FUN_05ded178(param_1 + 0x3e,0x80);
  FUN_05ded348(param_1 + 0x39);
  FUN_05ded348(param_1 + 0x3e);
  uVar1 = FUN_056300b4(param_2 + 0x39,0);
  uVar2 = FUN_009ce4a8(param_2 + 0x39);
  FUN_05ded508(param_1 + 0x39,uVar1,uVar2);
  uVar1 = FUN_056300b4(param_2 + 0x3e,0);
  uVar2 = FUN_009ce4a8(param_2 + 0x3e);
  FUN_05ded508(param_1 + 0x3e,uVar1,uVar2);
  return param_1;
}


