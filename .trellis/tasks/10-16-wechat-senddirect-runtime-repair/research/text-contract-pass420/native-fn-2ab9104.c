// Ghidra inferred pseudocode; requested=0x2ab9104
// entry=02ab9104 end=02ab91eb

void FUN_02ab9104(undefined8 param_1,long param_2)

{
  ulong uVar1;
  char *pcVar2;
  size_t sVar3;
  undefined1 **ppuVar4;
  undefined1 **ppuVar5;
  undefined1 *local_60;
  size_t local_58;
  undefined8 local_50;
  undefined4 local_44;
  
  ppuVar4 = &local_60;
  ppuVar5 = &local_60;
  local_44 = *(undefined4 *)(param_2 + 0x54);
  FUN_047252c4(&local_44);
  *(undefined4 *)(param_2 + 0x54) = local_44;
  pcVar2 = (char *)FUN_04dfda08();
  sVar3 = _strlen(pcVar2);
  if (0x7ffffffffffffff7 < sVar3) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_60);
  }
  if (sVar3 < 0x17) {
    local_50 = CONCAT17((char)sVar3,(undefined7)local_50);
    if (sVar3 == 0) goto LAB_02ab91a4;
  }
  else {
    uVar1 = 0x19;
    if ((sVar3 | 7) != 0x17) {
      uVar1 = (sVar3 | 7) + 1;
    }
    ppuVar4 = (undefined1 **)__Znwm(uVar1);
    local_50 = uVar1 | 0x8000000000000000;
    local_60 = (undefined1 *)ppuVar4;
    local_58 = sVar3;
  }
  _memmove(ppuVar4,pcVar2,sVar3);
  ppuVar5 = ppuVar4;
LAB_02ab91a4:
  *(undefined1 *)((long)ppuVar5 + sVar3) = 0;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_2 + 0xa8,&local_60)
  ;
  if ((long)local_50 < 0) {
    __ZdlPvm(local_60,local_50 & 0x7fffffffffffffff);
  }
  return;
}


