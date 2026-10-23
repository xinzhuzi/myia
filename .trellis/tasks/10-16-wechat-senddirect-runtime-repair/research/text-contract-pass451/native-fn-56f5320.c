// Ghidra inferred pseudocode; requested=0x56f5320
// entry=056f5320 end=056f5433

undefined8 * FUN_056f5320(undefined8 *param_1,undefined8 param_2)

{
  undefined8 uVar1;
  undefined8 *puVar2;
  code *pcVar3;
  undefined **local_78 [4];
  long alStack_58 [3];
  long *local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  *param_1 = &PTR____cxa_pure_virtual_09f23978;
  uVar1 = __Znwm(0xa8);
  FUN_02704484(local_78,param_2);
  FUN_056f8b78(uVar1,local_78);
  param_1[1] = uVar1;
  puVar2 = (undefined8 *)__Znwm(0x20);
  *puVar2 = &PTR___ZNSt3__119__shared_weak_countD2Ev_09f23998;
  puVar2[1] = 0;
  puVar2[2] = 0;
  puVar2[3] = uVar1;
  param_1[2] = puVar2;
  local_78[0] = &PTR_FUN_09da6148;
  FUN_0562e260(local_78);
  if (local_40 == alStack_58) {
    pcVar3 = *(code **)(*local_40 + 0x20);
  }
  else {
    if (local_40 == (long *)0x0) goto LAB_056f53f0;
    pcVar3 = *(code **)(*local_40 + 0x28);
  }
  (*pcVar3)();
LAB_056f53f0:
  FUN_0562e140(local_78);
  FUN_05632dcc(param_1 + 4);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return param_1;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


