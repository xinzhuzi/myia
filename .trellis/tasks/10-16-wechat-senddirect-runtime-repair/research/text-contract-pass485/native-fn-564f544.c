// Ghidra inferred pseudocode; requested=0x564f544
// entry=0564f544 end=0564f6ef

undefined1  [16] FUN_0564f544(long *param_1,undefined8 param_2,undefined8 *param_3)

{
  long lVar1;
  int iVar2;
  undefined8 *puVar3;
  undefined8 uVar4;
  long *plVar5;
  undefined8 *puVar6;
  long *plVar7;
  long *plVar8;
  undefined1 auVar9 [16];
  
  plVar7 = param_1 + 1;
  puVar3 = (undefined8 *)__Znwm(0x48);
  thunk_FUN_056308d8(puVar3 + 4,param_2);
  lVar1 = param_3[1];
  puVar3[7] = *param_3;
  puVar3[8] = lVar1;
  if (lVar1 != 0) {
    *(long *)(lVar1 + 8) = *(long *)(lVar1 + 8) + 1;
  }
  plVar5 = (long *)*plVar7;
  while (plVar8 = plVar7, plVar5 != (long *)0x0) {
    while (plVar7 = plVar5, iVar2 = FUN_056311f0(param_1 + 2,puVar3 + 4,plVar7 + 4), iVar2 == 0) {
      iVar2 = FUN_056311f0(param_1 + 2,plVar7 + 4,puVar3 + 4);
      if (iVar2 == 0) {
        puVar6 = (undefined8 *)*plVar8;
        if (puVar6 == (undefined8 *)0x0) goto LAB_0564f690;
        if (puVar3 == (undefined8 *)0x0) {
          uVar4 = 0;
        }
        else {
          plVar7 = (long *)puVar3[8];
          if (plVar7 != (long *)0x0) {
            LOAcquire();
            lVar1 = plVar7[1];
            plVar7[1] = lVar1 + -1;
            LORelease();
            if (lVar1 == 0) {
              (**(code **)(*plVar7 + 0x10))(plVar7);
              __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
            }
          }
          FUN_0562fd84(puVar3 + 4);
          __ZdlPvm(puVar3,0x48);
          uVar4 = 0;
        }
        goto LAB_0564f6d0;
      }
      plVar8 = plVar7 + 1;
      plVar5 = (long *)*plVar8;
      if ((long *)*plVar8 == (long *)0x0) goto LAB_0564f690;
    }
    plVar5 = (long *)*plVar7;
  }
LAB_0564f690:
  *puVar3 = 0;
  puVar3[1] = 0;
  puVar3[2] = plVar7;
  *plVar8 = (long)puVar3;
  puVar6 = puVar3;
  if (*(long *)*param_1 != 0) {
    *param_1 = *(long *)*param_1;
    puVar6 = (undefined8 *)*plVar8;
  }
  FUN_0002413c(param_1[1],puVar6);
  param_1[2] = param_1[2] + 1;
  uVar4 = 1;
  puVar6 = puVar3;
LAB_0564f6d0:
  auVar9._8_8_ = uVar4;
  auVar9._0_8_ = puVar6;
  return auVar9;
}


