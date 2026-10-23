// Ghidra inferred pseudocode; requested=0x2b4b150
// entry=02b4b150 end=02b4b40b

/* WARNING: Removing unreachable block (ram,0x02b4b200) */
/* WARNING: Removing unreachable block (ram,0x02b4b230) */

void FUN_02b4b150(undefined8 *param_1,undefined8 param_2,undefined8 *param_3)

{
  long *plVar1;
  long lVar2;
  long *plVar3;
  undefined1 *local_460;
  long *local_458;
  long local_450;
  char local_80;
  undefined8 local_78;
  long *local_70;
  undefined1 *local_68;
  long *local_60;
  undefined1 uStack_51;
  undefined1 *local_50;
  long *plStack_48;
  undefined8 local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_68 = &SUB_aaaaaaaaaaaaaaaa;
  local_60 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  if (*(char *)((long)param_3 + 0x17) < '\0') {
    FUN_00018d20(&local_50,*param_3,param_3[1]);
  }
  else {
    plStack_48 = (long *)param_3[1];
    local_50 = (undefined1 *)*param_3;
    local_40 = param_3[2];
  }
  FUN_0029ae04(&local_460,&local_50,1);
  FUN_02b4b4b8(&local_68,param_2,&local_460);
  if (local_460 != (undefined1 *)0x0) {
    for (; local_458 != (long *)local_460; local_458 = (long *)((long)local_458 + -0x18)) {
    }
    local_458 = (long *)local_460;
    __ZdlPvm(local_460,local_450 - (long)local_460);
  }
  local_460 = local_68;
  local_458 = local_60;
  lVar2 = 0;
  if (local_60 != (long *)0x0) {
    lVar2 = local_60[1];
    local_60[1] = lVar2 + 1;
  }
  local_450 = 0;
  FUN_066856fc(lVar2,&local_460);
  plVar3 = (long *)FUN_029e74e8(&local_460);
  plVar1 = local_458;
  if (local_458 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_458[1];
    local_458[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_458 + 0x10))(local_458);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  if (((char)plVar3[3] == '\x01') && (*plVar3 != plVar3[1])) {
    local_78 = 0;
    local_70 = (long *)0x0;
    FUN_0233200c(&local_460);
    local_80 = '\x01';
    local_50 = &SUB_aaaaaaaaaaaaaaaa;
    plStack_48 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    FUN_021efaf0(&local_50,&uStack_51);
    FUN_02b56834(&local_50,&local_460);
  }
  else {
    local_78 = 0;
    local_70 = (long *)0x0;
    local_460 = (undefined1 *)((ulong)local_460 & 0xffffffffffffff00);
    local_80 = '\0';
    local_50 = &SUB_aaaaaaaaaaaaaaaa;
    plStack_48 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    FUN_021efaf0(&local_50,&uStack_51);
    FUN_02b56834(&local_50,&local_460);
  }
  plVar1 = plStack_48;
  *param_1 = local_50;
  param_1[1] = plStack_48;
  if ((plStack_48 != (long *)0x0) && (plStack_48[1] = plStack_48[1] + 1, plStack_48 != (long *)0x0))
  {
    LOAcquire();
    lVar2 = plStack_48[1];
    plStack_48[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*plStack_48 + 0x10))(plStack_48);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  if (local_80 == '\x01') {
    FUN_02331b88(&local_460);
  }
  plVar1 = local_70;
  if (local_70 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_70[1];
    local_70[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_70 + 0x10))(local_70);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  plVar1 = local_60;
  if (local_60 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_60[1];
    local_60[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_60 + 0x10))(local_60);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar1);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


