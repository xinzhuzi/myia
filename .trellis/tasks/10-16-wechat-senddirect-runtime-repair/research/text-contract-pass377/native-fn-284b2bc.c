// Ghidra inferred pseudocode; requested=0x284b2bc
// entry=0284b2bc end=0284bbaf

/* WARNING: Removing unreachable block (ram,0x0284baf8) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0284b2bc(undefined8 param_1,int param_2,undefined8 ******param_3,undefined8 param_4,
                 long param_5)

{
  uint uVar1;
  undefined8 *****pppppuVar2;
  undefined8 *****pppppuVar3;
  undefined8 ******ppppppuVar4;
  byte bVar5;
  byte bVar6;
  undefined1 uVar7;
  undefined4 uVar8;
  uint3 uVar9;
  bool bVar10;
  int iVar11;
  long lVar12;
  long *plVar13;
  undefined8 *puVar14;
  size_t sVar15;
  undefined8 ******ppppppuVar16;
  long lVar17;
  long lVar18;
  undefined1 *puVar19;
  undefined1 *puVar20;
  ulong uVar21;
  undefined4 uVar22;
  undefined1 auStack_368 [8];
  undefined8 local_360;
  undefined7 local_350;
  char cStack_349;
  long *local_340;
  undefined8 *****local_338 [2];
  undefined7 local_328;
  char cStack_321;
  undefined8 *****local_320;
  undefined1 *local_318;
  undefined1 *local_310;
  undefined8 *****local_290;
  undefined1 *puStack_288;
  undefined1 *local_280;
  undefined8 *****local_270;
  undefined8 ****ppppuStack_268;
  undefined8 ****local_260;
  undefined8 *****local_250;
  undefined8 ****ppppuStack_248;
  undefined8 local_240;
  undefined8 *****local_238;
  undefined1 local_230;
  undefined8 *****local_1e8;
  undefined1 local_1e0;
  undefined8 *****local_198;
  undefined1 local_190;
  undefined1 uStack_149;
  undefined8 local_148;
  undefined8 local_140;
  undefined8 *****local_f8;
  undefined8 *****pppppuStack_f0;
  undefined8 *****local_e8;
  undefined8 *****pppppuStack_e0;
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
  lVar12 = __Znwm(0x98);
  FUN_05130244();
  *(uint *)(lVar12 + 0x94) = *(uint *)(lVar12 + 0x94) | 1;
  *(undefined4 *)(lVar12 + 0x20) = 0x33;
  ppppuStack_248 = (undefined8 ****)&SUB_aaaaaaaaaaaaaaaa;
  local_240 = &SUB_aaaaaaaaaaaaaaaa;
  local_250 = (undefined8 *****)&SUB_aaaaaaaaaaaaaaaa;
  plVar13 = (long *)FUN_04669774();
  puVar14 = (undefined8 *)(**(code **)(*plVar13 + 0x28))();
  if (*(char *)((long)puVar14 + 0x17) < '\0') {
    FUN_00018d20(&local_250,*puVar14,puVar14[1]);
  }
  else {
    ppppuStack_248 = (undefined8 ****)puVar14[1];
    local_250 = (undefined8 *****)*puVar14;
    local_240 = (undefined1 *)puVar14[2];
  }
  *(uint *)(lVar12 + 0x94) = *(uint *)(lVar12 + 0x94) | 2;
  puVar14 = *(undefined8 **)(lVar12 + 8);
  if (puVar14 == &DAT_0a524ad0) {
    puVar14 = (undefined8 *)__Znwm(0x18);
    *puVar14 = 0;
    puVar14[1] = 0;
    puVar14[2] = 0;
    *(undefined8 **)(lVar12 + 8) = puVar14;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar14,&local_250);
  ppppuStack_268 = (undefined8 ****)&SUB_aaaaaaaaaaaaaaaa;
  local_260 = (undefined8 ****)&SUB_aaaaaaaaaaaaaaaa;
  local_270 = (undefined8 *****)&SUB_aaaaaaaaaaaaaaaa;
  bVar5 = *(byte *)((long)param_3 + 0x17);
  pppppuVar3 = param_3[1];
  if (-1 < (char)bVar5) {
    pppppuVar3 = (undefined8 *****)(ulong)bVar5;
  }
  ppppppuVar16 = &local_250;
  if (pppppuVar3 != (undefined8 *****)0x0) {
    ppppppuVar16 = param_3;
  }
  bVar6 = local_240._7_1_;
  if (pppppuVar3 != (undefined8 *****)0x0) {
    bVar6 = bVar5;
  }
  if ((char)bVar6 < '\0') {
    pppppuVar2 = (undefined8 *****)ppppuStack_248;
    if (pppppuVar3 != (undefined8 *****)0x0) {
      pppppuVar2 = param_3[1];
    }
    FUN_00018d20(&local_270,*ppppppuVar16,pppppuVar2);
  }
  else {
    ppppuStack_268 = ppppppuVar16[1];
    local_270 = *ppppppuVar16;
    local_260 = ppppppuVar16[2];
  }
  *(uint *)(lVar12 + 0x94) = *(uint *)(lVar12 + 0x94) | 4;
  puVar14 = *(undefined8 **)(lVar12 + 0x10);
  if (puVar14 == &DAT_0a524ad0) {
    puVar14 = (undefined8 *)__Znwm(0x18);
    *puVar14 = 0;
    puVar14[1] = 0;
    puVar14[2] = 0;
    *(undefined8 **)(lVar12 + 0x10) = puVar14;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar14,&local_270);
  puVar19 = local_240;
  puStack_288 = &SUB_aaaaaaaaaaaaaaaa;
  local_280 = &SUB_aaaaaaaaaaaaaaaa;
  local_290 = (undefined8 *****)&SUB_aaaaaaaaaaaaaaaa;
  if ((DAT_0a39de0a & 1) == 0) {
    DAT_0a39de08 = 0x5f;
    DAT_0a39de0a = 1;
  }
  pppppuVar3 = (undefined8 *****)ppppuStack_248;
  if (-1 < (long)local_240) {
    pppppuVar3 = (undefined8 *****)((ulong)local_240 >> 0x38);
  }
  sVar15 = _strlen((char *)&DAT_0a39de08);
  local_320 = (undefined8 *****)&SUB_aaaaaaaaaaaaaaaa;
  local_318 = &SUB_aaaaaaaaaaaaaaaa;
  local_310 = &SUB_aaaaaaaaaaaaaaaa;
  puVar20 = (undefined1 *)((long)pppppuVar3 + sVar15);
  if ((undefined1 *)0x7ffffffffffffff7 < puVar20) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_320);
  }
  if (puVar20 < (undefined1 *)0x17) {
    local_318 = (undefined1 *)0x0;
    local_320 = (undefined8 ******)0x0;
    ppppppuVar16 = &local_320;
    local_310 = (undefined1 *)((long)puVar20 << 0x38);
  }
  else {
    uVar21 = 0x19;
    if (((ulong)puVar20 | 7) != 0x17) {
      uVar21 = ((ulong)puVar20 | 7) + 1;
    }
    ppppppuVar16 = (undefined8 ******)__Znwm(uVar21);
    local_310 = (undefined1 *)(uVar21 | 0x8000000000000000);
    local_318 = puVar20;
    local_320 = ppppppuVar16;
  }
  if (pppppuVar3 != (undefined8 *****)0x0) {
    ppppppuVar4 = (undefined8 ******)local_250;
    if (-1 < (long)puVar19) {
      ppppppuVar4 = &local_250;
    }
    _memmove(ppppppuVar16,ppppppuVar4,(size_t)pppppuVar3);
  }
  if (sVar15 != 0) {
    _memmove((undefined1 *)((long)ppppppuVar16 + (long)pppppuVar3),&DAT_0a39de08,sVar15);
  }
  ((undefined1 *)((long)ppppppuVar16 + (long)pppppuVar3))[sVar15] = 0;
  FUN_047471b0();
  FUN_000622d4(&local_f8);
  ppppppuVar16 = (undefined8 ******)pppppuStack_f0;
  ppppppuVar4 = (undefined8 ******)local_f8;
  if (-1 < (long)local_e8) {
    ppppppuVar16 = (undefined8 ******)((ulong)local_e8 >> 0x38);
    ppppppuVar4 = &local_f8;
  }
  plVar13 = (long *)__ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKcm
                              (&local_320,ppppppuVar4,ppppppuVar16);
  puStack_288 = (undefined1 *)plVar13[1];
  local_290 = (undefined8 *****)*plVar13;
  local_280 = (undefined1 *)plVar13[2];
  plVar13[1] = 0;
  plVar13[2] = 0;
  *plVar13 = 0;
  if ((long)local_310 < 0) {
    __ZdlPvm(local_320,(ulong)local_310 & 0x7fffffffffffffff);
  }
  *(uint *)(lVar12 + 0x94) = *(uint *)(lVar12 + 0x94) | 8;
  puVar14 = *(undefined8 **)(lVar12 + 0x18);
  if (puVar14 == &DAT_0a524ad0) {
    puVar14 = (undefined8 *)__Znwm(0x18);
    *puVar14 = 0;
    puVar14[1] = 0;
    puVar14[2] = 0;
    *(undefined8 **)(lVar12 + 0x18) = puVar14;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar14,&local_290);
  *(uint *)(lVar12 + 0x94) = *(uint *)(lVar12 + 0x94) | 0x40;
  puVar14 = *(undefined8 **)(lVar12 + 0x38);
  if (puVar14 == &DAT_0a524ad0) {
    puVar14 = (undefined8 *)__Znwm(0x18);
    *puVar14 = 0;
    puVar14[1] = 0;
    puVar14[2] = 0;
    *(undefined8 **)(lVar12 + 0x38) = puVar14;
  }
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar14,&local_270);
  lVar17 = __Znwm(0x28);
  FUN_0513021c();
  *(uint *)(lVar17 + 0x20) = *(uint *)(lVar17 + 0x20) | 2;
  *(int *)(lVar17 + 0x18) = param_2;
  uVar21 = *(ulong *)(param_5 + 8);
  if (-1 < (char)*(byte *)(param_5 + 0x17)) {
    uVar21 = (ulong)*(byte *)(param_5 + 0x17);
  }
  if (uVar21 != 0) {
    lVar18 = __Znwm(0x20);
    FUN_05130200();
    *(uint *)(lVar18 + 0x1c) = *(uint *)(lVar18 + 0x1c) | 1;
    puVar14 = *(undefined8 **)(lVar18 + 8);
    if (puVar14 == &DAT_0a524ad0) {
      puVar14 = (undefined8 *)__Znwm(0x18);
      *puVar14 = 0;
      puVar14[1] = 0;
      puVar14[2] = 0;
      *(undefined8 **)(lVar18 + 8) = puVar14;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar14,param_4);
    *(uint *)(lVar18 + 0x1c) = *(uint *)(lVar18 + 0x1c) | 2;
    puVar14 = *(undefined8 **)(lVar18 + 0x10);
    if (puVar14 == &DAT_0a524ad0) {
      puVar14 = (undefined8 *)__Znwm(0x18);
      *puVar14 = 0;
      puVar14[1] = 0;
      puVar14[2] = 0;
      *(undefined8 **)(lVar18 + 0x10) = puVar14;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(puVar14,param_5);
    if (*(long **)(lVar17 + 0x10) != (long *)0x0) {
      (**(code **)(**(long **)(lVar17 + 0x10) + 8))();
    }
    *(long *)(lVar17 + 0x10) = lVar18;
    *(uint *)(lVar17 + 0x20) =
         *(uint *)(lVar17 + 0x20) & 0xfffffff8 |
         *(uint *)(lVar17 + 0x20) & 3 | (uint)(lVar18 != 0) << 2;
  }
  if (*(long **)(lVar12 + 0x80) != (long *)0x0) {
    (**(code **)(**(long **)(lVar12 + 0x80) + 8))();
  }
  *(long *)(lVar12 + 0x80) = lVar17;
  *(uint *)(lVar12 + 0x94) =
       *(uint *)(lVar12 + 0x94) & 0xfffe0000 |
       *(uint *)(lVar12 + 0x94) & 0xffff | (uint)(lVar17 != 0) << 0x10;
  iVar11 = thunk_FUN_05e1d97c(2);
  if (iVar11 != 0) {
    FUN_0488143c(local_338);
    ppppppuVar16 = (undefined8 ******)local_338[0];
    if (-1 < cStack_321) {
      ppppppuVar16 = local_338;
    }
    if ((DAT_0a39dcf7 & 1) == 0) {
      DAT_0a39dce8._0_1_ = s_byp_hand_byp_08804940[0];
      DAT_0a39dce8._1_1_ = s_byp_hand_byp_08804940[1];
      DAT_0a39dce8._2_1_ = s_byp_hand_byp_08804940[2];
      DAT_0a39dce8._3_1_ = s_byp_hand_byp_08804940[3];
      DAT_0a39dce8._4_1_ = s_byp_hand_byp_08804940[4];
      DAT_0a39dce8._5_1_ = s_byp_hand_byp_08804940[5];
      DAT_0a39dce8._6_1_ = s_byp_hand_byp_08804940[6];
      DAT_0a39dce8._7_1_ = s_byp_hand_byp_08804940[7];
      DAT_0a39dcf0 = (undefined4)DAT_08549b60;
      DAT_0a39dcf4 = 0x6363;
      DAT_0a39dcf6 = 0;
      DAT_0a39dcf7 = 1;
    }
    if ((DAT_0a39debd & 1) == 0) {
      _DAT_0a39dea0 = CONCAT44((int)DAT_08804968,(int)DAT_087e2f50);
      uRam000000000a39dea8 = CONCAT44((int)DAT_088049c0,(int)DAT_087fa938);
      DAT_0a39deb0 = CONCAT44((int)DAT_088049c8,(int)DAT_084abdd8);
      DAT_0a39deb8 = (undefined4)DAT_085231f0;
      DAT_0a39debc = 0;
      DAT_0a39debd = 1;
    }
    FUN_05e1d050(&local_320,2,ppppppuVar16,&DAT_0a39dce8,&DAT_0a39dea0,299,0,0);
    local_148 = (undefined8 *****)0x0;
    if ((DAT_0a39df51 & 1) == 0) {
      uVar21 = 0;
      do {
        uVar22 = *(undefined4 *)((long)&DAT_08804e86 + uVar21);
        uVar9 = CONCAT12((char)((uint)uVar22 >> 8),(short)uVar22) & 0xff00ff;
        uVar8 = *(undefined4 *)((long)&DAT_08804e72 + uVar21 % 0x14);
        *(uint *)((long)&DAT_0a39df09 + uVar21) =
             CONCAT13((char)((uint)uVar22 >> 0x18) + 0x8aU ^ (byte)((uint)uVar8 >> 0x18),
                      CONCAT12((char)((uint)uVar22 >> 0x10) + 0x8aU ^ (byte)((uint)uVar8 >> 0x10),
                               CONCAT11((char)(uVar9 >> 0x10) + 0x8aU ^ (byte)((uint)uVar8 >> 8),
                                        (char)uVar9 + 0x8aU ^ (byte)uVar8)));
        uVar21 = uVar21 + 4;
      } while (uVar21 != 0x48);
      DAT_0a39df51 = 1;
    }
    lVar17 = 8;
    iVar11 = param_2;
    do {
      lVar18 = lVar17;
      *(undefined1 *)((long)&local_148 + lVar18) =
           *(undefined1 *)((long)&DAT_0a39df09 + (long)(iVar11 % 10 + 0x23));
      lVar17 = lVar18 + 1;
      uVar1 = iVar11 + 9;
      iVar11 = iVar11 / 10;
    } while (0x12 < uVar1);
    if (param_2 < 0) {
      *(undefined1 *)((long)&local_148 + lVar18 + 1) = 0x2d;
      lVar17 = lVar18 + 2;
    }
    *(undefined1 *)((long)&local_148 + lVar17) = 0;
    if (9 < lVar17) {
      puVar19 = &uStack_149 + lVar17;
      puVar20 = (undefined1 *)((long)&local_140 + 1);
      do {
        uVar7 = *puVar19;
        *puVar19 = puVar20[-1];
        puVar20[-1] = uVar7;
        bVar10 = puVar20 < puVar19 + -1;
        puVar19 = puVar19 + -1;
        puVar20 = puVar20 + 1;
      } while (bVar10);
    }
    local_198 = local_250;
    if (-1 < (long)local_240) {
      local_198 = &local_250;
    }
    local_190 = 0;
    local_1e8 = local_270;
    if (-1 < (long)local_260) {
      local_1e8 = &local_270;
    }
    local_1e0 = 0;
    local_238 = local_290;
    if (-1 < (long)local_280) {
      local_238 = &local_290;
    }
    local_230 = 0;
    if ((DAT_0a39df08 & 1) == 0) {
      uVar21 = 0;
      do {
        uVar22 = *(undefined4 *)((long)&DAT_08804e0b + uVar21);
        uVar9 = CONCAT12((char)((uint)uVar22 >> 8),(short)uVar22) & 0xff00ff;
        uVar8 = *(undefined4 *)((long)&DAT_08804df7 + uVar21 % 0x14);
        *(uint *)((long)&DAT_0a39debe + uVar21) =
             CONCAT13((char)((uint)uVar22 >> 0x18) + 0x8aU ^ (byte)((uint)uVar8 >> 0x18),
                      CONCAT12((char)((uint)uVar22 >> 0x10) + 0x8aU ^ (byte)((uint)uVar8 >> 0x10),
                               CONCAT11((char)(uVar9 >> 0x10) + 0x8aU ^ (byte)((uint)uVar8 >> 8),
                                        (char)uVar9 + 0x8aU ^ (byte)uVar8)));
        uVar21 = uVar21 + 4;
      } while (uVar21 != 0x48);
      DAT_0a39df06 = 0x5f;
      DAT_0a39df08 = 1;
    }
    local_f8 = (undefined8 *****)&local_148;
    pppppuStack_f0 = &local_198;
    local_e8 = &local_1e8;
    pppppuStack_e0 = &local_238;
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
    local_148 = (undefined8 *****)&local_140;
    FUN_05e1d31c(&local_320,&DAT_0a39debe,&local_f8);
    thunk_FUN_05e1d0bc(&local_320);
    if (cStack_321 < '\0') {
      __ZdlPvm(local_338[0],CONCAT17(cStack_321,local_328) & 0x7fffffffffffffff);
    }
  }
  FUN_02846da8(auStack_368,param_1,lVar12);
  if (local_340 != (long *)0x0) {
    LOAcquire();
    lVar12 = local_340[1];
    local_340[1] = lVar12 + -1;
    LORelease();
    if (lVar12 == 0) {
      (**(code **)(*local_340 + 0x10))(local_340);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_340);
    }
  }
  if (cStack_349 < '\0') {
    __ZdlPvm(local_360,CONCAT17(cStack_349,local_350) & 0x7fffffffffffffff);
  }
  if ((long)local_280 < 0) {
    __ZdlPvm(local_290,(ulong)local_280 & 0x7fffffffffffffff);
  }
  if ((long)local_260 < 0) {
    __ZdlPvm(local_270,(ulong)local_260 & 0x7fffffffffffffff);
  }
  if ((long)local_240 < 0) {
    __ZdlPvm(local_250,(ulong)local_240 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_78) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


