// Ghidra inferred pseudocode; requested=0x4cbd01c
// entry=04cbd01c end=04cbd40b

undefined8 * FUN_04cbd01c(undefined8 *param_1,int *param_2,int param_3,undefined8 param_4)

{
  long *plVar1;
  long lVar2;
  undefined4 uVar3;
  int iVar4;
  undefined8 *puVar5;
  long *plVar6;
  ulong uVar7;
  long *plVar8;
  long *local_80;
  long *plStack_78;
  undefined7 local_70;
  char cStack_69;
  ulong local_68;
  
  *param_1 = &PTR_thunk_FUN_00ac6290_09eb04f0;
  param_1[1] = 0;
  *(undefined4 *)(param_1 + 2) = 0;
  param_1[4] = 0;
  param_1[3] = 0;
  param_1[0x16] = 0;
  param_1[0x15] = 0;
  param_1[0x14] = 0;
  param_1[0x13] = 0;
  param_1[6] = 0;
  param_1[5] = 0;
  param_1[8] = 0;
  param_1[7] = 0;
  param_1[10] = 0;
  param_1[9] = 0;
  param_1[0xc] = 0;
  param_1[0xb] = 0;
  param_1[0xe] = 0;
  param_1[0xd] = 0;
  param_1[0x10] = 0;
  param_1[0xf] = 0;
  *(undefined8 *)((long)param_1 + 0x8a) = 0;
  *(undefined8 *)((long)param_1 + 0x82) = 0;
  *(undefined4 *)(param_1 + 0x17) = 0x3f800000;
  param_1[0x1b] = 0;
  param_1[0x1a] = 0;
  param_1[0x1d] = 0;
  param_1[0x1c] = 0;
  *(undefined2 *)(param_1 + 0x1e) = 0;
  param_1[0x19] = 0;
  param_1[0x18] = 0;
  *(undefined8 *)((long)param_1 + 0xfc) = 0;
  *(undefined8 *)((long)param_1 + 0xf4) = 0;
  param_1[0x2d] = 0;
  param_1[0x2c] = 0;
  param_1[0x27] = 0;
  param_1[0x26] = 0;
  *(undefined8 *)((long)param_1 + 0x124) = 0;
  *(undefined8 *)((long)param_1 + 0x11c) = 0;
  *(undefined8 *)((long)param_1 + 0x114) = 0;
  *(undefined8 *)((long)param_1 + 0x10c) = 0;
  *(undefined8 *)((long)param_1 + 0x104) = 0;
  param_1[0x29] = 0;
  param_1[0x28] = 0;
  param_1[0x2b] = 0;
  param_1[0x2a] = 0;
  param_1[0x2f] = 0;
  param_1[0x2e] = 0;
  param_1[0x31] = 0;
  param_1[0x30] = 0;
  FUN_04ea6ba0(param_1 + 0x32);
  puVar5 = (undefined8 *)__Znwm(0x20);
  puVar5[2] = 0;
  puVar5[1] = 0;
  *puVar5 = &PTR_FUN_09c08428;
  puVar5[3] = 0;
  param_1[0x41] = puVar5 + 3;
  param_1[0x42] = puVar5;
  *(undefined1 *)(param_1 + 0x43) = 0;
  param_1[0x45] = 0;
  param_1[0x44] = 0;
  param_1[0x47] = 0;
  param_1[0x46] = 0;
  *(undefined1 *)(param_1 + 0x48) = 1;
  param_1[0x4c] = 0;
  param_1[0x4e] = 0;
  param_1[0x4d] = 0;
  *(undefined1 *)(param_1 + 0x4b) = 0;
  param_1[0x4a] = 0;
  param_1[0x49] = 0;
  param_1[0x1f] = *(undefined8 *)(param_2 + 0x1c);
  uVar7 = *(ulong *)(param_2 + 0x14);
  *(int *)((long)param_1 + 0x114) = (int)((uVar7 >> 3) / 0x7d);
  param_1[0x20] = ((uVar7 >> 3) / 0x7d & 0xffffffff) * 1000;
  *(int *)((long)param_1 + 0x124) = (int)*(undefined8 *)(param_2 + 0x1e);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_1 + 3,param_2 + 2);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(param_1 + 6,param_2 + 8);
  iVar4 = *param_2;
  if (iVar4 == 0x31) {
    uVar3 = FUN_04ccd978(param_2 + 0xe);
    iVar4 = *param_2;
  }
  else {
    uVar3 = 0;
  }
  local_68 = CONCAT44(uVar3,iVar4);
  *(undefined1 *)(param_1 + 0x4b) = 0;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (param_1 + 0x26,param_2 + 0xe);
  uVar7 = FUN_048ac538(&local_68);
  if (((uVar7 & 1) == 0) &&
     ((*param_2 != 0x2712 || (iVar4 = FUN_048af5d8(param_2 + 0xe,param_4), iVar4 == 0)))) {
    iVar4 = 11000;
  }
  else {
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (param_1 + 0x2c,param_2 + 0x16);
    iVar4 = 10000;
    if (*param_2 != 0x2712) {
      iVar4 = *param_2;
    }
  }
  FUN_04cbbd20(param_1,iVar4);
  *(undefined4 *)(param_1 + 2) = uVar3;
  param_1[0x21] = *(undefined8 *)((long)param_1 + 0xc);
  if ((param_1[0x44] != 0) && (iVar4 = FUN_04a29d84(param_1), iVar4 != 0)) {
    *(undefined4 *)(param_1[0x44] + 0xc) = uVar3;
  }
  uVar3 = 5;
  if (param_3 != 0) {
    uVar3 = 6;
  }
  *(undefined4 *)(param_1 + 0x25) = uVar3;
  iVar4 = FUN_04cbd748(param_1);
  uVar3 = 2;
  if (iVar4 == 0) {
    uVar3 = 4;
  }
  *(undefined4 *)(param_1 + 0x23) = uVar3;
  uVar7 = FUN_04a290c4(param_1);
  if (((((uVar7 & 1) != 0) || (uVar7 = FUN_04a28ecc(param_1), (uVar7 & 1) != 0)) ||
      (uVar7 = FUN_04a29108(param_1), (uVar7 & 1) != 0)) ||
     ((uVar7 = FUN_04a291d0(param_1), (uVar7 & 1) != 0 ||
      (iVar4 = FUN_04a28ef8(param_1), iVar4 != 0)))) {
    FUN_04cbc3ac(param_1,1);
  }
  FUN_04cbbc88(&local_80,param_1);
  FUN_04cbb728(param_1,&local_80);
  if (cStack_69 < '\0') {
    __ZdlPvm(local_80,CONCAT17(cStack_69,local_70) & 0x7fffffffffffffff);
  }
  if (*(int *)((long)param_1 + 0xc) != 11000) goto LAB_04cbd3d8;
  uVar7 = FUN_04cbd748(param_1);
  if ((uVar7 & 1) == 0) {
    if (*(char *)((long)param_1 + 0x5f) < '\0') {
      if (param_1[10] == 0) goto LAB_04cbd32c;
    }
    else if (*(char *)((long)param_1 + 0x5f) == '\0') {
LAB_04cbd32c:
      if (*(int *)(param_1 + 2) == 0x7c) {
        plVar6 = (long *)__Znwm(0x808);
        plVar8 = plVar6 + 1;
        *plVar8 = 0;
        plVar6[2] = 0;
        *plVar6 = (long)&PTR_FUN_09c69900;
        plVar1 = plVar6 + 3;
        _bzero(plVar1,0x7f0);
        FUN_00ad6ec4(plVar1);
        local_80 = plVar1;
        plStack_78 = plVar6;
        (**(code **)(plVar6[3] + 0x18))(plVar1,param_1);
        if (plVar6 != (long *)0x0) {
          LOAcquire();
          lVar2 = *plVar8;
          *plVar8 = lVar2 + -1;
          LORelease();
          if (lVar2 == 0) {
            (**(code **)(*plVar6 + 0x10))(plVar6);
            __ZNSt3__119__shared_weak_count14__release_weakEv(plVar6);
          }
        }
      }
    }
  }
  *(undefined1 *)(param_1 + 0x4b) = 0;
  if (*(char *)((long)param_1 + 0x147) < '\0') {
    __ZdlPvm(param_1[0x26],param_1[0x28] & 0x7fffffffffffffff);
  }
  *(undefined1 *)(param_1 + 0x26) = 0;
  *(undefined1 *)((long)param_1 + 0x147) = 0;
LAB_04cbd3d8:
  *(undefined1 *)(param_1 + 0x48) = 0;
  FUN_04cbc4c0(param_1,0);
  return param_1;
}


