// Ghidra inferred pseudocode; requested=0x6676714
// entry=06676714 end=066767e7

void FUN_06676714(long param_1,ulong param_2)

{
  bool bVar1;
  long *plVar2;
  long *plVar3;
  long *plVar4;
  long *plVar5;
  long *plVar6;
  
  plVar5 = (long *)(param_1 + 0x10);
  plVar2 = (long *)*plVar5;
  plVar3 = plVar5;
  plVar4 = plVar2;
  if (plVar2 != (long *)0x0) {
    do {
      if ((ulong)plVar4[4] >= param_2) {
        plVar3 = plVar4;
      }
      plVar6 = plVar4 + ((ulong)plVar4[4] < param_2);
      plVar4 = (long *)*plVar6;
    } while ((long *)*plVar6 != (long *)0x0);
    if ((plVar3 != plVar5) && ((ulong)plVar3[4] <= param_2)) {
      plVar4 = plVar3;
      plVar5 = (long *)plVar3[1];
      if ((long *)plVar3[1] == (long *)0x0) {
        do {
          plVar6 = (long *)plVar4[2];
          bVar1 = (long *)*plVar6 != plVar4;
          plVar4 = plVar6;
        } while (bVar1);
      }
      else {
        do {
          plVar6 = plVar5;
          plVar5 = (long *)*plVar6;
        } while ((long *)*plVar6 != (long *)0x0);
      }
      if (*(long **)(param_1 + 8) == plVar3) {
        *(long **)(param_1 + 8) = plVar6;
      }
      *(long *)(param_1 + 0x18) = *(long *)(param_1 + 0x18) + -1;
      FUN_00024618(plVar2,plVar3);
      __ZdlPvm(plVar3,0x28);
      FUN_0667637c(param_1,1);
      return;
    }
  }
  return;
}


