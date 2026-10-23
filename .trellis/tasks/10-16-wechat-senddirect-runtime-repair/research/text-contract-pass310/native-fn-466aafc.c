// Ghidra inferred pseudocode; requested=0x466aafc
// entry=0466a420 end=0466aba7

/* WARNING: Removing unreachable block (ram,0x0466a7c0) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0466a420(void)

{
  undefined8 *******pppppppuVar1;
  uint3 uVar2;
  long ******pppppplVar3;
  undefined1 *puVar4;
  int iVar5;
  uint uVar6;
  int iVar7;
  long lVar8;
  long *******ppppppplVar9;
  long *******ppppppplVar10;
  undefined1 *puVar11;
  ulong uVar12;
  undefined1 *puVar13;
  long *******ppppppplVar14;
  undefined4 uVar15;
  undefined4 uVar16;
  undefined8 *******local_290 [2];
  undefined7 local_280;
  char cStack_279;
  long *******local_278;
  long *******ppppppplStack_270;
  undefined8 local_268;
  undefined1 local_1e8;
  undefined7 uStack_1e7;
  undefined7 local_1d8;
  char cStack_1d1;
  long *******local_1d0;
  long *******ppppppplStack_1c8;
  ulong local_1c0;
  undefined4 *local_1b8;
  undefined1 local_1b0;
  long *******local_168;
  undefined1 local_160;
  long *******local_118;
  long *******local_110 [9];
  long *******local_c8;
  long *******local_c0;
  undefined8 local_b8;
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
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_1d0 = (long *******)0x0;
  ppppppplStack_1c8 = (long *******)0x0;
  local_1c0 = 0;
  iVar5 = (**(code **)(*DAT_0a45df38 + 0x70))();
  if (iVar5 == 0) {
    ppppppplVar14 = (long *******)DAT_0a45df38[0x54];
    local_110[0] = (long *******)DAT_0a45df38[0x55];
    if (local_110[0] != (long *******)0x0) {
      local_110[0][1] = (long ******)((long)local_110[0][1] + 1);
    }
    if ((DAT_0a45e0a7 & 1) == 0) {
      _DAT_0a45e080 = CONCAT44((int)DAT_084e3210,(int)DAT_085b4630);
      uRam000000000a45e088 = CONCAT44((int)DAT_08a13428,(int)ram0x084f7f78);
      _DAT_0a45e090 = CONCAT44((int)DAT_084f26d8,(int)DAT_08499958);
      uRam000000000a45e098 = CONCAT44((int)DAT_08a13430,(int)ram0x084a6be0);
      DAT_0a45e0a0 = (undefined4)DAT_08480b48;
      DAT_0a45e0a4 = 0x7972;
      DAT_0a45e0a6 = 0;
      DAT_0a45e0a7 = 1;
    }
    local_118 = ppppppplVar14;
    ppppppplVar9 = (long *******)_strlen(&DAT_0a45e080);
    if ((long *******)0x7ffffffffffffff7 < ppppppplVar9) {
                    /* WARNING: Subroutine does not return */
      FUN_00018d9c(&local_c8);
    }
    if ((long *******)((long)&MACH_HEADER.sizeofcmds + 2) < ppppppplVar9) {
      uVar12 = 0x19;
      if (((ulong)ppppppplVar9 | 7) != 0x17) {
        uVar12 = ((ulong)ppppppplVar9 | 7) + 1;
      }
      ppppppplVar10 = (long *******)__Znwm(uVar12);
      local_b8 = (undefined4 **)(uVar12 | 0x8000000000000000);
      local_c8 = ppppppplVar10;
      local_c0 = ppppppplVar9;
LAB_0466a728:
      _memcpy(ppppppplVar10,&DAT_0a45e080,(size_t)ppppppplVar9);
    }
    else {
      local_b8 = (undefined4 **)CONCAT17((char)ppppppplVar9,(undefined7)local_b8);
      ppppppplVar10 = (long *******)&local_c8;
      if (ppppppplVar9 != (long *******)0x0) goto LAB_0466a728;
    }
    *(undefined1 *)((long)ppppppplVar10 + (long)ppppppplVar9) = 0;
    cStack_1d1 = '\0';
    local_1e8 = 0;
    FUN_045321c0(&local_278,ppppppplVar14,&local_c8,&local_1e8);
    if ((long)local_1c0 < 0) {
      __ZdlPvm(local_1d0,local_1c0 & 0x7fffffffffffffff);
    }
    local_1c0 = local_268;
    local_1d0 = local_278;
    ppppppplStack_1c8 = ppppppplStack_270;
    local_268 = local_268 & 0xffffffffffffff;
    local_278 = (long *******)((ulong)local_278 & 0xffffffffffffff00);
    ppppppplVar14 = local_110[0];
    if (cStack_1d1 < '\0') {
      __ZdlPvm(CONCAT71(uStack_1e7,local_1e8),CONCAT17(cStack_1d1,local_1d8) & 0x7fffffffffffffff);
      ppppppplVar14 = local_110[0];
    }
