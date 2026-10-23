// Ghidra inferred pseudocode; requested=0x4bb3c60
// entry=04bb3c60 end=04bb3e07

undefined8 FUN_04bb3c60(undefined8 *param_1)

{
  ulong uVar1;
  byte bVar2;
  int iVar3;
  size_t sVar4;
  undefined8 *puVar5;
  undefined8 ******ppppppuVar6;
  undefined8 uVar7;
  size_t sVar8;
  undefined8 *****local_48;
  size_t local_40;
  undefined8 local_38;
  
  bVar2 = *(byte *)((long)param_1 + 0x17);
  sVar8 = param_1[1];
  sVar4 = sVar8;
  if (-1 < (char)bVar2) {
    sVar4 = (ulong)bVar2;
  }
  if (sVar4 == 0) {
    return 0;
  }
  if ((DAT_0a4a553f & 1) == 0) {
    DAT_0a4a5538 = (undefined4)DAT_08575b00;
    DAT_0a4a553c = 0x6e69;
    DAT_0a4a553e = 0;
    DAT_0a4a553f = 1;
  }
  sVar4 = _strlen((char *)&DAT_0a4a5538);
  if ((char)bVar2 < '\0') {
    if (sVar4 == sVar8) {
      if (sVar8 == 0xffffffffffffffff) {
                    /* WARNING: Subroutine does not return */
        FUN_0020edd0(param_1);
      }
      puVar5 = (undefined8 *)*param_1;
      goto LAB_04bb3d04;
    }
  }
  else {
    puVar5 = param_1;
    if (sVar4 == bVar2) {
LAB_04bb3d04:
      iVar3 = _memcmp(puVar5,&DAT_0a4a5538,sVar4);
      if (iVar3 == 0) {
        return 0;
      }
    }
  }
  if ((DAT_0a4a5451 & 1) == 0) {
    DAT_0a4a544c = (undefined4)DAT_084b0240;
    DAT_0a4a5450 = 0;
    DAT_0a4a5451 = 1;
  }
  sVar4 = _strlen((char *)&DAT_0a4a544c);
  if (0x7ffffffffffffff7 < sVar4) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_48);
  }
  if (sVar4 < 0x17) {
    local_38 = CONCAT17((char)sVar4,(undefined7)local_38);
    ppppppuVar6 = &local_48;
    if (sVar4 == 0) goto LAB_04bb3db0;
  }
  else {
    uVar1 = 0x19;
    if ((sVar4 | 7) != 0x17) {
      uVar1 = (sVar4 | 7) + 1;
    }
    ppppppuVar6 = (undefined8 ******)__Znwm(uVar1);
    local_38 = uVar1 | 0x8000000000000000;
    local_48 = ppppppuVar6;
    local_40 = sVar4;
  }
  _memcpy(ppppppuVar6,&DAT_0a4a544c,sVar4);
LAB_04bb3db0:
  *(undefined1 *)((long)ppppppuVar6 + sVar4) = 0;
  uVar7 = FUN_066881c4(param_1,&local_48);
  if ((long)local_38 < 0) {
    __ZdlPvm(local_48,local_38 & 0x7fffffffffffffff);
  }
  return uVar7;
}


