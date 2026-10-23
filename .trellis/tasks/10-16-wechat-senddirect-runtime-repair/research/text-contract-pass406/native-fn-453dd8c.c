// Ghidra inferred pseudocode; requested=0x453dd8c
// entry=0453dd8c end=0453de8f

void FUN_0453dd8c(undefined8 *param_1,undefined8 param_2,undefined8 param_3)

{
  undefined1 **ppuVar1;
  undefined8 uVar2;
  undefined8 *puVar3;
  undefined8 uVar4;
  undefined1 *local_60;
  ulong uStack_58;
  undefined7 local_50;
  byte bStack_49;
  undefined8 local_48 [2];
  undefined7 local_38;
  char cStack_31;
  
  FUN_0453d700(local_48);
  if ((DAT_0a4557c8 & 1) == 0) {
    DAT_0a4557c6 = 0x3a;
    DAT_0a4557c8 = 1;
  }
  uVar2 = __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKc
                    (local_48,&DAT_0a4557c6);
  __ZNSt3__19to_stringEi(&local_60,param_3);
  ppuVar1 = (undefined1 **)local_60;
  if (-1 < (char)bStack_49) {
    uStack_58 = (ulong)bStack_49;
    ppuVar1 = &local_60;
  }
  puVar3 = (undefined8 *)
           __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
                     (uVar2,ppuVar1,uStack_58);
  if (*(char *)((long)puVar3 + 0x17) < '\0') {
    FUN_00018d20(param_1,*puVar3,puVar3[1]);
  }
  else {
    uVar4 = puVar3[1];
    uVar2 = *puVar3;
    param_1[2] = puVar3[2];
    param_1[1] = uVar4;
    *param_1 = uVar2;
  }
  if ((char)bStack_49 < '\0') {
    __ZdlPvm(local_60,CONCAT17(bStack_49,local_50) & 0x7fffffffffffffff);
  }
  if (cStack_31 < '\0') {
    __ZdlPvm(local_48[0],CONCAT17(cStack_31,local_38) & 0x7fffffffffffffff);
  }
  return;
}


