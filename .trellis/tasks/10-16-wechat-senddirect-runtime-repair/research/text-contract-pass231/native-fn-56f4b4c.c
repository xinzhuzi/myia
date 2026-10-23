// Ghidra inferred pseudocode; requested=0x56f4b4c
// entry=056f4b4c end=056f4c67

undefined8 FUN_056f4b4c(long param_1,undefined8 *param_2)

{
  long *plVar1;
  code *pcVar2;
  undefined8 uVar3;
  undefined **local_120 [4];
  long alStack_100 [3];
  long *local_e8;
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
  undefined1 *local_60;
  undefined1 *puStack_58;
  undefined1 *puStack_50;
  undefined1 *puStack_48;
  undefined1 *local_40;
  long local_38;
  
  local_38 = *(long *)PTR____stack_chk_guard_09b36c98;
  uVar3 = *param_2;
  local_40 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_58 = &SUB_aaaaaaaaaaaaaaaa;
  local_60 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_48 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_50 = &SUB_aaaaaaaaaaaaaaaa;
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
  (**(code **)(**(long **)(param_1 + 0x28) + 0x18))(local_120);
  FUN_056f8bfc(&local_e0,local_120,uVar3);
  local_120[0] = &PTR_FUN_09da6148;
  FUN_0562e260(local_120);
  if (local_e8 == alStack_100) {
    pcVar2 = *(code **)(*local_e8 + 0x20);
  }
  else {
    if (local_e8 == (long *)0x0) goto LAB_056f4c00;
    pcVar2 = *(code **)(*local_e8 + 0x28);
  }
  (*pcVar2)();
LAB_056f4c00:
  FUN_0562e140(local_120);
  plVar1 = *(long **)(param_1 + 0x20);
  if (plVar1 == (long *)0x0) {
                    /* WARNING: Subroutine does not return */
    FUN_0021eccc();
  }
  uVar3 = (**(code **)(*plVar1 + 0x30))(plVar1,&local_e0);
  thunk_FUN_056f8c84(&local_e0);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_38) {
    return uVar3;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


