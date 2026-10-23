// Ghidra inferred pseudocode; requested=0x597eda0
// entry=0597eda0 end=0597ee53

bool FUN_0597eda0(long param_1,undefined8 param_2)

{
  long lVar1;
  undefined1 auStack_140 [264];
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  thunk_FUN_05e1d500(auStack_140,1,"mars::mmext","MMStartTask","mmstn_manager.cc","MMStartTask",
                     0x4ad,0);
  lVar1 = *(long *)(param_1 + 0x18);
  if (lVar1 != 0) {
    FUN_059b73b0(lVar1,param_2);
  }
  thunk_FUN_05e1d684(auStack_140);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return lVar1 != 0;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


