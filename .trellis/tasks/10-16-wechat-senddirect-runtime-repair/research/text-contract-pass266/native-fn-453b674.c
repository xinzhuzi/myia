// Ghidra inferred pseudocode; requested=0x453b674
// entry=0453b674 end=0453ba57

long ** FUN_0453b674(long **param_1)

{
  ulong uVar1;
  long lVar2;
  long *plVar3;
  size_t sVar4;
  undefined8 uVar5;
  long ****pppplVar6;
  long ***ppplVar7;
  code *pcVar8;
  long **local_a0;
  long *local_98;
  long ***local_90;
  code *local_88;
  undefined8 local_80;
  undefined8 local_78;
  code *pcStack_70;
  undefined **local_68 [3];
  undefined ***local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  plVar3 = (long *)__Znwm(0x148);
  if ((DAT_0a455747 & 1) == 0) {
    DAT_0a455740 = (undefined4)DAT_084b0358;
    DAT_0a455744 = 0x6c65;
    DAT_0a455746 = 0;
    DAT_0a455747 = 1;
  }
  sVar4 = _strlen((char *)&DAT_0a455740);
  if (0x7ffffffffffffff7 < sVar4) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_90);
  }
  if (sVar4 < 0x17) {
    local_80 = (code *)CONCAT17((char)sVar4,(undefined7)local_80);
    pppplVar6 = &local_90;
    if (sVar4 != 0) goto LAB_0453b740;
  }
  else {
    uVar1 = 0x19;
    if ((sVar4 | 7) != 0x17) {
      uVar1 = (sVar4 | 7) + 1;
    }
    pppplVar6 = (long ****)__Znwm(uVar1);
    local_80 = (code *)(uVar1 | 0x8000000000000000);
    local_90 = (long ***)pppplVar6;
    local_88 = (code *)sVar4;
LAB_0453b740:
    _memcpy(pppplVar6,&DAT_0a455740,sVar4);
  }
  *(undefined1 *)((long)pppplVar6 + sVar4) = 0;
  FUN_066845d0(plVar3,&local_90);
  if ((long)local_80 < 0) {
    __ZdlPvm(local_90,(ulong)local_80 & 0x7fffffffffffffff);
  }
  param_1[7] = (long *)0x0;
  *(undefined1 *)(param_1 + 8) = 0;
  param_1[2] = (long *)0x0;
  param_1[3] = (long *)0x0;
  param_1[1] = plVar3;
  uVar5 = FUN_0668da74();
  FUN_0668dddc(uVar5,2);
  local_88 = (code *)__Znwm(0x20);
  *(long *)((long)local_88 + 8) = 0;
  *(long *)((long)local_88 + 0x10) = 0;
  *(undefined ***)local_88 = &PTR_FUN_09e86e78;
  local_90 = (long ***)((long)local_88 + 0x18);
  *local_90 = (long **)&PTR_FUN_09e86ec8;
  local_a0 = (long **)0x0;
  local_98 = (long *)0x0;
  uVar5 = FUN_0668da74();
  FUN_0668dbbc(uVar5,&local_90);
  pcVar8 = local_88;
  if (local_88 != (code *)0x0) {
    LOAcquire();
    lVar2 = *(long *)((long)local_88 + 8);
    *(long *)((long)local_88 + 8) = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*(long *)local_88 + 0x10))(local_88);
      __ZNSt3__119__shared_weak_count14__release_weakEv(pcVar8);
    }
  }
  plVar3 = local_98;
  if (local_98 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_98[1];
    local_98[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_98 + 0x10))(local_98);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  if ((DAT_0a455752 & 1) == 0) {
    DAT_0a455748._0_1_ = s_coroutinCoAsync_087e2ce0[0];
    DAT_0a455748._1_1_ = s_coroutinCoAsync_087e2ce0[1];
    DAT_0a455748._2_1_ = s_coroutinCoAsync_087e2ce0[2];
    DAT_0a455748._3_1_ = s_coroutinCoAsync_087e2ce0[3];
    DAT_0a455748._4_1_ = s_coroutinCoAsync_087e2ce0[4];
    DAT_0a455748._5_1_ = s_coroutinCoAsync_087e2ce0[5];
    DAT_0a455748._6_1_ = s_coroutinCoAsync_087e2ce0[6];
    DAT_0a455748._7_1_ = s_coroutinCoAsync_087e2ce0[7];
    DAT_0a455750 = 0x65;
    DAT_0a455752 = 1;
  }
  plVar3 = (long *)_strlen((char *)&DAT_0a455748);
  if ((long *)0x7ffffffffffffff7 < plVar3) {
                    /* WARNING: Subroutine does not return */
    FUN_00018d9c(&local_90);
  }
  if ((long *)((long)&MACH_HEADER.sizeofcmds + 2) < plVar3) {
    uVar1 = 0x19;
    if (((ulong)plVar3 | 7) != 0x17) {
      uVar1 = ((ulong)plVar3 | 7) + 1;
    }
    pppplVar6 = (long ****)__Znwm(uVar1);
    local_80 = (code *)(uVar1 | 0x8000000000000000);
    local_90 = (long ***)pppplVar6;
    local_88 = (code *)plVar3;
LAB_0453b8bc:
    _memcpy(pppplVar6,&DAT_0a455748,(size_t)plVar3);
  }
  else {
    local_80 = (code *)CONCAT17((char)plVar3,(undefined7)local_80);
    pppplVar6 = &local_90;
    if (plVar3 != (long *)0x0) goto LAB_0453b8bc;
  }
  *(undefined1 *)((long)pppplVar6 + (long)plVar3) = 0;
  local_68[0] = &PTR_FUN_09e86f28;
  local_50 = local_68;
  plVar3 = (long *)FUN_06666da4(&local_90,0x300000,local_68);
  *param_1 = plVar3;
  if (local_50 == local_68) {
    pcVar8 = (code *)(*local_50)[4];
  }
  else {
    if (local_50 == (undefined ***)0x0) goto LAB_0453b924;
    pcVar8 = (code *)(*local_50)[5];
  }
  (*pcVar8)();
LAB_0453b924:
  if ((long)local_80 < 0) {
    __ZdlPvm(local_90,(ulong)local_80 & 0x7fffffffffffffff);
  }
  plVar3 = *param_1;
  lVar2 = FUN_02e0a888(param_1[1]);
  *(long **)(lVar2 + 0x18) = plVar3;
  FUN_0453b474();
  uVar5 = FUN_066769d8();
  ppplVar7 = (long ***)__Znwm(0x20);
  *ppplVar7 = (long **)&PTR_FUN_09e86cf8;
  ppplVar7[1] = param_1;
  ppplVar7[3] = (long **)ppplVar7;
  local_a0 = (long **)ppplVar7;
  local_98 = (long *)__Znwm(0x28);
  *local_98 = (long)&PTR___ZNSt3__119__shared_weak_countD2Ev_09e86ca8;
  local_98[1] = 0;
  local_98[2] = 0;
  local_98[3] = (long)ppplVar7;
  local_98[4] = (long)FUN_0453ef84;
  local_88 = FUN_0453f0e4;
  local_80 = FUN_0453ef40;
  local_78 = 0;
  pcStack_70 = FUN_0453f110;
  local_90 = ppplVar7;
  FUN_06686420(uVar5,&local_90,0,0,0,&local_a0);
  plVar3 = local_98;
  if (local_98 != (long *)0x0) {
    LOAcquire();
    lVar2 = local_98[1];
    local_98[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*local_98 + 0x10))(local_98);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return param_1;
}


