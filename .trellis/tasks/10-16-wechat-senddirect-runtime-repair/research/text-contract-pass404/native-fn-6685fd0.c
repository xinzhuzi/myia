// Ghidra inferred pseudocode; requested=0x6685fd0
// entry=06685fd0 end=066860af

void FUN_06685fd0(long param_1,ulong param_2)

{
  int iVar1;
  long lVar2;
  bool bVar3;
  long *plVar4;
  long *plVar5;
  long *plVar6;
  long *plVar7;
  long *plVar8;
  
  __ZNSt3__15mutex4lockEv();
  plVar5 = (long *)(param_1 + 0x48);
  plVar4 = (long *)*plVar5;
  plVar7 = plVar5;
  plVar8 = plVar4;
  if (plVar4 != (long *)0x0) {
    do {
      if ((ulong)plVar8[4] >= param_2) {
        plVar7 = plVar8;
      }
      plVar6 = plVar8 + ((ulong)plVar8[4] < param_2);
      plVar8 = (long *)*plVar6;
    } while ((long *)*plVar6 != (long *)0x0);
    if (((plVar7 != plVar5) && ((ulong)plVar7[4] <= param_2)) &&
       (lVar2 = plVar7[5], iVar1 = (int)lVar2 + -1, *(int *)(plVar7 + 5) = iVar1,
       iVar1 == 0 || (int)lVar2 < 1)) {
      plVar8 = plVar7;
      plVar5 = (long *)plVar7[1];
      if ((long *)plVar7[1] == (long *)0x0) {
        do {
          plVar6 = (long *)plVar8[2];
          bVar3 = (long *)*plVar6 != plVar8;
          plVar8 = plVar6;
        } while (bVar3);
      }
      else {
        do {
          plVar6 = plVar5;
          plVar5 = (long *)*plVar6;
        } while ((long *)*plVar6 != (long *)0x0);
      }
      if (*(long **)(param_1 + 0x40) == plVar7) {
        *(long **)(param_1 + 0x40) = plVar6;
      }
      *(long *)(param_1 + 0x50) = *(long *)(param_1 + 0x50) + -1;
      FUN_00024618(plVar4,plVar7);
      __ZdlPvm(plVar7,0x30);
    }
  }
  __ZNSt3__15mutex6unlockEv(param_1);
  return;
}


