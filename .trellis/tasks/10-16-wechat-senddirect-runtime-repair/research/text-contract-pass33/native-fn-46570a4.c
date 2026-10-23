// Ghidra inferred pseudocode; requested=0x46570a4
// entry=046570a4 end=046570fb

void FUN_046570a4(undefined8 *param_1)

{
  long *plVar1;
  long lVar2;
  undefined8 uVar3;
  
  plVar1 = (long *)FUN_04669774();
  lVar2 = (**(code **)(*plVar1 + 0x10))();
  if (-1 < *(char *)(lVar2 + 0x7f)) {
    uVar3 = *(undefined8 *)(lVar2 + 0x68);
    param_1[1] = *(undefined8 *)(lVar2 + 0x70);
    *param_1 = uVar3;
    param_1[2] = *(undefined8 *)(lVar2 + 0x78);
    return;
  }
  FUN_00018d20(param_1,*(undefined8 *)(lVar2 + 0x68),*(undefined8 *)(lVar2 + 0x70));
  return;
}


