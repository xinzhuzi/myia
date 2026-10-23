// Ghidra inferred pseudocode; requested=0x5975054
// entry=05975054 end=05975123

void FUN_05975054(undefined8 param_1)

{
  int iVar1;
  long lVar2;
  undefined8 local_b0 [2];
  char local_99;
  
  FUN_05941fe8(local_b0,"default");
  FUN_0594199c(local_b0);
  lVar2 = FUN_0594c390();
  if (local_99 < '\0') {
    __ZdlPv(local_b0[0]);
  }
  if (lVar2 == 0) {
    iVar1 = thunk_FUN_05e1d97c(5);
    if (iVar1 != 0) {
      FUN_05e1d050(local_b0,5,"mars::mmext","mmstn_logic.cc","SetMMCallback",0x1dd,0,0);
      lVar2 = FUN_05e1d244(local_b0,"NULL != mmstn_manager");
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE6appendEPKc
                (lVar2 + 0x58,"mars2 mmstn_manager is empty.");
      thunk_FUN_05e1d0bc(local_b0);
    }
  }
  else {
    FUN_009d3cf0(lVar2,param_1);
  }
  return;
}


