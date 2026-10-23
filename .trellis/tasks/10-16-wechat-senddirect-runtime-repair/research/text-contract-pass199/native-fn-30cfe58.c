// Ghidra inferred pseudocode; requested=0x30cfe58
// entry=030cfe58 end=030d0083

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_030cfe58(long param_1,undefined8 param_2)

{
  undefined8 ***pppuVar1;
  int iVar2;
  undefined8 **local_1c8 [2];
  undefined7 local_1b8;
  char cStack_1b1;
  undefined8 **local_1b0 [2];
  undefined7 local_1a0;
  char cStack_199;
  undefined1 auStack_198 [144];
  undefined8 **local_108;
  undefined1 local_100;
  undefined8 **local_b8;
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
  undefined8 uStack_48;
  undefined8 local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  iVar2 = thunk_FUN_05e1d97c(2);
  if (iVar2 != 0) {
    FUN_0488143c(local_1b0);
    pppuVar1 = (undefined8 ***)local_1b0[0];
    if (-1 < cStack_199) {
      pppuVar1 = local_1b0;
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
    if ((DAT_0a3d8d15 & 1) == 0) {
      DAT_0a3d8d08._0_1_ = s_OnMessageAdd_084f0818[0];
      DAT_0a3d8d08._1_1_ = s_OnMessageAdd_084f0818[1];
      DAT_0a3d8d08._2_1_ = s_OnMessageAdd_084f0818[2];
      DAT_0a3d8d08._3_1_ = s_OnMessageAdd_084f0818[3];
      DAT_0a3d8d08._4_1_ = s_OnMessageAdd_084f0818[4];
      DAT_0a3d8d08._5_1_ = s_OnMessageAdd_084f0818[5];
      DAT_0a3d8d08._6_1_ = s_OnMessageAdd_084f0818[6];
      DAT_0a3d8d08._7_1_ = s_OnMessageAdd_084f0818[7];
      DAT_0a3d8d10 = (undefined4)ram0x084f0820;
      DAT_0a3d8d14 = 0;
      DAT_0a3d8d15 = 1;
    }
    FUN_05e1d050(auStack_198,2,pppuVar1,&DAT_0a3d8cf0,&DAT_0a3d8d08,0x1c,0,0);
    FUN_04cbe440(local_1c8,param_2);
    local_108 = local_1c8[0];
    if (-1 < cStack_1b1) {
      local_108 = local_1c8;
    }
    local_100 = 0;
    if ((DAT_0a3d8d30 & 1) == 0) {
      _DAT_0a3d8d18 = CONCAT44((int)DAT_084a8110,(int)DAT_08523260);
      uRam000000000a3d8d20 = CONCAT44((int)DAT_08507730,(int)ram0x084f0820);
      DAT_0a3d8d28 = CONCAT44((int)DAT_084d1ec0,(int)DAT_084a66b0);
      DAT_0a3d8d30 = 1;
    }
    uStack_a8 = 0;
    local_b0 = 0;
    local_b8 = &local_108;
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
    uStack_48 = 0;
    local_50 = 0;
    local_40 = 0;
    FUN_05e1d31c(auStack_198,&DAT_0a3d8d18,&local_b8);
    if (cStack_1b1 < '\0') {
      __ZdlPvm(local_1c8[0],CONCAT17(cStack_1b1,local_1b8) & 0x7fffffffffffffff);
    }
    thunk_FUN_05e1d0bc(auStack_198);
    if (cStack_199 < '\0') {
      __ZdlPvm(local_1b0[0],CONCAT17(cStack_199,local_1a0) & 0x7fffffffffffffff);
    }
  }
  FUN_030d00d0(param_1 + 0x18,param_2);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


