// Ghidra inferred pseudocode; requested=0x30c14a4
// entry=030c14a4 end=030c15b7

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_030c14a4(undefined8 *param_1)

{
  undefined8 uVar1;
  size_t sVar2;
  undefined8 *puVar3;
  ulong uVar4;
  
  uVar1 = _DAT_088acd90;
  param_1[1] = _UNK_088acd98;
  *param_1 = uVar1;
  param_1[2] = DAT_088acd88;
  puVar3 = param_1 + 3;
  if ((DAT_0a3d89fd & 1) == 0) {
    uVar4 = 0;
    do {
      (&DAT_0a3d89dc)[uVar4] = (&DAT_088ada2e)[uVar4] + 0x8a ^ (&DAT_088ada1e)[uVar4 & 0xf];
      uVar4 = uVar4 + 1;
    } while (uVar4 != 0x21);
    DAT_0a3d89fd = 1;
  }
  sVar2 = _strlen(&DAT_0a3d89dc);
  if (0x7ffffffffffffff7 < sVar2) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(puVar3);
  }
  if (sVar2 < 0x17) {
    *(char *)((long)param_1 + 0x2f) = (char)sVar2;
    if (sVar2 == 0) goto LAB_030c1594;
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
  _memcpy(puVar3,&DAT_0a3d89dc,sVar2);
LAB_030c1594:
  *(undefined1 *)((long)puVar3 + sVar2) = 0;
  *(undefined1 *)(param_1 + 6) = 1;
  return;
}


