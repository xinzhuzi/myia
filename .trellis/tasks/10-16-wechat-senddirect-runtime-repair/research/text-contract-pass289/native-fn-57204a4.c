// Ghidra inferred pseudocode; requested=0x57204a4
// entry=057204a4 end=0572056b

void FUN_057204a4(undefined8 param_1,ulong param_2)

{
  long lVar1;
  long lVar2;
  long lVar3;
  uint uVar4;
  undefined8 uStack_38;
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar2 = FUN_0571fd94();
  if (lVar2 != 0) {
    uStack_38 = &SUB_aaaaaaaaaaaaaaaa;
    lVar1 = 0;
    do {
      lVar3 = lVar1;
      uVar4 = (uint)param_2;
      *(byte *)((long)&uStack_38 + lVar3 + 7) =
           (char)param_2 + (char)((param_2 & 0xffffffff) / 10) * -10 | 0x30;
      lVar1 = lVar3 + -1;
      param_2 = (param_2 & 0xffffffff) / 10;
    } while (9 < uVar4);
    *(undefined1 *)((long)&uStack_38 + lVar3 + 6) = 0x2d;
    FUN_0571cb24(lVar2 + 0x10,lVar2,0x10,(long)&uStack_38 + lVar3 + 7,-(lVar3 + -1));
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


