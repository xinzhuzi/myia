// Ghidra inferred pseudocode; requested=0x32f26b8
// entry=032f26b8 end=032f314b

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_032f26b8(undefined8 *param_1,undefined8 param_2,long *******param_3,ulong param_4,
                 ulong param_5)

{
  long ******pppppplVar1;
  undefined8 *******pppppppuVar2;
  undefined1 uVar3;
  uint3 uVar4;
  long *******ppppppplVar5;
  bool bVar6;
  long lVar7;
  undefined8 ******ppppppuVar8;
  undefined8 *****pppppuVar9;
  int iVar10;
  undefined8 uVar11;
  undefined8 *******pppppppuVar12;
  undefined1 *puVar13;
  ulong uVar14;
  long lVar15;
  undefined1 *puVar16;
  uint uVar17;
  undefined4 uVar18;
  undefined4 uVar19;
  long ******local_2a0;
  long ******pppppplStack_298;
  long ******local_290;
  int local_288;
  undefined8 ******local_280;
  undefined8 ******local_278;
  undefined8 *******local_270 [2];
  undefined7 local_260;
  char cStack_259;
  undefined8 local_258;
  long *local_250;
  undefined8 ******local_1c8;
  undefined8 local_1c0;
  undefined8 *******local_178;
  undefined8 local_170;
  undefined7 local_168;
  char cStack_161;
  long *******local_128;
  undefined8 local_120;
  long *******local_d8;
  undefined8 *******local_d0;
  undefined8 ******ppppppuStack_c8;
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
  undefined8 uStack_68;
  undefined8 local_60;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  pppppplVar1 = param_3[1];
  if (-1 < (char)*(byte *)((long)param_3 + 0x17)) {
    pppppplVar1 = (long ******)(ulong)*(byte *)((long)param_3 + 0x17);
  }
  if ((((int)param_5 == 0) || ((int)param_4 == 0)) || (pppppplVar1 == (long ******)0x0)) {
    iVar10 = thunk_FUN_05e1d97c(4);
    if (iVar10 != 0) {
      FUN_0488143c(local_270);
      pppppppuVar2 = local_270[0];
      if (-1 < cStack_259) {
        pppppppuVar2 = local_270;
      }
      if ((DAT_0a3e7408 & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3e73f0)[uVar14] = (&DAT_088d08e0)[uVar14] + 0x8a ^ (&DAT_088d08d0)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x18);
        DAT_0a3e7408 = 1;
      }
      if ((DAT_0a3e8449 & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3e8431)[uVar14] = (&DAT_088d2618)[uVar14] + 0x8a ^ (&DAT_088d2608)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x18);
        DAT_0a3e8449 = 1;
      }
      FUN_05e1d050(&local_258,4,pppppppuVar2,&DAT_0a3e73f0,&DAT_0a3e8431,0x718,0,0);
      local_128 = (long *******)*param_3;
      if (-1 < *(char *)((long)param_3 + 0x17)) {
        local_128 = param_3;
      }
      local_120 = (undefined8 *******)((ulong)local_120 & 0xffffffffffffff00);
      local_178 = (undefined8 *******)0x0;
      if ((DAT_0a3ea7a2 & 1) == 0) {
        uVar14 = 0;
        do {
          uVar18 = *(undefined4 *)((long)&DAT_088d5f33 + uVar14);
          uVar4 = CONCAT12((char)((uint)uVar18 >> 8),(short)uVar18) & 0xff00ff;
          uVar19 = *(undefined4 *)((long)&DAT_088d5f1f + uVar14 % 0x14);
          *(uint *)((long)&DAT_0a3ea75a + uVar14) =
               CONCAT13((char)((uint)uVar18 >> 0x18) + 0x69U ^ (byte)((uint)uVar19 >> 0x18),
                        CONCAT12((char)((uint)uVar18 >> 0x10) + 0x69U ^ (byte)((uint)uVar19 >> 0x10)
                                 ,CONCAT11((char)(uVar4 >> 0x10) + 0x69U ^ (byte)((uint)uVar19 >> 8)
                                           ,(char)uVar4 + 0x69U ^ (byte)uVar19)));
          uVar14 = uVar14 + 4;
        } while (uVar14 != 0x48);
        DAT_0a3ea7a2 = 1;
      }
      lVar7 = 0;
      do {
        lVar15 = lVar7;
        uVar17 = (uint)param_5;
        *(undefined1 *)((long)&local_170 + lVar15) =
             *(undefined1 *)
              ((long)&DAT_0a3ea75a +
              (ulong)(uVar17 + (int)((param_5 & 0xffffffff) / 10) * -10 + 0x23));
        lVar7 = lVar15 + 1;
        param_5 = (param_5 & 0xffffffff) / 10;
      } while (9 < uVar17);
      *(undefined1 *)((long)&local_170 + lVar15 + 1) = 0;
      if (8 < lVar15 + 8U) {
        puVar13 = (undefined1 *)((long)&local_170 + lVar15);
        puVar16 = (undefined1 *)((long)&local_170 + 1);
        do {
          uVar3 = *puVar13;
          *puVar13 = puVar16[-1];
          puVar16[-1] = uVar3;
          bVar6 = puVar16 < puVar13 + -1;
          puVar13 = puVar13 + -1;
          puVar16 = puVar16 + 1;
        } while (bVar6);
      }
      local_178 = (undefined8 *******)&local_170;
      local_1c8 = (undefined8 ******)&local_1c0;
      lVar7 = 0;
      do {
        lVar15 = lVar7;
        uVar17 = (uint)param_4;
        *(undefined1 *)((long)&local_1c0 + lVar15) =
             *(undefined1 *)
              ((long)&DAT_0a3ea75a +
              (ulong)(uVar17 + (int)((param_4 & 0xffffffff) / 10) * -10 + 0x23));
        lVar7 = lVar15 + 1;
        param_4 = (param_4 & 0xffffffff) / 10;
      } while (9 < uVar17);
      *(undefined1 *)((long)&local_1c0 + lVar15 + 1) = 0;
      if (8 < lVar15 + 8U) {
        puVar13 = (undefined1 *)((long)&local_1c0 + lVar15);
        puVar16 = (undefined1 *)((long)&local_1c0 + 1);
        do {
          uVar3 = *puVar13;
          *puVar13 = puVar16[-1];
          puVar16[-1] = uVar3;
          bVar6 = puVar16 < puVar13 + -1;
          puVar13 = puVar13 + -1;
          puVar16 = puVar16 + 1;
        } while (bVar6);
      }
      if ((DAT_0a3e82f0 & 1) == 0) {
        _DAT_0a3e82c8 = CONCAT44((int)ram0x088cf4b8,(int)ram0x0856e310);
        uRam000000000a3e82d0 = CONCAT44((int)DAT_085d9870,(int)DAT_084a8110);
        _DAT_0a3e82d8 = CONCAT44((int)ram0x08483f60,(int)DAT_084d6688);
        uRam000000000a3e82e0 = CONCAT44((int)DAT_088cf4c0,(int)DAT_084d7798);
        DAT_0a3e82e8 = CONCAT44((int)DAT_0860d720,(int)DAT_08504b70);
        DAT_0a3e82f0 = 1;
      }
      local_d8 = (long *******)&local_128;
      local_d0 = &local_178;
      ppppppuStack_c8 = &local_1c8;
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
      uStack_68 = 0;
      local_70 = 0;
      local_60 = 0;
      FUN_05e1d31c(&local_258,&DAT_0a3e82c8,&local_d8);
      thunk_FUN_05e1d0bc(&local_258);
      if (cStack_259 < '\0') {
        __ZdlPvm(local_270[0],CONCAT17(cStack_259,local_260) & 0x7fffffffffffffff);
      }
    }
    FUN_0335fcb0(param_1);
    goto LAB_032f30f0;
  }
  local_1c8 = (undefined8 ******)&SUB_aaaaaaaaaaaaaaaa;
  local_1c0 = (undefined8 ******)&SUB_aaaaaaaaaaaaaaaa;
  FUN_0466aca8(&local_128);
  FUN_01205740(&local_d8,local_128);
  FUN_02603584(&local_258,local_d8);
  uVar11 = FUN_03289264(param_3);
  FUN_03bda648(&local_1c8,local_258,uVar11,param_5);
  if (local_250 != (long *)0x0) {
    LOAcquire();
    lVar7 = local_250[1];
    local_250[1] = lVar7 + -1;
    LORelease();
    if (lVar7 == 0) {
      (**(code **)(*local_250 + 0x10))(local_250);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_250);
    }
  }
  pppppppuVar2 = local_d0;
  if (local_d0 != (undefined8 *******)0x0) {
    LOAcquire();
    ppppppuVar8 = local_d0[1];
    local_d0[1] = (undefined8 ******)((long)ppppppuVar8 + -1);
    LORelease();
    if (ppppppuVar8 == (undefined8 ******)0x0) {
      (*(code *)(*local_d0)[2])(local_d0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(pppppppuVar2);
    }
  }
  pppppppuVar2 = local_120;
  if (local_120 == (undefined8 *******)0x0) {
LAB_032f27d8:
    if (local_1c8 != (undefined8 ******)0x0) goto LAB_032f27e0;
LAB_032f2bcc:
    iVar10 = thunk_FUN_05e1d97c(4);
    if (iVar10 != 0) {
      FUN_0488143c(&local_178);
      pppppppuVar2 = local_178;
      if (-1 < cStack_161) {
        pppppppuVar2 = &local_178;
      }
      if ((DAT_0a3e7408 & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3e73f0)[uVar14] = (&DAT_088d08e0)[uVar14] + 0x8a ^ (&DAT_088d08d0)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x18);
        DAT_0a3e7408 = 1;
      }
      if ((DAT_0a3e8449 & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3e8431)[uVar14] = (&DAT_088d2618)[uVar14] + 0x8a ^ (&DAT_088d2608)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x18);
        DAT_0a3e8449 = 1;
      }
      FUN_05e1d050(&local_258,4,pppppppuVar2,&DAT_0a3e73f0,&DAT_0a3e8431,0x720,0,0);
      local_128 = (long *******)0x0;
      local_128 = (long *******)&local_120;
      if ((DAT_0a3ea7a2 & 1) == 0) {
        uVar14 = 0;
        do {
          uVar18 = *(undefined4 *)((long)&DAT_088d5f33 + uVar14);
          uVar4 = CONCAT12((char)((uint)uVar18 >> 8),(short)uVar18) & 0xff00ff;
          uVar19 = *(undefined4 *)((long)&DAT_088d5f1f + uVar14 % 0x14);
          *(uint *)((long)&DAT_0a3ea75a + uVar14) =
               CONCAT13((char)((uint)uVar18 >> 0x18) + 0x69U ^ (byte)((uint)uVar19 >> 0x18),
                        CONCAT12((char)((uint)uVar18 >> 0x10) + 0x69U ^ (byte)((uint)uVar19 >> 0x10)
                                 ,CONCAT11((char)(uVar4 >> 0x10) + 0x69U ^ (byte)((uint)uVar19 >> 8)
                                           ,(char)uVar4 + 0x69U ^ (byte)uVar19)));
          uVar14 = uVar14 + 4;
        } while (uVar14 != 0x48);
        DAT_0a3ea7a2 = 1;
      }
      lVar7 = 0;
      do {
        lVar15 = lVar7;
        uVar17 = (uint)param_5;
        *(undefined1 *)((long)&local_120 + lVar15) =
             *(undefined1 *)
              ((long)&DAT_0a3ea75a +
              (ulong)(uVar17 + (int)((param_5 & 0xffffffff) / 10) * -10 + 0x23));
        lVar7 = lVar15 + 1;
        param_5 = (param_5 & 0xffffffff) / 10;
      } while (9 < uVar17);
      *(undefined1 *)((long)&local_120 + lVar15 + 1) = 0;
      if (8 < lVar15 + 8U) {
        puVar13 = (undefined1 *)((long)&local_120 + lVar15);
        puVar16 = (undefined1 *)((long)&local_120 + 1);
        do {
          uVar3 = *puVar13;
          *puVar13 = puVar16[-1];
          puVar16[-1] = uVar3;
          bVar6 = puVar16 < puVar13 + -1;
          puVar13 = puVar13 + -1;
          puVar16 = puVar16 + 1;
        } while (bVar6);
      }
      if ((DAT_0a3e78a9 & 1) == 0) {
        uVar14 = 0;
        do {
          (&DAT_0a3e7885)[uVar14] = (&DAT_088d0f08)[uVar14] + 0x8a ^ (&DAT_088d0ef8)[uVar14 & 0xf];
          uVar14 = uVar14 + 1;
        } while (uVar14 != 0x24);
        DAT_0a3e78a9 = 1;
      }
      ppppppuStack_c8 = (undefined8 ******)0x0;
      local_d0 = (undefined8 *******)0x0;
      local_d8 = (long *******)&local_128;
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
      uStack_68 = 0;
      local_70 = 0;
      local_60 = 0;
      FUN_05e1d31c(&local_258,&DAT_0a3e7885,&local_d8);
      thunk_FUN_05e1d0bc(&local_258);
      if (cStack_161 < '\0') {
        __ZdlPvm(local_178,CONCAT17(cStack_161,local_168) & 0x7fffffffffffffff);
      }
    }
    FUN_0335fcb0(param_1);
  }
  else {
    LOAcquire();
    ppppppuVar8 = local_120[1];
    local_120[1] = (undefined8 ******)((long)ppppppuVar8 + -1);
    LORelease();
    if (ppppppuVar8 != (undefined8 ******)0x0) goto LAB_032f27d8;
    (*(code *)(*local_120)[2])(local_120);
    __ZNSt3__119__shared_weak_count14__release_weakEv(pppppppuVar2);
    if (local_1c8 == (undefined8 ******)0x0) goto LAB_032f2bcc;
LAB_032f27e0:
    if (*(char *)((long)param_3 + 0x17) < '\0') {
      FUN_00018d20(&local_2a0,*param_3,param_3[1]);
    }
    else {
      pppppplStack_298 = param_3[1];
      local_2a0 = *param_3;
      local_290 = param_3[2];
    }
    local_278 = local_1c0;
    if (local_1c0 != (undefined8 ******)0x0) {
      local_1c0[1] = (undefined8 *****)((long)local_1c0[1] + 1);
    }
    local_d8 = (long *******)&SUB_aaaaaaaaaaaaaaaa;
    local_d0 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
    local_288 = (int)param_4;
    local_280 = local_1c8;
    FUN_021efaf0(&local_d8,&local_258);
    pppppppuVar2 = local_d0;
    ppppppplVar5 = local_d8;
    local_128 = local_d8;
    local_120 = local_d0;
    if (local_d0 != (undefined8 *******)0x0) {
      local_d0[1] = (undefined8 ******)((long)local_d0[1] + 1);
    }
    if ((DAT_0a3ead0b & 1) == 0) {
      DAT_0a3ead00._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
      DAT_0a3ead00._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
      DAT_0a3ead00._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
      DAT_0a3ead00._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
      DAT_0a3ead00._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
      DAT_0a3ead00._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
      DAT_0a3ead00._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
      DAT_0a3ead00._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
      DAT_0a3ead08 = 0x2928;
      DAT_0a3ead0a = 0;
      DAT_0a3ead0b = 1;
    }
    if ((DAT_0a3e7559 & 1) == 0) {
      uVar14 = 0;
      do {
        (&DAT_0a3e74ef)[uVar14] = (&DAT_088d0a59)[uVar14] + 0x8a ^ (&DAT_088d0a49)[uVar14 & 0xf];
        uVar14 = uVar14 + 1;
      } while (uVar14 != 0x6a);
      DAT_0a3e7559 = 1;
    }
    FUN_0003bb6c(&local_258,&DAT_0a3ead00,&DAT_0a3e74ef,0x726);
    pppppppuVar12 = (undefined8 *******)__Znwm(0x68);
    FUN_00033c40(pppppppuVar12,FUN_033677c4,FUN_03367954);
    if ((long)local_290 < 0) {
      FUN_00018d20(pppppppuVar12 + 5,local_2a0,pppppplStack_298);
    }
    else {
      pppppppuVar12[6] = pppppplStack_298;
      pppppppuVar12[5] = local_2a0;
      pppppppuVar12[7] = local_290;
    }
    *(int *)(pppppppuVar12 + 8) = local_288;
    pppppppuVar12[9] = local_280;
    pppppppuVar12[10] = local_278;
    ppppppuVar8 = (undefined8 ******)0x0;
    if (local_278 != (undefined8 ******)0x0) {
      ppppppuVar8 = (undefined8 ******)local_278[1];
      local_278[1] = (undefined8 *****)((long)ppppppuVar8 + 1);
    }
    pppppppuVar12[0xb] = ppppppplVar5;
    pppppppuVar12[0xc] = pppppppuVar2;
    if (pppppppuVar2 != (undefined8 *******)0x0) {
      ppppppuVar8 = pppppppuVar2[1];
      pppppppuVar2[1] = (undefined8 ******)((long)ppppppuVar8 + 1);
    }
    local_178 = pppppppuVar12;
    FUN_03c17870(ppppppuVar8,&local_258,&local_178);
    FUN_00033d2c(&local_178);
    if (pppppppuVar2 != (undefined8 *******)0x0) {
      LOAcquire();
      ppppppuVar8 = pppppppuVar2[1];
      pppppppuVar2[1] = (undefined8 ******)((long)ppppppuVar8 + -1);
      LORelease();
      if (ppppppuVar8 == (undefined8 ******)0x0) {
        (*(code *)(*pppppppuVar2)[2])(pppppppuVar2);
        __ZNSt3__119__shared_weak_count14__release_weakEv(pppppppuVar2);
      }
    }
    pppppppuVar2 = local_d0;
    *param_1 = local_d8;
    param_1[1] = local_d0;
    if ((local_d0 != (undefined8 *******)0x0) &&
       (local_d0[1] = (undefined8 ******)((long)local_d0[1] + 1),
       local_d0 != (undefined8 *******)0x0)) {
      LOAcquire();
      ppppppuVar8 = local_d0[1];
      local_d0[1] = (undefined8 ******)((long)ppppppuVar8 + -1);
      LORelease();
      if (ppppppuVar8 == (undefined8 ******)0x0) {
        (*(code *)(*local_d0)[2])(local_d0);
        __ZNSt3__119__shared_weak_count14__release_weakEv(pppppppuVar2);
      }
    }
    ppppppuVar8 = local_278;
    if (local_278 != (undefined8 ******)0x0) {
      LOAcquire();
      pppppuVar9 = local_278[1];
      local_278[1] = (undefined8 *****)((long)pppppuVar9 + -1);
      LORelease();
      if (pppppuVar9 == (undefined8 *****)0x0) {
        (*(code *)(*local_278)[2])(local_278);
        __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppuVar8);
      }
    }
    if ((long)local_290 < 0) {
      __ZdlPvm(local_2a0,(ulong)local_290 & 0x7fffffffffffffff);
    }
  }
  ppppppuVar8 = local_1c0;
  if (local_1c0 != (undefined8 ******)0x0) {
    LOAcquire();
    pppppuVar9 = local_1c0[1];
    local_1c0[1] = (undefined8 *****)((long)pppppuVar9 + -1);
    LORelease();
    if (pppppuVar9 == (undefined8 *****)0x0) {
      (*(code *)(*local_1c0)[2])(local_1c0);
      __ZNSt3__119__shared_weak_count14__release_weakEv(ppppppuVar8);
    }
  }
LAB_032f30f0:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_58) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


