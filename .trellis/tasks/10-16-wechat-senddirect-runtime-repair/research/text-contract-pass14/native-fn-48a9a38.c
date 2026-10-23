// Ghidra inferred pseudocode; requested=0x48a9a38
// entry=048a9a38 end=048a9af3

bool FUN_048a9a38(undefined8 *param_1)

{
  int iVar1;
  size_t sVar2;
  
  if ((DAT_0a474016 & 1) == 0) {
    DAT_0a474008 = s_SendMsgFtouserna_tou_088bac38._0_8_;
    DAT_0a474010 = (undefined4)DAT_084caf50;
    DAT_0a474014 = 100;
    DAT_0a474016 = 1;
  }
  sVar2 = _strlen((char *)&DAT_0a474008);
  if ((long)*(char *)((long)param_1 + 0x17) < 0) {
    if (sVar2 == param_1[1]) {
      if (sVar2 == 0xffffffffffffffff) {
                    /* WARNING: Subroutine does not return */
        FUN_0020edd0(param_1);
      }
      param_1 = (undefined8 *)*param_1;
      goto LAB_048a9ac0;
    }
  }
  else if (sVar2 == (long)*(char *)((long)param_1 + 0x17)) {
LAB_048a9ac0:
    iVar1 = _memcmp(param_1,&DAT_0a474008,sVar2);
    return iVar1 == 0;
  }
  return false;
}


