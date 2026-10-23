// Ghidra inferred pseudocode; requested=0x305d770
// entry=0305d770 end=0305d9ab

void FUN_0305d770(undefined8 *param_1,long *param_2)

{
  undefined8 uVar1;
  undefined8 uVar2;
  long *plVar3;
  long lVar4;
  long lVar5;
  long *plVar6;
  ulong uVar7;
  code *pcVar8;
  long *plVar9;
  long *plVar10;
  long alStack_a8 [3];
  long *local_90;
  undefined **local_88;
  undefined8 uStack_80;
  ulong local_78;
  undefined ***local_70;
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  lVar5 = __ZNSt3__16chrono12steady_clock3nowEv();
  plVar6 = (long *)__Znwm(0x58);
  plVar10 = plVar6 + 1;
  *plVar10 = 0;
  plVar6[2] = 0;
  *plVar6 = (long)&PTR_FUN_09d83580;
  plVar9 = plVar6 + 3;
  *plVar9 = 0x32aaaba7;
  plVar6[5] = 0;
  plVar6[4] = 0;
  plVar6[7] = 0;
  plVar6[6] = 0;
  plVar6[9] = 0;
  plVar6[8] = 0;
  plVar6[10] = 0;
  __ZNSt3__15mutex4lockEv(plVar9);
  uVar1 = *param_1;
  uVar2 = param_1[1];
  lVar4 = *param_2;
  plVar3 = (long *)param_2[1];
  if (plVar3 != (long *)0x0) {
    plVar3[1] = plVar3[1] + 1;
  }
  if (plVar6 != (long *)0x0) {
    *plVar10 = *plVar10 + 1;
  }
  local_90 = (long *)0x0;
  local_90 = (long *)__Znwm(0x30);
  *local_90 = (long)&PTR_FUN_09de58b8;
  local_90[1] = lVar4;
  local_90[2] = (long)plVar3;
  if (plVar3 != (long *)0x0) {
    plVar3[1] = plVar3[1] + 1;
  }
  local_90[3] = lVar5;
  local_90[4] = (long)plVar9;
  local_90[5] = (long)plVar6;
  uVar7 = FUN_0305da30(uVar1,uVar2,param_1 + 2,param_1 + 5,alStack_a8);
  if (local_90 == alStack_a8) {
    pcVar8 = *(code **)(*local_90 + 0x20);
LAB_0305d8b8:
    (*pcVar8)();
  }
  else if (local_90 != (long *)0x0) {
    pcVar8 = *(code **)(*local_90 + 0x28);
    goto LAB_0305d8b8;
  }
  if (plVar3 != (long *)0x0) {
    LOAcquire();
    lVar4 = plVar3[1];
    plVar3[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*plVar3 + 0x10))(plVar3);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  uStack_80 = *param_1;
  local_78 = uVar7 & 0xffffffff;
  local_88 = &PTR_FUN_09de5998;
  local_70 = &local_88;
  FUN_06668c44(*param_2,&local_88);
  if (local_70 == &local_88) {
    pcVar8 = (code *)(*local_70)[4];
  }
  else {
    if (local_70 == (undefined ***)0x0) goto LAB_0305d938;
    pcVar8 = (code *)(*local_70)[5];
  }
  (*pcVar8)();
LAB_0305d938:
  __ZNSt3__15mutex6unlockEv(plVar9);
  if (plVar6 != (long *)0x0) {
    LOAcquire();
    lVar4 = plVar6[1];
    plVar6[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*plVar6 + 0x10))(plVar6);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_68) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


