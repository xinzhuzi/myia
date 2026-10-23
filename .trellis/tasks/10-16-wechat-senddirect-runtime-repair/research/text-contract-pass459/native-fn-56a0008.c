// Ghidra inferred pseudocode; requested=0x56a0008
// entry=056a0008 end=056a03bb

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 FUN_056a0008(long param_1,long *param_2)

{
  char cVar1;
  int iVar2;
  ulong uVar3;
  long lVar4;
  undefined8 uVar5;
  long local_a8;
  undefined1 *local_a0;
  undefined1 *local_98;
  undefined1 *puStack_90;
  undefined1 *local_88;
  undefined1 *local_80;
  undefined1 *puStack_78;
  undefined1 *local_70;
  undefined1 *local_68;
  undefined1 *puStack_60;
  undefined1 auStack_58 [24];
  
  FUN_009abfd4();
  iVar2 = FUN_05695b38();
  if (iVar2 != 0) {
    FUN_056a0458(param_1,param_2);
  }
  FUN_056c22d4(auStack_58,param_2);
  if (*(char *)(param_1 + 0x50) == '\x01') {
    FUN_0569fbc0(param_1);
  }
  uVar3 = FUN_056a056c(param_1,auStack_58);
  if ((uVar3 & 1) != 0) {
    uVar5 = 1;
    goto LAB_056a00d0;
  }
  if ((*(char *)(param_1 + 0x50) == '\x01') &&
     (cVar1 = (**(code **)(*param_2 + 0x10))(param_2), 0xfb < (byte)(cVar1 - 0x28U))) {
    FUN_009abfd4(param_1);
    uVar5 = FUN_0109d770();
    iVar2 = FUN_05633da8();
    if ((iVar2 == 1) && (iVar2 = FUN_05634228(uVar5), iVar2 == 0)) {
      uVar5 = FUN_0109d770(uVar5);
      if ((DAT_0a4d7a11 & 1) == 0) {
        uRam000000000a4d7a08._0_1_ = s_no_such_column__LastInsertedId__08b2f940[8];
        uRam000000000a4d7a08._1_1_ = s_no_such_column__LastInsertedId__08b2f940[9];
        uRam000000000a4d7a08._2_1_ = s_no_such_column__LastInsertedId__08b2f940[10];
        uRam000000000a4d7a08._3_1_ = s_no_such_column__LastInsertedId__08b2f940[0xb];
        uRam000000000a4d7a08._4_1_ = s_no_such_column__LastInsertedId__08b2f940[0xc];
        uRam000000000a4d7a08._5_1_ = s_no_such_column__LastInsertedId__08b2f940[0xd];
        uRam000000000a4d7a08._6_1_ = s_no_such_column__LastInsertedId__08b2f940[0xe];
        uRam000000000a4d7a08._7_1_ = s_no_such_column__LastInsertedId__08b2f940[0xf];
        DAT_0a4d7a00 = s_no_such_column__LastInsertedId__08b2f940[0];
        DAT_0a4d7a00_1._0_1_ = s_no_such_column__LastInsertedId__08b2f940[1];
        DAT_0a4d7a00_1._1_1_ = s_no_such_column__LastInsertedId__08b2f940[2];
        DAT_0a4d7a00_1._2_1_ = s_no_such_column__LastInsertedId__08b2f940[3];
        DAT_0a4d7a00_1._3_1_ = s_no_such_column__LastInsertedId__08b2f940[4];
        DAT_0a4d7a00_1._4_1_ = s_no_such_column__LastInsertedId__08b2f940[5];
        DAT_0a4d7a00_1._5_1_ = s_no_such_column__LastInsertedId__08b2f940[6];
        DAT_0a4d7a00_1._6_1_ = s_no_such_column__LastInsertedId__08b2f940[7];
        DAT_0a4d7a10 = 0;
        DAT_0a4d7a11 = 1;
      }
      FUN_0562fcc8(&local_70,&DAT_0a4d7a00);
      iVar2 = FUN_05630464(uVar5,&local_70);
      if (iVar2 == 0) {
        iVar2 = (**(code **)(*param_2 + 0x10))(param_2);
        if (iVar2 == 0x25) {
          if ((DAT_0a4d7a1b & 1) == 0) {
            DAT_0a4d7a14 = (undefined4)DAT_084abe58;
            DAT_0a4d7a18 = 0x2065;
            DAT_0a4d7a1a = 0;
            DAT_0a4d7a1b = 1;
          }
          FUN_0562fcc8(&local_88,&DAT_0a4d7a14);
          iVar2 = FUN_05630464(uVar5,&local_88);
          if (iVar2 != 0) {
            if ((DAT_0a4d7a32 & 1) == 0) {
              _DAT_0a4d7a1c = CONCAT44((int)DAT_084e4880,(int)DAT_0859a140);
              uRam000000000a4d7a24 = CONCAT44((int)DAT_08b2f960,(int)DAT_08839b10);
              DAT_0a4d7a2c = (undefined4)ram0x08486ab8;
              DAT_0a4d7a30 = 0x20;
              DAT_0a4d7a32 = 1;
            }
            FUN_0562fcc8(&local_a0,&DAT_0a4d7a1c);
            uVar3 = FUN_056304e4(uVar5,&local_a0);
            FUN_0562fd84(&local_a0);
            FUN_0562fd84(&local_88);
            FUN_0562fd84(&local_70);
            if ((uVar3 & 1) == 0) goto LAB_056a00cc;
            goto LAB_056a0154;
          }
          FUN_0562fd84(&local_88);
        }
        FUN_0562fd84(&local_70);
      }
      else {
        FUN_0562fd84(&local_70);
LAB_056a0154:
        lVar4 = FUN_009abfd4(param_1);
        if ((lVar4 != 0) &&
           (lVar4 = ___dynamic_cast(lVar4,&PTR_DAT_09f1c670,&PTR_DAT_09f18cc0,0), lVar4 != 0)) {
          local_68 = &SUB_aaaaaaaaaaaaaaaa;
          puStack_60 = &SUB_aaaaaaaaaaaaaaaa;
          local_70 = &SUB_aaaaaaaaaaaaaaaa;
          FUN_0562fcb4(&local_70);
          local_80 = &SUB_aaaaaaaaaaaaaaaa;
          puStack_78 = &SUB_aaaaaaaaaaaaaaaa;
          local_88 = &SUB_aaaaaaaaaaaaaaaa;
          FUN_0562fcb4(&local_88);
          local_98 = &SUB_aaaaaaaaaaaaaaaa;
          puStack_90 = &SUB_aaaaaaaaaaaaaaaa;
          local_a0 = &SUB_aaaaaaaaaaaaaaaa;
          FUN_0562fcb4(&local_a0);
          local_a8 = 0;
          uVar3 = FUN_056a06f0(param_1,param_2,uVar5,&local_70,&local_88,&local_a0,&local_a8);
          if ((uVar3 & 1) == 0) {
LAB_056a0204:
            uVar5 = 0;
          }
          else {
            if (local_a8 == 0) {
              lVar4 = FUN_009abfd4(param_1);
              if (((lVar4 != 0) &&
                  (lVar4 = ___dynamic_cast(lVar4,&PTR_DAT_09f1c670,&PTR_DAT_09f1c878,0x38),
                  lVar4 != 0)) && (iVar2 = FUN_056a0ea4(lVar4,&DAT_0a5245b8), iVar2 != 0)) {
                lVar4 = FUN_056a0f40(lVar4,&DAT_0a5245b8);
                iVar2 = FUN_0565a354(lVar4 + 0x20,&local_88);
                if (iVar2 == 0) goto LAB_056a0204;
              }
            }
            else {
              uVar3 = FUN_056c64c4(local_a8,&local_70,&local_88,&local_a0,auStack_58,lVar4);
              if ((uVar3 & 1) == 0) goto LAB_056a0204;
            }
            FUN_0569fbc8(param_1);
            uVar5 = FUN_056a056c(param_1,auStack_58);
          }
          FUN_0562fd84(&local_a0);
          FUN_0562fd84(&local_88);
          FUN_0562fd84(&local_70);
          goto LAB_056a00d0;
        }
      }
    }
  }
LAB_056a00cc:
  uVar5 = 0;
LAB_056a00d0:
  FUN_0562fd84(auStack_58);
  return uVar5;
}


