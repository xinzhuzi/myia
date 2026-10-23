// Ghidra inferred pseudocode; requested=0x6685cf0
// entry=06685cf0 end=06685f8f

void FUN_06685cf0(long param_1)

{
  long *plVar1;
  code *pcVar2;
  bool bVar3;
  long *plVar4;
  long lVar5;
  ulong uVar6;
  long *plVar7;
  long *plVar8;
  long *plVar9;
  ulong uVar10;
  ulong uVar11;
  long lVar12;
  long *plVar13;
  ulong uVar14;
  long *plVar15;
  long lVar16;
  long lVar17;
  long lVar18;
  long lVar19;
  long lVar20;
  long lVar21;
  long *local_68;
  long *local_60;
  long *local_58;
  
  local_68 = (long *)0x0;
  local_60 = (long *)0x0;
  local_58 = (long *)0x0;
  __ZNSt3__15mutex4lockEv();
  uVar14 = *(ulong *)(param_1 + 0x50);
  if (uVar14 == 0) {
    plVar4 = (long *)0x0;
  }
  else {
    if (uVar14 >> 0x3d != 0) {
      FUN_06686994(&local_68);
LAB_06685f8c:
                    /* WARNING: Does not return */
      pcVar2 = (code *)SoftwareBreakpoint(1,0x6685f90);
      (*pcVar2)();
    }
    plVar4 = (long *)__Znwm(uVar14 << 3);
    local_58 = plVar4 + uVar14;
    local_68 = plVar4;
    local_60 = plVar4;
  }
  plVar15 = *(long **)(param_1 + 0x40);
  plVar1 = plVar4;
  do {
    if (plVar15 == (long *)(param_1 + 0x48)) {
      FUN_0004fa1c(param_1 + 0x40,*(undefined8 *)(param_1 + 0x48));
      *(undefined8 *)(param_1 + 0x48) = 0;
      *(undefined8 *)(param_1 + 0x50) = 0;
      *(long **)(param_1 + 0x40) = (long *)(param_1 + 0x48);
      __ZNSt3__15mutex6unlockEv(param_1);
      plVar15 = plVar1;
      for (; plVar1 != plVar4; plVar1 = plVar1 + 1) {
        (**(code **)(*(long *)*plVar1 + 0x10))((long *)*plVar1,*(undefined8 *)(param_1 + 0x58));
        plVar15 = local_68;
      }
      if (plVar15 != (long *)0x0) {
        __ZdlPvm(plVar15,(long)local_58 - (long)plVar15);
        return;
      }
      return;
    }
    if (plVar4 < local_58) {
      plVar13 = plVar4 + 1;
      *plVar4 = plVar15[4];
      plVar7 = local_68;
      plVar4 = local_58;
    }
    else {
      lVar16 = (long)plVar4 - (long)local_68;
      lVar12 = lVar16 >> 3;
      uVar14 = lVar12 + 1;
      if (uVar14 >> 0x3d != 0) {
        FUN_06686994(&local_68);
        goto LAB_06685f8c;
      }
      uVar6 = (long)local_58 - (long)local_68 >> 2;
      if (uVar6 <= uVar14) {
        uVar6 = uVar14;
      }
      if (0x7ffffffffffffff7 < (ulong)((long)local_58 - (long)local_68)) {
        uVar6 = 0x1fffffffffffffff;
      }
      if (uVar6 == 0) {
        lVar5 = 0;
      }
      else {
        if (uVar6 >> 0x3d != 0) {
                    /* WARNING: Subroutine does not return */
          FUN_001e96c0();
        }
        lVar5 = __Znwm(uVar6 << 3);
      }
      plVar1 = local_68;
      plVar4 = (long *)(lVar5 + lVar12 * 8);
      plVar13 = plVar4 + 1;
      *plVar4 = plVar15[4];
      plVar7 = plVar4;
      if ((long)local_60 - (long)local_68 != 0) {
        uVar14 = ((long)local_60 - (long)local_68) - 8;
        plVar9 = local_60;
        if ((0x37 < uVar14) && (0x3f < (ulong)((long)local_60 + (-lVar16 - lVar5)))) {
          uVar14 = (uVar14 >> 3) + 1;
          uVar10 = uVar14 & 0x3ffffffffffffff8;
          plVar9 = local_60 + -uVar10;
          plVar7 = plVar4 + -uVar10;
          plVar8 = local_60 + -4;
          plVar4 = plVar4 + -4;
          uVar11 = uVar10;
          do {
            lVar17 = *plVar8;
            lVar16 = plVar8[3];
            lVar12 = plVar8[2];
            lVar21 = plVar8[-3];
            lVar20 = plVar8[-4];
            lVar19 = plVar8[-1];
            lVar18 = plVar8[-2];
            plVar4[1] = plVar8[1];
            *plVar4 = lVar17;
            plVar4[3] = lVar16;
            plVar4[2] = lVar12;
            plVar4[-3] = lVar21;
            plVar4[-4] = lVar20;
            plVar4[-1] = lVar19;
            plVar4[-2] = lVar18;
            plVar8 = plVar8 + -8;
            plVar4 = plVar4 + -8;
            uVar11 = uVar11 - 8;
          } while (uVar11 != 0);
          if (uVar14 == uVar10) goto LAB_06685e80;
        }
        do {
          plVar9 = plVar9 + -1;
          plVar7 = plVar7 + -1;
          *plVar7 = *plVar9;
        } while (plVar9 != local_68);
      }
LAB_06685e80:
      plVar4 = (long *)(lVar5 + uVar6 * 8);
      if (local_68 != (long *)0x0) {
        lVar12 = (long)local_58 - (long)local_68;
        local_68 = plVar7;
        local_58 = plVar4;
        __ZdlPvm(plVar1,lVar12);
        plVar7 = local_68;
        plVar4 = local_58;
      }
    }
    local_58 = plVar4;
    local_68 = plVar7;
    plVar7 = (long *)plVar15[1];
    plVar9 = plVar15;
    local_60 = plVar13;
    plVar4 = plVar13;
    plVar1 = local_68;
    if ((long *)plVar15[1] == (long *)0x0) {
      do {
        plVar15 = (long *)plVar9[2];
        bVar3 = (long *)*plVar15 != plVar9;
        plVar9 = plVar15;
      } while (bVar3);
    }
    else {
      do {
        plVar15 = plVar7;
        plVar7 = (long *)*plVar15;
      } while ((long *)*plVar15 != (long *)0x0);
    }
  } while( true );
}


