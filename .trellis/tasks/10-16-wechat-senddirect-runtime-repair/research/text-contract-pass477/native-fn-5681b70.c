// Ghidra inferred pseudocode; requested=0x5681b70
// entry=05681b70 end=05681ccf

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_05681b70(long param_1,undefined8 param_2,undefined8 param_3)

{
  int iVar1;
  int iVar2;
  long lVar3;
  undefined1 auStack_58 [24];
  
  iVar2 = (int)param_3;
  if (*(int *)(param_1 + 100) == iVar2) {
    if ((DAT_0a4d7606 & 1) == 0) {
      _DAT_0a4d75e8 = CONCAT44((int)DAT_08480a60,(int)DAT_084e6be8);
      uRam000000000a4d75f0 = CONCAT44((int)DAT_08b2ecf0,(int)DAT_084a2f10);
      DAT_0a4d75f8 = CONCAT44((int)DAT_084838a8,(int)DAT_08532300);
      DAT_0a4d7600 = (undefined4)DAT_08489848;
      DAT_0a4d7604 = 0x65;
      DAT_0a4d7606 = 1;
    }
    FUN_0562fcc8(auStack_58,&DAT_0a4d75e8);
    FUN_05625c80(auStack_58);
    FUN_0562fd84(auStack_58);
  }
  else {
    for (lVar3 = *(long *)(param_1 + 0x38); lVar3 != param_1 + 0x30; lVar3 = *(long *)(lVar3 + 8)) {
      iVar1 = FUN_056a1608(lVar3 + 0x10);
      if (iVar2 <= iVar1) {
        (**(code **)(*(long *)(lVar3 + 0x10) + 0x58))(lVar3 + 0x10,param_2,param_3);
      }
    }
    FUN_05698f30(param_1);
    iVar1 = FUN_056a1608();
    if (iVar2 <= iVar1) {
      FUN_0569910c(param_1,param_2,param_3);
      return;
    }
  }
  return;
}


