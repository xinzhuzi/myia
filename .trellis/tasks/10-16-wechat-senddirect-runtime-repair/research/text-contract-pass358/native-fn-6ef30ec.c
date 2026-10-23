// Ghidra inferred pseudocode; requested=0x6ef30ec
// entry=06ef30ec end=06ef3173

ulong FUN_06ef30ec(undefined8 *param_1,undefined8 *param_2)

{
  int iVar1;
  ulong uVar2;
  long lVar3;
  undefined4 *puVar4;
  
  puVar4 = (undefined4 *)*param_1;
  if (puVar4 == &DAT_0a2320b0) {
    lVar3 = 0;
    puVar4 = (undefined4 *)*param_2;
    iVar1 = DAT_0a2320b4;
  }
  else {
    lVar3 = *(long *)(puVar4 + 4) + (long)puVar4;
    iVar1 = puVar4[1];
    puVar4 = (undefined4 *)*param_2;
  }
  if (puVar4 != &DAT_0a2320b0) {
    uVar2 = FUN_06eef64c((long)iVar1,lVar3,(long)(int)puVar4[1],*(long *)(puVar4 + 4) + (long)puVar4
                         ,1);
    return uVar2 >> 0x1f & 1;
  }
  uVar2 = FUN_06eef64c((long)iVar1,lVar3,(long)DAT_0a2320b4,0,1);
  return uVar2 >> 0x1f & 1;
}


