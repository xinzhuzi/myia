// Ghidra inferred pseudocode; requested=0x4bb5048
// entry=04bb5048 end=04bb50fb

bool FUN_04bb5048(undefined8 *param_1)

{
  int iVar1;
  size_t sVar2;
  
  if ((DAT_0a4a54b3 & 1) == 0) {
    DAT_0a4a54ac = (undefined4)DAT_0858ff60;
    DAT_0a4a54b0 = 0x6c69;
    DAT_0a4a54b2 = 0;
    DAT_0a4a54b3 = 1;
  }
  sVar2 = _strlen((char *)&DAT_0a4a54ac);
  if ((long)*(char *)((long)param_1 + 0x17) < 0) {
    if (sVar2 == param_1[1]) {
      if (sVar2 == 0xffffffffffffffff) {
                    /* WARNING: Subroutine does not return */
        FUN_0020edd0(param_1);
      }
      param_1 = (undefined8 *)*param_1;
      goto LAB_04bb50c8;
    }
  }
  else if (sVar2 == (long)*(char *)((long)param_1 + 0x17)) {
LAB_04bb50c8:
    iVar1 = _memcmp(param_1,&DAT_0a4a54ac,sVar2);
    return iVar1 == 0;
  }
  return false;
}


