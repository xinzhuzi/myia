// Ghidra inferred pseudocode; requested=0x4632830
// entry=04632830 end=04632913

undefined8 FUN_04632830(undefined8 param_1)

{
  ulong uVar1;
  undefined *puVar2;
  size_t sVar3;
  undefined8 ***pppuVar4;
  undefined8 uVar5;
  undefined8 **local_58;
  size_t local_50;
  undefined8 local_48;
  
  puVar2 = PTR_s_N4mars3stn12MMStnManagerE_09f2e408;
  sVar3 = _strlen((char *)((ulong)PTR_s_N4mars3stn12MMStnManagerE_09f2e408 & 0x7fffffffffffffff));
  if (0x7ffffffffffffff7 < sVar3) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_58);
  }
  if (sVar3 < 0x17) {
    local_48 = CONCAT17((char)sVar3,(undefined7)local_48);
    pppuVar4 = &local_58;
    if (sVar3 == 0) goto LAB_046328c0;
  }
  else {
    uVar1 = 0x19;
    if ((sVar3 | 7) != 0x17) {
      uVar1 = (sVar3 | 7) + 1;
    }
    pppuVar4 = (undefined8 ***)__Znwm(uVar1);
    local_48 = uVar1 | 0x8000000000000000;
    local_58 = pppuVar4;
    local_50 = sVar3;
  }
  _memmove(pppuVar4,(void *)((ulong)puVar2 & 0x7fffffffffffffff),sVar3);
LAB_046328c0:
  *(undefined1 *)((long)pppuVar4 + sVar3) = 0;
  uVar5 = FUN_05941f18(param_1,&local_58);
  if ((long)local_48 < 0) {
    __ZdlPvm(local_58,local_48 & 0x7fffffffffffffff);
  }
  return uVar5;
}


