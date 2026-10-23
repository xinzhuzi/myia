// Ghidra inferred pseudocode; requested=0x66859ec
// entry=066859ec end=06685a4b

void FUN_066859ec(void)

{
  long lVar1;
  undefined1 auStack_38 [8];
  long *local_30;
  
  FUN_06674c94(auStack_38);
  FUN_066856fc(auStack_38);
  if (local_30 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_30[1];
    local_30[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_30 + 0x10))(local_30);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_30);
    }
  }
  return;
}


