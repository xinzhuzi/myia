// Ghidra inferred pseudocode; requested=0x5626f58
// entry=05626f58 end=05626fab

long FUN_05626f58(long param_1)

{
  undefined8 *puVar1;
  ulong uVar2;
  undefined8 local_30;
  undefined8 uStack_28;
  
  puVar1 = (undefined8 *)FUN_05632420();
  *puVar1 = &PTR_thunk_FUN_056324e0_09f17148;
  uVar2 = FUN_05632ba4();
  if ((uVar2 & 1) == 0) {
    local_30 = 0;
    uStack_28 = 0;
    FUN_05626ae8(param_1,*(undefined8 *)(param_1 + 8),*(undefined8 *)(param_1 + 0x10),&local_30);
  }
  return param_1;
}


