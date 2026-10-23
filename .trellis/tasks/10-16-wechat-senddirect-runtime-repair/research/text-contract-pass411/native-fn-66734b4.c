// Ghidra inferred pseudocode; requested=0x66734b4
// entry=066734b4 end=066735af

long FUN_066734b4(void)

{
  undefined *puVar1;
  char *pcVar2;
  long *plVar3;
  long lVar4;
  undefined8 *puVar5;
  long *plVar6;
  
  puVar1 = PTR___tlv_bootstrap_0a24dee0;
  pcVar2 = (char *)(*(code *)PTR___tlv_bootstrap_0a24dee0)(&PTR___tlv_bootstrap_0a24dee0);
  if (*pcVar2 == '\0') {
    FUN_07133fc0();
  }
  plVar3 = (long *)(*(code *)PTR___tlv_bootstrap_0a24de68)();
  if (*plVar3 == 0) {
    pcVar2 = (char *)(*(code *)puVar1)(&PTR___tlv_bootstrap_0a24dee0);
    if (*pcVar2 == '\0') {
      FUN_07133fc0();
    }
    lVar4 = FUN_066703f8(0x80000,0);
    puVar5 = (undefined8 *)__Znwm(0x20);
    *puVar5 = &PTR___ZNSt3__119__shared_weak_countD2Ev_09fb26d0;
    puVar5[1] = 0;
    puVar5[2] = 0;
    puVar5[3] = lVar4;
    plVar6 = (long *)plVar3[1];
    *plVar3 = lVar4;
    plVar3[1] = (long)puVar5;
    if (plVar6 != (long *)0x0) {
      LOAcquire();
      lVar4 = plVar6[1];
      plVar6[1] = lVar4 + -1;
      LORelease();
      if (lVar4 == 0) {
        (**(code **)(*plVar6 + 0x10))(plVar6);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
      }
    }
  }
  pcVar2 = (char *)(*(code *)puVar1)(&PTR___tlv_bootstrap_0a24dee0);
  if (*pcVar2 == '\0') {
    FUN_07133fc0();
  }
  return *plVar3;
}


