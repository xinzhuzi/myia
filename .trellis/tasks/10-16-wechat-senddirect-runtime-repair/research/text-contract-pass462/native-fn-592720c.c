// Ghidra inferred pseudocode; requested=0x592720c
// entry=0592720c end=05927453

undefined4 FUN_0592720c(long param_1,char *param_2,uint param_3,uint param_4,code *param_5)

{
  undefined4 uVar1;
  int iVar2;
  int iVar3;
  size_t sVar4;
  void *pvVar5;
  uint uVar6;
  uint uVar7;
  char *pcVar8;
  ushort uVar9;
  long lVar10;
  int iVar11;
  ushort uVar12;
  
  if (param_2 == (char *)0x0) {
    if ((*(ushort *)(param_1 + 8) & 0x2400) == 0) {
      *(undefined2 *)(param_1 + 8) = 1;
      return 0;
    }
    FUN_05926da4(param_1);
    return 0;
  }
  lVar10 = *(long *)(param_1 + 0x28);
  if (lVar10 == 0) {
    iVar11 = 1000000000;
  }
  else {
    iVar11 = *(int *)(lVar10 + 0x7c);
  }
  uVar6 = 0x10;
  if (param_4 != 0) {
    uVar6 = 2;
  }
  uVar12 = (ushort)uVar6;
  if ((int)param_3 < 0) {
    if (param_4 == 1) {
      sVar4 = _strlen(param_2);
      param_3 = (uint)sVar4 & 0x7fffffff;
      if (iVar11 < (int)param_3) {
        param_3 = iVar11 + 1;
      }
    }
    else {
      param_3 = 0;
      if (-1 < iVar11) {
        pcVar8 = param_2 + 1;
        do {
          if (*pcVar8 == '\0' && pcVar8[-1] == '\0') break;
          pcVar8 = pcVar8 + 2;
          param_3 = param_3 + 2;
        } while ((int)param_3 <= iVar11);
      }
    }
    uVar6 = uVar6 | 0x200;
    uVar12 = (ushort)uVar6;
  }
  if (param_5 == (code *)0xffffffffffffffff) {
    uVar12 = (ushort)uVar6;
    uVar7 = 1;
    if (param_4 != 1) {
      uVar7 = 2;
    }
    if (iVar11 < (int)param_3) {
      return 0x12;
    }
    iVar3 = (uVar7 & (int)(uVar6 << 0x16) >> 0x1f) + param_3;
    iVar2 = iVar3;
    if (iVar3 < 0x21) {
      iVar2 = 0x20;
    }
    if (*(int *)(param_1 + 0x20) < iVar2) {
      iVar2 = FUN_059262e4(param_1,iVar2,0);
      if (iVar2 != 0) {
        return 7;
      }
      pvVar5 = *(void **)(param_1 + 0x10);
    }
    else {
      pvVar5 = *(void **)(param_1 + 0x18);
      *(void **)(param_1 + 0x10) = pvVar5;
      *(ushort *)(param_1 + 8) = *(ushort *)(param_1 + 8) & 0xd;
    }
    _memcpy(pvVar5,param_2,(long)iVar3);
  }
  else if (param_5 == FUN_058dffa4) {
    if (((*(ushort *)(param_1 + 8) & 0x2400) != 0) || (*(int *)(param_1 + 0x20) != 0)) {
      FUN_0592689c(param_1);
      lVar10 = *(long *)(param_1 + 0x28);
    }
    *(char **)(param_1 + 0x10) = param_2;
    *(char **)(param_1 + 0x18) = param_2;
    uVar1 = FUN_058dffb4(lVar10,param_2);
    *(undefined4 *)(param_1 + 0x20) = uVar1;
  }
  else {
    if (((*(ushort *)(param_1 + 8) & 0x2400) != 0) || (*(int *)(param_1 + 0x20) != 0)) {
      FUN_0592689c(param_1);
    }
    *(char **)(param_1 + 0x10) = param_2;
    *(code **)(param_1 + 0x30) = param_5;
    uVar9 = 0x800;
    if (param_5 != (code *)0x0) {
      uVar9 = 0x400;
    }
    uVar12 = uVar12 | uVar9;
  }
  *(uint *)(param_1 + 0xc) = param_3;
  *(ushort *)(param_1 + 8) = uVar12;
  uVar6 = param_4;
  if (param_4 < 2) {
    uVar6 = 1;
  }
  *(char *)(param_1 + 10) = (char)uVar6;
  if ((1 < param_4) && (iVar3 = FUN_059145b4(param_1), iVar3 != 0)) {
    return 7;
  }
  if ((int)param_3 <= iVar11) {
    return 0;
  }
  return 0x12;
}


