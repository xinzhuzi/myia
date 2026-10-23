// Ghidra inferred pseudocode; requested=0x667637c
// entry=0667637c end=0667668b

void FUN_0667637c(ulong *param_1,ulong param_2)

{
  ulong *puVar1;
  uint uVar2;
  ulong uVar3;
  long lVar4;
  ulong *puVar5;
  undefined8 *puVar6;
  long *plVar7;
  ulong *puVar8;
  ulong uVar9;
  code *pcVar10;
  long *plVar11;
  long *plVar12;
  ulong uVar13;
  ulong local_98;
  long *local_90;
  ulong local_88;
  long *local_80;
  ulong local_78;
  ulong uStack_70;
  long alStack_68 [3];
  long *local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  if (*param_1 <= param_1[3]) goto LAB_06676658;
  puVar1 = (ulong *)param_1[4];
  puVar8 = (ulong *)param_1[5];
  if (puVar1 == puVar8) goto LAB_06676658;
  local_88 = *puVar1;
  local_80 = (long *)puVar1[1];
  puVar5 = puVar1;
  if (local_80 != (long *)0x0) {
    local_80[1] = local_80[1] + 1;
    puVar8 = (ulong *)param_1[5];
    puVar5 = (ulong *)param_1[4];
  }
  uStack_70 = puVar1[3];
  local_78 = puVar1[2];
  FUN_0667d6b0(puVar5,puVar8,&local_98,(long)puVar8 - (long)puVar5 >> 5);
  uVar13 = param_1[5];
  plVar12 = *(long **)(uVar13 - 0x18);
  if (plVar12 != (long *)0x0) {
    LOAcquire();
    lVar4 = plVar12[1];
    plVar12[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*plVar12 + 0x10))(plVar12);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar12);
    }
  }
  uVar3 = uStack_70;
  uVar9 = local_88;
  param_1[5] = uVar13 - 0x20;
  local_98 = local_88;
  local_90 = local_80;
  if (local_80 != (long *)0x0) {
    local_80[1] = local_80[1] + 1;
  }
  puVar5 = param_1 + 2;
  puVar1 = (ulong *)*puVar5;
  puVar8 = puVar5;
  if ((ulong *)*puVar5 != (ulong *)0x0) {
    do {
      while (puVar5 = puVar1, local_88 < puVar5[4]) {
        puVar1 = (ulong *)*puVar5;
        puVar8 = puVar5;
        if ((ulong *)*puVar5 == (ulong *)0x0) goto LAB_066764a4;
      }
      if (local_88 <= puVar5[4]) goto LAB_066764e8;
      puVar1 = (ulong *)puVar5[1];
    } while ((ulong *)puVar5[1] != (ulong *)0x0);
    puVar8 = puVar5 + 1;
  }
LAB_066764a4:
  puVar6 = (undefined8 *)__Znwm(0x28);
  puVar6[4] = uVar9;
  *puVar6 = 0;
  puVar6[1] = 0;
  puVar6[2] = puVar5;
  *puVar8 = (ulong)puVar6;
  if (*(ulong *)param_1[1] != 0) {
    param_1[1] = *(ulong *)param_1[1];
    puVar6 = (undefined8 *)*puVar8;
  }
  FUN_0002413c(param_1[2],puVar6);
  param_1[3] = param_1[3] + 1;
LAB_066764e8:
  plVar12 = local_90;
  uVar13 = local_98;
  uVar2 = *(uint *)(local_98 + 0x288);
  uVar9 = (ulong)uVar2;
  if ((param_2 & 1) == 0) {
    if (uVar2 != 3) {
      plVar12 = (long *)__Znwm(0x20);
      plVar12[1] = uVar3;
      *plVar12 = (long)&PTR_FUN_09df9538;
      plVar12[2] = (long)PTR___ZTIx_09b36ac8;
      plVar12[3] = (long)(plVar12 + 1);
      plVar11 = *(long **)(uVar13 + 0x398);
      if (plVar11 != (long *)0x0) {
        plVar7 = (long *)*plVar11;
        *plVar11 = (long)plVar12;
        if (plVar7 != (long *)0x0) {
          (**(code **)(*plVar7 + 8))();
        }
        plVar12 = (long *)0x0;
        *(undefined8 *)(uVar13 + 0x398) = 0;
      }
      *(undefined8 *)(uVar13 + 0x390) = 0;
      FUN_06677e1c(uVar13);
      if (plVar12 != (long *)0x0) {
        pcVar10 = *(code **)(*plVar12 + 8);
        goto LAB_066765f4;
      }
    }
  }
  else if (uVar2 != 3) {
    plVar11 = *(long **)(local_98 + 0x268);
    if (local_90 != (long *)0x0) {
      uVar9 = local_90[1];
      local_90[1] = uVar9 + 1;
    }
    local_50 = (long *)0x0;
    local_50 = (long *)__Znwm(uVar9,0x20);
    *local_50 = (long)&PTR_FUN_09fb2b00;
    local_50[1] = uVar13;
    local_50[2] = (long)plVar12;
    local_50[3] = uVar3;
    (**(code **)(*plVar11 + 0x10))(plVar11,alStack_68);
    plVar12 = local_50;
    if (local_50 == alStack_68) {
      pcVar10 = *(code **)(*local_50 + 0x20);
    }
    else {
      if (local_50 == (long *)0x0) goto LAB_066765f8;
      pcVar10 = *(code **)(*local_50 + 0x28);
    }
LAB_066765f4:
    (*pcVar10)(plVar12);
  }
LAB_066765f8:
  plVar12 = local_90;
  if (local_90 != (long *)0x0) {
    LOAcquire();
    lVar4 = local_90[1];
    local_90[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*local_90 + 0x10))(local_90);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar12);
    }
  }
  plVar12 = local_80;
  if (local_80 != (long *)0x0) {
    LOAcquire();
    lVar4 = local_80[1];
    local_80[1] = lVar4 + -1;
    LORelease();
    if (lVar4 == 0) {
      (**(code **)(*local_80 + 0x10))(local_80);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar12);
    }
  }
LAB_06676658:
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


