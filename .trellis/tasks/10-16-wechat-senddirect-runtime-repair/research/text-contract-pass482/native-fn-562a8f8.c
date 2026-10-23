// Ghidra inferred pseudocode; requested=0x562a8f8
// entry=0562a8f8 end=0562a92b

void FUN_0562a8f8(long param_1,size_t param_2)

{
  void *pvVar1;
  
  pvVar1 = _calloc(param_2,0x28);
  *(void **)(param_1 + 8) = pvVar1;
  *(void **)(param_1 + 0x10) = (void *)((long)pvVar1 + param_2 * 0x20);
  return;
}


