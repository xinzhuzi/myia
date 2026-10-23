// Ghidra inferred pseudocode; requested=0x4cc12a0
// entry=04cc12a0 end=04cc131f

void FUN_04cc12a0(undefined8 param_1,undefined8 param_2,undefined8 param_3)

{
  undefined8 local_60 [2];
  undefined7 local_50;
  char cStack_49;
  undefined8 local_38;
  undefined7 local_28;
  char cStack_21;
  
  thunk_FUN_04d310bc(local_60,param_2);
  FUN_0112a590(param_1,local_60,param_3);
  if (cStack_21 < '\0') {
    __ZdlPvm(local_38,CONCAT17(cStack_21,local_28) & 0x7fffffffffffffff);
  }
  if (cStack_49 < '\0') {
    __ZdlPvm(local_60[0],CONCAT17(cStack_49,local_50) & 0x7fffffffffffffff);
  }
  return;
}


