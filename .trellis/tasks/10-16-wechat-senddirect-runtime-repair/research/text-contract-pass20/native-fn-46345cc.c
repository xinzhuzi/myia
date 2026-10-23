// Ghidra inferred pseudocode; requested=0x46345cc
// entry=046345cc end=046346c7

void FUN_046345cc(void)

{
  ulong uVar1;
  size_t sVar2;
  undefined8 ***pppuVar3;
  undefined8 **local_48;
  size_t local_40;
  undefined8 local_38;
  
  if ((DAT_0a45ce90 & 1) == 0) {
    DAT_0a45ce88 = s_default_084c7818;
    DAT_0a45ce90 = 1;
  }
  sVar2 = _strlen(DAT_0a45ce88);
  if (0x7ffffffffffffff7 < sVar2) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_48);
  }
  if (sVar2 < 0x17) {
    local_38 = CONCAT17((char)sVar2,(undefined7)local_38);
    pppuVar3 = &local_48;
    if (sVar2 == 0) goto LAB_04634674;
  }
  else {
    uVar1 = 0x19;
    if ((sVar2 | 7) != 0x17) {
      uVar1 = (sVar2 | 7) + 1;
    }
    pppuVar3 = (undefined8 ***)__Znwm(uVar1);
    local_38 = uVar1 | 0x8000000000000000;
    local_48 = pppuVar3;
    local_40 = sVar2;
  }
  _memcpy(pppuVar3,DAT_0a45ce88,sVar2);
LAB_04634674:
  *(undefined1 *)((long)pppuVar3 + sVar2) = 0;
  FUN_05cef5b8(1,&local_48);
  if ((long)local_38 < 0) {
    __ZdlPvm(local_48,local_38 & 0x7fffffffffffffff);
  }
  (*(code *)PTR_FUN_0a124bc8)();
  return;
}


