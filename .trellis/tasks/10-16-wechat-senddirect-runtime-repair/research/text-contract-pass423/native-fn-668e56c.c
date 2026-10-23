// Ghidra inferred pseudocode; requested=0x668e56c
// entry=0668e56c end=0668e5cf

void FUN_0668e56c(void)

{
  byte *pbVar1;
  long lVar2;
  
  pbVar1 = (byte *)(*(code *)PTR___tlv_bootstrap_0a24df40)();
  if ((*pbVar1 & 1) == 0) {
    FUN_071340b4();
  }
  lVar2 = (*(code *)PTR___tlv_bootstrap_0a24df28)();
  if (-1 < *(char *)(lVar2 + 0x4f)) {
    *(undefined1 *)(lVar2 + 0x38) = 0;
    *(undefined1 *)(lVar2 + 0x4f) = 0;
    return;
  }
  **(undefined1 **)(lVar2 + 0x38) = 0;
  *(undefined8 *)(lVar2 + 0x40) = 0;
  return;
}


