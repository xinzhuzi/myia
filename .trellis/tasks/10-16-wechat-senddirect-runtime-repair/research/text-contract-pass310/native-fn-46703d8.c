// Ghidra inferred pseudocode; requested=0x46703d8
// entry=0466fbd0 end=04670493

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0466fbd0(undefined8 ******param_1,undefined8 *param_2)

{
  undefined8 *******pppppppuVar1;
  undefined1 uVar2;
  uint3 uVar3;
  long *plVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  undefined8 *******pppppppuVar7;
  bool bVar8;
  undefined8 ******ppppppuVar9;
  int iVar10;
  undefined1 *puVar11;
  long lVar12;
  long lVar13;
  ulong uVar14;
  undefined1 *puVar15;
  undefined1 *puVar16;
  ulong uVar17;
  long lVar18;
  uint uVar19;
  long lVar20;
  long lVar21;
  long *plVar22;
  undefined4 uVar23;
  undefined4 uVar24;
  undefined4 uVar25;
  undefined4 uVar26;
  undefined4 uVar27;
  undefined4 uVar28;
  undefined4 uVar29;
  undefined4 uVar30;
  undefined4 uVar31;
  undefined4 uVar32;
  undefined4 uVar33;
  undefined4 uVar34;
  undefined4 uVar35;
  undefined4 uVar36;
  undefined4 uVar37;
  undefined4 uVar38;
  undefined4 uVar39;
  undefined8 *******local_2c8 [2];
  undefined7 local_2b8;
  char cStack_2b1;
  undefined8 *******local_2b0;
  undefined8 *******local_2a8;
  undefined8 local_2a0;
  long *local_220;
  long *local_218;
  undefined8 ******local_210;
  undefined8 local_208;
  undefined8 uStack_200;
  undefined8 local_1f8;
  undefined8 local_1f0;
  undefined1 local_1e8 [72];
  undefined8 *******local_1a0;
  undefined8 local_198;
  undefined8 *******local_150;
  undefined8 local_148;
  undefined8 *******local_100;
  undefined8 *******local_f8;
  undefined8 *local_f0;
  undefined8 local_e8;
  undefined8 uStack_e0;
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
  long local_80;
  
  local_80 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_210 = param_1;
  if (*(char *)((long)param_2 + 0x17) < '\0') {
    FUN_00018d20(&local_208,*param_2,param_2[1]);
  }
  else {
    uStack_200 = param_2[1];
    local_208 = *param_2;
    local_1f8 = param_2[2];
  }
  local_100 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
  local_f8 = (undefined8 *******)&SUB_aaaaaaaaaaaaaaaa;
  FUN_021efaf0(&local_100,&local_2b0);
  pppppppuVar7 = local_f8;
  pppppppuVar1 = local_100;
  ppppppuVar9 = local_210;
  local_150 = local_100;
  local_148 = local_f8;
  if (local_f8 != (undefined8 *******)0x0) {
    local_f8[1] = (undefined8 ******)((long)local_f8[1] + 1);
  }
  if ((DAT_0a45e7d3 & 1) == 0) {
    DAT_0a45e7c8._0_1_ = s_StartScaoperatorh_op_084cadf8[8];
    DAT_0a45e7c8._1_1_ = s_StartScaoperatorh_op_084cadf8[9];
    DAT_0a45e7c8._2_1_ = s_StartScaoperatorh_op_084cadf8[10];
    DAT_0a45e7c8._3_1_ = s_StartScaoperatorh_op_084cadf8[0xb];
    DAT_0a45e7c8._4_1_ = s_StartScaoperatorh_op_084cadf8[0xc];
    DAT_0a45e7c8._5_1_ = s_StartScaoperatorh_op_084cadf8[0xd];
    DAT_0a45e7c8._6_1_ = s_StartScaoperatorh_op_084cadf8[0xe];
    DAT_0a45e7c8._7_1_ = s_StartScaoperatorh_op_084cadf8[0xf];
    DAT_0a45e7d0 = 0x2928;
    DAT_0a45e7d2 = 0;
    DAT_0a45e7d3 = 1;
  }
  if ((DAT_0a45e308 & 1) == 0) {
    uVar17 = 0;
    do {
      uVar28 = *(undefined4 *)((long)&DAT_08a143c1 + uVar17);
      uVar3 = CONCAT12((char)((uint)uVar28 >> 8),(short)uVar28) & 0xff00ff;
      uVar36 = *(undefined4 *)((long)&DAT_08a143ad + uVar17 % 0x14);
      *(uint *)((long)&DAT_0a45e2c1 + uVar17) =
           CONCAT13((char)((uint)uVar28 >> 0x18) + 0x8aU ^ (byte)((uint)uVar36 >> 0x18),
                    CONCAT12((char)((uint)uVar28 >> 0x10) + 0x8aU ^ (byte)((uint)uVar36 >> 0x10),
                             CONCAT11((char)(uVar3 >> 0x10) + 0x8aU ^ (byte)((uint)uVar36 >> 8),
                                      (char)uVar3 + 0x8aU ^ (byte)uVar36)));
      uVar17 = uVar17 + 4;
    } while (uVar17 != 0x44);
    DAT_0a45e305 = 0x6363;
    DAT_0a45e307 = 0;
    DAT_0a45e308 = 1;
  }
  FUN_0003bb6c(&local_2b0,&DAT_0a45e7c8,&DAT_0a45e2c1,0x2a5);
  if (((ulong)ppppppuVar9 & 0xfffffffc00000000) == DAT_09ffaec8) {
    FUN_0003f84c(ppppppuVar9);
  }
  local_2c8[0] = (undefined8 *******)ppppppuVar9;
  puVar11 = (undefined1 *)__Znwm(0x58);
  FUN_00033c40(puVar11,FUN_0467b160,FUN_0467b308);
  *(undefined8 *******)(puVar11 + 0x28) = ppppppuVar9;
  local_2c8[0] = (undefined8 *******)0x0;
  *(undefined8 ********)(puVar11 + 0x30) = pppppppuVar1;
  *(undefined8 ********)(puVar11 + 0x38) = pppppppuVar7;
  if (pppppppuVar7 != (undefined8 *******)0x0) {
    pppppppuVar7[1] = (undefined8 ******)((long)pppppppuVar7[1] + 1);
  }
  if ((long)local_1f8 < 0) {
    FUN_00018d20(puVar11 + 0x40,local_208,uStack_200);
  }
  else {
    *(undefined8 *)(puVar11 + 0x48) = uStack_200;
    *(undefined8 *)(puVar11 + 0x40) = local_208;
    *(ulong *)(puVar11 + 0x50) = local_1f8;
  }
  local_1f0 = puVar11;
  FUN_04b7141c(&local_2b0,&local_1f0,0,0);
  FUN_00033d2c(&local_1f0);
  if (pppppppuVar7 != (undefined8 *******)0x0) {
    LOAcquire();
    ppppppuVar9 = pppppppuVar7[1];
    pppppppuVar7[1] = (undefined8 ******)((long)ppppppuVar9 + -1);
    LORelease();
    if (ppppppuVar9 == (undefined8 ******)0x0) {
      (*(code *)(*pppppppuVar7)[2])(pppppppuVar7);
      __ZNSt3__119__shared_weak_count14__release_weakEv(pppppppuVar7);
    }
  }
  pppppppuVar1 = local_f8;
  local_1a0 = local_100;
  local_198 = local_f8;
  if ((local_f8 != (undefined8 *******)0x0) &&
     (local_f8[1] = (undefined8 ******)((long)local_f8[1] + 1), local_f8 != (undefined8 *******)0x0)
     ) {
    LOAcquire();
    ppppppuVar9 = local_f8[1];
    local_f8[1] = (undefined8 ******)((long)ppppppuVar9 + -1);
    LORelease();
    if (ppppppuVar9 == (undefined8 ******)0x0) {
      (*(code *)(*local_f8)[2])(local_f8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(pppppppuVar1);
    }
  }
  local_2b0 = local_1a0;
  local_2a8 = local_198;
  ppppppuVar9 = (undefined8 ******)0x0;
  if (local_198 != (undefined8 *******)0x0) {
    ppppppuVar9 = local_198[1];
    local_198[1] = (undefined8 ******)((long)ppppppuVar9 + 1);
  }
  local_2a0 = 0;
  FUN_066856fc(ppppppuVar9,&local_2b0);
  FUN_0666a844(local_2b0);
  pppppppuVar1 = local_2a8;
  if (local_2a8 != (undefined8 *******)0x0) {
    LOAcquire();
    ppppppuVar9 = local_2a8[1];
    local_2a8[1] = (undefined8 ******)((long)ppppppuVar9 + -1);
    LORelease();
    if (ppppppuVar9 == (undefined8 ******)0x0) {
      (*(code *)(*local_2a8)[2])(local_2a8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(pppppppuVar1);
    }
  }
  pppppppuVar1 = local_198;
  if (local_198 != (undefined8 *******)0x0) {
    LOAcquire();
    ppppppuVar9 = local_198[1];
    local_198[1] = (undefined8 ******)((long)ppppppuVar9 + -1);
    LORelease();
    if (ppppppuVar9 == (undefined8 ******)0x0) {
      (*(code *)(*local_198)[2])(local_198);
      __ZNSt3__119__shared_weak_count14__release_weakEv(pppppppuVar1);
    }
  }
  if ((long)local_1f8 < 0) {
    __ZdlPvm(local_208,local_1f8 & 0x7fffffffffffffff);
  }
  lVar12 = FUN_0001accc(param_1[0x13]);
  uVar5 = s_input_ackernel_cpadV_08a133a0._8_8_;
  plVar22 = *(long **)(lVar12 + 0x10);
  if (plVar22 != (long *)0x0) {
    uVar23 = (undefined4)DAT_086fa3f0;
    uVar29 = (undefined4)DAT_084d88e0;
    uVar28 = (undefined4)DAT_0849b098;
    uVar24 = (undefined4)DAT_084cfd08;
    uVar25 = (undefined4)DAT_08a134b8;
    uVar30 = (undefined4)DAT_084cfd10;
    uVar26 = (undefined4)DAT_085465e0;
    uVar37 = (undefined4)DAT_085465e8;
    uVar31 = (undefined4)DAT_086026d8;
    uVar38 = (undefined4)DAT_08486068;
    uVar32 = (undefined4)DAT_084f0808;
    uVar39 = (undefined4)DAT_087e3180;
    uVar36 = (undefined4)DAT_084df420;
    uVar33 = (undefined4)DAT_08a134b0;
    uVar34 = (undefined4)DAT_085465d8;
    do {
      lVar12 = __ZNSt3__16chrono12steady_clock3nowEv();
      local_220 = (long *)plVar22[5];
      local_218 = (long *)plVar22[6];
      if (local_218 != (long *)0x0) {
        local_218[1] = local_218[1] + 1;
      }
      (**(code **)(*local_220 + 0x28))(local_220,param_2);
      lVar13 = __ZNSt3__16chrono12steady_clock3nowEv();
      uVar17 = FUN_04a0d4ac(plVar22 + 2);
      iVar10 = thunk_FUN_05e1d97c(2);
      plVar4 = local_218;
      if (iVar10 != 0) {
        FUN_0488143c(local_2c8);
        uVar6 = s_input_ackernel_cpadV_08a133a0._8_8_;
        pppppppuVar1 = local_2c8[0];
        if (-1 < cStack_2b1) {
          pppppppuVar1 = local_2c8;
        }
        if ((DAT_0a45df8a & 1) == 0) {
          s_input_ackernel_cpadV_08a133a0[8] = (char)uVar5;
          s_input_ackernel_cpadV_08a133a0[9] = SUB81(uVar5,1);
          s_input_ackernel_cpadV_08a133a0[10] = SUB81(uVar5,2);
          s_input_ackernel_cpadV_08a133a0[0xb] = SUB81(uVar5,3);
          s_input_ackernel_cpadV_08a133a0[0xc] = SUB81(uVar5,4);
          s_input_ackernel_cpadV_08a133a0[0xd] = SUB81(uVar5,5);
          s_input_ackernel_cpadV_08a133a0[0xe] = SUB81(uVar5,6);
          s_input_ackernel_cpadV_08a133a0[0xf] = SUB81(uVar5,7);
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
        if ((DAT_0a45e369 & 1) == 0) {
          DAT_0a45e368 = 0;
          DAT_0a45e369 = 1;
          _DAT_0a45e34c = CONCAT44(uVar32,uVar39);
          uRam000000000a45e354 = CONCAT44(uVar33,uVar36);
          DAT_0a45e35c = CONCAT44(uVar26,uVar34);
          DAT_0a45e364 = uVar37;
        }
        s_input_ackernel_cpadV_08a133a0._8_8_ = uVar6;
        FUN_05e1d050(&local_2b0,2,pppppppuVar1,&DAT_0a45df80,&DAT_0a45e34c,0x2b7,0,0);
        local_150 = (undefined8 *******)0x0;
        if ((DAT_0a45e65a & 1) == 0) {
          uVar14 = 0;
          do {
            uVar27 = *(undefined4 *)((long)&DAT_08a1498d + uVar14);
            uVar3 = CONCAT12((char)((uint)uVar27 >> 8),(short)uVar27) & 0xff00ff;
            uVar35 = *(undefined4 *)((long)&DAT_08a14979 + uVar14 % 0x14);
            *(uint *)((long)&DAT_0a45e612 + uVar14) =
                 CONCAT13((char)((uint)uVar27 >> 0x18) + 0x8aU ^ (byte)((uint)uVar35 >> 0x18),
                          CONCAT12((char)((uint)uVar27 >> 0x10) + 0x8aU ^
                                   (byte)((uint)uVar35 >> 0x10),
                                   CONCAT11((char)(uVar3 >> 0x10) + 0x8aU ^
                                            (byte)((uint)uVar35 >> 8),
                                            (char)uVar3 + 0x8aU ^ (byte)uVar35)));
            uVar14 = uVar14 + 4;
          } while (uVar14 != 0x48);
          DAT_0a45e65a = 1;
        }
        lVar21 = 0;
        uVar14 = uVar17;
        do {
          lVar18 = lVar21;
          uVar19 = (uint)uVar14;
          *(undefined1 *)((long)&local_148 + lVar18) =
               *(undefined1 *)
                ((long)&DAT_0a45e612 +
                (ulong)(uVar19 + (int)((uVar14 & 0xffffffff) / 10) * -10 + 0x23));
          lVar21 = lVar18 + 1;
          uVar14 = (uVar14 & 0xffffffff) / 10;
        } while (9 < uVar19);
        *(undefined1 *)((long)&local_148 + lVar18 + 1) = 0;
        if (8 < lVar18 + 8U) {
          puVar11 = (undefined1 *)((long)&local_148 + lVar18);
          puVar15 = (undefined1 *)((long)&local_148 + 1);
          do {
            uVar2 = *puVar11;
            *puVar11 = puVar15[-1];
            puVar15[-1] = uVar2;
            bVar8 = puVar15 < puVar11 + -1;
            puVar11 = puVar11 + -1;
            puVar15 = puVar15 + 1;
          } while (bVar8);
        }
        local_150 = (undefined8 *******)&local_148;
        local_1a0 = (undefined8 *******)0x0;
        uVar17 = uVar17 >> 0x20;
        lVar21 = 0;
        do {
          lVar18 = lVar21;
          uVar19 = (uint)uVar17;
          *(undefined1 *)((long)&local_198 + lVar18) =
               *(undefined1 *)
                ((long)&DAT_0a45e612 + (ulong)(uVar19 + (int)(uVar17 / 10) * -10 + 0x23));
          uVar17 = uVar17 / 10;
          lVar21 = lVar18 + 1;
        } while (9 < uVar19);
        *(undefined1 *)((long)&local_198 + lVar18 + 1) = 0;
        if (8 < lVar18 + 8U) {
          puVar11 = (undefined1 *)((long)&local_198 + lVar18);
          puVar15 = (undefined1 *)((long)&local_198 + 1);
          do {
            uVar2 = *puVar11;
            *puVar11 = puVar15[-1];
            puVar15[-1] = uVar2;
            bVar8 = puVar15 < puVar11 + -1;
            puVar11 = puVar11 + -1;
            puVar15 = puVar15 + 1;
          } while (bVar8);
        }
        lVar18 = (lVar13 - lVar12) / 1000000;
        lVar21 = 8;
        local_1a0 = (undefined8 *******)&local_198;
        do {
          lVar20 = lVar21;
          *(undefined1 *)((long)&local_1f0 + lVar20) = *(undefined1 *)(lVar18 % 10 + 0xa45e635);
          lVar21 = lVar20 + 1;
          uVar17 = lVar18 + 9;
          lVar18 = lVar18 / 10;
        } while (0x12 < uVar17);
        if (lVar13 - lVar12 < -999999) {
          *(undefined1 *)((long)&local_1f0 + lVar21) = 0x2d;
          lVar21 = lVar20 + 2;
        }
        *(undefined1 *)((long)&local_1f0 + lVar21) = 0;
        if (9 < lVar21) {
          puVar15 = (undefined1 *)((long)&local_1f8 + lVar21 + 7);
          puVar11 = local_1e8;
          do {
            puVar11 = puVar11 + 1;
            uVar2 = *puVar15;
            puVar16 = puVar15 + -1;
            *puVar15 = puVar11[-1];
            puVar11[-1] = uVar2;
            puVar15 = puVar16;
          } while (puVar11 < puVar16);
        }
        if ((DAT_0a45e397 & 1) == 0) {
          DAT_0a45e394 = 0x5f25;
          DAT_0a45e396 = 0;
          DAT_0a45e397 = 1;
          _DAT_0a45e36c = CONCAT44(uVar23,uVar29);
          uRam000000000a45e374 = CONCAT44(uVar24,uVar28);
          _DAT_0a45e37c = CONCAT44(uVar25,uVar30);
          uRam000000000a45e384 = CONCAT44(uVar37,uVar26);
          DAT_0a45e38c = CONCAT44(uVar31,uVar38);
        }
        uStack_e0 = 0;
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
        local_88 = 0;
        local_1f0 = local_1e8;
        local_100 = &local_150;
        local_f8 = &local_1a0;
        local_f0 = &local_1f0;
        FUN_05e1d31c(&local_2b0,&DAT_0a45e36c,&local_100);
        thunk_FUN_05e1d0bc(&local_2b0);
        plVar4 = local_218;
        if (cStack_2b1 < '\0') {
          __ZdlPvm(local_2c8[0],CONCAT17(cStack_2b1,local_2b8) & 0x7fffffffffffffff);
          plVar4 = local_218;
        }
      }
      local_218 = plVar4;
      if (plVar4 != (long *)0x0) {
        LOAcquire();
        lVar12 = plVar4[1];
        plVar4[1] = lVar12 + -1;
        LORelease();
        if (lVar12 == 0) {
          (**(code **)(*plVar4 + 0x10))(plVar4);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
        }
      }
      plVar22 = (long *)*plVar22;
    } while (plVar22 != (long *)0x0);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_80) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


