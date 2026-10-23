// Ghidra inferred pseudocode; requested=0x30f27e4
// entry=030f27e4 end=030f318b

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_030f27e4(long param_1,long *param_2)

{
  undefined8 ******ppppppuVar1;
  undefined1 uVar2;
  undefined8 uVar3;
  bool bVar4;
  long lVar5;
  int iVar6;
  int iVar7;
  uint uVar8;
  ulong uVar9;
  undefined1 *puVar10;
  undefined1 *puVar11;
  undefined1 *puVar12;
  ulong uVar13;
  long lVar14;
  long *plVar15;
  long *plVar16;
  undefined8 *****local_2b8 [2];
  undefined7 local_2a8;
  char cStack_2a1;
  undefined8 local_2a0;
  long *plStack_298;
  undefined1 *local_210;
  undefined1 local_208 [72];
  undefined1 *local_1c0;
  undefined1 local_1b8 [72];
  undefined1 *local_170;
  undefined1 local_168 [72];
  undefined8 *****local_120;
  undefined8 local_118;
  undefined7 local_110;
  char cStack_109;
  undefined8 *****local_d0;
  undefined1 **ppuStack_c8;
  undefined1 **local_c0;
  undefined1 **ppuStack_b8;
  undefined8 local_b0;
  undefined8 uStack_a8;
  undefined8 uStack_a0;
  undefined8 uStack_98;
  undefined8 local_90;
  undefined8 uStack_88;
  undefined8 uStack_80;
  undefined8 uStack_78;
  undefined8 local_70;
  undefined8 uStack_68;
  undefined8 uStack_60;
  undefined8 uStack_58;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  if ((*(long *)(param_1 + 0x18) == 0) || (*(int *)(*(long *)(param_1 + 0x18) + 0xf4) == 0)) {
    if ((*(long *)(param_1 + 8) != 0) && ((long *)*param_2 != (long *)0x0)) {
      iVar6 = (**(code **)(*(long *)*param_2 + 0x10))();
      iVar7 = (**(code **)(**(long **)(param_1 + 8) + 0x10))();
      if (iVar6 == iVar7) {
        iVar6 = (**(code **)(*(long *)*param_2 + 0x18))();
        iVar7 = (**(code **)(**(long **)(param_1 + 8) + 0x18))();
        if (iVar6 == iVar7) {
          iVar6 = thunk_FUN_05e1d97c(2);
          if (iVar6 == 0) goto LAB_030f3158;
          FUN_0488143c(&local_120);
          ppppppuVar1 = (undefined8 ******)local_120;
          if (-1 < cStack_109) {
            ppppppuVar1 = &local_120;
          }
          if ((DAT_0a3d9838 & 1) == 0) {
            uVar9 = 0;
            do {
              (&DAT_0a3d9820)[uVar9] = (&DAT_088b055e)[uVar9] + 0x8a ^ (&DAT_088b054e)[uVar9 & 0xf];
              uVar9 = uVar9 + 1;
            } while (uVar9 != 0x18);
            DAT_0a3d9838 = 1;
          }
          if ((DAT_0a3d992e & 1) == 0) {
            DAT_0a3d9920._0_1_ = s_sending__xwechatSetSendS_088b02f0[0x10];
            DAT_0a3d9920._1_1_ = s_sending__xwechatSetSendS_088b02f0[0x11];
            DAT_0a3d9920._2_1_ = s_sending__xwechatSetSendS_088b02f0[0x12];
            DAT_0a3d9920._3_1_ = s_sending__xwechatSetSendS_088b02f0[0x13];
            DAT_0a3d9920._4_1_ = s_sending__xwechatSetSendS_088b02f0[0x14];
            DAT_0a3d9920._5_1_ = s_sending__xwechatSetSendS_088b02f0[0x15];
            DAT_0a3d9920._6_1_ = s_sending__xwechatSetSendS_088b02f0[0x16];
            DAT_0a3d9920._7_1_ = s_sending__xwechatSetSendS_088b02f0[0x17];
            DAT_0a3d9928 = (undefined4)ram0x084e31f0;
            DAT_0a3d992c = 0x65;
            DAT_0a3d992e = 1;
          }
          FUN_05e1d050(&local_2a0,2,ppppppuVar1,&DAT_0a3d9820,&DAT_0a3d9920,0xe7,0,0);
          if ((DAT_0a3d9981 & 1) == 0) {
            uVar9 = 0;
            do {
              (&DAT_0a3d9955)[uVar9] = (&DAT_088b0713)[uVar9] + 0x8a ^ (&DAT_088b0703)[uVar9 & 0xf];
              uVar9 = uVar9 + 1;
            } while (uVar9 != 0x2c);
            DAT_0a3d9981 = 1;
          }
          uStack_68 = 0;
          local_70 = 0;
          uStack_58 = 0;
          uStack_60 = 0;
          uStack_88 = 0;
          local_90 = 0;
          uStack_78 = 0;
          uStack_80 = 0;
          uStack_a8 = 0;
          local_b0 = 0;
          uStack_98 = 0;
          uStack_a0 = 0;
          ppuStack_c8 = (undefined1 **)0x0;
          local_d0 = (undefined8 ******)0x0;
          ppuStack_b8 = (undefined1 **)0x0;
          local_c0 = (undefined1 **)0x0;
          FUN_05e1d31c(&local_2a0,&DAT_0a3d9955,&local_d0);
          goto LAB_030f2984;
        }
      }
      iVar6 = thunk_FUN_05e1d97c(2);
      if (iVar6 != 0) {
        FUN_0488143c(local_2b8);
        ppppppuVar1 = (undefined8 ******)local_2b8[0];
        if (-1 < cStack_2a1) {
          ppppppuVar1 = local_2b8;
        }
        if ((DAT_0a3d9838 & 1) == 0) {
          uVar9 = 0;
          do {
            (&DAT_0a3d9820)[uVar9] = (&DAT_088b055e)[uVar9] + 0x8a ^ (&DAT_088b054e)[uVar9 & 0xf];
            uVar9 = uVar9 + 1;
          } while (uVar9 != 0x18);
          DAT_0a3d9838 = 1;
        }
        if ((DAT_0a3d992e & 1) == 0) {
          DAT_0a3d9920._0_1_ = s_sending__xwechatSetSendS_088b02f0[0x10];
          DAT_0a3d9920._1_1_ = s_sending__xwechatSetSendS_088b02f0[0x11];
          DAT_0a3d9920._2_1_ = s_sending__xwechatSetSendS_088b02f0[0x12];
          DAT_0a3d9920._3_1_ = s_sending__xwechatSetSendS_088b02f0[0x13];
          DAT_0a3d9920._4_1_ = s_sending__xwechatSetSendS_088b02f0[0x14];
          DAT_0a3d9920._5_1_ = s_sending__xwechatSetSendS_088b02f0[0x15];
          DAT_0a3d9920._6_1_ = s_sending__xwechatSetSendS_088b02f0[0x16];
          DAT_0a3d9920._7_1_ = s_sending__xwechatSetSendS_088b02f0[0x17];
          DAT_0a3d9928 = (undefined4)ram0x084e31f0;
          DAT_0a3d992c = 0x65;
          DAT_0a3d992e = 1;
        }
        FUN_05e1d050(&local_2a0,2,ppppppuVar1,&DAT_0a3d9820,&DAT_0a3d9920,0xeb,0,0);
        uVar9 = (**(code **)(**(long **)(param_1 + 8) + 0x10))();
        local_120 = (undefined8 *****)0x0;
        local_120 = (undefined8 *****)&local_118;
        if ((DAT_0a3d9bbd & 1) == 0) {
          uVar13 = 0;
          do {
            (&DAT_0a3d9b75)[uVar13] = (&DAT_088b0a63)[uVar13] + 0x8a ^ (&DAT_088b0a53)[uVar13 & 0xf]
            ;
            uVar13 = uVar13 + 1;
          } while (uVar13 != 0x48);
          DAT_0a3d9bbd = 1;
        }
        lVar5 = 0;
        do {
          lVar14 = lVar5;
          uVar8 = (uint)uVar9;
          *(undefined1 *)((long)&local_118 + lVar14) =
               (&DAT_0a3d9b75)[uVar8 + (int)((uVar9 & 0xffffffff) / 10) * -10 + 0x23];
          uVar9 = (uVar9 & 0xffffffff) / 10;
          lVar5 = lVar14 + 1;
        } while (9 < uVar8);
        *(undefined1 *)((long)&local_118 + lVar14 + 1) = 0;
        if (8 < lVar14 + 8U) {
          puVar10 = (undefined1 *)((long)&local_118 + lVar14);
          puVar12 = (undefined1 *)((long)&local_118 + 1);
          do {
            uVar2 = *puVar10;
            *puVar10 = puVar12[-1];
            puVar12[-1] = uVar2;
            bVar4 = puVar12 < puVar10 + -1;
            puVar10 = puVar10 + -1;
            puVar12 = puVar12 + 1;
          } while (bVar4);
        }
        uVar9 = (**(code **)(**(long **)(param_1 + 8) + 0x18))();
        local_170 = (undefined1 *)0x0;
        local_170 = local_168;
        if ((DAT_0a3d9bbd & 1) == 0) {
          uVar13 = 0;
          do {
            (&DAT_0a3d9b75)[uVar13] = (&DAT_088b0a63)[uVar13] + 0x8a ^ (&DAT_088b0a53)[uVar13 & 0xf]
            ;
            uVar13 = uVar13 + 1;
          } while (uVar13 != 0x48);
          DAT_0a3d9bbd = 1;
        }
        lVar5 = 0;
        do {
          lVar14 = lVar5;
          uVar8 = (uint)uVar9;
          local_168[lVar14] = (&DAT_0a3d9b75)[uVar8 + (int)((uVar9 & 0xffffffff) / 10) * -10 + 0x23]
          ;
          uVar9 = (uVar9 & 0xffffffff) / 10;
          lVar5 = lVar14 + 1;
        } while (9 < uVar8);
        local_168[lVar14 + 1] = 0;
        if (8 < lVar14 + 8U) {
          puVar10 = local_168;
          puVar12 = local_168 + lVar14;
          do {
            puVar10 = puVar10 + 1;
            uVar2 = *puVar12;
            puVar11 = puVar12 + -1;
            *puVar12 = puVar10[-1];
            puVar10[-1] = uVar2;
            puVar12 = puVar11;
          } while (puVar10 < puVar11);
        }
        uVar9 = (**(code **)(*(long *)*param_2 + 0x10))();
        local_1c0 = (undefined1 *)0x0;
        local_1c0 = local_1b8;
        if ((DAT_0a3d9bbd & 1) == 0) {
          uVar13 = 0;
          do {
            (&DAT_0a3d9b75)[uVar13] = (&DAT_088b0a63)[uVar13] + 0x8a ^ (&DAT_088b0a53)[uVar13 & 0xf]
            ;
            uVar13 = uVar13 + 1;
          } while (uVar13 != 0x48);
          DAT_0a3d9bbd = 1;
        }
        lVar5 = 0;
        do {
          lVar14 = lVar5;
          uVar8 = (uint)uVar9;
          local_1b8[lVar14] = (&DAT_0a3d9b75)[uVar8 + (int)((uVar9 & 0xffffffff) / 10) * -10 + 0x23]
          ;
          uVar9 = (uVar9 & 0xffffffff) / 10;
          lVar5 = lVar14 + 1;
        } while (9 < uVar8);
        local_1b8[lVar14 + 1] = 0;
        if (8 < lVar14 + 8U) {
          puVar10 = local_1b8;
          puVar12 = local_1b8 + lVar14;
          do {
            puVar10 = puVar10 + 1;
            uVar2 = *puVar12;
            puVar11 = puVar12 + -1;
            *puVar12 = puVar10[-1];
            puVar10[-1] = uVar2;
            puVar12 = puVar11;
          } while (puVar10 < puVar11);
        }
        uVar9 = (**(code **)(*(long *)*param_2 + 0x18))();
        local_210 = local_208;
        if ((DAT_0a3d9bbd & 1) == 0) {
          uVar13 = 0;
          do {
            (&DAT_0a3d9b75)[uVar13] = (&DAT_088b0a63)[uVar13] + 0x8a ^ (&DAT_088b0a53)[uVar13 & 0xf]
            ;
            uVar13 = uVar13 + 1;
          } while (uVar13 != 0x48);
          DAT_0a3d9bbd = 1;
        }
        lVar5 = 0;
        do {
          lVar14 = lVar5;
          uVar8 = (uint)uVar9;
          local_208[lVar14] = (&DAT_0a3d9b75)[uVar8 + (int)((uVar9 & 0xffffffff) / 10) * -10 + 0x23]
          ;
          uVar9 = (uVar9 & 0xffffffff) / 10;
          lVar5 = lVar14 + 1;
        } while (9 < uVar8);
        local_208[lVar14 + 1] = 0;
        if (8 < lVar14 + 8U) {
          puVar10 = local_208;
          puVar12 = local_208 + lVar14;
          do {
            puVar10 = puVar10 + 1;
            uVar2 = *puVar12;
            puVar11 = puVar12 + -1;
            *puVar12 = puVar10[-1];
            puVar10[-1] = uVar2;
            puVar12 = puVar11;
          } while (puVar10 < puVar11);
        }
        if ((DAT_0a3d99cd & 1) == 0) {
          uVar9 = 0;
          do {
            (&DAT_0a3d9982)[uVar9] = (&DAT_088b074f)[uVar9] + 0x8a ^ (&DAT_088b073f)[uVar9 & 0xf];
            uVar9 = uVar9 + 1;
          } while (uVar9 != 0x4b);
          DAT_0a3d99cd = 1;
        }
        local_d0 = &local_120;
        ppuStack_c8 = &local_170;
        local_c0 = &local_1c0;
        ppuStack_b8 = &local_210;
        uStack_a8 = 0;
        local_b0 = 0;
        uStack_98 = 0;
        uStack_a0 = 0;
        uStack_88 = 0;
        local_90 = 0;
        uStack_78 = 0;
        uStack_80 = 0;
        uStack_68 = 0;
        local_70 = 0;
        uStack_58 = 0;
        uStack_60 = 0;
        FUN_05e1d31c(&local_2a0,&DAT_0a3d9982,&local_d0);
        thunk_FUN_05e1d0bc(&local_2a0);
        if (cStack_2a1 < '\0') {
          __ZdlPvm(local_2b8[0],CONCAT17(cStack_2a1,local_2a8) & 0x7fffffffffffffff);
        }
      }
    }
    lVar5 = *param_2;
    lVar14 = param_2[1];
    if (lVar14 != 0) {
      *(long *)(lVar14 + 8) = *(long *)(lVar14 + 8) + 1;
    }
    plVar15 = *(long **)(param_1 + 0x10);
    *(long *)(param_1 + 8) = lVar5;
    *(long *)(param_1 + 0x10) = lVar14;
    if (plVar15 != (long *)0x0) {
      LOAcquire();
      lVar5 = plVar15[1];
      plVar15[1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*plVar15 + 0x10))(plVar15);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar15);
      }
    }
    FUN_030efce4(&local_2a0,param_1);
    plVar15 = plStack_298;
    uVar3 = local_2a0;
    local_2a0 = 0;
    plStack_298 = (long *)0x0;
    plVar16 = *(long **)(param_1 + 0x20);
    *(long **)(param_1 + 0x20) = plVar15;
    *(undefined8 *)(param_1 + 0x18) = uVar3;
    if (plVar16 != (long *)0x0) {
      LOAcquire();
      lVar5 = plVar16[1];
      plVar16[1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*plVar16 + 0x10))(plVar16);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar16);
      }
    }
    plVar15 = plStack_298;
    if (plStack_298 != (long *)0x0) {
      LOAcquire();
      lVar5 = plStack_298[1];
      plStack_298[1] = lVar5 + -1;
      LORelease();
      if (lVar5 == 0) {
        (**(code **)(*plStack_298 + 0x10))(plStack_298);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar15);
      }
    }
  }
  else {
    iVar6 = thunk_FUN_05e1d97c(4);
    if (iVar6 == 0) goto LAB_030f3158;
    FUN_0488143c(&local_120);
    ppppppuVar1 = (undefined8 ******)local_120;
    if (-1 < cStack_109) {
      ppppppuVar1 = &local_120;
    }
    if ((DAT_0a3d9838 & 1) == 0) {
      uVar9 = 0;
      do {
        (&DAT_0a3d9820)[uVar9] = (&DAT_088b055e)[uVar9] + 0x8a ^ (&DAT_088b054e)[uVar9 & 0xf];
        uVar9 = uVar9 + 1;
      } while (uVar9 != 0x18);
      DAT_0a3d9838 = 1;
    }
    if ((DAT_0a3d992e & 1) == 0) {
      DAT_0a3d9920._0_1_ = s_sending__xwechatSetSendS_088b02f0[0x10];
      DAT_0a3d9920._1_1_ = s_sending__xwechatSetSendS_088b02f0[0x11];
      DAT_0a3d9920._2_1_ = s_sending__xwechatSetSendS_088b02f0[0x12];
      DAT_0a3d9920._3_1_ = s_sending__xwechatSetSendS_088b02f0[0x13];
      DAT_0a3d9920._4_1_ = s_sending__xwechatSetSendS_088b02f0[0x14];
      DAT_0a3d9920._5_1_ = s_sending__xwechatSetSendS_088b02f0[0x15];
      DAT_0a3d9920._6_1_ = s_sending__xwechatSetSendS_088b02f0[0x16];
      DAT_0a3d9920._7_1_ = s_sending__xwechatSetSendS_088b02f0[0x17];
      DAT_0a3d9928 = (undefined4)ram0x084e31f0;
      DAT_0a3d992c = 0x65;
      DAT_0a3d992e = 1;
    }
    FUN_05e1d050(&local_2a0,4,ppppppuVar1,&DAT_0a3d9820,&DAT_0a3d9920,0xe1,0,0);
    if ((DAT_0a3d9954 & 1) == 0) {
      uVar9 = 0;
      do {
        (&DAT_0a3d992f)[uVar9] = (&DAT_088b06de)[uVar9] + 0x8a ^ (&DAT_088b06ce)[uVar9 & 0xf];
        uVar9 = uVar9 + 1;
      } while (uVar9 != 0x25);
      DAT_0a3d9954 = 1;
    }
    uStack_68 = 0;
    local_70 = 0;
    uStack_58 = 0;
    uStack_60 = 0;
    uStack_88 = 0;
    local_90 = 0;
    uStack_78 = 0;
    uStack_80 = 0;
    uStack_a8 = 0;
    local_b0 = 0;
    uStack_98 = 0;
    uStack_a0 = 0;
    ppuStack_c8 = (undefined1 **)0x0;
    local_d0 = (undefined8 ******)0x0;
    ppuStack_b8 = (undefined1 **)0x0;
    local_c0 = (undefined1 **)0x0;
    FUN_05e1d31c(&local_2a0,&DAT_0a3d992f,&local_d0);
LAB_030f2984:
    thunk_FUN_05e1d0bc(&local_2a0);
    if (cStack_109 < '\0') {
      __ZdlPvm(local_120,CONCAT17(cStack_109,local_110) & 0x7fffffffffffffff);
    }
  }
LAB_030f3158:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


