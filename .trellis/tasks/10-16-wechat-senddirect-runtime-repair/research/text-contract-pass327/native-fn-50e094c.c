// Ghidra inferred pseudocode; requested=0x50e094c
// entry=050e094c end=050e0d23

/* WARNING: Type propagation algorithm not settling */

void FUN_050e094c(long param_1,long param_2)

{
  undefined4 uVar1;
  byte bVar2;
  uint3 uVar3;
  undefined8 uVar4;
  long lVar5;
  undefined8 *puVar6;
  long lVar7;
  uint uVar8;
  ulong uVar9;
  undefined4 uVar10;
  undefined1 uStack_61;
  undefined1 auStack_60 [48];
  
  if (param_2 == param_1) {
    if ((DAT_0a4c2819 & 1) == 0) {
      uVar9 = 0;
      do {
        uVar10 = *(undefined4 *)((long)&DAT_08b054e4 + uVar9);
        uVar3 = CONCAT12((char)((uint)uVar10 >> 8),(short)uVar10) & 0xff00ff;
        uVar1 = *(undefined4 *)((long)&DAT_08b054d0 + uVar9 % 0x14);
        *(uint *)((long)&DAT_0a4c27a3 + uVar9) =
             CONCAT13((char)((uint)uVar10 >> 0x18) + 0x8aU ^ (byte)((uint)uVar1 >> 0x18),
                      CONCAT12((char)((uint)uVar10 >> 0x10) + 0x8aU ^ (byte)((uint)uVar1 >> 0x10),
                               CONCAT11((char)(uVar3 >> 0x10) + 0x8aU ^ (byte)((uint)uVar1 >> 8),
                                        (char)uVar3 + 0x8aU ^ (byte)uVar1)));
        uVar9 = uVar9 + 4;
      } while (uVar9 != 0x74);
      DAT_0a4c2817 = 99;
      DAT_0a4c2819 = 1;
    }
    FUN_05ab442c(auStack_60,3,&DAT_0a4c27a3,
                 "wechat/.conan/data/mmmojo-mac/0.0.0.9/wechat-desktop/stable/package/5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9/Frameworks"
                );
    if ((DAT_0a4c283c & 1) == 0) {
      uVar9 = 0;
      do {
        (&DAT_0a4c281a)[uVar9] = (&DAT_08b0555a)[uVar9 & 0xf] ^ (&DAT_08b0556a)[uVar9];
        uVar9 = uVar9 + 1;
      } while (uVar9 != 0x22);
      DAT_0a4c283c = 1;
    }
    uVar4 = FUN_05ab4444(auStack_60,&DAT_0a4c281a);
    FUN_05ab4574(&uStack_61,uVar4);
    FUN_05ab457c(auStack_60);
    bVar2 = *(byte *)(param_2 + 0x38);
  }
  else {
    bVar2 = *(byte *)(param_2 + 0x38);
  }
  if (bVar2 != 0) {
    uVar8 = (uint)bVar2;
    if ((bVar2 & 1) != 0) {
      *(uint *)(param_1 + 0x38) = *(uint *)(param_1 + 0x38) | 1;
      lVar5 = *(long *)(param_1 + 8);
      if (lVar5 == 0) {
        lVar5 = __Znwm(0x20);
        FUN_0465b0bc();
        *(long *)(param_1 + 8) = lVar5;
        lVar7 = *(long *)(param_2 + 8);
      }
      else {
        lVar7 = *(long *)(param_2 + 8);
      }
      if (lVar7 == 0) {
        lVar7 = *(long *)(DAT_0a520ca0 + 8);
      }
      FUN_0465b0d4(lVar5,lVar7);
      uVar8 = *(uint *)(param_2 + 0x38);
    }
    if ((uVar8 >> 1 & 1) != 0) {
      uVar1 = *(undefined4 *)(param_2 + 0x30);
      *(uint *)(param_1 + 0x38) = *(uint *)(param_1 + 0x38) | 2;
      *(undefined4 *)(param_1 + 0x30) = uVar1;
      uVar8 = *(uint *)(param_2 + 0x38);
    }
    if ((uVar8 >> 2 & 1) != 0) {
      *(uint *)(param_1 + 0x38) = *(uint *)(param_1 + 0x38) | 4;
      puVar6 = *(undefined8 **)(param_1 + 0x10);
      if (puVar6 == (undefined8 *)0x0) {
        puVar6 = (undefined8 *)__Znwm(200);
        *puVar6 = &PTR_FUN_09edc180;
        puVar6[2] = 0;
        puVar6[1] = 0;
        puVar6[4] = 0;
        puVar6[3] = 0;
        puVar6[6] = 0;
        puVar6[5] = 0;
        puVar6[8] = 0;
        puVar6[7] = 0;
        *(undefined8 *)((long)puVar6 + 0x4c) = 0;
        *(undefined8 *)((long)puVar6 + 0x44) = 0;
        puVar6[0xb] = &DAT_0a524ad0;
        puVar6[0xc] = 0;
        puVar6[0xd] = &DAT_0a524ad0;
        puVar6[0xe] = 0;
        puVar6[0xf] = &DAT_0a524ad0;
        *(undefined4 *)((long)puVar6 + 0x54) = 0;
        puVar6[0x10] = 0;
        puVar6[0x11] = &DAT_0a524ad0;
        *(undefined8 *)((long)puVar6 + 0xbc) = 0;
        puVar6[0x13] = 0;
        puVar6[0x12] = 0;
        puVar6[0x15] = 0;
        puVar6[0x14] = 0;
        *(undefined8 *)((long)puVar6 + 0xb4) = 0;
        *(undefined8 *)((long)puVar6 + 0xac) = 0;
        *(undefined8 **)(param_1 + 0x10) = puVar6;
        lVar5 = *(long *)(param_2 + 0x10);
      }
      else {
        lVar5 = *(long *)(param_2 + 0x10);
      }
      if (lVar5 == 0) {
        lVar5 = *(long *)(DAT_0a520ca0 + 0x10);
      }
      FUN_050d9ca8(puVar6,lVar5);
      uVar8 = *(uint *)(param_2 + 0x38);
    }
    if ((uVar8 >> 3 & 1) != 0) {
      *(uint *)(param_1 + 0x38) = *(uint *)(param_1 + 0x38) | 8;
      puVar6 = *(undefined8 **)(param_1 + 0x18);
      if (puVar6 == (undefined8 *)0x0) {
        puVar6 = (undefined8 *)__Znwm(0x90);
        *puVar6 = &PTR_FUN_09edc1f8;
        puVar6[1] = &DAT_0a524ad0;
        puVar6[2] = &DAT_0a524ad0;
        puVar6[3] = 0;
        puVar6[4] = &DAT_0a524ad0;
        puVar6[5] = &DAT_0a524ad0;
        puVar6[6] = &DAT_0a524ad0;
        puVar6[7] = 0;
        puVar6[8] = &DAT_0a524ad0;
        puVar6[9] = 0;
        puVar6[10] = &DAT_0a524ad0;
        puVar6[0xb] = &DAT_0a524ad0;
        puVar6[0xc] = &DAT_0a524ad0;
        puVar6[0xd] = 0;
        puVar6[0x10] = 0;
        puVar6[0x11] = 0;
        puVar6[0xe] = &DAT_0a524ad0;
        puVar6[0xf] = 0;
        *(undefined8 **)(param_1 + 0x18) = puVar6;
        lVar5 = *(long *)(param_2 + 0x18);
      }
      else {
        lVar5 = *(long *)(param_2 + 0x18);
      }
      if (lVar5 == 0) {
        lVar5 = *(long *)(DAT_0a520ca0 + 0x18);
      }
      FUN_050dce34(puVar6,lVar5);
      uVar8 = *(uint *)(param_2 + 0x38);
    }
    if ((uVar8 >> 4 & 1) != 0) {
      *(uint *)(param_1 + 0x38) = *(uint *)(param_1 + 0x38) | 0x10;
      puVar6 = *(undefined8 **)(param_1 + 0x20);
      if (puVar6 == (undefined8 *)0x0) {
        puVar6 = (undefined8 *)__Znwm(0x40);
        *puVar6 = &PTR_FUN_09edc108;
        puVar6[2] = 0;
        puVar6[1] = 0;
        puVar6[4] = 0;
        puVar6[3] = 0;
        puVar6[6] = 0;
        puVar6[5] = 0;
        *(undefined4 *)(puVar6 + 7) = 0;
        *(undefined8 **)(param_1 + 0x20) = puVar6;
        lVar5 = *(long *)(param_2 + 0x20);
      }
      else {
        lVar5 = *(long *)(param_2 + 0x20);
      }
      if (lVar5 == 0) {
        lVar5 = *(long *)(DAT_0a520ca0 + 0x20);
      }
      FUN_050d8bb4(puVar6,lVar5);
      uVar8 = *(uint *)(param_2 + 0x38);
    }
    if ((uVar8 >> 5 & 1) != 0) {
      *(uint *)(param_1 + 0x38) = *(uint *)(param_1 + 0x38) | 0x20;
      puVar6 = *(undefined8 **)(param_1 + 0x28);
      if (puVar6 == (undefined8 *)0x0) {
        puVar6 = (undefined8 *)__Znwm(0x38);
        puVar6[1] = 0;
        puVar6[2] = 0;
        *puVar6 = &PTR_FUN_09edc270;
        *(undefined4 *)(puVar6 + 3) = 0;
        puVar6[4] = 0;
        puVar6[5] = 0;
        *(undefined4 *)(puVar6 + 6) = 0;
        *(undefined8 **)(param_1 + 0x28) = puVar6;
        lVar5 = *(long *)(param_2 + 0x28);
      }
      else {
        lVar5 = *(long *)(param_2 + 0x28);
      }
      if (lVar5 == 0) {
        lVar5 = *(long *)(DAT_0a520ca0 + 0x28);
      }
      FUN_050defec(puVar6,lVar5);
    }
  }
  return;
}


