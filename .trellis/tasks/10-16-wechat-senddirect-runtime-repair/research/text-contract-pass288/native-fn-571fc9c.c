// Ghidra inferred pseudocode; requested=0x571fc9c
// entry=0571fc9c end=0571fd8f

void FUN_0571fc9c(long *param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
                 uint param_5,undefined8 param_6)

{
  long lVar1;
  undefined **local_2878;
  undefined8 uStack_2870;
  undefined8 local_2868;
  undefined1 auStack_2860 [10240];
  undefined ***local_60;
  undefined8 local_58;
  uint local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_2878 = &PTR_FUN_09f249f0;
  local_2868 = 0;
  lVar1 = *param_1;
  uStack_2870 = param_2;
  if (lVar1 != 0) {
    _memset(auStack_2860,0xaa,0x2818);
    local_60 = &local_2878;
    local_58 = 0;
    if ((param_5 < 9) && ((0x191U >> (ulong)(param_5 & 0x1f) & 1) != 0)) {
      param_5 = *(uint *)(&DAT_08b37c60 + (ulong)param_5 * 4);
    }
    local_50 = param_5;
    FUN_0571f83c(auStack_2860,lVar1,param_3,param_4,param_6);
    FUN_05723894(auStack_2860,auStack_2860,local_58);
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


