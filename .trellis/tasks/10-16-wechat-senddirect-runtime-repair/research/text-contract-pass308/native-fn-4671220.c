// Ghidra inferred pseudocode; requested=0x4671220
// entry=04671220 end=04671323

void FUN_04671220(long param_1)

{
  undefined8 uVar1;
  undefined4 local_d8;
  undefined4 local_d4;
  undefined1 *local_d0;
  undefined8 uStack_c8;
  undefined8 uStack_c0;
  undefined8 uStack_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 uStack_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 uStack_80;
  undefined8 local_78;
  undefined8 local_70;
  ulong uStack_68;
  undefined8 local_60;
  undefined8 uStack_58;
  ulong local_50;
  undefined8 uStack_48;
  undefined4 local_40;
  undefined4 uStack_3c;
  undefined4 uStack_38;
  int iStack_34;
  undefined4 local_30;
  undefined4 uStack_2c;
  undefined8 uStack_28;
  
  local_d4 = 0;
  local_d0 = &DAT_aaaaaaaa00000000;
  uStack_2c = 0xaaaaaaaa;
  uStack_28 = 0;
  uStack_c0 = 0;
  uStack_c8 = 0;
  local_b0 = 0;
  uStack_b8 = 0;
  uStack_a0 = 0;
  uStack_a8 = 0;
  local_90 = 0;
  uStack_98 = 0;
  uStack_80 = 0;
  uStack_88 = 0;
  local_70 = 0;
  local_78 = 0;
  local_60 = 0;
  uStack_68 = 0;
  local_50 = 0;
  uStack_58 = 0;
  local_40 = 0;
  uStack_48 = 0;
  iStack_34 = 0;
  local_30 = 0;
  uStack_3c = 0;
  uStack_38 = 0;
  local_d8 = 0x15;
  uVar1 = FUN_04748e38();
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(&local_78,uVar1);
  FUN_04af307c(&local_d8,0);
  FUN_04a46168(*(undefined8 *)(param_1 + 0xb0));
  if (iStack_34 < 0) {
    __ZdlPvm(uStack_48,CONCAT44(iStack_34,uStack_38) & 0x7fffffffffffffff);
  }
  if ((long)local_50 < 0) {
    __ZdlPvm(local_60,local_50 & 0x7fffffffffffffff);
  }
  if ((long)uStack_68 < 0) {
    __ZdlPvm(local_78,uStack_68 & 0x7fffffffffffffff);
  }
  return;
}


