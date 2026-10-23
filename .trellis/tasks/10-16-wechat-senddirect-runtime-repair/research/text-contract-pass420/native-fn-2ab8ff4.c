// Ghidra inferred pseudocode; requested=0x2ab8ff4
// entry=02ab8ff4 end=02ab90e7

void FUN_02ab8ff4(undefined8 param_1,long param_2)

{
  ulong uVar1;
  int iVar2;
  char *pcVar3;
  size_t sVar4;
  undefined1 **ppuVar5;
  undefined1 **ppuVar6;
  undefined1 *local_60;
  size_t local_58;
  undefined8 local_50;
  undefined4 local_44;
  
  ppuVar5 = &local_60;
  ppuVar6 = &local_60;
  iVar2 = FUN_04bb5048(param_2 + 8);
  if (iVar2 == 0) {
    return;
  }
  local_44 = *(undefined4 *)(param_2 + 0x54);
  FUN_0472329c(&local_44);
  *(undefined4 *)(param_2 + 0x54) = local_44;
  pcVar3 = (char *)FUN_04e11118();
  sVar4 = _strlen(pcVar3);
  if (0x7ffffffffffffff7 < sVar4) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_60);
  }
  if (sVar4 < 0x17) {
    local_50 = CONCAT17((char)sVar4,(undefined7)local_50);
    if (sVar4 == 0) goto LAB_02ab90a0;
  }
  else {
    uVar1 = 0x19;
    if ((sVar4 | 7) != 0x17) {
      uVar1 = (sVar4 | 7) + 1;
    }
    ppuVar5 = (undefined1 **)__Znwm(uVar1);
    local_50 = uVar1 | 0x8000000000000000;
    local_60 = (undefined1 *)ppuVar5;
    local_58 = sVar4;
  }
  _memmove(ppuVar5,pcVar3,sVar4);
  ppuVar6 = ppuVar5;
LAB_02ab90a0:
  *(undefined1 *)((long)ppuVar6 + sVar4) = 0;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_2 + 0xa8,&local_60)
  ;
  if ((long)local_50 < 0) {
    __ZdlPvm(local_60,local_50 & 0x7fffffffffffffff);
  }
  return;
}


