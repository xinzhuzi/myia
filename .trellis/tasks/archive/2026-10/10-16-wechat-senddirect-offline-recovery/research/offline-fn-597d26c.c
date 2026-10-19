// Ghidra inferred pseudocode; requested=0x597d26c
// entry=0597d26c end=0597d417

undefined8
FUN_0597d26c(long param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
            undefined8 param_5,undefined8 param_6,undefined8 param_7,undefined4 param_8,
            undefined8 param_9,undefined2 param_10,long param_11)

{
  int iVar1;
  undefined8 uVar2;
  undefined1 auStack_178 [264];
  long local_70;
  
  local_70 = *(long *)PTR____stack_chk_guard_09b36c98;
  if ((*(long *)(param_1 + 0x10) == 0) && (iVar1 = thunk_FUN_05e1d97c(5), iVar1 != 0)) {
    FUN_05e1d050(auStack_178,5,"mars::mmext","mmstn_manager.cc","MMReq2Buf",0x312,0,0);
    FUN_05e1d244(auStack_178,"mmcallback_ != NULL");
    thunk_FUN_05e1d0bc(auStack_178);
  }
  thunk_FUN_05e1d500(auStack_178,1,"mars::mmext","MMReq2Buf","mmstn_manager.cc","MMReq2Buf",0x313,0)
  ;
  if (*(char *)(param_11 + 0x1c0) == '\x01') {
    uVar2 = FUN_0597d418(*(undefined8 *)(param_1 + 8));
    uVar2 = FUN_05cc1d14(uVar2,param_2,param_3,param_4,param_5,param_6,param_7,param_8,param_9,
                         param_10,param_11);
  }
  else {
    uVar2 = (**(code **)(**(long **)(param_1 + 0x10) + 0x50))
                      (*(long **)(param_1 + 0x10),param_2,param_3,param_4,param_5,param_6,param_7,
                       param_8,param_9,param_10);
  }
  thunk_FUN_05e1d684(auStack_178);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_70) {
    return uVar2;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


