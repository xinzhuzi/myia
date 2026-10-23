// Ghidra inferred pseudocode; requested=0x46a80c0
// entry=046a80c0 end=046a811b

undefined * FUN_046a80c0(void)

{
  int iVar1;
  
  if (((DAT_0a460498 & 1) == 0) && (iVar1 = ___cxa_guard_acquire(&DAT_0a460498), iVar1 != 0)) {
    FUN_046a8134(&DAT_0a4602f0);
    ___cxa_guard_release(&DAT_0a460498);
  }
  return &DAT_0a4602f0;
}


