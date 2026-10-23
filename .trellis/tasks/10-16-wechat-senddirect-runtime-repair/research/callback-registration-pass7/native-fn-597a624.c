// Ghidra inferred pseudocode; requested=0x597a624
// entry=0597a624 end=0597a7d3

undefined8 * FUN_0597a624(undefined8 *param_1,undefined8 param_2)

{
  undefined8 ***pppuVar1;
  long lVar2;
  long *plVar3;
  undefined8 **local_168;
  undefined8 uStack_160;
  long local_158;
  code *local_150;
  long *plStack_148;
  undefined8 *local_140;
  undefined8 uStack_138;
  undefined8 local_130;
  undefined8 uStack_128;
  undefined8 uStack_120;
  undefined8 uStack_118;
  undefined8 local_110;
  undefined8 uStack_108;
  undefined8 uStack_100;
  undefined8 uStack_f8;
  undefined8 local_f0;
  undefined8 uStack_e8;
  undefined8 uStack_e0;
  undefined8 uStack_d8;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  *param_1 = &PTR_thunk_FUN_0597a93c_09f2e3e8;
  param_1[1] = param_2;
  param_1[0xb] = 0;
  param_1[0xf] = 0;
  param_1[3] = 0;
  param_1[2] = 0;
  param_1[5] = 0;
  param_1[4] = 0;
  param_1[7] = 0;
  param_1[6] = 0;
  FUN_05974418();
  lVar2 = FUN_059738d8(param_2);
  local_150 = FUN_0597a7d4;
  plStack_148 = (long *)0x0;
  local_140 = param_1;
  FUN_0597a878(lVar2 + 0x10,&local_150);
  plVar3 = (long *)__Znwm(0xa0);
  plVar3[2] = 0;
  *plVar3 = (long)&PTR_FUN_09f2e4e8;
  plVar3[1] = 0;
  local_150 = (code *)thunk_FUN_05a2512c(plVar3 + 3,param_2);
  plStack_148 = plVar3;
  FUN_0596281c(param_1 + 6,&local_150);
  plVar3 = plStack_148;
  if (plStack_148 != (long *)0x0) {
    LOAcquire();
    lVar2 = plStack_148[1];
    plStack_148[1] = lVar2 + -1;
    LORelease();
    if (lVar2 == 0) {
      (**(code **)(*plStack_148 + 0x10))(plStack_148);
      __ZNSt3__119__shared_weak_count14__release_weakEv(plVar3);
    }
  }
  local_168 = (undefined8 ***)0x0;
  uStack_160 = 0;
  local_158 = 0;
  __ZNSt3__112basic_stringIcNS_11char_traitsIcEENS_9allocatorIcEEE7reserveEm(&local_168,0x200);
  uStack_e8 = 0;
  local_f0 = 0;
  uStack_d8 = 0;
  uStack_e0 = 0;
  uStack_108 = 0;
  local_110 = 0;
  uStack_f8 = 0;
  uStack_100 = 0;
  uStack_128 = 0;
  local_130 = 0;
  uStack_118 = 0;
  uStack_120 = 0;
  plStack_148 = (long *)0x0;
  local_150 = (code *)0x0;
  uStack_138 = 0;
  local_140 = (undefined8 *)0x0;
  FUN_05e1d898(&local_168,"mars2",&local_150);
  pppuVar1 = (undefined8 ***)local_168;
  if (-1 < local_158) {
    pppuVar1 = &local_168;
  }
  thunk_FUN_05e1d500(&local_150,0,"mars::mmext","MMStnManager","mmstn_manager.cc","MMStnManager",
                     0x3a,pppuVar1);
  if (local_158 < 0) {
    __ZdlPv(local_168);
  }
  thunk_FUN_05e1d684(&local_150);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return param_1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


