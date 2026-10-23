// Ghidra inferred pseudocode; requested=0x4c89510
// entry=04c89510 end=04c89853

void FUN_04c89510(undefined8 *param_1,long *param_2)

{
  undefined8 *puVar1;
  long lVar2;
  long *plVar3;
  undefined8 *puVar4;
  undefined8 uVar5;
  long lVar6;
  long *plVar7;
  undefined8 **local_3d8;
  long *plStack_3d0;
  undefined8 *local_88;
  undefined8 *local_80;
  long local_78;
  undefined8 local_70;
  long *local_68;
  long local_60;
  long *local_58;
  long *local_50;
  long *local_48;
  
  plVar3 = (long *)__Znwm(0x290);
  plVar3[1] = 0;
  plVar3[2] = 0;
  *plVar3 = (long)&PTR_FUN_09c92390;
  plVar7 = plVar3 + 3;
  _bzero(plVar7,0x278);
  FUN_00ac6038(plVar7);
  local_50 = plVar7;
  local_48 = plVar3;
  FUN_04cbbd20(plVar7,0x31);
  FUN_04cbcfd4(plVar7,0x13);
  if ((plVar3[0x47] == 0) ||
     (local_60 = ___dynamic_cast(plVar3[0x47],&PTR_DAT_09eb1040,&PTR_DAT_09eb0cc0,0), local_60 == 0)
     ) {
    local_60 = 0;
    local_58 = (long *)0x0;
  }
  else {
    local_58 = (long *)plVar3[0x48];
    if (local_58 != (long *)0x0) {
      local_58[1] = local_58[1] + 1;
    }
  }
  lVar2 = local_60;
  local_88 = (undefined8 *)0x0;
  local_80 = (undefined8 *)0x0;
  local_78 = 0;
  puVar4 = (undefined8 *)*param_2;
  puVar1 = (undefined8 *)param_2[1];
  local_3d8 = &local_88;
  plStack_3d0 = (long *)&DAT_aaaaaaaaaaaaaa00;
  lVar6 = (long)puVar1 - (long)puVar4;
  if (lVar6 != 0) {
    if (lVar6 < 0) {
                    /* WARNING: Subroutine does not return */
      FUN_00890a88(&local_88);
    }
    local_88 = (undefined8 *)__Znwm(lVar6);
    local_78 = (long)local_88 + lVar6;
    local_80 = local_88;
    do {
      *local_80 = *puVar4;
      lVar6 = puVar4[1];
      local_80[1] = lVar6;
      if (lVar6 != 0) {
        *(long *)(lVar6 + 8) = *(long *)(lVar6 + 8) + 1;
      }
      puVar4 = puVar4 + 2;
      local_80 = local_80 + 2;
    } while (puVar4 != puVar1);
  }
  FUN_04c88578(&local_70,&local_88,0x13);
  if (local_68 != (long *)0x0) {
    local_68[1] = local_68[1] + 1;
  }
  *(undefined8 *)(lVar2 + 0x6b0) = local_70;
  plVar7 = *(long **)(lVar2 + 0x6b8);
  *(long **)(lVar2 + 0x6b8) = local_68;
  if (plVar7 != (long *)0x0) {
    LOAcquire();
    lVar6 = plVar7[1];
    plVar7[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*plVar7 + 0x10))(plVar7);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
    }
  }
  if (local_68 != (long *)0x0) {
    LOAcquire();
    lVar6 = local_68[1];
    local_68[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*local_68 + 0x10))(local_68);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_68);
    }
  }
  puVar1 = local_88;
  puVar4 = local_80;
  if (local_88 != (undefined8 *)0x0) {
    for (; puVar4 != puVar1; puVar4 = puVar4 + -2) {
      plVar7 = (long *)puVar4[-1];
      if (plVar7 != (long *)0x0) {
        LOAcquire();
        lVar6 = plVar7[1];
        plVar7[1] = lVar6 + -1;
        LORelease();
        if (lVar6 == 0) {
          (**(code **)(*plVar7 + 0x10))(plVar7);
          __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
        }
      }
    }
    local_80 = puVar1;
    __ZdlPvm(local_88,local_78 - (long)local_88);
  }
  local_3d8 = *(undefined8 ***)(local_60 + 0x6b0);
  plVar7 = *(long **)(local_60 + 0x6b8);
  if (plVar7 != (long *)0x0) {
    plVar7[1] = plVar7[1] + 1;
  }
  plStack_3d0 = plVar7;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (local_60 + 0x1e0,local_3d8 + 6);
  if (plVar7 != (long *)0x0) {
    LOAcquire();
    lVar6 = plVar7[1];
    plVar7[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*plVar7 + 0x10))(plVar7);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
    }
  }
  FUN_04cbfc30(&local_3d8,local_50);
  puVar4 = (undefined8 *)__Znwm(0x368);
  puVar4[1] = 0;
  puVar4[2] = 0;
  *puVar4 = &PTR_FUN_09c12f88;
  uVar5 = FUN_00395584(puVar4 + 3,&local_3d8);
  *param_1 = uVar5;
  param_1[1] = puVar4;
  FUN_00396780(&local_3d8);
  plVar7 = local_58;
  if (local_58 != (long *)0x0) {
    LOAcquire();
    lVar6 = local_58[1];
    local_58[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*local_58 + 0x10))(local_58);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
    }
  }
  plVar7 = local_48;
  if (local_48 != (long *)0x0) {
    LOAcquire();
    lVar6 = local_48[1];
    local_48[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*local_48 + 0x10))(local_48);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar7);
    }
  }
  return;
}


