// Ghidra inferred pseudocode; requested=0x335bfac
// entry=0335bfac end=0335c0b7

void FUN_0335bfac(long param_1,long param_2)

{
  undefined8 uVar1;
  long *plVar2;
  long lVar3;
  undefined1 uVar4;
  undefined8 uVar5;
  undefined8 uVar6;
  long *plVar7;
  long *local_38;
  
  uVar5 = *(undefined8 *)(param_2 + 0x28);
  plVar7 = *(long **)(param_2 + 0x50);
  uVar6 = *(undefined8 *)(param_2 + 0x48);
  *(undefined8 *)(param_2 + 0x48) = 0;
  *(undefined8 *)(param_2 + 0x50) = 0;
  uVar1 = *(undefined8 *)(param_2 + 0x58);
  plVar2 = *(long **)(param_2 + 0x60);
  if (plVar2 != (long *)0x0) {
    param_1 = plVar2[1];
    plVar2[1] = param_1 + 1;
  }
  uVar4 = FUN_03274034(param_1,uVar6,param_2 + 0x30,uVar5);
  local_38 = (long *)__Znwm(0x20);
  *(undefined1 *)(local_38 + 1) = uVar4;
  *local_38 = (long)&PTR_FUN_09d86378;
  local_38[2] = (long)PTR___ZTIb_09b36aa0;
  local_38[3] = (long)(local_38 + 1);
  FUN_066696dc(uVar1,&local_38);
  if (local_38 != (long *)0x0) {
    (**(code **)(*local_38 + 8))();
  }
  if (plVar2 != (long *)0x0) {
    LOAcquire();
    lVar3 = plVar2[1];
    plVar2[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*plVar2 + 0x10))(plVar2);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  if (plVar7 != (long *)0x0) {
    LOAcquire();
    lVar3 = plVar7[1];
    plVar7[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*plVar7 + 0x10))(plVar7);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
    }
  }
  return;
}


