// Ghidra inferred pseudocode; requested=0x30e74f4
// entry=030e74f4 end=030e75c3

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_030e74f4(undefined8 *param_1)

{
  ulong uVar1;
  size_t sVar2;
  undefined8 *puVar3;
  
  if ((DAT_0a3d9633 & 1) == 0) {
    uRam000000000a3d9628 = s_TextMessageHandlImageMessageHand_088b0090._8_8_;
    _DAT_0a3d9620 = s_TextMessageHandlImageMessageHand_088b0090._0_8_;
    DAT_0a3d9630 = 0x7265;
    DAT_0a3d9632 = 0;
    DAT_0a3d9633 = 1;
  }
  sVar2 = _strlen(&DAT_0a3d9620);
  if (0x7ffffffffffffff7 < sVar2) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(param_1);
  }
  if (sVar2 < 0x17) {
    *(char *)((long)param_1 + 0x17) = (char)sVar2;
    puVar3 = param_1;
    if (sVar2 == 0) goto LAB_030e75a8;
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
  _memcpy(puVar3,&DAT_0a3d9620,sVar2);
  param_1 = puVar3;
LAB_030e75a8:
  *(undefined1 *)((long)param_1 + sVar2) = 0;
  return;
}


