// Ghidra inferred pseudocode; requested=0x4657108
// entry=04657108 end=0465718b

void FUN_04657108(undefined8 param_1,undefined8 param_2,undefined8 param_3,int param_4,
                 undefined8 param_5,undefined8 param_6,undefined8 param_7)

{
  undefined1 local_38;
  undefined7 uStack_37;
  undefined7 local_28;
  char cStack_21;
  
  if (param_4 != 0) {
    FUN_05cf0e54(param_2,param_3,param_5,param_6,param_7);
    return;
  }
  cStack_21 = '\0';
  local_38 = 0;
  FUN_05cf0d44(param_2,param_3,param_5,param_6,param_7,&local_38);
  if (cStack_21 < '\0') {
    __ZdlPvm(CONCAT71(uStack_37,local_38),CONCAT17(cStack_21,local_28) & 0x7fffffffffffffff);
  }
  return;
}


