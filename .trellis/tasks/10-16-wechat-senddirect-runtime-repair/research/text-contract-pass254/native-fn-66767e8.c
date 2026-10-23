// Ghidra inferred pseudocode; requested=0x66767e8
// entry=066767e8 end=066769bb

void FUN_066767e8(long *param_1,long *param_2,long *param_3)

{
  long lVar1;
  long *plVar2;
  undefined8 *puVar3;
  long *plVar4;
  long *plVar5;
  long *plVar6;
  long *plVar7;
  
  if (param_3 == (long *)0x0) {
    param_3 = (long *)FUN_066734b4();
  }
  plVar5 = param_2 + 1;
  plVar4 = (long *)*plVar5;
  plVar2 = plVar5;
  if (plVar4 != (long *)0x0) {
    do {
      if ((long *)plVar4[4] >= param_3) {
        plVar2 = plVar4;
      }
      plVar4 = (long *)plVar4[(long *)plVar4[4] < param_3];
    } while (plVar4 != (long *)0x0);
    if ((plVar2 != plVar5) && ((long *)plVar2[4] <= param_3)) {
      lVar1 = plVar2[6];
      *param_1 = plVar2[5];
      param_1[1] = lVar1;
      if (lVar1 != 0) {
        *(long *)(lVar1 + 8) = *(long *)(lVar1 + 8) + 1;
        return;
      }
      return;
    }
  }
  lVar1 = (**(code **)(*param_3 + 0x38))(param_3);
  plVar2 = (long *)__Znwm(0x58);
  plVar4 = plVar2 + 1;
  *plVar4 = 0;
  plVar2[2] = 0;
  *plVar2 = (long)&PTR_FUN_09fb2b80;
  plVar7 = plVar2 + 3;
  *plVar7 = lVar1;
  plVar2[6] = 0;
  plVar2[7] = 0;
  plVar2[5] = 0;
  plVar2[4] = (long)(plVar2 + 5);
  plVar2[8] = 0;
  plVar2[9] = 0;
  *param_1 = (long)plVar7;
  param_1[1] = (long)plVar2;
  if (plVar2 != (long *)0x0) {
    *plVar4 = *plVar4 + 1;
  }
  plVar4 = (long *)*plVar5;
  do {
    plVar6 = plVar5;
    if (plVar4 == (long *)0x0) {
LAB_06676904:
      puVar3 = (undefined8 *)__Znwm(0x38);
      puVar3[4] = param_3;
      puVar3[5] = plVar7;
      puVar3[6] = plVar2;
      *puVar3 = 0;
      puVar3[1] = 0;
      puVar3[2] = plVar5;
      *plVar6 = (long)puVar3;
      if (*(long *)*param_2 != 0) {
        *param_2 = *(long *)*param_2;
        puVar3 = (undefined8 *)*plVar6;
      }
      FUN_0002413c(param_2[1],puVar3);
      param_2[2] = param_2[2] + 1;
      plVar2 = (long *)0x0;
LAB_06676958:
      if (plVar2 != (long *)0x0) {
        LOAcquire();
        lVar1 = plVar2[1];
        plVar2[1] = lVar1 + -1;
        LORelease();
        if (lVar1 == 0) {
          (**(code **)(*plVar2 + 0x10))(plVar2);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar2);
        }
      }
      return;
    }
    while (plVar5 = plVar4, (long *)plVar5[4] <= param_3) {
      if (param_3 <= (long *)plVar5[4]) goto LAB_06676958;
      plVar4 = (long *)plVar5[1];
      if ((long *)plVar5[1] == (long *)0x0) {
        plVar6 = plVar5 + 1;
        goto LAB_06676904;
      }
    }
    plVar4 = (long *)*plVar5;
  } while( true );
}


