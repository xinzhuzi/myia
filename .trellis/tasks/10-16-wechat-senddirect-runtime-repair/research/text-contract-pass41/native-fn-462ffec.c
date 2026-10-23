// Ghidra inferred pseudocode; requested=0x462ffec
// entry=0462ffec end=046308a7

/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0462ffec(long *param_1,ulong param_2)

{
  ulong uVar1;
  undefined8 *******pppppppuVar2;
  undefined1 uVar3;
  undefined8 uVar4;
  long *plVar5;
  code *pcVar6;
  bool bVar7;
  int iVar8;
  long lVar9;
  uint uVar10;
  uint *******pppppppuVar11;
  undefined1 *puVar12;
  ulong uVar13;
  uint *******pppppppuVar14;
  uint *puVar15;
  undefined1 *puVar16;
  undefined1 *puVar17;
  ulong uVar18;
  ulong uVar19;
  uint *******pppppppuVar20;
  uint *******pppppppuVar21;
  ulong uVar22;
  uint *******pppppppuVar23;
  long *plVar24;
  long *plVar25;
  long lVar26;
  uint ******ppppppuVar27;
  uint ******ppppppuVar28;
  uint ******ppppppuVar29;
  uint ******ppppppuVar30;
  uint ******ppppppuVar31;
  uint ******ppppppuVar32;
  uint ******ppppppuVar33;
  undefined8 local_220;
  undefined8 uStack_218;
  undefined8 uStack_210;
  undefined8 uStack_208;
  undefined8 local_200;
  undefined8 uStack_1f8;
  undefined8 uStack_1f0;
  undefined8 uStack_1e8;
  undefined8 local_1e0;
  undefined8 uStack_1d8;
  undefined8 uStack_1d0;
  undefined8 uStack_1c8;
  undefined8 local_1c0;
  undefined8 uStack_1b8;
  undefined8 uStack_1b0;
  undefined4 uStack_1a8;
  undefined4 local_1a4;
  undefined4 uStack_1a0;
  undefined8 uStack_19c;
  undefined8 local_190;
  undefined8 uStack_188;
  ulong local_180;
  undefined8 *******local_178 [2];
  undefined7 local_168;
  char cStack_161;
  uint *******local_160;
  uint *******local_158;
  uint *******local_150;
  undefined1 *local_148;
  undefined1 local_140 [8];
  undefined7 local_138;
  char cStack_131;
  undefined1 **local_f8;
  undefined8 local_f0;
  undefined8 uStack_e8;
  undefined8 local_e0;
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
  long local_78;
  
  local_78 = *(long *)PTR____stack_chk_guard_09b36c98;
  iVar8 = thunk_FUN_05e1d97c(2);
  if (iVar8 != 0) {
    FUN_0488143c(&local_160);
    pppppppuVar14 = local_160;
    if (-1 < (long)local_150) {
      pppppppuVar14 = (uint *******)&local_160;
    }
    if ((DAT_0a45cea6 & 1) == 0) {
      uVar13 = 0;
      do {
        (&DAT_0a45ce91)[uVar13] = (&DAT_08a10f2b)[uVar13] + 0x8a ^ (&DAT_08a10f1b)[uVar13 & 0xf];
        uVar13 = uVar13 + 1;
      } while (uVar13 != 0x15);
      DAT_0a45cea6 = 1;
    }
    if ((DAT_0a45cec7 & 1) == 0) {
      DAT_0a45cec0 = (undefined4)ram0x08595a58;
      DAT_0a45cec4 = 0x6e69;
      DAT_0a45cec6 = 0;
      DAT_0a45cec7 = 1;
    }
    FUN_05e1d050(&local_220,2,pppppppuVar14,&DAT_0a45ce91,&DAT_0a45cec0,0xb6,0,0);
    local_148 = local_140;
    if ((DAT_0a45d389 & 1) == 0) {
      uVar13 = 0;
      do {
        (&DAT_0a45d341)[uVar13] = (&DAT_08a116aa)[uVar13] + 0x8a ^ (&DAT_08a1169a)[uVar13 & 0xf];
        uVar13 = uVar13 + 1;
      } while (uVar13 != 0x48);
      DAT_0a45d389 = 1;
    }
    lVar26 = 0;
    uVar13 = param_2;
    do {
      lVar9 = lVar26;
      local_140[lVar9] = (&DAT_0a45d364)[uVar13 % 10];
      bVar7 = 9 < uVar13;
      lVar26 = lVar9 + 1;
      uVar13 = uVar13 / 10;
    } while (bVar7);
    local_140[lVar9 + 1] = 0;
    if (8 < lVar9 + 8U) {
      puVar17 = local_140;
      puVar12 = local_140 + lVar9;
      do {
        puVar17 = puVar17 + 1;
        uVar3 = *puVar12;
        puVar16 = puVar12 + -1;
        *puVar12 = puVar17[-1];
        puVar17[-1] = uVar3;
        puVar12 = puVar16;
      } while (puVar17 < puVar16);
    }
    if ((DAT_0a45cede & 1) == 0) {
      uVar13 = 0;
      do {
        (&DAT_0a45cec8)[uVar13] = (&DAT_08a10fa1)[uVar13] + 0x8a ^ (&DAT_08a10f91)[uVar13 & 0xf];
        uVar13 = uVar13 + 1;
      } while (uVar13 != 0x16);
      DAT_0a45cede = 1;
    }
    uStack_e8 = 0;
    local_f0 = 0;
    local_f8 = &local_148;
    uStack_d8 = 0;
    local_e0 = 0;
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
    local_80 = 0;
    FUN_05e1d31c(&local_220,&DAT_0a45cec8,&local_f8);
    thunk_FUN_05e1d0bc(&local_220);
    if ((long)local_150 < 0) {
      __ZdlPvm(local_160,(ulong)local_150 & 0x7fffffffffffffff);
    }
  }
  FUN_05cf09f0(param_2);
  FUN_05cf0afc(0);
  if (param_2 == 0) {
    (*(code *)PTR_FUN_0a124bb0)();
    (*(code *)PTR_FUN_0a124bb8)();
    __ZNSt3__15mutex4lockEv(param_1 + 0x10);
    local_160 = (uint *******)0x0;
    local_158 = (uint *******)0x0;
    local_150 = (uint *******)0x0;
    uVar13 = param_1[0xf];
    if (uVar13 != 0) {
      if (uVar13 >> 0x3e != 0) {
        FUN_00801dbc(&local_160);
LAB_046308a4:
                    /* WARNING: Does not return */
        pcVar6 = (code *)SoftwareBreakpoint(1,0x46308a8);
        (*pcVar6)();
      }
      local_158 = (uint *******)__Znwm(uVar13 << 2);
      local_150 = (uint *******)((long)local_158 + uVar13 * 4);
    }
    plVar24 = (long *)param_1[0xd];
    pppppppuVar14 = local_158;
    pppppppuVar23 = local_158;
    while (local_160 = pppppppuVar23, local_158 = pppppppuVar14, plVar24 != param_1 + 0xe) {
      if (pppppppuVar14 < local_150) {
        pppppppuVar21 = (uint *******)((long)pppppppuVar14 + 4);
        *(uint *)pppppppuVar14 = *(uint *)(plVar24 + 4);
      }
      else {
        lVar26 = (long)pppppppuVar14 - (long)pppppppuVar23;
        uVar13 = (lVar26 >> 2) + 1;
        if (uVar13 >> 0x3e != 0) {
          FUN_00801dbc(&local_160);
          goto LAB_046308a4;
        }
        uVar22 = (long)local_150 - (long)pppppppuVar23;
        uVar1 = (long)uVar22 >> 1;
        if ((ulong)((long)uVar22 >> 1) <= uVar13) {
          uVar1 = uVar13;
        }
        if (0x7ffffffffffffffb < uVar22) {
          uVar1 = 0x3fffffffffffffff;
        }
        if (uVar1 == 0) {
          lVar9 = 0;
        }
        else {
          if (uVar1 >> 0x3e != 0) {
                    /* WARNING: Subroutine does not return */
            FUN_001e96c0();
          }
          lVar9 = __Znwm(uVar1 << 2);
        }
        pppppppuVar11 = (uint *******)(lVar9 + (lVar26 >> 2) * 4);
        pppppppuVar21 = (uint *******)((long)pppppppuVar11 + 4);
        *(uint *)pppppppuVar11 = *(uint *)(plVar24 + 4);
        local_160 = pppppppuVar11;
        if ((long)pppppppuVar14 - (long)pppppppuVar23 != 0) {
          uVar13 = ((long)pppppppuVar14 - (long)pppppppuVar23) - 4;
          if (0x9b < uVar13) {
            puVar15 = (uint *)((long)pppppppuVar14 + -4);
            uVar18 = (long)puVar15 - (long)pppppppuVar23 & 0xfffffffffffffffc;
            uVar19 = (lVar9 + lVar26) - 4;
            if (((uVar19 - uVar18 <= uVar19) && ((uint *)((long)puVar15 - uVar18) <= puVar15)) &&
               (0x3f < (ulong)((long)pppppppuVar14 + (-lVar26 - lVar9)))) {
              uVar13 = (uVar13 >> 2) + 1;
              uVar19 = uVar13 & 0x7ffffffffffffff0;
              local_160 = (uint *******)((long)pppppppuVar11 + uVar19 * -4);
              pppppppuVar20 = pppppppuVar14 + -4;
              pppppppuVar11 = pppppppuVar11 + -4;
              uVar18 = uVar19;
              do {
                ppppppuVar29 = *pppppppuVar20;
                ppppppuVar28 = pppppppuVar20[3];
                ppppppuVar27 = pppppppuVar20[2];
                ppppppuVar33 = pppppppuVar20[-3];
                ppppppuVar32 = pppppppuVar20[-4];
                ppppppuVar31 = pppppppuVar20[-1];
                ppppppuVar30 = pppppppuVar20[-2];
                pppppppuVar11[1] = pppppppuVar20[1];
                *pppppppuVar11 = ppppppuVar29;
                pppppppuVar11[3] = ppppppuVar28;
                pppppppuVar11[2] = ppppppuVar27;
                pppppppuVar11[-3] = ppppppuVar33;
                pppppppuVar11[-4] = ppppppuVar32;
                pppppppuVar11[-1] = ppppppuVar31;
                pppppppuVar11[-2] = ppppppuVar30;
                pppppppuVar20 = pppppppuVar20 + -8;
                pppppppuVar11 = pppppppuVar11 + -8;
                uVar18 = uVar18 - 0x10;
              } while (uVar18 != 0);
              pppppppuVar11 = local_160;
              pppppppuVar14 = (uint *******)((long)pppppppuVar14 + uVar19 * -4);
              if (uVar13 == uVar19) goto LAB_046303e4;
            }
          }
          do {
            pppppppuVar14 = (uint *******)((long)pppppppuVar14 + -4);
            local_160 = (uint *******)((long)pppppppuVar11 + -4);
            *(uint *)local_160 = *(uint *)pppppppuVar14;
            pppppppuVar11 = local_160;
          } while (pppppppuVar14 != pppppppuVar23);
        }
LAB_046303e4:
        local_150 = (uint *******)(lVar9 + uVar1 * 4);
        if (pppppppuVar23 != (uint *******)0x0) {
          local_158 = pppppppuVar21;
          __ZdlPvm(pppppppuVar23,uVar22);
        }
      }
      plVar5 = (long *)plVar24[1];
      plVar25 = plVar24;
      pppppppuVar14 = pppppppuVar21;
      pppppppuVar23 = local_160;
      if ((long *)plVar24[1] == (long *)0x0) {
        do {
          plVar24 = (long *)plVar25[2];
          bVar7 = (long *)*plVar24 != plVar25;
          plVar25 = plVar24;
        } while (bVar7);
      }
      else {
        do {
          plVar24 = plVar5;
          plVar5 = (long *)*plVar24;
        } while ((long *)*plVar24 != (long *)0x0);
      }
    }
    __ZNSt3__15mutex6unlockEv(param_1 + 0x10);
    pppppppuVar14 = local_158;
    uVar4 = ram0x08595a58;
    if (local_160 != local_158) {
      pppppppuVar23 = local_160;
      do {
        iVar8 = thunk_FUN_05e1d97c(2);
        if (iVar8 != 0) {
          FUN_0488143c(local_178);
          pppppppuVar2 = local_178[0];
          if (-1 < cStack_161) {
            pppppppuVar2 = local_178;
          }
          if ((DAT_0a45cea6 & 1) == 0) {
            uVar13 = 0;
            do {
              (&DAT_0a45ce91)[uVar13] =
                   (&DAT_08a10f2b)[uVar13] + 0x8a ^ (&DAT_08a10f1b)[uVar13 & 0xf];
              uVar13 = uVar13 + 1;
            } while (uVar13 != 0x15);
            DAT_0a45cea6 = 1;
          }
          if ((DAT_0a45cec7 & 1) == 0) {
            DAT_0a45cec0 = (undefined4)uVar4;
            DAT_0a45cec4 = 0x6e69;
            DAT_0a45cec6 = 0;
            DAT_0a45cec7 = 1;
          }
          FUN_05e1d050(&local_220,2,pppppppuVar2,&DAT_0a45ce91,&DAT_0a45cec0,0xcd,0,0);
          uVar10 = *(uint *)pppppppuVar23;
          if ((DAT_0a45d389 & 1) == 0) {
            uVar13 = 0;
            do {
              (&DAT_0a45d341)[uVar13] =
                   (&DAT_08a116aa)[uVar13] + 0x8a ^ (&DAT_08a1169a)[uVar13 & 0xf];
              uVar13 = uVar13 + 1;
            } while (uVar13 != 0x48);
            DAT_0a45d389 = 1;
          }
          uVar13 = (ulong)uVar10;
          lVar26 = 0;
          do {
            lVar9 = lVar26;
            uVar10 = (uint)uVar13;
            local_140[lVar9] = (&DAT_0a45d341)[uVar10 + (int)(uVar13 / 10) * -10 + 0x23];
            uVar13 = uVar13 / 10;
            lVar26 = lVar9 + 1;
          } while (9 < uVar10);
          local_140[lVar9 + 1] = 0;
          if (8 < lVar9 + 8U) {
            puVar12 = local_140 + lVar9;
            puVar17 = local_140;
            do {
              puVar17 = puVar17 + 1;
              uVar3 = *puVar12;
              puVar16 = puVar12 + -1;
              *puVar12 = puVar17[-1];
              puVar17[-1] = uVar3;
              puVar12 = puVar16;
            } while (puVar17 < puVar16);
          }
          if ((DAT_0a45cef2 & 1) == 0) {
            uVar13 = 0;
            do {
              (&DAT_0a45cedf)[uVar13] =
                   (&DAT_08a10fc7)[uVar13] + 0x8a ^ (&DAT_08a10fb7)[uVar13 & 0xf];
              uVar13 = uVar13 + 1;
            } while (uVar13 != 0x13);
            DAT_0a45cef2 = 1;
          }
          uStack_e8 = 0;
          local_f0 = 0;
          uStack_d8 = 0;
          local_e0 = 0;
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
          local_80 = 0;
          local_148 = local_140;
          local_f8 = &local_148;
          FUN_05e1d31c(&local_220,&DAT_0a45cedf,&local_f8);
          thunk_FUN_05e1d0bc(&local_220);
          if (cStack_161 < '\0') {
            __ZdlPvm(local_178[0],CONCAT17(cStack_161,local_168) & 0x7fffffffffffffff);
          }
        }
        uVar10 = *(uint *)pppppppuVar23;
        cStack_131 = '\0';
        local_148 = (undefined1 *)((ulong)local_148 & 0xffffffffffffff00);
        local_190 = 0;
        uStack_188 = 0;
        local_180 = 0;
        uStack_218 = 0;
        local_220 = 0;
        uStack_208 = 0;
        uStack_210 = 0;
        uStack_1f8 = 0;
        local_200 = 0;
        uStack_1e8 = 0;
        uStack_1f0 = 0;
        uStack_1d8 = 0;
        local_1e0 = 0;
        uStack_1c8 = 0;
        uStack_1d0 = 0;
        uStack_1b8 = 0;
        local_1c0 = 0;
        uStack_1a8 = 0;
        uStack_1b0 = 0;
        uStack_19c = 0;
        local_1a4 = 0;
        uStack_1a0 = 0;
        FUN_05ded178(&local_f8,0x80);
        (**(code **)(*param_1 + 0x10))
                  (param_1,uVar10,0,&local_148,0,0xfffffff9,&local_220,&local_f8);
        FUN_05ded188(&local_f8);
        if ((long)local_180 < 0) {
          __ZdlPvm(local_190,local_180 & 0x7fffffffffffffff);
        }
        if (cStack_131 < '\0') {
          __ZdlPvm(local_148,CONCAT17(cStack_131,local_138) & 0x7fffffffffffffff);
        }
        pppppppuVar23 = (uint *******)((long)pppppppuVar23 + 4);
      } while (pppppppuVar23 != pppppppuVar14);
    }
    if (*(int *)((long)param_1 + 0xc4) != 0) {
      FUN_04630978(param_1);
    }
    if (local_160 != (uint *******)0x0) {
      local_158 = local_160;
      __ZdlPvm(local_160,(long)local_150 - (long)local_160);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_78) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


