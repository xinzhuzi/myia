// Ghidra inferred pseudocode; requested=0x30f1d74
// entry=030f1d74 end=030f1eeb

void FUN_030f1d74(undefined8 *param_1,long param_2)

{
  long *plVar1;
  int iVar2;
  long lVar3;
  long lVar4;
  long *plVar5;
  undefined8 uVar6;
  undefined8 uVar7;
  
  if (*(long *)(param_2 + 0x18) == 0) {
    *(undefined1 *)((long)param_1 + 0x17) = 0;
    *(undefined1 *)param_1 = 0;
    return;
  }
  FUN_04cbd624();
  iVar2 = FUN_04bb4a4c();
  lVar3 = *(long *)(param_2 + 0x18);
  if (iVar2 != 0) {
    lVar4 = *(long *)(lVar3 + 0x230);
    plVar5 = *(long **)(lVar3 + 0x238);
    if (plVar5 == (long *)0x0) {
      if (lVar4 != 0) goto LAB_030f1e00;
    }
    else {
      plVar1 = plVar5 + 1;
      *plVar1 = *plVar1 + 1;
      if (lVar4 != 0) {
LAB_030f1e00:
        lVar3 = *(long *)(lVar4 + 0x98);
        plVar1 = *(long **)(lVar4 + 0xa0);
        if (plVar1 != (long *)0x0) {
          plVar1[1] = plVar1[1] + 1;
        }
        if (*(char *)(lVar3 + 0x8f) < '\0') {
          FUN_00018d20(param_1,*(undefined8 *)(lVar3 + 0x78),*(undefined8 *)(lVar3 + 0x80));
        }
        else {
          uVar7 = *(undefined8 *)(lVar3 + 0x80);
          uVar6 = *(undefined8 *)(lVar3 + 0x78);
          param_1[2] = *(undefined8 *)(lVar3 + 0x88);
          param_1[1] = uVar7;
          *param_1 = uVar6;
        }
        if (plVar1 != (long *)0x0) {
          LOAcquire();
          lVar3 = plVar1[1];
          plVar1[1] = lVar3 + -1;
          LORelease();
          if (lVar3 == 0) {
            (**(code **)(*plVar1 + 0x10))(plVar1);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
          }
        }
        if (plVar5 == (long *)0x0) {
          return;
        }
        LOAcquire();
        lVar3 = plVar5[1];
        plVar5[1] = lVar3 + -1;
        LORelease();
        if (lVar3 != 0) {
          return;
        }
        (**(code **)(*plVar5 + 0x10))(plVar5);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
        return;
      }
      LOAcquire();
      lVar3 = *plVar1;
      *plVar1 = lVar3 + -1;
      LORelease();
      if (lVar3 == 0) {
        (**(code **)(*plVar5 + 0x10))(plVar5);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
      }
    }
    lVar3 = *(long *)(param_2 + 0x18);
  }
  if (-1 < *(char *)(lVar3 + 0x47)) {
    uVar7 = *(undefined8 *)(lVar3 + 0x38);
    uVar6 = *(undefined8 *)(lVar3 + 0x30);
    param_1[2] = *(undefined8 *)(lVar3 + 0x40);
    param_1[1] = uVar7;
    *param_1 = uVar6;
    return;
  }
  FUN_00018d20(param_1,*(undefined8 *)(lVar3 + 0x30),*(undefined8 *)(lVar3 + 0x38));
  return;
}


