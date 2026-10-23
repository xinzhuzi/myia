// Ghidra inferred pseudocode; requested=0x6686420
// entry=06686420 end=0668654b

void FUN_06686420(long param_1,long *param_2,long param_3,undefined4 param_4,long param_5,
                 long *param_6)

{
  long *plVar1;
  long lVar2;
  long *plVar3;
  undefined1 *puVar4;
  long *plVar5;
  long *plVar6;
  long lVar7;
  undefined8 uVar8;
  long lVar9;
  long lVar10;
  long lVar11;
  long lVar12;
  long lVar13;
  undefined8 local_60;
  
  lVar11 = param_2[1];
  lVar10 = *param_2;
  lVar13 = param_2[3];
  lVar12 = param_2[2];
  puVar4 = &SUB_aaaaaaaaaaaaaaaa;
  lVar7 = param_2[4];
  local_60 = CONCAT44(0xaaaaaaaa,param_4);
  lVar2 = *param_6;
  plVar6 = (long *)param_6[1];
  if (plVar6 != (long *)0x0) {
    puVar4 = (undefined1 *)plVar6[1];
    plVar6[1] = (long)(puVar4 + 1);
  }
  uVar8 = *(undefined8 *)(param_1 + 8);
  __ZNSt3__15mutex4lockEv(puVar4,uVar8);
  lVar9 = *(long *)(param_1 + 8);
  plVar3 = (long *)__Znwm(0x60);
  plVar3[2] = lVar11;
  plVar3[1] = lVar10;
  plVar3[4] = lVar13;
  plVar3[3] = lVar12;
  plVar3[6] = param_3;
  plVar3[5] = lVar7;
  plVar3[8] = param_5;
  plVar3[7] = local_60;
  plVar3[9] = lVar2;
  plVar3[10] = (long)plVar6;
  if (plVar6 != (long *)0x0) {
    plVar1 = plVar6 + 1;
    *plVar1 = *plVar1 + 1;
    plVar3[0xb] = 0;
    plVar5 = *(long **)(lVar9 + 0x88);
    *plVar3 = *plVar5;
    *plVar5 = (long)plVar3;
    *(long **)(lVar9 + 0x88) = plVar3;
    __ZNSt3__15mutex6unlockEv(uVar8);
    LOAcquire();
    lVar2 = *plVar1;
    *plVar1 = lVar2 + -1;
    LORelease();
    if (lVar2 != 0) {
      return;
    }
    (**(code **)(*plVar6 + 0x10))(plVar6);
    __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
    return;
  }
  plVar3[0xb] = 0;
  plVar6 = *(long **)(lVar9 + 0x88);
  *plVar3 = *plVar6;
  *plVar6 = (long)plVar3;
  *(long **)(lVar9 + 0x88) = plVar3;
  __ZNSt3__15mutex6unlockEv(uVar8);
  return;
}


