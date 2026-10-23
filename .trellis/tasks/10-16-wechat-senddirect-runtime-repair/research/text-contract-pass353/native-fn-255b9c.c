// Ghidra inferred pseudocode; requested=0x255b9c
// entry=00255b9c end=00255c43

undefined8 * FUN_00255b9c(undefined8 *param_1,char *param_2)

{
  ulong uVar1;
  size_t sVar2;
  undefined8 *puVar3;
  
  sVar2 = _strlen(param_2);
  if (0x7ffffffffffffff7 < sVar2) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(param_1);
  }
  if (sVar2 < 0x17) {
    *(char *)((long)param_1 + 0x17) = (char)sVar2;
    puVar3 = param_1;
    if (sVar2 == 0) goto LAB_00255c20;
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
  _memmove(puVar3,param_2,sVar2);
LAB_00255c20:
  *(undefined1 *)((long)puVar3 + sVar2) = 0;
  return param_1;
}


