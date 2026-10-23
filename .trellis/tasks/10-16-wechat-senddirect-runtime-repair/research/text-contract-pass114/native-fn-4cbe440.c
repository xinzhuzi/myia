// Ghidra inferred pseudocode; requested=0x4cbe440
// entry=04cbe440 end=04cbe4b7

void FUN_04cbe440(undefined8 param_1,undefined8 param_2)

{
  undefined8 local_60 [2];
  undefined7 local_50;
  char cStack_49;
  undefined8 local_38;
  undefined7 local_28;
  char cStack_21;
  
  thunk_FUN_04d310bc(local_60,param_2);
  FUN_008ad29c(param_1,local_60);
  if (cStack_21 < '\0') {
    __ZdlPvm(local_38,CONCAT17(cStack_21,local_28) & 0x7fffffffffffffff);
  }
  if (cStack_49 < '\0') {
    __ZdlPvm(local_60[0],CONCAT17(cStack_49,local_50) & 0x7fffffffffffffff);
  }
  return;
}


