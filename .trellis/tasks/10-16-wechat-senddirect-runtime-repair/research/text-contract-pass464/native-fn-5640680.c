// Ghidra inferred pseudocode; requested=0x5640680
// entry=05640680 end=05640817

void FUN_05640680(long *param_1,undefined8 param_2,undefined8 param_3)

{
  long lVar1;
  int iVar2;
  long *plVar3;
  long *plVar4;
  long *plVar5;
  long *local_70;
  long *local_68;
  long *local_60;
  long *local_58;
  
  plVar4 = param_1 + 5;
  plVar5 = (long *)*plVar4;
  plVar3 = plVar4;
  if (plVar5 != (long *)0x0) {
    do {
      iVar2 = FUN_056311f0(param_1 + 6,plVar5 + 4,param_2);
      lVar1 = 8;
      if (iVar2 == 0) {
        lVar1 = 0;
        plVar3 = plVar5;
      }
      plVar5 = *(long **)((long)plVar5 + lVar1);
    } while (plVar5 != (long *)0x0);
    if ((plVar3 != plVar4) && (iVar2 = FUN_056311f0(param_1 + 6,param_2,plVar3 + 4), iVar2 == 0)) {
      return;
    }
  }
  plVar3 = (long *)__Znwm(0x48);
  plVar4 = plVar3 + 1;
  *plVar4 = 0;
  plVar3[2] = 0;
  *plVar3 = (long)&PTR_FUN_09f18698;
  local_70 = (long *)FUN_0564e844(plVar3 + 3,param_3);
  if (plVar3 != (long *)0x0) {
    *plVar4 = *plVar4 + 1;
  }
  local_68 = plVar3;
  local_60 = local_70;
  local_58 = plVar3;
  if ((*(byte *)(param_1 + 3) & 1) == 0) {
    FUN_0562a8f8(param_1,6);
    (**(code **)(*param_1 + 0x10))(param_1);
  }
  *(undefined1 *)(param_1 + 3) = 1;
  FUN_05643cd8(param_1 + 4,param_2,&local_70);
  (**(code **)(*local_70 + 0x10))(local_70,param_1);
  (**(code **)(*param_1 + 0x18))(param_1);
  plVar3 = local_68;
  if (local_68 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_68[1];
    local_68[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_68 + 0x10))(local_68);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  plVar3 = local_58;
  if (local_58 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_58[1];
    local_58[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_58 + 0x10))(local_58);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  return;
}


