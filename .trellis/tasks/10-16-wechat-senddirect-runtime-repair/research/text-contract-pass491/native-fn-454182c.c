// Ghidra inferred pseudocode; requested=0x454182c
// entry=0454182c end=04541953

void FUN_0454182c(undefined8 *param_1,long param_2,long *param_3)

{
  ulong uVar1;
  long lVar2;
  char *pcVar3;
  size_t sVar4;
  undefined8 ***pppuVar5;
  long lVar6;
  undefined1 uVar7;
  undefined8 **local_58;
  size_t local_50;
  undefined8 local_48;
  
  pcVar3 = (char *)(**(code **)(*param_3 + 0x10))(param_3);
  sVar4 = _strlen(pcVar3);
  if (0x7ffffffffffffff7 < sVar4) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_58);
  }
  if (sVar4 < 0x17) {
    local_48 = CONCAT17((char)sVar4,(undefined7)local_48);
    pppuVar5 = &local_58;
    if (sVar4 == 0) goto LAB_045418c4;
  }
  else {
    uVar1 = 0x19;
    if ((sVar4 | 7) != 0x17) {
      uVar1 = (sVar4 | 7) + 1;
    }
    pppuVar5 = (undefined8 ***)__Znwm(uVar1);
    local_48 = uVar1 | 0x8000000000000000;
    local_58 = pppuVar5;
    local_50 = sVar4;
  }
  _memmove(pppuVar5,pcVar3,sVar4);
LAB_045418c4:
  *(undefined1 *)((long)pppuVar5 + sVar4) = 0;
  lVar6 = FUN_02aea564(param_2 + 0x28,&local_58);
  if ((long)local_48 < 0) {
    __ZdlPvm(local_58,local_48 & 0x7fffffffffffffff);
  }
  if (lVar6 == 0) {
    uVar7 = 0;
    *(undefined1 *)param_1 = 0;
  }
  else {
    lVar2 = *(long *)(lVar6 + 0x30);
    *param_1 = *(undefined8 *)(lVar6 + 0x28);
    param_1[1] = lVar2;
    if (lVar2 != 0) {
      *(long *)(lVar2 + 8) = *(long *)(lVar2 + 8) + 1;
    }
    param_1[2] = *(undefined8 *)(lVar6 + 0x38);
    uVar7 = 1;
  }
  *(undefined1 *)(param_1 + 3) = uVar7;
  return;
}


