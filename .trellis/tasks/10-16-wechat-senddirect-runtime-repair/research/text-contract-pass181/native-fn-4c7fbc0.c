// Ghidra inferred pseudocode; requested=0x4c7fbc0
// entry=04c7fbc0 end=04c7ff17

void FUN_04c7fbc0(long *param_1,undefined8 param_2,long *param_3)

{
  long lVar1;
  int iVar2;
  undefined8 uVar3;
  long lVar4;
  long *plVar5;
  char cVar6;
  ulong uVar7;
  long local_70;
  long *plStack_68;
  ulong local_60;
  undefined1 *local_50;
  long *local_48;
  long local_40;
  long *local_38;
  
  *param_1 = (long)&SUB_aaaaaaaaaaaaaaaa;
  param_1[1] = (long)&SUB_aaaaaaaaaaaaaaaa;
  local_40 = *param_3;
  local_38 = (long *)param_3[1];
  if (local_38 != (long *)0x0) {
    local_38[1] = local_38[1] + 1;
  }
  FUN_04c6b5b8(param_1,param_2,&local_40);
  plVar5 = local_38;
  if (local_38 != (long *)0x0) {
    LOAcquire();
    lVar1 = local_38[1];
    local_38[1] = lVar1 + -1;
    LORelease();
    if (lVar1 == 0) {
      (**(code **)(*local_38 + 0x10))(local_38);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
    }
  }
  lVar1 = *param_3;
  uVar7 = (ulong)*(uint *)(lVar1 + 8);
  if (*(uint *)(lVar1 + 8) == 0x31) {
    uVar7 = (ulong)*(uint *)(lVar1 + 0xc) << 0x20 | 0x31;
  }
  if ((long)uVar7 < 0x3500000031) {
    if (uVar7 != 1) {
      if (uVar7 != 0x100000031) {
        return;
      }
      goto LAB_04c7fd00;
    }
    iVar2 = FUN_048a60b4(lVar1);
    if (iVar2 == 0) {
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (*param_1 + 0x148,*param_3 + 0xb8);
      return;
    }
    local_50 = &SUB_aaaaaaaaaaaaaaaa;
    local_48 = (long *)&SUB_aaaaaaaaaaaaaaaa;
    FUN_039ee5e4(&local_50,*param_3);
    lVar1 = *param_1;
    FUN_04cc0ca0(&local_70,local_50);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
              (lVar1 + 0x148,&local_70);
    plVar5 = local_48;
    if ((long)local_60 < 0) {
      __ZdlPvm(local_70,local_60 & 0x7fffffffffffffff);
      plVar5 = local_48;
    }
  }
  else if (uVar7 == 0x3500000031) {
LAB_04c7fd00:
    if ((*(long *)(lVar1 + 0x218) == 0) ||
       (local_70 = ___dynamic_cast(*(long *)(lVar1 + 0x218),&PTR_DAT_09eb1040,&PTR_DAT_09eb0cc0,0),
       local_70 == 0)) {
      local_70 = 0;
      plStack_68 = (long *)0x0;
    }
    else {
      plStack_68 = *(long **)(lVar1 + 0x220);
      if (plStack_68 != (long *)0x0) {
        plStack_68[1] = plStack_68[1] + 1;
      }
    }
    lVar1 = *param_1;
    uVar3 = FUN_04cd61bc(local_70);
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(lVar1 + 0x148,uVar3);
    plVar5 = plStack_68;
  }
  else {
    if (uVar7 == 0x5700000031) {
      if ((*(long *)(lVar1 + 0x218) == 0) ||
         (local_50 = (undefined1 *)
                     ___dynamic_cast(*(long *)(lVar1 + 0x218),&PTR_DAT_09eb1040,&PTR_DAT_09eb0cc0,0)
         , local_50 == (undefined1 *)0x0)) {
        local_50 = (undefined1 *)0x0;
        local_48 = (long *)0x0;
      }
      else {
        local_48 = *(long **)(lVar1 + 0x220);
        if (local_48 != (long *)0x0) {
          local_48[1] = local_48[1] + 1;
        }
      }
      plVar5 = local_48;
      lVar1 = *param_1;
      if ((char)local_50[0x6f7] < '\0') {
        FUN_00018d20(&local_70,*(undefined8 *)(local_50 + 0x6e0),*(undefined8 *)(local_50 + 0x6e8));
      }
      else {
        plStack_68 = *(long **)(local_50 + 0x6e8);
        local_70 = *(long *)(local_50 + 0x6e0);
        local_60 = *(ulong *)(local_50 + 0x6f0);
      }
      __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
                (lVar1 + 0x148,&local_70);
      if ((long)local_60 < 0) {
        __ZdlPvm(local_70,local_60 & 0x7fffffffffffffff);
      }
      if (plVar5 == (long *)0x0) {
        return;
      }
      LOAcquire();
      lVar1 = plVar5[1];
      plVar5[1] = lVar1 + -1;
      LORelease();
      if (lVar1 != 0) {
        return;
      }
      (**(code **)(*plVar5 + 0x10))(plVar5);
      goto LAB_04c7ff00;
    }
    if (uVar7 != 0x8b00000031) {
      return;
    }
    if ((*(long *)(lVar1 + 0x218) == 0) ||
       (local_70 = ___dynamic_cast(*(long *)(lVar1 + 0x218),&PTR_DAT_09eb1040,&PTR_DAT_09eb0cc0,0),
       local_70 == 0)) {
      local_70 = 0;
      plStack_68 = (long *)0x0;
      cVar6 = section_00000248.size._7_1_;
      if (section_00000248.size._7_1_ < '\0') goto LAB_04c7fe40;
LAB_04c7fcd8:
      lVar1 = *param_1;
      if (cVar6 != '\0') goto LAB_04c7fce0;
LAB_04c7fe4c:
      lVar4 = FUN_04cd61bc();
    }
    else {
      plStack_68 = *(long **)(lVar1 + 0x220);
      if (plStack_68 != (long *)0x0) {
        plStack_68[1] = plStack_68[1] + 1;
      }
      cVar6 = *(char *)(local_70 + 0x277);
      if (-1 < *(char *)(local_70 + 0x277)) goto LAB_04c7fcd8;
LAB_04c7fe40:
      lVar1 = *param_1;
      if (*(long *)(local_70 + 0x268) == 0) goto LAB_04c7fe4c;
LAB_04c7fce0:
      lVar4 = local_70 + 0x260;
    }
    __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(lVar1 + 0x148,lVar4);
    plVar5 = plStack_68;
  }
  if (plVar5 == (long *)0x0) {
    return;
  }
  LOAcquire();
  lVar1 = plVar5[1];
  plVar5[1] = lVar1 + -1;
  LORelease();
  if (lVar1 != 0) {
    return;
  }
  (**(code **)(*plVar5 + 0x10))(plVar5);
LAB_04c7ff00:
  __ZNSt3__119__shared_weak_count14__release_weakEv(plVar5);
  return;
}


