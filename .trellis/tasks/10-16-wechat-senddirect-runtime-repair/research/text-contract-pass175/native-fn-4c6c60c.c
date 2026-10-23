// Ghidra inferred pseudocode; requested=0x4c6c60c
// entry=04c6c60c end=04c6c85f

void FUN_04c6c60c(undefined8 *param_1,long param_2,long *param_3)

{
  void *pvVar1;
  size_t sVar2;
  code *pcVar3;
  undefined8 *puVar4;
  undefined8 uVar5;
  void *pvVar6;
  long *plVar7;
  void *local_150;
  void *local_148;
  void *local_140;
  undefined8 uStack_138;
  undefined1 *local_130;
  undefined1 *puStack_128;
  undefined1 *local_120;
  undefined1 *puStack_118;
  undefined1 *puStack_110;
  undefined1 *puStack_108;
  undefined1 *local_100;
  undefined1 *puStack_f8;
  undefined1 *puStack_f0;
  undefined1 *puStack_e8;
  undefined1 *local_e0;
  undefined1 *puStack_d8;
  undefined1 *puStack_d0;
  undefined1 *puStack_c8;
  undefined1 *local_c0;
  undefined1 *puStack_b8;
  undefined1 *puStack_b0;
  undefined1 *puStack_a8;
  undefined1 *local_a0;
  undefined1 *puStack_98;
  undefined1 *puStack_90;
  undefined1 *puStack_88;
  undefined1 *local_80;
  undefined1 *puStack_78;
  undefined1 *puStack_70;
  undefined1 *puStack_68;
  long local_58;
  
  local_58 = *(long *)PTR____stack_chk_guard_09b36c98;
  *param_1 = &SUB_aaaaaaaaaaaaaaaa;
  param_1[1] = &SUB_aaaaaaaaaaaaaaaa;
  puVar4 = (undefined8 *)__Znwm(0x678);
  puVar4[1] = 0;
  puVar4[2] = 0;
  *puVar4 = &PTR_FUN_09cb06b8;
  uVar5 = FUN_04d56fd0(puVar4 + 3,param_3);
  *param_1 = uVar5;
  param_1[1] = puVar4;
  puStack_78 = &SUB_aaaaaaaaaaaaaaaa;
  local_80 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_68 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_70 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_98 = &SUB_aaaaaaaaaaaaaaaa;
  local_a0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_88 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_90 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_b8 = &SUB_aaaaaaaaaaaaaaaa;
  local_c0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_a8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_b0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_d8 = &SUB_aaaaaaaaaaaaaaaa;
  local_e0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_c8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_d0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_f8 = &SUB_aaaaaaaaaaaaaaaa;
  local_100 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_e8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_f0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_118 = &SUB_aaaaaaaaaaaaaaaa;
  local_120 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_108 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_110 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_128 = &SUB_aaaaaaaaaaaaaaaa;
  local_130 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_0572111c(&local_130);
  if ((DAT_0a4ab7e9 & 1) == 0) {
    DAT_0a4ab7e0._0_1_ = s_new_nodesession_08ad06b0[0];
    DAT_0a4ab7e0._1_1_ = s_new_nodesession_08ad06b0[1];
    DAT_0a4ab7e0._2_1_ = s_new_nodesession_08ad06b0[2];
    DAT_0a4ab7e0._3_1_ = s_new_nodesession_08ad06b0[3];
    DAT_0a4ab7e0._4_1_ = s_new_nodesession_08ad06b0[4];
    DAT_0a4ab7e0._5_1_ = s_new_nodesession_08ad06b0[5];
    DAT_0a4ab7e0._6_1_ = s_new_nodesession_08ad06b0[6];
    DAT_0a4ab7e0._7_1_ = s_new_nodesession_08ad06b0[7];
    DAT_0a4ab7e8 = 0;
    DAT_0a4ab7e9 = 1;
  }
  uStack_138 = FUN_0571d610(&local_130,&DAT_0a4ab7e0);
  local_140 = (void *)0x0;
  local_150 = (void *)0x0;
  local_148 = (void *)0x0;
  pvVar1 = *(void **)(param_2 + 0x10);
  sVar2 = *(long *)(param_2 + 0x18) - (long)pvVar1;
  if (sVar2 == 0) {
    pvVar6 = (void *)0x0;
  }
  else {
    if ((long)sVar2 < 0) {
      FUN_00801dbc(&local_150);
                    /* WARNING: Does not return */
      pcVar3 = (code *)SoftwareBreakpoint(1,0x4c6c860);
      (*pcVar3)();
    }
    pvVar6 = (void *)__Znwm(sVar2);
    local_150 = pvVar6;
    local_140 = (void *)((long)pvVar6 + sVar2);
    _memcpy(pvVar6,pvVar1,sVar2);
    local_148 = (void *)((long)pvVar6 + sVar2);
  }
  FUN_0153c914(puVar4 + 0xb7,pvVar6,local_148,(long)local_148 - (long)pvVar6 >> 2);
  if (local_150 != (void *)0x0) {
    local_148 = local_150;
    __ZdlPvm(local_150,(long)local_140 - (long)local_150);
  }
  (**(code **)(*param_3 + 600))(param_3,&uStack_138);
  plVar7 = (long *)*param_1;
  (**(code **)(*plVar7 + 0x260))(plVar7,&uStack_138);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (plVar7 + 0x17,param_3 + 0x17);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (plVar7 + 0x23,param_3 + 0x23);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (plVar7 + 0x2c,param_3 + 0x2c);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (plVar7 + 0x4c,param_3 + 0x4c);
  *(int *)(plVar7 + 0x2f) = (int)param_3[0x2f];
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (plVar7 + 0x30,param_3 + 0x30);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (plVar7 + 0x33,param_3 + 0x33);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (plVar7 + 0x37,param_3 + 0x37);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (plVar7 + 0x3a,param_3 + 0x3a);
  plVar7[0x5b] = param_3[0x5b];
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (plVar7 + 0x5d,param_3 + 0x5d);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_
            (plVar7 + 0x60,param_3 + 0x60);
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEEaSERKS5_(plVar7 + 99,param_3 + 99)
  ;
  FUN_0572116c(&local_130);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_58) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


