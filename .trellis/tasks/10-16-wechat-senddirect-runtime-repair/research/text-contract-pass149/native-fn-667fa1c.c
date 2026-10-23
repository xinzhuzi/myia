// Ghidra inferred pseudocode; requested=0x667fa1c
// entry=0667fa1c end=0667fb2b

long FUN_0667fa1c(long param_1)

{
  long lVar1;
  undefined8 *puVar2;
  undefined8 local_60;
  undefined8 uStack_58;
  ulong local_50;
  undefined8 local_40;
  undefined8 uStack_38;
  ulong local_30;
  
  lVar1 = __Znwm(0x148);
  if (*(char *)(param_1 + 0x97) < '\0') {
    FUN_00018d20(&local_60,*(undefined8 *)(param_1 + 0x80),*(undefined8 *)(param_1 + 0x88));
  }
  else {
    uStack_58 = *(undefined8 *)(param_1 + 0x88);
    local_60 = *(undefined8 *)(param_1 + 0x80);
    local_50 = *(ulong *)(param_1 + 0x90);
  }
  if ((DAT_0a51826b & 1) == 0) {
    DAT_0a518264 = (undefined4)DAT_09685c40;
    DAT_0a518268 = 0x7075;
    DAT_0a51826a = 0;
    DAT_0a51826b = 1;
  }
  puVar2 = (undefined8 *)
           __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKc
                     (&local_60,&DAT_0a518264);
  uStack_38 = puVar2[1];
  local_40 = *puVar2;
  local_30 = puVar2[2];
  puVar2[1] = 0;
  puVar2[2] = 0;
  *puVar2 = 0;
  FUN_066845d0(lVar1,&local_40);
  if ((long)local_30 < 0) {
    __ZdlPvm(local_40,local_30 & 0x7fffffffffffffff);
  }
  if ((long)local_50 < 0) {
    __ZdlPvm(local_60,local_50 & 0x7fffffffffffffff);
  }
  *(undefined1 *)(lVar1 + 0xf8) = 0;
  FUN_06684684(lVar1,param_1 + 0xe0);
  return lVar1;
}


