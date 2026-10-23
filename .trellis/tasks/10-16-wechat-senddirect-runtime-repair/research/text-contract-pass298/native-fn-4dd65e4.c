// Ghidra inferred pseudocode; requested=0x4dd65e4
// entry=04dd65e4 end=04dd668b

undefined8 FUN_04dd65e4(void)

{
  int iVar1;
  undefined8 uVar2;
  undefined1 uStack_31;
  undefined1 **local_30;
  undefined1 *local_28;
  
  if (((DAT_0a4b6d40 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_0a4b6d40), iVar1 != 0)) {
    uVar2 = __Znwm(0x110);
    FUN_056f99d8();
    DAT_0a4b6d38 = uVar2;
    ___cxa_guard_release(&DAT_0a4b6d40);
  }
  if (DAT_0a4b6d48 != -1) {
    local_28 = &uStack_31;
    local_30 = &local_28;
    __ZNSt3__111__call_onceERVmPvPFvS2_E(&DAT_0a4b6d48,&local_30,FUN_04dd67a0);
  }
  return DAT_0a4b6d38;
}


