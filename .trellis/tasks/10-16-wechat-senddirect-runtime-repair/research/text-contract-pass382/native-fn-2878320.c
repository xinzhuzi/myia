// Ghidra inferred pseudocode; requested=0x2878320
// entry=02878320 end=028792db

/* WARNING: Removing unreachable block (ram,0x028784ec) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_02878320(long param_1,long param_2,long *param_3)

{
  undefined1 ***pppuVar1;
  char *pcVar2;
  undefined8 uVar3;
  undefined8 uVar4;
  undefined1 uVar5;
  uint3 uVar6;
  long *plVar7;
  char cVar8;
  long **pplVar9;
  bool bVar10;
  int iVar11;
  ulong *puVar12;
  undefined8 uVar13;
  undefined8 *puVar14;
  undefined1 *puVar15;
  undefined8 uVar16;
  long lVar17;
  ulong uVar18;
  long **pplVar19;
  undefined1 *puVar20;
  long lVar21;
  ulong uVar22;
  undefined4 uVar23;
  undefined4 uVar24;
  undefined4 local_33c;
  char local_328;
  undefined7 uStack_327;
  ulong *local_320;
  undefined7 local_318;
  char cStack_311;
  ulong local_310;
  long lStack_308;
  ulong local_300;
  undefined8 uStack_2f8;
  undefined8 local_2f0;
  undefined1 **local_280;
  ulong *puStack_278;
  undefined8 *local_270;
  undefined8 *local_268;
  undefined8 *local_260;
  undefined8 *puStack_258;
  undefined8 *local_250;
  undefined1 *puStack_248;
  ulong local_240;
  undefined8 uStack_238;
  undefined1 ***local_230;
  long **pplStack_228;
  ulong local_220;
  ulong local_210;
  long lStack_208;
  ulong local_200;
  undefined1 local_1f0 [8];
  undefined8 local_1e8;
  undefined1 local_1e0 [8];
  undefined8 local_1d8;
  undefined1 local_1d0 [8];
  undefined8 local_1c8;
  undefined1 *local_1c0;
  long *local_1b8;
  ulong local_1b0;
  long *local_1a8;
  long *local_1a0;
  undefined8 uStack_198;
  ulong local_190;
  undefined8 **local_148;
  ulong *local_140;
  ulong local_138;
  undefined8 local_130;
  undefined1 ***local_f8;
  long **pplStack_f0;
  ulong local_e8;
  long lStack_e0;
  undefined8 local_d8;
  undefined8 uStack_d0;
  undefined8 local_c8;
  undefined8 uStack_c0;
  undefined8 local_b8;
  undefined8 uStack_b0;
  undefined8 local_a8;
  undefined8 uStack_a0;
  undefined8 local_98;
  undefined8 uStack_90;
  undefined8 local_88;
  undefined8 uStack_80;
  long local_78;
  
  local_78 = *(long *)PTR____stack_chk_guard_09b36c98;
  FUN_000401d8(*(undefined8 *)(param_1 + 0x28));
  uVar16 = *(undefined8 *)(param_1 + 0x28);
  uVar3 = *(undefined8 *)(param_1 + 0x90);
  uVar4 = *(undefined8 *)(param_1 + 0x98);
  local_210 = 0;
  lStack_208 = 0;
  local_200 = 0;
  uVar22 = param_3[1];
  if (-1 < (char)*(byte *)((long)param_3 + 0x17)) {
    uVar22 = (ulong)*(byte *)((long)param_3 + 0x17);
  }
  if (uVar22 == 0) {
    local_140 = (ulong *)&SUB_aaaaaaaaaaaaaaaa;
    local_148 = (undefined8 **)&SUB_aaaaaaaaaaaaaaaa;
    FUN_04878be8(&local_148,param_2);
    local_1a0 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    uStack_198 = &SUB_aaaaaaaaaaaaaaaa;
    if ((DAT_0a39e330 & 1) == 0) {
      DAT_0a39e328[0] = s_success_08480a08[0];
      DAT_0a39e328[1] = s_success_08480a08[1];
      DAT_0a39e328[2] = s_success_08480a08[2];
      DAT_0a39e328[3] = s_success_08480a08[3];
      DAT_0a39e328[4] = s_success_08480a08[4];
      DAT_0a39e328[5] = s_success_08480a08[5];
      DAT_0a39e328[6] = s_success_08480a08[6];
      DAT_0a39e328[7] = s_success_08480a08[7];
      DAT_0a39e330 = 1;
    }
    FUN_04878ce0(&local_1a0,&local_148,DAT_0a39e328);
    local_33c = 1;
    if (((char)local_148 == '\x01') && ((char)local_1a0 == '\x04')) {
      if ((DAT_0a39e330 & 1) == 0) {
        DAT_0a39e328[0] = s_success_08480a08[0];
        DAT_0a39e328[1] = s_success_08480a08[1];
        DAT_0a39e328[2] = s_success_08480a08[2];
        DAT_0a39e328[3] = s_success_08480a08[3];
        DAT_0a39e328[4] = s_success_08480a08[4];
        DAT_0a39e328[5] = s_success_08480a08[5];
        DAT_0a39e328[6] = s_success_08480a08[6];
        DAT_0a39e328[7] = s_success_08480a08[7];
        DAT_0a39e330 = 1;
      }
      uVar22 = FUN_04878e40(&local_148,DAT_0a39e328,1);
      if ((uVar22 & 1) == 0) {
        local_e8 = local_e8 & 0xffffffffffffff;
        local_f8 = (undefined1 ***)((ulong)local_f8 & 0xffffffffffffff00);
        if ((DAT_0a39e35e & 1) == 0) {
          DAT_0a39e350._0_1_ = s_error_mea_er_08712068[0];
          DAT_0a39e350._1_1_ = s_error_mea_er_08712068[1];
          DAT_0a39e350._2_1_ = s_error_mea_er_08712068[2];
          DAT_0a39e350._3_1_ = s_error_mea_er_08712068[3];
          DAT_0a39e350._4_1_ = s_error_mea_er_08712068[4];
          DAT_0a39e350._5_1_ = s_error_mea_er_08712068[5];
          DAT_0a39e350._6_1_ = s_error_mea_er_08712068[6];
          DAT_0a39e350._7_1_ = s_error_mea_er_08712068[7];
          DAT_0a39e358 = (undefined4)DAT_084a8110;
          DAT_0a39e35c = 0x65;
          DAT_0a39e35e = 1;
        }
        FUN_0487929c(&local_310,&local_148,&DAT_0a39e350,&local_f8);
        if ((long)local_200 < 0) {
          __ZdlPvm(local_210,local_200 & 0x7fffffffffffffff);
        }
        lStack_208 = lStack_308;
        local_210 = local_310;
        local_200 = local_300;
        local_300 = local_300 & 0xffffffffffffff;
        local_310 = local_310 & 0xffffffffffffff00;
        local_33c = 0;
      }
    }
    FUN_001fa1c8(&uStack_198,(ulong)local_1a0 & 0xff);
    FUN_001fa1c8(&local_140,(ulong)local_148 & 0xff);
  }
  else {
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(&local_210,param_3);
    local_33c = 0;
  }
  uStack_238 = 0;
  local_240 = 0;
  pplStack_228 = (long **)0x0;
  local_230 = (undefined1 ***)0x0;
  local_220 = 0;
  if ((*(long *)(param_1 + 0xb8) != *(long *)(param_1 + 0xc0)) ||
     (*(long *)(param_1 + 0xd0) != *(long *)(param_1 + 0xd8))) {
    local_280 = (undefined1 **)&SUB_aaaaaaaaaaaaaaaa;
    puStack_278 = (ulong *)&SUB_aaaaaaaaaaaaaaaa;
    FUN_003b276c(&local_280,0,0,0,1);
    uVar22 = *(ulong *)(param_1 + 0xa8);
    if (-1 < (char)*(byte *)(param_1 + 0xb7)) {
      uVar22 = (ulong)*(byte *)(param_1 + 0xb7);
    }
    if (uVar22 == 0) {
LAB_028785cc:
      lVar17 = *(long *)(param_1 + 0xd0);
      lVar21 = *(long *)(param_1 + 0xd8);
      lStack_308 = 0;
      local_310 = 0;
      uStack_2f8 = 0;
      local_300 = 0;
      local_2f0 = 0xaaaaaaaa3f800000;
      for (; lVar17 != lVar21; lVar17 = lVar17 + 0x18) {
        FUN_003e8854(&local_310,lVar17,lVar17);
      }
      local_1a8 = (long *)0x0;
      local_1b0 = 2;
      local_1a8 = (long *)__Znwm(0x18);
      *local_1a8 = 0;
      local_1a8[1] = 0;
      local_1a8[2] = 0;
      lVar17 = *(long *)(param_1 + 0xb8);
      lVar21 = *(long *)(param_1 + 0xc0);
      if (lVar17 == lVar21) {
        lVar17 = 0;
LAB_028786c4:
        uVar22 = local_1a8[1] - lVar17 >> 4;
      }
      else {
        do {
          if (((char)local_280 != '\x01') ||
             (puVar12 = (ulong *)FUN_0026e564(puStack_278,lVar17), puStack_278 + 1 == puVar12)) {
            FUN_00239554(&local_f8,lVar17);
            FUN_003b223c(&local_1b0,&local_f8);
            FUN_001fa1c8(&pplStack_f0,(ulong)local_f8 & 0xff);
          }
          lVar17 = lVar17 + 0x18;
        } while (lVar17 != lVar21);
        uVar22 = local_1b0 & 0xff;
        if ((char)local_1b0 != '\0') {
          if ((char)local_1b0 == '\x01') {
            uVar22 = local_1a8[2];
          }
          else {
            if ((char)local_1b0 == '\x02') {
              lVar17 = *local_1a8;
              goto LAB_028786c4;
            }
            uVar22 = 1;
          }
        }
      }
      local_1c0 = &SUB_aaaaaaaaaaaaaaaa;
      local_1b8 = (long *)&SUB_aaaaaaaaaaaaaaaa;
      local_240 = uVar22;
      FUN_003b276c(&local_1c0,0,0,0,1);
      local_f8 = &local_280;
      pplStack_f0 = (long **)0x0;
      local_e8 = 0;
      lStack_e0 = -0x8000000000000000;
      uVar18 = (ulong)local_280 & 0xff;
      if ((char)local_280 == '\0') {
        lStack_e0 = 1;
      }
      else if ((char)local_280 == '\x02') {
        local_e8 = *puStack_278;
      }
      else if ((char)local_280 == '\x01') {
        pplStack_f0 = (long **)*puStack_278;
      }
      else {
        lStack_e0 = 0;
      }
      while( true ) {
        local_140 = (ulong *)0x0;
        local_138 = 0;
        local_130 = 0x8000000000000000;
        if ((int)uVar18 == 2) {
          local_138 = puStack_278[1];
        }
        else if ((int)uVar18 == 1) {
          local_140 = puStack_278 + 1;
        }
        else {
          local_130 = 1;
        }
        local_148 = &local_280;
        iVar11 = FUN_007674cc(&local_f8,&local_148);
        if (iVar11 != 0) break;
        uVar13 = FUN_024c3984(&local_f8);
        lVar17 = FUN_00758940(&local_310,uVar13);
        if (lVar17 == 0) {
          uVar13 = FUN_00749340(&local_f8);
          FUN_00238b64(local_1d0,uVar13);
          puVar14 = (undefined8 *)FUN_024c3984(&local_f8);
          if (*(char *)((long)puVar14 + 0x17) < '\0') {
            FUN_00018d20(&local_1a0,*puVar14,puVar14[1]);
          }
          else {
            uStack_198 = (undefined1 *)puVar14[1];
            local_1a0 = (long *)*puVar14;
            local_190 = puVar14[2];
          }
          puVar15 = (undefined1 *)FUN_00238320(&local_1c0,&local_1a0);
          uVar5 = *puVar15;
          *puVar15 = local_1d0[0];
          uVar13 = *(undefined8 *)(puVar15 + 8);
          *(undefined8 *)(puVar15 + 8) = local_1c8;
          local_1d0[0] = uVar5;
          local_1c8 = uVar13;
          if ((long)local_190 < 0) {
            __ZdlPvm(local_1a0,local_190 & 0x7fffffffffffffff);
          }
          FUN_001fa1c8(&local_1c8,local_1d0[0]);
        }
        if (*(char *)local_f8 == '\x02') {
          local_e8 = local_e8 + 0x10;
          uVar18 = (ulong)local_280 & 0xff;
        }
        else if (*(char *)local_f8 == '\x01') {
          pplVar19 = pplStack_f0;
          pplVar9 = (long **)pplStack_f0[1];
          if ((long **)pplStack_f0[1] == (long **)0x0) {
            do {
              pplStack_f0 = (long **)pplVar19[2];
              bVar10 = (long **)*pplStack_f0 != pplVar19;
              pplVar19 = pplStack_f0;
            } while (bVar10);
          }
          else {
            do {
              pplStack_f0 = pplVar9;
              pplVar9 = (long **)*pplStack_f0;
            } while ((long **)*pplStack_f0 != (long **)0x0);
          }
          uVar18 = (ulong)local_280 & 0xff;
        }
        else {
          lStack_e0 = lStack_e0 + 1;
          uVar18 = (ulong)local_280 & 0xff;
        }
      }
      if (uVar22 != 0) goto LAB_02878900;
      uVar22 = (ulong)local_1c0 & 0xff;
      if ((char)local_1c0 != '\0') {
        if ((char)local_1c0 == '\x02') {
          if (*local_1b8 != local_1b8[1]) goto LAB_02878900;
          uVar22 = 2;
        }
        else if (((char)local_1c0 == '\x01') && (local_1b8[2] == 0)) {
          uVar22 = 1;
        }
        else {
LAB_02878900:
          uStack_238 = 1;
          local_148 = (undefined8 **)&DAT_aaaaaaaaaaaaaa00;
          local_140 = (ulong *)0x0;
          FUN_00238b64(local_1e0,&local_1b0);
          if ((DAT_0a39ed61 & 1) == 0) {
            uRam000000000a39ed58._0_1_ = s_missing_requiredundefined_fields_088053c0[8];
            uRam000000000a39ed58._1_1_ = s_missing_requiredundefined_fields_088053c0[9];
            uRam000000000a39ed58._2_1_ = s_missing_requiredundefined_fields_088053c0[10];
            uRam000000000a39ed58._3_1_ = s_missing_requiredundefined_fields_088053c0[0xb];
            uRam000000000a39ed58._4_1_ = s_missing_requiredundefined_fields_088053c0[0xc];
            uRam000000000a39ed58._5_1_ = s_missing_requiredundefined_fields_088053c0[0xd];
            uRam000000000a39ed58._6_1_ = s_missing_requiredundefined_fields_088053c0[0xe];
            uRam000000000a39ed58._7_1_ = s_missing_requiredundefined_fields_088053c0[0xf];
            DAT_0a39ed50 = s_missing_requiredundefined_fields_088053c0[0];
            DAT_0a39ed50_1._0_1_ = s_missing_requiredundefined_fields_088053c0[1];
            DAT_0a39ed50_1._1_1_ = s_missing_requiredundefined_fields_088053c0[2];
            DAT_0a39ed50_1._2_1_ = s_missing_requiredundefined_fields_088053c0[3];
            DAT_0a39ed50_1._3_1_ = s_missing_requiredundefined_fields_088053c0[4];
            DAT_0a39ed50_1._4_1_ = s_missing_requiredundefined_fields_088053c0[5];
            DAT_0a39ed50_1._5_1_ = s_missing_requiredundefined_fields_088053c0[6];
            DAT_0a39ed50_1._6_1_ = s_missing_requiredundefined_fields_088053c0[7];
            DAT_0a39ed60 = 0;
            DAT_0a39ed61 = 1;
          }
          puVar15 = (undefined1 *)FUN_002366c8(&local_148,&DAT_0a39ed50);
          uVar5 = *puVar15;
          *puVar15 = local_1e0[0];
          uVar13 = *(undefined8 *)(puVar15 + 8);
          *(undefined8 *)(puVar15 + 8) = local_1d8;
          local_1e0[0] = uVar5;
          local_1d8 = uVar13;
          FUN_001fa1c8(&local_1d8);
          FUN_00238b64(local_1f0,&local_1c0);
          if ((DAT_0a39ed81 & 1) == 0) {
            uRam000000000a39ed78._0_1_ = s_missing_requiredundefined_fields_088053c0[0x18];
            uRam000000000a39ed78._1_1_ = s_missing_requiredundefined_fields_088053c0[0x19];
            uRam000000000a39ed78._2_1_ = s_missing_requiredundefined_fields_088053c0[0x1a];
            uRam000000000a39ed78._3_1_ = s_missing_requiredundefined_fields_088053c0[0x1b];
            uRam000000000a39ed78._4_1_ = s_missing_requiredundefined_fields_088053c0[0x1c];
            uRam000000000a39ed78._5_1_ = s_missing_requiredundefined_fields_088053c0[0x1d];
            uRam000000000a39ed78._6_1_ = s_missing_requiredundefined_fields_088053c0[0x1e];
            uRam000000000a39ed78._7_1_ = s_missing_requiredundefined_fields_088053c0[0x1f];
            DAT_0a39ed70 = s_missing_requiredundefined_fields_088053c0[0x10];
            DAT_0a39ed70_1._0_1_ = s_missing_requiredundefined_fields_088053c0[0x11];
            DAT_0a39ed70_1._1_1_ = s_missing_requiredundefined_fields_088053c0[0x12];
            DAT_0a39ed70_1._2_1_ = s_missing_requiredundefined_fields_088053c0[0x13];
            DAT_0a39ed70_1._3_1_ = s_missing_requiredundefined_fields_088053c0[0x14];
            DAT_0a39ed70_1._4_1_ = s_missing_requiredundefined_fields_088053c0[0x15];
            DAT_0a39ed70_1._5_1_ = s_missing_requiredundefined_fields_088053c0[0x16];
            DAT_0a39ed70_1._6_1_ = s_missing_requiredundefined_fields_088053c0[0x17];
            DAT_0a39ed80 = 0;
            DAT_0a39ed81 = 1;
          }
          puVar15 = (undefined1 *)FUN_002366c8(&local_148,&DAT_0a39ed70);
          uVar5 = *puVar15;
          *puVar15 = local_1f0[0];
          uVar13 = *(undefined8 *)(puVar15 + 8);
          *(undefined8 *)(puVar15 + 8) = local_1e8;
          local_1f0[0] = uVar5;
          local_1e8 = uVar13;
          FUN_001fa1c8(&local_1e8);
          FUN_00225b58(&local_f8,&local_148,0xffffffff,0x20,0,0);
          local_220 = local_e8;
          pplStack_228 = pplStack_f0;
          local_230 = local_f8;
          if (((long)local_e8 < 0) && ((long **)0x1000 < pplStack_f0)) {
            lVar17 = 0x1000;
            do {
              if ((*(byte *)((long)local_f8 + lVar17) & 0xc0) != 0x80) break;
              lVar17 = lVar17 + -1;
            } while (lVar17 != 0);
            __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6resizeEmc
                      (&local_230,lVar17,0);
          }
          FUN_001fa1c8(&local_140,(ulong)local_148 & 0xff);
          uVar22 = (ulong)local_1c0 & 0xff;
        }
      }
      FUN_001fa1c8(&local_1b8,uVar22);
      FUN_001fa1c8(&local_1a8,local_1b0 & 0xff);
      uVar22 = local_310;
      plVar7 = (long *)local_300;
      while (plVar7 != (long *)0x0) {
        lVar17 = *plVar7;
        local_310 = uVar22;
        if (*(char *)((long)plVar7 + 0x27) < '\0') {
          __ZdlPvm(plVar7[2],plVar7[4] & 0x7fffffffffffffff);
        }
        __ZdlPvm(plVar7,0x28);
        uVar22 = local_310;
        plVar7 = (long *)lVar17;
      }
      local_310 = 0;
      if (uVar22 != 0) {
        __ZdlPvm(uVar22,lStack_308 << 3);
      }
    }
    else {
      FUN_04878be8(&local_328,param_1 + 0xa0);
      puVar12 = puStack_278;
      cVar8 = (char)local_280;
      local_280 = (undefined1 **)CONCAT71(local_280._1_7_,local_328);
      local_328 = cVar8;
      puStack_278 = local_320;
      local_320 = puVar12;
      FUN_001fa1c8(&local_320);
      if ((char)local_280 == '\x01') goto LAB_028785cc;
    }
    FUN_001fa1c8(&puStack_278,(ulong)local_280 & 0xff);
  }
  pppuVar1 = (undefined1 ***)(param_1 + 0x48);
  FUN_028583b8(param_1 + 0x60,pppuVar1,uVar3,1,local_33c,&local_210,uVar4,local_240,uStack_238,
               &local_230);
  puStack_258 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
  local_260 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
  puStack_248 = &SUB_aaaaaaaaaaaaaaaa;
  local_250 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
  puStack_278 = (ulong *)&SUB_aaaaaaaaaaaaaaaa;
  local_280 = (undefined1 **)&SUB_aaaaaaaaaaaaaaaa;
  local_268 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
  local_270 = (undefined8 *)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0559f2d8(&local_280);
  if ((DAT_0a39e2b1 & 1) == 0) {
    _DAT_0a39e29c = CONCAT44((int)DAT_08482f20,(int)DAT_08572368);
    uRam000000000a39e2a4 = CONCAT44((int)DAT_088051b8,(int)DAT_08760488);
    DAT_0a39e2ac = (undefined4)DAT_088051c0;
    DAT_0a39e2b0 = 0;
    DAT_0a39e2b1 = 1;
  }
  puStack_248 = (undefined1 *)((ulong)puStack_248 | 0x100000000);
  if (puStack_278 == DAT_0a523c10) {
    puStack_278 = (ulong *)__Znwm(0x18);
    *puStack_278 = 0;
    puStack_278[1] = 0;
    puStack_278[2] = 0;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6assignEPKc
            (puStack_278,&DAT_0a39e29c);
  puStack_248 = (undefined1 *)((ulong)puStack_248 | 0x200000000);
  if (local_270 == &DAT_0a524ad0) {
    local_270 = (undefined8 *)__Znwm(0x18);
    *local_270 = 0;
    local_270[1] = 0;
    local_270[2] = 0;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(local_270,pppuVar1);
  puStack_248 = (undefined1 *)((ulong)puStack_248 | 0x400000000);
  if (local_268 == &DAT_0a524ad0) {
    local_268 = (undefined8 *)__Znwm(0x18);
    *local_268 = 0;
    local_268[1] = 0;
    local_268[2] = 0;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(local_268,param_1 + 0x60)
  ;
  uVar22 = *(ulong *)(param_1 + 0x80);
  if (-1 < (char)*(byte *)(param_1 + 0x8f)) {
    uVar22 = (ulong)*(byte *)(param_1 + 0x8f);
  }
  if (uVar22 != 0) {
    puStack_248 = (undefined1 *)((ulong)puStack_248 | 0x1000000000);
    if (puStack_258 == &DAT_0a524ad0) {
      puStack_258 = (undefined8 *)__Znwm(0x18);
      *puStack_258 = 0;
      puStack_258[1] = 0;
      puStack_258[2] = 0;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (puStack_258,param_1 + 0x78);
  }
  uVar22 = param_3[1];
  if (-1 < (char)*(byte *)((long)param_3 + 0x17)) {
    uVar22 = (ulong)*(byte *)((long)param_3 + 0x17);
  }
  if (uVar22 == 0) {
    puStack_248 = (undefined1 *)((ulong)puStack_248 | 0x800000000);
    if (local_260 == &DAT_0a524ad0) {
      local_260 = (undefined8 *)__Znwm(0x18);
      *local_260 = 0;
      local_260[1] = 0;
      local_260[2] = 0;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(local_260,param_2);
    iVar11 = thunk_FUN_05e1d97c(2);
    if (iVar11 == 0) goto LAB_02879208;
    FUN_0488143c(&local_328);
    pcVar2 = (char *)CONCAT71(uStack_327,local_328);
    if (-1 < cStack_311) {
      pcVar2 = &local_328;
    }
    if ((DAT_0a39e011 & 1) == 0) {
      _DAT_0a39dff8 = CONCAT44((int)DAT_08482f20,(int)DAT_08572368);
      uRam000000000a39e000 = CONCAT44((int)DAT_0849fe78,(int)DAT_08760488);
      DAT_0a39e008 = CONCAT44((int)DAT_0851e180,(int)DAT_0849b068);
      DAT_0a39e010 = 0;
      DAT_0a39e011 = 1;
    }
    if ((DAT_0a39ecfb & 1) == 0) {
      DAT_0a39ecf0._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
      DAT_0a39ecf0._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
      DAT_0a39ecf0._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
      DAT_0a39ecf0._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
      DAT_0a39ecf0._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
      DAT_0a39ecf0._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
      DAT_0a39ecf0._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
      DAT_0a39ecf0._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
      DAT_0a39ecf8 = 0x2928;
      DAT_0a39ecfa = 0;
      DAT_0a39ecfb = 1;
    }
    FUN_05e1d050(&local_310,2,pcVar2,&DAT_0a39dff8,&DAT_0a39ecf0,0x158,0,0);
    local_148 = *(undefined1 ****)(param_1 + 0x48);
    if (-1 < *(char *)(param_1 + 0x5f)) {
      local_148 = pppuVar1;
    }
    local_140 = (ulong *)((ulong)local_140 & 0xffffffffffffff00);
    uVar22 = *(ulong *)(param_2 + 8);
    if (-1 < (char)*(byte *)(param_2 + 0x17)) {
      uVar22 = (ulong)*(byte *)(param_2 + 0x17);
    }
    local_1a0 = &uStack_198;
    if ((DAT_0a39ece8 & 1) == 0) {
      uVar18 = 0;
      do {
        uVar23 = *(undefined4 *)((long)&DAT_08808a13 + uVar18);
        uVar6 = CONCAT12((char)((uint)uVar23 >> 8),(short)uVar23) & 0xff00ff;
        uVar24 = *(undefined4 *)((long)&DAT_088089ff + uVar18 % 0x14);
        *(uint *)((long)&DAT_0a39eca0 + uVar18) =
             CONCAT13((char)((uint)uVar23 >> 0x18) + 0x69U ^ (byte)((uint)uVar24 >> 0x18),
                      CONCAT12((char)((uint)uVar23 >> 0x10) + 0x69U ^ (byte)((uint)uVar24 >> 0x10),
                               CONCAT11((char)(uVar6 >> 0x10) + 0x69U ^ (byte)((uint)uVar24 >> 8),
                                        (char)uVar6 + 0x69U ^ (byte)uVar24)));
        uVar18 = uVar18 + 4;
      } while (uVar18 != 0x48);
      DAT_0a39ece8 = 1;
    }
    lVar17 = 0;
    do {
      lVar21 = lVar17;
      *(undefined1 *)((long)&uStack_198 + lVar21) = *(undefined1 *)(uVar22 % 10 + 0xa39ecc3);
      bVar10 = 9 < uVar22;
      uVar22 = uVar22 / 10;
      lVar17 = lVar21 + 1;
    } while (bVar10);
    *(undefined1 *)((long)&uStack_198 + lVar21 + 1) = 0;
    if (8 < lVar21 + 8U) {
      puVar15 = (undefined1 *)((long)&uStack_198 + lVar21);
      puVar20 = (undefined1 *)((long)&uStack_198 + 1);
      do {
        uVar5 = *puVar15;
        *puVar15 = puVar20[-1];
        puVar20[-1] = uVar5;
        bVar10 = puVar20 < puVar15 + -1;
        puVar15 = puVar15 + -1;
        puVar20 = puVar20 + 1;
      } while (bVar10);
    }
    if ((DAT_0a39ed24 & 1) == 0) {
      _DAT_0a39ecfc = CONCAT44((int)ram0x085cdbd8,(int)DAT_0848e640);
      uRam000000000a39ed04 = CONCAT44((int)DAT_084d0ff8,(int)DAT_085e6698);
      _DAT_0a39ed0c = CONCAT44((int)DAT_084c77e8,(int)DAT_084d8400);
      uRam000000000a39ed14 = CONCAT44((int)DAT_088051c0,(int)ram0x088052e0);
      DAT_0a39ed1c = CONCAT44((int)DAT_084fbc10,(int)DAT_088052e8);
      DAT_0a39ed24 = 1;
    }
    local_f8 = (undefined1 ***)&local_148;
    pplStack_f0 = &local_1a0;
    lStack_e0 = 0;
    local_e8 = 0;
    uStack_d0 = 0;
    local_d8 = 0;
    uStack_c0 = 0;
    local_c8 = 0;
    uStack_b0 = 0;
    local_b8 = 0;
    uStack_a0 = 0;
    local_a8 = 0;
    uStack_90 = 0;
    local_98 = 0;
    uStack_80 = 0;
    local_88 = 0;
    FUN_05e1d31c(&local_310,&DAT_0a39ecfc,&local_f8);
  }
  else {
    puStack_248 = (undefined1 *)((ulong)puStack_248 | 0x2000000000);
    if (local_250 == &DAT_0a524ad0) {
      local_250 = (undefined8 *)__Znwm(0x18);
      *local_250 = 0;
      local_250[1] = 0;
      local_250[2] = 0;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(local_250,param_3);
    iVar11 = thunk_FUN_05e1d97c(2);
    if (iVar11 == 0) goto LAB_02879208;
    FUN_0488143c(&local_328);
    pcVar2 = (char *)CONCAT71(uStack_327,local_328);
    if (-1 < cStack_311) {
      pcVar2 = &local_328;
    }
    if ((DAT_0a39e011 & 1) == 0) {
      _DAT_0a39dff8 = CONCAT44((int)DAT_08482f20,(int)DAT_08572368);
      uRam000000000a39e000 = CONCAT44((int)DAT_0849fe78,(int)DAT_08760488);
      DAT_0a39e008 = CONCAT44((int)DAT_0851e180,(int)DAT_0849b068);
      DAT_0a39e010 = 0;
      DAT_0a39e011 = 1;
    }
    if ((DAT_0a39ecfb & 1) == 0) {
      DAT_0a39ecf0._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
      DAT_0a39ecf0._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
      DAT_0a39ecf0._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
      DAT_0a39ecf0._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
      DAT_0a39ecf0._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
      DAT_0a39ecf0._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
      DAT_0a39ecf0._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
      DAT_0a39ecf0._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
      DAT_0a39ecf8 = 0x2928;
      DAT_0a39ecfa = 0;
      DAT_0a39ecfb = 1;
    }
    FUN_05e1d050(&local_310,2,pcVar2,&DAT_0a39dff8,&DAT_0a39ecf0,0x15b,0,0);
    local_148 = *(undefined1 ****)(param_1 + 0x48);
    if (-1 < *(char *)(param_1 + 0x5f)) {
      local_148 = pppuVar1;
    }
    local_140 = (ulong *)((ulong)local_140 & 0xffffffffffffff00);
    local_1a0 = (long *)*param_3;
    if (-1 < *(char *)((long)param_3 + 0x17)) {
      local_1a0 = param_3;
    }
    uStack_198 = (undefined1 *)((ulong)uStack_198 & 0xffffffffffffff00);
    if ((DAT_0a39ed4b & 1) == 0) {
      _DAT_0a39ed28 = CONCAT44((int)ram0x085cdbd8,(int)DAT_0848e640);
      uRam000000000a39ed30 = CONCAT44((int)DAT_084d0ff8,(int)DAT_085e6698);
      _DAT_0a39ed38 = CONCAT44((int)DAT_08480a00,(int)DAT_08771580);
      uRam000000000a39ed40 = CONCAT44((int)DAT_086cacf0,(int)DAT_08766b58);
      DAT_0a39ed48 = 0x5f25;
      DAT_0a39ed4a = 0;
      DAT_0a39ed4b = 1;
    }
    local_f8 = (undefined1 ***)&local_148;
    pplStack_f0 = &local_1a0;
    lStack_e0 = 0;
    local_e8 = 0;
    uStack_d0 = 0;
    local_d8 = 0;
    uStack_c0 = 0;
    local_c8 = 0;
    uStack_b0 = 0;
    local_b8 = 0;
    uStack_a0 = 0;
    local_a8 = 0;
    uStack_90 = 0;
    local_98 = 0;
    uStack_80 = 0;
    local_88 = 0;
    FUN_05e1d31c(&local_310,&DAT_0a39ed28,&local_f8);
  }
  thunk_FUN_05e1d0bc(&local_310);
  if (cStack_311 < '\0') {
    __ZdlPvm(CONCAT71(uStack_327,local_328),CONCAT17(cStack_311,local_318) & 0x7fffffffffffffff);
  }
LAB_02879208:
  FUN_02857158(uVar16,param_1 + 0x30,&local_280);
  FUN_055bf9ec(&local_280);
  if ((long)local_220 < 0) {
    __ZdlPvm(local_230,local_220 & 0x7fffffffffffffff);
  }
  if ((long)local_200 < 0) {
    __ZdlPvm(local_210,local_200 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_78) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


