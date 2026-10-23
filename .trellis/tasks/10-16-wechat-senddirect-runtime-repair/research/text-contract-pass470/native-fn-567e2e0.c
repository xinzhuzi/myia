// Ghidra inferred pseudocode; requested=0x567e2e0
// entry=0567e2e0 end=0567e48b

void FUN_0567e2e0(long *param_1,undefined8 param_2,long *param_3)

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
  
  plVar3 = param_1 + 5;
  plVar4 = (long *)*plVar3;
  plVar5 = plVar3;
  if (plVar4 != (long *)0x0) {
    do {
      iVar2 = FUN_056311f0(param_1 + 6,plVar4 + 4,param_2);
      lVar1 = 8;
      if (iVar2 == 0) {
        lVar1 = 0;
        plVar5 = plVar4;
      }
      plVar4 = *(long **)((long)plVar4 + lVar1);
    } while (plVar4 != (long *)0x0);
    if ((plVar5 != plVar3) && (iVar2 = FUN_056311f0(param_1 + 6,param_2,plVar5 + 4), iVar2 == 0)) {
      return;
    }
  }
  local_60 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_58 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_68 = (long *)__Znwm(0x80);
  plVar5 = local_68 + 1;
  *plVar5 = 0;
  local_68[2] = 0;
  *local_68 = (long)&PTR_FUN_09f1b658;
  lVar1 = 0;
  if (*param_3 != 0) {
    lVar1 = *param_3 + 0x20;
  }
  local_70 = (long *)FUN_0567f0f4(local_68 + 3,lVar1);
  if (local_68 != (long *)0x0) {
    *plVar5 = *plVar5 + 1;
  }
  local_60 = local_70;
  local_58 = local_68;
  if ((*(byte *)(param_1 + 3) & 1) == 0) {
    FUN_0562a8f8(param_1,0xc);
    (**(code **)(*param_1 + 0x10))(param_1);
  }
  *(undefined1 *)(param_1 + 3) = 1;
  FUN_0564f544(param_1 + 4,param_2,&local_70);
  (**(code **)(*local_70 + 0x10))(local_70,param_1);
  (**(code **)(*param_1 + 0x18))(param_1);
  plVar5 = local_68;
  if (local_68 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_68[1];
    local_68[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_68 + 0x10))(local_68);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
    }
  }
  plVar5 = local_58;
  if (local_58 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_58[1];
    local_58[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_58 + 0x10))(local_58);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
    }
  }
  return;
}


