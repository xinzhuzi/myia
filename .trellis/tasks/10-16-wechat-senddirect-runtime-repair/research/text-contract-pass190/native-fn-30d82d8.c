// Ghidra inferred pseudocode; requested=0x30d82d8
// entry=030d82d8 end=030d8503

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_030d82d8(undefined8 param_1)

{
  undefined8 ***pppuVar1;
  int iVar2;
  undefined8 **local_168 [2];
  undefined7 local_158;
  char cStack_151;
  undefined1 auStack_150 [144];
  undefined8 local_c0;
  undefined8 uStack_b8;
  undefined8 uStack_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 uStack_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 uStack_70;
  undefined8 uStack_68;
  undefined8 local_60;
  undefined8 uStack_58;
  undefined8 uStack_50;
  undefined8 uStack_48;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  iVar2 = thunk_FUN_05e1d97c(3);
  if (iVar2 != 0) {
    FUN_0488143c(local_168);
    pppuVar1 = (undefined8 ***)local_168[0];
    if (-1 < cStack_151) {
      pppuVar1 = local_168;
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
    if ((DAT_0a3d9091 & 1) == 0) {
      _DAT_0a3d9078 = CONCAT44((int)DAT_087e2df0,(int)ram0x087e2de8);
      uRam000000000a3d9080 = CONCAT44((int)DAT_088a71c0,(int)DAT_0854dcf8);
      DAT_0a3d9088 = CONCAT44((int)DAT_084a66b0,(int)DAT_085095c0);
      DAT_0a3d9090 = 0;
      DAT_0a3d9091 = 1;
    }
    FUN_05e1d050(auStack_150,3,pppuVar1,&DAT_0a3d8cf0,&DAT_0a3d9078,0x1ba,0,0);
    if ((DAT_0a3d90ba & 1) == 0) {
      _DAT_0a3d9094 = CONCAT44((int)DAT_088ae280,(int)DAT_08480908);
      uRam000000000a3d909c = CONCAT44((int)DAT_088ae298,(int)DAT_0884db28);
      _DAT_0a3d90a4 = CONCAT44((int)DAT_088a7260,(int)DAT_08676638);
      uRam000000000a3d90ac = CONCAT44((int)DAT_085312b0,(int)DAT_084a8110);
      DAT_0a3d90b4 = (undefined4)DAT_084d8740;
      DAT_0a3d90b8 = 0x67;
      DAT_0a3d90ba = 1;
    }
    uStack_58 = 0;
    local_60 = 0;
    uStack_48 = 0;
    uStack_50 = 0;
    uStack_78 = 0;
    local_80 = 0;
    uStack_68 = 0;
    uStack_70 = 0;
    uStack_98 = 0;
    local_a0 = 0;
    uStack_88 = 0;
    uStack_90 = 0;
    uStack_b8 = 0;
    local_c0 = 0;
    uStack_a8 = 0;
    uStack_b0 = 0;
    FUN_05e1d31c(auStack_150,&DAT_0a3d9094,&local_c0);
    thunk_FUN_05e1d0bc(auStack_150);
    if (cStack_151 < '\0') {
      __ZdlPvm(local_168[0],CONCAT17(cStack_151,local_158) & 0x7fffffffffffffff);
    }
  }
  FUN_0304f1cc(param_1,0,0);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


