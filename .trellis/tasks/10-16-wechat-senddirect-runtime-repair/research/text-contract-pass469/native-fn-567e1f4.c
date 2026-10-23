// Ghidra inferred pseudocode; requested=0x567e1f4
// entry=0567e1f4 end=0567e2df

long FUN_0567e1f4(undefined8 param_1,undefined8 param_2)

{
  long lVar1;
  int iVar2;
  long lVar3;
  ulong uVar4;
  long lVar5;
  long lVar6;
  undefined8 local_58;
  
  lVar3 = FUN_05697ec8();
  lVar5 = *(long *)(lVar3 + 0x1a8);
  if (lVar5 != 0) {
    lVar6 = lVar3 + 0x1a8;
    do {
      iVar2 = FUN_056311f0(lVar3 + 0x1b0,lVar5 + 0x20,&DAT_0a524570);
      lVar1 = 8;
      if (iVar2 == 0) {
        lVar1 = 0;
        lVar6 = lVar5;
      }
      lVar5 = *(long *)(lVar5 + lVar1);
    } while (lVar5 != 0);
    if ((lVar6 != lVar3 + 0x1a8) &&
       (iVar2 = FUN_056311f0(lVar3 + 0x1b0,&DAT_0a524570,lVar6 + 0x20), iVar2 == 0)) {
      return lVar3;
    }
  }
  uVar4 = FUN_0562fedc(param_2,&DAT_0a524570);
  if (((uVar4 & 1) == 0) && (uVar4 = FUN_0562fedc(param_2,&DAT_0a524558), (uVar4 & 1) == 0)) {
    local_58 = param_1;
    FUN_0567e2e0(lVar3 + 0x180,&DAT_0a524570,&local_58);
  }
  return lVar3;
}


