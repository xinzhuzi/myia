// Ghidra inferred pseudocode; requested=0x66617e4
// entry=066617e4 end=06661a2b

undefined8 FUN_066617e4(long *param_1,long *param_2)

{
  long *plVar1;
  undefined8 *puVar2;
  long lVar3;
  undefined8 *puVar4;
  undefined8 uVar5;
  long **pplVar6;
  code *pcVar7;
  long alStack_78 [3];
  long *local_60;
  long alStack_58 [3];
  long *local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  pplVar6 = (long **)(param_2 + 3);
  plVar1 = *pplVar6;
  if (plVar1 == (long *)0x0) {
    pplVar6 = &local_60;
LAB_06661830:
    *pplVar6 = (long *)0x0;
  }
  else {
    local_60 = plVar1;
    if (plVar1 != param_2) goto LAB_06661830;
    local_60 = alStack_78;
    (**(code **)(*plVar1 + 0x18))(plVar1,alStack_78);
  }
  puVar2 = (undefined8 *)__Znwm(0x48);
  *puVar2 = &PTR_FUN_09fb1840;
  puVar2[1] = 0;
  lVar3 = __Znwm(0x20);
  if (local_60 == (long *)0x0) {
    pplVar6 = &local_40;
LAB_0666189c:
    *pplVar6 = (long *)0x0;
  }
  else {
    if (local_60 != alStack_78) {
      pplVar6 = &local_60;
      local_40 = local_60;
      goto LAB_0666189c;
    }
    local_40 = alStack_58;
    (**(code **)(*local_60 + 0x18))(local_60,alStack_58);
  }
  *(undefined8 *)(lVar3 + 0x18) = 0;
  puVar4 = (undefined8 *)__Znwm(0x28);
  *puVar4 = &PTR_FUN_09fb1898;
  if (local_40 == (long *)0x0) {
    pplVar6 = (long **)(puVar4 + 4);
LAB_066618fc:
    *pplVar6 = (long *)0x0;
  }
  else {
    if (local_40 != alStack_58) {
      pplVar6 = &local_40;
      puVar4[4] = local_40;
      goto LAB_066618fc;
    }
    puVar4[4] = puVar4 + 1;
    (**(code **)(*local_40 + 0x18))(local_40);
  }
  *(undefined8 **)(lVar3 + 0x18) = puVar4;
  if (local_40 == alStack_58) {
    pcVar7 = *(code **)(*local_40 + 0x20);
LAB_0666194c:
    (*pcVar7)();
  }
  else if (local_40 != (long *)0x0) {
    pcVar7 = *(code **)(*local_40 + 0x28);
    goto LAB_0666194c;
  }
  puVar2[2] = lVar3;
  puVar2[3] = lVar3;
  puVar2[4] = FUN_025bf788;
  puVar2[5] = FUN_025bf3d8;
  puVar2[6] = 0;
  puVar2[7] = FUN_025bf7a0;
  uVar5 = (**(code **)(*(long *)param_1[1] + 0x20))();
  (**(code **)(*(long *)param_1[1] + 0x30))((long *)param_1[1],uVar5,0,puVar2,0,0);
  (**(code **)(*param_1 + 0x28))(param_1,uVar5,0,0,0);
  if (local_60 == alStack_78) {
    pcVar7 = *(code **)(*local_60 + 0x20);
  }
  else {
    if (local_60 == (long *)0x0) goto LAB_066619f8;
    pcVar7 = *(code **)(*local_60 + 0x28);
  }
  (*pcVar7)();
LAB_066619f8:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_38) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return uVar5;
}


