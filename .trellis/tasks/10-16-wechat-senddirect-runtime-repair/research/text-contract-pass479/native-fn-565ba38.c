// Ghidra inferred pseudocode; requested=0x565ba38
// entry=0565ba38 end=0565bfbb

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0565ba38(undefined8 *param_1,long param_2,undefined8 param_3,uint param_4,
                 undefined8 param_5)

{
  int iVar1;
  long lVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  ulong uVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  undefined8 uVar8;
  ulong uVar9;
  long lVar10;
  undefined1 auStack_e0 [24];
  undefined1 auStack_c8 [96];
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar2 = FUN_009ce4a8(param_3);
  if (lVar2 == 0) {
    FUN_00069f7c(param_1);
    *(undefined1 *)(param_1 + 1) = 0;
    FUN_056323cc(param_1 + 1,param_3);
    *(undefined1 *)param_1 = 1;
  }
  else {
    FUN_009ce4a8(param_3);
    uVar3 = FUN_057b0790();
    iVar1 = FUN_057abfac();
    if (iVar1 == 0) {
      uVar4 = FUN_0565c0a4(param_2 + 0x10);
      lVar2 = FUN_05662bcc(uVar4,uVar3);
      if (lVar2 != 0) {
        if (param_4 == 0) {
          uVar4 = FUN_05662b74(uVar4);
          uVar6 = FUN_05632b8c(param_3);
          uVar7 = FUN_009ce4a8(param_3);
          uVar5 = FUN_057b1488(uVar4,lVar2,uVar3,uVar6,uVar7);
LAB_0565be18:
          iVar1 = FUN_057abfac();
          if (iVar1 == 0) {
            uVar9 = FUN_009ce4a8(param_3);
            if (uVar9 <= uVar5) {
              if (*(long *)PTR____stack_chk_guard_09b36c98 == local_68) {
                FUN_0565c038(param_1,param_3);
                return;
              }
              goto LAB_0565bfb8;
            }
            FUN_05632308(auStack_c8,lVar2,uVar5);
            FUN_0565c224(param_1,auStack_c8);
            FUN_0563255c(auStack_c8);
            goto LAB_0565bb98;
          }
          FUN_0562fcc8(auStack_c8,0);
          FUN_057abfb8(uVar5);
          if ((DAT_0a4d6c82 & 1) == 0) {
            uRam000000000a4d6c78._0_1_ = s_Compress_fail___Decompress_fail__08b2e090[8];
            uRam000000000a4d6c78._1_1_ = s_Compress_fail___Decompress_fail__08b2e090[9];
            uRam000000000a4d6c78._2_1_ = s_Compress_fail___Decompress_fail__08b2e090[10];
            uRam000000000a4d6c78._3_1_ = s_Compress_fail___Decompress_fail__08b2e090[0xb];
            uRam000000000a4d6c78._4_1_ = s_Compress_fail___Decompress_fail__08b2e090[0xc];
            uRam000000000a4d6c78._5_1_ = s_Compress_fail___Decompress_fail__08b2e090[0xd];
            uRam000000000a4d6c78._6_1_ = s_Compress_fail___Decompress_fail__08b2e090[0xe];
            uRam000000000a4d6c78._7_1_ = s_Compress_fail___Decompress_fail__08b2e090[0xf];
            DAT_0a4d6c70 = s_Compress_fail___Decompress_fail__08b2e090[0];
            DAT_0a4d6c70_1._0_1_ = s_Compress_fail___Decompress_fail__08b2e090[1];
            DAT_0a4d6c70_1._1_1_ = s_Compress_fail___Decompress_fail__08b2e090[2];
            DAT_0a4d6c70_1._2_1_ = s_Compress_fail___Decompress_fail__08b2e090[3];
            DAT_0a4d6c70_1._3_1_ = s_Compress_fail___Decompress_fail__08b2e090[4];
            DAT_0a4d6c70_1._4_1_ = s_Compress_fail___Decompress_fail__08b2e090[5];
            DAT_0a4d6c70_1._5_1_ = s_Compress_fail___Decompress_fail__08b2e090[6];
            DAT_0a4d6c70_1._6_1_ = s_Compress_fail___Decompress_fail__08b2e090[7];
            DAT_0a4d6c80 = 0x73;
            DAT_0a4d6c82 = 1;
          }
          FUN_05630c8c(auStack_e0,&DAT_0a4d6c70);
          thunk_FUN_05695d78(param_5,1000,auStack_c8,auStack_e0);
        }
        else {
          if (0xfffffc18 < param_4 - 1000) {
            lVar10 = *(long *)(*(long *)(param_2 + 8) + (ulong)param_4 * 8);
            if (lVar10 != 0) {
              uVar5 = FUN_05662c34(lVar10);
              if ((uVar5 & 1) == 0) {
                FUN_0562fcc8(auStack_c8,0);
                if ((DAT_0a4d6c69 & 1) == 0) {
                  _DAT_0a4d6c4c = CONCAT44((int)DAT_084d8778,(int)DAT_08a9c328);
                  uRam000000000a4d6c54 = CONCAT44((int)DAT_0848a070,(int)ram0x088df230);
                  DAT_0a4d6c5c = CONCAT44((int)DAT_08967e18,(int)DAT_0855b898);
                  DAT_0a4d6c64 = (undefined4)DAT_085b0608;
                  DAT_0a4d6c68 = 0;
                  DAT_0a4d6c69 = 1;
                }
                FUN_05630c8c(auStack_e0,&DAT_0a4d6c4c);
                thunk_FUN_05695d78(param_5,1000,auStack_c8,auStack_e0);
                goto LAB_0565bb40;
              }
              uVar4 = FUN_05662b74(uVar4);
              uVar6 = FUN_05632b8c(param_3);
              uVar7 = FUN_009ce4a8(param_3);
              uVar8 = FUN_009ce4a8(lVar10);
              uVar5 = FUN_057b353c(uVar4,lVar2,uVar3,uVar6,uVar7,uVar8);
              goto LAB_0565be18;
            }
          }
          FUN_0562fcc8(auStack_c8,0);
          if ((DAT_0a4d6c4b & 1) == 0) {
            _DAT_0a4d6c24 = CONCAT44((int)DAT_084c7770,(int)DAT_0854cfd0);
            uRam000000000a4d6c2c = CONCAT44((int)ram0x0853ea60,(int)DAT_084a04e8);
            _DAT_0a4d6c34 = CONCAT44((int)DAT_086e8548,(int)DAT_084e1400);
            uRam000000000a4d6c3c = CONCAT44((int)DAT_084d87b0,(int)ram0x08b2e0b0);
            DAT_0a4d6c44 = (undefined4)DAT_084e4960;
            DAT_0a4d6c48 = 0x6425;
            DAT_0a4d6c4a = 0;
            DAT_0a4d6c4b = 1;
          }
          FUN_05630c8c(auStack_e0,&DAT_0a4d6c24);
          thunk_FUN_05695d78(param_5,1000,auStack_c8,auStack_e0);
        }
        goto LAB_0565bb40;
      }
      FUN_0562fcc8(auStack_c8,0);
      if ((DAT_0a4d6c23 & 1) == 0) {
        _DAT_0a4d6c04 = CONCAT44((int)DAT_08482fb0,(int)DAT_0869f008);
        uRam000000000a4d6c0c = CONCAT44((int)DAT_08b2e0b8,(int)DAT_0847fde0);
        DAT_0a4d6c14 = CONCAT44((int)DAT_084e4880,(int)DAT_0852e890);
        DAT_0a4d6c1c = (undefined4)DAT_084e3380;
        DAT_0a4d6c20 = 0x7972;
        DAT_0a4d6c22 = 0;
        DAT_0a4d6c23 = 1;
      }
      FUN_0562fcc8(auStack_e0,&DAT_0a4d6c04);
      thunk_FUN_05695d78(param_5,7,auStack_c8,auStack_e0);
      FUN_0562fd84(auStack_e0);
    }
    else {
      FUN_0562fcc8(auStack_c8,0);
      FUN_057abfb8(uVar3);
      if ((DAT_0a4d6c00 & 1) == 0) {
        _DAT_0a4d6be8 = CONCAT44((int)DAT_08482fb0,(int)DAT_0869f008);
        uRam000000000a4d6bf0 = CONCAT44((int)DAT_087b84b0,(int)DAT_0855b928);
        DAT_0a4d6bf8 = CONCAT44((int)DAT_0877c278,(int)DAT_086c6a88);
        DAT_0a4d6c00 = 1;
      }
      FUN_05630c8c(auStack_e0,&DAT_0a4d6be8);
      thunk_FUN_05695d78(param_5,1000,auStack_c8,auStack_e0);
LAB_0565bb40:
      FUN_0562fd84(auStack_e0);
    }
    FUN_0562fd84(auStack_c8);
    param_1[0xc] = 0;
    param_1[9] = 0;
    param_1[8] = 0;
    param_1[0xb] = 0;
    param_1[10] = 0;
    param_1[5] = 0;
    param_1[4] = 0;
    param_1[7] = 0;
    param_1[6] = 0;
    param_1[1] = 0;
    *param_1 = 0;
    param_1[3] = 0;
    param_1[2] = 0;
    FUN_00069f7c(param_1);
    *(undefined1 *)(param_1 + 1) = 0;
  }
LAB_0565bb98:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_68) {
    return;
  }
LAB_0565bfb8:
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


