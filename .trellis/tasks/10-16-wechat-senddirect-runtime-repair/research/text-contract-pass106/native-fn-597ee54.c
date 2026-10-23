// Ghidra inferred pseudocode; requested=0x597ee54
// entry=0597ee54 end=0597eef7

void FUN_0597ee54(long param_1,undefined8 param_2)

{
  undefined1 auStack_140 [264];
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  thunk_FUN_05e1d500(auStack_140,1,"mars::mmext","MMStopTask","mmstn_manager.cc","MMStopTask",0x4b6,
                     0);
  if (*(long *)(param_1 + 0x20) != 0) {
    FUN_05d5f2cc(*(long *)(param_1 + 0x20),param_2);
  }
  thunk_FUN_05e1d684(auStack_140);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


