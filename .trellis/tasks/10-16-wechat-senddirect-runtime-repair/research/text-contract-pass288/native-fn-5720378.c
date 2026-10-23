// Ghidra inferred pseudocode; requested=0x5720378
// entry=05720378 end=057203c7

void FUN_05720378(undefined8 param_1,char *param_2)

{
  long lVar1;
  size_t sVar2;
  
  lVar1 = FUN_0571fd94();
  if (lVar1 != 0) {
    sVar2 = _strlen(param_2);
    FUN_0571cb24(lVar1 + 0x10,lVar1,0x10,param_2,sVar2);
    return;
  }
  return;
}


