// Ghidra inferred pseudocode; requested=0x9ebf8
// entry=0009ebf8 end=0009ecc7

int FUN_0009ebf8(ushort *param_1,uint param_2)

{
  uint uVar1;
  int iVar2;
  uint uVar3;
  
  iVar2 = 0;
  if ((param_1 != (ushort *)0x0) && (0 < (int)param_2)) {
    uVar1 = param_2 & 3;
    if (3 < param_2) {
      uVar3 = (param_2 >> 2) + 1;
      do {
        param_2 = ((uint)*(byte *)((long)param_1 + 3) << 0x13 | (uint)(byte)param_1[1] << 0xb) ^
                  (*param_1 + param_2) * 0x10000 ^ *param_1 + param_2;
        param_1 = param_1 + 2;
        param_2 = param_2 + (param_2 >> 0xb);
        uVar3 = uVar3 - 1;
      } while (1 < uVar3);
    }
    if (uVar1 < 2) {
      if (uVar1 != 0) {
        param_2 = param_2 + (int)(char)*param_1;
        param_2 = param_2 ^ param_2 * 0x400;
        param_2 = param_2 + (param_2 >> 1);
      }
    }
    else if (uVar1 == 2) {
      param_2 = *param_1 + param_2 ^ (*param_1 + param_2) * 0x800;
      param_2 = param_2 + (param_2 >> 0x11);
    }
    else {
      param_2 = (int)(char)param_1[1] << 0x12 ^ (*param_1 + param_2) * 0x10000 ^ *param_1 + param_2;
      param_2 = param_2 + (param_2 >> 0xb);
    }
    param_2 = param_2 ^ param_2 << 3;
    param_2 = param_2 + (param_2 >> 5);
    param_2 = param_2 ^ param_2 * 0x10;
    param_2 = param_2 + (param_2 >> 0x11);
    param_2 = param_2 ^ param_2 * 0x2000000;
    iVar2 = param_2 + (param_2 >> 6);
  }
  return iVar2;
}


