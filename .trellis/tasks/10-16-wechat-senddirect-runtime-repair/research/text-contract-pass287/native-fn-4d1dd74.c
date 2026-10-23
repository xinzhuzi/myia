// Ghidra inferred pseudocode; requested=0x4d1dd74
// entry=04d1dd74 end=04d1eb67

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_04d1dd74(undefined8 *param_1,long *param_2)

{
  undefined8 *******pppppppuVar1;
  int iVar2;
  undefined *puVar3;
  ulong uVar4;
  long *plVar5;
  undefined **local_2e0 [4];
  undefined1 *puStack_2c0;
  undefined1 *local_2b8;
  undefined1 *puStack_2b0;
  undefined1 *local_2a8;
  undefined1 *puStack_2a0;
  undefined1 *local_298;
  undefined1 *puStack_290;
  undefined1 *local_288;
  undefined1 *puStack_280;
  undefined1 *local_278;
  undefined **ppuStack_270;
  undefined1 *local_268;
  undefined1 *puStack_260;
  undefined1 *local_258;
  undefined1 *puStack_250;
  undefined1 *local_248;
  undefined1 *puStack_240;
  undefined1 *local_238;
  undefined1 *puStack_230;
  undefined1 *local_228;
  undefined1 *puStack_220;
  undefined1 *local_218;
  undefined1 *puStack_210;
  undefined1 *local_208;
  undefined1 *puStack_200;
  undefined1 *local_1f8;
  undefined1 *puStack_1f0;
  undefined1 *local_1e8;
  undefined1 *puStack_1e0;
  undefined8 *******local_1d8 [2];
  undefined7 local_1c8;
  char cStack_1c1;
  undefined1 *local_1c0;
  undefined1 *local_1b8;
  undefined1 *local_1b0;
  undefined1 *puStack_1a8;
  undefined1 *local_1a0;
  undefined1 *puStack_198;
  undefined1 *puStack_190;
  undefined1 *puStack_188;
  undefined1 *local_180;
  undefined1 *puStack_178;
  undefined1 *puStack_170;
  undefined1 *puStack_168;
  undefined1 *local_160;
  undefined1 *puStack_158;
  undefined1 *puStack_150;
  undefined1 *puStack_148;
  undefined1 *local_140;
  undefined1 *puStack_138;
  undefined1 *puStack_130;
  undefined1 *puStack_128;
  undefined1 *local_120;
  undefined1 *puStack_118;
  undefined1 *puStack_110;
  undefined1 *puStack_108;
  undefined1 *local_100;
  undefined1 *puStack_f8;
  undefined1 *puStack_f0;
  undefined1 *puStack_e8;
  undefined8 local_e0;
  undefined8 uStack_d8;
  undefined8 uStack_d0;
  undefined8 uStack_c8;
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
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  puStack_f8 = &SUB_aaaaaaaaaaaaaaaa;
  local_100 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_e8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_f0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_118 = &SUB_aaaaaaaaaaaaaaaa;
  local_120 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_108 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_110 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_138 = &SUB_aaaaaaaaaaaaaaaa;
  local_140 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_128 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_130 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_158 = &SUB_aaaaaaaaaaaaaaaa;
  local_160 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_148 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_150 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_178 = &SUB_aaaaaaaaaaaaaaaa;
  local_180 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_168 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_170 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_198 = &SUB_aaaaaaaaaaaaaaaa;
  local_1a0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_188 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_190 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1a8 = &SUB_aaaaaaaaaaaaaaaa;
  local_1b0 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0572111c(&local_1b0);
  if ((DAT_0a4b0a82 & 1) == 0) {
    DAT_0a4b0a78._0_1_ = s_msgsourcsvri_08507770[0];
    DAT_0a4b0a78._1_1_ = s_msgsourcsvri_08507770[1];
    DAT_0a4b0a78._2_1_ = s_msgsourcsvri_08507770[2];
    DAT_0a4b0a78._3_1_ = s_msgsourcsvri_08507770[3];
    DAT_0a4b0a78._4_1_ = s_msgsourcsvri_08507770[4];
    DAT_0a4b0a78._5_1_ = s_msgsourcsvri_08507770[5];
    DAT_0a4b0a78._6_1_ = s_msgsourcsvri_08507770[6];
    DAT_0a4b0a78._7_1_ = s_msgsourcsvri_08507770[7];
    DAT_0a4b0a80 = 0x65;
    DAT_0a4b0a82 = 1;
  }
  local_1b8 = &SUB_aaaaaaaaaaaaaaaa;
  local_1b8 = (undefined1 *)FUN_0571d610(&local_1b0,&DAT_0a4b0a78);
  if (*(char *)((long)param_2 + 0x2f) < '\0') {
    if (param_2[4] != 0) goto LAB_04d1de34;
  }
  else if (*(char *)((long)param_2 + 0x2f) != '\0') {
LAB_04d1de34:
    local_2e0[0] = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
    if ((DAT_0a4b0aab & 1) == 0) {
      DAT_0a4b0aa0._0_1_ = s_atuserliimg_filealno_08ade0b8[0];
      DAT_0a4b0aa0._1_1_ = s_atuserliimg_filealno_08ade0b8[1];
      DAT_0a4b0aa0._2_1_ = s_atuserliimg_filealno_08ade0b8[2];
      DAT_0a4b0aa0._3_1_ = s_atuserliimg_filealno_08ade0b8[3];
      DAT_0a4b0aa0._4_1_ = s_atuserliimg_filealno_08ade0b8[4];
      DAT_0a4b0aa0._5_1_ = s_atuserliimg_filealno_08ade0b8[5];
      DAT_0a4b0aa0._6_1_ = s_atuserliimg_filealno_08ade0b8[6];
      DAT_0a4b0aa0._7_1_ = s_atuserliimg_filealno_08ade0b8[7];
      DAT_0a4b0aa8 = 0x7473;
      DAT_0a4b0aaa = 0;
      DAT_0a4b0aab = 1;
    }
    local_2e0[0] = (undefined **)FUN_0571d610(&local_1b8,&DAT_0a4b0aa0);
    uVar4 = FUN_04af2fcc(local_2e0);
    if ((uVar4 & 1) == 0) {
      local_e0 = FUN_0008a8b8(local_2e0);
      plVar5 = param_2 + 3;
      if (*(char *)((long)param_2 + 0x2f) < '\0') {
        plVar5 = (long *)*plVar5;
      }
      FUN_05720378(&local_e0,plVar5);
    }
  }
  if (*(char *)((long)param_2 + 0x47) < '\0') {
    if (param_2[7] != 0) goto LAB_04d1decc;
  }
  else if (*(char *)((long)param_2 + 0x47) != '\0') {
LAB_04d1decc:
    local_2e0[0] = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
    if ((DAT_0a4b0abe & 1) == 0) {
      DAT_0a4b0ab0._0_1_ = s_atuserliimg_filealno_08ade0b8[8];
      DAT_0a4b0ab0._1_1_ = s_atuserliimg_filealno_08ade0b8[9];
      DAT_0a4b0ab0._2_1_ = s_atuserliimg_filealno_08ade0b8[10];
      DAT_0a4b0ab0._3_1_ = s_atuserliimg_filealno_08ade0b8[0xb];
      DAT_0a4b0ab0._4_1_ = s_atuserliimg_filealno_08ade0b8[0xc];
      DAT_0a4b0ab0._5_1_ = s_atuserliimg_filealno_08ade0b8[0xd];
      DAT_0a4b0ab0._6_1_ = s_atuserliimg_filealno_08ade0b8[0xe];
      DAT_0a4b0ab0._7_1_ = s_atuserliimg_filealno_08ade0b8[0xf];
      DAT_0a4b0ab8 = (undefined4)DAT_084892f8;
      DAT_0a4b0abc = 0x65;
      DAT_0a4b0abe = 1;
    }
    local_2e0[0] = (undefined **)FUN_0571d610(&local_1b8,&DAT_0a4b0ab0);
    uVar4 = FUN_04af2fcc(local_2e0);
    if ((uVar4 & 1) == 0) {
      local_e0 = FUN_0008a8b8(local_2e0);
      plVar5 = param_2 + 6;
      if (*(char *)((long)param_2 + 0x47) < '\0') {
        plVar5 = (long *)*plVar5;
      }
      FUN_05720378(&local_e0,plVar5);
    }
  }
  if (param_2[9] != 0) {
    local_2e0[0] = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
    if ((DAT_0a4b0ac7 & 1) == 0) {
      DAT_0a4b0ac0 = (undefined4)ram0x08ade0c8;
      DAT_0a4b0ac4 = 0x6564;
      DAT_0a4b0ac6 = 0;
      DAT_0a4b0ac7 = 1;
    }
    local_2e0[0] = (undefined **)FUN_0571d610(&local_1b8,&DAT_0a4b0ac0);
    FUN_04d1b7e4(param_2[9],local_2e0);
  }
  if (param_2[0xb] != 0) {
    local_2e0[0] = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
    if ((DAT_0a4b0ad5 & 1) == 0) {
      DAT_0a4b0ac8._0_1_ = s_newmsgidsec_msg_bubble_tpreview__088babb8[8];
      DAT_0a4b0ac8._1_1_ = s_newmsgidsec_msg_bubble_tpreview__088babb8[9];
      DAT_0a4b0ac8._2_1_ = s_newmsgidsec_msg_bubble_tpreview__088babb8[10];
      DAT_0a4b0ac8._3_1_ = s_newmsgidsec_msg_bubble_tpreview__088babb8[0xb];
      DAT_0a4b0ac8._4_1_ = s_newmsgidsec_msg_bubble_tpreview__088babb8[0xc];
      DAT_0a4b0ac8._5_1_ = s_newmsgidsec_msg_bubble_tpreview__088babb8[0xd];
      DAT_0a4b0ac8._6_1_ = s_newmsgidsec_msg_bubble_tpreview__088babb8[0xe];
      DAT_0a4b0ac8._7_1_ = s_newmsgidsec_msg_bubble_tpreview__088babb8[0xf];
      DAT_0a4b0ad0 = (undefined4)DAT_084d78a8;
      DAT_0a4b0ad4 = 0;
      DAT_0a4b0ad5 = 1;
    }
    local_2e0[0] = (undefined **)FUN_0571d610(&local_1b8,&DAT_0a4b0ac8);
    FUN_04d1b8f4(param_2[0xb],local_2e0);
  }
  if (param_2[0xd] != 0) {
    local_2e0[0] = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
    if ((DAT_0a4b0ae2 & 1) == 0) {
      DAT_0a4b0ad8._0_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[0];
      DAT_0a4b0ad8._1_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[1];
      DAT_0a4b0ad8._2_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[2];
      DAT_0a4b0ad8._3_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[3];
      DAT_0a4b0ad8._4_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[4];
      DAT_0a4b0ad8._5_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[5];
      DAT_0a4b0ad8._6_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[6];
      DAT_0a4b0ad8._7_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[7];
      DAT_0a4b0ae0 = 0x67;
      DAT_0a4b0ae2 = 1;
    }
    local_2e0[0] = (undefined **)FUN_0571d610(&local_1b8,&DAT_0a4b0ad8);
    FUN_04d1bbcc(param_2[0xd],local_2e0);
  }
  if (param_2[0xf] != 0) {
    local_1d8[0] = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
    if ((DAT_0a4b0af4 & 1) == 0) {
      DAT_0a4b0ae8._0_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[8];
      DAT_0a4b0ae8._1_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[9];
      DAT_0a4b0ae8._2_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[10];
      DAT_0a4b0ae8._3_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[0xb];
      DAT_0a4b0ae8._4_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[0xc];
      DAT_0a4b0ae8._5_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[0xd];
      DAT_0a4b0ae8._6_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[0xe];
      DAT_0a4b0ae8._7_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[0xf];
      DAT_0a4b0af0 = (undefined4)ram0x087287c8;
      DAT_0a4b0af4 = 1;
    }
    local_1d8[0] = (undefined8 *******)FUN_0571d610(&local_1b8,&DAT_0a4b0ae8);
    plVar5 = (long *)param_2[0xf];
    if (*(char *)((long)plVar5 + 0x17) < '\0') {
      if (plVar5[1] != 0) goto LAB_04d1e0f4;
    }
    else if (*(char *)((long)plVar5 + 0x17) != '\0') {
LAB_04d1e0f4:
      if ((DAT_0a4b0991 & 1) == 0) {
        DAT_0a4b0988._0_1_ = s_sec_hashqy_msg_tuser_typbizchat__08ade080[0];
        DAT_0a4b0988._1_1_ = s_sec_hashqy_msg_tuser_typbizchat__08ade080[1];
        DAT_0a4b0988._2_1_ = s_sec_hashqy_msg_tuser_typbizchat__08ade080[2];
        DAT_0a4b0988._3_1_ = s_sec_hashqy_msg_tuser_typbizchat__08ade080[3];
        DAT_0a4b0988._4_1_ = s_sec_hashqy_msg_tuser_typbizchat__08ade080[4];
        DAT_0a4b0988._5_1_ = s_sec_hashqy_msg_tuser_typbizchat__08ade080[5];
        DAT_0a4b0988._6_1_ = s_sec_hashqy_msg_tuser_typbizchat__08ade080[6];
        DAT_0a4b0988._7_1_ = s_sec_hashqy_msg_tuser_typbizchat__08ade080[7];
        DAT_0a4b0990 = 0;
        DAT_0a4b0991 = 1;
      }
      local_e0 = FUN_0571d610(local_1d8,&DAT_0a4b0988);
      local_2e0[0] = (undefined **)FUN_0008a8b8(&local_e0);
      if (*(char *)((long)plVar5 + 0x17) < '\0') {
        plVar5 = (long *)*plVar5;
      }
      FUN_05720378(local_2e0,plVar5);
    }
  }
  if (param_2[0x11] != 0) {
    local_2e0[0] = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
    if ((DAT_0a4b0b01 & 1) == 0) {
      DAT_0a4b0af8._0_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[0x10];
      DAT_0a4b0af8._1_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[0x11];
      DAT_0a4b0af8._2_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[0x12];
      DAT_0a4b0af8._3_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[0x13];
      DAT_0a4b0af8._4_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[0x14];
      DAT_0a4b0af8._5_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[0x15];
      DAT_0a4b0af8._6_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[0x16];
      DAT_0a4b0af8._7_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[0x17];
      DAT_0a4b0b00 = 0;
      DAT_0a4b0b01 = 1;
    }
    local_2e0[0] = (undefined **)FUN_0571d610(&local_1b8,&DAT_0a4b0af8);
    FUN_04d1bd38(param_2[0x11],local_2e0);
  }
  if (param_2[0x13] != 0) {
    local_2e0[0] = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
    if ((DAT_0a4b0b20 & 1) == 0) {
      uRam000000000a4b0b18._0_1_ = s_message_source_centerprise_info_08ade140[0x18];
      uRam000000000a4b0b18._1_1_ = s_message_source_centerprise_info_08ade140[0x19];
      uRam000000000a4b0b18._2_1_ = s_message_source_centerprise_info_08ade140[0x1a];
      uRam000000000a4b0b18._3_1_ = s_message_source_centerprise_info_08ade140[0x1b];
      uRam000000000a4b0b18._4_1_ = s_message_source_centerprise_info_08ade140[0x1c];
      uRam000000000a4b0b18._5_1_ = s_message_source_centerprise_info_08ade140[0x1d];
      uRam000000000a4b0b18._6_1_ = s_message_source_centerprise_info_08ade140[0x1e];
      uRam000000000a4b0b18._7_1_ = s_message_source_centerprise_info_08ade140[0x1f];
      DAT_0a4b0b10 = s_message_source_centerprise_info_08ade140[0x10];
      DAT_0a4b0b10_1._0_1_ = s_message_source_centerprise_info_08ade140[0x11];
      DAT_0a4b0b10_1._1_1_ = s_message_source_centerprise_info_08ade140[0x12];
      DAT_0a4b0b10_1._2_1_ = s_message_source_centerprise_info_08ade140[0x13];
      DAT_0a4b0b10_1._3_1_ = s_message_source_centerprise_info_08ade140[0x14];
      DAT_0a4b0b10_1._4_1_ = s_message_source_centerprise_info_08ade140[0x15];
      DAT_0a4b0b10_1._5_1_ = s_message_source_centerprise_info_08ade140[0x16];
      DAT_0a4b0b10_1._6_1_ = s_message_source_centerprise_info_08ade140[0x17];
      DAT_0a4b0b20 = 1;
    }
    local_2e0[0] = (undefined **)FUN_0571d610(&local_1b8,&DAT_0a4b0b10);
    FUN_04d1bf44(param_2[0x13],local_2e0);
  }
  if (*(char *)((long)param_2 + 0x17) < '\0') {
    if (param_2[1] != 0) goto LAB_04d1e220;
  }
  else if (*(char *)((long)param_2 + 0x17) != '\0') {
LAB_04d1e220:
    local_2e0[0] = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
    if ((DAT_0a4b0b2a & 1) == 0) {
      DAT_0a4b0b24 = (undefined4)DAT_084937d0;
      DAT_0a4b0b28 = 100;
      DAT_0a4b0b2a = 1;
    }
    local_2e0[0] = (undefined **)FUN_0571d610(&local_1b8,&DAT_0a4b0b24);
    uVar4 = FUN_04af2fcc(local_2e0);
    if ((uVar4 & 1) == 0) {
      local_e0 = FUN_0008a8b8(local_2e0);
      plVar5 = param_2;
      if (*(char *)((long)param_2 + 0x17) < '\0') {
        plVar5 = (long *)*param_2;
      }
      FUN_05720378(&local_e0,plVar5);
    }
  }
  if ((int)param_2[0x17] != 0) {
    local_2e0[0] = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
    if ((DAT_0a4b0b42 & 1) == 0) {
      uVar4 = 0;
      do {
        (&DAT_0a4b0b2b)[uVar4] = (&DAT_08ade77f)[uVar4] + 0x8a ^ (&DAT_08ade76f)[uVar4 & 0xf];
        uVar4 = uVar4 + 1;
      } while (uVar4 != 0x17);
      DAT_0a4b0b42 = 1;
    }
    local_2e0[0] = (undefined **)FUN_0571d610(&local_1b8,&DAT_0a4b0b2b);
    uVar4 = FUN_04af2fcc(local_2e0);
    if ((uVar4 & 1) == 0) {
      local_e0 = FUN_0008a8b8(local_2e0);
      FUN_057203c8(&local_e0,(int)param_2[0x17]);
    }
  }
  if (*(char *)((long)param_2 + 0xcc) == '\x01') {
    local_1c0 = &SUB_aaaaaaaaaaaaaaaa;
    if ((DAT_0a4b0b5a & 1) == 0) {
      uVar4 = 0;
      do {
        (&DAT_0a4b0b43)[uVar4] = (&DAT_08ade7a6)[uVar4] + 0x8a ^ (&DAT_08ade796)[uVar4 & 0xf];
        uVar4 = uVar4 + 1;
      } while (uVar4 != 0x17);
      DAT_0a4b0b5a = 1;
    }
    local_1c0 = (undefined1 *)FUN_0571d610(&local_1b8,&DAT_0a4b0b43);
    uVar4 = FUN_04af2fcc(&local_1c0);
    if ((uVar4 & 1) == 0) {
      local_2e0[0] = (undefined **)FUN_0008a8b8(&local_1c0);
      FUN_057203c8(local_2e0,*(undefined1 *)((long)param_2 + 0xcc));
    }
    else {
      iVar2 = thunk_FUN_05e1d97c(4);
      if (iVar2 != 0) {
        FUN_0488143c(local_1d8);
        pppppppuVar1 = local_1d8[0];
        if (-1 < cStack_1c1) {
          pppppppuVar1 = local_1d8;
        }
        if ((DAT_0a4b0a42 & 1) == 0) {
          uRam000000000a4b0a38._0_1_ = s_message_source_centerprise_info_08ade140[8];
          uRam000000000a4b0a38._1_1_ = s_message_source_centerprise_info_08ade140[9];
          uRam000000000a4b0a38._2_1_ = s_message_source_centerprise_info_08ade140[10];
          uRam000000000a4b0a38._3_1_ = s_message_source_centerprise_info_08ade140[0xb];
          uRam000000000a4b0a38._4_1_ = s_message_source_centerprise_info_08ade140[0xc];
          uRam000000000a4b0a38._5_1_ = s_message_source_centerprise_info_08ade140[0xd];
          uRam000000000a4b0a38._6_1_ = s_message_source_centerprise_info_08ade140[0xe];
          uRam000000000a4b0a38._7_1_ = s_message_source_centerprise_info_08ade140[0xf];
          DAT_0a4b0a30 = s_message_source_centerprise_info_08ade140[0];
          DAT_0a4b0a30_1._0_1_ = s_message_source_centerprise_info_08ade140[1];
          DAT_0a4b0a30_1._1_1_ = s_message_source_centerprise_info_08ade140[2];
          DAT_0a4b0a30_1._2_1_ = s_message_source_centerprise_info_08ade140[3];
          DAT_0a4b0a30_1._3_1_ = s_message_source_centerprise_info_08ade140[4];
          DAT_0a4b0a30_1._4_1_ = s_message_source_centerprise_info_08ade140[5];
          DAT_0a4b0a30_1._5_1_ = s_message_source_centerprise_info_08ade140[6];
          DAT_0a4b0a30_1._6_1_ = s_message_source_centerprise_info_08ade140[7];
          DAT_0a4b0a40 = 99;
          DAT_0a4b0a42 = 1;
        }
        if ((DAT_0a4b0cd4 & 1) == 0) {
          DAT_0a4b0cc8._0_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x18];
          DAT_0a4b0cc8._1_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x19];
          DAT_0a4b0cc8._2_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x1a];
          DAT_0a4b0cc8._3_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x1b];
          DAT_0a4b0cc8._4_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x1c];
          DAT_0a4b0cc8._5_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x1d];
          DAT_0a4b0cc8._6_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x1e];
          DAT_0a4b0cc8._7_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x1f];
          DAT_0a4b0cd0 = (undefined4)DAT_08824c28;
          DAT_0a4b0cd4 = 1;
        }
        FUN_05e1d050(local_2e0,4,pppppppuVar1,&DAT_0a4b0a30,&DAT_0a4b0cc8,0x1c4,0,0);
        if ((DAT_0a4b0cea & 1) == 0) {
          uVar4 = 0;
          do {
            (&DAT_0a4b0cd5)[uVar4] = (&DAT_08adea27)[uVar4] + 0x8a ^ (&DAT_08adea17)[uVar4 & 0xf];
            uVar4 = uVar4 + 1;
          } while (uVar4 != 0x15);
          DAT_0a4b0cea = 1;
        }
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
        uStack_d8 = 0;
        local_e0 = 0;
        uStack_c8 = 0;
        uStack_d0 = 0;
        FUN_05e1d31c(local_2e0,&DAT_0a4b0cd5,&local_e0);
        thunk_FUN_05e1d0bc(local_2e0);
        if (cStack_1c1 < '\0') {
          __ZdlPvm(local_1d8[0],CONCAT17(cStack_1c1,local_1c8) & 0x7fffffffffffffff);
        }
      }
    }
  }
  if (*(char *)((long)param_2 + 0xcd) == '\x01') {
    local_1c0 = &SUB_aaaaaaaaaaaaaaaa;
    if ((DAT_0a4b0b83 & 1) == 0) {
      uVar4 = 0;
      do {
        (&DAT_0a4b0b5b)[uVar4] = (&DAT_08ade7cd)[uVar4] + 0x8a ^ (&DAT_08ade7bd)[uVar4 & 0xf];
        uVar4 = uVar4 + 1;
      } while (uVar4 != 0x28);
      DAT_0a4b0b83 = 1;
    }
    local_1c0 = (undefined1 *)FUN_0571d610(&local_1b8,&DAT_0a4b0b5b);
    uVar4 = FUN_04af2fcc(&local_1c0);
    if ((uVar4 & 1) == 0) {
      local_2e0[0] = (undefined **)FUN_0008a8b8(&local_1c0);
      FUN_057203c8(local_2e0,*(undefined1 *)((long)param_2 + 0xcd));
    }
    else {
      iVar2 = thunk_FUN_05e1d97c(4);
      if (iVar2 != 0) {
        FUN_0488143c(local_1d8);
        pppppppuVar1 = local_1d8[0];
        if (-1 < cStack_1c1) {
          pppppppuVar1 = local_1d8;
        }
        if ((DAT_0a4b0a42 & 1) == 0) {
          uRam000000000a4b0a38._0_1_ = s_message_source_centerprise_info_08ade140[8];
          uRam000000000a4b0a38._1_1_ = s_message_source_centerprise_info_08ade140[9];
          uRam000000000a4b0a38._2_1_ = s_message_source_centerprise_info_08ade140[10];
          uRam000000000a4b0a38._3_1_ = s_message_source_centerprise_info_08ade140[0xb];
          uRam000000000a4b0a38._4_1_ = s_message_source_centerprise_info_08ade140[0xc];
          uRam000000000a4b0a38._5_1_ = s_message_source_centerprise_info_08ade140[0xd];
          uRam000000000a4b0a38._6_1_ = s_message_source_centerprise_info_08ade140[0xe];
          uRam000000000a4b0a38._7_1_ = s_message_source_centerprise_info_08ade140[0xf];
          DAT_0a4b0a30 = s_message_source_centerprise_info_08ade140[0];
          DAT_0a4b0a30_1._0_1_ = s_message_source_centerprise_info_08ade140[1];
          DAT_0a4b0a30_1._1_1_ = s_message_source_centerprise_info_08ade140[2];
          DAT_0a4b0a30_1._2_1_ = s_message_source_centerprise_info_08ade140[3];
          DAT_0a4b0a30_1._3_1_ = s_message_source_centerprise_info_08ade140[4];
          DAT_0a4b0a30_1._4_1_ = s_message_source_centerprise_info_08ade140[5];
          DAT_0a4b0a30_1._5_1_ = s_message_source_centerprise_info_08ade140[6];
          DAT_0a4b0a30_1._6_1_ = s_message_source_centerprise_info_08ade140[7];
          DAT_0a4b0a40 = 99;
          DAT_0a4b0a42 = 1;
        }
        if ((DAT_0a4b0cd4 & 1) == 0) {
          DAT_0a4b0cc8._0_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x18];
          DAT_0a4b0cc8._1_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x19];
          DAT_0a4b0cc8._2_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x1a];
          DAT_0a4b0cc8._3_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x1b];
          DAT_0a4b0cc8._4_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x1c];
          DAT_0a4b0cc8._5_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x1d];
          DAT_0a4b0cc8._6_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x1e];
          DAT_0a4b0cc8._7_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x1f];
          DAT_0a4b0cd0 = (undefined4)DAT_08824c28;
          DAT_0a4b0cd4 = 1;
        }
        FUN_05e1d050(local_2e0,4,pppppppuVar1,&DAT_0a4b0a30,&DAT_0a4b0cc8,0x1cd,0,0);
        if ((DAT_0a4b0d02 & 1) == 0) {
          uRam000000000a4b0cf8._0_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[0x18];
          uRam000000000a4b0cf8._1_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[0x19];
          uRam000000000a4b0cf8._2_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[0x1a];
          uRam000000000a4b0cf8._3_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[0x1b];
          uRam000000000a4b0cf8._4_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[0x1c];
          uRam000000000a4b0cf8._5_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[0x1d];
          uRam000000000a4b0cf8._6_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[0x1e];
          uRam000000000a4b0cf8._7_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[0x1f];
          DAT_0a4b0cf0 = s_msg_cluster_typenew_node_is_empt_08ade190[0x10];
          DAT_0a4b0cf0_1._0_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[0x11];
          DAT_0a4b0cf0_1._1_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[0x12];
          DAT_0a4b0cf0_1._2_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[0x13];
          DAT_0a4b0cf0_1._3_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[0x14];
          DAT_0a4b0cf0_1._4_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[0x15];
          DAT_0a4b0cf0_1._5_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[0x16];
          DAT_0a4b0cf0_1._6_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[0x17];
          DAT_0a4b0d00 = 0x79;
          DAT_0a4b0d02 = 1;
        }
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
        uStack_d8 = 0;
        local_e0 = 0;
        uStack_c8 = 0;
        uStack_d0 = 0;
        FUN_05e1d31c(local_2e0,&DAT_0a4b0cf0,&local_e0);
        thunk_FUN_05e1d0bc(local_2e0);
        if (cStack_1c1 < '\0') {
          __ZdlPvm(local_1d8[0],CONCAT17(cStack_1c1,local_1c8) & 0x7fffffffffffffff);
        }
      }
    }
  }
  if (*(int *)((long)param_2 + 0xbc) != 0) {
    local_2e0[0] = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
    if ((DAT_0a4b0b8a & 1) == 0) {
      DAT_0a4b0b84 = (undefined4)DAT_084cc038;
      DAT_0a4b0b88 = 0x65;
      DAT_0a4b0b8a = 1;
    }
    local_2e0[0] = (undefined **)FUN_0571d610(&local_1b8,&DAT_0a4b0b84);
    uVar4 = FUN_04af2fcc(local_2e0);
    if ((uVar4 & 1) == 0) {
      local_e0 = FUN_0008a8b8(local_2e0);
      FUN_057203c8(&local_e0,*(undefined4 *)((long)param_2 + 0xbc));
    }
  }
  if ((int)param_2[0x18] != 0) {
    local_2e0[0] = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
    if ((DAT_0a4b0b98 & 1) == 0) {
      DAT_0a4b0b90._0_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[0x18];
      DAT_0a4b0b90._1_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[0x19];
      DAT_0a4b0b90._2_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[0x1a];
      DAT_0a4b0b90._3_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[0x1b];
      DAT_0a4b0b90._4_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[0x1c];
      DAT_0a4b0b90._5_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[0x1d];
      DAT_0a4b0b90._6_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[0x1e];
      DAT_0a4b0b90._7_1_ = s_share_mspassthrotmp_nodebizflag_08ade0d0[0x1f];
      DAT_0a4b0b98 = 1;
    }
    local_2e0[0] = (undefined **)FUN_0571d610(&local_1b8,&DAT_0a4b0b90);
    uVar4 = FUN_04af2fcc(local_2e0);
    if ((uVar4 & 1) == 0) {
      local_e0 = FUN_0008a8b8(local_2e0);
      FUN_057204a4(&local_e0,(int)param_2[0x18]);
    }
  }
  if ((char)param_2[0x19] == '\x01') {
    local_2e0[0] = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
    if ((DAT_0a4b0c91 & 1) == 0) {
      uRam000000000a4b0c88._0_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[8];
      uRam000000000a4b0c88._1_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[9];
      uRam000000000a4b0c88._2_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[10];
      uRam000000000a4b0c88._3_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[0xb];
      uRam000000000a4b0c88._4_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[0xc];
      uRam000000000a4b0c88._5_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[0xd];
      uRam000000000a4b0c88._6_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[0xe];
      uRam000000000a4b0c88._7_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[0xf];
      DAT_0a4b0c80 = s_msg_cluster_typenew_node_is_empt_08ade190[0];
      DAT_0a4b0c80_1._0_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[1];
      DAT_0a4b0c80_1._1_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[2];
      DAT_0a4b0c80_1._2_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[3];
      DAT_0a4b0c80_1._3_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[4];
      DAT_0a4b0c80_1._4_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[5];
      DAT_0a4b0c80_1._5_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[6];
      DAT_0a4b0c80_1._6_1_ = s_msg_cluster_typenew_node_is_empt_08ade190[7];
      DAT_0a4b0c90 = 0;
      DAT_0a4b0c91 = 1;
    }
    local_2e0[0] = (undefined **)FUN_0571d610(&local_1b8,&DAT_0a4b0c80);
    uVar4 = FUN_04af2fcc(local_2e0);
    if ((uVar4 & 1) == 0) {
      local_e0 = FUN_0008a8b8(local_2e0);
      if ((*(byte *)(param_2 + 0x19) & 1) == 0) {
                    /* WARNING: Subroutine does not return */
        FUN_004d04d4();
      }
      FUN_057203c8(&local_e0,*(undefined4 *)((long)param_2 + 0xc4));
    }
  }
  if (*(char *)((long)param_2 + 0xe7) < '\0') {
    if (param_2[0x1b] == 0) goto LAB_04d1e8f8;
  }
  else if (*(char *)((long)param_2 + 0xe7) == '\0') goto LAB_04d1e8f8;
  local_2e0[0] = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
  if ((DAT_0a4b0ca3 & 1) == 0) {
    DAT_0a4b0c98._0_1_ = s_kefumenuclas_08598af8[0];
    DAT_0a4b0c98._1_1_ = s_kefumenuclas_08598af8[1];
    DAT_0a4b0c98._2_1_ = s_kefumenuclas_08598af8[2];
    DAT_0a4b0c98._3_1_ = s_kefumenuclas_08598af8[3];
    DAT_0a4b0c98._4_1_ = s_kefumenuclas_08598af8[4];
    DAT_0a4b0c98._5_1_ = s_kefumenuclas_08598af8[5];
    DAT_0a4b0c98._6_1_ = s_kefumenuclas_08598af8[6];
    DAT_0a4b0c98._7_1_ = s_kefumenuclas_08598af8[7];
    DAT_0a4b0ca0 = 0x6469;
    DAT_0a4b0ca2 = 0;
    DAT_0a4b0ca3 = 1;
  }
  local_2e0[0] = (undefined **)FUN_0571d610(&local_1b8,&DAT_0a4b0c98);
  uVar4 = FUN_04af2fcc(local_2e0);
  if ((uVar4 & 1) == 0) {
    local_e0 = FUN_0008a8b8(local_2e0);
    plVar5 = param_2 + 0x1a;
    if (*(char *)((long)param_2 + 0xe7) < '\0') {
      plVar5 = (long *)*plVar5;
    }
    FUN_05720378(&local_e0,plVar5);
  }
