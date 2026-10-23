// Ghidra inferred pseudocode; requested=0x2b1650
// entry=002b1650 end=002b1f83

/* WARNING: Function: _objc_retain replaced with injection: _objc_retain_fixup */
/* WARNING: Function: _objc_retainAutoreleasedReturnValue replaced with injection:
   _objc_retain_fixup */
/* WARNING: Function: _objc_release replaced with injection: _objc_release_fixup */
/* WARNING: Removing unreachable block (ram,0x002b1f64) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_002b1650(undefined8 param_1,ID param_2,ID param_3)

{
  uint uVar1;
  char *pcVar2;
  undefined1 uVar3;
  undefined4 uVar4;
  uint3 uVar5;
  undefined8 uVar6;
  int *piVar7;
  bool bVar8;
  int iVar9;
  ID IVar10;
  void *pvVar11;
  long *plVar12;
  ulong *puVar13;
  size_t sVar14;
  undefined8 ******ppppppuVar15;
  undefined8 *******pppppppuVar16;
  undefined1 *puVar17;
  long lVar18;
  long lVar19;
  ulong uVar20;
  ID IVar21;
  undefined1 *puVar22;
  undefined4 uVar23;
  int *local_248;
  undefined8 *******local_240;
  undefined4 local_238;
  undefined7 local_230;
  char cStack_229;
  undefined8 *******local_228;
  undefined1 *local_220;
  undefined8 local_218;
  int *local_198;
  int *local_190;
  undefined8 local_188;
  undefined8 local_180;
  undefined8 local_178;
  undefined8 local_170;
  undefined8 local_168;
  undefined8 *******local_128;
  ulong local_120;
  undefined8 local_118;
  undefined8 *******local_d8;
  undefined8 *local_d0;
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
  undefined8 local_78;
  undefined8 uStack_70;
  undefined8 local_68;
  undefined8 uStack_60;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  if (param_3 != 0) {
    iVar9 = thunk_FUN_05e1d97c(4);
    if (iVar9 != 0) {
      FUN_0488143c(&local_240);
      pppppppuVar16 = local_240;
      if (-1 < cStack_229) {
        pppppppuVar16 = &local_240;
      }
      if ((DAT_0a27eb8d & 1) == 0) {
        _DAT_0a27eb70 = CONCAT44((int)DAT_084d83b8,(int)DAT_084a2f08);
        uRam000000000a27eb78 = CONCAT44((int)DAT_084c77d8,(int)DAT_0849b8b0);
        DAT_0a27eb80 = CONCAT44((int)ram0x084897a0,(int)DAT_084a8158);
        DAT_0a27eb88 = (undefined4)DAT_084e04b8;
        DAT_0a27eb8c = 0;
        DAT_0a27eb8d = 1;
      }
      if ((DAT_0a27ebeb & 1) == 0) {
        _DAT_0a27ebd4 = CONCAT44((int)DAT_08484518,(int)DAT_084e0518);
        uRam000000000a27ebdc = CONCAT44((int)DAT_084d71b0,(int)DAT_084e0520);
        DAT_0a27ebe4 = (undefined4)DAT_084d71b8;
        DAT_0a27ebe8 = 0x656b;
        DAT_0a27ebea = 0;
        DAT_0a27ebeb = 1;
      }
      FUN_05e1d050(&local_228,4,pppppppuVar16,&DAT_0a27eb70,&DAT_0a27ebd4,0x2f,0,0);
      IVar10 = _objc_msgSend(param_3,PTR_s_domain_09ff7540);
      IVar10 = _objc_retainAutorelease(IVar10);
      local_128 = (undefined8 *******)_objc_msgSend(IVar10,PTR_s_UTF8String_09ff5378);
      local_120 = local_120 & 0xffffffffffffff00;
      IVar10 = _objc_msgSend(param_3,PTR_s_code_09ff5680);
      local_178 = (char *)0x0;
      if ((DAT_0a27ec52 & 1) == 0) {
        uVar20 = 0;
        do {
          uVar23 = *(undefined4 *)((long)&DAT_084e0769 + uVar20);
          uVar5 = CONCAT12((char)((uint)uVar23 >> 8),(short)uVar23) & 0xff00ff;
          uVar4 = *(undefined4 *)((long)&DAT_084e0755 + uVar20 % 0x14);
          *(uint *)((long)&DAT_0a27ec0a + uVar20) =
               CONCAT13((char)((uint)uVar23 >> 0x18) + 0x8aU ^ (byte)((uint)uVar4 >> 0x18),
                        CONCAT12((char)((uint)uVar23 >> 0x10) + 0x8aU ^ (byte)((uint)uVar4 >> 0x10),
                                 CONCAT11((char)(uVar5 >> 0x10) + 0x8aU ^ (byte)((uint)uVar4 >> 8),
                                          (char)uVar5 + 0x8aU ^ (byte)uVar4)));
          uVar20 = uVar20 + 4;
        } while (uVar20 != 0x48);
        DAT_0a27ec52 = 1;
      }
      lVar19 = 8;
      IVar21 = IVar10;
      do {
        lVar18 = lVar19;
        *(undefined1 *)((long)&local_178 + lVar18) = *(undefined1 *)((long)IVar21 % 10 + 0xa27ec2d);
        lVar19 = lVar18 + 1;
        uVar20 = IVar21 + 9;
        IVar21 = (long)IVar21 / 10;
      } while (0x12 < uVar20);
      if ((long)IVar10 < 0) {
        *(undefined1 *)((long)&local_178 + lVar18 + 1) = 0x2d;
        lVar19 = lVar18 + 2;
      }
      *(undefined1 *)((long)&local_178 + lVar19) = 0;
      if (9 < lVar19) {
        puVar22 = (undefined1 *)((long)&local_180 + lVar19 + 7);
        puVar17 = (undefined1 *)((long)&local_170 + 1);
        do {
          uVar3 = *puVar22;
          *puVar22 = puVar17[-1];
          puVar17[-1] = uVar3;
          bVar8 = puVar17 < puVar22 + -1;
          puVar22 = puVar22 + -1;
          puVar17 = puVar17 + 1;
        } while (bVar8);
      }
      if ((DAT_0a27ec09 & 1) == 0) {
        _DAT_0a27ebec = CONCAT44((int)DAT_084c9850,(int)DAT_08481210);
        uRam000000000a27ebf4 = CONCAT44((int)DAT_0848baf8,(int)DAT_084c77d8);
        DAT_0a27ebfc = CONCAT44((int)DAT_084e0528,(int)DAT_084808a8);
        DAT_0a27ec04 = (undefined4)DAT_084d8ac0;
        DAT_0a27ec08 = 0;
        DAT_0a27ec09 = 1;
      }
      local_d8 = &local_128;
      local_d0 = &local_178;
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
      uStack_70 = 0;
      local_78 = 0;
      uStack_60 = 0;
      local_68 = 0;
      local_178 = (char *)&local_170;
      FUN_05e1d31c(&local_228,&DAT_0a27ebec,&local_d8);
      thunk_FUN_05e1d0bc(&local_228);
      if (cStack_229 < '\0') {
        __ZdlPvm(local_240,CONCAT17(cStack_229,local_230) & 0x7fffffffffffffff);
      }
    }
    FUN_04ad0970(0x6e);
    local_248 = &DAT_0a232178;
    FUN_002b74bc(DAT_0a52bdd0,1,&local_248);
    piVar7 = local_248;
    if (*local_248 != -1) {
      if (*local_248 != 0) {
        LOAcquire();
        iVar9 = *local_248;
        *local_248 = iVar9 + -1;
        LORelease();
        if (iVar9 != 1) goto LAB_002b1ef0;
      }
      if (*(long *)(local_248 + 4) != 0) {
        FUN_002a34e4();
        FUN_06ec553c(piVar7,*(undefined8 *)(piVar7 + 4),8);
      }
      FUN_06ec55e4(piVar7);
    }
    goto LAB_002b1ef0;
  }
  IVar10 = _objc_retainAutorelease(param_2);
  pvVar11 = (void *)_objc_msgSend(IVar10,PTR_s_bytes_09ff55c8);
  IVar10 = _objc_msgSend(param_2,PTR_s_length_09ff5eb0);
  puVar22 = (undefined1 *)(long)(int)IVar10;
  local_220 = &SUB_aaaaaaaaaaaaaaaa;
  local_218 = &SUB_aaaaaaaaaaaaaaaa;
  local_228 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
  if ((undefined1 *)0x7ffffffffffffff7 < puVar22) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_228);
  }
  if (puVar22 < (undefined1 *)0x17) {
    local_218 = (undefined1 *)CONCAT17((char)IVar10,0xaaaaaaaaaaaaaa);
    pppppppuVar16 = &local_228;
    if ((IVar10 & 0xffffffff) != 0) goto LAB_002b1b00;
  }
  else {
    uVar20 = 0x19;
    if (((ulong)puVar22 | 7) != 0x17) {
      uVar20 = ((ulong)puVar22 | 7) + 1;
    }
    pppppppuVar16 = (undefined8 *******)__Znwm(uVar20);
    local_218 = (undefined1 *)(uVar20 | 0x8000000000000000);
    local_228 = pppppppuVar16;
    local_220 = puVar22;
LAB_002b1b00:
    _memmove(pppppppuVar16,pvVar11,(size_t)puVar22);
  }
  *(undefined1 *)((long)pppppppuVar16 + (long)puVar22) = 0;
  FUN_03c75030(&local_228);
  local_180 = &DAT_0a232178;
  local_178 = (char *)0x0;
  local_d8 = (undefined8 *******)0x0;
  local_d0 = (undefined8 *)0x0;
  local_c8 = 0;
  local_128 = (undefined8 *******)0x0;
  local_120 = 0;
  local_118 = 0;
  local_170 = 0;
  local_168 = 0;
  local_188 = 0;
  iVar9 = FUN_03c7579c(&local_178,&local_d8,&local_128,&local_188);
  if (iVar9 != 0) {
    pppppppuVar16 = local_d8;
    uVar1 = (uint)local_d0;
    if (-1 < local_c8) {
      pppppppuVar16 = &local_d8;
      uVar1 = (uint)local_c8._7_1_;
    }
    FUN_06ed0084(&local_190,pppppppuVar16,uVar1);
    FUN_06fe12c4(&local_240,&local_190);
    plVar12 = (long *)FUN_002b2110(&local_180,&DAT_0a51cd68);
    ppppppuVar15 = (undefined8 ******)*plVar12;
    lVar19 = plVar12[1];
    *plVar12 = (long)local_240;
    *(undefined4 *)(plVar12 + 1) = local_238;
    local_240 = (undefined8 *******)ppppppuVar15;
    local_238 = (int)lVar19;
    FUN_06fe0f68(&local_240);
    if (*local_190 != -1) {
      if (*local_190 != 0) {
        LOAcquire();
        iVar9 = *local_190;
        *local_190 = iVar9 + -1;
        LORelease();
        if (iVar9 != 1) goto LAB_002b1bf8;
      }
      FUN_06ea14cc(local_190,1,8);
    }
LAB_002b1bf8:
    pppppppuVar16 = local_128;
    uVar1 = (uint)local_120;
    if (-1 < (long)local_118) {
      pppppppuVar16 = &local_128;
      uVar1 = (uint)local_118._7_1_;
    }
    FUN_06ed0084(&local_190,pppppppuVar16,uVar1);
    FUN_06fe12c4(&local_240,&local_190);
    plVar12 = (long *)FUN_002b2110(&local_180,&DAT_0a51cd70);
    ppppppuVar15 = (undefined8 ******)*plVar12;
    lVar19 = plVar12[1];
    *plVar12 = (long)local_240;
    *(undefined4 *)(plVar12 + 1) = local_238;
    local_240 = (undefined8 *******)ppppppuVar15;
    local_238 = (int)lVar19;
    FUN_06fe0f68(&local_240);
    if (*local_190 != -1) {
      if (*local_190 != 0) {
        LOAcquire();
        iVar9 = *local_190;
        *local_190 = iVar9 + -1;
        LORelease();
        if (iVar9 != 1) goto LAB_002b1c98;
      }
      FUN_06ea14cc(local_190,1,8);
    }
LAB_002b1c98:
    uVar1 = (uint)local_170;
    if (-1 < (long)local_168) {
      uVar1 = (uint)local_168._7_1_;
    }
    sVar14 = (size_t)uVar1;
    pcVar2 = local_178;
    if (-1 < (long)local_168) {
      pcVar2 = (char *)&local_178;
    }
    if ((pcVar2 != (char *)0x0) && (uVar1 == 0xffffffff)) {
      sVar14 = _strlen(pcVar2);
    }
    FUN_06ef81e0(&local_190,pcVar2,sVar14);
    FUN_06fe12fc(&local_240,&local_190);
    plVar12 = (long *)FUN_002b2110(&local_180,&DAT_0a51cd78);
    ppppppuVar15 = (undefined8 ******)*plVar12;
    lVar19 = plVar12[1];
    *plVar12 = (long)local_240;
    *(undefined4 *)(plVar12 + 1) = local_238;
    local_240 = (undefined8 *******)ppppppuVar15;
    local_238 = (int)lVar19;
    FUN_06fe0f68(&local_240);
    if (*local_190 != -1) {
      if (*local_190 != 0) {
        LOAcquire();
        iVar9 = *local_190;
        *local_190 = iVar9 + -1;
        LORelease();
        if (iVar9 != 1) goto LAB_002b1d54;
      }
      FUN_06ea14cc(local_190,2,8);
    }
LAB_002b1d54:
    FUN_06fe1284(&local_240,local_188);
    plVar12 = (long *)FUN_002b2110(&local_180,&DAT_0a51cd80);
    pppppppuVar16 = (undefined8 *******)*plVar12;
    lVar19 = plVar12[1];
    *plVar12 = (long)local_240;
    *(undefined4 *)(plVar12 + 1) = local_238;
    local_240 = pppppppuVar16;
    local_238 = (int)lVar19;
    FUN_06fe0f68(&local_240);
  }
  uVar6 = DAT_0a52bdd0;
  if (*local_180 - 1U < 0xfffffffe) {
    LOAcquire();
    *local_180 = *local_180 + 1;
    LORelease();
    local_198 = local_180;
  }
  else if (*local_180 == 0) {
    local_198 = (int *)FUN_06ec55ac();
    if (*(long *)(local_180 + 4) != 0) {
      puVar13 = (ulong *)FUN_002a3378();
      *(ulong **)(local_198 + 4) = puVar13;
      *puVar13 = *puVar13 & 3 | (ulong)(local_198 + 2);
      FUN_06ec5458(local_198);
    }
  }
  else {
    local_198 = local_180;
  }
  FUN_002b74bc(uVar6,6,&local_198);
  piVar7 = local_198;
  if (*local_198 != -1) {
    if (*local_198 != 0) {
      LOAcquire();
      iVar9 = *local_198;
      *local_198 = iVar9 + -1;
      LORelease();
      if (iVar9 != 1) goto LAB_002b1e74;
    }
    if (*(long *)(local_198 + 4) != 0) {
      FUN_002a34e4();
      FUN_06ec553c(piVar7,*(undefined8 *)(piVar7 + 4),8);
    }
    FUN_06ec55e4(piVar7);
  }
LAB_002b1e74:
  if ((long)local_168 < 0) {
    __ZdlPvm(local_178,local_168 & 0x7fffffffffffffff);
  }
  if ((long)local_118 < 0) {
    __ZdlPvm(local_128,local_118 & 0x7fffffffffffffff);
  }
  piVar7 = local_180;
  if (*local_180 != -1) {
    if (*local_180 != 0) {
      LOAcquire();
      iVar9 = *local_180;
      *local_180 = iVar9 + -1;
      LORelease();
      if (iVar9 != 1) goto LAB_002b1ed8;
    }
    if (*(long *)(local_180 + 4) != 0) {
      FUN_002a34e4();
      FUN_06ec553c(piVar7,*(undefined8 *)(piVar7 + 4),8);
    }
    FUN_06ec55e4(piVar7);
  }
LAB_002b1ed8:
  if ((long)local_218 < 0) {
    __ZdlPvm(local_228,(ulong)local_218 & 0x7fffffffffffffff);
  }
LAB_002b1ef0:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_58) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail(0);
  }
  return;
}


