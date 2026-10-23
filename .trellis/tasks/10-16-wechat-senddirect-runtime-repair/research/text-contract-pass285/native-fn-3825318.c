// Ghidra inferred pseudocode; requested=0x3825318
// entry=03825318 end=038259bf

void FUN_03825318(long param_1)

{
  long *plVar1;
  long lVar2;
  int iVar3;
  ulong uVar4;
  undefined4 uVar5;
  ulong uVar6;
  undefined8 local_50;
  long *local_48;
  undefined8 local_40;
  long *local_38;
  long local_30;
  long *local_28;
  
  uVar4 = FUN_0474715c();
  uVar6 = *(ulong *)(param_1 + 0x40);
  if (uVar6 != 0 && uVar6 < uVar4) {
    iVar3 = FUN_037f7dec(*(undefined8 *)(param_1 + 0x20));
    uVar5 = 7;
    if (iVar3 == 0) {
      uVar5 = 0;
    }
    FUN_049801c8(uVar5,uVar4 - uVar6,2);
    *(undefined8 *)(param_1 + 0x40) = 0;
  }
  FUN_0466aca8(&local_50);
  FUN_01205740(&local_40,local_50);
  FUN_024089a8(&local_30,local_40);
  (**(code **)(*(long *)(local_30 + 0x20) + 0x10))
            ((long *)(local_30 + 0x20),*(undefined8 *)(param_1 + 0x98));
  plVar1 = local_28;
  if (local_28 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_28[1];
    local_28[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_28 + 0x10))(local_28);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = local_38;
  if (local_38 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_38[1];
    local_38[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_38 + 0x10))(local_38);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = local_48;
  if (local_48 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_48[1];
    local_48[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_48 + 0x10))(local_48);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  FUN_0466aca8(&local_50);
  FUN_01205740(&local_40,local_50);
  FUN_024089a8(&local_30,local_40);
  (**(code **)(*(long *)(local_30 + 0x110) + 0x10))
            (local_30 + 0x110,*(undefined8 *)(param_1 + 0xa0));
  plVar1 = local_28;
  if (local_28 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_28[1];
    local_28[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_28 + 0x10))(local_28);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = local_38;
  if (local_38 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_38[1];
    local_38[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_38 + 0x10))(local_38);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = local_48;
  if (local_48 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_48[1];
    local_48[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_48 + 0x10))(local_48);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  FUN_0466aca8(&local_50);
  FUN_01205740(&local_40,local_50);
  FUN_0268f370(&local_30,local_40);
  (**(code **)(*(long *)(local_30 + 0x228) + 0x10))
            (local_30 + 0x228,*(undefined8 *)(param_1 + 0xa8));
  plVar1 = local_28;
  if (local_28 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_28[1];
    local_28[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_28 + 0x10))(local_28);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = local_38;
  if (local_38 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_38[1];
    local_38[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_38 + 0x10))(local_38);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = local_48;
  if (local_48 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_48[1];
    local_48[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_48 + 0x10))(local_48);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  FUN_0466aca8(&local_50);
  FUN_01205740(&local_40,local_50);
  FUN_0268f370(&local_30,local_40);
  (**(code **)(*(long *)(local_30 + 0x2a0) + 0x10))
            (local_30 + 0x2a0,*(undefined8 *)(param_1 + 0xb0));
  plVar1 = local_28;
  if (local_28 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_28[1];
    local_28[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_28 + 0x10))(local_28);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = local_38;
  if (local_38 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_38[1];
    local_38[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_38 + 0x10))(local_38);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = local_48;
  if (local_48 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_48[1];
    local_48[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_48 + 0x10))(local_48);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  FUN_0466aca8(&local_50);
  FUN_01205740(&local_40,local_50);
  FUN_0268f370(&local_30,local_40);
  (**(code **)(*(long *)(local_30 + 0x408) + 0x10))
            (local_30 + 0x408,*(undefined8 *)(param_1 + 0xb8));
  plVar1 = local_28;
  if (local_28 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_28[1];
    local_28[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_28 + 0x10))(local_28);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = local_38;
  if (local_38 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_38[1];
    local_38[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_38 + 0x10))(local_38);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = local_48;
  if (local_48 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_48[1];
    local_48[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_48 + 0x10))(local_48);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  FUN_0466aca8(&local_50);
  FUN_01205740(&local_40,local_50);
  FUN_0268f370(&local_30,local_40);
  (**(code **)(*(long *)(local_30 + 0x318) + 0x10))
            (local_30 + 0x318,*(undefined8 *)(param_1 + 0xc0));
  plVar1 = local_28;
  if (local_28 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_28[1];
    local_28[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_28 + 0x10))(local_28);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = local_38;
  if (local_38 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_38[1];
    local_38[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_38 + 0x10))(local_38);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = local_48;
  if (local_48 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_48[1];
    local_48[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_48 + 0x10))(local_48);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  FUN_0466aca8(&local_50);
  FUN_01205740(&local_40,local_50);
  FUN_0230000c(&local_30,local_40);
  (**(code **)(*(long *)(local_30 + 0x20) + 0x10))
            ((long *)(local_30 + 0x20),*(undefined8 *)(param_1 + 200));
  plVar1 = local_28;
  if (local_28 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_28[1];
    local_28[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_28 + 0x10))(local_28);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = local_38;
  if (local_38 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_38[1];
    local_38[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_38 + 0x10))(local_38);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = local_48;
  if (local_48 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_48[1];
    local_48[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_48 + 0x10))(local_48);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  FUN_0466aca8(&local_50);
  FUN_01205740(&local_40,local_50);
  FUN_024089a8(&local_30,local_40);
  (**(code **)(*(long *)(local_30 + 0x548) + 0x10))
            (local_30 + 0x548,*(undefined8 *)(param_1 + 0xd0));
  if (local_28 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_28[1];
    local_28[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_28 + 0x10))(local_28);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_28);
    }
  }
  if (local_38 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_38[1];
    local_38[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_38 + 0x10))(local_38);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_38);
    }
  }
  if (local_48 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_48[1];
    local_48[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_48 + 0x10))(local_48);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_48);
    }
  }
  FUN_0668272c(param_1 + 0xd8);
  FUN_066823c4(param_1 + 0xd8);
  return;
}


