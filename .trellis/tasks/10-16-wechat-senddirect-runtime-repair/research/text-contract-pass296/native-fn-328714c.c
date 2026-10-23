// Ghidra inferred pseudocode; requested=0x328714c
// entry=0328714c end=032872f3

void FUN_0328714c(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
                 undefined8 param_5,undefined8 param_6)

{
  long lVar1;
  undefined4 local_294;
  undefined **local_290;
  undefined1 *puStack_288;
  undefined1 *puStack_280;
  undefined1 *puStack_278;
  undefined1 *local_270;
  undefined1 *puStack_268;
  undefined1 *puStack_260;
  undefined1 *puStack_258;
  undefined1 *local_250;
  undefined1 *puStack_248;
  undefined1 *puStack_240;
  undefined **local_238;
  undefined1 *local_230;
  undefined1 *puStack_228;
  undefined1 *puStack_220;
  undefined1 *puStack_218;
  undefined1 *local_210;
  undefined1 *puStack_208;
  undefined1 *local_200;
  undefined **ppuStack_1f8;
  undefined1 *puStack_1f0;
  undefined1 *puStack_1e8;
  undefined1 *local_1e0;
  undefined **local_1d8 [11];
  undefined1 auStack_180 [64];
  undefined1 auStack_140 [200];
  long local_78;
  
  local_78 = *(long *)PTR____stack_chk_guard_09b36c98;
  local_1e0 = &SUB_aaaaaaaaaaaaaaaa;
  ppuStack_1f8 = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
  local_200 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1e8 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_1f0 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_208 = &SUB_aaaaaaaaaaaaaaaa;
  local_210 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_228 = &SUB_aaaaaaaaaaaaaaaa;
  local_230 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_218 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_220 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_248 = &SUB_aaaaaaaaaaaaaaaa;
  local_250 = &SUB_aaaaaaaaaaaaaaaa;
  local_238 = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
  puStack_240 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_268 = &SUB_aaaaaaaaaaaaaaaa;
  local_270 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_258 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_260 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_288 = &SUB_aaaaaaaaaaaaaaaa;
  local_290 = (undefined **)&SUB_aaaaaaaaaaaaaaaa;
  puStack_278 = &SUB_aaaaaaaaaaaaaaaa;
  puStack_280 = &SUB_aaaaaaaaaaaaaaaa;
  FUN_032a1020(local_1d8);
  lVar1 = FUN_032a10f0(local_1d8,param_3);
  FUN_056f5490(&local_290,lVar1);
  local_290 = &PTR_FUN_09da6548;
  FUN_056c2744(&local_238,lVar1 + 0x58);
  local_238 = &PTR_thunk_FUN_056c2628_09f21aa8;
  local_290 = &PTR_FUN_09df2148;
  FUN_027082b8(&puStack_1f0,lVar1 + 0xa0);
  ppuStack_1f8 = &PTR_FUN_09f249b8;
  FUN_056fad38(auStack_140);
  local_1d8[0] = &PTR_FUN_09da6548;
  thunk_FUN_056c2628(auStack_180);
  FUN_056f54fc(local_1d8);
  local_294 = 1;
  FUN_026f32ac(local_1d8,&local_294);
  FUN_02706f58(param_2,&local_290,param_4,param_5,local_1d8,param_6);
  FUN_056cd5a8(local_1d8);
  FUN_032a11e4(param_1,&local_290);
  FUN_056fad38(&ppuStack_1f8);
  local_290 = &PTR_FUN_09da6548;
  thunk_FUN_056c2628(&local_238);
  FUN_056f54fc(&local_290);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_78) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


