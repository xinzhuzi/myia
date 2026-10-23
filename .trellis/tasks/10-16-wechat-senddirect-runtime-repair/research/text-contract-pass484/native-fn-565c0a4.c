// Ghidra inferred pseudocode; requested=0x565c0a4
// entry=0565c0a4 end=0565c223

long * FUN_0565c0a4(uint *param_1)

{
  byte *pbVar1;
  undefined8 *puVar2;
  long *plVar3;
  long *plVar4;
  long *plVar5;
  long *plVar6;
  long *plVar7;
  uint uVar8;
  long *plVar9;
  long lVar10;
  
  pbVar1 = (byte *)(*(code *)PTR___tlv_bootstrap_0a24db08)();
  if ((*pbVar1 & 1) == 0) {
    FUN_0711c9ac();
  }
  puVar2 = (undefined8 *)(*(code *)PTR___tlv_bootstrap_0a24daf0)();
  plVar6 = (long *)*puVar2;
  if (plVar6 == (long *)0x0) {
    plVar6 = (long *)__Znwm(0x18);
    plVar6[2] = 0;
    plVar7 = plVar6 + 1;
    *plVar7 = 0;
    *plVar6 = (long)plVar7;
    *puVar2 = plVar6;
LAB_0565c190:
    uVar8 = *param_1;
    plVar5 = plVar7;
    plVar9 = plVar7;
  }
  else {
    plVar7 = plVar6 + 1;
    plVar4 = (long *)*plVar7;
    if (plVar4 == (long *)0x0) goto LAB_0565c190;
    uVar8 = *param_1;
    plVar3 = plVar7;
    plVar5 = plVar4;
    do {
      if (*(uint *)(plVar5 + 4) >= uVar8) {
        plVar3 = plVar5;
      }
      plVar5 = (long *)plVar5[*(uint *)(plVar5 + 4) < uVar8];
    } while (plVar5 != (long *)0x0);
    if ((plVar3 != plVar7) && (*(uint *)(plVar3 + 4) <= uVar8)) goto LAB_0565c1f8;
    do {
      while (plVar3 = plVar4, plVar5 = plVar3, *(uint *)(plVar3 + 4) <= uVar8) {
        if (uVar8 <= *(uint *)(plVar3 + 4)) goto LAB_0565c1f8;
        plVar4 = (long *)plVar3[1];
        if ((long *)plVar3[1] == (long *)0x0) {
          plVar9 = plVar3 + 1;
          goto LAB_0565c19c;
        }
      }
      plVar4 = (long *)*plVar3;
      plVar9 = plVar3;
    } while ((long *)*plVar3 != (long *)0x0);
  }
LAB_0565c19c:
  plVar3 = (long *)__Znwm(0x48);
  *(uint *)(plVar3 + 4) = uVar8;
  lVar10 = *(long *)(param_1 + 2);
  plVar3[6] = *(long *)(param_1 + 4);
  plVar3[5] = lVar10;
  lVar10 = *(long *)(param_1 + 6);
  plVar3[8] = *(long *)(param_1 + 8);
  plVar3[7] = lVar10;
  *plVar3 = 0;
  plVar3[1] = 0;
  plVar3[2] = (long)plVar5;
  *plVar9 = (long)plVar3;
  plVar4 = plVar3;
  if (*(long *)*plVar6 != 0) {
    *plVar6 = *(long *)*plVar6;
    plVar4 = (long *)*plVar9;
  }
  FUN_0002413c(*plVar7,plVar4);
  plVar6[2] = plVar6[2] + 1;
LAB_0565c1f8:
  return plVar3 + 5;
}


