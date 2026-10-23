// Ghidra inferred pseudocode; requested=0x4cbaf80
// entry=04cbaf80 end=04cbb027

undefined8 FUN_04cbaf80(void)

{
  int iVar1;
  undefined8 uVar2;
  undefined1 uStack_31;
  undefined1 **local_30;
  undefined1 *local_28;
  
  if (((DAT_0a4ad958 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_0a4ad958), iVar1 != 0)) {
    uVar2 = __Znwm(0x110);
    FUN_056f99d8();
    DAT_0a4ad950 = uVar2;
    ___cxa_guard_release(&DAT_0a4ad958);
  }
  if (DAT_0a4ad960 != -1) {
    local_28 = &uStack_31;
    local_30 = &local_28;
    __ZNSt3__111__call_onceERVmPvPFvS2_E(&DAT_0a4ad960,&local_30,FUN_04cc245c);
  }
  return DAT_0a4ad950;
}


