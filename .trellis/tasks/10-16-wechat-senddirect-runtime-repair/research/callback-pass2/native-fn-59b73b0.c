// Ghidra inferred pseudocode; requested=0x59b73b0
// entry=059b73b0 end=059b7483

void FUN_059b73b0(long param_1)

{
  long lVar1;
  int iVar2;
  undefined8 local_278;
  long *local_270;
  char local_261;
  undefined8 local_260;
  char local_249;
  undefined1 auStack_248 [184];
  undefined1 auStack_190 [352];
  
  thunk_FUN_05daa3c8(auStack_248);
  FUN_05ced7ac(&local_278);
  iVar2 = FUN_011ac530(local_278);
  if (local_270 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_270[1];
    local_270[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_270 + 0x10))(local_270);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_270);
    }
  }
  if (iVar2 != 0) {
    FUN_05df7418(&local_278);
    FUN_059c5798(auStack_190,&local_278,&local_278);
    if (local_249 < '\0') {
      __ZdlPv(local_260);
    }
    if (local_261 < '\0') {
      __ZdlPv(local_278);
    }
  }
  FUN_05d5d3bc(*(undefined8 *)(param_1 + 0x68),auStack_248);
  FUN_046364ec(auStack_248);
  return;
}


