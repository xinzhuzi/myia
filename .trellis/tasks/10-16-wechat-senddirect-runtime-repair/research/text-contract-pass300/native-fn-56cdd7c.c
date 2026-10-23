// Ghidra inferred pseudocode; requested=0x56cdd7c
// entry=056cdd7c end=056cdf8f

undefined8 * FUN_056cdd7c(undefined8 *param_1,undefined8 param_2)

{
  long lVar1;
  long lVar2;
  long *plVar3;
  code *pcVar4;
  long alStack_68 [3];
  long *local_50;
  long local_48;
  
  local_48 = *(long *)PTR____stack_chk_guard_09b36c98;
  param_1[0x24] = &PTR____cxa_pure_virtual_09da57d8;
  FUN_056c1e60();
  *param_1 = &PTR_FUN_09da5810;
  param_1[5] = &PTR____cxa_pure_virtual_09f22018;
  param_1[9] = 0;
  param_1[8] = 0;
  param_1[0xb] = 0;
  param_1[10] = 0;
  param_1[0xd] = 0;
  param_1[0xc] = 0;
  param_1[0xf] = 0;
  param_1[0xe] = 0;
  param_1[0x11] = 0;
  param_1[0x10] = 0;
  param_1[0x13] = 0;
  param_1[0x12] = 0;
  param_1[0x15] = 0;
  param_1[0x14] = 0;
  param_1[0x17] = 0;
  param_1[0x16] = 0;
  param_1[0x19] = 0;
  param_1[0x18] = 0;
  param_1[0x1b] = 0;
  param_1[0x1a] = 0;
  param_1[0x1d] = 0;
  param_1[0x1c] = 0;
  param_1[0x1f] = 0;
  param_1[0x1e] = 0;
  param_1[0x21] = 0;
  param_1[0x20] = 0;
  param_1[0x23] = 0;
  param_1[0x22] = 0;
  param_1[7] = 0;
  param_1[6] = 0;
  FUN_056dafd0();
  param_1[5] = &PTR_FUN_09f21e68;
  param_1[0x1f] = param_1 + 0x1f;
  param_1[0x20] = param_1 + 0x1f;
  param_1[0x21] = 0;
  *(undefined1 *)(param_1 + 0x22) = 0xff;
  *(undefined2 *)((long)param_1 + 0x113) = 0;
  *(undefined4 *)((long)param_1 + 0x116) = 0;
  *param_1 = &PTR_FUN_09f1fe78;
  param_1[1] = param_1 + 5;
  param_1[0x24] = &PTR_FUN_09f1fed0;
  param_1[0x25] = &PTR_FUN_09f1ff10;
  param_1[0x26] = &PTR_FUN_09f1ff50;
  param_1[0x27] = &PTR_FUN_09f1ff90;
  param_1[0x28] = &PTR_FUN_09f1ffd0;
  param_1[0x29] = &PTR_FUN_09f20010;
  param_1[0x2a] = &PTR_FUN_09f20050;
  param_1[0x2b] = &PTR_FUN_09f20090;
  lVar1 = FUN_056c252c(param_1);
  *(undefined1 *)(lVar1 + 0xe8) = 3;
  lVar1 = FUN_056c25d4(param_2);
  lVar2 = FUN_056c252c(param_1);
  lVar2 = FUN_056db4b4(lVar2 + 8);
  FUN_0562fddc(lVar2 + 0x10,lVar1 + 0x10);
  FUN_0562fddc(lVar2 + 0x28,lVar1 + 0x28);
  *(undefined1 *)(lVar2 + 0x40) = *(undefined1 *)(lVar1 + 0x40);
  FUN_0562fddc(lVar2 + 0x48,lVar1 + 0x48);
  plVar3 = *(long **)(lVar1 + 0x78);
  local_50 = (long *)0x0;
  if (plVar3 != (long *)0x0) {
    if (plVar3 == (long *)(lVar1 + 0x60)) {
      local_50 = alStack_68;
      (**(code **)(*plVar3 + 0x18))(plVar3,alStack_68);
    }
    else {
      local_50 = (long *)(**(code **)(*plVar3 + 0x10))();
    }
  }
  FUN_027056cc(alStack_68,lVar2 + 0x60);
  if (local_50 == alStack_68) {
    pcVar4 = *(code **)(*local_50 + 0x20);
  }
  else {
    if (local_50 == (long *)0x0) goto LAB_056cdf50;
    pcVar4 = *(code **)(*local_50 + 0x28);
  }
  (*pcVar4)();
LAB_056cdf50:
  *(undefined8 *)(lVar2 + 0x80) = *(undefined8 *)(lVar1 + 0x80);
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_48) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return param_1;
}


