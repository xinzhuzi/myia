// Ghidra inferred pseudocode; requested=0x4541f78
// entry=04541f78 end=0454232f

void FUN_04541f78(long param_1,undefined8 *param_2)

{
  ulong uVar1;
  undefined8 *******pppppppuVar2;
  long *plVar3;
  undefined8 *****pppppuVar4;
  undefined8 *******pppppppuVar5;
  long lVar6;
  long *plVar7;
  long *plVar8;
  long lVar9;
  char *pcVar10;
  undefined1 *local_b0;
  long *local_a8;
  undefined1 auStack_a0 [8];
  long *local_98;
  undefined8 *****local_90;
  long *local_88;
  undefined1 *local_80;
  long *local_78;
  undefined8 ******local_70;
  long *local_68;
  undefined8 local_60;
  long *local_58;
  
  pppppppuVar2 = (undefined8 *******)*param_2;
  plVar3 = (long *)param_2[1];
  if (plVar3 == (long *)0x0) {
    lVar9 = *(long *)(param_1 + 8);
    local_68 = (long *)0x0;
    pppppppuVar5 = pppppppuVar2;
  }
  else {
    plVar8 = plVar3 + 1;
    *plVar8 = *plVar8 + 1;
    lVar9 = *(long *)(param_1 + 8);
    pppppppuVar5 = (undefined8 *******)*plVar8;
    *plVar8 = (long)pppppppuVar5 + 1;
    local_68 = plVar3;
  }
  local_60 = 0;
  local_70 = pppppppuVar2;
  FUN_04542474(pppppppuVar5,lVar9 + 0x28,param_1 + 0x10,&local_70);
  plVar8 = local_68;
  if (local_68 != (long *)0x0) {
    LOAcquire();
    lVar6 = local_68[1];
    local_68[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*local_68 + 0x10))(local_68);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    }
  }
  local_80 = &SUB_aaaaaaaaaaaaaaaa;
  local_78 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  (**(code **)(**(long **)(param_1 + 0x18) + 0x18))(&local_80);
  local_90 = (undefined8 *****)&SUB_aaaaaaaaaaaaaaaa;
  local_88 = (long *)&SUB_aaaaaaaaaaaaaaaa;
  pcVar10 = *(char **)(param_1 + 0x10);
  plVar8 = *(long **)(param_1 + 0x18);
  plVar7 = (long *)_strlen(pcVar10);
  if ((long *)0x7ffffffffffffff7 < plVar7) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_70);
  }
  if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar7) {
    uVar1 = 0x19;
    if (((ulong)plVar7 | 7) != 0x17) {
      uVar1 = ((ulong)plVar7 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_60 = uVar1 | 0x8000000000000000;
    local_70 = pppppppuVar5;
    local_68 = plVar7;
LAB_0454208c:
    _memmove(pppppppuVar5,pcVar10,(size_t)plVar7);
  }
  else {
    local_60 = CONCAT17((char)plVar7,(undefined7)local_60);
    pppppppuVar5 = &local_70;
    if (plVar7 != (long *)0x0) goto LAB_0454208c;
  }
  *(undefined1 *)((long)pppppppuVar5 + (long)plVar7) = 0;
  local_b0 = local_80;
  local_a8 = local_78;
  if (local_78 != (long *)0x0) {
    local_78[1] = local_78[1] + 1;
  }
  FUN_04540e80(auStack_a0,lVar9,&local_70,&local_b0);
  (**(code **)(*plVar8 + 0x20))(&local_90,plVar8,auStack_a0);
  if (local_98 != (long *)0x0) {
    LOAcquire();
    lVar6 = local_98[1];
    local_98[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*local_98 + 0x10))(local_98);
      __ZNSt3__119__shared_weak_count14__release_weakEv(local_98);
    }
  }
  plVar8 = local_a8;
  if (local_a8 != (long *)0x0) {
    LOAcquire();
    lVar6 = local_a8[1];
    local_a8[1] = lVar6 + -1;
    LORelease();
    if (lVar6 == 0) {
      (**(code **)(*local_a8 + 0x10))(local_a8);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    }
  }
  if ((long)local_60 < 0) {
    __ZdlPvm(local_70,local_60 & 0x7fffffffffffffff);
  }
  pcVar10 = *(char **)(param_1 + 0x10);
  plVar8 = (long *)_strlen(pcVar10);
  if ((long *)0x7ffffffffffffff7 < plVar8) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_70);
  }
  if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar8) {
    uVar1 = 0x19;
    if (((ulong)plVar8 | 7) != 0x17) {
      uVar1 = ((ulong)plVar8 | 7) + 1;
    }
    pppppppuVar5 = (undefined8 *******)__Znwm(uVar1);
    local_60 = uVar1 | 0x8000000000000000;
    local_70 = pppppppuVar5;
    local_68 = plVar8;
  }
  else {
    local_60 = CONCAT17((char)plVar8,(undefined7)local_60);
    pppppppuVar5 = &local_70;
    if (plVar8 == (long *)0x0) goto LAB_045421ac;
  }
  _memmove(pppppppuVar5,pcVar10,(size_t)plVar8);
LAB_045421ac:
  *(undefined1 *)((long)pppppppuVar5 + (long)plVar8) = 0;
  lVar6 = FUN_02aea564(lVar9 + 0x28,&local_70);
  if (lVar6 != 0) {
    FUN_02aeab84(lVar9 + 0x28);
  }
  if ((long)local_60 < 0) {
    __ZdlPvm(local_70,local_60 & 0x7fffffffffffffff);
  }
  plVar8 = local_88;
  pppppuVar4 = local_90;
  local_70 = (undefined8 ******)local_90;
  local_68 = local_88;
  if (local_88 != (long *)0x0) {
    local_88[1] = local_88[1] + 1;
  }
  local_58 = (long *)__Znwm(0x28);
  local_58[1] = (long)pppppuVar4;
  *local_58 = (long)&PTR_FUN_09e87118;
  local_58[2] = (long)plVar8;
  local_58[3] = (long)&PTR_DAT_09e87168;
  local_58[4] = (long)(local_58 + 1);
  FUN_066696dc(pppppppuVar2,&local_58);
  if (local_58 != (long *)0x0) {
    (**(code **)(*local_58 + 8))();
  }
  plVar8 = local_88;
  if (local_88 != (long *)0x0) {
    LOAcquire();
    lVar9 = local_88[1];
    local_88[1] = lVar9 + -1;
    LORelease();
    if (lVar9 == 0) {
      (**(code **)(*local_88 + 0x10))(local_88);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    }
  }
  plVar8 = local_78;
  if (local_78 != (long *)0x0) {
    LOAcquire();
    lVar9 = local_78[1];
    local_78[1] = lVar9 + -1;
    LORelease();
    if (lVar9 == 0) {
      (**(code **)(*local_78 + 0x10))(local_78);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar8);
    }
  }
  if (plVar3 != (long *)0x0) {
    LOAcquire();
    lVar9 = plVar3[1];
    plVar3[1] = lVar9 + -1;
    LORelease();
    if (lVar9 == 0) {
      (**(code **)(*plVar3 + 0x10))(plVar3);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  return;
}


