// Ghidra inferred pseudocode; requested=0x668e658
// entry=0668e658 end=0668e6bb

void FUN_0668e658(void)

{
  byte *pbVar1;
  long lVar2;
  
  pbVar1 = (byte *)(*(code *)PTR___tlv_bootstrap_0a24df70)();
  if ((*pbVar1 & 1) == 0) {
    FUN_07134108();
  }
  lVar2 = (*(code *)PTR___tlv_bootstrap_0a24df58)();
  if (-1 < *(char *)(lVar2 + 0x4f)) {
    *(undefined1 *)(lVar2 + 0x38) = 0;
    *(undefined1 *)(lVar2 + 0x4f) = 0;
    return;
  }
  **(undefined1 **)(lVar2 + 0x38) = 0;
  *(undefined8 *)(lVar2 + 0x40) = 0;
  return;
}


