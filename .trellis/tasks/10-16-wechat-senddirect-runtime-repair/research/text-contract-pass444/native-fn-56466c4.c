// Ghidra inferred pseudocode; requested=0x56466c4
// entry=056466c4 end=056467f7

long FUN_056466c4(long param_1,long param_2)

{
  undefined8 uVar1;
  long lVar2;
  code *pcVar3;
  long *plVar4;
  long alStack_58 [3];
  long *local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  FUN_0562e1a0();
  uVar1 = *(undefined8 *)(param_2 + 0x18);
  lVar2 = *(long *)(param_2 + 0x20);
  if (lVar2 != 0) {
    *(long *)(lVar2 + 8) = *(long *)(lVar2 + 8) + 1;
  }
  plVar4 = *(long **)(param_1 + 0x20);
  *(undefined8 *)(param_1 + 0x18) = uVar1;
  *(long *)(param_1 + 0x20) = lVar2;
  if (plVar4 == (long *)0x0) {
LAB_05646724:
    plVar4 = *(long **)(param_2 + 0x40);
    if (plVar4 != (long *)0x0) goto LAB_0564672c;
LAB_0564676c:
    local_40 = (long *)0x0;
  }
  else {
    LOAcquire();
    lVar2 = plVar4[1];
    plVar4[1] = lVar2 + -1;
    LORelease();
    if (lVar2 != 0) goto LAB_05646724;
    (**(code **)(*plVar4 + 0x10))(plVar4);
    __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
    plVar4 = *(long **)(param_2 + 0x40);
    if (plVar4 == (long *)0x0) goto LAB_0564676c;
LAB_0564672c:
    if (plVar4 == (long *)(param_2 + 0x28)) {
      local_40 = alStack_58;
      (**(code **)(*plVar4 + 0x18))(plVar4,alStack_58);
    }
    else {
      local_40 = (long *)(**(code **)(*plVar4 + 0x10))();
    }
  }
  FUN_05646898(alStack_58,param_1 + 0x28);
  if (local_40 == alStack_58) {
    pcVar3 = *(code **)(*local_40 + 0x20);
  }
  else {
    if (local_40 == (long *)0x0) goto LAB_056467c4;
    pcVar3 = *(code **)(*local_40 + 0x28);
  }
  (*pcVar3)();
LAB_056467c4:
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return param_1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


