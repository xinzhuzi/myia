// Ghidra inferred pseudocode; requested=0x462ece8
// entry=0462ece8 end=0462edc7

void FUN_0462ece8(undefined8 param_1,undefined8 param_2)

{
  ulong uVar1;
  undefined *puVar2;
  size_t sVar3;
  undefined8 ***pppuVar4;
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
    if (sVar3 == 0) goto LAB_0462ed7c;
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
LAB_0462ed7c:
  *(undefined1 *)((long)pppuVar4 + sVar3) = 0;
  FUN_05941ea8(param_1,param_2,&local_58);
  if ((long)local_48 < 0) {
    __ZdlPvm(local_58,local_48 & 0x7fffffffffffffff);
  }
  return;
}


