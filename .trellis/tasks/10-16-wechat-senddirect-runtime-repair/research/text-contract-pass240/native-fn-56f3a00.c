// Ghidra inferred pseudocode; requested=0x56f3a00
// entry=056f3a00 end=056f3b97

void FUN_056f3a00(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
                 undefined8 param_5,undefined8 param_6,undefined8 param_7)

{
  undefined8 uVar1;
  long *plVar2;
  long lVar3;
  long *plVar4;
  undefined **local_230;
  long local_228;
  long *plStack_220;
  long local_218;
  undefined **local_210;
  undefined1 *puStack_208;
  undefined1 *puStack_200;
  undefined1 *puStack_1f8;
  undefined1 *local_1f0;
  undefined1 *puStack_1e8;
  undefined1 *puStack_1e0;
  undefined1 *puStack_1d8;
  undefined1 auStack_1c8 [352];
  long local_68;
  
  local_68 = *(long *)PTR____stack_chk_guard_09b36c98;
  puStack_1e8 = &SUB_aaaaaaaaaaaaaaaa;
  local_1f0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1d8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1e0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_208 = &SUB_aaaaaaaaaaaaaaaa;
  local_210 = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
  puStack_1f8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_200 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_056d7ad0(auStack_1c8);
  uVar1 = FUN_056d7b10(auStack_1c8,param_3);
  FUN_0270766c(&local_230,param_4);
  local_230 = &PTR_FUN_09da65e8;
  uVar1 = FUN_056d7cb4(uVar1,&local_230);
  FUN_056c2744(&local_210,uVar1);
  local_210 = &PTR_thunk_FUN_056c2628_09f21aa8;
  if (local_218 != 0) {
    plVar2 = *(long **)(local_228 + 8);
    lVar3 = *plStack_220;
    *(long **)(lVar3 + 8) = plVar2;
    *plVar2 = lVar3;
    local_218 = 0;
    plVar2 = plStack_220;
    while (plVar2 != &local_228) {
      plVar4 = (long *)plVar2[1];
      FUN_056d0bc4(plVar2 + 2);
      __ZdlPvm(plVar2,0x118);
      plVar2 = plVar4;
    }
  }
  thunk_FUN_056c2628(auStack_1c8);
  local_230 = (undefined **)CONCAT44(local_230._4_4_,1);
  FUN_026f32ac(auStack_1c8,&local_230);
  FUN_056f334c(param_2,&local_210,param_5,param_6,auStack_1c8,param_7);
  FUN_056cd5a8(auStack_1c8);
  FUN_056f3be0(param_1,param_2,&local_210);
  thunk_FUN_056c2628(&local_210);
  if (*(long *)PTR____stack_chk_guard_09b36c98 != local_68) {
                    /* WARNING: Subroutine does not return */
    ___stack_chk_fail();
  }
  return;
}


