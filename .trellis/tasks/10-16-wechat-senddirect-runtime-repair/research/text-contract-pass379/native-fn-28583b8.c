// Ghidra inferred pseudocode; requested=0x28583b8
// entry=028583b8 end=02858527

void FUN_028583b8(undefined8 param_1,undefined8 param_2,undefined8 param_3,uint param_4,uint param_5
                 ,undefined8 param_6,long param_7,undefined8 param_8,undefined8 param_9,
                 undefined8 param_10)

{
  long lVar1;
  ulong local_f0;
  undefined8 local_e8;
  undefined8 uStack_e0;
  ulong local_d8;
  ulong uStack_d0;
  undefined8 local_c8;
  undefined8 uStack_c0;
  undefined8 local_b8;
  undefined8 uStack_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  ulong uStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  ulong local_78;
  undefined8 uStack_70;
  undefined8 local_68;
  ulong uStack_60;
  undefined8 local_58;
  undefined8 uStack_50;
  ulong local_48;
  
  uStack_c0 = 0;
  local_c8 = 0;
  uStack_b0 = 0;
  local_b8 = 0;
  uStack_a0 = 0;
  local_a8 = 0;
  uStack_90 = 0;
  local_98 = 0;
  uStack_80 = 0;
  local_88 = 0;
  uStack_70 = 0;
  local_78 = 0;
  uStack_60 = 0;
  local_68 = 0;
  uStack_50 = 0;
  local_58 = 0;
  local_48 = 0;
  local_e8 = 0xaaaaaaaa00000001;
  local_d8 = (ulong)param_4;
  uStack_d0 = (ulong)param_5;
  uStack_e0 = param_3;
  lVar1 = thunk_FUN_000a5900();
  local_f0 = lVar1 - param_7 >> 0x3f ^ 0x8000000000000000;
  if (!SBORROW8(lVar1,param_7)) {
    local_f0 = lVar1 - param_7;
  }
  local_c8 = FUN_000a4ee8(&local_f0);
  local_b8 = param_9;
  uStack_c0 = param_8;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(&uStack_a0,param_1);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(&local_88,param_6);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(&uStack_70,param_2);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(&local_58,param_10);
  FUN_04ae091c(&local_e8);
  if ((long)local_48 < 0) {
    __ZdlPvm(local_58,local_48 & 0x7fffffffffffffff);
  }
  if ((long)uStack_60 < 0) {
    __ZdlPvm(uStack_70,uStack_60 & 0x7fffffffffffffff);
  }
  if ((long)local_78 < 0) {
    __ZdlPvm(local_88,local_78 & 0x7fffffffffffffff);
  }
  if ((long)uStack_90 < 0) {
    __ZdlPvm(uStack_a0,uStack_90 & 0x7fffffffffffffff);
  }
  return;
}


