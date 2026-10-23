// Ghidra inferred pseudocode; requested=0x56caefc
// entry=056caefc end=056caf67

byte * FUN_056caefc(byte *param_1)

{
  byte bVar1;
  
  bVar1 = *param_1;
  if (bVar1 < 3) {
    if ((bVar1 == 1) || (bVar1 == 2)) {
      param_1[8] = 0;
      param_1[9] = 0;
      param_1[10] = 0;
      param_1[0xb] = 0;
      param_1[0xc] = 0;
      param_1[0xd] = 0;
      param_1[0xe] = 0;
      param_1[0xf] = 0;
    }
  }
  else if (bVar1 == 3) {
    FUN_0562fd84(param_1 + 8);
  }
  else if (bVar1 == 4) {
    thunk_FUN_056324e0(param_1 + 8);
  }
  return param_1;
}


