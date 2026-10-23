// Ghidra inferred pseudocode; requested=0x5695028
// entry=05695028 end=056952c3

undefined8 FUN_05695028(long *param_1)

{
  int iVar1;
  ulong uVar2;
  undefined8 uVar3;
  undefined8 *puVar4;
  undefined1 auStack_218 [24];
  undefined1 auStack_200 [64];
  undefined1 *local_1c0;
  undefined1 *puStack_1b8;
  undefined1 *local_1b0;
  undefined1 *puStack_1a8;
  undefined1 *puStack_1a0;
  undefined1 *puStack_198;
  undefined1 *local_190;
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
  undefined1 *local_e0;
  undefined1 *puStack_d8;
  undefined1 *puStack_d0;
  undefined1 *puStack_c8;
  undefined1 *local_c0;
  undefined1 *puStack_b8;
  undefined1 *puStack_b0;
  undefined1 *puStack_a8;
  undefined1 *local_a0;
  undefined1 *puStack_98;
  undefined1 *puStack_90;
  undefined1 *puStack_88;
  undefined1 *local_80;
  undefined1 *puStack_78;
  undefined1 *puStack_70;
  undefined1 *puStack_68;
  undefined1 *local_60;
  undefined1 *puStack_58;
  undefined1 *puStack_50;
  undefined1 *puStack_48;
  
  if ((int)param_1[0x15] < 2) {
    (**(code **)(*param_1 + 0x30))(param_1);
    iVar1 = FUN_058de500(param_1[8]);
    if (iVar1 != 0) {
LAB_05695098:
      param_1[0x15] = 0;
      return 1;
    }
    if (((DAT_0a4d78e8 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_0a4d78e8), iVar1 != 0)) {
      puVar4 = (undefined8 *)__Znwm(0x40);
      FUN_056d1c24(&local_1c0);
      uVar3 = FUN_056d1c60(&local_1c0);
      FUN_056c2744(puVar4,uVar3);
      *puVar4 = &PTR_thunk_FUN_056c2628_09f20c98;
      thunk_FUN_056c2628(&local_1c0);
      DAT_0a4d78e0 = puVar4;
      ___cxa_guard_release(&DAT_0a4d78e8);
    }
    puVar4 = DAT_0a4d78e0;
    puStack_58 = &SUB_aaaaaaaaaaaaaaaa;
    local_60 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_48 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_50 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_78 = &SUB_aaaaaaaaaaaaaaaa;
    local_80 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_68 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_70 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_98 = &SUB_aaaaaaaaaaaaaaaa;
    local_a0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_88 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_90 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_b8 = &SUB_aaaaaaaaaaaaaaaa;
    local_c0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_a8 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_b0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_d8 = &SUB_aaaaaaaaaaaaaaaa;
    local_e0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_c8 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_d0 = &SUB_aaaaaaaaaaaaaaaa;
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
    puStack_188 = &SUB_aaaaaaaaaaaaaaaa;
    local_190 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_1a8 = &SUB_aaaaaaaaaaaaaaaa;
    local_1b0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_198 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_1a0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_1b8 = &SUB_aaaaaaaaaaaaaaaa;
    local_1c0 = &SUB_aaaaaaaaaaaaaaaa;
    thunk_FUN_0569fd80(&local_1c0,param_1);
    uVar2 = FUN_056a0008(&local_1c0,puVar4);
    if ((uVar2 & 1) == 0) {
      thunk_FUN_0569fefc(&local_1c0);
    }
    else {
      iVar1 = FUN_056a14e8(&local_1c0);
      FUN_056a15c0(&local_1c0);
      thunk_FUN_0569fefc(&local_1c0);
      if (iVar1 != 0) goto LAB_05695098;
    }
  }
  else {
    if ((*(int *)((long)param_1 + 0xac) != 0) || (iVar1 = FUN_058de500(param_1[8]), iVar1 != 0)) {
LAB_05695068:
      *(int *)(param_1 + 0x15) = (int)param_1[0x15] + -1;
      return 1;
    }
    FUN_056d7474(auStack_200);
    if ((DAT_0a4d7973 & 1) == 0) {
      DAT_0a4d7968._0_1_ = s__journalwcdb_lv_Invalid_statemen_08b2f560[8];
      DAT_0a4d7968._1_1_ = s__journalwcdb_lv_Invalid_statemen_08b2f560[9];
      DAT_0a4d7968._2_1_ = s__journalwcdb_lv_Invalid_statemen_08b2f560[10];
      DAT_0a4d7968._3_1_ = s__journalwcdb_lv_Invalid_statemen_08b2f560[0xb];
      DAT_0a4d7968._4_1_ = s__journalwcdb_lv_Invalid_statemen_08b2f560[0xc];
      DAT_0a4d7968._5_1_ = s__journalwcdb_lv_Invalid_statemen_08b2f560[0xd];
      DAT_0a4d7968._6_1_ = s__journalwcdb_lv_Invalid_statemen_08b2f560[0xe];
      DAT_0a4d7968._7_1_ = s__journalwcdb_lv_Invalid_statemen_08b2f560[0xf];
      DAT_0a4d7970 = 0x6425;
      DAT_0a4d7972 = 0;
      DAT_0a4d7973 = 1;
    }
    FUN_05630c8c(auStack_218,&DAT_0a4d7968);
    uVar3 = FUN_056d74b0(auStack_200,auStack_218);
    puStack_58 = &SUB_aaaaaaaaaaaaaaaa;
    local_60 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_48 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_50 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_78 = &SUB_aaaaaaaaaaaaaaaa;
    local_80 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_68 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_70 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_98 = &SUB_aaaaaaaaaaaaaaaa;
    local_a0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_88 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_90 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_b8 = &SUB_aaaaaaaaaaaaaaaa;
    local_c0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_a8 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_b0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_d8 = &SUB_aaaaaaaaaaaaaaaa;
    local_e0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_c8 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_d0 = &SUB_aaaaaaaaaaaaaaaa;
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
    puStack_188 = &SUB_aaaaaaaaaaaaaaaa;
    local_190 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_1a8 = &SUB_aaaaaaaaaaaaaaaa;
    local_1b0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_198 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_1a0 = &SUB_aaaaaaaaaaaaaaaa;
    puStack_1b8 = &SUB_aaaaaaaaaaaaaaaa;
    local_1c0 = &SUB_aaaaaaaaaaaaaaaa;
    thunk_FUN_0569fd80(&local_1c0,param_1);
    iVar1 = FUN_056a0008(&local_1c0,uVar3);
    if (iVar1 == 0) {
      thunk_FUN_0569fefc(&local_1c0);
      FUN_0562fd84(auStack_218);
      thunk_FUN_056c2628(auStack_200);
    }
    else {
      iVar1 = FUN_056a14e8(&local_1c0);
      FUN_056a15c0(&local_1c0);
      thunk_FUN_0569fefc(&local_1c0);
      FUN_0562fd84(auStack_218);
      thunk_FUN_056c2628(auStack_200);
      if (iVar1 != 0) goto LAB_05695068;
    }
  }
  return 0;
}


