// Ghidra inferred pseudocode; requested=0x46710fc
// entry=046710fc end=046711d3

void FUN_046710fc(undefined8 param_1)

{
  int iVar1;
  undefined8 uVar2;
  undefined1 local_38;
  undefined7 uStack_37;
  undefined7 local_28;
  char cStack_21;
  
  cStack_21 = '\0';
  local_38 = 0;
  FUN_04668010(0,&local_38);
  if (cStack_21 < '\0') {
    __ZdlPvm(CONCAT71(uStack_37,local_38),CONCAT17(cStack_21,local_28) & 0x7fffffffffffffff);
  }
  FUN_04b6e820();
  uVar2 = __Znwm(0x308);
  FUN_04666b54(uVar2,param_1);
  DAT_0a45df38 = uVar2;
  FUN_04667350(uVar2);
  FUN_04671220(DAT_0a45df38);
  if (((DAT_0a05a718 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_0a05a718), iVar1 != 0)) {
    FUN_046774f0(&DAT_0a05a660);
    ___cxa_atexit(thunk_FUN_04677558,&DAT_0a05a660,0);
    ___cxa_guard_release(&DAT_0a05a718);
  }
  return;
}


