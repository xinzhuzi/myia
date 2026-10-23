// Ghidra inferred pseudocode; requested=0x466ae88
// entry=0466ae88 end=0466bc0b

/* WARNING: Removing unreachable block (ram,0x0466b20c) */
/* WARNING: Removing unreachable block (ram,0x0466b16c) */
/* WARNING: Removing unreachable block (ram,0x0466b6dc) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0466ae88(undefined8 *param_1,long param_2,uint param_3)

{
  undefined1 *puVar1;
  undefined1 *puVar2;
  byte bVar3;
  undefined *puVar4;
  undefined4 uVar5;
  uint uVar6;
  int iVar7;
  size_t sVar8;
  ulong uVar9;
  char *pcVar10;
  undefined8 *******pppppppuVar11;
  char *******pppppppcVar12;
  undefined1 *puVar13;
  undefined8 uVar14;
  undefined1 *puVar15;
  undefined1 *puVar16;
  byte bVar17;
  undefined1 local_288;
  undefined7 uStack_287;
  undefined7 local_278;
  char cStack_271;
  undefined1 local_270;
  undefined7 uStack_26f;
  undefined7 local_260;
  char cStack_259;
  undefined1 local_258;
  undefined7 uStack_257;
  undefined7 local_248;
  char cStack_241;
  undefined1 local_240;
  undefined7 uStack_23f;
  undefined7 local_230;
  char cStack_229;
  undefined1 local_228;
  undefined7 uStack_227;
  undefined7 local_218;
  char cStack_211;
  undefined8 *******local_210;
  size_t sStack_208;
  undefined8 local_200;
  undefined8 uStack_1f8;
  undefined8 *******local_1f0;
  size_t sStack_1e8;
  ulong local_1e0;
  undefined8 ******ppppppuStack_1d8;
  size_t sStack_1d0;
  ulong local_1c8;
  undefined8 ******local_1c0;
  size_t sStack_1b8;
  ulong local_1b0;
  undefined8 ******local_1a8;
  size_t sStack_1a0;
  ulong uStack_198;
  undefined8 ******local_190;
  undefined1 uStack_188;
  undefined7 uStack_187;
  undefined1 local_180;
  undefined6 uStack_17f;
  char cStack_179;
  undefined1 local_178;
  undefined7 uStack_177;
  undefined8 uStack_170;
  undefined8 local_168;
  undefined8 uStack_160;
  undefined1 *local_158;
  undefined8 *******local_148;
  size_t local_140;
  undefined8 local_138;
  undefined1 local_130;
  undefined7 uStack_12f;
  undefined7 local_120;
  char cStack_119;
  char *******local_118;
  undefined1 *local_110;
  undefined8 local_108;
  undefined8 *******local_100;
  size_t sStack_f8;
  undefined8 local_f0;
  undefined8 uStack_e8;
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
  long local_78;
  
  puVar4 = PTR_s_mmkv_key_user_name_0a05a5f8;
  local_78 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_110 = &SUB_aaaaaaaaaaaaaaaa;
  local_108 = &SUB_aaaaaaaaaaaaaaaa;
  local_118 = (char *******)&SUB_aaaaaaaaaaaaaaaa;
  uVar14 = *(undefined8 *)(param_2 + 0x2a0);
  sVar8 = _strlen(PTR_s_mmkv_key_user_name_0a05a5f8);
  if (0x7ffffffffffffff7 < sVar8) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_210);
  }
  if (sVar8 < 0x17) {
    local_200 = CONCAT17((char)sVar8,(undefined7)local_200);
    pppppppuVar11 = &local_210;
    if (sVar8 != 0) goto LAB_0466af38;
  }
  else {
    uVar9 = 0x19;
    if ((sVar8 | 7) != 0x17) {
      uVar9 = (sVar8 | 7) + 1;
    }
    pppppppuVar11 = (undefined8 *******)__Znwm(uVar9);
    local_200 = uVar9 | 0x8000000000000000;
    local_210 = pppppppuVar11;
    sStack_208 = sVar8;
LAB_0466af38:
    _memmove(pppppppuVar11,puVar4,sVar8);
  }
  *(undefined1 *)((long)pppppppuVar11 + sVar8) = 0;
  cStack_119 = '\0';
  local_130 = 0;
  FUN_045321c0(&local_118,uVar14,&local_210,&local_130);
  if (cStack_119 < '\0') {
    __ZdlPvm(CONCAT71(uStack_12f,local_130),CONCAT17(cStack_119,local_120) & 0x7fffffffffffffff);
  }
  if ((long)local_200 < 0) {
    __ZdlPvm(local_210,local_200 & 0x7fffffffffffffff);
  }
  uVar9 = (**(code **)(*DAT_0a45df38 + 0x70))();
  if ((uVar9 & 1) == 0) {
    puVar15 = (undefined1 *)(ulong)local_108._7_1_;
    puVar16 = local_110;
    bVar17 = local_108._7_1_;
LAB_0466b044:
    puVar4 = PTR_s_mmkv_key_old_wechat_auto_login_l_0a05a640;
    if (-1 < (char)bVar17) {
      puVar16 = puVar15;
    }
    if (puVar16 != (undefined1 *)0x0) {
      uStack_177 = 0xaaaaaaaaaaaaaa;
      sStack_208 = 0;
      local_210 = (undefined8 *******)0x0;
      uStack_1f8 = 0;
      local_200 = 0;
      sStack_1e8 = 0;
      local_1f0 = (undefined8 *******)0x0;
      ppppppuStack_1d8 = (undefined8 ******)0x0;
      local_1e0 = 0;
      local_1c8 = 0;
      sStack_1d0 = 0;
      sStack_1b8 = 0;
      local_1c0 = (undefined8 ******)0x0;
      local_1a8 = (undefined8 ******)0x0;
      local_1b0 = 0;
      uStack_198 = 0;
      sStack_1a0 = 0;
      uStack_188 = 0;
      local_190 = (undefined8 ******)0x0;
      uStack_17f = 0;
      cStack_179 = '\0';
      local_178 = 0;
      uStack_187 = 0;
      local_180 = 0;
      uStack_160 = 0;
      uStack_170 = 0;
      local_168 = 0;
      local_158 = &DAT_aaaaaaaaaaaaaa00;
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (&local_210,&local_118);
      puVar4 = PTR_s_mmkv_key_auto_login_flag_0a05a600;
      uVar14 = *(undefined8 *)(param_2 + 0x2a0);
      sVar8 = _strlen(PTR_s_mmkv_key_auto_login_flag_0a05a600);
      if (0x7ffffffffffffff7 < sVar8) {
                    /* WARNING: Subroutine does not return */
        FUN_00018d9c(&local_100);
      }
      if (sVar8 < 0x17) {
        local_f0 = CONCAT17((char)sVar8,(undefined7)local_f0);
        pppppppuVar11 = &local_100;
        if (sVar8 != 0) goto LAB_0466b13c;
      }
      else {
        uVar9 = 0x19;
        if ((sVar8 | 7) != 0x17) {
          uVar9 = (sVar8 | 7) + 1;
        }
        pppppppuVar11 = (undefined8 *******)__Znwm(uVar9);
        local_f0 = uVar9 | 0x8000000000000000;
        local_100 = pppppppuVar11;
        sStack_f8 = sVar8;
LAB_0466b13c:
        _memmove(pppppppuVar11,puVar4,sVar8);
      }
      *(undefined1 *)((long)pppppppuVar11 + sVar8) = 0;
      uVar5 = FUN_04531d78(uVar14,&local_100,0);
      puVar4 = PTR_s_mmkv_key_push_login_url_expired__0a05a608;
      uStack_1f8 = CONCAT44(uStack_1f8._4_4_,uVar5);
      uVar14 = *(undefined8 *)(param_2 + 0x2a0);
      sVar8 = _strlen(PTR_s_mmkv_key_push_login_url_expired__0a05a608);
      if (0x7ffffffffffffff7 < sVar8) {
                    /* WARNING: Subroutine does not return */
        FUN_00018d9c(&local_100);
      }
      if (sVar8 < 0x17) {
        local_f0 = CONCAT17((char)sVar8,(undefined7)local_f0);
        pppppppuVar11 = &local_100;
        if (sVar8 != 0) goto LAB_0466b1dc;
      }
      else {
        uVar9 = 0x19;
        if ((sVar8 | 7) != 0x17) {
          uVar9 = (sVar8 | 7) + 1;
        }
        pppppppuVar11 = (undefined8 *******)__Znwm(uVar9);
        local_f0 = uVar9 | 0x8000000000000000;
        local_100 = pppppppuVar11;
        sStack_f8 = sVar8;
LAB_0466b1dc:
        _memmove(pppppppuVar11,puVar4,sVar8);
      }
      *(undefined1 *)((long)pppppppuVar11 + sVar8) = 0;
      uVar5 = FUN_04531b58(uVar14,&local_100,0);
      puVar4 = PTR_s_mmkv_key_nick_name_0a05a610;
      uStack_1f8 = CONCAT44(uVar5,(undefined4)uStack_1f8);
      uVar14 = *(undefined8 *)(param_2 + 0x2a0);
      sVar8 = _strlen(PTR_s_mmkv_key_nick_name_0a05a610);
      if (0x7ffffffffffffff7 < sVar8) {
                    /* WARNING: Subroutine does not return */
        FUN_00018d9c(&local_148);
      }
      if (sVar8 < 0x17) {
        local_138 = CONCAT17((char)sVar8,(undefined7)local_138);
        pppppppuVar11 = &local_148;
        if (sVar8 != 0) goto LAB_0466b27c;
      }
      else {
        uVar9 = 0x19;
        if ((sVar8 | 7) != 0x17) {
          uVar9 = (sVar8 | 7) + 1;
        }
        pppppppuVar11 = (undefined8 *******)__Znwm(uVar9);
        local_138 = uVar9 | 0x8000000000000000;
        local_148 = pppppppuVar11;
        local_140 = sVar8;
LAB_0466b27c:
        _memmove(pppppppuVar11,puVar4,sVar8);
      }
      *(undefined1 *)((long)pppppppuVar11 + sVar8) = 0;
      cStack_211 = '\0';
      local_228 = 0;
      FUN_045321c0(&local_100,uVar14,&local_148,&local_228);
      if ((long)local_1e0 < 0) {
        __ZdlPvm(local_1f0,local_1e0 & 0x7fffffffffffffff);
      }
      local_1e0 = local_f0;
      local_1f0 = local_100;
      sStack_1e8 = sStack_f8;
      local_f0 = local_f0 & 0xffffffffffffff;
      local_100 = (undefined8 *******)((ulong)local_100 & 0xffffffffffffff00);
      if (cStack_211 < '\0') {
        __ZdlPvm(CONCAT71(uStack_227,local_228),CONCAT17(cStack_211,local_218) & 0x7fffffffffffffff)
        ;
      }
      if ((long)local_138 < 0) {
        __ZdlPvm(local_148,local_138 & 0x7fffffffffffffff);
      }
      puVar4 = PTR_s_mmkv_key_auto_auth_key_0a05a618;
      uVar14 = *(undefined8 *)(param_2 + 0x2a0);
      sVar8 = _strlen(PTR_s_mmkv_key_auto_auth_key_0a05a618);
      if (0x7ffffffffffffff7 < sVar8) {
                    /* WARNING: Subroutine does not return */
        FUN_00018d9c(&local_148);
      }
      if (sVar8 < 0x17) {
        local_138 = CONCAT17((char)sVar8,(undefined7)local_138);
        pppppppuVar11 = &local_148;
        if (sVar8 != 0) goto LAB_0466b350;
      }
      else {
        uVar9 = 0x19;
        if ((sVar8 | 7) != 0x17) {
          uVar9 = (sVar8 | 7) + 1;
        }
        pppppppuVar11 = (undefined8 *******)__Znwm(uVar9);
        local_138 = uVar9 | 0x8000000000000000;
        local_148 = pppppppuVar11;
        local_140 = sVar8;
LAB_0466b350:
        _memmove(pppppppuVar11,puVar4,sVar8);
      }
      *(undefined1 *)((long)pppppppuVar11 + sVar8) = 0;
      cStack_229 = '\0';
      local_240 = 0;
      FUN_045321c0(&local_100,uVar14,&local_148,&local_240);
      if ((long)local_1c8 < 0) {
        __ZdlPvm(ppppppuStack_1d8,local_1c8 & 0x7fffffffffffffff);
      }
      local_1c8 = local_f0;
      ppppppuStack_1d8 = local_100;
      sStack_1d0 = sStack_f8;
      local_f0 = local_f0 & 0xffffffffffffff;
      local_100 = (undefined8 *******)((ulong)local_100 & 0xffffffffffffff00);
      if (cStack_229 < '\0') {
        __ZdlPvm(CONCAT71(uStack_23f,local_240),CONCAT17(cStack_229,local_230) & 0x7fffffffffffffff)
        ;
      }
      if ((long)local_138 < 0) {
        __ZdlPvm(local_148,local_138 & 0x7fffffffffffffff);
      }
      puVar4 = PTR_s_mmkv_key_head_img_url_0a05a620;
      uVar14 = *(undefined8 *)(param_2 + 0x2a0);
      sVar8 = _strlen(PTR_s_mmkv_key_head_img_url_0a05a620);
      if (0x7ffffffffffffff7 < sVar8) {
                    /* WARNING: Subroutine does not return */
        FUN_00018d9c(&local_148);
      }
      if (sVar8 < 0x17) {
        local_138 = CONCAT17((char)sVar8,(undefined7)local_138);
        pppppppuVar11 = &local_148;
        if (sVar8 != 0) goto LAB_0466b424;
      }
      else {
        uVar9 = 0x19;
        if ((sVar8 | 7) != 0x17) {
          uVar9 = (sVar8 | 7) + 1;
        }
        pppppppuVar11 = (undefined8 *******)__Znwm(uVar9);
        local_138 = uVar9 | 0x8000000000000000;
        local_148 = pppppppuVar11;
        local_140 = sVar8;
LAB_0466b424:
        _memmove(pppppppuVar11,puVar4,sVar8);
      }
      *(undefined1 *)((long)pppppppuVar11 + sVar8) = 0;
      cStack_241 = '\0';
      local_258 = 0;
      FUN_045321c0(&local_100,uVar14,&local_148,&local_258);
      if ((long)local_1b0 < 0) {
        __ZdlPvm(local_1c0,local_1b0 & 0x7fffffffffffffff);
      }
      local_1b0 = local_f0;
      local_1c0 = local_100;
      sStack_1b8 = sStack_f8;
      local_f0 = local_f0 & 0xffffffffffffff;
      local_100 = (undefined8 *******)((ulong)local_100 & 0xffffffffffffff00);
      if (cStack_241 < '\0') {
        __ZdlPvm(CONCAT71(uStack_257,local_258),CONCAT17(cStack_241,local_248) & 0x7fffffffffffffff)
        ;
      }
      if ((long)local_138 < 0) {
        __ZdlPvm(local_148,local_138 & 0x7fffffffffffffff);
      }
      puVar4 = PTR_s_mmkv_key_pc_account_name_0a05a628;
      uVar14 = *(undefined8 *)(param_2 + 0x2a0);
      sVar8 = _strlen(PTR_s_mmkv_key_pc_account_name_0a05a628);
      if (0x7ffffffffffffff7 < sVar8) {
                    /* WARNING: Subroutine does not return */
        FUN_00018d9c(&local_148);
      }
      if (sVar8 < 0x17) {
        local_138 = CONCAT17((char)sVar8,(undefined7)local_138);
        pppppppuVar11 = &local_148;
        if (sVar8 != 0) goto LAB_0466b4f8;
      }
      else {
        uVar9 = 0x19;
        if ((sVar8 | 7) != 0x17) {
          uVar9 = (sVar8 | 7) + 1;
        }
        pppppppuVar11 = (undefined8 *******)__Znwm(uVar9);
        local_138 = uVar9 | 0x8000000000000000;
        local_148 = pppppppuVar11;
        local_140 = sVar8;
LAB_0466b4f8:
        _memmove(pppppppuVar11,puVar4,sVar8);
      }
      *(undefined1 *)((long)pppppppuVar11 + sVar8) = 0;
      cStack_259 = '\0';
      local_270 = 0;
      FUN_045321c0(&local_100,uVar14,&local_148,&local_270);
      if ((long)uStack_198 < 0) {
        __ZdlPvm(local_1a8,uStack_198 & 0x7fffffffffffffff);
      }
      uStack_198 = local_f0;
      local_1a8 = local_100;
      sStack_1a0 = sStack_f8;
      local_f0 = local_f0 & 0xffffffffffffff;
      local_100 = (undefined8 *******)((ulong)local_100 & 0xffffffffffffff00);
      if (cStack_259 < '\0') {
        __ZdlPvm(CONCAT71(uStack_26f,local_270),CONCAT17(cStack_259,local_260) & 0x7fffffffffffffff)
        ;
      }
      if ((long)local_138 < 0) {
        __ZdlPvm(local_148,local_138 & 0x7fffffffffffffff);
      }
      puVar4 = PTR_s_mmkv_key_server_id_0a05a630;
      uVar14 = *(undefined8 *)(param_2 + 0x2a0);
      sVar8 = _strlen(PTR_s_mmkv_key_server_id_0a05a630);
      if (0x7ffffffffffffff7 < sVar8) {
                    /* WARNING: Subroutine does not return */
        FUN_00018d9c(&local_148);
      }
      if (sVar8 < 0x17) {
        local_138 = CONCAT17((char)sVar8,(undefined7)local_138);
        pppppppuVar11 = &local_148;
        if (sVar8 != 0) goto LAB_0466b5cc;
      }
      else {
        uVar9 = 0x19;
        if ((sVar8 | 7) != 0x17) {
          uVar9 = (sVar8 | 7) + 1;
        }
        pppppppuVar11 = (undefined8 *******)__Znwm(uVar9);
        local_138 = uVar9 | 0x8000000000000000;
        local_148 = pppppppuVar11;
        local_140 = sVar8;
LAB_0466b5cc:
        _memmove(pppppppuVar11,puVar4,sVar8);
      }
      *(undefined1 *)((long)pppppppuVar11 + sVar8) = 0;
      cStack_271 = '\0';
      local_288 = 0;
      FUN_045321c0(&local_100,uVar14,&local_148,&local_288);
      if (cStack_179 < '\0') {
        __ZdlPvm(local_190,CONCAT17(cStack_179,CONCAT61(uStack_17f,local_180)) & 0x7fffffffffffffff)
        ;
      }
      local_190 = local_100;
      uStack_188 = (undefined1)sStack_f8;
      uStack_187 = (undefined7)(sStack_f8 >> 8);
      local_180 = (undefined1)local_f0;
      uStack_17f = (undefined6)(local_f0 >> 8);
      cStack_179 = (char)(local_f0 >> 0x38);
      local_f0 = local_f0 & 0xffffffffffffff;
      local_100 = (undefined8 *******)((ulong)local_100 & 0xffffffffffffff00);
      if (cStack_271 < '\0') {
        __ZdlPvm(CONCAT71(uStack_287,local_288),CONCAT17(cStack_271,local_278) & 0x7fffffffffffffff)
        ;
      }
      if ((long)local_138 < 0) {
        __ZdlPvm(local_148,local_138 & 0x7fffffffffffffff);
      }
      puVar4 = PTR_s_mmkv_key_logout_locked_flag_0a05a658;
      uVar14 = *(undefined8 *)(param_2 + 0x2a0);
      sVar8 = _strlen(PTR_s_mmkv_key_logout_locked_flag_0a05a658);
      if (0x7ffffffffffffff7 < sVar8) {
                    /* WARNING: Subroutine does not return */
        FUN_00018d9c(&local_100);
      }
      if (sVar8 < 0x17) {
        local_f0 = CONCAT17((char)sVar8,(undefined7)local_f0);
        pppppppuVar11 = &local_100;
        if (sVar8 != 0) goto LAB_0466b6a8;
      }
      else {
        uVar9 = 0x19;
        if ((sVar8 | 7) != 0x17) {
          uVar9 = (sVar8 | 7) + 1;
        }
        pppppppuVar11 = (undefined8 *******)__Znwm(uVar9);
        local_f0 = uVar9 | 0x8000000000000000;
        local_100 = pppppppuVar11;
        sStack_f8 = sVar8;
LAB_0466b6a8:
        _memmove(pppppppuVar11,puVar4,sVar8);
      }
      *(undefined1 *)((long)pppppppuVar11 + sVar8) = 0;
      local_178 = FUN_04531f9c(uVar14,&local_100,0);
      uVar6 = (**(code **)(*DAT_0a45df38 + 0x70))();
      if (((uVar6 | param_3 ^ 1) & 1) == 0) {
        FUN_0466c494(param_2,&local_190);
      }
      uVar14 = local_200;
      param_1[1] = sStack_208;
      *param_1 = local_210;
      sStack_208 = 0;
      local_200 = 0;
      local_210 = (undefined8 *******)0x0;
      param_1[2] = uVar14;
      param_1[3] = uStack_1f8;
      param_1[5] = sStack_1e8;
      param_1[4] = local_1f0;
      param_1[6] = local_1e0;
      local_1f0 = (undefined8 *******)0x0;
      sStack_1e8 = 0;
      local_1e0 = 0;
      param_1[9] = local_1c8;
      param_1[8] = sStack_1d0;
      param_1[7] = ppppppuStack_1d8;
      ppppppuStack_1d8 = (undefined8 ******)0x0;
      sStack_1d0 = 0;
      local_1c8 = 0;
      param_1[0xc] = local_1b0;
      param_1[0xb] = sStack_1b8;
      param_1[10] = local_1c0;
      local_1c0 = (undefined8 ******)0x0;
      sStack_1b8 = 0;
      local_1b0 = 0;
      param_1[0xf] = uStack_198;
      param_1[0xe] = sStack_1a0;
      param_1[0xd] = local_1a8;
      local_1a8 = (undefined8 ******)0x0;
      sStack_1a0 = 0;
      uStack_198 = 0;
      param_1[0x12] = CONCAT17(cStack_179,CONCAT61(uStack_17f,local_180));
      param_1[0x11] = CONCAT71(uStack_187,uStack_188);
      param_1[0x10] = local_190;
      local_190 = (undefined8 ******)0x0;
      uStack_188 = 0;
      uStack_187 = 0;
      local_180 = 0;
      uStack_17f = 0;
      cStack_179 = 0;
      *(undefined1 *)(param_1 + 0x13) = local_178;
      param_1[0x16] = uStack_160;
      param_1[0x15] = local_168;
      param_1[0x14] = uStack_170;
      uStack_170 = 0;
      local_168 = 0;
      uStack_160 = 0;
      *(undefined1 *)(param_1 + 0x17) = local_158._0_1_;
      *(undefined1 *)(param_1 + 0x18) = 1;
      FUN_002b5e18(&local_210);
      goto LAB_0466bad0;
    }
    uVar14 = *(undefined8 *)(param_2 + 0x2a0);
    sVar8 = _strlen(PTR_s_mmkv_key_old_wechat_auto_login_l_0a05a640);
    if (0x7ffffffffffffff7 < sVar8) {
                    /* WARNING: Subroutine does not return */
      FUN_00018d9c(&local_210);
    }
    if (sVar8 < 0x17) {
      local_200 = CONCAT17((char)sVar8,(undefined7)local_200);
      pppppppuVar11 = &local_210;
      if (sVar8 != 0) goto LAB_0466b8f8;
    }
    else {
      uVar9 = 0x19;
      if ((sVar8 | 7) != 0x17) {
        uVar9 = (sVar8 | 7) + 1;
      }
      pppppppuVar11 = (undefined8 *******)__Znwm(uVar9);
      local_200 = uVar9 | 0x8000000000000000;
      local_210 = pppppppuVar11;
      sStack_208 = sVar8;
LAB_0466b8f8:
      _memmove(pppppppuVar11,puVar4,sVar8);
    }
    *(undefined1 *)((long)pppppppuVar11 + sVar8) = 0;
    uVar9 = FUN_04531f9c(uVar14,&local_210,0);
    if ((long)local_200 < 0) {
      __ZdlPvm(local_210,local_200 & 0x7fffffffffffffff);
    }
    if ((uVar9 & 1) == 0) {
      param_1[0x18] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x15] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x14] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x17] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x16] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x11] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x10] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x13] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0x12] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0xd] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0xc] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0xf] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0xe] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[9] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[8] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[0xb] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[10] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[5] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[4] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[7] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[6] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[1] = &SUB_aaaaaaaaaaaaaaaa;
      *param_1 = &SUB_aaaaaaaaaaaaaaaa;
      param_1[3] = &SUB_aaaaaaaaaaaaaaaa;
      param_1[2] = &SUB_aaaaaaaaaaaaaaaa;
      FUN_04a724b8(param_1);
      if (*(char *)(param_1 + 0x18) == '\x01') {
        FUN_0466bdcc(param_2,param_1);
        uVar6 = (**(code **)(*DAT_0a45df38 + 0x70))();
        if (((uVar6 | param_3 ^ 1) & 1) == 0) {
          FUN_0466c494(param_2,param_1 + 0x10);
        }
        FUN_0466ad94(param_2);
      }
      goto LAB_0466bad0;
    }
  }
  else {
    pcVar10 = (char *)(**(code **)(*DAT_0a45df38 + 0x28))();
    puVar16 = local_110;
    bVar3 = pcVar10[0x17];
    puVar13 = (undefined1 *)(ulong)bVar3;
    puVar1 = *(undefined1 **)(pcVar10 + 8);
    if (-1 < (char)bVar3) {
      puVar1 = puVar13;
    }
    bVar17 = local_108._7_1_;
    puVar15 = (undefined1 *)(ulong)local_108._7_1_;
    puVar2 = local_110;
    if (-1 < (long)local_108) {
      puVar2 = puVar15;
    }
    if (puVar1 == puVar2) {
      pppppppcVar12 = local_118;
      if (-1 < (long)local_108) {
        pppppppcVar12 = (char *******)&local_118;
      }
      if ((char)bVar3 < '\0') {
        iVar7 = _memcmp(*(void **)pcVar10,pppppppcVar12,(size_t)*(undefined1 **)(pcVar10 + 8));
        if (iVar7 != 0) goto LAB_0466b938;
      }
      else if (bVar3 != 0) {
        do {
          if (*pcVar10 != *(char *)pppppppcVar12) goto LAB_0466b938;
          pcVar10 = pcVar10 + 1;
          pppppppcVar12 = (char *******)((long)pppppppcVar12 + 1);
          puVar13 = puVar13 + -1;
        } while (puVar13 != (undefined1 *)0x0);
      }
      goto LAB_0466b044;
    }
LAB_0466b938:
    iVar7 = thunk_FUN_05e1d97c(2);
    if (iVar7 != 0) {
      FUN_0488143c(&local_148);
      pppppppuVar11 = local_148;
      if (-1 < (long)local_138) {
        pppppppuVar11 = &local_148;
      }
      if ((DAT_0a45df8a & 1) == 0) {
        DAT_0a45df80._0_1_ = s_input_ackernel_cpadV_08a133a0[8];
        DAT_0a45df80._1_1_ = s_input_ackernel_cpadV_08a133a0[9];
        DAT_0a45df80._2_1_ = s_input_ackernel_cpadV_08a133a0[10];
        DAT_0a45df80._3_1_ = s_input_ackernel_cpadV_08a133a0[0xb];
        DAT_0a45df80._4_1_ = s_input_ackernel_cpadV_08a133a0[0xc];
        DAT_0a45df80._5_1_ = s_input_ackernel_cpadV_08a133a0[0xd];
        DAT_0a45df80._6_1_ = s_input_ackernel_cpadV_08a133a0[0xe];
        DAT_0a45df80._7_1_ = s_input_ackernel_cpadV_08a133a0[0xf];
        DAT_0a45df88 = 99;
        DAT_0a45df8a = 1;
      }
      if ((DAT_0a45e121 & 1) == 0) {
        uRam000000000a45e118._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x18];
        uRam000000000a45e118._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x19];
        uRam000000000a45e118._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x1a];
        uRam000000000a45e118._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x1b];
        uRam000000000a45e118._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x1c];
        uRam000000000a45e118._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x1d];
        uRam000000000a45e118._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x1e];
        uRam000000000a45e118._7_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x1f];
        DAT_0a45e110 = s_login_service_ccGetAutoLoginInfo_089be4f0[0x10];
        DAT_0a45e110_1._0_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x11];
        DAT_0a45e110_1._1_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x12];
        DAT_0a45e110_1._2_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x13];
        DAT_0a45e110_1._3_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x14];
        DAT_0a45e110_1._4_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x15];
        DAT_0a45e110_1._5_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x16];
        DAT_0a45e110_1._6_1_ = s_login_service_ccGetAutoLoginInfo_089be4f0[0x17];
        DAT_0a45e120 = 0;
        DAT_0a45e121 = 1;
      }
      FUN_05e1d050(&local_210,2,pppppppuVar11,&DAT_0a45df80,&DAT_0a45e110,0x155,0,0);
      if ((DAT_0a45e144 & 1) == 0) {
        _DAT_0a45e124 = CONCAT44((int)DAT_08a13438,(int)DAT_084d1028);
        uRam000000000a45e12c = CONCAT44((int)DAT_084d8880,(int)DAT_085b57a0);
        _DAT_0a45e134 = CONCAT44((int)DAT_084d4a60,(int)DAT_084e4af8);
        uRam000000000a45e13c = CONCAT44((int)ram0x086a14e8,(int)DAT_084abdf0);
        DAT_0a45e144 = 1;
      }
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
      sStack_f8 = 0;
      local_100 = (undefined8 *******)0x0;
      uStack_e8 = 0;
      local_f0 = 0;
      FUN_05e1d31c(&local_210,&DAT_0a45e124,&local_100);
      thunk_FUN_05e1d0bc(&local_210);
      if ((long)local_138 < 0) {
        __ZdlPvm(local_148,local_138 & 0x7fffffffffffffff);
      }
    }
  }
  *(undefined1 *)param_1 = 0;
  *(undefined1 *)(param_1 + 0x18) = 0;
LAB_0466bad0:
  if ((long)local_108 < 0) {
    __ZdlPvm(local_118,(ulong)local_108 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_78) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


