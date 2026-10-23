// Ghidra inferred pseudocode; requested=0x56cb048
// entry=056cb048 end=056cb127

byte * FUN_056cb048(byte *param_1,byte *param_2)

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
  bVar1 = *param_2;
  *param_1 = bVar1;
  if (bVar1 < 3) {
    if (bVar1 == 1) {
      *(undefined8 *)(param_1 + 8) = *(undefined8 *)(param_2 + 8);
    }
    else if (bVar1 == 2) {
      *(undefined8 *)(param_1 + 8) = *(undefined8 *)(param_2 + 8);
    }
  }
  else if (bVar1 == 3) {
    FUN_0562fd60(param_1 + 8,param_2 + 8);
  }
  else if (bVar1 == 4) {
    FUN_05632378(param_1 + 8,param_2 + 8);
    *(undefined ***)(param_1 + 8) = &PTR_thunk_FUN_056324e0_09f17148;
  }
  return param_1;
}


