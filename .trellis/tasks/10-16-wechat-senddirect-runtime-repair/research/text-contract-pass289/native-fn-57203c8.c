// Ghidra inferred pseudocode; requested=0x57203c8
// entry=057203c8 end=057204a3

void FUN_057203c8(undefined8 param_1,uint param_2)

{
  undefined1 *puVar1;
  long lVar2;
  long lVar3;
  long lVar4;
  uint uVar5;
  ulong uVar6;
  undefined8 uStack_38;
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar3 = FUN_0571fd94();
  if (lVar3 != 0) {
    uStack_38 = &SUB_aaaaaaaaaaaaaaaa;
    uVar5 = -param_2;
    if (-1 < (int)param_2) {
      uVar5 = param_2;
    }
    lVar2 = 0;
    uVar6 = (ulong)uVar5;
    do {
      lVar4 = lVar2;
      uVar5 = (uint)uVar6;
      *(byte *)((long)&uStack_38 + lVar4 + 7) = (char)uVar6 + (char)(uVar6 / 10) * -10 | 0x30;
      lVar2 = lVar4 + -1;
      uVar6 = uVar6 / 10;
    } while (9 < uVar5);
    puVar1 = (undefined1 *)((long)&uStack_38 + lVar4 + 6);
    *puVar1 = 0x2d;
    FUN_0571cb24(lVar3 + 0x10,lVar3,0x10,puVar1 + (~param_2 >> 0x1f),
                 1 - ((ulong)(~param_2 >> 0x1f) + lVar4 + -1));
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


