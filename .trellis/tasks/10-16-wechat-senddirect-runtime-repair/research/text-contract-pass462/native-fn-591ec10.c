// Ghidra inferred pseudocode; requested=0x591ec10
// entry=0591ec10 end=0591ef2b

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_0591ec10(long *param_1,uint param_2)

{
  uint uVar1;
  undefined8 uVar2;
  undefined1 *puVar3;
  long lVar4;
  
  if (param_1 == (long *)0x0) {
    if ((DAT_0a4f1474 & 1) == 0) {
      _DAT_0a4f144c = CONCAT44((int)DAT_0848e640,(int)DAT_08b77d78);
      uRam000000000a4f1454 = CONCAT44((int)DAT_084d87b0,(int)DAT_084f6208);
      _DAT_0a4f145c = CONCAT44((int)DAT_08563470,(int)ram0x08728640);
      uRam000000000a4f1464 = CONCAT44((int)DAT_0852a960,(int)DAT_08483880);
      DAT_0a4f146c = CONCAT44((int)DAT_084abf00,(int)DAT_08b77d80);
      puVar3 = &DAT_0a4f1474;
LAB_0591ee58:
      *puVar3 = 1;
    }
  }
  else {
    if (*param_1 != 0) {
      FUN_058e178c(*(undefined8 *)(*param_1 + 0x18));
      if ((*(int *)((long)param_1 + 0x24) == 0x2df20da3) && (*(int *)((long)param_1 + 0x34) < 0)) {
        if (((int)param_2 < 1) || ((int)(short)param_1[4] < (int)param_2)) {
          uVar2 = 0x19;
          FUN_0591472c(*param_1,0x19);
          FUN_058e17a4(*(undefined8 *)(*param_1 + 0x18));
        }
        else {
          lVar4 = param_1[0x10] + (ulong)(param_2 - 1) * 0x38;
          FUN_0592687c(lVar4);
          *(undefined2 *)(lVar4 + 8) = 1;
          *(undefined4 *)(*param_1 + 0x50) = 0;
          if (*(uint *)((long)param_1 + 0x11c) != 0) {
            uVar1 = 0x80000000;
            if (param_2 < 0x20) {
              uVar1 = 1 << (ulong)(param_2 - 1 & 0x1f);
            }
            if ((*(uint *)((long)param_1 + 0x11c) & uVar1) != 0) {
              *(ushort *)((long)param_1 + 0xc5) = *(ushort *)((long)param_1 + 0xc5) & 0xfffc | 1;
              return 0;
            }
          }
          uVar2 = 0;
        }
        return uVar2;
      }
      FUN_0591472c(*param_1,0x15);
      FUN_058e17a4(*(undefined8 *)(*param_1 + 0x18));
      if ((DAT_0a4f14a0 & 1) == 0) {
        _DAT_0a4f1478 = CONCAT44((int)DAT_084fc108,(int)DAT_0861ce38);
        uRam000000000a4f1480 = CONCAT44((int)DAT_08b77d90,(int)DAT_08b77d88);
        _DAT_0a4f1488 = CONCAT44((int)DAT_08530658,(int)DAT_0884db28);
        uRam000000000a4f1490 = CONCAT44((int)DAT_08480950,(int)ram0x084897a0);
        DAT_0a4f1498 = CONCAT44((int)DAT_08a2c928,(int)DAT_08b77d98);
        DAT_0a4f14a0 = 1;
      }
      FUN_058ffdcc(0x15,&DAT_0a4f1478);
      uVar2 = 0x509;
      goto LAB_0591ee6c;
    }
    if ((DAT_0a4f1449 & 1) == 0) {
      _DAT_0a4f141c = CONCAT44((int)DAT_0848e640,(int)DAT_08b77d78);
      uRam000000000a4f1424 = CONCAT44((int)DAT_084d87b0,(int)DAT_084f6208);
      _DAT_0a4f142c = CONCAT44((int)ram0x08484500,(int)DAT_086e61e8);
      uRam000000000a4f1434 = CONCAT44((int)DAT_087e2df0,(int)DAT_087715c8);
      DAT_0a4f143c = CONCAT44((int)DAT_0848b6b0,(int)DAT_0857ba08);
      DAT_0a4f1444 = (undefined4)DAT_08483220;
      DAT_0a4f1448 = 0;
      puVar3 = &DAT_0a4f1449;
      goto LAB_0591ee58;
    }
  }
  FUN_058ffdcc(0x15);
  uVar2 = 0x501;
LAB_0591ee6c:
  uVar2 = FUN_058d8f5c(uVar2);
  return uVar2;
}


