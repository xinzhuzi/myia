// Ghidra inferred pseudocode; requested=0x5973a80
// entry=05973a80 end=05973bbb

void FUN_05973a80(undefined8 param_1)

{
  int iVar1;
  long lVar2;
  undefined8 local_1d0 [2];
  char local_1b9;
  undefined1 auStack_140 [264];
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  thunk_FUN_05e1d500(auStack_140,1,"mars::mmext","MMStopTask","mmstn_logic.cc","MMStopTask",0x126,0)
  ;
  FUN_05941fe8(local_1d0,"default");
  FUN_0594199c(local_1d0);
  lVar2 = FUN_0594c390();
  if (local_1b9 < '\0') {
    __ZdlPv(local_1d0[0]);
  }
  if (lVar2 == 0) {
    iVar1 = thunk_FUN_05e1d97c(5);
    if (iVar1 != 0) {
      FUN_05e1d050(local_1d0,5,"mars::mmext","mmstn_logic.cc","MMStopTask",0x128,0,0);
      lVar2 = FUN_05e1d244(local_1d0,"NULL != mmstn_manager");
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKc
                (lVar2 + 0x58,"mars2 mmstn_manager is empty.");
      thunk_FUN_05e1d0bc(local_1d0);
    }
  }
  else {
    FUN_0597ee54(lVar2,param_1);
  }
  thunk_FUN_05e1d684(auStack_140);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


