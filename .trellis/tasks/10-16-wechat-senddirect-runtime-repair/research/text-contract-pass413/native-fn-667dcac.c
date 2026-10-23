// Ghidra inferred pseudocode; requested=0x667dcac
// entry=0667dcac end=0667dd4f

void FUN_0667dcac(long param_1)

{
  long lVar1;
  long *plVar2;
  long lVar3;
  long lVar4;
  
  lVar3 = *(long *)(param_1 + 0x38);
  if (lVar3 != 0) {
    lVar4 = *(long *)(param_1 + 0x40);
    lVar1 = lVar3;
    if (lVar4 != lVar3) {
      do {
        plVar2 = *(long **)(lVar4 + -0x18);
        if (plVar2 != (long *)0x0) {
          LOAcquire();
          lVar1 = plVar2[1];
          plVar2[1] = lVar1 + -1;
          LORelease();
          if (lVar1 == 0) {
            (**(code **)(*plVar2 + 0x10))(plVar2);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
          }
        }
        lVar4 = lVar4 + -0x20;
      } while (lVar4 != lVar3);
      lVar1 = *(long *)(param_1 + 0x38);
    }
    *(long *)(param_1 + 0x40) = lVar3;
    __ZdlPvm(lVar1,*(long *)(param_1 + 0x48) - lVar1);
  }
  FUN_0005037c(param_1 + 0x20,*(undefined8 *)(param_1 + 0x28));
  return;
}


