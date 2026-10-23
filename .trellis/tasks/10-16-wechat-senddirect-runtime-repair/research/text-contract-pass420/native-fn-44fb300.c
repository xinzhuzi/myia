// Ghidra inferred pseudocode; requested=0x44fb300
// entry=044fb300 end=044fb46f

void FUN_044fb300(long *param_1,long param_2,undefined8 *param_3)

{
  ulong uVar1;
  undefined8 *puVar2;
  long lVar3;
  int iVar4;
  long lVar5;
  long *plVar6;
  long *plVar7;
  long *plVar8;
  undefined1 uStack_39;
  undefined8 *local_38;
  
  uVar1 = param_3[1];
  puVar2 = (undefined8 *)*param_3;
  if (-1 < (char)*(byte *)((long)param_3 + 0x17)) {
    uVar1 = (ulong)*(byte *)((long)param_3 + 0x17);
    puVar2 = param_3;
  }
  iVar4 = FUN_04bb49a8(puVar2,uVar1);
  if (iVar4 != 0) {
    *param_1 = (long)&SUB_aaaaaaaaaaaaaaaa;
    param_1[1] = (long)&SUB_aaaaaaaaaaaaaaaa;
    FUN_044fb48c(param_1,param_2,param_3);
    if (*param_1 != 0) {
      return;
    }
    plVar8 = (long *)param_1[1];
    if (plVar8 != (long *)0x0) {
      LOAcquire();
      lVar3 = plVar8[1];
      plVar8[1] = lVar3 + -1;
      LORelease();
      if (lVar3 == 0) {
        (**(code **)(*plVar8 + 0x10))(plVar8);
        __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
      }
    }
  }
  __ZNSt3__15mutex4lockEv(param_2 + 0x130);
  lVar3 = FUN_02a31ddc(param_2 + 0x98,param_3);
  if (lVar3 == 0) {
    lVar3 = FUN_044fbf20(param_2 + 0xd8,param_3);
    if (lVar3 != 0) {
      plVar6 = *(long **)(lVar3 + 0x28);
      plVar8 = *(long **)(param_2 + 200);
      if ((plVar6 != plVar8) && (plVar7 = (long *)plVar6[1], plVar7 != plVar8)) {
        lVar3 = *plVar6;
        *(long **)(lVar3 + 8) = plVar7;
        *plVar7 = lVar3;
        lVar3 = *plVar8;
        *(long **)(lVar3 + 8) = plVar6;
        *plVar6 = lVar3;
        *plVar8 = (long)plVar6;
        plVar6[1] = (long)plVar8;
        plVar8 = *(long **)(param_2 + 200);
      }
      if (plVar8 != (long *)(param_2 + 0xc0)) {
        lVar3 = plVar8[6];
        *param_1 = plVar8[5];
        param_1[1] = lVar3;
        goto joined_r0x044fb448;
      }
    }
    *param_1 = 0;
    param_1[1] = 0;
  }
  else {
    local_38 = param_3;
    lVar5 = FUN_02ae64dc(param_2 + 0x98,param_3,&DAT_08b7a8b8,&local_38,&uStack_39);
    lVar3 = *(long *)(lVar5 + 0x30);
    *param_1 = *(long *)(lVar5 + 0x28);
    param_1[1] = lVar3;
joined_r0x044fb448:
    if (lVar3 != 0) {
      *(long *)(lVar3 + 8) = *(long *)(lVar3 + 8) + 1;
    }
  }
  __ZNSt3__15mutex6unlockEv(param_2 + 0x130);
  return;
}


