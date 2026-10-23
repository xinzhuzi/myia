// Ghidra inferred pseudocode; requested=0x668dad0
// entry=0668dad0 end=0668db5b

bool FUN_0668dad0(int param_1)

{
  uint *puVar1;
  int extraout_w8;
  undefined1 uStack_31;
  undefined1 **local_30;
  undefined1 *local_28;
  
  if (DAT_0a518cb8 != -1) {
    local_28 = &uStack_31;
    local_30 = &local_28;
    __ZNSt3__111__call_onceERVmPvPFvS2_E(&DAT_0a518cb8,&local_30,FUN_0669440c);
  }
  puVar1 = (uint *)(*(code *)PTR___tlv_bootstrap_0a24df10)(*DAT_0a518cb0);
  return (*puVar1 & 1) == 0 && extraout_w8 <= param_1;
}


