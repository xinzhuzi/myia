// Ghidra inferred pseudocode; requested=0x30d05d0
// entry=030d05d0 end=030d09c7

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_030d05d0(long param_1,undefined8 param_2,long param_3)

{
  undefined8 ******ppppppuVar1;
  undefined1 uVar2;
  uint3 uVar3;
  long lVar4;
  int iVar5;
  undefined1 *puVar6;
  uint uVar7;
  undefined1 *puVar8;
  long lVar9;
  undefined1 *puVar10;
  ulong uVar11;
  undefined4 uVar12;
  undefined4 uVar13;
  undefined8 *****local_278 [2];
  undefined7 local_268;
  char cStack_261;
  undefined8 *****local_260 [2];
  undefined7 local_250;
  char cStack_249;
  undefined1 auStack_248 [144];
  undefined1 *local_1b8;
  undefined1 local_1b0 [72];
  undefined1 *local_168;
  undefined1 local_160 [72];
  undefined8 *****local_118;
  undefined1 local_110;
  undefined8 *****local_c8;
  undefined1 **ppuStack_c0;
  undefined1 **local_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 local_60;
  undefined8 uStack_58;
  undefined8 local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  iVar5 = thunk_FUN_05e1d97c(2);
  if (iVar5 != 0) {
    FUN_0488143c(local_260);
    ppppppuVar1 = (undefined8 ******)local_260[0];
    if (-1 < cStack_249) {
      ppppppuVar1 = local_260;
    }
    if ((DAT_0a3d8d03 & 1) == 0) {
      uRam000000000a3d8cf8._0_1_ = s_message_handler_get_aeskey_faile_088ae330[8];
      uRam000000000a3d8cf8._1_1_ = s_message_handler_get_aeskey_faile_088ae330[9];
      uRam000000000a3d8cf8._2_1_ = s_message_handler_get_aeskey_faile_088ae330[10];
      uRam000000000a3d8cf8._3_1_ = s_message_handler_get_aeskey_faile_088ae330[0xb];
      uRam000000000a3d8cf8._4_1_ = s_message_handler_get_aeskey_faile_088ae330[0xc];
      uRam000000000a3d8cf8._5_1_ = s_message_handler_get_aeskey_faile_088ae330[0xd];
      uRam000000000a3d8cf8._6_1_ = s_message_handler_get_aeskey_faile_088ae330[0xe];
      uRam000000000a3d8cf8._7_1_ = s_message_handler_get_aeskey_faile_088ae330[0xf];
      DAT_0a3d8cf0 = s_message_handler_get_aeskey_faile_088ae330[0];
      DAT_0a3d8cf0_1._0_1_ = s_message_handler_get_aeskey_faile_088ae330[1];
      DAT_0a3d8cf0_1._1_1_ = s_message_handler_get_aeskey_faile_088ae330[2];
      DAT_0a3d8cf0_1._2_1_ = s_message_handler_get_aeskey_faile_088ae330[3];
      DAT_0a3d8cf0_1._3_1_ = s_message_handler_get_aeskey_faile_088ae330[4];
      DAT_0a3d8cf0_1._4_1_ = s_message_handler_get_aeskey_faile_088ae330[5];
      DAT_0a3d8cf0_1._5_1_ = s_message_handler_get_aeskey_faile_088ae330[6];
      DAT_0a3d8cf0_1._6_1_ = s_message_handler_get_aeskey_faile_088ae330[7];
      DAT_0a3d8d00 = 0x6363;
      DAT_0a3d8d02 = 0;
      DAT_0a3d8d03 = 1;
    }
    if ((DAT_0a3d8d50 & 1) == 0) {
      uRam000000000a3d8d48._0_1_ = s_PreviewViewModelNotifyDataUpdate_08648e90[0x28];
      uRam000000000a3d8d48._1_1_ = s_PreviewViewModelNotifyDataUpdate_08648e90[0x29];
      uRam000000000a3d8d48._2_1_ = s_PreviewViewModelNotifyDataUpdate_08648e90[0x2a];
      uRam000000000a3d8d48._3_1_ = s_PreviewViewModelNotifyDataUpdate_08648e90[0x2b];
      uRam000000000a3d8d48._4_1_ = s_PreviewViewModelNotifyDataUpdate_08648e90[0x2c];
      uRam000000000a3d8d48._5_1_ = s_PreviewViewModelNotifyDataUpdate_08648e90[0x2d];
      uRam000000000a3d8d48._6_1_ = s_PreviewViewModelNotifyDataUpdate_08648e90[0x2e];
      uRam000000000a3d8d48._7_1_ = s_PreviewViewModelNotifyDataUpdate_08648e90[0x2f];
      DAT_0a3d8d40 = s_PreviewViewModelNotifyDataUpdate_08648e90[0x20];
      DAT_0a3d8d40_1._0_1_ = s_PreviewViewModelNotifyDataUpdate_08648e90[0x21];
      DAT_0a3d8d40_1._1_1_ = s_PreviewViewModelNotifyDataUpdate_08648e90[0x22];
      DAT_0a3d8d40_1._2_1_ = s_PreviewViewModelNotifyDataUpdate_08648e90[0x23];
      DAT_0a3d8d40_1._3_1_ = s_PreviewViewModelNotifyDataUpdate_08648e90[0x24];
      DAT_0a3d8d40_1._4_1_ = s_PreviewViewModelNotifyDataUpdate_08648e90[0x25];
      DAT_0a3d8d40_1._5_1_ = s_PreviewViewModelNotifyDataUpdate_08648e90[0x26];
      DAT_0a3d8d40_1._6_1_ = s_PreviewViewModelNotifyDataUpdate_08648e90[0x27];
      DAT_0a3d8d50 = 1;
    }
    FUN_05e1d050(auStack_248,2,ppppppuVar1,&DAT_0a3d8cf0,&DAT_0a3d8d40,0x21,0,0);
    FUN_04cbe440(local_278,param_3);
    local_118 = local_278[0];
    if (-1 < cStack_261) {
      local_118 = local_278;
    }
    local_110 = 0;
    uVar7 = *(uint *)(param_3 + 0x120);
    local_168 = (undefined1 *)0x0;
    if ((DAT_0a3d949f & 1) == 0) {
      uVar11 = 0;
      do {
        uVar12 = *(undefined4 *)((long)&DAT_088afca7 + uVar11);
        uVar3 = CONCAT12((char)((uint)uVar12 >> 8),(short)uVar12) & 0xff00ff;
        uVar13 = *(undefined4 *)((long)&DAT_088afc93 + uVar11 % 0x14);
        *(uint *)((long)&DAT_0a3d9457 + uVar11) =
             CONCAT13((char)((uint)uVar12 >> 0x18) + 0x8aU ^ (byte)((uint)uVar13 >> 0x18),
                      CONCAT12((char)((uint)uVar12 >> 0x10) + 0x8aU ^ (byte)((uint)uVar13 >> 0x10),
                               CONCAT11((char)(uVar3 >> 0x10) + 0x8aU ^ (byte)((uint)uVar13 >> 8),
                                        (char)uVar3 + 0x8aU ^ (byte)uVar13)));
        uVar11 = uVar11 + 4;
      } while (uVar11 != 0x48);
      DAT_0a3d949f = 1;
    }
    uVar11 = (ulong)uVar7;
    lVar4 = 0;
    do {
      lVar9 = lVar4;
      uVar7 = (uint)uVar11;
      local_160[lVar9] =
           *(undefined1 *)((long)&DAT_0a3d9457 + (ulong)(uVar7 + (int)(uVar11 / 10) * -10 + 0x23));
      uVar11 = uVar11 / 10;
      lVar4 = lVar9 + 1;
    } while (9 < uVar7);
    local_160[lVar9 + 1] = 0;
    if (8 < lVar9 + 8U) {
      puVar10 = local_160;
      puVar6 = local_160 + lVar9;
      do {
        puVar10 = puVar10 + 1;
        uVar2 = *puVar6;
        puVar8 = puVar6 + -1;
        *puVar6 = puVar10[-1];
        puVar10[-1] = uVar2;
        puVar6 = puVar8;
      } while (puVar10 < puVar8);
    }
    local_168 = local_160;
    local_1b8 = local_1b0;
    lVar4 = 0;
    uVar11 = (ulong)*(uint *)(param_3 + 0x11c);
    do {
      lVar9 = lVar4;
      uVar7 = (uint)uVar11;
      local_1b0[lVar9] =
           *(undefined1 *)((long)&DAT_0a3d9457 + (ulong)(uVar7 + (int)(uVar11 / 10) * -10 + 0x23));
      lVar4 = lVar9 + 1;
      uVar11 = uVar11 / 10;
    } while (9 < uVar7);
    local_1b0[lVar9 + 1] = 0;
    if (8 < lVar9 + 8U) {
      puVar10 = local_1b0;
      puVar6 = local_1b0 + lVar9;
      do {
        puVar10 = puVar10 + 1;
        uVar2 = *puVar6;
        puVar8 = puVar6 + -1;
        *puVar6 = puVar10[-1];
        puVar10[-1] = uVar2;
        puVar6 = puVar8;
      } while (puVar10 < puVar8);
    }
    if ((DAT_0a3d8d7d & 1) == 0) {
      _DAT_0a3d8d54 = CONCAT44((int)DAT_084a8110,(int)DAT_08523260);
      uRam000000000a3d8d5c = CONCAT44((int)DAT_084d4ae0,(int)DAT_084d8af0);
      _DAT_0a3d8d64 = CONCAT44((int)DAT_084ec280,(int)DAT_08486a48);
      uRam000000000a3d8d6c = CONCAT44((int)ram0x084897a0,(int)DAT_084e3ff8);
      DAT_0a3d8d74 = CONCAT44((int)DAT_08504b70,(int)DAT_088612f0);
      DAT_0a3d8d7c = 0;
      DAT_0a3d8d7d = 1;
    }
    local_c8 = &local_118;
    ppuStack_c0 = &local_168;
    local_b8 = &local_1b8;
    uStack_a8 = 0;
    local_b0 = 0;
    uStack_98 = 0;
    local_a0 = 0;
    uStack_88 = 0;
    local_90 = 0;
    uStack_78 = 0;
    local_80 = 0;
    uStack_68 = 0;
    local_70 = 0;
    uStack_58 = 0;
    local_60 = 0;
    local_50 = 0;
    FUN_05e1d31c(auStack_248,&DAT_0a3d8d54,&local_c8);
    if (cStack_261 < '\0') {
      __ZdlPvm(local_278[0],CONCAT17(cStack_261,local_268) & 0x7fffffffffffffff);
    }
    thunk_FUN_05e1d0bc(auStack_248);
    if (cStack_249 < '\0') {
      __ZdlPvm(local_260[0],CONCAT17(cStack_249,local_250) & 0x7fffffffffffffff);
    }
  }
  FUN_030d0a14(param_1 + 0x90,param_2,param_3);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


