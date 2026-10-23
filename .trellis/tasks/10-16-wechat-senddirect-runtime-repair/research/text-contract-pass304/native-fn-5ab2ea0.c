// Ghidra inferred pseudocode; requested=0x5ab2ea0
// entry=05ab2ea0 end=05ab2f8f

/* WARNING: Removing unreachable block (ram,0x05ab2f7c) */
/* WARNING: Removing unreachable block (ram,0x05ab2f8c) */

undefined8 FUN_05ab2ea0(long param_1,uint *param_2)

{
  byte *pbVar1;
  undefined8 uVar2;
  uint uVar3;
  byte *pbVar4;
  uint local_28 [2];
  
  pbVar1 = *(byte **)(param_1 + 8);
  if (((int)*(byte **)(param_1 + 0x10) - (int)pbVar1 < 10) && (*(byte **)(param_1 + 0x10) <= pbVar1)
     ) {
    uVar2 = FUN_05ab2d58(param_1,local_28);
    if ((int)uVar2 != 0) {
      *param_2 = local_28[0];
    }
  }
  else {
    pbVar4 = pbVar1 + 1;
    uVar3 = *pbVar1 & 0x7f;
    if ((char)*pbVar1 < '\0') {
      uVar3 = uVar3 | ((int)(char)pbVar1[1] & 0x7fU) << 7;
      if ((char)pbVar1[1] < 0) {
        uVar3 = uVar3 | ((int)(char)pbVar1[2] & 0x7fU) << 0xe;
        if ((char)pbVar1[2] < 0) {
          uVar3 = uVar3 | ((int)(char)pbVar1[3] & 0x7fU) << 0x15;
          if ((char)pbVar1[3] < 0) {
            uVar3 = uVar3 | (int)(char)pbVar1[4] << 0x1c;
            if ((char)pbVar1[4] < 0) {
              pbVar4 = pbVar1 + 6;
            }
            else {
              pbVar4 = pbVar1 + 5;
            }
          }
          else {
            pbVar4 = pbVar1 + 4;
          }
        }
        else {
          pbVar4 = pbVar1 + 3;
        }
      }
      else {
        pbVar4 = pbVar1 + 2;
      }
    }
    *param_2 = uVar3;
    *(byte **)(param_1 + 8) = pbVar4;
    uVar2 = 1;
  }
  return uVar2;
}


