// Ghidra inferred pseudocode; requested=0x30dc518
// entry=030dc518 end=030dc61f

byte FUN_030dc518(undefined8 param_1,long *param_2,int param_3)

{
  long lVar1;
  byte *pbVar2;
  long *plVar3;
  long *plVar4;
  int iVar5;
  long lVar6;
  byte bVar7;
  
  bVar7 = 0;
  if ((param_3 == 0x66) && (lVar6 = *param_2, lVar6 != 0)) {
    lVar1 = *(long *)(lVar6 + 0x18);
    plVar3 = *(long **)(lVar6 + 0x20);
    if (plVar3 != (long *)0x0) {
      plVar3[1] = plVar3[1] + 1;
      lVar6 = *param_2;
    }
    pbVar2 = *(byte **)(lVar6 + 0x28);
    plVar4 = *(long **)(lVar6 + 0x30);
    if (plVar4 != (long *)0x0) {
      lVar6 = plVar4[1];
      plVar4[1] = lVar6 + 1;
    }
    if (((lVar1 == 0 || pbVar2 == (byte *)0x0) ||
        (iVar5 = FUN_030f320c(lVar6,*param_2), iVar5 != 10)) ||
       (iVar5 = FUN_04a28ef8(lVar1), iVar5 == 0)) {
      bVar7 = 0;
    }
    else {
      bVar7 = *pbVar2;
    }
    if (plVar4 != (long *)0x0) {
      LOAcquire();
      lVar6 = plVar4[1];
      plVar4[1] = lVar6 + -1;
      LORelease();
      if (lVar6 == 0) {
        (**(code **)(*plVar4 + 0x10))(plVar4);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar4);
      }
    }
    if (plVar3 != (long *)0x0) {
      LOAcquire();
      lVar6 = plVar3[1];
      plVar3[1] = lVar6 + -1;
      LORelease();
      if (lVar6 == 0) {
        (**(code **)(*plVar3 + 0x10))(plVar3);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
      }
    }
  }
  return bVar7 & 1;
}


