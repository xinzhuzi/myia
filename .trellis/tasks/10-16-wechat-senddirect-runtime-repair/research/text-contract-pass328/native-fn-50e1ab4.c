// Ghidra inferred pseudocode; requested=0x50e1ab4
// entry=050e1ab4 end=050e1bbf

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_050e1ab4(undefined8 *param_1)

{
  ulong uVar1;
  size_t sVar2;
  undefined8 *puVar3;
  
  if ((DAT_0a4c2b6f & 1) == 0) {
    _DAT_0a4c2b54 = CONCAT44((int)DAT_08a12af8,(int)ram0x086f4e70);
    uRam000000000a4c2b5c = CONCAT44((int)DAT_088bb140,(int)DAT_08b052f8);
    DAT_0a4c2b64 = CONCAT44((int)DAT_08545098,(int)DAT_087e31d8);
    DAT_0a4c2b6c = 0x6573;
    DAT_0a4c2b6e = 0;
    DAT_0a4c2b6f = 1;
  }
  sVar2 = _strlen(&DAT_0a4c2b54);
  if (0x7ffffffffffffff7 < sVar2) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(param_1);
  }
  if (sVar2 < 0x17) {
    *(char *)((long)param_1 + 0x17) = (char)sVar2;
    puVar3 = param_1;
    if (sVar2 == 0) goto LAB_050e1ba4;
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
  _memcpy(puVar3,&DAT_0a4c2b54,sVar2);
  param_1 = puVar3;
LAB_050e1ba4:
  *(undefined1 *)((long)param_1 + sVar2) = 0;
  return;
}