LAB_04d1e8f8:
  if ((char)param_2[0x21] == '\x01') {
    if ((DAT_0a4b0cb6 & 1) == 0) {
      DAT_0a4b0ca8._0_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[8];
      DAT_0a4b0ca8._1_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[9];
      DAT_0a4b0ca8._2_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[10];
      DAT_0a4b0ca8._3_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0xb];
      DAT_0a4b0ca8._4_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0xc];
      DAT_0a4b0ca8._5_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0xd];
      DAT_0a4b0ca8._6_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0xe];
      DAT_0a4b0ca8._7_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0xf];
      DAT_0a4b0cb0 = (undefined4)ram0x087b86e0;
      DAT_0a4b0cb4 = 0x67;
      DAT_0a4b0cb6 = 1;
    }
    local_e0 = FUN_0571d610(&local_1b8,&DAT_0a4b0ca8);
    local_2e0[0] = (undefined **)FUN_0008a8b8(&local_e0);
    FUN_057203c8(local_2e0,(char)param_2[0x21]);
  }
  if (param_2[0x15] != 0) {
    if ((DAT_0a4b0cc4 & 1) == 0) {
      DAT_0a4b0cb8._0_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x10];
      DAT_0a4b0cb8._1_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x11];
      DAT_0a4b0cb8._2_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x12];
      DAT_0a4b0cb8._3_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x13];
      DAT_0a4b0cb8._4_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x14];
      DAT_0a4b0cb8._5_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x15];
      DAT_0a4b0cb8._6_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x16];
      DAT_0a4b0cb8._7_1_ = s_cdnvideogreetingmsg_wordEncodeTo_08ade108[0x17];
      DAT_0a4b0cc0 = (undefined4)DAT_084a2f38;
      DAT_0a4b0cc4 = 1;
    }
    local_2e0[0] = (undefined **)FUN_0571d610(&local_1b8,&DAT_0a4b0cb8);
    FUN_04d1ecdc(param_2[0x15],local_2e0);
  }
  local_278 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1e0 = &SUB_aaaaaaaaaaaaaaaa;
  local_1e8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1f0 = &SUB_aaaaaaaaaaaaaaaa;
  local_1f8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_200 = &SUB_aaaaaaaaaaaaaaaa;
  local_208 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_210 = &SUB_aaaaaaaaaaaaaaaa;
  local_218 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_220 = &SUB_aaaaaaaaaaaaaaaa;
  local_228 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_230 = &SUB_aaaaaaaaaaaaaaaa;
  local_238 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_240 = &SUB_aaaaaaaaaaaaaaaa;
  local_248 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_250 = &SUB_aaaaaaaaaaaaaaaa;
  local_258 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_260 = &SUB_aaaaaaaaaaaaaaaa;
  local_268 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_280 = &SUB_aaaaaaaaaaaaaaaa;
  local_288 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_290 = &SUB_aaaaaaaaaaaaaaaa;
  local_298 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_2a0 = &SUB_aaaaaaaaaaaaaaaa;
  local_2a8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_2b0 = &SUB_aaaaaaaaaaaaaaaa;
  local_2b8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_2c0 = &SUB_aaaaaaaaaaaaaaaa;
  local_2e0[3] = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
  local_2e0[2] = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
  local_2e0[1] = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
  ppuStack_270 = &PTR_FUN_09f46210;
  local_2e0[0] = (undefined **)PTR_PTR_09f46228;
  *(undefined **)((long)local_2e0 + *(long *)(PTR_PTR_09f46228 + -0x18)) = PTR_PTR_09f46230;
  puVar3 = local_2e0[0][-3];
  __ZNSt3__18ios_base4initEPv((undefined *)((long)local_2e0 + (long)puVar3),local_2e0 + 1);
  *(undefined8 *)((long)&local_258 + (long)puVar3) = 0;
  *(undefined4 *)((long)&puStack_250 + (long)puVar3) = 0xffffffff;
  local_2e0[0] = &PTR_FUN_09f461e8;
  ppuStack_270 = &PTR_FUN_09f46210;
  __ZNSt3__115basic_streambufIcNS_11char_traitsIcEEEC2Ev(local_2e0 + 1);
  local_2e0[1] = &PTR_FUN_09f2b5a8;
  puStack_290 = (undefined1 *)0x0;
  local_298 = (undefined1 *)0x0;
  puStack_280 = (undefined1 *)0x0;
  local_288 = (undefined1 *)0x0;
  local_278 = (undefined1 *)CONCAT44(local_278._4_4_,0x10);
  FUN_0571fc9c(&local_1b0,local_2e0,"",4,0,0);
  param_1[1] = &SUB_aaaaaaaaaaaaaaaa;
  param_1[2] = &SUB_aaaaaaaaaaaaaaaa;
  *param_1 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_05f96e3c(param_1,local_2e0 + 1);
  local_2e0[0] = (undefined **)PTR_PTR_09f46220;
  *(undefined **)((long)local_2e0 + *(long *)(PTR_PTR_09f46220 + -0x18)) = PTR_PTR_09f46238;
  local_2e0[1] = &PTR_FUN_09f2b5a8;
  if ((long)local_288 < 0) {
    __ZdlPvm(local_298,(ulong)local_288 & 0x7fffffffffffffff);
  }
  __ZNSt3__115basic_streambufIcNS_11char_traitsIcEEED2Ev(local_2e0 + 1);
  __ZNSt3__113basic_ostreamIcNS_11char_traitsIcEEED2Ev(local_2e0,&PTR_PTR_09f46228);
  __ZNSt3__19basic_iosIcNS_11char_traitsIcEEED2Ev(&ppuStack_270);
  FUN_0572116c(&local_1b0);
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_58) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


