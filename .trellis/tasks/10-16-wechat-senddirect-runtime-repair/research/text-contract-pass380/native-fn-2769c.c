// Ghidra inferred pseudocode; requested=0x2769c
// entry=0002769c end=0002780b

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0002769c(int *param_1)

{
  uint3 uVar1;
  int iVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  ulong uVar5;
  undefined4 uVar6;
  undefined4 uVar7;
  undefined1 auStack_30 [8];
  long local_28;
  
  iVar2 = *param_1;
  *param_1 = iVar2 + 1;
  if ((DAT_0a24ffef & 1) == 0) {
    _DAT_0a24ffd4 = CONCAT44((int)DAT_08483208,(int)DAT_08483200);
    uRam000000000a24ffdc = CONCAT44((int)DAT_08483218,(int)DAT_08483210);
    DAT_0a24ffe4 = CONCAT44((int)DAT_08483228,(int)DAT_08483220);
    DAT_0a24ffec = 0x3020;
    DAT_0a24ffee = 0;
    DAT_0a24ffef = 1;
  }
  if (iVar2 < 1) {
    uVar3 = FUN_000219f4();
    uVar4 = FUN_000219f4(0);
    FUN_0002239c(&local_28,&DAT_0a24ffd4,uVar3,uVar4);
    if (local_28 != 0) {
      if ((DAT_0a25005a & 1) == 0) {
        uVar5 = 0;
        do {
          uVar6 = *(undefined4 *)((long)&DAT_084837d8 + uVar5);
          uVar1 = CONCAT12((char)((uint)uVar6 >> 8),(short)uVar6) & 0xff00ff;
          uVar7 = *(undefined4 *)((long)&DAT_084837c4 + uVar5 % 0x14);
          *(uint *)((long)&DAT_0a24fff0 + uVar5) =
               CONCAT13((char)((uint)uVar6 >> 0x18) + 0x8aU ^ (byte)((uint)uVar7 >> 0x18),
                        CONCAT12((char)((uint)uVar6 >> 0x10) + 0x8aU ^ (byte)((uint)uVar7 >> 0x10),
                                 CONCAT11((char)(uVar1 >> 0x10) + 0x8aU ^ (byte)((uint)uVar7 >> 8),
                                          (char)uVar1 + 0x8aU ^ (byte)uVar7)));
          uVar5 = uVar5 + 4;
        } while (uVar5 != 0x68);
        DAT_0a250058 = 0x68;
        DAT_0a25005a = 1;
      }
      FUN_000217e4(auStack_30,&DAT_0a24fff0,0xe0,&local_28);
      FUN_0001a86c(auStack_30);
    }
  }
  return;
}


