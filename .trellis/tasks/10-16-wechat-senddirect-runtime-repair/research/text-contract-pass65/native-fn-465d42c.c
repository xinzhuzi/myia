// Ghidra inferred pseudocode; requested=0x465d42c
// entry=0465d42c end=0465d5af

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0465d42c(long param_1,long param_2)

{
  uint3 uVar1;
  undefined8 uVar2;
  ulong uVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  undefined1 uStack_51;
  undefined1 auStack_50 [48];
  
  if (param_2 == param_1) {
    if ((DAT_0a45dd0b & 1) == 0) {
      uVar3 = 0;
      do {
        uVar4 = *(undefined4 *)((long)&DAT_08a12e24 + uVar3);
        uVar1 = CONCAT12((char)((uint)uVar4 >> 8),(short)uVar4) & 0xff00ff;
        uVar5 = *(undefined4 *)((long)&DAT_08a12e10 + uVar3 % 0x14);
        *(uint *)((long)&DAT_0a45dca3 + uVar3) =
             CONCAT13((char)((uint)uVar4 >> 0x18) + 0x8aU ^ (byte)((uint)uVar5 >> 0x18),
                      CONCAT12((char)((uint)uVar4 >> 0x10) + 0x8aU ^ (byte)((uint)uVar5 >> 0x10),
                               CONCAT11((char)(uVar1 >> 0x10) + 0x8aU ^ (byte)((uint)uVar5 >> 8),
                                        (char)uVar1 + 0x8aU ^ (byte)uVar5)));
        uVar3 = uVar3 + 4;
      } while (uVar3 != 0x68);
      DAT_0a45dd0b = 1;
    }
    FUN_05ab442c(auStack_50,3,&DAT_0a45dca3,0x356);
    if ((DAT_0a45dd2e & 1) == 0) {
      _DAT_0a45dd0c = CONCAT44((int)DAT_08a12ad0,(int)DAT_08a12ac8);
      uRam000000000a45dd14 = CONCAT44((int)DAT_08a12ad8,(int)ram0x08480938);
      _DAT_0a45dd1c = CONCAT44((int)DAT_08a12ae0,(int)DAT_084d7818);
      uRam000000000a45dd24 = CONCAT44((int)DAT_08a12af0,(int)DAT_08a12ae8);
      DAT_0a45dd2c = 0x20;
      DAT_0a45dd2e = 1;
    }
    uVar2 = FUN_05ab4444(auStack_50,&DAT_0a45dd0c);
    FUN_05ab4574(&uStack_51,uVar2);
    FUN_05ab457c(auStack_50);
  }
  FUN_04663a3c(param_1 + 8,param_2 + 8);
  if ((*(byte *)(param_2 + 0x28) & 1) != 0) {
    uVar4 = *(undefined4 *)(param_2 + 0x20);
    *(uint *)(param_1 + 0x28) = *(uint *)(param_1 + 0x28) | 1;
    *(undefined4 *)(param_1 + 0x20) = uVar4;
  }
  return;
}