joined_r0x0466a7a0:
    if (ppppppplVar14 != (long *******)0x0) {
      LOAcquire();
      pppppplVar3 = ppppppplVar14[1];
      ppppppplVar14[1] = (long ******)((long)pppppplVar3 + -1);
      LORelease();
      if (pppppplVar3 == (long ******)0x0) {
        (*(code *)(*ppppppplVar14)[2])(ppppppplVar14);
        __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar14);
      }
    }
  }
  else {
    (**(code **)(*DAT_0a45df38 + 0x68))(&local_278);
    ppppppplVar14 = ppppppplStack_270;
    local_c8 = local_278;
    local_c0 = ppppppplStack_270;
    if ((ppppppplStack_270 != (long *******)0x0) &&
       (ppppppplStack_270[1] = (long ******)((long)ppppppplStack_270[1] + 1),
       ppppppplStack_270 != (long *******)0x0)) {
      LOAcquire();
      pppppplVar3 = ppppppplStack_270[1];
      ppppppplStack_270[1] = (long ******)((long)pppppplVar3 + -1);
      LORelease();
      if (pppppplVar3 == (long ******)0x0) {
        (*(code *)(*ppppppplStack_270)[2])(ppppppplStack_270);
        __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar14);
      }
    }
    lVar8 = (*(code *)(*local_c8)[1])();
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (&local_1d0,lVar8 + 0xe0);
    ppppppplVar14 = local_c0;
    if (local_c0 != (long *******)0x0) {
      LOAcquire();
      pppppplVar3 = local_c0[1];
      local_c0[1] = (long ******)((long)pppppplVar3 + -1);
      LORelease();
      if (pppppplVar3 == (long ******)0x0) {
        (*(code *)(*local_c0)[2])(local_c0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppplVar14);
      }
    }
    ppppppplVar14 = ppppppplStack_1c8;
    if (-1 < (long)local_1c0) {
      ppppppplVar14 = (long *******)(local_1c0 >> 0x38);
    }
    if (ppppppplVar14 != (long *******)0x0) {
      ppppppplVar14 = (long *******)DAT_0a45df38[0x54];
      local_c0 = (long *******)DAT_0a45df38[0x55];
      if (local_c0 != (long *******)0x0) {
        local_c0[1] = (long ******)((long)local_c0[1] + 1);
      }
      if ((DAT_0a45e0a7 & 1) == 0) {
        _DAT_0a45e080 = CONCAT44((int)DAT_084e3210,(int)DAT_085b4630);
        uRam000000000a45e088 = CONCAT44((int)DAT_08a13428,(int)ram0x084f7f78);
        _DAT_0a45e090 = CONCAT44((int)DAT_084f26d8,(int)DAT_08499958);
        uRam000000000a45e098 = CONCAT44((int)DAT_08a13430,(int)ram0x084a6be0);
        DAT_0a45e0a0 = (undefined4)DAT_08480b48;
        DAT_0a45e0a4 = 0x7972;
        DAT_0a45e0a6 = 0;
        DAT_0a45e0a7 = 1;
      }
      local_c8 = ppppppplVar14;
      ppppppplVar9 = (long *******)_strlen(&DAT_0a45e080);
      if ((long *******)0x7ffffffffffffff7 < ppppppplVar9) {
                    /* WARNING: Subroutine does not return */
        FUN_00018d9c(&local_278);
      }
      if ((long *******)((long)&MACH_HEADER.sizeofcmds + 2) < ppppppplVar9) {
        uVar12 = 0x19;
        if (((ulong)ppppppplVar9 | 7) != 0x17) {
          uVar12 = ((ulong)ppppppplVar9 | 7) + 1;
        }
        ppppppplVar10 = (long *******)__Znwm(uVar12);
        local_268 = uVar12 | 0x8000000000000000;
        local_278 = ppppppplVar10;
        ppppppplStack_270 = ppppppplVar9;
LAB_0466a7fc:
        _memcpy(ppppppplVar10,&DAT_0a45e080,(size_t)ppppppplVar9);
      }
      else {
        local_268 = CONCAT17((char)ppppppplVar9,(undefined7)local_268);
        ppppppplVar10 = (long *******)&local_278;
        if (ppppppplVar9 != (long *******)0x0) goto LAB_0466a7fc;
      }
      *(undefined1 *)((long)ppppppplVar10 + (long)ppppppplVar9) = 0;
      FUN_04532894(ppppppplVar14,&local_278,&local_1d0);
      ppppppplVar14 = local_c0;
      if ((long)local_268 < 0) {
        __ZdlPvm(local_278,local_268 & 0x7fffffffffffffff);
        ppppppplVar14 = local_c0;
      }
      goto joined_r0x0466a7a0;
    }
  }
  ppppppplVar14 = ppppppplStack_1c8;
  if (-1 < (long)local_1c0) {
    ppppppplVar14 = (long *******)(local_1c0 >> 0x38);
  }
  if (ppppppplVar14 == (long *******)0x0) {
    uVar6 = 0;
  }
  else {
    uVar6 = FUN_04724330(&local_1d0);
    uVar6 = uVar6 ^ 1;
  }
  FUN_04de809c(uVar6);
  iVar7 = thunk_FUN_05e1d97c(2);
  if (iVar7 == 0) goto joined_r0x0466ab30;
  FUN_0488143c(local_290);
  pppppppuVar1 = local_290[0];
  if (-1 < cStack_279) {
    pppppppuVar1 = local_290;
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
  if ((DAT_0a45e0c3 & 1) == 0) {
    uRam000000000a45e0b8._0_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x18];
    uRam000000000a45e0b8._1_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x19];
    uRam000000000a45e0b8._2_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x1a];
    uRam000000000a45e0b8._3_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x1b];
    uRam000000000a45e0b8._4_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x1c];
    uRam000000000a45e0b8._5_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x1d];
    uRam000000000a45e0b8._6_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x1e];
    uRam000000000a45e0b8._7_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x1f];
    DAT_0a45e0b0 = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x10];
    DAT_0a45e0b0_1._0_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x11];
    DAT_0a45e0b0_1._1_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x12];
    DAT_0a45e0b0_1._2_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x13];
    DAT_0a45e0b0_1._3_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x14];
    DAT_0a45e0b0_1._4_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x15];
    DAT_0a45e0b0_1._5_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x16];
    DAT_0a45e0b0_1._6_1_ = s_3_coroutine_uninSetWordingsProdu_08a135a0[0x17];
    DAT_0a45e0c0 = 0x7463;
    DAT_0a45e0c2 = 0;
    DAT_0a45e0c3 = 1;
  }
  FUN_05e1d050(&local_278,2,pppppppuVar1,&DAT_0a45df80,&DAT_0a45e0b0,0x130,0,0);
  if ((DAT_0a45e7e9 & 1) == 0) {
    DAT_0a45e7e6 = 0x6425;
    DAT_0a45e7e8 = 0;
    DAT_0a45e7e9 = 1;
  }
  _snprintf((char *)local_110,0x41,(char *)&DAT_0a45e7e6);
  local_168 = local_1d0;
  if (-1 < (long)local_1c0) {
    local_168 = (long *******)&local_1d0;
  }
  local_160 = 0;
  if (iVar5 == 0) {
    local_1b8 = &DAT_0a45e664;
    if ((DAT_0a45e66a & 1) == 0) {
      DAT_0a45e664 = (undefined4)DAT_0847fe48;
      puVar4 = &DAT_0a45e668;
      puVar11 = &DAT_0a45e669;
      puVar13 = &DAT_0a45e66a;
      goto LAB_0466aa28;
    }
  }
  else {
    local_1b8 = (undefined4 *)&DAT_0a45e65b;
    if ((DAT_0a45e660 & 1) == 0) {
      DAT_0a45e65b = 0x7274;
      DAT_0a45e65d = 0x75;
      puVar11 = &DAT_0a45e65f;
      puVar4 = &DAT_0a45e65e;
      puVar13 = &DAT_0a45e660;
LAB_0466aa28:
      *puVar4 = 0x65;
      *puVar11 = 0;
      *puVar13 = 1;
    }
  }
  local_1b0 = 0;
  if ((DAT_0a45e0ff & 1) == 0) {
    uVar12 = 0;
    do {
      uVar15 = *(undefined4 *)((long)&DAT_08a1408f + uVar12);
      uVar2 = CONCAT12((char)((uint)uVar15 >> 8),(short)uVar15) & 0xff00ff;
      uVar16 = *(undefined4 *)((long)&DAT_08a1407b + uVar12 % 0x14);
      *(uint *)((long)&DAT_0a45e0c4 + uVar12) =
           CONCAT13((char)((uint)uVar15 >> 0x18) + 0x8aU ^ (byte)((uint)uVar16 >> 0x18),
                    CONCAT12((char)((uint)uVar15 >> 0x10) + 0x8aU ^ (byte)((uint)uVar16 >> 0x10),
                             CONCAT11((char)(uVar2 >> 0x10) + 0x8aU ^ (byte)((uint)uVar16 >> 8),
                                      (char)uVar2 + 0x8aU ^ (byte)uVar16)));
      uVar12 = uVar12 + 4;
    } while (uVar12 != 0x38);
    DAT_0a45e0fc = 0x5f25;
    DAT_0a45e0fe = 0;
    DAT_0a45e0ff = 1;
  }
  local_c8 = (long *******)&local_118;
  local_c0 = (long *******)&local_168;
  local_b8 = &local_1b8;
  uStack_a8 = 0;
  local_b0 = 0;
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
  local_50 = 0;
  local_118 = (long *******)local_110;
  FUN_05e1d31c(&local_278,&DAT_0a45e0c4,&local_c8);
  thunk_FUN_05e1d0bc(&local_278);
  if (cStack_279 < '\0') {
    __ZdlPvm(local_290[0],CONCAT17(cStack_279,local_280) & 0x7fffffffffffffff);
  }
joined_r0x0466ab30:
  if ((long)local_1c0 < 0) {
    __ZdlPvm(local_1d0,local_1c0 & 0x7fffffffffffffff);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


