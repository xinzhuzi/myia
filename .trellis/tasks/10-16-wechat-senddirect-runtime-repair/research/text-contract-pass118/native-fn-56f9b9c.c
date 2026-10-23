// Ghidra inferred pseudocode; requested=0x56f9b9c
// entry=056f9b9c end=056f9d1f

long FUN_056f9b9c(long param_1,undefined8 param_2,undefined8 param_3,undefined **param_4)

{
  long lVar1;
  long *plVar2;
  long *plVar3;
  undefined8 local_230;
  undefined1 local_221;
  undefined1 *local_220 [28];
  undefined1 auStack_140 [24];
  undefined **local_128 [28];
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_230 = param_2;
  FUN_0562fd3c(auStack_140,param_3);
  local_220[0] = (undefined1 *)&local_230;
  local_128[0] = param_4;
  lVar1 = FUN_056fa15c(param_1 + 0xd8,&local_230,&DAT_08b7a8b8,local_220,&local_221);
  FUN_05630ba8(lVar1 + 0x28,auStack_140);
  *(undefined ***)(lVar1 + 0x40) = local_128[0];
  FUN_0562fd84(auStack_140);
  local_221 = (**(code **)(*param_4 + 0x10))(param_4);
  FUN_056f9e2c(local_220,param_3,&local_221);
  FUN_0562fd3c(auStack_140,param_3);
  FUN_038c879c(local_128,local_220);
  local_128[0] = &PTR_FUN_09f1fe20;
  FUN_056f9d84(param_1 + 8,auStack_140);
  FUN_056cd2f4(local_128);
  FUN_0562fd84(auStack_140);
  FUN_056cd2f4(local_220);
  plVar2 = (long *)__Znwm(0x108);
  *plVar2 = 0;
  plVar2[1] = 0;
  FUN_056fa274(plVar2 + 2,param_3,param_4);
  plVar3 = (long *)(param_1 + 0xf8);
  lVar1 = *plVar3;
  *plVar2 = lVar1;
  plVar2[1] = (long)plVar3;
  *(long **)(lVar1 + 8) = plVar2;
  *plVar3 = (long)plVar2;
  *(long *)(param_1 + 0x108) = *(long *)(param_1 + 0x108) + 1;
  lVar1 = FUN_056c252c(plVar2 + 2);
  *(long *)(lVar1 + 0x80) = param_1;
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_48) {
    return *plVar3 + 0x10;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


