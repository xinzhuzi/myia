// Ghidra inferred pseudocode; requested=0x2705378
// entry=02705378 end=0270551f

long * FUN_02705378(long param_1,long *param_2,long param_3,long param_4)

{
  long *plVar1;
  long *plVar2;
  long *plVar3;
  long lVar4;
  long lVar5;
  
  plVar2 = param_2;
  if (param_3 != param_4) {
    plVar2 = (long *)__Znwm(0x108);
    plVar2[0x18] = (long)&PTR____cxa_pure_virtual_09da57d8;
    *plVar2 = 0;
    plVar2[1] = 0;
    FUN_02703c98(plVar2 + 2,&PTR_PTR_09f24220,param_3 + 0x10);
    plVar2[2] = (long)&PTR_FUN_09f23fe8;
    plVar2[0x18] = (long)&PTR_FUN_09f24040;
    plVar2[0x19] = (long)&PTR_FUN_09f24080;
    plVar2[0x1a] = (long)&PTR_FUN_09f240c0;
    plVar2[0x1b] = (long)&PTR_FUN_09f24100;
    plVar2[0x1c] = (long)&PTR_FUN_09f24140;
    plVar2[0x1d] = (long)&PTR_FUN_09f24180;
    plVar2[0x1e] = (long)&PTR_FUN_09f241c0;
    plVar2[0x1f] = (long)&PTR_FUN_09f24200;
    plVar2[0x20] = *(long *)(param_3 + 0x100);
    lVar5 = 1;
    plVar1 = plVar2;
    for (lVar4 = *(long *)(param_3 + 8); lVar4 != param_4; lVar4 = *(long *)(lVar4 + 8)) {
      plVar3 = (long *)__Znwm(0x108);
      *plVar3 = (long)plVar1;
      plVar3[1] = 0;
      plVar3[0x18] = (long)&PTR____cxa_pure_virtual_09da57d8;
      FUN_02703c98(plVar3 + 2,&PTR_PTR_09f24220,lVar4 + 0x10);
      plVar3[2] = (long)&PTR_FUN_09f23fe8;
      plVar3[0x18] = (long)&PTR_FUN_09f24040;
      plVar3[0x19] = (long)&PTR_FUN_09f24080;
      plVar3[0x1a] = (long)&PTR_FUN_09f240c0;
      plVar3[0x1b] = (long)&PTR_FUN_09f24100;
      plVar3[0x1c] = (long)&PTR_FUN_09f24140;
      plVar3[0x1d] = (long)&PTR_FUN_09f24180;
      plVar3[0x1e] = (long)&PTR_FUN_09f241c0;
      plVar3[0x1f] = (long)&PTR_FUN_09f24200;
      plVar3[0x20] = *(long *)(lVar4 + 0x100);
      plVar1[1] = (long)plVar3;
      lVar5 = lVar5 + 1;
      plVar1 = plVar3;
    }
    lVar4 = *param_2;
    *(long **)(lVar4 + 8) = plVar2;
    *plVar2 = lVar4;
    *param_2 = (long)plVar1;
    plVar1[1] = (long)param_2;
    *(long *)(param_1 + 0x10) = *(long *)(param_1 + 0x10) + lVar5;
  }
  return plVar2;
}


