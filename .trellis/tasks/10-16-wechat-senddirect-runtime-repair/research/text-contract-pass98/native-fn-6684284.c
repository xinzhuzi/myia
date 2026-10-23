// Ghidra inferred pseudocode; requested=0x6684284
// entry=06684284 end=06684343

undefined8 FUN_06684284(void)

{
  long lVar1;
  int iVar2;
  undefined8 uVar3;
  undefined8 *puVar4;
  long local_30;
  long *plStack_28;
  
  FUN_06673848(&local_30);
  if (plStack_28 != (long *)0x0) {
    LOAcquire();
    lVar1 = plStack_28[1];
    plStack_28[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*plStack_28 + 0x10))(plStack_28);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plStack_28);
    }
  }
  if (local_30 == 0) {
    puVar4 = (undefined8 *)(*(code *)PTR___tlv_bootstrap_0a24def8)();
    uVar3 = *puVar4;
  }
  else {
    if (((DAT_0a518858 & 1) == 0) && (iVar2 = ___cxa_guard_acquire(&DAT_0a518858), iVar2 != 0)) {
      DAT_0a518850 = FUN_06675760(0);
      ___cxa_guard_release(&DAT_0a518858);
    }
    uVar3 = FUN_06675ec4(DAT_0a518850);
  }
  return uVar3;
}


