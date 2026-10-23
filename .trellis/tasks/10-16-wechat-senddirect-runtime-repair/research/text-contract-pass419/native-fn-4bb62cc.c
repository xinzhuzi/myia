// Ghidra inferred pseudocode; requested=0x4bb62cc
// entry=04bb62cc end=04bb639f

bool FUN_04bb62cc(undefined8 *param_1)

{
  int iVar1;
  size_t sVar2;
  ulong uVar3;
  
  if ((DAT_0a4a5835 & 1) == 0) {
    uVar3 = 0;
    do {
      (&DAT_0a4a5821)[uVar3] = (&DAT_08ac42fe)[uVar3] + 0x8a ^ (&DAT_08ac42ee)[uVar3 & 0xf];
      uVar3 = uVar3 + 1;
    } while (uVar3 != 0x14);
    DAT_0a4a5835 = 1;
  }
  sVar2 = _strlen(&DAT_0a4a5821);
  if ((long)*(char *)((long)param_1 + 0x17) < 0) {
    if (sVar2 == param_1[1]) {
      if (sVar2 == 0xffffffffffffffff) {
                    /* WARNING: Subroutine does not return */
        FUN_0020edd0(param_1);
      }
      param_1 = (undefined8 *)*param_1;
      goto LAB_04bb636c;
    }
  }
  else if (sVar2 == (long)*(char *)((long)param_1 + 0x17)) {
LAB_04bb636c:
    iVar1 = _memcmp(param_1,&DAT_0a4a5821,sVar2);
    return iVar1 == 0;
  }
  return false;
}


