// Ghidra inferred pseudocode; requested=0x56f412c
// entry=056f412c end=056f430f

undefined8 FUN_056f412c(long *param_1,long *param_2)

{
  undefined8 uVar1;
  long *plVar2;
  ulong uVar3;
  long *plVar4;
  code *pcVar5;
  long **pplVar6;
  long alStack_d8 [3];
  long *local_c0;
  long *local_b8;
  long alStack_b0 [3];
  long *local_98;
  undefined1 *local_90;
  undefined1 *puStack_88;
  undefined1 *local_80;
  undefined1 *puStack_78;
  undefined1 *puStack_70;
  undefined1 *puStack_68;
  undefined1 *local_60;
  undefined1 *puStack_58;
  undefined1 *puStack_50;
  undefined1 *puStack_48;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  puStack_58 = &SUB_aaaaaaaaaaaaaaaa;
  local_60 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_48 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_50 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_78 = &SUB_aaaaaaaaaaaaaaaa;
  local_80 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_68 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_70 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_88 = &SUB_aaaaaaaaaaaaaaaa;
  local_90 = &SUB_aaaaaaaaaaaaaaaa;
  (**(code **)(*param_1 + 0x10))(&local_90,param_1,1);
  if (puStack_78 != (undefined1 *)0x0) {
    uVar1 = FUN_0564668c(&local_90);
    plVar2 = (long *)param_2[3];
    local_c0 = (long *)0x0;
    if (plVar2 != (long *)0x0) {
      if (plVar2 == param_2) {
        local_c0 = alStack_d8;
        (**(code **)(*plVar2 + 0x18))(plVar2,alStack_d8);
      }
      else {
        local_c0 = (long *)(**(code **)(*plVar2 + 0x10))();
      }
    }
    local_98 = (long *)0x0;
    local_b8 = param_1;
    plVar2 = (long *)__Znwm(0x30);
    *plVar2 = (long)&PTR_FUN_09f238f8;
    if (local_c0 == (long *)0x0) {
      pplVar6 = (long **)(plVar2 + 4);
LAB_056f4210:
      *pplVar6 = (long *)0x0;
      plVar4 = param_1;
    }
    else {
      if (local_c0 != alStack_d8) {
        pplVar6 = &local_c0;
        plVar2[4] = (long)local_c0;
        goto LAB_056f4210;
      }
      plVar2[4] = (long)(plVar2 + 1);
      (**(code **)(*local_c0 + 0x18))(local_c0);
      plVar4 = local_b8;
    }
    plVar2[5] = (long)plVar4;
    local_98 = plVar2;
    uVar3 = FUN_056462d0(uVar1,alStack_b0);
    if (local_98 == alStack_b0) {
      pcVar5 = *(code **)(*local_98 + 0x20);
LAB_056f427c:
      (*pcVar5)();
    }
    else if (local_98 != (long *)0x0) {
      pcVar5 = *(code **)(*local_98 + 0x28);
      goto LAB_056f427c;
    }
    if (local_c0 == alStack_d8) {
      pcVar5 = *(code **)(*local_c0 + 0x20);
LAB_056f42a8:
      (*pcVar5)();
    }
    else if (local_c0 != (long *)0x0) {
      pcVar5 = *(code **)(*local_c0 + 0x28);
      goto LAB_056f42a8;
    }
    if ((uVar3 & 1) != 0) {
      uVar1 = 1;
      goto LAB_056f42d4;
    }
    FUN_0564668c(&local_90);
    uVar1 = FUN_0109d770();
    FUN_056f2390(param_1,uVar1);
  }
  uVar1 = 0;
LAB_056f42d4:
  thunk_FUN_05646544(&local_90);
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_38) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return uVar1;
}


