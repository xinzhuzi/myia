// Ghidra inferred pseudocode; requested=0x6661abc
// entry=06661abc end=06661d0f

undefined8 FUN_06661abc(long *param_1,undefined8 param_2,long *param_3)

{
  long *plVar1;
  undefined8 *puVar2;
  long lVar3;
  undefined8 *puVar4;
  undefined8 uVar5;
  long **pplVar6;
  code *pcVar7;
  long alStack_88 [3];
  long *local_70;
  long alStack_68 [3];
  long *local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  pplVar6 = (long **)(param_3 + 3);
  plVar1 = *pplVar6;
  if (plVar1 == (long *)0x0) {
    pplVar6 = &local_70;
LAB_06661b10:
    *pplVar6 = (long *)0x0;
  }
  else {
    local_70 = plVar1;
    if (plVar1 != param_3) goto LAB_06661b10;
    local_70 = alStack_88;
    (**(code **)(*plVar1 + 0x18))(plVar1,alStack_88);
  }
  puVar2 = (undefined8 *)__Znwm(0x48);
  *puVar2 = &PTR_FUN_09fb1840;
  puVar2[1] = 0;
  lVar3 = __Znwm(0x20);
  if (local_70 == (long *)0x0) {
    pplVar6 = &local_50;
LAB_06661b7c:
    *pplVar6 = (long *)0x0;
  }
  else {
    if (local_70 != alStack_88) {
      pplVar6 = &local_70;
      local_50 = local_70;
      goto LAB_06661b7c;
    }
    local_50 = alStack_68;
    (**(code **)(*local_70 + 0x18))(local_70,alStack_68);
  }
  *(undefined8 *)(lVar3 + 0x18) = 0;
  puVar4 = (undefined8 *)__Znwm(0x28);
  *puVar4 = &PTR_FUN_09fb1918;
  if (local_50 == (long *)0x0) {
    pplVar6 = (long **)(puVar4 + 4);
LAB_06661bdc:
    *pplVar6 = (long *)0x0;
  }
  else {
    if (local_50 != alStack_68) {
      pplVar6 = &local_50;
      puVar4[4] = local_50;
      goto LAB_06661bdc;
    }
    puVar4[4] = puVar4 + 1;
    (**(code **)(*local_50 + 0x18))(local_50);
  }
  *(undefined8 **)(lVar3 + 0x18) = puVar4;
  if (local_50 == alStack_68) {
    pcVar7 = *(code **)(*local_50 + 0x20);
LAB_06661c2c:
    (*pcVar7)();
  }
  else if (local_50 != (long *)0x0) {
    pcVar7 = *(code **)(*local_50 + 0x28);
    goto LAB_06661c2c;
  }
  puVar2[2] = lVar3;
  puVar2[3] = lVar3;
  puVar2[4] = FUN_025bf788;
  puVar2[5] = FUN_025bf3d8;
  puVar2[6] = 0;
  puVar2[7] = FUN_025bf7a0;
  uVar5 = (**(code **)(*(long *)param_1[1] + 0x20))();
  (**(code **)(*(long *)param_1[1] + 0x30))((long *)param_1[1],uVar5,1,puVar2,param_2,0);
  (**(code **)(*param_1 + 0x28))(param_1,uVar5,1,param_2,0);
  if (local_70 == alStack_88) {
    pcVar7 = *(code **)(*local_70 + 0x20);
  }
  else {
    if (local_70 == (long *)0x0) goto LAB_06661cd8;
    pcVar7 = *(code **)(*local_70 + 0x28);
  }
  (*pcVar7)();
LAB_06661cd8:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return uVar5;
}


