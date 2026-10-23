// Ghidra inferred pseudocode; requested=0x268f370
// entry=0268f370 end=0268f4cf

void FUN_0268f370(undefined8 *param_1,undefined8 param_2)

{
  long *plVar1;
  undefined8 uVar2;
  long lVar3;
  undefined8 *puVar4;
  long *plVar5;
  undefined1 *local_70;
  long *local_68;
  undefined1 *local_60;
  undefined1 *puStack_58;
  undefined1 *local_50;
  long *plStack_48;
  undefined1 *puStack_40;
  undefined1 *local_38;
  undefined **local_28;
  
  local_28 = &PTR_FUN_09da2000;
  plStack_48 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  local_50 = &SUB_aaaaaaaaaaaaaaaa;
  local_38 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_40 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0454182c(&local_50,param_2,&local_28);
  local_60 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_58 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_06676adc(&local_60);
  if ((char)local_38 == '\x01') {
    FUN_066856fc(&local_50);
    puVar4 = (undefined8 *)FUN_021b3684(&local_50);
    uVar2 = *puVar4;
    plVar5 = (long *)puVar4[1];
    if (plVar5 == (long *)0x0) {
      *param_1 = uVar2;
      param_1[1] = 0;
      goto LAB_0268f47c;
    }
    plVar1 = plVar5 + 1;
    *plVar1 = *plVar1 + 1;
    *param_1 = uVar2;
    param_1[1] = plVar5;
    *plVar1 = *plVar1 + 1;
    LOAcquire();
    lVar3 = *plVar1;
    *plVar1 = lVar3 + -1;
    LORelease();
    if (lVar3 != 0) goto LAB_0268f47c;
    (**(code **)(*plVar5 + 0x10))(plVar5);
  }
  else {
    local_70 = &SUB_aaaaaaaaaaaaaaaa;
    local_68 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    FUN_04540bd8(&local_70,param_2,&local_28);
    plVar5 = local_68;
    *param_1 = local_70;
    param_1[1] = local_68;
    if (local_68 == (long *)0x0) goto LAB_0268f47c;
    local_68[1] = local_68[1] + 1;
    if (local_68 == (long *)0x0) goto LAB_0268f47c;
    LOAcquire();
    lVar3 = local_68[1];
    local_68[1] = lVar3 + -1;
    LORelease();
    if (lVar3 != 0) goto LAB_0268f47c;
    (**(code **)(*local_68 + 0x10))(local_68);
  }
  __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
LAB_0268f47c:
  FUN_06676b84(&local_60);
  plVar5 = plStack_48;
  if (((char)local_38 == '\x01') && (plStack_48 != (long *)0x0)) {
    LOAcquire();
    lVar3 = plStack_48[1];
    plStack_48[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*plStack_48 + 0x10))(plStack_48);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
    }
  }
  return;
}


