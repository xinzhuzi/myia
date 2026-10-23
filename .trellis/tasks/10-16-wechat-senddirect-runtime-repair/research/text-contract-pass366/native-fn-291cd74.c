// Ghidra inferred pseudocode; requested=0x291cd74
// entry=0291cd74 end=0291d45f

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0291cd74(long param_1)

{
  ulong uVar1;
  size_t sVar2;
  undefined8 ****ppppuVar3;
  undefined8 ***local_130;
  size_t local_128;
  undefined8 local_120;
  undefined8 ***local_118;
  size_t local_110;
  undefined8 local_108;
  undefined8 ***local_100;
  size_t local_f8;
  undefined8 local_f0;
  undefined8 ***local_e8;
  size_t local_e0;
  undefined8 local_d8;
  undefined8 ***local_d0;
  size_t local_c8;
  undefined8 local_c0;
  undefined8 ***local_b8;
  size_t local_b0;
  undefined8 local_a8;
  undefined8 ***local_a0;
  size_t local_98;
  undefined8 local_90;
  undefined8 ***local_88;
  size_t local_80;
  undefined8 local_78;
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_09b36c98;
  if ((DAT_0a3a54e8 & 1) == 0) {
    DAT_0a3a54e0 = s_group_idmore_texchat_id_08585928._16_8_;
    DAT_0a3a54e8 = 1;
  }
  sVar2 = _strlen((char *)&DAT_0a3a54e0);
  if (0x7ffffffffffffff7 < sVar2) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_b8);
  }
  if (sVar2 < 0x17) {
    local_a8 = CONCAT17((char)sVar2,(undefined7)local_a8);
    ppppuVar3 = &local_b8;
    if (sVar2 != 0) goto LAB_0291ce2c;
  }
  else {
    uVar1 = 0x19;
    if ((sVar2 | 7) != 0x17) {
      uVar1 = (sVar2 | 7) + 1;
    }
    ppppuVar3 = (undefined8 ****)__Znwm(uVar1);
    local_a8 = uVar1 | 0x8000000000000000;
    local_b8 = ppppuVar3;
    local_b0 = sVar2;
LAB_0291ce2c:
    _memcpy(ppppuVar3,&DAT_0a3a54e0,sVar2);
  }
  *(undefined1 *)((long)ppppuVar3 + sVar2) = 0;
  ppppuVar3 = &local_a0;
  if ((DAT_0a3a54fd & 1) == 0) {
    DAT_0a3a54f0._0_1_ = s_message_sg_d_0866d0f8[0];
    DAT_0a3a54f0._1_1_ = s_message_sg_d_0866d0f8[1];
    DAT_0a3a54f0._2_1_ = s_message_sg_d_0866d0f8[2];
    DAT_0a3a54f0._3_1_ = s_message_sg_d_0866d0f8[3];
    DAT_0a3a54f0._4_1_ = s_message_sg_d_0866d0f8[4];
    DAT_0a3a54f0._5_1_ = s_message_sg_d_0866d0f8[5];
    DAT_0a3a54f0._6_1_ = s_message_sg_d_0866d0f8[6];
    DAT_0a3a54f0._7_1_ = s_message_sg_d_0866d0f8[7];
    DAT_0a3a54f8 = (undefined4)DAT_08489788;
    DAT_0a3a54fc = 0;
    DAT_0a3a54fd = 1;
  }
  sVar2 = _strlen((char *)&DAT_0a3a54f0);
  if (0x7ffffffffffffff7 < sVar2) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(ppppuVar3);
  }
  if (sVar2 < 0x17) {
    local_90 = CONCAT17((char)sVar2,(undefined7)local_90);
    if (sVar2 != 0) goto LAB_0291cedc;
  }
  else {
    uVar1 = 0x19;
    if ((sVar2 | 7) != 0x17) {
      uVar1 = (sVar2 | 7) + 1;
    }
    ppppuVar3 = (undefined8 ****)__Znwm(uVar1);
    local_90 = uVar1 | 0x8000000000000000;
    local_a0 = ppppuVar3;
    local_98 = sVar2;
LAB_0291cedc:
    _memcpy(ppppuVar3,&DAT_0a3a54f0,sVar2);
  }
  *(undefined1 *)((long)ppppuVar3 + sVar2) = 0;
  ppppuVar3 = &local_88;
  if ((DAT_0a3a5513 & 1) == 0) {
    uRam000000000a3a5508 = _UNK_08824cb8;
    _DAT_0a3a5500 = _DAT_08824cb0;
    DAT_0a3a5510 = 0x3436;
    DAT_0a3a5512 = 0;
    DAT_0a3a5513 = 1;
  }
  sVar2 = _strlen(&DAT_0a3a5500);
  if (0x7ffffffffffffff7 < sVar2) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(ppppuVar3);
  }
  if (sVar2 < 0x17) {
    local_78 = CONCAT17((char)sVar2,(undefined7)local_78);
    if (sVar2 != 0) goto LAB_0291cf88;
  }
  else {
    uVar1 = 0x19;
    if ((sVar2 | 7) != 0x17) {
      uVar1 = (sVar2 | 7) + 1;
    }
    ppppuVar3 = (undefined8 ****)__Znwm(uVar1);
    local_78 = uVar1 | 0x8000000000000000;
    local_88 = ppppuVar3;
    local_80 = sVar2;
LAB_0291cf88:
    _memcpy(ppppuVar3,&DAT_0a3a5500,sVar2);
  }
  *(undefined1 *)((long)ppppuVar3 + sVar2) = 0;
  FUN_0029ae04(param_1,&local_b8,3);
  if ((DAT_0a3a54e8 & 1) == 0) {
    DAT_0a3a54e0._0_1_ = s_group_idmore_texchat_id_08585928[0x10];
    DAT_0a3a54e0._1_1_ = s_group_idmore_texchat_id_08585928[0x11];
    DAT_0a3a54e0._2_1_ = s_group_idmore_texchat_id_08585928[0x12];
    DAT_0a3a54e0._3_1_ = s_group_idmore_texchat_id_08585928[0x13];
    DAT_0a3a54e0._4_1_ = s_group_idmore_texchat_id_08585928[0x14];
    DAT_0a3a54e0._5_1_ = s_group_idmore_texchat_id_08585928[0x15];
    DAT_0a3a54e0._6_1_ = s_group_idmore_texchat_id_08585928[0x16];
    DAT_0a3a54e0._7_1_ = s_group_idmore_texchat_id_08585928[0x17];
    DAT_0a3a54e8 = 1;
  }
  sVar2 = _strlen((char *)&DAT_0a3a54e0);
  if (0x7ffffffffffffff7 < sVar2) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_130);
  }
  if (sVar2 < 0x17) {
    local_120 = CONCAT17((char)sVar2,(undefined7)local_120);
    ppppuVar3 = &local_130;
    if (sVar2 != 0) goto LAB_0291d028;
  }
  else {
    uVar1 = 0x19;
    if ((sVar2 | 7) != 0x17) {
      uVar1 = (sVar2 | 7) + 1;
    }
    ppppuVar3 = (undefined8 ****)__Znwm(uVar1);
    local_120 = uVar1 | 0x8000000000000000;
    local_130 = ppppuVar3;
    local_128 = sVar2;
LAB_0291d028:
    _memcpy(ppppuVar3,&DAT_0a3a54e0,sVar2);
  }
  *(undefined1 *)((long)ppppuVar3 + sVar2) = 0;
  ppppuVar3 = &local_118;
  if ((DAT_0a3a54fd & 1) == 0) {
    DAT_0a3a54f0._0_1_ = s_message_sg_d_0866d0f8[0];
    DAT_0a3a54f0._1_1_ = s_message_sg_d_0866d0f8[1];
    DAT_0a3a54f0._2_1_ = s_message_sg_d_0866d0f8[2];
    DAT_0a3a54f0._3_1_ = s_message_sg_d_0866d0f8[3];
    DAT_0a3a54f0._4_1_ = s_message_sg_d_0866d0f8[4];
    DAT_0a3a54f0._5_1_ = s_message_sg_d_0866d0f8[5];
    DAT_0a3a54f0._6_1_ = s_message_sg_d_0866d0f8[6];
    DAT_0a3a54f0._7_1_ = s_message_sg_d_0866d0f8[7];
    DAT_0a3a54f8 = (undefined4)DAT_08489788;
    DAT_0a3a54fc = 0;
    DAT_0a3a54fd = 1;
  }
  sVar2 = _strlen((char *)&DAT_0a3a54f0);
  if (0x7ffffffffffffff7 < sVar2) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(ppppuVar3);
  }
  if (sVar2 < 0x17) {
    local_108 = CONCAT17((char)sVar2,(undefined7)local_108);
    if (sVar2 != 0) goto LAB_0291d0c8;
  }
  else {
    uVar1 = 0x19;
    if ((sVar2 | 7) != 0x17) {
      uVar1 = (sVar2 | 7) + 1;
    }
    ppppuVar3 = (undefined8 ****)__Znwm(uVar1);
    local_108 = uVar1 | 0x8000000000000000;
    local_118 = ppppuVar3;
    local_110 = sVar2;
LAB_0291d0c8:
    _memcpy(ppppuVar3,&DAT_0a3a54f0,sVar2);
  }
  *(undefined1 *)((long)ppppuVar3 + sVar2) = 0;
  ppppuVar3 = &local_100;
  if ((DAT_0a3a5513 & 1) == 0) {
    uRam000000000a3a5508 = _UNK_08824cb8;
    _DAT_0a3a5500 = _DAT_08824cb0;
    DAT_0a3a5510 = 0x3436;
    DAT_0a3a5512 = 0;
    DAT_0a3a5513 = 1;
  }
  sVar2 = _strlen(&DAT_0a3a5500);
  if (0x7ffffffffffffff7 < sVar2) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(ppppuVar3);
  }
  if (sVar2 < 0x17) {
    local_f0 = CONCAT17((char)sVar2,(undefined7)local_f0);
    if (sVar2 != 0) goto LAB_0291d164;
  }
  else {
    uVar1 = 0x19;
    if ((sVar2 | 7) != 0x17) {
      uVar1 = (sVar2 | 7) + 1;
    }
    ppppuVar3 = (undefined8 ****)__Znwm(uVar1);
    local_f0 = uVar1 | 0x8000000000000000;
    local_100 = ppppuVar3;
    local_f8 = sVar2;
LAB_0291d164:
    _memcpy(ppppuVar3,&DAT_0a3a5500,sVar2);
  }
  *(undefined1 *)((long)ppppuVar3 + sVar2) = 0;
  ppppuVar3 = &local_e8;
  if ((DAT_0a3a5524 & 1) == 0) {
    DAT_0a3a5518._0_1_ = s_content_refer_icon__084f26e0[0];
    DAT_0a3a5518._1_1_ = s_content_refer_icon__084f26e0[1];
    DAT_0a3a5518._2_1_ = s_content_refer_icon__084f26e0[2];
    DAT_0a3a5518._3_1_ = s_content_refer_icon__084f26e0[3];
    DAT_0a3a5518._4_1_ = s_content_refer_icon__084f26e0[4];
    DAT_0a3a5518._5_1_ = s_content_refer_icon__084f26e0[5];
    DAT_0a3a5518._6_1_ = s_content_refer_icon__084f26e0[6];
    DAT_0a3a5518._7_1_ = s_content_refer_icon__084f26e0[7];
    DAT_0a3a5520 = (undefined4)DAT_08572320;
    DAT_0a3a5524 = 1;
  }
  sVar2 = _strlen((char *)&DAT_0a3a5518);
  if (0x7ffffffffffffff7 < sVar2) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(ppppuVar3);
  }
  if (sVar2 < 0x17) {
    local_d8 = CONCAT17((char)sVar2,(undefined7)local_d8);
    if (sVar2 != 0) goto LAB_0291d20c;
  }
  else {
    uVar1 = 0x19;
    if ((sVar2 | 7) != 0x17) {
      uVar1 = (sVar2 | 7) + 1;
    }
    ppppuVar3 = (undefined8 ****)__Znwm(uVar1);
    local_d8 = uVar1 | 0x8000000000000000;
    local_e8 = ppppuVar3;
    local_e0 = sVar2;
LAB_0291d20c:
    _memcpy(ppppuVar3,&DAT_0a3a5518,sVar2);
  }
  *(undefined1 *)((long)ppppuVar3 + sVar2) = 0;
  ppppuVar3 = &local_d0;
  if ((DAT_0a3a5540 & 1) == 0) {
    uRam000000000a3a5538._0_1_ = s_my_group_nicknammessage_subtype_088053a0[0x18];
    uRam000000000a3a5538._1_1_ = s_my_group_nicknammessage_subtype_088053a0[0x19];
    uRam000000000a3a5538._2_1_ = s_my_group_nicknammessage_subtype_088053a0[0x1a];
    uRam000000000a3a5538._3_1_ = s_my_group_nicknammessage_subtype_088053a0[0x1b];
    uRam000000000a3a5538._4_1_ = s_my_group_nicknammessage_subtype_088053a0[0x1c];
    uRam000000000a3a5538._5_1_ = s_my_group_nicknammessage_subtype_088053a0[0x1d];
    uRam000000000a3a5538._6_1_ = s_my_group_nicknammessage_subtype_088053a0[0x1e];
    uRam000000000a3a5538._7_1_ = s_my_group_nicknammessage_subtype_088053a0[0x1f];
    DAT_0a3a5530 = s_my_group_nicknammessage_subtype_088053a0[0x10];
    DAT_0a3a5530_1._0_1_ = s_my_group_nicknammessage_subtype_088053a0[0x11];
    DAT_0a3a5530_1._1_1_ = s_my_group_nicknammessage_subtype_088053a0[0x12];
    DAT_0a3a5530_1._2_1_ = s_my_group_nicknammessage_subtype_088053a0[0x13];
    DAT_0a3a5530_1._3_1_ = s_my_group_nicknammessage_subtype_088053a0[0x14];
    DAT_0a3a5530_1._4_1_ = s_my_group_nicknammessage_subtype_088053a0[0x15];
    DAT_0a3a5530_1._5_1_ = s_my_group_nicknammessage_subtype_088053a0[0x16];
    DAT_0a3a5530_1._6_1_ = s_my_group_nicknammessage_subtype_088053a0[0x17];
    DAT_0a3a5540 = 1;
  }
  sVar2 = _strlen(&DAT_0a3a5530);
  if (0x7ffffffffffffff7 < sVar2) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(ppppuVar3);
  }
  if (sVar2 < 0x17) {
    local_c0 = CONCAT17((char)sVar2,(undefined7)local_c0);
    if (sVar2 == 0) goto LAB_0291d2b8;
  }
  else {
    uVar1 = 0x19;
    if ((sVar2 | 7) != 0x17) {
      uVar1 = (sVar2 | 7) + 1;
    }
    ppppuVar3 = (undefined8 ****)__Znwm(uVar1);
    local_c0 = uVar1 | 0x8000000000000000;
    local_d0 = ppppuVar3;
    local_c8 = sVar2;
  }
  _memcpy(ppppuVar3,&DAT_0a3a5530,sVar2);
LAB_0291d2b8:
  *(undefined1 *)((long)ppppuVar3 + sVar2) = 0;
  FUN_0029ae04(param_1 + 0x18,&local_130,5);
  if ((long)local_c0 < 0) {
    __ZdlPvm(local_d0,local_c0 & 0x7fffffffffffffff);
  }
  if ((long)local_d8 < 0) {
    __ZdlPvm(local_e8,local_d8 & 0x7fffffffffffffff);
  }
  if ((long)local_f0 < 0) {
    __ZdlPvm(local_100,local_f0 & 0x7fffffffffffffff);
  }
  if ((long)local_108 < 0) {
    __ZdlPvm(local_118,local_108 & 0x7fffffffffffffff);
  }
  if ((long)local_120 < 0) {
    __ZdlPvm(local_130,local_120 & 0x7fffffffffffffff);
  }
  if ((long)local_78 < 0) {
    __ZdlPvm(local_88,local_78 & 0x7fffffffffffffff);
  }
  if ((long)local_90 < 0) {
    __ZdlPvm(local_a0,local_90 & 0x7fffffffffffffff);
  }
  if ((long)local_a8 < 0) {
    __ZdlPvm(local_b8,local_a8 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_70) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


