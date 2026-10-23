// Ghidra inferred pseudocode; requested=0x56c2744
// entry=056c2744 end=056c279f

void FUN_056c2744(undefined8 param_1,long param_2)

{
  long lVar1;
  undefined8 *puVar2;
  long lVar3;
  
  puVar2 = (undefined8 *)FUN_056c1e78();
  *puVar2 = &PTR_FUN_09f1f2a0;
  lVar3 = *(long *)(param_2 + 0x28);
  lVar1 = *(long *)(param_2 + 0x30);
  puVar2[5] = lVar3;
  puVar2[6] = lVar1;
  if (lVar1 != 0) {
    *(long *)(lVar1 + 8) = *(long *)(lVar1 + 8) + 1;
    lVar3 = *(long *)(param_2 + 0x28);
  }
  *(bool *)(puVar2 + 7) = lVar3 == 0;
  if (lVar3 != 0) {
    *(undefined1 *)(param_2 + 0x38) = 0;
  }
  return;
}


