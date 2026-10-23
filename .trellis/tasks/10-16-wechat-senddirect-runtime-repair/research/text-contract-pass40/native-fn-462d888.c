// Ghidra inferred pseudocode; requested=0x462d888
// entry=0462d888 end=0462d95f

void FUN_0462d888(undefined8 param_1,undefined8 param_2,char *param_3)

{
  ulong uVar1;
  size_t sVar2;
  undefined8 ******ppppppuVar3;
  undefined8 *****local_58;
  size_t local_50;
  undefined8 local_48;
  
  if (param_3 == (char *)0x0) {
    return;
  }
  sVar2 = _strlen(param_3);
  if (0x7ffffffffffffff7 < sVar2) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_58);
  }
  if (sVar2 < 0x17) {
    local_48 = CONCAT17((char)sVar2,(undefined7)local_48);
    ppppppuVar3 = &local_58;
    if (sVar2 == 0) goto LAB_0462d914;
  }
  else {
    uVar1 = 0x19;
    if ((sVar2 | 7) != 0x17) {
      uVar1 = (sVar2 | 7) + 1;
    }
    ppppppuVar3 = (undefined8 ******)__Znwm(uVar1);
    local_48 = uVar1 | 0x8000000000000000;
    local_58 = ppppppuVar3;
    local_50 = sVar2;
  }
  _memcpy(ppppppuVar3,param_3,sVar2);
LAB_0462d914:
  *(undefined1 *)((long)ppppppuVar3 + sVar2) = 0;
  FUN_046442c4(param_2,&local_58,0);
  if ((long)local_48 < 0) {
    __ZdlPvm(local_58,local_48 & 0x7fffffffffffffff);
  }
  return;
}


