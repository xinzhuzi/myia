// Ghidra inferred pseudocode; requested=0x4cbb054
// entry=04cbb054 end=04cbb543

undefined8 * FUN_04cbb054(undefined8 *param_1,long param_2)

{
  size_t sVar1;
  size_t sVar2;
  undefined8 ****ppppuVar3;
  uint uVar4;
  byte bVar5;
  byte bVar6;
  bool bVar7;
  int iVar8;
  undefined8 *puVar9;
  long *plVar10;
  char *pcVar11;
  undefined8 uVar12;
  char *pcVar13;
  long lVar14;
  ulong uVar15;
  long lVar16;
  char *pcVar17;
  undefined8 ***local_188 [2];
  undefined7 local_178;
  char cStack_171;
  undefined8 local_170 [2];
  undefined7 local_160;
  char cStack_159;
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
  *param_1 = &PTR_thunk_FUN_00ac6290_09eb04f0;
  param_1[1] = 0;
  *(undefined4 *)(param_1 + 2) = 0;
  pcVar17 = (char *)(param_1 + 3);
  param_1[4] = 0;
  pcVar17[0] = '\0';
  pcVar17[1] = '\0';
  pcVar17[2] = '\0';
  pcVar17[3] = '\0';
  pcVar17[4] = '\0';
  pcVar17[5] = '\0';
  pcVar17[6] = '\0';
  pcVar17[7] = '\0';
  param_1[0x10] = 0;
  param_1[0xf] = 0;
  param_1[0x14] = 0;
  param_1[0x13] = 0;
  param_1[0x16] = 0;
  param_1[0x15] = 0;
  param_1[6] = 0;
  param_1[5] = 0;
  param_1[8] = 0;
  param_1[7] = 0;
  param_1[10] = 0;
  param_1[9] = 0;
  param_1[0xc] = 0;
  param_1[0xb] = 0;
  param_1[0xe] = 0;
  param_1[0xd] = 0;
  *(undefined8 *)((long)param_1 + 0x8a) = 0;
  *(undefined8 *)((long)param_1 + 0x82) = 0;
  *(undefined4 *)(param_1 + 0x17) = 0x3f800000;
  param_1[0x19] = 0;
  param_1[0x18] = 0;
  param_1[0x1b] = 0;
  param_1[0x1a] = 0;
  param_1[0x1d] = 0;
  param_1[0x1c] = 0;
  *(undefined2 *)(param_1 + 0x1e) = 0;
  *(undefined8 *)((long)param_1 + 0xfc) = 0;
  *(undefined8 *)((long)param_1 + 0xf4) = 0;
  *(undefined8 *)((long)param_1 + 0x124) = 0;
  *(undefined8 *)((long)param_1 + 0x10c) = 0;
  *(undefined8 *)((long)param_1 + 0x104) = 0;
  *(undefined8 *)((long)param_1 + 0x11c) = 0;
  *(undefined8 *)((long)param_1 + 0x114) = 0;
  param_1[0x2f] = 0;
  param_1[0x2e] = 0;
  param_1[0x31] = 0;
  param_1[0x30] = 0;
  param_1[0x2b] = 0;
  param_1[0x2a] = 0;
  param_1[0x2d] = 0;
  param_1[0x2c] = 0;
  param_1[0x27] = 0;
  param_1[0x26] = 0;
  param_1[0x29] = 0;
  param_1[0x28] = 0;
  FUN_04ea6ba0(param_1 + 0x32);
  puVar9 = (undefined8 *)__Znwm(0x20);
  puVar9[2] = 0;
  puVar9[1] = 0;
  *puVar9 = &PTR_FUN_09c08428;
  puVar9[3] = 0;
  param_1[0x41] = puVar9 + 3;
  param_1[0x42] = puVar9;
  *(undefined1 *)(param_1 + 0x43) = 0;
  param_1[0x45] = 0;
  param_1[0x44] = 0;
  param_1[0x47] = 0;
  param_1[0x46] = 0;
  *(undefined1 *)(param_1 + 0x48) = 1;
  param_1[0x4c] = 0;
  param_1[0x4e] = 0;
  param_1[0x4d] = 0;
  *(undefined1 *)(param_1 + 0x4b) = 0;
  param_1[0x4a] = 0;
  param_1[0x49] = 0;
  param_1[0x1f] = *(undefined8 *)(param_2 + 0x50);
  lVar14 = *(long *)(param_2 + 0x20);
  if (lVar14 == 0) {
    lVar14 = *(long *)(DAT_0a521850 + 0x20);
  }
  uVar12 = *(undefined8 *)(lVar14 + 8);
  *(undefined1 *)(param_1 + 0x4b) = 0;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_1 + 0x26,uVar12);
  uVar4 = *(uint *)(param_2 + 0x48);
  *(uint *)((long)param_1 + 0x114) = uVar4;
  param_1[0x20] = (ulong)uVar4 * 1000;
  *(undefined4 *)(param_1 + 0x23) = *(undefined4 *)(param_2 + 0x28);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 0x2c,*(undefined8 *)(param_2 + 0x38));
  *(undefined4 *)((long)param_1 + 0x124) = *(undefined4 *)(param_2 + 0x4c);
  lVar14 = *(long *)(param_2 + 8);
  if (lVar14 == 0) {
    lVar14 = *(long *)(DAT_0a521850 + 8);
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (pcVar17,*(undefined8 *)(lVar14 + 8));
  lVar14 = *(long *)(param_2 + 0x18);
  if (lVar14 == 0) {
    lVar14 = *(long *)(DAT_0a521850 + 0x18);
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 6,*(undefined8 *)(lVar14 + 8));
  FUN_04cbbc88(local_170,param_1);
  FUN_04cbb728(param_1,local_170);
  if (cStack_159 < '\0') {
    __ZdlPvm(local_170[0],CONCAT17(cStack_159,local_160) & 0x7fffffffffffffff);
  }
  uVar12 = *(undefined8 *)(param_2 + 0x60);
  *(uint *)((long)param_1 + 0x204) = *(uint *)((long)param_1 + 0x204) | 0x400;
  param_1[0x3c] = uVar12;
  FUN_04cbbd20(param_1,*(undefined4 *)(param_2 + 0x14));
  plVar10 = (long *)FUN_04669774();
  pcVar11 = (char *)(**(code **)(*plVar10 + 0x28))();
  if (*(int *)((long)param_1 + 0xc) == 10000) {
    bVar5 = *(byte *)((long)param_1 + 0x2f);
    uVar15 = (ulong)bVar5;
    sVar1 = param_1[4];
    if (-1 < (char)bVar5) {
      sVar1 = uVar15;
    }
    bVar6 = pcVar11[0x17];
    sVar2 = *(size_t *)(pcVar11 + 8);
    if (-1 < (char)bVar6) {
      sVar2 = (ulong)bVar6;
    }
    if (sVar1 == sVar2) {
      pcVar13 = *(char **)pcVar11;
      if (-1 < (char)bVar6) {
        pcVar13 = pcVar11;
      }
      if ((char)bVar5 < '\0') {
        iVar8 = _memcmp(*(void **)pcVar17,pcVar13,param_1[4]);
        if (iVar8 != 0) goto LAB_04cbb324;
      }
      else {
        pcVar11 = pcVar17;
        if (bVar5 != 0) {
          do {
            if (*pcVar11 != *pcVar13) goto LAB_04cbb324;
            pcVar13 = pcVar13 + 1;
            uVar15 = uVar15 - 1;
            pcVar11 = pcVar11 + 1;
          } while (uVar15 != 0);
        }
      }
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(pcVar17,param_1 + 6);
      lVar14 = *(long *)(param_2 + 8);
      if (lVar14 == 0) {
        lVar14 = *(long *)(DAT_0a521850 + 8);
      }
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (param_1 + 6,*(undefined8 *)(lVar14 + 8));
    }
  }
LAB_04cbb324:
  lVar16 = *(long *)(param_2 + 0x30);
  lVar14 = lVar16;
  if (lVar16 == 0) {
    lVar14 = *(long *)(DAT_0a521850 + 0x30);
  }
  bVar7 = *(int *)((long)param_1 + 0xc) != 0x22;
  if (*(int *)(lVar14 + 0x10) == 0) {
    if (!bVar7) {
      iVar8 = thunk_FUN_05e1d97c(3);
      if (iVar8 != 0) {
        FUN_0488143c(local_188);
        ppppuVar3 = (undefined8 ****)local_188[0];
        if (-1 < cStack_171) {
          ppppuVar3 = local_188;
        }
        if ((DAT_0a4ad97b & 1) == 0) {
          DAT_0a4ad970._0_1_ = s_message_SetSendeSetType_08ad4560[0];
          DAT_0a4ad970._1_1_ = s_message_SetSendeSetType_08ad4560[1];
          DAT_0a4ad970._2_1_ = s_message_SetSendeSetType_08ad4560[2];
          DAT_0a4ad970._3_1_ = s_message_SetSendeSetType_08ad4560[3];
          DAT_0a4ad970._4_1_ = s_message_SetSendeSetType_08ad4560[4];
          DAT_0a4ad970._5_1_ = s_message_SetSendeSetType_08ad4560[5];
          DAT_0a4ad970._6_1_ = s_message_SetSendeSetType_08ad4560[6];
          DAT_0a4ad970._7_1_ = s_message_SetSendeSetType_08ad4560[7];
          DAT_0a4ad978 = 0x6363;
          DAT_0a4ad97a = 0;
          DAT_0a4ad97b = 1;
        }
        if ((DAT_0a4ad988 & 1) == 0) {
          DAT_0a4ad980[0] = s_Message_08901908[0];
          DAT_0a4ad980[1] = s_Message_08901908[1];
          DAT_0a4ad980[2] = s_Message_08901908[2];
          DAT_0a4ad980[3] = s_Message_08901908[3];
          DAT_0a4ad980[4] = s_Message_08901908[4];
          DAT_0a4ad980[5] = s_Message_08901908[5];
          DAT_0a4ad980[6] = s_Message_08901908[6];
          DAT_0a4ad980[7] = s_Message_08901908[7];
          DAT_0a4ad988 = 1;
        }
        FUN_05e1d050(local_170,3,ppppuVar3,&DAT_0a4ad970,DAT_0a4ad980,0x6f,0,0);
        if ((DAT_0a4ad99f & 1) == 0) {
          uVar15 = 0;
          do {
            (&DAT_0a4ad989)[uVar15] = (&DAT_08ad4c6c)[uVar15 & 0xf] ^ (&DAT_08ad4c7c)[uVar15];
            uVar15 = uVar15 + 1;
          } while (uVar15 != 0x16);
          DAT_0a4ad99f = 1;
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
        FUN_05e1d31c(local_170,&DAT_0a4ad989,&local_e0);
        thunk_FUN_05e1d0bc(local_170);
        if (cStack_171 < '\0') {
          __ZdlPvm(local_188[0],CONCAT17(cStack_171,local_178) & 0x7fffffffffffffff);
        }
      }
      *(undefined4 *)(param_1 + 0x24) = 0;
    }
  }
  else if (bVar7) {
    if (lVar16 == 0) {
      lVar16 = *(long *)(DAT_0a521850 + 0x30);
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (param_1 + 0xc,*(undefined8 *)(lVar16 + 8));
  }
  else {
    if (lVar16 == 0) {
      lVar16 = *(long *)(DAT_0a521850 + 0x30);
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (param_1 + 0xf,*(undefined8 *)(lVar16 + 8));
    *(undefined4 *)(param_1 + 0x24) = 1;
  }
  FUN_04cbc3ac(param_1,1);
  FUN_04cbc4c0(param_1,1);
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_58) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return param_1;
}


