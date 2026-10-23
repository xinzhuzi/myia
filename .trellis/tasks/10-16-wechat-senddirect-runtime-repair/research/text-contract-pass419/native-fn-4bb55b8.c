// Ghidra inferred pseudocode; requested=0x4bb55b8
// entry=04bb55b8 end=04bb566b

bool FUN_04bb55b8(undefined8 *param_1)

{
  int iVar1;
  size_t sVar2;
  
  if ((DAT_0a4a554b & 1) == 0) {
    DAT_0a4a5540 = s_filehelp_948cddbc_085afe68._0_8_;
    DAT_0a4a5548 = 0x7265;
    DAT_0a4a554a = 0;
    DAT_0a4a554b = 1;
  }
  sVar2 = _strlen((char *)&DAT_0a4a5540);
  if ((long)*(char *)((long)param_1 + 0x17) < 0) {
    if (sVar2 == param_1[1]) {
      if (sVar2 == 0xffffffffffffffff) {
                    /* WARNING: Subroutine does not return */
        FUN_0020edd0(param_1);
      }
      param_1 = (undefined8 *)*param_1;
      goto LAB_04bb5638;
    }
  }
  else if (sVar2 == (long)*(char *)((long)param_1 + 0x17)) {
LAB_04bb5638:
    iVar1 = _memcmp(param_1,&DAT_0a4a5540,sVar2);
    return iVar1 == 0;
  }
  return false;
}


