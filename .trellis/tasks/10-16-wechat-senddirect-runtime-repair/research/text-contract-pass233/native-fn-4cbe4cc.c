// Ghidra inferred pseudocode; requested=0x4cbe4cc
// entry=04cbe4cc end=04cbe5eb

void FUN_04cbe4cc(undefined8 *param_1,long param_2)

{
  undefined1 **ppuVar1;
  undefined8 *puVar2;
  undefined8 uVar3;
  undefined1 *local_70;
  ulong uStack_68;
  undefined7 local_60;
  byte bStack_59;
  undefined8 local_58 [2];
  undefined7 local_48;
  char cStack_41;
  undefined8 local_40;
  undefined8 uStack_38;
  ulong local_30;
  
  FUN_04cbe440(local_58);
  if ((DAT_0a4ada57 & 1) == 0) {
    DAT_0a4ada55 = 0x5f;
    DAT_0a4ada57 = 1;
  }
  puVar2 = (undefined8 *)
           __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKc
                     (local_58,&DAT_0a4ada55);
  uStack_38 = puVar2[1];
  local_40 = *puVar2;
  local_30 = puVar2[2];
  puVar2[1] = 0;
  puVar2[2] = 0;
  *puVar2 = 0;
  __ZNSt3__19to_stringEy(&local_70,*(undefined8 *)(param_2 + 0xf8));
  ppuVar1 = (undefined1 **)local_70;
  if (-1 < (char)bStack_59) {
    uStack_68 = (ulong)bStack_59;
    ppuVar1 = &local_70;
  }
  puVar2 = (undefined8 *)
           __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
                     (&local_40,ppuVar1,uStack_68);
  uVar3 = *puVar2;
  param_1[1] = puVar2[1];
  *param_1 = uVar3;
  param_1[2] = puVar2[2];
  puVar2[1] = 0;
  puVar2[2] = 0;
  *puVar2 = 0;
  if ((char)bStack_59 < '\0') {
    __ZdlPvm(local_70,CONCAT17(bStack_59,local_60) & 0x7fffffffffffffff);
  }
  if ((long)local_30 < 0) {
    __ZdlPvm(local_40,local_30 & 0x7fffffffffffffff);
  }
  if (cStack_41 < '\0') {
    __ZdlPvm(local_58[0],CONCAT17(cStack_41,local_48) & 0x7fffffffffffffff);
  }
  return;
}


