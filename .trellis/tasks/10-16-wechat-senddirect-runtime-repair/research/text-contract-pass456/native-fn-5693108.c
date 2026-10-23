// Ghidra inferred pseudocode; requested=0x5693108
// entry=05693108 end=0569318f

long FUN_05693108(long param_1)

{
  long *plVar1;
  long lVar2;
  long *plVar3;
  undefined1 auStack_1e8 [440];
  
  FUN_05699278(auStack_1e8,param_1);
  plVar1 = (long *)__Znwm(0x1c8);
  *plVar1 = 0;
  plVar1[1] = 0;
  FUN_056991d0(plVar1 + 2,auStack_1e8);
  plVar3 = (long *)(param_1 + 0x78);
  lVar2 = *plVar3;
  *plVar1 = lVar2;
  plVar1[1] = (long)plVar3;
  *(long **)(lVar2 + 8) = plVar1;
  *plVar3 = (long)plVar1;
  *(long *)(param_1 + 0x88) = *(long *)(param_1 + 0x88) + 1;
  FUN_056992ec(auStack_1e8);
  FUN_056a2a48(*plVar3 + 0x10);
  return *plVar3 + 0x10;
}


