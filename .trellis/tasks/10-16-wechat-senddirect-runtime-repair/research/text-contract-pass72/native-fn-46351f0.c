// Ghidra inferred pseudocode; requested=0x46351f0
// entry=046351f0 end=04635387

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_046351f0(uint param_1)

{
  uint uVar1;
  ulong uVar2;
  int iVar3;
  undefined8 uVar4;
  uint uVar5;
  ulong uVar6;
  ulong uVar7;
  long *plVar8;
  ulong uVar9;
  undefined2 uVar10;
  undefined8 local_50;
  undefined8 uStack_48;
  undefined8 uStack_40;
  undefined8 uStack_38;
  undefined8 local_30;
  long local_28;
  ulong uVar11;
  
  local_28 = *(long *)PTR____stack_chk_guard_09b36c98;
  if (((DAT_0a45cd78 & 1) == 0) && (iVar3 = ___cxa_guard_acquire(&DAT_0a45cd78), iVar3 != 0)) {
    local_30 = 0x5728000003db;
    uStack_48 = _UNK_08a10cc8;
    local_50 = _DAT_08a10cc0;
    uStack_38 = _UNK_08a10cd8;
    uStack_40 = _DAT_08a10cd0;
    FUN_0168b310(&DAT_0a45cd50,&local_50,10);
    ___cxa_atexit(FUN_00deeae4,&DAT_0a45cd50,0);
    ___cxa_guard_release(&DAT_0a45cd78);
  }
  if (DAT_0a45cd58 != 0) {
    uVar6 = (ulong)param_1;
    uVar4 = CONCAT17(POPCOUNT((char)(DAT_0a45cd58 >> 0x38)),
                     CONCAT16(POPCOUNT((char)(DAT_0a45cd58 >> 0x30)),
                              CONCAT15(POPCOUNT((char)(DAT_0a45cd58 >> 0x28)),
                                       CONCAT14(POPCOUNT((char)(DAT_0a45cd58 >> 0x20)),
                                                CONCAT13(POPCOUNT((char)(DAT_0a45cd58 >> 0x18)),
                                                         CONCAT12(POPCOUNT((char)(DAT_0a45cd58 >>
                                                                                 0x10)),
                                                                  CONCAT11(POPCOUNT((char)(
                                                  DAT_0a45cd58 >> 8)),POPCOUNT((char)DAT_0a45cd58)))
                                                  )))));
    uVar10 = NEON_uaddlv(uVar4,1);
    uVar11 = CONCAT62((int6)((ulong)uVar4 >> 0x10),uVar10);
    uVar5 = (uint)DAT_0a45cd58;
    if ((uVar11 & 0xffffffff) < 2) {
      uVar7 = (ulong)(uVar5 - 1 & param_1);
    }
    else {
      uVar7 = uVar6;
      if (DAT_0a45cd58 <= uVar6) {
        uVar1 = 0;
        if (uVar5 != 0) {
          uVar1 = param_1 / uVar5;
        }
        uVar7 = (ulong)(param_1 - uVar1 * uVar5);
      }
    }
    plVar8 = *(long **)(DAT_0a45cd50 + uVar7 * 8);
    if ((plVar8 != (long *)0x0) && (plVar8 = (long *)*plVar8, plVar8 != (long *)0x0)) {
      do {
        uVar9 = plVar8[1];
        if (uVar9 == uVar6) {
          if (*(uint *)(plVar8 + 2) == param_1) {
            uVar4 = 1;
            goto LAB_046352d4;
          }
        }
        else {
          if ((uVar11 & 0xffffffff) < 2) {
            uVar9 = uVar9 & DAT_0a45cd58 - 1;
          }
          else if (DAT_0a45cd58 <= uVar9) {
            uVar2 = 0;
            if (DAT_0a45cd58 != 0) {
              uVar2 = uVar9 / DAT_0a45cd58;
            }
            uVar9 = uVar9 - uVar2 * DAT_0a45cd58;
          }
          if (uVar9 != uVar7) break;
        }
        plVar8 = (long *)*plVar8;
      } while (plVar8 != (long *)0x0);
    }
  }
  uVar4 = 0;
LAB_046352d4:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail(uVar4);
}


