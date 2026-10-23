// Ghidra inferred pseudocode; requested=0x30e3df8
// entry=030e3df8 end=030e3f3b

void FUN_030e3df8(undefined8 *param_1,int param_2,undefined8 param_3)

{
  undefined1 **ppuVar1;
  undefined8 *puVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  undefined1 *local_80;
  ulong uStack_78;
  undefined7 local_70;
  byte bStack_69;
  undefined8 local_68 [2];
  undefined7 local_58;
  char cStack_51;
  undefined8 local_50;
  undefined8 uStack_48;
  ulong local_40;
  
  if (param_2 != 0x31) {
    __ZNSt3__19to_stringEi();
    return;
  }
  __ZNSt3__19to_stringEi(local_68);
  if ((DAT_0a3d9612 & 1) == 0) {
    DAT_0a3d9610 = 0x5f;
    DAT_0a3d9612 = 1;
  }
  puVar2 = (undefined8 *)
           __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKc
                     (local_68,&DAT_0a3d9610);
  uStack_48 = puVar2[1];
  local_50 = *puVar2;
  local_40 = puVar2[2];
  puVar2[1] = 0;
  puVar2[2] = 0;
  *puVar2 = 0;
  __ZNSt3__19to_stringEi(&local_80,param_3);
  ppuVar1 = (undefined1 **)local_80;
  if (-1 < (char)bStack_69) {
    uStack_78 = (ulong)bStack_69;
    ppuVar1 = &local_80;
  }
  puVar2 = (undefined8 *)
           __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
                     (&local_50,ppuVar1,uStack_78);
  uVar4 = puVar2[1];
  uVar3 = *puVar2;
  param_1[2] = puVar2[2];
  param_1[1] = uVar4;
  *param_1 = uVar3;
  puVar2[1] = 0;
  puVar2[2] = 0;
  *puVar2 = 0;
  if ((char)bStack_69 < '\0') {
    __ZdlPvm(local_80,CONCAT17(bStack_69,local_70) & 0x7fffffffffffffff);
  }
  if ((long)local_40 < 0) {
    __ZdlPvm(local_50,local_40 & 0x7fffffffffffffff);
  }
  if (cStack_51 < '\0') {
    __ZdlPvm(local_68[0],CONCAT17(cStack_51,local_58) & 0x7fffffffffffffff);
  }
  return;
}


