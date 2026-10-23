// Ghidra inferred pseudocode; requested=0x33677c4
// entry=033677c4 end=03367903

void FUN_033677c4(long param_1)

{
  undefined4 uVar1;
  long *plVar2;
  long lVar3;
  int iVar4;
  undefined8 uVar5;
  undefined8 local_550;
  long *local_548;
  undefined8 local_540;
  long *plStack_538;
  undefined1 local_528 [632];
  char local_2b0;
  undefined1 auStack_2a8 [632];
  
  uVar1 = *(undefined4 *)(param_1 + 0x40);
  plStack_538 = *(long **)(param_1 + 0x50);
  uVar5 = *(undefined8 *)(param_1 + 0x48);
  *(undefined8 *)(param_1 + 0x48) = 0;
  *(undefined8 *)(param_1 + 0x50) = 0;
  local_550 = *(undefined8 *)(param_1 + 0x58);
  local_548 = *(long **)(param_1 + 0x60);
  if (local_548 != (long *)0x0) {
    local_548[1] = local_548[1] + 1;
  }
  local_540 = uVar5;
  _bzero(auStack_2a8,0x278);
  FUN_00ac6038(auStack_2a8);
  iVar4 = FUN_03273830(uVar5,auStack_2a8,param_1 + 0x28,uVar1,1);
  if (iVar4 == 0) {
    local_528[0] = 0;
    local_2b0 = '\0';
    FUN_0335fdd8(&local_550,local_528);
  }
  else {
    FUN_02a0cf30(local_528,auStack_2a8);
    local_2b0 = '\x01';
    FUN_0335fdd8(&local_550,local_528);
  }
  if (local_2b0 == '\x01') {
    FUN_00ac6290(local_528);
  }
  FUN_00ac6290(auStack_2a8);
  plVar2 = local_548;
  if (local_548 != (long *)0x0) {
    LOAcquire();
    lVar3 = local_548[1];
    local_548[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*local_548 + 0x10))(local_548);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  plVar2 = plStack_538;
  if (plStack_538 != (long *)0x0) {
    LOAcquire();
    lVar3 = plStack_538[1];
    plStack_538[1] = lVar3 + -1;
    LORelease();
    if (lVar3 == 0) {
      (**(code **)(*plStack_538 + 0x10))(plStack_538);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
    }
  }
  return;
}


