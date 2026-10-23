// Ghidra inferred pseudocode; requested=0x562e0a8
// entry=0562e0a8 end=0562e10b

undefined8 * FUN_0562e0a8(undefined8 *param_1)

{
  undefined4 *puVar1;
  undefined8 *puVar2;
  
  *param_1 = &PTR____cxa_pure_virtual_09da6188;
  puVar1 = (undefined4 *)__Znwm(4);
  *puVar1 = 0;
  param_1[1] = puVar1;
  puVar2 = (undefined8 *)__Znwm(0x20);
  *puVar2 = &PTR___ZNSt3__119__shared_weak_countD2Ev_09f17608;
  puVar2[1] = 0;
  puVar2[2] = 0;
  puVar2[3] = puVar1;
  param_1[2] = puVar2;
  return param_1;
}


