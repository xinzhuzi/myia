// Ghidra inferred pseudocode; requested=0x4eae1b8
// entry=04eae1b8 end=04eae84f

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_04eae1b8(long param_1,long param_2)

{
  uint uVar1;
  uint3 uVar2;
  undefined8 uVar3;
  undefined8 *puVar4;
  long lVar5;
  ulong uVar6;
  undefined4 uVar7;
  undefined4 uVar8;
  undefined1 uStack_51;
  undefined1 auStack_50 [48];
  
  if (param_2 == param_1) {
    if ((DAT_0a4b960e & 1) == 0) {
      uVar6 = 0;
      do {
        uVar7 = *(undefined4 *)((long)&DAT_08af1d34 + uVar6);
        uVar2 = CONCAT12((char)((uint)uVar7 >> 8),(short)uVar7) & 0xff00ff;
        uVar8 = *(undefined4 *)((long)&DAT_08af1d20 + uVar6 % 0x14);
        *(uint *)((long)&DAT_0a4b9593 + uVar6) =
             CONCAT13((char)((uint)uVar7 >> 0x18) + 0x8aU ^ (byte)((uint)uVar8 >> 0x18),
                      CONCAT12((char)((uint)uVar7 >> 0x10) + 0x8aU ^ (byte)((uint)uVar8 >> 0x10),
                               CONCAT11((char)(uVar2 >> 0x10) + 0x8aU ^ (byte)((uint)uVar8 >> 8),
                                        (char)uVar2 + 0x8aU ^ (byte)uVar8)));
        uVar6 = uVar6 + 4;
      } while (uVar6 != 0x78);
      DAT_0a4b960b = 0x6363;
      DAT_0a4b960d = 0;
      DAT_0a4b960e = 1;
    }
    FUN_05ab442c(auStack_50,3,&DAT_0a4b9593,
                 "stem/Library/Frameworks/CoreText.framework/Versions/A/CoreText");
    if ((DAT_0a4b9632 & 1) == 0) {
      _DAT_0a4b9610 = CONCAT44((int)DAT_08a12ad0,(int)DAT_08a12ac8);
      uRam000000000a4b9618 = CONCAT44((int)DAT_08a12ad8,(int)ram0x08480938);
      _DAT_0a4b9620 = CONCAT44((int)DAT_08a12ae0,(int)DAT_084d7818);
      uRam000000000a4b9628 = CONCAT44((int)DAT_08a12af0,(int)DAT_08a12ae8);
      DAT_0a4b9630 = 0x20;
      DAT_0a4b9632 = 1;
    }
    uVar3 = FUN_05ab4444(auStack_50,&DAT_0a4b9610);
    FUN_05ab4574(&uStack_51,uVar3);
    FUN_05ab457c(auStack_50);
  }
  uVar1 = *(uint *)(param_2 + 0x74);
  if ((uVar1 & 0xff) != 0) {
    if ((uVar1 & 1) != 0) {
      uVar7 = *(undefined4 *)(param_2 + 8);
      *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 1;
      *(undefined4 *)(param_1 + 8) = uVar7;
      uVar1 = *(uint *)(param_2 + 0x74);
    }
    if ((uVar1 >> 1 & 1) != 0) {
      uVar7 = *(undefined4 *)(param_2 + 0xc);
      *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 2;
      *(undefined4 *)(param_1 + 0xc) = uVar7;
      uVar1 = *(uint *)(param_2 + 0x74);
    }
    if ((uVar1 >> 2 & 1) != 0) {
      *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 4;
      puVar4 = *(undefined8 **)(param_1 + 0x10);
      if (puVar4 == (undefined8 *)0x0) {
        puVar4 = (undefined8 *)__Znwm(0x28);
        *puVar4 = &PTR_FUN_09ec3b98;
        puVar4[1] = 0;
        puVar4[2] = &DAT_0a524ad0;
        puVar4[3] = &DAT_0a524ad0;
        puVar4[4] = 0;
        *(undefined8 **)(param_1 + 0x10) = puVar4;
        lVar5 = *(long *)(param_2 + 0x10);
      }
      else {
        lVar5 = *(long *)(param_2 + 0x10);
      }
      if (lVar5 == 0) {
        lVar5 = *(long *)(DAT_0a51f728 + 0x10);
      }
      FUN_04ea6d78(puVar4,lVar5);
      uVar1 = *(uint *)(param_2 + 0x74);
    }
    if ((uVar1 >> 3 & 1) != 0) {
      *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 8;
      puVar4 = *(undefined8 **)(param_1 + 0x18);
      if (puVar4 == (undefined8 *)0x0) {
        puVar4 = (undefined8 *)__Znwm(0x40);
        puVar4[1] = 0;
        puVar4[2] = 0;
        *puVar4 = &PTR_FUN_09ec3c10;
        *(undefined8 *)((long)puVar4 + 0x15) = 0;
        puVar4[4] = &DAT_0a524ad0;
        puVar4[5] = &DAT_0a524ad0;
        puVar4[6] = 0;
        *(undefined4 *)(puVar4 + 7) = 0;
        *(undefined8 **)(param_1 + 0x18) = puVar4;
        lVar5 = *(long *)(param_2 + 0x18);
      }
      else {
        lVar5 = *(long *)(param_2 + 0x18);
      }
      if (lVar5 == 0) {
        lVar5 = *(long *)(DAT_0a51f728 + 0x18);
      }
      FUN_04ea766c(puVar4,lVar5);
      uVar1 = *(uint *)(param_2 + 0x74);
    }
    if ((uVar1 >> 4 & 1) != 0) {
      *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 0x10;
      puVar4 = *(undefined8 **)(param_1 + 0x20);
      if (puVar4 == (undefined8 *)0x0) {
        puVar4 = (undefined8 *)__Znwm(0x20);
        puVar4[2] = 0;
        *puVar4 = &PTR_FUN_09ec3d78;
        puVar4[1] = &DAT_0a524ad0;
        *(undefined4 *)(puVar4 + 3) = 0;
        *(undefined8 **)(param_1 + 0x20) = puVar4;
        lVar5 = *(long *)(param_2 + 0x20);
      }
      else {
        lVar5 = *(long *)(param_2 + 0x20);
      }
      if (lVar5 == 0) {
        lVar5 = *(long *)(DAT_0a51f728 + 0x20);
      }
      FUN_04ea95e4(puVar4,lVar5);
      uVar1 = *(uint *)(param_2 + 0x74);
    }
    if ((uVar1 >> 5 & 1) != 0) {
      *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 0x20;
      puVar4 = *(undefined8 **)(param_1 + 0x28);
      if (puVar4 == (undefined8 *)0x0) {
        puVar4 = (undefined8 *)__Znwm(0x38);
        puVar4[5] = 0;
        *puVar4 = &PTR_FUN_09ec3df0;
        puVar4[1] = &DAT_0a524ad0;
        puVar4[2] = &DAT_0a524ad0;
        puVar4[3] = &DAT_0a524ad0;
        puVar4[4] = &DAT_0a524ad0;
        *(undefined4 *)(puVar4 + 6) = 0;
        *(undefined8 **)(param_1 + 0x28) = puVar4;
        lVar5 = *(long *)(param_2 + 0x28);
      }
      else {
        lVar5 = *(long *)(param_2 + 0x28);
      }
      if (lVar5 == 0) {
        lVar5 = *(long *)(DAT_0a51f728 + 0x28);
      }
      FUN_04ea9d08(puVar4,lVar5);
      uVar1 = *(uint *)(param_2 + 0x74);
    }
    if ((uVar1 >> 6 & 1) != 0) {
      *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 0x40;
      puVar4 = *(undefined8 **)(param_1 + 0x30);
      if (puVar4 == (undefined8 *)0x0) {
        puVar4 = (undefined8 *)__Znwm(0x38);
        puVar4[1] = 0;
        puVar4[2] = 0;
        *puVar4 = &PTR_thunk_FUN_04ea8dd8_09ec3d00;
        *(undefined4 *)(puVar4 + 3) = 0;
        puVar4[4] = &DAT_0a524ad0;
        puVar4[5] = 0;
        *(undefined4 *)(puVar4 + 6) = 0;
        *(undefined8 **)(param_1 + 0x30) = puVar4;
        lVar5 = *(long *)(param_2 + 0x30);
      }
      else {
        lVar5 = *(long *)(param_2 + 0x30);
      }
      if (lVar5 == 0) {
        lVar5 = *(long *)(DAT_0a51f728 + 0x30);
      }
      FUN_04ea8b08(puVar4,lVar5);
      uVar1 = *(uint *)(param_2 + 0x74);
    }
    if ((uVar1 >> 7 & 1) != 0) {
      *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 0x80;
      puVar4 = *(undefined8 **)(param_1 + 0x38);
      if (puVar4 == (undefined8 *)0x0) {
        puVar4 = (undefined8 *)__Znwm(0x40);
        *puVar4 = &PTR_FUN_09ec3e68;
        puVar4[1] = 0;
        puVar4[2] = 0;
        puVar4[3] = &DAT_0a524ad0;
        puVar4[4] = &DAT_0a524ad0;
        puVar4[5] = 0;
        puVar4[6] = 0;
        *(undefined4 *)(puVar4 + 7) = 0;
        *(undefined8 **)(param_1 + 0x38) = puVar4;
        lVar5 = *(long *)(param_2 + 0x38);
      }
      else {
        lVar5 = *(long *)(param_2 + 0x38);
      }
      if (lVar5 == 0) {
        lVar5 = *(long *)(DAT_0a51f728 + 0x38);
      }
      FUN_04eaa904(puVar4,lVar5);
      uVar1 = *(uint *)(param_2 + 0x74);
    }
  }
  if ((uVar1 & 0xff00) != 0) {
    if ((uVar1 >> 8 & 1) != 0) {
      *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 0x100;
      puVar4 = *(undefined8 **)(param_1 + 0x40);
      if (puVar4 == (undefined8 *)0x0) {
        puVar4 = (undefined8 *)__Znwm(0x18);
        *puVar4 = &PTR_FUN_09ec3ee0;
        puVar4[1] = &DAT_0a524ad0;
        puVar4[2] = 0;
        *(undefined8 **)(param_1 + 0x40) = puVar4;
        lVar5 = *(long *)(param_2 + 0x40);
      }
      else {
        lVar5 = *(long *)(param_2 + 0x40);
      }
      if (lVar5 == 0) {
        lVar5 = *(long *)(DAT_0a51f728 + 0x40);
      }
      FUN_04eab788(puVar4,lVar5);
      uVar1 = *(uint *)(param_2 + 0x74);
    }
    if ((uVar1 >> 9 & 1) != 0) {
      *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 0x200;
      puVar4 = *(undefined8 **)(param_1 + 0x48);
      if (puVar4 == (undefined8 *)0x0) {
        puVar4 = (undefined8 *)__Znwm(0x18);
        *puVar4 = &PTR_FUN_09ec3f58;
        puVar4[1] = 0;
        *(undefined4 *)(puVar4 + 2) = 0;
        *(undefined8 **)(param_1 + 0x48) = puVar4;
        lVar5 = *(long *)(param_2 + 0x48);
      }
      else {
        lVar5 = *(long *)(param_2 + 0x48);
      }
      if (lVar5 == 0) {
        lVar5 = *(long *)(DAT_0a51f728 + 0x48);
      }
      FUN_04eabd84(puVar4,lVar5);
      uVar1 = *(uint *)(param_2 + 0x74);
    }
    if ((uVar1 >> 10 & 1) != 0) {
      uVar3 = *(undefined8 *)(param_2 + 0x50);
      *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 0x400;
      *(undefined8 *)(param_1 + 0x50) = uVar3;
      uVar1 = *(uint *)(param_2 + 0x74);
    }
    if ((uVar1 >> 0xb & 1) != 0) {
      *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 0x800;
      puVar4 = *(undefined8 **)(param_1 + 0x58);
      if (puVar4 == (undefined8 *)0x0) {
        puVar4 = (undefined8 *)__Znwm(0x30);
        *(undefined4 *)(puVar4 + 2) = 0;
        *puVar4 = &PTR_FUN_09ec40c0;
        puVar4[1] = 0;
        *(undefined1 *)((long)puVar4 + 0x14) = 0;
        puVar4[4] = 0;
        puVar4[5] = 0;
        puVar4[3] = 0;
        *(undefined8 **)(param_1 + 0x58) = puVar4;
        lVar5 = *(long *)(param_2 + 0x58);
      }
      else {
        lVar5 = *(long *)(param_2 + 0x58);
      }
      if (lVar5 == 0) {
        lVar5 = *(long *)(DAT_0a51f728 + 0x58);
      }
      FUN_04eacbdc(puVar4,lVar5);
      uVar1 = *(uint *)(param_2 + 0x74);
    }
    if ((uVar1 >> 0xc & 1) != 0) {
      *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 0x1000;
      puVar4 = *(undefined8 **)(param_1 + 0x60);
      if (puVar4 == (undefined8 *)0x0) {
        puVar4 = (undefined8 *)__Znwm(0x18);
        *puVar4 = &PTR_FUN_09ec4138;
        *(undefined8 *)((long)puVar4 + 0xc) = 0;
        *(undefined2 *)(puVar4 + 1) = 0;
        *(undefined8 **)(param_1 + 0x60) = puVar4;
        lVar5 = *(long *)(param_2 + 0x60);
      }
      else {
        lVar5 = *(long *)(param_2 + 0x60);
      }
      if (lVar5 == 0) {
        lVar5 = *(long *)(DAT_0a51f728 + 0x60);
      }
      FUN_04ead798(puVar4,lVar5);
      uVar1 = *(uint *)(param_2 + 0x74);
    }
    if ((uVar1 >> 0xd & 1) != 0) {
      *(uint *)(param_1 + 0x74) = *(uint *)(param_1 + 0x74) | 0x2000;
      puVar4 = *(undefined8 **)(param_1 + 0x68);
      if (puVar4 == (undefined8 *)0x0) {
        puVar4 = (undefined8 *)__Znwm(0x18);
        *puVar4 = &PTR_FUN_09ec41b0;
        *(undefined8 *)((long)puVar4 + 0xc) = 0;
        *(undefined1 *)(puVar4 + 1) = 0;
        *(undefined8 **)(param_1 + 0x68) = puVar4;
        lVar5 = *(long *)(param_2 + 0x68);
      }
      else {
        lVar5 = *(long *)(param_2 + 0x68);
      }
      if (lVar5 == 0) {
        lVar5 = *(long *)(DAT_0a51f728 + 0x68);
      }
      FUN_04eadd14(puVar4,lVar5);
    }
  }
  return;
}


