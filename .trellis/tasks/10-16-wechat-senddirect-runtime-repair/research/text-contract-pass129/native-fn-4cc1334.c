// Ghidra inferred pseudocode; requested=0x4cc1334
// entry=04cc1334 end=04cc13cb

void FUN_04cc1334(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
                 undefined8 param_5)

{
  undefined8 local_70 [2];
  undefined7 local_60;
  char cStack_59;
  undefined8 local_48;
  undefined7 local_38;
  char cStack_31;
  
  thunk_FUN_04d310bc(local_70,param_2);
  FUN_01129c84(param_1,local_70,param_3,param_4,param_5);
  if (cStack_31 < '\0') {
    __ZdlPvm(local_48,CONCAT17(cStack_31,local_38) & 0x7fffffffffffffff);
  }
  if (cStack_59 < '\0') {
    __ZdlPvm(local_70[0],CONCAT17(cStack_59,local_60) & 0x7fffffffffffffff);
  }
  return;
}


