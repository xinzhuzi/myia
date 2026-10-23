// Ghidra inferred pseudocode; requested=0x55bf46c
// entry=055bf46c end=055bf577

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_055bf46c(undefined8 *param_1)

{
  ulong uVar1;
  size_t sVar2;
  undefined8 *puVar3;
  
  if ((DAT_0a4d42b8 & 1) == 0) {
    _DAT_0a4d429c = CONCAT44((int)ram0x08b28300,(int)DAT_084967c8);
    uRam000000000a4d42a4 = CONCAT44((int)DAT_085cc658,(int)DAT_08b287a0);
    DAT_0a4d42ac = CONCAT44((int)DAT_084d87c0,(int)DAT_08587a18);
    DAT_0a4d42b4 = (undefined4)ram0x08563380;
    DAT_0a4d42b8 = 1;
  }
  sVar2 = _strlen(&DAT_0a4d429c);
  if (0x7ffffffffffffff7 < sVar2) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(param_1);
  }
  if (sVar2 < 0x17) {
    *(char *)((long)param_1 + 0x17) = (char)sVar2;
    puVar3 = param_1;
    if (sVar2 == 0) goto LAB_055bf55c;
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
  _memcpy(puVar3,&DAT_0a4d429c,sVar2);
  param_1 = puVar3;
LAB_055bf55c:
  *(undefined1 *)((long)param_1 + sVar2) = 0;
  return;
}


