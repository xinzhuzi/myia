// Ghidra inferred pseudocode; requested=0x4bb4c9c
// entry=04bb4c9c end=04bb4da3

undefined8 FUN_04bb4c9c(undefined8 param_1)

{
  ulong uVar1;
  size_t sVar2;
  undefined8 ***pppuVar3;
  undefined8 uVar4;
  undefined8 **local_48;
  size_t local_40;
  undefined8 local_38;
  
  if ((DAT_0a4a5752 & 1) == 0) {
    DAT_0a4a574c = (undefined4)DAT_08ac3920;
    DAT_0a4a5750 = 0x67;
    DAT_0a4a5752 = 1;
  }
  sVar2 = _strlen((char *)&DAT_0a4a574c);
  if (0x7ffffffffffffff7 < sVar2) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_48);
  }
  if (sVar2 < 0x17) {
    local_38 = CONCAT17((char)sVar2,(undefined7)local_38);
    pppuVar3 = &local_48;
    if (sVar2 == 0) goto LAB_04bb4d54;
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
  _memcpy(pppuVar3,&DAT_0a4a574c,sVar2);
LAB_04bb4d54:
  *(undefined1 *)((long)pppuVar3 + sVar2) = 0;
  uVar4 = FUN_066881c4(param_1,&local_48);
  if ((long)local_38 < 0) {
    __ZdlPvm(local_48,local_38 & 0x7fffffffffffffff);
  }
  return uVar4;
}


