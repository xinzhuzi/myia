// Ghidra inferred pseudocode; requested=0x6676adc
// entry=06676adc end=06676b83

long * FUN_06676adc(long *param_1)

{
  long *plVar1;
  long *plVar2;
  long lVar3;
  
  plVar2 = (long *)(*(code *)PTR___tlv_bootstrap_0a24de80)();
  plVar2 = (long *)*plVar2;
  if (plVar2 == (long *)0x0) {
    *param_1 = 0;
    param_1[1] = 0;
LAB_06676b54:
    lVar3 = *param_1;
    if (*(int *)(lVar3 + 0x288) != 3) {
      *(int *)(lVar3 + 0x3c8) = *(int *)(lVar3 + 0x3c8) + 1;
    }
    return param_1;
  }
  if (plVar2[1] != 0) {
    lVar3 = *plVar2;
    plVar2 = (long *)__ZNSt3__119__shared_weak_count4lockEv();
    if (plVar2 != (long *)0x0) {
      *param_1 = lVar3;
      param_1[1] = (long)plVar2;
      plVar1 = plVar2 + 1;
      *plVar1 = *plVar1 + 1;
      LOAcquire();
      lVar3 = *plVar1;
      *plVar1 = lVar3 + -1;
      LORelease();
      if (lVar3 == 0) {
        (**(code **)(*plVar2 + 0x10))();
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
      }
      goto LAB_06676b54;
    }
  }
                    /* WARNING: Subroutine does not return */
  FUN_00283500();
}


