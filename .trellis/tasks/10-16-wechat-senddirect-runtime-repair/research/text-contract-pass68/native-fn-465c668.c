// Ghidra inferred pseudocode; requested=0x465c668
// entry=0465c668 end=0465c943

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0465c668(long param_1,long param_2)

{
  byte bVar1;
  uint3 uVar2;
  long lVar3;
  undefined8 *puVar4;
  long lVar5;
  uint uVar6;
  ulong uVar7;
  undefined8 uVar8;
  undefined4 uVar9;
  undefined4 uVar10;
  undefined1 uStack_61;
  undefined1 auStack_60 [48];
  
  if (param_2 == param_1) {
    if ((DAT_0a45dd0b & 1) == 0) {
      uVar7 = 0;
      do {
        uVar9 = *(undefined4 *)((long)&DAT_08a12e24 + uVar7);
        uVar2 = CONCAT12((char)((uint)uVar9 >> 8),(short)uVar9) & 0xff00ff;
        uVar10 = *(undefined4 *)((long)&DAT_08a12e10 + uVar7 % 0x14);
        *(uint *)((long)&DAT_0a45dca3 + uVar7) =
             CONCAT13((char)((uint)uVar9 >> 0x18) + 0x8aU ^ (byte)((uint)uVar10 >> 0x18),
                      CONCAT12((char)((uint)uVar9 >> 0x10) + 0x8aU ^ (byte)((uint)uVar10 >> 0x10),
                               CONCAT11((char)(uVar2 >> 0x10) + 0x8aU ^ (byte)((uint)uVar10 >> 8),
                                        (char)uVar2 + 0x8aU ^ (byte)uVar10)));
        uVar7 = uVar7 + 4;
      } while (uVar7 != 0x68);
      DAT_0a45dd0b = 1;
    }
    FUN_05ab442c(auStack_60,3,&DAT_0a45dca3,0x277);
    if ((DAT_0a45dd2e & 1) == 0) {
      _DAT_0a45dd0c = CONCAT44((int)DAT_08a12ad0,(int)DAT_08a12ac8);
      uRam000000000a45dd14 = CONCAT44((int)DAT_08a12ad8,(int)ram0x08480938);
      _DAT_0a45dd1c = CONCAT44((int)DAT_08a12ae0,(int)DAT_084d7818);
      uRam000000000a45dd24 = CONCAT44((int)DAT_08a12af0,(int)DAT_08a12ae8);
      DAT_0a45dd2c = 0x20;
      DAT_0a45dd2e = 1;
    }
    uVar8 = FUN_05ab4444(auStack_60,&DAT_0a45dd0c);
    FUN_05ab4574(&uStack_61,uVar8);
    FUN_05ab457c(auStack_60);
    bVar1 = *(byte *)(param_2 + 0x34);
  }
  else {
    bVar1 = *(byte *)(param_2 + 0x34);
  }
  if (bVar1 != 0) {
    uVar6 = (uint)bVar1;
    if ((bVar1 & 1) != 0) {
      *(uint *)(param_1 + 0x34) = *(uint *)(param_1 + 0x34) | 1;
      lVar3 = *(long *)(param_1 + 8);
      if (lVar3 == 0) {
        lVar3 = __Znwm(0x18);
        FUN_04f33c00();
        *(long *)(param_1 + 8) = lVar3;
        lVar5 = *(long *)(param_2 + 8);
      }
      else {
        lVar5 = *(long *)(param_2 + 8);
      }
      if (lVar5 == 0) {
        lVar5 = *(long *)(DAT_0a51ea38 + 8);
      }
      FUN_04f37870(lVar3,lVar5);
      uVar6 = *(uint *)(param_2 + 0x34);
    }
    if ((uVar6 >> 1 & 1) != 0) {
      uVar8 = *(undefined8 *)(param_2 + 0x10);
      *(uint *)(param_1 + 0x34) = *(uint *)(param_1 + 0x34) | 2;
      puVar4 = *(undefined8 **)(param_1 + 0x10);
      if (puVar4 == &DAT_0a524ad0) {
        puVar4 = (undefined8 *)__Znwm(0x18);
        puVar4[1] = 0;
        puVar4[2] = 0;
        *puVar4 = 0;
        *(undefined8 **)(param_1 + 0x10) = puVar4;
      }
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar4,uVar8);
      uVar6 = *(uint *)(param_2 + 0x34);
    }
    if ((uVar6 >> 2 & 1) != 0) {
      uVar9 = *(undefined4 *)(param_2 + 0x18);
      *(uint *)(param_1 + 0x34) = *(uint *)(param_1 + 0x34) | 4;
      *(undefined4 *)(param_1 + 0x18) = uVar9;
      uVar6 = *(uint *)(param_2 + 0x34);
    }
    if ((uVar6 >> 3 & 1) != 0) {
      uVar9 = *(undefined4 *)(param_2 + 0x1c);
      *(uint *)(param_1 + 0x34) = *(uint *)(param_1 + 0x34) | 8;
      *(undefined4 *)(param_1 + 0x1c) = uVar9;
      uVar6 = *(uint *)(param_2 + 0x34);
    }
    if ((uVar6 >> 4 & 1) != 0) {
      uVar9 = *(undefined4 *)(param_2 + 0x28);
      *(uint *)(param_1 + 0x34) = *(uint *)(param_1 + 0x34) | 0x10;
      *(undefined4 *)(param_1 + 0x28) = uVar9;
      uVar6 = *(uint *)(param_2 + 0x34);
    }
    if ((uVar6 >> 5 & 1) != 0) {
      uVar8 = *(undefined8 *)(param_2 + 0x20);
      *(uint *)(param_1 + 0x34) = *(uint *)(param_1 + 0x34) | 0x20;
      puVar4 = *(undefined8 **)(param_1 + 0x20);
      if (puVar4 == &DAT_0a524ad0) {
        puVar4 = (undefined8 *)__Znwm(0x18);
        puVar4[1] = 0;
        puVar4[2] = 0;
        *puVar4 = 0;
        *(undefined8 **)(param_1 + 0x20) = puVar4;
      }
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar4,uVar8);
      uVar6 = *(uint *)(param_2 + 0x34);
    }
    if ((uVar6 >> 6 & 1) != 0) {
      uVar9 = *(undefined4 *)(param_2 + 0x2c);
      *(uint *)(param_1 + 0x34) = *(uint *)(param_1 + 0x34) | 0x40;
      *(undefined4 *)(param_1 + 0x2c) = uVar9;
    }
  }
  return;
}


