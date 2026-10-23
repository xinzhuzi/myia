// Ghidra inferred pseudocode; requested=0x4bb4a4c
// entry=04bb4a4c end=04bb4c57

/* WARNING: Type propagation algorithm not settling */

undefined8 FUN_04bb4a4c(undefined8 param_1)

{
  size_t sVar1;
  undefined8 *******pppppppuVar2;
  ulong uVar3;
  undefined8 uVar4;
  undefined1 **ppuVar5;
  undefined1 **ppuVar6;
  undefined1 *local_70;
  size_t local_68;
  undefined8 local_60;
  undefined8 *******local_58;
  size_t local_50;
  undefined8 local_48;
  
  ppuVar5 = &local_70;
  ppuVar6 = &local_70;
  if ((DAT_0a4a574a & 1) == 0) {
    DAT_0a4a5744 = (undefined4)DAT_08ac3920;
    DAT_0a4a5748 = 0x75;
    DAT_0a4a574a = 1;
  }
  sVar1 = _strlen((char *)&DAT_0a4a5744);
  if (0x7ffffffffffffff7 < sVar1) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_58);
  }
  if (sVar1 < 0x17) {
    local_48 = CONCAT17((char)sVar1,(undefined7)local_48);
    pppppppuVar2 = &local_58;
    if (sVar1 != 0) goto LAB_04bb4af8;
  }
  else {
    uVar3 = 0x19;
    if ((sVar1 | 7) != 0x17) {
      uVar3 = (sVar1 | 7) + 1;
    }
    pppppppuVar2 = (undefined8 *******)__Znwm(uVar3);
    local_48 = uVar3 | 0x8000000000000000;
    local_58 = pppppppuVar2;
    local_50 = sVar1;
LAB_04bb4af8:
    _memcpy(pppppppuVar2,&DAT_0a4a5744,sVar1);
  }
  *(undefined1 *)((long)pppppppuVar2 + sVar1) = 0;
  uVar3 = FUN_066881c4(param_1,&local_58);
  if ((uVar3 & 1) != 0) {
    uVar4 = 1;
    goto joined_r0x04bb4c40;
  }
  if ((DAT_0a4a5752 & 1) == 0) {
    DAT_0a4a574c = (undefined4)DAT_08ac3920;
    DAT_0a4a5750 = 0x67;
    DAT_0a4a5752 = 1;
  }
  sVar1 = _strlen((char *)&DAT_0a4a574c);
  if (0x7ffffffffffffff7 < sVar1) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_70);
  }
  if (sVar1 < 0x17) {
    local_60 = CONCAT17((char)sVar1,(undefined7)local_60);
    if (sVar1 != 0) goto LAB_04bb4bd4;
  }
  else {
    uVar3 = 0x19;
    if ((sVar1 | 7) != 0x17) {
      uVar3 = (sVar1 | 7) + 1;
    }
    ppuVar5 = (undefined1 **)__Znwm(uVar3);
    local_60 = uVar3 | 0x8000000000000000;
    local_70 = (undefined1 *)ppuVar5;
    local_68 = sVar1;
LAB_04bb4bd4:
    _memcpy(ppuVar5,&DAT_0a4a574c,sVar1);
    ppuVar6 = ppuVar5;
  }
  *(undefined1 *)((long)ppuVar6 + sVar1) = 0;
  uVar4 = FUN_066881c4(param_1,&local_70);
  if ((long)local_60 < 0) {
    __ZdlPvm(local_70,local_60 & 0x7fffffffffffffff);
  }
joined_r0x04bb4c40:
  if ((long)local_48 < 0) {
    __ZdlPvm(local_58,local_48 & 0x7fffffffffffffff);
  }
  return uVar4;
}


