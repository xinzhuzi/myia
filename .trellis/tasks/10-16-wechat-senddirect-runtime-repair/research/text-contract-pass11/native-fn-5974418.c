// Ghidra inferred pseudocode; requested=0x5974418
// entry=05974418 end=0597462b

void FUN_05974418(void)

{
  undefined1 auStack_130 [264];
  long local_28;
  
  local_28 = *(long *)PTR____stack_chk_guard_09b36c98;
  thunk_FUN_05e1d500(auStack_130,2,"mars::mmext","InitStaticFuncPtr","mmstn_logic.cc",
                     "InitStaticFuncPtr",0x197,0);
  PTR_FUN_0a124e48 = FUN_0597462c;
  FUN_05974768(&DAT_0a525490,FUN_05a20400);
  FUN_05974808(&DAT_0a5254b0,FUN_05a208f4);
  FUN_059748a8(&DAT_0a5254d0,FUN_05a20a24);
  FUN_05974948(&DAT_0a5254f0,FUN_05a20d88);
  FUN_059749e8(&DAT_0a525510,FUN_05a20ed4);
  PTR_FUN_0a124b90 = FUN_05973938;
  PTR_FUN_0a124b98 = FUN_05973a80;
  PTR_FUN_0a124ba0 = FUN_05973bbc;
  PTR_FUN_0a124ba8 = FUN_05973d04;
  PTR_FUN_0a124bb0 = FUN_05973e30;
  PTR_FUN_0a124bc8 = FUN_05973f5c;
  PTR_FUN_0a124bd0 = FUN_05974088;
  PTR_FUN_0a124be8 = FUN_059741c0;
  PTR_FUN_0a124bf0 = FUN_059742ec;
  PTR_FUN_0a124bc0 = FUN_05973740;
  PTR_FUN_0a124bf8 = FUN_05974a88;
  PTR_FUN_0a124c08 = FUN_05974bc4;
  PTR_FUN_0a124c00 = FUN_05974d00;
  FUN_05974fb4(&DAT_0a525668,FUN_05974e3c);
  thunk_FUN_05e1d684(auStack_130);
  if (*(long *)PTR____stack_chk_guard_09b36c98 == local_28) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  ___stack_chk_fail();
}


