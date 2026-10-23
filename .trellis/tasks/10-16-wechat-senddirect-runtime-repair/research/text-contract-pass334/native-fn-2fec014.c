// Ghidra inferred pseudocode; requested=0x2fec014
// entry=02fec014 end=02fec0e3

undefined4 * FUN_02fec014(undefined4 *param_1,undefined4 *param_2)

{
  undefined8 uVar1;
  undefined8 uVar2;
  
  *param_1 = *param_2;
  if (*(char *)((long)param_2 + 0x1f) < '\0') {
    FUN_00018d20(param_1 + 2,*(undefined8 *)(param_2 + 2),*(undefined8 *)(param_2 + 4));
  }
  else {
    uVar2 = *(undefined8 *)(param_2 + 4);
    uVar1 = *(undefined8 *)(param_2 + 2);
    *(undefined8 *)(param_1 + 6) = *(undefined8 *)(param_2 + 6);
    *(undefined8 *)(param_1 + 4) = uVar2;
    *(undefined8 *)(param_1 + 2) = uVar1;
  }
  *(undefined8 *)(param_1 + 8) = *(undefined8 *)(param_2 + 8);
  if (*(char *)((long)param_2 + 0x3f) < '\0') {
    FUN_00018d20(param_1 + 10,*(undefined8 *)(param_2 + 10),*(undefined8 *)(param_2 + 0xc));
  }
  else {
    uVar2 = *(undefined8 *)(param_2 + 0xc);
    uVar1 = *(undefined8 *)(param_2 + 10);
    *(undefined8 *)(param_1 + 0xe) = *(undefined8 *)(param_2 + 0xe);
    *(undefined8 *)(param_1 + 0xc) = uVar2;
    *(undefined8 *)(param_1 + 10) = uVar1;
  }
  if (*(char *)((long)param_2 + 0x57) < '\0') {
    FUN_00018d20(param_1 + 0x10,*(undefined8 *)(param_2 + 0x10),*(undefined8 *)(param_2 + 0x12));
  }
  else {
    uVar2 = *(undefined8 *)(param_2 + 0x12);
    uVar1 = *(undefined8 *)(param_2 + 0x10);
    *(undefined8 *)(param_1 + 0x14) = *(undefined8 *)(param_2 + 0x14);
    *(undefined8 *)(param_1 + 0x12) = uVar2;
    *(undefined8 *)(param_1 + 0x10) = uVar1;
  }
  if (*(char *)((long)param_2 + 0x6f) < '\0') {
    FUN_00018d20(param_1 + 0x16,*(undefined8 *)(param_2 + 0x16),*(undefined8 *)(param_2 + 0x18));
  }
  else {
    uVar2 = *(undefined8 *)(param_2 + 0x18);
    uVar1 = *(undefined8 *)(param_2 + 0x16);
    *(undefined8 *)(param_1 + 0x1a) = *(undefined8 *)(param_2 + 0x1a);
    *(undefined8 *)(param_1 + 0x18) = uVar2;
    *(undefined8 *)(param_1 + 0x16) = uVar1;
  }
  return param_1;
}


