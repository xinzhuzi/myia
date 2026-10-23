// Ghidra inferred pseudocode; requested=0x4bb3974
// entry=04bb3974 end=04bb3a87

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

bool FUN_04bb3974(long *param_1)

{
  void *pvVar1;
  long *plVar2;
  byte bVar3;
  char cVar4;
  bool bVar5;
  int iVar6;
  size_t sVar7;
  long *plVar8;
  void *pvVar9;
  void *pvVar10;
  ulong uVar11;
  
  bVar3 = *(byte *)((long)param_1 + 0x17);
  uVar11 = param_1[1];
  if (-1 < (char)bVar3) {
    uVar11 = (ulong)bVar3;
  }
  if (uVar11 == 0) {
    bVar5 = false;
  }
  else {
    if ((DAT_0a4a56ca & 1) == 0) {
      _DAT_0a4a56c0 = s__chatroo_085051b0._0_8_;
      DAT_0a4a56c8 = 0x6d;
      DAT_0a4a56ca = 1;
    }
    plVar2 = (long *)*param_1;
    if (-1 < (char)bVar3) {
      plVar2 = param_1;
    }
    sVar7 = _strlen(&DAT_0a4a56c0);
    if (sVar7 == 0) {
      bVar5 = true;
    }
    else {
      pvVar1 = (void *)((long)plVar2 + uVar11);
      pvVar10 = pvVar1;
      if ((long)sVar7 <= (long)uVar11) {
        cVar4 = DAT_0a4a56c0;
        plVar8 = plVar2;
        do {
          pvVar10 = pvVar1;
          if (((0xfffffffffffffffe < uVar11 - sVar7) ||
              (pvVar9 = _memchr(plVar8,(int)cVar4,(uVar11 - sVar7) + 1), pvVar9 == (void *)0x0)) ||
             (iVar6 = _memcmp(pvVar9,&DAT_0a4a56c0,sVar7), pvVar10 = pvVar9, iVar6 == 0)) break;
          plVar8 = (long *)((long)pvVar9 + 1);
          uVar11 = (long)pvVar1 - (long)plVar8;
          pvVar10 = pvVar1;
        } while ((long)sVar7 <= (long)uVar11);
      }
      bVar5 = pvVar10 != pvVar1 && (long)pvVar10 - (long)plVar2 != -1;
    }
  }
  return bVar5;
}


