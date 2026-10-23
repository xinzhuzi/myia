// Ghidra inferred pseudocode; requested=0xd7cf04
// entry=00d7cf04 end=00d7d207

void FUN_00d7cf04(undefined8 *param_1,undefined8 *param_2)

{
  ulong uVar1;
  size_t sVar2;
  undefined1 *puVar3;
  ulong uVar4;
  byte bVar5;
  undefined4 uVar6;
  int iVar7;
  undefined8 uVar8;
  long lVar9;
  undefined8 *puVar10;
  size_t sVar11;
  undefined8 *****pppppuVar12;
  undefined8 *puVar13;
  undefined8 ****local_78;
  undefined1 *local_70;
  undefined1 *local_68;
  
  param_1[1] = &SUB_aaaaaaaaaaaaaaaa;
  *param_1 = &SUB_aaaaaaaaaaaaaaaa;
  param_1[3] = &SUB_aaaaaaaaaaaaaaaa;
  param_1[2] = &SUB_aaaaaaaaaaaaaaaa;
  param_1[3] = 0;
  param_1[4] = &SUB_aaaaaaaaaaaaaaaa;
  *(undefined1 *)param_1 = 0;
  param_1[1] = 0;
  param_1[6] = 0;
  param_1[5] = 0;
  param_1[2] = 0;
  *(undefined4 *)(param_1 + 4) = 0;
  param_1[8] = 0;
  param_1[7] = 0;
  param_1[10] = 0;
  param_1[9] = 0;
  param_1[0xc] = 0;
  param_1[0xb] = 0;
  param_1[0xe] = 0;
  param_1[0xd] = 0;
  param_1[0x10] = 0;
  param_1[0xf] = 0;
  param_1[0x12] = 0;
  param_1[0x11] = 0;
  param_1[0x14] = 0;
  param_1[0x13] = 0;
  param_1[0x16] = 0;
  param_1[0x15] = 0;
  param_1[0x18] = 0;
  param_1[0x17] = 0;
  param_1[0x19] = 0;
  uVar8 = FUN_0001accc(*param_2);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_1 + 5,uVar8);
  uVar8 = FUN_0109d438(*param_2);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_1 + 8,uVar8);
  uVar8 = FUN_00fffbb0(*param_2);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_1 + 1,uVar8);
  lVar9 = FUN_0037a964(*param_2);
  uVar1 = *(ulong *)(lVar9 + 8);
  if (-1 < (char)*(byte *)(lVar9 + 0x17)) {
    uVar1 = (ulong)*(byte *)(lVar9 + 0x17);
  }
  if (uVar1 != 0) {
    uVar8 = FUN_0037a964(*param_2);
    uVar6 = FUN_04b56748(uVar8,0);
    *(undefined4 *)(param_1 + 4) = uVar6;
  }
  lVar9 = FUN_04d1b390(*param_2);
  uVar1 = *(ulong *)(lVar9 + 8);
  if (-1 < (char)*(byte *)(lVar9 + 0x17)) {
    uVar1 = (ulong)*(byte *)(lVar9 + 0x17);
  }
  if (uVar1 != 0) {
    puVar10 = (undefined8 *)FUN_04d1b390(*param_2);
    if ((DAT_0a2c79da & 1) == 0) {
      DAT_0a2c79d8 = 0x20;
      DAT_0a2c79da = 1;
    }
    bVar5 = *(byte *)((long)puVar10 + 0x17);
    sVar2 = puVar10[1];
    if (-1 < (char)bVar5) {
      sVar2 = (ulong)bVar5;
    }
    sVar11 = _strlen((char *)&DAT_0a2c79d8);
    local_78 = (undefined8 ****)&SUB_aaaaaaaaaaaaaaaa;
    local_70 = &SUB_aaaaaaaaaaaaaaaa;
    local_68 = &SUB_aaaaaaaaaaaaaaaa;
    uVar1 = sVar2 + sVar11;
    if (0x7ffffffffffffff7 < uVar1) {
                    /* WARNING: Subroutine does not return */
      FUN_00018d9c(&local_78);
    }
    if (uVar1 < 0x17) {
      local_70 = (undefined1 *)0x0;
      local_78 = (undefined8 *****)0x0;
      pppppuVar12 = &local_78;
      local_68 = (undefined1 *)(uVar1 << 0x38);
    }
    else {
      uVar4 = 0x19;
      if ((uVar1 | 7) != 0x17) {
        uVar4 = (uVar1 | 7) + 1;
      }
      pppppuVar12 = (undefined8 *****)__Znwm(uVar4);
      local_68 = (undefined1 *)(uVar4 | 0x8000000000000000);
      local_70 = (undefined1 *)uVar1;
      local_78 = pppppuVar12;
    }
    if (sVar2 != 0) {
      puVar13 = (void *)*puVar10;
      if (-1 < (char)bVar5) {
        puVar13 = puVar10;
      }
      _memmove(pppppuVar12,puVar13,sVar2);
    }
    if (sVar11 != 0) {
      _memmove((void *)((long)pppppuVar12 + sVar2),&DAT_0a2c79d8,sVar11);
    }
    *(undefined1 *)((long)((long)pppppuVar12 + sVar2) + sVar11) = 0;
    puVar3 = local_70;
    pppppuVar12 = (undefined8 *****)local_78;
    if (-1 < (long)local_68) {
      puVar3 = (undefined1 *)((ulong)local_68 >> 0x38);
      pppppuVar12 = &local_78;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
              (param_1 + 0xb,pppppuVar12,puVar3);
    if ((long)local_68 < 0) {
      __ZdlPvm(local_78,(ulong)local_68 & 0x7fffffffffffffff);
    }
  }
  lVar9 = FUN_02e0a888(*param_2);
  uVar1 = *(ulong *)(lVar9 + 8);
  if (-1 < (char)*(byte *)(lVar9 + 0x17)) {
    uVar1 = (ulong)*(byte *)(lVar9 + 0x17);
  }
  if (uVar1 != 0) {
    puVar13 = (undefined8 *)FUN_02e0a888(*param_2);
    uVar1 = puVar13[1];
    puVar10 = (undefined8 *)*puVar13;
    if (-1 < (char)*(byte *)((long)puVar13 + 0x17)) {
      uVar1 = (ulong)*(byte *)((long)puVar13 + 0x17);
      puVar10 = puVar13;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
              (param_1 + 0xb,puVar10,uVar1);
  }
  iVar7 = FUN_04d1b4ec(*param_2);
  if (iVar7 == 2) {
    *(undefined1 *)param_1 = 1;
    uVar8 = FUN_012ee8e4(*param_2);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_1 + 0xe,uVar8);
    uVar8 = FUN_016449c8(*param_2);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_1 + 0x11,uVar8);
    uVar8 = FUN_04d1b3f0(*param_2);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_1 + 0x14,uVar8);
  }
  return;
}


