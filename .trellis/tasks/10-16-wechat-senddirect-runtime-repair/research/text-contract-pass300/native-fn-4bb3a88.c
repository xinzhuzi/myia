// Ghidra inferred pseudocode; requested=0x4bb3a88
// entry=04bb3a88 end=04bb3ba3

bool FUN_04bb3a88(long *param_1)

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
    if ((DAT_0a4a5735 & 1) == 0) {
      DAT_0a4a5728 = s__im_chat_strange_lbsroom_groupca_08ac38d0._0_8_;
      DAT_0a4a5730 = (undefined4)DAT_084f5b38;
      DAT_0a4a5734 = 0;
      DAT_0a4a5735 = 1;
    }
    plVar2 = (long *)*param_1;
    if (-1 < (char)bVar3) {
      plVar2 = param_1;
    }
    sVar7 = _strlen((char *)&DAT_0a4a5728);
    if (sVar7 == 0) {
      bVar5 = true;
    }
    else {
      pvVar1 = (void *)((long)plVar2 + uVar11);
      pvVar10 = pvVar1;
      if ((long)sVar7 <= (long)uVar11) {
        cVar4 = (char)DAT_0a4a5728;
        plVar8 = plVar2;
        do {
          pvVar10 = pvVar1;
          if (((0xfffffffffffffffe < uVar11 - sVar7) ||
              (pvVar9 = _memchr(plVar8,(int)cVar4,(uVar11 - sVar7) + 1), pvVar9 == (void *)0x0)) ||
             (iVar6 = _memcmp(pvVar9,&DAT_0a4a5728,sVar7), pvVar10 = pvVar9, iVar6 == 0)) break;
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


