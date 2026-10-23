// Ghidra inferred pseudocode; requested=0x3181628
// entry=03181628 end=03181fb3

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_03181628(undefined8 param_1,undefined8 param_2,undefined8 *param_3,long *******param_4)

{
  long *******ppppppplVar1;
  undefined1 uVar2;
  uint3 uVar3;
  long ******pppppplVar4;
  long *******ppppppplVar5;
  bool bVar6;
  long ****pppplVar7;
  int iVar8;
  long lVar9;
  undefined8 *puVar10;
  ulong uVar11;
  long lVar12;
  undefined1 *puVar13;
  undefined1 *puVar14;
  long ******pppppplVar15;
  long *****ppppplVar16;
  undefined4 uVar17;
  undefined4 uVar18;
  long *******local_238 [2];
  undefined7 local_228;
  char cStack_221;
  long ******local_220;
  long ******pppppplStack_218;
  long ******local_210;
  long ******local_208;
  long ******local_200;
  long local_1f8;
  long *******local_188;
  undefined8 local_180;
  ulong local_178;
  long *******local_138;
  undefined1 local_130;
  long *******local_e8;
  long *******local_e0;
  undefined8 uStack_d8;
  undefined8 local_d0;
  undefined8 uStack_c8;
  undefined8 local_c0;
  undefined8 uStack_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 local_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 local_80;
  undefined8 uStack_78;
  undefined8 local_70;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar9 = FUN_03221ac0(param_2,param_4);
  iVar8 = thunk_FUN_05e1d97c(2);
  if (iVar8 == 0) {
LAB_03181888:
    if (lVar9 != 0) goto LAB_0318188c;
LAB_03181be0:
    local_188 = (long *******)0x0;
    local_180 = (long *******)0x0;
    local_178 = 0;
    local_180 = (long *******)FUN_0320cce0(&local_188,param_3);
    if (*(char *)((long)param_4 + 0x17) < '\0') {
      FUN_00018d20(&local_220,*param_4,param_4[1]);
      local_200 = (long ******)local_180;
    }
    else {
      pppppplStack_218 = param_4[1];
      local_220 = *param_4;
      local_210 = param_4[2];
      local_200 = (long ******)local_180;
    }
    local_208 = (long ******)local_188;
    local_1f8 = local_178;
    local_180 = (long *******)0x0;
    local_178 = 0;
    local_188 = (long *******)0x0;
    FUN_03221c50(param_2,&local_220,&local_220);
    pppppplVar4 = local_208;
    pppppplVar15 = local_200;
    if (local_208 != (long ******)0x0) {
      for (; pppppplVar15 != pppppplVar4; pppppplVar15 = pppppplVar15 + -2) {
        ppppplVar16 = pppppplVar15[-1];
        if (ppppplVar16 != (long *****)0x0) {
          LOAcquire();
          pppplVar7 = ppppplVar16[1];
          ppppplVar16[1] = (long ****)((long)pppplVar7 + -1);
          LORelease();
          if (pppplVar7 == (long ****)0x0) {
            (*(code *)(*ppppplVar16)[2])(ppppplVar16);
            __ZNSt3__119__shared_weak_count14__release_weakEv(ppppplVar16);
          }
        }
      }
      local_200 = pppppplVar4;
      __ZdlPvm(local_208,local_1f8 - (long)local_208);
    }
    if ((long)local_210 < 0) {
      __ZdlPvm(local_220,(ulong)local_210 & 0x7fffffffffffffff);
    }
    iVar8 = thunk_FUN_05e1d97c(2);
    if (iVar8 != 0) {
      FUN_0488143c(local_238);
      ppppppplVar1 = local_238[0];
      if (-1 < cStack_221) {
        ppppppplVar1 = (long *******)local_238;
      }
      if ((DAT_0a3dd363 & 1) == 0) {
        uVar11 = 0;
        do {
          (&DAT_0a3dd350)[uVar11] = (&DAT_088bce97)[uVar11] + 0x8a ^ (&DAT_088bce87)[uVar11 & 0xf];
          uVar11 = uVar11 + 1;
        } while (uVar11 != 0x13);
        DAT_0a3dd363 = 1;
      }
      if ((DAT_0a3e01ea & 1) == 0) {
        _DAT_0a3e01d4 = CONCAT44((int)DAT_0848f630,(int)DAT_0855bb40);
        uRam000000000a3e01dc = CONCAT44((int)DAT_084fb690,(int)DAT_0856e3f8);
        DAT_0a3e01e4 = (undefined4)DAT_08492618;
        DAT_0a3e01e8 = 0x74;
        DAT_0a3e01ea = 1;
      }
      FUN_05e1d050(&local_220,2,ppppppplVar1,&DAT_0a3dd350,&DAT_0a3e01d4,0xfcb,0,0);
      local_138 = (long *******)*param_4;
      if (-1 < *(char *)((long)param_4 + 0x17)) {
        local_138 = param_4;
      }
      local_130 = 0;
      if ((DAT_0a3e027f & 1) == 0) {
        _DAT_0a3e0248 = CONCAT44((int)DAT_084a66b0,(int)DAT_088ba9c0);
        uRam000000000a3e0250 = CONCAT44((int)DAT_086b7540,(int)DAT_086b5ec0);
        _DAT_0a3e0258 = CONCAT44((int)DAT_084a2f50,(int)DAT_08567f28);
        uRam000000000a3e0260 = CONCAT44((int)DAT_084d8570,(int)DAT_08592a10);
        _DAT_0a3e0268 = CONCAT44((int)DAT_08500d08,(int)DAT_088ba9d0);
        uRam000000000a3e0270 = CONCAT44((int)DAT_088ba9c8,(int)DAT_088ba9d8);
        DAT_0a3e0278 = (undefined4)DAT_084808d8;
        DAT_0a3e027c = 0x313a;
        DAT_0a3e027e = 0;
        DAT_0a3e027f = 1;
      }
      uStack_d8 = 0;
      local_e0 = (long *******)0x0;
      local_e8 = (long *******)&local_138;
      uStack_c8 = 0;
      local_d0 = 0;
      uStack_b8 = 0;
      local_c0 = 0;
      uStack_a8 = 0;
      local_b0 = 0;
      uStack_98 = 0;
      local_a0 = 0;
      uStack_88 = 0;
      local_90 = 0;
      uStack_78 = 0;
      local_80 = 0;
      local_70 = 0;
      FUN_05e1d31c(&local_220,&DAT_0a3e0248,&local_e8);
      thunk_FUN_05e1d0bc(&local_220);
      if (cStack_221 < '\0') {
        __ZdlPvm(local_238[0],CONCAT17(cStack_221,local_228) & 0x7fffffffffffffff);
      }
    }
    ppppppplVar5 = local_188;
    local_238[0] = local_188;
    ppppppplVar1 = local_180;
    if (local_188 == (long *******)0x0) goto LAB_03181f78;
    for (; local_188 = local_238[0], ppppppplVar1 != ppppppplVar5; ppppppplVar1 = ppppppplVar1 + -2)
    {
      pppppplVar15 = ppppppplVar1[-1];
      if (pppppplVar15 != (long ******)0x0) {
        LOAcquire();
        ppppplVar16 = pppppplVar15[1];
        pppppplVar15[1] = (long *****)((long)ppppplVar16 + -1);
        LORelease();
        if (ppppplVar16 == (long *****)0x0) {
          (*(code *)(*pppppplVar15)[2])(pppppplVar15);
          __ZNSt3__119__shared_weak_count14__release_weakEv(pppppplVar15);
        }
      }
      local_238[0] = local_188;
    }
    local_180 = ppppppplVar5;
    uVar11 = local_178 - (long)local_238[0];
  }
  else {
    FUN_0488143c(&local_188);
    ppppppplVar1 = local_188;
    if (-1 < (long)local_178) {
      ppppppplVar1 = (long *******)&local_188;
    }
    if ((DAT_0a3dd363 & 1) == 0) {
      uVar11 = 0;
      do {
        (&DAT_0a3dd350)[uVar11] = (&DAT_088bce97)[uVar11] + 0x8a ^ (&DAT_088bce87)[uVar11 & 0xf];
        uVar11 = uVar11 + 1;
      } while (uVar11 != 0x13);
      DAT_0a3dd363 = 1;
    }
    if ((DAT_0a3e01ea & 1) == 0) {
      _DAT_0a3e01d4 = CONCAT44((int)DAT_0848f630,(int)DAT_0855bb40);
      uRam000000000a3e01dc = CONCAT44((int)DAT_084fb690,(int)DAT_0856e3f8);
      DAT_0a3e01e4 = (undefined4)DAT_08492618;
      DAT_0a3e01e8 = 0x74;
      DAT_0a3e01ea = 1;
    }
    FUN_05e1d050(&local_220,2,ppppppplVar1,&DAT_0a3dd350,&DAT_0a3e01d4,0xfc3,0,0);
    FUN_030f1f08(local_238,*param_3);
    local_138 = local_238[0];
    if (-1 < cStack_221) {
      local_138 = (long *******)local_238;
    }
    local_130 = 0;
    if ((DAT_0a3e020b & 1) == 0) {
      _DAT_0a3e01ec = CONCAT44((int)DAT_084a66b0,(int)DAT_088ba9c0);
      uRam000000000a3e01f4 = CONCAT44((int)DAT_08482350,(int)DAT_086b5ec0);
      DAT_0a3e01fc = CONCAT44((int)DAT_08562ab8,(int)ram0x08487528);
      DAT_0a3e0204 = (undefined4)DAT_088ba9c8;
      DAT_0a3e0208 = 0x5f25;
      DAT_0a3e020a = 0;
      DAT_0a3e020b = 1;
    }
    uStack_d8 = 0;
    local_e0 = (long *******)0x0;
    local_e8 = (long *******)&local_138;
    uStack_c8 = 0;
    local_d0 = 0;
    uStack_b8 = 0;
    local_c0 = 0;
    uStack_a8 = 0;
    local_b0 = 0;
    uStack_98 = 0;
    local_a0 = 0;
    uStack_88 = 0;
    local_90 = 0;
    uStack_78 = 0;
    local_80 = 0;
    local_70 = 0;
    FUN_05e1d31c(&local_220,&DAT_0a3e01ec,&local_e8);
    if (cStack_221 < '\0') {
      __ZdlPvm(local_238[0],CONCAT17(cStack_221,local_228) & 0x7fffffffffffffff);
    }
    thunk_FUN_05e1d0bc(&local_220);
    if (-1 < (long)local_178) goto LAB_03181888;
    __ZdlPvm(local_188,local_178 & 0x7fffffffffffffff);
    if (lVar9 == 0) goto LAB_03181be0;
LAB_0318188c:
    puVar10 = *(undefined8 **)(lVar9 + 0x30);
    if (puVar10 < *(undefined8 **)(lVar9 + 0x38)) {
      *puVar10 = *param_3;
      lVar12 = param_3[1];
      puVar10[1] = lVar12;
      if (lVar12 != 0) {
        *(long *)(lVar12 + 8) = *(long *)(lVar12 + 8) + 1;
      }
      puVar10 = puVar10 + 2;
    }
    else {
      puVar10 = (undefined8 *)FUN_0320cce0(lVar9 + 0x28,param_3);
    }
    *(undefined8 **)(lVar9 + 0x30) = puVar10;
    iVar8 = thunk_FUN_05e1d97c(2);
    if (iVar8 == 0) goto LAB_03181f78;
    FUN_0488143c(local_238);
    ppppppplVar1 = local_238[0];
    if (-1 < cStack_221) {
      ppppppplVar1 = (long *******)local_238;
    }
    if ((DAT_0a3dd363 & 1) == 0) {
      uVar11 = 0;
      do {
        (&DAT_0a3dd350)[uVar11] = (&DAT_088bce97)[uVar11] + 0x8a ^ (&DAT_088bce87)[uVar11 & 0xf];
        uVar11 = uVar11 + 1;
      } while (uVar11 != 0x13);
      DAT_0a3dd363 = 1;
    }
    if ((DAT_0a3e01ea & 1) == 0) {
      _DAT_0a3e01d4 = CONCAT44((int)DAT_0848f630,(int)DAT_0855bb40);
      uRam000000000a3e01dc = CONCAT44((int)DAT_084fb690,(int)DAT_0856e3f8);
      DAT_0a3e01e4 = (undefined4)DAT_08492618;
      DAT_0a3e01e8 = 0x74;
      DAT_0a3e01ea = 1;
    }
    FUN_05e1d050(&local_220,2,ppppppplVar1,&DAT_0a3dd350,&DAT_0a3e01d4,0xfc6,0,0);
    local_138 = (long *******)*param_4;
    if (-1 < *(char *)((long)param_4 + 0x17)) {
      local_138 = param_4;
    }
    local_130 = 0;
    lVar12 = *(long *)(lVar9 + 0x28);
    lVar9 = *(long *)(lVar9 + 0x30);
    local_188 = (long *******)&local_180;
    if ((DAT_0a3e2eba & 1) == 0) {
      uVar11 = 0;
      do {
        uVar17 = *(undefined4 *)((long)&DAT_088c56c9 + uVar11);
        uVar3 = CONCAT12((char)((uint)uVar17 >> 8),(short)uVar17) & 0xff00ff;
        uVar18 = *(undefined4 *)((long)&DAT_088c56b5 + uVar11 % 0x14);
        *(uint *)((long)&DAT_0a3e2e72 + uVar11) =
             CONCAT13((char)((uint)uVar17 >> 0x18) + 0x69U ^ (byte)((uint)uVar18 >> 0x18),
                      CONCAT12((char)((uint)uVar17 >> 0x10) + 0x69U ^ (byte)((uint)uVar18 >> 0x10),
                               CONCAT11((char)(uVar3 >> 0x10) + 0x69U ^ (byte)((uint)uVar18 >> 8),
                                        (char)uVar3 + 0x69U ^ (byte)uVar18)));
        uVar11 = uVar11 + 4;
      } while (uVar11 != 0x48);
      DAT_0a3e2eba = 1;
    }
    uVar11 = lVar9 - lVar12 >> 4;
    lVar9 = 0;
    do {
      lVar12 = lVar9;
      *(undefined1 *)((long)&local_180 + lVar12) = (&DAT_0a3e2e95)[uVar11 % 10];
      bVar6 = 9 < uVar11;
      uVar11 = uVar11 / 10;
      lVar9 = lVar12 + 1;
    } while (bVar6);
    *(undefined1 *)((long)&local_180 + lVar12 + 1) = 0;
    if (8 < lVar12 + 8U) {
      puVar13 = (undefined1 *)((long)&local_180 + lVar12);
      puVar14 = (undefined1 *)((long)&local_180 + 1);
      do {
        uVar2 = *puVar13;
        *puVar13 = puVar14[-1];
        puVar14[-1] = uVar2;
        bVar6 = puVar14 < puVar13 + -1;
        puVar13 = puVar13 + -1;
        puVar14 = puVar14 + 1;
      } while (bVar6);
    }
    if ((DAT_0a3e0244 & 1) == 0) {
      uVar11 = 0;
      do {
        uVar17 = *(undefined4 *)((long)&DAT_088c1516 + uVar11);
        uVar3 = CONCAT12((char)((uint)uVar17 >> 8),(short)uVar17) & 0xff00ff;
        uVar18 = *(undefined4 *)((long)&DAT_088c1502 + uVar11 % 0x14);
        *(uint *)((long)&DAT_0a3e020c + uVar11) =
             CONCAT13((char)((uint)uVar17 >> 0x18) + 0x69U ^ (byte)((uint)uVar18 >> 0x18),
                      CONCAT12((char)((uint)uVar17 >> 0x10) + 0x69U ^ (byte)((uint)uVar18 >> 0x10),
                               CONCAT11((char)(uVar3 >> 0x10) + 0x69U ^ (byte)((uint)uVar18 >> 8),
                                        (char)uVar3 + 0x69U ^ (byte)uVar18)));
        uVar11 = uVar11 + 4;
      } while (uVar11 != 0x38);
      DAT_0a3e0244 = 1;
    }
    local_e8 = (long *******)&local_138;
    local_e0 = (long *******)&local_188;
    local_d0 = 0;
    uStack_d8 = 0;
    local_c0 = 0;
    uStack_c8 = 0;
    local_b0 = 0;
    uStack_b8 = 0;
    local_a0 = 0;
    uStack_a8 = 0;
    local_90 = 0;
    uStack_98 = 0;
    local_80 = 0;
    uStack_88 = 0;
    local_70 = 0;
    uStack_78 = 0;
    FUN_05e1d31c(&local_220,&DAT_0a3e020c,&local_e8);
    thunk_FUN_05e1d0bc(&local_220);
    if (-1 < cStack_221) goto LAB_03181f78;
    uVar11 = CONCAT17(cStack_221,local_228) & 0x7fffffffffffffff;
  }
  __ZdlPvm(local_238[0],uVar11);
LAB_03181f78:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_68) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


