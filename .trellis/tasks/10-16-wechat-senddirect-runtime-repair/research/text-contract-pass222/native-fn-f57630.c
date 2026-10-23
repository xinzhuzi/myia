// Ghidra inferred pseudocode; requested=0xf57630
// entry=00f57630 end=00f57967

undefined8 * FUN_00f57630(undefined8 *param_1,long param_2)

{
  void *pvVar1;
  char cVar2;
  size_t sVar3;
  void *pvVar4;
  undefined8 uVar5;
  long lVar6;
  undefined8 uVar7;
  undefined8 uVar8;
  undefined8 uVar9;
  undefined8 uVar10;
  undefined8 uVar11;
  undefined8 uVar12;
  
  *param_1 = &PTR_thunk_FUN_00ac6290_09eb04f0;
  uVar5 = *(undefined8 *)(param_2 + 8);
  *(undefined4 *)(param_1 + 2) = *(undefined4 *)(param_2 + 0x10);
  param_1[1] = uVar5;
  if (*(char *)(param_2 + 0x2f) < '\0') {
    FUN_00018d20(param_1 + 3,*(undefined8 *)(param_2 + 0x18),*(undefined8 *)(param_2 + 0x20));
    cVar2 = *(char *)(param_2 + 0x47);
  }
  else {
    uVar7 = *(undefined8 *)(param_2 + 0x20);
    uVar5 = *(undefined8 *)(param_2 + 0x18);
    param_1[5] = *(undefined8 *)(param_2 + 0x28);
    param_1[4] = uVar7;
    param_1[3] = uVar5;
    cVar2 = *(char *)(param_2 + 0x47);
  }
  if (cVar2 < '\0') {
    FUN_00018d20(param_1 + 6,*(undefined8 *)(param_2 + 0x30),*(undefined8 *)(param_2 + 0x38));
  }
  else {
    uVar7 = *(undefined8 *)(param_2 + 0x38);
    uVar5 = *(undefined8 *)(param_2 + 0x30);
    param_1[8] = *(undefined8 *)(param_2 + 0x40);
    param_1[7] = uVar7;
    param_1[6] = uVar5;
  }
  if (*(char *)(param_2 + 0x5f) < '\0') {
    FUN_00018d20(param_1 + 9,*(undefined8 *)(param_2 + 0x48),*(undefined8 *)(param_2 + 0x50));
  }
  else {
    uVar7 = *(undefined8 *)(param_2 + 0x50);
    uVar5 = *(undefined8 *)(param_2 + 0x48);
    param_1[0xb] = *(undefined8 *)(param_2 + 0x58);
    param_1[10] = uVar7;
    param_1[9] = uVar5;
  }
  if (*(char *)(param_2 + 0x77) < '\0') {
    FUN_00018d20(param_1 + 0xc,*(undefined8 *)(param_2 + 0x60),*(undefined8 *)(param_2 + 0x68));
  }
  else {
    uVar7 = *(undefined8 *)(param_2 + 0x68);
    uVar5 = *(undefined8 *)(param_2 + 0x60);
    param_1[0xe] = *(undefined8 *)(param_2 + 0x70);
    param_1[0xd] = uVar7;
    param_1[0xc] = uVar5;
  }
  if (*(char *)(param_2 + 0x8f) < '\0') {
    FUN_00018d20(param_1 + 0xf,*(undefined8 *)(param_2 + 0x78),*(undefined8 *)(param_2 + 0x80));
  }
  else {
    uVar7 = *(undefined8 *)(param_2 + 0x80);
    uVar5 = *(undefined8 *)(param_2 + 0x78);
    param_1[0x11] = *(undefined8 *)(param_2 + 0x88);
    param_1[0x10] = uVar7;
    param_1[0xf] = uVar5;
  }
  *(undefined2 *)(param_1 + 0x12) = *(undefined2 *)(param_2 + 0x90);
  FUN_00396384(param_1 + 0x13,param_2 + 0x98);
  if (*(char *)(param_2 + 0xd7) < '\0') {
    FUN_00018d20(param_1 + 0x18,*(undefined8 *)(param_2 + 0xc0),*(undefined8 *)(param_2 + 200));
  }
  else {
    uVar7 = *(undefined8 *)(param_2 + 200);
    uVar5 = *(undefined8 *)(param_2 + 0xc0);
    param_1[0x1a] = *(undefined8 *)(param_2 + 0xd0);
    param_1[0x19] = uVar7;
    param_1[0x18] = uVar5;
  }
  if (*(char *)(param_2 + 0xef) < '\0') {
    FUN_00018d20(param_1 + 0x1b,*(undefined8 *)(param_2 + 0xd8),*(undefined8 *)(param_2 + 0xe0));
  }
  else {
    uVar7 = *(undefined8 *)(param_2 + 0xe0);
    uVar5 = *(undefined8 *)(param_2 + 0xd8);
    param_1[0x1d] = *(undefined8 *)(param_2 + 0xe8);
    param_1[0x1c] = uVar7;
    param_1[0x1b] = uVar5;
  }
  uVar7 = *(undefined8 *)(param_2 + 0xf8);
  uVar5 = *(undefined8 *)(param_2 + 0xf0);
  uVar9 = *(undefined8 *)(param_2 + 0x108);
  uVar8 = *(undefined8 *)(param_2 + 0x100);
  uVar11 = *(undefined8 *)(param_2 + 0x118);
  uVar10 = *(undefined8 *)(param_2 + 0x110);
  uVar12 = *(undefined8 *)(param_2 + 0x11c);
  *(undefined8 *)((long)param_1 + 0x124) = *(undefined8 *)(param_2 + 0x124);
  *(undefined8 *)((long)param_1 + 0x11c) = uVar12;
  param_1[0x21] = uVar9;
  param_1[0x20] = uVar8;
  param_1[0x23] = uVar11;
  param_1[0x22] = uVar10;
  param_1[0x1f] = uVar7;
  param_1[0x1e] = uVar5;
  if (*(char *)(param_2 + 0x147) < '\0') {
    FUN_00018d20(param_1 + 0x26,*(undefined8 *)(param_2 + 0x130),*(undefined8 *)(param_2 + 0x138));
  }
  else {
    uVar7 = *(undefined8 *)(param_2 + 0x138);
    uVar5 = *(undefined8 *)(param_2 + 0x130);
    param_1[0x28] = *(undefined8 *)(param_2 + 0x140);
    param_1[0x27] = uVar7;
    param_1[0x26] = uVar5;
  }
  if (*(char *)(param_2 + 0x15f) < '\0') {
    FUN_00018d20(param_1 + 0x29,*(undefined8 *)(param_2 + 0x148),*(undefined8 *)(param_2 + 0x150));
  }
  else {
    uVar7 = *(undefined8 *)(param_2 + 0x150);
    uVar5 = *(undefined8 *)(param_2 + 0x148);
    param_1[0x2b] = *(undefined8 *)(param_2 + 0x158);
    param_1[0x2a] = uVar7;
    param_1[0x29] = uVar5;
  }
  if (*(char *)(param_2 + 0x177) < '\0') {
    FUN_00018d20(param_1 + 0x2c,*(undefined8 *)(param_2 + 0x160),*(undefined8 *)(param_2 + 0x168));
  }
  else {
    uVar7 = *(undefined8 *)(param_2 + 0x168);
    uVar5 = *(undefined8 *)(param_2 + 0x160);
    param_1[0x2e] = *(undefined8 *)(param_2 + 0x170);
    param_1[0x2d] = uVar7;
    param_1[0x2c] = uVar5;
  }
  param_1[0x2f] = 0;
  param_1[0x30] = 0;
  param_1[0x31] = 0;
  pvVar1 = *(void **)(param_2 + 0x178);
  sVar3 = *(long *)(param_2 + 0x180) - (long)pvVar1;
  if (sVar3 != 0) {
    if ((long)sVar3 < 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00018e5c(param_1 + 0x2f);
    }
    pvVar4 = (void *)__Znwm(sVar3);
    param_1[0x2f] = pvVar4;
    param_1[0x30] = pvVar4;
    param_1[0x31] = (long)pvVar4 + sVar3;
    _memcpy(pvVar4,pvVar1,sVar3);
    param_1[0x30] = (long)pvVar4 + sVar3;
  }
  FUN_04eae868(param_1 + 0x32,param_2 + 400);
  param_1[0x41] = *(undefined8 *)(param_2 + 0x208);
  lVar6 = *(long *)(param_2 + 0x210);
  param_1[0x42] = lVar6;
  if (lVar6 != 0) {
    *(long *)(lVar6 + 8) = *(long *)(lVar6 + 8) + 1;
  }
  *(undefined1 *)(param_1 + 0x43) = *(undefined1 *)(param_2 + 0x218);
  param_1[0x44] = *(undefined8 *)(param_2 + 0x220);
  lVar6 = *(long *)(param_2 + 0x228);
  param_1[0x45] = lVar6;
  if (lVar6 != 0) {
    *(long *)(lVar6 + 8) = *(long *)(lVar6 + 8) + 1;
  }
  param_1[0x46] = *(undefined8 *)(param_2 + 0x230);
  lVar6 = *(long *)(param_2 + 0x238);
  param_1[0x47] = lVar6;
  if (lVar6 != 0) {
    *(long *)(lVar6 + 8) = *(long *)(lVar6 + 8) + 1;
  }
  *(undefined1 *)(param_1 + 0x48) = *(undefined1 *)(param_2 + 0x240);
  param_1[0x49] = *(undefined8 *)(param_2 + 0x248);
  lVar6 = *(long *)(param_2 + 0x250);
  param_1[0x4a] = lVar6;
  if (lVar6 != 0) {
    *(long *)(lVar6 + 0x10) = *(long *)(lVar6 + 0x10) + 1;
  }
  *(undefined1 *)(param_1 + 0x4b) = *(undefined1 *)(param_2 + 600);
  if (*(char *)(param_2 + 0x277) < '\0') {
    FUN_00018d20(param_1 + 0x4c,*(undefined8 *)(param_2 + 0x260),*(undefined8 *)(param_2 + 0x268));
  }
  else {
    uVar7 = *(undefined8 *)(param_2 + 0x268);
    uVar5 = *(undefined8 *)(param_2 + 0x260);
    param_1[0x4e] = *(undefined8 *)(param_2 + 0x270);
    param_1[0x4d] = uVar7;
    param_1[0x4c] = uVar5;
  }
  return param_1;
}


