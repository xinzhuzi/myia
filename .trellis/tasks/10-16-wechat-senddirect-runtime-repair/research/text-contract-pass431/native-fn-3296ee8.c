// Ghidra inferred pseudocode; requested=0x3296ee8
// entry=03296ee8 end=03297093

long FUN_03296ee8(long param_1,long param_2)

{
  undefined8 uVar1;
  long *plVar2;
  long lVar3;
  long *plVar4;
  undefined1 auStack_90 [8];
  long local_88;
  long *plStack_80;
  long local_78;
  undefined **local_70;
  long local_68;
  long *plStack_60;
  long local_58;
  undefined **local_50;
  long local_48;
  long *plStack_40;
  long local_38;
  
  if (param_1 + 0x98 != param_2) {
    FUN_027052a4(param_1 + 0xa0,*(undefined8 *)(param_2 + 0x10),param_2 + 8);
  }
  FUN_0270583c(&local_50,param_2);
  local_50 = &PTR_FUN_09da63b0;
  uVar1 = FUN_056d63ac(param_1 + 0x58,&local_50);
  FUN_056cb938(auStack_90,*(undefined8 *)(param_2 + 0x18));
  FUN_02705c78(&local_70,auStack_90);
  local_70 = &PTR_FUN_09da5f48;
  FUN_056d6590(uVar1,&local_70);
  if (local_58 != 0) {
    plVar2 = *(long **)(local_68 + 8);
    lVar3 = *plStack_60;
    *(long **)(lVar3 + 8) = plVar2;
    *plVar2 = lVar3;
    local_58 = 0;
    plVar2 = plStack_60;
    while (plVar2 != &local_68) {
      plVar4 = (long *)plVar2[1];
      FUN_056cd5a8(plVar2 + 2);
      __ZdlPvm(plVar2,0x170);
      plVar2 = plVar4;
    }
  }
  if (local_78 != 0) {
    plVar2 = *(long **)(local_88 + 8);
    lVar3 = *plStack_80;
    *(long **)(lVar3 + 8) = plVar2;
    *plVar2 = lVar3;
    local_78 = 0;
    plVar2 = plStack_80;
    while (plVar2 != &local_88) {
      plVar4 = (long *)plVar2[1];
      FUN_056cb8d0(plVar2 + 2);
      __ZdlPvm(plVar2,0x60);
      plVar2 = plVar4;
    }
  }
  if (local_38 != 0) {
    plVar2 = *(long **)(local_48 + 8);
    lVar3 = *plStack_40;
    *(long **)(lVar3 + 8) = plVar2;
    *plVar2 = lVar3;
    local_38 = 0;
    plVar2 = plStack_40;
    while (plVar2 != &local_48) {
      plVar4 = (long *)plVar2[1];
      (**(code **)plVar2[2])();
      __ZdlPvm(plVar2,0x100);
      plVar2 = plVar4;
    }
  }
  return param_1;
}


