// Ghidra inferred pseudocode; requested=0x11c2a60
// entry=011c2a60 end=011c2b33

void FUN_011c2a60(long param_1)

{
  undefined1 auStack_a0 [8];
  undefined8 local_98;
  undefined7 local_88;
  char cStack_81;
  undefined8 local_80;
  undefined7 local_70;
  char cStack_69;
  undefined8 local_68;
  undefined7 local_58;
  char cStack_51;
  undefined8 local_50;
  undefined7 local_40;
  char cStack_39;
  undefined8 local_38;
  undefined7 local_28;
  char cStack_21;
  
  FUN_011c2bc8(auStack_a0);
  FUN_011bad90(*(undefined8 *)(param_1 + 8),auStack_a0);
  if (cStack_21 < '\0') {
    __ZdlPvm(local_38,CONCAT17(cStack_21,local_28) & 0x7fffffffffffffff);
  }
  if (cStack_39 < '\0') {
    __ZdlPvm(local_50,CONCAT17(cStack_39,local_40) & 0x7fffffffffffffff);
  }
  if (cStack_51 < '\0') {
    __ZdlPvm(local_68,CONCAT17(cStack_51,local_58) & 0x7fffffffffffffff);
  }
  if (cStack_69 < '\0') {
    __ZdlPvm(local_80,CONCAT17(cStack_69,local_70) & 0x7fffffffffffffff);
  }
  if (cStack_81 < '\0') {
    __ZdlPvm(local_98,CONCAT17(cStack_81,local_88) & 0x7fffffffffffffff);
  }
  return;
}


