// Ghidra inferred pseudocode; requested=0x48a60b4
// entry=048a60b4 end=048a617b

bool FUN_048a60b4(long param_1)

{
  bool bVar1;
  long *plVar2;
  long lVar3;
  long *plVar4;
  
  lVar3 = *(long *)(param_1 + 0x228);
  plVar4 = *(long **)(param_1 + 0x230);
  if (plVar4 != (long *)0x0) {
    plVar4[1] = plVar4[1] + 1;
  }
  plVar2 = (long *)(lVar3 + 0x18);
  if (*(char *)(lVar3 + 0x2f) < '\0') {
    if (*(long *)(lVar3 + 0x20) == 0x10) {
      plVar2 = (long *)*plVar2;
      goto LAB_048a6100;
    }
  }
  else if (*(char *)(lVar3 + 0x2f) == '\x10') {
LAB_048a6100:
    bVar1 = *plVar2 == 0x65636e756f6e6e61 && plVar2[1] == 0x6c6c6140746e656d;
    goto joined_r0x048a613c;
  }
  bVar1 = false;
joined_r0x048a613c:
  if (plVar4 != (long *)0x0) {
    LOAcquire();
    lVar3 = plVar4[1];
    plVar4[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*plVar4 + 0x10))(plVar4);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    }
  }
  return bVar1;
}


