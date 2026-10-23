// Ghidra inferred pseudocode; requested=0x2fec684
// entry=02fec684 end=02fec7b3

void FUN_02fec684(long param_1)

{
  long lVar1;
  undefined1 uVar2;
  int iVar3;
  int iVar4;
  long *plVar5;
  undefined8 uVar6;
  long *local_40;
  long *local_38;
  
  iVar3 = __ZSt19uncaught_exceptionsv();
  if (*(long *)(param_1 + 0x10) != 0) {
    plVar5 = (long *)__ZNSt3__119__shared_weak_count4lockEv();
    local_38 = plVar5;
    if (plVar5 != (long *)0x0) {
      local_40 = *(long **)(param_1 + 8);
      if (local_40 == (long *)0x0) {
        uVar2 = 0;
      }
      else {
        uVar6 = FUN_04669774();
        uVar2 = FUN_046735dc(uVar6,param_1 + 0x18);
      }
      LOAcquire();
      lVar1 = plVar5[1];
      plVar5[1] = lVar1 + -1;
      LORelease();
      if (lVar1 == 0) {
        (**(code **)(*plVar5 + 0x10))(plVar5);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
      }
      goto LAB_02fec71c;
    }
  }
  uVar2 = 0;
LAB_02fec71c:
  local_40 = (long *)__Znwm(0x20);
  *local_40 = (long)&PTR_FUN_09d86378;
  *(undefined1 *)(local_40 + 1) = uVar2;
  local_40[2] = (long)PTR___ZTIb_09b36aa0;
  local_40[3] = (long)(local_40 + 1);
  FUN_066696dc(*(undefined8 *)(param_1 + 0x100),&local_40);
  if (local_40 != (long *)0x0) {
    (**(code **)(*local_40 + 8))();
  }
  iVar4 = __ZSt19uncaught_exceptionsv();
  if (iVar3 < iVar4) {
    local_40 = (long *)0x0;
    FUN_06669050(*(undefined8 *)(param_1 + 0x100),&local_40);
    if (local_40 != (long *)0x0) {
      (**(code **)(*local_40 + 8))();
    }
  }
  return;
}


