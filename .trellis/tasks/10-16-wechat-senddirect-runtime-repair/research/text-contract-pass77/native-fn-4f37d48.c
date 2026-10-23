// Ghidra inferred pseudocode; requested=0x4f37d48
// entry=04f37d48 end=04f37e53

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_04f37d48(undefined8 *param_1)

{
  ulong uVar1;
  size_t sVar2;
  undefined8 *puVar3;
  
  if ((DAT_0a4bbbb7 & 1) == 0) {
    _DAT_0a4bbb9c = CONCAT44((int)DAT_08a12af8,(int)ram0x086f4e70);
    uRam000000000a4bbba4 = CONCAT44((int)DAT_08af6830,(int)DAT_08af6828);
    DAT_0a4bbbac = CONCAT44((int)ram0x0847fe58,(int)DAT_08af6880);
    DAT_0a4bbbb4 = 0x745f;
    DAT_0a4bbbb6 = 0;
    DAT_0a4bbbb7 = 1;
  }
  sVar2 = _strlen(&DAT_0a4bbb9c);
  if (0x7ffffffffffffff7 < sVar2) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(param_1);
  }
  if (sVar2 < 0x17) {
    *(char *)((long)param_1 + 0x17) = (char)sVar2;
    puVar3 = param_1;
    if (sVar2 == 0) goto LAB_04f37e38;
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
  _memcpy(puVar3,&DAT_0a4bbb9c,sVar2);
  param_1 = puVar3;
LAB_04f37e38:
  *(undefined1 *)((long)param_1 + sVar2) = 0;
  return;
}


