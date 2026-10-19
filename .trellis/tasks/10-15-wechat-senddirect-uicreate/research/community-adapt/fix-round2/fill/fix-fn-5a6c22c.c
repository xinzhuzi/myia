// requested=0x5a6c22c
// entry=05a6c22c end=05a6c373

void FUN_05a6c22c(long param_1,long param_2)

{
  undefined4 uVar1;
  byte bVar2;
  undefined8 uVar3;
  undefined8 *puVar4;
  uint uVar5;
  undefined1 uStack_61;
  undefined1 auStack_60 [48];
  
  if (param_2 == param_1) {
    FUN_05ab442c(auStack_60,3,
                 "/Users/bkdevops/.wconan2/mmnet/e27341bb_1784873910/mars-wechat/mars/mm-ext/src/protobuf/mmaction.pb.cc"
                 ,0x264);
    uVar3 = FUN_05ab4444(auStack_60,"CHECK failed: (&from) != (this): ");
    FUN_05ab4574(&uStack_61,uVar3);
    FUN_05ab457c(auStack_60);
  }
  bVar2 = *(byte *)(param_2 + 0x24);
  uVar5 = (uint)bVar2;
  if (bVar2 == 0) {
    return;
  }
  if ((bVar2 & 1) == 0) {
    if ((bVar2 >> 1 & 1) == 0) goto joined_r0x05a6c2a4;
  }
  else {
    uVar3 = *(undefined8 *)(param_2 + 8);
    *(uint *)(param_1 + 0x24) = *(uint *)(param_1 + 0x24) | 1;
    puVar4 = *(undefined8 **)(param_1 + 8);
    if (puVar4 == &DAT_0a524ad0) {
      puVar4 = (undefined8 *)__Znwm(0x18);
      puVar4[1] = 0;
      puVar4[2] = 0;
      *puVar4 = 0;
      *(undefined8 **)(param_1 + 8) = puVar4;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar4,uVar3);
    uVar5 = *(uint *)(param_2 + 0x24);
    if ((uVar5 >> 1 & 1) == 0) goto joined_r0x05a6c2a4;
  }
  uVar1 = *(undefined4 *)(param_2 + 0x18);
  *(uint *)(param_1 + 0x24) = *(uint *)(param_1 + 0x24) | 2;
  *(undefined4 *)(param_1 + 0x18) = uVar1;
  uVar5 = *(uint *)(param_2 + 0x24);
joined_r0x05a6c2a4:
  if ((uVar5 >> 2 & 1) != 0) {
    uVar3 = *(undefined8 *)(param_2 + 0x10);
    *(uint *)(param_1 + 0x24) = *(uint *)(param_1 + 0x24) | 4;
    puVar4 = *(undefined8 **)(param_1 + 0x10);
    if (puVar4 == &DAT_0a524ad0) {
      puVar4 = (undefined8 *)__Znwm(0x18);
      puVar4[1] = 0;
      puVar4[2] = 0;
      *puVar4 = 0;
      *(undefined8 **)(param_1 + 0x10) = puVar4;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar4,uVar3);
    uVar5 = *(uint *)(param_2 + 0x24);
  }
  if ((uVar5 >> 3 & 1) != 0) {
    uVar1 = *(undefined4 *)(param_2 + 0x1c);
    *(uint *)(param_1 + 0x24) = *(uint *)(param_1 + 0x24) | 8;
    *(undefined4 *)(param_1 + 0x1c) = uVar1;
  }
  return;
}


