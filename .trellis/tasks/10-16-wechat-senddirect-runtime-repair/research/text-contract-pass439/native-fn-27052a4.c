// Ghidra inferred pseudocode; requested=0x27052a4
// entry=027052a4 end=02705377

void FUN_027052a4(long *param_1,long param_2,long param_3)

{
  long *plVar1;
  long lVar2;
  long *plVar3;
  
  plVar3 = (long *)param_1[1];
  if ((param_2 != param_3) && (plVar3 != param_1)) {
    do {
      FUN_027055ac(plVar3 + 2,param_2 + 0x10);
      plVar3[0x20] = *(long *)(param_2 + 0x100);
      param_2 = *(long *)(param_2 + 8);
      plVar3 = (long *)plVar3[1];
    } while (param_2 != param_3 && plVar3 != param_1);
  }
  if (plVar3 != param_1) {
    plVar1 = *(long **)(*param_1 + 8);
    lVar2 = *plVar3;
    *(long **)(lVar2 + 8) = plVar1;
    *plVar1 = lVar2;
    do {
      plVar1 = (long *)plVar3[1];
      param_1[2] = param_1[2] + -1;
      FUN_056fa308(plVar3 + 2);
      __ZdlPvm(plVar3,0x108);
      plVar3 = plVar1;
    } while (plVar1 != param_1);
    return;
  }
  FUN_02705378(param_1,param_1,param_2,param_3);
  return;
}


