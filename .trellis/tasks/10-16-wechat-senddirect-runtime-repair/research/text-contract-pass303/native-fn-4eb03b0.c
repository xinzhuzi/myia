// Ghidra inferred pseudocode; requested=0x4eb03b0
// entry=04eb03b0 end=04eb04bb

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_04eb03b0(undefined8 *param_1)

{
  ulong uVar1;
  size_t sVar2;
  undefined8 *puVar3;
  
  if ((DAT_0a4b97eb & 1) == 0) {
    _DAT_0a4b97d0 = CONCAT44((int)DAT_08a12af8,(int)ram0x086f4e70);
    uRam000000000a4b97d8 = CONCAT44((int)DAT_084a66b0,(int)DAT_08af1c10);
    DAT_0a4b97e0 = CONCAT44((int)DAT_08771688,(int)DAT_087711d0);
    DAT_0a4b97e8 = 0x6f66;
    DAT_0a4b97ea = 0;
    DAT_0a4b97eb = 1;
  }
  sVar2 = _strlen(&DAT_0a4b97d0);
  if (0x7ffffffffffffff7 < sVar2) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(param_1);
  }
  if (sVar2 < 0x17) {
    *(char *)((long)param_1 + 0x17) = (char)sVar2;
    puVar3 = param_1;
    if (sVar2 == 0) goto LAB_04eb04a0;
  }
  else {
    uVar1 = 0x19;
    if ((sVar2 | 7) != 0x17) {
      uVar1 = (sVar2 | 7) + 1;
    }
    puVar3 = (undefined8 *)__Znwm(uVar1);
    param_1[1] = sVar2;
    param_1[2] = uVar1 | 0x8000000000000000;
    *param_1 = puVar3;
  }
  _memcpy(puVar3,&DAT_0a4b97d0,sVar2);
  param_1 = puVar3;
LAB_04eb04a0:
  *(undefined1 *)((long)param_1 + sVar2) = 0;
  return;
}


