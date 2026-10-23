// Ghidra inferred pseudocode; requested=0x305c2b8
// entry=0305c2b8 end=0305c3cb

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0305c2b8(undefined8 *param_1)

{
  undefined8 uVar1;
  size_t sVar2;
  undefined8 *puVar3;
  ulong uVar4;
  
  uVar1 = _DAT_088a4f40;
  param_1[1] = _UNK_088a4f48;
  *param_1 = uVar1;
  param_1[2] = DAT_088a4f28;
  puVar3 = param_1 + 3;
  if ((DAT_0a3d5a2d & 1) == 0) {
    uVar4 = 0;
    do {
      (&DAT_0a3d5a0c)[uVar4] = (&DAT_088a61ea)[uVar4] + 0x8a ^ (&DAT_088a61da)[uVar4 & 0xf];
      uVar4 = uVar4 + 1;
    } while (uVar4 != 0x21);
    DAT_0a3d5a2d = 1;
  }
  sVar2 = _strlen(&DAT_0a3d5a0c);
  if (0x7ffffffffffffff7 < sVar2) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(puVar3);
  }
  if (sVar2 < 0x17) {
    *(char *)((long)param_1 + 0x2f) = (char)sVar2;
    if (sVar2 == 0) goto LAB_0305c3a8;
  }
  else {
    uVar4 = 0x19;
    if ((sVar2 | 7) != 0x17) {
      uVar4 = (sVar2 | 7) + 1;
    }
    puVar3 = (undefined8 *)__Znwm(uVar4);
    param_1[4] = sVar2;
    param_1[5] = uVar4 | 0x8000000000000000;
    param_1[3] = puVar3;
  }
  _memcpy(puVar3,&DAT_0a3d5a0c,sVar2);
LAB_0305c3a8:
  *(undefined1 *)((long)puVar3 + sVar2) = 0;
  *(undefined1 *)(param_1 + 6) = 1;
  return;
}


