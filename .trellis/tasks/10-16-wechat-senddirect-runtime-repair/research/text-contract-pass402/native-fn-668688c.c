// Ghidra inferred pseudocode; requested=0x668688c
// entry=0668688c end=0668697f

void FUN_0668688c(long param_1,long param_2)

{
  long *plVar1;
  long *plVar2;
  uint uVar3;
  long *plVar4;
  undefined8 uVar5;
  long *plVar6;
  long lVar7;
  long lVar8;
  long lVar9;
  long lVar10;
  long lVar11;
  long lVar12;
  long lVar13;
  
  uVar5 = *(undefined8 *)(param_1 + 8);
  __ZNSt3__15mutex4lockEv(uVar5);
  plVar6 = (long *)*(long *)(*(long *)(param_1 + 8) + 0x80);
  while (plVar1 = plVar6, plVar1 != (long *)0x0) {
    plVar6 = (long *)*plVar1;
    uVar3 = *(uint *)(plVar1 + 7);
    if ((uVar3 >> 1 & 1) == 0) {
      plVar2 = (long *)__Znwm(0x60);
      lVar8 = plVar1[2];
      lVar7 = plVar1[1];
      lVar10 = plVar1[4];
      lVar9 = plVar1[3];
      lVar12 = plVar1[6];
      lVar11 = plVar1[5];
      lVar13 = plVar1[7];
      plVar2[8] = plVar1[8];
      plVar2[7] = lVar13;
      plVar2[6] = lVar12;
      plVar2[5] = lVar11;
      plVar2[4] = lVar10;
      plVar2[3] = lVar9;
      plVar2[2] = lVar8;
      plVar2[1] = lVar7;
      lVar7 = plVar1[10];
      plVar2[9] = plVar1[9];
      plVar2[10] = lVar7;
      if (lVar7 != 0) {
        *(long *)(lVar7 + 8) = *(long *)(lVar7 + 8) + 1;
      }
      plVar2[0xb] = plVar1[0xb];
      plVar4 = *(long **)(param_2 + 8);
      *plVar2 = *plVar4;
      *plVar4 = (long)plVar2;
      *(long **)(param_2 + 8) = plVar2;
      uVar3 = *(uint *)(plVar1 + 7);
    }
    if ((uVar3 & 3) == 1) {
      *(uint *)(plVar1 + 7) = uVar3 | 2;
      if (plVar1[6] != 0) {
        FUN_06685fd0(plVar1[6],param_1);
      }
      *(undefined1 *)(*(long *)(param_1 + 8) + 0x99) = 1;
    }
  }
  __ZNSt3__15mutex6unlockEv(uVar5);
  return;
}


